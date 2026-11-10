---
id: peer-loops
type: plan
status: in-progress
version: 1.0
created: 2026-11-10
priority: high
origin: stated
informed_by:
  - id: standing-watch-specification
    commit: ef7215d2186a844beabef705300a7cb0e6c5a015
  - id: ad-hoc-message-loop
    commit: ef7215d2186a844beabef705300a7cb0e6c5a015
  - id: the-seat
    commit: ef7215d2186a844beabef705300a7cb0e6c5a015
tags: [a2a, peer-loops, ticket, doorbell, operator-seat, attestation, derive-not-define, sequence]
linked_things:
  - id: review-peer-agent-loops-field-research-2026-11-10-workspace-2
    relation: derived-from
    notes: "The cited survey of the field this plan was revised against before it was agreed. Its eight ranked changes are the source of the four small pieces of code below; its refusals of this plan's refusals are answered in What This Plan Refuses."
  - id: substrate-native-a2a
    relation: extends
    notes: "That plan built the channel: the watch, the ticket, the wake. This one is about what goes in the channel and who may start it. Its owed live round trip is this plan's Phase 1 proof."
  - id: the-seat
    relation: extends
    notes: "The seat, the stall ring and the turn budget are that plan's and are used here as built. This plan adds the operator as a seat, and reads who sits where from the seats' own commits."
  - id: standing-watch-specification
    relation: extends
    notes: "Phase 1 changes what a wake carries: two reminder lines and the last few turns, beside the message it already delivers. Phase 3 and Phase 5 add rows to its harness bindings."
  - id: ad-hoc-message-loop
    relation: extends
    notes: "The loop definition is the skill the rules live in. Phase 1 rewrites its template around the fourteen rules."
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    relation: implements
    notes: "The carrier decision stands: status is the addressee, the body is the current message, git is the transcript. This plan makes the third clause true in practice by giving the transcript a read."
  - id: a-note-on-a-held-ticket-rings-its-addressee-2026-11-02
    relation: extends
    notes: "The note rings since 3.51.0. This plan names its three kinds and has the holder say what it did with it."
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: extends
    notes: "A conversation is a work item; a lane is a run. Phase 4 is where a long lane becomes a run with one short ticket per exchange."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: implements
    notes: "The reason the rules ride on the wake and not only in the definition. The body rule was written and not followed for two months; what arrives with the turn is read."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: references
    notes: "The turn budget's insight. Published review loops run five to fifteen rounds; the budget's default is revisited in Phase 4 on a lane's own record."
  - id: a2a-conversations-on-their-own-branch
    relation: references
    notes: "The evidence behind this plan reads against a branch per conversation: the failure was one conversation stacking in its own file, never two colliding on main, and the field's measured benefit of a branch is per work item. That plan's status is the operator's to rule and is unchanged here."
  - id: workflow-state-specification
    relation: references
    notes: "A run names each role to a seat and holds the cursor. Rule 8 adds that it names who holds the work and who reviews it."
triggers:
  - type: time
    condition: "2026-11-24 reached"
    action: surface
    note: "Has Phase 1's proof crossed? One ticket between the two substrate clones, a note landing mid-task, no body past a page, and the wake carrying the two lines and the last turns. If it has not, say which of the three it stopped at: the payload was not built, the clones were not armed, or the ticket crossed and the body still grew. Also read whether the operator has declared a seat and a signing key, which Phase 2 waits on and no agent may do for them."
---

# Peer Loops: Conversations Between Seats That Nobody Has To Carry

## What This Is

The substrate carries agent-to-agent conversation and has done since the
ticket landed. The channel works. What goes into it, and who has to stand
over it, did not. This plan is the answer to a two-month record read on
2026-11-06 to 11-09 and a cited survey of the field read on 2026-11-09 and
11-10 (`review-peer-agent-loops-field-research-2026-11-10-workspace-2`). The
operator agreed it on 2026-11-10: *"I like it. Let's go."*

It adds no thing type, no service and no coordinator. It changes what a
wake carries, gives the operator a seat whose rulings can be checked, and
writes down how one seat starts a loop and then steps back.

## The Evidence

Read from the busiest live workspace's remote history at one pinned commit.

| Measured | Result |
|---|---|
| Handovers that were answered | 396 |
| Answered inside fifteen minutes | 262 |
| Waited more than an hour | 46, holding 415 of 479 waiting hours |
| Ticket commits naming the operator, a ruling, an approval or a hold | about three in ten |
| Builder rounds on one lane that restated pull request state | 78 of 96 |
| Largest ticket bodies, in characters | 232k, 133k, 108k |
| One run's body and commit count | 238k, 294 |
| Separate wake mechanisms in that one workspace | 5 |

