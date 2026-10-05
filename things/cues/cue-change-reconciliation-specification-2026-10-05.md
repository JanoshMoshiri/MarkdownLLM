---
id: cue-change-reconciliation-specification-2026-10-05
type: cue
status: answered
version: 1.0
created: 2026-10-05
subject: change-reconciliation-specification
raised_at: d492283f84b8a5251c9f7b133e3179b6ef7af572
raised_by: "floor — mdllm cues --staged --raise"
verdict: inflection
verdict_reason: "The Ask changes who is asked and when: the cue verdict is asked where the change lands, through the harness's own prompt, and the agent's commit waits for the cue; coverage gains one-ask-per-subject-per-day."
informed_by:
  - id: the-verdict-is-asked-where-the-change-lands-2026-10-05
    commit: 3c59f9cf8b77c681c159fd9756b4e6686f4cb518
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `change-reconciliation-specification` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-05: `change-reconciliation-specification` is a
definition surface (`specification`) and changes in the commit this cue rides in,
on top of `d492283`. 27 thing(s) depend on it: `a-generated-surface-collapses-its-walk`, `change-safety-is-defense-in-depth`, `consistency-is-maintained-at-change-not-by-sweeping`, `cross-domain-handoff-is-built-inbound-only`, +23 more. `mdllm touchpoints change-reconciliation-specification` lists what
depends on it; `git show` on the carrying commit shows what moved. The raise
is mechanical; the verdict was asked where the change landed
(`the-verdict-is-asked-where-the-change-lands-2026-10-05`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
**Inflection.** *The Ask — Where The Change Lands* changes the spec's own
rule for where the cue question is put and who answers it at the commit
boundary, and the coverage rule gains the same-day clause. Walked in the
same arc: `orchestration.md` 1.25 (the `pre-commit:gate` row in the hook
table), the entry file's `post-write:commit` hook and the generated
domain hook list (`domain_kernel.py`), the dispatch prompt's step 6, the
operator guide's `cues` line, the kernel regenerated. The 23 further
dependants are insights and decisions that reference the spec's existing
doctrine (the driver names the inflection; the floor never answers;
consistency at change, not by sweeping), none of which The Ask alters —
it moves the ask, not the verdict. Sealed by the commit that carries
this cue.

*Answered by citation under `framework-agent-closes-settled-cues-2026-09-13`: the operator's ruling of 2026-10-05 covers this change. The operator was not at the keyboard when the gate asked — the session that built the gate answered under delegated authority, and says so; overturn it by editing the verdict.*
