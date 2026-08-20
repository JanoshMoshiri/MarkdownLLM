"""Domain birth and the pre-commit hook — the `pre-domain-scaffold:isolate`
hard hook, mechanised, plus `install-hook`.

`MDLLM_ENTRY` is the public entry shim (`tools/mdllm.py`) — the path every
installed hook and generated settings file must reference; the package is an
implementation detail behind it.
"""

from __future__ import annotations

import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import adapters as harness_adapters
from .adapter_install import portable_artifact_parts
from .boundary import TERMS_FILE
from .harness_ports import (
    HarnessContext, RenderPort, ScaffoldNoticePort, ShortcutPort,
)
from .runtime import SH_RESOLVE, execution_test_hook
from .domain_kernel import apply_domain_kernel, build_domain_kernel_blocks
from .model import ID_RE, parse_frontmatter
from .repository_transaction import (
    RepositoryTransaction, RepositoryTransactionError,
)
from .yaml_loader import load_version_sentinel

MDLLM_ENTRY = Path(__file__).resolve().parents[1] / "mdllm.py"

HOOK_BODY = """#!/bin/sh
# mdllm pre-commit: deterministic validation floor (transformation plan Phase 1)
# Portable: repo root and interpreter are resolved at run time, mdllm.py via a
# path relative to the repo root — so the same hook works wherever this repo is
# checked out or mounted (Windows, WSL, CI, sandboxed agent harnesses).
ROOT="$(git rev-parse --show-toplevel)"
MDLLM_ROUTE="{rel}"
case "$MDLLM_ROUTE" in
  /*|[A-Za-z]:/*) MDLLM="$MDLLM_ROUTE" ;;
  *) MDLLM="$ROOT/$MDLLM_ROUTE" ;;
esac
# Interpreter resolution (one owner: markdownllm/runtime.py — the comment
# there explains the candidate order and why the probe imports the floor's
# real dependency rather than just proving an interpreter exists).
{resolve}
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  echo "mdllm: validation floor unavailable (no interpreter with PyYAML, or $MDLLM not found) — commit blocked."
  echo "Run \\`mdllm runtime-probe .\\` (or \\`python <framework>/tools/mdllm.py runtime-probe .\\`) for a per-candidate report."
  exit 1
fi
# Freeze one exact candidate for every floor subprocess. Without this pin,
# four individually immutable RepositoryView.index constructions could still
# observe four different trees if another process changed the index between
# commands. The end comparison is the optimistic CAS: movement blocks retry.
MDLLM_FROZEN_INDEX_TREE="$(git write-tree)" || {{
  echo "mdllm: could not freeze the staged candidate — commit blocked."
  exit 1
}}
MDLLM_FROZEN_INDEX_ROOT="$ROOT"
export MDLLM_FROZEN_INDEX_TREE MDLLM_FROZEN_INDEX_ROOT
# Disclosure boundary first: cheapest check, clearest message. Reads the LOCAL
# gitignored .boundary-terms; absent (every fresh clone, all CI) => silent no-op.
mdllm_python "$MDLLM" boundary "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: staged content crosses the disclosure boundary — commit blocked."
  exit 1
}}
mdllm_python "$MDLLM" validate "$ROOT" --quiet --view index || {{
  echo ""
  echo "mdllm: validation Errors — commit blocked. Fix or run with --no-verify (discouraged)."
  exit 1
}}
# Coherence: generated-artifact freshness (kernel/index drift) + spec-catalog
# integrity. Self-scoping — at a domain root (no .markdownllm) only the general
# checks run, so the same hook is correct in the framework and in every domain.
mdllm_python "$MDLLM" coherence "$ROOT" --quiet --view index || {{
  echo ""
  echo "mdllm: coherence Errors — a generated artifact (kernel/index) or the spec catalog is stale. Regenerate and re-commit, or --no-verify (discouraged)."
  exit 1
}}
# Change-reconciliation advisories (estate-cadence-cluster Phase 1+4): the cue
# question (modified thing that is reasoned-from) and the serve-side notice
# (modified thing that is exposed). Advisory only — never blocks the commit.
mdllm_python "$MDLLM" candidates "$ROOT" --view index || true
MDLLM_CURRENT_INDEX_TREE="$(git write-tree)" || {{
  echo "mdllm: could not re-read the staged candidate — commit blocked."
  exit 1
}}
if [ "$MDLLM_CURRENT_INDEX_TREE" != "$MDLLM_FROZEN_INDEX_TREE" ]; then
  echo ""
  echo "mdllm: the staged index changed while the floor was running — commit blocked; retry against one candidate."
  exit 1
fi
"""

# The publication leg (estate-cadence-cluster Phase 1): after a commit lands
# and the floor has validated it, publish it — transport of already-committed,
# already-validated state, the mirror of estate-sync's fast-forwards. Opt-in
# per repo via literal `git: autopush: true` in AGENTS.md frontmatter; absence,
# malformed policy, and false are all off.
# All outcome handling (rejected = DIVERGED surfaced never resolved, offline =
# publication debt, no --force ever) lives in `mdllm autopush`; the hook only
# invokes it and always exits 0 — a post-commit surface must never fail the
# commit it follows.
POST_COMMIT_HOOK_BODY = """#!/bin/sh
# mdllm post-commit: autopush publication leg (estate-cadence-cluster Phase 1)
ROOT="$(git rev-parse --show-toplevel)"
MDLLM_ROUTE="{rel}"
case "$MDLLM_ROUTE" in
  /*|[A-Za-z]:/*) MDLLM="$MDLLM_ROUTE" ;;
  *) MDLLM="$ROOT/$MDLLM_ROUTE" ;;
esac
{resolve}
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  exit 0  # no floor available: publication stays manual; estate-sync --status reports the debt
fi
mdllm_python "$MDLLM" autopush "$ROOT" || true
exit 0
"""

