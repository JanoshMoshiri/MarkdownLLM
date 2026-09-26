"""Can this clone see its whole history? — the question every git read owes.

Most of the floor reads the commit stream as ground truth: structural pins
resolve against it, velocity and stall lines are computed from it, the
born-verified check finds a thing's creation commit in it, conflict age and
retrospective cadence read dates off it. All of that assumes the clone holds
the history. A **shallow clone** does not, and it fails in the worst way:
git still answers, confidently, from a truncated stream.

The lived instance (Claude Code cloud session, 2026-09-24): the harness
cloned the framework root at depth 50 of 938 commits. `validate` reported 148
Errors — every pin older than the shallow boundary "resolves to no commit" —
and 3 born-verified Warnings, because the grafted boundary commit looks like
the creation commit of every file older than it. Session-start's velocity
read `0 · 3 · 21 · 17` against a true `44 · 14 · 21 · 17`, and its whole
stall section vanished: every old file appeared touched on the boundary
date, so nothing had been untouched for 21 days. Nothing said the clone was
shallow. That is `a-check-run-where-it-cannot-see-mints-a-false-finding` by a
second mechanism: the first was a single-repo container that could not see
its siblings; this one could not see its own past.

The existing degraded-environment rule covered "git cannot be consulted at
all". Shallow is the case it missed — git *can* be consulted, and answers
wrongly. This module is the one place that question is asked, so every
consumer asks it the same way:

* ``estate-sync`` repairs it: completing history is a fetch of state already
  real on the remote — the same transport argument as a fast-forward.
* ``doctor`` and ``session-start`` say so loudly when the repair did not
  happen (offline, no remote, a budget exhausted).
* checks whose answer depends on history before the boundary report that
  they could not look, instead of minting a finding.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from dataclasses import dataclass
from pathlib import Path

UNSHALLOW_REMEDY = "`git fetch --unshallow`"


@dataclass(frozen=True)
class CloneDepth:
    """One observation of whether a clone holds its full history.

    ``shallow`` is None when the question could not be answered (not a git
    repository, git unavailable) — the null-result primitive: "could not ask"
    is never rendered as "full history".
    """

    shallow: bool | None
    boundaries: tuple[str, ...] = ()
    oldest_visible: dt.date | None = None

    @property
    def truncated(self) -> bool:
        return self.shallow is True

    def horizon(self) -> str:
        """Plain words for where visible history stops."""
        if self.oldest_visible is not None:
            return f"history before {self.oldest_visible.isoformat()} is absent"
        return "part of the history is absent"


def _git(root: Path, *args: str):
    try:
        return subprocess.run(["git", *args], cwd=root, capture_output=True,
                              text=True, encoding="utf-8", errors="replace")
    except OSError:
        return None


def clone_depth(root: Path) -> CloneDepth:
    """Ask git whether ``root``'s repository is shallow, and where it stops.

    ``--is-shallow-repository`` needs git 2.15+. Older git echoes an
    unsupported ``rev-parse`` option back instead of failing (the floor was
    fooled by exactly that once — `fix: old git echoes an unsupported option`),
    so only the literal answers ``true``/``false`` are believed; anything else
    falls back to the shallow file git itself maintains.
    """
    root = Path(root)
    out = _git(root, "rev-parse", "--is-shallow-repository")
    if out is None or out.returncode != 0:
        return CloneDepth(shallow=None)
    answer = out.stdout.strip()
    if answer == "false":
        # The common case costs exactly one spawn: this runs inside the
        # session-start hook, whose git-spawn budget is test-pinned.
        return CloneDepth(shallow=False)
    shallow_path = _git(root, "rev-parse", "--git-path", "shallow")
    shallow_file = None
    if shallow_path is not None and shallow_path.returncode == 0:
        candidate = Path(shallow_path.stdout.strip())
        shallow_file = candidate if candidate.is_absolute() else root / candidate
    if answer != "true":
        if shallow_file is None or not shallow_file.is_file():
            return CloneDepth(shallow=False)
    boundaries: tuple[str, ...] = ()
    if shallow_file is not None and shallow_file.is_file():
        boundaries = tuple(line.strip() for line in
                           shallow_file.read_text(encoding="utf-8").splitlines()
                           if line.strip())
    oldest = None
    if boundaries:
        dates = _git(root, "log", "--no-walk", "--format=%cs", *boundaries)
        if dates is not None and dates.returncode == 0:
            parsed = []
            for line in dates.stdout.split():
                try:
                    parsed.append(dt.date.fromisoformat(line.strip()))
                except ValueError:
                    continue
            oldest = min(parsed) if parsed else None
    return CloneDepth(shallow=True, boundaries=boundaries, oldest_visible=oldest)


def shallow_warning_text(depth: CloneDepth) -> str:
    """The one sentence every surface uses, so they cannot drift apart."""
    return (f"clone is SHALLOW — {depth.horizon()}, so every check that reads "
            f"git history (commit pins, verified flips, conflict age, "
            f"retrospective cadence, velocity, stall lines) sees a truncated "
            f"stream. Run {UNSHALLOW_REMEDY} (estate-sync does this when the "
            f"remote is reachable)")