Three containers turned into dated logs: a ticket per reply in one month, a
ticket per lane in the next, and the run itself. The agents were reaching
for an ordered history they could read. The substrate keeps one, in git,
and gave them no read of it, so they wrote it into the body. The carrier
decision said the body is the current message and git is the transcript;
the loop definition said the addressee overwrites the body with one reply.
Both were read and neither was followed.

So the operator was doing two jobs by hand: carrying authority into every
lane, and starting and restarting the listeners.

## What The Field Says

Nobody has published this loop: equal peers across vendors, over bare git,
with no server, roster or coordinator. Almost every part has a practised
analogue. The review sorts the plan into three piles and this plan was
revised to match.

- **Matches practice.** Work state on the work item; one message per
  record with history in a log; a note delivered at the next tool boundary;
  approvals cited and never relayed; standing delegations with scope and an
  end date; the first commit as the receipt.
- **The evidence opposed it, so it changed.** Rules carried only in a
  skill; the operator's name on an unsigned commit as an approval; a
  summon typed in the operator's name.
- **No published evidence either way.** Who sits where read from commits;
  a body replaced in place with history in git; peers across vendors with
  no lead. This is where the approach is its own, and each is a claim this
  plan tests on its own record.

Three corrections to the review, from this session's hands-on checks: the
turn budget and the stall ring already exist (`the-seat` Phases 7 and 8),
so its fifth change is half built; the Codex installed on the operator's
machine still has the server mode the review says was removed; and every
harness statement in the review is documentation read on one day and not
tested, so each binding is checked by hand in its phase.

## The Principle: Derive, Never Define

Anything written down as a list has to be kept true by someone. Anything
read from what the seats already do stays true by itself and grows as they
work. So there is no roster. Each fact a loop needs is read from where it
already lives.

| What a seat needs to know | Read from |
|---|---|
| Who sits in this workspace | The authors of its commits |
| What surface a seat runs on | The seat's own address on its commits, set when it declares |
| Whose turn it is | The ticket's status |
| What was said before | The ticket's git history |
| Where the work stands | The run's cursor and the pull request |
| What has been approved | Signed commits from the operator's seat, and the standing delegations |
| Whether a seat is listening | How recently it committed, and whether its doorbell answers |
| Whether a seat can be launched from here | Whether a clone on this machine declares it |

One thing has to be defined, and the review is firm on it: whose signature
counts. Git's own manual says the author's name has no effect on
authentication. For a single operator that is one key. It is an identity
and not a list of seats.

Reading the busiest workspace's commit authors already returns its seats
with nobody listing them, and shows what a maintained list would have
hidden: one seat under two names, two clones on one machine declaring the
same seat, and several hundred early commits under the operator's identity
from before seats were declared. A seat under two names is fixed where it
was declared. No alias list is kept.

## The Rules

The contract lives in the loop definition, which is a skill, and its
template carries it to every workspace on refresh. The two that matter
most also arrive with every wake.

**Conversation**

1. A ticket is one conversation. Its status names whose turn it is. Its
   body is one message.
2. The wake brings the last few turns. Older history is in git. Never copy
   a turn into the body.
3. Reply by replacing the body. Then hand the turn on, or close.
4. Anyone may leave a note on a ticket they do not hold, and says which
   kind it is: steer now, follow up next turn, or just be aware. The holder
   says in the next reply what it did with it.
5. A conversation has a budget of about twenty turns. At the budget,
   conclude it or split the work.

**Work**

6. The state of the work goes on the run and on the pull request. The
   ticket carries only what nothing else carries.
7. A run's body says where the work is and what is next. Its past is git.
8. The run names who holds the work and who reviews it. The reviewer
   finds. The holder decides which findings to act on.

**Authority**

9. A go is a signed commit from the operator's seat that names the commit
   it approves. Cite it. Never relay it.
10. A standing delegation is a written decision with a class of gate,
    conditions and an end date. Act inside it without asking. Outside it,
    address the operator's seat.

**Starting**

11. To start a loop: write the run with each role named to a seat, write
    each seat's opening ticket, launch any local seat that is not
    listening, take its first commit as the receipt, then act as a peer.
    Never send a message as the operator.
12. Who sits where is read from the commits. Nothing lists the seats.

**Stopping**

13. When blocked, address the ticket to the seat that can unblock you and
    say what you need. Never wait silently.
14. A doorbell that cannot read says so. Silence means nothing moved only
    when the bell can still look.

## The Code, All Of It

