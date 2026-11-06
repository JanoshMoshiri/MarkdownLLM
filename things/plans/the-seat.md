---
id: the-seat
type: plan
status: in-progress
version: 1.4
created: 2026-10-15
session: 2026-10-15
priority: critical
tags: [seat, clone, identity, generated-block, version-guard, ticket, work-item, a2a, watch]
linked_things:
  - id: the-felt-symptom-names-one-cause-the-record-ranks-them
    relation: references
    notes: "How this plan came to exist: the remedy that arrived with the felt symptom addressed the smallest cause; one pinned read of the record ranked the rest, and this plan builds them in that order."
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: implements
    notes: "The ruling this plan builds."
  - id: a2a-conversations-on-their-own-branch
    relation: references
    notes: "Follows this plan in order: the branch addresses the smallest of the four causes the evidence found, and its doorbell phase needs the seat."
  - id: standing-watch-specification
    relation: extends
    notes: "The Ticket is per work item with a declared reopen; actors are seats."
  - id: the-reckoning
    relation: references
    notes: "The next arc after this one, by the operator's ordering."
  - id: a-ring-is-calibrated-on-the-healthy-rhythm-not-the-failures
    relation: references
    notes: "What Phase 7's calibration correction taught: the window is the healthy rhythm's tail, the ceiling silences the forgotten; harvested at the 2026-11-06 close."
triggers:
  - type: time
    condition: "2026-11-20 reached"
    action: surface
    note: "Answered 2026-11-06 by citation: both clones had declared seats by 2026-11-02 — and the first declaration was wrong by naming, caught by an occupant change, not by the digest (seats-are-named-for-the-clone-not-the-agent-2026-10-30); the root vocabulary followed on 2026-11-03 (ad-hoc-message-loop 1.4, release 3.51.0). Whether any generated block was rewritten in turns is still unread; the second clone's log is on this machine since the merge of 2026-11-02, so the next look reads it. Earlier: Two weeks: has every clone that takes turns declared its seat (the digest says), and since the release carrying the guard, has any generated block been rewritten in turns by two clones? If seats are still undeclared, the digest line is being read past — say so."
---

# Plan: The Seat

**What this delivers.** The three causes of agent-to-agent trouble that the
2026-10-14 evidence read found larger than the turn race, each fixed in its
own place: a seat the floor can read, so the record says who sat and a turn
that never left is named where it can be fixed; a guard so two clones on
different frameworks stop rewriting one generated block in turns; and the
ticket as one conversation per work item with a declared reopen, so the
loop's own record reads as conversations. With them, the loop definitions
read as operative rules entered by role.

**What it does not deliver.** A branch per conversation (its own plan,
after this). Any floor act that declares a seat for an agent — only the
agent arriving in a clone knows who it is. Any change to a generated
block's output before the next release.

## Phases

- [x] **Phase 0 — Record it.** `seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15`
      in the operator's words; this plan. *Done 2026-10-15.*
- [x] **Phase 1 — The seat.** `mdllm seat` reads the clone's declaration
      (`mdllm.seat.name`, `.agent`, `.declared`) and its git identity, and
      counts the turns on the checked-out branch its upstream lacks with
      the oldest's age; `--set <actor> --agent <harness>` declares it and
      sets `user.name`/`user.email` locally; `--clear` withdraws it. The
      session-start digest carries the line: the seat, or *undeclared* with
      the ask — louder where the schema declares `ticket` — and *a turn
      that never left* when one is unpublished. *Done 2026-10-15.*
- [x] **Phase 2 — The guard.** The entry file's frontmatter records
      `framework_kernel_from`, the framework commit that last wrote its
      blocks. `kernel_source_check` compares this clone's framework by
      `framework_version_seen` against the running version, then by commit
      ancestry when the framework is a git clone: *ok*, *behind*, *unknown*
      (a commit this clone does not have), *diverged*. `mdllm domain-kernel`
      and `mdllm refresh` refuse to regenerate when not *ok* and leave the
      blocks standing; `domain-kernel --check`, coherence and doctor read
      the difference as *behind*, Info or WARN, never drift Error. *Done
      2026-10-15.* **Transition:** the guard protects an estate only once
      every clone runs a framework that has it; until the next release, no
      `_dk_*` builder's output changes, so a clone on the published release
      and a clone ahead of it write identical bytes.
- [x] **Phase 3 — The ticket is a work item.** The definition template
      declares `closed → <actor>` edges; the ticket template is
      `ticket-<item>`; the schema template's comment says so;
      `standing-watch.md` → The Ticket carries the work-item shape, what
      `closed` means, and *Actors are seats*. *Done 2026-10-15.* The
      workspace half — the live definitions and skills rewritten as
      operative rules entered by role, the per-item ticket, the reopen
      edges, the bindings — done the same day in the busiest live
      workspace on the operator's explicit instruction.
- [ ] **Phase 4 — The watch knows its seat.** `mdllm watch` keys its state
      and lock by seat and branch, under `git rev-parse --git-dir` so a
      linked working copy keeps its lock; its *turn that never left* reads
      the seat's upstream. (The doorbell phase of the branch plan moves
      here.) *Done when two seats in one clone's working copies each hold
      their own watch.*
