---
id: mechanical-assimilation-is-blind-to-prose-dependencies
type: insight
status: active
version: 1.0
created: 2026-06-14
session: 2026-06-14
source: both
confidence: high
origin: synthesised
tags: [change-reconciliation, validation, limits-of-automation, human-in-the-loop]
linked_things:
  - id: change-reconciliation-specification
    relation: informs
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: supports
  - id: tracking-artifacts-can-drift-from-reality
    relation: supports
---

# Mechanical Assimilation Is Blind to Prose Dependencies

## The Insight

The Assimilate beat of a change-reconciliation pass is complete only over
**declared** edges — the `linked_things` relations and `informed_by`/`derived-from`
pins that the `relationships` and `provenance` indexes can walk. Dependencies
expressed in **prose** are invisible to those indexes: routing tables, narrative
cross-references, embedded lists, one thing named in another's body. The
mechanical pass will report a clean, complete assimilation while a real
dependency sits untouched in plain text.

This surfaced the day `change-reconciliation.md` shipped. The spec was wired into
every frontmatter-level surface — sentinel, catalog, `mdllm` tiers, framework-map
edges — and the blast-radius query came back clean. Yet the one dependency that
actually governed whether a domain agent would *load* the spec, the `AGENTS.md`
Tier 2 routing table, was a prose table the index could not see. The human caught
it; the machine could not.

## Why It Matters

It is the structural reason the **Walk is human-backed**, not a convenience.
Mechanical assimilation narrows the field and guarantees the *declared* set is
complete; the expert is the irreducible backstop for the prose the machine cannot
read. The practical discipline: when a change is significant, ask explicitly
*"what refers to this in prose, not in frontmatter?"* — and shrink the dark region
over time by promoting prose mentions into declared edges. It is also a caution
against trusting a clean automated report as proof of completeness — the same
drift risk recorded in `tracking-artifacts-can-drift-from-reality`.

## Context

Caught 2026-06-14 in the first live use of `change-reconciliation.md`: the
operator's worry — "will my domain agent even pick this up?" — located a touch
point the mechanical assimilate had missed. The fix added the routing row; this
insight captures why the miss was structural, not an oversight to be automated
away. The lesson is made operative in `change-reconciliation.md` → Walking the
Dark Region, and as a spec-change checklist item in `AGENTS.md`.
