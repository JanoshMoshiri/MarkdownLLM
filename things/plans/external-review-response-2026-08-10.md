---
id: external-review-response-2026-08-10
type: plan
status: in-progress
version: 2.0
created: 2026-08-11
priority: medium
tags: [reconciliation, review-response, doctrine, cadence]
linked_things:
  - id: coherence-mechanism-build
    relation: references
    notes: "The build successor. It owns the sequencing and names this plan as Phase 4's owner — so this plan survives shrunk, holding only R3/R4/R5, rather than retiring and dangling that pointer."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "R1 and R2 were routed here and are complete as routing; the backlog is their sole owner now"
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: references
    notes: "F4 encoded as its own insight — the asymptote claim, discovered in the nine-review record"
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: "F1's external corroboration lands as an evidence note on the already-promoted insight — one owner, no restatement"
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: references
    notes: "The loop's measured result supplied R3's dose–response evidence and superseded this plan's build sequencing"
---

# External Review Response — Residue

`reviews/REVIEW-external-2026-08-10.md` returned five recommendations. Four of
the five are now closed or owned elsewhere; this plan is what remains, kept
alive for one structural reason: `coherence-mechanism-build` deliberately does
not restate other plans' items, and its Phase 4 names *this* plan as the owner
of R3 and R4. Retiring it would dangle that pointer and orphan the doctrine
items in R5, which nothing else owns.

## Closed / superseded (2026-08-11)

- **R1, R2 — closed as routing.** Both landed in
  `mechanical-coherence-checks-backlog`, which is their sole owner. Nothing to
  track here.
- **Execution sequence — superseded** by `coherence-mechanism-build`, written
  with the eight-round loop's evidence this plan was staged to wait for. Its
  Phase 1 (derive the root's entry file) is the better-informed form of the
  preference order this plan proposed; its Phase 3 (flow probes) covers a layer
  this plan never saw. Read it, not this, for what to build and in what order.
- **Review-ordinal collision — resolved by practice.** Both records landed
  identified by date and kind (`REVIEW-loop-2026-08-10`,
  `REVIEW-external-2026-08-10`); neither carries an ordinal, which was the
  candidate fix. No further action.

## Open — the residue this plan owns

**R3 — cold-read cadence.** *What* to schedule is now measured: **one cold read
after a substantial release**, never a loop. The loop's finds decayed
6→7→6→6→7→4→3→3 with severity falling faster than count, and by round 8 every
finding was residue of the loop's own fixes
(`an-adversarial-review-loop-converges-on-its-own-fix-residue`). The mechanism
is the *blind* read — zero context, adversarial brief — which is the active
ingredient a general "review" does not reproduce. **Still open and the
operator's:** where the ritual lives — `retrospective.md`'s cadence doctrine, a
standing note in `reviews/` practice, or consciously declined as prose the
operator reliably performs.

**R4 — walk attestation, held.** A session-gate-shaped Warning for
definition-surface commits carrying no recorded walk. The hold stands and its
release condition is unchanged: re-judge only after the backlog's checks land,
because promoting restatements out of prose removes most of what the walk was
catching, and a warning added while its load is being removed is a cry-wolf
seed (`a-check-that-always-fires-teaches-the-operator-to-ignore-it`).

**R5 — doctrine, partly open.** Executed: F4 encoded as
`coherence-is-a-maintained-rate-not-a-state`; F1's external corroboration noted
on `hook-enforcement-has-three-anchors`. Open, and owned nowhere else: the
manifesto's "Standing On Shoulders" section predates the canon findings
(Parnas, Naur, Lehman, Weinberg each confirmed as independent rediscoveries)
and the field positioning — extending it is the operator's voice. *Closed 2026-08-11:* the
review's external literature claims are verified — the operator checked the
sources and the flip is committed with attribution.

## Done when

- [x] R1 / R2 routed to their owner and closed here
- [x] Doctrine insights created (F4, F1 corroboration)
- [x] Build sequencing superseded by `coherence-mechanism-build`
- [x] Ordinal collision resolved by date+kind naming
- [ ] R3 cadence home chosen, or consciously declined
- [ ] R4 re-judged after the backlog's checks land
- [ ] Manifesto Standing-on-Shoulders extension written, or consciously declined
- [x] Literature claims verified (2026-08-11, `verified_by: Janosh Moshiri` —
      the flip committed separately from the declaration, per the quarantine
      rule; canon citations confirmed at claim level, not page level)

When the remaining three close, this plan completes — there is nothing else
holding it open.
