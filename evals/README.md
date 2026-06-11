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

**Stage 2 (next):** the full loop — copy a fixture's `seed/` things into a temp
worktree, run a fresh agent session against it with the scenario prompt
(headless, e.g. `claude -p`), then run Stage 1 assertions on the result. That is
what makes "did this spec change improve agent behaviour?" answerable, and what
enables the small-model-vs-structure experiment from the manifesto.

## Conventions

- One fixture per scenario, named `<domain>-<scenario>.yaml`
- Fixtures assert *contracts* (statuses, links, key figures), not exact prose
- A fixture that asserts current production state doubles as a regression net:
  it fails if a future session corrupts what was already correct
