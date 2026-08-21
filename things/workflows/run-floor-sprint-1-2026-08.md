---
id: run-floor-sprint-1-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-21
definition: substrate-floor-development
current_stage: requirements
held_by: claude-code
linked_things:
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The finding ledger this sprint draws from; the operator's superseding execution order (recorded there 2026-08-21) names the floor block this run executes."
---

# Run: Floor Sprint 1 — correctness residue, speed, and the test workflow

## Where This Is

Born at `requirements` — the `problems` stage was satisfied before this run
existed: two independent substrate reviews (Claude and Codex, 2026-08-20),
their consolidated remedy ledger, and the 2026-08-21 measured bottleneck
evidence (session-start 67.8s→2.1s, pre-commit ~8.7min→~20s, full test suite
37min serial) together form the problem inventory with evidence. The operator
handed execution authority to the agent on 2026-08-21: stages advance on the
agent's judgement, with human gates only at seal and irreversible acts.

## Next

Write the floor-block requirements thing (functional set from the remedy
ledger + non-functional budgets with numbers from the measured baseline),
then advance to `analysis` and record the sprint-1 scope cut as a pinned
decision.
