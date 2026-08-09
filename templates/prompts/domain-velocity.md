---
id: domain-velocity
type: prompt
status: stable
version: 1.1
created: 2026-06-08
inputs:
  - name: git-log-things
    description: "git log over things/ with dates and subjects (the domain event stream)"
  - name: current-date
    description: "Today's date, for computing how long things have been untouched"
  - name: active-things-summary
    description: "Metadata of things at a non-terminal status (per the type's terminal_statuses, or the universal defaults) — to cross-reference against commit recency"
outputs:
  - name: velocity-summary
    description: "3–5 observations about domain movement: what is stalling, what is moving, what is untouched"
bound_to:
  - hook: session-start
linked_things:
  - id: orchestration-specification
    relation: implements
  - id: git-workflow-specification
    relation: references
  - id: derived-index-specification
    relation: complements
---

# Domain Velocity

## Purpose

Read the git history *as telemetry* — not to load thing content, but to reason about
the domain's movement. This is the reflexive counterpart to `session-orientation`:
orientation asks "what changed since I was last here?"; velocity asks "what *should*
have changed and hasn't?" It surfaces stalls the current-state snapshot cannot see,
because a thing sitting at `in-progress` for six weeks looks identical to one that
was updated yesterday until you consult the history.

This prompt reads git directly and maintains no index — the commit log is already
the source of truth (see `derived-index.md` → velocity needs no index).

## Reasoning Template

### 1. Gather the event stream

```
git log --format="%ad %s" --date=short -- things/
git log --diff-filter=M --name-only --since="30 days ago" -- things/
```

The first gives the full cadence of domain state changes; the second shows which
things were actually modified recently.

### 2. Compute velocity signals

| Signal | How to read it |
|---|---|
| **Stalled work** | A thing is `in-progress` but its file has no commit in > N days (default 21). It looks active but isn't. |
| **Untouched commitments** | A thing is `high`/`critical` priority and `not-started`, with no commit since creation. |
| **Cadence** | Commits per week over the period — is the domain accelerating, steady, or gone quiet? |
| **Churn vs. progress** | Many `update:` commits on one thing with no `complete:`/`unblock:` — spinning, not finishing. |
| **Recently unblocked, then ignored** | An `unblock:` commit with no follow-up commit on that thing — the unblock didn't lead to action. |

### 3. Proportional reporting

Velocity is background context, like `session-orientation` — not a dashboard dump.
Surface only what is actionable:

- Lead with the most stalled high-value thing.
- Name the stall in time terms: "X has been in-progress with no change for 5 weeks."
- If the domain is moving healthily, say so in one line and stop.

## Output Behavior

Internal context that shapes how the agent opens and what it proactively raises. Emit
a full velocity report only if the user asks "how's this domain moving?" or similar.
Otherwise fold the single most important signal into the greeting, if any warrants it.
