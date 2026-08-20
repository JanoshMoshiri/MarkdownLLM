---
id: cowork-adapter
type: plan
status: in-progress
version: 1.6
created: 2026-08-18
priority: high
tags: [harness, adapters, cowork, bootstrap, discovery, contract-emission, publication, estate, clean-architecture]
linked_things:
  - id: cowork-remote-phase5-evidence-2026-08-19
    relation: references
    notes: "Remote leg graded PARTIAL: transport controls passed; fresh receipt, stale-bundle and behavioral claims remain bounded."
  - id: harness-capability-evidence-matrix-2026-08-20
    relation: references
    notes: "Exact observed build/evidence boundary across all three registered adapters."
  - id: vendor-harness-adapter-foundation
    relation: extends
    notes: "Exercises the third-adapter rule with a run-time-bound bundle rather than another project artifact."
  - id: cowork-integrity-estate-sweep
    relation: extends
    notes: "Promotes the earlier plugin assembly layer into a framework-owned adapter while the Git floor remains the fail-safe."
  - id: framework-discovery-specification
    relation: extends
    notes: "Adds explicit bootstrap/emission for a harness with no project entry-file discovery."
  - id: agents-md-discovery-is-harness-dependent
    relation: implements
  - id: hook-enforcement-has-three-anchors
    relation: implements
  - id: portability-claims-need-execution-tests
    relation: implements
  - id: a-consuming-environments-gate-is-a-build-time-constraint
    relation: implements
    notes: "Installer limits and executable line endings are producer-side build refusals."
  - id: a-controls-guarantee-can-rest-on-a-coincidence-of-its-birth-environment
    relation: implements
    notes: "Receipt evidence is definition-bound instead of inheriting trust from the environment that created it."
  - id: the-estates-second-clone-is-an-independent-witness
    relation: references
    notes: "The remote packet's published commit chain was corroborated from a second clone."
---

# Cowork Adapter

## Current purpose

The run-time-bound adapter and its remote assembly path exist. This plan stays
open for a real local-transport run, the controlled stale-bundle branch, fresh
acceptance of the hardened Tier-0 receipt, and the operator's rollout/release
decision. The former 536-line build diary is preserved in Git:

`git show 27b95e7:things/plans/cowork-adapter.md`.

The forward evidence boundary is
[`harness-capability-evidence-matrix-2026-08-20`](../../evidence/harness-capability-evidence-matrix-2026-08-20.md).

## Settled design

- Cowork is a registered **estate-level, run-time-bound** adapter. It renders
  an account-level bundle and no project configuration.
- The bundle is a thin discovery/transport projection: credential intake,
  framework clone, dependency probe, mechanism-currency check, then handoff to
  the harness-neutral floor.
- `mdllm assemble` owns domain cloning/reuse, real-default-branch resolution,
  identity, hook installation, credential leak checks, ordered sync and
  session-start emission. `mdllm publish` owns guarded publication.
- Mechanism templates are public; rendered estate config is private,
  gitignored output derived from local remotes and Git identity.
- Consumer constraints are producer build refusals: LF-only shell bytes and
  Cowork's description-length limit are tested before a bundle can render.
- Installation is not activation. Registration/build tests cannot earn a
  compatibility row; only a live transport packet can.
- Emission can make compliance possible, not guaranteed. Public wording must
  not turn a contract delivery record into a claim about agent behavior.

## Completed implementation

| Phase | State | Durable result |
|---|---|---|
| 0 — port fit | complete | Cowork registry entry, honest capabilities, run-time diagnostic shape and architecture fitness coverage |
| 1 — contract emission | complete in code | Floor-owned Tier-0 emission, receipt artifact and attestation path; current semantics require fresh live acceptance |
| 2 — publication | complete | Real branch is read, wrong/detached/missing/diverged cases refuse, plain ff-only push is verified, token is command-scoped |
| 3 — bundle projection | complete | Derived bundle/config, mechanism hash, stale warning path, render-time install constraints and neutral assembly service |
| 3 follow-on — repository reuse | complete in code (2026-08-20) | Assembly consumes the shared token-aware `sync_repo`; clean clones ff-only, dirty/diverged/in-operation states are reported and untouched; public Git credential ports replace private cross-module imports |

