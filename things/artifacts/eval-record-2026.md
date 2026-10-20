---
id: eval-record-2026
type: artifact
status: evolving
version: 1.0
created: 2026-10-20
origin: stated
exposed: false
tags: [evals, record, results, controls, defects, structure-beats-scale, longitudinal]
linked_things:
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "The plan reads this record for what has been run and what the runner still owes; the record never ranks the work."
  - id: review-critical-comparison-2026-10-17-claude
    relation: references
    notes: "The review's defensibility table names the two measurements this record does not yet contain."
  - id: withholding-is-not-isolation
    relation: references
    notes: "The control-leak finding below is this insight's evidence base."
  - id: first-2x2-measured-convention-following-not-reasoning
    relation: references
    notes: "The honest reading of the first 2×2, recorded here with its table."
---

# Eval record 2026 — every run, what it found, and what the runner still owes

This is the laboratory record the eval programme's README used to carry.
It moved here on 2026-10-20 because a README is the shape of a thing and
this is its history: dated result sections, honest readings, the controls a
cold review added, the defects still owed. Nothing below is a conclusion;
the standing direction since 2026-10-05 is that no write-up follows until
much more testing. Each section is verbatim from the README at commit
6af9b4c, with its date in its heading; new runs append new dated sections.
The design of the experiment it records — the 2×2, the fairness note, the
assertion kinds — stays in [`evals/README.md`](../../evals/README.md).

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

## Controls added after the 2026-10-05 cold review

An independent cold read of the fixtures and runner found five defects that
would have invalidated any framework-vs-bare conclusion. Each is now a
mechanical control; none of this section reports a result.

1. **The answer key is no longer reachable.** The framework arm used to be
   granted the whole checkout with `--add-dir`, and the checkout contains
   `evals/` — every fixture's expected figures and the generators that print
   them. The arm is now granted a **pruned view** (`FRAMEWORK_VIEW_INCLUDE`
   in `evals.py`: kernel, operative specs, `tools/`, the calculation
   reference; never `evals/`, `things/`, `examples/` or `domain/`), built per
   invocation under the run root, fingerprinted, and checked after every
   trial — a mutated view voids the trial and stops the arm, like the seed.
   `MDLLM_EVAL_FRAMEWORK_DIR` names a prepared view instead (refused if it
   contains `evals/`). Transcripts are also scanned for references to fixture
   or generator paths; a hit voids the trial (`voided` in the result).
   Every framework-arm result recorded before this date was produced under
   the open grant and is re-run under the guard before it is cited.
2. **Committed state is the carrier, by construction.** Between sessions the
   runner runs `git reset --hard && git clean -fd` in the workspace, so
   uncommitted edits do not survive. Each session records
   `uncommitted_at_end`.
3. **A hint-matched control arm.** `--condition bare-coached` strips the
   tree like `bare` but prepends the fixture's `coached_preamble` — the
   seed's domain guidance as plain prompt text, with no schema, kernel or
   tool behind it. A framework win over `bare` alone could be the hints; the
   2×3 separates hints from structure.
4. **Delta scoring.** A longitudinal fixture tags each assertion
   `changed: true|false` against the previous session's expected value. A
   do-nothing agent passes every unchanged assertion (≈88% of this fixture),
   so the aggregate pass rate is nearly uninformative; results carry the
   changed-set and unchanged-set counts per session, the failed assertion
   labels, and `--report` prints a per-session table.
5. **Rounding margins.** `polar-station-htc`'s generator tunes the seed so
   every expected net load sits ≥ 0.3 W from a rounding boundary, and the
   code states which steps round. Thirteen figures had sat within 0.3 W, one
   at 0.012 W: a correct method carrying one more decimal failed.

Also: full model ids are passed (`--model claude-haiku-4-5-20251001`), the
ids the CLI reports using are recorded (`models_observed`), the per-session
timeout default is 1800 s, and `--report` groups by fixture content hash so a
regenerated fixture is never pooled with its predecessor's runs.

### The 2026-10-05 runs, committed 2026-10-20 as evidence, not as a result

Fifty-three FAC-longitudinal result files from 2026-10-05 sat untracked for
fifteen days. They are committed now, sorted by what they are:

- **Four clean guarded runs stay in `results/`** (pinned ids, the pruned
  view, after the controls above landed): opus 44/44 once; haiku 36/44 twice
  with the same eight failures, and once 240/251 across six sessions. They
  confirm what the section above already says — the fixture's core
  saturates at opus and leaves a stable gap at haiku — and nothing is
  concluded from four trials.
- **Eleven open-grant runs go to `results/excluded/`**: the morning's five
  opus and five haiku framework trials and one bare trial were produced
  under the whole-checkout grant that defect 1 closed, so by that rule they
  are re-run under the guard before they are cited, never cited as they are.
- **Thirty-eight aborted runs go to `results/excluded/`**, and they are the
  evidence this section was missing. After the controls landed, every
  `bare` and `bare-coached` trial on both models and eighteen of twenty-two
  framework trials exited at launch — `process exited 1`, one turn, six
  seconds, no cost — and the runner scored each as 44 or 266 *failed*
  assertions with `voided` unset. Two defects follow, numbered to continue
  the list above and owed to the next fixture before it runs:
  6. **An aborted trial is void, never failed.** A result with no turns, no
     cost, or `aborted: true` must carry `voided` and be excluded from the
     table mechanically; today a dead process reads as a do-nothing agent.
  7. **The launch failure is undiagnosed.** The same build that produced the
     four clean runs refused the other thirty-eight within the same hour;
     the exit status was recorded and the cause was not. Diagnose from
     `evals/runs/` before any arm is run again.
