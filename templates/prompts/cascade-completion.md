---
id: cascade-completion
type: prompt
status: stable
version: 1.1
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
    relation: implements
  - id: thing-specification
    relation: references
---

# Cascade Completion

## Purpose

When a thing is completed, evaluate what it unblocks and what should change downstream. This is the primary mechanism for automatic progress propagation.

## Gather mechanically, dispose semantically

The downstream walk is mechanical — it is set membership over declared edges, exactly the kind of work the kernel forbids re-deriving by reasoning (`validate.thing.md`: *never re-perform a mechanical check by reasoning*). So **run the tool, then dispose of what it reports**:

```
python {framework_root}/tools/mdllm.py cascade <completed-thing-id> [domain-path]
```

`mdllm cascade` is the outbound mirror of `mdllm touchpoints`: where touchpoints answers *"what did I just put at risk?"*, cascade answers *"what did I just unblock?"*. It returns, for the completed thing:

- **Unblock candidates** — things whose every prerequisite (read from both `dependencies` and the reverse `blocks` edge) is now terminal, priority-flagged.
- **Partial progress** — downstream things still waiting on other prerequisites.
- **Parent rollup** — whether the parent's children are now all terminal (a completion candidate).
- **Trigger watchers** — things whose `triggers` watch the completed thing; evaluate these with `mdllm triggers`, which owns trigger evaluation.

It **reports candidates; it never applies a status change** — that is this prompt's job.

## Disposition (yours)

For each candidate the tool surfaces, decide — the part no edge can settle:

- **Unblock candidate** → does the thing's *narrative* hold a soft blocker the declared edges cannot see? If not, change its status (typically `blocked` → `not-started`) and cascade onward from that change.
- **Parent completion candidate** → *suggest* completing the parent to the user; do not auto-complete a parent.
- **Priority-flagged** unblocked work → surface it immediately, with emphasis, and note if it creates a new longest chain.
- **Trigger watcher** → run `mdllm triggers` and act on its declared action.

Then incorporate the dispositions into your response to the user. The mechanical set is the tool's; the judgment is yours.
