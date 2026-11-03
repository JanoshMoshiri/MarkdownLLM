---
id: cue-ad-hoc-message-loop-2026-11-03
type: cue
status: answered
version: 1.0
created: 2026-11-03
subject: ad-hoc-message-loop
raised_at: ee5940dce77e0746660c706d051bb22109d5d9ce
raised_by: "floor — mdllm cues --staged --raise"
verdict: inflection
verdict_reason: "The definition's 'only writer' sentence became 'only writer of the turn' with the note added, on the operator's ruling; stages and transitions are unchanged."
tags: [cue, raised-mechanically, commit-boundary]
---

# Cue: `ad-hoc-message-loop` was modified — inflection?

## The Change
Raised by the floor at the commit boundary on 2026-11-03: `ad-hoc-message-loop` is a
definition surface (`workflow-definition`) and changes in the commit this cue rides in,
on top of `ee5940d`. 6 thing(s) depend on it: `a-note-on-a-held-ticket-rings-its-addressee-2026-11-02`, `run-reckoning-phase-4-2026-10`, `ticket-reckoning-phase-4-review`, `standing-watch-specification`, +2 more. `git show` on the carrying commit shows what
moved. The raise and the walk list below are mechanical; the judgement on
each line is the agent's, within the four bounds; the ruling on what the
agent may not settle is the operator's
(`the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05`).

## The Walk
- [x] `a-note-on-a-held-ticket-rings-its-addressee-2026-11-02` — linked_things `informs` — ruling — the operator's answer, in their words, is this decision: "There needs to be an interrupt, or at least a flag set that's picked up on the end of processing of a turn… I think it should be an interrupt… It works the same way as prompts do when they're steering."
- [x] `run-reckoning-phase-4-2026-10` — linked_things `references` — consistent — a run scoped to this loop; its stages and edges are unchanged, only the writer sentence moved
- [x] `ticket-reckoning-phase-4-review` — linked_things `references` — consistent — a closed ticket on this loop; nothing it did is re-read differently
- [x] `standing-watch-specification` — names it in the body — revised — the Ticket section, in this commit (0.8 -> 0.9)
- [x] `substrate-native-a2a` — names it in the body — revised — Phase 3's double-send line, in this commit (1.7 -> 1.8)
- [x] `ticket-is-the-ad-hoc-carrier-2026-09-30` — names it in the body — revised — superseded in part, in this commit (1.0 -> 1.1)
Mark each line: `consistent` — holds as written; `revised` — a
restatement-level edit in this commit (say what); `ruling` — the operator's
answer, in their words, to a question you could not settle. The conceptual
residue — a thing that reasons about `ad-hoc-message-loop` without naming it — is yours
to read; add a line for it if you find one.

## The Answer
Open until every line above is marked. `verdict: inflection` if any line is
`revised` or `ruling`; `not-inflection` if every line held. One-line
`verdict_reason`; `status: answered`; the revisions in this commit. An
unattended run leaves this open, the checklist unmarked, and writes its
proposed revisions here (`unattended-cue-carrier-2026-09-12`).

## The Answer — walked 2026-11-03

One line ruled, three revised, two held. The definition's stages and
declared edges did not move; the sentence that said the addressee is the
only writer now says the only writer *of the turn*, and names the note the
other seat may append and the ring it causes. The shipped template says the
same. The run and the ticket that instantiate this loop are unaffected: a
note is a new kind of write, not a new stage. **Verdict: inflection**,
ruled by the operator.

## Second change, same day — the actors are the seat names

The stages and edges are renamed `claude` / `codex` -> `workspace-1` /
`workspace-2`, the rename the 2026-10-30 seat ruling deferred until both
clones carried clone names; the schema's ticket vocabulary and the generated
types block follow, and the session-wake paragraph says the role defaults
to the declared seat and the message rides the wake. The gate found this
cue already carrying the day. Same six dependants: the completed run
`run-reckoning-phase-4-2026-10` names the old vocabulary in its narrative
as what was declared on 2026-10-20, which is history and holds; its
`current_stage` is its own definition's, not this loop's; the one ticket is
closed and reads nothing by the old names; the spec, the plan and the
carrier decision are unchanged by a rename. **Verdict stands: inflection**
— the definition's turn tokens changed on the operator's ruling.
