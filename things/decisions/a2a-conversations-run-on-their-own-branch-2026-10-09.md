---
id: a2a-conversations-run-on-their-own-branch-2026-10-09
type: decision
status: made
version: 1.1
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
   `main` when the conversation opens; its turns go there and land on
   `main` when it concludes. Concurrent conversations never touch each
   other's branch, so the divergence their turns cause is removed at the
   source, not managed. (What else the branch carries is open, below.)
2. **A conversation has a working copy of its own in each clone.** Two
   working copies cannot check out one branch, and the two sides of one
   conversation never write at the same time — so the unit of isolation is
   the conversation, not the agent: one linked working copy per conversation
   per clone, shared by its two parties, beside the workspace at the same
   depth so the framework is found the same way.
3. **The landing is a commit the floor validates, and the reckoning keeps
   it from being forgotten.** Whoever concludes the conversation lands it on
   `main` through a commit the commit gate, the pre-commit floor and
   publication run on, like any other. A merge git cannot make cleanly is
   the operator's. A concluded conversation left unlanded, or one gone quiet
   without concluding, is an attention item at the next close.

## Open — The Operator's, To Weigh Before Phases 1, 3 And 4

A first draft of this record (a98ad97) wrote three of these as settled from
the live record and the floor. The operator corrected it on 2026-10-10: they
are his, he wants to think through the options and implications, and he
will answer later. His leanings, in his words, with what each would mean:

1. **What ends a conversation.** *"What ends the conversation, which is a
   difficult one. I'm going to have to go into my options in that."*
   Candidates on the record: the ticket closing (what the live workspace
   does today); the PR it is about merging; an explicit conclude by either
   party; a run reaching its terminal stage. What any answer needs: the end
   must be a fact the floor can read inside the workspace, or the reckoning
   cannot chase a conversation that ended and never landed.
2. **How it lands.** *"I don't think we should merge every turn.
   Conversation should stay until the end, and then it merges in at the
   end."* The conversation stays on its branch and lands once, never turn
   by turn — the shape the plan already takes. Still open within it:
   whether the landing keeps the turns as history (a merge commit) or
   brings them as one commit (a squash). What a squash would mean: commit
   pins made on the branch are checked by existence, so once the branch is
   deleted they point at nothing — unless the branch is kept, or pins on a
   conversation are made only against `main`.
3. **What the branch carries.** *"In my mind, I thought the branch only
   should carry the conversation because then normal commits will happen at
   normal times."* The tickets and review records ride the branch; the work
   itself is committed to `main` as it happens. What that would mean: two
   pairs revising documents at once would still publish to one branch, so
   their work commits — not their turns — could still refuse each other's
   pushes: far fewer collisions than today, not none.
4. **May the floor prepare a clean merge?** Whether the floor may set up a
   merge git can make cleanly and leave the commit to the agent, or only
   name the commands. Recommended: prepare — "the floor never merges"
   protects judgement, and a clean merge holds none; the commit that lands
   it stays the agent's and is validated.

*"I need to think about all of those things, the implications, so I have to
wait."* Nothing that depends on them is built until he rules; the plan's
trigger puts them back to him in one prompt.

## What This Settles

- `main` stays the agreed truth; a conversation's turns are not on it until
  it concludes, so orientation and the dispatcher read a conversation only
  once it lands.
- Inside a conversation nothing changes: alternation, publication as the
  turn, the self-heal of a rejected push.
- Exploration branches and person-to-person branching stay where
  `git-workflow.md` parked them.
- Claude Code and local clones first; cloud clones and Codex after, as for
  every gate this month.