- [ ] **Phase 5 — The entry file says it.** The generated session-start
      block gains one line: declare your seat before taking a turn. Not in
      3.48.0, the release that carries the guard — a clone still on 3.47.0
      has no guard and would rewrite the changed block in turns; in the
      release after, once every clone that takes turns has pulled 3.48.0.
      *(Corrected 2026-10-17 at the release: the first wording said "at the
      next release", which is the one release this must not be.)*
- [ ] **Phase 6 — See.** Two weeks after the release carrying the guard:
      every clone that takes turns has a declared seat (the digest says),
      no generated block has been rewritten in turns, and `git log` in the
      busiest workspace reads who took each turn.
      *First observation, 2026-10-30 (the trigger's answer):* this clone had
      declared a seat — `codex (codex)`, 2026-10-24 — and the declaration
      was wrong the first time its occupant changed: a Claude session
      arrived and would have committed as codex. The digest line was not
      read past; it was read and said nothing wrong, because the seat was
      named after the agent and the agent had moved. Ruled the same day:
      seats are named for the clone, agnostic of the agent
      (`seats-are-named-for-the-clone-not-the-agent-2026-10-30`); this clone
      is `workspace-1`, the other `workspace-2`. Whether any generated block
      was rewritten in turns needs the second clone's log and is not yet
      read.
- [x] **Phase 7 — The ring.** *(Added and shipped 2026-10-30.)* The
      second-largest cause — a turn that never left — was named at the
      next session start, which is when somebody arrives; the operator's
      account of every attempt is that this stall "has bitten more times
      than most" and cost the most to intervene on. Read against
      Anthropic's published orchestration (every mechanism they ship for
      scale restarts or rings on a silent agent; the wake channel is the
      weak joint, never the message channel), the fix is the one Phase 2
      of `the-record-holds-unattended` gave the dispatcher: the same read,
      made to ring. `mdllm seat` now reads two stalls against a declared
      window: a commit unpublished, and an open ticket whose last turn is
      older than the window — *owed by this seat* when its addressee is
      this clone's seat, *awaiting `<seat>`* otherwise. The lines ride
      the session-start digest and estate-sync's attention section in
      every walked workspace that declares a ticket type; `mdllm seat
      --stall-exit` and `estate-sync --silence-exit` return 5 on a stall
      so a scheduled task rings on the code alone.
      **Calibration, corrected the same day.** The first cut set the
      window at 12 hours from the failures on record. The operator: the
      turns that wait half a day or three weeks "are ones that I've
      forgotten about and the loop has finished… a bad metric to calibrate
      on"; the ones that need attending are "maybe an hour or less"
      apart. The busiest workspace's tickets were then measured at one
      pinned read (783 gaps between consecutive turns on 87 tickets,
      2026-09-25 to 10-30): a reply from the other seat arrives in a
      median of 5 minutes, 75% within 16 minutes, 90% within about an
      hour, 95% within under four; the 16 gaps past 12 hours and the 4
      past a day are the forgotten tail. So there are two thresholds,
      both declared, neither inferred from cadence: the **window** (1h
      by default; `--stall-hours`, or clone config
      `mdllm.seat.stall-hours`) rings on a live conversation that has
      stopped, and the **ceiling** (24h; `--abandon-hours`,
      `mdllm.seat.abandon-hours`) stops it ringing — a ticket open past
      the ceiling is reported once as *abandoned*, close it or reopen it,
      because a ring that fires on every forgotten ticket teaches the
      operator to ignore the ring. At the 1h window the ring is false on
      about one healthy gap in ten; at 2h about one in twenty. The
      operator chose the hour. *Done when:* a stalled turn has rung an
      operator who was not in a session — the same unexercised half the
      dispatcher's ring has.
- [x] **Phase 8 — The turn budget.** *(Added and shipped 2026-10-31.)*
      Asked what the loop still lacked against Anthropic's published
      orchestration (every shipped mechanism caps a run; a conversation
      here ran until someone stopped it), the operator ruled one addition
      and refused another: *"What we do need is a turn count. 120 sounds
      like a good number."* And no rule asking a seat to record that it was
      woken by hand: *"The system that was designed to document documents,
      we don't need to tell it to document again."* So: every commit that
      touched a ticket is a turn, read from the record; an open ticket at or
      past its budget is a line in the same read as the stall ring and
      rings with it (`--stall-exit`, `--silence-exit`); the budget is 120,
      or the clone's `mdllm.seat.turn-budget`, or the ticket's own
      `turn_budget` where the schema declares the field. A closed ticket
      owes nothing. The line asks for a decision — conclude, split, or
      raise the budget deliberately — because the insight it implements
      says the agent inside the loop will not ask it. *Done when:* a
      conversation has reached its budget and been concluded or re-budgeted
      on the line rather than on someone noticing.

## Done when

- [ ] Every clone that takes turns in a loop commits under its seat.
- [ ] Two clones on different frameworks never rewrite one block in turns.
- [ ] A turn that never left is named at the next session start in the
      clone that holds it.
- [ ] A stalled turn — unpublished, or unanswered past the window — rings
      an operator who is not in a session (Phase 7).
- [ ] A conversation at its turn budget is concluded or re-budgeted on the
      floor's line, not on someone noticing (Phase 8).
- [ ] The loop's own record reads as conversations, one per work item.
