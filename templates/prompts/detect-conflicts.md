---
id: detect-conflicts
type: prompt
status: stable
version: 1.1
created: 2026-05-20
inputs:
  - name: proposed-change
    description: "Change mode: the modification the agent is about to make (thing ID, field, old value, new value)"
  - name: affected-thing
    description: "Change mode: full context of the thing being modified"
  - name: relationship-index
    description: "Scan mode: the domain's relationships index (things/_index/relationships.md), if it maintains one — the edge list for systematic scanning"
  - name: domain-lenses
    description: "Reasoning lenses defined in the domain specification (if any)"
outputs:
  - name: conflicts
    description: "List of detected conflicts with severity and affected parties"
  - name: recommendation
    description: "proceed, warn-and-proceed, or block-and-ask (change mode); or conflict things to create (scan mode)"
bound_to:
  - hook: post-write
    when: "a significant change is proposed (status, priority, scope, or deletion)"
  - hook: on-status-change
    when: "a spec moves to stable, or an insight is promoted — its claims now carry full weight and should be checked against the corpus"
  - hook: retrospective
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: write-thing-specification
    relation: integrates-with
  - id: belief-revision-specification
    relation: integrates-with
  - id: derived-index-specification
    relation: operates-on
---

# Detect Conflicts

## Purpose

Catch problems that structural validation won't — logical contradictions, lens
conflicts, and domain rule violations. This prompt runs in two modes.

## Two Modes

**Change mode** (bound to `post-write`) — the original use: before a single
significant change is finalised, check whether *that change* conflicts with existing
state. Reactive, narrow, cheap. Use the Reasoning Template below.

**Scan mode** (bound to `on-status-change` and `retrospective`) — proactive: sweep the
corpus for contradictions that already exist but no one has flagged. The framework's
belief-revision machinery (`belief-revision.md`) is only as good as the moment a
conflict is *noticed*; change mode only notices conflicts a fresh edit introduces. Scan
mode is how standing contradictions get found.

### Scan Mode Reasoning

Triggered when claims gain weight or at periodic reflection:

- **On `on-status-change`** — a spec moved to `stable`, or an insight was promoted. Its
  assertions now carry full authority. Scope the scan to *that thing and its immediate
  neighbours*: load its `linked_things` (Level 2), and check whether its now-authoritative
  claims contradict any neighbour. This is a small subgraph — a few things, ~3–6k tokens.
- **On `retrospective`** — full-domain sweep. Use the `relationships` index
  (`things/_index/relationships.md`) if the domain maintains one: walk edges of type
  `informs`, `implements`, `extends`, and for each pair load Level 2 only for the
  endpoints and check for contradiction. The index keeps this affordable (see
  `derived-index.md`); without it, fall back to a Level 2 load of all things, which is
  why the full sweep is reserved for retrospective cadence.

For any contradiction found in either mode, hand off to `belief-revision.md`: create a
`type: conflict` thing with `origin: inferred`, `confidence: low`, add `contradicts`
links to both parties, and surface for human confirmation before committing. Be
conservative — flag genuine semantic contradiction, not difference in emphasis or scope.

## Reasoning Template (Change Mode)

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
