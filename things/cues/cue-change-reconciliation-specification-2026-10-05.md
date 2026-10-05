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

## The Walk — second edit of the day (1.6 → 1.7, the walk-on-detection reading)
Judged material and walked again; one cue per subject per day keeps the record
here. 35 declared edges, 6 literal; cues and indexes excluded.

- [x] `estate-mechanics-guide` (documents) — **revised**: the diagram's prose said the advisory feeds a human verdict that declares an inflection; it now says the advisory and the gate feed the agent's walk and the human rules on the residue.
- [x] `inflection-candidates-are-computable` (complements) — **ruling**: its thesis was "the cue is human"; the operator, asked through the harness's prompt, chose *narrow in place* — title re-cut, a dated note, the verdict sentence re-cut to "the ruling on the residue is human", linked to the ruling (1.1).
- [x] `reconciliation-candidates-are-detectable-from-the-commit-stream` (informs) — **ruling**: same question, same answer — the "walk stays human" sentence re-cut, dated note, link (1.1).
- [x] `circulation-is-not-disposition` (literal) — **revised**: a section name updated to the new title.
- [x] `cue-carrier` (extends) — **revised** earlier this arc (1.5, Phase 7 corrected).
- [x] `unattended-cue-carrier-2026-09-12` (extends) — **consistent**: it ruled the unattended run and anticipated a separate ruling for the attended case; that ruling now exists and links to it.
- [x] `the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`, `the-verdict-is-asked-where-the-change-lands-2026-10-05` (informs) — **consistent**: the ruling and the ruling it superseded.
- [x] `retrospective-specification` (complements) — **consistent**: scan 4 remains the net beneath; "answers each" now means marks the walk, which the spec's own wording already covers.
- [x] `provenance-specification`, `consistency-is-maintained-at-change-not-by-sweeping`, `a-generated-surface-collapses-its-walk`, `cumulative-drift-is-invisible-to-per-change-walks`, `mechanical-assimilation-is-blind-to-prose-dependencies`, `orient-and-reconciliation-are-the-corpus-two-sides`, `structural-pointers-need-reverse-edge-indexing`, `judgement-checks-need-a-suppression-list-which-is-itself-drift`, `change-safety-is-defense-in-depth`, `cross-domain-handoff-is-built-inbound-only`, `mechanism-pairs-come-from-two-reflection-axes`, `premature-publish-manufactures-discipline-eroding-urgency` — **consistent**: they reason from the four beats, the dark region and the indexes, none from who starts the pass.
- [x] `cross-domain-sync-catchup`, `dissolve-continuity-into-reconciliation`, `estate-cadence-cluster`, `substrate-currency-sweep`, `substrate-review-retrospective-reconciliation-2026-08-20`, `mcp-domain-server-design`, `review-external-conflict-lifecycle-2026-09-08` (plans, a design, a review) — **consistent**: records of work under the old reading; history, not restatement.
- [x] `framework-retrospective-2026-09`, `framework-relationships-index`, `framework-provenance-index` (literal) — **consistent**: a retrospective quoting the old rule as history; the indexes regenerated.
- [x] conceptual residue — `AGENTS.md`'s spec catalog line restated the human cue without naming the spec's section: **revised**. `orchestration.md`'s hook-table row: **revised** to the walk. The generated domain hook list and the cue template: **revised**. `feels-automatic-is-persistence-of-the-question`: **consistent** and now extended by `a-preserved-question-is-not-a-done-walk`.

Verdict for this edit: inflection (two rulings, five revisions).
