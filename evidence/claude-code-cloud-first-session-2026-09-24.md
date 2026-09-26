---
id: claude-code-cloud-first-session-2026-09-24
type: artifact
status: stable
created: 2026-09-24
tags: [claude-code, cloud, ephemeral-container, execution-evidence, first-hand, degraded-clone, shallow-clone]
linked_things:
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: supports
    notes: "Second lived instance, second mechanism: the first container could not see its sibling repos; this one could not see its own history."
  - id: operator-seat-and-harness-native-onramp
    relation: informs
    notes: "Phase 3 route evidence for Claude Code: the cloud surface's entry and lifecycle facts, and the clone defects any silent bootstrap must repair."
  - id: lifecycle-output-truncation-2026-08-14
    relation: extends
    notes: "The hook channel still cut the digest mid-line on this surface; the direct channel delivered the kernel whole."
  - id: portability-claims-need-execution-tests
    relation: supports
    notes: "The spec called estate-sync on a fresh cloud clone 'a cheap no-op' by design intent; the first execution disproved it."
---

# Claude Code cloud session — first framework-root session (2026-09-24)

**First-hand.** A Claude Code session on the web (claude.ai/code), in an
ephemeral cloud container, opened on the framework root at
`commit:8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a` on a harness-created branch.
The operator asked for a full session start and a full-corpus read. Everything
below was observed by the session itself; nothing is relayed.

## What the surface delivered

| Fact | Observed |
|---|---|
| Entry | `CLAUDE.md` → `@AGENTS.md` import delivered the body before the first tool call; frontmatter stripped (`an-injected-file-arrives-without-its-frontmatter`). |
| Lifecycle | The checked-in project SessionStart hook fired with no operator setup: harness attestation `estate-sync=0, session-start=0`, `source: claude-code-project-hook`. Also fired on each later turn of the session. |
| Runtime | Python 3.11 with PyYAML 6.0.1 importable; `git` 2.43. |
| Hook channel | The digest arrived cut mid-line in several places (`[truncated]`); the kernel was deferred by design. Re-running `session-start` on the direct channel delivered the kernel whole: 106 lines, sha256 `228bf9b291a1`. |

## What the clone got wrong

| Defect | Consequence as cloned | Repair |
|---|---|---|
| **Shallow**: 50 of 938 commits, boundary 2026-09-09 | `validate`: 145 Errors (framework) + 3 (life-manager example), all "pin resolves to no commit"; 3 false born-verified Warnings at the boundary commit. Velocity `0 · 3 · 21 · 17` against a true `44 · 14 · 21 · 17`; the stall section absent — eleven high-priority stalls hidden. | `git fetch --unshallow` → 0 Errors, 0 Warnings, stalls restored. |
| **No upstream** on the harness branch, although `origin/<same name>` was fetched | `estate-sync`: `no-upstream` — sync inert | `git branch --set-upstream-to` (session); floor now compares with the same-name ref read-only |
| **No git hooks** (never cloned) | doctor: DEGRADED | `mdllm install-hook .` → FLOOR ACTIVE |
| **No `.boundary-terms`** (local-only by design) | The disclosure boundary is a silent no-op for every cloud session on a public repository | **Open** — cannot be repaired from inside the repository |
| **One repository** | No domains present; estate reads (two of four fired triggers) unevaluable here | Out of scope for this surface; `mdllm assemble` is the post-clone path |

Nothing on any surface named the shallow clone. The floor's degraded-environment
rule covered "git cannot be consulted"; this was git consulted and answering
wrongly.

## What changed because of it

`build: a clone that cannot see its history says so — and estate-sync heals it`
(framework, 2026-09-26): `clone_depth` detection; estate-sync completes shallow
history and reads an upstream-less branch against its same-name ref; validate,
doctor and session-start report could-not-look instead of minting findings.
Re-verified on a real depth-50 clone of this repository: 148 Errors → 0 with
honest Warnings; one estate-sync → full history, stalls restored.

## Limits of this record

- One surface (Claude Code on the web), one build, one container image. It
  says nothing about Codex cloud or Cowork remote, whose clones may differ.
- The hook firing on each turn was observed from the injected context, not
  from harness logs.
- Receipt and adherence remain testimony (`emitted-content-is-read-instructed-content-is-economised`);
  this record grades delivery and consequence only.
