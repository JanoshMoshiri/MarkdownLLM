---
id: floor-sprint-1-design-2026-08
type: plan
status: in-progress
version: 1.0
created: 2026-08-21
priority: high
tags: [design, sprint, floor, concurrency, tests]
informed_by:
  - id: floor-sprint-1-scope-2026-08-21
    commit: 10443b5aed763503161acc96833484c6786e6c7b
  - id: floor-block-requirements-2026-08
    commit: 8521d0d7b99e1a72eb68ca8fa513012ec59b1a6f
linked_things:
  - id: run-floor-sprint-1-2026-08
    relation: informs
    notes: "Design-stage artifact of this run."
---

# Floor Sprint 1 — Design

Design, not plan: each in-scope requirement gets its components, mechanism,
budget proof, focused test set, and commit boundary. Constraints binding
throughout: no transaction weakening, no daemons/persistent caches/new
primitives, typed non-definite results preserved, individual subcommands
unchanged for direct operator use.

## F9 — session-start structural anti-regression tests *(necessity)*

**Mechanism.** In `tools/tests/test_digest_signals.py`: a fixture repo of ~20
things; monkeypatch-count (a) `markdownllm.model.scan` invocations and (b)
git subprocess spawns during `cmd_session_start`. Assert exactly one corpus
scan and a spawn bound set well below the per-thing shape (bound chosen from
the fixture's measured constant + slack, as the landed index-scan bound was).
A second assertion pins `_things_history` to one `git log` walk.

**Budget proof.** None owed — this is the guard for already-met N1.
**Focused tests.** The new tests themselves + existing digest suite.
**Commit.** One: `test: session-start cannot regress to N+1 scans or walks`.

## F10 — test execution workflow *(necessity)*

**Mechanism.**
1. `pytest-xdist` added as a pinned dev dependency (venv + the repo's dev
   dependency surface; CI arrives sprint 2 with F7). Suite verified green
   under `-n auto` twice; any test with hidden ordering/shared-state
   dependence is fixed or explicitly grouped (`xdist_group`), each with a
   recorded reason — no silent serialisation.
2. Focused-selection convention codified in `tools/tests/README.md`: the
   module→test-file map (which test files own which floor modules), the
   inner-loop command shapes, and the rule that the full suite runs at the
   verify stage and release boundaries, not per change.
3. Tier markers (`unit` vs `gitfs`) registered in pytest config; applied
   incrementally — new tests must carry one; back-marking the 690 is not
   sprint work.

**Budget proof.** N7: full suite `-n auto` measured ≤ 12 min (37 min serial
today). N6: README documents per-file runs; spot-measure three
representative files ≤ 120s.
**Risk.** Parallel isolation failures → fix or group with reason; if >5% of
the suite needs grouping, stop and re-enter analysis (the suite has a
structural coupling problem F6 must own instead).
**Commits.** Two: dependency + green parallel run; convention doc + markers.

## F11 — pre-commit leg concurrency *(necessity — designed as the 3C coordinator)*

**Mechanism.** One new composing command, `mdllm precommit <root>`:
1. Constructs ONE frozen `RepositoryView.index` and **pre-warms it
   single-threaded** (tree map + definition-blob prefetch) so the fan-out
   reads immutable cache hits — thread-safety by warm-before-share, not
   locks.
2. Runs the three legs concurrently (ThreadPoolExecutor): boundary,
   validation reports, coherence — each the existing function, unchanged
   semantics, composed not reimplemented (remedy 3C's exact constraint).
3. Prints findings in the canonical order (boundary → validate → coherence)
   after all legs complete; exit severity is the max of the legs; per-leg
   failure messages byte-compatible with today's hook output sections.
4. The generated pre-commit hook body calls `mdllm precommit` instead of
   three interpreter launches (also removes two Python startups ~0.6s).
   Regenerated at the framework root via `mdllm install-hook .`; estate
   repos keep their current (correct, slower) hooks until their next
   refresh — recorded in the run body, not silently migrated.

**Budget proof.** N3: hook wall at root = max(validate ~8.7s, coherence
~9.6s) + one startup ≈ 10.5s ≤ 12s; F12 widens the margin. Measured before/
after in the run body.
**Risk.** Concurrent residual blob fetches spawn git from two threads —
safe (independent processes) but wasteful; the pre-warm makes them rare.
Index movement mid-run is already rejected by the hook's final tree compare;
the coordinator preserves that check.
**Focused tests.** New: coordinator produces identical findings + exit
severity to the three commands run serially on fixtures (clean, Error-in-
validate, Error-in-coherence, boundary-block). Existing hook-contract suite.
**Commits.** Two: coordinator + tests; hook body regen at root.

## F1 — perimeter truth corrections *(necessity)*

Three surfaces, located: `docs/calculation-reference.md:87` ("always a
Warning" — strict mode has made unevaluable an Error); the installed
`.claude/commands/end-session.md` (teaches publication default-on; the
templates were already corrected — align to fail-closed autopush doctrine);
`templates/decision.md.template` + its worked example (abbreviated pins →
full-SHA rule). **Commit.** One: `fix: prose no longer teaches weaker
behaviour than the floor executes`, citing each surface.

## F12 — quarantine git batching *(should)*

**Mechanism.** `quarantine_findings` currently spawns per verified-external
thing (show HEAD:rel, creation-commit log, historical shows). Replace with:
one `git log --format=%H%x1f%cs --name-only -- things` walk building
path→(creation commit, flip commits) facts, and HEAD-content reads through a
shared `RepositoryView.commit(HEAD)` using the existing batch prefetch.
Same findings, constant spawns.
**Budget proof.** Root validate drops ~2s; N3 margin. Existing quarantine
tests are the oracle (they pin the findings, not the call shape).
**Commit.** One.

## F13 — corpora-concurrent validate *(should)*

**Mechanism.** `validation_reports` warms the shared view, then evaluates
root + example corpora in a ThreadPoolExecutor, aggregating reports in
deterministic (current) order. Same findings; wall ≈ max(corpus) not sum.
**Risk.** All three corpora share the view's caches — warm first, as F11.
**Commit.** One.

## F4 — hook-byte contract dependency move *(should)*

**Mechanism.** The hook byte/dir facts move from the scaffold (birth) module
into `hook_contract.py` (the existing leaf); diagnostics import the leaf.
Pure dependency-direction fix; `test_architecture_fitness` is the oracle.
**Commit.** One.

## Stretch (F2 machinery, F6 extraction)

Designed only if reached: F2 = workspace assembly outside the repo tree +
seed byte-identity assertion, into `evals.py`; F6 = move `_git_repo`/
`write`/`thing_text` helpers to `tools/tests/fixtures.py` imported by the
monolith (no test-body changes). Neither starts before necessity + should
are verified.

## Verify stage plan

Per-change focused suites as named above; then one full `-n auto` suite; then
the budget table re-measured (N3, N6, N7 the ones currently missed) and
recorded in the run body with commands and numbers. Any missed budget loops
to build; any budget change is a recorded decision, never drift.

## Order of build

F9 → F10 → F11 → F1 → F12 → F13 → F4 → (stretch). F9 first so every later
change builds under the guard; F10 second so the rest of the sprint inherits
the fast loop.
