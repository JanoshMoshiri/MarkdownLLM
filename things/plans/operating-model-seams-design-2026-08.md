---
id: operating-model-seams-design-2026-08
type: plan
status: in-progress
version: 1.0
created: 2026-08-26
priority: high
tags: [design, workflow-state, revision-binding, activation, sprint]
informed_by:
  - id: operating-model-seams-scope-2026-08-26
    commit: 8a88c40b1436330b39894572e7325571966dd9a1
linked_things:
  - id: run-operating-model-seams-2026-08
    relation: informs
    notes: "The run whose design stage this satisfies."
  - id: floor-block-requirements-2026-08
    relation: references
    notes: "F17-F20 are the requirements this design meets; never restated here."
---

# Design: Operating-Model Seams Sprint

All work is additive — no restructuring, so no identity-first split is
needed; every commit is deliberate behaviour change against verified
structure.

## F18 — revision binding (mechanism)

**Spec** (`workflow-state.md` v0.5 → 0.6, new section *Revision Binding*):

- A run MAY carry `definition_commit: <full-sha>` — the commit whose
  committed definition governs this run. Set at run creation to the
  then-HEAD (or any commit containing the governing definition bytes).
- **Stay-pinned is the default.** A definition change never moves a live
  run. Migration is a deliberate act: a commit that changes
  `definition_commit` and nothing else on the run. Restart/abandon use
  existing statuses.
- **The self-authorization guard (non-negotiable, operator-pinned):** a
  single commit changing both `definition_commit` and `current_stage` on
  one run is rejected by the floor — otherwise a run could authorize its
  own move by choosing a friendlier revision. This mirrors the existing
  rule that a definition migration and a cursor advance are separate
  meaning-boundary commits.
- Legacy runs without the pin keep today's semantics (transition checked
  against the prior committed definition) and draw an Info advisory
  naming the adoption remedy.

**Floor** (`tools/markdownllm/validation.py`,
`workflow_transition_findings` and the run-reference checks):

- Pin resolves: `definition_commit` is a commit in this repo whose tree
  contains the definition. Resolution: try the definition's HEAD path at
  the pinned commit (`git show sha:path`); on a miss (file moved since),
  locate by id in the pinned tree — bounded fallback, rename-proof.
- Stage membership and edge existence for a pinned run are read from the
  **pinned** revision's definition, not HEAD's prior state.
- The both-changed rejection above (Error), scoped to the run file's own
  diff — a definition file changing in the same commit is a different
  file and stays governed by the existing separate-commits rule.
- Git reads batched per corpus (F12 pattern); measured at verify against
  N3–N5 — no budget regression.

## F17 — activation and fulfilment (semantics on existing references)

**Spec** (`workflow-state.md`, new section *Activation and Fulfilment*):

- **Initiating evidence:** the demand that instanced a run is pinned in
  the run's `informed_by` at creation (thing + full SHA, transcribed from
  the log — never recalled; this sprint's own run banked that lesson).
  A self-initiated run (routine maintenance) may have none; that is
  legal and stated.
- **Produced evidence:** durable outputs carry `informed_by` → the run
  (+ commit). The chain demand → run → output is then walkable in both
  directions through the existing reverse-provenance index — no new
  index, no new artefact type.
- **Fulfilment:** whether the terminal output satisfies the initiating
  demand is judged at `review-verify` and recorded in the run's closing
  narrative; the floor checks link presence only, never adequacy.
- Stretch only: an Info finding for a *completed* run with neither an
  initiating pin nor any output pointing at it.

## F19 — executor vs authority (doctrine)

`workflow-state.md` definition-body contract gains one sentence pair: the
body declares **who or what performs** each stage (human, agent,
deterministic automation, hybrid) *separately from* **who may authorise**
its transition or accept its output. `operating-model.md` gate-authority
dimension row gains the same distinction. No fields; the two-live-modules
condition for machine-readable modality is stated beside it.

## F20 — consumer contract + addressing (doctrine)

`operating-model.md` Module-to-Module gains: the consumption contract as
a named composition (address-book entry · import triggers · the
definition an admitted input starts · the fulfilment output class · the
cadence that makes silence visible), consumer-owned always; and the
addressing qualification — *addressed* is declared intended relevance on
the exposed thing, never delivery authority. A shared "contract" between
two modules is really two contracts, one per direction, each owned by
that direction's consumer.

## Reconcile-stage obligations (declared now)

Grep for "prior committed definition" across specs + kernel and update
any sentence F18 changes (kernel regen only if a kernel block moves);
walk the examples (both corpora are two versions stale — pay or defer on
the record); life-manager's definition/run pair models the new
semantics; CHANGELOG carries the domain-facing adoption note.

## Focused test set (N6 ≤ 120s per file)

New `test_workflow_revision_binding.py`: pin resolves · membership via
pin · edge via pin · both-changed rejection · legacy fallback + advisory
· rename-proof resolution. Extended activation tests beside the existing
workflow tests: initiating pin recognised · output-to-run chain indexed ·
stretch advisory fires only on completed runs.

## Commit granularity

1. spec: workflow-state v0.6 (F18 + F17 sections, F19 sentence)
2. spec: operating-model 0.2 (F19 row, F20 paragraph)
3. tool: revision-binding legs + tests
4. tool: activation advisory (stretch, droppable)
5. self-application: this sprint's run pins itself — first pinned run
6. reconcile walk · 7. verify record

## Risks

- **Git-read cost** — mitigated by batching; measured at verify.
- **Rename resolution** — bounded id-scan fallback; tested explicitly
  (the atom's own move to the spec layer is the live precedent).
- **Adoption confusion** — additive-optional everywhere; Info-grade
  advisories; CHANGELOG note travels with the next version bump.
- **Scope creep at build** — F19/F20 are sentences, not sections; if
  either grows past a paragraph it returns to analysis.
