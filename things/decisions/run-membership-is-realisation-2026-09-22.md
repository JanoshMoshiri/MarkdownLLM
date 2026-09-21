---
id: run-membership-is-realisation-2026-09-22
type: decision
status: made
version: 1.0
created: 2026-09-22
session: 2026-09-22
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [workflow-run, membership, standing-watch, scope, provenance, a2a]
informed_by:
  - id: between-sessions-surface-is-real-2026-09-21
    commit: dc673b5e41755511c47f0a98e7b97e9f6bd52aaf
  - id: workflow-state-specification
    commit: dc673b5e41755511c47f0a98e7b97e9f6bd52aaf
  - id: standing-watch-specification
    commit: dc673b5e41755511c47f0a98e7b97e9f6bd52aaf
linked_things:
  - id: between-sessions-surface-is-real-2026-09-21
    relation: extends
    notes: "That ruling named this debt and declined to pay it. This one pays it."
  - id: workflow-state-specification
    relation: informs
    notes: "The spec this ruling amends: 0.7 → 0.8, the Membership paragraph under Activation and Fulfilment and its Division-of-Labour row."
  - id: standing-watch-specification
    relation: informs
    notes: "The consumer that was waiting on it: `mdllm watch --run` reads this edge and no other."
  - id: substrate-native-a2a
    relation: informs
    notes: "Phase 6's first checkbox — the precondition — is this decision."
---

# Decision: A Run's Members Are the Things That Realise It

## Context

`standing-watch.md` specified the scope of a watch as a `workflow-run` and
stopped at a precondition: run membership was declared one way in the spec
and another in the live domain. `workflow-state.md` → *Activation and
Fulfilment* said a run's produced outputs carry `informed_by` naming the run.
The engineering domain attaches its design specs to their runs with
`linked_things: {id: <run>, relation: implements}` and carries no
`informed_by` on them at all. A scope built before this settled would read
whichever edge its author picked.

The question was put to the operator with its meaning made explicit: this is
not a field-name choice. `informed_by` says *I was caused by this run* —
origin, past-facing, provenance. `linked_things: implements` says *I am this
run's realisation* — function, present-facing, structure. A thing can be
produced under one run and be the realisation of another, so the two can
diverge, and whichever is chosen decides whether a thing's membership is about
where it came from or what it does.

## Inputs Considered

- **`workflow-state.md` 0.7** — the Activation and Fulfilment section, which
  had only ever specified the provenance direction and called it "produced
  evidence", never membership.
- **`standing-watch.md` 0.1** — the Scope section's stated precondition, and
  its three "for free" claims that depend on the run being the scope.
- **The live corpus** — two runs, two design specs, both attached by
  `implements`, neither by `informed_by`. The domain had already answered by
  practice before the spec asked.

## Options

1. **`informed_by` naming the run** — membership is origin. Consistent with the
   spec as written; would require the live domain to add a field it does not
   carry, and would make a thing's membership a fact about its history rather
   than its role.
2. **`linked_things: {relation: implements}`** — membership is function. Matches
   what the domain already does; leaves `informed_by` meaning exactly what
   provenance says it means; a thing can move between runs by re-declaring
   what it realises, without rewriting where it came from.
3. **Both required** — belt and braces. Rejected: two declarations of one fact
   is the drift shape the framework keeps paying for, and they *can* legitimately
   differ.
4. **A new structural field (`run:`)** — modelled on `definition:` and `parent`.
   Rejected: a singular structural pointer earns its own field when the floor
   must resolve exactly one target, and a thing may realise more than one run.

## Decision

**Option 2, ruled by the operator on 2026-09-22:** *"It needs to say I am this
run's realisation. Because that's what it is."*

Membership is function, not origin. A thing declares that it is a run's
realisation with `linked_things: {id: <run>, relation: implements}`, and that
edge — no other — is what the floor reads when it needs a run's members.
`informed_by` naming a run stays what it always was: provenance.

## Consequences

- `workflow-state.md` 0.7 → 0.8: a *Membership* paragraph under Activation and
  Fulfilment, and a Division-of-Labour row. Raised and answered as an
  inflection cue in the same commit
  (`cue-workflow-state-specification-2026-09-22`).
- `mdllm watch --run <id>` becomes buildable and is built: the board is the
  things that realise the named run, at the named definition's stages.
- `standing-watch.md` → *Scope* drops its precondition and corrects two
  claims that building the scope proved imprecise — the run and the
  definition a watch reads are two *different* definitions, and the pin that
  "comes for free" is the run's own, which only a vertical watch reads.
- The engineering domain's existing declarations are already conformant.
  Nothing there changes.
