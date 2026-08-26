---
id: review-independent-operating-model-2026-08-26-codex
type: artifact
status: evolving
version: 1.0
created: 2026-08-26
origin: external
verified: false
tags: [review, independent, operating-model, workflow-state, convergence]
linked_things:
  - id: operating-model-specification
    relation: validates
    notes: "The review's subject: does the composition doctrine converge with the operator's operating-model vision, and where are the seams?"
  - id: workflow-state-specification
    relation: validates
    notes: "Three of the four gaps land in this primitive's seams: activation/fulfilment correlation, definition revision binding, executor vs authority."
---

# Independent Review — Operating-Model Convergence (Codex, 2026-08-26)

**Reviewer:** independent Codex agent, separate environment, read-only
brief. **Framework snapshot:** `0bfa375f98737a5d0ae426c8de638d7d55f88b5e`
(v3.35.0). The review also read one live portfolio domain of the private
estate; **this framework-filed copy is redacted at the disclosure
boundary** — the private domain's name, paths, HEAD, and thing titles are
substituted with "[private portfolio domain]". The unredacted original is
the operator's to file in that domain's own repo. No framework finding is
altered by the redaction.

## Executive conclusion (reviewer's)

The vision has largely converged already. `operating-model.md` is the
missing composition doctrine: modules, interleaved accumulative arcs and
repeatable loops, sensor-driven metabolism, consumer-pulled faces, an
estate-radius portfolio loop. The [private portfolio domain]'s company
model is a concrete specialisation of that doctrine, not a competing
architecture. The remaining work is not another top-level model — it sits
at four seams in existing primitives.

**Semantic qualification carried whole:** "addressed output" is fully
expressed only if *addressed* means the consumer elects and configures
the source it consumes, or the producer states intended relevance. It is
deliberately not producer-targeted delivery — a producer-side recipient
list, push route, or remotely created execution state would conflict with
the producer-blindness invariant (`provenance.md` → The Membrane's
Direction Is a Ruling). The reviewer judges that constraint sound:
admission belongs to the receiving module, which alone knows its
capacity, priorities, controls and state.

## The four gaps

### Gap 1 — Run activation and outcome correlation

`operating-model.md` says each demand is instanced as a run, but
`workflow-run` does not normatively identify: the demand/input that
caused the instance to exist; the durable outputs produced by the run;
the fulfilment relation between initiating demand and terminal output.
`universal-workflow.md` names one output per stage as the exit gate;
`workflow-state.md` leaves stage outputs in definition prose;
`provenance.md` connects outputs to *decisions*, and routine mechanical
work needs no decision record — so the end-to-end causal chain is not
guaranteed for every run. **Smallest repair:** define a run's initiating
and produced evidence semantics on existing references
(`workflow-state.md` / `provenance.md`); no new artefact type unless live
use proves references cannot carry it.

### Gap 2 — A live run is not bound to a committed definition revision

`workflow-run.definition` points to a mutable thing id, not the committed
revision whose graph and stage meanings govern the run. The floor already
compares cursor moves against the prior committed definition and requires
definition migration and cursor advance to be separate commits, but no
policy settles an *active* run when its definition changes: stay pinned,
migrate, restart, or abandon. Repeatability and auditability require
knowing which process contract was actually executed — a mutable pointer
proves identity, not procedure version. **Smallest repair:** a
revision-binding/migration rule in `workflow-state.md`, reusing git
commits as the citation unit. Mechanism-level, so it belongs in the
primitive spec, not `operating-model.md`.

### Gap 3 — Executor modality is not separated from gate authority

The specs represent decision/verification attribution (`decided_by`,
`verified_by`), advisory possession (`held_by`), orchestration anchors,
and external schedulers — but no clear generic statement of **who or what
performs a stage**: human, agent, deterministic automation, or hybrid.
Execution responsibility and authorisation are different facts: a hybrid
stage may be machine-executed but human-authorised; an agent may prepare
a decision but be forbidden to accept it. **Smallest repair:** doctrine
first — every specialisation declares execution responsibility separately
from transition/acceptance authority, proportionately. Machine-readable
modality fields only after at least two live modules need automation to
consume them.

### Gap 4 — The consumer-owned module contract is implicit

The porch specifies transport and trust, not the operational contract:
which face and thing class the consumer accepts; which workflow
definition that input starts; what output/evidence class constitutes
fulfilment; what cadence makes non-consumption or non-completion visible;
what happens on decline. Parts exist locally in the [private portfolio
domain]'s kernel and consumption rulings. **Constraint on any repair:**
the contract must be consumer-owned and may reference a producer's face;
never a producer subscriber list, push route, or reverse dependency
registry. A minimal declaration can be composed from existing
address-book entries, trigger declarations, workflow definitions and body
prose before any new primitive is justified.

## Apparent gaps already owned elsewhere (reviewer's table, kept whole)

| Apparent gap | Existing owner |
|---|---|
| Universal process model | `universal-workflow.md` — the seven decisions, two shapes |
| Operating-model runtime/cursor | Rejected: the operating model is read, not run; `workflow-run` is the executable instance |
| Async messaging between modules | `interface.md` + `provenance.md`: face, consumer pull, reference triple, freshness states |
| Scheduler inside the framework | `trigger-specification.md`: triggers are attention signals; invocation is external |
| Execution engine in orchestration | `orchestration.md` attaches reasoning to events; harnesses execute |
| Producer push / acknowledgement | Rejected by producer blindness; consumption lives consumer-side |
| Cross-domain cascade on changed input | `imports-check` signals; `change-reconciliation.md` walks locally |
| Same-run locking | `coordination-claim.md` advisory claim; runtime locking deliberately outside |
| Stage history / blocked run status | Both explicitly rejected in `workflow-state.md` |
| Canonical/execution/reasoning surface split | `operating-model.md` state-surface map |
| Portfolio admission | The estate-radius repeatable portfolio loop |
| Per-stage reasoning checklists | Skills/prompts/orchestration, proportionately |

## Redundant concepts to avoid adding (reviewer's list, condensed)

No `module` thing type or module cursor; no domain=module identity
invariant; no `arc`/`loop` types (shapes formed by run relationships); no
porch envelope, event bus, subscriber registry, or producer push; no
global estate manifest or shared cross-domain work id; no
`stage_history`, resume field, or `blocked` run status; no standing
capacity dimension; no human/automated/hybrid workflow *types* (modality
is orthogonal to workflow meaning); no universal per-stage skills or
approval-artefact requirements (specialisation, proportionate); no second
portfolio dispatch mechanism.

## What sits outside the substrate (reviewer's placement, kept)

The substrate is a durable reasoning and evidence system, not the runtime
executor. Triggers detect; orchestration attaches reasoning; schedulers
and workers invoke from outside; chat/CLI/IDE/voice are input routes;
task systems hold execution state where declared; controlled-document
stores hold canonical records where declared; domains hold reasoning,
run-state, decisions, provenance. A future automated worker that watches
inputs, instantiates runs, invokes actors and commits transitions must
remain a replaceable execution layer writing evidence back into the
stable substrate.
