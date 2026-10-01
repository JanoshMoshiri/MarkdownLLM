---
id: cue-framework-map-2026-10-01
type: cue
status: answered
version: 1.0
created: 2026-10-01
subject: framework-map
raised_at: ee2096ec2414a79d6e91c6693fe5757a77cc2c19
raised_by: "framework domain agent, 2026-10-01, attended session; answered under framework-agent-closes-settled-cues-2026-09-13"
verdict: not-inflection
verdict_reason: "Only the mechanical `spec-edges` managed block moved — `mdllm docs .` regenerated it after standing-watch.md gained one derived-from edge to ticket-is-the-ad-hoc-carrier-2026-09-30. No authored prose, count or drawn edge changed."
informed_by:
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    commit: 5f8a90a46920733b877528c039003f7a5583bc1c
tags: [cue, raised-mechanically-derived]
---

# Cue: `framework-map` was modified — inflection?

## The Change

Commit `ee2096e` regenerated the map's `spec-edges` managed block: the
`standing-watch.md` line now reads "+11 edge(s) outside the spec layer"
instead of +10, because the spec gained a `derived-from` edge to the ticket
ruling. The regeneration was demanded by `mdllm coherence` and produced by
`mdllm docs .`; no human-authored line in the map moved.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer

**Not an inflection.** A regenerated derived block is the floor keeping a
view current, not a change to anything the domain reasons from. The
underlying inflection — the ticket — is raised and walked on
`standing-watch.md` (`cue-standing-watch-specification-2026-10-01`). The
prose-only residue the tool cannot read (View 1 counts, drawn edges,
`accDescr`) was checked and does not mention the edge count that moved.

*Answered by the framework domain agent in an attended session under
`framework-agent-closes-settled-cues-2026-09-13`. The operator may overturn
this verdict by editing it — the cue stays on the record either way.*
