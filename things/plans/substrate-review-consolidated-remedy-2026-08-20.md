---
id: substrate-review-consolidated-remedy-2026-08-20
type: plan
status: not-started
version: 1.0
created: 2026-08-20
tags: [substrate, remedy, deterministic-floor, performance, coherence]
priority: high
exposed: false
linked_things:
  - id: independent-substrate-review-2026-08-20-claude
    relation: derived-from
  - id: independent-substrate-current-state-review-2026-08-20-codex
    relation: derived-from
  - id: codex-substrate-review-response-2026-08-20
    relation: references
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: substrate-totality-residue
    relation: subtask
  - id: floor-structure-residue
    relation: subtask
  - id: framework-retrospective-2026-08b
    relation: subtask
  - id: evidence-and-eval-backlog
    relation: subtask
  - id: coherence-mechanism-build
    relation: subtask
  - id: v3-33-release-and-external-acceptance
    relation: subtask
  - id: session-start-hardening
    relation: references
  - id: vendor-harness-adapter-foundation
    relation: references
  - id: cowork-adapter
    relation: references
  - id: mechanical-coherence-checks-backlog
    relation: references
  - id: external-review-response-2026-08-10
    relation: references
---

# Consolidated Substrate Remedy — 20 August 2026

## Commission

Turn the independent Claude and Codex reviews of the current substrate into one
ordered remedy. This is the execution and acceptance ledger, not a third review
and not a replacement for the plans that already own individual findings.

The review of the private domain estate was deliberately a private diagnostic.
No domain names, domain findings, or domain-level conformance judgements are
inputs to this public-framework plan. Domain refresh is a downstream consequence
of an accepted substrate release, not a workstream recorded here.

## Consolidated Verdict

The substrate does not need a new architecture. The three-layer model, the
deterministic/semantic split, the immutable repository view, the transaction
boundary, and human authority over irreversible consequence are the right
design. The recent transaction remediation is real and must not be reopened.

The remaining problem has three connected parts:

1. **Truth is not yet total at a few failure edges.** Several commands still
   turn “could not inspect” into a confident negative or fresh result. These are
   small defects with high epistemic importance.
2. **Correct mechanisms are composed too expensively.** Session start, trigger
   evaluation, pre-commit, worktree discovery, and estate sync repeat corpus,
   history, process, and network work. The lifecycle budget was widened around
   this cost; the work itself was not reduced.
3. **Experience is accumulating faster than it is being compressed.** The
   overdue retrospective, insight population, stale plans, unfinished eval, and
   unclosed external receipts mean the substrate has more learning than settled
   judgement.

Claude found the remaining false-certainty, isolation, structural, and perimeter
residue. Codex found the common execution edge underneath it: many individually
reasonable mechanisms lack a single owner for their combined cost. These are
not competing diagnoses. They meet at one design rule:

> **One immutable view, one derivation pass, many honest consumers.**

The remedy is therefore: restore totality, compress the learning, consolidate
execution, remove structural residue, then prove the result end to end before a
release decision.

## What Is Settled

These are constraints on every phase, not questions to reopen:

- Keep the three-layer architecture and the deterministic/semantic boundary.
- Keep repository and index compare-and-swap protection across all mutating
  commands. Performance work may not weaken the transaction contract.
- A deterministic result may only be definite when the floor obtained the
  evidence needed to compute it. Unreachable, unreadable, incomplete, and
  execution-failed states remain typed and visible.
- Keep semantic judgement, inflection declaration, publication, credentials,
  trust installation, and irreversible action human-owned.
- Add no new framework primitive, durable service, database, daemon, or cache
  merely to make the current choreography faster.
- Prefer derivation and deletion over another maintained restatement. A new
  check belongs in the floor only when its truth is owned by the same builder.
- Existing plans remain the owners of their findings. This plan supplies order,
  gates, integration, and final acceptance; it must not grow duplicate task
  lists that can drift from those owners.
- The completed pre-remediation response plan remains completed. Its accepted
  transaction architecture is an input to this work, not unfinished work to
  reopen.

## Finding-to-Owner Ledger

