---
id: session-start-loses-to-the-first-request
type: insight
status: active
version: 1.1
created: 2026-06-23
session: 2026-06-23
source: both
confidence: high
origin: inferred
linked_things:
  - id: hook-enforcement-has-three-anchors
    relation: supports
    notes: "Names why the harness-session anchor specifically fails under interpretation — the trigger collides with the user's first message."
  - id: agents-md-discovery-is-harness-dependent
    relation: supports
  - id: orchestration-specification
    relation: informs
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: references
    notes: "2026-08-18 evidence extends the skip to a stronger model tier in two harnesses at once, and sharpens the mechanical-delivery fix to a rule about form: emit the content, don't instruct its load."
---

# Session-Start Loses To The User's First Request — Regardless Of Model Tier

## The Insight

The `session-start` hook fires at the same instant as the user's first message, and
the live request reliably out-competes a standing instruction sitting in the entry
file — observed **even on Opus in Claude Code**, not only on weaker models. So
session-start is the framework's most-skipped hook *by construction*: interpretation
alone cannot carry it, because the one moment it must fire is the one moment the model
is most pulled elsewhere. It is therefore the prime hardening target — computable
state and Tier-0 content are delivered mechanically at t=0, while the irreducible
orientation judgement remains explicitly invoked rather than falsely claimed as
performed by injection.

## Why It Matters

- It reframes session-start skipping from a **model-capability** problem (fixable with
  a better model) to a **structural** one (fixable only by changing *when/how* the
  ritual arrives). That redirected the v3.15.0 fix from "slim the entry file" alone to
  "also inject the ritual at the real session-start event" (`mdllm session-start` +
  the optional adapter).
- It falsified the former claim that interpretation is sufficient for correctness:
  session-start is where the weakness became visible first, not a unique exception.
  The adapter is *hardening*, not gold-plating, and its evidence still stops at the
  exact delivery/execution state observed.
- It predicts an ordering worth testing: as model strength drops, interpretation-anchored
  hooks fail in **reverse anchor-strength order — session-start first**. Git-anchored
  hooks never fail; that asymmetry is the whole case for the three-anchor model.

## Context

Surfaced while building the domain kernel (v3.15.0). The operator reported Claude Code
on Opus jumping straight from the first request into the task, skipping the Tier-0
ritual (load kernel, version-check, velocity) — proving the skip was not a weak-model
artefact. Walking it showed the trigger collides with the user's message and loses.
The fix became `mdllm session-start` emitting the ritual to stdout for a `SessionStart`
hook to inject. Extends [[hook-enforcement-has-three-anchors]]: the `harness-session`
anchor is enforced only where an adapter binds it, and session-start is the case that
proves why.
