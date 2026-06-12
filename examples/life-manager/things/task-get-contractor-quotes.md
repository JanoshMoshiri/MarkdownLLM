---
id: task-get-contractor-quotes
type: task
status: completed
priority: high
created: 2026-05-20
parent: project-kitchen-renovation
tags: [home, renovation]
---

# Get Contractor Quotes

## What to Do

Collect at least three like-for-like quotes for the kitchen fit: supply of
labour only, units already ordered, worktop templated separately.

## Why It Matters

Everything downstream — budget, fitting dates, the worktop decision — keys off
who does the work and what they charge. Hierarchy note: this task points at its
project through the `parent` field; the project points back with a `subtask`
relation. Neither duplicates the other's job.

## Success Criteria

Three written quotes, comparable scope. Met on 2026-06-04.

## Outcome

Quotes received from Howell Joinery (£4,800, 3-week lead), Brightfit Kitchens
(£4,200, 7-week lead), and a local independent (£3,900, no fixed date). The
choice and its reasoning are recorded in `decision-hire-howell-joinery` with
this task pinned as input — the decision record, not this task, is where the
"why" lives.
