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
from markdownllm_explorer.core.models import BoundaryToken, CommitRecord, Page, RepositoryState

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
            ["log", query_revision, "--topo-order", f"--skip={state.offset}", f"--max-count={count}", "--format=%H%x00%s%x00%an%x00%aI%x00%x1e"],
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

    def _run(self, root: Path, arguments: list[str]) -> str:
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
                self._limits.git_seconds, self._limits.git_output_bytes,
            )
        )
        if result.returncode:
            raise ExplorerError("git_unavailable")
        try:
            return result.output.decode("utf-8")
        except UnicodeDecodeError:
            return result.output.decode("utf-8", errors="replace")


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
            and arguments[5] == "--format=%H%x00%s%x00%an%x00%aI%x00%x1e"
        )
    return False
