---
id: cross-domain-handoff-is-built-inbound-only
type: insight
status: active
version: 1.1
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
[[mechanism-pairs-come-from-two-reflection-axes]] — but with a **twist the lift
exposes**: the domain boundary is asymmetric in a way the thing boundary is not.

- **At the thing boundary**, the inbound/outbound pair is closed —
  `touchpoints` (inbound) and `cascade` (outbound) both exist, and `cascade` can
  genuinely *push* because the graph is shared: one repo, one id-space, edges to
  walk forward.
- **At the domain boundary**, there is no shared graph to push along. A literal
  producer-side push would require A to hold a **registry of its consumers** —
  which breaks domain isolation and the no-global-index rule outright. **A cannot
  know who consumes it.** So the outbound obligation cannot be discharged as a
  push; it *collapses onto the consumer side* as a standing poll.

The corrected mirror, therefore, is not a cross-boundary cascade. It is
**re-quarantine-on-drift**: the standing-check twin of quarantine-on-import, and
both live on the consumer side, because the boundary is an isolation boundary that
only the consumer ever chose to cross. Quarantine-on-import is a *one-time gate*
at first consumption; re-quarantine-on-drift is the *standing check* that the
pinned source has not moved underneath it. That asymmetry — push works one level
down, only pull works one level up — is *why* this felt like a missing half rather
than an obvious build.

It is the known-unhandled: foreseen since 2026-06-15 (the hand-off design was
deferred), but the duality lens reframes *what* is missing — not a producer push,
but the consumer-side standing freshness check that re-opens the quarantine.

## Why It Matters

It sharpens a deferred design from "spec cross-domain references some day" to a
single, well-shaped question: **how does the consumer learn its pinned source
moved?** — and the **keystone is that the framework already answers it for N=1.**
The session-start *upward* version-check (`orchestration.md`) holds a pin
(`framework_version_seen`) and compares it against the **cached remote-tracking
state** of the framework repo — no live fetch — surfacing drift. That is exactly a
consumer-side freshness poll against a pinned external source. The framework is
simply the one source domain *every* domain imports from. Cross-domain hand-off is
that same check generalised from the single privileged source to an arbitrary
`source_domain`. The candidate shape: a commit-pinned reference triple
(`source_domain` + `source_id` + `source_commit`) on the consumer, checked against
the source's cached remote head, re-opening the quarantine (`verified: false`) on
drift — which hands the human an **external inflection**, entering
`change-reconciliation` on B's dependents. Three specs converge —
`provenance` (the pin), `orchestration` version-check (the cached-remote compare),
`change-reconciliation` (the re-opened quarantine as cue) — and none is reinvented.

It also completes the framework's self-description: a symmetry/coverage map of the
maintenance surfaces would show every interior cell filled and this one boundary
cell empty — the visible hole that makes the gap impossible to not see, which is
the floor's own design philosophy turned on the framework itself.

**Scope marker.** This insight is the *consistency/freshness* facet only — keeping
an already-established hand-off honest as the source moves. It is the narrow
doorway into a much larger cross-domain I/O surface (discovery: how does a domain
*search* another's content; awareness: how does a domain learn something useful
exists elsewhere; permeability: whether frontmatter is inspectable across the
seam without blurring domain boundaries). Those are deliberately *not* folded in
here — they are a broader adjacent design space, candidate for their own
insight(s) when worked.

## Status / Next

The capture is high-confidence; the *design* is not yet specified. Promote toward
a spec when a second concrete cross-domain consumer appears or when a
`workflow-run` hand-off is actually exercised across two domains — whichever comes
first (inherits the trigger from
[[cross-domain-handoff-is-verified-external-input]]). This insight is the outbound
half of that same deferred design, now named so it cannot quietly stay invisible.
