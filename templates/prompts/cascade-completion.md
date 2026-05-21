---
id: cascade-completion
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: completed-thing
    description: "The thing whose status just changed to completed"
  - name: downstream-things
    description: "All things that reference the completed thing in dependencies, blocks, or trigger watch lists"
outputs:
  - name: status-changes
    description: "Things whose status should change as a result"
  - name: surfaced-items
    description: "Things to bring to the user's attention"
bound_to:
  - hook: on-status-change
    when: "new status is completed"
  - hook: post-write
    when: "a thing was marked completed"
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: thing-specification
    relation: operates-on
---

# Cascade Completion

## Purpose

When a thing is completed, evaluate what it unblocks and what should change downstream. This is the primary mechanism for automatic progress propagation.

## Reasoning Template

Given the completed thing, perform these evaluations in order:

### 1. Direct Dependency Resolution

Find all things where `dependencies` includes the completed thing's ID.

For each:
- Are **all** of its dependencies now completed? → Change status from `blocked` to `not-started`
- Are **some** but not all resolved? → No status change, but note progress

### 2. Trigger Evaluation

Find all things with `triggers` of type `dependency` that `watch` the completed thing.

For each:
- Does the trigger condition match? (e.g., `on: status_changed_to`, `value: completed`) → Execute the trigger's declared action
- Common actions: `unblock` (change status), `surface` (notify user), `re_evaluate` (reassess the thing)

### 3. Parent Completion Check

If the completed thing has a `parent`:
- Load all siblings (things sharing the same parent)
- Are all siblings now completed? → Suggest completing the parent
- Is a threshold trigger on the parent now satisfied? → Fire it

### 4. Critical Path Awareness

Among the things just unblocked:
- Is any `priority: critical` or `priority: high`? → Surface immediately with emphasis
- Does unblocking create a new longest chain? → Note it for the user

## Output Format

Report to the agent (not directly to user) in this structure:

```
Cascade results for [completed-thing-id]:
- Unblocked: [list of thing IDs moved from blocked → not-started]
- Triggered: [list of trigger actions that fired]
- Parent status: [suggest-completion | partial-progress | n/a]
- Attention: [high-priority items that are now actionable]
```

The agent then incorporates this into its response to the user.
