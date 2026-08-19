---
id: agents-cannot-self-install-permission-bearing-hooks
type: insight
status: active
version: 1.1
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

A project-bound session-lifecycle adapter may own a permission-bearing file
(`.claude/settings.json` is the first observed case). The harness
self-modification guard blocks an agent from editing that file as ordinary
content because the edit could widen its own authority. So the adapter
**cannot be self-installed through the agent's editor**. Installation is an
operator-reviewed tool action: `mdllm scaffold` may render it at birth, and
`mdllm adapter-install --dry-run` now shows the exact renderer-owned diff for
an existing domain before the operator invokes or approves the apply.
Adapter installation is structurally a human/tool action, not an agent action
— and the line is precise: the guard is on **agent-via-editor
self-modification**, not on deterministic tool output reviewed at a human
boundary.

## Why It Matters

- It is stronger than the design rule "adapters should stay optional." The agent
  *literally cannot* self-install the adapter into a live repo, so the human (or a
  tool they invoked) is **always in the loop** for granting the framework new
  automatic powers. That is an enforced guarantee, not a convention.
- It dictates the deployment story: session-start hardening ships as a
  scaffold-time render or an explicit renderer-backed install reviewed by the
  operator — never as an agent convenience edit mid-session. Static pasteable
  examples are wrong because path-instantiated, definition-hash-bound output is
  stale as soon as it is copied.
- It removes the old false choice between unavoidable hand-paste and new-domain
  only support. Existing domains have an opt-in dry-run/apply route, while
  unknown stale state, local extensions, and ambiguity still refuse.

## Context

While rounding off the v3.15.0 deployment, the agent tried twice to add the
SessionStart/PostToolUse hooks to `.claude/settings.json` (via Write, then Edit) and
was blocked both times by the auto-mode classifier as self-modification /
permission-widening — because that file also carries permission allow-rules. The
framework and JMTM hooks had to be pasted by the operator; `scaffold` wrote them for
new domains precisely because it ran as the tool, outside the guarded editor path.
That incident remains the evidence for the authority boundary. The later
`adapter-install` service replaced the paste mechanism without changing who
authorises the consequence.
