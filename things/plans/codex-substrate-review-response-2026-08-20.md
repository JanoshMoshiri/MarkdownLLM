---
id: codex-substrate-review-response-2026-08-20
type: plan
status: completed
version: 1.2
created: 2026-08-20
priority: critical
exposed: false
tags: [review-response, security, transaction-integrity, repository-view, adapters, specification-adherence, closeout]
linked_things:
  - id: independent-substrate-review-2026-08-20-codex
    relation: derived-from
    notes: "Immutable requirements and finding oracle."
  - id: substrate-review-phase0-disposition-2026-08-20
    relation: references
    notes: "Pinned baseline, reproductions, dispositions, ownership, and touchpoint residue."
  - id: substrate-review-implementation-evidence-2026-08-20
    relation: references
    notes: "Finding-by-finding implementation, tests, commits, residual risk, and final closeout evidence."
  - id: harness-capability-evidence-matrix-2026-08-20
    relation: references
    notes: "Exact-build live-harness evidence boundary; pending rows remain external acceptance."
  - id: session-start-hardening
    relation: complements
    notes: "Owns contract delivery and fresh receipt/read/application evidence."
  - id: vendor-harness-adapter-foundation
    relation: complements
    notes: "Owns fresh Claude Code and Codex product acceptance."
  - id: cowork-adapter
    relation: complements
    notes: "Owns fresh Cowork remote and local product acceptance."
  - id: llm-driven-systems-manifesto
    relation: references
    notes: "The reconciliation preserves the thesis while narrowing guarantees to demonstrated layers."
---

# Codex Substrate Review Response — Local Closeout

## Purpose And Current State

This plan executes the sealed Codex review as the requirements specification
for the substrate hardening. Local implementation, reconciliation, and Phase 8
acceptance are complete. The final tested architecture is
`eb80d46f141d7fb77027cdf51e222d7f72db5a6c`; complete Windows and native WSL
suites and the exact candidate/full-commit checks accepted those bytes.

The original design, sequencing, gates, and checklists remain immutable in Git
at `27b95e739f78cad6fa609cee7b1359897ccf40ae`. This v1.2 surface deliberately
does not retain hundreds of stale open boxes after their implementation landed.
Detailed finding evidence lives in
`substrate-review-implementation-evidence-2026-08-20`; exact product evidence
lives in `harness-capability-evidence-matrix-2026-08-20`.

The plan is **completed locally**. The containing closeout-record commit seals
this plan, the implementation evidence, and their regenerated indexes; its SHA
is intentionally resolved from Git history rather than embedded
self-referentially. Live harnesses, hosted CI, independent review, and release
authority remain in the external register below.

## Authority And Completion Boundary

The operator authorised local code, tests, specifications, templates, docs,
evidence artifacts, generated artifacts, and commits. That authority does not
include a public release or push, credentials, live external trust grants, or a
claim that an unavailable product surface was verified.

Local remediation can close without self-certifying live model behaviour.
Fresh Claude Code, Codex, and Cowork sessions, public release/push judgement,
and the requested independent Claude assessment have been transferred to the
external acceptance register below. They remain real work under their existing
owners, but are not prerequisites that this local implementation can honestly
mark passed.

## Sealed Commit And Evidence Boundaries

| Boundary | Immutable reference | Meaning |
|---|---|---|
| Review and original response design | `27b95e739f78cad6fa609cee7b1359897ccf40ae` | Requirements, architecture, Phase 0–8 design, and initial acceptance gates |
| Mechanical architecture | `26731680996b8706eb8f1cd08835de3b70769339` | Repository views and transactions, external trust, strict definitions, total mechanical state, eval, adapters, templates, and tests |
| Doctrine and reconciliation | `a14b0c3f9439cb14e5058bc5820526e65e2ee402` | v3.33 specifications, claims, human guides, evidence, generated artifacts, and compact subject plans |
| Final tested architecture | `eb80d46f141d7fb77027cdf51e222d7f72db5a6c` | Dependency-direction closure, typed sync results, clean-checkout LF contract, and final code/test tree |
| Final cross-platform suites | C3 above | Windows 682 passed; native WSL 675 passed and 7 platform-conditional skips |
| Closeout record seal | Commit containing this plan | Exact-index validation/hook judges the plan, evidence, and regenerated indexes; `git log -1 -- <path>` resolves the non-self-referential SHA |

