---
id: a-remembered-step-is-a-missing-actor
type: insight
status: active
version: 1.0
created: 2026-09-24
session: 2026-09-22
source: operator
confidence: high
origin: inferred
tags: [coherence, reconciliation, retrospective, dispatcher, loop, seat, actor]
linked_things:
  - id: closed-loop-operating-state
    relation: informs
    notes: "The dispatcher is the actor this names; the plan is where it lives."
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: extends
    notes: "That insight says a mechanised step quiets the rest. This one says what the rest are: steps with a check and no actor."
  - id: inflection-candidates-are-computable
    relation: references
    notes: "The question was computable a month before anyone computed an actor for it."
  - id: loop-turns-self-heal-2026-09-23
    relation: references
  - id: dispatcher-ticks-headless-on-the-substrate-machine-2026-09-23
    relation: references
---

# A step that waits on someone remembering is a missing actor, not a missing check

## The observation

The operator's question on 2026-09-23 was that coherence still drifts
although the mechanisms were built: change reconciliation is ruled the
driver's to declare, and "more often than not, it doesn't happen". The sweep
traced every hole he named and found the same shape three times. The cue
question was computed at every commit by the pre-commit advisory — and this
agent walked past it twice in one day. The retrospective's cadence was a
dated trigger that fired correctly — and nothing read it. The loop's rejected
push was recorded by `autopush` — to a session about to end. In every case
the *check* existed and was correct. What was missing was anyone whose job it
was to act on it at that moment.

## Why this is structural

A check writes to a reader. Where the reader is a person who must remember —
"raise a cue", "run the retrospective", "confirm from the ref" — the check's
output lands in the same channel as everything else competing for that
person's attention, and a correct check becomes wallpaper
(`a-check-that-always-fires-teaches-the-operator-to-ignore-it`). Adding
another check to the same channel makes it worse. The remedy that worked in
each case was an **actor**: something whose run *is* the step. The floor
raises the cue (`mdllm cues --raise`); the watch wakes the side that can heal
(`loop-turns-self-heal-2026-09-23`); the tick drafts the retrospective
(`dispatcher-ticks-headless-on-the-substrate-machine-2026-09-23`). The human
keeps only the part that is judgement — and that part is then *presented* as
a choice they must actively skip (`open-questions-arrive-as-a-prompt-2026-09-23`),
because a question described is a question passed over.

## The rule

When a step is found undone, ask first whether it had an actor before asking
whether it needs a better check. If the step is computable, give it one —
the floor at a boundary, the watch on a poll, the tick on a schedule. If it is
judgement, give the *presentation* an actor: emitted as options, recommended
first, skipped only on purpose. A human seat is for rulings, not for
remembering.
