"""Bounded, read-only Git history adapter."""

from __future__ import annotations

import os
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import (
    BoundaryToken, CommitDetail, CommitFile, CommitRecord, HistoricalDocument, Page, RelativePath, RepositoryState,
)

from .cursors import CursorCodec, CursorState
from .filesystem_catalogue import BoundaryRegistry, _is_reparse
from .process_runner import BoundedProcessRunner, ProcessRequest


class GitCommitHistory:
    def __init__(
        self, registry: BoundaryRegistry, cursors: CursorCodec, limits: ExplorerLimits,
        git_executable: str | None = None, runner: BoundedProcessRunner | None = None,
    ) -> None:
        self._git = git_executable
        self._registry = registry
        self._cursors = cursors
        self._limits = limits
        self._runner = runner or BoundedProcessRunner()

    def repository_state(self, token: BoundaryToken) -> RepositoryState:
        if not self._git:
            return RepositoryState("unavailable", issue="git_unavailable")
        boundary = self._registry.by_token(token)
        try:
            self._validate_store(boundary.root)
            return self._state_from_status(boundary.root)
        except ExplorerError as error:
            kind = "external-store" if error.code == "git_store_external" else "unavailable"
            return RepositoryState(kind, issue=error.code)

    def commits(self, token: BoundaryToken, cursor: str | None, head_hint: str | None = None, *, validate_store: bool = True) -> Page[CommitRecord]:
        if not self._git:
            raise ExplorerError("git_unavailable")
        boundary = self._registry.by_token(token)
        if validate_store:
            self._validate_store(boundary.root)
        state = self._cursors.decode(cursor, operation="commits", source=boundary.source.id.value, context="HEAD")
        if state.revision:
            if not self._commit_exists(boundary.root, state.revision):
                raise ExplorerError("source_changed")
            pinned_head = state.revision
        else:
            pinned_head = head_hint or self._optional(boundary.root, ["rev-parse", "--verify", "HEAD"])
            if not pinned_head:
                return Page((), None, False, datetime.now(timezone.utc).isoformat())
        return self._commit_page(boundary.root, boundary.source.id.value, state, pinned_head, pinned_head)

    def _commit_page(
        self,
        root: Path,
        source_id: str,
        state: CursorState,
        query_revision: str,
        pinned_head: str | None,
    ) -> Page[CommitRecord]:
        count = self._limits.commit_page + 1
        output = self._run(
            root,
            ["log", query_revision, "--topo-order", f"--skip={state.offset}", f"--max-count={count}", _COMMIT_FORMAT],
        )
        records: list[CommitRecord] = []
        for raw_record in output.split("\x1e"):
            fields = raw_record.strip("\r\n\x00").split("\x00")
            if len(fields) >= 4 and len(fields[0]) == 40:
                records.append(CommitRecord(fields[0], fields[1], fields[2], fields[3]))
        more = len(records) > self._limits.commit_page
        records = records[: self._limits.commit_page]
        next_cursor = None
        if more:
            effective_head = pinned_head or (records[0].sha if records else "")
            if not re.fullmatch(r"[0-9a-f]{40}", effective_head):
                raise ExplorerError("source_changed")
            next_cursor = self._cursors.encode(CursorState("commits", source_id, "HEAD", state.offset + self._limits.commit_page, effective_head))
        return Page(tuple(records), next_cursor, False, datetime.now(timezone.utc).isoformat())

    def snapshot(self, token: BoundaryToken, cursor: str | None) -> tuple[RepositoryState, Page[CommitRecord]]:
        empty = Page((), None, False, datetime.now(timezone.utc).isoformat())
        if not self._git:
            return RepositoryState("unavailable", issue="git_unavailable"), empty
        boundary = self._registry.by_token(token)
        try:
            self._validate_store(boundary.root)
            if cursor:
                commit_reader = lambda: self.commits(token, cursor, validate_store=False)
            else:
                state = CursorState("commits", boundary.source.id.value, "HEAD", 0, "")
                commit_reader = lambda: self._commit_page(
                    boundary.root, boundary.source.id.value, state, "HEAD", None
                )
            with ThreadPoolExecutor(max_workers=2, thread_name_prefix="explorer-git-snapshot") as executor:
                repository_future = executor.submit(self._state_from_status, boundary.root)
                commits_future = executor.submit(commit_reader)
                repository = repository_future.result()
                try:
                    commits = commits_future.result()
                except ExplorerError:
                    if repository.kind == "unborn":
                        commits = empty
                    else:
                        raise
            if repository.kind != "repository":
                commits = empty
            elif not cursor and (
                not commits.items or commits.items[0].sha != repository.head_sha
            ):
                # HEAD moved between the concurrent reads. Re-run against the
                # full SHA reported by status so repository metadata and page
                # identity remain one coherent snapshot.
                commits = self.commits(
                    token, None, repository.head_sha, validate_store=False
                )
            return repository, commits
        except ExplorerError as error:
            kind = "external-store" if error.code == "git_store_external" else "unavailable"
            return RepositoryState(kind, issue=error.code), empty

    def detail(self, token: BoundaryToken, sha: str) -> CommitDetail:
        """The paths one commit touched, against its first parent.

        The comparison is an explicit two-tree diff between the first parent and
        the commit, because `diff-tree --first-parent` on a *merge* prints
        nothing at all: a merge commit reported zero changed files until this
        was corrected. A commit with no parent is compared against the empty
        tree with `--root` instead.

        Renames are off, so a rename reads as a delete beside an add. That is
        the honest shape here: this view never renders removed content, so a
        rename presented as one row would claim a continuity the reader cannot
        open.
        """
        root = self._prepared_root(token, sha)
        header = self._run(root, _detail_arguments(sha))
        record, parents = self._detail_record(header)
        parent = parents[0] if parents else None
        output = self._run(root, _raw_arguments(parent, sha))
        files: list[CommitFile] = []
        partial = False
        for mode, status, raw in _raw_entries(output):
            if len(files) >= self._limits.commit_files:
                partial = True
                break
            try:
                relative = RelativePath.parse(raw)
            except ExplorerError:
                # A path this source cannot even express is not shown; it is
                # never handed onward as a git argument.
                continue
            files.append(CommitFile(relative, _CHANGE.get(status[:1], "modified"), regular=mode in _REGULAR_MODES))
        files.sort(key=lambda item: (item.path.value.casefold(), item.path.value))
        return CommitDetail(record.sha, record.subject, record.author_name, record.authored_at, tuple(files), partial)

    def historical(self, token: BoundaryToken, sha: str, path: RelativePath) -> HistoricalDocument:
        """A file's bytes at one commit, with that commit's added line ranges.

        The caller has already decided this source admits the path.  The size
        is checked before the content is fetched so an oversized blob is
        refused by the same limit as a live read rather than by the process
        runner's output ceiling.
        """
        boundary = self._registry.by_token(token)
        root = self._prepared_root(token, sha)
        spec = f"{sha}:{path.value}"
        size = self._object_size(root, spec)
        if size is None:
            raise ExplorerError("file_not_found")
        if size > self._limits.file_bytes:
            raise ExplorerError("file_too_large")
        if self._entry_mode(root, sha, path.value) not in _REGULAR_MODES:
            # A symlink or gitlink entry carries a target, not content. The live
            # reader refuses to follow one, and this route must not become the
            # way to read what it points at.
            raise ExplorerError("path_type_changed")
        payload = self._run_bytes(root, ["cat-file", "blob", spec])
        if len(payload) != size:
            # The runner merges stderr into stdout, so a warning git prints on a
            # successful read would otherwise be served as file content. The
            # size git already reported is the check that catches it.
            raise ExplorerError("source_changed")
        if b"\x00" in payload:
            raise ExplorerError("binary_unsupported")
        try:
            text = payload.decode("utf-8-sig")
        except UnicodeDecodeError:
            raise ExplorerError("encoding_unsupported") from None
        ranges, ranges_known = self._added_lines(root, sha, path)
        return HistoricalDocument(boundary.source.id, path, sha, text, ranges, len(payload), ranges_known)

    def _added_lines(self, root: Path, sha: str, path: RelativePath) -> tuple[tuple[tuple[int, int], ...], bool]:
        """Which lines this commit put on its own side of the file.

        A patch is not a payload: it is read for its hunk headers and discarded,
        and it is roughly twice the size of the file because it carries both
        sides. Budgeting it like a response body made a 565 KB file — well
        inside the documented 1 MiB read limit — fail with `git_unavailable`,
        blaming git for a ceiling of ours. It gets its own, larger budget, and
        beyond that the file is still served: only the marking is unavailable,
        which is the proportionate loss.
        """
        parent = self._first_parent(root, sha)
        try:
            diff = self._run(
                root,
                _added_lines_arguments(parent, sha, path.value),
                output_limit=self._limits.diff_output_bytes,
            )
        except ExplorerError:
            return (), False
        return _added_ranges(diff), True

    def _first_parent(self, root: Path, sha: str) -> str | None:
        record, parents = self._detail_record(self._run(root, _detail_arguments(sha)))
        return parents[0] if parents else None

    def _prepared_root(self, token: BoundaryToken, sha: str) -> Path:
        if not self._git:
            raise ExplorerError("git_unavailable")
        if not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ExplorerError("invalid_request")
        boundary = self._registry.by_token(token)
        self._validate_store(boundary.root)
        if not self._commit_exists(boundary.root, sha):
            raise ExplorerError("source_changed")
        return boundary.root

    def _entry_mode(self, root: Path, sha: str, path: str) -> str | None:
        record = self._run(root, _entry_arguments(sha, path)).split("\x00")[0]
        head = record.split(" ", 1)[0].strip()
        return head if re.fullmatch(r"[0-7]{6}", head) else None

    def _object_size(self, root: Path, spec: str) -> int | None:
        try:
            return int(self._run(root, ["cat-file", "-s", spec]).strip())
        except ExplorerError as error:
            if error.code == "git_unavailable":
                return None
            raise
        except ValueError:
            return None

    @staticmethod
    def _detail_record(output: str) -> tuple[CommitRecord, tuple[str, ...]]:
        for raw_record in output.split("\x1e"):
            # Only newlines are stripped. A root commit's parent field is empty,
            # and stripping NUL from the right would eat it, leaving the record
            # one field short and the commit unreadable.
            fields = raw_record.strip("\r\n").lstrip("\x00").split("\x00")
            if len(fields) >= 5 and len(fields[0]) == 40:
                parents = tuple(
                    item for item in fields[4].split(" ") if re.fullmatch(r"[0-9a-f]{40}", item)
                )
                return CommitRecord(fields[0], fields[1], fields[2], fields[3]), parents
        raise ExplorerError("source_changed")

    def _state_from_status(self, root: Path) -> RepositoryState:
        output = self._run(root, ["status", "--porcelain=v2", "--branch", "--untracked-files=no"])
        head = branch = None
        dirty = False
        for line in output.splitlines():
            if line.startswith("# branch.oid "):
                candidate = line.removeprefix("# branch.oid ").strip()
                head = candidate if re.fullmatch(r"[0-9a-f]{40}", candidate) else None
            elif line.startswith("# branch.head "):
                candidate = line.removeprefix("# branch.head ").strip()
                branch = None if candidate == "(detached)" else candidate
            elif line and not line.startswith("# "):
                dirty = True
        return RepositoryState("repository" if head else "unborn", head, branch, dirty if head else None)

    def _validate_store(self, root: Path) -> None:
        git_entry = root / ".git"
        if not git_entry.exists():
            raise ExplorerError("git_unavailable")
        # A source-owned ordinary repository has a real .git directory at its
        # registered root. Worktree pointer files and reparse points can lead
        # outside that source and are intentionally unavailable in v1.
        if _is_reparse(git_entry) or not git_entry.is_dir():
            raise ExplorerError("git_store_external")
        try:
            registered_root = root.resolve(strict=True)
            git_dir = git_entry.resolve(strict=True)
        except OSError:
            raise ExplorerError("git_unavailable") from None
        if not _inside(git_dir, registered_root):
            raise ExplorerError("git_store_external")

        common = git_dir
        common_pointer = git_dir / "commondir"
        if common_pointer.exists():
            try:
                if (
                    _is_reparse(common_pointer)
                    or not common_pointer.is_file()
                    or common_pointer.stat().st_size > 64 * 1024
                ):
                    raise ExplorerError("git_store_external")
                lines = common_pointer.read_text(encoding="utf-8").splitlines()
            except (OSError, UnicodeError):
                raise ExplorerError("git_store_external") from None
            if len(lines) != 1 or not lines[0].strip():
                raise ExplorerError("git_store_external")
            candidate = Path(lines[0].strip())
            if not candidate.is_absolute():
                candidate = git_dir / candidate
            try:
                common = candidate.resolve(strict=True)
            except OSError:
                raise ExplorerError("git_store_external") from None
        if _is_reparse(common) or not common.is_dir() or not _inside(common, registered_root):
            raise ExplorerError("git_store_external")
        self._validate_object_store(common / "objects", root, set(), 0)

    def _validate_object_store(self, store: Path, root: Path, seen: set[Path], depth: int) -> None:
        """Validate the effective object database and every local alternate.

        Git resolves relative alternates from the object database containing the
        ``info/alternates`` file.  We mirror that rule without asking repository
        configuration to execute anything, bound the graph, and fail closed on
        HTTP/promisor stores because their complete object set is not owned by
        the selected source snapshot.
        """
        if depth > 8 or len(seen) >= 32:
            raise ExplorerError("git_store_external")
        try:
            resolved = store.resolve(strict=True)
        except OSError:
            raise ExplorerError("git_unavailable") from None
        if _is_reparse(store) or not resolved.is_dir() or not _inside(resolved, root):
            raise ExplorerError("git_store_external")
        if resolved in seen:
            return
        seen.add(resolved)
        if any((resolved / "pack").glob("*.promisor")):
            raise ExplorerError("git_store_external")
        http_alternates = resolved / "info" / "http-alternates"
        if _nonempty_bounded_file(http_alternates):
            raise ExplorerError("git_store_external")
        alternates = resolved / "info" / "alternates"
        if not alternates.exists():
            return
        try:
            if alternates.stat().st_size > 64 * 1024:
                raise ExplorerError("git_store_external")
            lines = alternates.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeError):
            raise ExplorerError("git_store_external") from None
        if len(lines) > 32:
            raise ExplorerError("git_store_external")
        for value in lines:
            if not value.strip():
                continue
            candidate = Path(value.strip())
            if not candidate.is_absolute():
                candidate = resolved / candidate
            self._validate_object_store(candidate, root, seen, depth + 1)

    def _optional(self, root: Path, arguments: list[str]) -> str:
        try:
            return self._run(root, arguments).strip()
        except ExplorerError as error:
            if error.code == "git_unavailable":
                return ""
            raise

    def _commit_exists(self, root: Path, revision: str) -> bool:
        try:
            self._run(root, ["cat-file", "-e", f"{revision}^{{commit}}"])
            return True
        except ExplorerError as error:
            if error.code == "git_unavailable":
                return False
            raise

    def _run_bytes(self, root: Path, arguments: list[str], output_limit: int | None = None) -> bytes:
        if not self._git:
            raise ExplorerError("git_unavailable")
        if not _allowed_arguments(arguments):
            raise ExplorerError("internal_error", detail="git argument template rejected")
        environment: dict[str, str] = {}
        for name in ("SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP"):
            if value := os.environ.get(name):
                environment[name] = value
        environment.update(
            {
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_NO_LAZY_FETCH": "1",
                "GIT_PAGER": "cat",
                "PAGER": "cat",
                "GIT_EDITOR": "true",
                "GIT_SEQUENCE_EDITOR": "true",
                "GIT_EXTERNAL_DIFF": "",
                "GIT_NO_REPLACE_OBJECTS": "1",
                # A path is a path, never a glob. Without this a filename
                # containing [ ] * or ? is read by git as a pattern, and the
                # ranges returned describe whichever other files it matched.
                "GIT_LITERAL_PATHSPECS": "1",
                "GIT_ASKPASS": "",
                "SSH_ASKPASS": "",
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "LC_ALL": "C.UTF-8",
            }
        )
        fixed = (
            "-c", f"safe.directory={root}",
            "-c", f"core.hooksPath={os.devnull}",
            "-c", "core.pager=cat",
            "-c", "core.fsmonitor=false",
            "-c", "core.untrackedCache=false",
            "-c", "core.preloadIndex=false",
            "-c", "diff.external=",
            "-c", "credential.helper=",
            "-c", "core.alternateRefsCommand=",
            "-c", "filter.lfs.smudge=",
            "-c", "filter.lfs.process=",
            "-c", "protocol.file.allow=never",
        )
        result = self._runner.run(
            ProcessRequest(
                self._git, (*fixed, *arguments), root, environment,
                self._limits.git_seconds, output_limit or self._limits.git_output_bytes,
            )
        )
        if result.returncode:
            raise ExplorerError("git_unavailable")
        return result.output

    def _run(self, root: Path, arguments: list[str], output_limit: int | None = None) -> str:
        payload = self._run_bytes(root, arguments, output_limit)
        try:
            return payload.decode("utf-8")
        except UnicodeDecodeError:
            return payload.decode("utf-8", errors="replace")