# The commit MESSAGE is a surface pre-commit structurally cannot see (git has
# not collected it yet) — and it is where honour-system disclosure failures
# actually live. Same portable preamble as HOOK_BODY; $1 is the message file.
COMMIT_MSG_HOOK_BODY = """#!/bin/sh
# mdllm commit-msg: disclosure-boundary check on the commit message
# (boundary-disclosure-check plan). Local .boundary-terms only; absent => no-op.
ROOT="$(git rev-parse --show-toplevel)"
MDLLM_ROUTE="{rel}"
case "$MDLLM_ROUTE" in
  /*|[A-Za-z]:/*) MDLLM="$MDLLM_ROUTE" ;;
  *) MDLLM="$ROOT/$MDLLM_ROUTE" ;;
esac
{resolve}
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  exit 0  # no floor available: the pre-commit hook already reported/blocked
fi
mdllm_python "$MDLLM" boundary "$ROOT" --message "$1" --quiet || {{
  echo ""
  echo "mdllm: the commit MESSAGE crosses the disclosure boundary — commit blocked."
  exit 1
}}
"""

# Interpreter resolution has ONE owner (runtime.py); substituted here once so
# every consumer — install_hook's writes, doctor's currency comparison — sees
# the same final bytes. Only {rel} remains for per-repo formatting, so the
# fragment's shell braces (${MDLLM%/*/*}) are doubled to survive .format().
_SH_RESOLVE_ESCAPED = SH_RESOLVE.replace("{", "{{").replace("}", "}}")
HOOK_BODY = HOOK_BODY.replace("{resolve}", _SH_RESOLVE_ESCAPED)
POST_COMMIT_HOOK_BODY = POST_COMMIT_HOOK_BODY.replace(
    "{resolve}", _SH_RESOLVE_ESCAPED)
COMMIT_MSG_HOOK_BODY = COMMIT_MSG_HOOK_BODY.replace(
    "{resolve}", _SH_RESOLVE_ESCAPED)


_HOOK_BODIES = {
    "pre-commit": HOOK_BODY,
    "commit-msg": COMMIT_MSG_HOOK_BODY,
    "post-commit": POST_COMMIT_HOOK_BODY,
}

_HOOK_MARKERS = {
    "pre-commit": "# mdllm pre-commit:",
    "commit-msg": "# mdllm commit-msg:",
    "post-commit": "# mdllm post-commit:",
}


def _git_path(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args],
                          capture_output=True, text=True)


def repository_root(root: Path) -> Path:
    """Resolve the worktree root through git, including a `.git` gitfile."""
    result = _git_path(root, "rev-parse", "--show-toplevel")
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit(f"mdllm: {root} is not inside a git worktree")
    return Path(result.stdout.strip()).resolve()


def resolve_hooks_dir(root: Path) -> Path:
    """Return the directory git will actually use for hooks.

    `git rev-parse --git-path hooks` is the authority here: unlike
    `root/.git/hooks`, it follows gitfiles/linked worktrees and
    `core.hooksPath`.  The absolute form is available on supported modern git;
    the fallback retains compatibility with older git and resolves its answer
    against the worktree root.
    """
    repo = repository_root(root)
    result = _git_path(
        repo, "rev-parse", "--path-format=absolute", "--git-path", "hooks")
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    result = _git_path(repo, "rev-parse", "--git-path", "hooks")
    if result.returncode != 0 or not result.stdout.strip():
        sys.exit(f"mdllm: git could not resolve the hooks directory for {repo}")
    hooks = Path(result.stdout.strip())
    return hooks.resolve() if hooks.is_absolute() else (repo / hooks).resolve()


def hook_mdllm_route(repo: Path) -> str:
    """Route embedded in a hook, portable unless git shares it by worktree.

    Linked worktrees share their common hooks directory but can sit at
    unrelated filesystem depths. A route relative to whichever worktree ran
    install would break the others, so that local (never cloned) hook uses the
    framework's absolute path. Ordinary repos retain the move-friendly route.
    """
    repo = repository_root(repo)
    if (repo / ".git").is_file():
        return MDLLM_ENTRY.as_posix()
    try:
        return Path(os.path.relpath(MDLLM_ENTRY, repo)).as_posix()
    except ValueError:  # different drives: no valid relative route exists
        return MDLLM_ENTRY.as_posix()


def _managed_for_repo(path: Path, name: str, rel: str) -> bool:
    """True only for a hook previously installed for this repository.

    A marker alone is insufficient when `core.hooksPath` is shared: replacing
    another repository's mdllm hook would still be overwriting operator state.
    The embedded route must agree as well.
    """
    try:
        installed = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError):
        return False
    return (_HOOK_MARKERS[name] in installed
            and f'MDLLM_ROUTE="{rel}"' in installed)


class HookTransactionError(RuntimeError):
    """A multi-hook install/uninstall could not complete atomically."""


class HookTransactionConflict(HookTransactionError):
    """A hook changed after the transaction observed it."""


@dataclass(frozen=True)
class _HookSnapshot:
    existed: bool
    data: bytes = b""
    mode: int = 0


def _hook_snapshot(path: Path) -> _HookSnapshot:
    """Read one hook state without following a replacement symlink."""
    if path.is_symlink():
        raise HookTransactionConflict(f"hook became a symlink: {path}")
    if not path.exists():
        return _HookSnapshot(False)
    if not path.is_file():
        raise HookTransactionConflict(f"hook is no longer a file: {path}")
    return _HookSnapshot(True, path.read_bytes(), path.stat().st_mode)


def _stage_hook(path: Path, payload: bytes, mode: int) -> Path:
    """Durably stage hook bytes beside their atomic replacement target."""
    fd, raw = tempfile.mkstemp(
        prefix=f".{path.name}.mdllm-", suffix=".tmp", dir=path.parent)
    staged = Path(raw)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            staged.chmod(mode)
        except OSError:
            pass  # Windows: executability is not a file-mode concern
        return staged
    except BaseException:
        staged.unlink(missing_ok=True)
        raise


