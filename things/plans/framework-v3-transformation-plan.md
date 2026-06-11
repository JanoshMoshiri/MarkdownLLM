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

### Phase 1 — The deterministic floor: `mdllm` CLI + normative schemas
- [ ] Single-file Python CLI (`tools/mdllm.py`, stdlib + PyYAML): `validate` (Levels 1–2 mechanical checks), `triggers` (time/dependency/threshold evaluation), `index check|rebuild` (rebuild-and-diff), `tokens`
- [ ] Normative per-domain schema (`things/_schema.yaml`): declared types, required fields per type, valid status vocabulary per type, allowed transitions
- [ ] Resolve the status contradiction: thing.md + validate.thing.md change to "status must be in the domain's declared vocabulary; the six workflow values are the default when no schema exists"
- [ ] Declare jmtm-software's status vocabulary in its schema (the domain was right, not wrong)
- [ ] Git `pre-commit` hook running `mdllm validate --staged`; optional vendor adapters (e.g. Claude Code PostToolUse) in `adapters/`
- [ ] Rewrite validate.thing.md contract: Levels 1–3 delegated to the tool; LLM keeps Level 4 semantic checks only

**Done when:** `mdllm validate` passes clean on framework + jmtm, the pre-commit hook blocks a deliberately broken thing, validate.thing.md reflects the new division of labour.

### Phase 2 — The deletion pass
- [ ] CHANGELOG generated from structured commit messages (`mdllm changelog`); stop hand-writing
- [ ] REVIEWLOG migrated into dated retrospective things; file deleted
- [ ] Prompt input/output chain validation removed from validate.thing.md
- [ ] Speculative trigger conditions (`in_progress_count`, `warn_overload`) pruned — return when felt
- [ ] Version surfaces consolidated: `.markdownllm` canonical; AGENTS.md version mirrored by tooling

**Done when:** four tracking surfaces remain (git log, WORKLOG, continuity, retrospectives) and nothing mechanically derivable is hand-maintained.

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