Focused transaction/assembly/publication verification at the follow-on
boundary: **47 passed** using an external basetemp. This is deterministic
implementation evidence, not a Cowork product event.

## Remote evidence disposition

The committed remote packet is **PARTIAL**, not failed and not accepted. It
establishes explicit skill activation, assembly, floor blocks, real guarded
publication (including refusal under unplanned divergence), zero publication
debt, no persisted credential, and the current mechanism-hash branch. It also
found the boundaries that must remain visible:

- contract output was preview-truncated and manually recovered;
- the then-current marker/gate semantics did not prove receipt;
- emission did not itself produce contract-compliant behavior;
- the deliberately stale bundle was not run;
- the Cowork client build was not observable.

Later code can close a defect, but it cannot rewrite this historical packet or
accept itself. The retests below are therefore still owed.

## Phase 4 — local transport

- [ ] Define explicit/local-estate selection without cloning or a PAT. Use
  ambient credentials and the same floor services; do not duplicate the
  remote path in another script.
- [ ] Emit the same contract, lifecycle and handoff, with one honest transport
  line and no remote-mode `AUTH-FAILED` residue.
- [ ] Run one real local Cowork session on a real domain and capture the packet
  below.

## Phase 5 — live acceptance

- [x] Preserve and grade the remote packet with first-hand/relayed provenance,
  exact observable versions, commit chain, mechanism hash and explicit limits.
- [ ] Re-run remote Tier-0 receipt after the current session-start hardening;
  the agent must not recover omitted content manually.
- [ ] Install a known-older bundle in a fresh Cowork session and observe the
  `STALE` branch. A matching-bundle run cannot prove this retrospectively.
- [ ] Record the local-transport packet to the same standard: activation,
  contract before first write, attestation, default branch, floor consequence,
  real commit/publication or ambient-autopush result, debt and credential
  residue.
- [ ] Record the Cowork client build if observable; otherwise keep `unknown`.

Each packet receives `pass` / `partial` / `fail` requirement by requirement.
Unavailable evidence is `NOT TESTED`, never reconstructed.

## Phase 6 — specifications and public surfaces

- [x] Framework discovery names explicit bootstrap/emission as a first-class
  route and keeps it separate from project entry discovery.
- [x] Current public docs describe Cowork as registered/run-time-bound and
  explicitly withhold a compatibility row while live gates remain open.
- [ ] After both transports pass, update the compatibility matrix no wider
  than their exact surfaces/builds; retain the behavioral claim boundary.
- [ ] Disposition the standing discovery/control insights from the accepted
  evidence and complete the change-reconciliation dark-region walk.

## Phase 7 — rollout and release (operator-owned)

- [ ] Build from the live estate, review the private derived config, install
  the accepted bundle and retire the superseded account-level plugin.
- [ ] Keep PAT paste/revoke as an explicit operator ritual until the platform
  supplies credential brokering.
- [ ] Let regulated domains decide their own additional session discipline.
- [ ] Version, changelog and deliberately publish the release surface.

## Completion criteria

- The third harness stays an adapter plus ports/tests/docs, not a conditional
  in neutral services.
- Existing clean clones fast-forward; unresolved Git state is never merged,
  reset or discarded by assembly.
- Remote and local transports both have graded live evidence, including the
  stale-bundle and current Tier-0 receipt paths.
- The public claim is exactly as broad as those packets and no broader.

## Outside this plan

- Cowork credential brokering and a PostToolUse-equivalent product event.
- Making the bundle a second specification source.
- Automatic conflict/divergence resolution or unattended account-level
  installation.