## Phase Outcomes

| Phase | Local status | Outcome |
|---|---|---|
| **0 — Freeze, reproduce, and route** | **Complete** | Pinned the clean `27b95e7…` baseline; reproduced and accepted every mechanical finding; assigned owners; recorded the touchpoint and prose-only residue in `substrate-review-phase0-disposition-2026-08-20`. |
| **1 — External execution boundary** | **Complete** | Added clone-local, configuration-hash-bound, granular `ExternalTrustPolicy`; automatic session/trigger paths default deny; command/HTTP execution is bounded, redacted, protocol-correct, and tested without public-network calls. |
| **2 — One repository view** | **Complete** | Added explicit WORKTREE, frozen INDEX, and immutable COMMIT views; validation, coherence, MCP provenance, significant reads, and prior/candidate state name the bytes they judge; mismatch and moved-HEAD fixtures pass. |
| **3 — Transaction and publication authority** | **Complete** | Added exact-path optimistic repository transactions, staged-state preservation, Git-resolved hook handling, foreign-hook safety, scaffold failure recovery, and literal-true-only publication authority with explanatory diagnostics. |
| **4 — Canonical definitions** | **Complete** | Added strict duplicate-rejecting YAML across operative definition surfaces, a canonical structural-reference registry, and lossless A/M/D/R candidate parsing including Git-valid tabs and newlines. |
| **5 — Total state and evidence semantics** | **Complete** | Trigger results are total and typed; workflow edges use prior/candidate views; calculation preserves lexical decimals and makes strict non-evaluation blocking; eval failures return failure; session assurance states and contract fingerprints remain distinct. |
| **6 — Adapter lifecycle and forward state** | **Complete** | Cowork assembly uses shared sync application services; adapter evidence uses seven distinct lifecycle dimensions; the build-specific matrix records what actually ran; the three oversized subject plans were compacted without deleting Git history. |
| **7 — Birth, supply, and claims** | **Complete** | Distributable templates instantiate and validate; Git attributes preserve their exact LF bytes in fresh Windows checkouts; examples distinguish policy, enforcement, and evidence; dependencies/actions/install guidance are pinned or integrity-checked; public prose separates deterministic structure, probabilistic interpretation, recorded state, and build-specific evidence. |

“Complete” in this table means the locally executable outcome and its focused
regression evidence exist in the sealed implementation, reconciliation, and
final architecture commits.
It does not erase the explicit residuals in the implementation evidence or
promote an external acceptance row.

## Phase 8 — Local Closeout Complete

### Committed baseline already established

At doctrine commit `a14b0c3f9439cb14e5058bc5820526e65e2ee402`:

- the full Windows unit/integration suite passed: **675 passed in 881.15s**;
- exact-index validation accepted 237 framework things, 6 compliance-pattern
  things, and 14 life-manager things;
- exact-index coherence reported no Errors or Warnings;
- exact-index provenance had informational dated-input advisories only; and
- the installed frozen-tree hook passed against the exact staged candidate.

This remained the comparison baseline while C3 closed the last architecture
and clean-checkout gaps.

### Final local gates

- [x] Seal the final tested architecture and record full SHA
  `eb80d46f141d7fb77027cdf51e222d7f72db5a6c` in this plan and the
  implementation-evidence artifact.
- [x] Run the complete Windows suite from a fresh clone of C3: **682 passed in
  929.50 seconds**.
- [x] Run the complete native WSL/Ubuntu suite from a fresh clone of C3:
  **675 passed, 7 platform-conditional skips in 118.26 seconds**.
- [x] Prove the exact candidate boundary and rerun validation, coherence,
  relationship/provenance index checks, immutable-commit provenance, doctor,
  kernel/build, installer parsers, and template checkout-byte acceptance. C3
  exact-index validation was 237 + 6 + 14 clean with no Error or Warning;
  doctor reported the installed hook executing with validation clean.
