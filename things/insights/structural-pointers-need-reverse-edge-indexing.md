---
id: structural-pointers-need-reverse-edge-indexing
type: insight
status: active
version: 1.0
created: 2026-06-16
session: 2026-06-16
source: both
confidence: high
origin: synthesised
tags: [change-reconciliation, derived-index, schema-evolution, completeness]
linked_things:
  - id: change-reconciliation-specification
    relation: informs
  - id: derived-index-specification
    relation: informs
  - id: workflow-state-specification
    relation: informs
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: supports
---

# Structural Pointers Are Declared Edges the Index Must Walk

## The Insight

When a relationship earns its own singular frontmatter field instead of living in
`linked_things` — the `parent` precedent, and now `definition` on a
`workflow-run` — the `relationships` index stops seeing it, because the index was
built solely from `linked_things`. The edge is still **declared** and
**structured**; it is simply declared *somewhere else*. So a reverse read over the
index — "what points at this thing?" — silently omits a definition's runs and a
parent's children, even though both are first-class declared edges.

This is distinct from, and sharper than,
`mechanical-assimilation-is-blind-to-prose-dependencies`. That blindness is to
*prose* — the dark region the machine genuinely cannot read, and the structural
reason the Walk is human-backed. This one is a blindness in the **lit** region: a
declared, machine-readable edge that the index just wasn't taught to walk. The
spec promised "total recall over what is declared, like a compiler listing every
call site," and for `definition`/`parent` that promise was quietly false —
degrading to whatever the textual-trace grep happened to catch.

## Why It Matters

The change-reconciliation Assimilate beat is only as complete as the indexes it
reads. A forward referential check (does `definition` resolve? is `current_stage`
a member?) does not imply reverse recall (given this definition, which runs
instance it?) — the two directions are separate mechanisms, the same lesson the
bidirectional version-check already taught. The fix is to emit structural pointers
into the `relationships` index alongside `linked_things`, after which both the
forward and retrospective reconciliation modes inherit the recall for free, because
both read the same index.

The durable rule is general and forward-looking: **any singular load-bearing
pointer added to the schema must also be emitted into the `relationships` index, or
it becomes an unwalked declared edge.** This recurs every time the framework mints
the next `parent`-shaped field. The deeper tell: a forward resolver and a reverse
index are two obligations, and adding the field is only half the work.

## Context

Surfaced 2026-06-16 from a design review of the just-shipped `workflow-state.md`.
The `workflow-definition` → `workflow-run` link is carried by the structural
`definition:` field (chosen deliberately, modelled on `parent`). Tracing the floor
showed `build_index_body`'s `relationships` signal walked only `linked_things`,
and the `provenance` reverse index only `informed_by`/`derived-from` — so changing
a definition would not mechanically surface its runs. `parent` had the same latent
gap since it was introduced; the orphan check already treated it as a relationship,
but the index never emitted it. Made operative in `change-reconciliation.md` (the
Assimilate beat and Dark Region tiers now name structural pointers) and
`derived-index.md` (the `relationships` index aggregates every declared edge
wherever it lives), with a floor self-test pinning the behaviour.
