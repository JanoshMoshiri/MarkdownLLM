---
id: a-cleanup-is-scoped-by-lifecycle-not-by-location
type: insight
status: active
version: 1.0
created: 2026-08-17
confidence: high
origin: stated
disposition: keep-active
disposition_reason: "A standing behavioural lesson about disposal ordering, not work any one live thing consumes. Manufacturing an inbound edge to a plan it does not inform would be worse than holding it unattached; it applies to every session that deletes anything."
source: session — deleted a task-output directory while a running command was still writing its log into it
session: 2026-08-17
tags: [agent-behaviour, disposal, ordering, irreversibility]
linked_things:
  - id: consequence-is-recoverable-only-in-retrospect
    relation: extends
    notes: "The standing truth says defer the irreversible; this names the specific blind spot that makes a disposal look reversible when it is not — the dependents are not in the listing."
  - id: claude-phase6-no-adapter-and-root-2026-08-16
    relation: references
    notes: "The sitting where both instances occurred, and whose verification figures nearly went with them."
---

# A Cleanup Is Scoped By Lifecycle, Not By Location

## The Insight

"Clean up the scratchpad" reads as a place. It is actually a lifecycle: the set
of things nothing still depends on. Those two sets look identical in a directory
listing and are not the same set, because a listing shows what is *in* a place
and never shows what still *depends* on it.

A running process is a dependent that no `ls` will ever reveal.

## The Evidence

Two instances in one sitting, the same shape both times.

**The disposal.** Asked to clear leftovers, I enumerated by location and deleted
the task-output directory — while one of my own commands was still writing its
log into it. The command completed; its output was gone. I had destroyed the
record of the very verification I was running, and only because I was still
holding the result in context did nothing need repeating.

**The location choice.** Earlier the same sitting, I pointed an eight-minute
test suite at a basetemp inside an already deeply nested scratchpad. The path
crossed Windows' 260-character limit and two tests failed on it. One second of
checking beforehand would have cost nothing; discovering it afterwards cost the
whole run.

Different acts, one shape: **the place carried an obligation the instruction did
not name.** Neither was a hard question — both were cheap to check before and
expensive to discover after.

## Why It Matters

Disposal is the irreversible class. The standing truth already says to defer
what cannot be taken back — but that only helps if the act *looks* irreversible,
and a cleanup does not. It looks like tidying. The reversibility judgement is
made against the visible contents, while the thing that makes it irreversible is
an invisible dependent.

The generalisation beyond deletion: any step whose target is named by *place*
rather than by *state* inherits obligations that the instruction did not mention
and the listing will not show.

## How To Apply

- **Before deleting, enumerate consumers, not contents.** What is still running,
  still reading, still cited? Anything in flight is a consumer.
- **Sequence disposal after quiescence,** not after the instruction. "Clean up"
  is not a moment; it is a condition.
- **When something is cited as evidence, check the citation survives the
  disposal** — or record the loss as a stated limit before it happens, not after.
- **When choosing a location for an expensive operation, check the location's
  constraints first.** Path length, nesting, whether it sits inside a repository
  worktree. The command does not carry those; the place does.
