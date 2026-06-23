# Plan: Domain Kernel + Harness Hardening Foundation

> **Durable execution record.** This plan lives in-repo so it survives context
> compaction. Progress is tracked in the table below; per-change commits are the
> ledger of work done; `continuity.md` captures mid-phase position. After any
> compaction, reconstruct state from these three — not the context window.

## Progress

| Phase | Status | Notes |
|---|---|---|
| 1 — Taxonomy: anchor-primary | ⏳ in progress | started 2026-06-23 |
| 2 — Domain kernel + generator | ⬜ not started | |
| 3 — Session-start adapter | ⬜ not started | |
| 4 — Deliberate slash commands | ⬜ not started | |
| 5 — Rollout via existing rails | ⬜ not started | |

Legend: ⬜ not started · ⏳ in progress · ✅ done · ⚠ blocked

---

## Context

**The problem.** Domain agents skip their session-start ritual (load framework
kernel, version-check, velocity) — observed even on Opus in Claude Code, not just
weak models. Root cause is structural, not model-tier: session-start fires at the
same instant as the user's first message, and the live request always outranks a
standing instruction buried in a long, reference-heavy `AGENTS.md`. The framework
labels these "hard hooks," but their **anchor** is interpretation/session-lifecycle
— which `things/insights/hook-enforcement-has-three-anchors.md` already establishes
is *not enforced*. The label promised an enforcement the architecture never built.

**The fix, in layers.** (1) Make the entry surface a slim, *generated* **domain
kernel** so the imperative isn't drowned and can't accumulate residue. (2) Harden
session-start with an optional, harness-specific adapter that injects the ritual at
the real `SessionStart` event. (3) Keep session-end/retrospective **human-decided**
(slash command + natural language) — the operator chooses when a session is worth
harvesting; no automatic catch-up. (4) Correct the taxonomy so **anchor** (what
makes a hook fire) is primary and hard/soft is a config flag.

**Substrate, verified from the docs (2026-06):** target harnesses are **Claude
Code** and **Copilot in VS Code (agent mode)** — both inject at `SessionStart` and
inject+block at `PreToolUse`; VS Code Copilot reads `.claude/settings.json`
directly, so **one Claude-format adapter covers both**. Copilot cloud/CLI are off
the table (covered for free by the interpretation floor). Everything stays
**optional/additive** — a domain with no kernel/adapter still boots via
interpretation. Migration rides the existing `domain-refresh` rail on version bump.

**Out of scope (future, by request):** PreToolUse security/risk-reasoning hooks.
The foundation deliberately leaves PreToolUse free for them.

---

## Phase 1 — Taxonomy: anchor-primary (low blast radius)

Goal: stop "hard" implying "enforced." Two orthogonal attributes, both always
stated on a hook: **anchor** (`interpretation` | `git-fs` | `harness-session`) and
**config** (`hard` | `soft`). "hard + interpretation" becomes a valid, honest label
that flags a hardening candidate instead of hiding the gap.

- Edit `orchestration.md`: lead the Enforcement section with anchor; demote hard/soft
  to a config flag; annotate the 3 framework hard hooks and the Hook Points table
  with their anchor. Add optional `anchor:` to the `hard_hooks` / binding declaration
  syntax. **Edit the `<!-- kernel -->` block** to match.
