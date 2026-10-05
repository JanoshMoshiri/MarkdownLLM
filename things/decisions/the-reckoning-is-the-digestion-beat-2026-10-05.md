---
id: the-reckoning-is-the-digestion-beat-2026-10-05
type: decision
status: made
version: 1.0
created: 2026-10-05
session: 2026-10-05
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [digestion, reckoning, disposition, insight, conflict, trigger, import, session-end, dispatcher, closed-loop, floor, seat]
informed_by:
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    commit: 69dade015b2d6114c706d8539dfb58434e11e488
  - id: closed-loop-operating-state
    commit: 68c83cee2b400b75c52f346c0506c01dfd273bb2
  - id: circulation-is-not-disposition
    commit: 8c52a723496f4a45fbcb042b1c61f5b49816c60b
  - id: a-stated-dismissal-condition-needs-a-reader
    commit: 7bffcb162f01c5cc6afb98756eca58bc5c5f79fe
  - id: session-memory-specification
    commit: 214770d5a267aa102c8c2a0eb36fd7a0e571bbea
  - id: retrospective-specification
    commit: 7487ab3c219946dc468ecda2ee228e4157437d6e
linked_things:
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    relation: extends
    notes: "The same principle, one beat later: the floor detects and assembles, the agent acts within bounds, the human rules on the residue, at a boundary the harness owns. That ruling gave the walk an actor; this gives disposition one."
  - id: circulation-is-not-disposition
    relation: references
    notes: "The diagnosis: attention items are created at three cadences and disposed of at none. This ruling is the disposition cadence."
  - id: a-stated-dismissal-condition-needs-a-reader
    relation: references
    notes: "Why nothing enters without its exit: a dismissal condition the floor can evaluate is the reader that insight asked for."
  - id: a-preserved-question-is-not-a-done-walk
    relation: references
    notes: "Why the reckoning gets an actor at a boundary and not a sixth backstop."
  - id: closed-loop-operating-state
    relation: informs
    notes: "Phase 3's seat queue: the reckoning's residue band is that queue, assembled by the floor."
  - id: session-memory-specification
    relation: informs
    notes: "The brake it names — capture and reckoning in balance — becomes a floor command and a gate on the session-end commit."
  - id: retrospective-specification
    relation: informs
    notes: "Scans 5 and 6 become reads of the reckoning; scan 7's promotion half is where surviving insights land."
  - id: the-reckoning
    relation: informs
    notes: "The plan that builds it."
---

# Decision: The Reckoning Is the Digestion Beat

## Context

The full read of the estate on 2026-10-05 (pinned at `c3c17e6`) found the
intake side of the loop mechanised and the release side missing. Triggers
fire, cues are raised, imports are mirrored and insights are harvested at
three cadences; conflicts, insights, cues, fired triggers, imports and stale
work are disposed of at none. In the workspaces: 307 active insights against
34 ever promoted, 44 open conflicts aged to 78 days, a digest line reading
"49 fired lines queued for the CTO, none dispatchable", a retrospective that
flagged 72 of 75 insights active and a population now at 87 of 95. The
record had named the pattern (`circulation-is-not-disposition`) and assigned
the act to two rituals — the session-end brake and retrospective scans 5 and
6 — which run at the end of a session, where they are economised, or at a
cadence that has not run in six weeks.

## The Ruling

The operator, 2026-10-05:

> "I don't want it to turn into another insight. I want it to turn into
> something that we can resolve the problem with. It's quite clear what the
> issue is: we've got some mechanisms that handle how things come in, but
> the mechanisms that handle how things are processed once in, and retained
> or released, are not quite right. So let's resolve that."

> "Exactly what you're describing is what I've been trying to create the
> whole time. We're in a position where we could act now to produce some
> mechanisms that would get us closer. Let's shape this and make this work
> properly in Claude Code, and then we'll bring it to Codex."

**Disposition gets an actor at a boundary, with the same split as the
walk.** The record's own name for the act is the reckoning
(`session-memory.md`: capture and reckoning stay in balance). It is built in
four parts:

1. **Nothing enters without its exit.** Every attention item carries an exit
   rule the floor can evaluate — a type default, overridable per item. An
   insight is promotable when its `promoted_to` target exists and dies
   unreferenced after a stated interval unless live work links it; a
   conflict is resolvable when both parties have moved or one is superseded;
   a fired trigger is self-answered when its action is already satisfied; an
   import is re-pinnable when its source moved and withdrawable when the
   source completed; in-progress work with every box ticked is completable.
2. **The floor reckons.** `mdllm reckon` computes every item's disposition
   candidate with its evidence, in three bands: *mechanical* (derivable from
   fields and git facts; the floor applies it with `--apply`), *settled* (the
   agent decides by citing the record or the evidence), *residue* (the
   operator, through the harness's own prompt). A clean reckoning is an empty
   residue: green is reachable.
3. **Two actors, no new ritual.** Attended, the session-end commit is refused
   by the commit-message leg while the mechanical band is pending, so the
   brake cannot be economised; the agent reckons, decides the settled band,
   and puts the residue to the operator. Unattended, the dispatcher's tick
   applies the mechanical band, drafts the settled one and files the residue
   in its digest. Retrospective scans 5 and 6 become reads of the same
   command.
4. **Retention is promotion.** An insight that survives is folded into a
   skill; a skill is a definition surface; the walk gate takes it from there.
   Intake, reckoning, promotion, walk: the loop closes on primitives that
   already exist.

A rate goes on the wall: created against disposed per week, open-age
distribution, walks against definition-surface changes, one line per
workspace in the digest.

## What This Settles

- The floor never decides a disposition of meaning: dismissing an insight
  that live work still cites, choosing a side in a conflict, cancelling work.
  Those are the residue and reach the operator through the prompt.
- Claude Code first, where the gates exist; Codex after, through its own
  adapter or the post-write channel. The nine dormant workspaces are not
  touched by hand; one unattended reckoning clears them once it works.
- Nothing further is built until the loop closes once: the first live
  reckoning is the QMS's twenty conflicts and eighty-seven insights, by hand,
  with the residue counted.