def _restore_applied_hooks(
        applied: list[tuple[Path, _HookSnapshot, _HookSnapshot]],
        ) -> list[str]:
    """Rollback only our still-current bytes; preserve concurrent edits.

    There is no portable filesystem compare-and-swap primitive.  Rechecking
    immediately before each atomic replace closes the useful optimistic
    window, while the expected-after guard is the critical invariant: a later
    failure can never make rollback blindly overwrite bytes an operator wrote
    after mdllm's replacement.
    """
    failures: list[str] = []
    for path, before, expected_after in reversed(applied):
        staged: Path | None = None
        try:
            current = _hook_snapshot(path)
            if current != expected_after:
                raise HookTransactionConflict(
                    "rollback conflict: hook changed after mdllm wrote it")
            if not before.existed:
                path.unlink()
                continue
            staged = _stage_hook(path, before.data, before.mode)
            if _hook_snapshot(path) != expected_after:
                raise HookTransactionConflict(
                    "rollback conflict: hook changed while restore was staged")
            staged.replace(path)
        except BaseException as exc:
            failures.append(f"{path}: {exc}")
        finally:
            if staged is not None:
                staged.unlink(missing_ok=True)
    return failures


def _raise_hook_failure(
        operation: str, original: BaseException, rollback: list[str]) -> None:
    if rollback:
        raise HookTransactionError(
            f"hook {operation} failed: {original}; rollback conflicts: "
            + "; ".join(rollback)) from original
    raise original


def install_hook(root: Path) -> str:
    """Install mdllm's three hooks without overwriting operator hooks.

    The operation preflights all hook names before writing any of them. A
    foreign hook causes a safe refusal with its bytes untouched; mdllm-owned
    hooks for this same repository may be upgraded. Normal write failures roll
    the three paths back to their exact bytes and modes.

    Returns the mdllm path embedded in the hooks (for reporting).
    """
    repo = repository_root(Path(root).resolve())
    hooks_dir = resolve_hooks_dir(repo)
    rel = hook_mdllm_route(repo)

    targets = {name: hooks_dir / name for name in _HOOK_BODIES}
    for name, path in targets.items():
        tmp = hooks_dir / f".{name}.mdllm-install"
        if tmp.exists():
            sys.exit(
                f"mdllm: refusing to replace existing hook transaction file "
                f"{tmp}; inspect it before retrying")
        if not path.exists():
            continue
        if (path.is_symlink() or not path.is_file()
                or not _managed_for_repo(path, name, rel)):
            sys.exit(
                f"mdllm: refusing to replace existing operator hook {path}; "
                "preserve or chain it explicitly, then retry")

    snapshots = {path: _hook_snapshot(path) for path in targets.values()}
    staged: dict[Path, tuple[Path, _HookSnapshot]] = {}
    applied: list[tuple[Path, _HookSnapshot, _HookSnapshot]] = []

    try:
        hooks_dir.mkdir(parents=True, exist_ok=True)
        for name, path in targets.items():
            payload = _HOOK_BODIES[name].format(rel=rel).encode("utf-8")
            before = snapshots[path]
            mode = (before.mode | 0o111) if before.existed else 0o755
            tmp = _stage_hook(path, payload, mode)
            staged[path] = (tmp, _HookSnapshot(True, payload, tmp.stat().st_mode))
        for path, (tmp, expected_after) in staged.items():
            before = snapshots[path]
            if _hook_snapshot(path) != before:
                raise HookTransactionConflict(
                    f"{path} changed while hook payloads were staged")
            tmp.replace(path)
            applied.append((path, before, expected_after))
    except BaseException as exc:
        rollback = _restore_applied_hooks(applied)
        _raise_hook_failure("install", exc, rollback)
    finally:
        for tmp, _ in staged.values():
            tmp.unlink(missing_ok=True)
    return rel


def uninstall_hook(root: Path) -> Path:
    """Remove only hooks demonstrably owned by mdllm for this repository.

    Foreign or operator-edited hooks cause an all-or-nothing refusal. Because
    installation never moves or rewrites foreign hooks, uninstalling needs no
    lossy reconstruction step.
    """
    repo = repository_root(Path(root).resolve())
    hooks_dir = resolve_hooks_dir(repo)
    rel = hook_mdllm_route(repo)
    targets = {name: hooks_dir / name for name in _HOOK_BODIES}
    for name, path in targets.items():
        if path.exists() and (path.is_symlink() or not path.is_file()
                              or not _managed_for_repo(path, name, rel)):
            sys.exit(f"mdllm: refusing to remove operator hook {path}")
    snapshots = {path: _hook_snapshot(path) for path in targets.values()}
    applied: list[tuple[Path, _HookSnapshot, _HookSnapshot]] = []
    try:
        for path in targets.values():
            before = snapshots[path]
            if _hook_snapshot(path) != before:
                raise HookTransactionConflict(
                    f"{path} changed during hook uninstall")
            if before.existed:
                path.unlink()
                applied.append((path, before, _HookSnapshot(False)))
    except BaseException as exc:
        rollback = _restore_applied_hooks(applied)
        _raise_hook_failure("uninstall", exc, rollback)
    return hooks_dir


def cmd_install_hook(args) -> int:
    root = Path(args.path).resolve()
    if getattr(args, "uninstall", False):
        hooks_dir = uninstall_hook(root)
        print(f"uninstalled mdllm-owned hooks from {hooks_dir}; operator hooks were untouched")
        return 0
    rel = install_hook(root)
    hooks_dir = resolve_hooks_dir(root)
    print(f"installed {hooks_dir / 'pre-commit'} + {hooks_dir / 'commit-msg'} "
          f"+ {hooks_dir / 'post-commit'} (mdllm via {rel})")
    # The execution test fires a real pre-commit, which is a full validate.
    # On a large domain that is minutes, and chaining it in a harness silently
    # blew a 120s tool timeout and read as a hang (field report 2026-08-13).
    # Skipping is opt-in and downgrades the claim honestly: installed is a
    # weaker fact than runs, and the report must say which one it has.
    if getattr(args, "no_test", False):
        print("execution test: SKIPPED (--no-test) — the hook is installed but "
              "unproven; it will first fire at the next real commit")
        return 0
    # Execution-test the hook we just wrote (vendor-harness-adapter-foundation
    # Phase 1): installed is a weaker fact than runs. The runtime owns safe
    # modern-Git and compatibility execution; no safe route remains untested.
    result = execution_test_hook(root)
    if not result["supported"]:
        print("execution test: UNTESTED — no semantics-preserving execution "
              f"route was available ({result['detail']}); the hook will first "
              "fire at the next real commit")
        return 0
    if result["passed"]:
        print("execution test: pre-commit ran and passed")
        return 0
    print("execution test: pre-commit ran and FAILED — the floor is wired but "
          "blocking; its output follows:")
    if result.get("detail"):
        print(result["detail"])
    return 1


