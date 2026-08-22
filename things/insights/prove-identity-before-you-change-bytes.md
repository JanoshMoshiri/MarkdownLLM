---
id: prove-identity-before-you-change-bytes
type: insight
status: active
version: 1.0
created: 2026-08-22
session: 2026-08-22
source: agent
confidence: high
origin: synthesised
tags: [refactor, sequencing, golden-fixtures, proof, commit-granularity, design]
linked_things:
  - id: substrate-floor-development
    relation: informs
    notes: "A design-stage sequencing rule for the process: when a change set contains both restructuring and behaviour change, the design orders them so each is provable."
  - id: run-floor-sprint-2-2026-08
    relation: derived-from
    notes: "Commits A and B were byte-identical by construction with goldens as the proof; commit C then changed bytes once, deliberately, against a known-good structure."
  - id: recognition-data-must-be-frozen-not-derived
    relation: complements
    notes: "The sequencing is what made that defect findable: the byte change landed against an already-verified structure, so the failing frozen-hash tests could only mean the fragment change."
---

# Prove Identity Before You Change Bytes

## The Insight

A refactor that moves code and changes output *in the same commit* can prove
neither. The golden fixtures — the strongest evidence available that
restructuring preserved behaviour — become unusable the moment the same
change also alters what is emitted: a golden diff no longer means "the
refactor broke something," it means "something changed, and the two candidate
causes are indistinguishable." So the fixture gets regenerated, the diff gets
waved through, and the one instrument that could have caught a structural
mistake has been spent on a behavioural one.

Sequence them apart and both become provable. Land the restructuring **byte-
identical by construction** — goldens unchanged is the proof — then change
the bytes once, deliberately, against a structure already known good.

## How It Surfaced

Sprint 2 moved the hook byte contract to a leaf module, collapsed duplicated
adapter emission into a shared module, and added existence-guards that alter
every emitted hook body and definition hash. The design ordered them A, B, C:
A and B claimed byte-identity (proven against `HEAD` for the resolution
fragment and all three hook bodies, and by unchanged goldens for both
adapters), and C alone regenerated goldens and reinstalled the root hooks.

The ordering paid for itself immediately. When C's frozen-hash tests failed,
the cause was unambiguous — the structure had already been verified twice —
so the failure could be read for what it was: recognition data that had been
computed from the live renderer all along. Had the move and the byte change
shared a commit, that failure would have been indistinguishable from
refactor damage, and the most likely response would have been to regenerate
the frozen hashes and lose the finding entirely.

## Why It Matters

- **Proof is a property of sequencing, not of effort.** The same three
  changes in one commit produce the same code and no evidence.
- **It makes byte-identity a claim the commit message can carry** —
  and therefore something a reviewer or a later session can check, rather
  than trust.
- **It concentrates the blast radius.** One commit changes hashes across the
  estate; everything before it is provably inert, so a drift report
  elsewhere has exactly one candidate cause.

## The Rule

At design time, split a change set into byte-identical restructuring and
deliberate behaviour change, and order identity first. State the proof for
each restructuring commit before writing it — if you cannot name what would
demonstrate identity, the split is not yet right.
