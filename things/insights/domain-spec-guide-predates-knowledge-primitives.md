---
id: domain-spec-guide-predates-knowledge-primitives
type: insight
status: promoted
version: 1.1
created: 2026-05-27
confidence: high
origin: stated
source: session — consistency review
session: 2026-05-27 Session 4
promoted_to: domain-specification-guide
tags: [domain-specification-guide, continuity, insight, conflict, retrospective]
linked_things:
  - id: domain-specification-guide
    relation: references
  - id: session-memory-specification
    relation: references
  - id: belief-revision-specification
    relation: references
  - id: retrospective-specification
    relation: references
---

# domain-specification-guide.md Predates The Knowledge Primitives

## The Insight

The `domain-specification-guide.md` was last meaningfully updated before `session-memory.md`, `belief-revision.md`, and `retrospective.md` existed. A new domain created by following the current guide will have no awareness of:

- `continuity.md` (the live session-continuity document)
- `type: insight` and `things/insights/`
- `type: conflict` and `things/conflicts/`
- `type: retrospective` and `things/retrospectives/`
- The session-end:continuity ritual

The domain will work fine structurally, but it won't benefit from the knowledge management layer unless a human explicitly tells it about these primitives.

## Why It Matters

The domain-specification-guide is how new domains are bootstrapped. It is the first place an LLM looks when creating a new domain. If the guide doesn't mention the knowledge primitives, new domains will silently skip them.

## Context

Originally deferred during the 27 May Session 4 consistency pass. The guide was subsequently updated to v2.5 with all knowledge primitives integrated: `continuity.md` in the domain structure, `type: insight`/`type: conflict`/`type: retrospective` in a dedicated Knowledge Management section, session-end:continuity in the AGENTS.md template, and knowledge sub-folders in the scaffolding steps. The design question (where in the creation flow to introduce these) was resolved as Day 1 setup — they are part of the initial scaffold, not optional extensions.

Promoted to `status: promoted` on 28 May 2026 during holistic framework review.
