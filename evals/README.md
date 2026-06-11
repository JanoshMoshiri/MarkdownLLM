# Behavioral Evals

Golden-scenario fixtures that make spec quality measurable (transformation plan
Phase 6). A fixture declares the *expected end state* of a domain after a
workflow runs; `mdllm eval` checks the assertions deterministically.

```
python tools/mdllm.py eval <domain-path> --fixture evals/<fixture>.yaml
```

## Assertion kinds

```yaml
name: short fixture name
description: what scenario this verifies
assertions:
  - thing_exists: some-thing-id
  - status: { id: some-thing-id, equals: figures-ready }
  - field: { id: some-thing-id, name: net_vat_due, equals: 1234.56 }
  - link: { from: a-return, relation: has-deadline, to: a-deadline }
  - validates_clean: true
```

## The two-stage loop

**Stage 1 (implemented):** assertion checking against current state. Use after
running a workflow with the agent: did it leave the domain in the contracted
state? Also usable in CI as a regression net over committed state.

**Stage 2 (implemented):** the full loop. The fixture adds `seed` (a directory
copied into an isolated git workspace under `evals/runs/`, gitignored) and
`prompt` (the scenario instruction). The runner invokes a fresh headless agent
(`claude -p`, requires the CLI on PATH: `npm i -g @anthropic-ai/claude-code`),
then runs the Stage 1 assertions on whatever the agent left behind, recording
score, wall time, cost, and turns per trial.

```bash
# the framework condition
python tools/mdllm.py eval . --fixture evals/vat-quarter-basic.yaml --run --model haiku --trials 5
# the no-framework condition: same data, AGENTS.md/skills/schema stripped
python tools/mdllm.py eval . --fixture evals/vat-quarter-basic.yaml --run --model haiku --trials 5 --bare
# inspect what a run would do without invoking an agent
python tools/mdllm.py eval . --fixture evals/vat-quarter-basic.yaml --run --dry-run
# aggregate all recorded runs into the per-cell summary table
python tools/mdllm.py eval . --report
```

The bare condition is a real control: the framework checkout is not granted to
the agent (`--add-dir` is framework-condition only), so a bare agent cannot
discover the specs it is being measured without. Timed-out trials are recorded
as 0/N, not discarded.

## The structure-beats-scale experiment

The manifesto claims a smaller model in a well-defined domain outperforms a
larger model without structure. The 2×2 that tests it:

| | framework | bare |
|---|---|---|
| **haiku** | `--model haiku` | `--model haiku --bare` |
| **opus** | `--model opus` | `--model opus --bare` |

Protocol: ≥5 trials per cell per fixture (models are stochastic — single runs
mean nothing); score = assertion pass rate; report cost and wall time alongside
(`eval --report` builds the table from `evals/runs/*/result.json`). The first
fixture (`vat-quarter-basic`) embeds a discriminator: blocked
client-entertainment VAT that must *not* be reclaimed — summing naively gives
430.00 instead of 380.00. Run directories are kept as evidence; prune manually.

**Fairness note for interpreting the 2×2:** some assertions encode contracts
the bare prompt does not state — e.g. the `has-deadline` link in
`vat-quarter-basic` is named in the seed's AGENTS.md workflow but not in the
`bare_preamble`. That asymmetry is the point (spontaneous structure is part of
what the framework buys), but it caps the bare cells below 7/7 by construction.
Report per-assertion results, not just totals, so the comparison stays honest:
the figures assertions (output/input/net VAT) are condition-neutral; the
link/status assertions measure structure-following.

### First results (2026-06-11, vat-quarter-basic, 5 trials/cell)

| model | condition | fully passing | assertion pass rate | mean wall s | mean cost $ |
|---|---|---|---|---|---|
| haiku | bare | 0/5 | 30/35 (86%) | 64 | 0.070 |
| haiku | framework | 3/5 | 33/35 (94%) | 77 | 0.096 |
| opus | bare | 1/5 | 31/35 (89%) | 115 | 0.417 |
| opus | framework | 5/5 | 35/35 (100%) | 197 | 0.858 |

**Honest reading:** the fixture's reasoning core saturated — all 20 trials in
all cells got the figures right, including the blocked-VAT trap. Every point
of variance was the `has-deadline` link assertion (the asymmetric one above).
So this run shows structure buying determinism (opus+framework is the only
5/5 cell) and the diagonal going the manifesto's way at ~23% of the cost
(haiku+framework 94% / $0.096 vs opus+bare 89% / $0.417), but it does **not**
yet test the claim's reasoning component. A harder fixture, where the
condition-neutral figures actually discriminate, is needed before the claim
can cite this experiment. See insight
`first-2x2-measured-convention-following-not-reasoning`. (The pre-fix smoke
run lives in `evals/runs/_excluded-pre-fix/`, excluded from the report — it
ran against the fixture's pre-fix id template through a broken runner.)

## Conventions

- One fixture per scenario, named `<domain>-<scenario>.yaml`
- Fixtures assert *contracts* (statuses, links, key figures), not exact prose
- A fixture that asserts current production state doubles as a regression net:
  it fails if a future session corrupts what was already correct
