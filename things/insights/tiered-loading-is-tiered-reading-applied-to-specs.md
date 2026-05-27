---
id: tiered-loading-is-tiered-reading-applied-to-specs
type: insight
status: active
version: 1.0
created: 2026-05-27
confidence: high
origin: synthesised
source: session — context window cost analysis
session: 2026-05-27 Session 4
tags: [startup, context-window, architecture, performance]
linked_things:
  - id: thing-specification
    relation: references
  - id: orchestration-specification
    relation: references
---

# Tiered Loading Is Just Tiered Reading Applied To Specs

## The Insight

The framework already had a tiered reading model for *things* (Level 1: metadata only / Level 2: relationships / Level 3: full context). But the startup sequence applied flat "load all" to *specs*.

When the framework grew to 16+ spec files (~60k tokens), the inconsistency became expensive. The fix was not a new idea — it was applying an existing principle to a new target.

Wherever the framework says "load X before proceeding" there is a latent question: does everything in X need to be loaded at full depth, every time? The answer is almost always no.

## Why It Matters

This insight generalises. Every time a new spec, primitive, or skill is added to the framework, the default instinct is "add it to startup." That instinct grows the mandatory load. The right instinct is: "which tier does this belong to, and what query type triggers it?"

## Context

Measured cost before: ~60k tokens mandatory (30–65% of a typical model's context window). After tiered startup: ~15k tokens for Q&A, ~33k for read/write, ~60k only for new domain creation. The architecture was already correct; only the application was missing.