@dataclass(frozen=True)
class _OuterIsolation:
    root: Path | None
    rel_target: str = ""
    gitignore: Path | None = None
    original: bytes = b""
    original_existed: bool = False
    needs_commit: bool = False
    transaction: RepositoryTransaction | None = None
    original_index: bytes = b""


def _gitignore_literal_rule(relative_target: str) -> str:
    """Render one repository-rooted literal directory rule.

    A scaffold target may sit below an operator-named parent containing Git
    ignore metacharacters.  Writing that path raw can silently fail to isolate
    the newborn (or match unrelated paths).  Root anchoring plus escaping
    makes the exact resolved relative path the rule's only meaning.
    """
    raw = relative_target.strip("/")
    escaped = "".join(("\\" + char) if char in "\\*?[]#! " else char
                      for char in raw)
    return f"/{escaped}/"


def _preflight_outer_isolation(target: Path) -> _OuterIsolation:
    """Resolve and validate the outer isolation transaction without writes."""
    probe = target.parent
    while not probe.exists() and probe != probe.parent:
        probe = probe.parent
    outer = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], cwd=probe,
        capture_output=True, text=True)
    if outer.returncode != 0 or not outer.stdout.strip():
        return _OuterIsolation(None)

    outer_root = Path(outer.stdout.strip()).resolve()
    try:
        transaction = RepositoryTransaction.begin(outer_root)
    except RepositoryTransactionError as exc:
        sys.exit(f"mdllm: could not start outer repository transaction: {exc}")
    rel_t = Path(os.path.relpath(target, outer_root)).as_posix() + "/"
    gi = outer_root / ".gitignore"
    if gi.is_symlink():
        sys.exit(f"mdllm: refusing to rewrite symlinked outer ignore file {gi}")
    existed = gi.is_file()
    original = gi.read_bytes() if existed else b""
    try:
        existing = original.decode("utf-8")
    except UnicodeDecodeError:
        sys.exit(f"mdllm: {gi} is not UTF-8; refusing to rewrite it")
    ignored = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", "--", rel_t],
        cwd=outer_root, capture_output=True).returncode == 0
    exact_rule_present = rel_t.rstrip("/") in {
        line.strip().rstrip("/") for line in existing.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    exact_rule_present = (exact_rule_present
                          or _gitignore_literal_rule(rel_t) in {
                              line.strip() for line in existing.splitlines()
                              if line.strip() and not line.lstrip().startswith("#")
                          })
    if ignored:
        return _OuterIsolation(
            outer_root, rel_t, gi, original, existed, False, transaction)
    if exact_rule_present:
        # A later negation can make a visually present rule ineffective. Do
        # not claim isolation merely because text resembling a rule exists.
        sys.exit(
            f"mdllm: {gi} names {rel_t!r} but git does not ignore it; "
            "resolve the conflicting ignore rules before scaffolding")

    # The exact-path commit below deliberately coexists with unrelated staged
    # work, but it cannot safely absorb pre-existing changes to .gitignore.
    gi_status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--", ".gitignore"],
        cwd=outer_root, capture_output=True, text=True)
    if gi_status.returncode != 0:
        sys.exit(f"mdllm: could not preflight {gi}: {gi_status.stderr.strip()}")
    if gi_status.stdout.strip():
        sys.exit(
            f"mdllm: refusing to scaffold while {gi} has existing changes; "
            "commit or restore them first so isolation remains one exact commit")
    index_state = subprocess.run(
        ["git", "ls-files", "--stage", "--", ".gitignore"],
        cwd=outer_root, capture_output=True)
    if index_state.returncode != 0:
        sys.exit(f"mdllm: could not snapshot the index entry for {gi}")
    return _OuterIsolation(
        outer_root, rel_t, gi, original, existed, True, transaction,
        index_state.stdout)


def _rollback_empty_domain_repo(
        target: Path, created_dirs: list[Path]) -> bool:
    """Undo a demonstrably untouched, unborn ``git init`` only.

    A concurrent writer may start using the newborn between init and an outer
    failure.  In that case its worktree and repository metadata are retained;
    cleanup is not more important than preserving operator state.
    """
    git_meta = target / ".git"
    try:
        entries = set(target.iterdir()) if target.is_dir() else set()
        if entries != {git_meta}:
            return False
        head = subprocess.run(
            ["git", "rev-parse", "--verify", "-q", "HEAD"], cwd=target,
            capture_output=True)
        status = subprocess.run(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=target, capture_output=True)
        if head.returncode == 0 or status.returncode != 0 or status.stdout.strip():
            return False
        if git_meta.is_dir():
            shutil.rmtree(git_meta)
        elif git_meta.is_file():
            git_meta.unlink()
        for directory in created_dirs:
            if directory.is_dir() and not any(directory.iterdir()):
                directory.rmdir()
        return True
    except OSError:
        return False


def _head_blob(root: Path, path: str) -> tuple[bool, bytes]:
    result = subprocess.run(
        ["git", "show", f"HEAD:{path}"], cwd=root, capture_output=True)
    return result.returncode == 0, result.stdout


