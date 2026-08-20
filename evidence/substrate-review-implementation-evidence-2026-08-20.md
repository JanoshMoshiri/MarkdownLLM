---
id: substrate-review-implementation-evidence-2026-08-20
type: artifact
status: stable
version: 1.1
created: 2026-08-20
origin: synthesised
exposed: false
tags: [review-response, implementation-evidence, transaction-integrity, security, repository-view, adapters]
linked_things:
  - id: independent-substrate-review-2026-08-20-codex
    relation: derived-from
    notes: "The sealed review is the immutable requirements and finding oracle."
  - id: codex-substrate-review-response-2026-08-20
    relation: documents
    notes: "Maps the response plan's implemented surfaces and its remaining acceptance gates."
  - id: substrate-review-phase0-disposition-2026-08-20
    relation: extends
    notes: "Carries Phase 0's accepted findings forward to implementation disposition."
  - id: harness-capability-evidence-matrix-2026-08-20
    relation: references
    notes: "The build-specific matrix owns the exact live-harness evidence boundary."
---

# Substrate Review Response — Implementation Evidence

## Purpose And Evidence Boundary

This artifact maps every finding in
`independent-substrate-review-2026-08-20-codex` to the implementation now in
the repository, the tests that exercise it, its commit boundary, and any risk
that code in this session cannot truthfully close. It is an implementation
record, not a claim that a local test proves model reading, live vendor
behaviour, publication, or an independent review.

The commit labels used below are:

- **C1 — architecture and implementation:**
  `26731680996b8706eb8f1cd08835de3b70769339`
  (`security: pin repository authority and transaction boundaries`).
- **C2 — doctrine and reconciliation:**
  `a14b0c3f9439cb14e5058bc5820526e65e2ee402`
  (`reconcile: seal v3.33 transaction-integrity doctrine`).
- **C3 — final tested architecture:**
  `eb80d46f141d7fb77027cdf51e222d7f72db5a6c`
  (`architecture: close dependency cycles and type sync outcomes`).
- **Final cross-platform suite at C3:** Windows **682 passed in 929.50
  seconds**; native WSL/Ubuntu **675 passed, 7 skipped in 118.26 seconds**.
  Both runs used fresh clones of the same full SHA. The Windows clone used the
  repository's pinned PyYAML-capable `.venv` through a local junction; the WSL
  clone used Python 3.14.4, PyYAML 6.0.3, and pytest 9.0.2.

The closeout-record commit is intentionally not embedded in its own content:
that would require a self-referential Git SHA. The commit containing this
artifact and the completed plan is resolved with `git log -1 -- <path>`; its
candidate must pass the installed frozen-index hook before Git accepts it.

In the table, **closed locally** means the mechanical defect is resolved in C1,
C2, or C3 and has regression evidence. It does not promote local evidence into a
live-harness, release, or independent-assessment result. **Narrowed** means the
local enforceable boundary is implemented but part of the original finding is
necessarily owned by a later human, harness, or release observation.

## Finding-To-Implementation Disposition

