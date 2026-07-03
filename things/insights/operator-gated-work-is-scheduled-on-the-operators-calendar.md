---
id: operator-gated-work-is-scheduled-on-the-operators-calendar
type: insight
status: active
version: 1.0
created: 2026-07-03
session: 2026-07-03
source: both
confidence: high
origin: synthesised
tags: [evidence, backlog, prioritisation, operator, loop-limits, scheduling]
linked_things:
  - id: felt-deployment-lands-in-undisclosable-work
    relation: extends
    notes: "That insight explains why the strongest evidence lives outside the repo; this one names the scheduling consequence — the loop cannot fetch it, so the operator's calendar is the unit of planning."
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "The v2.0 reframe of the backlog operationalises this: two operator sessions with agent support, agent pre-work listed separately."
---

# Operator-Gated Work Is Scheduled on the Operator's Calendar, Not in a Backlog Row

## The Insight

A corrective loop staffed by an agent **can only complete artifacts the agent
can produce.** Work whose missing input is an operator act — a disclosure
decision, a remembered conversation, a run on the operator's machine, a second
human's hour — will sit at the top of every priority list and never move, no
matter how correctly it is ranked, because ranking assigns it to the wrong
executor. The backlog row makes the work *look* agent-shaped; each session the
loop then does the highest agent-shaped work instead, and the gap reads —
falsely — as the loop "choosing" mechanism over evidence.

The worked case: every framework review from June 11 to July 2 (four sittings,
two reviewers) ranked the sanitised validation record first; over the same
weeks the loop shipped floors, kernels, and remediations while `evidence/`
stayed a README and a template. Review 6 named the pattern: not a
prioritisation failure but a capability boundary. Each top evidence item needs
the operator — the validation record is *dictation* of a session only the
operator witnessed; the longitudinal eval is *runs* on the operator's machine.

The fix is a reframe, not a re-rank: label the item an **operator session with
agent support**, split out the agent pre-work (templates, fixtures, protocols
— deliverable before the session so the operator's time is spent on the part
only they can do), and put the session on the operator's calendar. A cadence
like "felt-when-felt" cannot pace this work either — the loop never *feels*
work it cannot start.

## How to Apply

When a backlog item survives multiple prioritisation passes unmoved, ask
**"who is the missing input's producer?"** before asking "why wasn't this
prioritised?" If the answer is the operator, rewrite the item as a scheduled
operator session, extract the agent pre-work as its own row, and stop
expecting the loop to close it.

## Context

Synthesised 2026-07-03 from review 6's strategic reading of the three-week
evidence gap, adopted the same session as `evidence-and-eval-backlog` v2.0
(two operator sessions defined; "felt-when-felt" retired for this class).
