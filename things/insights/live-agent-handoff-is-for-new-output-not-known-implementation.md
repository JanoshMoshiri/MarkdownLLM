---
id: live-agent-handoff-is-for-new-output-not-known-implementation
type: insight
status: active
version: 1.0
created: 2026-06-26
session: 2026-06-26
source: both
confidence: high
origin: synthesised
tags: [cross-domain, mcp, run-domain-task, ownership-boundary, razor]
linked_things:
  - id: cross-domain-handoff-is-built-inbound-only
    relation: supports
  - id: cross-domain-handoff-is-verified-external-input
    relation: supports
  - id: interface-specification
    relation: informs
  - id: phase-3-run-domain-task-reverted
    relation: informs
    notes: "run_domain_task was reverted 2026-06-27; this is design knowledge for the deferred A2A layer, not a live tool"
---

# The Live-Agent Hand-off Is For Producing New Output, Not Implementing What's Already Specified

> **Reconciled 2026-06-27 — capability reverted.** `run_domain_task` (Phase 3) was
> built and then removed in full ([[phase-3-run-domain-task-reverted]]); the
> live-agent hand-off is deferred to a later, separate A2A peer layer. This insight
> stands as **design knowledge for that future surface** — the razor for *when* a
> live-agent hand-off earns its keep — not as documentation of a tool that ships
> today. Read it in the future tense.

## The Insight

`run_domain_task` (the cross-domain live-agent hand-off — a consumer calls a
producer's agent to do work and returns a deliverable) is for when the consumer
needs the producer's **skill to produce something it does not have**: a new
design, a decision, a computation. It is **not** for implementing work the
producer has already specified. When the design already exists — as a verified
spec the consumer ingested — implementing it is the *consumer's* job by the
ownership boundary's own terms, and that spec **is already the deliverable**.
Dispatching such a task back across the seam **inverts the ownership** the
architecture defines.

The razor, before any `run_domain_task` call: *does the producer need to produce
something new here, or is the design already done and this is mine to implement?*
If the latter, build directly — the spec is the deliverable; the hand-off adds
nothing and mis-assigns ownership.

## Why It Matters

It scopes the most powerful (and highest-stakes) cross-domain capability to where
it actually earns its keep, and away from where it would corrupt the boundary. It
also re-reads the operator's original goal honestly: "code-architect changes the
website" is *already* satisfied by the Phase 1/2 flow (expose spec → consume →
verify → build) for any change whose design is settled; the live-agent hand-off is
reserved for *new* design/skill the consumer lacks. A good `run_domain_task`
demonstration is therefore a "design something new" task (e.g. "design the
architecture for adding a CMS"), not an already-decided one.

## Context

Surfaced 2026-06-26 on the first live cross-domain run. Asked to route a
contact-form upgrade through code-architect's `run_domain_task`, the jmtm agent
declined: the design decision (Resend via a Server Action) already existed in the
verified architecture it had ingested, so implementation was jmtm's by the
boundary, and routing it back would invert ownership. It built directly instead —
the correct call. The planned demo was a poor fit precisely because the change was
already designed. (The agent's refusal also raised a separate claims-integrity
question — see [[boundary-respect-was-interpretation-not-enforcement]].)
