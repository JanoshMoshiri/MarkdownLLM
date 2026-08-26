---
id: run-kitchen-renovation
type: workflow-run
status: active
created: 2026-06-15
definition: home-renovation-process
definition_commit: e51faae1eadf1d067ae715e8c9ecac1b20645718
current_stage: materials
held_by: homeowner
tags: [home, renovation]
informed_by:
  - id: project-kitchen-renovation
    commit: 219c62e5bcb61d189c57dc9a0deddcf4f3cac09c
linked_things:
  - id: project-kitchen-renovation
    relation: references
  - id: decision-hire-howell-joinery
    relation: informs
---

# Run: Kitchen Renovation

## Where This Is

At `materials`, and stuck there. The `quotes` stage closed when Howell Joinery
was hired (see `decision-hire-howell-joinery`). The fitter is booked in
principle, but the worktop choice — the long pole — is still open and now
overdue, so the run cannot advance to `fitting`. The last transition was
`quotes → materials` on hiring.

## Next

Make the worktop decision (`task-choose-worktop`). That unblocks
`task-book-fitter` and lets this run advance `materials → fitting`. No rework
loop is in play yet; the risk is schedule, not scope.

## Notes

`held_by: homeowner` is the advisory claim — the homeowner is driving this run,
not the contractor. The day-to-day project breakdown (subtasks, the
`subtasks_complete` trigger) lives in `project-kitchen-renovation`; this run
holds only the process cursor and the resume point. No `stage_history` here —
the cursor's path is the commit log. `definition_commit` binds the instance to
the process revision it actually follows, while `informed_by` pins the project
demand that instanced it. Any durable completion output would point back to this
run with its own `informed_by` pin.
