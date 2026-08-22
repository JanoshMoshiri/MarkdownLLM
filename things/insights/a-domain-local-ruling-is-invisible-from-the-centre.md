---
id: a-domain-local-ruling-is-invisible-from-the-centre
type: insight
status: active
version: 1.0
created: 2026-08-23
session: 2026-08-22
source: both
confidence: high
origin: synthesised
tags: [estate, sweep, embodiment, domain-autonomy, refresh, operator-rulings]
linked_things:
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: complements
    notes: "That insight distrusts the sweep as a consistency instrument; this names what a sweep additionally destroys when it is run from the centre — the domain's own recorded rulings."
  - id: a-generated-contract-change-is-an-estate-migration
    relation: complements
    notes: "The migration this insight governs: how to execute one across thirteen domains without flattening their local decisions."
  - id: the-estates-second-clone-is-an-independent-witness
    relation: references
    notes: "Both turn on the domain being a real, separate vantage rather than a row in a table."
---

# A Domain-Local Ruling Is Invisible From The Centre

## The Insight

An estate-wide operation looks like a loop over directories. Framed that
way, it executes the same mechanical steps in each one — and that framing is
exactly what makes it dangerous, because **a domain can carry a recorded
operator decision that changes what the correct step is, and that decision
is only legible to something oriented inside the domain.**

From the centre, every domain looks like a row: version seen, hooks present,
blocks in sync. Nothing in that row says "this domain deliberately declined
this adoption, and here is the condition that would reverse it."

## How It Surfaced

The estate refresh to v3.34.0 ran across thirteen domains. Twelve took the
standard walk. One did not: the agent embodied in it found a recorded
operator decision from 2026-08-04 parking kernel-shape adoption, with an
explicit unpark condition — *the next real working session adopts first*. It
judged, correctly, that a mechanical estate refresh is not that session,
skipped the regeneration, and named the skip in its commit.

A central loop would have regenerated those blocks without ever knowing the
ruling existed. Nothing would have failed. The floor would have been clean.
The operator's decision would simply have been quietly overwritten, and the
commit message would have claimed a successful refresh.

## Why It Matters

- **Embodiment is not ceremony.** Reading the domain's own entry contract and
  orienting inside it is what surfaces its rulings, its conflicts, and its
  parked decisions. Skipping it turns an agent into a loop body.
- **The domain is the authority on itself.** The framework can compute what
  is *mechanically* owed; only the domain records why something owed was
  deliberately not done. Those two answers disagree exactly where it matters.
- **A clean sweep is not evidence of a correct sweep.** Every mechanical
  check would have passed on the overwritten version. The only instrument
  that caught it was an agent that had read the domain.

## The Rule

Run estate-wide operations **per domain, embodied** — one isolated context
each, each reading its own AGENTS.md and orienting before acting — not as a
loop from the centre. Before applying any mechanical step, check whether the
domain records a decision about that step; if it does, the ruling wins and
the skip is named in the commit. Parallelism is fine and desirable; shared
context is not, because the ninth domain reasoned with eight others resident
is no longer reading the ninth.
