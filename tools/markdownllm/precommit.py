"""One pre-commit application boundary: the hook's legs, run concurrently.

The generated pre-commit hook freezes one candidate tree, then used to launch
boundary, validation, coherence, and the reconciliation-cue advisory as four
sequential interpreter processes. Every leg reads the same frozen tree, none
mutates anything, and each pays its own interpreter start — so the wall time
was the SUM of four legs when their independence makes it the MAX (the
consolidated remedy's 3C: one transaction implemented as several programs).

``mdllm precommit`` composes the existing legs without reimplementing them:
each child is the same CLI command with the same arguments and inherits the
same frozen-index environment, so per-leg output and semantics are
byte-identical to the sequential hook. The coordinator only decides
scheduling (concurrent), presentation (canonical order: boundary → validate
→ coherence → candidates), and the combined exit.

When invoked outside an already-frozen hook environment (a direct operator
run), the coordinator freezes the index itself and performs the same final
compare-and-swap the hook script performs, so one candidate is still one
candidate. It adds no semantic rule and owns no findings.
"""

from __future__ import annotations

import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .hook_contract import MDLLM_ENTRY
from .repository_view import (
    FROZEN_INDEX_ROOT_ENV,
    FROZEN_INDEX_TREE_ENV,
)

# (name, argv-suffix, blocking, failure message) — the exact wrapper messages
# the sequential hook printed, so a blocked commit reads identically.
_LEGS: tuple[tuple[str, tuple[str, ...], bool, str], ...] = (
    ("boundary", ("--quiet",), True,
     "mdllm: staged content crosses the disclosure boundary — commit blocked."),
    ("validate", ("--quiet", "--view", "index"), True,
     "mdllm: validation Errors — commit blocked. Fix or run with "
     "--no-verify (discouraged)."),
    ("coherence", ("--quiet", "--view", "index"), True,
     "mdllm: coherence Errors — a generated artifact (kernel/index) or the "
     "spec catalog is stale. Regenerate and re-commit, or --no-verify "
     "(discouraged)."),
    ("candidates", ("--view", "index"), False, ""),
)


def _git_write_tree(root: Path) -> str | None:
    out = subprocess.run(["git", "write-tree"], cwd=root,
                         capture_output=True, text=True)
    tree = (out.stdout or "").strip()
    return tree if out.returncode == 0 and tree else None


def _floor_entry() -> Path:
    """The entry the children must run: the one THIS process was launched
    from. In a nested estate the hook's ``$MDLLM`` may name a different
    framework checkout than the one this module was imported from — the
    coordinator must not silently substitute its own. Falls back to this
    checkout's entry when argv[0] is not a real file (embedded callers)."""
    candidate = Path(sys.argv[0]).resolve() if sys.argv and sys.argv[0] else None
    if (candidate is not None and candidate.name == "mdllm.py"
            and candidate.is_file()):
        return candidate
    return MDLLM_ENTRY


def _run_leg(name: str, suffix: tuple[str, ...], root: Path,
             env: dict, entry: Path) -> tuple[str, int, str]:
    proc = subprocess.run(
        [sys.executable, str(entry), name, str(root), *suffix],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=env, cwd=root)
    text = (proc.stdout or "")
    if proc.stderr:
        text += proc.stderr
    return name, proc.returncode, text


def cmd_precommit(args) -> int:
    root = Path(args.path).resolve()

    env = dict(os.environ)
    owns_freeze = FROZEN_INDEX_TREE_ENV not in env
    if owns_freeze:
        tree = _git_write_tree(root)
        if tree is None:
            print("mdllm: could not freeze the staged candidate — commit "
                  "blocked.")
            return 1
        env[FROZEN_INDEX_TREE_ENV] = tree
        env[FROZEN_INDEX_ROOT_ENV] = str(root)

    entry = _floor_entry()
    with ThreadPoolExecutor(max_workers=len(_LEGS)) as pool:
        results = list(pool.map(
            lambda leg: _run_leg(leg[0], leg[1], root, env, entry), _LEGS))

    by_name = {name: (code, text) for name, code, text in results}
    blocked = False
    for name, suffix, blocking, message in _LEGS:
        code, text = by_name[name]
        if text.strip():
            print(text.rstrip("\n"))
        if blocking and code != 0:
            print("")
            print(message)
            blocked = True
    if blocked:
        return 1

    if owns_freeze:
        current = _git_write_tree(root)
        if current is None:
            print("mdllm: could not re-read the staged candidate — commit "
                  "blocked.")
            return 1
        if current != env[FROZEN_INDEX_TREE_ENV]:
            print("")
            print("mdllm: the staged index changed while the floor was "
                  "running — commit blocked; retry against one candidate.")
            return 1
    return 0
