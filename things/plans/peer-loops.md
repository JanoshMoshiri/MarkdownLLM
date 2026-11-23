---
id: peer-loops
type: plan
status: in-progress
version: 2.3
created: 2026-11-10
priority: high
origin: stated
informed_by:
  - id: review-agent-coordination-leaders-2026-11-13-workspace-2
    commit: 888eb7b388ff121e55664f8f42b580912c8d8656
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
    notes: "Phase 1 changes what a wake carries: two reminder lines and the last few turns, beside the message it already delivers. Phase 2 adds a line to the wake on a star run; Phase 3 and Phase 7 add rows to its harness bindings."
  - id: ad-hoc-message-loop
    relation: extends
    notes: "The loop definition is the skill the rules live in. Phase 1 rewrote its template around the fourteen rules; Phase 2 adds the six Shape rules and a star turn graph."
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    relation: implements
    notes: "The carrier decision stands: status is the addressee, the body is the current message, git is the transcript. This plan makes the third clause true in practice by giving the transcript a read."
  - id: a-note-on-a-held-ticket-rings-its-addressee-2026-11-02
    relation: extends
    notes: "The note rings since 3.51.0. This plan names its three kinds and has the holder say what it did with it."
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: extends
    notes: "A conversation is a work item; a lane is a run. Phase 2 is where a long lane becomes a run with one short ticket per exchange."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: implements
    notes: "The reason the rules ride on the wake and not only in the definition. The body rule was written and not followed for two months; what arrives with the turn is read."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: references
    notes: "The turn budget's insight. Published review loops run five to fifteen rounds; the budget's default is revisited in Phase 2 on the star lane's own record."
  - id: a2a-conversations-on-their-own-branch
    relation: references
    notes: "The evidence behind this plan reads against a branch per conversation: the failure was one conversation stacking in its own file, never two colliding on main, and the field's measured benefit of a branch is per work item. That plan's status is the operator's to rule and is unchanged here."
  - id: workflow-state-specification
    relation: references
    notes: "A run names each role to a seat and holds the cursor. Rule 8 adds that it names who holds the work and who reviews it."
  - id: a-filter-is-a-missing-instance
    relation: references
    notes: "The Scope section is this insight's second case: sessions in one clone reached for a filter on the wake, and the lane they were each working was a run the watch could already be scoped to."
  - id: review-agent-coordination-leaders-2026-11-13-workspace-2
    relation: derived-from
    notes: "The wider reading of the field made after the operator stepped back on 2026-11-12, against the shape the operator actually runs. Everything after Phase 1 was re-cut against it on 2026-11-14 (version 2.0)."
  - id: review-agent-swarms-scaling-limit-2026-11-16-workspace-2
    relation: derived-from
    notes: "How swarms of tens to thousands of agents coordinate, read on 2026-11-16 against the operator's shape of a hub, two or three spokes and one graph per spoke. The Graphs Below A Spoke section and Phase 8 are written from it."
  - id: coordination-claim-specification
    relation: references
    notes: "A graph's workers claim nodes. Phase 8 tests the claim under contention before any change to it is proposed."
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    relation: references
    notes: "Phase 4, review that starts blind, waits on what that programme finds. Who reviews whom in a star is written from its record and not from the field's argument alone."
  - id: continuity-across-surfaces-is-the-purpose-2026-11-23
    relation: references
    notes: "Lifts the order of work set on 2026-11-16 and ends Phase 4's wait on the review-catch programme."
  - id: run-membership-is-realisation-2026-09-22
    relation: references
    notes: "A ticket joins a lane by declaring `implements: <run>`, the membership edge that ruling made the watch's scope. The Scope section uses it as built."
triggers:
  - type: time
    condition: "2026-11-24 reached"
    action: surface
    note: "Has Phase 1's proof crossed? One ticket between the two substrate clones, a note landing mid-task, no body past a page, and the wake carrying the two lines and the last turns. If it has not, say which of the three it stopped at: the payload was not built, the clones were not armed, or the ticket crossed and the body still grew. Then Phase 2: has the operator picked the star lane, and has it started? Also read whether the operator has declared a seat and a signing key, which Phase 5 waits on and no agent may do for them."
