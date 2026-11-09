---
id: run-eval-cycle-0-polar-baseline-2026-10
type: workflow-run
status: active
version: 1.1
created: 2026-10-30
session: 2026-11-09
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
  - id: the-eval-question-is-which-surfaces-carry-the-weight-2026-11-08
    relation: references
    notes: "The ruling that re-planned cycles 1–3 on 2026-11-09: the baseline cell stands; the cycles after it move surfaces of the structure, not the model tier or structure-vs-bare."
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
departs from.

**The cycles after it — re-planned 2026-11-09.** As written on 2026-10-30,
cycle 1 moved *structure* (→ bare), cycle 2 moved *tier* (→ opus), cycle 3
moved *the seed's contract*. The ruling of 2026-11-08
(`the-eval-question-is-which-surfaces-carry-the-weight-2026-11-08`)
withdrew the first two: structure-against-bare and tier were arms of the
model-tier question, which this programme no longer tests. From this
baseline the cycles now move one surface of the **work-continuity layer**
each, every arm keeping the model, the fixture, the facts and the knowledge
layer the baseline had (`eval-cycle` → The moving surfaces):

- **cycle 1 — the digest.** Same seed, same files; the session start emits
  the computed `mdllm session-start` digest in one arm and the same files
  injected verbatim, nothing computed, in the other. Pre-registered in the
  reread review §6: this surface carries more weight than the schema
  surface — re-establishment falls and the open loop is acted on unprompted
  where the digest is present. Pre-work: a runner switch for the digest.
- **cycle 2 — status and stage cursors.** A seed variant whose records
  carry no `status` and whose runs carry no `current_stage` — the facts
  identical, the "what is in flight" property removed. Pre-work: the
  stripped seed variant.
- **cycle 3 — the seed's contract** (unchanged from 2026-10-30): a variant
  whose contract pushes the walk before the figures, read against the
  read set as `flagship-models-look-around-the-edges` 1.1 predicts.

The order is the review's prediction, not a fixed rule: if cycle 1 shows no
movement, cycle 2 runs anyway, and the reflection says the digest story was
wrong. Each cycle is a new run pinned to this one by `informed_by`.

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
than the direction asked for at this tier. Under the 2026-11-09 re-plan
that is no longer a reason to move the tier; it is a reason to harden the
fixture before cycle 1, because an ablation needs headroom below the
ceiling to show a surface's removal costing anything.

## Reflection

Not yet — the stage is `baseline`.
