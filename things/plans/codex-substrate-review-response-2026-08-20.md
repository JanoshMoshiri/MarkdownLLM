---
id: codex-substrate-review-response-2026-08-20
type: plan
status: in-progress
version: 1.0
created: 2026-08-20
priority: critical
exposed: false
tags: [review-response, security, transaction-integrity, repository-view, adapters, specification-adherence, hardening]
linked_things:
  - id: independent-substrate-review-2026-08-20-codex
    relation: derived-from
    notes: "Immutable finding set and acceptance oracle for this remediation."
  - id: independent-review-2026-08-11-codex
    relation: references
    notes: "The fifteen earlier findings are re-dispositioned rather than copied into a second untraceable backlog."
  - id: session-start-hardening
    relation: complements
    notes: "Existing owner for contract delivery, integrity, orientation pull, and live re-test; this plan owns cross-cutting evidence semantics and integration acceptance."
  - id: vendor-harness-adapter-foundation
    relation: complements
    notes: "Existing owner for Claude Code and Codex adapter acceptance; this plan owns transaction/trust prerequisites and the integrated three-harness closeout."
  - id: cowork-adapter
    relation: complements
    notes: "Existing owner for Cowork assembly and live evidence; this plan requires lifecycle-service parity and consumes its acceptance records."
  - id: evidence-and-eval-backlog
    relation: complements
    notes: "Existing owner for longitudinal/model evidence; eval-command correctness is repaired here only to make that owner's evidence boundary trustworthy."
  - id: deterministic-calculation
    relation: complements
    notes: "Existing owner for calculation capability; this plan routes strict-mode and exact-decimal defects there and verifies their closure."
  - id: mechanical-coherence-checks-backlog
    relation: complements
    notes: "Existing owner for earned deterministic checks; template-instantiation validation is reconciled there rather than duplicated."
  - id: scaffold-declares-visibility
    relation: complements
    notes: "The exposure-at-birth work remains separately owned; scaffold transaction changes must not silently absorb or bypass it."
  - id: llm-driven-systems-manifesto
    relation: references
    notes: "Final claim reconciliation preserves the thesis while narrowing guarantees to demonstrated layers."
---

# Codex Substrate Review Response — Transaction Integrity

## Purpose

Disposition and remediate `independent-substrate-review-2026-08-20-codex`
without creating fifteen unrelated patches or stealing scope from existing live
plans. The programme is organised around the five shared seams the review found:
repository state view, authority/transaction, canonical definition, evidence
semantics, and claim vocabulary.

The plan was drafted behind an operator-review gate. On 2026-08-20 the operator
explicitly waived that intermediate pause, accepted the review as the
requirements specification, accepted this plan as the design, and instructed
execution through completion without further routine input. This commit seals
the plan before Phase 0 implementation begins.

Exposure decision: **no**. This plan is internal framework work. Its eventual
public result belongs in a release note derived after acceptance, not in a live
served face while the findings remain open.

## Authority And Autonomy Boundary

Approval of this plan authorises the agent to implement code, tests, templates,
specifications, docs, review/decision/evidence things, index regeneration, and
local commits at the meaning boundaries below. It does **not** authorise a
release, push of the framework public repository, modification of downstream
domain repositories, use or storage of credentials, live network trust, or a
claim that an unavailable harness was verified.

The agent can complete all local engineering and documentary work without
further input after approval. Four closeout facts remain human- or
environment-dependent:

1. approval or rejection of the recommended autopush reversal (default deny,
   explicit `autopush: true`);
2. fresh live acceptance sessions in Claude Code, Codex, and Cowork where this
   session cannot launch the actual product surface;
3. public release/push judgement;
4. the requested independent Claude assessment.

If the operator approves this plan unchanged, item 1 is considered decided in
favour of the recommended default-deny design. The agent should then need no
interruption until it reaches live-harness evidence or a genuinely new product
choice not represented here.

## Ownership Rule

One surface, one owner. This plan owns the integration sequence, new shared
ports, critical trust boundary, transaction corrections, and final acceptance
matrix. Existing plans keep their subject-matter ownership:

| Surface | Owning plan | This plan's role |
|---|---|---|
| Session contract delivery and deep-orient routing | `session-start-hardening` | verify evidence vocabulary; integrate and close only after its gates close |
| Claude Code / Codex lifecycle adapter | `vendor-harness-adapter-foundation` | supply shared state/transaction ports; consume acceptance evidence |
| Cowork bootstrap/assembly/live behaviour | `cowork-adapter` | repair shared lifecycle use; consume local and remote acceptance |
| Longitudinal/model evidence programme | `evidence-and-eval-backlog` | make the eval command a trustworthy boundary; do not redesign the programme |
| Calculation capability | `deterministic-calculation` | route exactness/strictness fixes and test them in the integrated floor |
| Earned coherence checks and template residue | `mechanical-coherence-checks-backlog` | add only same-builder template instantiation checks that meet its admission rule |
| Exposure at scaffold birth | `scaffold-declares-visibility` | preserve its decision and avoid duplicate implementation |

