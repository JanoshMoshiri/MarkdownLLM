---
id: cue-unattended-cue-carrier-2026-09-12-provenance-2026-09-13
type: cue
status: answered
version: 1.0
created: 2026-09-13
subject: unattended-cue-carrier-2026-09-12
raised_at: 2b12791fcfb2d6eb6c3f971bf444169667fb0815
raised_by: "agent — the framework domain agent, 2026-09-13, at session end"
verdict: not-inflection
verdict_reason: "A provenance correction and its postscript: one over-claimed informed_by pin to an unverified external artifact dropped, the linked_things reference kept. The ruling's content — who may raise, who may answer, what a run does — is untouched, and the two internal inputs it actually rests on are still pinned."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
tags: [cue, provenance, quarantine, session-end]
---

# Cue: `unattended-cue-carrier-2026-09-12` was modified — inflection?

## The Change
Commit 2b12791 dropped the `informed_by` pin to
`review-external-conflict-lifecycle-2026-09-08` (an `origin: external`,
`verified: false` artifact the quarantine rule forbids resting on) and added
a postscript recording why. The `linked_things: references` edge to the same
review survives, which is the honest relation: the review *raised* F5; the
ruling rests on the operator's judgement.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Not an inflection.** Nothing the decision rules changed: option 3 with
option 2's net, raise-never-answer for unattended runs, the receipt's shape.
What changed is a provenance claim that was too strong — and correcting a
provenance over-claim strengthens the decision's standing rather than
weakening it, because what it rests on is now exactly what it actually rests
on. The eleven things that link to this decision cite its ruling, not its
inputs.

*Answered by the framework domain agent under `framework-agent-closes-settled-cues-2026-09-13`. The operator may
overturn this verdict by editing it — the cue stays on the record either way.*
