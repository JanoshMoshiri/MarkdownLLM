---
id: explorer-publication-readiness
type: plan
status: blocked
version: 1.1
created: 2026-08-27
priority: high
tags: [explorer, release, publication, windows, review, cleanup, uat]
linked_things:
  - id: explorer-publication-position
    relation: derived-from
  - id: markdownllm-explorer-comprehensive-review-2026-08-27
    relation: references
  - id: markdownllm-explorer-windows-distribution
    relation: references
  - id: markdownllm-explorer-comprehensive-review-remediation-2026-08-27
    relation: references
---

# Explorer publication readiness

This plan is the single carrier for publishing the current in-repository
Windows preview. It closes only when the reviewed release candidate, its
installer and the public claims all describe the same state.

## Current position

- [x] Standalone read-only Explorer implemented using Clean Architecture
  boundaries.
- [x] Native per-user Windows installer, shortcuts and tray lifecycle built.
- [x] Public installation and user guides use a generated fictional estate.
- [x] The stale evidence-seal blocker from the comprehensive review was
  corrected and the full technical trace was resealed on the corrected tree.
- [x] Operator acceptance is recorded; the installation and user guides are
  reconciled to the accepted product and current publication claim.
- [x] Operator performs and records the human-owned UAT dispositions: 30
  accepted and zero pending.
- [x] Correct or explicitly disposition the active upgrade/uninstall shutdown
  race identified by the comprehensive review.
- [x] Expand the retained adapter-swap evidence to all four declared ports, or
  narrow the requirement with explicit authority.
- [x] Reconcile the remaining non-blocking review findings selected for this
  release.
- [x] Before repository publication, resolve the two current baseline floor
  regression failures: the scaffold test's stale 12-item expectation after a
  ninth prompt was added, and the assemble test's environment-sensitive
  substring check against global Git configuration.
- [x] Run the documented release clean-up and prove ignored construction
  output is absent from the tracked release surface.
- [x] Rebuild the unsigned candidate from the final source, record its hash and
  retain it only as a local signing input.
- [x] Implement a fail-closed signed build for the frozen application,
  generated uninstaller and setup.
- [ ] Supply authorised Authenticode signing credentials and an HTTPS RFC 3161
  timestamp service, then build the signed release installer.
- [ ] Execute active install, upgrade and uninstall against the signed release
  bytes, reseal the seven dependent technical requirements and record the final
  signed hash.
- [ ] At the final signed release boundary, generate the complete changelog
  from the unpushed commit range and make the framework version decision.
- [x] Preserve push and publication as a separate explicit operator act; no
  publication was performed in this session.

## Release claim

The truthful claim is **operator-accepted Windows preview candidate;
publication blocked on signing and signed-byte native verification**. The
source, reproducible packaging recipe and signing hooks are tracked. The
unsigned build is not a release asset.

## Done when

The final candidate passes framework and Explorer validation, all technical
blockers and human UAT items have explicit dispositions, the clean-up check is
complete, and the signed installer distributed to users is byte-identical to
the installer that completed the native lifecycle verification.

## Blocker evidence

The current subject is
`sha256:faab2f2cd91daea6dd0d39e358d506795d8e085a69cda7e6a1021820b74628ad`.
The unsigned setup candidate is 10,509,386 bytes with SHA-256
`a963d146e40e9813c522b2f87bb67dde4e48a3aa14f3d5a3516b3dd27ddf4c27`.
Windows Code Integrity event 3077 blocked the generated unsigned uninstaller
under policy `0283ac0f-fff1-49ae-ada1-8a933130cad6`; the operator's installed
Explorer was deliberately left untouched. Full detail is retained in the
review-remediation artifact and `windows-publication-gate.json`.
