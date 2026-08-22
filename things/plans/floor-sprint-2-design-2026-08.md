---
id: floor-sprint-2-design-2026-08
type: plan
status: completed
version: 1.0
created: 2026-08-22
priority: high
tags: [design, floor, structure, sprint, adapters, fitness-gate, tests]
linked_things:
  - id: run-floor-sprint-2-2026-08
    relation: informs
    notes: "The run whose design stage this thing satisfies."
  - id: floor-sprint-2-scope-2026-08-22
    relation: derived-from
    notes: "The analysis cut this design realises: necessity F3/F5/F4, should F6/F7-record, stretch F7-matrix/F14."
  - id: floor-structure-residue
    relation: implements
    notes: "Items 1-4 and 6 are the subject; item 5 landed in sprint 1."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "The governance surface read before this design: dependency direction, naming-as-architecture, seams named before implementation, conscious shortcuts recorded."
---

# Floor Sprint 2 Design — Structure

Design read against the code-architect governance surface (Clean Architecture
dependency rule, naming reveals intent, the seam named before the
implementation, conscious shortcuts recorded). Facts below were measured on
this checkout at design time, not assumed.

## F3 — Fitness-gate inversion

**Component:** `tools/tests/test_architecture_fitness.py`.

**Design.** The hand-curated `NEUTRAL_MODULES` allowlist (14 entries against a
~40-module package) inverts: every `*.py` under `markdownllm/` **except
`adapters/**`** is neutral by construction; the vendor-vocabulary and
registry-import checks run over that derived set. Exceptions are declared in
the test as `{module: reason}` and must be *exact*: a declared exception whose
module no longer trips the gate fails the suite (a stale exception is the
same-builder blindness the residue names).

Probe results (design-time, this checkout): the inverted gate flags exactly
three modules —

- `model.py` — scan-config data, the already-documented exception; keeps it.
- `evals.py` — drives the vendor CLI *as its subject* (`claude -p` eval
  agent); the vocabulary is the module's purpose, not leaked adapter policy;
  declared exception with that reason.
