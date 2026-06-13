---
id: consistency-is-maintained-at-change-not-by-sweeping
type: insight
status: active
version: 1.0
created: 2026-06-13
session: 2026-06-13
source: both
confidence: high
origin: synthesised
tags: [validation, change-management, semantic-validation, human-in-the-loop]
linked_things:
  - id: change-reconciliation-specification
    relation: informs
  - id: provenance-specification
    relation: supports
  - id: validate-thing-specification
    relation: supports
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Consistency Is Maintained at Change, Not by Sweeping

## The Insight

Structural validation works because structure is **intrinsic, local, and
preventable** — a malformed thing is invalid on its own and the floor rejects it
at write time. Semantic consistency has none of those properties: a contradiction
lives *between* two individually-valid things, and writing the second is a
locally legal act. So semantic validation can never be a write-time gate the way
structure is.

The instinct is therefore to *sweep* — periodically hunt the whole corpus for
drift. That instinct is wrong, and the reframe is the insight: **a fresh thing
on a clean slate carries no consistency risk.** There is nothing for it to
contradict. Risk is not a property of the corpus you scan; it is a property of
*change* to something the domain already reasons from. Consistency is maintained
at the moment of change, by reconciling that change against what it touches —
not after the fact, by sweeping.

Two consequences follow. **The agent does not need better eyesight; it needs a
reflex bound to the change** — the mechanical layer's job is not to judge risk
but to make the agent unable to *not see* the shape of what a change disturbs
(the `relationships` and reverse-`provenance` indexes already supply that shape).
And **the trigger is the human's, not the agent's**: recognising that a change is
a genuine inflection — a change of the logical path, not of its expression — is
the expert judgement the framework supplements, not automates.

## Why It Matters

It dissolves the "how do we validate reasoning?" problem into something
tractable. You don't build a semantic validator that scans everything; you run a
scale-free reconciliation pass at the point of change — cue (human), assimilate
(mechanical, total), walk (agent, semantic), seal (record + supersede). It also
explains why connectivity is the real lever: the agent's field of view is exactly
as wide as the corpus is linked, and the pass itself leaves new edges behind, so
awareness compounds. This is the realisation specified by
[change-reconciliation.md](change-reconciliation.md).

## Context

Synthesised 2026-06-13 in a design dialogue: the human drove the two load-bearing
reframes — that this is change management rather than sweeping, and that the
driver (not the agent) names the inflection — and the framework's existing
provenance and derived-index machinery turned out to already supply the
mechanical substrate. No new infrastructure was required to make the pass
runnable; the contribution is the pattern, not a tool.
