---
id: domain-spec-guide-predates-knowledge-primitives
type: insight
status: active
version: 1.0
created: 2026-05-27
confidence: high
origin: stated
source: session — consistency review
session: 2026-05-27 Session 4
tags: [domain-specification-guide, continuity, insight, conflict, retrospective, deferred]
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

Deliberately deferred — adding this to the guide is a small but non-trivial update because it requires deciding *where in the domain creation flow* these concepts are introduced (before or after the first session? as optional extensions? as Day 1 setup?). Not urgent for domains that are actively developed with a human in the loop, but important before the framework is used more autonomously.