- `sync.py` — one vendor word in a user-facing message string ("restricted
  Codex task"). Not excepted: **reworded neutrally** in the same commit
  ("network-restricted harness task"), because exceptions are for modules
  whose purpose is vendor-facing, not for incidental prose.

**Focused tests:** the fitness suite itself; grep the test corpus for the
reworded sync.py message before changing it. **Budget:** none touched
(test-only + one string). **Commit:** one.

## F4 + F5 — The leaf contract move and the adapter collapse

Three commits, sequenced so byte-identity is provable before bytes change:

### Commit A — F4: hook contract moves to the leaf (byte-identical)

**Components:** `hook_contract.py` (grows), `scaffold.py` (shrinks),
`runtime.py`, `doctor.py`, `session.py`, both adapters' imports,
`test_architecture_fitness.py`.

Current wrong-direction edges (measured): `doctor.py` imports
`rendered_hook_contract, resolve_hooks_dir` from scaffold; `session.py`
imports the hook bodies from scaffold; both adapters and scaffold import
`SH_RESOLVE` from runtime. The leaf (`hook_contract.py`, 30 lines, imports
nothing) is the declared right home.

**Moves into the leaf:** the interpreter-candidate tables and
`_render_sh_resolve`/`SH_RESOLVE` (from runtime.py); the three hook-body
templates, their `{resolve}` substitution, `_HOOK_BODIES`,
`rendered_hook_contract`, and `resolve_hooks_dir` (from scaffold.py).
scaffold.py keeps install/uninstall mechanics — the producer act, not the
contract. Consumers (runtime, scaffold, doctor, session, adapters) flip
imports to the leaf. If build finds runtime's Python-side resolution shares
the candidate tables, they move with the fragment (one owner); if sh-only,
the move is clean either way.

**Fitness extension in the same commit:**
`test_hook_execution_layers_do_not_depend_on_scaffold` gains `doctor` and
`session` — the two edges this commit deletes must be mechanically
unrecreatable.

**Proof of byte-identity:** rendered hook bodies and both adapters' golden
fixtures are unchanged; any golden diff in this commit is a defect.

### Commit B — F5: adapter duplication collapse (byte-identical)

**Component:** new `adapters/project_hook_emission.py` (name states what it
owns; no Helper/Utils per the naming rule), consumed by `claude_code.py`
(647 lines) and `codex.py` (724 lines).

**Owns the converged shape:** shell single-quoting and PowerShell quoting,
the POSIX lifecycle-command template (root resolution → MDLLM path →
`SH_RESOLVE` embed → unavailable-envelope fallback → `harness-event`
invocation), the definition-hash-with-placeholder pattern over
`managed_definition_hash`, handler-dict construction, and probe
construction. **Stays per-adapter:** event names, matchers, config paths,
legacy definitions, Codex's Windows variants, envelope specifics.

Composition over inheritance: shared *functions* taking explicit parameters,
no adapter base class — the convergence is contractual, and a hierarchy
would couple the adapters' independent evolution. Vendor vocabulary stays
inside `adapters/`, so the F3 gate is untouched.

**Proof:** golden fixtures byte-identical; both adapter suites green.

### Commit C — probe existence-guards (the one deliberate byte change)

**Component:** `_render_sh_resolve` (now in the leaf).

File-path candidates gain `[ -x "<path>" ] &&` before `mdllm_probe`;
PATH-name candidates gain `command -v <name> >/dev/null 2>&1 &&`. Both are
shell builtins — the ~330ms dead `timeout`+python spawn per absent candidate
(measured, POSIX venv path on Windows) disappears; total wrapper overhead
~0.65s/invocation is the target of record.

**Blast radius, handled deliberately:** this changes the three git hook
bodies, both adapters' emitted commands, and every definition hash. In this
commit: goldens regenerated, `mdllm install-hook` re-run at the framework
root so the local floor carries the new bytes. **Estate domains are not
walked** — each domain's doctor surfaces definition drift and its refresh
cycle reconciles it; that is the designed channel, recorded here so the
verify stage doesn't mistake per-domain drift reports for a defect.

**Focused tests (A/B/C):** `test_runtime.py`, `test_adapter_install.py`,
`test_lifecycle_runner.py`, `test_adapter_contract.py`,
`test_codex_adapter.py`, `test_cowork_adapter.py`,
`test_harness_diagnostics.py`, `test_architecture_fitness.py`, golden
fixtures. **Budget proof:** N5's wrapper component — time a lifecycle hook
invocation before commit A and after commit C on this machine; expect
≥0.3s saved; N4 re-measured at verify.

## F6 — Test fixture extraction and monolith split

**Components:** `tools/tests/test_mdllm.py` (3601 lines), new
`tools/tests/corpus_harness.py`, `test_calc.py`,
`test_cohesiveness_sensors.py`.

**Commit D:** extract the shared helpers (`_ns`, `thing_text`, `write`,
`all_findings`, `messages`, and the rest of the monolith's helper banner)
into `corpus_harness.py` — named for what it owns: corpus construction and
CLI invocation for floor tests. The two measured importers flip; any third
import form found at build flips too.

**Commits E…:** one commit per banner-coherent section lifted out of the
monolith — candidates measured from the banner map: session gate (~line
3177), the membrane/sync sections (the unnamed banners ~2276–3100, named at
build from their content), scaffold+doctor, mcp-serve, imports-check,
quarantine flip, terminal statuses. The design rule rather than a fixed
list: each lifted file is one coherent section importing `corpus_harness`,
and **the collection count is invariant** — `pytest --collect-only -q`
totals identical before and after every lift; a lost test is a build error.

**Budget:** N6 improves (finer focused selection); N7 unchanged (same
tests). **Focused tests:** the lifted file + the remaining monolith after
each lift.

## F7 — CI

**Commit F (record leg):** the single-platform limitation recorded where
portability claims are read — the `validate.yml` header comment and
`tools/tests/README.md`. Honest sentence: the floor's most
platform-sensitive machinery (Windows command carriers, shell resolver,
line-ending contract) is CI-exercised on Linux only; Windows evidence is
operator-machine measurement.

**Commit G (stretch, matrix leg):** `strategy.matrix.os:
[ubuntu-24.04, windows-2025]` with the suite under `-n auto`. Its *proof* is
publication-gated — CI runs only after the operator's push — so the verify
record states "config landed, run unproven" rather than claiming coverage.
Windows runner wall time is unknown (2-core hosted runners); if the first
real run is intolerable, dropping the leg is the operator's call at the
release act.

## F14 — Worktree-walk residual (stretch)

**Components:** the worktree-view corpus listing (`repository_view.py` /
`model.py` scan path). Rule if reached: derive the candidate list from git's
index plus status-reported untracked paths instead of an rglob over ~37k
files, preserving view semantics exactly (tracked + untracked things minus
excludes). Proof: post-suite session-start re-measured against N1's
steady-state figure; focused tests `test_repository_view.py`,
`test_coherence_repository_view.py`.

## Build order and loop discipline

F3 → A → B → C → D → E… → F → (G, F14 if reached). F3 lands first so the
reshaping happens under the inverted gate. Verify runs focused suites per
commit, the full suite once at the stage boundary, budgets per the v1.1
measurement protocol (steady-state; post-suite recorded as context).

## Risks

1. **Definition-hash desync across the estate** — sequenced so bytes change
   exactly once (commit C); root reinstalled in the same commit; domain
   drift is the refresh channel's job, recorded above.
2. **Silent golden drift** — goldens are the byte-identity proof for A and
   B; any diff there loops back to build, never gets regenerated-through.
3. **Lost tests in the split** — collection-count invariant per lift.
4. **Stale fitness exceptions** — exactness check fails the suite when an
   exception stops being needed.
5. **sync.py message is asserted somewhere** — grep the test corpus before
   rewording; update assertions in the same commit.
6. **`runtime`'s Python-side resolution entangled with the sh tables** —
   if the tables serve both, they move to the leaf as one owner; if that
   drags runtime internals leafward, stop, record, and re-scope F4 per the
   decision's re-open condition rather than half-moving.
