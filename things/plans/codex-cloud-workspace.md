---
id: codex-cloud-workspace
type: plan
status: in-progress
version: 1.1
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
- Version 2 estate manifest assembles separately versioned reference domains,
  writable domains and ordinary code repositories around the host checkout.
  The framework excludes code Markdown from its corpus. Each extra repository
  has a declared GitHub URL, branch or commit, access intention, credential
  variable and publication policy. Existing version 1 bundles still read.
- Exact-repository credential helper takes a persistent environment variable
  name, never a token value in the manifest or Git config. Agent-time remote
  reads can be probed; setup-only secrets are not treated as agent credentials.
  Optional private boundary terms are installed only into ignored domain files.
- The primary clone's `mdllm.sync=observe` preserves Codex's selected HEAD;
  `mdllm.publication=pr` uses its host PR path. Secondary manual publication
  is distinct; `declared` defers to the owning domain's literal autopush rule.
  `cloud start` syncs before delivering the chosen domain's contract; `cloud
  status` reports local drafts, history and cached publication comparisons.
- A cloud diagnostic found that host checkout access did not become ordinary
  shell Git authentication for two private remotes. The fixture and claim
  boundary are recorded in `evidence/codex-cloud-git-boundary-2026-09-27.md`.

The implementation and user-facing instructions are in
`adapters/codex-cloud.md`. No VM, environment settings or GitHub repository has
been changed by the build. Public framework publication remains a separate
release event under the root's `autopush: false` policy.

## Remaining acceptance

- [ ] Authorised framework release: reconcile/version/changelog/publish, then
  regenerate a deployable bundle at the published commit.
- [ ] Adopt the generated files in the selected primary repository and publish
  them under that repository's policy; inspect its lifecycle adapter currency
  independently. Choose secondary repository roles and credentials explicitly.
- [ ] Configure the actual cloud environment and observe a fresh task plus a
  cache resume. Record setup execution, working-agent Tier-0 receipt, Git hook
  enforcement, project trust and lifecycle execution as separate facts.

The route is built and fixture-tested, not yet a live cloud compatibility claim.
