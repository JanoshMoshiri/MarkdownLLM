---
id: a-record-that-only-accumulates-has-no-metabolism
type: insight
status: active
version: 1.0
created: 2026-11-18
session: 2026-11-18
source: both
confidence: medium
origin: stated
tags: [metabolism, lifecycle, intake, disposal, expulsion, floor, accumulation, reckoning]
linked_things:
  - id: thing-lifecycle-specification
    relation: informs
    notes: "The deferred spec already holds the expulsion half: rolling window, stubs, rehydration"
  - id: operating-model-specification
    relation: references
    notes: "Names the metabolism between modules as doctrine, with no mechanism"
  - id: session-memory-specification
    relation: references
    notes: "The reckoning disposes of attention items; it does not move records through their lifecycle"
  - id: conformance-not-determinism
    relation: complements
    notes: "Each stage of a record's life is a station the floor can check"
  - id: a-surface-without-a-floor-accumulates-repairs-not-progress
    relation: supports
    notes: "Accumulation is what a surface without a floor does"
---

# A Record That Only Accumulates Has No Metabolism

## The Insight

A record is alive only if things move through it: born, processed, and
expelled. Reporting its state is not the same as moving it. Every record type
needs a checkable intake (how it is born and what it must carry), a
checkable processing path (the states it moves through and how long it may
sit in each), and a checkable expulsion (how it leaves: closed, superseded,
promoted, archived). The metabolism rate is disposal against intake, per type
and per domain; below one, the record accumulates.

The operator, 2026-11-18, in his own words:

> "And it sounds like there needs to be more mechanism, a lot more floor. The
> floor needs to enforce more. That's what I'm hearing. And the digest needs
> to be better. And not this the wrong word, because digest has a meaning.
> The metabolism of the things, the expulsion, the moving through the system
> from inception to process to expulsion."

On the specifications that state truths rather than carry checks:

> "Some things, universal workflow, I want to keep those things anyway. Even
> though they're not used, for me, they still define important truths."

## The Evidence

A read-only survey of the estate on 2026-11-18 (19 corpora, 3,228 things,
6,084 commits, read at committed HEAD) found that most specifications are used
and checked, and that the weakness is accumulation and uneven gauges:

- 1,481 of 3,228 things are open; 66 of 84 workflow runs are active; 44 of 85
  conflicts are open;
- 323 of 446 active insights are exempt from the orphan check by
  `keep-active`;
- tickets sit open past the abandonment ceiling;
- the cue and session-end gate is projected in 5 of 19 repositories;
- the one rate gauge, `mdllm reckon --rates`, reported intake 0 and disposal 0
  for the week in which this corpus gained new decisions, plans and reviews:
  it measures the attention queue, not the flow of records.

## Why It Matters

It names the organ the framework is missing and points at where half of it is
already written: `thing-lifecycle.md`, deferred and unused, specifies the
expulsion half. It also sets the roadmap's first move: gauges and metabolism
before more communication work, because everything else rests on a record
that is checked and that flows.

## Context

Reached on 2026-11-18 after the survey, when the operator read its result as
"not a lot of specs that are not used" and the need as more floor, not fewer
specifications. The survey and research reports are local working documents
and are not committed.
