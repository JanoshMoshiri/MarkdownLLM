---
id: cue-standing-watch-specification-2026-10-30
type: cue
status: answered
version: 1.0
created: 2026-10-30
subject: standing-watch-specification
raised_at: bf2d230080bb08cf27afa82735b343bbec516c6b
raised_by: "floor — mdllm cues --staged --raise"
verdict: inflection
verdict_reason: "Harness bindings recorded (Hermes, Claude Code via /watch, Codex relayed) and the self-wake made seat-aware; the ad-hoc loop's wake paragraph and the a2a plan revised in this commit on the operator's direction of 2026-10-30."
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `standing-watch-specification` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-10-30: `standing-watch-specification` is a
definition surface (`specification`) and changes in the commit this cue rides in,
on top of `bf2d230`. 14 thing(s) depend on it: `a2a-conversations-on-their-own-branch`, `ad-hoc-message-loop`, `between-sessions-surface-is-real-2026-09-21`, `loop-turns-self-heal-2026-09-23`, +10 more. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `a2a-conversations-on-their-own-branch` — linked_things `extends` — consistent
- [x] `ad-hoc-message-loop` — linked_things `implements` — revised — its *Session wake* paragraph replaced the blocking-watch instruction with the per-harness binding, in this commit (1.1 -> 1.2)
- [x] `between-sessions-surface-is-real-2026-09-21` — linked_things `informs` — consistent
- [x] `loop-turns-self-heal-2026-09-23` — linked_things `informs`; informed_by pin — consistent — the self-heal rule stands; the ring is narrowed to the commits the declared seat authored, which is what *your* turn meant
- [x] `mesh-safety-is-the-floor-not-the-topology` — linked_things `informs` — consistent
- [x] `openclaw-adapter` — linked_things `implements` — consistent
- [x] `openclaw-adapter-acceptance-matrix-2026-09-24` — linked_things `implements` — consistent
- [x] `openclaw-adapter-seam-analysis-2026-09-24` — linked_things `references` — consistent
- [x] `run-membership-is-realisation-2026-09-22` — linked_things `informs`; informed_by pin — consistent
- [x] `seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15` — linked_things `references` — consistent — the ruling wanted the record to tell seats apart; the watch now uses that
- [x] `substrate-native-a2a` — linked_things `informs` — revised — *The wake itself* records both fixes and the live proof still owed, in this commit (1.6 -> 1.7)
- [x] `the-record-holds-unattended` — linked_things `references` — consistent
- [x] `the-seat` — linked_things `extends` — consistent — Phase 1's seat is what the watch now reads; Phase 4 (the watch knows its seat) and Phase 7's ring are unchanged, the ring named here as the backstop
- [x] `ticket-is-the-ad-hoc-carrier-2026-09-30` — linked_things `informs`; informed_by pin — consistent
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

## The Answer — walked 2026-10-30

Two lines revised, the rest held. The change adds the section the spec
lacked — what rises on exit 0, per harness — and narrows the self-wake to
the declared seat's own commits. The operator's direction, in their words
(2026-10-30): *"let's build them both… At least get Claude working, and
we'll put the self-waking properly."* The only dependant whose operative
text moved is `ad-hoc-message-loop`, whose *Session wake* paragraph told a
seat without an adapter to hold a blocking watch inside its turn — the
instruction the record of 2026-10-11 shows failing — and now names the
binding per harness; `substrate-native-a2a` records the same under *The
wake itself*. The OpenClaw adapter things hold: their binding is theirs and
this section does not claim it. **Verdict: inflection**, ruled by the
operator; the live round trip with no human relay remains the proof owed.
