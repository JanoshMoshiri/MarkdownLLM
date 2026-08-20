---
id: harness-capability-evidence-matrix-2026-08-20
type: artifact
status: evolving
version: 1.0
created: 2026-08-20
tags: [internal, harness, adapters, capability-matrix, execution-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Forward-readable evidence boundary for the Claude Code and Codex adapter plan."
  - id: cowork-adapter
    relation: documents
    notes: "Records the remote PARTIAL result and the local/stale-bundle evidence still owed."
  - id: session-start-hardening
    relation: references
    notes: "The live records predate the current Tier-0 receipt and contract-fingerprint hardening, so they cannot accept that newer implementation."
  - id: claude-gate-6r-acceptance-2026-08-16
    relation: derived-from
  - id: claude-phase6-no-adapter-and-root-2026-08-16
    relation: derived-from
  - id: claude-no-adapter-entry-probe-2026-08-17
    relation: derived-from
  - id: codex-phase6-post-6r-acceptance-2026-08-16
    relation: derived-from
  - id: codex-desktop-session-start-negative-2026-08-14
    relation: derived-from
  - id: cowork-remote-phase5-evidence-2026-08-19
    relation: derived-from
---

# Harness Capability and Evidence Matrix — 2026-08-20

This is an internal routing view over committed evidence, not a new execution
record and not a compatibility claim. It separates product surface and build
because a successful CLI run is not evidence for a desktop build, and it says
`unknown` where the harness did not expose a version. The linked records remain
the evidence of record.

## Evidence-backed surfaces

| Harness surface | Exact observed build | What first-hand evidence establishes | Boundary and grade | Evidence of record |
|---|---|---|---|---|
| Claude Code project-bound adapter | CLI **2.1.229**, Windows 11 Pro 10.0.26200 | Automatic `SessionStart` on a framework root and a large nested domain; root `startup` and `resume`; automatic advisory PostToolUse validation; current-definition attestations; Git floor independent of the adapter | **Verified on the named Windows CLI surfaces.** `clear`/`compact`, macOS, POSIX and Copilot are not established | [Gate 6R](claude-gate-6r-acceptance-2026-08-16.md), [root and no-adapter record](claude-phase6-no-adapter-and-root-2026-08-16.md) |
| Claude Code without an adapter | CLI **2.1.233** headless `-p`, Windows 11 Pro 10.0.26200 | Differential entry proof: core `CLAUDE.md` pointer present → `AGENTS.md` in context; pointer absent → no project entry. Manual contract ritual plus strict session gate and Git floor completed the portable path | **Verified for the exact headless CLI probe.** It is memory injection, not lifecycle-hook execution | [No-adapter differential](claude-no-adapter-entry-probe-2026-08-17.md) |
| Codex project-bound adapter | CLI **0.147.0**, Windows 11 Pro 10.0.26200 | Real project-hook dispatch at framework root and directly opened nested domain; bounded SessionStart content; advisory invalid/repair PostToolUse consequences; hash-bound evidence; no-adapter degradation through AGENTS + Git floor | **Verified on the named Windows CLI surfaces.** Source normalization, POSIX/macOS, `clear` and `compact` are not established | [Post-6R acceptance](codex-phase6-post-6r-acceptance-2026-08-16.md), [earlier live dispatch](codex-cli-live-dispatch-2026-08-14.md) |
| Codex Desktop task start | package **26.803.10989.0**, Windows | Workspace `AGENTS.md` arrived and the Git floor remained active, but no project SessionStart output or Codex execution attestation appeared | **Negative for automatic SessionStart on this exact build/task surface.** No wider Desktop claim | [Desktop negative record](codex-desktop-session-start-negative-2026-08-14.md) |
| Cowork remote ephemeral VM | Cowork client build **unknown / not observable**; `markdownllm-bootstrap` **v3.31.0**; framework **v3.32.0** at `eda847c4f30b89e9c04ea208aa3b76a0ee5c85b9`; mechanism `c060e2b55bb6414cfaeed1f63e7b866b8a48faf51d3cf064e735e65286dde1f5` | Explicit skill activation, clone/assembly, real floor blocks, guarded publication and debt clearing, token non-persistence, current mechanism-hash path | **PARTIAL.** Contract receipt was manually recovered after preview truncation; old gate semantics were hollow; stale-bundle branch and harness-session hook execution were not tested | [Remote Phase 5 evidence](cowork-remote-phase5-evidence-2026-08-19.md) |
| Cowork local transport | No build observed | No live local-session packet exists | **NOT TESTED** | Owed by `cowork-adapter` |

## Shared lifecycle-result vocabulary

Every lifecycle dimension below uses the same evidence states: **observed**
(the linked record directly establishes it), **negative-observed** (the record
looked and did not see it), **not-tested**, **not-applicable**, or **unknown**
(the surface was exercised but the evidence cannot decide). Contract delivery
adds only the observed form, `whole`, `deferred`, or `partial/manual`; it never
promotes emission into receipt. “Output received” means a harness-owned record
shows model-visible output; it does not mean the model read or applied it.

| Surface/build | Dispatched | Executed | Output received | Contract whole/deferred | Floor active | Write feedback available | Publication authority |
|---|---|---|---|---|---|---|---|
| Claude Code CLI 2.1.229 | observed | observed | observed | not-tested for the current fingerprint/receipt definition | observed | observed | not-tested |
| Claude Code CLI 2.1.233, no adapter | not-applicable (manual route) | observed manual ritual | observed | not-tested for the current fingerprint/receipt definition | observed | not-applicable | not-tested |
| Codex CLI 0.147.0 | observed | observed | observed | not-tested for the current fingerprint/receipt definition | observed | observed | not-tested |
| Codex Desktop 26.803.10989.0 | negative-observed | negative-observed | negative-observed | not-tested | observed | not-tested | not-tested |
| Cowork remote, client build unknown; bootstrap 3.31.0 | observed bootstrap | observed bootstrap | partial/manual | partial/manual; current definition not-tested | observed | not-applicable | observed guarded command scope |
| Cowork local, build unknown | not-tested | not-tested | not-tested | not-tested | not-tested | not-tested | not-tested |

These seven columns are deliberately independent. In particular, an adapter
configuration can make dispatch available without proving execution; execution
can emit output without proving receipt; receipt cannot prove reading or
adherence; and an active commit floor says nothing about push authority.

## Capability boundary

| Capability | Claude Code | Codex | Cowork |
|---|---|---|---|
| Core entry without optional lifecycle adapter | Verified through the Claude pointer on CLI 2.1.233 | Verified through native AGENTS interpretation on CLI 0.147.0 | Explicit bootstrap skill is the discovery route; activation was explicit in the one remote record |
| Optional session-start hardening | Verified on Claude Code CLI 2.1.229 | Verified on Codex CLI 0.147.0; negative on Desktop 26.803.10989.0 | Bootstrap ran the lifecycle, but current receipt semantics have no fresh live acceptance |
| Advisory post-write feedback | Verified on Claude Code CLI 2.1.229 | Verified on Codex CLI 0.147.0 | No equivalent harness event established |
| Git pre-commit enforcement | Verified independently of adapters | Verified independently of adapters | Verified in the remote VM |
| Guarded publication | Floor capability; not accepted by these Claude records | Floor capability; QMS transport corroborated separately, not a universal Codex property | Verified in the remote VM, including refusal under real divergence |
| Current adapter definition on 2026-08-20 working tree | Deterministic tests required; no fresh live run recorded here | Deterministic tests required; no fresh live run recorded here | Deterministic tests required; remote record predates current sync/receipt hardening |

## Acceptance still owed

- Re-run the Tier-0 receipt probe on at least one Claude and one Codex surface
  after the current session-attestation changes. Historical live evidence does
  not accept changed definitions.
- Run one real Cowork local session using the same evidence packet as the
  remote leg.
- Install a deliberately stale Cowork bundle and observe its warning in a
  fresh session.
- Record a Cowork client build only if the product exposes one; never infer it
  from the plugin or framework version.

No other domain needs to rest on this derived operator view, so it is not an
exposed cross-domain fact. The source evidence is committed and stable; Git
history preserves every superseded plan narrative this matrix makes easier to
navigate.
