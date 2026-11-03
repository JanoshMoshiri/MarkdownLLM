---
id: a-note-on-a-held-ticket-rings-its-addressee-2026-11-02
type: decision
status: made
version: 1.0
created: 2026-11-02
session: 2026-11-02
decided_by: Janosh Moshiri
confidence: high
origin: stated
exposed: false
tags: [a2a, ticket, standing-watch, wake, note, interrupt, double-send, belief-revision]
linked_things:
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    relation: supersedes
    notes: "Only the double-send clause: that ruling answered the optional content-change wake *no* until a live run showed the need. The run arrived on 2026-11-02 and the answer is now yes. Everything else in it stands."
  - id: standing-watch-specification
    relation: informs
    notes: "The Ticket section's one-writer and one-message rules are revised to carry the note, and the watch's board gains a content key for the things at this role's stages."
  - id: substrate-native-a2a
    relation: informs
    notes: "Phase 3's 'double-send question, settled: no' is reopened and answered by this ruling."
  - id: ad-hoc-message-loop
    relation: informs
    notes: "The loop definition's 'only writer' sentence becomes 'only writer of the turn'; a note by another seat rings the addressee without moving the turn."
  - id: the-seat
    relation: references
    notes: "The seat read carries the same event at rest — an unread note on a ticket addressed to this seat — beside the stall ring of Phase 7."
---

# A Note On A Held Ticket Rings Its Addressee

## Context

The ticket's protocol, ruled on 2026-09-30, had one writer at any moment
— the addressee — and one message per turn. The floor made both true
rather than merely asking for them: the watch's board was `{thing_id:
status}` and the diff skipped an unchanged status, so a second write
without moving the addressee reached nobody. Whether to add an optional
content-change wake, to allow a double-send, was deferred: *no, until a
live run shows the need.*

The run arrived on 2026-11-02, in the busiest live workspace. A seat
handed a ticket to a third seat with the next act named as the operator's
merge. The merge landed ten minutes later. The handing seat recorded it
on the ticket as a note, at the same status, and nothing rang; the third
seat sat holding a turn it could not take, waiting for a fact that was
already on the record. The handing seat's own diagnosis was right: the
watch fires only when the ticket passes from one side to the other, and
the ticket was already on the other side. The same seat had written notes
on held tickets twice before, on 29 October, without consequence, because
the holder was already acting.

Read first as a protocol slip — the ticket should have gone to the seat
that would see the merge land — and the recommended fix was a loud
warning on a non-addressee write, with the deferral closed as *no*. The
operator overruled that reading.

## Ruling (the operator's words, 2026-11-02)

> There needs to be an interrupt, or at least a flag set that's picked up
> on the end of processing of a turn to say, hey, this thing that you
> looked at, this note, this communication ticket has changed, and that
> should trigger reevaluation. I think it should be an interrupt, to be
> honest. If that's doable. It works the same way as prompts do when
> they're steering.

A write on a ticket by a seat that does not hold it is a **note**. A note
rings the ticket's addressee the way a steering prompt reaches a running
session: as an interrupt where the harness can deliver one, and as a flag
read at the end of the turn or the start of the next where it cannot.

## What changed

- **The watch** keys the board on content as well as status for the
  things at this role's stages. A body that changes under an unchanged
  status addressed to this role rings it — `ROLE UP: a note landed on
  <id> while it is addressed to you` — unless this seat wrote it. The
  author is read from the commits between the two polls and matched to
  the declared seat the way the self-wake matches its own commits; an
  unknown author is rung, never assumed to be this seat. The holder's own
  writes at its status ring nobody: the other side is not waiting on
  drafts, and reads a quiet `body:` line instead.
- **The seat read** carries the same event at rest. `mdllm seat`, the
  session-start digest and estate-sync report an unread note — a ticket
  addressed to this seat that another seat wrote on since this seat last
  touched it — and `--stall-exit` and `--silence-exit` ring on it. This
  seat's next write on the ticket clears it.
- **The protocol.** The addressee owns the turn; anyone may leave a note.
  A note is appended, never an overwrite of the holder's message, and
  short: two writers on one file can conflict at the holder's next commit,
  and the holder resolves it as its own file. One message per turn still
  describes the turn; the note is the exception the record asked for.

## What follows, and is not done here

- The harness half. Claude Code delivers a background command's exit
  mid-turn at the agent's next tool boundary, which is the steer the
  operator described; idle, it starts a turn. Hermes starts a turn on the
  process exit. Neither has been exercised on a note yet, and the live
  round trip with no human relay that `substrate-native-a2a` Phase 4 owes
  is owed for the note as well as the turn.
- The upstream slip stands as advice, not rule: a ticket is addressed to
  whoever's act is next, and when that act is a human's or the world's,
  the seat that will observe it holds the ticket.
