---
id: cross-domain-handoff-is-built-inbound-only
type: insight
status: active
version: 1.0
created: 2026-06-24
session: 2026-06-24
source: both
confidence: high
origin: synthesised
tags: [cross-domain, provenance, interface, change-reconciliation, symmetry, gap]
linked_things:
  - id: cross-domain-handoff-is-verified-external-input
    relation: extends
  - id: directional-graph-reads-come-in-inbound-outbound-pairs
    relation: supports
  - id: mechanism-pairs-come-from-two-reflection-axes
    relation: supports
  - id: interface-specification
    relation: informs
  - id: provenance-specification
    relation: informs
  - id: change-reconciliation-specification
    relation: informs
---

# Cross-Domain Hand-off Is Built Inbound-Only — The Outbound Half Is The Standing Gap

## The Insight

The framework's three reflexive maintenance surfaces — change-reconciliation
(correctness, at-change), the deterministic floor (structure, at-write), and the
retrospective (quality, periodic) — are each complete *for the interior of a
single domain*. They all stop at the repo boundary. The one surface that crosses
it, **cross-domain hand-off, is specified inbound-only.**

The consuming side exists: when domain B imports a deliverable from domain A, it
arrives `origin: external`, quarantined (`verified: false`) until a human
confirms ([[cross-domain-handoff-is-verified-external-input]]). That is a
*pull-side defence* — it fires when B re-imports.

The producing side does not exist: when A **changes** a deliverable B already
consumed, nothing propagates a staleness signal to B. `cascade` — the outbound
post-completion read — stops at the domain boundary. So the consumer can only
*re-check on its own initiative*; the producer never *notifies*.

This is precisely [[directional-graph-reads-come-in-inbound-outbound-pairs]]
applied one level up, and it is an instance of
[[mechanism-pairs-come-from-two-reflection-axes]]:

- **At the thing boundary**, the inbound/outbound pair is closed —
  `touchpoints` (inbound) and `cascade` (outbound) both exist.
- **At the domain boundary**, only the inbound half exists (quarantine-on-import).
  The missing mirror is a **cross-boundary cascade**: a producer-side signal that
  a consumed deliverable changed, carried across the seam to its consumers.

It is the known-unhandled: foreseen since 2026-06-15 (the hand-off design was
deferred), but the duality lens reframes *what* is missing — not the whole
hand-off mechanism, but specifically its outbound, producing-side half.

## Why It Matters

It sharpens a deferred design from "spec cross-domain references some day" to a
single, well-shaped question: **how does a change in a source domain reach the
domains that consumed its outputs?** The answer must respect the constraints
already established — separate id-spaces, independent gitignored repos, no global
index ([[cross-domain-handoff-is-verified-external-input]]) — so it cannot be a
live link. The candidate shape is a *commit-pinned reference triple*
(`source_domain` + `source_id` + commit pin) on the consuming side, against which
a producer-side or consumer-poll check can detect "the pinned commit moved" —
the cross-domain analogue of `provenance`'s Freshness check, which already does
exactly this *within* a domain. The machinery largely exists; what is missing is
the seam-crossing wiring and the producer-side obligation.

It also completes the framework's self-description: a symmetry/coverage map of the
maintenance surfaces would show every interior cell filled and this one boundary
cell empty — the visible hole that makes the gap impossible to not see, which is
the floor's own design philosophy turned on the framework itself.

## Status / Next

The capture is high-confidence; the *design* is not yet specified. Promote toward
a spec when a second concrete cross-domain consumer appears or when a
`workflow-run` hand-off is actually exercised across two domains — whichever comes
first (inherits the trigger from
[[cross-domain-handoff-is-verified-external-input]]). This insight is the outbound
half of that same deferred design, now named so it cannot quietly stay invisible.
