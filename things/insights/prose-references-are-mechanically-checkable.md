---
id: prose-references-are-mechanically-checkable
type: insight
status: active
version: 1.0
created: 2026-06-24
session: 2026-06-23
source: both
confidence: high
origin: inferred
linked_things:
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: challenges
    notes: "Refines it — the prose dark region is not monolithic; its referential layer is mechanical."
  - id: existence-is-not-currency
    relation: supports
  - id: mis-keyed-links-pass-the-floor-silently
    relation: supports
    notes: "That hole was in frontmatter links; this is the same hole one layer out, in body prose."
---

# The Prose Dark Region Has A Mechanical Half — Referential Integrity

## The Insight

The "prose dark region" splits cleanly in two, and only one half is actually dark.
**Semantic** agreement between prose — does spec A's *claim* still hold after spec B
changed? — is irreducibly interpretive. But **referential** integrity in prose — does
a `[[id]]` wikilink or an inline `{framework_root}/X.md` mention point at something that
*exists*? — is mechanical, and the floor doesn't check it today: `validate` covers
frontmatter `linked_things`, `coherence` covers the spec catalog, but **body references
are unverified**. Distinguishing the two tells you exactly where mechanization stops.

## Why It Matters

- It refines `mechanical-assimilation-is-blind-to-prose-dependencies`: the dark region
  is smaller than it looks. The part worth ceding to agent judgement is *semantic*
  agreement; the *referential* part is a missing mechanical check, not an inherent limit.
- It names a concrete, scoped addition to `mdllm coherence` — flag broken `[[id]]`
  wikilinks and broken inline spec-path references — that converts one interpretive
  cohesion surface into a mechanical one. It fits the `existence-is-not-currency` family:
  a reference that names a thing must resolve to a thing that exists.
- It gives change-reconciliation one less surface to walk by hand each time, shrinking
  the diligence-dependent floor toward the mechanical one.

## Context

During the v3.15.0 change-reconciliation, the agent hand-checked that every `[[wikilink]]`
in `things/` and every `{framework_root}/X.md` prose mention resolved — a pass `validate`
and `coherence` don't perform. The manual check came back clean, but *having to do it by
hand* is the tell: it is a mechanizable surface currently left to diligence. Generalises
[[mis-keyed-links-pass-the-floor-silently]] (a frontmatter-link hole) outward to body prose.
