---
id: protecting-one-budget-displaces-the-failure-into-the-other
type: insight
status: active
version: 1.0
created: 2026-08-16
session: 2026-08-16
source: field
confidence: medium
origin: stated
linked_things:
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: complements
    notes: "That insight explains why the failure was invisible; this one explains why fixing it once was not enough."
  - id: lifecycle-output-truncation-2026-08-14
    relation: derived-from
    notes: "The second failure, arriving in the character dimension immediately after the first was fixed in the time dimension."
  - id: claude-gate-6r-acceptance-2026-08-16
    relation: derived-from
    notes: "The correction that closed the displaced failure, by applying the same protection mechanism in the unprotected dimension."
---

# Protecting one budget displaces the failure into the unprotected one

## The observation

A lifecycle step was truncated by a **time** budget: orientation exceeded its
25-second per-step slice and was cut. The fix gave it a protected share of
time that could absorb capacity earlier steps did not use, and the step then
completed.

It was still truncated — now by the **character** budget. The same content,
the same operator-visible loss, one dimension over. Both bounds were correct
individually; neither was wrong to exist. The pressure simply moved to
whichever dimension had no allocation policy.

The second fix applied the same mechanism in the second dimension: a
protected share per step, inheritable from unused capacity, inside an
absolute total.

## The rule

**When a resource is bounded along more than one dimension, protecting one
dimension relocates the failure rather than removing it.** A budget that
allocates time but not output — or output but not time, or either but not
count — protects nothing in particular, because the constrained thing fails
at whichever bound is still first-come-first-served.

The practical test when fixing a truncation, timeout, or quota defect: *name
every dimension in which this output is bounded, and say what the policy is
for each.* An unstated policy is "whoever gets there first", which is exactly
the behaviour just removed from the other dimension.

## Scope and evidence

One clear instance, recorded honestly: time (2026-08-13, Gate 5R.5) then
characters (2026-08-16, Gate 6R), same step, same operator-visible symptom,
five days apart. That is enough to name the mechanism and not enough to claim
a law — a third dimension has not been observed. Treat it as a checklist
prompt when bounding anything, not as a prediction that a third failure is
waiting.

## Why it is easy to miss

The first fix *works*, and its evidence is genuine: the step completes, the
tests pass, the acceptance record is honest. Nothing about that record is
wrong — it simply measured the dimension that had just been repaired. The
displaced failure is only visible where the resource is actually scarce,
which on this estate meant the two largest domains and nowhere else.