---

# Peer Loops: Conversations Between Seats That Nobody Has To Carry

## What This Is

The substrate carries agent-to-agent conversation and has done since the
ticket landed. The channel works. What goes into it, and who has to stand
over it, did not. This plan is the answer to a two-month record read on
2026-11-06 to 11-09 and a cited survey of the field read on 2026-11-09 and
11-10 (`review-peer-agent-loops-field-research-2026-11-10-workspace-2`). The
operator agreed it on 2026-11-10: *"I like it. Let's go."*

It adds no thing type and no service. It changes what a wake carries,
gives the operator a seat whose rulings can be checked, and writes down
how one seat starts a loop and runs it as its hub, so that the operator
steers and does not carry.

**Re-cut on 2026-11-14 (version 2.0).** On 2026-11-12 the operator stepped
back from the design. The plan assumed equal peers with no lead. The loops
the operator runs are a star: one seat is hub and reviewer, the others are
spokes, the operator speaks to the hub, mostly by voice, and goes to a
spoke directly only for that agent's own view. Peer-to-peer stays wanted,
for bounded work. The setup has to land on the hub and never on a
non-technical user. The field was read against that shape
(`review-agent-coordination-leaders-2026-11-13-workspace-2`), and on
2026-11-14 the operator asked for the plan to be re-cut so the shape can
be tested:

> I feel like I'm babysitting my loop too much at the minute, and I don't
> know if it's down to the loop, it's down to the infrastructure.

Phase 1 and the Scope section stand. Everything after Phase 1 is re-cut
below. The first thing built is the smallest that answers that question
from the record: one lane run as a star, with every turn saying what woke
it.

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

## The Shape: A Star First, Peers For Bounded Work

*Added 2026-11-14.*

A loop has one of two shapes, and its run says which.

- **Star.** One seat is the hub. The operator speaks to the hub. The hub
  writes the run, opens each spoke's ticket, and is the only seat a spoke
  hands a turn to. Spokes do not address each other. This is the default.
- **Peers.** No hub. Any seat may address any seat. It is for a bounded
  task only: a named holder, a check that decides when the task is done, a
  turn budget and a written scope.

**Why the star first.** It is how the operator already works, and the
review's controlled evidence backs it for a reason that is not speed: the
hub is where checking sits, and a hub contains errors better than
independent agents do. The same evidence names the star's cost. A hub that
retells a spoke's words loses some of them, and one vendor measured a
large gain from forwarding them untouched. So the hub cites the spoke's
commit and never retells it. The ticket record makes that free, because a
spoke's words are already a commit.

**Why peers at all, and why bounded.** Flat teams in the review finished
large work when a near-perfect check decided done, and failed when nobody
owned the hard part. So peers is granted to one task at a time, on the
four conditions above, and the run is where they are written.

**No switch is built.** The field has no system that changes shape while
it runs. What the field has separated is messaging from authority:
messages may travel peer to peer while consent stays with one owner.
Moving a lane from star to peers is a line in its run, written by the hub
on the operator's word.

**Nothing new is declared.** A loop definition already lists who may
address whom, as each stage's `to` list, and a run already names roles to
seats. The run gains one word for its shape and names its hub beside its
holder and its reviewer. The floor checks a declared edge on a run's
cursor today. It does not check a ticket's status move against the loop's
turn graph. So in Phase 2 the star is a written rule that also arrives
with the wake, and a floor check is added only if the lane's record shows
a spoke addressing a spoke.

**The operator's own voice.** The operator may speak to any seat, and
doing so must not move a turn. A seat spoken to directly quotes the
operator's words on its ticket as a steer note, and the turn stays where
it was. The hub then reconciles from the record and not from memory. This
is the review's answer to crossed turns, which it found no product solves.

