---
id: a2a-conversations-run-on-their-own-branch-2026-10-09
type: decision
status: made
version: 1.3
created: 2026-10-10
session: 2026-10-09
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [a2a, ticket, branch, worktree, concurrency, turn-taking, merge, git]
linked_things:
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: supersedes
    notes: "2026-10-24: replaces only ruling 3's conversation-end clause with an explicit conclusion by either party. Its seat, version-guard, work-item identity and role rulings remain in force."
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
   source, not managed. (The contents ruling is settled in the
   2026-10-24 amendment below.)
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

## Questions Held Open — 2026-10-10 (Answered 2026-10-24)

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
wait."* These questions held Phases 1, 3 and 4 until the operator answered
the plan's reminder on 2026-10-24, below. This section preserves the earlier
options and leanings; the answers below govern implementation.

## Four Implementation Rulings — 2026-10-24

Janosh Moshiri answered all four through the native choice prompt during
session start:

1. **End:** *"A party explicitly concludes the conversation."* Either
   party's explicit conclusion is the end signal. The implementation must
   record that declaration in committed state so the watch and reckoning
   can read it. A ticket closing still means nothing is owed now; neither
   that close nor the underlying work item's completion substitutes for an
   explicit conclusion. This replaces only the end clause of ruling 3 in
   `seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15`;
   conversation identity remains one per work item.
2. **Landing:** *"Merge once, preserving turn history."* Land the
   conversation branch on `main` once at its conclusion, through a merge
   commit preserving the turns. The existing requirement that the landing
   commit runs the floor remains in force; branch commits remain reachable
   through that history, including any commit pins they carry.
3. **Contents:** *"Conversation records only; work commits go to main."*
   Tickets and review records travel on the conversation branch; changes
   to the work being discussed are committed to `main` at their normal
   meaning boundaries. The earlier evidence that 36% of turns also wrote
   durable work remains evidence of the split the implementation must
   support. Conversation branches isolate turn traffic; concurrent work
   commits still share `main` and can require reconciliation.
4. **Preparation:** *"Allow preparation; the agent makes the validated
   commit."* The floor may prepare a merge Git can make without conflicts.
   The agent makes the landing commit through the commit gate and
   pre-commit validation. A merge with conflicts remains the operator's.

The four design holds are answered. This records the contract for the
existing build plan; none of its implementation phases is marked delivered
by these answers. The fired 2026-10-23 questions reminder is disarmed on the
plan; its implementation and seat prerequisites remain visible there.

## The Evidence — Read 2026-10-14

At the operator's ask (*"focus less on my view and opinion and more on the
evidence of what is"*), the busiest live workspace's whole history was read
at one pinned commit: 1,230 commits, 24 ticket files, 378 ticket revisions
across 315 commits since 2026-10-01. Three independent readers, each
read-only. What the record says against each open question, with its
limits:

**On 1, what ends a conversation.** `closed` means *nothing is owed right
now*, not *finished*. Of 81 conversations (a run of turns ending in
`closed`; median 3 turns, 17 minutes), 57 were reopened — 63% continuing
the same item, 21% moving to the next item of the same run, 16% starting
a new topic. Only 2 of 77 closes followed the item's real end (a merge).
The real end — the artefact merged, the specification approved — is
recorded elsewhere, usually after the close, and three threads were never
closed at all. No workflow run reached a terminal stage in the window.
*Inference at the time:* the durable unit is the work item (the change
under review, the specification set), not the ticket round; a
conversation's end is that item's end. The 2026-10-24 ruling retains the
work-item identity and replaces that inferred end signal with an explicit
conclusion by either party.

**On 2, how it lands.** No merge in the window touched the same file on
both sides; the collisions were between turns, not content. Nine merges
in two weeks: five quick ones on one night, each joining a local turn
under four minutes old with a remote one — the turn race this ruling
targets — and two long divergences (a dispatcher commit unpublished for
35 hours; one party's turn unpublished in another clone for 13 hours, so
its addressee could not see it).

**On 3, what the branch carries.** 36% of turn commits also write
durable things in the same commit — specifications, run records, review
records, decisions. One party's turns are almost all ticket-only (71 of
73) because its output is the state of the external pull request. A
branch carrying the conversation only would have to split a third of the
turns as they are made today.

**What went wrong, in order of size.** (1) Two clones on different
framework versions fought over a generated block in the entry file: one
rewrote it fifteen times, the others kept restoring it; it blocked commits
and expired session gates, and stopped when every clone reached 3.47.0.
(2) Turns that never left — the two long divergences above. (3) Two
agents in one working copy and one git index, colliding on the index
lock. (4) The turn race: real, and the smallest of the four. The record
never mentions a detached HEAD. Three of the four are not what a branch
per conversation fixes.

**On the second loop and the simpler-model question.** Of 43 recorded
incidents since 2026-09-07, the external-harness agent is named in ten,
eight of them channel and turn mechanics (watch not running, a false
"turn never left" from a shared checkout, heartbeat workarounds the
operator rejected, the external review channel blocked or returning
errors, the wrong pair asked to publish); none records a wrong review
judgement by it. Nothing it loads points it at a loop definition — the
workspace's entry file says no workflow is in force — and the instructed
reading path is roughly 21,000 words, the loop definition itself 61%
version history with role-specific rules under a tenth of its text. The
definitions were last edited 2026-09-22 and 2026-09-29; October's rules
live in tickets and decisions.

**Limits.** Every non-external commit shares one git identity, so who
acted comes from ticket direction and the records' own text. Push times
are not recorded. Relatedness of a commit to a conversation is a reading,
not a fact. The pull-request threads live outside the repository.

## What This Settles

- `main` stays the agreed truth; a conversation's turns are not on it until
  it concludes, so orientation and the dispatcher read a conversation only
  once it lands. The work being discussed continues to commit to `main`.
- An explicit conclusion by either party ends the conversation; the merge
  preserves its history and lands once. The floor may prepare a clean
  merge, and the agent makes the validated landing commit.
- Inside a conversation nothing changes: alternation, publication as the
  turn, the self-heal of a rejected push.
- Exploration branches and person-to-person branching stay where
  `git-workflow.md` parked them.
- Claude Code and local clones first; cloud clones and Codex after, as for
  every gate this month.
