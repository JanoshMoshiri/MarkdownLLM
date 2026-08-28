---
id: gates-census-ratified-2026-08-28
type: decision
status: made
version: 1.0
created: 2026-08-28
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [gates-census, ratification, seats, closed-loop, dispatcher, pilot]
informed_by:
  - id: gates-census-2026-08
    commit: 47f709099f6551ba6b1968ca1da26a2b5a0618c6
  - id: operator-queue-2026-08-28
    commit: c3b357cc1b66f0467f603df01bf5d6578bb9b991
  - id: closed-loop-operating-state
    commit: d818697185cdece9e50f8ad98fc93455ae81531c
  - id: settled-reasoning-is-standing-authority
    commit: c3b357cc1b66f0467f603df01bf5d6578bb9b991
linked_things:
  - id: gates-census-2026-08
    relation: implements
    notes: "The census this decision ratifies. Its twenty proposed verdicts are confirmed as proposed; the artifact goes stable on this ruling."
  - id: closed-loop-operating-state
    relation: implements
    notes: "Closes Phase 1's Done-When box, and rules Phase 4's pilot domain. Phase 2b's authority grant remains outstanding and is not covered here."
  - id: operator-queue-2026-08-28
    relation: informs
    notes: "Rules queue rows 1 and 5. Rows 2, 3 and 4 — the dispatcher grant, the release push, the two verified re-flips — stay open and stay the operator's."
  - id: settled-reasoning-is-standing-authority
    relation: complements
    notes: "The two rulings compose: that decision granted authority where reasoning is settled; this one settles which seats are consequence-permanent, so the standing grant now has a ratified exclusion list rather than a referenced proposal."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "The law the eight consequence-permanent rows enforce, unchanged and unnarrowed by this ratification."
---

# Decision: The Gates Census Is Ratified

Ruled by the operator, in session, 2026-08-28. The census's twenty proposed
verdicts are **confirmed as proposed** — no row flipped.

## What is now settled

- **Eight rows are consequence-permanent** and stay human by construction: the
  release push, granting publication authority, remote creation and first
  publish, `verified` flips on external things, history rewrite and deletion,
  money and external-party effects, authority grants and permission-bearing
  installations, and the boundary-terms file.
- **Six are designed seats working as designed** — conflict resolution,
  convergence and boundary calls, option-bearing retrospective outputs,
  deploy-when-felt lifts, operator-calendar work, and stall routing as a split
  (agent proposes with a default; operator picks at cadence).
- **Six are familiarity-shaped and move to structure.** Four had already moved
  in practice. Row 15 — ritual-sanctioned spec updates, status truthing,
  kernel regeneration, index rebuilds — and row 17 (insight triage and
  disposition) are agent execution from today, with **row 1's push as the
  review seat**. Row 16 (session launch and ritual invocation) moves on the
  dispatcher, whose grant is still outstanding. Row 18 (priority and status at
  write) moves now, escalating contention to a seat.

**The operator's standing surface, ratified: four seats, one push, one feel.**

## What this composes with

`settled-reasoning-is-standing-authority` granted the agent authority to act
where reasoning is already settled, and adopted this census's
consequence-permanent rows *by reference* as its exclusion list. Those rows
were proposals at the time. They are ratified now, so the standing grant rests
on a confirmed boundary rather than a proposed one. Nothing in the grant
widens: the excluded classes are exactly the eight above, and a widening of
the grant itself remains outside its own scope.

## The pilot, ruled in the same sitting

Phase 4's hands-off cycle runs on **`regulated-qms`** (operator's choice,
2026-08-28). It qualifies on the stated criterion: its definition is declared
*and* gap-free, with two real runs behind it, one of them closed with
attributable acceptance. The dispatcher will be installed there first, tied to
a scheduled run in the operator's working harness — chosen because it is the
harness already taking real work off him, not because it is the best-tested.

The pilot's shape is the one Phase 2a decided and the dispatch prompt carries:
the tick is dumb and carries no schedule; the domain's own already-declared
triggers *are* the schedule; each ritual runs under that repo's own contract,
as that domain's agent.

## What is NOT ratified here

Three Tier-1 items stay open and stay the operator's:

1. **The dispatcher authority grant** — permission-bearing, per row 7 and
   `agents-cannot-self-install-permission-bearing-hooks`. Ratifying the census
   does not grant it; it is a separate constructive act, once per harness.
2. **The release push** — the root's stack, and the review seat that row 15's
   verdict now leans on.
3. **The two stale mirrors' `verified` re-flips** — row 4 of the census,
   consequence-permanent.

The Seat 1 queue (the lifecycle ruling, the calculation-plan closure, the two
stalls, the three process gaps) is likewise unruled by this decision and stays
in the operator queue.

## Cross-harness evidence, recorded as intent

The operator stated the intent to exercise the dispatched shape in **two
further harnesses** as soon as possible, beyond the one carrying the pilot.
Recorded because the framework's own doctrine forbids inferring cross-harness
behaviour from one build: contract *emitted* is a separate evidence class from
*received whole*, *read*, *applied*, and *outcome-validated*, and every claim
made about the dispatcher outside its pilot harness is a claim until a run
evidences it.
