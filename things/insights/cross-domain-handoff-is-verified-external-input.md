---
id: cross-domain-handoff-is-verified-external-input
type: insight
status: promoted
version: 1.1
created: 2026-06-15
promoted_to: provenance-specification
session: 2026-06-15
source: both
confidence: medium
origin: synthesised
tags: [cross-domain, provenance, interface, workflow, deferred-design]
linked_things:
  - id: llm-driven-systems-manifesto
    relation: challenges
  - id: provenance-specification
    relation: informs
  - id: interface-specification
    relation: informs
  - id: workflow-state-specification
    relation: informs
---

# Cross-Domain Hand-off Is Verified External Input

## The Insight

The manifesto promised domains can "reference each other," but domains are isolated, gitignored, **separate-id-space** repos with no cross-reference spec — so the promise was unspecified. A naive fix (let `linked_things` point into another domain) breaks the model: ids are only unique *within* a domain, and the repos are independent. The promise has now been softened in the manifesto; this captures the design that should eventually replace it.

The key reframe: **a cross-domain hand-off is not a link — it is an import of external input.** When domain B consumes a deliverable produced by domain A, that deliverable enters B from *outside the human-agent pair that owns B* — which is exactly the definition of `origin: external` (`provenance.md`). So the framework already has the machinery: the hand-off arrives quarantined (`verified: false`), nothing in B may rest on it until a human confirms, and the reference carries `source_domain` + `source_id` + a commit pin rather than a bare id. The producing side is an `interface.md` deliverable; the consuming side is a quarantined external thing. No new trust model is needed — only a small schema for the reference triple.

## Why It Matters

This keeps cross-domain composition on the spine instead of inventing a global id space or a shared index. It also means the first real consumer is already here: a `workflow-run` (`workflow-state.md`) produces deliverables on hand-off, and those become another domain's inputs — the concrete case the review said makes this foreseeable. Designing the hand-off as verified external input means a downstream domain inherits provenance's audit trail for free.

## Status / Next

Deferred by deliberate choice (#6 in the 2026-06-15 review → Option B: retract the over-promise, draft the design). `confidence: medium` because the reference-triple schema and the producer-side deliverable contract are sketched, not specified. Spec it when a second concrete cross-domain case appears, or when the workflow-run hand-off is actually exercised across two domains — whichever comes first. Until then, the manifesto no longer claims it as delivered.

## Promoted 2026-10-17

The design this captured is the one that shipped: a cross-domain hand-off is an import — `source_domain` + `source_id` + `source_commit`, the reference triple — entering the consumer as `origin: external`, `verified: false` until a human flips it in its own attributed commit, re-quarantined when `imports-check` finds the source moved. `provenance.md` and `interface.md` carry it; `mdllm imports-check` and `estate-check` enforce it. Cited live by seven things for 124 days. Promoted into `provenance.md`.
