---
id: trigger-specification
type: specification
status: stable
version: 1.2
created: 2026-05-29
linked_things:
  - id: thing-specification
    relation: extends
  - id: orchestration-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
---

# Trigger Specification

Triggers are declarative attention signals attached to a thing. They are not code and do not execute anything — they are metadata telling the agent "when you're next active, check whether this condition is true, and if so, direct your reasoning here." The LLM decides how to respond. The trigger says "look here."

This is a fundamental distinction from traditional event systems. In a traditional system, a trigger causes code to run. In this framework, a trigger causes the LLM to *think about something*.

The framework is pull-based — a human initiates a session, and the agent reasons. Without triggers, the agent only thinks about what the human asks about. With triggers, the agent can proactively surface things that need attention based on conditions the human defined in advance.

## Structure

```yaml
triggers:
  - type: time|dependency|threshold|relationship
    condition: [what to check]
    action: [what to do if true]
```

## Trigger Types

### Time-based

Conditions that depend on time passing.

```yaml
triggers:
  - type: time
    condition: due_date_passed
    action: surface
  - type: time
    condition: review_date_reached
    action: re_evaluate
  - type: time
    condition: stale
    threshold: 30d
    action: surface
```

- `due_date_passed` — The thing's `due_date` is in the past and status is not `completed` or `cancelled`
- `review_date_reached` — The thing's `review_date` has arrived
- `stale` — The thing hasn't been modified in longer than `threshold`
- Any other condition string is **free text**. The evaluator (`mdllm triggers`)
  still honours it mechanically where it can: if the text names an ISO date
  (`2026-09-01`), that date is treated as the fire date — past dates on
  unsettled things fire, dates within 30 days surface as upcoming, later dates
  join the horizon. A free-text condition naming no parseable date is reported
  as not mechanically evaluable — never silently dropped.
- `type: date` is accepted as an alias of `type: time` — domains write it
  naturally, and rejecting it silently would kill the control one character of
  drift away from the supported spelling.

### Dependency-based

Conditions that fire when something this thing depends on changes.

```yaml
triggers:
  - type: dependency
    watch: [prerequisite-task-id, approval-decision-id]
    on: status_changed_to
    value: completed
    action: unblock
```

- `watch` — The IDs of things being observed
- `on` — What change to watch for (`status_changed_to`, `priority_changed`, `any_modification`)
- `value` — The specific value that satisfies the condition (if applicable)

### Threshold-based

Conditions that fire when accumulated state crosses a boundary.

```yaml
triggers:
  - type: threshold
    condition: subtasks_complete
    threshold: 100%
    action: suggest_completion
  - type: threshold
    condition: blocked_duration
    threshold: 7d
    action: escalate
```

- `subtasks_complete` — All linked things with relation `subtask` have status `completed`
- `blocked_duration` — The thing has been in `blocked` status longer than `threshold`

*(v1.2 removed the speculative `in_progress_count` condition and `warn_overload` action — no domain ever used them. Per "spec when foreseeable, deploy when felt": they return if a domain feels the need.)*

### Relationship-based

Conditions that fire when a connected thing changes in any way.

```yaml
triggers:
  - type: relationship
    watch: parent-project-id
    on: priority_changed
    action: re_evaluate
  - type: relationship
    watch: related-goal-id
    on: status_changed_to
    value: cancelled
    action: surface
```

More general than dependency triggers — watches any relationship, not just blocking dependencies. Useful for propagating priority changes, detecting when a parent goal shifts, or noticing when related context changes.

## Actions

Actions are declarative. They tell the agent what kind of response is appropriate — not how to implement it.

| Action | Meaning |
|--------|---------|
| `surface` | Bring to the user's attention at next opportunity. "This needs your eyes." |
| `re_evaluate` | Load this thing at full context and reason about whether it's still correct (status, priority, scope). |
| `suggest_completion` | Conditions indicate this thing may be done. Propose marking it complete. |
| `unblock` | A dependency has been satisfied. Update status from `blocked` to the appropriate active state. |
| `escalate` | Something has been stuck too long or a risk condition exists. Flag prominently. |
| `cascade` | Check all things downstream of this one (things that depend on it, things it blocks). |
| `notify` | Push through output route (calendar update, notification, reminder). |

## When Triggers Are Evaluated

1. **Session start** — The agent scans active things for trigger conditions. Any that are met get surfaced immediately: "3 things need attention since your last session." This is the primary evaluation point. **At scale, scanning every thing's frontmatter here becomes expensive.** A domain that has grown past the point where this is cheap maintains a `triggers` derived index (`things/_index/triggers.md`) — a regenerable aggregation of every active trigger — and the agent evaluates the index instead of re-reading all things. Index maintenance rides the `post-write` event; evaluation is performed by the `evaluate-triggers` prompt. See `derived-index.md`.
2. **After every write** — When the agent modifies a thing, it checks whether any other things have triggers watching it and cascades accordingly. This is how completing a task automatically surfaces things it was blocking. If a triggers index exists, this same write is when its affected entry is updated (in the same commit).
3. **Scheduled invocation** — An external mechanism (cron job, OS scheduler, GitHub Actions, a recurring calendar event) periodically invokes the agent with a "check triggers" intent.

## Idempotency

A trigger that's true stays true until the condition changes. The agent doesn't need "already fired" state — it reasons about *how long* the condition has been true and responds proportionally:

- First session overdue: "This is now past due."
- Fifth session overdue: "This has been overdue for a week. Should we reprioritise or cancel?"

Git history provides the temporal context. The agent can see when it last mentioned this trigger by reviewing recent commits or worklog entries. No additional state machinery is needed.

## Example

```yaml
---
id: quarterly-review-preparation
type: task
status: not-started
priority: high
created: 2026-05-01
due_date: 2026-06-15
dependencies: [data-collection, stakeholder-feedback]
triggers:
  - type: dependency
    watch: [data-collection, stakeholder-feedback]
    on: status_changed_to
    value: completed
    action: unblock
  - type: time
    condition: due_date_passed
    action: escalate
  - type: threshold
    condition: blocked_duration
    threshold: 14d
    action: surface
---
```

This thing will:
- Surface as unblocked when both dependencies complete
- Escalate if its due date passes without completion
- Surface for attention if it has been blocked for more than 2 weeks
