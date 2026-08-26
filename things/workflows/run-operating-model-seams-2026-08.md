---
id: run-operating-model-seams-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-26
definition: substrate-floor-development
definition_commit: bbc17c355b85ae044d88f1825b445746e312e50d
current_stage: seal
held_by: codex-desktop-2026-08-26
informed_by:
  - id: review-independent-operating-model-2026-08-26-codex
    commit: ed44b2d91b84215fb7a5d95f33a8dbbf2325468b
linked_things:
  - id: review-independent-operating-model-2026-08-26-codex
    relation: references
    notes: "The initiating demand: the verified convergence review's four seams, plus the operator's direction in session — 'we know the problem, we know our current state, we know where we need to get to; let's follow our own workflow methodology.'"
  - id: floor-block-requirements-2026-08
    relation: references
    notes: "The requirements surface this run is cut from — F17-F20, added v1.4. This run never restates them."
  - id: run-floor-sprint-3-2026-08
    relation: references
    notes: "The sealed predecessor run of the same definition."
  - id: universal-workflow-methodology
    relation: implements
    notes: "Doubly: the run follows the substrate specialisation of the methodology, and its subject is closing the seams that make the methodology fully operable. Designated at birth as the candidate for the first worked example (type: example) of the methodology executing itself, to be distilled at seal."
---

# Run: Operating-Model Seams — 2026-08

The sprint that makes the operating model fully operable: the four seams
the verified convergence review named (F17–F20), worked through the
substrate's own specialisation of the operator's universal workflow
methodology — deliberately, as its own demonstration. **Example-candidate:**
at seal, this run's story is distilled into a `type: example` thing — one
of the first documented executions of the methodology on real work.

## Where This Is

At **seal**. Build and verification remain as recorded below. The declared
reconciliation walk closed in `12ff5ef`: operative wording, adoption
templates, both example corpora, derived indexes and the worked
self-application example now agree with the new contract. The remaining work
is closure only — update the plan and requirements ledger to truth, make the
version/changelog judgement, release the advisory claim, and report
publication debt.

## Verify record (2026-08-26)

**Full suite:** 752 passed, 1 skipped in 220.4s under `-n auto` — N7 met
against ≤12 minutes. The focused revision-binding file passed all 11
tests in 8.853s — N6 met against ≤120s.

Steady-state budget readings:

| ID | Budget | Measured | Verdict |
|---|---|---|---|
| N3 precommit, framework root (pinned run live) | ≤12s | 4.208s, exit 0 | met |
| N4 precommit, 54-thing live domain | ≤5s | 1.143s | met for latency; candidate remained red on pre-existing domain-kernel drift |
| N5 validate, same live domain | ≤3s | 0.931s, exit 0 | met |
| N6 focused affected file | ≤120s | 8.853s | met |

**Adversarial guard attempt:** a staged candidate migrated from the v1
definition pin to a v2 revision whose graph authorised `intake → done`
*and* moved the cursor to `done` in the same run-file diff. The candidate
was rejected for changing both `definition_commit` and `current_stage`;
the attack test passed in 1.822s. This attempts the bypass the guard exists
to prevent rather than merely exercising a friendly transition.

**Context, not a sprint regression:** the largest live corpus
tested (251 things) measured ~24s and was already red on a stale
session attestation plus domain-kernel drift. It contains no workflow
runs, so neither revision resolution nor pinned Git reads execute there;
its quarantine-heavy validation path is an existing separate performance
surface, recorded rather than silently substituted for this sprint's
changed path.

## Reconcile record (2026-08-26)

**Cue:** the operator explicitly requested the reconciliation suite after the
workflow/operating-model inflection. The significant read was pinned to
`45a582b3fc424cb3bf812e235be3cc576615098d`; HEAD was asserted unchanged
immediately before the reconciliation writes.

**Assimilate and walk:** declared touchpoints for workflow state, the operating
model, the universal methodology and the substrate definition were walked with
their linked insights, review, plan and active run. A literal sweep for
`prior committed definition`, `definition_commit`, transition language and
executor/authority wording found one stale operative statement in
`validate.thing.md`, one stale maturity summary in `workflow-state.md`, and the
anticipated birth/example adoption surfaces. Historical review and design
statements were kept historical rather than rewritten.

**Actions:** `validate.thing.md` 3.1 now distinguishes pinned governing
revisions from legacy prior-definition semantics; workflow birth templates
teach revision pins, activation/fulfilment and performer versus gate authority;
the life-manager definition/run pair is a real pinned worked instance with an
initiating evidence pin; both example agents absorbed framework 3.35.0. The
promoted workflow-run insight now distinguishes its three-field birth shape
from the later optional revision pin. The design input's non-resolving
transcribed SHA was corrected from Git history.

The pinned example exposed a direct-validation seam: a nested corpus did not
resolve revisions at its containing repository. The resolver now discovers the
owning Git root once while keeping the scan scoped to the requested corpus;
the twelfth focused gitfs test pins that case. No additional primitive or
per-run Git scan was introduced.

**Seal of the walk:** all four indexes were rebuilt (280 framework things),
coherence has no Errors or Warnings, provenance has no sprint-specific Warning,
and both example corpora validate without Errors or Warnings in the framework
pass. The life-manager direct pass is also clean of Errors/Warnings apart from
its pre-existing retrospective-cadence Info. The kernel was not regenerated:
no `<!-- kernel -->` block moved, and the literal kernel sweep found no stale
copy. No spec was added or removed, so the framework-map count/node residue was
not implicated. The framework example is deliberately `exposed: false` because
this doctrine travels through version + domain refresh, not a served face.

**CHANGELOG judgement:** the changelog is a generated per-push release surface.
The domain-facing adoption note therefore travels with the next version/push;
writing a release entry without authorising that release would make the
changelog contradict its own contract. Publication remains the human gate.

## Next — seal

Mark the sprint design complete, disposition F17–F20 on the requirements
ledger without closing the broader ledger, run the final candidate and
reconciliation checks, close this run at its terminal stage, and report the
unpushed release debt. The actual push remains unauthorised.
