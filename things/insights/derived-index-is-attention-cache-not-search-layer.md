---
id: derived-index-is-attention-cache-not-search-layer
type: insight
status: active
version: 1.0
created: 2026-06-08
confidence: high
origin: synthesised
source: session — reflexive behaviour design; reconciling derived indexes with the scalability principle
session: 2026-06-08
tags: [derived-index, scalability, belief-revision, reconciliation, transparency]
linked_things:
  - id: derived-index-specification
    relation: informs
  - id: scalability-guide
    relation: challenges
  - id: tracking-artifacts-can-drift-from-reality
    relation: supports
---

# A Derived Index Is An Attention Cache, Not A Search Layer

## The Insight

Introducing derived indexes appeared to contradict a stable principle in `scalability-guide.md`: *"Scale through abstraction, not through search or indexing. Don't build database functionality."* The contradiction is only apparent — it resolves on what "indexing" the principle actually forbids.

The principle forbids an **opaque query/search/database layer that the agent reasons over instead of the data** — hidden state that breaks transparency, portability, and the property that the agent's context *is* the data. A derived index is the opposite on every axis:

- **Transparent**, not hidden — a git-committed markdown file a human can read and diff.
- **Regenerable**, not authoritative — it holds no information not already in the things; the things win on any disagreement.
- **Attention-directing**, not answer-providing — it tells the agent *which* things and *which* signal to look at; the agent still reasons over the actual things.

It is a map back to the data, not a replacement for it. So the principle stands unamended; the index is a permitted instance, and the guide now says so explicitly.

## Why It Matters

This is belief-revision resolving a real tension into `both-valid` rather than `superseded`: the scalability principle and the derived-index spec are both correct because they refer to different things by the word "indexing." Recording the distinction prevents a future session from either (a) deleting derived indexes as a principle violation, or (b) using the precedent to justify a genuine hidden-database layer that *would* violate it. The line is: does the agent reason over the data, or over a proxy for it? Indexes keep the agent on the data.

## Context

Surfaced during the 8 June reflexive-behaviour build, when adding `derived-index.md` required editing the very principle it seemed to break. Rather than weaken the principle, the resolution sharpened its meaning. Captured here as the canonical reconciliation; `derived-index.md` and `scalability-guide.md` both point at it.
