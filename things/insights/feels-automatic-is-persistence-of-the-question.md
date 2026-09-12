---
id: feels-automatic-is-persistence-of-the-question
type: insight
status: active
version: 1.0
created: 2026-09-12
session: 2026-09-12
source: both
confidence: high
origin: synthesised
tags: [automation, seat-protocol, cue, change-reconciliation, onramp, operator-experience]
linked_things:
  - id: unattended-cue-carrier-2026-09-12
    relation: derived-from
    notes: "The ruling this generalises: the operator asked for reconciliation to be automatic and ruled, on the record, for the question to persist and the verdict to stay human."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: supports
    notes: "Why the answer cannot be automated: judgement is pulled, not injected — automating the invocation produces the motions, not the verdict."
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: supports
    notes: "Why persistence is the safe form of automation: it makes the seam loud instead of mechanising around it."
  - id: closed-loop-operating-state
    relation: informs
    notes: "Phase 3's queue assembly is this insight applied to the other seat items — options, ambiguity, irreversibles, breakage — each wanting a carrier that waits, not a mechanism that decides."
  - id: operator-seat-and-harness-native-onramp
    relation: informs
    notes: "A newcomer's 'it should just work' has the same shape: what they need forgotten-proof is the sync and the refresh, not the judgement."
---

# "Feels automatic" is the question persisting, not the answer being automated

## The Insight

When an operator says a ritual *should just be automatic*, what they are
usually asking for is that **nothing be forgotten** — not that the judgement
be made by the machine. The two come apart cleanly once separated: the
*question* (does anything reason from what just changed? is this due? does
this contradict that?) is mechanical and can be computed and re-emitted
every session until answered; the *answer* is a verdict, and every time the
framework has tried to mechanise a verdict it has found the reasons not to
(`emitted-content-is-read-instructed-content-is-economised`,
`partial-coverage-quiets-the-uncovered-steps`,
`an-agent-in-a-loop-optimises-the-loop-not-the-goal`). What makes a system
*feel* automatic is that the question waits somewhere the operator will
see it without having to remember it. That is persistence, and persistence
is cheap, safe and honest in a way automation of the answer is not.

## Why It Matters

- It is a **diagnostic for the next automation request.** Before building
  a mechanism that acts, ask: is the felt gap that the *acting* is missing,
  or that the *remembering* is? On 2026-09-12 it was the remembering — the
  cue question had been mechanical for five weeks and printed to stdout at
  3am; the fix was a carrier (`type: cue`) and a digest line, and the
  operator's own framing on ruling it was "make it loud so the user doesn't
  have to remember."
- It names the shape every seat item wants. Conflicts already have it
  (`type: conflict`, open until ruled); cues now have it; options,
  irreversibles and breakage do not yet. The closed-loop plan's Phase 3 —
  the seat queue's *assembly* — is this insight applied to the rest: one
  view that re-lists every waiting question until a human answers it.
- It bounds what the onramp should automate for a newcomer: the sync, the
  refresh, the floor — everything whose *absence* would be a thing to
  remember — and none of the rulings.

## Context

The operator opened 2026-09-12 with the felt need to "integrate change
reconciliation into everything… every single time there's a change… it
should be automatic if you've got network access," against an external
review that had independently found the same gap from the other side
(finding 4: human authority lacks durable representation; finding 5 of the
2026-09-08 review: who declares an inflection when a run commits). The
record answered from its own insights: the question is automatic, the
verdict is human, and what was missing was a place for the question to
wait. The operator ruled exactly that, and the carrier was built and walked
against itself the same day.

Dismissal condition: dismissed if a persisted-question carrier is found to
produce the same skip rate as the printed advisory it replaced — that is,
if loudness at session start does not change whether the verdict gets
given. Promoted if the seat-queue assembly (closed-loop Phase 3) lands on
this principle for the remaining seat classes.
