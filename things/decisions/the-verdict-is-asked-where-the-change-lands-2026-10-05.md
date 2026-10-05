---
id: the-verdict-is-asked-where-the-change-lands-2026-10-05
type: decision
status: made
version: 1.0
created: 2026-10-05
session: 2026-10-05
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [seat, seat-protocol, cue, change-reconciliation, commit-boundary, harness, prompt, closed-loop, attention]
informed_by:
  - id: open-questions-arrive-as-a-prompt-2026-09-23
    commit: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
  - id: unattended-cue-carrier-2026-09-12
    commit: 2b12791fcfb2d6eb6c3f971bf444169667fb0815
  - id: cue-carrier
    commit: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
  - id: change-reconciliation-specification
    commit: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
  - id: a-remembered-step-is-a-missing-actor
    commit: 68c83cee2b400b75c52f346c0506c01dfd273bb2
linked_things:
  - id: open-questions-arrive-as-a-prompt-2026-09-23
    relation: extends
    notes: "That ruled the shape of an open question at session start. This moves the ask to the moment the change lands and names the harness's own choice dialog as its carrier, because the digest's relay is passed over."
  - id: unattended-cue-carrier-2026-09-12
    relation: references
    notes: "Unchanged: an unattended run never answers. The gate makes it raise, which is the half that ruling left to instruction."
  - id: cue-carrier
    relation: informs
    notes: "Phase 7: the ask at the commit boundary. The carrier held the question; this is where it is put in front of the person."
  - id: change-reconciliation-specification
    relation: informs
    notes: "The Cue Persists gains The Ask: the verdict is asked where the change lands, through the harness's native prompt, and the commit waits for the cue."
  - id: a-remembered-step-is-a-missing-actor
    relation: references
    notes: "The ask had no actor at the moment of change: the digest listed, nobody asked. The gate is that actor."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: references
    notes: "Why a refusal in the tool's own channel and not a line in the digest: a refusal is read because the next move depends on it; a listed question is economised."
---

# Decision: The Verdict Is Asked Where the Change Lands, Through the Harness's Own Prompt

## Context

The cue carrier made the inflection question persist: a reasoned-from thing
changes, the floor computes the question from the commit stream, and the
session-start digest lists it until a human answers. On 2026-10-01 that list
read 172 unraised in one domain and 146 in another, with no verdict on any
of them since late August. The question was never lost. It was never *asked*.

The operator named why, from the seat, on 2026-10-05: the digest's relay is
not where decisions get made.

> "Session start happens. It doesn't really matter what session start says.
> I kind of carry on and just move on to whatever's important. The session
> start is more for me about the certainty that my domain agent is going to
> understand the read and write skills and its specification skill... I
> think it's not sensible to trust that relay that comes from session start,
> or even, even if it wasn't session start, even if it was mid-session, and
> you popped out with something and said it. I think it's less likely to be
> impactful and actually decided at the moment it needs to be."

And why the question cannot be heard in the words, only read off the change:

> "From my experience, when you're working, you don't announce an inflection
> point. You just say this needs to change in your mind. But you don't say
> that in those words. You just say, we need to do this now. This is how it
> needs to be. You can't semantically have a rule that will understand that
> as an inflection."

## The Ruling

The operator, 2026-10-05:

> "The problem is a change happens and the change reconciliation, the
> decision of it, the human in the loop needs to be pulled in at that point
> when the reconciliation happens, at the inflection point. That's when the
> human needs to say, yep, okay, this is the right shape, or no, this is how
> it needs to be. And at the moment, from my experience, it doesn't happen,
> even when it pops up. So could we have it the same way that Claude, or any
> one of the AI harnesses, pops up a multiple-choice decision? That's the
> most certainty we're going to be able to get in catching the user to make
> a decision on the state of something. It's only through that mechanism of:
> here's a decision, there's some options, or other."

**The cue verdict is asked where the change lands, through the harness's
own choice prompt, and the commit waits for it.** The floor detects the
change (a definition surface in the commit, no cue on disk) and refuses the
commit; the refusal tells the agent, in the tool's own channel, to put the
question to the operator through the native dialog, options first, with the
agent's recommendation marked and *file to the seat* as the explicit
deferral; the operator's pick is recorded in the cue, in their words, and the
commit goes through carrying it. Nobody has to remember, and nobody has to
read a list: the next move is blocked until the question is answered or
deliberately deferred.

## What This Settles And What It Does Not

- **Detection stays mechanical and structural.** The floor never reads the
  words; it reads the diff. The predicate is the one `candidates` and `cues`
  already apply, narrowed at the gate to definition surfaces (the types that
  exist to be reasoned from), because that is where "this is how it needs to
  be" lands. Data things that are reasoned from by fan-in stay with the
  digest and the retrospective's net.
- **The verdict stays the operator's.** `The Driver Names The Inflection`
  is untouched. The agent recommends, from what was just said in the room;
  the operator picks. An unattended run meets the same refusal and is told
  the other thing: raise the cue open and file it, never answer
  (`unattended-cue-carrier-2026-09-12`).
- **One ask per subject per day.** A cue on disk for the subject, raised
  today, covers the day's further edits to it; the fifth refinement of a
  skill in one sitting is not a fifth dialog.
- **What the record proves.** The commit carries the cue and the verdict
  with its reason. Whether the dialog appeared is in the harness transcript,
  not in git; the floor cannot verify a click. The refusal makes the ask the
  agent's critical path, which is the most certainty available, and the
  retrospective remains the net beneath.
- **Where it binds.** The gate is a harness lifecycle moment, so it exists
  where an adapter projects it: Claude Code today. A Codex seat or a hand
  commit keeps the git-level `candidates` advisory and the digest. Making
  the git pre-commit hook itself refuse is a separate flip, not taken here,
  because it would also gate every hand edit the operator makes.

## Consequences

- A third lifecycle moment, `pre-commit`, with a new delivery kind, `gate`;
  the Claude Code adapter binds it to a PreToolUse hook on the shell tools
  and translates a refusal into the harness's deny envelope. Its one step is
  `mdllm cues . --staged`; `--staged --raise` writes the open cue for the
  commit in hand, pinned to its parent.
- `cue-carrier` Phase 7 builds it; `change-reconciliation.md` gains *The
  Ask* beside *The Cue Persists*; the dispatch prompt's step 6 names the
  gate as what makes its raise-never-answer rule mechanical; the dispatcher's
  tick marks its launches unattended.
- `open-questions-arrive-as-a-prompt-2026-09-23` keeps its half: items that
  have no commit to land on (a drafted retrospective's dispositions, a
  conflict, an unsent irreversible) still arrive at session start as a
  prompt block. That block is still to build; this ruling takes the cue out
  of its queue and puts it where the change is.
