"""The session-start ritual, mechanically emitted.

The mechanical half of the session-start ritual, printed to stdout for a
harness SessionStart hook to inject (Claude Code; Copilot agent mode). This is
the HARDENING for the `session-start:version-check` hook whose anchor is
`harness-session`: a weak (or distracted) model receives the ritual at t=0
instead of having to recall it from a buried entry file. Optional — the
AGENTS.md prose stays the interpretation floor where no adapter is installed.
Read-only; safe on every session.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml

from .domain_kernel import build_domain_kernel_blocks, domain_kernel_status
from .model import TERMINAL_STATUSES, parse_frontmatter, scan
from .validation import version_tuple

def _velocity_signal(domain: Path) -> str:
    things = domain / "things"
    if not things.is_dir():
        return "no `things/` directory yet."
    last = subprocess.run(["git", "log", "-1", "--format=%cr|%s", "--", "things"],
                          cwd=domain, capture_output=True, text=True)
    if last.returncode != 0 or not last.stdout.strip():
        return "no committed history over `things/` yet."
    when, _, subj = last.stdout.strip().partition("|")
    cnt = subprocess.run(["git", "rev-list", "--count", "--since=30.days", "HEAD",
                          "--", "things"], cwd=domain, capture_output=True, text=True)
    n = cnt.stdout.strip() if cnt.returncode == 0 else "?"
    return (f"last `things/` change {when} (\"{subj.strip()}\"); {n} commit(s) in 30d. "
            f"Read `git log -- things/` for the full picture.")


# Types that sit at a non-terminal status as a steady state (knowledge/reference),
# so they are NOT "open work" — excluded from the forward orientation view.
_ORIENT_KNOWLEDGE_TYPES = {"specification", "guide", "manifesto", "insight",
                           "retrospective", "index", "continuity-brief", "prompt",
                           "workflow-definition", "decision", "artifact"}


def _orient_forward(domain: Path) -> list[str]:
    """The forward half of orientation — the open loops the next session inherits,
    computed from the thing graph. Orient is the session-memory counterpart to
    change-reconciliation's work-content state: backward orientation is the commit
    stream (velocity), this is its forward complement (what is still open). Replaces
    the hand-maintained continuity brief (dissolve-continuity-into-reconciliation)."""
    try:
        corpus, _ = scan(domain)
    except Exception:
        return []
    conflicts, loops = [], []
    for t in corpus.things:
        typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
        if typ == "conflict" and status == "open":
            conflicts.append(t.id)
        elif typ not in _ORIENT_KNOWLEDGE_TYPES and status not in TERMINAL_STATUSES:
            loops.append((t.id, typ, status))
    lines: list[str] = []
    if conflicts:
        lines.append("- **Open conflicts (%d):** %s — resolve or carry forward."
                     % (len(conflicts), ", ".join(f"`{c}`" for c in sorted(conflicts))))
    if loops:
        lines.append(f"- **Open loops ({len(loops)}):** forward work still in flight —")
        for tid, typ, status in sorted(loops)[:15]:
            lines.append(f"    - `{tid}` ({typ}, {status})")
        if len(loops) > 15:
            lines.append(f"    - …and {len(loops) - 15} more (`mdllm validate` lists all).")
    return lines


def cmd_session_start(args) -> int:
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    meta = {}
    if agents.is_file():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        meta = meta or {}

    out = ["# MarkdownLLM — Session Start (run before the user's first request)", "",
           "The live request will pull you toward itself; do these first, then await intent:",
           "1. Load `kernel.md` (operative kernel).",
           "2. Act on the version + velocity (backward) and open-loops (forward) status below.",
           "3. Evaluate triggers and surface what needs the user.", ""]

    fr = meta.get("framework_root")
    if (domain / ".markdownllm").is_file():
        # This IS a framework root (it carries the sentinel), not a downstream
        # domain — `framework_root: .` points at itself, so the domain
        # version-check does not apply.
        fv = str((yaml.safe_load((domain / ".markdownllm").read_text(encoding="utf-8"))
                  or {}).get("version"))
        out.append(f"- **Version:** framework root (v{fv}) — not a downstream domain; "
                   f"no refresh applies.")
    elif not fr:
        out.append("- **Version:** n/a — no `framework_root` in AGENTS.md.")
    else:
        sentinel = (domain / fr).resolve() / ".markdownllm"
        if not sentinel.is_file():
            out.append(f"- **Version:** unknown — `framework_root` `{fr}` has no .markdownllm.")
        else:
            fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}).get("version"))
            seen = str(meta.get("framework_version_seen", ""))
            if not seen:
                out.append(f"- **Version: STALE** — framework v{fv}; domain has no "
                           f"`framework_version_seen`. Run `mdllm refresh .` and adopt.")
            elif version_tuple(seen) != version_tuple(fv):
                out.append(f"- **Version: MISMATCH** — framework v{fv}; domain last saw "
                           f"v{seen}. Validate the domain, then `mdllm refresh .` → adopt "
                           f"→ `--seal`.")
            else:
                out.append(f"- **Version: in sync** (framework v{fv}).")

    out.append(f"- **Velocity:** {_velocity_signal(domain)}")

    if agents.is_file():
        _, drifted = domain_kernel_status(
            agents.read_text(encoding="utf-8"),
            build_domain_kernel_blocks(domain, meta))
        if drifted:
            out.append(f"- **Domain kernel: DRIFT** in {', '.join(drifted)} — run "
                       f"`mdllm domain-kernel .` and commit.")

    out.extend(_orient_forward(domain))

    print("\n".join(out))
    return 0
