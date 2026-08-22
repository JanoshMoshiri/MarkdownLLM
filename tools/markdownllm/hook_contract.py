"""Leaf contracts shared by hook producers, executors, and diagnosers.

One owner for the hook byte contract (floor-structure-residue item 3, landed
sprint 2): the interpreter-candidate policy, the emitted sh resolution
fragment, the three managed git-hook bodies, and the rendering that turns
them into exact trusted bytes all live here. Scaffold (the producer) installs
these bytes; runtime (the executor) probes the same candidate policy from the
Python side; doctor and session (the diagnosers) compare installed bytes
against them. None of those consumers reaches back into another.

This module imports only the ports contract (`harness_ports`, itself
stdlib-pure) — never a producer or executor module.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from .harness_ports import LAUNCH_RESOLUTION_SECONDS


MDLLM_ENTRY = Path(__file__).resolve().parents[1] / "mdllm.py"

# The dependency that makes an interpreter *usable* by the floor, not merely
# present. One name, probed everywhere the floor may run.
FLOOR_DEPENDENCY = "yaml"


@dataclass(frozen=True)
class HookByteContract:
    """Exact trusted bytes for zero or more Git hook names."""

    entries: tuple[tuple[str, bytes], ...] = ()

    @classmethod
    def from_mapping(cls, hooks: Mapping[str, bytes]) -> "HookByteContract":
        return cls(tuple(sorted((str(name), bytes(body))
                                for name, body in hooks.items())))

    def expected(self, name: str) -> bytes | None:
        return next((body for hook, body in self.entries if hook == name), None)


# --------------------------------------------- interpreter candidate policy
# Emitted into every hook body after ROOT and MDLLM are set. Kept free of
# braces so the surrounding template's .format(rel=...) passes it through.
# Candidate order: domain-local environment first (a domain that manages its
# own venv wins), then the framework-root environment derived from MDLLM,
# then PATH interpreters. POSIX and Windows venv layouts are both covered.
# The framework root comes from parameter expansion, NOT dirname: managed
# Git-hook shells (Codex, Phase 2B finding) run without the external utility
# set on PATH, and $MDLLM always ends tools/mdllm.py, so stripping the last
# two path components is exact and needs no subprocess at all.
@dataclass(frozen=True)
class InterpreterCandidate:
    """One candidate as executable plus immutable prefix arguments."""

    executable: str
    prefix_args: tuple[str, ...] = ()

    def command(self, *args: str) -> list[str]:
        return [self.executable, *self.prefix_args, *args]


RELATIVE_CANDIDATES: tuple[tuple[str, str, str], ...] = (
    ("root", ".venv/bin/python", "posix"),
    ("root", ".venv/Scripts/python.exe", "windows"),
    ("framework", ".venv/bin/python", "posix"),
    ("framework", ".venv/Scripts/python.exe", "windows"),
)
PATH_CANDIDATES: tuple[tuple[InterpreterCandidate, str], ...] = (
    (InterpreterCandidate("python3"), "any"),
    (InterpreterCandidate("python"), "any"),
    (InterpreterCandidate("py", ("-3",)), "windows"),
)


def _render_sh_resolve() -> str:
    """Encode the neutral candidate policy for an sh-compatible edge."""
    lines = [
        'FW="${MDLLM%/*/*}"', 'PY=""', 'PY_PREFIX=""',
        'MDLLM_LAUNCH_DEADLINE=""', 'MDLLM_DATE=""', 'MDLLM_TIMEOUT=""',
        'if [ -x /usr/bin/date ] && [ -x /usr/bin/timeout ]; then',
        '  MDLLM_DATE=/usr/bin/date',
        '  MDLLM_TIMEOUT=/usr/bin/timeout',
        'elif timeout --version >/dev/null 2>&1 && '
        'date +%s >/dev/null 2>&1; then',
        '  MDLLM_DATE=date',
        '  MDLLM_TIMEOUT=timeout',
        'fi',
        'if [ -n "$MDLLM_DATE" ] && [ -n "$MDLLM_TIMEOUT" ]; then',
        f'  MDLLM_LAUNCH_DEADLINE=$(( $("$MDLLM_DATE" +%s) + '
        f'{LAUNCH_RESOLUTION_SECONDS} ))',
        'fi',
        'mdllm_probe() {',
        '  [ -n "$MDLLM_LAUNCH_DEADLINE" ] || return 1',
        '  mdllm_remaining=$(( MDLLM_LAUNCH_DEADLINE - '
        '$("$MDLLM_DATE" +%s) ))',
        '  [ "$mdllm_remaining" -gt 0 ] || return 1',
        f'  "$MDLLM_TIMEOUT" "$mdllm_remaining" "$@" -c "import {FLOOR_DEPENDENCY}" '
        '>/dev/null 2>&1',
        '}',
    ]
    specs: list[tuple[str, tuple[str, ...], str]] = []
    for anchor, suffix, platform in RELATIVE_CANDIDATES:
        base = "$ROOT" if anchor == "root" else "$FW"
        specs.append((f"{base}/{suffix}", (), platform))
    specs.extend((candidate.executable, candidate.prefix_args, platform)
                 for candidate, platform in PATH_CANDIDATES)
    # MSYSTEM is the positive Git-for-Windows shell signal observed by the
    # live Claude dispatch probe. Unlike inherited COMSPEC/Windows PATH
    # entries, it is absent in native WSL/POSIX shells.
    lines.append('MDLLM_WINDOWS_SH="${MSYSTEM:-}"')
    for executable, prefix, platform in specs:
        quoted = f'"{executable}"' if executable.startswith("$") else executable
        prefix_text = " ".join(f'"{arg}"' for arg in prefix)
        command = " ".join(part for part in
                           ('mdllm_probe', quoted, prefix_text) if part)
        platform_guard = ('[ -n "$MDLLM_WINDOWS_SH" ] && '
                          if platform == "windows" else "")
        # Existence-guard before the spawn (floor-structure-residue, landed
        # sprint 2): probing a candidate that cannot exist still paid a
        # timeout+python spawn (~330ms per dead file-path candidate on
        # Windows). Both guards are shell builtins — a file candidate is
        # tested with [ -x ], a PATH name with command -v — so an absent
        # candidate now costs no process at all.
        existence_guard = (
            f'[ -x {quoted} ] && ' if executable.startswith("$")
            else f'command -v {executable} >/dev/null 2>&1 && ')
        lines.append(
            f'if [ -z "$PY" ] && {platform_guard}{existence_guard}'
            f'{command}; then')
        lines.append(f'  PY="{executable}"')
        if prefix:
            lines.append(f'  PY_PREFIX="{prefix[0]}"')
        lines.append("fi")
    lines.extend((
        "mdllm_python() {",
        '  if [ -n "$PY_PREFIX" ]; then',
        '    "$PY" "$PY_PREFIX" "$@"',
        "  else",
        '    "$PY" "$@"',
        "  fi",
        "}",
    ))
    return "\n".join(lines)


SH_RESOLVE = _render_sh_resolve()


# ------------------------------------------------------ managed hook bodies
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
# Interpreter resolution (one owner: markdownllm/hook_contract.py — the
# comment there explains the candidate order and why the probe imports the
# floor's real dependency rather than just proving an interpreter exists).
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
# All four floor legs — boundary, validate, coherence (blocking) and the
# change-reconciliation candidates advisory (never blocking) — run
# CONCURRENTLY against the frozen candidate through one coordinator. The
# legs are the same CLI commands with the same arguments and inherit the
# frozen-index environment above; per-leg output, messages, and semantics
# are unchanged (mdllm precommit composes, never reimplements). Wall time
# is the slowest leg, not the sum of four (floor-sprint-1 F11 / remedy 3C).
mdllm_python "$MDLLM" precommit "$ROOT" || exit 1
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

# Interpreter resolution has ONE owner (this module); substituted here once so
# every consumer — install_hook's writes, doctor's currency comparison — sees
# the same final bytes. Only {rel} remains for per-repo formatting, so the
# fragment's shell braces (${MDLLM%/*/*}) are doubled to survive .format().
_SH_RESOLVE_ESCAPED = SH_RESOLVE.replace("{", "{{").replace("}", "}}")
HOOK_BODY = HOOK_BODY.replace("{resolve}", _SH_RESOLVE_ESCAPED)
POST_COMMIT_HOOK_BODY = POST_COMMIT_HOOK_BODY.replace(
    "{resolve}", _SH_RESOLVE_ESCAPED)
COMMIT_MSG_HOOK_BODY = COMMIT_MSG_HOOK_BODY.replace(
    "{resolve}", _SH_RESOLVE_ESCAPED)


HOOK_BODIES = {
    "pre-commit": HOOK_BODY,
    "commit-msg": COMMIT_MSG_HOOK_BODY,
    "post-commit": POST_COMMIT_HOOK_BODY,
}

HOOK_MARKERS = {
    "pre-commit": "# mdllm pre-commit:",
    "commit-msg": "# mdllm commit-msg:",
    "post-commit": "# mdllm post-commit:",
}


# ------------------------------------------------- contract rendering + paths
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


def rendered_hook_contract(root: Path) -> HookByteContract:
    """Return the exact managed hook bytes trusted for ``root``."""
    rel = hook_mdllm_route(root)
    return HookByteContract.from_mapping({
        name: body.format(rel=rel).encode("utf-8")
        for name, body in HOOK_BODIES.items()
    })