def resolve_trusted_git(source_root: Path) -> str | None:
    discovered = shutil.which("git")
    if not discovered:
        return None
    try:
        candidate = Path(discovered).resolve(strict=True)
        if not candidate.is_file() or candidate.is_symlink():
            return None
        candidate.relative_to(source_root.resolve(strict=True))
        return None
    except ValueError:
        return str(candidate)
    except OSError:
        return None


def _inside(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root.resolve(strict=True))
        return True
    except ValueError:
        return False


def _nonempty_bounded_file(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        if not path.is_file() or path.stat().st_size > 64 * 1024:
            raise ExplorerError("git_store_external")
        return bool(path.read_bytes().strip())
    except OSError:
        raise ExplorerError("git_store_external") from None


_CHANGE = {"A": "added", "D": "deleted"}

# Only an ordinary file has content this reader can serve. A symlink (120000)
# or a gitlink (160000) entry carries a path or a commit id, and serving one as
# a document would publish a target the live reader refuses to follow.
_REGULAR_MODES = {"100644", "100755"}

_COMMIT_FORMAT = "--format=%H%x00%s%x00%an%x00%aI%x00%x1e"
# The detail read needs the parent too, because the comparison is an explicit
# two-tree diff rather than --first-parent, which prints nothing at all for a
# merge commit.
_DETAIL_FORMAT = "--format=%H%x00%s%x00%an%x00%aI%x00%P%x00%x1e"

# --raw rather than --name-status: the raw record carries the destination file
# mode, which is what distinguishes an ordinary file from a symlink or gitlink.
_RAW_FLAGS = ["--no-commit-id", "-r", "--no-renames", "-z", "--raw"]
_ADDED_LINES_FLAGS = ["-p", "--unified=0", "--no-commit-id", "--no-renames", "-r"]

# --unified=0 makes every hunk header describe exactly the lines this commit put
# on its own side of the file, so the added ranges are read from the headers
# alone and no removed line is ever parsed, stored or returned.
_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


def _revision_pair(parent: str | None, sha: str) -> list[str]:
    """Compare against the first parent, or against the empty tree at a root."""
    return [parent, sha] if parent else ["--root", sha]


def _detail_arguments(sha: str) -> list[str]:
    return ["log", sha, "--topo-order", "--skip=0", "--max-count=1", _DETAIL_FORMAT]


def _entry_arguments(sha: str, path: str) -> list[str]:
    return ["ls-tree", "-z", sha, "--", path]


def _raw_arguments(parent: str | None, sha: str) -> list[str]:
    return ["diff-tree", *_RAW_FLAGS, *_revision_pair(parent, sha)]


def _added_lines_arguments(parent: str | None, sha: str, path: str) -> list[str]:
    return ["diff-tree", *_ADDED_LINES_FLAGS, *_revision_pair(parent, sha), "--", path]


def _raw_entries(output: str):
    """Yield (destination mode, status, path) from `diff-tree --raw -z` records.

    Each record is `:<srcmode> <dstmode> <srcsha> <dstsha> <status>` followed by
    the path, both NUL-terminated.
    """
    fields = output.split("\x00")
    for index in range(0, len(fields) - 1, 2):
        meta, raw = fields[index].strip("\r\n"), fields[index + 1]
        if not meta.startswith(":") or not raw:
            continue
        parts = meta[1:].split(" ")
        if len(parts) < 5:
            continue
        yield parts[1], parts[4], raw


def _added_ranges(diff: str) -> tuple[tuple[int, int], ...]:
    ranges: list[tuple[int, int]] = []
    for line in diff.splitlines():
        match = _HUNK.match(line)
        if not match:
            continue
        start = int(match.group(1))
        count = 1 if match.group(2) is None else int(match.group(2))
        if count:
            ranges.append((start, start + count - 1))
    return tuple(ranges)


def _is_tree_path(value: str) -> bool:
    """The independent path gate for arguments that carry one.

    Every path reaching here has already passed RelativePath.parse and source
    admission.  This gate does not trust that: it is the check that stops an
    option-looking, traversing or control-bearing path from ever becoming a
    git argument, and it is deliberately stricter than the parse it repeats.
    """
    if not value or len(value) > 1024 or value.startswith("-"):
        return False
    if any(character in value for character in ("\x00", "\\", ":")):
        return False
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in value):
        return False
    return all(part and part not in {".", ".."} for part in value.split("/"))


