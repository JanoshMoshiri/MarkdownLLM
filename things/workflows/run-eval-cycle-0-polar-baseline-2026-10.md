---
id: run-eval-cycle-0-polar-baseline-2026-10
type: workflow-run
status: active
version: 1.0
created: 2026-10-30
session: 2026-10-30
definition: eval-cycle
definition_commit: 99327652afc99d85a508e0ad759f3d53a7afd5fc
current_stage: baseline
informed_by:
  - id: eval-record-2026
    commit: 0f403e54abb8cda4f4dc2ddbd36e28f7ee7547c4
  - id: flagship-models-look-around-the-edges
    commit: 0f403e54abb8cda4f4dc2ddbd36e28f7ee7547c4
linked_things:
  - id: evidence-and-eval-backlog
    relation: implements
    notes: "The first cycle of the run evening the plan names; its order (one trial first, polar first, one arm at a time) is this run's protocol."
  - id: eval-record-2026
    relation: references
    notes: "The one earlier polar-station trial (haiku framework, 240/251, fixture bfddcbee) that this baseline's hypothesis rests on, and where this run's reflection will land."
---

# Run: Eval Cycle 0 — the polar-station baseline

## Where this is

At `baseline`. The scene is set below; the baseline cell has not been run.
The stage belongs to the operator: five clean trials from an authenticated
terminal, one arm, polar-station first, one trial before the arm to
confirm the launch is alive.

## The frozen set (set-scene, 2026-10-30)

| surface | frozen at |
|---|---|
| model tier | `claude-haiku-4-5-20251001` |
| structure | `framework` (seed as-is, pruned framework view granted) |
| the seed's contract | `evals/seeds/polar-station-htc/AGENTS.md` as committed — the rulebook contract, whose one exploratory push is "walk every thing that rests on the changed clause" |
| fixture | `evals/polar-station-longitudinal.yaml` at sha256 `abad0ddc…` (the current bytes; the 2026-10-05 trial ran `bfddcbee…`, a revision before delta scoring and the rounding margins — not poolable) |
| framework | the checkout at this run's `informed_by` commit, or later on the same line — recorded by the runner per trial |
| harness | whatever `claude --version` reports on the evening; recorded per trial |
| tools | the fixture's `allowed_tools` (Edit Write Read Glob Grep, git, python) |
| effort | CLI default |

**Baseline cell:** haiku × framework. Chosen because it is the cheapest
cell (≈ $2.30 a trial, ≈ 20 minutes), the one cell with any prior
observation, and the cell every later cycle's single-surface change
departs from: cycle 1 moves *structure* (→ bare), cycle 2 moves *tier*
(→ opus), cycle 3 moves *the seed's contract* (→ a variant that pushes
the walk before the figures), each from this baseline.

## Hypothesis for the baseline (written before the run)

From the one trial at the earlier revision (41/41 · 39/41 · 40/41 · 40/41
· 38/41 · 42/46, $2.29, 1219 s):

- Aggregate pass rate per trial between 90% and 97%; **no trial at 100%**.
- The weakest sessions are `erratum` and `dock` — the two where a change
  cascades furthest (a material's conductivity moves every assembly that
  uses it; a docking turns an external wall into a party wall and splits a
  shared assembly). `build` is the strongest.
- Changed-set pass rate is lower than the aggregate in every session after
  `build`, because the unchanged set is ≈ 88% of the assertions and a
  do-nothing agent passes it.
- Read set: the agent opens every module and heat-load record in `build`,
  and in later sessions opens *fewer* than the set the change touches —
  the under-walk is the predicted mechanism of the misses.
- At least one of five trials leaves a session's figure coherent but wrong
  — carried faithfully from a stale body
  (`committed-state-carries-defects-as-faithfully-as-facts`).

If the aggregate lands above 97% across all five, the fixture is softer
than the direction asked for at this tier and cycle 2 (→ opus) is moved
ahead of cycle 1 to find out whether it saturates.

## Reflection

Not yet — the stage is `baseline`.
