---
id: session-memory-specification
type: specification
status: stable
version: 1.1
created: 2026-05-27
linked_things:
  - id: thing-specification
    relation: extends
  - id: orchestration-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: belief-revision-specification
    relation: complements
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
confidence: high|medium|low
origin: stated|inferred|synthesised
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

## The Session-Start Staleness Check

Insights are written once and then re-enter every session as trusted context via
the continuity brief — but the domain keeps moving after they're written. Without
a check, a session can reason confidently from an insight whose factual basis
changed three sessions ago.

The check is **scoped, not a sweep** (added v1.1, transformation plan Phase 4):

1. Take the live insight IDs from `continuity.md` — a small, bounded set
2. Identify things modified since the brief's `last_updated` (git provides this
   for free: commits or diff since that date, scoped to `things/`)
3. Re-read only the live insights whose subject matter overlaps the changed
   things; surface any that no longer hold rather than silently reasoning from them

Cost: near-zero when nothing relevant changed; a few targeted reads when it did.
The full-corpus contradiction sweep remains a retrospective-cadence behaviour
(`belief-revision.md` → When To Scan For Conflicts) — this check exists precisely
so that gap doesn't leak into every session. Implemented as Step 0 of the
`session-orientation` prompt.

---

## The Session-End Extraction Ritual

This ritual is implemented as the **`session-end-continuity` prompt** bound to the `session-end` hook point. See `templates/prompts/session-end-continuity.md` for the full prompt template, and `orchestration.md` → Bindings for how it is invoked.

The prompt is explicitly invoked at session end — either by the user requesting it, or by the agent recognising the session is closing. It is not automatic; it requires a deliberate trigger.

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

### Step 3: Belief Revision — Check For Contradictions

Before updating the continuity brief, scan for contradictions introduced this session:

- Did any new insight or modification assert something that conflicts with an existing thing?
- Do any two things now in view hold incompatible positions?

For each contradiction found:
1. If it can be resolved in-session (one position clearly supersedes the other): update the relevant things, declare `relation: supersedes` / `relation: superseded-by`, and mark the old position deprecated if appropriate.
2. If it cannot be resolved in-session: create a `type: conflict` thing in `things/conflicts/`, add `relation: contradicts` to both parties' `linked_things`, and add the conflict to the continuity brief as an open thread.

Be conservative — only flag genuine semantic contradictions, not differences in emphasis or scope. When uncertain, surface for human confirmation rather than silently creating a conflict thing. Full spec: `belief-revision.md`.

### Step 4: Update The Continuity Brief

Load `continuity.md`. Make these updates:
- Add new open threads from this session
- Remove threads that resolved in this session
- Add new live insight IDs (with one-line summaries)
- Remove insights that were promoted or dismissed
- Update pending decisions — remove resolved ones, add new ones
- Add any new open conflicts (from Step 3) as open threads
- Refresh the questions list

### Step 5: Commit

Commit all new insight things, new conflict things, and the updated continuity brief following `git-workflow.md` conventions.

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
- **orchestration.md** — The `session-end-continuity` and `worklog-update` prompts are bound to the `session-end` hook point. These are explicitly invoked prompts, not automatic hooks — they require the user or agent to trigger them at session close.
- **write.thing.md** — Creating and updating insight things follows standard write operations. The session-end ritual is an extension of the write workflow.
- **git-workflow.md** — Insight things and continuity brief updates are committed following standard conventions. The session-end commit is the natural pairing of the `post-write:commit` hard hook.
