---
id: cue-first-hour-guide-2026-10-17
type: cue
status: answered
version: 1.0
created: 2026-10-17
subject: first-hour-guide
raised_at: cc0f5025c90f4a31a7c5f968c3d4d16ea150031e
raised_by: "floor — mdllm cues --staged --raise"
verdict: not-inflection
verdict_reason: "One bullet naming the typed session start (/orient); both dependants reason from the onramp's sentence-first route, which the bullet serves rather than replaces."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    commit: 69dade015b2d6114c706d8539dfb58434e11e488
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `first-hour-guide` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-17: `first-hour-guide` is a
definition surface (`guide`) and changes in the commit this cue rides in,
on top of `cc0f502`. 2 thing(s) depend on it: `operator-seat-and-harness-native-onramp`, `the-onramp-is-the-operators-own-sentence`. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `operator-seat-and-harness-native-onramp` — linked_things `references` — **consistent**: the onramp is the agent performing sync, refresh, floor and session start on the operator's sentence; `/orient` is a step that agent can now take with the digest whole, inside that route, not a second route beside it
- [x] `the-onramp-is-the-operators-own-sentence` — linked_things `references` — **consistent**: the command is model-invocable, so the operator's own word "orient" still reaches it; seat-language at the door is untouched — the slash form is the agent's pull, named for the developer who reads this guide
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle. The conceptual
residue — a thing that reasons about `first-hour-guide` without naming it — is yours
to read; add a line for it if you find one.

## The Answer
**Not inflection.** The guide gained one bullet under its session-start-hardening note: the startup hook's channel is capped at 10,000 characters, so `/orient` is the typed session start that injects the kernel and digest whole and then walks the judgement half. Neither dependant's reasoning moved. Walked by the framework agent in the commit that built the route (`session-start-hardening` Phase 6).
