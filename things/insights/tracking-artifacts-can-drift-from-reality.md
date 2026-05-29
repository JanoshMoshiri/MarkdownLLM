---
id: tracking-artifacts-can-drift-from-reality
type: insight
status: active
version: 1.0
created: 2026-05-28
confidence: high
origin: synthesised
source: session — holistic framework review
session: 2026-05-28
tags: [consistency, tracking, single-source-of-truth, discoverability]
linked_things:
  - id: domain-spec-guide-predates-knowledge-primitives
    relation: references
  - id: thing-lifecycle-specification
    relation: references
  - id: validate-thing-specification
    relation: informs
---

# Tracking Artifacts Can Drift From Reality

## The Insight

The framework has now had two instances of the same pattern: something exists in the repo but the tracking surfaces (AGENTS.md inventory, CHANGELOG known gaps, insight status) don't reflect reality.

1. **thing-lifecycle.md** — A complete draft spec at root, invisible to AGENTS.md. Existed since 23 May, not discoverable until 28 May when explicitly added.
2. **domain-specification-guide.md** — Updated to v2.5 with all knowledge primitives, but the CHANGELOG (v2.5.0) still listed it as a "known deferred gap" and the insight tracking it was still `status: active`.

Both are instances of work getting committed without all tracking surfaces being updated in the same transaction. The framework's "single source of truth" claim is undermined when multiple surfaces disagree about what's done.

## Why It Matters

This is a recurring risk, not a one-off. Every time a spec is created or updated, there are potentially 3–4 surfaces to maintain: the spec itself, AGENTS.md inventory, CHANGELOG, and any related insight or WORKLOG entry. Missing one creates a silent inconsistency that can persist for days until someone does a full review.

A possible mitigation: validation (validate.thing.md) could include a check for orphaned specs — files at root matching `*.md` with YAML frontmatter that don't appear in AGENTS.md's spec inventory. This would have caught thing-lifecycle.md on day one.

## Context

Both instances discovered during the 28 May holistic framework review. The pattern is: focused work sessions commit the primary artifact correctly but don't sweep all secondary references. The consistency pass at the end of 27 May Session 4 caught five bugs of this kind — suggesting end-of-session sweeps help, but aren't foolproof.
