---
id: inbound-edges-decide-which-plan-survives-consolidation
type: insight
status: active
version: 1.0
created: 2026-08-11
session: 2026-08-11
source: both
confidence: high
origin: synthesised
linked_things:
  - id: external-review-response-2026-08-10
    relation: references
    notes: "The instance: 80% superseded by a better-informed successor, yet kept alive shrunk because that successor delegates R3/R4 to it by name"
  - id: coherence-mechanism-build
    relation: references
    notes: "The successor whose deliberate no-restatement rule created the delegation — the pointer that decided the outcome"
  - id: divergence-is-an-unrouted-decision
    relation: supports
    notes: "Retiring a delegated-to plan is the silent-default sin at the plan layer: the orphaned items resolve however they fall out"
---

# Inbound Edges Decide Which Plan Survives Consolidation — Not Which One Feels Stale

## The Insight

The kernel's compose rule says: one responsibility spread across several things
→ consolidate into the cohesive survivor, mark the rest `superseded-by` it. It
reads as though supersession is total — one thing wins, the others retire. In
practice a plan can be *substantially* superseded and still be the sole owner
of a residue, and then retiring it is wrong however stale it feels.

The deciding evidence is not the author's sense of which document is better. It
is **what other live things point at.** A successor that deliberately refuses to
restate other plans' items (correctly — one owner per fact applies to plans too)
creates delegation edges *into* the plan it supersedes. Those edges are load-
bearing: retire the target and the pointer dangles, and every item the successor
delegated is orphaned with no owner at all.

The move is therefore not retire-or-keep but **shrink to the residue**: strip
everything the successor genuinely absorbed, mark it superseded in place, and
leave the thing alive holding only what nothing else owns — with its id intact
so the inbound pointers still resolve.

## Why It Matters

- **It converts a plan-layer retirement into a checkable question.** Before
  retiring any thing, read its inbound edges (`mdllm touchpoints <id>`). If a
  live thing delegates *to* it by name, full retirement is a broken-body
  reference waiting to happen — the exact class queued on
  `mechanical-coherence-checks-backlog`.
- **It names the silent default at the plan layer.** "This is done, bin it" is
  how delegated items resolve by falling out rather than by routing. The three
  honest routes apply to plans as they do to any divergence.
- **It is the cost of the one-owner rule, and worth paying.** Because a good
  successor declines to restate, supersession is often partial by construction.
  Partial supersession is a normal, stable state — not a mess to be tidied into
  a single document.

## Context

Surfaced 2026-08-11. The operator, reading the eight-round loop's conclusion,
judged `external-review-response-2026-08-10` no longer needed. It was indeed
mostly superseded: its build sequencing had been overtaken by
`coherence-mechanism-build`, written with evidence the older plan was staged to
wait for. But that successor's Phase 4 named the older plan as the owner of R3
and R4 and deliberately did not restate them. Retiring it would have dangled
that pointer and orphaned three live items. The plan was shrunk from 142 lines
to its residue instead, and the operator's intent — most of it gone — was met
without losing what only it held.
