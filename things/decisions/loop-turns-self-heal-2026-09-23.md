---
id: loop-turns-self-heal-2026-09-23
type: decision
status: made
version: 1.0
created: 2026-09-23
session: 2026-09-23
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [standing-watch, a2a, loop, divergence, publication, self-heal, floor-vs-agent]
informed_by:
  - id: standing-watch-specification
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
  - id: git-workflow-specification
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
  - id: substrate-native-a2a
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
linked_things:
  - id: standing-watch-specification
    relation: informs
    notes: "Adds a floor row to the division of labour: the watch reports its own clone's unpublished or diverged turn and wakes this role with the reconcile instruction. 0.2 → 0.3."
  - id: git-workflow-specification
    relation: informs
    notes: "The kernel's turn-taking paragraph gains the sentence that closes the gap it named: the watch says so, on the side that can see it."
  - id: substrate-native-a2a
    relation: informs
    notes: "The loop's silent drop-off, seen in the field, and the phase that fixes it."
  - id: between-sessions-surface-is-real-2026-09-21
    relation: extends
    notes: "The watch was specified to read the ref and nothing else. This adds one local read, for the one failure the ref cannot show."
---

# Decision: A Loop Turn That Never Left Wakes Its Own Side

## Context

Two instances take turns through the repository. A turn is real when its new
state is visible on the remote — the kernel says so, and `standing-watch.md`
assigns "confirm the turn has passed, from the ref" to the agent. In the
field that assignment is not met: the committing side's push is rejected
(the remote moved under it), `autopush` records `rejected` and exits 0 as a
post-commit hook must, the session ends, and the only party who could act
never reads the line. The other side's watch reads the remote ref and only
the remote ref, so silence there is indistinguishable from "no turn yet".
One side of the loop drops off the list and both sides wait.

## The Ruling

The operator, 2026-09-23:

> "I want the two agent loop to self heal. So when the watcher catches the
> divergence, it posts that back to the agent that did not manage to push to
> the remote. And it tells that agent to do a pull merge and then push
> again. So we have that automated — a healing effect for that symptom."

**The watch also watches its own clone.** Each poll, beside the ref read it
already makes, it compares the local branch to the remote head. Local ahead
of the ref, or diverged from it, is an unpublished turn: the watch emits it
as a wake for *this* role with the instruction — pull, merge, push again —
and exits as it would for any wake. Behind or equal is nothing. It wakes
once per local tip, so an agent that has not yet acted is not woken every
poll, and one that commits again without publishing is woken again.

## Where the line stays

The floor still reports and never resolves. The watch does not pull, merge
or push; it says what it sees and rings. The merge is the agent's, because
the agent whose turn it is owns the decision the kernel says a rejected push
owes — and a merge it cannot make cleanly is filed to the seat, not guessed.
`autopush` is unchanged: exit 0, never forced. Nothing crosses to the other
side; the heal happens on the side that can see the debt, which is the only
side that can.

## Consequences

- `mdllm watch`: one local read per poll; a new wake line; `woke_unpublished`
  persisted in the state so the wake is once per tip.
- `standing-watch.md` 0.2 → 0.3: a floor row in the division of labour; the
  agent's row narrows to the merge itself.
- `git-workflow.md` kernel: one sentence in the turn-taking paragraph.
- `substrate-native-a2a`: the residual is named and closed by the build, not
  carried.
