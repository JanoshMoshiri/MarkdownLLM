---
id: evidence-and-eval-backlog
type: plan
status: in-progress
version: 2.0
created: 2026-06-27
priority: high
tags: [evals, evidence, validation, isolation, longitudinal, docs]
linked_things:
  - id: felt-deployment-lands-in-undisclosable-work
    relation: references
    notes: "Much of this is disclosable-proxy work — the real adoption lives in confidential domains"
  - id: withholding-is-not-isolation
    relation: implements
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

**Attempted 2026-07-08 from a hosted agent session; blocked — and the block is
itself confirming evidence.** All 15 nested `claude -p` agents 401'd before doing
any work (`ANTHROPIC_API_KEY` unset; this session authenticates via a
host-refreshed OAuth token that does **not** propagate to a spawned child
process). Zero cost, zero tokens, nothing measured; the junk result JSONs were
quarantined out of the report. The runner is agent-pre-built, but *executing* it
still requires an authenticated operator terminal — the run cannot be launched
from inside an agent session. That is exactly the v2.0 thesis made concrete: this
is an operator-terminal task, not an agent task. **Run it from a local `claude`
terminal** (file-based credentials on disk), haiku then opus, `--trials 5`.

## Behind those two

- **Real bare-control isolation.** A frontier opus-bare trial defeated the
  withhold-by-placement control by reading the seed `AGENTS.md` inside the repo
  (`withholding-is-not-isolation`). Bare workspaces need real isolation — run outside
  the repo tree / OS sandbox; `--add-dir` withheld is not sufficient. (Operator
  machine; can share session 2's evening.)
- **Doc evidence pass (Bucket 3):** `limitations.md`, the read-side of quarantine
  written up (`verified: true` is still a flag any agent can write), the "why not
  CLAUDE.md + a notes folder" answer the corpus could win and never makes, one page
  on concurrency (the jmtm mid-session collision + the trial agent's `index.lock`
  are two live exhibits), and the Obsidian-vault claim execution test
  (`portability-claims-need-execution-tests`). Agent-executable once sessions 1–2
  give it something to cite.
