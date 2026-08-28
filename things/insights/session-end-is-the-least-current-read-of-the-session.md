---
id: session-end-is-the-least-current-read-of-the-session
type: insight
status: active
version: 1.0
created: 2026-08-28
session: 2026-08-28
source: agent
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Promote into session-memory.md + the session-end-continuity prompt on a second sighting, or immediately if a session-end report is ever filed from a stale base without the discrepancy being caught. Dismiss if a ruling records that session-end state reports are deliberately point-in-time and unpinned — a defensible position, but it should be written down rather than left as an absence."
linked_things:
  - id: a-session-harvest-must-read-the-commit-stream
    relation: extends
    notes: "Same ritual, the other half. That insight fixed what a session-end *harvested* (context is lossy, so read the commit range); this names what a session-end *asserts about state* — open loops, conflicts, publication debt — which inherits the start digest and has no currency gate at all."
  - id: existence-is-not-currency
    relation: supports
    notes: "The sixth instance of one idea: the digest existed, was well-formed, and was emitted seconds before it was read — none of which made it current."
  - id: a-well-kept-record-reads-as-a-governed-world
    relation: implements
    notes: "An instance of the law, one day after it was minted, on the substrate's own attention surface: the digest was authoritative in form and 40+ commits behind in fact, and its quality is exactly why it would have been believed."
  - id: session-start-loses-to-the-first-request
    relation: complements
    notes: "The bookend. That insight is about the ritual at t=0 losing to the live request; this is about the ritual at t=end inheriting t=0's view. Both are the lifecycle's ends failing for structural rather than motivational reasons."
  - id: estate-retrospective-synthesis-2026-08
    relation: derived-from
    notes: "Found while ending that synthesis's session — the session whose write was correctly pinned and whose close, 31 hours later, was not."
---

# Session End Is the Least Current Read of the Session

## The Insight

The significant-read boundary protects **writes**: pin a `commit:<sha>` base,
and re-assert it with `--assert-head` immediately before writing conclusions
from a long read. The session-end ritual then writes a different class of
conclusion — open loops, contradictions introduced, insight dispositions, and
a publication-debt report — and **has no currency gate of any kind**. Grepped
against `templates/prompts/session-end-continuity.md` (2026-08-28): no
`assert-head`, no pin, no base, no re-read instruction for state.

The exposure is structural rather than occasional. **Session end is by
construction the moment of greatest elapsed time since the session's pin.**
Every other beat in the lifecycle runs earlier than it does. So the one beat
that reports on current domain state is the one guaranteed to be furthest
from the state it reports.

## The Evidence (2026-08-28)

The session that produced `estate-retrospective-synthesis-2026-08` pinned
`3c1b449` and asserted it correctly before writing — the boundary worked. The
session then stayed open and was closed **31 hours later**. At close, the
session-start digest presented to the ritual named:

- significant-read base `43ba81a` — an ancestor **40+ commits** behind actual
  HEAD (`e27240d`);
- publication debt **"+17 (unpushed)"**;
- 28 open loops and a velocity line reading "last `things/` change 4 hours ago".

Direct `git` reads at close established the real state: the operator had
**pushed** (`origin/main` at `e5c97da`), leaving the root `ahead 1` — and
`ahead 2` a few commands later, because another session committed *during the
ritual*. In the interval the gates census had been ratified, three floor
defects the synthesis named had been fixed, a zero-run sensor built, and two
owed retrospectives written.

Had step 6 been performed from the digest, it would have reported a
seventeen-commit publication debt that did not exist and, more seriously,
**missed that the release push had already happened** — the single event the
report exists to surface. Steps 3 and 4 would have reasoned about
contradictions and open loops in a tree superseded a day earlier.

The mechanism producing the stale digest is not established from inside the
session, and does not need to be: the lesson holds whether it was a cached
emission or a hook that ran hours before the close. *A ritual that reports
state must establish its own currency rather than inherit it.*

## Why It Is Not Covered Already

`a-session-harvest-must-read-the-commit-stream` fixed the adjacent half and is
promoted into this same ritual: the *harvest* must read the commit range
because surviving context is lossy. That rule is about what the session
**learned**. It says nothing about the state the session-end **asserts**, and a
session can obey it perfectly — as this one did, reading the full range since
its own commit — while still filing a publication-debt line from a stale
digest. The two failures have different sources: context loss versus base
drift.

## The Candidate Remedy (not built here)

One line in the ritual, mirroring the boundary that already exists for writes:
**re-assert the base before step 4**, and derive the publication-debt report
from a live `estate-sync --status` rather than from the start digest — which
step 6 already instructs, and which is precisely why the discrepancy surfaced
here at all. The cheap version is a sentence in
`templates/prompts/session-end-continuity.md`; the mechanical version is the
same `--assert-head` call the write path uses, with moved HEAD as a
reconciliation stop rather than a blocker, since a session-end must still be
allowed to close.

The choice between them is a doctrine call for `session-memory.md`, not a code
fix — which is why this is recorded rather than applied.

## The Shape Worth Keeping

Ask of any beat that reports state: **when was its view established, and what
re-establishes it?** A beat that inherits its view from an earlier beat inherits
that beat's age too — and the later it sits in a lifecycle, the more that
inheritance costs.