Where execution discovers duplicate ownership, reconcile the plans before code.
Do not let this umbrella become another 2,000-line history ledger.

## Phase 0 — Freeze, Reproduce, And Route

Pin the implementation baseline and turn every review finding into an evidence-
backed disposition against current HEAD.

- [ ] Record baseline full SHA, branch, working-tree/index state, Python/runtime,
  test count, and validator/coherence/index/provenance results.
- [ ] Reproduce every open previous finding and each new finding with the
  smallest deterministic fixture that proves or refutes it.
- [ ] Mark each finding `accepted`, `narrowed`, `already-fixed`, or `rejected`,
  with evidence and exact owner; do not treat the review's severity as proof.
- [ ] Run `mdllm touchpoints` for every specification or stable thing whose rule
  will change; record the prose-only residue the index cannot see.
- [ ] Reconcile the existing plan graph so no checklist item has two owners.
- [ ] Add regression tests that fail for every accepted mechanical defect before
  implementing the fix, where a safe failing fixture is possible.

**Gate:** one disposition matrix, no accepted finding unowned, a clean pinned
baseline, and failing tests that describe the critical/high defects precisely.

## Phase 1 — Close The Automatic External-Execution Boundary

This phase precedes architectural refactoring because the current session-start
path can reach repository-supplied commands and network destinations.

- [ ] Introduce an `ExternalTrustPolicy` application port. Its input is the
  exact server entry plus repository identity; its result distinguishes
  command, network, headers/credentials, and body-read authorization.
- [ ] Store approvals only in the clone's Git directory or another explicitly
  local untracked location, pinned to a cryptographic hash of the exact selected
  `.mcp.json` entry. A config change invalidates trust.
- [ ] Make automatic/session/trigger paths default to `unevaluable-untrusted`;
  they must not launch a command or make a request merely because the repository
  declares one.
- [ ] Add an explicit CLI trust/review flow that shows command, arguments, URL,
  header names (never secret values), repository, and hash before recording
  approval. Trust is granular and revocable.
- [ ] Bound response bytes and time, redact errors, constrain schemes, handle
  redirects deliberately, and complete the MCP initialize/initialized sequence.
- [ ] Treat external bodies as quoted data in egress/prompt surfaces; metadata
  quarantine is not permission to execute instructions found in the body.
- [ ] Test malicious stdio sentinel, config-hash drift, arbitrary URL, redirect,
  header redaction, oversized body, timeout, protocol sequence, and trusted happy
  paths. No test may actually exfiltrate or call the public network.

**Gate:** opening or orienting an untrusted repository cannot execute its
configured MCP command or make its configured request; trusted entries remain
usable and hash-bound.

## Phase 2 — One Repository View For Every Deterministic Claim

Add the minimum central abstraction needed to name the bytes being reasoned
about. Avoid a general virtual filesystem.

- [ ] Introduce `RepositoryView` with three explicit modes: `WORKTREE` for
  drafts, `INDEX` for the commit candidate, and immutable `COMMIT(<full-sha>)`
  for stable reads/serving.
- [ ] Make scanning/parsing accept a view and logical path rather than opening
  ambient filesystem paths internally. Preserve current CLI worktree behaviour
  unless a command's contract requires another mode.
- [ ] Make the pre-commit floor validate the exact candidate tree (`git
  write-tree`/index plumbing), including examples, schemas, indexes, boundary
  checks, and candidate cues.
- [ ] Prove both mismatch directions with real Git commits: invalid staged +
  repaired worktree must block; valid staged + invalid worktree must commit.
- [ ] Make MCP serve bytes from the exact full commit it stamps. Dirty exposed
  worktree content is refused or explicitly marked uncommitted without a false
  reference triple.
- [ ] Pin full-corpus and significant agent reads to a base commit; before write,
  detect moved HEAD and require explicit reconciliation rather than silently
  applying conclusions from a mixed snapshot.
- [ ] Expose prior/current candidate views for mechanical state-transition checks
  without teaching each validator Git plumbing.

**Gate:** validation, provenance, serving, and long-read evidence each name one
view; no test can make committed bytes differ from the bytes the floor accepted.

## Phase 3 — Make Mutation And Publication Transactional

Reuse the adapter installer's preflight/plan/apply/verify shape instead of
inventing another transaction model.

- [ ] Add a small `RepositoryTransaction` service for exact-path staging,
  temporary-index or equivalent isolation, apply/rollback reporting, and
  optimistic HEAD checks.
