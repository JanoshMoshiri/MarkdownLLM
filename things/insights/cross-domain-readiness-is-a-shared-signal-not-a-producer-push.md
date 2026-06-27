---
id: cross-domain-readiness-is-a-shared-signal-not-a-producer-push
type: insight
status: active
disposition: keep-active
disposition_reason: "Parked — capture-don't-decide; awaiting a real heterogeneous multi-agent hand-off before the awareness signal is designed."
version: 1.1
created: 2026-06-26
session: 2026-06-26
source: operator-scenario
confidence: medium
origin: synthesised
tags: [cross-domain, mcp, orchestration, coordination, awareness, symmetry, gap, undecided]
linked_things:
  - id: cross-domain-handoff-is-built-inbound-only
    relation: extends
  - id: directional-graph-reads-come-in-inbound-outbound-pairs
    relation: supports
  - id: mechanism-pairs-come-from-two-reflection-axes
    relation: supports
  - id: coordination-claim-specification
    relation: informs
  - id: structural-pointers-need-reverse-edge-indexing
    relation: supports
  - id: mcp-domain-server-design
    relation: informs
  - id: provenance-specification
    relation: informs
---

# Cross-Domain Readiness Is A Shared Signal, Not A Producer Push

## The Insight

There are **two** producer-side cross-domain obligations, not one, and they
divide on *what the consumer already knows*:

- **Freshness** — "did the source of a thing I already import move underneath
  me?" Resolved. It collapses onto the consumer's own pin, because the consumer
  *already knows what it imported* — `imports-check` re-reads the pinned
  `source_commit` and re-quarantines on drift. The producer pushes nothing;
  pull works because the pin exists ([[cross-domain-handoff-is-built-inbound-only]]).
- **Awareness / readiness** — "the producer just made something *new* I never
  imported and am not polling for." This is the facet the inbound-only insight
  explicitly **carved out** (its Scope marker: *"awareness: how does a domain
  learn something useful exists elsewhere"* — deferred to its own insight). This
  is that insight.

The motivating scenario (the sharpener): one operator runs several
heterogeneous agents over MarkdownLLM domains — a calendar domain on Claude, a
marketing domain on Codex, a social domain on OpenClaude. The marketing agent
finishes a long-running task and is *ready to hand the result to the social
agent* — a deliverable the social domain never pinned and has no reason to be
checking for. The question is not "is my pin fresh" but **"how does the social
agent come to know there is now something for it at all?"**

### Why a producer push is still the wrong mirror

The hard wall from [[cross-domain-handoff-is-built-inbound-only]] holds
unchanged: **a domain cannot enumerate its consumers.** A producer-held
registry of "who consumes me" breaks domain isolation and the no-global-index
rule — the same wall that ruled out a cross-boundary `cascade` for freshness
rules out a producer→consumer notification for awareness. The instinct to build
a doorbell the producer *rings* is the wrong half of the pair again.

So the obligation collapses the same way freshness did — onto a **pull the
consumer initiates** — but onto a *different surface*, because here there is no
pin to poll:

- Freshness collapsed onto **the consumer's own frontmatter** (each consumer
  already records what it imports).
- Awareness has nothing on the consumer yet, so it collapses onto **the
  operator's trust zone** — the address book the operator already wired (the
  per-trust-zone introducer / address-zero in [[mcp-domain-server-design]]). The
  operator is the one party that *does* know all three domains exist and may
  speak to each other; the producer never has to.

**Readiness is therefore a property the producer publishes, not a message it
sends.** "Ready to hand off" already has a mechanical definition in the
framework: a thing that is `exposed: true`, reaches a terminal status, and is
**committed** (the commit is the moment state becomes real). The missing piece is
only how a *wired peer discovers a newly-exposed thing on a face it already
trusts* — and that stays a pull at the consumer's own initiative (session start),
exactly like the version-check, never a daemon the consumer must keep awake.

## The Fork (undecided — capture, don't decide)

The operator is deliberately on the fence about whether to build this at all and,
if so, which shape. Three candidates, ordered most- to least- framework-native:

1. **Discovery-poll — widen the existing pull.** `imports-check` (or the
   session-start check) currently asks "is my *pinned* source fresh?" Widen it to
   "what is *newly exposed* on the faces in my address book that I have not yet
   imported?" Pure pull, no new primitive, almost already there: the producer
   just publishes (`exposed: true` + commit); the wired consumer notices on its
   next session. The face (`mcp-serve`) and the address book already exist.
2. **A shared coordination signal** — a small thing in the operator's trust zone
   that the producer writes ("X is ready for the social domain") and consumers
   read. This is the sibling of [[coordination-claim-specification]]: a *signal*
   ("ready for you") where the claim is a *hold* ("I have this"). One new
   lightweight concept, deploy-when-felt like the claim itself.
3. **Extend `coordination-claim`** — give it a second role/field rather than a
   new spec. Cheapest in surface, but risks overloading a concept whose one
   reason to change is contention, not notification (a cohesion smell — likely
   the wrong home).

Leaning (1): it adds no new primitive, keeps pull as the spine, and reuses the
two surfaces already built. But this is a lean recorded for later, not a
decision.

## Why It Matters

It keeps the framework honest about a real, named gap *without* letting the
"orchestration" framing smuggle in a conductor. MarkdownLLM is a substrate, not a
harness; the answer to "how do N heterogeneous agents coordinate a hand-off" must
stay *coordination through shared state across the membrane*, not a scheduler.
This insight is the razor that holds that line for the awareness facet: when a
producer is "ready," the framework-true move is **publish + let the wired peer
discover**, never **push to a consumer the producer should not be able to name.**

It also notes the heterogeneous-harness part is the *easy* part — MCP is the
protocol, harness-agnostic by construction; Codex and OpenClaude read a domain's
face exactly as Claude does (remote reach is the unbuilt Phase 5 transport, not a
new design). The hard part is purely the awareness signal above.

## Status / Next

Capture is medium-confidence (the scenario is concrete; the resolution leans on
(1) but is not settled). The *design* is undecided and deliberately parked.
Promote toward a spec when the multi-agent scenario becomes real — the operator
actually runs two heterogeneous domains that need an unsolicited hand-off — or
fold it into the broader cross-domain I/O design (discovery / awareness /
permeability) when that surface is worked. Inherits the "second concrete
consumer" trigger from [[cross-domain-handoff-is-built-inbound-only]]; this is its
awareness half, now named so it cannot quietly stay invisible.
