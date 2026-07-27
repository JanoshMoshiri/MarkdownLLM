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
run's evidence lives in `evals/results/excluded/`, excluded from the report — it
ran against the fixture's pre-fix id template through a broken runner.)

## The cold-start scaffold rehearsal (2026-06-12, cold-start-scaffold)

The agent-only half of the cold-start eval: a fresh headless agent, an
operator-voiced brief, read access to the framework, and eleven mechanical
assertions over birth quality (isolation, commits, versioned AGENTS.md,
schema, skills, hook, validates clean). Run the day `mdllm scaffold` was
built — deliberately, in this order:

| trial | guide state | score | miss | wall | cost |
|---|---|---|---|---|---|
| opus t1 | pre-scaffold | 10/11 | **zero commits in the domain repo** | 1019s | $6.43 |
| haiku t1 | pre-scaffold | 10/11 | **no outer .gitignore isolation** | 325s | $0.52 |
| haiku t2 | guide routes to `mdllm scaffold` | **11/11** | — (used the tool; its first commit is the scaffold commit) | 261s | $0.45 |

**Honest reading (n=3, so a pattern, not a proof):** both pre-scaffold trials
built structurally valid domains — schema declared, four skills, 9 things,
validates clean, hook installed — and each dropped a *different mechanical*
step of the `pre-domain-scaffold:isolate` sequence. The semantic half was
reliably good; the mechanical half decayed exactly the way
`hook-compliance-correlates-with-scope-not-awareness` predicts (the opus
trial ran 96 turns and never committed). Mechanising the mechanical half
(`mdllm scaffold`, same day) took the next trial to 11/11 at a fraction of
the cost. The opus trial also left a stale `index.lock` on the *framework*
repo despite a read-only instruction — agent git activity outside its
workspace is real, which is why scaffold owns the outer-repo commit.
Three additional trials died in 2s with an unparseable 1-turn result before
the runner captured agent output (evidence in `evals/results/excluded/`,
excluded from the report; `agent-stdout.json`/`agent-stderr.txt` are persisted
per-trial since the fix, so future failures are diagnosable). Scored evidence
is mirrored to `evals/results/` — committed with the repo — because the run
workspaces themselves are gitignored nested repos; the claim and the data
travel together.

The human half of the cold-start eval still stands as designed — a non-author
operator, observed not helped. This rehearsal cleared the path for it: the
template bugs it would have hit (an unparseable `_schema.yaml.template`,
undeclared relations) were found and fixed building the fixture.

## The reasoning discriminator (sleeping-bag-fac, 2026-06-16/17)

`first-2x2-measured-convention-following-not-reasoning` called for a fixture
whose condition-neutral core *discriminates*. `sleeping-bag-fac` is it: a
fictional outfitter's Field-Adjusted Comfort rule (the Tarn & Fell coefficients —
`+10` female, `−1` per complete 800 m above 1200 m, `+4` below a
surface-dependent pad-R threshold, ceiling round) lives **only** in the seed
`AGENTS.md`, so the five `fac_celsius` figures (4, −1, −5, 2, −5) cannot be
reconstructed from training or the web. The five trips isolate the traps,
including the hammock inversion (off-ground ≠ no penalty) and the snow-threshold.

### Result (clean trials; one leaked trial excluded)

| model | condition | figures correct | fully passing | assertion rate |
|---|---|---|---|---|
| haiku | framework | 5/5 every trial | 0/6 | 96/126 (76%) |
| haiku | bare | 0/5 (nothing / wrong) | 0/6 | 26/126 (21%) |
| opus | framework | 5/5 every trial | 5/5 | 105/105 (100%) |
| opus | bare | 0/5 (all produced nothing) | 0/4 | 4/84 (5%) |

**Honest reading.** Unlike the VAT run, the reasoning core *did* discriminate:
both framework models got every figure right (every trap), every trial; both
bare conditions got zero. **Condition decided the reasoning; model tier did
not.** Scale showed up only in the convention layer — opus wrote canonical
`linked_things` (21/21), haiku invented a `relations:` key the floor silently
ignores (16/21; see `mis-keyed-links-pass-the-floor-silently`). That is exactly
where manifesto v2.4 places model-tier superiority: a secondary corollary, not
the spine. The framework cells were perfectly deterministic; the bare cells were
erratic. See `structure-decides-figures-scale-decides-convention`.

### The control leak (the more valuable finding)

One uninterrupted **opus-bare** trial (`20260617-002833`) scored 16/21 with every
figure correct — not by reasoning the fictional rule into existence, but by
reading the answer key. The bare condition removes `AGENTS.md` from the
*workspace*, but the workspace lives inside the repo, where the original seed
still sits; the agent located `evals/seeds/sleeping-bag-fac/AGENTS.md` and applied
it, **disclosing the breach in its own transcript**. *Withholding is not
isolation.* The trial is excluded under `results/excluded/`; the bare control
needs real filesystem isolation (workspaces outside the repo tree, or a sandbox)
before the next run — `--add-dir` withheld is necessary but not sufficient. This
is a property of capability that will intensify, not a defect; see
`withholding-is-not-isolation`.

## The longitudinal floor test (sleeping-bag-longitudinal, first run 2026-07-09)

