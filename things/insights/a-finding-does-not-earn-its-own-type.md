---
id: a-finding-does-not-earn-its-own-type
type: insight
status: active
version: 1.0
created: 2026-08-19
session: 2026-08-19
source: human
confidence: high
origin: stated
disposition: keep-active
disposition_reason: "A standing razor on type-vocabulary growth, not a task — it exists to be met at the next moment someone reaches for a new type. Promote if a second provenance-shaped type is proposed and refused on the same grounds."
tags: [vocabulary, types, insights, reviews, minimal-core]
linked_things:
  - id: thing-specification
    relation: informs
    notes: "A boundary on the reserved type set: provenance of a thought is not a type distinction, so the vocabulary does not grow to hold it"
  - id: session-memory-specification
    relation: informs
    notes: "Names insights as the single destination for preserved thought regardless of where it came from — a review, a sweep, a session, an argument"
  - id: retrospective-specification
    relation: references
    notes: "The retrospective's scans produce findings; this rules where they land"
  - id: external-review-2026-08-10
    relation: references
    notes: "The review class that made the question live — reviews produce findings in volume (the eight-round loop produced 44), which is exactly when a new type starts to look justified"
---

# A Finding Does Not Earn Its Own Type

## The Insight

Operator ruling, stated 2026-08-18: *"This is an insight. This is a finding.
And as far as this substrate is concerned, a finding is an insight because
it's insightful."*

Reviews, sweeps, and audits produce **findings**. The framework has no
`type: finding` and should not grow one. A finding that is worth keeping is
kept as a `type: insight`; a finding that is not worth keeping is not kept at
all. The admission test is the preservation test the extraction heuristic
already states — *would a fresh agent benefit from knowing this?* — and that
test does not consult where the thought came from.

## Why This Is A Ruling And Not A Detail

The pressure to add the type is real and recurring. Findings arrive in
volume (the eight-round loop produced 44 in two days), they arrive with
provenance the author wants to keep, and they *feel* categorically different
from a thought that surfaced mid-session. Every one of those is an argument
about **origin**, and origin is already a field — `origin: stated |
inferred | synthesised`, plus `source` and the `linked_things` edge back to
the review artifact that carried it. A type would encode, badly and
permanently, what two existing fields encode well.

This is `thing.md`'s minimal-core principle meeting a concrete temptation:
complexity is added only when it earns its place, and a distinction fully
expressible in existing fields has not earned one. The framework already
holds the review *record* as `type: artifact` — the container has a type
because it has a lifecycle; the thought inside it does not need one because
its lifecycle is the insight lifecycle, already specified.

## The Consequence Worth Stating

Findings therefore inherit the whole insight machinery, and that is the
point: session-end disposition, retrospective triage, orphan detection,
`promoted_to`, consolidation. A `type: finding` would have inherited none of
it, and would have needed each rebuilt — the same trap the framework avoided
when `continuity-brief` was retired rather than maintained. The vocabulary
stays small so the mechanisms stay shared.

## How To Apply

When a review, sweep, or audit yields something worth keeping: write a
`type: insight` thing, set `origin` honestly, and link it to the artifact
that produced it. Do not create a parallel bucket, a `findings/` directory,
or a status vocabulary for triage state — the insight lifecycle is the triage
state. If a future case genuinely cannot be expressed this way, that is the
signal to revisit the ruling, and the burden sits with the new case.
