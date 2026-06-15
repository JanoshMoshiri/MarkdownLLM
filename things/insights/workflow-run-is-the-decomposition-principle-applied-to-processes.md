---
id: workflow-run-is-the-decomposition-principle-applied-to-processes
type: insight
status: active
version: 1.0
created: 2026-06-15
session: 2026-06-15
source: both
confidence: high
origin: synthesised
tags: [thing-model, workflow, decomposition, concurrency, clean-architecture]
linked_things:
  - id: workflow-state-specification
    relation: informs
  - id: composition-is-the-inverse-of-decomposition
    relation: supports
  - id: the-notation-changed-not-the-primitives
    relation: supports
  - id: continuity-briefs-solve-external-state-drift
    relation: challenges
---

# A Workflow Run Is the Decomposition Principle Applied to Processes

## The Insight

The framework modelled **knowledge state** richly — insights, conflicts, decisions, provenance, continuity — but barely modelled **workflow state**. Workflows existed only as *definitions* (prose in a workflow skill); there was no representation of a workflow *run*, so the run-state of a long-running, multi-session instance had to be reconstructed by hand each session from the continuity brief and the related things.

The fix is not a new mechanism. A run is the **instance** of a workflow **definition** — exactly the `template-for` / `instance-of` pair the decomposition section of [thing.md](../../thing.md) already governs. Today workflow definitions *violate* that principle: the skeleton lives as prose in a skill and the instance does not exist at all, so run-state smears across `continuity.md` and a pile of things. Minting `workflow-definition` + `workflow-run` is **finishing the decomposition**, not bolting on a feature.

## Why It Matters

Two things move at once. First, run-state becomes *read*, not reconstructed: `current_stage` is a cursor into the definition's stage set. Second, the worst concurrency object in the design — `continuity.md`, a single-writer singleton and merge-conflict magnet — is decomposed away: two operators on two different instances now touch two different files, which git merges without thought. Only same-instance contention remains, addressable with a lightweight advisory `held_by` claim rather than a lock.

The razor it passes: almost everything is inherited (it is a thing; decisions pin via provenance; transitions commit at git meaning boundaries; the definition pointer is `instance-of`). Only three things are irreducibly new — the **cursor** (`current_stage`), the **coordination claim** (`held_by`), and a **per-instance resume point** (the body). This mirrors composition's "four lines, not a new mechanism" signature: the proof it is a genuine primitive is how little it adds. It is the constructive sibling of [composition-is-the-inverse-of-decomposition](composition-is-the-inverse-of-decomposition.md) — there the existing discipline was half-applied in one direction; here it had never been applied to a *kind of thing* (a process) at all.

## Context

Surfaced by the third independent review (2026-06-15), which moved this gap from theoretical ("gap 4, parked" in the continuity brief) to felt: a real domain running a multi-session pipeline was reconstructing instance state by hand every session. The review's framing — "spec when foreseeable, deploy when felt" — settled that a primitive being undeployed in a domain does not make it not-primitive, exactly how the framework already treats `conflict` and `index`.
