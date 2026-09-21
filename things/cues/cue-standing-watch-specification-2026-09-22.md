---
id: cue-standing-watch-specification-2026-09-22
type: cue
status: answered
version: 1.0
created: 2026-09-22
subject: standing-watch-specification
raised_at: b38a62f69edf906e1577ef67e51edd2fdb73cc53
raised_by: "agent — session end 2026-09-22, under framework-agent-closes-settled-cues-2026-09-13"
verdict: not-inflection
verdict_reason: "A draft spec correcting its own day-old claims by building what it specified (0.1 → 0.2). Its dependents — two rulings, the plan, the reconciliation cue — were all written in this arc; none reasoned from the pin claim or the empty-board wording the build corrected. The contract every consumer actually reads (refusals, exit codes, the five decisions) is unchanged."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: b38a62f69edf906e1577ef67e51edd2fdb73cc53
  - id: run-membership-is-realisation-2026-09-22
    commit: b38a62f69edf906e1577ef67e51edd2fdb73cc53
tags: [cue, standing-watch, change-reconciliation, draft]
---

# Cue: `standing-watch-specification` was modified — inflection?

## The Change

`b38a62f`, version 0.1 → 0.2, one day after birth. The Scope section drops
its precondition (the membership edge was ruled) and corrects two claims the
build proved imprecise: the pin that "came for free" is the run's own, which
only a vertical watch on `current_stage` reads — a horizontal watch reads the
loop at the remote head like everything else; and the fifth decision's
empty-board wording, which had silenced the one event a one-member scoped
board exists to carry. The usage line gains `[--run <id>]`; the Maturity Path
records the scope as landed.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer

**Not an inflection.** The spec is `draft`, and this is the draft doing the
one thing `draft` is for: being corrected by the first thing built against
it. The corrected claims had no dependents — every inbound edge is from this
arc, and each reasoned from the parts that did not move: the two channels,
the refusals, the exit-code contract, the five decisions, peers-not-
orchestrator. The scope's *direction* was right; two of its *details* were
not, and both are now recorded in place with the date and the reason rather
than silently rewritten.

Worth stating for the next reader: `draft → evolving` is still gated on
Phase 4 of `substrate-native-a2a` crossing a real turn. This correction does
not advance the status; a spec validated by its own tests is validated by
its own tests.

*Answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`, citing
`run-membership-is-realisation-2026-09-22`. The operator may overturn this
verdict by editing it — the cue stays on the record either way.*