| Concern | Canonical owner | Evidence that closes it |
|---|---|---|
| Import-trigger, pin-current, and provenance false-certainty defects; same-class siblings | `substrate-totality-residue` | Focused regression fixtures plus an end-to-end unreachable/read-failed route showing a typed non-definite result |
| Eval agent can still reach or write the canonical source/seed | `evidence-and-eval-backlog` | A disposable external workspace, denied canonical write path, unchanged source-tree hash/sentinel, and a valid rerun |
| Vendor-fitness allowlist, adapter duplication, diagnostics/scaffold dependency, worktree walk, atomic-write duplication, test monolith, platform coverage | `floor-structure-residue` | Structural tests, bounded traversal evidence, and the agreed cross-platform suite |
| Calculation severity wording, publication-teaching examples, abbreviated decision pins | `floor-structure-residue` | Prose and examples agree with executable behaviour and full-SHA policy |
| Insight triage, consolidation, stale standing claims, and periodic quality reflection | `framework-retrospective-2026-08b` | Completed retrospective and an explicit disposition for every active insight |
| Generated contract surfaces, admitted coherence checks, and flow probes | `coherence-mechanism-build` with accepted candidates from `mechanical-coherence-checks-backlog` | Rebuild-and-diff checks and end-to-end probes pass from a clean clone |
| Current Claude, Codex, and Cowork receipt evidence and the release decision | `v3-33-release-and-external-acceptance` plus the three adapter/hardening carriers | Dated, commit-pinned evidence on the current contract or a narrower public claim |
| Combined lifecycle cost and repeated derivation | **This plan, Phase 3** | Structural work-count tests and reference-checkout latency evidence show consolidation without semantic or transaction regression |

If execution discovers a new defect, first classify it into an existing owner.
Create a new carrier only when no current thing owns the concern and the concern
is cohesive enough to stand alone.

## Execution Order

### Phase 0 — Freeze and Establish the Performance Contract

Purpose: make improvement falsifiable before changing the implementation.

- [ ] Move this plan to `in-progress` and pin the implementation baseline to a
      full commit SHA.
- [ ] Record the reference environment and separate local computation from
      remote/network wait.
- [ ] Measure at least three cold and three warm runs of the representative
      paths: target sync, estate sync, session start, triggers, validation,
      coherence, no-op pre-commit, changed pre-commit, refresh, and session
      close.
- [ ] Record structural work as well as time: corpus parses/walks, Git history
      subprocesses, Python application launches, worktree entries visited, and
      network repositories contacted.
- [ ] Preserve representative command output and exit-state fixtures so later
      optimisation can prove behavioural equivalence, including dirty,
      divergent, offline, unreadable, and stale-index states.
- [ ] Lock the wall-clock acceptance budget before implementation. The
      recommended starting gate is a material reduction on the reference
      checkout, with a goal of at least 50% for local session start and no-op
      pre-commit; if a different threshold is accepted, record the reason now,
      never after seeing the result.

The current reviews supply orientation, not a universal benchmark: validation
and coherence index paths were sub-second, trigger evaluation was about 7.6s,
session start about 33s, and an earlier lifecycle run observed roughly 60s for
estate sync and 36s for session start. Repeat these under one documented harness
before treating them as a baseline.

**Exit:** a committed measurement record, fixed behavioural fixtures, and an
accepted performance budget exist. No optimisation is credited without both the
structural and temporal comparison.

### Phase 1 — Restore Epistemic Totality and Test Containment

Purpose: correctness precedes speed and new evidence precedes new claims.

- [ ] Execute `substrate-totality-residue` in small, meaning-boundary commits:
      fix the three high findings first, then resolve or explicitly rule out the
      same-class siblings.
- [ ] Give unreachable/no-address-book/incomplete import evaluation and failed
      pin-body reads explicit typed outcomes; never render them as not-fired or
      fresh.
- [ ] Match provenance inputs by parsed thing identity and pinned commit, never
      by path suffix.
- [ ] Preserve retrospective-computation failures, distinguish “no remote” from
      “sync command could not run,” and centralise the quarantine predicate.
- [ ] Close the eval-isolation hole before any longitudinal rerun. Construct the
      agent workspace outside the canonical repository, remove any explicit
      canonical write channel, and prove the canonical seed and source tree are
      byte-identical before and after an adversarial run.
- [ ] Land the three low-risk perimeter truth corrections through
      `floor-structure-residue`: strict calculation severity, publication
      examples, and full-SHA decision pins.

