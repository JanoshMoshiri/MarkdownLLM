---
id: cue-first-hour-guide-2026-09-15
type: cue
status: answered
version: 1.0
created: 2026-09-15
subject: first-hour-guide
raised_at: 8d51b6f7464079217cc31b78087f299272d37e32
raised_by: "agent — the framework domain agent, 2026-09-15, on the build commit's candidates advisory"
verdict: not-inflection
verdict_reason: "One sentence restating the scaffold's harness default was corrected to the ruled behaviour — a fact brought current, not a change to what the guide teaches or gates; the ruling is already on the record."
informed_by:
  - id: scaffold-harness-is-an-explicit-selection-2026-09-15
    commit: 4d56957223c45678f01709d5731b685899efe3d4
tags: [cue, docs, scaffold, phase-8]
---

# Cue: `first-hour-guide` was modified — inflection?

## The Change
The build commit for `scaffold-harness-is-an-explicit-selection-2026-09-15`
corrected the sentence in *The agent builds in isolation* saying omission of `--harness` preserved the Claude compatibility default in `docs/first-hour.md`. The guide now says what the tool does: omitted,
`scaffold` asks at a keyboard and refuses with the list otherwise. Nothing else
in the guide moved.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Not an inflection.** The guide restated a mechanical fact — the tool's
default — and the fact changed by a ruling recorded before the edit. The
guide's own path (what it teaches an operator to do, and in what order) is
unchanged: the reader still runs `scaffold` with a harness selection; the
only difference is what happens when they forget the flag, and that is now the
tool's to say. Dependants that cite this guide cite its walk, not that
sentence. Had the guide's *instruction* changed — a new step, a removed one —
the four-beat pass would be owed.

*Answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`, by citation of the ruling
that made the change. The operator may overturn it by editing the verdict.*
