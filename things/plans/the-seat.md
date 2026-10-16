---
id: the-seat
type: plan
status: in-progress
version: 1.0
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
triggers:
  - type: time
    condition: "2026-10-29 reached"
    action: surface
    note: "Two weeks: has every clone that takes turns declared its seat (the digest says), and since the release carrying the guard, has any generated block been rewritten in turns by two clones? If seats are still undeclared, the digest line is being read past — say so."
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
- [ ] **Phase 5 — The entry file says it.** At the next release, and only
      then, the generated session-start block gains one line: declare your
      seat before taking a turn. Until every clone has the guard, a changed
      block restarts the fight the guard ends.
- [ ] **Phase 6 — See.** Two weeks after the release carrying the guard:
      every clone that takes turns has a declared seat (the digest says),
      no generated block has been rewritten in turns, and `git log` in the
      busiest workspace reads who took each turn.

## Done when

- [ ] Every clone that takes turns in a loop commits under its seat.
- [ ] Two clones on different frameworks never rewrite one block in turns.
- [ ] A turn that never left is named at the next session start in the
      clone that holds it.
- [ ] The loop's own record reads as conversations, one per work item.
