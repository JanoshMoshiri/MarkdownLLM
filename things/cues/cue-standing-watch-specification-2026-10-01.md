---
id: cue-standing-watch-specification-2026-10-01
type: cue
status: answered
version: 1.0
created: 2026-10-01
subject: standing-watch-specification
raised_at: 5f8a90a46920733b877528c039003f7a5583bc1c
raised_by: "framework domain agent, 2026-10-01, attended session — raised in the modifying commit, so the pin is its parent; answered in the same commit under framework-agent-closes-settled-cues-2026-09-13 by citing the operator's ruling"
verdict: inflection
verdict_reason: "0.4 → 0.5 adds a protocol — the ticket — and qualifies a refusal. Ruled by the operator 2026-09-30 (ticket-is-the-ad-hoc-carrier-2026-09-30); dependants walked: substrate-native-a2a (Phase 7, refusal qualified, 1.6), AGENTS routing row, operator-guide watch line, _schema.yaml.template. workflow-state, trigger, coordination-claim and git-workflow are consumed unchanged — the ticket adds no field, no edge and no floor code."
informed_by:
  - id: ticket-is-the-ad-hoc-carrier-2026-09-30
    commit: 5f8a90a46920733b877528c039003f7a5583bc1c
tags: [cue, ticket, a2a]
---

# Cue: `standing-watch-specification` was modified — inflection?

## The Change

`standing-watch.md` 0.4 → 0.5: a new section, *The Ticket — An Ad-Hoc
Message With No Artefact Behind It*, carrying a protocol (who writes, one
message per turn, how to close, the safety rule, why the type is
domain-declared); the refusal *no new thing type for the turn* narrowed to
artefact turns and qualified; the maturity ladder's `evolving` condition
widened to accept one ticket round trip. `mdllm touchpoints
standing-watch-specification` lists what depends on it.

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?
(`change-reconciliation.md` → The Driver Names The Inflection.)

## The Answer

**Inflection — walked and sealed in the raising commit.** A new protocol is a
new path, and a qualified refusal is a changed rule. The driver is the
operator's ruling of 2026-09-30, recorded as
`ticket-is-the-ad-hoc-carrier-2026-09-30`, which this cue cites rather than
re-decides.

Touch points walked:

- `substrate-native-a2a` — its own copy of the refusal qualified in the same
  words; Phase 7 added; Done-When extended; 1.5 → 1.6. Cued separately
  (`cue-substrate-native-a2a-2026-10-01`).
- `AGENTS.md` routing row for `standing-watch.md` — names the ticket.
- `docs/operator-guide.md` `watch` when-line — names the ticket.
- `templates/_schema.yaml.template` — the commented `ticket` entry.
- `workflow-state.md`, `trigger-specification.md`, `coordination-claim.md`,
  `git-workflow.md` — consumed, not amended: the ticket uses `stages[].actor`,
  `status_changed_to`, publication-is-the-turn and the existing board exactly
  as specified, and declines `held_by` because the status already names the
  one writer. Nothing in them changes.
- The floor — unchanged by test: `TestTicketLoop` proves the existing
  contract carries the ticket.

*Answered by the framework domain agent in an attended session under
`framework-agent-closes-settled-cues-2026-09-13`, citing the operator's
ruling. The operator may overturn this verdict by editing it — the cue stays
on the record either way.*
