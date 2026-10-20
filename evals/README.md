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
domain_dir: client-tracker   # optional — scaffold fixtures: thing/status/field/link/
                             # validates assertions scan this workspace subfolder
allowed_tools: "..."         # optional — override the agent's tool allowlist
assertions:
  - thing_exists: some-thing-id
  - status: { id: some-thing-id, equals: figures-ready }
  - field: { id: some-thing-id, name: net_vat_due, equals: 1234.56 }
  - link: { from: a-return, relation: has-deadline, to: a-deadline }
  - validates_clean: true
  # scaffold-style (workspace-relative; added for the cold-start rehearsal):
  - file_exists: client-tracker/AGENTS.md      # or a list — any match passes
  - file_contains: { path: .gitignore, text: "client-tracker" }
  - git_repo: client-tracker                   # subfolder is its own git repo
  - git_commits: { path: client-tracker, min: 1 }
  - min_things: 5
```

## The two-stage loop

**Stage 1 (implemented):** assertion checking against current state. Use after
running a workflow with the agent: did it leave the domain in the contracted
state? `validates_clean` invokes the complete `mdllm validate` boundary,
including scan/parse findings rather than only validators that received a
corpus. Any failed assertion returns a non-zero command status. Also usable in
CI as a regression net over committed state.

**Stage 2 (implemented):** the full loop. The fixture adds `seed` (a directory
copied into an isolated git workspace under `evals/runs/`, gitignored) and
`prompt` (the scenario instruction). The runner invokes a fresh headless agent
(`claude -p`, requires the CLI on PATH: `npm i -g @anthropic-ai/claude-code`),
then runs the Stage 1 assertions on whatever the agent left behind. A non-zero
process, timeout, unparseable result, agent-reported error, validation Error, or
failed assertion fails the trial and makes the command return non-zero. It is
impossible for a failed evidence leg to produce a successful eval exit status.

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

Run workspaces live outside the source repository by default (`$TMP/mdllm-evals`,
or `MDLLM_EVAL_RUN_ROOT`). This is an isolation boundary, not merely a
gitignored folder: an agent cannot walk upward into the canonical seed and edit
or read the answer key. The bare condition also withholds the framework
`--add-dir`. Timed-out and failed invocations are recorded, never discarded.

Every result uses a collision-resistant run id and records the full framework
commit, framework/tool version, fixture SHA-256, model, requested and observed
effort facts, harness and observed CLI build, process status, complete validation
summary, and assertion result. Raw stdout/stderr stays with the isolated run;
the result JSON is mirrored into `evals/results/` so any committed evidence can
travel with the claim.

**Longitudinal fixtures (Stage 2 only):** replace the top-level `prompt` /
`assertions` pair with a `sessions:` list — each entry `{name, prompt,
assertions}`. The runner seeds the workspace once, then runs each session as a
**fresh** headless agent (`claude -p`, no conversation memory) against the
**same** workspace, checking that session's assertions after it exits. The only
carrier between sessions is committed state — which is exactly the property
under test: drift resistance. A session timeout aborts the chain (downstream
sessions depend on its end state) and fails all remaining assertions. The
result JSON gains a per-session breakdown; `--report` aggregates trial totals
as before. Stage 1 (no `--run`) against an existing domain checks the *final*
session's assertions — the end-state contract.

## The structure-beats-scale experiment

The manifesto claims a smaller model in a well-defined domain outperforms a
larger model without structure. The 2×2 that tests it:

| | framework | bare |
|---|---|---|
| **haiku** | `--model haiku` | `--model haiku --bare` |
| **opus** | `--model opus` | `--model opus --bare` |

Protocol: ≥5 trials per cell per fixture (models are stochastic — single runs
mean nothing); score = assertion pass rate; report cost and wall time alongside
(`eval --report` builds the table from `evals/results/*.json`, the committed
evidence mirror). The first
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

## Where the record lives

This file is the shape of the programme; it does not carry results. The dated
record — every run since 2026-06-11, what each found, the controls the
2026-10-05 cold review added and the defects still owed — is a thing:
[`things/artifacts/eval-record-2026.md`](../things/artifacts/eval-record-2026.md).
Result files are the evidence mirror under `results/`; `results/excluded/`
holds the trials the record excludes and says why in its own README. The
forward work is `things/plans/evidence-and-eval-backlog.md`. The standing
direction (2026-10-05): no write-ups or conclusions until much more testing —
the next fixture must be genuinely hard, its bare arm isolated rather than
merely withheld, and its model ids pinned.

## Conventions

- One fixture per scenario, named `<domain>-<scenario>.yaml`
- Fixtures assert *contracts* (statuses, links, key figures), not exact prose
- A fixture that asserts current production state doubles as a regression net:
  it fails if a future session corrupts what was already correct
