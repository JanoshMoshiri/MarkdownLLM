---
id: run-floor-sprint-1-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-21
definition: substrate-floor-development
current_stage: design
held_by: claude-code
linked_things:
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The finding ledger this sprint draws from; the operator's superseding execution order (recorded there 2026-08-21) names the floor block this run executes."
---

# Run: Floor Sprint 1 — correctness residue, speed, and the test workflow

## Where This Is

At `design`. Analysis exited with `floor-sprint-1-scope-2026-08-21` — the
MoSCoW cut (necessity F9/F10/F11/F1, should F12/F13/F4, stretch F2/F6-part,
structure and coherence deferred to sprints 2–3) with inputs pinned and a
re-open condition recorded (budgets move only by recorded decision).
Execution authority is with the agent per the operator's 2026-08-21
handover; human gates only at seal and irreversible acts.

## Next

Produce the sprint-1 design thing: per-requirement components touched, how
each change proves its budget (N3, N6, N7 are the missed ones), the focused
test set per change, commit granularity, and risks with mitigations. Design
must show F11 meeting N3 or promote F12 per the decision's re-open condition.
