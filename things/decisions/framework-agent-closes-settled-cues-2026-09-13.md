---
id: framework-agent-closes-settled-cues-2026-09-13
type: decision
status: made
version: 1.0
created: 2026-09-13
decided_by: the operator, in session, in voice, 2026-09-13
confidence: high
origin: stated
tags: [standing-authority, cue, change-reconciliation, self-healing, seat-protocol, closed-loop, framework-agent]
informed_by:
  - id: settled-reasoning-is-standing-authority
    commit: c3b357cc1b66f0467f603df01bf5d6578bb9b991
  - id: unattended-cue-carrier-2026-09-12
    commit: 069007b51977ac9150e1c8d5ffe9d7d9e7d7bfe7
  - id: feels-automatic-is-persistence-of-the-question
    commit: 05c22b26cf978c1faf3f72d047cc27eafe7ebca7
  - id: gates-census-ratified-2026-08-28
    commit: e27240d35c954ee43c3b4f5af2998afee51155c6
linked_things:
  - id: settled-reasoning-is-standing-authority
    relation: extends
    notes: "That ruling granted the agent authority to act where the corpus already holds the evidence and the direction; this one names the cue verdict as such an act."
  - id: unattended-cue-carrier-2026-09-12
    relation: extends
    notes: "Yesterday's ruling said an agent may answer on a person's stated ruling; today's says a decision already on the record IS that stated ruling, and the citation is the receipt."
  - id: feels-automatic-is-persistence-of-the-question
    relation: implements
    notes: "The link is the second half of that insight: the question persists, and a recorded ruling answers many of them at once."
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 3's seat narrows: a cue reaches the operator only when no recorded decision covers it and the reasoning is not settled. The first seat item with a carrier is also the first the agent may close."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "The boundary this ruling does not move: nothing in a cue verdict is irreversible — it is a commit, overturnable by editing — which is why it can be the agent's. The consequence-permanent rows stay exactly where the census put them."
  - id: cue-carrier
    relation: informs
    notes: "Phase 6's first real observation: the loop closed on the day the authority was granted — 28 cues answered by citation and settled reasoning, unraised 27 → 0."
---

# Decision: The Framework Agent Closes Settled Cues

Ruled by the operator, in session, in voice, 2026-09-13 — the morning after
the cue carrier was built and its first live reading showed 27 reasoned-from
things modified since the last retrospective with no verdict on any of them.
Recorded here because a ruling that lives only in conversation is not domain
state, and because this one changes who may write a particular kind of
record.

## The ruling, in the operator's words

*"It's time to close the loop. The intention behind all of this is that the
mechanism is intelligent enough to see the thing that needs to be done, and
it doesn't need to always require my judgment as the operator to make that
done. My view and reasoning has a limitation to the amount of things I can
remember — that is drastically increased with the ability that you can
traverse through the things, through frontmatter and linkages. We could
resolve this problem by adding nothing more, just linking. The intelligence
of the system grows with the system as the system grows. You don't always
need my ruling to do it if it's something that's sensible. This should be
self-healing, self-correcting. There should be a sovereignty and authority of
self-improvement from you as my domain agent, the framework domain agent. So
you do what you think needs to be done, because I agree."*

## What is granted

The **framework domain agent** — a session operating the framework root under
its own entry contract, with the operator present — holds standing authority
to **answer a reconciliation cue** in either of two ways, and to raise one
whenever it judges:

1. **By citation.** When a decision already on the record covers the change
   that raised the cue, the agent answers by pinning that decision in the
   cue's `informed_by` and saying so in `verdict_reason`. The human ruled
   once; the citation propagates it. This is
   `unattended-cue-carrier-2026-09-12`'s "an agent may answer on a person's
   stated ruling" with the stated ruling read from the corpus rather than
   from the conversation — which is where the operator's own formula lands:
   *nothing more, just linking.* One ruling answers many cues.

2. **On settled reasoning.** When no decision names the change but the
   agent's walk finds the reasoning settled by the corpus — the bar
   `settled-reasoning-is-standing-authority` already sets: the evidence
   recorded, the direction decided, precedent that transfers — the agent
   answers on its own walk and records the reasoning as the receipt. For an
   inflection whose direction is settled, that means running the four beats
   and sealing them, not merely marking the verdict.

In both cases the verdict is a commit, overturnable by the operator by
editing the cue thing. That reversibility is what makes it grantable at
all.

## What is not moved

- **The consequence-permanent rows** (`gates-census-ratified-2026-08-28`):
  the release push, publication authority, remote creation, `verified` flips
  on external things, history rewrite and deletion, money and external-party
  effects, authority grants, the boundary-terms file. A cue verdict touches
  none of them. This ruling widens nothing there and could not.
- **The unattended rule.** A dispatch run still raises and never answers
  (option 3 of the 2026-09-08 review's F5). The reason survives this ruling:
  a run is a depth-limited visitor with nobody present to overturn it in
  the same session, and `closed-loop-operating-state` Phase 4 has not yet
  produced a run that reached a ritual. Revisit on that evidence, not
  before.
- **The seat.** A cue with no covering decision and unsettled reasoning is
  still the operator's — raised, listed, and left open. What this ruling
  changes is that the seat receives only those, instead of every cue.
- **The bar for "sensible."** It is not the agent's taste; it is the
  standing-authority bar, and a verdict that cannot name its evidence and
  its direction is not settled and is not the agent's to give.

## Why this is the right shape, from the record

- `feels-automatic-is-persistence-of-the-question` (2026-09-12): what an
  operator asking for automation wants is that nothing be forgotten. The
  carrier persists the question; this ruling lets a recorded answer reach
  it. Together they make the loop close without mechanising a verdict
  nobody gave.
- `a-check-that-always-fires-teaches-the-operator-to-ignore-it`: 27 unraised
  on the first reading was already at the wallpaper line. Without citation
  the digest grows monotonically; with it, most of any backlog collapses to
  the handful of rulings it traces to. The link is what keeps the carrier
  honest at scale.
- `settled-reasoning-is-standing-authority` (2026-08-28): the operator ruled
  once already that waiting for a confirmation which adds no information is
  the defect, not the caution. A cue whose answer the corpus already holds
  is exactly such a confirmation.

## The first act under it

Executed in the same session: the 27 unraised subjects since the 27 August
retrospective, plus the one cue left open the day before, traced to four
rulings — the gates census and dispatch design (28–30 August), the
watertight-membrane sprint (30–31 August), the Desktop-to-onramp reversal
(3–7 September), and the conflict-lifecycle review (8–11 September) — each of
which had been walked and sealed by the session that made it. Twenty-eight
cues answered by citation or settled reasoning; the digest's line goes to
zero; the count to watch starts from there.
