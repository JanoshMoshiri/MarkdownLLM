---
id: cue-ticket-is-the-ad-hoc-carrier-2026-09-30-2026-11-03
type: cue
status: answered
version: 1.0
created: 2026-11-03
subject: ticket-is-the-ad-hoc-carrier-2026-09-30
raised_at: ee5940dce77e0746660c706d051bb22109d5d9ce
raised_by: "floor — mdllm cues --staged --raise"
verdict: inflection
verdict_reason: "The decision is superseded in part: its double-send clause deferred to a live run, the run arrived, and the operator ruled the note an interrupt; the spec and plan that restated the clause are revised in this commit."
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `ticket-is-the-ad-hoc-carrier-2026-09-30` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-11-03: `ticket-is-the-ad-hoc-carrier-2026-09-30` is a
definition surface (`decision`) and changes in the commit this cue rides in,
on top of `ee5940d`. 5 thing(s) depend on it: `a-note-on-a-held-ticket-rings-its-addressee-2026-11-02`, `a2a-conversations-run-on-their-own-branch-2026-10-09`, `seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15`, `standing-watch-specification`, +1 more. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `a-note-on-a-held-ticket-rings-its-addressee-2026-11-02` — linked_things `supersedes` — ruling — the operator's answer, in their words, is this decision: "There needs to be an interrupt, or at least a flag set that's picked up on the end of processing of a turn… I think it should be an interrupt… It works the same way as prompts do when they're steering." — it supersedes the double-send clause and nothing else
- [x] `a2a-conversations-run-on-their-own-branch-2026-10-09` — linked_things `extends` — consistent — the explicit-end clause and the branch lifecycle are untouched
- [x] `seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15` — linked_things `extends` — consistent — one ticket per work item, status the addressee, both unchanged
- [x] `standing-watch-specification` — linked_things `derived-from` — revised — the Ticket section's two protocol bullets, in this commit (0.8 -> 0.9)
- [x] `substrate-native-a2a` — linked_things `derived-from` — revised — Phase 3's double-send line, in this commit (1.7 -> 1.8)
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle. The conceptual
residue — a thing that reasons about `ticket-is-the-ad-hoc-carrier-2026-09-30` without naming it — is yours
to read; add a line for it if you find one.

## The Answer
Open until every line above is marked. `verdict: inflection` if any line is
`revised` or `ruling`; `not-inflection` if every line held. One-line
`verdict_reason`; `status: answered`; the revisions in this commit. An
unattended run leaves this open, the checklist unmarked, and writes its
proposed revisions here (`unattended-cue-carrier-2026-09-12`).

## The Answer — walked 2026-11-03

One line ruled, two revised, two held. The change to this decision is the
appended *Superseded in part* section and the `superseded-by` backlink: the
clause that answered the content-change wake *no until a live run shows the
need* is replaced by the 2026-11-02 ruling; the carrier itself, the
transcript-in-git, the safety rule and the transient tree all stand. The
spec and the a2a plan restated the clause and are edited with it here; the
branch ruling and the work-item ruling never leaned on it. **Verdict:
inflection**, ruled by the operator.
