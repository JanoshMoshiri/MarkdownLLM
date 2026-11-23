---
id: every-spec-stays-and-gauges-come-before-clearing-2026-11-23
type: decision
status: made
version: 1.0
created: 2026-11-23
session: 2026-11-18/23
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [roadmap, rulings, specifications, floor, gauges, hypothesis, baseline, metabolism, evals, open-plans]
informed_by:
  - id: conformance-roadmap
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: conformance-not-determinism
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: work-set-on-trust-has-nothing-to-check-against
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: a-record-that-only-accumulates-has-no-metabolism
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: peer-loops
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
linked_things:
  - id: conformance-roadmap
    relation: informs
    notes: "The Phase 0 rulings on the order of work, on doctrine and on the open plans."
  - id: continuity-across-surfaces-is-the-purpose-2026-11-23
    relation: complements
    notes: "Made in the same conversation. That one says what the framework is for; this one says how the roadmap proceeds."
  - id: peer-loops
    relation: informs
    notes: "The eval gates nothing, so that plan's order of work is lifted."
  - id: conformance-not-determinism
    relation: implements
    notes: "A gauge is a reference the worker did not write."
  - id: a-record-that-only-accumulates-has-no-metabolism
    relation: implements
    notes: "The accumulated record is left for the gauges to sort, not cleared by hand."
---

# Every Spec Stays, And The Gauges Come Before Any Clearing

## Context

The conformance roadmap's Phase 0 put three rulings to the operator: the
order of work, which specifications are doctrine, and the open plans. The
operator ruled across two exchanges on 2026-11-21, after asking the session
to be critical and not simply agree.

On the specifications and the eval:

> "In all those kind of specs and constituent pieces, the lowest level
> specifications, we got to a point where some of them weren't enforced by
> the floor, but I feel like a lot of them should be. If anything, maybe
> all of them should be, apart from the manifesto and some other ones which
> are more about the history and theory behind the approach. [...] No, I
> don't think the evals should be the thing that are the gate to stop all
> this. I think the evals give us insight, but I think what's very clear
> from this plan is that gauges is something that we can run without the
> evals. So, and once we run the gauges, then we get an insight that will
> supplement the insight we'd get from running the evals."

The session answered that a check against an agent's own report is not a
gauge, that the estate's trouble is rules that do not run everywhere and
not too few rules, that every new rule lands on the operator unless it
resolves itself, and that a specification never revised by use is a
hypothesis and not yet a proven truth. The operator:

> "No, I think you're right. I think we need to have a obvious distinction
> between specs that have been tried and tested in experience and ones that
> have been hypothesized and sit in the theoretical domain and space until
> they're tested through experience. So I think we should have a flag to,
> well, not a flag, but a way to determine those two between each other. I
> don't think there's a problem having a hypothesis sitting there to be
> proven or disproven, but we need to have the distinction. And from my
> perspective, I think you're right. Let's put the gauges in place before
> we clean anything out. I don't even know we should clean any of the old
> stuff out. If they're going to be cleaned by the gauges in the long run,
> once they work, then maybe we should just leave it all and have it all as
> the test, as the things that can be sorted by the gauges."

## Decision

1. **The eval gates nothing.** The gauges are built and run without waiting
   on any eval. Evals give insight and supplement what the gauges report.
2. **Every specification stays.** None is dropped, and none is set aside as
   doctrine to make the enforced set smaller. The floor should hold as many
   of them as it can. The manifesto and the writing about history and
   theory are the exception.
3. **Tried and tested is told apart from hypothesised.** A specification
   that has not been tested through experience may sit in the record as a
   hypothesis, to be proven or disproven. The two must be told apart, and
   by something better than a flag someone sets.
4. **The gauges go in before anything is cleared.** Nothing in the
   accumulated record is cleared by hand: not the stalled plans, the fired
   triggers, the open cues or the abandoned tickets. It is left as the test
   the gauges will sort.
5. **No open plan is closed by these rulings.** The roadmap's table of
   which phase each open plan serves stands as proposed, and each row is
   confirmed by reading the plan when its phase opens.

## Agreed in general, on the session's proposal

The operator's "I think you're right" answered the whole critical reading
and named two of its points. The others are the session's, accepted in
general and not ruled one by one:

- **A gauge checks against a reference the worker did not write:** the
  record's structure, the commit history, a timestamp, a re-run. A field in
  which an agent reports its own behaviour is a form, not a gauge.
- **The rules that exist run everywhere before a new rule is added.** The
  roadmap's Phase 1 finishes before Phase 2 adds one.
- **A new rule arrives with its own resolution,** or it adds to the
  operator's queue.
- **For behaviour, a tool comes before a check.** A command that does the
  read and records it costs less than policing reads afterwards.

## Proposed by the session, not yet ruled

- **How the standing is told.** The floor derives it from history and does
  not trust a label: tested needs live records of the types a specification
  owns, or commits in which use changed it. A hypothesis that starts being
  used is flagged for promotion. The status field is not used for this,
  because it already misleads: a specification with hundreds of live
  records behind it and one with none both read `draft`.
- **A baseline.** For this corpus, commit
  `6d4e504ee2727305d65fae9b303c63698f14311c` is the baseline. Each gauge's
  first count is taken against it and becomes the number that may only
  fall. Without one, the session-start digest goes on listing the same
  stale items every day, and that trains the reader to ignore it.

## Consequences

- `conformance-roadmap` Phase 0: the three rulings are made. Its proposed
  doctrine set of three specifications is withdrawn.
- `peer-loops`: the order of work is lifted.
- The fired triggers in the session-start digest are left as they stand.
  They are part of the test.
