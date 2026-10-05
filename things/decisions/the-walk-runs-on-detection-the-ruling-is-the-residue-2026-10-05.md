---
id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
type: decision
status: made
version: 1.0
created: 2026-10-05
session: 2026-10-05
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [change-reconciliation, walk, cue, seat, seat-protocol, commit-boundary, harness, prompt, closed-loop, integrity]
informed_by:
  - id: the-verdict-is-asked-where-the-change-lands-2026-10-05
    commit: 3c59f9cf8b77c681c159fd9756b4e6686f4cb518
  - id: change-reconciliation-specification
    commit: 54e906dcad0955857c3a086d076c4dbe7e6a8284
  - id: cue-carrier
    commit: 54e906dcad0955857c3a086d076c4dbe7e6a8284
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: e0fb483b2bed72edcb69f36a3e9fc56e900813d9
  - id: unattended-cue-carrier-2026-09-12
    commit: 2b12791fcfb2d6eb6c3f971bf444169667fb0815
linked_things:
  - id: the-verdict-is-asked-where-the-change-lands-2026-10-05
    relation: supersedes
    notes: "Same day, same operator, corrected on the problem statement: that ruling put the human at the front of every change, asked for a verdict only the walk can give. This puts the walk first and the human on the residue. What survives of it is carried here: the commit boundary as the actor, the harness's own prompt as the carrier for a decision, the unattended rule."
  - id: a-preserved-question-is-not-a-done-walk
    relation: references
    notes: "The diagnosis this rules on: five mechanisms preserved the cue question, none walked; 1,250 domain commits in six weeks, zero walks."
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: references
    notes: "The principle this finally makes operative: the pass at the change was doctrine with no actor, so consistency was in practice maintained by sweeps, late."
  - id: framework-agent-closes-settled-cues-2026-09-13
    relation: extends
    notes: "That granted the agent the verdict on settled questions, in the framework root; this grants the agent the walk itself, on detection, in every domain, within four bounds — the same move one step earlier."
  - id: unattended-cue-carrier-2026-09-12
    relation: references
    notes: "Unchanged: an unattended run assimilates and files; it applies nothing."
  - id: a-remembered-step-is-a-missing-actor
    relation: references
    notes: "The walk was a remembered step. This gives it an actor."
  - id: change-reconciliation-specification
    relation: informs
    notes: "The Driver Names The Inflection becomes The Walk Runs On Detection; the driver names the residue."
  - id: cue-carrier
    relation: informs
    notes: "Phase 7, corrected: the gate demands the walk's record, not the operator's verdict."
---

# Decision: The Walk Runs On Detection; The Ruling Is The Residue

## Context

The reconciliation pass — cue, assimilate, walk, seal — was specified in June
with a human cue: the driver declares an inflection and the agent runs the
pass. The record as it stood at 3.46.0 says what that produced. In the six
weeks from 26 August, roughly 1,250 commits landed across fifteen domain
repositories; the declaration count was zero; the pass ran nowhere but the
framework root, where the agent had been granted the verdict on settled
questions and closed 83 of 125 cues by citation. Every backstop built since —
the commit advisory, the cue thing, the mechanical raise, the digest line, the
retrospective's scan 4 — preserved the *question*; none did the *walk*. Two
live domains carried 184 and 146 unraised subjects; a third had nine cues its
agent raised that nobody answered in fifteen days. The drift the record itself
attributes to unwalked change surfaced late, through sweeps and accidents: a
44-commit contradiction between a skill and its schema, a 59-file repair, five
stale restatements found by a cold read.

A ruling made earlier the same day
(`the-verdict-is-asked-where-the-change-lands-2026-10-05`) had answered the
wrong half of this: it moved the question to the commit boundary and gave it
the harness's own prompt, and still asked the human first — for a verdict
that only the walk can give well. The operator corrected it on the problem
statement.

## The Ruling

The operator, 2026-10-05:

> "I wanted a way that if you ask for something to be changed, the walk
> would happen automatically for change reconciliation — because inherently
> the mechanics, the floor, can detect the change, and the walk means that
> your change affects something else. My hope was that this would now be an
> active action that happens on every change of everything, to keep the
> integrity and cohesiveness of the domain up to date."

> "Sometimes the walk just happens and it can all be mechanically figured
> out. I've done change reconciliation before where I say this is the
> inflection point, and it goes away and does the change and the dark region
> walk and everything — and actually there's nothing for me to rule on. But
> there are sometimes when there are decisions, and this is why it couldn't be
> automated. My suggestion was: why doesn't *that* decision surface in the way
> I described?"

> "This is the thing I'm trying to create: the domain is the ability to
> reason from a record. The mechanics of something auditable, in a system
> written not 100% in code but in specifications an LLM agent can read — specs
> that can be fixed, understood with complete clarity — and the system itself
> can metabolise things coming in, let things go, and keep itself true to the
> reality of things."

**The walk runs on detection, by the agent, within four bounds. The human
rules only on what the walk cannot settle.** A definition surface changes;
the floor sees it; the agent in the session runs the pass there and then —
touchpoints, each dependant judged, revisions in the same commit, derived
surfaces regenerated — and records the walk in the cue. Only a touchpoint the
agent may not settle reaches the operator, through the harness's own
multiple-choice prompt, with the concrete alternatives as its options. Most
walks end with nothing to rule on. That is the point.

## The Four Bounds

The reason the pass was never automated was churn — cascade through the
graph, and an agent rewriting meaning it does not hold. The operator and an
agent had decided that together once, and it was right as a bound and wrong
as a veto: the alternative to bounded churn was not no churn but no walk.

1. **Scope.** Definition surfaces only: the types that exist to be reasoned
   from (`specification`, `skill`, `guide`, `manifesto`, `prompt`,
   `workflow-definition`, `insight`, `decision`). A data thing reasoned from
   by fan-in — a register, a requirement — does not trigger a walk; it stays
   with the digest and the retrospective's net.
2. **Depth and kind of edit.** One hop: the declared and literal dependants
   of the changed thing. The agent revises on its own only at restatement
   level — a name, a path, a count, a reference, a regenerated block. A
   revision that would change a dependant's meaning, or a dependant that
   contradicts the change, is a question for the operator. That line is the
   spec's own line between knowing and pattern-following.
3. **Rate.** One walk per subject per day. Autocommit saves every write; the
   gate walks the first commit of a subject in a day and the agent judges
   whether a later edit the same day is material enough to walk again.
4. **Attendance.** An attended session walks. An unattended run assimilates
   and files: it writes the cue with the touchpoints and the proposed
   revisions and applies nothing (`unattended-cue-carrier-2026-09-12`).

## What This Settles

- The cue's verdict records the walk's outcome; it is no longer a permission
  asked before it. `inflection` means a dependant was revised or a ruling
  given; `not-inflection` means every touchpoint held as written. Either way
  the body names each touchpoint with its verdict — the audit trail the
  operator asked for.
- The commit boundary is still the actor (what survives of the superseded
  ruling): where a harness projects the `pre-commit` moment, the commit is
  refused until the walk is on record. The refusal's instruction is the walk,
  not a question.
- The residue reaches the operator through the native prompt, one question
  per unsettled touchpoint, the alternatives as options, *defer to the seat*
  always among them.
- What the record proves: the commit carries the walk. What it cannot prove:
  that the agent read what it marked consistent. The retrospective's scan 4
  samples that, and every revision is a visible commit.
- Where no harness projects the moment (a Codex seat, a hand commit), the
  `candidates` advisory and the digest remain, and the git-level refusal is
  still a separate flip, not taken.
