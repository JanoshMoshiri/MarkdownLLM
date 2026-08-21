---
id: run-floor-sprint-1-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-21
definition: substrate-floor-development
current_stage: analysis
held_by: claude-code
linked_things:
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The finding ledger this sprint draws from; the operator's superseding execution order (recorded there 2026-08-21) names the floor block this run executes."
---

# Run: Floor Sprint 1 — correctness residue, speed, and the test workflow

## Where This Is

At `analysis`. The requirements stage exited with
`floor-block-requirements-2026-08` committed: thirteen functional
requirements (F1–F13, owners preserved) and the N1–N8 budget table bound to
the measured reference machine. The run was born at `requirements` because
the problems inventory pre-existed it (the two 2026-08-20 reviews, the
consolidated remedy, the 2026-08-21 measurements). Execution authority is
with the agent per the operator's 2026-08-21 handover; human gates only at
seal and irreversible acts.

## Next

Record the sprint-1 scope cut as a `type: decision` with inputs pinned, then
advance to `design`.
