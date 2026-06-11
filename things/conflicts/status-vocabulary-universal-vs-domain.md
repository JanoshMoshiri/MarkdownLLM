---
id: status-vocabulary-universal-vs-domain
type: conflict
status: resolved
created: 2026-06-11
session: 2026-06-11
parties:
  - validate-thing-specification
  - domain-specification-guide
resolution: superseded
resolved_by: domain-specification-guide
confidence: medium
origin: inferred
linked_things:
  - id: validate-thing-specification
    relation: references
  - id: domain-specification-guide
    relation: references
  - id: framework-v3-transformation-plan
    relation: references
    notes: "Phase 1 was the designated resolution path; resolved same day"
---

# Universal Status Enum vs Domain-Defined State Machines

## The Clash

The framework simultaneously asserts that domain things must use a fixed universal
status vocabulary and that domains may define their own status state machines. Both
positions are load-bearing, and live domain practice has already chosen a side.

## Position A — validate-thing-specification

Level 1 (Structural Validation) declares: `status` value must be one of
`not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled` —
severity **Error** — with exceptions only for framework-internal types
(specification/guide/manifesto, insight, index). `thing.md` states the same
vocabulary for domain things. Under this rule, every one of the 17 things in the
live jmtm-software domain (statuses: `confirmed`, `open`, `upcoming`, `met`,
`submitted`, `in-preparation`, `pending`) is structurally invalid.

## Position B — domain-specification-guide

The guide (and validate.thing.md's own Level 3) treats status workflows as
domain-defined: domains may declare state machines with valid transitions, and the
jmtm-software workflow skill builds an explicit compliance state machine
(`open → figures-ready → submitted → paid → reconciled`) that is *better* domain
modelling than the universal enum. Level 3 validates against the domain's declared
transitions — implying the vocabulary is the domain's to define.

## The Resolution Question

Which layer owns the status vocabulary? The proposed resolution (transformation
plan, Phase 1): the domain owns it. thing.md and validate.thing.md change to
"status must be in the domain's declared vocabulary (via the normative domain
schema); the six universal workflow values are the default when no schema exists."
jmtm-software's vocabulary then gets declared, not corrected. Resolution lands when
Phase 1 ships and both specs are updated.

## Resolution

**Resolved 2026-06-11, same session, outcome `superseded`.** Position B (the
guide's domain-defined state machines) survived. The domain owns its status
vocabulary, declared in the normative schema (`things/_schema.yaml`) and enforced
deterministically by `tools/mdllm.py validate`. The six universal workflow values
became the advisory default applying only when a type declares no vocabulary.

Implemented in: `thing.md` v2.11 (status field rewritten),
`validate.thing.md` v2.0 (mechanical floor delegated to mdllm; status table
replaced with domain-ownership rule), `domain-specification-guide.md` v2.6
(schema declaration added to domain structure), and
`domain/jmtm-software/things/_schema.yaml` (the live domain's vocabulary
declared as correct rather than corrected). The `contradicts` links on both
parties were downgraded to `references` per the resolution protocol.
