---
id: review-external-conflict-lifecycle-2026-09-08
type: artifact
status: stable
version: 1.0
created: 2026-09-08
origin: external
verified: false
tags: [review, external, conflict, retrospective, reconciliation, invocation-point]
linked_things:
  - id: circulation-is-not-disposition
    relation: informs
    notes: "Finding F2 promoted to its own insight — this record is its evidence base."
  - id: belief-revision-specification
    relation: references
    notes: "v1.3 — Who Reads An Open Conflict; Reasoning While A Conflict Is Open — is the reconciliation of F2 and F3."
  - id: retrospective-specification
    relation: references
    notes: "v1.6 — produces item 3 (whole-set conflict triage); the command surfaces now fire all seven scans (F1, F4)."
  - id: change-reconciliation-specification
    relation: references
    notes: "F5 — who declares an inflection when an unattended agent commits — is left open against The Driver Names The Inflection, for the operator."
---

# External Review — Conflict Lifecycle And The Retrospective Entry Point (2026-09-08)

**Reviewer:** an independent session, relayed by the operator; it read the two
ritual command files as the actual entry points rather than the specs as
written, then `belief-revision.md`, `change-reconciliation.md`, and
`retrospective.md`. **Quarantine:** `origin: external`, unverified at birth —
the flip is the operator's separate, attributed commit, exactly the two-commit
rule the operator described to the reviewer. Each finding below was checked
against the code and the files before anything was changed; where the review
was wrong the disconfirmation is recorded, not smoothed over.

## Verdict As Received

> The retrospective command fires three of the spec's seven scans. Scan 4 —
> change-driven reconciliation, "the net beneath the net" — is the one both
> specs point at and the invocation point does not have. Conflicts are created
> at two cadences and dispositioned at none; the framework's higher-stakes
> object has the weaker lifecycle. Smallest fix that closes the most: add scan
> 4 to the retrospective command, and add a conflict-disposition beat to
> end-session mirroring the insight brake.

## Findings And Dispositions

**F1 — The retrospective command fired 3 of 7 scans.** *Confirmed.*
`templates/commands/retrospective.md` (and its three projections) ran scans
1, 2 and 7; scans 3–6 existed only in the spec. Change-driven reconciliation
(scan 4) was bound to the `retrospective` hook by *both*
`change-reconciliation.md` and `retrospective.md` and wired by neither
command. **Fixed:** all four command surfaces now enumerate the seven scans
plus whole-set conflict triage, each numbered against the spec's list so
drift between the two is visible on read.

**F2 — Conflicts had creation at both cadences and disposition at neither.**
*Confirmed in substance; one detail disconfirmed.* The reviewer said "unlike
insights there's no validate finding to drive a brake." There was one: the
floor has raised Info for an `open` conflict with no inbound edge from a live
thing since 2026-06-27 (`validation.py`, dissolve-continuity Phase B). What
was missing was a *reader* — the end-session brake acted only on
insight-disposition findings — and the second finding both specs promised
from v1.0 and the floor never carried: *open conflict untouched 30+ days →
Info*. The corpus's one open conflict demonstrated the gap live: 12 days old,
a proposed resolution written in its body, a live inbound edge, and every
mechanical signal reading healthy. **Fixed:** `conflict_age_findings`
(commit-stream age, never mtime; fires through a live edge by design); the
`disposition: keep-active` + `disposition_reason` hold marker extended to
conflicts with the same no-reason nudge; the session-end brake reads both
findings (`session-end-continuity` v1.4, `session-memory.md` v1.6, all four
end-session command surfaces); the retrospective triages the whole open set
(`retrospective.md` v1.6, produces item 3) and its conditions-met pass re-reads
held conflicts' reasons. Promoted to `circulation-is-not-disposition`.

**F3 — What does a consumer do while a conflict sits unratified?** *Was
implicit.* The operator's answer for the external route — nothing may rest
on an unverified import; trust is a named human's separate commit; only a
trusted import can raise a conflict at all — was correct and unrecorded.
**Recorded** in `belief-revision.md` → Reasoning While A Conflict Is Open,
together with a framework default for the internal case that the review
asked for and the operator had not yet stated: *proceed and flag* — reason on
the body's proposed reading, else the previously accepted position; name the
conflict in any output resting on it; never synthesise, never pick silently —
with per-conflict and per-domain tightening to *block*. The internal default
is this session's, not the reviewer's or the operator's; it is flagged for
the operator as the one rule defined beyond the review's explicit answers.

**F4 — Scans 3, 5 and 6.** Scan 3 (index rebuild): the floor refuses a
drifted deployed index at every commit, so the retrospective beat resets
provenance anchors rather than restoring parity — now said in the spec and
the command. Scan 5: the orphan half already ran at session cadence; the
composition pre-filter now runs in the command. Scan 6 (conditions-met): was
covered nowhere; now in the command, reading held conflicts as well as kept
insights.

**F5 — Who declares the inflection when an unattended agent commits?**
*Open — the operator's decision.* `change-reconciliation.md` defends the human
cue correctly and assumes a human at the keyboard when the change lands. The
reviewer's three options: (1) agents cannot inflect — anything that would be
one blocks for the operator; (2) agent changes are presumed un-reconciled and
swept by retrospective reconciliation as a matter of course; (3) agents may
raise a cue but not answer it — the change lands flagged and disposition
queues for the operator. What exists today toward option 3: the pre-commit
`candidates` leg already classifies every staged thing and prints the cue —
advisory, exit 0, to a terminal nobody reads at 3am. What does not exist: a
persisted place an unanswered cue goes. With scan 4 now wired, option 2's net
at least fires each period. Recorded here, not decided.

**Structural observation, recorded.** `retrospective.md` is `stable`;
`change-reconciliation.md` is `draft`. The draft carried the tighter reasoning
and the binding into the stable spec's entry point; the stable spec was making
a promise the draft was supposed to keep. Normal for draft-status work; worth
knowing when the next binding is written.

## What The Review Got Right That The Record Should Keep

Refusing to auto-resolve conflicts is the QMS instinct applied properly: a
conflict is a finding, and findings are dispositioned by a human, not by a
tiebreak rule. Making cross-domain communication an addressable interface,
arriving untrusted, with trust as a separate human-authored commit, and
conflicts held as state with two independent reconciliation cadences — that
is the flagship example, and none of it is visible from the README.
