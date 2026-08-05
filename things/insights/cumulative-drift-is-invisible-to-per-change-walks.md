---
id: cumulative-drift-is-invisible-to-per-change-walks
type: insight
status: active
version: 1.0
created: 2026-08-05
session: 2026-08-05
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Standing cadence razor — decides when an unscoped sweep is owed; candidate for promotion into change-reconciliation.md or retrospective.md once a second sweep confirms the cadence."
linked_things:
  - id: change-reconciliation-specification
    relation: informs
    notes: "Names a blind spot in the spec's own scoping: the Walk is scoped to one inflection's blast radius, and some surfaces are outside every single blast radius while inside the union of all of them."
  - id: a-generated-surface-collapses-its-walk
    relation: complements
    notes: "The other escape. That insight kills restatement cost by generation; this one names the class generation can't reach (narrative, curated, judgement-shaped surfaces) and gives it a different instrument."
  - id: tracking-artifacts-can-drift-from-reality
    relation: supports
    notes: "The 2026-06 phenomenon, now with its mechanism: those artifacts drift because their truth is coupled to accumulation, so no per-change walk ever visits them."
  - id: substrate-currency-sweep
    relation: derived-from
    notes: "The evidence. The sweep that found the class and is itself the instrument that clears it."
---

# Cumulative Drift Is Invisible to Per-Change Walks

## The Insight

Change-reconciliation walks the blast radius of *one* change. But some
surfaces are coupled to the **accumulation** of many changes, not to any
single one — inventories (a spec table), walkthroughs (a first-hour guide),
measured figures (a token count), curated lists (a CLI section). No single
release puts them at risk enough to enter its walk; every release moves them
a little. Their drift is real, monotonic, and **outside every individual
blast radius while inside the union of all of them.**

## Evidence (2026-08-05 sweep)

Nine releases (v3.18 → v3.26) each ran their reconciliation honestly — the
specs and floor stayed coherent throughout. The same nine releases left
README nine releases stale (14 of 23 specs listed, the estate CLI layer
absent, a token figure 40% off), the newcomer walkthrough ignorant of three
major mechanisms, and the end-session ritual updated on one of its five
surfaces. Per-change discipline was *kept*, and the perimeter rotted anyway.

## The Two Escapes

1. **Generate the surface** (`a-generated-surface-collapses-its-walk`) —
   right for mechanical restatements (counts, inventories, ritual steps).
2. **Run an unscoped Assimilate periodically** — right for narrative and
   judgement-shaped surfaces that generation can't produce. The
   substrate-currency-sweep is the instrument: floor first, then greps keyed
   to each release's changes, then judgement reads, oldest-touched first.

A surface that keeps reappearing in unscoped sweeps is telling you it wants
escape 1.

## The Razor

When drift is found on a surface, ask: *was this inside any single change's
blast radius?* If yes — a walk was missed; tighten the walk. If no — no walk
would ever have caught it; the surface needs generation or a sweep cadence,
and blaming the per-change discipline is aiming at the wrong instrument.
