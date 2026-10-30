---
id: eval-cycle
type: workflow-definition
status: draft
version: 1.0
created: 2026-10-30
session: 2026-10-30
exposed: false
tags: [evals, method, traceability, evidence, one-surface, hypothesis, workflow]
stages:
  - id: set-scene
    to: [baseline, hypothesise]
    actor: agent
  - id: baseline
    to: [hypothesise, set-scene]
    actor: operator
  - id: hypothesise
    to: [run, set-scene]
    actor: agent
  - id: run
    to: [reflect, hypothesise]
    actor: operator
  - id: reflect
    to: [logged]
    actor: agent
  - id: logged
    to: []
linked_things:
  - id: universal-workflow-methodology
    relation: derived-from
    notes: "A specialisation of the seven decisions: set-scene is define-need + assess-current; hypothesise collapses define-prioritise, set-mvp-target and design-plan into one pre-registered prediction; run is execute; reflect is review-verify; logged is its terminal output. Iteration is a new run pinned to the last, as the loop section requires."
  - id: evidence-and-eval-backlog
    relation: implements
    notes: "The protocol the backlog's run evenings now follow; the plan names the order of cycles."
  - id: eval-record-2026
    relation: references
    notes: "Where every cycle's reflection lands as a dated section — the log the loop writes to."
  - id: flagship-models-look-around-the-edges
    relation: references
    notes: "The first hypothesis this definition carries, and the refinement that made the read set a measured surface."
---

# Eval Cycle — the evidence-led traceability loop

**What this is.** The operator's method for proving, with evidence, the
outcomes of a non-deterministic agent: name the surfaces that can move,
freeze them, take a baseline, then change **one** surface at a time —
predicting the effect before the run, measuring it, and logging the
result whether or not the prediction held. The outcome of each cycle
steers the next. In the operator's words (2026-10-30):

> You look at the moving surfaces that can be changed. You set the scene
> in accordance to what can be changed. You take a baseline with your
> test. Then you change one of the moving surfaces — only one — and you
> work from that baseline in the frozen set. You make your hypothesis as
> to how that change will affect the output. You run it through your
> tests, and then you reflect: did that change have the effect I expected?
> If it did, you log it. If it didn't, you log it. Then you move on to the
> next change. The outcome of the test will affect the next change.

Devised as a software architect's way to develop agents deterministically
against their instructions, their model, their knowledge source, their
orchestration environment and their connected technologies — the same
surfaces the framework's eval runner already pins on every result.

**One cycle is one run of this definition.** A cycle changes one surface.
The next cycle is a new run whose `informed_by` pins the last cycle's
reflection, so the chain of changes reads as provenance between runs, not
as an arrow inside one (`universal-workflow.md` → The loop).

## The moving surfaces

What the runner records on every result, and therefore what a cycle may
move — one per cycle, the rest frozen:

| surface | where it is pinned | how it moves |
|---|---|---|
| model tier | `model`, `models_observed` (full ids, never aliases) | `--model` |
| structure | `condition`: framework / bare / bare-coached | `--condition` |
| the seed's contract | the seed `AGENTS.md` and skills, inside `seed_sha256` | a seed variant (e.g. one whose contract pushes the walk) |
| fixture | `fixture_sha256` — a regenerated fixture is a different fixture | the generator |
| framework | `framework_commit`, `framework_version`, the pruned view's hash | the checkout |
| harness | `harness_build` | the installed CLI |
| tools | the fixture's `allowed_tools` | the fixture |
| effort | `reasoning_effort_requested` | the fixture |

Anything not in this table that changes between two cycles is a confound,
and the reflection says so.

## Stages

**set-scene** — *What can move, and what is frozen?*
Name the surfaces this cycle may touch and pin every other one by its
recorded value. For cycle 0 this includes choosing the baseline cell.
Output: the frozen set, as a table in the run's body.

**baseline** — *Where are we now?* (cycle 0 only)
Run the baseline cell to n ≥ 5 clean trials under the frozen set, from an
operator terminal (the runner shells to `claude -p`; a hosted session's
token does not reach it). Voided trials do not count toward n.
Output: the baseline cell's per-session figures in `evals/results/`.

**hypothesise** — *If this one surface moves, what happens, and why?*
Name the one surface and its new value. Write the prediction before the
run: the expected direction and rough size of change in the changed-set
pass rate, and — since 2026-10-30 — in the read set (what the agent
explores). Name the mechanism the prediction rests on. Written in the run's
body and committed *before* the run starts; a prediction written after is
not one.
Output: the pre-registered hypothesis.

**run** — *Run it, one arm at a time.*
n ≥ 5 clean trials of the changed cell, same frozen set, one arm at a time
(three concurrent arms are on the record the night every launch died).
Two launch deaths stop the arm; a stopped arm is not a run and the stage
does not advance.
Output: the cell's results, with their read sets.

**reflect** — *Did the change have the predicted effect?*
Compare against the baseline (or the previous cycle) per session and per
changed-set, and the read set against the predicted exploration. Three
honest answers: held, did not hold, or the run cannot say (n too small,
a confound moved). Say which, and what the next surface to move is.
Output: the reflection, as a dated section in `eval-record-2026`.

**logged** — terminal.
The reflection is committed; the next cycle, if any, is a new run pinned
to this one by `informed_by`. Nothing is concluded from one cycle; the
standing direction (no write-up until much more testing) holds across the
chain.

## What this definition refuses

- Moving two surfaces in one cycle, however tempting the saving.
- A hypothesis written after the run, or amended to fit it.
- Reading a voided trial as a measurement.
- Pooling results across fixture revisions (`--report` already refuses).