def _restore_outer_ignore_if_unchanged(
        isolation: _OuterIsolation, applied: bytes) -> str | None:
    """Restore our failed isolation write without erasing concurrent state."""
    assert isolation.root is not None and isolation.gitignore is not None
    assert isolation.transaction is not None
    gi = isolation.gitignore

    def conflict() -> str | None:
        if gi.is_symlink() or not gi.is_file() or gi.read_bytes() != applied:
            return "the outer .gitignore changed after mdllm wrote it"
        index_now = subprocess.run(
            ["git", "ls-files", "--stage", "--", ".gitignore"],
            cwd=isolation.root, capture_output=True)
        if (index_now.returncode != 0
                or index_now.stdout != isolation.original_index):
            return "the outer .gitignore index entry changed concurrently"
        current_head = subprocess.run(
            ["git", "rev-parse", "--verify", "-q", "HEAD"],
            cwd=isolation.root, capture_output=True, text=True)
        current = (current_head.stdout.strip()
                   if current_head.returncode == 0 else None)
        if current != isolation.transaction.expected_head:
            blob_existed, blob = _head_blob(isolation.root, ".gitignore")
            if (blob_existed != isolation.original_existed
                    or (blob_existed and blob != isolation.original)):
                return "moved HEAD accepted different outer .gitignore bytes"
        return None

    reason = conflict()
    if reason:
        return reason
    staged: Path | None = None
    try:
        if isolation.original_existed:
            staged = _stage_hook(
                gi, isolation.original, gi.stat().st_mode)
            reason = conflict()
            if reason:
                return reason
            staged.replace(gi)
        else:
            # Recheck immediately before removal; this is the narrowest
            # portable optimistic window available for an absent original.
            reason = conflict()
            if reason:
                return reason
            gi.unlink()
    except OSError as exc:
        return f"could not restore outer .gitignore: {exc}"
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)
    return None


def _initialise_and_isolate(
        target: Path, isolation: _OuterIsolation) -> Path | None:
    """Create the nested repo, then land only its outer ignore rule."""
    if isolation.needs_commit:
        assert isolation.transaction is not None
        try:
            isolation.transaction.assert_head_unchanged()
        except RepositoryTransactionError as exc:
            sys.exit(f"mdllm: outer repository changed after scaffold preflight; "
                     f"no birth writes were made ({exc})")
    created_dirs: list[Path] = []
    cursor = target
    while not cursor.exists() and cursor != cursor.parent:
        created_dirs.append(cursor)
        cursor = cursor.parent
    target.mkdir(parents=True, exist_ok=True)
    initialised = subprocess.run(
        ["git", "init", "-q"], cwd=target, capture_output=True, text=True)
    if initialised.returncode != 0:
        cleaned = _rollback_empty_domain_repo(target, created_dirs)
        sys.exit(f"mdllm: could not initialise {target}: "
                 f"{initialised.stderr.strip() or initialised.stdout.strip()}"
                 + ("" if cleaned else "; partial target retained for inspection"))
    if not isolation.needs_commit:
        return isolation.root

    assert isolation.root is not None and isolation.gitignore is not None
    assert isolation.transaction is not None
    gi = isolation.gitignore
    current = gi.read_bytes() if gi.is_file() else b""
    if current != isolation.original:
        cleaned = _rollback_empty_domain_repo(target, created_dirs)
        sys.exit(f"mdllm: {gi} changed after scaffold preflight; no isolation "
                 "write was applied"
                 + ("" if cleaned else "; newborn repo retained because it changed"))
    separator = b"" if not isolation.original or isolation.original.endswith(b"\n") else b"\n"
    applied = (
        isolation.original + separator
        + f"{_gitignore_literal_rule(isolation.rel_target)}\n".encode("utf-8"))
    gi.write_bytes(applied)
    isolated = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", "--",
         isolation.rel_target], cwd=isolation.root,
        capture_output=True, text=True)
    commit_error = None
    commit_result = None
    if isolated.returncode == 0:
        try:
            commit_result = isolation.transaction.commit_exact(
                (".gitignore",),
                f"chore: isolate domain {isolation.rel_target} (scaffold)")
        except RepositoryTransactionError as exc:
            commit_error = str(exc)
    else:
        commit_error = "the exact .gitignore rule did not isolate the target"
    if commit_result is None:
        # The caller's real index was never touched: RepositoryTransaction
        # stages in a temporary index and compare-and-swaps HEAD. Restore only
        # our exact worktree bytes, then undo the otherwise empty nested repo.
        restore_conflict = _restore_outer_ignore_if_unchanged(
            isolation, applied)
        cleaned = (False if restore_conflict else
                   _rollback_empty_domain_repo(target, created_dirs))
        if restore_conflict or not cleaned:
            reasons = "; ".join(x for x in (
                commit_error, restore_conflict,
                None if cleaned else "newborn repo retained for recovery",
            ) if x)
            sys.exit(
                f"mdllm: outer isolation commit failed in {isolation.root}; "
                f"concurrent or partial state was preserved ({reasons})")
        sys.exit(
            f"mdllm: outer isolation commit failed in {isolation.root}; "
            f"all pre-birth writes were rolled back ({commit_error})")

    changed = subprocess.run(
        ["git", "diff-tree", "--root", "--no-commit-id", "--name-only",
         "-r", commit_result.commit_sha], cwd=isolation.root,
        capture_output=True, text=True)
    committed_paths = {line.strip().replace("\\", "/")
                       for line in changed.stdout.splitlines() if line.strip()}
    if (changed.returncode != 0 or committed_paths != {".gitignore"}
            or set(commit_result.committed_paths) != {".gitignore"}):
        sys.exit(
            "mdllm: outer isolation commit landed but its path audit was not "
            f"exactly .gitignore ({sorted(committed_paths)}); stop and inspect "
            f"{isolation.root}")
    return isolation.root


@dataclass
class _ScaffoldProgress:
    target: Path
    stage: str = "preflight"
    isolation_landed: bool = False
    outer_root: Path | None = None


