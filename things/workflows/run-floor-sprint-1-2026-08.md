---
id: run-floor-sprint-1-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-21
definition: substrate-floor-development
current_stage: build
held_by: claude-code
linked_things:
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The finding ledger this sprint draws from; the operator's superseding execution order (recorded there 2026-08-21) names the floor block this run executes."
---

# Run: Floor Sprint 1 — correctness residue, speed, and the test workflow

## Where This Is

At `build`. Design exited with `floor-sprint-1-design-2026-08`: mechanisms,
budget proofs, focused test sets, risks, and commit boundaries for
F9/F10/F11/F1 (necessity), F12/F13/F4 (should), F2/F6-part (stretch). F11's
N3 proof closes at ~10.5s ≤ 12s without promoting F12, so the scope
decision's re-open condition is untriggered. Build order: F9 → F10 → F11 →
F1 → F12 → F13 → F4 → stretch.

## Next

Build F9 (session-start structural anti-regression tests), then F10 (xdist +
focused-selection convention). Deviations from the design get recorded here
as they happen.