| Review finding | Final disposition | Principal implementation files | Principal regression evidence | Commit | Residual risk and owner |
|---|---|---|---|---|---|
| **1. Pre-commit validated worktree, not index** | **Closed locally; exact-candidate acceptance passed** | `tools/markdownllm/repository_view.py`, `validation.py`, `coherence.py`, `scaffold.py` | `test_repository_view.py`, `test_coherence_repository_view.py`, `test_phase1_4_integration_audit.py` prove both invalid-index/repaired-worktree and valid-index/invalid-worktree directions and a frozen candidate tree. | C1 + C3 | The installed hook accepted C3's exact frozen tree; future commits retain the same compare-and-swap boundary. Owner: repository-view and validation boundary. |
| **2. No consistent read snapshot** | **Closed locally for modelled deterministic and significant-read paths** | `repository_view.py`, `model.py`, `session.py`, `provenance.py` | `test_repository_view.py` covers worktree/index/immutable-commit views, full-SHA reads, nested scans, HEAD movement, and significant-read refusal. | C1 | A caller must still select the view its contract requires; moved HEAD requires explicit reconciliation. Owner: each application service through `RepositoryView`. |
| **3. Autopush failed open** | **Closed locally** | `sync.py`, `publish.py`, `doctor.py`, `scaffold.py`, `templates/AGENTS.md.template` | `test_publish.py`, `test_repository_transactions.py`, `test_residual_totality.py`, `test_mdllm.py` cover literal true, false, absent, malformed, and unreadable policy plus explanatory diagnostics. | C1 + C2 | No publication is authorised by this work. The operator owns any one-shot publish or later release decision. |
| **4. Scaffold and hook installation were not transactional** | **Closed locally with an explicit recovery model** | `repository_transaction.py`, `hook_contract.py`, `scaffold.py`, `runtime.py` | `test_repository_transactions.py`, `test_scaffold_harness_selection.py`, `test_phase1_4_integration_audit.py` cover unrelated index state, optimistic HEAD checks, custom hooks paths, worktrees, foreign hooks, exact old-Git hook bytes, rollback, and failure injection. | C1 + C3 | Some failures after isolation truthfully leave a recoverable state instead of claiming impossible atomic rollback across Git and filesystem effects. Owner: scaffold transaction; operator only when a reported recovery step remains. |
| **5. MCP provenance could stamp the wrong bytes** | **Closed locally** | `repository_view.py`, `mcp_server.py`, `model.py` | `test_repository_view.py` proves commit-served bytes carry the same immutable revision, index candidates never claim commit provenance, and dirty content is refused or explicitly uncommitted. | C1 | Uncommitted serving must continue to be labelled as such; no adjacent commit may be inferred. Owner: MCP egress through `RepositoryView`. |
| **6. Structural graph lists drifted** | **Closed mechanically** | `structural_refs.py`, `validation.py`, `indexes.py`, `touchpoints.py`, `mcp_server.py` | `test_structural_reference_registry.py` proves shared ownership across validation, extraction, reverse indexes, cues, schema ownership, and egress privacy. | C1 | The registry's semantics remain specification content and require reconciliation when extended. Owner: structural-reference registry. |
| **7. Duplicate YAML keys were accepted** | **Closed mechanically** | `yaml_loader.py`, `model.py`, `repo.py`, `doctor.py`, `kernel_gen.py`, `refresh.py`, `session.py`, `scaffold.py` | `test_strict_yaml.py`, `test_residual_totality.py`, `test_phase1_4_integration_audit.py` cover duplicate keys, non-mappings, malformed sentinels/config, and clean CLI findings without tracebacks. | C1 | The deliberate YAML 1.1 `on` normalisation remains compatibility behaviour and must stay consistent. Owner: strict YAML boundary. |
| **8. Eval could succeed on failed evidence** | **Closed mechanically** | `evals.py`, `validation.py` | `test_eval_integrity.py` covers scan/full-validation findings, non-zero process and failed-trial status, transport/agent distinctions, exact evidence pins, observed build metadata, and collision-resistant run identities. | C1 | New longitudinal model trials remain owned by `evidence-and-eval-backlog`; they are not a code-fix acceptance condition. |
| **9. Calculation strictness and exactness loopholes** | **Closed mechanically for lexical inputs** | `yaml_loader.py`, `calc.py`, `validation.py` | `test_calc.py`, `test_strict_yaml.py`, `test_eval_integrity.py` cover exact decimal lexemes, strict unevaluability as Error, and visible quarantine/exclusion. | C1 | A binary float rounded before it reaches the framework cannot recover its source lexeme; exact external decimals must remain lexical/quoted. Owner: deterministic calculation boundary. |
| **10. Workflow transition legality was agent-owned** | **Closed mechanically for declared edges** | `validation.py`, `repository_view.py` | `test_mechanical_state.py` covers allowed and illegal prior-to-candidate edges and prevents the same candidate from rewriting its definition to authorise its transition. | C1 | Whether the work deserves advancement remains semantic Layer 2 judgement. Owner: workflow validation. |
| **11. Trigger evaluation was partial or unsafe** | **Closed mechanically** | `triggers.py`, `validation.py`, `imports_check.py` | `test_mechanical_state.py`, `test_mdllm.py`, `test_external_trust.py` cover typed total outcomes, malformed thresholds, unknown or absent inputs, missing subtasks, and untrusted external conditions. | C1 | Genuinely unavailable conditions remain explicit `unevaluable`, never silent success. Owner: typed trigger evaluator. |
| **12. Session attestation SHA and semantics were insufficient** | **Narrowed; local evidence vocabulary closed, live assurance pending** | `session.py`, `session_contract.py`, `repository_view.py`, `harness_ports.py`, `lifecycle_runner.py` | `test_contract_emission.py`, `test_repository_view.py`, `test_lifecycle_runner.py`, and `test_mdllm.py` cover contract fingerprints, integrity/elision, significant-read base SHA, and freshness tied to contract content rather than unrelated HEAD movement. | C1 + C2 + C3 | Local code cannot self-prove that a model read, applied, or complied with emitted content. Fresh product probes own those higher evidence states. |
| **13. External integration trust boundary** | **Closed for automatic local execution authority** | `external_trust.py`, `imports_check.py`, `session.py`, `triggers.py`, `cli.py` | `test_external_trust.py`, `test_architecture_fitness.py` cover default deny, clone-local hash-bound granular trust, drift/revoke, command and network separation, secret redaction, bounded I/O/time, schemes/redirects, MCP initialisation, and commit pins. | C1 | Explicitly trusted execution is authorised, not sandboxed. No security test calls the public network. Human operator owns grant/revoke judgement. |
| **14. Birth-surface defects and overclaims** | **Closed locally** | `.gitattributes`, `templates/`, `examples/`, `domain-specification-guide.md`, `docs/first-hour.md` | `test_template_instantiation.py`, `test_template_sources.py`, `test_scaffold_harness_selection.py` instantiate distributable templates, check source shape, and enforce checkout-stable LF bytes; examples are labelled synthetic and non-authoritative. | C1 + C2 + C3 | Fresh Windows and native WSL checkouts passed locally. A released-version birth run remains release acceptance. Owner: template/coherence backlog and release operator. |
| **15. Supply-chain hardening** | **Narrowed; next-release acceptance pending** | `.github/workflows/validate.yml`, `requirements-ci.txt`, `install.sh`, `install.ps1`, `.gitattributes`, `templates/cowork-bundle/bootstrap.sh.template`, `README.md` | `test_template_sources.py`, `test_architecture_fitness.py`, adapter/bootstrap tests | C1 + C2 + C3 | The repository pins actions and PyYAML, verifies installer bytes, and fixes executable/template checkout bytes, but no v3.33 public release artifact or signature exists yet. The documented remaining trust root and release/push judgement belong to the operator. |
| **A. Automatic orientation crossed repository-supplied execution** | **Closed locally through the external-trust boundary** | `external_trust.py`, `imports_check.py`, `session.py`, `triggers.py` | `test_external_trust.py` proves untrusted automatic paths do not spawn commands or make requests and that config drift revokes authority. | C1 | Same authorised-not-sandboxed residual as Finding 13. Owner: `ExternalTrustPolicy` plus operator authority. |
| **B. Five assurance states were conflated** | **Narrowed; vocabulary closed, live evidence pending** | `session.py`, `session_contract.py`, `harness_ports.py`, `lifecycle_runner.py`, `evidence/harness-capability-evidence-matrix-2026-08-20.md` | `test_contract_emission.py`, `test_harness_diagnostics.py`, `test_lifecycle_runner.py` keep `emitted`, `received-whole`, `read-observed`, `applied-evidence`, and `outcome-validated` distinct. | C1 + C2 + C3 | No stronger state may be inferred from a weaker one. Fresh harness runs own receipt/read/application/outcome evidence. |
| **C. Cowork assembly overstated the lifecycle it ran** | **Closed locally; live Cowork pending** | `assemble.py`, `sync.py`, `git_transport.py`, `bundle_service.py`, `adapters/cowork.py` | `test_assemble.py` covers clean reused-clone fast-forward, dirty and diverged non-resolution, and immutable `SyncResult`/`SyncState` behaviour; Cowork adapter/bundle tests cover rendering. | C1 + C3 | Fresh Cowork remote and local runs with an exact client/plugin build remain pending. Owner: `cowork-adapter`. |
| **D. Forward-work surfaces exceeded agent-readable shape** | **Closed locally** | `things/plans/vendor-harness-adapter-foundation.md`, `things/plans/cowork-adapter.md`, `things/plans/session-start-hardening.md` | The live plans are 135, 168, and 124 lines respectively, reduced from 2,021, 536, and approximately 303 while Git retains the detailed history. | C2 | The umbrella plan must remain a forward-state and acceptance surface, not become a reconstructed history ledger. Owner: each plan's maintainer. |
| **E. Adapter product clarity lagged correctness** | **Closed as a clarity artifact; live rows remain explicit** | `evidence/harness-capability-evidence-matrix-2026-08-20.md`, adapter registry/diagnostics surfaces | `test_harness_diagnostics.py`, `test_harness_ports.py`, `test_adapter_contract.py` support the seven distinct lifecycle dimensions recorded by exact known build. | C1 + C2 | Cowork client build/local evidence and fresh Claude Code, Codex, and Cowork rows remain pending rather than promoted to support claims. Owner: harness-specific plans and capability matrix. |

