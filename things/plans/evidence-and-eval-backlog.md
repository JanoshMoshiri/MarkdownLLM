---
id: evidence-and-eval-backlog
type: plan
status: not-started
version: 1.0
created: 2026-06-27
priority: medium
tags: [evals, evidence, validation, isolation, longitudinal, docs]
linked_things:
  - id: felt-deployment-lands-in-undisclosable-work
    relation: references
    notes: "Much of this is disclosable-proxy work — the real adoption lives in confidential domains"
  - id: withholding-is-not-isolation
    relation: implements
  - id: structure-decides-figures-scale-decides-convention
    relation: references
---

# Evidence & Eval Backlog

The evidence/validation work that turns *use* into *artifact* — the strongest thing
about the framework (independent adoption, a production domain) lives outside the
repo. Migrated from continuity on its retirement
(`dissolve-continuity-into-reconciliation`).

- **Sanitised narrative validation record.** The cold-start human eval happened
  informally (the operator's brother); a clean, sourced, *disclosable* writeup is the
  disclosable-proxy backlog — `evidence/` scaffold + template already shipped. Worth
  more than the next three specs (every reviewer's conclusion turns on it).
- **Real bare-control isolation.** A frontier opus-bare trial defeated the
  withhold-by-placement control by reading the seed `AGENTS.md` inside the repo
  (`withholding-is-not-isolation`). Bare workspaces need real isolation — run outside
  the repo tree / OS sandbox; `--add-dir` withheld is not sufficient.
- **Longitudinal floor test.** The 2×2 was single-shot; the drift-resistance half of
  the thesis still needs a multi-session fixture (the sleeping-bag rule is reusable
  as a component). Do **not** re-run the 2×2 to "fix" the leak — the leaked trial is
  itself the finding.
- **Doc evidence pass (Bucket 3):** `limitations.md`, the read-side of quarantine
  written up, one page on concurrency (the jmtm mid-session collision + the trial
  agent's `index.lock` are two live exhibits).

Felt-when-felt; the narrative validation record is the highest-leverage item.
