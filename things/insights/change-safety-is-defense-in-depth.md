---
id: change-safety-is-defense-in-depth
type: insight
status: active
version: 1.0
created: 2026-06-15
session: 2026-06-15
source: both
confidence: high
origin: synthesised
tags: [change-reconciliation, validation, software-engineering, architecture]
linked_things:
  - id: change-reconciliation-specification
    relation: informs
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: supports
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: supports
  - id: retrospective-specification
    relation: supports
---

# Change Safety Is Defense in Depth, Not a Single Gate

## The Insight

No single mechanism catches every way a change can break a domain, because the
dependencies a change touches are tiered — declared, literal, conceptual (see
`mechanical-assimilation-is-blind-to-prose-dependencies`) — and each tier needs a
different tool. The mature posture is the one professional software engineering
settled on: **layer overlapping, progressively cheaper nets so a miss falls
through to the next, and what survives them all is rare and cheap to catch later.**

The framework's nets, in order: **design for change** (single source of truth —
link, don't restate — shrinks the dark region before the change); **static trace**
(the `relationships`/`provenance` indexes walk declared edges); **textual trace**
(grep for the literal name, reaching prose references the indexes miss);
**invariants** (consistency assertions re-checked forever — deferred while the
retrospective covers the same ground); **the walk** (the expert reconciles the
conceptual residue); and the **retrospective** (the standing backstop that catches
whatever slipped every change-time net).

## Why It Matters

It reframes the inherent dark region from a flaw into a managed condition: you do
not eliminate misses, you make them progressively rarer and cheaper. It sets the
build priority — the cheapest net that closes the widest gap wins (textual trace
was that net). And it keeps the human exactly where they belong: not as a net
among nets, but as the backstop for the residue no mechanical net can reach.

## Context

Synthesised 2026-06-15 while mapping software-engineering change-safety practice
onto the framework through the birth/run/evolve lifecycle. The textual-trace net
was added to `change-reconciliation.md` the same session and immediately caught a
spec-count drift the deterministic floor structurally could not see — defense in
depth proving itself on first use. The invariants/test-suite tier was deliberately
deferred: the retrospective is the standing backstop, and a second mechanism for
the same job would be redundant machinery.
