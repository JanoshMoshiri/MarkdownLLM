---
id: shared-domain-failures-are-a-framework-signal-without-a-path
type: insight
status: active
version: 1.0
created: 2026-08-05
confidence: high
origin: stated
source: human
tags: [membrane, estate, upward-signal, diagnosis, porch]
linked_things:
  - id: divergence-is-an-unrouted-decision
    relation: references
    notes: "The unrouted decision here is a diagnosis: N domains routing the same divergence locally IS the evidence it was never theirs to route. The verdict 'framework problem, not domain problem' currently has no surface on which to form."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: complements
    notes: "Same family, opposite direction: that insight is about signal travelling down (framework → operator) at the wrong moment; this one is about signal that cannot travel up (domains → framework) at all."
---

# Shared domain failures are a framework signal with no path to the framework

## The Insight

When several domains hit the **same** problem independently, that coincidence
is itself a verdict: the problem is the substrate's, not any domain's. The
2026-08-05 re-sweep found the pattern three times in one week — the
`git: branch` config lie (fixed in three domains, then reborn in a newborn
because the scaffold default was never corrected), the empty disclosure
boundary (11 of 13 domains, inert), and the framework's own prompt-contract
fields flagging a domain 24 times. Every instance was handled *locally*,
sometimes repeatedly, until an estate-wide pass happened to see them
side-by-side.

The operator's retraction, stated 2026-08-05: the framework probably **does**
need a consume side — a way to receive problem information from its domains —
"if that information could have got to the substrate, there would have been a
clear verdict that something needed to be done, and it was a framework
problem, not a domain problem."

## Why this is not a new mechanism

The pieces exist. Domains can expose insights on their faces; the framework
can consume across the porch (the divergence primitive arrived exactly that
way, verified triple and all); `triggers --estate` and `estate-check` already
batch per-domain reads at the operator axis. What is missing is only the
**aggregation read**: nothing compares findings *across* faces to notice that
the same friction appears in N places. The re-sweep also showed the path
failing at both ends today — a `framework_promotion: candidate` sat 35 days
unrouted partly because it was never `exposed`, so no membrane path existed
even for a willing consumer.

Doctrine is untouched: producers still never learn their consumers; the
framework consuming domain faces is an ordinary consumer act; the direction
of the membrane stays a ruling. This is spec-when-foreseeable territory —
the sketch lives in [[framework-upward-signal]], and it deploys when felt.

## The felt evidence

Three independent rediscoveries of one defect class in a single week, each
paid for separately. The next one is the trigger.