- Regenerate `kernel.md` via `python tools/mdllm.py kernel .` (do **not** hand-edit
  `kernel.md` — it's generated).
- No domain files change. Rename nothing — terms stay; only framing + an additive
  attribute.
- Commit: `refine(taxonomy): anchor is primary, hard/soft is a config flag`.

## Phase 2 — Domain kernel + generator (risk concentrated here, fully testable)

Goal: the harness-loaded `AGENTS.md` becomes a slim, generated, kernel-shaped entry;
verbose reference moves to skills/specs. Authored identity preserved across
regenerations; framework-derived sections regenerate (residue-free by construction).

**Generator** — new `cmd_domain_kernel(args)` in `tools/mdllm.py`, mirroring
`cmd_kernel` (1601) and reusing `parse_frontmatter` (144), `TIERS` (933), and the
scaffold `instantiate()` substitution style (2022). Assembles `AGENTS.md` from:
- **Authored island (preserved):** frontmatter (`name`, `description`,
  `framework_root`, `framework_version_seen`, `git`) + identity block ("What This
  System Does", principles pointer, domain thing-types). Read from existing `AGENTS.md`
  between `<!-- authored -->` markers and re-emit verbatim.
- **Generated blocks (rewritten each run), delimited `<!-- generated:start/end -->`:**
  the consequence-blindness "Standing Truth" para; the **imperative session-start
  ritual first** (load `kernel.md` → version-check → velocity → evaluate-triggers →
  surface-attention → orientation); the **Tier table generated from `TIERS`**; the
  **hard-hook + anchor table** (Phase 1); bound-prompt declarations
  (`session-end-continuity`@session-end, retrospective bundle) **marked deliberate**;
  deterministic-floor note.
- Frontmatter on regen carries `generated`/`generated_from` SHA like `kernel.md`.
- `--check`: drift between on-disk generated blocks and a fresh build → exit 1.

**Template** — restructure `templates/AGENTS.md.template` into kernel shape with the
`<!-- authored -->` / `<!-- generated -->` markers (scaffold + generator share one source).

**Drift check** — extend `coherence_findings` (1671) with a corpus-general
domain-kernel check (Error on drift), inherited via the pre-commit hook — same shape
as the framework kernel-drift check (1732).

**Wire-up** — add `domain-kernel` subparser near `kernel` (2166). Tests in
`tools/tests/`: authored-island preservation, generated blocks deterministic,
`--check` catches drift, `TIERS` table matches.

**Prove it** — regenerate `domain/jmtm-software/AGENTS.md`. Confirm: line count drops;
identity preserved; `validate domain/jmtm-software` passes; `domain-kernel --check` in sync.

## Phase 3 — Session-start adapter (Claude Code + VS Code Copilot)
- New `cmd_session_start(args)`: version-check (both legs, reuse `cmd_refresh`/`cmd_doctor`
  logic) + velocity (`git log`), prints imperative + outputs to stdout for injection.
- Extend `adapters/claude-code.settings.example.json` (PostToolUse only today) with a
  `SessionStart` hook calling `mdllm session-start`. One Claude-format file serves both
  targets; add `.github/hooks/*.json` only if cloud/CLI wanted later.
- Optional/opt-in; interpretation remains the floor without an adapter.

## Phase 4 — Deliberate slash commands (human-decided; NO auto catch-up)
- `.claude/commands/end-session.md` → invoke `session-end-continuity`.
- `.claude/commands/retrospective.md` → `detect-conflicts` (scan) + `review-schema-coherence`.
- Copilot mirrors: `.github/prompts/{end-session,retrospective}.prompt.md`.
- session-end stays human-triggered (slash + NL) — operator decides when to harvest.

## Phase 5 — Rollout via existing rails
- `cmd_scaffold` (1991): instantiate generated kernel + optional adapter + optional
  slash commands at domain birth.
- `domain-refresh.md` + `cmd_refresh` (1169): regenerate the kernel when absorbing a
  framework version bump — the migration rail.
- `cmd_doctor` (1813): report domain-kernel staleness + adapter presence.
- Bump `.markdownllm` version (major) → version-check triggers refresh → kernels regenerate.

---

## Verification

- **Phase 1:** `mdllm kernel . --check` in sync; `mdllm coherence .` clean; orchestration
  reads coherently (anchor-primary).
- **Phase 2:** `mdllm domain-kernel domain/jmtm-software` then `git diff` (slims, identity
  intact) · `validate` passes · `domain-kernel --check` in sync · `pytest tools/tests` green.
- **Phase 3:** `mdllm session-start domain/jmtm-software` prints version + velocity +
  imperative; wire a test `.claude/settings.json`, start a real session, confirm the ritual
  fires unprompted (manual).
- **Phase 4:** invoke `/end-session`; confirm the continuity ritual runs.
- **Phase 5:** `scaffold` a throwaway domain → kernel/adapter/commands born; `doctor`
  reports staleness after a hand-edit; bump version → `refresh` regenerates a kernel.
