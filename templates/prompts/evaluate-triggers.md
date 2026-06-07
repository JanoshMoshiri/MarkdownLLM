---
id: evaluate-triggers
type: prompt
status: stable
version: 1.1
created: 2026-05-20
inputs:
  - name: trigger-index
    description: "The domain's triggers index (things/_index/triggers.md), if it maintains one — the preferred scan substrate at scale"
  - name: things-to-scan
    description: "Set of things to evaluate triggers for — used directly when no trigger index exists, or as the affected subset after a write"
  - name: current-date
    description: "Today's date for time-based trigger evaluation"
  - name: git-history
    description: "Recent commits since last session (for detecting what changed)"
outputs:
  - name: fired-triggers
    description: "List of triggers whose conditions are now true, with their declared actions"
  - name: attention-items
    description: "Things that need user attention based on fired triggers"
bound_to:
  - hook: session-start
  - hook: post-write
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: thing-specification
    relation: operates-on
---

# Evaluate Triggers

## Purpose

Scan things for trigger conditions that are currently true. This is the framework's proactive attention system — it ensures the agent notices what needs noticing without the user asking.

## Choosing The Scan Substrate

**If the domain maintains a `triggers` index** (`things/_index/triggers.md`), scan the
index rather than every thing's frontmatter — this is the whole reason the index exists
(see `derived-index.md`). The index already aggregates every active trigger, so reading
it is O(index) instead of O(all things). Before trusting it, do the cheap staleness
check: if `generated_from` is behind `HEAD` and intervening commits touched things with
triggers, rebuild the index first (or fall back to a direct scan for this session and
flag the index for rebuild).

**If the domain has no trigger index** (small domains usually won't), scan
`things-to-scan` directly. After a write, scan only the affected subset, index or not.

## Reasoning Template

For each trigger (from the index, or from each thing's `triggers` array directly),
evaluate as follows:

### Time-Based Triggers

Check against `current-date`:

| Condition | True When |
|-----------|-----------|
| `due_date_passed` | `due_date` < today AND status ∉ {completed, cancelled} |
| `review_date_reached` | `review_date` ≤ today |
| `stale` | Last modification > `threshold` days ago AND status ∉ {completed, cancelled, paused} |

### Dependency-Based Triggers

Check against current state of watched things:

| Condition | True When |
|-----------|-----------|
| `status_changed_to` | Watched thing's status == `value` |
| `priority_changed` | Watched thing's priority differs from last known |
| `any_modification` | Watched thing's file was modified since last evaluation |

### Threshold-Based Triggers

Check against accumulated state:

| Condition | True When |
|-----------|-----------|
| `subtasks_complete` | Count of completed subtasks / total subtasks ≥ threshold |
| `blocked_duration` | Thing has been `blocked` for > threshold duration |
| `in_progress_count` | System-wide count of `in-progress` things > threshold |

### Relationship-Based Triggers

Check against connected things:

| Condition | True When |
|-----------|-----------|
| `priority_changed` | Related thing's priority changed |
| `status_changed_to` | Related thing reached specified status |

## Proportional Response

A trigger that has been true for one session gets mentioned once. A trigger that has been true for multiple sessions gets escalated:

- **First occurrence:** Surface normally — "X is overdue"
- **Persistent (3+ sessions):** Escalate — "X has been overdue for 2 weeks. Should we reprioritize, reschedule, or cancel?"
- **Chronic (7+ sessions):** Flag for decision — "X has been flagged repeatedly without resolution. This needs a decision."

The agent infers persistence from git history (how long has the condition been true?) rather than maintaining separate state.

## Output Format

```
Trigger evaluation complete:
- Fired: [count] triggers across [count] things
- Time-based: [list with thing IDs and conditions]
- Dependency-based: [list with thing IDs and what changed]
- Threshold-based: [list with thing IDs and current values]
- Actions required: [grouped by action type: surface, escalate, unblock, etc.]
```
