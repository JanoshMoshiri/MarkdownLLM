---
id: cue-git-workflow-specification-retro-2026-09-13
type: cue
status: answered
version: 1.0
created: 2026-09-13
subject: git-workflow-specification
raised_at: 07648b21c13230bee101186967ca4cbb63a16810
raised_by: "agent — the framework domain agent running framework-retrospective-2026-09, 2026-09-13, under framework-agent-closes-settled-cues-2026-09-13; raised in the retrospective's own commit"
verdict: not-inflection
verdict_reason: "Ten commit prefixes the live stream had been using for weeks added to the Actions table with meanings and examples, plus a sentence saying the set is a vocabulary the hook does not read; the commit-boundary rules, the machine axis and the publication rules are unchanged. Scan 7's finding, applied."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
tags: [cue, retrospective-2026-09, change-reconciliation]
---

# Cue: `git-workflow-specification` was modified — inflection?

## The Change
The retrospective commit: rows for decide, plan, reconcile, fix, build, review, record, harvest, retrospective and release; version 1.8. The kernel block is untouched.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Not an inflection.** The table describes practice and had fallen behind it; the rows restore description. No session will commit differently, and `mdllm worklog` grouped by these prefixes already. The seven inbound edges reason from the state-machine rules, which did not move.

*Answered by the framework domain agent under `framework-agent-closes-settled-cues-2026-09-13`; the walk is
`framework-retrospective-2026-09`. The operator may overturn this verdict by
editing it — the cue stays on the record either way.*
