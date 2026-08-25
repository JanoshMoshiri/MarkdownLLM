---
id: universal-workflow-methodology
type: specification
status: draft
version: 1.2
created: 2026-08-25
linked_things:
  - id: workflow-state-specification
    relation: implements
    notes: "The methodology's stage graph is expressed in the workflow-definition shape that spec owns; a domain specialising this methodology mints its own definition and runs."
  - id: a-true-primitive-is-discovered-not-authored
    relation: references
    notes: "The integration posture: the methodology arrived as doctrine the existing primitives already carry — zero mechanism was added to house it."
---

# The Universal Workflow Methodology

The general method for approaching any problem in an evidence-driven,
analytical, iterable way — a software build, a regulated change control, a
one-shot record generation. Authored by Janosh Moshiri as *Universal
Development Methodology v1.0*; integrated 2026-08-25 under its truer name
(the method is not development-specific), and promoted from hosted content
to this spec the same day: the methodology is **foundation**, so it
reaches domains the way foundation does.

**Distribution — the correction that moved it here (2026-08-25):** this
spec arrives at every domain through the framework version and
`domain-refresh.md`, exactly as `thing.md` does. It is **never** imported
over a porch: the face/import/quarantine machinery is the domain↔domain
axis, and conflating the two channels put the foundation on the wrong
one. A domain does not import the methodology — it *receives* it with the
framework and **specialises** it: minting its own `workflow-definition`
(per `workflow-state.md`) whose stages realise these decisions for its
context, linked `implements` to this spec.

**Core idea** (from the source document): each stage establishes enough
clarity to enter the next. Progression is evidence-led rather than
automatic and may result in continuing, revising, deferring or stopping.
The structure remains constant while the activities and evidence within it
vary according to context, scale and risk.

Those four progression outcomes are the four moves a `workflow-run`
already has:

| Progression outcome | Run mechanics (workflow-state.md) |
|---|---|
| Continuing | advance `current_stage` along a forward edge |
| Revising | move along the declared backward edge |
| Deferring | `status: paused` |
| Stopping | `status: abandoned` |

## The seven stages

Each stage is a decision with a guiding question and one named output —
the output is the stage's exit gate. A specialising definition keeps the
decisions and re-names or subdivides the stages as its context demands
(worked example in `operating-model.md`). The reference stage graph, in
the workflow-definition shape a domain copies and adapts:

```yaml
stages:
  - id: define-need
    to: [assess-current]
  - id: assess-current
    to: [define-prioritise, define-need]
  - id: define-prioritise
    to: [set-mvp-target, assess-current]
  - id: set-mvp-target
    to: [design-plan, define-prioritise]
  - id: design-plan
    to: [execute, set-mvp-target]
  - id: execute
    to: [review-verify, design-plan]
  - id: review-verify
    to: []
```

**define-need** — *What are we trying to solve, and for who?*
Clearly describe the need, problem or opportunity before assessing
possible change. Identify who experiences it, why it matters, the outcome
sought, the boundaries of the problem and the assumptions that still need
to be tested. Avoid prematurely defining a solution.
Output: agreed problem statement, intended outcome and initial scope.

**assess-current** — *Where are we now?*
Establish what exists, how it operates, who it affects, and the evidenced
problems, pain points, constraints, dependencies and risks.
Output: current-state assessment and case for change.

**define-prioritise** — *Where do we need to go, and why?*
Turn the evidence into a defined direction. Identify the required
outcomes, assess risk, impact and value, and prioritise the changes that
are justified.
Output: prioritised outcomes and change objectives.

**set-mvp-target** — *What is the smallest acceptable destination?*
Define the minimum outcomes, capabilities and controls needed to reach an
acceptable position, including how it will be owned, operated, supported
and monitored. Keep future aspiration separate.
Output: minimum viable target state and success criteria.

**design-plan** — *How will we get there?*
Compare the current and target states, uncover the constituent pieces of
work, define requirements and dependencies, and assemble them into a
coherent design and sequenced transition plan.
Output: solution design, work packages and plan.

**execute** — *How will we deliver it under control?*
Perform the planned work while managing ownership, progress, decisions,
risks, issues, dependencies, changes and evidence. Validate outputs as
the work proceeds.
Output: completed work and delivery evidence.

**review-verify** — *Did we achieve the target state?*
Compare the delivered state with the minimum target and success criteria.
Use suitable review, assessment or testing, record residual gaps and feed
the verified outcome into the next assessment cycle.
Output: outcome assessment and improvement backlog.

## The loop

*Review becomes evidence for the next current-state assessment.* The loop
is deliberately **not** a cyclic stage edge: `review-verify` is terminal,
and iteration is a new run. The evidence hand-off is structural: the next
run pins the prior run's outcome assessment via `informed_by`, making the
loop a provenance edge between runs rather than an arrow inside one.