def _is_object_spec(value: str) -> bool:
    head, separator, path = value.partition(":")
    return bool(separator) and bool(re.fullmatch(r"[0-9a-f]{40}", head)) and _is_tree_path(path)


def _allowed_arguments(arguments: list[str]) -> bool:
    exact = {
        ("rev-parse", "--path-format=absolute", "--show-toplevel", "--git-dir", "--git-common-dir"),
        ("rev-parse", "--verify", "HEAD"),
        ("symbolic-ref", "--short", "HEAD"),
        ("status", "--porcelain=v2", "--untracked-files=no"),
        ("status", "--porcelain=v2", "--branch", "--untracked-files=no"),
    }
    value = tuple(arguments)
    if value in exact:
        return True
    if len(arguments) == 3 and arguments[:2] == ["cat-file", "-e"]:
        return bool(re.fullmatch(r"[0-9a-f]{40}\^\{commit\}", arguments[2]))
    if len(arguments) == 6 and arguments[0] == "log":
        return bool(
            (arguments[1] == "HEAD" or re.fullmatch(r"[0-9a-f]{40}", arguments[1]))
            and arguments[2] == "--topo-order"
            and re.fullmatch(r"--skip=\d+", arguments[3])
            and re.fullmatch(r"--max-count=\d+", arguments[4])
            and arguments[5] in {_COMMIT_FORMAT, _DETAIL_FORMAT}
        )
    if len(arguments) == 3 and arguments[0] == "cat-file" and arguments[1] in {"blob", "-s"}:
        return _is_object_spec(arguments[2])
    if len(arguments) == 5 and arguments[0] == "ls-tree":
        return (
            arguments[1] == "-z"
            and bool(re.fullmatch(r"[0-9a-f]{40}", arguments[2]))
            and arguments[3] == "--"
            and _is_tree_path(arguments[4])
        )
    if arguments[:1] == ["diff-tree"]:
        if len(arguments) == len(_RAW_FLAGS) + 3:
            return arguments[1:-2] == _RAW_FLAGS and _is_revision_pair(arguments[-2:])
        if len(arguments) == len(_ADDED_LINES_FLAGS) + 5:
            return (
                arguments[1:-4] == _ADDED_LINES_FLAGS
                and _is_revision_pair(arguments[-4:-2])
                and arguments[-2] == "--"
                and _is_tree_path(arguments[-1])
            )
    return False


def _is_revision_pair(pair: list[str]) -> bool:
    """Either two full object ids, or the empty-tree marker and one id.

    The marker is admitted only in the leading position, so `--root` can never
    be smuggled in where a revision is expected.
    """
    left, right = pair
    if not re.fullmatch(r"[0-9a-f]{40}", right):
        return False
    return left == "--root" or bool(re.fullmatch(r"[0-9a-f]{40}", left))
