---
id: a2a-conversations-run-on-their-own-branch-2026-10-09
type: decision
status: made
version: 1.0
created: 2026-10-10
session: 2026-10-09
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [a2a, ticket, branch, worktree, concurrency, turn-taking, merge, git]
linked_things:
  - id: loop-turns-self-heal-2026-09-23
    relation: extends
    notes: "Inside one conversation nothing changes: turns alternate, a turn is real only on the remote, and the agent who holds a rejected turn pulls, merges and pushes again. This ruling removes the cause of rejection between conversations."
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    relation: extends
    notes: "The ticket becomes one per conversation rather than one per pair, and names its branch by its own id."
  - id: a-shared-worktree-merges-authorship-at-the-index
    relation: references
    notes: "Its fix — a working copy of one's own — is applied here per conversation, the unit that never writes concurrently."
  - id: git-workflow-specification
    relation: references
    notes: "Its Branching section parked multi-hand branching as a future consideration with main as the agreed truth; this is the first case built."
---

# A2A Conversations Run On Their Own Branch

## Context

The operator ran four agents in one workspace from two clones — a developer
and a reviewer on each — all taking turns through the agent-to-agent loop. A
turn passes by publishing a commit (`loop-turns-self-heal-2026-09-23`), and
every conversation published to the same branch. Within one conversation
that never diverges: only one side holds the turn. Between conversations it
always does: each turn one pair publishes moves `main` under the other pair,
whose next push is refused and must be pulled, merged and pushed again — a
merge per turn, multiplied by every pair at once. A pull that stops on a
conflict leaves the clone mid-rebase on a detached HEAD, and two agents
sharing one working copy then build on it. The live record shows the shape:
in the busiest live workspace most of the last 25 commits are ticket, reply
and record turns, one is a sync merge, and a local clone stood 11 behind
another.

## The Ruling

In the operator's words, 2026-10-09: *"it feels to me like actually the way
to do it for A2A communication, there needs to be like a branching. So it
creates a separate branch to do the A2A communication. And then once the
communication is concluded, that branch gets merged in."* The concern it
answers: *"concurrent development with multiple agents, all using A2A in a
single domain, even if their clones, becomes problematic."* The shape was put
back to him the same day and he asked for it as a plan.

1. **A conversation runs on its own branch.** `a2a/<ticket-id>`, cut from
   `main` when the conversation opens. Its turns, and the in-repository
   documents it revises, go there; `main` moves only when a conversation
   concludes. Concurrent conversations never touch each other's branch, so
   the divergence between them is removed at the source, not managed.
2. **A conversation has a working copy of its own in each clone.** Two
   working copies cannot check out one branch, and the two sides of one
   conversation never write at the same time — so the unit of isolation is
   the conversation, not the agent: one linked working copy per conversation
   per clone, shared by its two parties, beside the workspace at the same
   depth so the framework is found the same way.
3. **The end is a fact the floor can read: the ticket closes.** The live
   record closes conversations by closing their ticket; a PR merging
   elsewhere reaches the workspace only through a later record commit. The
   ticket becomes one per conversation, not one per pair.
4. **The merge keeps every turn.** A real merge commit, never a squash: the
   floor's commit pins are checked by existence, so a squashed and deleted
   branch would leave every `informed_by` pin made on it pointing at
   nothing, and a regulated workspace wants the conversation on the record.
5. **The merge is a commit the floor validates, and the reckoning keeps it
   from being forgotten.** The agent holding the last turn concludes the
   conversation into `main`; the commit gate, the pre-commit floor and
   publication run on it as on any commit. A merge git cannot make cleanly
   is the operator's. A concluded conversation left unmerged, or one gone
   quiet without concluding, is an attention item at the next close.

## Open

One ruling is still the operator's: whether the floor may *prepare* a merge
git can make cleanly (`git merge --no-ff --no-commit`), leaving the commit
to the agent, or only name the commands. Recommended: prepare. The line
"the floor never merges" protects judgement, and a clean merge holds none;
the act that lands it — the commit — stays the agent's and is validated.
Until he rules, the conclude step names the commands.

## What This Settles

- `main` stays the agreed truth; a conversation's turns are not on it until
  it concludes, so orientation and the dispatcher read a conversation only
  once it lands. Work under review is not accepted state.
- Inside a conversation nothing changes: alternation, publication as the
  turn, the self-heal of a rejected push.
- Exploration branches and person-to-person branching stay where
  `git-workflow.md` parked them.
- Claude Code and local clones first; cloud clones and Codex after, as for
  every gate this month.
