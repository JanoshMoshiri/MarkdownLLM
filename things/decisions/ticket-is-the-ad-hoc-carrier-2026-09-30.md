---
id: ticket-is-the-ad-hoc-carrier-2026-09-30
type: decision
status: made
version: 1.0
created: 2026-09-30
session: 2026-10-01
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [a2a, ticket, standing-watch, turn-taking, between-sessions, transport]
informed_by:
  - id: substrate-native-a2a
    commit: 38ab1d8643f6baaa9df5ce92f356a5134603cca0
  - id: standing-watch-specification
    commit: 38ab1d8643f6baaa9df5ce92f356a5134603cca0
  - id: mesh-safety-is-the-floor-not-the-topology
    commit: 38ab1d8643f6baaa9df5ce92f356a5134603cca0
  - id: transport-follows-corpus-holdability-not-distance
    commit: 38ab1d8643f6baaa9df5ce92f356a5134603cca0
linked_things:
  - id: substrate-native-a2a
    relation: informs
    notes: "Qualifies that plan's refusal 'no new thing type for the turn' — it was about artefact turns, which had a carrier. Ad-hoc messages had none. Phase 7 there is this decision's build."
  - id: standing-watch-specification
    relation: informs
    notes: "The spec that carries the protocol: who writes, one message per turn, how to close, the safety rule. 0.4 → 0.5."
  - id: mesh-safety-is-the-floor-not-the-topology
    relation: implements
    notes: "A ticket carries requests, never approvals or rulings. The recipient acts within its own permissions; the irreversible still goes to the seat. The safety is the floor, not the fact that two peers are talking."
  - id: transport-follows-corpus-holdability-not-distance
    relation: implements
    notes: "The governing constraint, honoured: the ticket crosses no wire git does not already send."
---

# Decision: The Ticket Is the Carrier for Ad-Hoc Agent-to-Agent Messages

## Context

The substrate carries agent-to-agent turn-taking for **artefacts** and has
done since `mdllm watch` landed: a thing's `status` is the turn token,
`held_by` the claim, git the message channel, `--exit-on-wake` the wake
channel. Two agents in two harnesses go back and forth on anything they
create with no human relay.

What it could not carry was a message with **no artefact behind it** —
*"Codex, quickly review X"*, *"Hermes, go and do Y"*. Nothing on the board
changes status when one agent wants to say something to another, so nothing
rings. This was the last gap in autonomous communication on the substrate,
and the operator ruled its shape on 2026-09-30.

