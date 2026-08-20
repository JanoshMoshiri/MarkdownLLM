"""Small optimistic Git transaction for exact-path commits.

The repository index belongs to the operator.  A mechanical commit therefore
builds its candidate in a temporary index seeded from one expected HEAD, runs
the normal commit hooks against that candidate, creates the commit object, and
updates ``HEAD`` with Git's old-object compare-and-swap.  A concurrent commit
can leave an unreachable object, but it can never be absorbed, overwritten, or
silently used as this transaction's parent.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile

from .hook_contract import HookByteContract
from .runtime import run_git_hook


class RepositoryTransactionError(RuntimeError):
    """An exact repository operation could not be completed safely."""


class RepositoryTransactionConflict(RepositoryTransactionError):
    """Repository HEAD changed after the transaction was planned."""


def _run(root: Path, *args: str, env: dict | None = None):
    return subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True, env=env,
    )


def _head(root: Path) -> str | None:
    result = _run(root, "rev-parse", "--verify", "-q", "HEAD")
    return result.stdout.strip() if result.returncode == 0 else None


def _logical_path(value: str | Path) -> str:
    logical = PurePosixPath(str(value).replace("\\", "/"))
    if (logical.is_absolute() or not logical.parts
            or any(part in ("", ".", "..") for part in logical.parts)):
        raise RepositoryTransactionError(
            f"transaction path must be repository-relative: {value!r}")
    return logical.as_posix()


@dataclass(frozen=True)
class RepositoryCommitResult:
    commit_sha: str
    committed_paths: tuple[str, ...]
    post_commit_detail: str = ""


@dataclass(frozen=True)
class RepositoryTransaction:
    """One exact-path commit planned against an immutable expected HEAD."""

    root: Path
    expected_head: str | None
    hook_contract: HookByteContract = HookByteContract()

    @classmethod
    def begin(
            cls, root: Path, *,
            hook_contract: HookByteContract | None = None,
            ) -> "RepositoryTransaction":
        resolved = Path(root).resolve()
        top = _run(resolved, "rev-parse", "--show-toplevel")
        if (top.returncode != 0 or not top.stdout.strip()
                or Path(top.stdout.strip()).resolve() != resolved):
            raise RepositoryTransactionError(
                f"transaction root must be a Git worktree root: {resolved}")
        return cls(resolved, _head(resolved),
                   hook_contract or HookByteContract())

    def assert_head_unchanged(self) -> None:
        current = _head(self.root)
        if current != self.expected_head:
            raise RepositoryTransactionConflict(
                "repository HEAD moved during the transaction: expected "
                f"{self.expected_head or '<unborn>'}, now "
                f"{current or '<unborn>'}")

    def _run_hook(self, name: str, args: tuple[str, ...], env: dict) -> None:
        resolved = _run(
            self.root, "rev-parse", "--path-format=absolute", "--git-path",
            f"hooks/{name}")
        if resolved.returncode != 0 or not resolved.stdout.strip():
            fallback = _run(self.root, "rev-parse", "--git-path", f"hooks/{name}")
            if fallback.returncode != 0 or not fallback.stdout.strip():
                return
            hook_path = Path(fallback.stdout.strip())
            if not hook_path.is_absolute():
                hook_path = self.root / hook_path
        else:
            hook_path = Path(resolved.stdout.strip())
        if not hook_path.is_file():
            return  # Git commit also treats an absent hook as success.
        if os.name != "nt" and not os.access(hook_path, os.X_OK):
            return  # Match Git's non-executable-hook skip semantics.
        expected = self.hook_contract.expected(name)
        try:
            if expected is not None and hook_path.read_bytes() != expected:
                expected = None
        except OSError:
            expected = None
        result = run_git_hook(
            self.root, name, args, env=env, expected_bytes=expected)
        if not result["supported"]:
            raise RepositoryTransactionError(
                f"{name} hook exists but cannot be executed safely on this "
                f"Git/platform combination: {result.get('detail', 'untested')}")
        if not result["passed"]:
            detail = result.get("detail") or "nonzero exit"
            raise RepositoryTransactionError(
                f"{name} hook refused the exact-path transaction: {detail}")

    def commit_exact(
        self, paths: tuple[str | Path, ...], message: str,
    ) -> RepositoryCommitResult:
        """Commit only ``paths`` while preserving the caller's real index.

        Hooks receive ``GIT_INDEX_FILE`` and therefore validate the exact
        temporary candidate.  The changed-path audit happens before the
        compare-and-swap, so a hook that stages an unrelated path cannot widen
        the transaction.
        """
        selected = tuple(dict.fromkeys(_logical_path(path) for path in paths))
        if not selected:
            raise RepositoryTransactionError("an exact commit needs at least one path")
        self.assert_head_unchanged()
        real_index_before = _run(
            self.root, "ls-files", "--stage", "--", *selected)
        if real_index_before.returncode != 0:
            raise RepositoryTransactionError(
                "caller index could not be snapshotted: "
                + (real_index_before.stderr.strip()
                   or real_index_before.stdout.strip()))

        git_dir_result = _run(self.root, "rev-parse", "--absolute-git-dir")
        if git_dir_result.returncode != 0 or not git_dir_result.stdout.strip():
            raise RepositoryTransactionError("Git directory could not be resolved")
        git_dir = Path(git_dir_result.stdout.strip()).resolve()
        git_dir.mkdir(parents=True, exist_ok=True)
        fd, index_name = tempfile.mkstemp(prefix="mdllm-index-", dir=git_dir)
        os.close(fd)
        index_path = Path(index_name)
        index_path.unlink()  # Git requires an absent path for a new index.
        fd, message_name = tempfile.mkstemp(prefix="mdllm-message-", dir=git_dir)
        os.close(fd)
        message_path = Path(message_name)
        message_path.write_text(message.rstrip("\n") + "\n", encoding="utf-8")
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(index_path)

        try:
            seed = (_run(self.root, "read-tree", self.expected_head, env=env)
                    if self.expected_head else
                    _run(self.root, "read-tree", "--empty", env=env))
            if seed.returncode != 0:
                raise RepositoryTransactionError(
                    "temporary index could not be seeded: "
                    + (seed.stderr.strip() or seed.stdout.strip()))
            added = _run(self.root, "add", "--", *selected, env=env)
            if added.returncode != 0:
                raise RepositoryTransactionError(
                    "exact paths could not be staged: "
                    + (added.stderr.strip() or added.stdout.strip()))

            self.assert_head_unchanged()
            self._run_hook("pre-commit", (), env)
            self._run_hook(
                "prepare-commit-msg", (str(message_path), "message"), env)
            self._run_hook("commit-msg", (str(message_path),), env)

            tree = _run(self.root, "write-tree", env=env)
            if tree.returncode != 0 or not tree.stdout.strip():
                raise RepositoryTransactionError(
                    "temporary candidate tree could not be written: "
                    + (tree.stderr.strip() or tree.stdout.strip()))
            tree_sha = tree.stdout.strip()
            changed = (_run(self.root, "ls-files", "--", env=env)
                       if self.expected_head is None else
                       _run(self.root, "diff", "--name-only",
                            self.expected_head, tree_sha))
            changed_paths = tuple(sorted(
                line.strip().replace("\\", "/")
                for line in changed.stdout.splitlines() if line.strip()))
            if changed.returncode != 0 or set(changed_paths) != set(selected):
                raise RepositoryTransactionError(
                    "exact-path candidate audit failed: expected "
                    f"{sorted(selected)}, got {list(changed_paths)}")

            commit_args = ["commit-tree", tree_sha]
            if self.expected_head:
                commit_args += ["-p", self.expected_head]
            commit_args += ["-F", str(message_path)]
            commit = _run(self.root, *commit_args, env=env)
            if commit.returncode != 0 or not commit.stdout.strip():
                raise RepositoryTransactionError(
                    "commit object could not be created: "
                    + (commit.stderr.strip() or commit.stdout.strip()))
            commit_sha = commit.stdout.strip()

            old = self.expected_head or ("0" * len(commit_sha))
            moved = _run(
                self.root, "update-ref", "-m", message.splitlines()[0],
                "HEAD", commit_sha, old)
            if moved.returncode != 0:
                current = _head(self.root)
                raise RepositoryTransactionConflict(
                    "repository HEAD moved before the exact commit could land: "
                    f"expected {self.expected_head or '<unborn>'}, now "
                    f"{current or '<unborn>'}")

            # A normal ``git commit`` advances these exact entries in the real
            # index to the new HEAD.  Our temporary-index commit must do that
            # explicitly or each newly committed path appears staged for
            # deletion.  Reconcile only if another process has not changed
            # those selected index entries since begin; unrelated entries are
            # never addressed.
            real_index_now = _run(
                self.root, "ls-files", "--stage", "--", *selected)
            index_detail = ""
            if (real_index_now.returncode == 0
                    and real_index_now.stdout == real_index_before.stdout):
                reconciled = _run(
                    self.root, "reset", "-q", "HEAD", "--", *selected)
                if reconciled.returncode != 0:
                    index_detail = (
                        "commit landed, but its exact real-index entries could "
                        "not be reconciled: "
                        + (reconciled.stderr.strip()
                           or reconciled.stdout.strip()))
            else:
                index_detail = (
                    "commit landed; selected real-index entries changed "
                    "concurrently and were preserved")

            # Post-commit cannot veto a commit in normal Git either.  Preserve
            # its diagnostic for the caller, but do not manufacture rollback
            # after the ref has atomically moved.
            post_env = os.environ.copy()
            try:
                self._run_hook("post-commit", (), post_env)
                detail = index_detail
            except RepositoryTransactionError as exc:
                detail = "; ".join(x for x in (index_detail, str(exc)) if x)
            return RepositoryCommitResult(commit_sha, changed_paths, detail)
        finally:
            index_path.unlink(missing_ok=True)
            message_path.unlink(missing_ok=True)