- [x] Replace every closeout placeholder in the implementation-evidence
  artifact and set this plan to `completed`; the containing record-seal
  candidate is committed only after the same frozen-index hook accepts it.

Local remediation is complete. The behavioural evidence is pinned to the final
code SHA; the subsequent record seal changes only this plan, its evidence, and
derived indexes and is judged by the exact-index hook. A public push is not part
of this completion condition.

## External Acceptance Register — Transferred, Not Self-Certified

| External acceptance | Current truthful state | Owner and durable destination | Relationship to local closeout |
|---|---|---|---|
| Fresh Claude Code lifecycle, contract receipt/read/application probe, nested floor, and write feedback | Pending exact-build rerun | `vendor-harness-adapter-foundation` + `session-start-hardening`; record in the harness capability matrix | Does not block local mechanical closeout |
| Fresh Codex app/CLI instruction delivery, lifecycle dispatch, restricted-to-approved Git path, nested floor, and write-feedback limits | Pending exact-build rerun | `vendor-harness-adapter-foundation` + `session-start-hardening`; record in the harness capability matrix | Does not block local mechanical closeout |
| Fresh Cowork remote and local assembly, sync, contract, adherence, commit floor, and publication-path evidence | Pending exact client/plugin runs | `cowork-adapter`; record in the harness capability matrix | Does not block local mechanical closeout |
| Public v3.33 release and push | Not authorised or performed | Operator; reconcile changelog, compatibility/migration notes, artifact integrity, publication debt, and release judgement | Explicitly outside local completion |
| Independent Claude assessment of review, plan, commits, evidence, and residuals | Pending after final immutable commit/evidence | Operator/review follow-up; preserve Claude's closed/narrowed/reopened disposition as a review artifact | Independent assurance, not something this implementation may self-award |

Pending rows must remain pending. “Adapter exists,” “content emitted,” and
“tests pass” are not substitutes for a product receiving, reading, applying, or
independently satisfying a contract.

## Residual Risk Register

| Residual | Local control | Remaining owner |
|---|---|---|
| Trusted external execution is authorised but not sandboxed | Default deny, granular permissions, exact config hash, local revocation, bounded/redacted I/O | Human granting trust; future sandbox work only if separately specified |
| Model read/application/outcome cannot be inferred from delivery | Five distinct evidence states and build-specific matrix | Harness plans and live product probes |
| Exact external decimals can be lost before reaching YAML | Lexical decimal preservation and strict errors | Domain author must quote/preserve exact external inputs |
| Scaffold can cross effects Git cannot universally roll back | Preflight, exact staging, preservation, and truthful recoverable-state reporting | Operator only when an explicit recovery instruction is emitted |
| Supply-chain trust cannot be reduced to zero | Pinned actions/dependency, full commit input, installer-byte verification, documented trust root | Release operator |

## Execution Variance

The original plan required commits at each phase or smaller meaning boundary
and updates after every boundary. Execution instead accumulated the integrated
mechanical work in one **84-file** C1 commit (8,800 insertions, 925 deletions),
then placed the 33-file doctrine/evidence/generated reconciliation in C2. C3
returned to a smaller boundary for dependency direction, typed sync results,
and deterministic checkout bytes. C1 preserved one internally consistent
frozen candidate, but enlarged the review and bisection radius beyond the
designed shape.

The umbrella plan was also updated late rather than after every meaning
boundary. That process variance is recorded rather than rewritten as intended
execution. Traceability is recovered through the immutable original design at
`27b95e739f78cad6fa609cee7b1359897ccf40ae`, the Phase 0 disposition, the
finding-by-finding implementation evidence, focused regression files, and the
C1/C2/C3 split. Future work should return to smaller boundary commits and live
forward-state updates.

## Closeout Outcome

The completion rule is satisfied at C3 plus this record seal: the final tested
architecture SHA, Windows and WSL results, and exact-byte acceptance are written
into the implementation evidence, while the record candidate remains subject
to the installed frozen-index hook. External acceptance stays with its named
owners. Publication debt is reported separately; no authority to push is
inferred.
