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
```

## The structure-beats-scale experiment

The manifesto claims a smaller model in a well-defined domain outperforms a
larger model without structure. The 2×2 that tests it:

| | framework | bare |
|---|---|---|
| **haiku** | `--model haiku` | `--model haiku --bare` |
| **opus** | `--model opus` | `--model opus --bare` |

Protocol: ≥5 trials per cell per fixture (models are stochastic — single runs
mean nothing); score = assertion pass rate; report cost and wall time alongside.
The first fixture (`vat-quarter-basic`) embeds a discriminator: blocked
client-entertainment VAT that must *not* be reclaimed — summing naively gives
430.00 instead of 380.00. Run directories are kept as evidence; prune manually.

## Conventions

- One fixture per scenario, named `<domain>-<scenario>.yaml`
- Fixtures assert *contracts* (statuses, links, key figures), not exact prose
- A fixture that asserts current production state doubles as a regression net:
  it fails if a future session corrupts what was already correct