## Two shapes of application

Stated by the author 2026-08-25, extending the v1.0 document. The same
seven decisions carry two shapes of work, and the structural difference
between them is **where `review-verify`'s output lands**:

- **Accumulative** — chained runs converging on or evolving a goal:
  development, migration, remediation. The review feeds the *next run's*
  `assess-current` (an `informed_by` pin run-to-run). The chain refines
  the work.
- **Repeatable** — sibling runs of one stable definition, each instanced
  by a demand: an automation, a procedure, a record generation. Similar
  outcome each time under different variants. The review's improvement
  backlog feeds the *definition's own evolution*, not the next run. The
  series refines the process.

The two interleave inside any operational module — an accumulative arc
delivers operating state, repeatable loops maintain it. That composition
is `operating-model.md`'s subject, not this spec's.

## Capacity at the cut

Capacity is considered where the task set falls out and the minimal set
is cut — `set-mvp-target` into `design-plan` — and nowhere else as a
standing concern. It is not inherently human capacity: one resolution of
"who does this" is *nobody — automate it*, which spawns a child
accumulative arc whose deliverable is a new repeatable definition. One
shape manufactures the other; the fractal closes on itself.

## Proportionate use

From the source document's *stable structure*: the seven stages describe
the decisions that must be made, not a fixed set of documents, roles or
ceremonies. Each application defines the proportionate activities,
evidence, controls and artefacts required within them. For a small,
low-risk change, each stage may be represented by a few lines in a single
working note. For a shared, regulated or operationally important service,
the same stages may contain formal evidence, requirements, design
records, testing, approvals, support arrangements and controlled change
records. **The depth changes; the flow does not.**

> **Working rule:** use the lightest process that still provides enough
> evidence, control, ownership and traceability for the consequences of
> failure.

(This is the framework's own restraint principle, met from the other
direction — and the working rule is a consequence-scaled gate: process
weight is set by what failure would cost, not by what the stage could
theoretically carry.)

## Principles carried through every stage

| Principle | Meaning | Where the substrate already holds it |
|---|---|---|
| Evidence and traceability | Preserve a proportionate line from the original case for change through decisions, work performed and verification of the outcome. | The provenance chain: `type: decision` with `informed_by` pins; git as the event stream. |
| Ownership and accountability | Make clear who owns decisions, delivery and the resulting operational state. | `decided_by`, `verified_by`, the run's `held_by` claim. |
| Constraints and dependencies | Identify and refine the boundaries that shape what is achievable and how the transition can proceed. | `dependencies` / `blocks` structural references; floor-checked. |
| Fit for purpose | Apply the quality, risk and control requirements relevant to the context rather than prescribing every possible requirement universally. | Emergent schema; deploy-when-felt; the restraint rule on prompts and hooks. |

The third column is orientation, not a claim of mechanical enforcement:
the substrate holds each principle's *record*; honouring it in the work
remains the judgement of whoever runs the stage.

## Qualities that support longevity

The target state and design should be fit for purpose. Wherever
relevant, also test the whole operating state against four standing
qualities:

- **Maintainable** — can it be understood, supported and changed safely?
- **Extendable** — can future needs be added without excessive rework?
- **Manageable** — can ownership, operation and change be controlled?
- **Monitorable** — can health, use, failure and outcomes be observed?

These are questions asked of the *target state* at `set-mvp-target` and
re-asked of the *delivered state* at `review-verify` — the same four
lenses at both ends of the transition.

## Position in the framework

The framework's existing rituals already trace arcs of this loop:
session orientation and the velocity digest are a standing current-state
assessment; triggers are declared evidence that a need exists;
change-reconciliation's cue → assimilate → walk → seal is a compressed
traversal for one inflection; a retrospective is review-and-verify at
domain radius; a floor sprint is a full traversal. This spec names the
spine those rituals share — a discovery of common shape, not a new
authority over them. Each ritual's own spec remains its authority.

`substrate-floor-development` is the framework's own specialisation: the
same seven decisions with two substrate-specific gates added
(reconcile's consistency walk, seal's human gates) — the edge lives on
that thing. How many loops compose into modules and an estate is
`operating-model.md`'s subject.

## History

Born 2026-08-25 as an exposed `workflow-definition` thing
(`things/workflows/`, v1.0–v1.1); promoted to this spec the same day
when the operator corrected the distribution channel. The id travelled
with the content, so every edge minted against the thing resolves here
unchanged. The v1.0 stage prose is the source document's, transcribed
complete; v1.1 added the two shapes and the capacity closure (operator,
in session); v1.2 is this promotion.
