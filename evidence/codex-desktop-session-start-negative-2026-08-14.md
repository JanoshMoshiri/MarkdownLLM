---
id: codex-desktop-session-start-negative-2026-08-14
type: artifact
status: stable
created: 2026-08-14
tags: [codex, desktop, phase-6, execution-evidence, negative-evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Narrow Phase 6 observation: the tested Codex Desktop build injected AGENTS but did not dispatch the current project SessionStart hook."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Separates configuration and interpretation from the absent harness-bound side effect."
---

# Codex Desktop SessionStart Negative Record — 2026-08-14

## Scope

This record covers one fresh framework-root task in Codex Desktop for Windows,
package build `26.803.10989.0`. It is a negative execution observation for that
exact surface, not a universal assertion that all Desktop versions lack project
hooks and not a substitute for the pending Codex CLI test.

The tracked project configuration was present and current at
`.codex/hooks.json`, SHA-256
`a68be54142e7acbe9d268ef8895baab25cda0b3cef800870c4e8258186b66461`.
The fresh task followed the plan-only boundary commit `efdacfe`; concurrent
Claude POSIX evidence landed before this record was captured. The task did not
print its exact start HEAD, so this record does not invent one.

## Test

The operator opened a fresh framework-root task and explicitly instructed the
agent not to run `session-start` or `harness-event` manually. The first duties
were to report automatically injected lifecycle context, inspect the Codex
attestation, and run `mdllm doctor . --harness codex`.

## Observed Consequences

- The task received the workspace `AGENTS.md` policy through the interpretation
  surface.
- No Codex SessionStart lifecycle output was injected into the conversation.
- `.git/mdllm-harness-attest` contained the existing
  `claude-code/session-start.json` only; no Codex SessionStart record existed.
- Doctor reported Codex configuration `present`, currency `current`, launch
  currency `current`, runtime `command-runs`, and execution `untested` with
  `no real-event execution attestation for this definition`.
- The Git pre-commit floor remained active independently.

The required side effect—automatic project-hook dispatch—was absent even
though configuration, runtime resolution, and AGENTS interpretation were all
available. No manual lifecycle command was used to manufacture evidence.

## Disposition

Codex Desktop build `26.803.10989.0` remains unverified for project
SessionStart on this tested task-start surface. Phase 6 moves its positive Codex
root and nested-domain execution tests to Codex CLI, where the project hook and
human review surfaces can be exercised directly. Desktop PostToolUse is not
claimed either way by this test; the fresh-task probe tested SessionStart only.
