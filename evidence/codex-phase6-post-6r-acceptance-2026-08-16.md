---
id: codex-phase6-post-6r-acceptance-2026-08-16
type: artifact
status: stable
created: 2026-08-16
tags: [codex, codex-cli, windows, phase-6, execution-evidence, git-floor]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Post-Gate-6R automatic Codex evidence at the framework root, a directly opened nested domain, and a disposable no-adapter domain."
  - id: codex-cli-live-dispatch-2026-08-14
    relation: extends
    notes: "Re-establishes the earlier CLI evidence against the corrected Gate-6R definition hashes and adds the nested and adapter-optionality legs."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Acceptance asserts emitted orientation, validation outcomes, hash-bound evidence and Git-floor consequences rather than hook completion alone."
---

# Codex Phase 6 acceptance after Gate 6R — 2026-08-16

**Verified on the named Windows Codex CLI surface.** These records were
created by real Codex project-hook dispatch. Neither `session-start` nor
`harness-event` was invoked manually in the root or nested adapter runs.

## Tested surface

| Fact | Framework root | Directly opened nested architecture domain |
|---|---|---|
| Harness | Codex CLI 0.147.0 | Codex CLI 0.147.0 |
| Platform | Windows 11 Pro 10.0.26200 | same host |
| Repository HEAD before probe | `d14abc8dece1c5d7dca25ec11473f75092792a1e` | `768bc546c17314ef7f2d5b9a5c504202151f0184` |
| `.codex/hooks.json` SHA-256 | `433db4b323ce91642d5d5c2c1daa2484c6eab0aff388f5970aea0567383e604f` | `1afbb8915b35fff493d48d2fa1746c7cbccca4b4d9e2747b3839f017aa10be50` |
| SessionStart definition | `sha256:f2b78cb9f51a98f3fdaaf4917c9576ddcc501eaef037c6b5e53a1f4cfbe11e76` | `sha256:e42011cbd47953025fd9f7c3d830c61f2d25e46f7a8b4123030245e8bc2aea10` |
| PostToolUse definition | `sha256:e95a4046a29adcadac24f8236ff8d3ca228df6b56e07918c45104c6ce20cdb2a` | `sha256:e90fab4f7adb04a9b463bc48ce45c1b13b154ffceaac1c270ffe86c4c566a86e` |

The operator used the ordinary CLI review flow. In the nested workspace the
first process was used only to review and trust the two definitions. It did
not create a startup attestation; a fresh process was then opened, proving
that trust taking effect and lifecycle dispatch were separate events.

## Automatic SessionStart consequence

The framework-root transcript
`01a00a56-a620-7701-a1a8-f7e29d4c1acb` (local JSONL SHA-256
`8a8eb9d43871ea1978d96928f082a9971ba77a41b0ac3bf1d72ec063a553783b`)
received the automatic bounded lifecycle block before the first agent action.
It contained both step results and the load-bearing orientation sections:
estate state, framework version, velocity, open loops and triggers. The
contemporaneous attestation recorded `estate-sync=0, session-start=0`, outcome
`passed`, source `codex-project-hook`, and `definition_current=true`.

The directly opened nested workspace repeated that consequence in transcript
`01a00a5c-cff8-74e3-85b4-d96a7d1c43a0` (SHA-256
`efcbf84dc30a2ebec68936df7f69ae70156e810b115859c488a7a1a09e7f2557`).
Its orientation contained domain version, velocity, open work and triggers;
doctor resolved the framework `.venv`, reported both lifecycle definitions
current, and the real nested `git hook run pre-commit` returned zero.

Later automatic launches during the PostToolUse probes refreshed the same
definition-current SessionStart evidence at
`2026-08-16T11:46:00.286416+00:00` (root) and
`2026-08-16T11:42:03.995350+00:00` (nested). This proves generic
SessionStart dispatch. The attestation schema does not carry the normalized
`startup|resume|clear|compact` source, so this record deliberately does not
promote those four sources individually.

## Automatic PostToolUse consequence

Each workspace used `apply_patch` to create one temporary frontmatter thing
without `created`. The real PostToolUse result was advisory and non-blocking:

```text
[steps: validate=1]
[validate: exit 1]
missing required field `created`
```

Adding `created: 2026-08-16` automatically produced `validate=0`; deleting
the probe automatically produced another clean pass. The final attestations
record outcome `passed`, detail `validate=0`, the definition hashes above,
and `definition_current=true`. Both repositories then had clean worktrees.

The nested PostToolUse transcript is
`01a00a60-d0fa-7ba1-a659-20fc7daa5acb` (SHA-256
`1f0d60cb813f1e7ce47548c990b45f562cec072373d5ef30eb9a496b4a777f46`);
the root transcript is `01a00a63-83c8-7741-b35a-31979025686e`
(SHA-256
`74e43280b81af58a78d5522c6b987072efe4713bdf156c6b4f95f3492e306865`).
The repaired attestations were observed at
`2026-08-16T11:43:19.367043+00:00` and
`2026-08-16T11:47:32.762669+00:00`, respectively.

## Adapter optionality — Codex

An out-of-estate disposable domain was scaffolded with `--harness none`.
`.codex`, `.claude`, and `.git/mdllm-harness-attest` were all absent. In the
read-only Codex session `01a00a68-231b-7500-87a3-f4803f03271c` (JSONL
SHA-256
`38c4ac0483266e7dd255abc87a76caef222cc8e7620cb6f7521f05bf12206282`),
AGENTS interpretation still supplied the domain identity and prescribed
startup/commit contract; no lifecycle output was injected or inferred.

Following that portable contract, `mdllm session-start` established the
strict session-gate attestation. A valid synthetic thing then committed
through the installed Git hook at
`53acdf2a8e3313e107dea252bb363fa288d2fc83`. A second synthetic thing omitted
`created`; the real commit returned `1` and named that exact error. The
fixture was outside the estate and was deleted after capture.

This proves the intended degradation model for Codex: removing the project
adapter removes automatic lifecycle hardening, but AGENTS interpretation and
the Git validation floor remain sufficient. The equivalent disposable Claude
Code run remains independently Claude-owned.

## Scope and failures

- The complete suite passed **465 tests** with its basetemp outside the
  framework repository. A first run placed basetemp under the repository and
  produced 463 passes plus two expected-environment failures: fixtures named
  as non-repositories inherited the parent `.git` floor. Re-running them in
  the acceptance environment removed both failures; no production change was
  made to disguise the fixture-location error.
- Codex Desktop build `26.803.10989.0` remains a separately recorded negative
  task-start surface; this record does not generalize CLI behavior to Desktop.
- The first nested CLI process correctly produced no startup proof while hook
  trust was still being decided. Evidence begins only with the fresh trusted
  process.
- The lifecycle record is generic SessionStart evidence because source
  normalization is absent. `clear` and `compact` are not claimed.
- This verifies Windows CLI root, nested-workspace and Codex no-adapter
  behavior. It does not claim Codex on POSIX or macOS, Claude's disposable
  proof, GitHub Copilot lifecycle behavior, or any untested harness.
