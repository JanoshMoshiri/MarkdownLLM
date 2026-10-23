---
id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
type: decision
status: made
version: 1.1
created: 2026-10-15
session: 2026-10-15
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [seat, clone, identity, a2a, ticket, work-item, generated-block, version, loop, evidence]
linked_things:
  - id: a2a-conversations-run-on-their-own-branch-2026-10-09
    relation: extends
    notes: "That ruling's evidence read (2026-10-14) found three causes of the trouble larger than the turn race it targets; this ruling answers those three, and leaves the branch plan behind it in order."
  - id: a2a-conversations-run-on-their-own-branch-2026-10-09
    relation: superseded-by
    notes: "2026-10-24: only ruling 3's end clause is replaced by an explicit conclusion by either party. Seats, the version guard, work-item identity and roles remain in force."
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    relation: extends
    notes: "The ticket becomes one per work item rather than one per pair, and `closed` means nothing is owed rather than finished."
  - id: loop-turns-self-heal-2026-09-23
    relation: references
    notes: "A turn that never left is now named at the seat's own session start, not only by the watch on the other side."
  - id: a-shared-worktree-merges-authorship-at-the-index
    relation: references
    notes: "The seat is where that insight's fix is declared: one agent, one working copy, one identity."
  - id: standing-watch-specification
    relation: references
    notes: "The Ticket section carries the work-item shape and the seat; the definition template declares the reopen edge."
---

# Seats Are Declared, And A Conversation Is A Work Item

## Context

On 2026-10-14 the operator asked for the evidence rather than anyone's
view: *"I want us to focus less on my view and opinion and more on the
evidence of what is."* The busiest live workspace's whole history was read
at one pinned commit by three independent readers (recorded on the branch
ruling, *The Evidence — Read 2026-10-14*). What it found, in order of size:

1. **Two clones on different framework versions rewrote one generated
   block in turns** — fifteen times in two days — blocking commits and
   expiring session gates until both reached the same release.
2. **Turns that never left:** commits made in a clone and not published
   for 35 and 13 hours, invisible to their addressee.
3. **Two agents in one working copy**, colliding on the git index.
4. **The turn race** between concurrent conversations — real, and the
   smallest of the four.

None of the first three is anything a branch per conversation fixes, and
all three were invisible in the record itself, because every agent
committed under the operator's git identity. The ticket, meant as one
conversation, carried many: `closed` was used to mean *nothing is owed
now*, fifty-seven of eighty-one conversations reopened, and the real end
of each — the change merged, the specification approved — was recorded on
the work item, not the ticket. An external-harness agent's recorded
incidents were channel and turn mechanics, not judgement; nothing it
loaded pointed it at the loop it was running, and the loop definition was
mostly history.

## The Ruling

In the operator's words, 2026-10-15: *"the biggest problem is a
configuration problem between clones and versions of things on those
clones … that's a problem that's bigger than just A2A communication … I
don't want to try and fix the world in one place. I want to break out into
its sensible places."* On the shape of a loop: *"there doesn't always have
to be three agents in the loop … otherwise, we just do this whole thing
with two."* And on proceeding: *"The evidence is there. I'm closing the
loop. Do what needs to be done."*

1. **A seat is declared.** One agent, in one clone, on one framework,
   under one git identity. It is declared in the clone — clone-local
   config, never the corpus, because clones share a corpus and a seat is a
   property of one of them — with `mdllm seat . --set <actor>`, which also
   sets the clone's git identity to the seat so every commit says who sat.
   The floor reads it: the session-start digest names the seat and any
   turn it committed that never left; doctor warns when a workspace that
   runs loops has an undeclared seat. The floor never declares one.
2. **A clone behind the framework that wrote a workspace's generated
   blocks does not rewrite them.** The entry file records the generating
   framework commit; regeneration, refresh and the drift checks compare
   this clone's framework to it by version and by ancestry, refuse when
   behind, and read the difference as *behind*, never drift.
3. **A conversation is a work item.** A ticket is one per work item,
   `ticket-<item>`, never per pair. `closed` means nothing is owed now; a
   reopen is a declared move. **Amended 2026-10-24:** either party
   explicitly concludes the conversation, as ruled in
   `a2a-conversations-run-on-their-own-branch-2026-10-09`. The original
   item's-end clause is superseded; work-item identity remains in force.
4. **Roles, not agents; seats, not roles.** A loop definition names its
   roles and the actor at each stage, never which agent holds which role
   — that is assigned by the ticket or run that commissions the work, and
   rotates. Two seats is the default shape. A third seat that forwards
   another's actions to a service it cannot reach is a publisher: it holds
   no stage and carries no judgement.
5. **A loop definition is operative rules only, entered by role.** Its
   history goes to the record. A simpler model entering as the builder, the
   writer or the reviewer reads its own entry and the shared channel, and
   nothing else.

## What This Settles

- The branch-per-conversation ruling stands; its four implementation
  questions were answered by the operator on 2026-10-24 in that decision's
  amendment. Its plan follows this one in order, because it
  addresses the smallest of the four causes and needs seats first.
- The framework carries 1, 2, and the templates and spec for 3 and 4; a
  workspace carries its own definitions and skills. Both halves were built
  the day of the ruling, the workspace's on the operator's explicit
  instruction to the framework session.
- The guard takes effect across an estate only once every clone runs a
  framework that has it; until the next release, no generated block's
  output changes, so the clones on the published release and the clones
  ahead of it write the same bytes.
