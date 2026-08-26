---
id: a-check-is-only-as-trustworthy-as-who-controls-its-inputs
type: insight
status: active
version: 1.0
created: 2026-08-26
session: 2026-08-25/26
source: both
confidence: high
origin: stated
tags: [floor, checks, authority, self-authorization, versioning, failure-modes]
linked_things:
  - id: workflow-state-specification
    relation: informs
    notes: "The revision-binding section's self-authorization guard exists for this reason, and the reason is not obvious from the rule — without it the rule reads as bureaucratic separation rather than the thing that keeps the check independent."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: complements
    notes: "Same family: both are about where authority sits rather than what a mechanism can compute. That one defers the irreversible to the human; this one keeps a check's inputs out of the hands of the party it checks."
---

# A Check Is Only As Trustworthy As Who Controls Its Inputs

## The Insight

The floor's workflow-transition check asks one question: *does the
definition declare this edge?* It has been trustworthy for a specific
structural reason that is easy to miss — the answer comes from the
**prior committed** definition, a surface the commit being checked cannot
rewrite. The check is independent because its input is out of the
candidate's reach.

Revision binding (`workflow-state.md` v0.6) improves that check. A run
names the exact committed revision that governs it, so the floor stops
inferring which procedure version applies and reads it. Strictly better
— except that the improvement hands the run **control of which
definition answers the question**:

> A run that can change its own pin can pick the revision whose graph
> permits the move it wants, and the check will faithfully confirm it.

The same edit makes the check sharper and forgeable at once. Nothing
about the mechanism looks wrong; it is the *authority* over the new input
that moved, and authority has no representation in the bytes.

## The General Rule

**When you add an input to a check, ask who controls that input.** If the
answer is "the party being checked," the check has quietly become
advisory, however rigorous its logic. This is not specific to workflows —
it is the shape of every pinning, versioning, or self-declaration
mechanism: a dependency that names its own lockfile, a document that
declares which policy governs it, a run that names its definition
revision.

## The Remedy Shape

Do not remove the input — the sharper check is worth having. **Separate
the acts in time**: forbid changing the input and exercising the check in
the same commit. A pin change is its own meaning boundary; a cursor move
is another. Each is then checked against a state its own commit could not
author. The separation is not ceremony; it is the entire reason the check
still means something.

## Provenance

Found while designing F18 (2026-08-26), listed among the sprint's
constraints, and pinned by the operator in session — *"specifically the
first one, the self authorization hole, we can't let that slip"* — before
any of the mechanism was built. Recorded because the guard's rule is
cheap to write and cheap to later "simplify away" by someone who never
saw what it was protecting.
