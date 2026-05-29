---
id: srp-extraction-is-tier-promotion
type: insight
status: active
version: 1.0
created: 2026-05-29
session: 2026-05-29
source: agent
confidence: high
origin: synthesised
linked_things:
  - id: tiered-loading-is-tiered-reading-applied-to-specs
    relation: extends
  - id: thing-specification
    relation: references
  - id: example-things-specification
    relation: supports
  - id: reasoning-lenses-specification
    relation: supports
---

# SRP Compliance and Context Load Reduction Are the Same Operation

## The Insight

When embedded content is extracted from a low-tier spec (Tier 0 or Tier 1) into a dedicated spec, it automatically becomes a Tier 2 candidate — moving from loading in every session to loading only on demand. Following the Single Responsibility Principle and reducing baseline context load are not competing goals; they are the same act applied to knowledge organisation. You cannot follow SRP on a spec file without also improving context economics.

## Why It Matters

This gives LLMs a concrete, operational reason to prefer extraction over embedding — not just for cleanliness, but because it directly affects how cheaply the framework can be reasoned on. When deciding whether to keep content inline or extract it into a dedicated spec, the question "does this serve a different audience or change at a different rate?" has an immediate practical consequence: if yes, every session that doesn't need that content is currently paying to load it anyway. This should sharpen the decomposition decision in both directions: extraction becomes more obviously worth doing, and the cost of leaving violations in place becomes measurable.

## Context

The 29 May 2026 SRP correction sweep extracted `type: example` content from `thing.md` (Tier 0) and multi-lens reasoning from `read.thing.md` and `write.thing.md` (Tier 1) into dedicated Tier 2 specs. The CHANGELOG analysis showed that baseline context load was lower post-v2.8.0 than pre-v2.8.0 despite adding two new spec files — because the content had always been there, just always loaded. The insight is that this outcome was not incidental: it is what SRP compliance at the spec level always produces.
