---
id: decision-status-vocabulary-domain-owned
type: decision
status: made
created: 2026-06-11
session: 2026-06-11
decided_by: both
confidence: high
informed_by:
  - id: status-vocabulary-universal-vs-domain
    commit: e876b28
  - id: framework-retrospective-2026-06
    commit: e876b28
  - id: framework-v3-transformation-plan
    commit: 258fa67
linked_things:
  - id: thing-specification
    relation: informs
    notes: "Implemented in thing.md v2.11 status rewrite"
  - id: validate-thing-specification
    relation: informs
    notes: "Implemented in validate.thing.md v2.0 mechanical floor"
---

# Decision: The Domain Owns Its Status Vocabulary

## Context

The 2026-06-11 framework review found every thing in the live jmtm-software
domain failing validate.thing.md's Level 1 status check at Error severity,
undetected. The spec held two positions simultaneously (the pinned conflict
thing documents both): a fixed universal status enum at Error severity, and
domain-defined state machines at Level 3. One had to win.

## Inputs Considered

- The conflict thing (pinned at its open state): both positions stated, with the
  observation that the domain's vocabulary was better modelling than the enum.
- The June retrospective: the enforcement gap is live; LLM-only validation
  missed a mechanical rule violation in production.
- The transformation plan: Phase 1 designated this resolution and specified the
  normative-schema mechanism.

## Options

1. **Correct the domain** — force jmtm things into the six universal statuses.
   Rejected: destroys real state-machine information (`figures-ready`, `reconciled`)
   to satisfy a generic rule; the map would be worse than the territory.
2. **Domain-declared vocabularies, tool-enforced** — each domain declares its
   statuses in `_schema.yaml`; the universal six become the advisory default.
   Chosen.
3. **No vocabulary rule at all** — any string is a valid status. Rejected: typos
   and synonym drift (`done` vs `completed`) would accumulate undetected, exactly
   what a deterministic floor exists to prevent.

## Decision

The domain owns its status vocabulary (option 2). Declared per-type in the
normative schema; enforced at Error severity by `mdllm validate` when declared;
the universal six apply at Warning severity when nothing is declared.
Framework-reserved types keep fixed vocabularies domains cannot redefine.
Decided jointly: the agent proposed it in the review, Janosh confirmed by
directing the transformation plan's execution.

## Consequences

- thing.md v2.11 and validate.thing.md v2.0 rewritten; conflict resolved
  (`superseded`, the guide's position survived).
- jmtm-software's vocabulary was declared, not corrected (`things/_schema.yaml`).
- Every future domain declares its state machines as part of scaffolding
  (domain-specification-guide v2.6).
- This record is the framework's first `type: decision` — its own inputs are
  pinned to the commits at which they were read, making it the working example
  of the provenance chain it implements.
