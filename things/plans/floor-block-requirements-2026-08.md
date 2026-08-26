---
id: floor-block-requirements-2026-08
type: plan
status: in-progress
version: 1.5
created: 2026-08-21
priority: high
tags: [requirements, floor, performance, tests, concurrency, sprint]
linked_things:
  - id: run-floor-sprint-1-2026-08
    relation: informs
    notes: "The run whose requirements stage this thing satisfies."
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: derived-from
    notes: "The finding-to-owner ledger supplies every review-sourced requirement; owners stay canonical there — this thing adds the bottleneck census and the budget table, never duplicate task lists."
  - id: floor-structure-residue
    relation: references
  - id: coherence-mechanism-build
    relation: references
  - id: evidence-and-eval-backlog
    relation: references
  - id: a-sharing-parameter-no-caller-passes-is-a-fix-that-did-not-happen
    relation: references
    notes: "F9's rationale: the structural tests exist because the four-scan fix was landed as an unwired parameter and believed complete for two days."
  - id: a-performance-requirement-inherits-its-measurement-context
    relation: implements
    notes: "The v1.1 measurement protocol is that insight's mechanism: budgets are steady-state facts, non-steady readings are recorded as context, and F14 carries its did-not-reproduce evidence rather than being silently dropped or built anyway."
---

# Floor Block Requirements — 2026-08

The requirement set for the operator's floor block (recorded execution order,
consolidated remedy → Operator Rulings 2026-08-21). Requirements are
problem-driven: every row cites its evidence. Owners named in the remedy's
ledger stay canonical; this thing exists so the block's requirements —
functional and non-functional — are one committed surface a sprint can be cut
from.

## Status at the floor-sprint-3 seal (2026-08-23)

**Met:** F1, F9–F13 (sprint 1) · F3–F7 (sprint 2) · F8a, F8b, F16, and the
first two thirds of F8c (sprint 3). Every non-functional budget N1–N8 was
measured green at each sprint's verify stage, and the block's constraints
held throughout: no transaction weakening, no daemons or persistent caches,
no new primitives for speed, typed non-definite results preserved.

**Open, and none of it buildable by another sprint of the same kind:**

- **F2** — machinery whose owner (`evidence-and-eval-backlog`) is
  operator-sequenced and now **27 days stalled**. Declined by two
  consecutive sprints rather than absorbed; the third surfacing is at this
  seal, and the decision is the operator's.
- **F8c remainder** — probes 3–5, owned by `coherence-mechanism-build`.
- **F14** — its re-open condition is now **two sprints unmet**: the
  post-suite N1 transient did not reproduce in either. Bounding an
  unmeasured cost stays speculative work.
- **F15** — the face-read timeout. Still needs its own analysis cut; it
  widens a product config surface. It did not fire once during sprint 3.

**The block's own exit is therefore a judgement, not a checklist**: what is
buildable is built, and the remainder is either an operator decision (F2,
and the Node 20 trust-root bump routed to seal) or a requirement whose
motivating measurement keeps failing to reproduce (F14).

## Status at the operating-model-seams seal (2026-08-26)

**Met:** F17–F20. `workflow-state.md` now carries activation/fulfilment,
committed definition revision binding and the executor-versus-gate-authority
contract; `operating-model.md` carries the consumer-owned contract and
addressing qualification. The floor resolves pinned definitions, reads
membership and edges from them, preserves legacy behaviour with an advisory,
and rejects one-candidate pin-plus-cursor self-authorization. The stretch
completed-run fulfilment cue also shipped. Evidence: the committed sprint run
`run-operating-model-seams-2026-08`, its 12 focused gitfs tests, adversarial
guard attempt, full-suite record, latency-budget table, reconciliation record
and distilled worked example.

**The broader ledger remains `in-progress`.** This seal closes only the four
requirements added in v1.4; F2, the F8c remainder, F14 and F15 retain the
dispositions recorded above. No unrelated open requirement was absorbed into
this sprint or made to appear complete by its closure.

## Reference environment

All budgets are measured on and bound to the operator's machine (Windows 11
Pro 10.0.26200, repo at the framework root with 14 nested estate repos, git
process spawn ~300ms cold / ~150ms warm, libyaml compiled in). Budgets are
per-machine facts, not portable claims; a second reference machine gets its
own column when CI supplies one.

## Measured baseline (2026-08-21, commits 2ede668 → fbe7b52)

