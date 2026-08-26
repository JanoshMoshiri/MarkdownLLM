---
id: run-operating-model-seams-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-26
definition: substrate-floor-development
definition_commit: bbc17c355b85ae044d88f1825b445746e312e50d
current_stage: verify
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

At **verify**. The spec/doctrine half remains the committed design input
(`f1ca2bc`, `96a207c`). The mandatory revision-binding floor and focused
tests landed in `02e6c7c`; the F17 activation/fulfilment advisory stretch
landed separately in `6d1adf8`. The focused revision suite and its
neighbouring workflow/reference suites are green, including the
adversarial migration-plus-cursor case.

## Next — the remaining arc, carried in another harness

**Build through seal goes to the next session, deliberately in a
different harness** (operator's routing, 2026-08-26). Two things come
free from that choice: exercising verify, reconcile and **seal** outside
the harness that designed them is the portability evidence the framework
claims and rarely tests, and the builder is no longer its own verifier
(`a-same-builder-check-is-blind-to-a-self-contradictory-builder`).

Run the full suite once at this gate, measure N3–N6, and attempt to *defeat* the
self-authorization guard rather than merely confirm it. Then reconcile
the design's declared obligations (including the stale examples) and
seal; version/changelog judgement and the push remain the human gates.

One trap, named because it is this sprint's own mechanism biting its
author: the self-application pin will be **rejected** if it shares a
commit with any cursor move. Pin alone. That is the guard working.

Everything else — the legs, their order, the tests, the budgets, the
rationale for the guard — lives in
`operating-model-seams-design-2026-08` and the specs it implements. This
run deliberately does not restate any of it.
