---
id: run-floor-sprint-2-2026-08
type: workflow-run
status: completed
version: 1.0
created: 2026-08-22
definition: substrate-floor-development
current_stage: seal
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

## Seal record (2026-08-22)

Ledgers set to truth (024ccc4): floor-structure-residue items 1–3, 5, 6
and the sh-fragment guard struck with dated commits, item 4 half-landed
with the remainder named, all done-when boxes ticked; the sprint design
plan completed; F14's did-not-reproduce evidence and re-open condition
recorded at the requirements ledger.

**Left honestly open:** the monolith's remaining banner sections (item 4's
second half); the smaller same-family items (duplicate staged-atomic-write,
prose-matching diagnostic, resemblance-classifying inspectors,
hand-restated pins); F8 → sprint 3 (`coherence-mechanism-build`); F2 with
its operator-sequenced owner `evidence-and-eval-backlog` — now 25 days
stalled and surfaced to the operator at this seal, per the scope decision.

**Human gates — all at this boundary, none pre-empted:** the framework
root declares `autopush: false`, so every sprint commit is local truth
awaiting the operator's deliberate push; the CHANGELOG entry and version
judgement belong to that release act; the Windows CI leg's first run (and
the keep/drop call if it proves slow) happens only after publication.

## Post-seal addendum (2026-08-22, after publication)

The run stays sealed; this records what the human gate found, because the
seal predicted exactly this and the outcome belongs with the prediction.

The operator pushed, and the F7 Windows leg's first real run **failed at
interpreter setup, before any test executed**: the shared pin `3.12.13`
has no win32-x64 build — `actions/python-versions` ships Windows builds of
3.12 only through 3.12.10 (3.12 is security-only; upstream stopped
publishing Windows installers). Repaired in `30ecef1` with a per-OS pin,
Linux keeping reference-machine parity. **Windows CI still has zero test
evidence**, and the repair is itself publication-gated.

Two things this confirms rather than contradicts: the verify record was
right to claim only the *authored* leg and never coverage, and
"publication-gated proof" is a real gap in the loop, not a formality — the
first three build-stage defects of a CI change are invisible to every
local instrument the floor has.

Also surfaced by the same run, unfixed here: GitHub is deprecating Node 20,
which both pinned actions (`checkout` v4.2.2, `setup-python` v5.6.0) run
on. Currently a warning. Bumping them changes pinned trust roots, so it is
a deliberate decision rather than a repair — routed to
`floor-structure-residue`.

**Second publication finding (same day).** With the interpreter fixed, the
Windows leg ran the suite and produced **56 failures with one cause**: the
runner puts the workspace on `D:` and `TEMP` on `C:`, so every test
scaffolding into `tmp_path` hit scaffold's deliberate refusal to embed an
absolute machine-specific adapter route. The floor was right; the suite's
unstated same-drive assumption was not. Fixed in `b4d022a` by pointing
`--basetemp` at `RUNNER_TEMP`, plus the regression test the branch had
never had — provoked portably, so it now runs on Linux too. Reproduced
locally first with a `subst` virtual drive; that reproduction's extra
publish/assemble errors passed in isolation and appear nowhere in CI's
list, so they were excluded as artifacts rather than folded in.

**A flake promoted to a recorded defect.** `test_imports_freshness_fresh_
then_stale` failed once during this sprint's build (dismissed then as
transient) and again in the post-fix suite. Two occurrences is a pattern:
traced to the face-read timeout being unreachable from the call path, and
recorded as **F15** at the requirements ledger with its mechanism and a
proposed shape. Deliberately not built — the run is sealed and the fix
widens a product config surface, which belongs to an analysis cut.

## Next

Nothing — the run is complete. Sprint 3 (derivation: F8's three phases)
starts as a new run of `substrate-floor-development` when execution
resumes, generating from the module layout this sprint settled.

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

## Verify record (2026-08-22)

**Full suite: 694 passed, 2 skipped, 4:03 under `-n auto`** (696 collected —
the invariant held through every lift; the one xdist flake seen once during
build did not recur). Budgets, steady-state per the v1.1 measurement
protocol:

| ID | Budget | Measured | Verdict |
|---|---|---|---|
| N1 session-start root | ≤ 5s | 1.8s | met |
| N2 estate-sync root | ≤ 8s | 5.1s | met |
| N3 precommit root | ≤ 12s | 3.3s | met |
| N4 precommit domain | ≤ 5s | 1.4s | met |
| N5 validate domain | ≤ 3s | 0.8s | met |
| N6 focused loop | ≤ 120s | 2–57s across the build's focused runs | met |
| N7 full suite | ≤ 12min | 4:03 | met |
| N8 lifecycle step ≤ ⅓ budget | 20s | ~1.8s | met |

Wrapper overhead (commit C's target): 348→273ms per invocation at the
root, 514→311ms in a venv-less domain repo, measured in Git Bash.

**Post-suite context (protocol-mandated, not a verdict):** N1 immediately
after the full suite measured **1.9s** — sprint 1's 5.5–5.8s transient did
not reproduce (the suite itself now finishes in 4:03 vs 9:20). **F14 left
unbuilt on that evidence**: its motivating symptom is absent on today's
measurement, and bounding an unmeasured cost would be speculative work.
F14 stays owned at the requirements ledger with this dated context.

**F7 matrix leg** (ef07edc): config landed, proof publication-gated — the
verify record claims the authored leg, never coverage.

**Estate observation:** the live domain used for the N4/N5 measurements
shows domain-kernel drift against a fresh build (its coherence errors
surfaced during measurement). That is the refresh channel carrying
framework changes to a domain at its own cadence — not a sprint defect and
not fixed from here.

## Reconcile record (2026-08-22)

Walked and committed (9b8e723, 8e37c36): the standing framework-map
warning closed — `precommit` gained its View 3 node and all three count
restatements moved 33 → 34 (the third hid in View 1's accDescr; the
checker found it after the first fix, which is the mechanical check doing
what prose walks miss). No other stale prose: greps for the moved
resolution owner and the lifted monolith sections returned nothing; the
suite README was reconciled inside the F7 commits; no spec kernel block
changed, so no kernel regeneration was owed — `mdllm coherence` reports
clean. The disclosure boundary blocked one commit mid-verify for naming a
private domain and the wording was corrected — noted as the boundary leg
working, not as a defect.

## Notes

Sprint 1's two recorded deviations carry forward as constraints: the F11
in-process composition variant stays open only if margin is ever needed (it
is not, at current measurements), and F4's move must land as part of the F5
adapter reshaping, not as a half-inversion.