def _report_recoverable_birth(
        progress: _ScaffoldProgress, error: BaseException) -> int:
    """Report a post-isolation failure without erasing accepted state."""
    target = progress.target
    head = subprocess.run(
        ["git", "rev-parse", "--verify", "-q", "HEAD"], cwd=target,
        capture_output=True, text=True)
    status = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all"], cwd=target,
        capture_output=True, text=True)
    print(f"## Scaffold incomplete — {target}")
    print(f"  FAIL  stage: {progress.stage}: {error}")
    print("  RECOVERY  the initialised domain repo was retained; no accepted "
          "outer isolation commit was erased")
    if progress.outer_root is not None:
        print(f"  RECOVERY  outer isolation remains in {progress.outer_root}")
    if head.returncode == 0:
        print(f"  RECOVERY  domain HEAD: {head.stdout.strip()}")
    else:
        print("  RECOVERY  domain HEAD is unborn; generated bytes are not yet accepted")
    if status.returncode == 0:
        rows = [line for line in status.stdout.splitlines() if line]
        print(f"  RECOVERY  domain status entries: {len(rows)} (inspect with "
              f"`git -C {target} status --short`)")
    if progress.stage == "hook installation":
        print(f"  NEXT  fix the hook conflict, then run `mdllm install-hook {target}`")
    elif progress.stage in {"domain staging", "first commit"}:
        print("  NEXT  inspect the retained files and hooks, then make the first "
              "domain commit; unrelated outer index state was not addressed")
    else:
        print("  NEXT  inspect it or move the partial target to a private location "
              "outside the outer worktree, then rerun scaffold; the existing "
              "outer ignore rule makes retry isolation idempotent")
    print("BIRTH SEQUENCE INCOMPLETE — retained state is explicit and recoverable.")
    return 1


def cmd_scaffold(args) -> int:
    """Public scaffold boundary with truthful post-isolation recovery."""
    progress = _ScaffoldProgress(Path(args.path).resolve())
    try:
        return _cmd_scaffold_impl(args, progress)
    except SystemExit as exc:
        if not progress.isolation_landed:
            raise
        return _report_recoverable_birth(progress, exc)
    except Exception as exc:
        if not progress.isolation_landed:
            raise
        return _report_recoverable_birth(progress, exc)


