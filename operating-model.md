---
id: operating-model-specification
type: specification
status: draft
version: 0.1
created: 2026-08-25
linked_things:
  - id: universal-workflow-methodology
    relation: extends
    notes: "The atom this spec composes. The atom defines one loop and its two shapes; this spec defines how many loops run together and how the compositions relate."
  - id: workflow-state-specification
    relation: extends
    notes: "Definitions and runs are the mechanics every composition statement here resolves to; nothing in this spec exists outside them."
  - id: trigger-specification
    relation: complements
    notes: "The operating interval's sensors — declared triggers are how a module at rest raises its next need."
  - id: provenance-specification
    relation: complements
    notes: "Inter-run and inter-module evidence chains; the estate's audit line is the union of module chains crossing at faces."
  - id: coordination-claim-specification
    relation: complements
    notes: "Concurrent loops contending for one thing use the advisory claim; composition multiplies the occasions."
  - id: interface-specification
    relation: references
    notes: "Module-to-module composition rests on served faces — the exposure and egress semantics live there and in thing.md."
---

# The Operating Model — Composing the Atom

## What This Specifies

`universal-workflow-methodology` (a thing, not a spec — the framework
hosts it as exposed content) defines the **atom**: one loop of seven
evidence-gated decisions, applied in two shapes. This spec defines
**composition**: how many atoms run together inside a module, how modules
compose into an estate, and what an application declares to make its
composition auditable.

It is doctrine over existing primitives — definitions, runs, cursors,
pins, triggers, claims, served faces. It adds **no mechanism, no types,
no fields**. If that ever stops being true of a draft, see The Razor.

**The operating model is read, not run.** You instance and run atoms
(`workflow-run`s). The operating model is the declared composition a
module or estate *exhibits* — auditable by reading its declarations, never
itself a thing with a cursor.

## The Module

A module is an operational area — quality, engineering, finance, a
personal capacity — that runs many atoms over its own state. In this
framework a module is typically a domain (its own corpus and repo); a
large domain may hold several. The module is the unit that:

- runs **accumulative arcs** and **repeatable loops** (the atom's two
  shapes — defined there, not restated here),
- owns the **operating state** those arcs deliver,
- declares the **dimensions** below, proportionately to its tier.

## The Metabolism

Inside a module the two shapes interleave into a standing cycle:

1. **Accumulative arcs deliver operating state** — the live thing the
   module now operates.
2. **Repeatable loops maintain it** — each demand (a request, a record
   needed, a scheduled procedure) instanced as a run of a stable
   definition.
3. **Sensors on the operating state seed the next arc** — declared
   triggers and telemetry over the event stream raise the evidence that
   becomes a new `define-need`.

A module at rest is not idle: the **operating interval** between arcs is
where evidence accrues, and the substrate's standing machinery —
triggers, velocity, orientation — is that interval's instrumentation.
This is why the interval needs no new mechanism: the framework already
lives there.

## The Fractal

The same mechanics operate at every radius, micro to macro. Composition
is three references the corpus already has:

- **`parent`** — a child run points at the run (or plan) that spawned it.
- **`dependencies`** — cross-run prerequisites; a run may not complete
  over unfinished work it depends on (floor-enforced).
- **`informed_by`** — evidence pins; a run's stage outputs pin the
  committed things they rest on.

Three consequences:

- **Downward recursion.** A work package uncovered at the cut may itself
  be a run — the whole flow re-applied inside one stage of a larger flow.
- **The arc.** Chained runs form an accumulative arc: each run's
  `assess-current` pins its predecessor's `review-verify` output. The
  loop is a provenance edge between runs, never a cyclic stage edge.
- **The closure.** At the cut, capacity resolution may be *automate it*:
  a child accumulative arc whose deliverable is a new repeatable
  definition. One shape manufactures the other — the fractal generates
  itself. This closure is the model's strongest universality evidence.

Radius (task, project, programme, portfolio) is **declared context** — a
tag, a body statement — never a mechanic. The floor treats a task-radius
run and a portfolio-radius run identically; only judgement scales.

## Module to Module — the Estate Radius

- **Faces.** Modules rest on each other only through exposed things,
  imported with the reference triple and re-checked (`mdllm
  imports-check`). Exposure is not delivery; a face is only assessable
  against its consumption.
