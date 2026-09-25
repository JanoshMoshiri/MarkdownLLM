---
id: openclaw-adapter-acceptance-matrix-2026-09-24
type: artifact
status: evolving
created: 2026-09-24
origin: synthesised
confidence: high
tags: [openclaw, adapter, acceptance, evidence, lifecycle, public-release]
linked_things:
  - id: openclaw-adapter
    relation: validates
    notes: "Requirement-to-evidence carrier for OCA-01 through OCA-10."
  - id: openclaw-adapter-seam-analysis-2026-09-24
    relation: extends
    notes: "Moves the selected seam from source evidence into executable acceptance."
  - id: standing-watch-specification
    relation: implements
    notes: "Records exact-session wake and self-healing turn evidence."
---

# OpenClaw Adapter Acceptance Matrix - 2026-09-24

## Verdict

**IN PROGRESS - deterministic and clean-profile Windows evidence is green;
public acceptance is not yet earned.**

The lifecycle, domain-admission and watch-recovery slices have executable
evidence. Clean-profile OpenClaw installation/removal is now evidenced on
Windows; live session lifecycle, POSIX execution and observed CI remain open.
This artifact must not be read as release approval.

Snapshot:

- MarkdownLLM implementation chain: `a2401a5`, `283e908`, `61315c9`,
  `a86e328`, `fdf4a25`, `a310573`, plus the release-hardening changes carried
  with this artifact.
- OpenClaw compatibility target: 2026.9.3 only.
- Platform executed here: Windows.
- BookRite evidence: none, by design.

## Mechanical run

- `.venv\\Scripts\\python.exe -m pytest
  tools/tests/test_openclaw_adapter.py tools/tests/test_lifecycle_runner.py
  tools/tests/test_watch.py -q`: 80 passed.
- `npm test` in `integrations/openclaw`: 29 passed.
- `npm pack --dry-run --json`: prepack passed; 18 public files; no tests,
  fixtures, source TypeScript or private paths in the tarball.
- `npm run test:install`: passed in a disposable named OpenClaw 2026.9.3
  profile; managed tarball install, explicit conversation-hook consent, five typed
  hooks, config validation, Plugin Doctor, uninstall and cleanup all passed.
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
| OCA-08 | deterministic pass | Tests isolate agents/sessions and reject cross-agent keys; recovery targets one exact session. | Concurrent two-domain live run. |
| OCA-09 | partial | Strict manifest, public SDK import, bounded compatibility, build, prepack, package-content, clean-profile install/uninstall, security/removal docs, licence, contribution and release-candidate metadata pass on Windows. | Observe the configured Windows and Ubuntu CI matrix. |
| OCA-10 | deterministic pass | Public fixtures and temporary Git remotes supply all data; no BookRite dependency exists. | Overall acceptance waits on live and portability rows. |

## Fitness boundary

The source-level fitness test enforces:

- only `openclaw/plugin-sdk/plugin-entry` is imported from OpenClaw;
- no private distribution, repository-source or trusted-only Gateway seam;
- no direct OpenClaw session/transcript mutation;
- one lifecycle invocation owner, `core.ts`;
- no filesystem, YAML, frontmatter or workflow-state interpretation in the
  standing-watch bridge.

## Open rows

1. Observe the configured Windows and Ubuntu CI matrix on the unpublished release candidate.
2. Exercise fresh/continued session, reset, compaction, Gateway/plugin restart,
   two-domain isolation and exact-session wake through the live host.
3. Close any defects surfaced by those live and portable runs, then rerun the
   deterministic and clean-profile gates.
4. Ask for publication authority only after every row above is evidenced.

## Acceptance boundary

The adapter remains unaccepted and unpublished. BookRite cannot begin as the
agentic business operating-model proof until this matrix has no open
requirement row and the operator has made the release decision.
