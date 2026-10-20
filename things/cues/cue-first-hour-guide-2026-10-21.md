---
id: cue-first-hour-guide-2026-10-21
type: cue
status: answered
version: 1.0
created: 2026-10-21
subject: first-hour-guide
raised_at: b7df2830ff3d0e83c1f763635f19bb782f769517
raised_by: "floor — mdllm cues --staged --raise"
verdict: not-inflection
verdict_reason: "The guide was rewritten to the shape the 2026-10-20 ruling ordered; its five dependants are that ruling, the glossary it now links, the audit it answers, and the onramp plan and insight it still cites as they stand — none reasons from the text that changed."
informed_by:
  - id: documentation-rulings-2026-10-20
    commit: 08f6ac78389c5fe1355089f80c166a707f3a3dc5
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `first-hour-guide` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-21: `first-hour-guide` is a
definition surface (`guide`) and changes in the commit this cue rides in,
on top of `b7df283`. 5 thing(s) depend on it: `documentation-rulings-2026-10-20`, `glossary`, `operator-seat-and-harness-native-onramp`, `review-documentation-audit-2026-10-20-claude`, +1 more. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `documentation-rulings-2026-10-20` — linked_things `informs` — **consistent**: the ruling ordered this rewrite — workspace wording, the generated install pin, an hour ending in one whole session; v1.8 is that ruling carried out
- [x] `glossary` — linked_things `complements` — **consistent**: the guide now links the glossary's anchored rows at first use (workspace, floor, thing, orient, walk, the close); every anchor it links exists in glossary 1.1
- [x] `operator-seat-and-harness-native-onramp` — linked_things `references` — **consistent**: the guide still names that plan as the route for the newcomer who will never open a terminal, and now says it is paused, which is the plan's status
- [x] `review-documentation-audit-2026-10-20-claude` — linked_things `informs` — **consistent**: the audit's findings on this guide — the stale install pin, /orient only in a footnote, no session end, Explorer offered while parked, the onramp 'being built' — are each answered in v1.8
- [x] `the-onramp-is-the-operators-own-sentence` — linked_things `references` — **consistent**: the honest footnote keeps the insight's four ideas for the domain expert who will not open a terminal, unchanged
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle. The conceptual
residue — a thing that reasons about `first-hour-guide` without naming it — is yours
to read; add a line for it if you find one.

## The Answer
**Not inflection.** First-hour 1.8 is package 5 of the documentation arc: workspace wording, the install through the README's generated pin, the Explorer and Desktop history removed, glossary links at first use, and an hour that ends in one whole session — /orient, work, a refused commit walked and ruled on, /end-session. None of its dependants reasons from the replaced text.