- **Crossing provenance.** A decision in one module pins evidence served
  by another; the estate's audit line is the union of module chains
  crossing at faces.
- **The portfolio loop.** Which needs get arcs *at all* is itself a
  standing repeatable loop at estate radius — a `workflow-definition`
  whose runs read the faces, propose work, and refuse work, on a cadence
  with a heartbeat (a schedule whose absence is invisible is not a
  control). It proposes; it never creates execution state on another
  module's surface.

## The Declared Dimensions

Five declarations make a module's composition auditable. Each resolves
to an existing primitive; none is mandatory (see Posture).

| Dimension | What the module declares | The primitive that holds it |
|---|---|---|
| **Gate authority** | Who may pass each stage gate of its definitions — and which gates are human-only (irreversible edges) | `decided_by` / `verified_by` on gate outputs; seal-style human gates; `consequence-is-recoverable-only-in-retrospect` |
| **Entry classification** | The fixed rule that sets a run's tier once, at entry; the tier decides evidence depth thereafter | A field on the run (e.g. `track:`), set at the first stage, read at every gate |
| **Operating interval** | The sensors over its operating state — triggers, and heartbeats for its standing loops | `triggers:` blocks; the run series as the evidence a schedule fired |
| **Portfolio** | Which standing loop (if any) admits new arcs, at what radius, reading what | A `workflow-definition` + its run series |
| **State-surface map** | Where each class of state lives: canonical definitions, execution state, reasoning/run-state/provenance | The domain always owns reasoning, run-state and provenance; external surfaces are declared, and content from them enters quarantined (`origin: external`) |

**Capacity is deliberately not a dimension.** It is resolved inside each
atom at the cut — sometimes by allocation, sometimes by the automation
closure above — and a standing capacity declaration would restate what
every cut must judge freshly (see the atom, v1.1).

## Posture: Open by Doctrine

Deploy-when-felt, with no minimum bar. A regulated module will declare
all five dimensions because its tier demands it; a personal module may
declare none and still be running the model. The floor never encodes
what a quality system *should* require — that is the module's own
declaration to make and its auditors' to judge.

The spec's own admission rule is the same test: a dimension — or any
future addition to this spec — enters **only on convergence**: felt
independently in more than one live corpus. Something is true here
because it is true in many domains, many states, many places
(`a-true-primitive-is-discovered-not-authored`). Field evidence,
2026-08: three live corpora independently grew a staged lifecycle
definition, a regulated change procedure, and a cadence loop — each then
hitting the same undeclared dimensions (an open gate-authority conflict,
a tier rule, a heartbeat). The convergence named the rule; this spec
records it. It must never grow by design.

## Worked Derivation: the Development Lifecycle

The model was derived through the software-development lens; the mapping
is nearly step-to-step, which is the derivation showing:

| Generic lifecycle | The atom |
|---|---|
| Intake + classification | `define-need` + entry classification |
| Requirements | `assess-current` + `define-prioritise` |
| Release scoping | `set-mvp-target` |
| Architecture, design, test specification | `design-plan` |
| Implementation | `execute` |
| Verification + acceptance | `review-verify` |
| Maintenance and service around the delivered system | The metabolism: repeatable loops over operating state |

A development methodology is the atom specialised with domain gates
added; a change-control procedure is the same specialisation at a
different tier. Neither needs this spec to run — they need it only to
recognise each other.

## The Razor

This spec composes; it must never mechanise. If a draft adds a field, a
type, a status, or a subcommand requirement, it has smuggled mechanism
that belongs in one of the specs it composes — move it there or drop it.
The division of labour is unchanged from `validate.thing.md`: the floor
enforces what the composed primitives already enforce (stage membership,
edges, references, pins); the composition itself is semantic, and
auditing it means reading declarations, not running a tool.

## Relationship to Other Specifications

- **universal-workflow-methodology** (thing) — the atom: one loop, seven
  decisions, two shapes. This spec never restates its stages.
- **workflow-state.md** — definitions and runs; every composition
  statement resolves to them.
- **trigger-specification.md** — the operating interval's sensors.
- **provenance.md** — pins and chains; inter-run and inter-module
  evidence.
- **coordination-claim.md** — contention between concurrent loops.
- **interface.md** — the served faces modules rest on.
- **change-reconciliation.md** — what happens when a definition a module
  reasons from is itself changed; composition multiplies the dependents.