| Path | Before | After (today) | Evidence |
|---|---|---|---|
| session-start, framework root, warm | 13.5s (67.8s on 2026-08-19) | ~2.1s | commit 2ede668 |
| estate-sync, root, 14 repos, online | ~21s | ~4.8s | commit 2ede668 |
| validate, root, worktree view | ~13s | ~4.5s | commit 2ede668 |
| validate, root, index view (hook path) | 302s | ~8.7s | commit fbe7b52 |
| coherence, root, index view (hook path) | 216s | ~9.6s | commit fbe7b52 |
| pre-commit hook total, root | ~8.7 min | ~20s | fbe7b52, observed |
| validate / session-start, live domain | — | ~0.7s / ~1.3s | measured 2026-08-21 |
| full test suite, serial | 37 min (690 tests) | unchanged | run 2026-08-21 |
| lifecycle hook wrapper probe overhead | ~0.65s per invocation | unchanged | measured 2026-08-21 |

## Functional requirements

Review-sourced (owner in brackets; the remedy ledger is canonical):

- **F1** — Perimeter truth corrections: strict calc severity wording,
  publication-teaching in the installed session-close commands, full-SHA
  decision pins in template + worked example. [floor-structure-residue]
- **F2** — Eval-isolation machinery: agent workspace constructed outside the
  canonical repo, no canonical write channel, byte-identity proof of the seed
  before/after an adversarial run. Machinery only; the rerun is
  operator-gated. [evidence-and-eval-backlog]
- **F3** — Fitness-gate inversion: vendor-vocabulary check total over neutral
  modules by construction, exceptions by declaration. [floor-structure-residue]
- **F4** — Hook-byte contract moved out of the birth module (dependency
  direction). [floor-structure-residue]
- **F5** — Adapter duplication collapse, carrying the probe existence-guard
  (~0.65s per lifecycle hook invocation) into the regenerated hook bodies.
  [floor-structure-residue]
- **F6** — Shared test fixture module extracted; test monolith split along
  its banners. [floor-structure-residue]
- **F7** — CI matrix widened to Windows + Linux, or the single-platform
  limitation recorded where portability claims are read. [floor-structure-residue]
- **F8** — Coherence by derivation. Decomposed at v1.3 (2026-08-23) because
  one line covered three phases of unequal size and one slice of it had
  already landed unnoticed. Owner stays `coherence-mechanism-build`; its
  phases are canonical, these are the requirements they must satisfy.

  - **F8a — the root's entry file stops restating derivable facts.**
    `AGENTS.md` at the framework root is the estate's only entry file with
    no managed blocks, and it produced findings in five of eight loop
    rounds. Requirement, in the loop insight's own order (*delete > derive
    > check*): a fact restated in the entry file is **deleted** in favour
    of a pointer where the pointer suffices, **generated** where a block
    can own the whole fact, and **checked** where the section is authored
    prose carrying a derivable annotation. Success test unchanged from the
    owner: the sections that drifted in rounds 1–5 become incapable of
    drifting silently. [coherence-mechanism-build Phase 1]

  - **F8b — the felt commit-boundary checks land.** The backlog is the
    authority on *which*; the requirement here is only that the items its
    own hold has lifted are built under its same-builder gate, and that
    F8a runs first so no checker is built for a restatement F8a deletes.
    [mechanical-coherence-checks-backlog, via Phase 2]

  - **F8c — the execution flows cold reads cannot verify get probes.**
    Executable scenario probes, each asserting observable output, each
    failing if the behaviour it pins regresses — in CI, with no human
    reading anything. [coherence-mechanism-build Phase 3]

  **Already landed, not re-scoped (measured 2026-08-23).** Part of F8a's
  stated territory arrived through other work and must not be rebuilt:
  `mdllm coherence` already checks `.markdownllm foundational_specs` ↔
  files on disk, the `TIERS` map ↔ the catalog *in both directions*,
  `kernel.md` drift, the framework-map subcommand count, and example
  `framework_version_seen` pins — and the domain-kernel managed-block
  drift check exists and is generic, applied today to domains only. What
  remains unbuilt at the root is the entry file itself.