- [ ] Scaffold preflights the outer repository and either preserves unrelated
  staged state exactly or refuses before any write. Its isolation commit contains
  only the intended `.gitignore` delta.
- [ ] Scaffold failure leaves a recoverable, truthfully reported state; add
  failure injection at every boundary and assert no unrelated state moves.
- [ ] Resolve the hooks directory through Git, including gitfiles, worktrees,
  bare/linked layouts, and `core.hooksPath`.
- [ ] Never overwrite operator hooks. Install a managed fragment/dispatcher,
  chain safely, or refuse with an explicit reviewed replacement path. Preserve
  bytes, order, exit semantics, and uninstallability.
- [ ] Reverse publication authorization to fail closed: explicit
  `git.autopush: true` enables; false, absent, malformed, or unknown disables and
  `doctor` explains why. Update scaffold/template/migration guidance so new
  domains make an explicit choice rather than inheriting ambiguity.
- [ ] Preserve the framework root's deliberate `autopush: false`; never publish
  this remediation automatically.

**Gate:** adversarial staged-state, worktree, custom-hooks-path, existing-hook,
parse-failure, and partial-failure tests show exact preservation; no send occurs
without explicit valid authorization.

## Phase 4 — Give Definitions One Canonical Owner

- [ ] Introduce one strict YAML loader for thing frontmatter, schemas, sentinel,
  AGENTS frontmatter, fixtures, and internal config. Reject duplicate mapping
  keys with file/key/location; preserve the deliberate YAML-1.1 `on` handling or
  replace it consistently.
- [ ] Add corpus regression fixtures for duplicate status, dependencies,
  origin/verified, Git policy, and schema keys.
- [ ] Introduce one structural-reference registry describing field shape,
  target cardinality, egress privacy, reverse indexing, validation, and cue
  relevance. Make validation, indexes, touchpoints, MCP egress, candidates, and
  schema-field ownership consume it.
- [ ] Extend candidate semantics to additions, modifications, deletions, and
  renames. Each state receives a truthful cue question; a new thing is not
  presumed incapable of contradiction.
- [ ] Delete duplicated field lists only after cross-builder tests prove the
  registry feeds each consumer.

**Gate:** duplicate keys cannot enter any operative definition surface; adding
one registered structural field makes all relevant consumers see it or makes a
fitness test fail.

## Phase 5 — Make Mechanical State And Evidence Semantics Total

Split into meaning-boundary commits; the grouping here is about one guarantee:
machine-readable conditions never crash, fall silent, or return success for
failure.

### 5A — Trigger and workflow state

- [ ] Compile trigger declarations into typed results: `fired`, `not-fired`,
  `unevaluable`, or `invalid`, with reasons. Evaluators do not throw on input.
- [ ] Invalid thresholds, unknown conditions/types, absent watched things, and
  missing subtasks are explicit validation/evaluation results. Empty or partial
  sets never become success.
- [ ] Use prior-commit and candidate views to enforce declared workflow
  transition edges mechanically. Whether work deserves advancement remains
  semantic; whether an edge exists is not.

### 5B — Calculation and eval evidence

- [ ] Route exact-decimal and strict-mode fixes through
  `deterministic-calculation`: preserve numeric lexemes or require quoted exact
  decimals; strict non-evaluability is Error; excluded/quarantined inputs are
  visible whenever they change the input set.
- [ ] Make `validates_clean` invoke the complete validation boundary and retain
  scan findings.
- [ ] Agent process non-zero, timeout, parse failure, agent-reported error,
  validation error, or failed assertion makes the trial fail and the command
  return non-zero.
- [ ] Use collision-resistant run identity and record full framework commit,
  fixture content hash, CLI/tool version, model, effort, harness/build, process
  status, validation summary, and assertion result.

### 5C — Session evidence vocabulary

- [ ] Reconcile with `session-start-hardening`; do not create a parallel gate.
- [ ] Record contract version/content fingerprint and distinguish `emitted`,
  `received-whole`, `read-observed`, `applied-evidence`, and
  `outcome-validated`. No stronger state is inferred from a weaker one.
- [ ] Invalidate freshness when the operative contract changes, not whenever
  unrelated HEAD advances.
- [ ] Replace vacuous or permissive assertions with behavioural tests.

**Gate:** malformed definitions produce findings rather than exceptions or
silence; every failed eval leg returns non-zero; session reports use only the
evidence level actually established.

## Phase 6 — Unify The Three Adapter Lifecycles And Compact Forward State

- [ ] Replace Cowork assembler's fetch-under-an-estate-sync-heading with the
  shared sync application service and its typed result; reused clean clones
  fast-forward, dirty/diverged clones are reported and never resolved.
- [ ] Remove private cross-module imports in assembly by promoting only the
  smallest stable application ports required.