## Final Architecture Acceptance Evidence

C2 remains the last doctrine baseline; C3 is the final tested code and
checkout-contract tree. The closeout record changes only this evidence, its
plan, and their regenerated indexes, so the full behavioural suites are pinned
to C3 while the record candidate is judged separately by the exact-index hook.

| Validation surface | Final result |
|---|---|
| Full Windows unit/integration suite | **682 passed in 929.50 seconds** from a fresh Windows Git clone of C3. The clean checkout exposed LF template/fixture bytes and used the repository's pinned `.venv` through a local junction. |
| Full native WSL/Ubuntu suite | **675 passed, 7 skipped in 118.26 seconds** from a fresh Linux Git clone of C3. The skips are platform-conditional; no test failed. |
| Architecture fitness | **7 dedicated checks passed** and are included in both full suites: the package import graph has zero strongly connected components, there are zero cross-module private imports, hook execution layers do not depend on scaffold, and vendor seams remain port-only. |
| Exact-index validation at C3 | **Clean:** 237 framework things, 6 compliance-pattern things, and 14 life-manager things; 0 Errors, 0 Warnings, 0 Info. The frozen tree was `019e6eeecac67f6a6e94b179d67834b873faa8f0`. |
| Exact-index coherence at C3 | **Accepted:** 0 Errors and 0 Warnings; four informational recency prompts for stable specifications changed within the last 15 commits. |
| Derived indexes at C3 | **In sync:** relationships coverage 237 and provenance coverage 36; optional trigger/schema indexes remain intentionally undeployed. |
| Immutable provenance at C3 | **Accepted:** view `commit:eb80d46f141d7fb77027cdf51e222d7f72db5a6c`; informational dated-input advisories only. |
| Kernel and build surfaces | `kernel --check` in sync; `compileall` clean; PowerShell installer parser clean; `bash -n` clean for `install.sh` and the Cowork bootstrap template; the complete argparse registry rendered successfully. |
| Installed frozen-tree hook and doctor | The installed pre-commit hook **passed** C3's exact candidate. With real Git candidate permissions, doctor reported `pre-commit hook EXECUTES (validation currently clean)` and `FLOOR ACTIVE`; publication authority remained literal-false/off. |

