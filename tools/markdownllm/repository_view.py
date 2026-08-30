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
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path, PurePosixPath


# Directories the worktree walk never descends into: version-control internals,
# virtualenvs, and build/package caches. None can hold a domain thing, and the
# COMMIT arm of `list_paths` (git ls-tree) already excludes them — pruning is
# what makes the two modes return the same logical corpus.
_WALK_PRUNE = frozenset({
    ".git", ".venv", "venv", ".env", "node_modules", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".eggs",
    ".idea", ".vs", ".cache",
})


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


def _git(root: Path, *args: str, text: bool = False,
         input_bytes: bytes | None = None) -> bytes | str:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, check=True, capture_output=True,
            text=text, input=input_bytes,
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
    # Per-view caches (INDEX/COMMIT only): the tree's path->blob-oid map and
    # prefetched blob contents. Cache CONTENTS mutate; the field bindings stay
    # frozen, and both views name immutable trees so the caches cannot go
    # stale within a view's lifetime. Excluded from repr/eq by design.
    _tree_blobs: dict = field(default_factory=dict, repr=False, compare=False)
    _blob_bytes: dict = field(default_factory=dict, repr=False, compare=False)

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
            for dirpath, dirnames, filenames in os.walk(self.root):
                # Prune infrastructure the COMMIT arm cannot see either: it
                # lists `git ls-tree`, so `.git`, `.venv` and friends are
                # absent there by construction. An unpruned rglob made the
                # two modes disagree AND stat'd 37k files to find 172 things
                # — 36s at the framework root, which pushed the session-start
                # hook past its 60s budget (2026-08-20).
                dirnames[:] = [d for d in dirnames if d not in _WALK_PRUNE]
                for name in filenames:
                    if suffix is not None and not name.endswith(suffix):
                        continue
                    logical = PurePosixPath(
                        Path(dirpath, name).relative_to(self.root).as_posix())
                    paths.append(logical)
            return tuple(sorted(paths, key=lambda p: p.as_posix()))

        # The tree map already names every readable blob; deriving the listing
        # from it makes repeated list_paths calls free on an immutable view
        # (coherence alone called this ten times per run — ten ls-tree spawns
        # for one frozen tree).
        paths = [PurePosixPath(name) for name in self._tree_blob_map()
                 if suffix is None or name.endswith(suffix)]
        return tuple(sorted(paths, key=lambda p: p.as_posix()))

    def iter_paths(self, suffix: str | None = None):
        """Iterator spelling for callers that do not need the materialized tuple."""
        return iter(self.list_paths(suffix=suffix))

    def _tree_blob_map(self) -> dict[str, str]:
        """{logical posix path: blob oid} for the whole frozen tree, built
        from ONE `git ls-tree -r -z` walk and cached on the view.

        The per-path predecessor (`git ls-tree -z <tree> -- <path>` followed
        by `git cat-file blob <oid>`, per file) spawned two git processes for
        every thing read — at ~300ms per spawn on a cold Windows machine the
        pre-commit hook's index-view validate ran for minutes and timed out
        the very commits it was protecting."""
        cached = self._tree_blobs.get("map")
        if cached is not None:
            return cached
        raw = _git(self.root, "ls-tree", "-r", "-z", self._treeish())
        assert isinstance(raw, bytes)
        blobs: dict[str, str] = {}
        for entry in raw.split(b"\0"):
            if not entry:
                continue
            header, sep, name = entry.partition(b"\t")
            if not sep:
                continue
            fields = header.split()
            if len(fields) != 3 or fields[1] != b"blob":
                continue  # submodules/trees are not readable blobs — absent
            oid = fields[2].decode("ascii")
            if not _FULL_OBJECT_ID.fullmatch(oid):
                raise RepositoryViewError(
                    f"Git returned a non-blob id in tree listing: {oid!r}")
            blobs[name.decode("utf-8", errors="surrogateescape")] = oid
        self._tree_blobs["map"] = blobs
        return blobs

    def _blob_id(self, logical: PurePosixPath) -> str:
        oid = self._tree_blob_map().get(logical.as_posix())
        if oid is None:
            raise FileNotFoundError(logical.as_posix())
        return oid

    def prefetch(self, paths) -> None:
        """Batch-read the given logical paths' contents into the view cache.

        INDEX/COMMIT only (worktree reads are already cheap): one
        `git cat-file --batch` invocation fetches every requested blob in a
        single process, so a corpus scan costs two git spawns instead of two
        per file. Paths absent from the tree are skipped silently — the later
        per-path read raises the same FileNotFoundError it always did."""
        if self.mode is RepositoryViewMode.WORKTREE:
            return
        blob_map = self._tree_blob_map()
        wanted: list[str] = []
        for path in paths:
            oid = blob_map.get(_logical(path).as_posix())
            if oid is not None and oid not in self._blob_bytes:
                wanted.append(oid)
        if not wanted:
            return
        request = "".join(f"{oid}\n" for oid in dict.fromkeys(wanted))
        raw = _git(self.root, "cat-file", "--batch",
                   input_bytes=request.encode("ascii"))
        assert isinstance(raw, bytes)
        pos = 0
        while pos < len(raw):
            nl = raw.find(b"\n", pos)
            if nl < 0:
                break
            header = raw[pos:nl].split()
            pos = nl + 1
            if len(header) == 3 and header[1] != b"missing":
                oid = header[0].decode("ascii")
                size = int(header[2])
                self._blob_bytes[oid] = raw[pos:pos + size]
                pos += size + 1  # trailing LF after content
            # `<oid> missing` (2 fields) carries no body; loop continues

    def read_bytes(self, path: str | Path | PurePosixPath) -> bytes:
        logical = _logical(path)
        if self.mode is RepositoryViewMode.WORKTREE:
            candidate = self._worktree_path(logical)
            if not candidate.is_file():
                raise FileNotFoundError(logical.as_posix())
            return candidate.read_bytes()
        oid = self._blob_id(logical)
        cached = self._blob_bytes.get(oid)
        if cached is not None:
            return cached
        # First miss: batch-fetch every definition-surface blob in the tree
        # (.md/.yaml/.yml/.json — ~2.5MB at the framework root) rather than
        # paying one git spawn per scattered read. Coherence alone read 33
        # files one at a time through this path. One-shot, flagged, and the
        # missed file falls through to a single fetch if it is outside the
        # definition set.
        if "definitions-prefetched" not in self._tree_blobs:
            self._tree_blobs["definitions-prefetched"] = True
            self.prefetch(
                PurePosixPath(name) for name in self._tree_blob_map()
                if name.endswith((".md", ".yaml", ".yml", ".json")))
            cached = self._blob_bytes.get(oid)
            if cached is not None:
                return cached
        raw = _git(self.root, "cat-file", "blob", oid)
        assert isinstance(raw, bytes)
        self._blob_bytes[oid] = raw
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
        cached = self._tree_blobs.get("last-commits")
        if cached is not None:
            return cached.get(logical.as_posix())
        at = self.commit_sha if self.mode is RepositoryViewMode.COMMIT else "HEAD"
        try:
            out = str(_git(
                self.root, "log", "-1", "--format=%H", str(at), "--",
                logical.as_posix(), text=True,
            )).strip()
        except RepositoryViewError:
            return None
        return out.lower() if _FULL_OBJECT_ID.fullmatch(out) else None

    def prefetch_last_commits(self) -> None:
        """One history walk answering `last_commit_for` for every path at once.

        The per-path form spawns one `git log -1` per call — the same
        process-spawn cost class `prefetch` retired for blob reads (and the
        perimeter check retired for its dating, F12). A face serving N exposed
        things pays it N times per client session; measured 2026-08-30 at
        ~33s for one 46-thing manifest on a cold Windows machine, past the
        membrane client's own 10s deadline. One `--name-only` walk newest-first
        answers all of them: the first block naming a path is that path's last
        touch. Memoised on the view; `last_commit_for` reads through it."""
        if "last-commits" in self._tree_blobs:
            return
        at = self.commit_sha if self.mode is RepositoryViewMode.COMMIT else "HEAD"
        try:
            raw = str(_git(self.root, "log", "--format=%x01%H", "--name-only",
                           str(at), text=True))
        except RepositoryViewError:
            return
        last_touch: dict[str, str] = {}
        for block in raw.split("\x01")[1:]:
            lines = block.splitlines()
            if not lines:
                continue
            sha = lines[0].strip().lower()
            if not _FULL_OBJECT_ID.fullmatch(sha):
                continue
            for name in lines[1:]:
                name = name.strip()
                if name and name not in last_touch:
                    last_touch[name] = sha
        self._tree_blobs["last-commits"] = last_touch

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
