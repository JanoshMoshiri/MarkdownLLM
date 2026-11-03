---
id: cue-standing-watch-specification-2026-11-03
type: cue
status: answered
version: 1.0
created: 2026-11-03
subject: standing-watch-specification
raised_at: ee5940dce77e0746660c706d051bb22109d5d9ce
raised_by: "floor — mdllm cues --staged --raise"
verdict: inflection
verdict_reason: "The one-writer and one-message rules now carry the note, on the operator's ruling of 2026-11-02; the loop definition, the a2a plan and the carrier decision are revised with it in this commit."
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `standing-watch-specification` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-11-03: `standing-watch-specification` is a
definition surface (`specification`) and changes in the commit this cue rides in,
on top of `ee5940d`. 16 thing(s) depend on it: `a-note-on-a-held-ticket-rings-its-addressee-2026-11-02`, `a2a-conversations-on-their-own-branch`, `ad-hoc-message-loop`, `between-sessions-surface-is-real-2026-09-21`, +12 more. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `a-note-on-a-held-ticket-rings-its-addressee-2026-11-02` — linked_things `informs` — ruling — the operator's answer, in their words, is this decision: "There needs to be an interrupt, or at least a flag set that's picked up on the end of processing of a turn… I think it should be an interrupt… It works the same way as prompts do when they're steering."
- [x] `a2a-conversations-on-their-own-branch` — linked_things `extends` — consistent
- [x] `ad-hoc-message-loop` — linked_things `implements` — revised — 'only writer' became 'only writer of the turn' and the note sentence was added, in this commit (1.2 -> 1.3)
- [x] `between-sessions-surface-is-real-2026-09-21` — linked_things `informs` — consistent
- [x] `loop-turns-self-heal-2026-09-23` — linked_things `informs`; informed_by pin — consistent — the self-wake is untouched; the note reuses its author-to-seat match
- [x] `mesh-safety-is-the-floor-not-the-topology` — linked_things `informs` — consistent
- [x] `openclaw-adapter` — linked_things `implements` — consistent
- [x] `openclaw-adapter-acceptance-matrix-2026-09-24` — linked_things `implements` — consistent
- [x] `openclaw-adapter-seam-analysis-2026-09-24` — linked_things `references` — consistent
- [x] `run-membership-is-realisation-2026-09-22` — linked_things `informs`; informed_by pin — consistent
- [x] `seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15` — linked_things `references` — consistent — the note is told from the holder's own write by the declared seat, which is what that ruling made readable
- [x] `seats-are-named-for-the-clone-not-the-agent-2026-10-30` — linked_things `references` — consistent — the author match is against the seat's name, whatever it is named for
- [x] `substrate-native-a2a` — linked_things `informs` — revised — Phase 3's double-send line carries the reopen and the answer, in this commit (1.7 -> 1.8)
- [x] `the-record-holds-unattended` — linked_things `references` — consistent
- [x] `the-seat` — linked_things `extends` — consistent — Phase 7's ring is unchanged; the seat read gains the unread-note line beside it, which the plan's 'the same read, made to ring' already describes
- [x] `ticket-is-the-ad-hoc-carrier-2026-09-30` — linked_things `informs`; informed_by pin — revised — superseded in part (the double-send clause) with the backlink, in this commit (1.0 -> 1.1)
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle. The conceptual
residue — a thing that reasons about `standing-watch-specification` without naming it — is yours
to read; add a line for it if you find one.

## The Answer
Open until every line above is marked. `verdict: inflection` if any line is
`revised` or `ruling`; `not-inflection` if every line held. One-line
`verdict_reason`; `status: answered`; the revisions in this commit. An
unattended run leaves this open, the checklist unmarked, and writes its
proposed revisions here (`unattended-cue-carrier-2026-09-12`).

## The Answer — walked 2026-11-03

Three lines revised, one ruled, the rest held. The change is the Ticket
section's two protocol bullets: the addressee owns the turn and anyone may
leave a note; a write at an unchanged status is a note and rings its
addressee, read from a content digest beside the status board and told
from the holder's own write by the declared seat. The ruling line is the
decision this commit records, in the operator's words. The revised
dependants are the three that restated the old rule — the loop definition's
'only writer', the a2a plan's 'settled: no', the carrier decision's deferral
— each edited at restatement level in this commit, the carrier decision
superseded in part with its backlink. The OpenClaw things, the branch plan,
the self-heal insight and the seat rulings hold: none of them reasons from
the one-message rule, and the note reuses the author match the self-wake
already had. **Verdict: inflection**, ruled by the operator; the live round
trip with no human relay is owed for the note as it is for the turn.