For comparison, C2's committed Windows baseline was 675 passed in 881.15
seconds with the same 237 + 6 + 14 corpus counts. C3 supersedes that behavioural
baseline and additionally closes the typed-sync, dependency-direction, and
fresh-Windows-checkout gaps found during final acceptance.

## Execution Variance — 84-File Implementation Commit

The umbrella plan instructed execution to commit at each phase or smaller
meaning boundary. C1 instead sealed the integrated mechanical implementation as
one **84-file** commit, with 8,800 insertions and 925 deletions; C2 then kept the
33-file doctrine, evidence, generated artifacts, and plan compaction separate.
C3 is a smaller, independently tested architecture boundary for dependency
direction, typed sync results, and deterministic Windows checkout bytes.

This is a recorded execution variance. The shared abstractions and their
consumers were accepted together, which preserved an internally consistent
candidate and let the installed exact-index hook judge one frozen tree, but it
also enlarged the review and bisection radius beyond the plan's preferred
shape. The per-finding tests and this map restore traceability; they do not make
the variance disappear. The independent Claude closeout should assess the C1
diff at the finding level and the distinct C2 doctrine/C3 architecture closeouts.

## Residual Acceptance And Authority

The following are deliberately not marked complete by local implementation:

1. **External execution:** trusted command or network use is explicit,
   clone-local, granular, and hash-bound, but it is not sandboxed. Tests use
   local fixtures and do not call the public network. Real trust grants remain
   human authority.
2. **Live harnesses:** fresh exact-build Claude Code and Codex sessions, plus
   Cowork remote and local assembly/session runs, still owe receipt, read,
   application, floor, write-feedback, and outcome evidence at only the level
   each product can actually expose.
3. **Hosted CI:** native WSL/Ubuntu accepted C3 locally, but the pinned hosted
   workflow has not run for an unpublished commit. Local POSIX evidence is not
   a claim about a remote CI service.
4. **Release and publication:** no public push or v3.33 release is authorised or
   recorded here. The framework root remains `autopush: false`; reconciliation,
   compatibility notes, artifact integrity, and publication judgement remain
   operator-owned.
5. **Independent review:** Claude has not yet received the immutable review,
   response plan, C1–C3 implementation, this artifact, and the final suite
   result. Its independent closed/narrowed/reopened assessment remains pending.
6. **Filesystem concurrency:** the transaction layer rechecks before atomic
   replace and never blindly overwrites a detected concurrent edit, but ordinary
   filesystems expose no universal content compare-and-swap primitive. A narrow
   recheck-to-replace race against a non-cooperating writer remains. Owner:
   future transaction hardening if field evidence makes a stronger primitive
   worth its complexity.

## Closeout Handoff

The local mechanical architecture, doctrine, and cross-platform acceptance are
complete through C3. The record seal containing this artifact and the completed
plan must still preserve the distinctions above: implementation is not live
adherence; explicit authority is not sandboxing; a locally accepted commit is
not a hosted-CI result; and a local commit is not a release or push.
