---
id: cue-substrate-native-a2a-2026-10-01
type: cue
status: answered
version: 1.0
created: 2026-10-01
subject: substrate-native-a2a
raised_at: 5f8a90a46920733b877528c039003f7a5583bc1c
raised_by: "framework domain agent, 2026-10-01, attended session — raised in the modifying commit, so the pin is its parent; answered in the same commit under framework-agent-closes-settled-cues-2026-09-13 by citing the operator's ruling"
verdict: inflection
verdict_reason: "1.5 → 1.6 qualifies a standing refusal (no new thing type for the turn → artefact turns only) and adds Phase 7. Ruled by the operator 2026-09-30 (ticket-is-the-ad-hoc-carrier-2026-09-30). The one dependant that reasons from the refusal — standing-watch.md — carries the same qualification in the same commit (cue-standing-watch-specification-2026-10-01)."
informed_by:
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    commit: 5f8a90a46920733b877528c039003f7a5583bc1c
tags: [cue, ticket, a2a]
---

# Cue: `substrate-native-a2a` was modified — inflection?

## The Change

`substrate-native-a2a` 1.5 → 1.6: the refusal *no new thing type for the
turn* narrowed to artefact turns and qualified for ad-hoc messages; Phase 7
(the ticket) added with the live test and the Codex-timeout risk recorded;
two Done-When lines added. This plan has seven inbound edges and
`standing-watch.md` inherits its refusal list verbatim, which is why a change
to a refusal is reasoned-from.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer

**Inflection — walked and sealed in the raising commit.** The earlier cues on
this plan were `not-inflection` because phases advancing is bookkeeping. This
one changes a *refusal*, which is a rule other things reason from. The driver
is the operator's ruling of 2026-09-30
(`ticket-is-the-ad-hoc-carrier-2026-09-30`), cited rather than re-decided.

Touch points walked: `standing-watch.md`, the one dependant that inherits
the refusal, carries the identical qualification and the protocol
(`cue-standing-watch-specification-2026-10-01`). `transport-follows-corpus-
holdability-not-distance` and `phase-3-run-domain-task-reverted` are
untouched — the ticket crosses no wire and stays intra-domain, so the
transport and cross-domain refusals stand exactly as written.

*Answered by the framework domain agent in an attended session under
`framework-agent-closes-settled-cues-2026-09-13`, citing the operator's
ruling. The operator may overturn this verdict by editing it — the cue stays
on the record either way.*
