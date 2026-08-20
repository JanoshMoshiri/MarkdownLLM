"""Logical, Git-aware read views over one repository.

The deterministic floor has three legitimate sources of bytes:

* the worktree, where an operator is drafting;
* the index tree, which is the exact next-commit candidate; and
* an immutable commit, which is the only stable provenance boundary.

``RepositoryView`` names those sources without becoming a virtual filesystem.
It only lists repository-relative logical paths and reads their bytes.  Git
plumbing stays here so validators and serving code do not each invent subtly
different index/commit semantics.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path, PurePosixPath


class RepositoryViewError(RuntimeError):
    """The requested repository view could not be constructed or read."""


class RepositoryHeadMoved(RepositoryViewError):
    """A significant read's immutable base is no longer repository HEAD."""

    def __init__(self, expected: str, actual: str):
        super().__init__(
            f"repository HEAD moved during the operation: expected {expected}, "
            f"now {actual}; reconcile before writing"
        )
        self.expected = expected
        self.actual = actual


class RepositoryViewMode(str, Enum):
    WORKTREE = "worktree"
    INDEX = "index"
    COMMIT = "commit"


_FULL_OBJECT_ID = re.compile(r"^(?:[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$")
FROZEN_INDEX_TREE_ENV = "MDLLM_FROZEN_INDEX_TREE"
FROZEN_INDEX_ROOT_ENV = "MDLLM_FROZEN_INDEX_ROOT"


def _git(root: Path, *args: str, text: bool = False) -> bytes | str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True,
            text=text,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = ""
        if isinstance(exc, subprocess.CalledProcessError):
            stderr = exc.stderr or b""
            if isinstance(stderr, bytes):
                stderr = stderr.decode("utf-8", errors="replace")
            detail = str(stderr).strip()
        suffix = f": {detail}" if detail else ""
        raise RepositoryViewError(
            f"git {' '.join(args)} failed in {root}{suffix}"
        ) from exc
    return result.stdout


def _logical(path: str | Path | PurePosixPath) -> PurePosixPath:
    raw = str(path).replace("\\", "/")
    logical = PurePosixPath(raw)
    if logical.is_absolute() or not logical.parts or logical == PurePosixPath("."):
        raise ValueError(f"logical repository path must be relative: {path!r}")
    if any(part in ("", ".", "..") for part in logical.parts):
        raise ValueError(f"logical repository path escapes its repository: {path!r}")
    return logical


def _ensure_repository_root(root: Path) -> None:
    """Refuse to silently bind a nested corpus to an ancestor repository."""
    top = str(_git(root, "rev-parse", "--show-toplevel", text=True)).strip()
    if not top or Path(top).resolve() != root:
        raise RepositoryViewError(
            f"repository view root must be the Git worktree root: {root}"
        )


