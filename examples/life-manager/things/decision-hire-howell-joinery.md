---
id: decision-hire-howell-joinery
type: decision
status: made
created: 2026-06-05
tags: [home, renovation]
informed_by:
  - id: task-get-contractor-quotes
    # Always the full 40-hex id — never abbreviated (full-SHA pin rule)
    commit: 219c62e5bcb61d189c57dc9a0deddcf4f3cac09c
linked_things:
  - id: project-kitchen-renovation
    relation: references
---

# Decision: Hire Howell Joinery

## The Choice

Howell Joinery at £4,800, over Brightfit Kitchens (£4,200) and the local
independent (£3,900).

## Reasoning

The deciding factor was the 3-week lead time against Brightfit's 7 — with an
immovable late-August deadline on `project-kitchen-renovation`, the £600
premium buys a month of slack. The independent's quote had no fixed date,
which for a deadline-driven project is the same as no quote.

## Provenance Mechanics (Why This Thing Looks Like This)

This is a `type: decision` — a framework-reserved type. The `informed_by`
field pins the quote-gathering task **at the commit where its figures were
current**. `mdllm provenance` verifies the pin mechanically: the commit must
exist, the input must exist at it, and if the input changes in later commits
the tool reports the decision as possibly dated rather than silently stale.
The pin above is a real commit in this repository — `git show` it — because
`mdllm validate` now resolves every structural pin at the commit boundary, and
a pin that names no commit is an Error there. A plausible-looking SHA is not a
pin; it only looks like one, which is exactly why the floor resolves it rather
than reading it.
If this decision is ever revisited, the new choice gets its own decision
thing that `supersedes` this one — decisions are not edited, they are
replaced.
