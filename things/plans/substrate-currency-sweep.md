---
id: substrate-currency-sweep
type: plan
status: in-progress
version: 1.0
created: 2026-08-05
priority: high
tags: [reconciliation, staleness, documentation, templates, cue-tuning, sweep]
linked_things:
  - id: change-reconciliation-specification
    relation: implements
    notes: "This plan is the framework's second whole-substrate Assimilate pass (the first ran inside v3.26.0's release walk, scoped to the push doctrine). This one is unscoped: every narrative surface checked for currency against nine releases of change. The drift found is the spec's own prediction — restatements not walked."
  - id: a-generated-surface-collapses-its-walk
    relation: references
    notes: "The end-session ritual restated on five surfaces, one walked at v3.26.0 — past the insight's promote-when-a-walk-revisits-twice threshold. Phase 2 patches the surfaces; promotion to a generated source is recorded as the durable fix candidate, not built here."
  - id: inflection-candidates-are-computable
    relation: implements
    notes: "Phase 7 fixes the shipped predicate's membership bug: DEFINITION_SURFACE_TYPES excludes `insight` and `decision`, contradicting its own criterion ('types whose entire function is to be reasoned from'). Found felt: the operator worked porch-bound insights in another domain on 2026-08-05 and the cue never fired."
  - id: tracking-artifacts-can-drift-from-reality
    relation: references
    notes: "The sweep's headline classes are this insight at scale: README nine releases behind, figures owned by `mdllm tokens` restated stale, a template shipped for a type retired five weeks ago."
  - id: estate-cadence-cluster
    relation: references
    notes: "v3.26.0's own walk updated the live end-session command but missed its four sibling surfaces — the gap Phase 2 closes."
---

# Substrate Currency Sweep — the correction pass after nine unwalked releases

## The finding (sweep, 2026-08-05)

The operator asked for a whole-substrate staleness view: change-reconciliation
had been running scoped to each release's own inflection, but the narrative
surfaces — README, walkthroughs, shipped templates — had not been walked as
a set since ~v3.17.5. The sweep (mechanical floor first, then greps keyed to
each release's changes, then judgement reads) found the drift clustered in
exactly the classes the spec predicts:

1. **One truth restated on N surfaces, walked on 1.** The end-session ritual
   lives on five surfaces; v3.26.0's walk updated one (`.claude/commands/`).
   README restates the CLI surface, the spec inventory, and a token figure
   `mdllm tokens` owns — all stale.
2. **The newcomer path predates the machinery it now walks through.**
   `docs/first-hour.md` (06-24) says nothing about estate-sync output,
   boundary terms at scaffold, or autopush.
3. **Residue and un-dispositioned legacies.** One superseded doctrine
   citation (`orchestration.md:240`); a template still shipped for the
   retired `continuity-brief` type; two legacy `docs/plans/` files; an
   insight-corpus walk last run at v3.17.1.
4. **Floor-flagged items** already known: framework-map count 24 vs 26,
   both examples pinned at 3.24.0.

## The ruling (operator, voice, 2026-08-05)

- The v3.26.0 cue mechanism (`mdllm candidates`) is **correct as built** —
  the operator's felt concern ("shouldn't reconciliation apply to every
  change?") is answered by the cue running per-commit; no scope change.
- **One bug is real and felt:** `DEFINITION_SURFACE_TYPES` omits `insight`
  and `decision` — types that meet the set's own written criterion. Fix it.
- **Deferred, explicitly not built now:** `exposed: true` ⇒ cue
  unconditionally; set + threshold schema-declarable à la
  `terminal_statuses` (v3.19.0 shape). Both doctrine-compatible; neither
  yet felt. Record here so the candidates survive.
- Execute the correction pass across everything the sweep highlighted,
  then fix the bug.

## Phases

| Phase | Scope | Status |
|---|---|---|
| 1 — Mechanical | framework-map count + View 3 rows (`autopush`, `candidates`); `orchestration.md:240` residue; examples walk + re-pin to 3.26.0 (no-op absorb: `computed` opt-in undeclared, autopush repo-level n/a, cue hook-side); installer prose (hook legs undersold) | ✅ done |
| 2 — End-session collapse | Patch the four stale surfaces (templates/commands, copilot-prompts, .github/prompts, templates/prompts/session-end-continuity.md) with the publication-debt step | ✅ done (prompt → v1.1, new §7 + output) |
| 3 — README rewrite | Spec table from the catalog (23), CLI section gains the estate layer + publication story, figures re-measured (kernel 2,897), domain count stated generically | ✅ done |
| 4 — first-hour walk | Newcomer path through estate-sync, boundary, autopush | ✅ done (v1.1 — three new footnotes, hook legs named) |
| 5 — Dispositions | continuity-brief template deleted (type stays reserved-but-deprecated by design, thing.md:88); both docs/plans legacies carry archival banners; retrospective-specification confirmed `stable` (estate section named a discovered practice; contract unchanged) | ✅ done |
| 6 — Judgement walks | Insight corpus: six flagged actives walked, one live-claim fixed (`tracking-artifacts` named WORKLOG as a live surface; now annotated — the insight's own lesson applied), five confirmed historical/annotated. Skill templates: all four walked — deliberately generic, references current; old dates are stability, not rot | ✅ done |
| 7 — Cue membership fix | `insight` + `decision` join DEFINITION_SURFACE_TYPES; self-tests; patch release | pending |

## Success criteria

- Floor quiet: `validate` + `coherence` clean (the two example pins and the
  map count Warning gone).
- Every surface the sweep flagged either corrected or carrying an explicit
  disposition — nothing left implicitly stale.
- A modified `insight` or `decision` fires the pre-commit cue line with no
  fan-in requirement, covered by a self-test.
- All work committed at meaning boundaries; framework root stays unpushed
  (release surface — publish remains the operator's deliberate act).
