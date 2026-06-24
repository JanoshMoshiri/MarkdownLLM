---
id: directional-graph-reads-come-in-inbound-outbound-pairs
type: insight
status: active
version: 1.0
created: 2026-06-24
session: 2026-06-24
source: both
confidence: high
origin: synthesised
tags: [derived-index, change-reconciliation, floor-affordance, symmetry]
linked_things:
  - id: derived-index-is-attention-cache-not-search-layer
    relation: supports
  - id: structural-pointers-need-reverse-edge-indexing
    relation: supports
  - id: derived-index-specification
    relation: informs
---

# A Directional Read Over the Relationship Graph Implies Its Opposite

## The Insight

`touchpoints` and `cascade` are the same mechanism pointed in opposite
directions. `touchpoints <id>` reads the graph **inbound** — "what points at me,
what did I just put at risk?" — and serves the change-reconciliation Assimilate
beat. `cascade <id>` reads the same edges **outbound** — "what do I unblock, what
did I just complete-forward?" — and serves the post-completion cascade. Neither is
a new primitive: both are `derived-index-is-attention-cache-not-search-layer`
applied to a single thing's neighbourhood, computed live, so the agent reads a
precomputed chain instead of re-walking the corpus by hand (which the kernel
forbids: *never re-perform a mechanical walk by reasoning*).

The durable, forward-looking rule: **when the floor grows a mechanical read over
the relationship graph in one direction, its opposite direction is a distinct and
usually equally-useful affordance — look for the mirror before assuming the job is
done.** Inbound and outbound are two obligations, not one, the same shape as
`structural-pointers-need-reverse-edge-indexing`'s "a forward resolver and a
reverse index are two mechanisms." A directional read answers only half of the
neighbourhood question.

## Why It Matters

It is a razor against two opposite errors. Against *under-building*: shipping the
inbound read (risk/assimilation) and never noticing the outbound read
(propagation/unblocking) is a real gap — `cascade` existed only as a hand-walked
prompt for weeks while `touchpoints` was already a tool. Against *over-building*:
the mirror is **not** a second feature to design from scratch; it is the same
index walk with the direction flipped, so it inherits the same
report-don't-apply discipline (detection mechanical, disposition the agent's) and
the same live-not-cached property. Recognising the pair keeps the two affordances
consistent by construction rather than drifting into two different shapes.

The pairing is also a naming and discoverability win: *"what did I put at risk?"*
(inbound) and *"what did I just unblock?"* (outbound) are the two halves a user
intuitively asks at a change boundary, and giving them mirror-image commands makes
the floor legible.

## Context

Surfaced 2026-06-24 building `mdllm cascade` as the deliberate mirror of the
v3.13.0 `mdllm touchpoints`. The design question that produced it — "is cascade
just touchpoints rebound?" — resolved to *no*: they walk **different edge sets**
(cascade reads `dependencies`/`blocks`/`parent`/`triggers`; touchpoints reads
`linked_things`/`parent`/`definition`/`informed_by`) in **opposite directions**,
which is exactly what makes them a genuine pair rather than a duplicate. The
shared architecture (live neighbourhood read, report-not-apply) is the invariant;
the edge set and direction are the variables.
