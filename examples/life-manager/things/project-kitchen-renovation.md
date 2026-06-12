---
id: project-kitchen-renovation
type: project
status: in-progress
priority: high
created: 2026-05-20
due_date: 2026-08-14
tags: [home, renovation]
linked_things:
  - id: task-get-contractor-quotes
    relation: subtask
  - id: task-choose-worktop
    relation: subtask
  - id: task-book-fitter
    relation: subtask
triggers:
  - type: threshold
    condition: subtasks_complete
    action: "all subtasks done — review the project for completion"
---

# Kitchen Renovation

## Goal

Replace the kitchen — units, worktop, sink — before the in-laws visit on
2026-08-22. The `due_date` is a week earlier to leave slack for snagging.

## Deliverables

A fitted kitchen, a paid invoice, and nothing left in the garage.

## Timeline and Phases

1. Quotes (done — see `task-get-contractor-quotes` and the hiring decision in
   `decision-hire-howell-joinery`)
2. Materials selection (in progress — worktop choice is the long pole)
3. Fitting (blocked until the worktop is chosen; fitter availability is the
   schedule risk)

## Current Status

Contractor chosen and booked in principle. The worktop decision is overdue and
now blocks the fitting date — this is the project's critical path.

## Blockers

None at project level; `task-book-fitter` is blocked on the worktop choice.
The `subtasks_complete` trigger fires when every subtask reaches a terminal
status, prompting a completion review rather than auto-completing the project.
