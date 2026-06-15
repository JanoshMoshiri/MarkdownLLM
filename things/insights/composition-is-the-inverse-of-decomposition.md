---
id: composition-is-the-inverse-of-decomposition
type: insight
status: active
version: 1.0
created: 2026-06-15
session: 2026-06-15
source: both
confidence: high
origin: synthesised
tags: [thing-model, decomposition, refactoring, clean-architecture, knowledge-organisation]
linked_things:
  - id: thing-specification
    relation: informs
  - id: srp-extraction-is-tier-promotion
    relation: supports
  - id: the-notation-changed-not-the-primitives
    relation: supports
  - id: session-memory-specification
    relation: informs
---

# Composition Is the Inverse of Decomposition

## The Insight

`thing.md`'s cohesion discipline was specified in one direction only: **decompose** — split a thing that holds more than one reason to change. Its mirror was never written. When a single responsibility is instead *spread across several things* — duplicate insights, converged methodologies, a rule restated in four places — the move is the inverse: **compose**, consolidating the fragments into the one cohesive thing and tombstoning the rest via the existing `supersedes`/`superseded-by` vocabulary.

The operational consequence: "insight consolidation" was never a new feature to design. An insight *is* a thing, so managing insights is managing things — and the discipline for that already existed, merely half-applied. The gap was a missing direction, not a missing primitive.

## Why It Matters

This is a razor for evolving the framework: **when a new gap looks like it needs a new primitive, first check whether an existing discipline is only half-applied.** Completing the discipline is cheaper, more coherent, and leans on proven technique (here, the SOLID/clean-architecture treatment `thing.md` already encodes) rather than bolting on bespoke machinery for a reserved type. It is the constructive sibling of [the-notation-changed-not-the-primitives](the-notation-changed-not-the-primitives.md): that one rejects new mechanisms when the primitives haven't changed; this one says the existing primitive's *discipline* may simply be incomplete — extend it, don't duplicate it.

## Context

Surfaced 2026-06-15 (session 2) while specifying insight lifecycle management. The proposed "consolidation" mechanism dissolved the moment the human reframed it as a problem already solved in `thing.md` — only the compose direction was unwritten. Reusing `supersedes` for the tombstone (rather than inventing a relation) was the deliberate move; it forced one reconciliation, broadening `belief-revision.md`'s narrow "incorrect or outdated" definition of `supersedes` to cover replacement-by-consolidation as well as replacement-by-correction — the single contradiction the change-reconciliation walk caught.
