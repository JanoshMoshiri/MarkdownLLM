"""Bounded, read-only Git history adapter."""

from __future__ import annotations

import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import BoundaryToken, CommitRecord, Page, RepositoryState

from .cursors import CursorCodec, CursorState
from .filesystem_catalogue import BoundaryRegistry
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
        head = head_hint or self._optional(boundary.root, ["rev-parse", "--verify", "HEAD"])
        if not head:
            return Page((), None, False, datetime.now(timezone.utc).isoformat())
        state = self._cursors.decode(cursor, operation="commits", source=boundary.source.id.value, context="HEAD")
        pinned_head = state.revision or head
        if state.revision and not self._commit_exists(boundary.root, pinned_head):
            raise ExplorerError("source_changed")
        count = self._limits.commit_page + 1
        output = self._run(
            boundary.root,
            ["log", pinned_head, "--topo-order", f"--skip={state.offset}", f"--max-count={count}", "--format=%H%x00%s%x00%an%x00%aI%x00%x1e"],
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
            next_cursor = self._cursors.encode(CursorState("commits", boundary.source.id.value, "HEAD", state.offset + self._limits.commit_page, pinned_head))
        return Page(tuple(records), next_cursor, False, datetime.now(timezone.utc).isoformat())

    def snapshot(self, token: BoundaryToken, cursor: str | None) -> tuple[RepositoryState, Page[CommitRecord]]:
        empty = Page((), None, False, datetime.now(timezone.utc).isoformat())
        if not self._git:
            return RepositoryState("unavailable", issue="git_unavailable"), empty
        boundary = self._registry.by_token(token)
        try:
            self._validate_store(boundary.root)
            repository = self._state_from_status(boundary.root)
            commits = self.commits(token, cursor, repository.head_sha, validate_store=False) if repository.kind == "repository" else empty
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
        if not (root / ".git").exists():
            raise ExplorerError("git_unavailable")
        values = self._run(root, ["rev-parse", "--path-format=absolute", "--show-toplevel", "--git-dir", "--git-common-dir"]).splitlines()
        if len(values) < 3:
            raise ExplorerError("git_unavailable")
        try:
            top = Path(values[0]).resolve(strict=True)
            git_dir = Path(values[1]).resolve(strict=True)
            common = Path(values[2]).resolve(strict=True)
        except OSError:
            raise ExplorerError("git_unavailable") from None
        if top != root.resolve(strict=True) or not _inside(git_dir, root) or not _inside(common, root):
            raise ExplorerError("git_store_external")

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
            re.fullmatch(r"[0-9a-f]{40}", arguments[1])
            and arguments[2] == "--topo-order"
            and re.fullmatch(r"--skip=\d+", arguments[3])
            and re.fullmatch(r"--max-count=\d+", arguments[4])
            and arguments[5] == "--format=%H%x00%s%x00%an%x00%aI%x00%x1e"
        )
    return False
