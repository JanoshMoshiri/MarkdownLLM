---
id: run-operating-model-seams-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-26
definition: substrate-floor-development
current_stage: design
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

## Next — the remaining arc, carried in another harness

**Build through seal goes to the next session, deliberately in a
different harness** (operator's routing, 2026-08-26). Two things come
free from that choice: exercising verify, reconcile and **seal** outside
the harness that designed them is the portability evidence the framework
claims and rarely tests, and the builder is no longer its own verifier
(`a-same-builder-check-is-blind-to-a-self-contradictory-builder`).

Claim the run, then work the design's legs in order. Advance the cursor
`design → build` once the build legs are committed, and carry on through
verify (focused suites first, the full suite at the stage gate, budgets
N3–N6 measured, and an adversarial attempt to *defeat* the
self-authorization guard rather than confirm it), reconcile (the
obligations the design declares, including the two-versions-stale
examples), and seal — where the human gates are the operator's:
version/changelog judgement and the push.

One trap, named because it is this sprint's own mechanism biting its
author: the self-application pin will be **rejected** if it shares a
commit with any cursor move. Pin alone. That is the guard working.

Everything else — the legs, their order, the tests, the budgets, the
rationale for the guard — lives in
`operating-model-seams-design-2026-08` and the specs it implements. This
run deliberately does not restate any of it.
