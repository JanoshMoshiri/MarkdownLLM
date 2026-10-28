---
id: the-gate-reads-presence-the-spec-promises-the-walk
type: conflict
status: open
created: 2026-10-27
session: 2026-10-27
parties:
  - change-reconciliation-specification
  - the-verdict-is-asked-where-the-change-lands-2026-10-05
confidence: high
origin: stated
tags: [commit-gate, cue, walk, seat-protocol, floor]
linked_things:
  - id: change-reconciliation-specification
    relation: references
    notes: "The Walk Runs On Detection: the dependants judged, the revisions and the answered cue in the same commit — the commit is refused until its walk is on record."
  - id: the-verdict-is-asked-where-the-change-lands-2026-10-05
    relation: references
    notes: "The ruling the gate implements: refuse while a definition surface changes with no cue on disk; one ask per subject per day; a cue raised today covers the day's later edits."
  - id: cue-carrier
    relation: references
    notes: "Phase 7(a), done 2026-10-05, states the same-day rule in so many words. Phase 6's observations and the holistic review's F1 are the evidence that presence and walk are not the same record."
  - id: the-record-holds-unattended
    relation: derived-from
    notes: "Phase 4 files this conflict and settles nothing; the plan's other phases do not wait on it."
  - id: review-holistic-substrate-2026-10-21-codex
    relation: references
    notes: "F1: the gate checks that a cue exists, not that it was answered. Confirmed by probe 2026-10-24 and met live three times on 2026-10-27."
---

# The gate reads presence; the spec promises the walk

## The two positions

**`change-reconciliation.md` → The Walk Runs On Detection.** A change to a
definition surface is refused at the commit boundary until its walk is on
record: the dependants judged, the revisions made, the cue answered with
its verdict, all in the commit the change lands in. The README and the
AGENTS.md hard-hook line say the same in the operator's words — *refused
until its walk is on record*.

**`the-verdict-is-asked-where-the-change-lands-2026-10-05`**, implemented
by `cue-carrier` Phase 7(a). The gate refuses while a definition surface
changes with *no cue on disk*; it asks once per subject per day; a cue
raised today covers the day's later edits to its subject. The verdict's
currency is not read. This was deliberate — the digest's re-listing is the
enforcement for a cue left unanswered, and one ask per day keeps the
boundary from nagging — and it is what runs.

## Why they are in conflict

Both are specified; the floor enforces the weaker. Three instances on
2026-10-27 alone: the manifesto changed twice (2.10 then 2.11), the
closed-loop plan changed with an answered cue from 2026-10-17 on disk, and
the operator guide changed twice — in each case `cues --staged --raise`
raised nothing and the commit would have passed with no walk of the second
change. The agent walked each on the existing cue by hand and said so;
nothing required it to. The holistic review's F1 (2026-10-21) named the
gap; the probe of 2026-10-24 confirmed it; today it was met live.

A reader of the spec expects the second change refused until walked. A
reader of the ruling expects it covered by the day's cue. The record
promises one thing and does another, and `docs/limitations.md` tells a
newcomer the first.

## The three readings — stated, not recommended

1. **The gate reads the verdict.** A cue on disk covers a change only
   while its `raised_at` precedes the change and its `verdict` is recorded;
   a later edit to the same subject, or an unanswered cue, refuses the
   commit. The walk is sealed or the change does not land. Cost: more
   refusals in a working day; the unattended run already raises-and-files
   under this reading.
2. **Presence is enough; the digest enforces.** What runs today. The spec's
   sentence and the README's are revised to say *until its question is on
   record*, and the walk's completion is the digest's and the
   retrospective's to chase (scan 4). Cost: the public claim weakens to
   what the floor does.
3. **The seat decides.** Presence is enough for an unattended seat (it may
   not answer); the verdict and its currency are required for an attended
   one. `MDLLM_UNATTENDED` already distinguishes them at the gate. Cost: two
   behaviours for one boundary, each documented.

## What resolves it

An operator ruling, recorded here as `resolution` with the reading chosen
and the sentence that changes — in the spec, or in the floor. Until then
the agent walks a second same-day change on the existing cue and says so,
as was done today, and nothing else waits.