**What woke the seat.** Every turn's commit says what woke the seat: its
bell, the stall ring, or the operator. On 2026-11-12 the operator said
*"I'm relaying the bell rather than steering."* This line makes that
countable from `git log`. When the operator had to wake a seat, the seat's
reply also says in one line why its bell did not: not armed, armed and
silent, logged out, machine busy, or unknown. That separates the loop's
faults from the machine's, which nothing in the record does today.

**Who is waiting.** The hub keeps no list of its own. Asked, it reads the
record and says it: the tickets addressed to the operator, the turns
stalled past their window, the notes nobody has read. The seat read and
the estate sync already compute all three. Spoken by the hub on request,
they are the single inbox the review found the operator lacks, with
nothing built.

**A first look at a live star, 2026-11-16.** Two of the operator's loops
were read from their shared history before Phase 2: a hub with one
Hermes spoke, and a hub with two Codex lanes and the same Hermes spoke.
The operator had begun waking the Hermes spoke over SSH from the hub.
What the record showed, and what the operator corrected:

- Every handover went spoke to hub or hub to spoke, though the
  workspace's turn graph lets any seat address any other. The star held
  as a habit. That is the evidence for leaving its floor check unbuilt.
- The hub answered its 17 handovers that day with a median of three
  minutes.
- The spoke's stalls were turns that ended before handing back, and a
  watch that hit its notification cap. They were not a bell that failed
  to ring. Each time, the hub wrote a note on the ticket and then woke
  the spoke over SSH. The babysitting moved from the operator to the hub.
- One spoke serving two lanes left one lane without a turn for two days
  until the hub set the order.
- The hub's turns were committed under another seat's name, because the
  clone it ran in was declared for that seat. Phase 2 measures from
  status moves, never from authors.
- **Corrected by the operator.** A ticket that read as stalled on the hub
  had been paused deliberately. A quiet day was the operator's own quiet
  day. Two silent lanes were silent because the operator had switched
  their runners off. None of that was in the record. Stall readings from
  the record alone mislead while the operator's pauses go unrecorded, and
  the operator means to record them.

Three things follow, and are added to Phase 2. The waker list gains
`hub`. A hub's nudge is written on the ticket first and then delivered by
whatever channel reaches the spoke: SSH, a harness's own messages, a
queue. The ticket stays the truth, and the shape does not depend on any
one channel. And a spoke holds one lane at a time, or the hub sets its
order on the ticket.

## Graphs Below A Spoke

*Added 2026-11-16, from the operator's shape and the reading of the
field it was checked against
(`review-agent-swarms-scaling-limit-2026-11-16-workspace-2`).*

The operator's rule:

> You never have more than 3 spokes. Maybe 2 is favorable. Maybe 3 if
> one's doing the other side task. [...] You'd only ever run 1 graph on a
> single harness, because then it can run and be managed by a spoke or by
> the orchestrator. In my mind, it'd probably be managed by the spoke.
> [...] You could then essentially have 2,000 agents, more than 2,000, 2
> spokes with 1,000 each and an orchestrator.

**What the field says about it.** The "three to four agents" figure
behind the spoke limit was not measured. It is an extrapolation, under a
fixed budget split across agents, from a curve fitted to coordination
turns. The same study's own small sweep peaked at five to seven. What
the evidence does show is that conversation scales badly: agents that
talk, share one context or split one budget get worse as more are added,
and a peer network of a hundred agents falls to near nothing. Agents that
never talk, each with its own budget, working separable pieces and
handing back only a result, scale to hundreds. Every system found above
about twenty agents on code is a tree of this kind. So the operator's
shape is the one the evidence supports: a small conversation at the top,
and wide, silent fan-out beneath it. The limit on spokes is the hub's
review load and the operator's attention, and Phase 2's record is where
it is read.

**Revised by the operator the same day.** On reading the review, the
operator dropped the limit and named what the plan is for:

> We're not going to give a limit to the amount of spokes that a hub can
> run. We'll leave that for now. I think there'll be a limit. [...] I
> want to say that we've tested it with [...] 3.

> You have all of these separate domain agents working together to
> achieve a goal. [...] The graph only works when the test is strict.
> [...] I achieve that by tests and handover contracts, but it can just
> be tests, that's fine, but that strictness has to hold.

