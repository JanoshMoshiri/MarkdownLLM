---
id: recurring-weekly-review
type: recurring
status: active
created: 2026-05-20
cadence: weekly
review_date: 2026-06-15
tags: [process]
triggers:
  - type: time
    condition: review_date_reached
    action: "run the weekly review (workflow skill, Sub-Processes) and advance review_date one week"
---

# Weekly Review

## What Happens

Monday morning, fifteen minutes: what completed, what's blocked, what's
overdue, what gets the week's focus. The workflow skill's "Weekly Review"
sub-process is the script.

## Why It Recurs

Triggers catch individual conditions; the review catches drift — the slow
accumulation of stale statuses and quietly abandoned work that no single
trigger fires on.

## Mechanics

The `review_date` field plus the `review_date_reached` trigger make this
mechanical: `mdllm triggers` reports it the first session on or after each
Monday. The session that runs the review advances `review_date` by a week —
that update is the trigger's idempotency.
