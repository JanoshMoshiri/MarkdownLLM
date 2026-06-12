---
id: task-choose-worktop
type: task
status: in-progress
priority: medium
created: 2026-05-24
due_date: 2026-06-10
parent: project-kitchen-renovation
dependencies: [task-get-contractor-quotes]
tags: [home, renovation]
triggers:
  - type: time
    condition: due_date_passed
    action: "overdue — the fitter cannot be booked until the worktop is chosen"
---

# Choose Worktop

## What to Do

Decide between oak (warmer, needs oiling) and quartz (costlier, zero
maintenance). Get the chosen one on order — lead times are 2–3 weeks either
way.

## Why It Matters

This is the project's critical path: `task-book-fitter` lists this task in its
`dependencies` and stays blocked until it completes.

## Success Criteria

One worktop ordered, confirmation email received.

## Current State

Two showroom visits done, samples at home. The due date has deliberately been
left in the past in this example dataset: run `mdllm triggers` against this
domain and this task's `due_date_passed` trigger fires — that is the
demonstration.
