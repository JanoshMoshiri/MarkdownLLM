---
id: open-questions-arrive-as-a-prompt-2026-09-23
type: decision
status: made
version: 1.0
created: 2026-09-23
session: 2026-09-23
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [seat, seat-protocol, cue, session-start, prompt, closed-loop, attention]
informed_by:
  - id: closed-loop-operating-state
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
  - id: unattended-cue-carrier-2026-09-12
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
  - id: cue-carrier
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
linked_things:
  - id: closed-loop-operating-state
    relation: informs
    notes: "Phase 3, the seat protocol: this rules the shape a seat item takes at session start."
  - id: unattended-cue-carrier-2026-09-12
    relation: extends
    notes: "That ruling made the question persist. This rules how it is presented when it does."
  - id: cue-carrier
    relation: informs
    notes: "The cue is the first seat-queue item with a carrier; it is the first item rendered in this shape."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: references
    notes: "Why the options are emitted, not described: a described question is skipped; an emitted one must be declined."
---

# Decision: Open Questions Arrive as a Prompt, Recommended First, Skipped Only on Purpose

## Context

The cue persists until a human answers it, and the session-start digest
re-lists it every session. It re-lists it as prose — a line among lines —
and the 2026-09-23 sweep found ten such lines that had survived every
session since 13 September. A question described is a question passed over.

## The Ruling

The operator, 2026-09-23:

> "At the start of the next session, after session start happens, the user
> is faced with the same thing: a prompt where they can pick the recommended
> option one, and then option two and three. They could just skip it, but it
> being shown to them like that brings it to their attention without them
> being able to just forget it. They have to actively skip it. That can work
> whether it's running with one harness or another — it doesn't matter."

**Every open seat item is emitted as a prompt: numbered options, the
recommended one first, and an explicit skip.** The framework emits the
options in the digest; whichever agent is running presents them in its own
harness's way — a choice dialog where one exists, a numbered list where not.
Skipping is an act the operator takes, and a skipped item returns next
session; it is deferred, never dismissed, because the point is that it
cannot be forgotten.

**Where the options come from.** For a cue: the two verdicts, with the
agent's recommendation and its reason where the record settles it. For a
drafted retrospective's dispositions, a conflict, an unsent irreversible: the
options the ritual already produces. The carrier grows an `options` list so
the digest can emit them rather than the agent recomposing them.

## Consequences

- `mdllm session-start`: the cue line becomes a prompt block per open item —
  options, recommended first, skip last.
- `type: cue` and its template gain `options` (recommended first) and a
  `recommendation_reason`; the mechanical raise fills the two verdicts and
  leaves the recommendation to whoever answers by citation.
- `closed-loop-operating-state` Phase 3: the presentation half is ruled;
  the assembly half — one view over cues, conflicts, options, irreversibles
  — stays that phase's open gap.
- Not built in this sitting: the raise and the loop heal came first; the
  digest's prompt block follows once the tick has produced the first
  machine-raised cues to render.
