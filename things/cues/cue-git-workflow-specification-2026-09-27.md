---
id: cue-git-workflow-specification-2026-09-27
type: cue
status: answered
version: 1.0
created: 2026-09-27
subject: git-workflow-specification
raised_at: 2ed6dfe33fac2348bd6238b4c22afb459f326579
raised_by: "floor — mdllm cues --raise"
verdict: inflection
verdict_reason: "Clone-local Cloud restraints now preserve a host-selected primary HEAD and refuse automatic sends from a secondary branch other than the manifest branch. Walked the shared sync/publication policy, post-commit hook, generated kernel, Cloud adapter/setup and Git fixtures; sealed by 690d75b and 2ed6dfe."
tags: [cue, raised-mechanically]
---

# Cue: `git-workflow-specification` was modified — inflection?

## The Change
Raised by the floor on 2026-09-27: `git-workflow-specification` is reasoned-from (definition surface (`specification`)) and
was modified in 2 commit(s) since the baseline 2026-09-13 — latest
2026-09-27 (`2ed6dfe`) — with no cue covering the change. `mdllm touchpoints
git-workflow-specification` lists what depends on it; `git log -p 2ed6dfe` shows what moved.
The raise is mechanical (`inflection-candidates-are-computable`); the
verdict never is (`unattended-cue-carrier-2026-09-12`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
**Inflection — walked and sealed.** The prior Cloud PR restraint cue already
ruled the move to host-managed primary publication. This follow-through adds
an observe-only inbound path for that primary and a branch guard for declared
automatic publication from a secondary. The shared `sync_repo`,
`publication_policy` and `autopush_repo` paths, Git hook, generated kernel,
Cloud setup and adapter guide were checked together. Real Git fixtures cover
the selected primary, a writable secondary and wrong-branch refusal. Other
clones retain the old behaviour when the local keys are absent. Commits
`690d75b` and `2ed6dfe` seal the walk; they grant no publication authority.
