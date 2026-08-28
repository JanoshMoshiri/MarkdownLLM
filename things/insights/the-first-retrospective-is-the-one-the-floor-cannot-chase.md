---
id: the-first-retrospective-is-the-one-the-floor-cannot-chase
type: insight
status: active
version: 1.0
created: 2026-08-28
session: 2026-08-28
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Dismiss when the first-retrospective case has its own admission rule, or when a ruling records that the 60-day silence is intended for it too. Promote into retrospective.md + the floor check on a second independent sighting, or immediately if a domain's first retrospective is again produced only by hand-direction."
linked_things:
  - id: retrospective-specification
    relation: informs
    notes: "The spec says monthly, or after a significant milestone. The floor's own cadence check cannot speak for the first 60 days, so the two disagree precisely over first retrospectives."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: extends
    notes: "The doctrine the young-domain gate correctly implements — and the case where implementing it costs more than it saves, because the gate written for the recurring case also silences the never-written one."
  - id: a-uniform-answer-is-a-dead-judgment
    relation: complements
    notes: "Its sibling at the cadence layer: a check that cannot fire in a window is indistinguishable, from the operator's seat, from a check reporting that all is well there."
  - id: existence-is-not-currency
    relation: supports
    notes: "The branch exists in the code and reads as coverage; it is unreachable in the window where it is the only applicable branch. Existing is not the same as being able to fire."
---

# The First Retrospective Is the One the Floor Cannot Chase

## The Insight

`validate.py`'s retrospective-cadence check carries two branches: one for *no
retrospective has ever been written*, and one for *none since <date>*. Both sit
behind a single guard — `if (today - born).days <= 60: return []`.

The guard is correct doctrine for the second branch and wrong for the first.
**A domain younger than 60 days cannot be told it has never written a
retrospective, which is exactly the window in which that is the only thing
worth telling it.** The branch written for the first-retrospective case is
unreachable for precisely the period where it is the only applicable case.

Meanwhile `retrospective.md` says a retrospective is due when the domain
*"crosses a monthly boundary with meaningful activity"*, and names volume and
milestone triggers besides. Spec and floor therefore disagree over exactly one
class of document — the first one — and the floor is the surface an operator
actually reads.

## The Evidence (2026-08-28)

Two first retrospectives were written this day, both produced by hand-direction
rather than by any chase:

- `regulated-prom` — born 2026-07-24, active, 55 things. Under the guard its
  cadence check first speaks **2026-09-22**: two months of silence over a
  domain whose retrospective, when finally written, found three decision
  packets drafted and undelivered, a 35-day-old governance contradiction born
  on day one, and an insight that had predicted its own domain's staleness
  failure and was never adopted.
- The estate's largest unreflected corpus — born 2026-08-01 — likewise silent
  under the guard, and likewise full of findings on first reading.

Both were found by an estate-radius synthesis reading the layer beneath it,
not by either domain's own floor. The synthesis is the instrument that caught
them, and the synthesis is operator-invoked.

## Why It Matters

The estate's own measured finding is that **first retrospectives recover the
most** — every first-generation retrospective in this estate found a backlog
its domain had accumulated invisibly, and every second-period one then showed
the discipline holding. So the highest-yield instance of the ritual is the one
the floor is structurally least able to prompt, and it therefore depends on
someone remembering — which is the condition the whole cadence mechanism
exists to remove (`repeated-drift-promotes-a-fact-into-the-floor`, one layer
up).

There is a real tension to resolve rather than a simple bug to swat, which is
why this is recorded rather than built:

- The young-domain gate exists for a good reason
  (`a-check-that-always-fires-teaches-the-operator-to-ignore-it`) — a
  three-day-old domain nagged for a retrospective teaches the operator to
  discount the check.
- But *age* is the wrong axis for the first one. The spec's own trigger is
  **activity across a boundary**, and the estate's cadence finding (F9) was
  explicit that **volume beats time**: 34 quiet days produced one domain's
  first backlog and 16 busy days produced a larger one.

## The Candidate Remedies (not chosen here)

1. **Split the guard.** Keep the 60-day silence for *none since <date>*; admit
   the never-written branch on the spec's own condition — a monthly boundary
   crossed *with meaningful activity* (both operands are already computed in
   this function: `born` and the recent-commit count).
2. **Volume rule.** Admit on things-or-commits-since-birth rather than age,
   which follows F9's measured conclusion directly.
3. **Rule the silence intended.** Record that a domain's first 60 days are
   deliberately unchased, and accept that first retrospectives are
   operator-initiated by design.

All three are defensible; choosing between them is a cadence-doctrine call for
`retrospective.md`, not a code fix. The mechanical half is decided either way:
whichever admission rule is chosen, the two branches should not share one
guard.

## The Shape Worth Keeping

A guard written for the steady-state case, applied to the first-instance case,
silences exactly the instance with the most to say. Look for it wherever a
check has a "never happened yet" branch behind a maturity gate: the gate is
usually reasoning about *recurrence*, and the first instance is not a
recurrence.
