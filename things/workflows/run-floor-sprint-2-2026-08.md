---
id: run-floor-sprint-2-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-22
definition: substrate-floor-development
current_stage: verify
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

## Build record

- **F3 landed** (4cb9ca9): gate inverted, three-module exception probe held
  exactly (model.py/evals.py excepted, sync.py reworded), 8/8 fitness green.
- **Commit A / F4 landed** (fb587a1): leaf move byte-identical (SH_RESOLVE
  1528 chars + all three hook bodies proven against HEAD). Two deviations
  from the design, recorded as they happened:
  1. `LAUNCH_RESOLUTION_SECONDS` **stayed in harness_ports** — it sits in a
     cohesive family of lifecycle-timing constants; moving one member out
     fractured the family for leaf purity the module never claimed absolutely.
     The leaf now imports the ports contract (stdlib-pure leaf → leaf edge,
     depending toward stability); its docstring says so.
  2. `MDLLM_ENTRY` became **late-bound through the leaf** in scaffold — the
     move exposed a double-binding (two module-level copies) that two tests
     were monkeypatching around; one binding now serves every consumer and
     every test double.
- **Commit B / F5 collapse landed** (6d3aa81): `project_hook_emission` owns
  the converged shape (quoting, envelope, POSIX command, binding-hash
  payload, placeholder); goldens unchanged — byte-identity proven. 161
  focused tests green.
- **Commit C / probe guards landed** (b33f6b4): `[ -x ]` + `command -v`
  guards; measured 348→273ms root, 514→311ms domain-repo per lifecycle
  invocation. Third deviation, found by the frozen-hash tests:
  3. The **output-tail legacy definitions were live-computed** — recognition
     data that would drift with every renderer change. The v1 fragment is
     now frozen as data (`adapters/legacy/sh-resolve-v1.txt`) and threaded
     through the legacy paths; the original frozen hashes pass again, which
     is the proof the freeze reproduces history. Root hooks reinstalled
     (execution test passed); estate domains reconcile via refresh, and
     their doctors will honestly report definition drift until they do.
- Necessity (F3, F4, F5) is complete. 230 focused tests green at b33f6b4.
- **F6 landed** (9ed15a2, bc29e8e, c0c194c, 9726711): corpus_harness
  extracted (cross-file test imports gone), then estate-sync+autopush,
  membrane, and session-gate lifted along their banners. Monolith
  3601 → 2675 lines; collection count 696 held at every step. Two more
  cross-section helpers (_trust_mcp_entry, _consumer_with_import) surfaced
  and moved to the harness. One transient xdist flake observed once
  (test_imports_freshness_fresh_then_stale) and green on every re-run —
  watched at verify.
- **F7 record leg landed** (1e400e5): platform-coverage limitation recorded
  in the suite README and the CI workflow header; module→test map updated.
- Should scope complete. Stretch (F7-matrix, F14) waits on verify per the
  design gate.

## Notes

Sprint 1's two recorded deviations carry forward as constraints: the F11
in-process composition variant stays open only if margin is ever needed (it
is not, at current measurements), and F4's move must land as part of the F5
adapter reshaping, not as a half-inversion.
