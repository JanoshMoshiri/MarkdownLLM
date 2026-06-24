---
id: agents-cannot-self-install-permission-bearing-hooks
type: insight
status: active
version: 1.0
created: 2026-06-24
session: 2026-06-24
source: both
confidence: high
origin: inferred
linked_things:
  - id: hook-enforcement-has-three-anchors
    relation: informs
    notes: "The harness-session anchor's adapter has a human-gated install path — the agent cannot deploy it itself."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: supports
    notes: "Granting the framework new automatic powers is exactly the kind of privileged act the structure should keep with the human."
---

# An Agent Cannot Self-Install Its Own Hooks — They Live In A Permissions-Gated File

## The Insight

The session-lifecycle hardening adapter is a `hooks` block in `.claude/settings.json`
— the *same file* that holds permission allow-rules. The harness self-modification
guard blocks an agent from writing that file at all (it reads any edit as the agent
widening its own permissions), even to add only hooks. So the hardening adapter
**cannot be installed by the agent through its editor**; it is installed only by a
human paste, or by a deterministic tool the human ran (`mdllm scaffold` writes it at
domain birth). Adapter installation is *structurally* a human/tool action, not an
agent action — and the line is precise: the guard is on **agent-via-editor
self-modification**, not on tool output.

## Why It Matters

- It is stronger than the design rule "adapters should stay optional." The agent
  *literally cannot* self-install the adapter into a live repo, so the human (or a
  tool they invoked) is **always in the loop** for granting the framework new
  automatic powers. That is an enforced guarantee, not a convention.
- It dictates the deployment story: session-start hardening must ship as (a) a
  documented human paste, or (b) a scaffold-time tool write — never as an agent
  convenience step mid-session. Plan and docs should say so, or an agent will keep
  trying and hitting the wall.
- It explains a real friction the operator will otherwise re-hit: copying the hooks
  block by hand into every existing domain's `settings.json` is unavoidable;
  scaffold solves it only for *new* domains.

## Context

While rounding off the v3.15.0 deployment, the agent tried twice to add the
SessionStart/PostToolUse hooks to `.claude/settings.json` (via Write, then Edit) and
was blocked both times by the auto-mode classifier as self-modification /
permission-widening — because that file also carries permission allow-rules. The
framework and jmtm hooks had to be pasted by the operator; `scaffold` writes them for
new domains precisely because it runs as the tool, outside the guarded editor path.