So the unit of this plan is a domain agent: a long-lived seat whose
specialisation is its record. A graph is an option below a spoke, never
the plan's unit. And one rule covers every handover, between seats or
between nodes: it carries a strict check.

**The rules.**

- No limit on spokes is set. The shape has been seen working at three
  spokes, across two vendors' harnesses and a Hermes agent, on one
  operator's work. The limit is read from the record: the point where the
  hub's time to answer, or the spokes' time waiting, starts to climb.
- Every handover carries a strict check. Tests are enough; a contract
  beside them is welcome and is not a substitute.
- A spoke may run one graph, inside its own harness, with the harness's
  own way of starting workers. The spoke plans it, runs it and checks it.
- A graph's workers never write a ticket and never address a seat. The
  spoke hands the hub one turn per graph result.
- Every node of a graph has an automatic check that decides when it is
  done. Every working swarm the field has had one; where it stopped
  producing separable pieces, the swarm collapsed to one effective agent.
  A contract without a check is not enough, and no system found declares
  contracts between sibling nodes at all.
- A graph's working state stays off the shared branch until the spoke
  merges it: on its own branch, or in a repository local to the harness.
  A hosted repository serialises pushes at about six a minute, which on
  the review's own arithmetic holds a few dozen workers on one branch.
- Two spokes' graphs work on separate parts of the codebase, and the hub
  merges between them. Changes from different agents conflicted about
  twice as often as changes from the same agent.
- A graph is as wide as the work has separable pieces. Gains flatten
  around a hundred agents, cost grows with every one, and on sequential
  work more agents make the result worse.
- The hub runs no graph. It plans the spokes' work and reviews what comes
  back.

**What the record would need, and does not have yet.** A record per
node, kept apart from tickets, with a gate that holds the parent's merge
until its children are done. The floor refusing a node's move to done
unless its check passes. Claims that count only once pushed and are
written as new files rather than edits. And node records kept out of the
framework corpus or retired on merge, since one graph of a hundred
workers can write more records than the corpus is sized for. Phase 8 is
the experiment that says which of these are needed; none is built before
it.

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

**Shape** *(proposed 2026-11-14. Rules 1 to 14 above are in the template
as built. These enter it in Phase 2.)*

15. The run says its shape: star or peers. It is a star unless it says
    otherwise, and a star's run names its hub.
16. In a star, a spoke hands its turn to the hub, or closes. The hub hands
    a spoke's words on by citing the commit, never by retelling them.
17. The operator may speak to any seat. A seat spoken to directly quotes
    the operator's words on its ticket as a steer note. The turn stays
    where it was.
18. Every turn's commit says what woke the seat: `Woke: bell`,
    `Woke: ring`, `Woke: hub` or `Woke: operator`. A hub's nudge is a note
    on the ticket first, then delivered by any channel that reaches the
    spoke.
19. Asked who is waiting, the hub reads the record and says it. It keeps
    no list of its own.
20. Peers needs four things written in the run: a holder, a check that
    decides done, a turn budget and a scope. Missing one, the run is a
    star.

Three of the fourteen change with them.

- **Rule 2** gains its owed clause: read the wake whole, and never cut or
  filter what it prints.
- **Rule 9**, for a star. The operator's go reaches a spoke through the
  hub. The hub records it as the operator's own words, quoted and dated. A
  spoke may act on that record for work it can undo. For what cannot be
  undone, the go is the operator's own act in the session that performs
  it, a signed commit once Phase 5 exists, or a standing delegation. A
  hub's account of a go is never the go. *This is a proposal. Whether it
  stands is the operator's to rule before Phase 2's lane starts.*
- **Rule 11** tells each seat to bind its watch inside its own session,
  scoped to the run, and never as a scheduled task. It ends "then act as
  the hub" where it said "then act as a peer".

## The Code, All Of It

The operator's position is that a written contract drives this and code
does not run it. The record and the review agree on where that stops
working: rules 1 to 3 were written and not followed. So there are four
small pieces of code, each at a boundary that already exists, and nothing
else.