**Exit:** every “could not look” path stays non-definite; the regression family
passes; the canonical evaluation source is demonstrably unwritable from the
trial; prose no longer teaches weaker or more permissive behaviour than the
floor.

### Phase 2 — Compress the Learning Before Building More

Purpose: use the substrate's own learning mechanism before deciding which
mechanisms survive or combine.

- [ ] Complete `framework-retrospective-2026-08b` immediately after the
      correctness pass rather than waiting for its date trigger.
- [ ] Disposition every active insight: promote, dismiss, consolidate, or keep
      active with a concrete reason and a live inbound route.
- [ ] Resolve the named consolidation clusters, stale standing claims,
      dismissal-condition census, and decisions-staked-on-absent-mechanisms
      census.
- [ ] Walk the whole corpus, including insights, for semantic drift caused by
      the recent transaction and deterministic-flow inflections.
- [ ] Produce a mechanism disposition ledger: keep, consolidate, derive,
      retire, or defer. A mechanism survives because current evidence needs it,
      not because a previous incident once created it.
- [ ] Reconcile or close stale plan rows so that open-loop state describes the
      real programme rather than its history.
- [ ] Decide the deferred cold-read cadence from
      `external-review-response-2026-08-10`. Recommended: one blind independent
      read after each substantial release, not a continuous review loop.

No new non-correctness mechanism should be admitted between Phase 0 and the
retrospective close. This prevents the response to accumulated mechanism cost
from being one more mechanism added before the corpus has judged what it already
has.

**Exit:** the retrospective is complete, every active insight has a disposition,
the mechanism ledger and plan population agree, and Phase 3's design decisions
are recorded rather than inferred from this plan.

### Phase 3 — Consolidate the Lifecycle Around One Immutable Derivation

Purpose: make the correct path economical without changing what the framework
means.

#### 3A. One session snapshot

- [ ] Introduce an internal application-level session snapshot derived from one
      `RepositoryView`, one parsed corpus, and a bounded set of bulk Git facts.
      It is an implementation value, not a framework primitive or persisted
      source of truth.
- [ ] Derive stalls, open loops, retrospective state, trigger results, and the
      session digest from that snapshot rather than rewalking the corpus for
      each consumer.
- [ ] Replace per-candidate history calls with one bulk history read and an
      in-memory last-touch/flip map.
- [ ] Keep presenters and semantic judgements downstream of the snapshot; do not
      move judgement into the floor to save a call.
- [ ] Add structural tests that fail when session start regresses to repeated
      corpus parses, repeated trigger passes, or N+1 history queries.

The target is one corpus derivation, one trigger derivation, and one bulk history
derivation per pinned session-start view. Small Git calls needed to establish
HEAD, status, or the immutable boundary are not to be hidden in that count; they
are named separately in the measurement record.

#### 3B. Sync follows the read set

- [ ] Record an explicit human decision on the startup sync scope before
      changing the hard hook. **Recommendation:** automatic startup syncs the
      target repository only; import or estate sync is invoked when intent first
      expands the read set to those repositories. Keep `estate-sync` as the
      explicit complete-estate affordance.
- [ ] If accepted, treat the change as a framework inflection and reconcile
      `orchestration.md`, `git-workflow.md`, AGENTS/templates, adapters, operator
      guides, bootstraps, tests, and stale insight claims in one declared pass.
- [ ] Preserve fail-closed publication, dirty/divergent reporting, bounded
      offline behaviour, and the rule that a significant read happens only
      after its actual read set has been synchronised.
- [ ] Prove that a local single-domain session performs no network work against
      unrelated repositories and that an estate read cannot silently omit its
      explicit estate sync.

If the recommendation is declined, the decision must instead name the evidence
that makes estate-wide startup cost part of every local session's necessary
contract. Merely retaining the current behaviour by inertia is not an outcome.

#### 3C. One pre-commit application process

- [ ] Consolidate boundary validation, thing validation, coherence, and
      inflection-candidate presentation behind one pre-commit coordinator that
      freezes and shares one index-backed view.
- [ ] Preserve the existing individual subcommands for direct operator use; the
      coordinator composes them internally and adds no new semantic rule.
- [ ] Preserve compare-and-swap checks before mutation/commit and exact
      candidate-byte semantics.
- [ ] Prove that a hook run starts one application process, parses one candidate
      view, and produces equivalent findings and exit severity to the preserved
      fixtures.

