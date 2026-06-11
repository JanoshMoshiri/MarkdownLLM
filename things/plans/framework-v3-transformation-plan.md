---
id: framework-v3-transformation-plan
type: plan
status: in-progress
version: 1.0
created: 2026-06-11
priority: high
tags: [transformation, validation, provenance, tooling, roadmap]
linked_things:
  - id: validate-thing-specification
    relation: references
    notes: "Phase 1 delegates Levels 1-3 to deterministic tooling"
  - id: session-memory-specification
    relation: references
    notes: "Phase 4 adds the scoped insight-staleness check"
  - id: derived-index-specification
    relation: references
    notes: "Phase 5 applies the derived-index pattern to the spec corpus itself"
  - id: llm-driven-systems-manifesto
    relation: implements
    notes: "The plan operationalises 'LLM does reasoning, not mechanical parsing'"
---

# Framework v3 Transformation Plan

## What This Is

The phased plan to evolve the framework from a specification-only system into one
with a deterministic enforcement floor, first-class provenance, and measurable
behaviour. Produced from the full framework review of 2026-06-11, which found:

1. **The enforcement gap is live, not theoretical** — all 17 things in the
   jmtm-software domain fail `validate.thing.md` Level 1 status checks at Error
   severity, undetected, because the only validator is honor-system LLM reasoning.
2. **The status vocabulary is self-contradictory** — Level 1 hardcodes six workflow
   statuses as Error while Level 3 and live domain practice permit domain-defined
   state machines (see conflict: `status-vocabulary-universal-vs-domain`).
3. **Each failure mode has been answered with new prose machinery**, which adds
   cognitive load — the documented *cause* of hook non-compliance
   (`hook-compliance-correlates-with-scope-not-awareness`).

The through-line: Phase 1 gives the framework ground truth, Phase 2 gives it back
attention, Phase 3 gives it memory of *why*, Phases 5–7 convert all three into
speed, proactivity, and proof. The LLM ends up spending its reliability budget
exclusively on what only an LLM can do.

## Phases

### Phase 0 — Baseline and honesty pass ✅ COMPLETE (2026-06-11)
- [x] Write the framework's first `type: retrospective` (May–June period), folding in the review findings → `framework-retrospective-2026-06`
- [x] Create the framework's own `continuity.md` (prescribed by session-memory.md; never existed)
- [x] Record the status-vocabulary contradiction as the framework's first `type: conflict` thing → `status-vocabulary-universal-vs-domain`
- [x] Measure actual token costs per spec and per tier; replace asserted numbers in AGENTS.md with measured ones → Tier 0 = 13.5k, Tier 0+1 = 26.5k, full = 65.5k (`tools/measure-tokens.py`)
- [x] Tag the repo `v2.9-pre-floor`

**Done when:** retrospective committed, real token numbers in AGENTS.md, tag pushed.