- [ ] Define one lifecycle result vocabulary across Claude Code, Codex, and
  Cowork: dispatched, executed, output received, contract whole/deferred,
  floor active, write feedback available, and publication authority.
- [ ] Publish an internal capability/evidence matrix by exact harness build;
  “adapter exists” is never a synonym for adherence or full support.
- [ ] Complete local automated renderer/inspector/runner/install/sync tests for
  all three adapters.
- [ ] Reconcile completed narrative out of the 2,021-line adapter foundation and
  other oversized live plans into stable evidence/review artifacts. Live plans
  retain current state, remaining gates, decisions, and links; Git retains the
  detailed evolution. Do not delete evidence.
- [ ] Finish agent-executable parts of `session-start-hardening`,
  `vendor-harness-adapter-foundation`, and `cowork-adapter`; preserve any real
  live-product gate as pending rather than self-certifying it.

**Gate:** one shared service implements each lifecycle action; plans are
forward-readable; local matrix green; unavailable live rows remain explicitly
pending.

## Phase 7 — Harden Birth, Release, And Claim Surfaces

- [ ] Treat templates as build inputs: instantiate every scaffold/evidence/thing
  template into disposable fixtures and validate the result under its target
  schema. Reconcile the check into `mechanical-coherence-checks-backlog`.
- [ ] Repair example language to separate declared policy, enforcement
  mechanism, and evidence of operation; label legal examples synthetic and
  non-authoritative.
- [ ] Replace moving-branch pipe-to-shell guidance with versioned release
  artifacts and integrity verification. Pin dependencies and CI actions where
  practicable; document the remaining trust root.
- [ ] Reconcile manifesto, README, operator docs, framework map, adapter matrix,
  and release claims around the accepted vocabulary: deterministic structural
  layer, probabilistic interpreter, recorded accepted state, incomplete reason
  trace, and build-specific harness evidence.
- [ ] Preserve the manifesto's thesis and efficiency hypothesis; narrow only
  claims the substrate cannot test or guarantee.

**Gate:** a fresh domain born from every supported template validates and runs
its declared floor; installation guidance is version-pinned; public prose does
not claim a stronger guarantee than the acceptance matrix demonstrates.

## Phase 8 — Adversarial Acceptance And Independent Closeout

### Agent-executable acceptance

- [ ] Full unit/integration suite green on Windows and the available POSIX CI
  surface.
- [ ] Framework validation, examples, coherence, index checks, provenance,
  doctor, package/build, and template-instantiation checks clean at one full
  commit.
- [ ] Real-Git adversarial suite covers staged/worktree mismatch, concurrent
  HEAD movement, dirty MCP serving, malicious `.mcp.json`, unrelated staged
  state, existing hooks, malformed publication policy, invalid transitions,
  total trigger results, strict calculations, and failed eval exit status.
- [ ] Produce a stable implementation evidence artifact mapping every review
  finding to commit, test, disposition, residual risk, and owner.
- [ ] Update this plan after every meaning boundary; do not wait until the end
  to reconstruct progress.

### Human/harness acceptance

- [ ] Fresh Claude Code run: exact build, automatic lifecycle, contract receipt,
  read/application probe, nested domain floor, and write feedback.
- [ ] Fresh Codex run: exact app/CLI build, instruction delivery, lifecycle
  dispatch, restricted→approved Git path, nested domain floor, and write
  feedback limitations.
- [ ] Fresh Cowork remote and local runs: exact build/plugin, assembly sync,
  contract receipt, adherence probe, commit floor, and publication path.
- [ ] Operator decides release/push after reviewing change reconciliation,
  changelog, version, compatibility/migration notes, and residual risk.
- [ ] Claude receives this immutable review, this plan, the implementation
  evidence, and the final commit range; Claude independently marks each finding
  closed, narrowed, rejected, or reopened.

**Done when:** every critical/high finding is closed or explicitly accepted by
the operator with residual risk; lower findings are closed or owned with a
dated gate; the three-harness evidence matrix says exactly what ran; Claude's
assessment is captured; validation/coherence/tests are clean; the tree is
committed; publication debt is reported. A public push is a separate release
decision and is not a completion criterion for the local remediation.

## Execution Discipline

- Commit at each phase or smaller meaning boundary; never one giant remediation
  commit.
- Significant rule changes run cue → assimilate → walk → seal across the full
  corpus, including insights and human docs.
- Add a test before or with every mechanical fix. A prose claim does not close a
  code finding; a code path does not close a live-harness claim.
- Prefer deletion/consolidation of duplicated mechanism over another drift
  checker. Add checks only where truth is mechanically decidable and built from
  a different artifact than the surface being checked.
- Do not broaden the ontology while transaction work is open unless a finding
  proves a missing primitive.
- Never use `--no-verify`, never force-push, never silently overwrite operator
  state, and never promote unavailable evidence into “passed.”
