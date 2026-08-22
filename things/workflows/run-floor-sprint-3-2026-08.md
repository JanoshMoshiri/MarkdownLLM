---
id: run-floor-sprint-3-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-23
definition: substrate-floor-development
current_stage: requirements
held_by: claude-code
linked_things:
  - id: run-floor-sprint-2-2026-08
    relation: references
    notes: "The sealed predecessor. Its seal record names this sprint's subject explicitly — 'Sprint 3 (derivation: F8's three phases) starts as a new run of substrate-floor-development when execution resumes, generating from the module layout this sprint settled.'"
  - id: coherence-mechanism-build
    relation: references
    notes: "Problem owner for the whole of F8; its four phases are this sprint's work inventory, and its precondition (a settled module layout) was met at sprint 2's seal."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Phase 2's owner. Canonical on which checks to build and their same-builder gate; this run never restates its items."
  - id: floor-block-requirements-2026-08
    relation: references
    notes: "The requirements surface this sprint is cut from; the requirements stage decomposes F8 there rather than minting a duplicate."
---

# Run: Floor Sprint 3 — derivation

## Where This Is

At `requirements`. Born there, same as both predecessors: the `problems`
stage was satisfied before this run existed. Sprint 2's seal record named
the subject, `coherence-mechanism-build` carries the evidence for every
phase (the eight-round review loop's measurement — derived surfaces held
clean in all eight rounds, hand prose never did), and the plan's
precondition — derive from a settled module layout, not one about to be
reshaped — was discharged by sprint 2's landed structure work. No
aspirational entries.

## What closes with this sprint

Sprint 3 is the floor block's last *buildable* sprint. Of the block's
fifteen requirements: F1 and F9–F13 landed in sprint 1, F3–F7 in sprint 2,
and F8 is this sprint. What remains after it is not buildable here —

- **F2** — owner `evidence-and-eval-backlog` is operator-sequenced and now
  stalled 27 days; surfaced again at this sprint's seal, not absorbed.
- **F14** — left unbuilt on sprint 2's measurement, with a dated re-open
  condition at the requirements ledger.
- **F15** — recorded with mechanism and a proposed shape; widening a product
  config surface needs its own analysis cut.

That matters for sequencing: the operator's order puts the framework
retrospective after the block, and its time trigger fires 2026-08-27.

## Next

Decompose F8 at `floor-block-requirements-2026-08` (v1.3) with the slice
that has already landed marked as such, then advance to `analysis` for the
cut.
