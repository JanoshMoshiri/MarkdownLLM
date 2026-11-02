---
id: seats-are-named-for-the-clone-not-the-agent-2026-10-30
type: decision
status: made
version: 1.0
created: 2026-10-30
session: 2026-10-30
decided_by: Janosh Moshiri
confidence: high
origin: stated
exposed: false
tags: [seat, clone, identity, naming, a2a, ticket, harness-agnostic]
linked_things:
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: extends
    notes: "That ruling made the seat a declared, floor-readable identity; this one settles what the identity is named after. Nothing else in it moves."
  - id: the-seat
    relation: informs
    notes: "The answer to the plan's two-week trigger: this clone had declared a seat, and the declaration was wrong the first time its occupant changed."
  - id: standing-watch-specification
    relation: references
    notes: "Actors are seats; a seat's name is now the clone's, and the agent sitting in it is the declaration's second field."
---

# Seats Are Named For The Clone, Not The Agent

## Context

The `the-seat` plan's two-week trigger fired on 2026-10-29 asking whether
every clone that takes turns had declared its seat. This clone had — as
`codex (codex)`, declared 2026-10-24 — and on 2026-10-30 a Claude session
arrived in it. Every commit from this clone since 2026-10-24 reads as
codex's turn; the first commit of the Claude session would have too. The
seat had been named after the agent that happened to be sitting in it, so
the first time the occupant changed, the record would have misnamed the
author. The second clone is known in the record as Workspace-2 and carries
the same shape of name.

## Ruling (the operator's words, 2026-10-30)

> This domain and framework substrate was running with Codex, but I think
> it's probably going to be better to just call it MarkdownLLM workspace 1.
> And my other one is workspace 2. I think that's a better name because
> it's agnostic. So sometimes it's Codex, today it's Claude, tomorrow it
> might be GLM. Who knows?

A seat is named for the **clone** — the working copy that takes turns — and
the name is agnostic of whoever sits in it. The agent is the declaration's
second field (`--agent`), redeclared when the occupant changes; the name is
not.

## What changed

- This clone: `mdllm seat . --set workspace-1 --agent claude`
  (2026-10-30). Commits from here now carry `workspace-1`.
- The second clone is `workspace-2`; its redeclaration is the operator's
  act on that machine, not something this clone can do for it.

## What follows, and is not done here

- The root schema's `ticket` vocabulary (`claude / codex / closed`) names
  seats by the old convention. The one ticket on record is closed, so
  nothing live reads it. The vocabulary becomes `workspace-1 / workspace-2 /
  closed` when both seats carry the new names — a definition-surface change
  with its own walk, not folded into this ruling.
- The `the-seat` plan's Phase 6 reads this as its first observation: a
  declared seat that was wrong by naming, caught by an occupant change, not
  by the digest.
