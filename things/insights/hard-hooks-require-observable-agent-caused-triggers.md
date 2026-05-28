---
id: hard-hooks-require-observable-agent-caused-triggers
type: insight
status: active
version: 1.0
created: 2026-05-28
confidence: high
origin: both
source: session — session-end hook review and refactor
session: 2026-05-28
tags: [hooks, orchestration, design-principle, classification]
linked_things:
  - id: orchestration-specification
    relation: informs
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: extends
---

# Hard Hooks Require Observable, Agent-Caused Triggers

## The Insight

For a hook to be genuinely "hard" (always fires, no exceptions, no configuration), it must be triggered by an event the agent itself caused and can observe unambiguously. The two surviving hard hooks — `post-write:commit` (agent just modified a file) and `pre-domain-scaffold:isolate` (agent is creating a new domain) — both meet this criterion. `session-end:continuity` did not — "the session is ending" is a state that no agent can detect without an external signal.

The design principle: **if the trigger depends on something external to the agent's own actions, it is not a hard hook — it is a prompt bound to a hook point, explicitly invoked.**

## Why It Matters

This principle prevents future over-classification. Any time something feels important enough to be "mandatory," the question is: can the agent detect the trigger from its own actions? If yes → hard hook. If no → bound prompt. Importance alone does not make something hard; observability does.

## Context

Discovered during review of why `session-end:continuity` wasn't firing reliably across sessions. The ritual was well-specified and the agent was aware of it, but compliance drifted because there was no event to trigger it. Reclassifying as a prompt with explicit invocation resolved the tension between "this matters" and "this can't fire automatically."
