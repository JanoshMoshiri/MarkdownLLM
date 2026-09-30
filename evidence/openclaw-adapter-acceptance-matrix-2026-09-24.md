---
id: openclaw-adapter-acceptance-matrix-2026-09-24
type: artifact
status: stable
created: 2026-09-24
origin: synthesised
confidence: high
tags: [openclaw, adapter, acceptance, evidence, lifecycle, public-release]
linked_things:
  - id: openclaw-adapter
    relation: validates
    notes: "Requirement-to-evidence carrier for OCA-01 through OCA-11."
  - id: openclaw-adapter-seam-analysis-2026-09-24
    relation: extends
    notes: "Moves the selected seam from source evidence into executable acceptance."
  - id: standing-watch-specification
    relation: implements
    notes: "Records exact-session wake and self-healing turn evidence."
---

# OpenClaw Adapter Acceptance Matrix - 2026-09-24

## Verdict

**ACCEPTED FOR PUBLIC RELEASE.**

The lifecycle, domain-admission, domain-selection and watch-recovery slices have
executable evidence. The current package completed a managed clean-profile
installation on Windows, and the operator accepted the live adaptive workflow
as finished, tested and working well on 2026-09-30. Public compatibility remains
bounded to OpenClaw 2026.9.3.

Snapshot:

- MarkdownLLM implementation chain: `a2401a5`, `283e908`, `61315c9`,
  `a86e328`, `fdf4a25`, `a310573`, plus the release-hardening changes carried
  with this artifact, domain-routing commit `96da9d7`, and fixes through
  `038d084`.
- OpenClaw compatibility target: 2026.9.3 only.
- Platform executed here: Windows.
- Downstream-product evidence: none, by design.

## Mechanical run

- Focused Python adapter/lifecycle/clone-depth suite: 41 passed.
- `npm test` in `integrations/openclaw`: 32 passed.
- `npm pack --dry-run --json`: prepack passed; 21 public files; no tests,
  fixtures, source TypeScript or private paths in the tarball.
- The current 0.1.0 build passed `npm run test:install` in a disposable
  OpenClaw 2026.9.3 profile on Windows.
- The full floor suite was attempted on this node but could not produce a valid
  repository-wide verdict: Git 2.16.1 lacks fixture commands including
  `git init -b`. Representative setup and ordinary failures reproduced on an
  untouched 3.44.0 worktree, so they are not attributed to this release delta.
- `git diff --check`: clean.

## Requirement matrix

| ID | Deterministic status | Evidence | Remaining evidence |
|---|---|---|---|
| OCA-01 | pass | Admission tests cover valid fixture entry, declared and ancestor roots, missing entry/sentinel, absolute-root refusal and framework identity emission. | Live wrong-workspace refusal. |
| OCA-02 | pass | Runner tests pin admission-before-execution and neutral ordering; plugin invocation names only framework-owned `harness-event`. | Live command observation. |
| OCA-03 | pass | Core and registration tests cover once-per-fingerprint gating, isolation, failure release and compaction invalidation. | Live restart and reset. |
| OCA-04 | pass | Tests cover additive context, output bounds, structural retention and integrity-marked framework output; system-prompt replacement is forbidden. | Live prompt observation. |
| OCA-05 | pass | State is process-local and bounded. Fitness tests forbid session patching, entry creation, transcript access and private Gateway calls; clean-profile uninstall passed. | Live continuity. |
| OCA-06 | pass | Tests cover subprocess failure, empty output, timeout-class handling, failed advisory envelopes and hash-bound attestation. | Live missing-command and stopped-gateway observations. |
| OCA-07 | pass | Exit 0/1/2/3, exact key, ambiguous wake stop and Git-backed unpublished/diverged recovery pass. Recovery reaches the responsible session; HEAD remains unresolved by the adapter. | Live exact-session wake. |
| OCA-08 | pass | Tests isolate agents/sessions and reject cross-agent keys; recovery targets one exact session. | Operator-accepted live adaptive run. |
| OCA-09 | pass | Strict manifest, public SDK imports, bounded compatibility, build, prepack, package-content, security/removal docs, licence, contribution, and current-build clean-profile installation pass. | Public Windows and Ubuntu CI remain the post-publication portability monitor. |
| OCA-10 | pass | Public fixtures and temporary Git remotes supply all data; no downstream-product dependency exists. | None. |
| OCA-11 | pass | Owner-gated command tests cover explicit route status, unbound refusal, domain listing, agent/workspace admission, existing-topic reuse, topic creation, config persistence and rollback without changing the current workspace. | Operator-accepted live adaptive run. |

## Fitness boundary

The source-level fitness test enforces:

- only `openclaw/plugin-sdk/plugin-entry` and
  `openclaw/plugin-sdk/telegram-account` are imported from OpenClaw;
- no private distribution, repository-source or trusted-only Gateway seam;
- no direct OpenClaw session/transcript mutation;
- one lifecycle invocation owner, `core.ts`;
- no filesystem, YAML, frontmatter or workflow-state interpretation in the
  standing-watch bridge.

## Open rows

1. Observe the public Windows and Ubuntu CI matrix after publication.
2. Route any defect through a patch release and rerun deterministic and
   clean-profile gates.
3. Retest before widening the OpenClaw 2026.9.3 compatibility range.

## Acceptance boundary

The bounded adapter contract is accepted for public release. Publication is a
separate deliberate act governed by the root repository's fail-closed release
policy.