1. The wake carries two reminder lines and the last few turns of the
   ticket, read from git.
2. The floor refuses a new ticket body that holds more than one turn,
   where the workspace has opted in; elsewhere it warns.
3. The floor checks the signature on the operator's approvals.
4. The wake's rule lines name the hub when the woken ticket's run is a
   star, so a spoke is told where its turn goes at the moment it takes it.
   *(Since 2026-11-14. Not built.)*

The fourth piece was a Codex resume loop until 2026-11-13. It is set
aside. The operator's record is that a Codex desktop session told to bind
its watch inside the session holds it for a day or two. What failed was a
scheduled heartbeat task standing in for the bound watch, and watches on
a starved machine. The start card in Phase 2 says which to use. The
resume loop returns only if a session-bound Codex watch is seen to drop
on a machine that is not starved.

One more piece is named and not built: a floor check that reports a
spoke addressing a spoke in a star run. It waits for the Phase 2 lane to
show the written rule being skipped.

Scoping a session's watch to its own conversation is not a further piece.
It is already built; the next section says how.

## Scope: Which Conversation a Watch Hears

*Added 2026-11-11, from the first reading of Phase 1 in use.*

A seat is a clone: its name, its agent and the git identity its commits
carry are clone-local configuration, and every session in that clone shares
them. A ticket waits for a seat, because its status names one. So when two
sessions in one clone work two lanes, each session's watch wakes on every
ticket addressed to that seat, and each session ends up reaching for a
filter on what the wake prints. On 2026-11-11 two live sessions had done
exactly that, one with `tail -40` and one with a filter that kept only the
message block, and the earlier turns Phase 1 built never reached either of
them.

Three answers were weighed in session with the operator.

- **A seat per session.** Rejected. A watch refuses to arm for a role that
  is not a stage of the loop, and the floor refuses a status the schema
  does not declare, so every session's name would have to be added to both
  and pruned when its lane ends. That is the roster this plan refuses. It
  also does not separate the record: two sessions in one clone still commit
  under one identity. A seat per session is right only when each session
  has its own clone or worktree, which is a Phase 3 item.
- **A ticket-id scope** (`--ticket <id>`). Proposed in session, then set
  aside. `standing-watch.md` → Scope rules that a watch is scoped to a run
  and never to a thing, and the narrowing it would add already exists.
- **The run.** Chosen. The scope was built on 2026-09-22 (`--run`). A lane
  is a run; a ticket joins it by declaring `implements: <run>`; a session's
  watch armed with `--run <lane>` hears only that lane's tickets. Nothing is
  listed, nothing new is built, and the seat stays per clone. This is
  `a-filter-is-a-missing-instance` a second time: the lane was the instance,
  unnamed to the watch.

**Dismissal condition.** A seat routinely holds two conversations at once
that belong to no run, often enough that writing a run for each is the
burden. Then a ticket scope comes back as a fifth piece of code, and the
spec's never-to-a-thing ruling is revised with it.

## Phases

Each phase is built, used on something real, read back from the record,
and fixed before the next one starts.

- [x] **Phase 0 — Record it.** This plan and the review it rests on,
      2026-11-10.

