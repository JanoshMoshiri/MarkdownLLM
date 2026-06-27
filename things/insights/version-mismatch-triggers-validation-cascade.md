---
id: version-mismatch-triggers-validation-cascade
type: insight
status: promoted
version: 1.1
created: 2026-06-02
promoted_to: orchestration-specification
session: 2026-06-02
source: both
confidence: high
origin: synthesised
tags: [version-check, validation, hard-hooks, design-pattern, tier-0]
linked_things:
  - id: orchestration-specification
    relation: informs
  - id: domain-refresh-specification
    relation: informs
  - id: hard-hooks-require-observable-agent-caused-triggers
    relation: extends
  - id: tiered-loading-is-tiered-reading-applied-to-specs
    relation: complements
---

# Version Mismatch Should Trigger Validation, Not Just Surfacing

## The Insight

When a domain agent detects a framework version mismatch at session start, the correct first response is to run `validate.thing.md` against the domain's existing things — not merely to surface the mismatch and wait for the user to decide what to do.

A newer framework version may have changed what valid things look like: new required fields, changed status vocabularies, updated relation values, or structural rules. Surfacing the mismatch alone leaves the domain in an ambiguous state — the user knows something changed but doesn't know whether their things are still valid. Running validation immediately answers the most urgent question before the session proceeds.

## Why This Matters

This pattern reuses existing infrastructure (validate.thing.md) rather than inventing a new "check framework changes" workflow. It follows the framework's own principle of minimal new machinery — the validation spec already knows how to check structural, referential, and semantic integrity. Version detection + validation is therefore: detect (tiny sentinel read) → assess (existing spec) → report → offer refresh.

## The Paired Insight

This cascades with the observation that version detection itself must be done via a tiny, single-purpose sentinel file (`.markdownllm`) rather than reading CHANGELOG.md. The cost model matters: reading CHANGELOG.md on every session to detect a mismatch wastes context on sessions where nothing changed. Reading a few lines of `.markdownllm` costs almost nothing. The sentinel's job is to be cheap. The cascade into validation is only triggered when the cheap check fires — not on every session.

## Generalisation

For any Tier 0 session-start check that must be cheap:
1. Read only a tiny sentinel field (not a narrative document)
2. If the check passes: no further cost incurred
3. If the check fails: cascade into the appropriate existing machinery

This is the session-start equivalent of the tiered loading principle applied to things.