#### 3D. Remove avoidable traversal

- [ ] Prune excluded directories during traversal rather than after a complete
      walk, beginning with interactive worktree listing.
- [ ] Measure before introducing any persistent cache. A cache is admissible only
      if the one-pass design still misses the accepted budget and the cache can
      be pinned to immutable commit/index identity, rebuilt, and diff-validated.

**Exit:** the structural budgets hold, the locked latency budget is met or a
human records a pre-release rejection, and every transaction, degraded-state,
and output-equivalence fixture still passes.

### Phase 4 — Remove Structural Residue and Strengthen Coherence

Purpose: leave the implementation easier to reason about than the one reviewed.

- [ ] Execute the structural rows in `floor-structure-residue`: invert the
      neutral-module vendor-vocabulary test, collapse project-bound adapter
      duplication, move the hook-byte contract to the correct dependency
      direction, share atomic-write logic, split shared test fixtures from the
      monolith, and make platform coverage explicit.
- [ ] Make the architecture-fitness gate total over neutral modules with only
      declaration/adapter boundaries exempt. Do not maintain a curated list of
      supposedly neutral modules.
- [ ] Run CI on Windows and Linux for the deterministic floor, or record a
      deliberate support limitation in the contract and public claims.
- [ ] Execute the admitted `coherence-mechanism-build` phases: derive eligible
      root AGENTS surfaces, add only same-builder mechanical checks that pass the
      suppression-list razor, and land the clean-clone flow probes.
- [ ] Keep performance budgets as tests/measurements at their proper application
      boundary; do not disguise machine-dependent timings as corpus coherence.
- [ ] Commit each dependency inversion, derivation, check family, and probe
      family at its own meaning boundary. Do not repeat the previous mega-commit
      execution variance.

**Exit:** the vendor boundary is complete by construction, duplicated ownership
is removed, traversal is bounded, platform claims match CI evidence, and every
new mechanical check has one builder-owned source of truth.

### Phase 5 — Prove Utility, Efficiency, and Harness Receipt

Purpose: test the whole system after it becomes stable, not the intermediate
implementation.

- [ ] Finish the isolated longitudinal floor rerun in
      `evidence-and-eval-backlog`; retain invalid historical runs as labelled
      evidence rather than silently replacing them.
- [ ] Replace the saturated efficiency fixture with a discriminating task suite.
      Measure outcome quality, rule adherence, honest uncertainty, token/context
      load, tool calls, wall-clock time, deterministic failures, and human
      interventions. Separate network wait from local floor cost.
- [ ] Preserve the structured/unstructured and model-capability comparison so
      the manifesto's efficiency hypothesis can be supported, narrowed, or
      rejected rather than asserted from one saturated result.
- [ ] Run the clean-clone flow probes: first boot, scaffold birth, invariant
      breach, refresh, session close, unreachable import, stale bundle, and
      current receipt.
- [ ] Obtain fresh current-contract evidence for Claude and Codex, and the scoped
      local/remote/stale-bundle Cowork evidence, through
      `v3-33-release-and-external-acceptance` and the existing adapter carriers.
- [ ] Update the compatibility matrix only from dated, exact-version evidence.
      Where receipt is unproved, narrow the claim instead of extrapolating.
- [ ] Commission one final blind substrate cold read by a reviewer that did not
      implement the remedy. Classify every finding as closed, accepted tradeoff,
      deferred with owner, or release-blocking.

**Exit:** the longitudinal run is valid, the efficiency test can discriminate,
the flow probes pass, harness claims are current and bounded, and the final cold
read has no unowned release-blocking residue.

### Phase 6 — Reconcile, Release, and Offer Refresh

Purpose: make publication a deliberate version event after the evidence settles.

- [ ] Reconcile any changed operative rule through cue → assimilate → walk →
      seal, including the full-corpus conceptual residue and insight corpus.
- [ ] Update specifications, generated kernel, templates, guides, capability
      matrix, changelog, and version from the accepted evidence; run coherence
      after any catalog/spec surface change.
- [ ] Decide adapter default-selection behaviour and existing-domain opt-in
      rollout through `vendor-harness-adapter-foundation`; do not batch-install
      trust or permission configuration.
- [ ] Decide whether the manifesto's efficiency claim is supported, should stay
      a hypothesis, or must be narrowed. Utility evidence and efficiency
      evidence remain distinct.
