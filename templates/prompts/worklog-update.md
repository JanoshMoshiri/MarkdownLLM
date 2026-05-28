---
id: worklog-update
type: prompt
status: stable
version: 1.0
created: 2026-05-28
inputs:
  - name: session-conversation
    description: "The full session dialogue — work done, decisions made, topics discussed"
  - name: current-worklog
    description: "The domain's current WORKLOG.md"
  - name: current-date
    description: "Today's date for the session heading"
outputs:
  - name: updated-worklog
    description: "WORKLOG.md appended with this session's entry"
bound_to:
  - hook: session-end
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: session-memory-specification
    relation: complements
---

# Worklog Update

## Purpose

At the end of a session, append a structured entry to `WORKLOG.md` summarising what was done. The WORKLOG is retrospective — it records what happened, not what's still live. It serves as an audit trail and historical record.

## Reasoning Template

### 1. Identify The Session's Work

Scan the session for:
- Topics discussed or worked on
- Decisions made (and their rationale)
- Things created, modified, or completed
- Design choices and trade-offs considered
- Problems encountered and how they were resolved
- Work deferred or explicitly left for a future session

### 2. Structure The Entry

Append to WORKLOG.md under today's date (create a new date heading if this is the first entry for the day, or add a new session sub-heading if one already exists):

```markdown
## [Date]

### Session [N]

#### Topic: [One-line summary of what the session was about]

[1-3 sentence narrative: what was the goal and what happened]

#### Completed

- [x] **[Thing or action]**: [Brief description of what was done]
- [x] ...

#### Decisions

- **[Decision]**: [What was decided and why — the rationale matters]

#### Deferred

- [ ] **[Item]**: [What was explicitly left for later and why]
```

### 3. Commit

Commit the updated WORKLOG.md following `git-workflow.md` conventions.

## Writing Heuristic

**Include if:**
- It represents work that changed the state of the domain
- It's a decision that a future reader would want to trace
- It's context needed to understand why things are the way they are

**Do not include if:**
- It's routine navigation or exploration that led nowhere
- It's conversation that didn't result in any state change or decision
- It duplicates what's already recorded in thing frontmatter or commit messages