def _cmd_scaffold_impl(args, progress: _ScaffoldProgress) -> int:
    """The pre-domain-scaffold:isolate hard hook, mechanised. Owns the
    deterministic sequence of domain birth: directories, templates with
    mechanical placeholders substituted (name, dates, framework_root,
    framework_version_seen), a nested git repo, the outer repo's .gitignore
    isolation (added and committed BEFORE the domain's first commit, per the
    hard hook's ordering), the pre-commit hook, and the first commit.
    What remains semantic — thing types and vocabularies in _schema.yaml,
    skill content, AGENTS.md sections, the first real things — stays with
    the agent and the human, where it belongs."""
    fw_root = MDLLM_ENTRY.parents[1]
    sentinel = fw_root / ".markdownllm"
    if not sentinel.is_file():
        sys.exit("mdllm: scaffold requires a framework checkout (.markdownllm not found)")
    try:
        sentinel_data = load_version_sentinel(
            sentinel.read_text(encoding="utf-8"), source=sentinel)
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        sys.exit(f"mdllm: scaffold refused invalid/unreadable {sentinel} — {exc}")
    fw_version = str(sentinel_data.get("version"))
    autopush_choice = str(getattr(args, "autopush", None) or "false").lower()
    if autopush_choice not in {"true", "false"}:
        sys.exit("mdllm: scaffold --autopush must be true or false")
    target = Path(args.path).resolve()
    name = target.name
    if not ID_RE.match(name):
        sys.exit(f"mdllm: domain folder name must be kebab-case (got {name!r})")
    if target.exists() and any(target.iterdir()):
        sys.exit(f"mdllm: {target} exists and is not empty")
    templates = fw_root / "templates"
    title = " ".join(w.capitalize() for w in name.split("-"))
    today = f"{dt.date.today():%Y-%m-%d}"
    try:
        rel_fw = Path(os.path.relpath(fw_root, target)).as_posix()
    except ValueError:
        sys.exit("mdllm: framework and target have no relative path; refusing "
                 "to embed an absolute machine-specific adapter command")

    # Resolve the complete outer projection before creating the target.  This
    # makes an unknown selection or a cross-adapter path collision a true
    # preflight failure rather than a half-scaffolded domain.
    selected_names = harness_adapters.selection(
        getattr(args, "harness", None))
    selected_adapters = tuple(harness_adapters.get(n) for n in selected_names)
    ctx = HarnessContext(framework_root_rel=rel_fw)
    adapter_shortcuts: list[tuple[str, Path]] = []
    adapter_artifacts: list[tuple[str, bytes]] = []
    projected: dict[tuple[str, ...], tuple[str, bool]] = {}

    def claim_projection(
            relpath: str, owner: str, *, directory: bool = False) -> str:
        """Reserve a portable target path before scaffold creates anything.

        The projection is case-folded and separator-normalised even off
        Windows.  A scaffold committed on one platform must not contain two
        paths which become the same path when cloned on another.  Core
        directories reserve their whole namespace from adapter output.
        """
        if not isinstance(relpath, str):
            sys.exit(f"mdllm: {owner!r} projected non-string path {relpath!r}")
        try:
            # Scaffold accepts either separator spelling as adapter input but
            # reserves and writes one POSIX projection.  That lets a Windows-
            # shaped path collide visibly with its portable spelling instead
            # of becoming a second file after clone.
            parts = portable_artifact_parts(relpath.replace("\\", "/"))
        except ValueError:
            sys.exit(f"mdllm: {owner!r} projected unsafe path {relpath!r}")
        key = tuple(part.casefold() for part in parts)
        for previous_key, (previous_owner, previous_directory) in projected.items():
            same = key == previous_key
            within_previous = (previous_directory
                               and key[:len(previous_key)] == previous_key)
            owns_previous_parent = (directory
                                    and previous_key[:len(key)] == key)
            # Two file projections also cannot stand in an ancestor relation:
            # the first would need to be both a file and a directory.
            file_prefix = (not directory and not previous_directory
                           and (key[:len(previous_key)] == previous_key
                                or previous_key[:len(key)] == key))
            if same or within_previous or owns_previous_parent or file_prefix:
                sys.exit(
                    f"mdllm: adapter projection collision at {relpath!r}: "
                    f"{previous_owner} and {owner}")
        projected[key] = (owner, directory)
        return "/".join(parts)

    # Reserve every path the harness-neutral scaffold owns before asking an
    # adapter for its projection.  Directory reservations cover all generated
    # skills/prompts and the git metadata namespace, including paths added to
    # those core sets by future template evolution.
    for core_path in ("things", "skills", ".git"):
        claim_projection(core_path, "scaffold:core", directory=True)
    if (templates / "prompts").is_dir():
        claim_projection("prompts", "scaffold:core", directory=True)
    # Entry pointers are core, not adapter projection: they are reserved here
    # so an adapter cannot claim one, and they are written in every selection.
    entry_dir = templates / "entry"
    entry_pointers = (sorted(entry_dir.glob("*.template"))
                      if entry_dir.is_dir() else [])
    for core_path in ("AGENTS.md",
                      *(p.stem for p in entry_pointers)):
        claim_projection(core_path, "scaffold:core")
    boundary_template = templates / "boundary-terms.template"
    if boundary_template.is_file():
        claim_projection(TERMS_FILE, "scaffold:core")
        claim_projection(".gitignore", "scaffold:core")

    for adapter in selected_adapters:
        if isinstance(adapter, ShortcutPort):
            for relpath, src in adapter.shortcut_sources(templates).items():
                normalised = claim_projection(
                    relpath, f"{adapter.name}:shortcuts")
                adapter_shortcuts.append((normalised, src))
        if isinstance(adapter, RenderPort):
            for relpath, data in adapter.render(ctx).items():
                normalised = claim_projection(relpath, f"{adapter.name}:render")
                adapter_artifacts.append((normalised, data))

    def instantiate(text: str) -> str:
        text = (text.replace("[domain]", name)
                    .replace("[Domain Name]", title)
                    .replace("[Domain]", title)
                    .replace("[ISO-date]", today)
                    # Required-at-t0 paths must live in prose as well as
                    # frontmatter: harness injection may deliver only the
                    # AGENTS.md body (Gate 7.0 live QMS finding).
                    .replace("[framework-root]", rel_fw))
        text = re.sub(r"framework_root: \[[^\]]*\]", f"framework_root: {rel_fw}", text)
        text = re.sub(r"framework_version_seen: \[[^\]]*\]",
                      f"framework_version_seen: {fw_version}", text)
        return text

    def instantiate_agents(text: str) -> str:
        """Render the irreversible publication choice into the newborn."""
        rendered = instantiate(text)
        front_end = rendered.find("\n---", 4) if rendered.startswith("---\n") else -1
        if front_end < 0:
            sys.exit("mdllm: AGENTS.md template has no YAML frontmatter")
        front = rendered[:front_end]
        front, count = re.subn(
            r"(?m)^([ \t]*autopush:[ \t]*)(?:true|false)([ \t]*(?:#.*)?)$",
            lambda match: match.group(1) + autopush_choice + match.group(2),
            front, count=1)
        if count != 1:
            sys.exit("mdllm: AGENTS.md template must declare one git.autopush choice")
        return front + rendered[front_end:]

    # Everything above this line is projection/precondition work only. The
    # nested repo and its exact outer-isolation commit land before any domain
    # template does, matching the hard hook's transaction order.
    progress.stage = "outer isolation"
    isolation = _preflight_outer_isolation(target)
    isolated_in = _initialise_and_isolate(target, isolation)
    progress.isolation_landed = True
    progress.outer_root = isolated_in
    progress.stage = "domain rendering"
    broken: list[str] = []

    (target / "things").mkdir(parents=True, exist_ok=True)
    (target / "skills").mkdir(exist_ok=True)
    written: list[str] = []
    birth_paths: list[str] = []
    (target / "AGENTS.md").write_text(
        instantiate_agents(
            (templates / "AGENTS.md.template").read_text(encoding="utf-8")),
        encoding="utf-8", newline="\n")
    written.append("AGENTS.md")
    birth_paths.append("AGENTS.md")
    # A domain has ONE entry file. Some harnesses auto-load a differently named
    # one instead, and a domain they cannot see is a domain that does not run —
    # so every selection, `none` included, is born with the pointers that route
    # those harnesses back to AGENTS.md. This is the entry surface, not adapter
    # hardening: the pointer costs a few bytes when it is redundant, and costs
    # the whole domain when it is missing (2026-08-16 Phase 6 finding). WHICH
    # pointers exist is data in templates/entry/ — never a vendor name here.
    for src in entry_pointers:
        (target / src.stem).write_text(
            instantiate(src.read_text(encoding="utf-8")),
            encoding="utf-8", newline="\n")
        written.append(src.stem)
        birth_paths.append(src.stem)
    (target / "things" / "_schema.yaml").write_text(
        (templates / "_schema.yaml.template").read_text(encoding="utf-8")
        .replace("[domain-name]", name),
        encoding="utf-8", newline="\n")
    written.append("things/_schema.yaml")
    birth_paths.append("things/_schema.yaml")
    for t in sorted(templates.glob("domain-*.skill.md.template")):
        out_name = t.name.replace("domain-", f"{name}-", 1)
        out_name = out_name[:-len(".template")]
        (target / "skills" / out_name).write_text(
            instantiate(t.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        written.append(f"skills/{out_name}")
        birth_paths.append(f"skills/{out_name}")

    # Deliberate-ritual shortcut projections (inert until the operator invokes
    # them). WHERE each file belongs is the adapter's knowledge; the placeholder
    # substitution and the writes stay here with every other template. The
    # auto-firing lifecycle adapter stays opt-in (hint printed below).
    # Every adapter capability is a declared port, tested with isinstance —
    # an adapter without shortcuts simply projects none (v1.6).
    for relpath, src in adapter_shortcuts:
        dst = target / relpath
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(instantiate(src.read_text(encoding="utf-8")),
                       encoding="utf-8", newline="\n")
        written.append(relpath)
        birth_paths.append(relpath)

    # Reasoning prompts (orchestration.md): the generated session-start block
    # names `evaluate-triggers`, `surface-attention`, `session-orientation`,
    # `domain-velocity` (and the rituals name more) — until v3.24.0 scaffold
    # never delivered them, so every domain was born instructed to run prompts
    # it did not have (2026-08-01 estate sweep). They are things (type: prompt)
    # and land in the domain's own corpus.
    if (templates / "prompts").is_dir():
        pr_dir = target / "prompts"
        pr_dir.mkdir(exist_ok=True)
        for src in sorted((templates / "prompts").glob("*.md")):
            text = instantiate(src.read_text(encoding="utf-8"))
            # The relational graph is stripped on egress (thing.md, `exposed`):
            # a prompt's linked_things point into the FRAMEWORK's id space and
            # would dangle in the domain's separate corpus — same rule the
            # membrane applies to every thing that crosses a boundary.
            text = re.sub(r"(?m)^linked_things:\n(?:[ \t]+.*\n)+", "", text)
            (pr_dir / src.name).write_text(text, encoding="utf-8", newline="\n")
            written.append(f"prompts/{src.name}")
            birth_paths.append(f"prompts/{src.name}")

    # Fill the domain-kernel managed blocks now that skills AND prompts exist,
    # so the entry file is born in sync — the tier-routing block routes both
    # from the filesystem, and filling it before prompts/ landed would make
    # the birth commit drift against its own fresh build (the pre-commit
    # coherence check would rightly block it).
    ag = target / "AGENTS.md"
    ag_text = ag.read_text(encoding="utf-8")
    ag_meta, _, _ = parse_frontmatter(ag_text)
    ag_filled, _, _ = apply_domain_kernel(
        ag_text, build_domain_kernel_blocks(target, ag_meta or {}))
    ag.write_text(ag_filled, encoding="utf-8", newline="\n")

    # Lifecycle adapter: render the default harness's managed artifacts so a
    # new domain is hardened out of the box — startup context and post-write
    # feedback per the inward lifecycle bindings. The adapter owns the vendor
    # format; the bytes are written verbatim here. Still optional in spirit:
    # delete the artifacts and the domain kernel drives both by interpretation.
    # Scaffold writes directly (it runs as the tool, not through a
    # permissions-gated editor).
    for relpath, data in adapter_artifacts:
        dst = target / relpath
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        written.append(relpath)
        birth_paths.append(relpath)

    # Disclosure boundary (boundary-disclosure-check plan): a domain is born
    # with its own LOCAL terms file — per-repo boundaries; a domain's disclosure
    # surface is its own — and a .gitignore that keeps it local BEFORE the
    # exact-path first commit, so the vocabulary never enters any repo,
    # including the domain's own.
    bt_template = boundary_template
    if bt_template.is_file():
        (target / TERMS_FILE).write_text(
            bt_template.read_text(encoding="utf-8"),
            encoding="utf-8", newline="\n")
        gi_d = target / ".gitignore"
        gi_existing = gi_d.read_text(encoding="utf-8") if gi_d.is_file() else ""
        if TERMS_FILE not in {ln.strip() for ln in gi_existing.splitlines()}:
            gi_d.write_text(
                gi_existing.rstrip("\n") + ("\n" if gi_existing else "")
                + f"# local disclosure boundary — never committed\n{TERMS_FILE}\n",
                encoding="utf-8", newline="\n")
        written.append(f".gitignore (+ local {TERMS_FILE}, never committed)")
        birth_paths.append(".gitignore")

    # Private-by-default at birth: register the newborn's NAME in the framework
    # root's own local terms file, so framework commits cannot mention it until
    # the operator deletes the line — making publication an explicit decision
    # rather than a default. Same invariant as the .gitignore step above: which
    # domains exist is domain state, and it reaches the framework repo only as
    # a local, uncommitted fact.
    fw_terms = fw_root / TERMS_FILE
    fw_existing = (fw_terms.read_text(encoding="utf-8")
                   if fw_terms.is_file() else "")
    fw_terms_present = {ln.split("==>")[0].strip().lower()
                        for ln in fw_existing.splitlines()
                        if ln.strip() and not ln.strip().startswith("#")}
    if name.lower() not in fw_terms_present:
        if not fw_existing and bt_template.is_file():
            fw_existing = bt_template.read_text(encoding="utf-8")
        fw_terms.write_text(
            fw_existing.rstrip("\n") + ("\n" if fw_existing else "")
            + f"{name}\n", encoding="utf-8", newline="\n")

    progress.stage = "hook installation"
    hook_via = install_hook(target)
    progress.stage = "domain staging"
    first = None
    try:
        transaction = RepositoryTransaction.begin(target)
        progress.stage = "first commit"
        first = transaction.commit_exact(
            tuple(birth_paths),
            f"scaffold: {name} — framework v{fw_version}")
    except RepositoryTransactionError as exc:
        broken.append(
            "first domain exact commit failed — generated files remain "
            f"uncommitted and recoverable ({exc})")

    print(f"## Scaffolded {name} — {target}\n")
    for w in written:
        print(f"  wrote {w}")
    print(f"  git repo initialised; pre-commit hook installed (mdllm via {hook_via})")
    print(f"  autopush: {autopush_choice} (explicit birth authority)")
    if isolated_in:
        print(f"  isolated: {isolated_in / '.gitignore'} ignores the domain")
    if first is not None:
        print(f"  first commit made (framework_version_seen: {fw_version})")
        if first.post_commit_detail:
            print(f"  NOTE  {first.post_commit_detail}")
    for b in broken:
        print(f"  FAIL  {b}")
    print("\nStill yours (and your agent's) — the semantic half:")
    print("  - AGENTS.md: name, description, principles, thing types")
    print("  - things/_schema.yaml: declare your types and status vocabularies")
    print("  - skills/: fill the four skill bodies with the domain's reasoning")
    print("  - things/: create the first real things")
    print("  - a remote, if the domain should have one")
    print("  - run `mdllm session-start .` before your next commit: this domain "
          "is born with `session_gate: strict` (v3.28.0), so from the second "
          "commit on, the floor requires a fresh session-start attestation — "
          "the birth commit you just saw was the only exempt one")
    for adapter in selected_adapters:
        if isinstance(adapter, ScaffoldNoticePort):
            print(adapter.scaffold_guidance())
    if broken:
        print("\nBIRTH SEQUENCE INCOMPLETE — isolation state remains intact "
              "(including an accepted outer rule where applicable); the "
              "retained domain files and hooks are recoverable. Fix the FAIL "
              "lines before using the domain.")
    if not broken:
        progress.stage = "complete"
    return 1 if broken else 0
