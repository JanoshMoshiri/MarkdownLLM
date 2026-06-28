---
id: long-running-tasks-lack-pre-compaction-checkpoint
type: insight
status: active
disposition: keep-active
disposition_reason: "Parked framework gap — long tasks can lose state on compaction; the continuity work mitigated it (open loops are committed things) but the general gap awaits a felt fix."
version: 1.2
created: 2026-06-20
confidence: medium
origin: synthesised
source: session — README awareness/compaction framing review
session: 2026-06-20
tags: [compaction, session-memory, long-running-tasks, deferred, transparency]
linked_things:
  - id: session-memory-specification
    relation: informs
  - id: orchestration-specification
    relation: informs
  - id: git-workflow-specification
    relation: references
---

# Long-Running Tasks Lack a Pre-Compaction Checkpoint

## The Insight

The framework protects *committed* state continuously — `post-write:commit` writes every thing to git the moment it's made — but it has no automatic checkpoint for the *in-flight, uncommitted* reasoning of a long-running task. Between commits, that reasoning lives only in the context window; if the harness compacts there, its lossy summary is all that survives, and the task can resume on a blurred memory of its own work.

In practice this is rarely felt, and deliberately not yet built. A task large enough to risk it is normally planned as a workflow — itself a documented set of MD files — and executed with frequent commits, so the agent re-grounds from files rather than from the window. The gap is real but the mitigation is structural and already present; the missing piece is only the *guaranteed* capture of reasoning that hasn't reached a commit.

## Why It Matters

This is recorded for transparency, not just memory. An operator with deep framework understanding mitigates this instinctively — plan the task as a workflow, commit often. Someone fresh to the framework may not, and could watch a long autonomous task drift without knowing why. This insight exists so that when they ask the agent "why did this drift?", the agent can surface it as a **known, deliberately-deferred limitation** rather than improvise — a public marker someone else can find, and fix.

It also preserves the path if it ever becomes a felt problem, so the next person isn't starting cold:

- **Where it would live:** when this was written the proposed home was an "Active Task Checkpoint" section in `continuity.md`; continuity was dissolved into orientation at v3.17, so the checkpoint would now be transient, task-scoped state hung off the session-start open-loops/orientation view — still *distinct* from a session close, because it bridges a compaction (possibly mid-session). Present only while a long task is in flight; removed on completion. It belongs with disposable task-scoped state, **not** as an `insight`, because it is not crystallised knowledge.
- **Baseline (portable):** an interpretation cadence — the agent refreshes and commits the checkpoint at meaningful sub-steps. Best-effort; "the agent should", not guaranteed.
- **Hard mitigation (configurable):** bind the harness's pre-compaction hook (Claude Code's `PreCompact`; vendor equivalents as they appear) to fire the checkpoint automatically. This is a lowest-consequence, adapter-hardened hook in the sense of `orchestration.md` — never required, never the difference between working and not.

**Revisit when felt:** if compaction ever strands uncommitted reasoning on a long autonomous task in a way the workflow-plus-commits discipline doesn't already cover.

## Context

Surfaced 2026-06-20 while making the README's compaction framing honest. The opening had claimed state "survives every compaction" — literally true of committed files, but it implied an automatic in-flight guarantee the framework does not make. The line was changed to state the mechanism plainly: work rides in files and git as it's made, so the agent re-grounds from them. The operator's lived experience confirmed the framing — long, workflow-driven tasks generating many MD files had worked past compaction without trouble, precisely because the workflow was written down and commits were frequent. The decision was to state the truth honestly and not build a safeguard for a problem not yet felt — capturing the deferral here so the choice is visible rather than silent.
