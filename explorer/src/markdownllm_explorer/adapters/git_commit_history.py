"""Bounded, read-only Git history adapter."""

from __future__ import annotations

import os
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import BoundaryToken, CommitRecord, Page, RepositoryState

from .cursors import CursorCodec, CursorState
from .filesystem_catalogue import BoundaryRegistry


class GitCommitHistory:
    def __init__(self, registry: BoundaryRegistry, cursors: CursorCodec, limits: ExplorerLimits, git_executable: str | None = None) -> None:
        discovered = git_executable or shutil.which("git")
        self._git = str(Path(discovered).resolve(strict=True)) if discovered else None
        self._registry = registry
        self._cursors = cursors
        self._limits = limits

    def repository_state(self, token: BoundaryToken) -> RepositoryState:
        if not self._git:
            return RepositoryState("unavailable", issue="git_unavailable")
        boundary = self._registry.by_token(token)
        try:
            self._validate_store(boundary.root)
            head = self._optional(boundary.root, ["rev-parse", "--verify", "HEAD"])
            if not head:
                return RepositoryState("unborn", branch=self._optional(boundary.root, ["symbolic-ref", "--short", "HEAD"]))
            branch = self._optional(boundary.root, ["symbolic-ref", "--short", "HEAD"])
            dirty = bool(self._run(boundary.root, ["status", "--porcelain=v1", "--untracked-files=no"]).strip())
            return RepositoryState("repository", head, branch or None, dirty)
        except ExplorerError as error:
            kind = "external-store" if error.code == "git_store_external" else "unavailable"
            return RepositoryState(kind, issue=error.code)

    def commits(self, token: BoundaryToken, cursor: str | None) -> Page[CommitRecord]:
        if not self._git:
            raise ExplorerError("git_unavailable")
        boundary = self._registry.by_token(token)
        self._validate_store(boundary.root)
        head = self._optional(boundary.root, ["rev-parse", "--verify", "HEAD"])
        if not head:
            return Page((), None, False, datetime.now(timezone.utc).isoformat())
        state = self._cursors.decode(cursor, operation="commits", source=boundary.source.id.value, context="HEAD")
        pinned_head = state.revision or head
        if state.revision and state.revision != head:
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

    def _run(self, root: Path, arguments: list[str]) -> str:
        if not self._git:
            raise ExplorerError("git_unavailable")
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
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_SYSTEM": os.devnull,
                "LC_ALL": "C.UTF-8",
            }
        )
        command = [
            self._git, "-c", f"safe.directory={root}", "-c", "core.pager=cat", "-c", "diff.external=",
            "-c", "filter.lfs.smudge=", "-c", "filter.lfs.process=", *arguments,
        ]
        try:
            result = subprocess.run(
                command, cwd=root, env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, timeout=self._limits.git_seconds, check=False,
            )
        except subprocess.TimeoutExpired:
            raise ExplorerError("git_timeout") from None
        except OSError:
            raise ExplorerError("git_unavailable") from None
        if len(result.stdout) > self._limits.git_output_bytes or len(result.stderr) > self._limits.git_output_bytes:
            raise ExplorerError("git_unavailable")
        if result.returncode:
            raise ExplorerError("git_unavailable")
        try:
            return result.stdout.decode("utf-8")
        except UnicodeDecodeError:
            return result.stdout.decode("utf-8", errors="replace")


def _inside(candidate: Path, root: Path) -> bool:
    try:
        candidate.relative_to(root.resolve(strict=True))
        return True
    except ValueError:
        return False