- [ ] Run the complete validation, coherence, focused regression, cross-platform,
      clean-clone, and hook-install/self-test suites at the release candidate
      commit.
- [ ] Complete or explicitly disposition every linked subtask plan and update
      this plan's ledger against their terminal states.
- [ ] Ask the human operator for the publication decision. Versioning and the
      release commit do not imply push authority; `autopush: false` remains
      decisive.
- [ ] After publication, offer downstream domains a commit-pinned refresh. Do
      not auto-migrate them and do not record their private conformance results
      in the public substrate.

**Exit:** the release is either published by explicit authority or deliberately
deferred with a reason; the public claims equal the evidence; downstream refresh
has a bounded offer; no publication debt is hidden.

## Human Decision Gates

The programme may prepare evidence for these decisions but must not silently
take them:

| Gate | Latest point | Recommendation |
|---|---|---|
| D1 — performance budget | End of Phase 0 | Lock structural counts and a material reference-checkout latency reduction before code changes |
| D2 — automatic sync scope | Before Phase 3B | Sync the target repository automatically; sync imports/estate when intent expands the read set |
| D3 — cold-read cadence | End of Phase 2 | One independent blind read per substantial release |
| D4 — adapter default/rollout | Before Phase 6 | Explicit selection with opt-in refresh; no silent trust installation |
| D5 — manifesto efficiency wording | After Phase 5 eval | Keep it a hypothesis unless the discriminating fixture earns a stronger statement |
| D6 — publish | End of Phase 6 | Human-only, after reconciliation and evidence review |

## Phase Gates and Parallelism

- Phase 0 precedes all performance changes.
- The totality fix and eval-containment fix in Phase 1 may proceed independently,
  but no eval rerun starts until containment is proved.
- Phase 2 precedes structural design choices so that stale mechanisms are not
  optimised before they are judged.
- Phase 3's session, sync, hook, and traversal branches may be implemented in
  separate small commits against the same fixtures. Any operative sync change
  requires its own full change-reconciliation pass.
- Phase 4 may overlap with Phase 3 only where ownership is disjoint and the
  shared baseline remains immutable.
- External receipt probes and the final cold read happen after operative
  behaviour freezes. Earlier probes are development evidence, not release
  acceptance.
- Release work starts only after Phases 1–5 have closed or the human has accepted
  an explicitly documented exception.

## Definition of Done

This plan is complete only when all of the following are true:

- [ ] No deterministic path returns a definite answer from unavailable or
      uninspected evidence.
- [ ] Repository and index transaction invariants still hold for every mutating
      command and their adversarial fixtures.
- [ ] The eval agent cannot modify or depend on mutable canonical test sources.
- [ ] Session start and pre-commit meet their structural work budgets and the
      pre-declared reference latency budget.
- [ ] Automatic sync scope matches the recorded human decision and the actual
      read set; unrelated repositories are not contacted accidentally.
- [ ] The overdue retrospective is complete and every active insight has an
      explicit disposition.
- [ ] Structural residue and perimeter truth mismatches are closed or rejected
      with recorded rationale.
- [ ] Coherence checks are builder-owned, flow probes pass from a clean clone,
      and platform claims match tested platforms.
- [ ] The longitudinal and efficiency evals are valid and discriminating; public
      claims are no stronger than their results.
- [ ] Fresh harness receipts and the final independent cold read have no unowned
      release blocker.
- [ ] Every `subtask` link above is terminal and honestly dispositioned.
- [ ] Release is published with explicit authority or deliberately deferred;
      post-commit publication debt is reported.
- [ ] No private estate content has entered this plan, its evidence artifacts,
      or the public release surface.

## Explicit Non-Goals

- Rewriting the framework or changing its three-layer ontology.
- Mechanising semantic judgement, inflection declaration, or human authority.
- Adding a database, daemon, opaque mutable cache, or vendor memory service.
- Making estate-wide startup work cheap by hiding failures or extending timeout
  budgets again.
- Treating tests, hooks, emitted content, or documentation as proof that a model
  received, read, or followed a contract.
- Claiming universality from the currently observed harnesses.
- Migrating or publishing private domains as part of substrate remediation.
- Promising zero defects. The promise is that every found residue has an owner,
  evidence, and an honest disposition.

