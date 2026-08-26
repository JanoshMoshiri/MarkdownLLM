---
id: operating-model-seams-scope-2026-08-26
type: decision
status: made
version: 1.0
created: 2026-08-26
tags: [sprint-scope, analysis, workflow-state, operating-model, seams]
informed_by:
  - id: review-independent-operating-model-2026-08-26-codex
    commit: ed44b2d91b84215fb7a5d95f33a8dbbf2325468b
  - id: floor-block-requirements-2026-08
    commit: 19579efeea0dbd4abe1d0bdbd0499b60d79f1651
  - id: run-operating-model-seams-2026-08
    commit: bc4aabcf140445baae2c824e17fcf1249e0eda09
linked_things:
  - id: run-operating-model-seams-2026-08
    relation: informs
    notes: "The run this analysis-stage decision scopes."
---

# Decision: Operating-Model Seams Sprint Scope

Made by the agent under the operator's execution handover, at the
analysis stage of `run-operating-model-seams-2026-08`. The subject was
fixed by the verified review and the operator's direction in session
("we know the problem, we know our current state, we know where we need
to get to — let's follow our own workflow methodology"); this cut decides
how much one sprint takes.

## The cut

**Necessity** — the sprint fails without these:

- **F18 in full** (definition revision binding): the `workflow-state.md`
  rule — a run pins the committed revision governing it; stay-pinned is
  the default; migration is a deliberate meaning-boundary commit distinct
  from any cursor move; restart/abandon use existing statuses — plus the
  floor legs (pin resolves; membership and edges read through the pinned
  revision; unpinned legacy runs degrade to current behaviour with an
  advisory) and their focused tests.
- **F17 semantics** (activation and fulfilment): the `workflow-state.md`
  section defining initiating evidence and produced evidence on existing
  references (`informed_by` for the demand at birth; outputs pin the run
  back), with `provenance.md` touched only where the chain crosses a
  face. Includes the lesson this run already banked: pins are transcribed
  from the log, never recalled.

**Should** — taken unless the sprint runs long:

- **F19 doctrine**: executor declared separately from gate authority, in
  `workflow-state.md`'s definition-body contract and the gate-authority
  row of `operating-model.md`. No fields.
- **F20 doctrine**: the consumer-owned contract named in
  `operating-model.md` as a composition of existing pieces, with the
  addressing qualification (intended relevance, never delivery authority)
  in the Module-to-Module section. No primitive.

**Stretch** — explicitly droppable:

- The F17 advisory floor check (a completed run with neither an
  initiating pin nor any output pointing at it → Info) and a provenance
  leg at pre-commit that resolves pinned SHAs (motivated by this run's
  own mistyped pin, caught by hand not by the floor).

## Deliberately out

No new artefact types, no modality fields, no consumer-contract
primitive, no porch envelope — every deferral already carries its
condition in the specs (convergence in a second live corpus), per the
review's smallest-repair discipline and the operating model's own
admission rule.
