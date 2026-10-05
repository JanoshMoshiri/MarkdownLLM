---
id: cue-operator-guide-2026-10-05
type: cue
status: answered
version: 1.0
created: 2026-10-05
subject: operator-guide
raised_at: d492283f84b8a5251c9f7b133e3179b6ef7af572
raised_by: "floor — mdllm cues --staged --raise"
verdict: not-inflection
verdict_reason: "The generated toolbox picked up --staged and the authored cues line gained a sentence; the guide's shape and the operator's job are unchanged."
informed_by:
  - id: the-verdict-is-asked-where-the-change-lands-2026-10-05
    commit: 3c59f9cf8b77c681c159fd9756b4e6686f4cb518
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `operator-guide` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-05: `operator-guide` is a
definition surface (`guide`) and changes in the commit this cue rides in,
on top of `d492283`. 2 thing(s) depend on it: `first-hour-guide`, `framework-map`. `mdllm touchpoints operator-guide` lists what
depends on it; `git show` on the carrying commit shows what moved. The raise
is mechanical; the verdict was asked where the change landed
(`the-verdict-is-asked-where-the-change-lands-2026-10-05`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
**Not an inflection.** The toolbox block regenerated (`cues` gains
`--staged`) and the authored when-line gained one sentence saying the gate
asks through the harness's own prompt. Nothing the two dependants reason
from moved.

*Answered by citation under `framework-agent-closes-settled-cues-2026-09-13`: the operator's ruling of 2026-10-05 covers this change. The operator was not at the keyboard when the gate asked — the session that built the gate answered under delegated authority, and says so; overturn it by editing the verdict.*
