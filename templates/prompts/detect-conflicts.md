---
id: detect-conflicts
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: proposed-change
    description: "The modification the agent is about to make (thing ID, field, old value, new value)"
  - name: affected-thing
    description: "Full context of the thing being modified"
  - name: domain-lenses
    description: "Reasoning lenses defined in the domain specification (if any)"
outputs:
  - name: conflicts
    description: "List of detected conflicts with severity and affected parties"
  - name: recommendation
    description: "proceed, warn-and-proceed, or block-and-ask"
bound_to:
  - hook: post-write
    when: "a significant change is proposed (status, priority, scope, or deletion)"
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: write-thing-specification
    relation: integrates-with
---

# Detect Conflicts

## Purpose

Before a significant change is finalized, check whether it conflicts with existing state, domain constraints, or reasoning lenses. This prompt catches problems that structural validation won't — logical contradictions, lens conflicts, and domain rule violations.

## Reasoning Template

### 1. Dependency Conflicts

If the proposed change is a status change:

- **Completing a thing with incomplete dependencies** → Block. Something is wrong — either the dependencies were wrong or the thing isn't actually complete.
- **Cancelling a thing that other things depend on** → Warn. Those downstream things will be permanently blocked unless redirected.
- **Unblocking without resolving the blocker** → Warn. Ask what changed.

### 2. Priority Conflicts

If the proposed change involves priority:

- **Elevating priority without adjusting capacity** → Warn if `in_progress_count` is already at threshold. Something else may need to deprioritize.
- **Lowering priority of something with approaching due date** → Warn. The user may be procrastinating or may have a good reason.

### 3. Lens Conflicts

If the domain defines reasoning lenses (in its specification skill):

- Evaluate the proposed change through each lens
- If all lenses agree → No conflict
- If lenses disagree → Report the tension, recommend `block-and-ask`

Example:
```
Domain Logic: "Yes, consolidate the data"
Compliance Logic: "No, violates data minimization"
→ Conflict detected. Block and ask user to resolve.
```

### 4. Scope Conflicts

If the proposed change modifies scope (narrative body, splitting, merging):

- **Splitting a thing that has external dependencies pointing at it** → Warn. Which subthing inherits the dependency?
- **Merging things with different statuses** → Warn. What's the resulting status?
- **Changing scope without updating linked things** → Warn. Related things may have stale references.

## Decision Matrix

| Conflict Type | Severity | Action |
|---------------|----------|--------|
| Dependency violation | High | Block — don't proceed without user decision |
| Lens conflict | High | Block — surface the tension, let user decide |
| Capacity overload | Medium | Warn — proceed but flag the tradeoff |
| Scope ambiguity | Medium | Warn — suggest resolution, proceed if user confirms |
| Priority/date mismatch | Low | Note — mention once, don't block |

## Output Format

```
Conflict check for [proposed-change]:
- Conflicts found: [count]
  - [severity]: [description] — affects [thing IDs]
- Recommendation: proceed | warn-and-proceed | block-and-ask
- Resolution needed: [description of what the user must decide, if blocking]
```

## When NOT To Run

Skip this prompt for trivial changes:
- Updating narrative text without changing scope
- Adding tags
- Fixing typos in metadata
- Changes that only affect the thing itself with no downstream impact

The `post-write` binding should include `when: "a significant change is proposed"` to avoid unnecessary overhead on minor edits.
