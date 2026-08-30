---
id: operating-layer-staleness-review-2026-08-30
type: artifact
status: evolving
version: 1.0
created: 2026-08-30
session: 2026-08-30
tags: [staleness, coherence, operating-layer, workflows, watertight, review]
linked_things:
  - id: watertight-membrane-sprint-2026-08-30
    relation: implements
    notes: "Phase E — the operator's ask: workflows become each domain's driving force, so the mechanism keeping the entry file and skills current must be watertight."
  - id: operating-layer-quality-loop
    relation: derived-from
    notes: "That plan built the skill-vocabulary check and the retrospective scan this review verifies in the field; this is the first estate-wide reading of its coverage."
  - id: mechanical-coherence-checks-backlog
    relation: informs
    notes: "One candidate check routed to its suppression-list gate: workflow stage vocabulary in skills, below."
---

# Operating-Layer Staleness Review — 2026-08-30

The question, as the operator put it: workflows are about to be each
domain's driving force — is the mechanism that keeps AGENTS.md and the
skills from going stale after changes watertight? Reviewed estate-wide,
against the live floor at v3.37.0.

## What the floor already holds — verified in the field, not from prose

**Eight corpus-general coherence checks** ride every domain's pre-commit
hook: stable-staleness, dead declared vocabulary, zero-run workflow
definitions, redundant known-fields, template residue, derived-index drift
(Error), domain-kernel drift (Error), and skill-vocabulary drift (Warning —
a skill instructing a type, status, or field the schema never declared).
The generator and the drift check share one builder, so they cannot
disagree.

**Field verification, this session:**

- **Hook bytes: 13/13 domains byte-identical to the contract.** Compared
  installed `pre-commit` bytes against `rendered_hook_contract` per clone —
  not presence, identity. Zero drift, zero missing.
- **Generated AGENTS.md blocks: 12/13 domains carry them**, so the
  domain-kernel Error arm is live almost everywhere.
- **The checks bite in practice:** this session's own framework commits were
  blocked twice for index drift, and two domain writes were blocked by the
  strict session gate until fresh attestations were recorded. The boundary
  is enforcing, not advisory.

## Findings

1. **One domain has no generated blocks** — the parked one (four unrunnable
   workflows, park recorded 2026-08-28). Its entry file predates the
   domain-kernel mechanism entirely (references v3.12/v3.14 mechanics,
   retired continuity surfaces). **Deliberately not fixed here:** injecting
   generated blocks into an old-shape entry file is half a refresh performed
   on a dormant domain. The recorded decision: its wake-up act is
   `domain-refresh`, which brings the blocks; until then the park is its
   protection.
2. **Version drift is live in the two most active regulated domains** — both
   report `framework_version_seen: 3.36.0` against v3.37.0. The downward
   version-check surfaced it correctly at session-start; the refresh → adopt
   → seal walk is each domain agent's own arc and is owed, not overdue (the
   3.37 delta is one day old).
3. **The one genuine gap — workflow stage vocabulary in skills.** The
   skill-vocabulary check keys skills to `_schema.yaml` and the reserved
   sets. It does not key stage names. A domain whose skills instruct its
   workflow stages by name (one regulated domain has five per-stage SDLC
   skills) gets no check that those names match the definition's declared
   `stages` — rename a stage in the definition and every skill instructing
   the old name drifts silently, exactly where "workflows as the driving
   force" concentrates future change. **Routed as a candidate to
   `mechanical-coherence-checks-backlog`'s gate, not built here** — it is
   mechanical (stage ids are declared data; skill text is scannable), it has
   one live near-instance, and the backlog owns the decision of what may
   become a check.
4. **The egress leak, fixed this session:** the face render carried the
   producer's `exposed: true` across the membrane; a consumer landing the
   render verbatim would re-export the import unexamined. Floor fix +
   regression test + spec sentence landed together (thing.md v2.22); found
   live by the first mirror re-sync.

## Verdict

Watertight where the floor reaches: byte-identical hooks, dual-Error drift
gates on generated surfaces, and a vocabulary check that fires on undeclared
instruction. The residue is exactly three items — a parked domain whose
protection is its park, an owed one-day version refresh, and one named check
candidate now sitting at the gate that owns it.
