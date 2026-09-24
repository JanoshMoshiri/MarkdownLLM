---
id: codex-cloud-workspace
type: plan
status: in-progress
version: 1.0
created: 2026-09-24
priority: high
tags: [adapters, bootstrap, cloud, publication]
linked_things:
  - id: cowork-adapter
    relation: references
  - id: framework-discovery-specification
    relation: implements
  - id: git-workflow-specification
    relation: implements
  - id: interface-specification
    relation: implements
---

# Codex Cloud workspace

The operator approved building a reusable cloud bootstrap and conversational
configuration route on 2026-09-24, after reviewing the distinction between
Codex Cloud settings and the separate Agents API. The runtime must accept the
domain checkout the host already owns and materialise the public substrate
around it. Exposure: no; this is framework implementation state, not a fact
another domain needs to import.

## Built

- Adapter-owned files/settings through a neutral CloudWorkspacePort and
  `mdllm cloud configure/check/prepare`; Codex lifecycle binding remains separate.
- Strict JSON manifest; exact public-framework pin; temporary clone with
  isolation/collision checks; pinned private runtime; fresh/cached preparation.
- Shared Git-floor installation and domain validation; the session gate remains
  deferred until the working agent actually emits its contract. Setup writes
  no attestation and never substitutes log output for model receipt.
- Clone-local PR publication restraint; it can only reduce standing authority,
  never enable a send or rewrite the domain's AGENTS.md.
- A discoverable `configure-codex-cloud` skill, generated settings guide and
  a private preview path for reviewing an unpublished build.
- Linux fixtures exercise the real shell bootstrap, Git floor, fresh setup,
  cached maintenance, selected-HEAD/index preservation and strict session gate.

The implementation and user-facing instructions are in
`adapters/codex-cloud.md`. No VM, environment settings or GitHub repository has
been changed by the build. Public framework publication remains a separate
release event under the root's `autopush: false` policy.

## Remaining acceptance

- [ ] Authorised framework release: reconcile/version/changelog/publish, then
  regenerate a deployable bundle at the published commit.
- [ ] Adopt the generated files in the selected domain and publish them under
  that domain's policy; inspect its lifecycle adapter currency independently.
- [ ] Configure the actual cloud environment and observe a fresh task plus a
  cache resume. Record setup execution, working-agent Tier-0 receipt, Git hook
  enforcement, project trust and lifecycle execution as separate facts.

The route is built and fixture-tested, not yet a live cloud compatibility claim.