- [ ] **Phase 1 — The doorbell carries the contract.**
      - [x] The wake emits two reminder lines with every ticket message:
            the body is one message, and the earlier turns are above and in
            git. Built 2026-11-10 (`standing-watch.md` 0.10). An artefact's
            wake is unchanged, because its body is the artefact.
      - [x] The wake emits the last three turns of the woken ticket, read
            from the ticket's git history, each cut at 1,500 characters,
            oldest first. Built 2026-11-10.
      - [x] The floor reports an open ticket created on or after 2026-11-10
            whose body holds more than one message, and refuses the commit
            where the workspace declares `ticket_body: strict`. Built
            2026-11-10; the root declares it. Opt-in, as the session gate
            is: a refusal arriving with a refresh would stop every seat's
            commits in a live workspace the moment one ticket stacked.
            Older tickets and closed ones are left alone.
      - [x] The loop definition template carries the fourteen rules, and
            the root's own loop follows it (`ad-hoc-message-loop` 1.5).
      - [x] A note names its kind: steer, follow up, or aware (rule 4).
            A rule and nothing more; the watch does not read the kind.
      - [ ] Rule 2 gains a clause, and the template carries it: read the
            wake whole, never cut or filter what it prints. Owed since
            2026-11-11, when two live sessions were found cutting it (see
            Scope).
      - [ ] **Proof.** One ticket crosses between the two substrate clones
            with a note landing mid-task, and no body grows past a page.
            This is also the live round trip `substrate-native-a2a` has
            owed since 2026-11-03.
            *First reading, 2026-11-11, not the proof.* The payload was
            published and both substrate clones carry it. Every live ticket
            turn that day stayed one message. One wake was seen carrying
            the earlier turns and the rule whole; two sessions cut theirs
            before reading it, and one watch was still on code from before
            the change. The check for a stacked body has not yet fired,
            because no ticket born on or after 2026-11-10 had turns. The
            proof still needs a new ticket, with watches armed whole.

*Phases 2 to 7 were re-cut on 2026-11-14. The earlier Phase 2 is now
Phase 5, the earlier Phase 4 is folded into Phase 2's proof, and the
earlier Phase 5 is now Phase 7.*

- [ ] **Phase 2 — One lane as a star.** The test of the shape. It needs
      one small piece of code and no new setup from the operator.
      - [ ] The loop template gains the Shape rules (15 to 20), the
            changes to rules 2 and 11, and a three-seat star turn graph
            beside the two-seat default.
      - [ ] The start card: the text the hub writes at the head of each
            spoke's opening ticket. It names the seat and the run, gives
            the one command that arms the watch, says to bind it in this
            session and never as a scheduled task, says turns go to the
            hub, and says to quote the operator's direct words as a steer
            note. A spoke needs nothing else to join.
      - [ ] The wake names the hub on a star run's ticket (code piece 4).
      - [ ] A check before the lane starts, and again before a stall is
            blamed on the loop: every seat is logged in and its clone can
            fetch and push, the machine is not starved, and every watch
            runs current code. The hub reads these with tools that exist
            and tells the operator in a sentence. It does not fix a login.
      - [ ] The operator rules on rule 9 as proposed for a star.
      - [ ] A spoke holds one lane at a time, or the hub sets its order
            on the ticket. The start card tells a spoke that when its
            turn runs low it pushes what it has and hands back, because
            on 2026-11-16 the hub had to say so in every nudge.
      - [ ] The operator's own pauses, holds and switched-off runners are
            recorded where the stall read sees them, so a deliberate
            pause does not read as a stall.
      - [ ] One doorbell per seat in place of the five wake mechanisms
            the baseline counted, each session's watch armed with `--run`
            for its own lane, and the lane a run with one short ticket
            per exchange.
      - [ ] **Proof.** One real lane with three seats runs as a star for
            its natural length, the operator speaking to the hub. The
            script that produced the baseline reads it back: the share of
            turns woken by the bell, the ring, the hub and the operator;
            each hub or operator wake sorted to the loop, a turn that ran
            out, a capped watch, a login or the machine; any
            spoke that addressed a spoke; handovers that waited past the
            window; body size. The baseline to beat is 46 of 396 handovers
            waiting more than an hour and about three ticket commits in
            ten naming the operator. The turn budget's default is
            revisited on the same record.
            *The agent's expectation, written 2026-11-14 before any such
            lane has run.* Fewer than one turn in ten is woken by the
            operator, and most of those are sorted to a login or the
            machine. If operator wakes stay near three in ten with every
            seat logged in and the machine idle, the star did not fix the
            bell, and the fault is in how the watches are bound and not
            in the shape.