The operator's position is that a written contract drives this and code
does not run it. The record and the review agree on where that stops
working: rules 1 to 3 were written and not followed. So there are four
small pieces of code, each at a boundary that already exists, and nothing
else.

1. The wake carries two reminder lines and the last few turns of the
   ticket, read from git.
2. The floor refuses a new ticket body that holds more than one turn.
3. The floor checks the signature on the operator's approvals.
4. Codex gets a short loop that resumes its session when its watch exits,
   because nothing documented wakes a local Codex session from outside.

## Phases

Each phase is built, used on something real, read back from the record,
and fixed before the next one starts.

- [x] **Phase 0 — Record it.** This plan and the review it rests on,
      2026-11-10.

- [ ] **Phase 1 — The doorbell carries the contract.**
      - [ ] The wake emits two reminder lines with every message: the body
            is one message, and the last turns are below.
      - [ ] The wake emits the last few turns of the woken ticket, read
            from the ticket's git history, bounded, newest last.
      - [ ] The floor refuses a ticket created on or after this phase's
            release whose body holds more than one turn. Older tickets are
            left alone.
      - [ ] The loop definition template is rewritten around the fourteen
            rules, and the root's own loop follows it.
      - [ ] A note names its kind: steer, follow up, or aware.
      - [ ] **Proof.** One ticket crosses between the two substrate clones
            with a note landing mid-task, and no body grows past a page.
            This is also the live round trip `substrate-native-a2a` has
            owed since 2026-11-03.

- [ ] **Phase 2 — The operator's signed seat.**
      - [ ] The operator declares a seat and creates a signing key the
            agents cannot use. This is the operator's act and no agent
            does it for them.
      - [ ] Git's repository-local allowed-signers mechanism is read at
            source before the check is designed; the review did not verify
            it.
      - [ ] The floor checks the signature on an approval, and an approval
            names the commit it approves.
      - [ ] The delegation pattern is written as a `decision` with a class
            of gate, conditions and an end date.
      - [ ] **Proof.** A signed approval naming a commit is accepted. The
            same approval unsigned, or made by an agent, is refused.

- [ ] **Phase 3 — Start a loop from one place.**
      - [ ] The start skill is written from rules 11 and 12.
      - [ ] A seat names its surface in its own address when it declares,
            so every commit says both.
      - [ ] The Codex resume loop, tested by hand before it is trusted.
      - [ ] **Proof.** From one Claude Code session, one spoken
            instruction starts a Codex seat on the same machine and a
            ticket makes the round trip with no relay.

- [ ] **Phase 4 — One fresh lane, read back against the baseline.**
      - [ ] In the busiest workspace: one doorbell per seat in place of
            five, a lane as a run with one short ticket per exchange, the
            holder and the reviewer named, and one class of gate under a
            delegation.
      - [ ] The turn budget's default is revisited on that lane's record.
      - [ ] **Proof.** The script that produced the baseline reads the
            lane back: body size, the slow tail of handovers, and the
            share of rulings relayed by an agent. No published work makes
            this comparison.

- [ ] **Phase 5 — Doorbells that ring themselves.**
      - [ ] Hermes rings itself from a scheduled job that checks the
            remote and declines to wake when nothing moved.
      - [ ] OpenClaw's wake endpoint is wired to the same check.
      - [ ] **Proof.** A three-seat loop started from one place runs
            overnight, and the morning's record shows no stall longer than
            the ring's window.

## What This Plan Refuses

- A roster, a registry, or any list of seats that someone has to keep
  true. This includes an alias list.
- A coordinator service, or an agent that relays turns between others.
- A new kind of thing for messages, or a thing per message.
- Authority carried in an agent's words.
- A message sent as the operator, on any channel.
- A second carrier narrating a turn that another system already holds.
- An unattended process rewriting a record when a deadline lapses. It
  rings, and a person or a seat acts.
- The standard protocols' state names on a ticket. A ticket's status names
  a seat, which those protocols cannot express.

## What Stays The Operator's

- Declaring their seat and holding their signing key.
- Whether the reviewer keeps directing. The weakest evidence in the review
  still points at the split in rule 8; Phase 4 is where it is tried.
- The status of `a2a-conversations-on-their-own-branch`.
- Which lane is the fresh lane in Phase 4.

## Done When

- [ ] A ticket body stays one message across a whole lane, with no rule
      being cited to make it so.
- [ ] An approval can be verified by any seat without trusting the seat
      that mentions it.
- [ ] A loop across two vendors' harnesses is started from one seat and
      runs with no human relay.
- [ ] The three baseline measures have been read again after the change,
      and the reading is in the record whichever way it came out.
