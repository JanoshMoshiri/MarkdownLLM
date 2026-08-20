---
id: substrate-review-phase0-disposition-2026-08-20
type: artifact
status: stable
version: 1.0
created: 2026-08-20
origin: synthesised
exposed: false
tags: [review-response, phase-0, baseline, disposition, transaction-integrity]
linked_things:
  - id: independent-substrate-review-2026-08-20-codex
    relation: derived-from
  - id: codex-substrate-review-response-2026-08-20
    relation: documents
---

# Substrate Review Response — Phase 0 Disposition

## Pinned Baseline

The response programme began from local commit
`27b95e739f78cad6fa609cee7b1359897ccf40ae` on `main`, the commit that sealed
the immutable Codex review and its remediation design. The tree and index were
clean at that meaning boundary. The framework public remote was not pushed.

Execution environment at capture:

- Windows 11 build 26200, x64
- CPython 3.12.13 from the repository `.venv`
- PyYAML 6.0.3
- pytest 9.1.1
- framework version 3.32.0

The review's reconciled baseline accounted for 526 passing tests: 523 in the
full run and three Git-boundary fixtures that failed only because the runner's
temporary directory was beneath the real framework repository, then passed in
a true external temporary root. Framework validation covered 232 things with
0 Errors, 0 Warnings, and 1 Info; examples, coherence, relationships, and
provenance were clean/in sync. This artifact preserves that distinction rather
than retroactively calling the first run wholly green.

## Finding Disposition And Owner

| Review finding | Disposition at Phase 0 | Evidence/reproduction | Mechanical owner |
|---|---|---|---|
| 1. Pre-commit read worktree, not index | accepted / critical | real-Git mismatch fixtures demonstrate both invalid-staged/repaired-worktree and valid-staged/invalid-worktree directions | `RepositoryView` + validation/coherence hook callers |
| 2. No consistent read snapshot | accepted / high | mutable-path scan was the only model input and no base-HEAD check existed | `RepositoryView` |
| 3. Autopush failed open | accepted / high; operator-approved reversal | absent/malformed policy enabled send in the old service | `RepositoryTransaction`/sync publication policy |
| 4. Scaffold/hook install not transactional | accepted / high | unrelated staged state and foreign-hook overwrite surfaces were reachable | scaffold transaction + resolved hooks directory |
| 5. MCP could stamp adjacent bytes | accepted / high | dirty worktree body could receive a path-derived commit pin | commit-view MCP egress |
| 6. Structural graph lists drifted | accepted / high | validation, indexes, touchpoints, cues, and egress each owned a different list | structural-reference registry |
| 7. Duplicate YAML keys collapsed | accepted / high | duplicate `source_domain` existed in the live corpus and PyYAML retained only the last value | strict YAML boundary |
| 8. Eval could succeed on failed evidence | accepted / high | scan findings, process failure, result identity, and final exit were independently incomplete | eval application boundary |
| 9. Calculation strictness/exactness | accepted / high in strict domains | long YAML decimal passed through binary float; strict non-evaluation remained non-blocking | strict YAML numeric token + calculation validation |
| 10. Workflow edge legality agent-owned | accepted / medium-high | only cursor membership was checked despite machine-readable transition edges | prior/candidate workflow validation |
| 11. Trigger evaluation partial/unsafe | accepted / medium-high | malformed stale threshold raised; absent watch/subtask branches could become quiet/partial success | typed trigger evaluator |
| 12. Session attestation semantics | narrowed / high semantics | emission outcome was recorded, but freshness did not identify the operative contract and could not prove reading/application | existing session gate, content fingerprint, evidence-level vocabulary |
| 13 / New A. Repository-supplied external execution | accepted / critical | automatic import trigger reached `.mcp.json` command/HTTP routes without clone-local hash-bound authority | `ExternalTrustPolicy` |
| 14. Birth defects/overclaims | accepted / medium | evidence template frontmatter/lifecycle, root-relative skill paths, relation vocabulary, and synthetic legal examples reproduced concrete defects | template build validation + example corpus |
| 15. Supply chain | accepted / medium-high | moving-branch bootstrap and mutable dependency/action references survived | installer/bundle/CI trust surfaces |
| New B. Five session assurance states conflated | accepted / high | producer-side receipt facts had no vocabulary boundary preventing promotion to reading/compliance | session evidence matrix |
| New C. Cowork lifecycle name overstated execution | accepted / high | assembler printed estate-sync while fetching and did not fast-forward reused clones | shared sync application service |
| New D. Plans exceeded executable shape | accepted / medium-high | live plans were 2,021, 536, and 303 lines with history mixed into forward state | compact plan residue + stable evidence artifacts |
| New E. Adapter product clarity | accepted / medium | one support word hid discovery/config/lifecycle/floor/write-feedback/live-evidence differences | build-specific harness capability matrix |

No accepted finding was rejected as merely stylistic. The review severities were
not treated as proof: each mechanical item received a regression fixture or a
minimal source-path reproduction, while session/harness claims were narrowed to
the evidence class actually observable.

## Ownership Reconciliation

The umbrella plan owns the three shared ports and integration acceptance.
Subject plans retain their semantic surfaces: `session-start-hardening` owns
contract delivery, `vendor-harness-adapter-foundation` and `cowork-adapter` own
harness-specific acceptance, `evidence-and-eval-backlog` owns the longitudinal
programme, `deterministic-calculation` owns calculation capability, and
`mechanical-coherence-checks-backlog` owns earned template checks. This avoids
closing the same checkbox in two histories.

## Prose-Only Residue To Walk

The deterministic touchpoint set is only the first tier. Significant rule
changes must also reconcile:

- the Tier 2 routing and framework catalog in `AGENTS.md`;
- kernel blocks and their generated `kernel.md` projection;
- the human framework/operator/first-hour/estate maps;
- manifesto claims about determinism, auditability, prompts, universality, and
  reasoning history;
- adapter evidence language that distinguishes designed, rendered, dispatched,
  executed, received, applied, and independently validated;
- templates, examples, installers, CI, and nested-domain birth surfaces.

The final implementation evidence records the completed walk and command
matrix. This Phase 0 record remains the pinned before-state.
