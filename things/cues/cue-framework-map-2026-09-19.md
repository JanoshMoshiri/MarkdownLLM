---
id: cue-framework-map-2026-09-19
type: cue
status: answered
version: 1.0
created: 2026-09-19
subject: framework-map
raised_at: ce1a1e6a13c700759c02f9082e2aef40cd934911
raised_by: "agent — the substrate-native-a2a build session of 2026-09-19, under framework-agent-closes-settled-cues-2026-09-13; raised in the commit that made the change"
verdict: not-inflection
verdict_reason: "A subcommand count 36 -> 37 and one View-3 node for `watch`. Identical in shape to cue-framework-map-2026-09-12, which ruled the same change not-inflection: the map documents and defines nothing, and coherence blocks the commit if the count does not move with the CLI."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
tags: [cue, substrate-native-a2a, change-reconciliation]
---

# Cue: `framework-map` was modified — inflection?

## The Change

Commit `ce1a1e6`: the subcommand count raised 36 → 37 in View 1 and the
accessibility description, and View 3 gained `watch` mapped to
`workflow-state.md`.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer

**Not an inflection**, on the direct precedent of
`cue-framework-map-2026-09-12`, which ruled exactly this change shape — a
count and one View-3 node for a newly landed subcommand — the same way. The
map documents; it defines nothing. Its three inbound edges reference it as a
navigation surface, not as a rule.

The change was not discretionary: `mdllm coherence` had already blocked the
commit for the stale count, which is the dark region being mechanical rather
than remembered.

*Answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`. The operator may overturn
this verdict by editing it — the cue stays on the record either way.*