- [ ] **Phase 3 — The hub starts the lane from one instruction.**
      - [ ] The start skill is written from rules 11, 12 and 15. It
            writes the run, the tickets and the start cards, and runs
            Phase 2's check.
      - [ ] A seat names its surface in its own address when it declares,
            so every commit says both.
      - [ ] Every seat commits under its own identity. Two seats may share
            a clone, as the operator runs them today (ruled 2026-11-16),
            but on 2026-11-11 and again on 2026-11-16 one seat's turns
            were found authored as another's, because both ran in a clone
            declared for one of them. A worktree per seat is the first
            thing to try. Whether a worktree can hold a seat of its own
            is checked at source before it is relied on: git shares one
            configuration across worktrees unless told otherwise. The
            operator declares each seat, once, never once per lane.
      - [ ] **Proof.** One spoken instruction to the hub starts a
            three-seat star across two vendors, and the first round trip
            completes before the operator types into any spoke.

- [ ] **Phase 4 — Review that starts blind.** No longer waits on the
      review-catch programme. The operator stepped away from that question
      on 2026-11-21 (`continuity-across-surfaces-is-the-purpose-2026-11-23`),
      so the items below are settled from the operator's practice and not
      from an eval.
      - [ ] Who reviews whom in a star, the hub's own work included. The
            review argues the hub's work should go to a spoke.
      - [ ] Whether a reviewer receives the change without the author's
            account of it, and records a verdict before reading the
            author's reasoning.
      - [ ] Both are written from the operator's practice. Today that
            practice is that the hub reviews, and that a cold review by a
            fresh session holds at least as much weight as a second vendor.
      - [ ] **Proof.** To be set by the operator. It was to be set from the
            programme's first two cycles, which are paused.

- [ ] **Phase 5 — The operator's signed seat.** Moved after the star
      because the star lane does not need it, and because it has waited
      on the operator's own act since 2026-11-10.
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

- [ ] **Phase 6 — Peers, on one bounded task.**
      - [ ] The template's peers turn graph, and rule 20's four
            conditions as the run's own fields.
      - [ ] The operator picks the task and grants the shape.
      - [ ] **Proof.** Two spokes finish one bounded task addressing each
            other, inside its turn budget, the hub appearing only at the
            start and at the end. The check that decided done is in the
            record.

- [ ] **Phase 7 — Doorbells that ring themselves.**
      - [ ] Hermes rings itself from a scheduled job that checks the
            remote and declines to wake when nothing moved.
      - [ ] OpenClaw's wake endpoint is wired to the same check.
      - [ ] **Proof.** A three-seat star started from one instruction runs
            overnight, and the morning's record shows no stall longer than
            the ring's window.

- [ ] **Phase 8 — A graph under one spoke.** May start once Phase 2's
      lane has run; it does not wait on Phases 3 to 7.
      - [ ] One spoke runs one graph inside its own harness on a task with
            a real check per node: tests, a known-good oracle, or a
            comparison against a reference. The graph's width is the
            task's separable pieces.
      - [ ] The graph's working state lives on its own branch or in a
            repository local to the harness. Only the spoke's merged
            result and its one turn reach the shared record.
      - [ ] Measured as it runs: claim races, pushes rejected, merge
            conflicts, the floor's time per commit, tokens, and the
            nodes whose check passed at the first attempt.
      - [ ] **Proof.** The graph's result merges, the hub reviews it from
            one turn, and the measures say which of the four missing
            pieces in Graphs Below A Spoke were needed. A run of this
            kind on a git-backed record would be one of very few
            published data points.

## Order Of Work, And What Is Still Open

*Added 2026-11-16. The operator asked for the approach to be examined
critically before the plan was committed, and then set the order.*

*Revised 2026-11-23. The operator lifted this order. The eval gates
nothing, and the cross-vendor review question is no longer pursued
(`every-spec-stays-and-gauges-come-before-clearing-2026-11-23`,
`continuity-across-surfaces-is-the-purpose-2026-11-23`). The order of work
is now the conformance roadmap's. "The order" and "What the eval's result
changes here" are kept below as they stood from 2026-11-16 to 2026-11-21.
The open points from the critical reading still stand.*

