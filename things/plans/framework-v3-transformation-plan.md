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

### Phase 3 — Provenance as a first-class spec
- [ ] New spec `provenance.md`: `origin: external` with quarantine rule (external content never feeds calculations/filings/outputs until human-verified)
- [ ] New framework-reserved `type: decision`: ADR-shaped record with `informed_by: [{id, commit}]` — inputs pinned to the exact committed version that informed the decision
- [ ] The chain: knowledge thing (pinned) → decision → output, walkable from any deliverable back to exact knowledge versions
- [ ] `mdllm provenance`: pinned commits exist, things existed at those commits, no output derives from unverified external content
- [ ] Reverse-provenance derived index (`things/_index/provenance.md`): which decisions/outputs depend on each knowledge thing

**Done when:** provenance.md spec'd, one real jmtm filing produced through a decision record with pinned inputs, `mdllm provenance` validates the chain.

### Phase 4 — Scoped insight-staleness check
- [ ] session-memory.md gains Step 0 of orientation: live insights listed in the continuity brief checked against things modified since the brief's `last_updated` (via git diff) — no new cadence, no full sweep

### Phase 5 — The operative kernel
- [ ] Each spec gains a delimited operative section (rules/tables/contracts) separate from rationale
- [ ] `mdllm kernel` generates a provenance-stamped `kernel.md` loaded at Tier 0; full specs load only when reasoning *about* the framework
- [ ] Measured against the Phase 0 baseline; target Tier 0 ~15k → ~5k tokens

### Phase 6 — Behavioral evals
- [ ] 5–10 golden scenario fixtures per domain with expected assertions (files created, statuses set, figures correct, hooks fired)
- [ ] `mdllm eval` runs scenarios against a fresh agent session and checks assertions
- [ ] Run on every spec change — spec quality gets an answer that isn't anecdote

### Phase 7 — New powers
- [ ] Diff-driven regeneration: reverse-provenance index flags decisions/outputs whose pinned inputs changed; agent offers re-runs
- [ ] Proactive operation: scheduled `mdllm triggers` + notification (jmtm deadlines surface without a session)
- [ ] Test the manifesto: eval suite run on small vs large models — "structure beats scale" becomes a reproducible result
- [ ] CI for domains: `mdllm validate && mdllm provenance && mdllm eval` on every push

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

Phase 0 complete (2026-06-11); Phase 1 is next. This thing is the canonical plan;
phase checkboxes are updated as work lands, and each phase completion is a commit
boundary.