Every eval above is single-shot; the drift-resistance half of the thesis —
committed structure keeps *later, memoryless* sessions coherent — had never
been tested. `sleeping-bag-longitudinal` is the fixture (evidence-and-eval-backlog,
operator session 2; the fixture + runner protocol are the committed agent
pre-work, the trial run is the operator's evening):

1. **build** — the sleeping-bag-fac scenario as-is: five FAC figures from the
   fictional rule (21 assertions + commit growth).
2. **perturb** — operator-voiced fact change: the Aonach Ridge party moves to
   3300 m and upgrades to an R 4.2 pad. New figure −1.0 discriminates on *both*
   edits landing (elevation alone → 3, pad alone → 0); nothing in the prompt
   names the assessment — the agent must find it via the `assesses` link. The
   four untouched figures are re-asserted: the drift check.
3. **amend-rule** — the inflection walk: the elevation adjustment tightens to
   −1°C per complete 500 m. Both high camps must move (aonach −3.0; summit-bivvy
   ceil(−6.5+10−3) = ceil(0.5) = **1.0** — the half-degree ceiling trap survives
   the amendment) and the three low camps must *not* (900/1000/600 m — a corpus
   walk that over-touches fails them).

Session 3's aonach figure presumes session 2's committed state (3300 m) — the
chained dependency is the design, not a defect: session N inherits session
N−1's reality, which is what "longitudinal" means.

Protocol for the run evening: ≥5 trials framework condition
(`--fixture evals/sleeping-bag-longitudinal.yaml --run --model haiku --trials 5`,
then opus), report per-session pass rates, not just totals — *where in the
chain* drift enters is the finding. **Run from a terminal where `claude` has its
own on-disk credentials** — the runner shells out to `claude -p`, and a hosted
agent session's host-refreshed OAuth token does not propagate to that child (it
401s; observed 2026-07-08). This is an operator-terminal task, not an agent task. A bare longitudinal run is near-meaningless
as designed (the bare preamble deliberately omits the FAC method, and session 3
amends a file the bare condition deletes) — do not read a bare cell as a
control without redesigning it.

### First multi-trial run (2026-07-09) — one valid arm, one contaminated

Ran haiku ×5 then opus ×5, framework condition, from the operator's authenticated
terminal. **The opus arm is void and the seed was corrupted mid-run** — read
`isolation-must-contain-writes-not-just-reads` before trusting anything here.

**What happened:** haiku t5's *perturb* agent wrote the fact-change to the
**shared source seed** (`evals/seeds/sleeping-bag-fac/…/trip-aonach-ridge.md`)
and committed it to the framework repo (`46493d4`) instead of editing its
workspace. Every opus trial was seeded *after* that commit, so all five started
from the already-perturbed 3300 m/R 4.2 inputs: opus's build-Aonach of −1 was
*correct for the corrupted seed*, scored as a miss against the 2400 m-era
expectation of 4, and its perturb was a no-op. The seed is reverted (`c060f21`);
the five opus results plus haiku t5 are quarantined under `results/excluded/`.

**Valid data — haiku, four trials (t1–t4) seeded before the corruption, plus the
2026-07-06 smoke.** Per-session, the story is clean:

| trial | build | perturb | amend | chain figure (aonach) |
|---|---|---|---|---|
| haiku t1 | 17/22 | 10/11 | 9/11 | −3 ✓ full cascade |
| haiku t2 | 17/22 | 9/11 | 9/11 | −3 ✓ full cascade |
| haiku t3 | 17/22 | 10/11 | 9/11 | −3 ✓ full cascade |
| haiku t4 | 17/22 | 9/11 | 8/11 | **3 ✗ cascade dropped** |

**Honest reading.** Two layers separate cleanly:

- **Within-session reasoning and the controls never drifted.** All four valid
  trials got the summit-bivvy ceiling trap (ceil(0.5)=1) and all three low-camp
  controls right, in every session — the memoryless later sessions stayed
  coherent off committed state alone. Drift resistance, as far as the valid arm
  goes, holds.
- **The cross-session cascade is where drift lives, and it is not free.** The
  Aonach figure is the only one that requires carrying an edit *across* sessions
  (perturb changes the trip → the derived assessment must follow via the
  `assesses` link → amend recomputes under the new rule). Haiku carried it in
  3/4; t4 dropped it — perturb updated the *trip* (3300/4.2) but never cascaded
  to the assessment, so amend recomputed off the stale build-era body (its
  working literally reads "2400 m … pad R 2.8 → +4") and landed 3. A
  coherent-but-wrong figure, faithfully propagated
  ([[committed-state-carries-defects-as-faithfully-as-facts]]).
- **The link convention is the standing haiku miss** (the constant 5/22 build
  gap): every trial mis-keys `assesses`/`references` as top-level frontmatter
  instead of `linked_things`, so all eight link assertions fail while the
  semantic link is present (`mis-keyed-links-pass-the-floor-silently`).

**Still owed:** a valid opus arm, re-run from the restored seed under real
workspace isolation (outside the repo tree), and haiku re-run to n≥5 clean if a
trial is lost to the same isolation fix. Report per-session, not just totals.

## Conventions

- One fixture per scenario, named `<domain>-<scenario>.yaml`
- Fixtures assert *contracts* (statuses, links, key figures), not exact prose
- A fixture that asserts current production state doubles as a regression net:
  it fails if a future session corrupts what was already correct
