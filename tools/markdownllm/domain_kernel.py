"""Domain-kernel managed blocks — the generated operative sections of a
domain's AGENTS.md.

The domain entry file (AGENTS.md) is the harness-loaded surface. Its
operative sections are generated into managed `<!-- generated:NAME -->`
blocks so the session-start imperative is never buried and cannot accumulate
residue across refreshes — the same drift-safe-by-construction property as
derived indexes and kernel.md. The generator owns ONLY the managed blocks;
frontmatter and authored identity outside them are preserved verbatim.
Anchor vocabulary follows orchestration.md. Opt-in: a domain whose AGENTS.md
has no managed blocks is left untouched and still boots by interpretation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .model import parse_frontmatter
from .repo import TIERS

DOMAIN_KERNEL_BLOCKS = ("standing-truth", "session-start", "tier-routing",
                        "hooks", "floor")

_FRAMEWORK_HARD_HOOKS = (
    "- `post-write:commit` — commit every created/modified frontmatter `.md` to the "
    "owning repo before completing the response. Anchor: `git-fs` (validation via the "
    "pre-commit hook) + `interpretation` (the commit act itself).\n"
    "- `session-start:version-check` — performed in **Session Start** above. "
    "Anchor: `harness-session`.\n"
    "- `pre-domain-scaffold:isolate` — new domains are born via `mdllm scaffold`. "
    "Anchor: `git-fs`.")


def _gen_block_re(name: str) -> "re.Pattern":
    return re.compile(
        r"(<!--\s*generated:" + re.escape(name) + r"\s*-->[ \t]*\n)"
        r"(.*?)"
        r"(\n[ \t]*<!--\s*/generated:" + re.escape(name) + r"\s*-->)",
        re.DOTALL)


def _dk_standing_truth(domain: Path, meta: dict) -> str:
    return (
        "You predict the next move — the next token, sentence, or action — from the "
        "stream of what comes next. You cannot predict its *consequence* the same way. "
        "Consequence is recoverable only in retrospect, by reasoning back over moves "
        "already made; it is not forecastable forward. Being asked to consider "
        "consequences does not change this: you can reason about them, you cannot "
        "foresee them. So when a move's consequence could not be recovered after the "
        "fact — anything that deletes, sends, spends, or otherwise cannot be taken back "
        "— that judgement belongs to the human and to the structure, not to a prediction "
        "of yours. Reach for the structure; defer the irreversible. This is orientation, "
        "not a hook the floor enforces. Full reasoning: "
        "`{framework_root}/things/insights/consequence-is-recoverable-only-in-retrospect.md`.")


def _dk_session_start(domain: Path, meta: dict) -> str:
    return (
        "**Run this before responding to the user's first request — the live request "
        "will pull you toward itself; resist until these are done.**\n\n"
        "0. **Estate sync** — `session-start:estate-sync` (anchor `interpretation`; "
        "an adapter may have run it already). If this domain is worked from more "
        "than one machine, run `python {framework_root}/tools/mdllm.py estate-sync .` "
        "*before* anything below — orientation and velocity read `git log`, and the "
        "log is only whole after the fetch. Fast-forwards are taken silently; "
        "DIVERGED/dirty are reported for the operator, never resolved; offline "
        "degrades to an advisory line. Never push.\n"
        "1. Load `{framework_root}/kernel.md` — the operative kernel (rules without "
        "rationale). The hard hooks it carries are always active.\n"
        "2. Read the **open loops (forward)** the orientation generates — non-terminal "
        "work things + open conflicts, computed from the graph (`mdllm session-start`). "
        "Backward history is the commit stream (velocity); insight "
        "liveness is a graph property — see session-memory.md. (continuity.md is retired.)\n"
        "3. **Version check** — `session-start:version-check` (anchor `harness-session`). "
        "Read `{framework_root}/.markdownllm` `version`; compare to `framework_version_seen` "
        "in this file's frontmatter. On mismatch: surface it, run "
        "`python {framework_root}/tools/mdllm.py validate .`, then offer "
        "`{framework_root}/domain-refresh.md`.\n"
        "4. **Orientation** — `session-orientation`: summarise what changed since last "
        "session (new things, status transitions) and run the scoped insight-staleness "
        "check (live insights — `active`, with a live inbound edge — × things changed "
        "since they were last touched).\n"
        "5. **Velocity** — `domain-velocity`, the counterpart to orientation: read `git log` "
        "over `things/` for what *should* have moved and hasn't (stalls, churn, untouched "
        "commitments). One line if the domain is healthy.\n"
        "6. **Triggers + attention** — `evaluate-triggers` then `surface-attention` (which "
        "consumes orientation's snapshot): scan things (or `things/_index/triggers.md` at "
        "scale) for fired conditions and order what needs the user.\n"
        "7. Then await intent.")


def _dk_tier_routing(domain: Path, meta: dict) -> str:
    t1 = TIERS["Tier 1 (full specs, load individually on demand)"]
    t2 = TIERS["Tier 2 (on demand)"]
    skills = (sorted(p.name for p in (domain / "skills").glob("*.skill.md"))
              if (domain / "skills").is_dir() else [])
    t1_specs = " · ".join(f"`{{framework_root}}/{n}`" for n in t1)
    skills_line = (" · ".join(f"`skills/{s}`" for s in skills)
                   if skills else "_(none yet)_")
    t2_specs = " · ".join(f"`{{framework_root}}/{n}`" for n in t2)
    return (
        "**Tier 0 — always:** `AGENTS.md` (this file) · `{framework_root}/kernel.md`\n\n"
        "**Tier 1 — load a full spec only when the kernel doesn't settle it:** "
        + t1_specs + "\n\n"
        "**Domain skills — load those relevant to session intent:** " + skills_line + "\n\n"
        "**Tier 2 — on demand:** " + t2_specs)


def _dk_hooks(domain: Path, meta: dict) -> str:
    parts = ["**Framework hard hooks (always active by config; anchor decides "
             "enforcement):**\n" + _FRAMEWORK_HARD_HOOKS]
    dh = meta.get("hard_hooks") or []
    if isinstance(dh, list):
        lines = []
        for h in dh:
            if not isinstance(h, dict):
                continue
            action = str(h.get("action", "")).rstrip()
            if action and not action.endswith((".", "!", "?")):
                action += "."
            lines.append(f"- `{h.get('hook', '?')}` — {action} "
                         f"Anchor: `{h.get('anchor', 'interpretation')}`.")
        if lines:
            parts.append("**Domain hard hooks:**\n" + "\n".join(lines))
    parts.append(
        "**Deliberate rituals — you invoke these; they never fire automatically:**\n"
        "- Session end → `session-end-continuity` (extract insights, disposition the "
        "standing insights, detect conflicts, manage open-loop things). Invoke via `/end-session` or natural "
        "language *when you judge the session worth harvesting* — the operator decides "
        "when a session is worth it, not the floor.\n"
        "- Retrospective → `detect-conflicts` (scan) + `review-schema-coherence`, when "
        "writing a `type: retrospective`.")
    return "\n\n".join(parts)


def _dk_floor(domain: Path, meta: dict) -> str:
    return (
        "Structure (`id`/`type`/`status`/`created`), reference integrity, and schema "
        "conformance are owned by `python {framework_root}/tools/mdllm.py validate .` and "
        "enforced by the git pre-commit hook — never re-perform them by reasoning. Your "
        "validation duty is semantic only (metadata–narrative consistency, scope, "
        "staleness, duplicates); see `{framework_root}/validate.thing.md`.")


_DK_BUILDERS = {
    "standing-truth": _dk_standing_truth,
    "session-start": _dk_session_start,
    "tier-routing": _dk_tier_routing,
    "hooks": _dk_hooks,
    "floor": _dk_floor,
}


def build_domain_kernel_blocks(domain: Path, meta: dict) -> dict:
    """Canonical body for each managed block — the single source the generator
    writes and the drift check compares against, so the two cannot disagree."""
    return {name: _DK_BUILDERS[name](domain, meta) for name in DOMAIN_KERNEL_BLOCKS}


def domain_kernel_status(text: str, blocks: dict) -> tuple[list, list]:
    """(present_block_names, drifted_block_names) for an AGENTS.md text."""
    present, drifted = [], []
    for name, body in blocks.items():
        m = _gen_block_re(name).search(text)
        if not m:
            continue
        present.append(name)
        if m.group(2).strip() != body.strip():
            drifted.append(name)
    return present, drifted


def apply_domain_kernel(text: str, blocks: dict) -> tuple[str, list, list]:
    """Splice canonical bodies into the managed blocks. Returns (new_text,
    written, missing). Everything outside the blocks is preserved verbatim."""
    written, missing = [], []
    out = text
    for name, body in blocks.items():
        rx = _gen_block_re(name)
        if not rx.search(out):
            missing.append(name)
            continue
        out = rx.sub(lambda m: m.group(1) + body + m.group(3), out, count=1)
        written.append(name)
    return out, written, missing


def cmd_domain_kernel(args) -> int:
    """Generate/refresh the managed operative blocks in a domain's AGENTS.md."""
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    if not agents.is_file():
        sys.exit(f"mdllm: no AGENTS.md in {domain}")
    text = agents.read_text(encoding="utf-8")
    meta, _, err = parse_frontmatter(text)
    if err:
        sys.exit(f"mdllm: AGENTS.md frontmatter error — {err}")
    blocks = build_domain_kernel_blocks(domain, meta or {})

    if args.check:
        present, drifted = domain_kernel_status(text, blocks)
        if not present:
            print(f"domain-kernel: no managed blocks in {agents.name} — not kernel-shaped "
                  f"(opt-in; nothing to check)")
            return 0
        if drifted:
            print("domain-kernel: DRIFT — managed blocks differ from a fresh build: "
                  + ", ".join(drifted)
                  + f"\n  run `mdllm domain-kernel {args.path}` and commit the result")
            return 1
        print(f"domain-kernel: in sync ({len(present)} block(s))")
        return 0

    new_text, written, missing = apply_domain_kernel(text, blocks)
    if not written:
        print(f"domain-kernel: no `<!-- generated:NAME -->` blocks found in {agents.name}.\n"
              f"  Add the managed blocks (see templates/AGENTS.md.template) where you want "
              f"the generated operative sections, then re-run. Authored content outside the "
              f"blocks is always preserved.")
        return 1
    if new_text != text:
        agents.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"domain-kernel: wrote {len(written)} block(s) into {agents.name}: "
          + ", ".join(written))
    if missing:
        print("  blocks not present (skipped): " + ", ".join(missing))
    return 0
