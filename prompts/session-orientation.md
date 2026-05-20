---
id: session-orientation
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: git-log-since-last-session
    description: "Commits made since the agent was last active"
  - name: active-things-summary
    description: "Metadata of all things with status not in {completed, cancelled, archived}"
  - name: current-date
    description: "Today's date for temporal context"
outputs:
  - name: orientation-summary
    description: "Brief summary of what changed and what's relevant now"
  - name: suggested-focus
    description: "What the user might want to work on based on state"
bound_to:
  - hook: session-start
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: read-thing-specification
    relation: follows
---

# Session Orientation

## Purpose

At the start of every session, orient the agent to the current state of the domain. This prompt ensures continuity across sessions — the agent quickly understands what happened since it was last active and what's most relevant right now.

## Reasoning Template

### 1. What Changed Since Last Session

Parse `git-log-since-last-session` to understand recent activity:

- **New things created** — What was added to the domain?
- **Status transitions** — What moved forward, got blocked, or was completed?
- **Priority changes** — Did anything become more or less urgent?
- **Structural changes** — Were things split, merged, or reorganized?

If no commits since last session: note that the domain is unchanged.

### 2. Current State Snapshot

From `active-things-summary`, build a quick picture:

- **In-progress:** What's actively being worked on?
- **Blocked:** What's stuck and why?
- **High priority + not-started:** What's important but hasn't begun?
- **Overdue:** Anything past its due date?

### 3. Temporal Context

Based on `current-date`:

- Are any due dates approaching within the next 7 days?
- Are any review dates today?
- Is it the start/end of a week, month, or quarter? (Relevant for periodic things)

### 4. Suggested Focus

Based on the above, infer what's most likely relevant:

- If something was recently unblocked → it's probably the next action
- If something is overdue → it probably needs attention
- If nothing has changed → the user might need help deciding what to work on next

## Output Behavior

The session-orientation output is **internal to the agent** — it informs how the agent greets the user and what it proactively mentions. It is NOT dumped as a raw report unless the user asks "what's the state of things?"

**If the user opens with a specific request:** Use orientation as background context but respond to their request directly. Don't lead with a status dump.

**If the user opens with something general** ("hey", "what should I work on", "catch me up"): Use orientation as the basis for a concise, helpful summary.

### Tone

- Brief, not exhaustive
- Lead with what matters most
- Don't list things that are fine and don't need attention
- Make it feel like catching up with a competent collaborator, not reading a dashboard
