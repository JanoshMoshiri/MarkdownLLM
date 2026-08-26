---
id: run-operating-model-seams-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-26
definition: substrate-floor-development
current_stage: requirements
held_by: claude-framework-session-2026-08-26
informed_by:
  - id: review-independent-operating-model-2026-08-26-codex
    commit: ed44b2d1d3708524a1eddc31358176a37348d654
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

At **requirements**. The problems inventory is the verified review
(ingested and quarantine-lifted 2026-08-26, this run's `informed_by`
pin); the requirements are F17–F20 on `floor-block-requirements-2026-08`
v1.4, committed. This run's own dogfooding note: its `informed_by` pin to
the review is F17 practised before F17 is specified — the initiating
demand named on the run itself.

## Next

The analysis cut: which of F17–F20 this sprint takes, at what depth, as a
`type: decision` with pinned inputs. Then design (the revision-binding
semantics are the load-bearing piece), build, verify, reconcile, seal.
Human gates at seal: version/changelog judgement and the push.