### Phase 1 — The deterministic floor: `mdllm` CLI + normative schemas ✅ COMPLETE (2026-06-11)
- [x] Single-file Python CLI (`tools/mdllm.py`, PyYAML): `validate`, `triggers` (+ deadline horizon), `index check|rebuild`, `tokens` (absorbed measure-tokens.py), `install-hook`
- [x] Normative per-domain schema: framework `_schema.yaml` + jmtm `things/_schema.yaml` — types, status vocabularies, required fields, relation vocabulary, options
- [x] Status contradiction resolved: thing.md v2.11 + validate.thing.md v2.0 — domain-declared vocabularies; universal six as advisory default. Conflict thing resolved (`superseded`, guide's position survived)
- [x] jmtm-software vocabulary declared as correct (validates 0 Errors / 0 Warnings; 8 advisory orphan Infos remain for the domain agent)
- [x] Pre-commit hooks installed in framework + jmtm repos; **verified to block** a deliberately broken thing (exit 1)
- [x] validate.thing.md rewritten: tool owns mechanical floor; LLM keeps semantic layer; prompt I/O chain validation deleted
- [ ] Vendor adapters (`adapters/` — e.g. Claude Code PostToolUse) — deferred to Phase 7 alongside CI

**Verified:** framework 38/38 clean, jmtm 0 Errors, hook blocks broken things, framework bumped to v3.0.

### Phase 2 — The deletion pass ✅ COMPLETE (2026-06-11)
- [x] CHANGELOG generated: `mdllm changelog --since <tag>` drafts entries from structured commits; header documents the new process
- [x] REVIEWLOG migrated verbatim into `framework-retrospective-2026-05` (three May reviews); file deleted; WORKLOG link removed; validator confirmed zero broken references
- [x] Prompt input/output chain validation removed (done in Phase 1's validate.thing.md v2.0 rewrite)
- [x] Speculative trigger machinery pruned: `in_progress_count` condition + `warn_overload` action removed from trigger-specification.md v1.2 and from mdllm
- [ ] AGENTS.md version auto-mirrored from `.markdownllm` by tooling — deferred (manual for now; `.markdownllm` remains canonical)

**Result:** tracking surfaces are now git log, WORKLOG, continuity, retrospectives — plus a CHANGELOG that is drafted by tooling rather than remembered.

### Phase 3 — Provenance as a first-class spec ✅ COMPLETE (2026-06-11)
- [x] `provenance.md` (v1.0, draft): quarantine rule, `verified` flag, the pinning rule, enforcement table
- [x] `type: decision` framework-reserved (`made`/`superseded`); thing.md v2.12 adds `origin: external` + `verified`; template at `templates/decision.md.template`
- [x] The chain proven with a real record: `decision-status-vocabulary-domain-owned` — this session's actual resolution decision, inputs pinned to the commits they were read at
- [x] `mdllm provenance`: pin shape, commit existence, input existence (current or at-pin), quarantine, freshness (Info), unverified-external aging. Freshness check verified live — it correctly flagged the decision's inputs as changed-since-pin
- [x] Reverse-provenance index (`mdllm index rebuild --signal provenance`) built and committed
- [ ] First real jmtm filing through a decision record — lands with the next actual filing event (annual accounts, due 2026-07-31)

### Phase 4 — Scoped insight-staleness check ✅ COMPLETE (2026-06-11)
- [x] session-memory.md v1.1: Session-Start Staleness Check section — live insights × things changed since `last_updated`, no new cadence, full sweep stays at retrospective
- [x] session-orientation prompt v1.1: the check is Step 0 of the reasoning template

### Phase 5 — The operative kernel ✅ v1 COMPLETE (2026-06-11)
- [x] `<!-- kernel -->` blocks added to the six Tier 0/1 specs (thing, orchestration, validate, git-workflow, read, write)
- [x] `mdllm kernel` extracts blocks into provenance-stamped `kernel.md` (a derived index over the spec corpus)
- [x] Measured: kernel.md = **1.6k tokens** replacing **21.4k** of full Tier 0+1 specs (93% reduction); new Tier 0 (AGENTS.md + kernel.md) ≈ 5.3k vs 26.5k baseline — target met
- [x] Framework + jmtm AGENTS.md re-tiered: kernel at Tier 0, full specs load individually on demand; kernel regeneration added to the validation checklist
- [ ] Kernel blocks for Tier 2 specs (session-memory, belief-revision, provenance, triggers, derived-index) — next session; diminishing returns since they're demand-loaded

### Phase 6 — Behavioral evals ⚙ STAGE 1 COMPLETE (2026-06-11)
- [x] `mdllm eval --fixture`: deterministic assertion engine (thing_exists, status, field, link, validates_clean) — see `evals/README.md`
- [x] First fixture: `evals/jmtm-vat-2026q1-filed.yaml` — regression net over the completed VAT cycle, 6/6 passing against the live domain
- [ ] Stage 2: the full loop — seed a temp worktree, run a fresh headless agent session on the scenario prompt, assert the result. This is what makes spec changes measurable and enables the model experiment
- [ ] Grow to 5–10 fixtures per domain as workflows complete

### Phase 7 — New powers ⚙ ADAPTERS LANDED (2026-06-11)
- [x] Diff-driven regeneration *signal*: `mdllm provenance` freshness check + reverse-provenance index — verified live (it flagged the first decision's inputs as changed-since-pin the same day). Agent-offered re-runs ride on this
- [x] Proactive operation: `adapters/scheduled-triggers.ps1` — daily `mdllm triggers` with Windows toast on hits; registration via schtasks (one command, documented in the script)
- [x] CI: `.github/workflows/validate.yml` — validate + provenance + index drift on every push/PR
- [x] Claude Code vendor adapter example: `adapters/claude-code.settings.example.json` (PostToolUse validation)
- [ ] Test the manifesto: small-vs-large model eval run — blocked on Phase 6 Stage 2

## Sequencing

| Phase | Depends on | Effort |
|---|---|---|
| 0 | — | ½ day |
| 1 | 0 | 2–4 sessions |
| 2 | 1 | 1–2 sessions |
| 3 | 1 | 2–3 sessions |
| 4 | — | 1 session |
| 5 | 1 | 2 sessions |
| 6 | 1 | 2–3 sessions |
| 7 | 3 + 6 | incremental |

## Current State

Phases 0–5 complete, Phase 6 Stage 1 and Phase 7 adapters landed — all on
2026-06-11, the day the plan was written. Remaining open items: Tier 2 kernel
blocks (5, low priority), eval Stage 2 (the headless agent loop), the
small-model experiment (blocked on Stage 2), AGENTS version auto-mirroring
(deferred), and the first jmtm filing through a decision record (lands with the
annual accounts, due 2026-07-31). This thing is the canonical plan; phase
checkboxes are updated as work lands.
