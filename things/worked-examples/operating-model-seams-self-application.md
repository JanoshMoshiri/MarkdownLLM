---
id: operating-model-seams-self-application
type: example
status: stable
version: 1.0
created: 2026-08-26
pattern_type: universal-workflow-self-application
demonstrates: good-practice
applies_to: [workflow-run, workflow-definition, framework-development]
exposed: false
tags: [universal-workflow, self-application, revision-binding, verification]
informed_by:
  - id: run-operating-model-seams-2026-08
    commit: 45a582b3fc424cb3bf812e235be3cc576615098d
linked_things:
  - id: universal-workflow-methodology
    relation: implements
  - id: operating-model-specification
    relation: implements
  - id: run-operating-model-seams-2026-08
    relation: derived-from
---

# Operating-Model Seams — the Workflow Applied to Itself

## The Pattern

Use the universal workflow as a sequence of evidence gates, not as seven labels
applied after implementation. Keep one small `workflow-run` cursor, put each
stage's durable output in the thing graph, and commit every transition on its
own meaning boundary. The 2026-08 operating-model seams sprint followed that
shape while building the revision binding that makes the shape repeatable.

| Stage | Question answered | Durable evidence |
|---|---|---|
| need | What outcome is required? | The verified convergence review named four missing seams (F17–F20). |
| current-state | What already exists? | Existing references, Git transaction views, workflow state and operating-model doctrine were walked before adding mechanism. |
| approach | What is the smallest useful cut? | The scope decision selected one mandatory guard, two doctrine clarifications and one droppable advisory. |
| plan | How will it be delivered and proved? | The committed design mapped each requirement to files, focused tests, budgets and commit boundaries. |
| implement | Does the result match the plan? | Revision resolution, cached immutable views, the self-authorization guard and fulfilment advisory landed separately. |
| review-verify | Is the outcome evidenced? | Eleven focused tests, the adversarial bypass attempt, the full suite and four latency budgets were recorded on the run. |
| iterate | What must the next cycle inherit? | Reconciliation updated the operative contract, birth templates and worked corpus; this example carries the reusable learning forward. |

## Why It Matters

Self-application is useful only when it creates inspectable evidence. A stage
name in prose does not prove a gate was passed; a committed output, a separate
cursor transition and a verification record do. Pinning the run to the
definition revision it follows closes the remaining repeatability gap, while
keeping performer and gate authority distinct prevents execution capability
from becoming permission by implication.

The output chain is explicit: the initiating review pins the run, and this
example pins the run commit from which it was distilled. No new history array,
workflow artefact or reverse-link mechanism was needed.

## Structure Example

The run uses the minimal reusable form:

```yaml
definition: substrate-floor-development
definition_commit: <full commit carrying that definition>
current_stage: <one declared stage>
informed_by:
  - id: <initiating demand>
    commit: <full commit actually read>
```

The definition declares stage meaning, performer and gate authority. Durable
outputs carry `informed_by` back to the run. Git holds the cursor history.

## Anti-Patterns

- Changing `definition_commit` and `current_stage` together. The run could pick
  a friendlier graph to authorise its own move; the floor rejects this.
- Treating the stage performer as its gate authority. An agent may execute a
  check without being allowed to accept the result or authorise publication.
- Calling a producer-side subscriber list a consumption contract. Admission,
  cadence and non-consumption detection stay consumer-owned.
- Reporting a green structural check as proof of semantic fulfilment. The floor
  can see link presence; the terminal review judges adequacy.
- Adding `stage_history` to the run. Cursor commits already are the history.

## How to Adapt

Specialise the seven questions and outputs for the domain, declare them as a
workflow definition, and create a run only when real work begins. Pin the
definition and initiating evidence from Git, keep migrations separate from
cursor moves, measure the budgets that matter for the changed path, and let the
terminal review seed the next run or improve the repeatable definition.

This example is framework-internal (`exposed: false`). The governing doctrine
reaches domains through framework versioning and domain refresh, not through a
domain-to-domain served face.
