---
id: framework-reserved-types-need-thing-md-as-single-source
type: insight
status: dismissed
version: 1.1
created: 2026-05-27
confidence: high
origin: inferred
source: session — consistency review
session: 2026-05-27 Session 4
tags: [consistency, reserved-types, single-source-of-truth]
linked_things:
  - id: thing-specification
    relation: references
---

# Framework-Reserved Types Must Have thing.md As Their Single Source

> **Dismissed 2026-06-27.** The fix shipped long ago — thing.md is now the canonical
> reserved-types list (7 types, stable). What remained was a generic single-source-of-
> truth reminder ("update thing.md first when adding a reserved type") already covered
> by the framework's SRP/cohesion discipline, on a type set that no longer churns.
> Origin `inferred`, the oldest insight in the corpus, no distinct ongoing teaching
> value. Kept for audit, not deleted.

## The Insight

When `retrospective` was added as a framework-reserved type in Session 3, it was added to AGENTS.md's Thing Types section — but not to `thing.md`. This created a split source of truth.

The consistency review caught it, but the root cause is structural: there is no enforced rule that says "adding a framework-reserved type requires updating thing.md first, then propagating outward." AGENTS.md was treated as the authoritative list when it should be a summary pointing back to thing.md.

## Why It Matters

`thing.md` is the spec that domain agents and framework agents load to understand what a thing is. If framework-reserved type definitions live in AGENTS.md but not in thing.md, any agent that reads thing.md but hasn't loaded AGENTS.md will have an incomplete picture. AGENTS.md should summarise; thing.md should define.

## Context

Fix applied: thing.md now lists all four reserved types (insight, continuity-brief, conflict, retrospective) with a pointer to the relevant specs. Rule to remember: when a new reserved type is added, update thing.md first.