- **F9** — Structural anti-regression tests for the consolidated derivation
  paths: session-start must fail a test if it regresses to repeated corpus
  scans or N+1 history walks (index-scan spawn bound landed 2026-08-21;
  session-start's own bound is owed). [remedy Phase 0 residue]

Bottleneck-census-sourced (new; evidence measured today):

- **F10** — Test execution workflow: parallel execution (pytest-xdist),
  tier markers (fast unit vs git-fixture integration), and a documented
  focused-selection convention so the inner loop runs affected files only;
  the full suite becomes a verify-stage gate, not an inner loop.
  *Felt again 2026-08-25 (operator, in session):* the 3.35.0 release gate
  ran the full suite — sanctioned, it is the stage gate — but at N7's
  measured 37 minutes for a session whose code delta was two data lines,
  and the operator challenged it believing attribution was already solved.
  It is solved as doctrine and as this requirement; only the mechanism is
  unbuilt. Recurrence at the operator's own hand is the deploy-when-felt
  signal: pull F10 into the next floor sprint's cut.
- **F11** — Pre-commit concurrency: boundary/validate/coherence legs run
  concurrently against the same frozen tree (safe by immutability); wall
  time approaches max(legs), not sum.
- **F12** — Remaining per-thing git calls batched (quarantine findings:
  11 spawns ≈ 2.9s at the root today).
- **F13** — Validate's three corpora (root + examples) evaluated
  concurrently.

Review-sourced (added v1.4, 2026-08-26; evidence:
`review-independent-operating-model-2026-08-26-codex`, verified — the
four seams the operating-model convergence review named in existing
primitives):

- **F17** — Run activation and outcome correlation: `workflow-state.md`
  (with `provenance.md` where the chain crosses) defines a run's
  *initiating evidence* and *produced evidence* on existing references —
  which demand instanced the run, which durable outputs belong to it,
  which terminal output fulfilled the demand — so the end-to-end causal
  chain holds even for routine work that never mints a decision record.
  No new artefact type unless live use proves references cannot carry it.
- **F18** — Definition revision binding: a live run names the committed
  revision of the definition that governs it (git commit as the citation
  unit, per the house pinning pattern), with an explicit policy for an
  active run whose definition changes — stay pinned (default), migrate
  by deliberate meaning-boundary commit, restart, or abandon. Floor legs:
  the pin resolves; stage membership and transition edges read through
  the pinned revision; legacy runs without the pin degrade to today's
  behaviour with an advisory. Repeatability is unprovable without this.
- **F19** — Executor vs gate authority (doctrine first): every
  specialisation declares *who or what performs* a stage separately from
  *who may authorise* its transition or accept its output. Prose in
  `workflow-state.md` (definition body contract) + the gate-authority
  dimension in `operating-model.md`. Machine-readable modality fields
  only after two live modules need automation to consume them.
- **F20** — Consumer-owned contract (doctrine first): `operating-model.md`
  names the consumption contract as a composition of existing pieces —
  address-book entry, import triggers, the definition an admitted input
  starts, the fulfilment output class, the cadence that makes
  non-consumption visible — consumer-owned always; producer blindness is
  inviolable (no subscriber lists, no push, no remote execution state).
  Alongside it, the addressing qualification: *addressed* = declared
  intended relevance on the exposed thing, never delivery authority.

Sprint-1-verify-sourced (added v1.1, evidence in the sealed run's verify
record):

- **F14** — Worktree-walk residual: session-start at the root still walks
  the ~37k-file worktree to list the corpus; after a full test suite evicts
  the filesystem cache, that walk alone pushes N1 from ~2.1s steady-state to
  5.5–5.8s. Requirement: bound the walk to the corpus (index-assisted
  listing, deeper pruning, or an equivalent) so the post-suite case
  approaches the steady state rather than tripling it. [run-floor-sprint-1
  verify record, N1 row] *Sprint-2 evidence (2026-08-22): the symptom did
  not reproduce — post-suite N1 measured 1.9s against 1.8s steady, with the
  full suite itself at 4:03. Left unbuilt on that measurement; re-open only
  if a post-suite exceedance is observed again.*

Constraints carried from the remedy (settled, restated as requirements):
no weakening of the transaction contract; no daemons, persistent caches, or
new framework primitives for speed; typed non-definite results everywhere the
floor could not look.

Flake-sourced (added v1.2, 2026-08-22 — diagnosed, deliberately not built):

- **F15** — The face-read timeout is unreachable from the call path, so
  `imports_freshness` tests are load-flaky. Mechanism, traced end to end:
  `imports_freshness` → `_mcp_face_read` → `_mcp_client_read`, and the last
  hop never passes a timeout, so every face read uses
  `DEFAULT_EXTERNAL_TIMEOUT_SECONDS = 10.0`. Each read spawns a real
  interpreter that imports the whole package; under `-n auto` contention
  that can exceed 10s, `_mcp_client_read` returns `None`, and the state
  becomes `unreachable`. **The product is behaving correctly** — degrading
  to "sync state unknown" rather than a silent `fresh` is the designed
  answer (imports_check.md docstring) — so this is a *test* that is
  coupled to a wall-clock budget on a loaded machine, not a floor defect.

  Evidence: `test_imports_freshness_fresh_then_stale` failed twice under
  `-n auto` (2026-08-21 during the F6 lifts, 2026-08-22 in the sprint-2
  post-fix suite) and passes on every isolated run. 17 test call sites
  share the exposure; only this one has been observed failing.

  Proposed shape (unbuilt, needs an analysis cut): let the `.mcp.json`
  entry carry a `timeout`, threaded through `_mcp_face_read` — the same
  ecosystem convention `headers` already rides, default unchanged at 10s,
  so a slow source (or a loaded test) can declare a longer budget. Entries
  are permissive (`_addressed` checks only for `command`/`url`; no key
  allowlist), so this is additive. **Not built in sprint 2**: the run was
  sealed, and widening a product config surface is a design decision, not a
  repair to bundle into a CI fix.

  Until it is fixed, a red CI leg on this test alone is a known flake, not
  a regression — re-run before investigating.

Vocabulary-registry-sourced (added v1.3, 2026-08-23 — measured while
opening sprint 3):

- **F16** — `held_by` / `held_until` are framework vocabulary a domain is
  made to register. Both fields are declared by two framework specs
  (`coordination-claim.md`, `workflow-state.md`) and shipped into every
  domain as part of the `workflow-run` reserved type's frontmatter
  contract, yet neither is in `CORE_FIELDS` — so any domain that adopts
  the framework's own advisory-claim convention is flagged
  "field not in CORE_FIELDS or declared known_fields" for it.

  This is `CORE_FIELDS`' **criterion 2** exactly ("the FRAMEWORK ships the
  field into a domain as part of a reserved type's contract — a domain must
  never be made to register the framework's own vocabulary"), and the same
  class the comment beside it already records twice: the ingestion triple
  (unregistered until v3.24.0) and the `type: prompt` contract (which
  "flagged a domain 24 times for the framework's own field names").
  Criterion 1 does not apply — `grep held_by tools/` returns nothing, so no
  tool code reads the fields; they are read by agents, like `inputs`/
  `outputs`/`bound_to`.

  Evidence: `run-floor-sprint-2-2026-08` carried `held_by: claude-code`
  through five stages under this warning, and `run-floor-sprint-3-2026-08`
  took the same warning at creation on 2026-08-23 — the framework's own
  corpus, using the framework's own reserved type, failing the framework's
  own field check. Same-builder, no suppression list, two lines of fix.

## Non-functional requirements — the budget table

Budgets any in-scope change must meet and the verify stage must measure.
"Root" = this framework checkout, the estate's worst case.

| ID | Path | Budget | Today | Headroom rationale |
|---|---|---|---|---|
| N1 | session-start, root, warm | ≤ 5s | ~2.1s | hook budget 60s; 3× cold-cache allowance inside 5s |
| N2 | estate-sync, root, online | ≤ 8s | ~4.8s | slowest single fetch ~2s; concurrency holds the sum |
| N3 | pre-commit hook, root | ≤ 12s | ~20s | met by F11 (max ≈ 9.6s) + F12 |
| N4 | pre-commit hook, live domain | ≤ 5s | ~2–4s | the surface a domain operator feels every commit |
| N5 | post-write validate, live domain | ≤ 3s | ~0.7s + wrapper | met further by F5 |
| N6 | focused test loop (one affected file) | ≤ 120s | 30–75s typical | inner-loop tolerability on this machine |
| N7 | full suite | ≤ 12 min | 37 min | F10 parallelism; 8 workers realistic |
| N8 | any lifecycle hook step | ≤ ⅓ of its harness budget at the root | varies | headroom is the requirement — 67.1s/60s must never recur |

### What binds a new check (added v1.3)

Every check F8b adds runs inside the pre-commit hook's coherence leg, so
**N3 is the budget a new check spends against** — not a separate allowance.
The leg is concurrent with validate and boundary (F11), which means a check
is free until the coherence leg becomes the max; past that it is charged at
full wall-clock. Today's root pre-commit is 3.3s against a 12s budget, so
there is real headroom — and a verify stage that does not re-measure N3
after adding checks has not verified them.

### Measurement protocol (added v1.1 — the definition sprint 1's verify owed)

Budgets describe **steady state**: warm filesystem cache, no full test suite
run in the preceding minutes, measured on the reference machine above. The
verify stage measures each budget in steady state and records that as the
verdict. Two named non-steady contexts are *recorded as context, never as
budget misses*:

- **Post-suite** — immediately after the full suite (hundreds of thousands
  of temp files churn the cache). Record alongside the steady figure; a
  post-suite exceedance is a finding for the residual's owner (F14), not a
  loop-back trigger.
- **Network-dominated paths** (N2) — remote round-trip variance dominates
  local compute. A single-evening exceedance is not a verdict; re-measure
  across days before any loop-back, and only a persistent local-compute
  regression loops back to build.

A budget is relaxed only by a requirements-stage revision of this thing,
never by the verify stage reinterpreting a number.

## Out of scope for the block

The retrospective (sequenced after, operator's order); sync-scope redesign
(D2 declined for now, dated ruling in the remedy); machine-level remedies
(Defender exclusion is a system security setting — operator-only); any
harness receipt or release work (Phases 5–6 carriers own them).
