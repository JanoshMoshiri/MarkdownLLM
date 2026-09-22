---
id: evidence-and-eval-backlog
type: plan
status: in-progress
version: 2.1
created: 2026-06-27
priority: high
tags: [evals, evidence, validation, isolation, longitudinal, docs]
linked_things:
  - id: felt-deployment-lands-in-undisclosable-work
    relation: references
    notes: "Much of this is disclosable-proxy work — the real adoption lives in confidential domains"
  - id: withholding-is-not-isolation
    relation: implements
  - id: isolation-must-contain-writes-not-just-reads
    relation: implements
    notes: "Its run-workspaces-outside-the-repo-tree requirement now binds the FRAMEWORK arm, not just bare — a hard prerequisite for the next multi-trial run"
  - id: structure-decides-figures-scale-decides-convention
    relation: references
  - id: operator-gated-work-is-scheduled-on-the-operators-calendar
    relation: implements
    notes: "The v2.0 reframe is this insight operationalised: two operator sessions with agent support, agent pre-work split out, felt-when-felt retired for this class."
---

# Evidence & Eval Backlog

The evidence/validation work that turns *use* into *artifact* — the strongest thing
about the framework (independent adoption, a production domain) lives outside the
repo. Migrated from continuity on its retirement
(`dissolve-continuity-into-reconciliation`).

**Reframed 2026-07-02 (sixth review):** every review since June 11 ranked this work
first and none of it moved — not because the loop keeps choosing mechanism over
evidence, but because *the loop can only produce artifacts the agent can produce, and
every artifact here requires the operator*: a disclosure decision, a remembered
session, a multi-session run on the operator's machine. These are **operator sessions
with agent support**, not agent tasks with operator sign-off. The unit of scheduling
is the operator's calendar. "Felt-when-felt" was the wrong cadence for work the loop
cannot feel — retired with this version.

## Operator session 1 — sanitised validation record  (~1 sitting, highest leverage)

The cold-start human eval happened informally (the operator's brother); a clean,
sourced, *disclosable* writeup is the missing artifact every reviewer's conclusion
turns on. `evidence/` scaffold + template already shipped — the shape is a redacted
workflow-definition; **it is dictation, not design**. Operator brings: the disclosure
decision and the memory. Agent brings: the template, the structure, the redaction pass.
Also on this session's agenda (small decisions queued by reviews 5+6): the
root-AGENTS.md kernel question, the razor index, the review-moratorium decision.

## Operator session 2 — longitudinal floor test  (~1 evening; agent pre-builds)

The 2×2 was single-shot; the drift-resistance half of the thesis has never seen a
second session. Build → perturb → resume: three prompts, the sleeping-bag rule
reused as the discriminator, the `mdllm eval` assertion engine already exists.
**Agent pre-work (no gate): DONE 2026-07-06** — `sessions:` support in the runner
(chained fresh agents, one workspace, per-session assertions, timeout aborts the
chain), the `sleeping-bag-longitudinal.yaml` fixture (build / perturb / amend-rule,
expected figures worked from the seed rule), and the run-evening protocol in
`evals/README.md`. The operator's evening is now running
`eval . --fixture evals/sleeping-bag-longitudinal.yaml --run --model <m> --trials 5`
per model and reading per-session pass rates. Do **not** re-run
the 2×2 to "fix" the leak — the leaked trial is itself the finding.

**First run 2026-07-09 (operator's authenticated terminal): haiku arm valid,
opus arm void.** Two things were learned before a single figure could be read.
(1) The run *cannot* be launched from a hosted agent session — nested `claude -p`
401s because the host-refreshed OAuth token doesn't propagate to a child (the
2026-07-08 attempt); it is an operator-terminal task, exactly the v2.0 thesis.
(2) On the operator's terminal it ran, but haiku t5's perturb agent committed the
fact-change to the **shared source seed** in the framework repo (`46493d4`),
silently seeding every opus trial from perturbed inputs — the whole opus arm is
invalid. Seed reverted (`c060f21`); contaminated results quarantined. See new
insight [[isolation-must-contain-writes-not-just-reads]] and the results section
in `evals/README.md`.

**Valid finding (haiku t1–t4 + smoke):** within-session reasoning and controls
never drift; the *cross-session cascade* (perturb's edit → derived figure via the
`assesses` link → amend recompute) is where drift enters — carried in 3/4, dropped
in 1/4. The drift-resistance half of the thesis holds for within-session, and is
real-but-imperfect across sessions at the cascade point.

**The isolation blocker is gone, and had been for a month before anyone told
this plan (corrected 2026-09-22).** `_eval_run_dir` has defaulted run
workspaces to `<os-temp>/mdllm-evals` and *refused* any source-tree
descendant since `2673168` (2026-08-20); `MDLLM_EVAL_RUN_ROOT` pins a sandbox
root. Verified live, not assumed: a dry run of the longitudinal fixture puts
trial 1 at `…/AppData/Local/Temp/mdllm-evals/…`, and the seed reads 2400 m /
R 2.8 — the restored pre-corruption state. So this plan spent roughly a month
in the stall list naming a blocker the floor had already removed, which is its
own finding: a plan that records what blocks it does not learn when the block
is lifted somewhere else.

**What the fix did not reach, and now has a detector (2026-09-22).** Workspace
isolation moved the *copy* out of the repo; it did not withdraw the
`--add-dir <framework>` grant, because that grant *is* the framework
condition — the agent must read the specs. So the canonical seed remains
reachable and, with `Bash(git:*)`, writable, exactly as
[[isolation-must-contain-writes-not-just-reads]] describes. The residue was
never really the placement; it was that **nothing in the run output said so**.
It does now: the runner fingerprints the seed tree before the trials and after
each one (`seed_sha256` / `seed_mutated` on every committed result), and on a
mismatch prints the mutation loudly and **stops the arm** rather than seeding
another trial from moved bytes — the precise way the opus arm was lost. The
digest reads bytes rather than revisions, because the 2026-07 damage was
*committed*, so a HEAD comparison would have moved with it and agreed.

**Still owed — and it is now only the operator's evening:** a valid opus
longitudinal arm from the restored seed, and haiku re-run to n≥5 clean.
Report per-session, not just totals. The one constraint that has not moved is
the credential one: the runner shells out to `claude -p`, and a hosted agent
session's token does not propagate to that child, so this is an
operator-terminal task and no amount of agent pre-work changes that.

## Behind those two

- **Real bare-control isolation — satisfied by the same 2026-08-20 fix.** A
  frontier opus-bare trial had defeated the withhold-by-placement control by
  reading the seed `AGENTS.md` inside the repo
  (`withholding-is-not-isolation`). The bare condition strips
  `AGENTS.md`/`CLAUDE.md`/`_schema.yaml`/`skills` from the workspace copy *and*
  withholds `--add-dir`, and the workspace now sits outside the repo — so there
  is no longer a reachable seed to read past the boundary. Worth one explicit
  bare trial on the run evening to confirm the control holds where it once
  leaked; it is a check, no longer a build.
- **Doc evidence pass (Bucket 3):** `limitations.md`, the read-side of quarantine
  written up (`verified: true` is still a flag any agent can write), the "why not
  CLAUDE.md + a notes folder" answer the corpus could win and never makes, one page
  on concurrency (the jmtm mid-session collision + the trial agent's `index.lock`
  are two live exhibits), and the Obsidian-vault claim execution test
  (`portability-claims-need-execution-tests`). Agent-executable once sessions 1–2
  give it something to cite.
