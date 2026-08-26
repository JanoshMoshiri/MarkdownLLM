---
id: run-operating-model-seams-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-26
definition: substrate-floor-development
definition_commit: bbc17c355b85ae044d88f1825b445746e312e50d
current_stage: reconcile
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

At **reconcile**. The spec/doctrine half remains the committed design input
(`f1ca2bc`, `96a207c`). The mandatory revision-binding floor and focused
tests landed in `02e6c7c`; the F17 activation/fulfilment advisory stretch
landed separately in `6d1adf8`; self-application landed, pin-only, in
`1725a6f`; verification is sealed in `4317e6c` and green on the changed
surface.

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

## Next — the remaining arc, carried in another harness

**Build through seal goes to the next session, deliberately in a
different harness** (operator's routing, 2026-08-26). Two things come
free from that choice: exercising verify, reconcile and **seal** outside
the harness that designed them is the portability evidence the framework
claims and rarely tests, and the builder is no longer its own verifier
(`a-same-builder-check-is-blind-to-a-self-contradictory-builder`).

Enter reconcile: run the declared touchpoint/literal/conceptual walk,
bring the two stale example surfaces forward, add the domain-facing
CHANGELOG adoption note, and regenerate any derived surfaces. Then seal;
version judgement and the push remain the human gates.

Everything else — the legs, their order, the tests, the budgets, the
rationale for the guard — lives in
`operating-model-seams-design-2026-08` and the specs it implements. This
run deliberately does not restate any of it.
