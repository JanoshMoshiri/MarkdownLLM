---
id: unattended-cue-carrier-2026-09-12
type: decision
status: made
version: 1.0
created: 2026-09-12
decided_by: the operator, in session, 2026-09-12 — on the agent's recommendation from the record
confidence: high
origin: stated
tags: [change-reconciliation, cue, seat-protocol, dispatcher, authority-receipt, closed-loop]
informed_by:
  - id: review-external-conflict-lifecycle-2026-09-08
    commit: 7c5c21111295793ccb50ec41a67545bf62c82f47
  - id: inflection-candidates-are-computable
    commit: 7c5c21111295793ccb50ec41a67545bf62c82f47
  - id: closed-loop-operating-state
    commit: 7c5c21111295793ccb50ec41a67545bf62c82f47
linked_things:
  - id: review-external-conflict-lifecycle-2026-09-08
    relation: references
    notes: "F5 named the three options and recorded the recommendation; this decision is the ruling it was waiting for."
  - id: inflection-candidates-are-computable
    relation: implements
    notes: "The cue QUESTION is mechanical and the VERDICT is human — this decision gives the question a place to wait for the verdict."
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 3's added row (who declares an inflection when a run commits) is ruled here; the persisted cue is the first floor-readable seat-queue item."
  - id: change-reconciliation-specification
    relation: extends
    notes: "The Cue beat gains a carrier; the driver-names-the-inflection rule is unchanged."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "A run raises; it does not answer. The verdict is a ruling, and rulings stay with the human."
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: implements
    notes: "The countermeasure that insight names — make the seam loud — is what the session-start line does: the unanswered question is emitted every session until answered."
---

# Decision: An Unanswered Cue Persists, Loudly, Until A Human Answers It

Ruled by the operator, in session, 2026-09-12. The question was F5 of the
2026-09-08 external review — *who declares the inflection when an unattended
agent commits?* — and the same question from the other side, in the
operator's own words the same day: *"make it loud so the user doesn't have to
remember."*

## The ruling

**Option 3, with option 2's net beneath it.** A session — attended or not —
may **raise** a cue but may not **answer** it. The cue is a persisted thing
(`type: cue`, reserved) with a `subject` (the reasoned-from thing that was
modified), a `raised_at` commit pin, and a `status` of `open` until a human
records a `verdict` — `inflection` or `not-inflection` — with a
`verdict_reason`. That pair is the authority receipt: saying *no* to a named
question is a decision, where not being asked was drift.

The net beneath: any cue still open at retrospective cadence is answered
there, by scan 4 (retrospective reconciliation), which was wired 2026-09-08.
A cue missed at change time is therefore a cue answered late, never a cue
lost.

## What the floor does, and does not do

- **Computes the question.** `mdllm cues` reads the commit stream since the
  last retrospective and lists every reasoned-from thing modified in that
  window that no cue thing covers — *unraised* — alongside every cue thing
  still `open` — *unanswered*. The session-start digest emits both, every
  session, under one heading. This is the loudness the operator asked for:
  the question waits in the digest rather than in anyone's memory.
- **Checks the receipt's shape.** An `answered` cue must carry a verdict from
  the two-value set and a non-empty reason (Error); an `open` cue must not
  carry a verdict (Warning); `subject` must resolve (Error); `raised_at` must
  resolve as a local pin (Error, through the existing structural-pin check).
- **Never answers.** No floor path sets a verdict. No hook creates a cue
  thing. The floor makes the question impossible to not see; the answer is a
  write a person makes or an agent makes on a person's stated ruling.

## What a dispatch run does

A run that modifies a reasoned-from thing raises the cue as part of its own
commit — a cue thing, `status: open`, `raised_by` naming the launch — and
files it as a seat-queue item in its digest. It does not answer it, does not
run the reconciliation pass on its own initiative, and does not treat a cue it
raised as a reason to widen its scope. This is `dispatch-loop.md`'s step 6
(respect the seats) with the cue named explicitly as seat-shaped.

## Why not the other two options

**Option 1 — runs cannot inflect; anything that would be one blocks for the
seat.** Correct in spirit, wrong in mechanism: the run does not know whether
its change *is* an inflection (that is the verdict), so it would have to block
on every modification of a reasoned-from thing, which is most useful work.
Blocking is the shape of option 1; option 3 keeps the work and queues the
question.

**Option 2 alone — presume un-reconciled, sweep at retrospective.** Already
true and now wired; insufficient alone because the retrospective is itself
human-invoked, and the record shows both nets down together in August 2026.
It stays as the net; it is not the primary.

## What this does not decide

- The seat queue's *assembly* — how every seat-shaped item (options,
  ambiguity, irreversibles, breakage, and now cues) is regenerated into one
  operator-facing view. Phase 3 of `closed-loop-operating-state` still
  carries that; the cue is the first such item with a floor-readable carrier,
  and it is the template the others will copy or refute.
- Any change to who declares an inflection when a human is at the keyboard —
  unchanged, and reaffirmed: the Cue verdict is the driver's.
- Whether the cue's shape survives contact. The operator's own framing:
  *"things might change shape after some time"* — this is deploy-and-see,
  ruled on the record so the seeing has something to compare against.

> **Postscript, 2026-09-13 — not part of the ruling.** It changed shape the
> next morning, in one direction: "an agent may answer on a person's stated
> ruling" became "a decision already on the record *is* that stated ruling,
> and the citation is the receipt" — `framework-agent-closes-settled-cues-
> 2026-09-13`, which extends this decision and leaves its unattended rule
> intact. The 27 unraised the first reading found were closed under it the
> same day.
