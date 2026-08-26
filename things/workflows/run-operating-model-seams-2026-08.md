---
id: run-operating-model-seams-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-26
definition: substrate-floor-development
current_stage: design
held_by: unheld — released 2026-08-26 for the build handover; the next builder claims it
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

At **design**, with the design committed
(`operating-model-seams-design-2026-08`): F18 revision binding carrying
the operator-pinned self-authorization guard as its non-negotiable
centre; F17 on existing references; F19/F20 as bounded doctrine. The
operator reviewed the constraint set in session and pinned the guard
("we can't let that slip"); external contract-map diagrams from a second
agent independently drew F20's consumer-owned-contract shape — the
convergence rule fed twice in one day.

**The spec half of build is already committed** — do not redo it:

- `spec: workflow-state v0.6` (f1ca2bc) — revision binding incl. the
  self-authorization guard, activation/fulfilment, executor-vs-authority.
- `spec: operating-model 0.2` (96a207c) — consumer contract, addressing,
  the executor/authority row.

## Next — build handover (operator's routing, 2026-08-26)

The remaining build legs go to a **Codex session**; this Claude session
returns at **verify**. Split chosen by the operator so the builder and
the verifier are different agents — the same separation
`a-same-builder-check-is-blind-to-a-self-contradictory-builder` argues
for, applied deliberately rather than after the fact.

**For the builder.** `operating-model-seams-design-2026-08` is the
contract; build to it, not to this summary. Remaining legs, in its
declared order:

1. **Floor legs** — `tools/markdownllm/validation.py`, around
   `workflow_transition_findings` (index view only, ~line 319): resolve
   `definition_commit`; read stage membership and edges from the
   **pinned** revision for pinned runs; keep today's prior-HEAD path for
   unpinned runs plus the Info adoption advisory; rename-proof resolution
   (current path first, id-scan in the pinned tree as fallback); batch
   git reads per corpus. Register `definition_commit` where the
   structural-reference/field registry requires it.
2. **The non-negotiable** — reject (Error) any single commit that changes
   both `definition_commit` and `current_stage` on the same run.
   Rationale is `a-check-is-only-as-trustworthy-as-who-controls-its-inputs`;
   read it before touching this leg. It is not optional and not
   simplifiable.
3. **Focused tests** — new `test_workflow_revision_binding.py` covering:
   pin resolves · membership via pin · edge via pin · both-changed
   rejection · legacy fallback + advisory · rename-proof resolution.
   Plus activation cases beside the existing workflow tests.
4. **Stretch, droppable** — the F17 Info advisory (completed run with no
   initiating pin and no output pointing at it), and pin resolution at
   the pre-commit provenance leg.
5. **Self-application** — this run adds its own `definition_commit`,
   becoming the estate's first revision-bound run. Its own guard applies:
   that pin lands in a commit that moves nothing else on this run.

Claim this run (`held_by`) before starting; leave the cursor at `design`
until the build legs are committed, then advance to `build`.

**Then verify** (Claude, next session): focused suites, full suite at the
stage gate, budgets N3–N6 measured, and an adversarial read of the guard
specifically — the verifier's job is to try to defeat it, not confirm it.
Reconcile obligations are declared in the design (including the
two-versions-stale examples); seal holds the human gates.
