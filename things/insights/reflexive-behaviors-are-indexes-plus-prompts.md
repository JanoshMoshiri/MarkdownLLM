---
id: reflexive-behaviors-are-indexes-plus-prompts
type: insight
status: active
version: 1.0
created: 2026-06-08
confidence: high
origin: synthesised
source: session — reflexive behaviour design (git telemetry, trigger eval, conflict scan, schema review)
session: 2026-06-08
tags: [reflexive, derived-index, orchestration, design-principle, srp]
linked_things:
  - id: derived-index-specification
    relation: informs
  - id: orchestration-specification
    relation: references
  - id: tracking-artifacts-can-drift-from-reality
    relation: extends
---

# Reflexive Behaviours Are Derived Index + Bound Prompt

## The Insight

Four capabilities the agent was missing — git-as-telemetry (velocity), systematic trigger evaluation, systematic conflict scanning, and schema-coherence review — turned out to be one pattern, not four. Each is the agent reasoning *about* the domain rather than *within* it, and each decomposes into the same two parts:

1. **A derived index** — a regenerable cache aggregating the relevant signal across all things, so the behaviour is O(index) not O(all things). (Velocity is the exception: its signal already lives in git, so it needs no index — caching it would only add a drift surface.)
2. **A bound prompt** — the reasoning template that reads the index/log and acts, attached to the lifecycle moment where it belongs (session-start for velocity and trigger eval; on-status-change and retrospective for conflict scan; retrospective for schema review).

## Why It Matters

This is the framework's own SRP/decomposition principle confirming itself: when several proposed features share an identity and a reason to change, they should be one primitive instantiated several times, not several bespoke mechanisms. Defining `derived-index.md` once and instantiating it for triggers/relationships/schema kept the surface area small and consistent. It also means future reflexive behaviours have a known shape: find the signal, decide whether it needs an index or already exists as ground truth (like git), write a bound prompt. The user named this before the design did — "the same pattern along all these different lines."

## Context

Surfaced while working through Janosh's four "what can agents do that the framework isn't exploiting" items. The unification became obvious once the maintenance model (ride `post-write`) and the read model (index at session start) were the same for three of the four, and the fourth (velocity) declined an index for a principled reason rather than an arbitrary one.
