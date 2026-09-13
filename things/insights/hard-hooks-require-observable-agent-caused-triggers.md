---
id: hard-hooks-require-observable-agent-caused-triggers
type: insight
status: active
version: 1.1
created: 2026-05-28
confidence: high
origin: synthesised
source: session — session-end hook review and refactor
session: 2026-05-28
tags: [hooks, orchestration, design-principle, classification]
linked_things:
  - id: orchestration-specification
    relation: informs
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: extends
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: "The anchor taxonomy that redefined 'hard' after this insight was written; v1.1 restates the principle in its vocabulary — the requirement here is for enforcement, not for the label"
  - id: hard-hook-vocabulary-contradicts-observable-trigger-insight
    relation: references
    notes: "The conflict that surfaced the vocabulary drift and was ruled both-valid on 2026-09-13; this revision is its remedy"
---

# Hard Hooks Require Observable, Agent-Caused Triggers

## The Insight

For a hook to be genuinely "hard" (always fires, no exceptions, no configuration), it must be triggered by an event the agent itself caused and can observe unambiguously. The two surviving hard hooks — `post-write:commit` (agent just modified a file) and `pre-domain-scaffold:isolate` (agent is creating a new domain) — both meet this criterion. `session-end:continuity` did not — "the session is ending" is a state that no agent can detect without an external signal.

The design principle: **if the trigger depends on something external to the agent's own actions, it is not a hard hook — it is a prompt bound to a hook point, explicitly invoked.**

## Revised 2026-09-13 — the principle in anchor vocabulary

The principle above is right about **enforcement** and was wrong to bind it to
the word "hard". Since `hook-enforcement-has-three-anchors`, *hard* means
always-on configuration and says nothing about enforcement; enforcement is the
anchor axis. Restated: **a hook can be enforced only where its trigger is
observable to the thing that enforces it** — agent-caused acts anchor at
`git-fs` and fire mechanically; harness events anchor at `harness-session`
and fire where an adapter binds them; everything else is interpretation,
however hard its configuration. The two hooks this insight named are the two
`git-fs`-anchored ones. The session-start hooks it excluded are hard *and*
unenforced wherever no adapter runs them — both true, on different axes.

The classification test becomes: *can the agent detect the trigger from its
own actions?* If yes, it can be enforced at `git-fs`. If no, it is enforced
only by an adapter or not at all — and its "hard" label is a statement about
configuration, not a promise. The original reasoning stands as the history of
how the anchor model was reached.

## Why It Matters

This principle prevents future over-classification. Any time something feels important enough to be "mandatory," the question is: can the agent detect the trigger from its own actions? If yes → hard hook. If no → bound prompt. Importance alone does not make something hard; observability does.

## Context

Discovered during review of why `session-end:continuity` wasn't firing reliably across sessions. The ritual was well-specified and the agent was aware of it, but compliance drifted because there was no event to trigger it. Reclassifying as a prompt with explicit invocation resolved the tension between "this matters" and "this can't fire automatically."
