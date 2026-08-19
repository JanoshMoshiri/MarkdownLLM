---
id: a-generated-contract-change-is-an-estate-migration
type: insight
status: active
version: 1.1
created: 2026-08-18
session: 2026-08-18
source: agent
confidence: high
origin: synthesised
tags: [generated-surfaces, migration, currency, rollout, compatibility]
linked_things:
  - id: a-generated-surface-collapses-its-walk
    relation: complements
    notes: "Generation collapses reconciliation cost; this insight names the inverse rollout consequence when all consumers enforce currency against that generator."
  - id: existence-is-not-currency
    relation: complements
    notes: "Same-builder currency is the mechanism that turns a shared generator change into immediate estate-wide drift."
  - id: vendor-harness-adapter-foundation
    relation: derived-from
    notes: "Gate 7.0 kept the managed-block builder stable; an authored QMS probe was later removed after JMTM proved the shared repair without it, avoiding an unnecessary estate migration."
---

# A generated contract change is an estate migration

## The Insight

A same-builder currency check gives a shared generator an important outbound
consequence: changing the generator makes every existing consumer stale at
once. The edit may be local and mechanically cheap, but its deployment is an
estate migration wherever consumers validate themselves against the current
builder.

## Why It Matters

This is the inverse face of generated surfaces collapsing the reconciliation
walk. Generation removes hand-edited restatements and makes drift visible, but
it also removes the ability to roll a new contract out consumer by consumer
unless the design provides a versioned or authored compatibility seam. Before
changing a shared generator, ask whether every currency-enforcing consumer may
adopt the new bytes now. If not, introduce the compatibility surface first and
leave the canonical builder stable until migration is deliberately offered.

## Context

Gate 7.0 needed to correct the manual MarkdownLLM launch route in one active QMS
domain. Changing the domain-kernel builder would have fixed the text in one
place, but all thirteen managed domains compare their entry blocks against that
same current builder; the other twelve would have become stale and potentially
commit-blocked before the operator's Phase 8 rollout decision. The first probe
therefore put authored compatibility prose in QMS without touching the shared
builder. A later JMTM session — still on the older domain entry surface and
without the paragraph — successfully used the shared launcher and the
restricted-then-approved sync path. That differential proved the authored QMS
addition redundant, so it was removed rather than offered estate-wide. The
general rule remains: change a currency-enforced generator only when the
resulting estate migration is intentional, not merely because one probe used a
local seam.
