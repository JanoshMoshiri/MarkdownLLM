---
id: session-memory-specification
type: specification
status: stable
version: 1.0
created: 2026-05-27
linked_things:
  - id: thing-specification
    relation: extends
  - id: orchestration-specification
    relation: integrates-with
  - id: write-thing-specification
    relation: complements
  - id: git-workflow-specification
    relation: integrates-with
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Session Memory

## What This Specifies

This document defines how the framework preserves **generative knowledge** — the ideas, views, hypotheses, and unresolved threads that surface during a session but are not yet ready to become specs, decisions, or domain things.

The framework already handles **resolved knowledge** well: a decision becomes a thing, a spec gets committed, a task gets status-tracked. But generative knowledge — the reasoning behind a decision, competing perspectives, open questions raised but deferred — disappears when a session ends. Without explicit preservation, every session starts cold.

This specification defines two primitives and one mandatory ritual to close that gap.

---

## The Two Primitives

### `type: insight`

An insight is an emerging idea, held view, working hypothesis, or captured perspective that surfaced during a session and is worth carrying forward.

**What it is:**
- An emerging idea that isn't yet fully formed into a spec or decision
- A held view or position that will influence how future decisions should be made
- A hypothesis that was agreed on but not yet tested or acted on
- A tension that was identified but not resolved
- A question that was raised but not answered in the session

**What it is not:**
- A decision (update the relevant thing directly)
- A specification (create a `type: specification` thing)
- A routine status update or procedural confirmation

**Structure:**

```yaml
---
id: [descriptive-kebab-case-id]
type: insight
status: active|promoted|dismissed
version: 1.0
created: [ISO-date]
session: [YYYY-MM-DD]
source: human|agent|both
promoted_to: [thing-id]        # populate if status becomes promoted
linked_things:
  - id: [related-thing-id]
    relation: informs|challenges|supports
---

# [Insight Title]

## The Insight
[One to three sentences: the actual idea, view, or hypothesis]

## Why It Matters
[Why this is worth carrying forward — what decisions or threads it affects]

## Context
[What triggered this in the session — the question, tension, or observation that surfaced it]
```

**Lifecycle:**

| Status | Meaning |
|--------|---------|
| `active` | Still live — needs to return in a future session |
| `promoted` | Crystallised into a spec, decision, or domain thing — `promoted_to` field is populated |
| `dismissed` | Considered and deliberately set aside — kept for audit trail, not deleted |

**Location:** `things/insights/` within the domain.

---

### `type: continuity-brief`

A continuity brief is the domain's live forward-looking session-continuity document. There is exactly one per domain.

**What it is:**
- A rolling document that bridges sessions
- Updated at session end, loaded at session start
- Contains: open threads, live insights, pending decisions, and questions that need to return

**What it is not:**
- A log (the WORKLOG is the log — retrospective, audit trail)
- A summary of what was done (WORKLOG handles this)
- A substitute for thing files

**Relationship to WORKLOG:**

| | WORKLOG | Continuity Brief |
|---|---|---|
| **Direction** | Retrospective | Forward-looking |
| **Content** | What was done, decided, discussed | What is still live |
| **Audience** | Audit trail, human retrospective | Next session's agent |
| **Growth** | Always grows (append-only) | Stays lean — resolved items are removed |

**Location:** Domain root, named `continuity.md` — alongside WORKLOG.md and AGENTS.md.

**Structure:**

```yaml
---
id: [domain]-continuity-brief
type: continuity-brief
status: live
version: 1.0
created: [ISO-date]
domain: [domain-id]
last_updated: [ISO-date-of-last-session]
---
```

**Body sections:**

- **Open Threads** — Design questions, active tensions, or lines of reasoning that are mid-flight. One line per thread: what it is and what's needed to close it.
- **Live Insights** — Active insight things that need to return. Listed by ID with a one-line summary.
- **Pending Decisions** — Decisions raised but not yet made. Two candidate options noted where possible.
- **Questions For Next Session** — Specific questions that must be answered before certain threads can progress.

**Update discipline:**
- Resolved thread: remove it — the WORKLOG has the history
- New thread opens: add it
- Insight promoted to a spec: remove from brief, link via the promoted thing
- Keep it short — if it grows past ~30 lines, stale items have accumulated

---

## The Session-End Extraction Ritual

This ritual is a **framework-level hard hook** (`session-end:continuity`). See `orchestration.md` for the full hard hook definition. It fires at the end of any session in which a domain was discussed or modified.

### Step 1: Scan For Insights

Review the session for:
- Non-obvious positions taken by either party
- Hypotheses that were agreed on but not acted on
- Questions raised but not answered
- Tensions identified but not resolved
- Reframings that changed how something is understood

Apply the **preservation test**: *Would a fresh agent starting this domain cold benefit from knowing this?* If yes, preserve. If routine, procedural, or already captured in a thing, skip.

### Step 2: Create Insight Things

For each insight worth preserving, create a `type: insight` thing in `things/insights/`.

### Step 3: Update The Continuity Brief

Load `continuity.md`. Make these updates:
- Add new open threads from this session
- Remove threads that resolved in this session
- Add new live insight IDs (with one-line summaries)
- Remove insights that were promoted or dismissed
- Update pending decisions — remove resolved ones, add new ones
- Refresh the questions list

### Step 4: Commit

Commit all new insight things and the updated continuity brief following `git-workflow.md` conventions.

---

## Extraction Heuristic

**Preserve if:**
- It's a held view that will influence future decisions
- It's an unresolved tension that needs to return
- It was surprising or contradicted a prior assumption
- It's a hypothesis agreed on but not yet tested or acted on
- It's a question that blocks progress on something

**Do not preserve if:**
- It's a routine status update or procedural confirmation
- It's a decision already captured in a thing
- It's context that won't affect anything in the future
- It was raised and fully resolved in the same session

The continuity brief stays lean. Git history has everything else.

---

## Initialising Session Memory In A Domain

When scaffolding a new domain, `continuity.md` should be created alongside `AGENTS.md` and `WORKLOG.md`. Use the template at `templates/continuity-brief.md.template`.

If the agent encounters a domain without a `continuity.md`, it should:
1. Create one using the template
2. Populate it with any live threads from the current session
3. Commit it with a note that it is being initialised

---

## Relationship To Other Specs

- **thing.md** — `insight` and `continuity-brief` are framework-reserved types defined here. All other type mechanics (frontmatter, linking, triggers) are inherited from `thing.md`.
- **orchestration.md** — The `session-end:continuity` hard hook is the enforcement mechanism that makes this ritual mandatory rather than optional.
- **write.thing.md** — Creating and updating insight things follows standard write operations. The session-end ritual is an extension of the write workflow.
- **git-workflow.md** — Insight things and continuity brief updates are committed following standard conventions. The session-end commit is the natural pairing of the `post-write:commit` hard hook.
