---
id: uncommitted-work-is-judged-from-the-record-that-left-it
type: insight
status: active
version: 1.0
created: 2026-10-22
session: 2026-10-22
source: both
confidence: high
origin: inferred
disposition: keep-active
disposition_reason: "A standing rule for every brief that hands another session's uncommitted state to an agent; no spec carries it because the brief is harness-level, not framework-level."
tags: [delegation, brief, staged-work, backward-record, session-end, authority]
linked_things:
  - id: git-workflow-specification
    relation: extends
    notes: "The commit is the backward record — so the last commit's message is the first read on anything left uncommitted after it."
  - id: session-memory-specification
    relation: informs
    notes: "A session-end commit that says 'left uncommitted on the operator's ruling' is a ruling; a later agent that reads the diff before the commit commits against it."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: supports
    notes: "The commit was recoverable (revert, stash); the publish made it visible to every consumer first. The irreversible step is the one the brief should have gated."
---

# Uncommitted Work Is Judged From The Record That Left It, Not From Its Bytes

## The Insight

A staged-and-never-committed change set looks like a unit of work waiting
for its commit. It is not, until the record says so. The session that left
it wrote why in the one place the framework guarantees survives — the last
commit's message, the handoff plan, the stash's description — and an agent
briefed to "deal with the staged work" that reads `git diff --cached` before
`git log -1` has skipped the only authority on it.

On 2026-10-22 a delegated domain agent, acting correctly on the brief it was
given, committed and published fourteen staged files in a private workspace
whose previous session-end commit and handoff plan both recorded the
operator's ruling to leave them uncommitted. The floor passed them: they
were structurally valid. The ruling was prose in the backward record, and
the brief sent the agent to the bytes first. The operator ruled a revert the
same hour; the edits survived in the reverted commit and a stash, but two
exposed records had already carried the change to other workspaces' import
checks.

**The rule:** any brief that hands uncommitted or staged state to an agent
names, in order, the last commit message, the latest handoff or plan record
and `git stash list` as the first reads; a ruling found there binds; when
nothing is found, leave the state as it was and report. The brief gates the
irreversible step (the publish), not the reversible one (the commit).

## Why It Generalises

The framework's own claim is that the commit is the backward record. The
corollary is that uncommitted state is *defined* by that record — what the
last commit says about it is what it is. A floor can verify the bytes; only
the record says whether they were meant to land.