**The order.** The review-catch eval runs first. Nothing in Phases 2 to
8 is built until its first two cycles have been reflected on. Meanwhile
the record is read, because that needs nothing built. The operator's own
experience is that two vendors reviewing one piece of work find
different things, on code and on a contract alike. That is the reason
for the loop and it is the eval's first prediction. What the experience
does not yet show is whether the difference comes from the vendor or
from a fresh context, and how many of the extra findings are real.

**What the eval's result changes here.**

- A second vendor catches more than the same model reviewing twice:
  review by a different vendor becomes a rule of the loop, the hub's own
  work included.
- The two come out equal: fresh context is what matters, and reviews are
  routed by budget and speed.
- Showing the author's account lowers catches: a reviewer receives the
  change without it.

**Open, from the critical reading.**

1. Nothing yet shows the loop does better than one good agent. The
   controlled studies find multi-agent coding neutral to slightly worse
   at matched cost. The answer offered is validation, and it is untested
   until the eval reports.
2. The operator is the part that scales worst. Every change waits on the
   operator's approval, and pauses and priorities live outside the record.
3. Nobody reviews the hub. It reviews the spokes, answers in minutes, and
   makes rulings of its own that cite no one.
4. Strictness is not holding even on code. On 2026-11-16 a spoke handed
   back with every check green several times and the hub still sent the
   work back. The real check was the hub looking, which does not carry to
   a graph.
5. Shared clones conflict with The Principle's first row. Who sits in a
   workspace cannot be read from commit authors while one seat commits
   under another's name. Either each seat gets its own identity (Phase 3)
   or that row goes.
6. Cost per merged change has never been measured.
7. Every fix so far has needed the operator. No non-technical person has
   run a loop.
8. This plan has twenty rules, and its own evidence is that a rule which
   does not arrive with the wake is skipped, while the star held with no
   rule at all. It may need fewer rules and more measurement.

**What the record could answer with nothing built.**

- Review rounds per change, by builder, and how often a handback with
  every check green was sent back.
- The hub's rulings: which cite the operator and which are its own, and
  how many were later reversed.
- Where elapsed time goes: agents working, agents waiting on each other,
  work waiting on the operator.
- Fixes made after the hub cleared a change, traced back to that change.
  This is the review-catch method pointed at product work.

**What needs research or thought.**

- A strict check for work that has no tests.
- Hubs of hubs: a domain agent that is hub in its own domain and spoke in
  another's. No evidence was found either way.
- One seat's ticket is another seat's instructions, and a hub may now
  hold a command channel into a spoke's machine.

## What This Plan Refuses

- A roster, a registry, or any list of seats that someone has to keep
  true. This includes an alias list.
- A coordinator service. A hub is a seat like any other: it holds
  tickets, takes turns and follows the same rules. A hub that retells a
  spoke's words where it could cite them is refused with it.
- A switch that changes a loop's shape while it runs.
- A scheduled task standing in for a watch bound to a session.
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
- Which seat is the hub, lane by lane.
- Which lane is the star lane in Phase 2.
- Rule 9 as proposed for a star: whether the hub's quoted record of a go
  is enough for work a spoke can undo.
- Whether the hub also reviews. The field's evidence points at the split
  in rule 8 and at a reviewer that starts blind. The review-catch
  programme that was to give this repository evidence of its own is
  paused, so this is the operator's judgement from practice.
- Granting peers to a task.
- How many spokes a hub holds, and which spoke and task run the first
  graph in Phase 8.
- The status of `a2a-conversations-on-their-own-branch`.

## Done When

- [ ] A ticket body stays one message across a whole lane, with no rule
      being cited to make it so.
- [ ] An approval can be verified by any seat without trusting the seat
      that mentions it.
- [ ] A three-seat lane across two vendors runs as a star with the
      operator speaking only to the hub, and its record shows what woke
      every turn.
- [ ] One bounded task has run as peers and ended inside its budget.
- [ ] One graph has run under one spoke, merged, and been reviewed by the
      hub from a single turn.
- [ ] The three baseline measures have been read again after the change,
      and the reading is in the record whichever way it came out.
