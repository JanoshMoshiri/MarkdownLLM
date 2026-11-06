---
id: a-ring-is-calibrated-on-the-healthy-rhythm-not-the-failures
type: insight
status: active
version: 1.0
created: 2026-11-06
session: 2026-11-06
source: both
confidence: high
origin: inferred
tags: [calibration, ring, stall, threshold, attention, a2a, seat]
linked_things:
  - id: the-seat
    relation: derived-from
    notes: "Phase 7: the first cut set the stall window at twelve hours from the failures on record; the operator's correction and one measured read set it at one hour with a one-day ceiling."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: extends
    notes: "That insight is about a check that fires on every run; this one is about the opposite failure of the same instrument — a threshold set so wide from the failures that it fires only after the operator has stopped caring."
  - id: standing-watch-specification
    relation: informs
    notes: "The stall ring's two thresholds — window and ceiling — are this insight applied; both are declared, neither inferred from cadence at run time."
---

# A Ring Is Calibrated On The Healthy Rhythm, Not The Failures

## The Insight

When a threshold is set from the failures on record, it is set by the
forgotten tail. The stall window's first cut was twelve hours, read off
the turns that had waited half a day or three weeks before someone
noticed. The operator's correction (2026-10-30): those turns "are ones
that I've forgotten about and the loop has finished… a bad metric to
calibrate on"; the ones that need attending are "maybe an hour or less"
apart. One pinned read of the busiest workspace's tickets confirmed it —
783 gaps on 87 tickets, a reply in a median of five minutes, 90% within
about an hour — and the window became one hour, with a one-day ceiling
past which a ticket is abandoned and reported once, never rung.

The general form: a ring exists to catch a *live* process that has
stopped. Its window is the rhythm of the live process, measured when it is
healthy, plus the slack the operator will tolerate. The failures are the
wrong population twice over — they are few, and the long ones are the
cases where nobody was waiting, so a window wide enough to include them
is a ring that fires after the question has already been dropped. A
second, separate threshold (the ceiling) handles that tail by *silencing*
it, because a ring that fires on every forgotten item teaches the
operator to ignore the ring.

## Why It Matters

Every attention mechanism in this substrate has a threshold somewhere:
the stall window, the turn budget, the dispatcher's silence, the 30-day
conflict age, the 120-day insight promotion. Each one set from "how long
did the bad cases take" will drift wide and go quiet. Each one set from
"how fast does this run when it runs" and then declared will ring while
the operator still remembers the question.

## How To Apply

- Measure the healthy inter-event gap on the live record before setting a
  window; cite the read. Set the window near the tail of the healthy
  distribution (the 90th percentile was the operator's choice here), not
  beyond the failures.
- Declare both numbers — window and ceiling — as configuration the
  operator can move, never inferred at run time from cadence.
- Expect a false-ring rate and state it (about one healthy gap in ten at
  the hour); a ring with a stated false rate is read, a ring with none is
  distrusted.
