---
id: cue-standing-watch-specification-2026-09-24
type: cue
status: answered
version: 1.0
created: 2026-09-24
subject: standing-watch-specification
raised_at: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
raised_by: "floor — mdllm cues --raise"
verdict: inflection
verdict_reason: "loop-turns-self-heal-2026-09-23 moved one check from the agent to the floor: the watch now reads its own clone's branch against the ref and wakes the side whose turn never left; walked and sealed in 8d3a635."
informed_by:
  - id: loop-turns-self-heal-2026-09-23
    commit: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
tags: [cue, raised-mechanically]
---

# Cue: `standing-watch-specification` was modified — inflection?

## The Change
Raised by the floor on 2026-09-24: `standing-watch-specification` is reasoned-from (definition surface (`specification`)) and
was modified in 1 commit(s) since the baseline 2026-09-13 — latest
2026-09-23 (`8d3a635`) — with no cue covering the change. `mdllm touchpoints
standing-watch-specification` lists what depends on it; `git log -p 8d3a635` shows what moved.
The raise is mechanical (`inflection-candidates-are-computable`); the
verdict never is (`unattended-cue-carrier-2026-09-12`).

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer
**Inflection.** The division of labour changed: confirming that a turn left was the agent's alone, and the field showed it went undone. The floor now reports the clone's own unpublished or diverged turn and rings that role; the merge stays the agent's. Walked in the modifying commit `8d3a635`: the git-workflow kernel's turn-taking sentence, `substrate-native-a2a`'s done-when, and the two rows in this spec's division of labour. The engineering domain's watchers inherit the behaviour through the floor on its next refresh; its own declarations reason from the ref contract, which is unchanged.

*Answered by citation under `framework-agent-closes-settled-cues-2026-09-13`; the operator may overturn it by editing the verdict.*
