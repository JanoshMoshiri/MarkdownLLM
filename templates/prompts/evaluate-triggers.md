---
id: evaluate-triggers
type: prompt
status: stable
version: 1.3
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
    relation: implements
  - id: thing-specification
    relation: references
---

# Evaluate Triggers

## Purpose

Scan things for trigger conditions that are currently true. This is the framework's proactive attention system — it ensures the agent notices what needs noticing without the user asking.

## The Floor Evaluates; You Judge

`mdllm triggers` (and the session-start orient view) performs the mechanical
evaluation — never re-perform its date arithmetic or state reads by
reasoning. Its output keeps four buckets apart, and so must your report:

- **Fired** — the condition is true NOW. This is the only bucket that is
  pressure.
- **Upcoming (≤30d)** — a look-ahead, *not* fired. Reporting look-aheads as a
  fired backlog manufactures strain in a quiet domain (2026-08-08 field
  evidence — the reason the buckets are mechanically separate).
- **Horizon (>30d)** — visible, not actionable.
- **Not mechanically evaluable** — prose conditions left to your judgment;
  these, plus the proportional-response reasoning below, are what this prompt
  is for.
- **Self-answering armed (heuristic)** — armed future-dated triggers whose
  action text already answers the condition ("do not re-ask", "already
  issued", "remedies are spent"). Left armed, they fire on their own answer
  — six wore this pattern at once in one live domain. The floor cues them;
  confirming each and disarming or re-conditioning it is yours.

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
| `due_date_passed` | `due_date` < today AND status is non-terminal (the type's `terminal_statuses`, or the universal defaults where none declared) |
| `review_date_reached` | `review_date` ≤ today |
| `stale` | Last commit touching the thing > `threshold` days ago AND status is non-terminal |

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
| `subtasks_complete` | Count of terminal-status subtasks / total subtasks ≥ threshold |
| `blocked_duration` | Thing has been `blocked` for > threshold duration (needs status history — the floor routes this to you) |

*(`in_progress_count` was removed from the trigger vocabulary in
trigger-specification v1.2 — no domain ever used it. This template restated
it for two releases after removal; the spec is the authority.)*

### Import-Based Triggers

Keyed to the state `mdllm imports-check` computes for cross-domain imports
(trigger-specification v1.3):

| Condition | True When |
|-----------|-----------|
| `state_is` | Any watched import's current state matches `value` (default trio: `stale`, `diverged`, `withdrawn`) — a live face read the floor performs |
| `porch_offers_unimported` | A source's face offers things this domain has not imported |

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
