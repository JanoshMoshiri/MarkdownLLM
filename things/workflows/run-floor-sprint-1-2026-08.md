---
id: run-floor-sprint-1-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-21
definition: substrate-floor-development
current_stage: verify
held_by: claude-code
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

## Next

Verify: full suite under `-n auto`, then the budget table re-measured
(N1–N8) and recorded here with numbers. Then reconcile (new `precommit`
subcommand touches the CLI surface docs) and seal.
