---
id: a-performance-requirement-inherits-its-measurement-context
type: insight
status: active
version: 1.0
created: 2026-08-22
session: 2026-08-22
source: agent
confidence: high
origin: synthesised
tags: [performance, requirements, measurement, sprint, scope, speculative-work]
linked_things:
  - id: floor-block-requirements-2026-08
    relation: informs
    notes: "The measurement protocol added in v1.1 is this insight's mechanism: budgets are steady-state, and named non-steady contexts are recorded rather than judged."
  - id: run-floor-sprint-2-2026-08
    relation: derived-from
    notes: "F14 was carried into sprint 2 from sprint 1's post-suite measurement, and evaporated on re-measurement because a sibling change had removed its context."
  - id: an-incident-seeded-list-encodes-the-symptom-not-the-rule
    relation: complements
    notes: "Both are the same class error at different altitudes: that one enumerates from an incident instead of a rule, this one carries a symptom forward without its conditions."
---

# A Performance Requirement Inherits Its Measurement Context

## The Insight

A performance requirement is never just a number — it is **a symptom observed
under conditions**. Write it down and the number survives into the next
sprint; the conditions usually do not. So a requirement carried forward
arrives looking like a fact ("post-suite session-start takes 5.5s against a
5s budget") when it is actually a conditional ("...*when the preceding full
suite ran for nine minutes and evicted the filesystem cache*"). Change
anything upstream of those conditions and the requirement may already be
satisfied — or meaningless — before a line is written to address it.

## How It Surfaced

F14 (bound the root's worktree walk) entered sprint 2's requirement ledger
from sprint 1's verify record, where session-start measured 5.5–5.8s
immediately after the full suite against a 2.1s steady state. At sprint 2's
verify the same post-suite measurement returned **1.9s against 1.8s steady**
— the transient was gone. Nothing in sprint 2 had touched the walk. What
had changed was a *sibling*: the suite that did the cache-evicting now
finishes in 4:03 instead of 9:20, so it evicts far less. The requirement's
number was real; its conditions had dissolved underneath it.

Building F14 anyway would have been speculative work with a plausible
justification and a stale measurement behind it — the most expensive kind,
because it looks disciplined.

## Why It Matters

- **Re-measure before building, not after.** A perf requirement more than
  one sprint old is a hypothesis, not an input. The re-measurement is
  cheaper than the fix in every case where it matters.
- **Record the conditions with the number,** or the next reader inherits a
  bare fact they cannot re-derive. The measurement protocol
  (`floor-block-requirements-2026-08` v1.1) exists for exactly this: budgets
  are steady-state, and post-suite or network-dominated readings are
  recorded as *context*, never as verdicts.
- **A requirement that evaporates is a result, not a failure.** Retire it
  with its evidence and a re-open condition, so the next session inherits
  the reasoning rather than re-discovering the symptom and re-scoping it.

## The Rule

Before building against an inherited performance requirement, reproduce its
measurement under its stated conditions. If the symptom is absent, record
the absence with its date and a re-open condition and do not build. If the
requirement carries no stated conditions, that gap is the first thing to fix.
