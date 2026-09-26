---
id: cue-git-workflow-specification-2026-09-26
type: cue
status: answered
version: 1.0
created: 2026-09-26
subject: git-workflow-specification
raised_at: 214770d5a267aa102c8c2a0eb36fd7a0e571bbea
raised_by: "floor — mdllm cues --raise; answered by the framework domain agent, 2026-09-26, attended session, under framework-agent-closes-settled-cues-2026-09-13 (operator: 'do what the domain agent needs to do')"
verdict: inflection
verdict_reason: "Two rule changes: turn-taking is publication and the watch heals a turn that never left (ce1a1e6, 8d3a635; ruled in the pinned decision), and history is part of the state — a shallow clone is completed at sync (214770d). Walked: standing-watch, orchestration hook 4, validate's pin clause, operator-guide watch/estate-sync lines — sealed by 214770d."
informed_by:
  - id: loop-turns-self-heal-2026-09-23
    commit: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
tags: [cue, raised-mechanically]
---

# Cue: `git-workflow-specification` was modified — inflection?

## The Change
Raised by the floor on 2026-09-26: `git-workflow-specification` is reasoned-from (definition surface (`specification`)) and
was modified in 2 commit(s) since the baseline 2026-09-13 — latest
2026-09-26 (`214770d`) — with no cue covering the change. `mdllm touchpoints
git-workflow-specification` lists what depends on it; `git log -p 214770d` shows what moved.
The raise is mechanical (`inflection-candidates-are-computable`); the
verdict never is (`unattended-cue-carrier-2026-09-12`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
**Inflection — walked and sealed.** Two rule changes: turn-taking is publication and the watch heals a turn that never left (ce1a1e6, 8d3a635; ruled in the pinned decision), and history is part of the state — a shallow clone is completed at sync (214770d). Walked: standing-watch, orchestration hook 4, validate's pin clause, operator-guide watch/estate-sync lines — sealed by 214770d.

*Answered by the framework domain agent in an attended session under
`framework-agent-closes-settled-cues-2026-09-13`. The operator may overturn this
verdict by editing it — the cue stays on the record either way.*
