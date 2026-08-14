---
id: lifecycle-output-truncation-2026-08-14
type: artifact
status: stable
created: 2026-08-14
tags: [harness, lifecycle, truncation, execution-evidence, phase-5r]
linked_things:
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Third independent instance in two days: exit 0, hook_success, and the operator's orientation missing anyway."
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Found while migrating the estate onto the 5R.2 projection. Belongs to the lifecycle runner's output budget, a neutral port — returned rather than patched."
  - id: claude-gate-5r5-acceptance-2026-08-13
    relation: derived-from
    notes: "5R.5 fixed the TIME budget the same way this needs the OUTPUT budget fixing: the head of orientation is the part that must survive."
---

# Lifecycle output truncation drops the head of orientation

Found on 2026-08-14 while verifying the estate migration with real Claude
sessions. Not a migration defect — the projection works. It is a defect in
how the lifecycle runner spends its **output** budget, and it is the exact
counterpart of the time-budget defect closed at Gate 5R.5.

## The measurement

Real sessions, one per domain, reading the harness transcript:

| Domain | Emitted context | Truncated |
|---|---|---|
| large domain A | 2200 chars | **yes** |
| large domain B | 2200 chars | **yes** |
| small domain | 1952 chars | no |

Both large domains land on exactly 2200 characters and carry
`[earlier lifecycle output truncated]`. The small one sits just under the cap
and is complete.

## The defect: the wrong end survives

A bounded output is correct and deliberate — Codex's adapter declares
`additionalContextLimit: 2500`, and unbounded lifecycle output would be its
own problem. The defect is **which end is kept**.

The retained tail preserves the *end* of the orientation — the triggers line
— while dropping what precedes it: **version drift, velocity, and open
loops.** Those are the lines the operator orients from, and on the two
largest domains in the estate they are exactly what is lost.

So the session opens with the least load-bearing slice of the report, and the
first thing an agent is told about a large domain is the part that says
nothing is currently firing.

## Same family as the 5R.5 defect

This is the third instance in two days of a harness-bound path degrading
while reporting success:

1. the session gate that emitted the contract but never attested;
2. the orientation that exceeded a 25-second per-step budget and truncated;
3. this — the orientation that fits the time budget and is then cut by the
   output budget.

Every one exits 0 and produces `hook_success`. Only inspecting the *content*
reveals them, which is what `the-harness-bound-path-is-the-least-tested-path`
now has three confirmations for.

It also shows how a fix can move a limit rather than remove it: 5R.5 gave
orientation a protected share of *time*, and it now runs out of *characters*
instead. A budget that protects one resource and not the other protects
nothing in particular.

## The operator's constraint on any fix

Recorded because it shapes the design, not merely the priority:

> I don't mind cutting things of no value in the sessions and not
> orientation. But just because it's not of value today doesn't mean it's not
> going to be of value tomorrow.

That rules out a fix that hard-codes *what* is disposable. Estate-sync's
per-repo listing looks droppable today; the day a repo diverges, that line
is the most important text in the report. The operator also raised — without
claiming to know the implications — the possibility of an **exception that
lets a specific output exceed the limit on both sides**, and explicitly
flagged the Codex-side implications as unknown.

## Returned, not patched

The output budget lives with the lifecycle runner and its bindings — a
neutral port. Per the standing rule, an acceptance pass does not alter
neutral ports, so this is returned to the owner of that seam.

Two shapes worth weighing, neither chosen here:

- **Protect the head of the last step** rather than keeping the global tail,
  mirroring `protected_seconds` in the character dimension;
- **A declared per-step output share**, so a step that must survive says so,
  rather than the runner inferring importance from position.

Both keep a bound. Neither requires deciding, in advance and forever, which
content is worthless — which is the constraint above.
