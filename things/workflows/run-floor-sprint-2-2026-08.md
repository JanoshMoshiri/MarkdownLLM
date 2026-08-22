---
id: run-floor-sprint-2-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-22
definition: substrate-floor-development
current_stage: build
held_by: claude-code
linked_things:
  - id: run-floor-sprint-1-2026-08
    relation: references
    notes: "The sealed predecessor whose seal record assembled this sprint's problem inventory: F3/F4/F5/F6/F7 at floor-structure-residue, F8 at coherence-mechanism-build, N1's worktree-walk residual, and the requirements thing's measurement-protocol definition."
  - id: floor-structure-residue
    relation: references
    notes: "Problem owner for the structure items; its review rows are the evidence the problems stage requires."
  - id: floor-block-requirements-2026-08
    relation: references
    notes: "The requirements surface this sprint is cut from; the requirements stage revises it (measurement protocol, sprint-2 rows) rather than minting a duplicate."
---

# Run: Floor Sprint 2 — structure

## Where This Is

Born at `requirements` — the `problems` stage was satisfied before this run
existed, same as sprint 1: the problem inventory was assembled by sprint 1's
seal record, and every item carries evidence. The structure items (F3–F7)
cite review rows in `floor-structure-residue`; F4 carries sprint 1's recorded
layering evidence for its deferral (`SH_RESOLVE` lives in runtime, which
imports the leaf — the clean move rides with F5's reshaping); the N1
worktree-walk residual and the measurement-protocol gap are measured findings
in sprint 1's verify record. No aspirational entries.

## Next

Build, in the design's order: F3 (gate inversion + sync.py rewording) →
commit A (F4 leaf move, byte-identical) → commit B (F5 adapter collapse,
byte-identical) → commit C (probe guards — the one deliberate byte change,
root hooks reinstalled) → D (corpus_harness extraction) → E… (per-section
monolith lifts under the collection-count invariant) → F (F7 record leg) →
stretch only after necessity + should are verified. Deviations recorded
here as they happen, not reconstructed. Design: `floor-sprint-2-design-2026-08`
(550fb37).

## Notes

Sprint 1's two recorded deviations carry forward as constraints: the F11
in-process composition variant stays open only if margin is ever needed (it
is not, at current measurements), and F4's move must land as part of the F5
adapter reshaping, not as a half-inversion.