The question had a complication. `substrate-native-a2a` refuses *"a new
thing type for the turn — a contended singleton across two clones."* Read
literally that refusal forbids the obvious carrier. Read for its reason it
does not: it was written about artefact turns, which already *had* a carrier
(the artefact's own status), so a second thing for the same turn would have
been two declarations of one fact. An ad-hoc message has no artefact and
therefore no existing carrier. This decision names that as a new case and
**qualifies** the refusal rather than silently excepting it.

## Inputs Considered

- **`standing-watch.md` 0.4** — the two-channel distinction, the arming
  refusals, and the fact (verified in `watch.py`, not trusted) that
  `read_board` skips reserved types on a status-keyed board and `diff_board`
  ignores `was == now`. Both constrain the shape below.
- **`substrate-native-a2a` 1.5** — the transport refusal and the
  no-new-type refusal, with the reasoning behind each.
- **`mesh-safety-is-the-floor-not-the-topology`** — why a channel between
  two peers must not become a channel for authority.
- **`transport-follows-corpus-holdability-not-distance`** — the standing
  constraint that nothing crosses a wire git does not already send.

## Options

1. **A hosted mailbox MCP server** — a small service agents post to and poll.
   *Rejected:* fails the transport refusal outright. It would also be the
   message channel on a wire, which `standing-watch.md` names as the design
   error the between-sessions band exists to prevent: it discards
   versioning, validation and audit and rebuilds them worse.
2. **`mcp_agent_mail`** (a third-party agent-mail MCP) — an off-the-shelf
   version of option 1. *Rejected* on the same ground, and on a second that
   is independent of design: its licence carries a rider withholding rights
   from OpenAI and Anthropic, which makes it unusable in an estate whose two
   principal agents are theirs.
3. **A message thing per message** — an append-only log of small things.
   *Rejected:* an archive to maintain, an id scheme to invent, and the
   transcript smeared across files when git already keeps it per file.
4. **The ticket** — one overwritable thing per conversation (in practice per
   agent pair), whose `status` is the addressee and whose body is the current
   message. Git history is the transcript. *Chosen.*

## Decision

**Option 4, ruled by the operator on 2026-09-30.** The ticket:

- is a thing whose `status` names the **addressee** — the actor whose turn it
  is — plus a terminal `closed`;
- is written **only by the current addressee**: to reply, overwrite the body,
  set `status` to the next addressee, commit, publish. One writer at any
  moment, so no merge conflicts across clones. The status *is* the claim; a
  ticket carries no `held_by`;
- carries **one message per turn** — you speak, then wait. This is floor
  behaviour, not just protocol: a body-only change at the same status is
  invisible to every watcher (`diff_board` skips `was == now`), so a second
  message without a handover reaches nobody. The open question — should the
  watch optionally wake on content change at the same status, to allow
  double-sends? — is answered **no** unless the live test shows the need;
- keeps **git history as the transcript**. The working tree shows only the
  latest message; `git log -p` on the ticket is the whole audited
  conversation. No other message store is built;
- is **transient in the tree**: anything durable a conversation produces is
  written as a proper thing, and the ticket links to it;
- is a **domain-declared type, never reserved**. `read_board` skips reserved
  types on a status-keyed board, so a reserved `ticket` would never wake
  anyone. The substrate ships the template; each domain declares the type
  with its own actor names as statuses and `closed` as terminal.

**The safety rule, stated as part of the protocol.** A ticket carries
*requests*, never approvals or rulings. The recipient acts within its own
permissions, exactly as if the request had come from a human in chat; a
ticket grants nothing. Anything irreversible still goes to the human seat.
A peer-to-peer channel distributes *requests*; it must not become a way of
distributing *authority* (`mesh-safety-is-the-floor-not-the-topology`).

**The refusal, qualified.** `substrate-native-a2a`'s *"no new thing type for
the turn"* stands for artefact turns: where the work has a status, that
status is the carrier and nothing else is. It does not reach ad-hoc
messages, which have no artefact. The ticket is not a second declaration of
an existing turn; it is the first declaration of a turn that had nowhere to
live. Two agents never both write it — the addressee rule is what keeps it
from being the contended singleton the refusal feared.

## Consequences

- `standing-watch.md` 0.4 → 0.5: a *Ticket* section carrying the protocol,
  and the refusal list amended to say what the no-new-type rule covers.
- `substrate-native-a2a` 1.5 → 1.6: the refusal qualified in place; Phase 7
  — the ticket build and the live round trip Claude Code → Codex → Claude
  Code, which also discharges Phase 4's unticked PowerShell-route item.
- Shipped templates: `templates/ticket.md.template` and
  `templates/ad-hoc-message-loop.md.template` (a `workflow-definition` with
  `stages[].actor` declared), plus a commented `ticket` entry in
  `_schema.yaml.template`. Domains adopt by declaring the type and the
  definition; the engineering domain is the first adopter, by its own agent.
- No floor code. `tools/tests/test_watch.py::TestTicketLoop` pins that the
  existing contract already carries the ticket: addressee wakes, sender does
  not, body-only change wakes nobody, `closed` wakes nobody.
- The live test is the operator's. Its main risk is Codex's command timeout
  on a long blocking `mdllm watch --exit-on-wake`; the fallbacks are recorded
  on the plan.