@dataclass(frozen=True)
class RepositoryView:
    """One named source of repository bytes.

    Construct views through :meth:`worktree`, :meth:`index`, or :meth:`commit`.
    Index construction freezes the current index as a Git tree object, so a
    caller cannot accidentally validate half of one candidate and half of a
    later one.  Commit construction resolves any accepted revision immediately
    and stores only its full object id.
    """

    root: Path
    mode: RepositoryViewMode
    commit_sha: str | None = None
    tree_sha: str | None = None

    @classmethod
    def worktree(cls, root: Path) -> "RepositoryView":
        return cls(Path(root).resolve(), RepositoryViewMode.WORKTREE)

    @classmethod
    def index(cls, root: Path) -> "RepositoryView":
        resolved = Path(root).resolve()
        _ensure_repository_root(resolved)
        pinned_tree = os.environ.get(FROZEN_INDEX_TREE_ENV)
        pinned_root = os.environ.get(FROZEN_INDEX_ROOT_ENV)
        if pinned_tree is not None or pinned_root is not None:
            if not pinned_tree or not pinned_root:
                raise RepositoryViewError(
                    "incomplete frozen-index environment: tree and root are "
                    "both required")
            if Path(pinned_root).resolve() != resolved:
                raise RepositoryViewError(
                    "frozen-index root does not match the requested repository")
            tree = pinned_tree.strip()
            if not _FULL_OBJECT_ID.fullmatch(tree):
                raise RepositoryViewError(
                    f"frozen index contains a non-object id: {tree!r}")
            kind = str(_git(resolved, "cat-file", "-t", tree, text=True)).strip()
            if kind != "tree":
                raise RepositoryViewError(
                    f"frozen index object is {kind!r}, not a tree")
        else:
            tree = str(_git(resolved, "write-tree", text=True)).strip()
        if not _FULL_OBJECT_ID.fullmatch(tree):
            raise RepositoryViewError(f"git write-tree returned a non-object id: {tree!r}")
        return cls(resolved, RepositoryViewMode.INDEX, tree_sha=tree.lower())

    @classmethod
    def commit(cls, root: Path, revision: str = "HEAD") -> "RepositoryView":
        resolved = Path(root).resolve()
        _ensure_repository_root(resolved)
        # ``--end-of-options`` prevents a repository-controlled or caller-
        # supplied revision beginning with '-' from becoming a Git option.
        sha = str(_git(
            resolved, "rev-parse", "--verify", "--end-of-options",
            f"{revision}^{{commit}}", text=True,
        )).strip()
        if not _FULL_OBJECT_ID.fullmatch(sha):
            raise RepositoryViewError(f"git rev-parse returned a non-commit id: {sha!r}")
        return cls(resolved, RepositoryViewMode.COMMIT, commit_sha=sha.lower())

    @property
    def identifier(self) -> str:
        if self.mode is RepositoryViewMode.COMMIT:
            return f"commit:{self.commit_sha}"
        if self.mode is RepositoryViewMode.INDEX:
            return f"index:{self.tree_sha}"
        return "worktree"

    @property
    def immutable(self) -> bool:
        # The index is frozen to a write-tree result at construction time.
        return self.mode is not RepositoryViewMode.WORKTREE

    def _treeish(self) -> str:
        if self.mode is RepositoryViewMode.COMMIT and self.commit_sha:
            return self.commit_sha
        if self.mode is RepositoryViewMode.INDEX and self.tree_sha:
            return self.tree_sha
        raise RepositoryViewError("the worktree has no Git tree object")

    def _worktree_path(self, logical: PurePosixPath) -> Path:
        candidate = self.root.joinpath(*logical.parts)
        # Resolving also closes the symlink-file escape that a lexical
        # ``relative_to`` check would miss.
        resolved = candidate.resolve(strict=False)
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise RepositoryViewError(
                f"worktree path escapes repository root: {logical.as_posix()}"
            ) from exc
        return resolved

    def list_paths(self, suffix: str | None = None) -> tuple[PurePosixPath, ...]:
        """List file paths in this view, sorted by logical POSIX path."""
        if self.mode is RepositoryViewMode.WORKTREE:
            paths: list[PurePosixPath] = []
            for path in self.root.rglob("*"):
                if not path.is_file():
                    continue
                logical = PurePosixPath(path.relative_to(self.root).as_posix())
                if suffix is None or logical.name.endswith(suffix):
                    paths.append(logical)
            return tuple(sorted(paths, key=lambda p: p.as_posix()))

        raw = _git(self.root, "ls-tree", "-r", "-z", "--name-only", self._treeish())
        assert isinstance(raw, bytes)
        paths = []
        for item in raw.split(b"\0"):
            if not item:
                continue
            logical = _logical(item.decode("utf-8", errors="surrogateescape"))
            if suffix is None or logical.name.endswith(suffix):
                paths.append(logical)
        return tuple(sorted(paths, key=lambda p: p.as_posix()))

    def iter_paths(self, suffix: str | None = None):
        """Iterator spelling for callers that do not need the materialized tuple."""
        return iter(self.list_paths(suffix=suffix))

    def _blob_id(self, logical: PurePosixPath) -> str:
        raw = _git(
            self.root, "ls-tree", "-z", self._treeish(), "--", logical.as_posix()
        )
        assert isinstance(raw, bytes)
        entries = [entry for entry in raw.split(b"\0") if entry]
        for entry in entries:
            header, sep, name = entry.partition(b"\t")
            if not sep:
                continue
            decoded = name.decode("utf-8", errors="surrogateescape")
            if decoded != logical.as_posix():
                continue
            fields = header.split()
            if len(fields) != 3 or fields[1] != b"blob":
                raise FileNotFoundError(logical.as_posix())
            oid = fields[2].decode("ascii")
            if not _FULL_OBJECT_ID.fullmatch(oid):
                raise RepositoryViewError(f"Git returned a non-blob id for {logical}: {oid!r}")
            return oid
        raise FileNotFoundError(logical.as_posix())

    def read_bytes(self, path: str | Path | PurePosixPath) -> bytes:
        logical = _logical(path)
        if self.mode is RepositoryViewMode.WORKTREE:
            candidate = self._worktree_path(logical)
            if not candidate.is_file():
                raise FileNotFoundError(logical.as_posix())
            return candidate.read_bytes()
        raw = _git(self.root, "cat-file", "blob", self._blob_id(logical))
        assert isinstance(raw, bytes)
        return raw

    def read_text(
        self, path: str | Path | PurePosixPath, encoding: str = "utf-8"
    ) -> str:
        # Decode bytes directly rather than using universal-newline text I/O;
        # callers that compare against a Git blob must retain exact CRLF bytes.
        return self.read_bytes(path).decode(encoding)

    def exists(self, path: str | Path | PurePosixPath) -> bool:
        try:
            self.read_bytes(path)
            return True
        except FileNotFoundError:
            return False

    def last_commit_for(self, path: str | Path | PurePosixPath) -> str | None:
        """Return the full last-touch commit for ``path`` in this view's history."""
        logical = _logical(path)
        at = self.commit_sha if self.mode is RepositoryViewMode.COMMIT else "HEAD"
        try:
            out = str(_git(
                self.root, "log", "-1", "--format=%H", str(at), "--",
                logical.as_posix(), text=True,
            )).strip()
        except RepositoryViewError:
            return None
        return out.lower() if _FULL_OBJECT_ID.fullmatch(out) else None

    def assert_head_unchanged(self) -> str:
        """Optimistic concurrency check for a commit-pinned significant read.

        Agents can pin a long read with ``RepositoryView.commit(root)`` and
        call this immediately before applying conclusions.  HEAD movement is
        a reconciliation event, never permission to write against a mixed
        snapshot.
        """
        if self.mode is not RepositoryViewMode.COMMIT or not self.commit_sha:
            raise RepositoryViewError(
                "HEAD currency can only be checked for an immutable commit view"
            )
        actual = RepositoryView.commit(self.root).commit_sha
        assert actual is not None
        if actual != self.commit_sha:
            raise RepositoryHeadMoved(self.commit_sha, actual)
        return actual
