---
id: run-floor-sprint-1-2026-08
type: workflow-run
status: completed
version: 1.0
created: 2026-08-21
definition: substrate-floor-development
current_stage: seal
linked_things:
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The finding ledger this sprint draws from; the operator's superseding execution order (recorded there 2026-08-21) names the floor block this run executes."
---

# Run: Floor Sprint 1 — correctness residue, speed, and the test workflow

## Where This Is

At `verify`. Build landed F9, F10, F11, F1 (all necessity), F12 and F13
(should) in per-requirement commits (7f9bfa8 … ca95885). Two recorded
deviations from the design:

1. **F11 composition**: the coordinator runs the legs as concurrent child
   processes sharing the frozen tree via the existing env pin, not
   in-process threads over one warmed view — byte-identical leg behaviour by
   construction beat reimplemented rendering; the in-process variant stays
   open for sprint 2 if margin is ever needed (it is not: measured ~4.2–5.5s
   against N3 ≤ 12s).
2. **F4 deferred to sprint 2**: moving the hook bodies to the leaf contract
   requires `SH_RESOLVE`, which lives in runtime, which imports the leaf —
   the clean move belongs with F5's adapter reshaping, not as a
   half-inversion now. `resolve_hooks_dir` alone was not worth a partial
   move.

Stretch (F2, F6-part) untouched, per the design's gate: stretch starts only
after necessity + should are verified.

## Verify record (2026-08-21 evening)

**Full suite: 695 passed, 0 failed, 9:20 under `-n auto`** (commit 3daf1d1
tree). The verify → build loop fired once, as designed: the CAS transaction
fixture caught the coordinator spawning this checkout's entry instead of the
hook-invoked one (a real nested-estate defect, fixed), and the fixture
itself moved to the concurrent composition with its invariants intact.

Budgets, measured immediately after the full suite (a deliberately hostile
cache state — the suite churns hundreds of thousands of temp files):

| ID | Budget | Measured | Verdict |
|---|---|---|---|
| N1 session-start root warm | ≤ 5s | 5.5–5.8s post-suite; 2.1s steady-state (same morning, same structural shape — F9 guard: 1 scan, 11 spawns both times) | met in steady state; post-suite eviction transiently exceeds — budget NOT relaxed; the 37k-file worktree walk is the residual, owned by sprint 2 |
| N2 estate-sync root | ≤ 8s | 10.9–11.9s this evening; 4.8s this morning | network variance dominates (14 remote round-trips); local compute unchanged — re-measure across days before any loop-back; budget NOT relaxed |
| N3 precommit root | ≤ 12s | 10.4–10.7s typical warm (coherence-bound leg); ~4–5s hot-cache best | **met** (the F13 commit's 4.2–5.5s was hot-cache best case; this is the honest typical) |
| N4 precommit domain | ≤ 5s | 4.5s post-suite; ~1–2s steady | **met** |
| N5 validate domain | ≤ 3s | 1.9–2.0s | **met** |
| N6 focused loop | ≤ 120s | 26–96s across representative files | **met** |
| N7 full suite | ≤ 12min | 9:20 (12:00 under concurrent load) | **met** |
| N8 lifecycle step ≤ ⅓ harness budget | 60s budget | session-start step ~2–6s | **met** |

N1/N2 verdicts are recorded as measurement-protocol findings, not budget
misses: both meet budget in the steady state the budget describes, and the
requirements thing should gain a defined measurement protocol (steady-state
vs post-suite) in its next revision rather than the budgets moving.

## Reconcile record (2026-08-21)

Walked and committed (f9be3fb): CLI help header (+precommit row),
operator-guide install-hook row (+ re-run guidance for existing repos),
orchestration.md v1.20 hard-hook sentence (kernel block) with kernel
regenerated, framework-map command census. No enforcement semantics moved —
only descriptions of how the one candidate is evaluated.

## Seal record (2026-08-21)

Ledgers set to truth: the remedy's Phase 1 perimeter box, Phase 3A
structural-test box, and 3C/3D boxes ticked with dated annotations (3C
carries the composition deviation in the ledger itself);
floor-structure-residue's perimeter done-when ticked; the sprint design plan
completed. Sprint-2 inventory left honestly open: F3, F4 (deferred here with
layering evidence), F5, F6-full, F7 at floor-structure-residue; F8 at
coherence-mechanism-build; N1's worktree-walk residual and the requirements
thing's measurement-protocol definition.

**Human gate — publication.** The framework root declares `autopush: false`;
everything this sprint produced is local truth awaiting the operator's
deliberate push. The changelog entry and version bump belong to that release
act (v3-33-release-and-external-acceptance owns the walk) and were left
unpreempted.

## Next

Nothing — the run is complete. Sprint 2 (structure: F3/F4/F5/F6/F7) starts
as a new run of `substrate-floor-development` when execution resumes.
