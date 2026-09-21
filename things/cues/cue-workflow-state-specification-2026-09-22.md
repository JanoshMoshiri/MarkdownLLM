---
id: cue-workflow-state-specification-2026-09-22
type: cue
status: answered
version: 1.0
created: 2026-09-22
subject: workflow-state-specification
raised_at: dc673b5e41755511c47f0a98e7b97e9f6bd52aaf
raised_by: "agent — the standing-watch Phase 6 session of 2026-09-22, under framework-agent-closes-settled-cues-2026-09-13; raised in the commit that made the change"
verdict: inflection
verdict_reason: "A reserved type's membership semantics were defined where before only its provenance direction was. Ruled by the operator (run-membership-is-realisation-2026-09-22): membership is function, not origin. The walk found the live corpus already conformant and no dependent reasoning from the old reading."
informed_by:
  - id: framework-agent-closes-settled-cues-2026-09-13
    commit: dc673b5e41755511c47f0a98e7b97e9f6bd52aaf
linked_things:
  - id: run-membership-is-realisation-2026-09-22
    relation: derived-from
    notes: "The ruling this cue's verdict cites. Born in the same commit, so it is linked rather than pinned; the pin above names the standing authority under which an agent may close a settled cue."
tags: [cue, standing-watch, substrate-native-a2a, change-reconciliation, workflow-state, membership]
---

# Cue: `workflow-state-specification` was modified — inflection?

## The Change

Version 0.7 → 0.8. Under *Activation and Fulfilment*, a **Membership**
paragraph: a thing that is a run's realisation declares it with
`linked_things: {id: <run>, relation: implements}`, and that edge is what the
floor reads for a run's members. Explicitly distinguished from `informed_by`
naming the run, which stays provenance. A Division-of-Labour row for the read.
The *Blocked-ness* paragraph now points at "its members" where it said "the
work things the run coordinates".

## The Question

Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer

**Inflection.** Before this change the spec said how a run's *outputs* were
attributed (`informed_by`) and never said what a run's *members* were. It
referred to "the work things the run coordinates" without defining the
edge. A consumer needing that set — the standing watch's scope — had two
candidate edges and no ruling. Now there is one edge and a ruling, and the
ruling encodes an ontology: membership is what a thing *does* for the run,
not where it *came from*. That is a definition surface, not an expression.

The competing reading — *the domain was already doing this, so nothing
changed* — is true of the domain and false of the spec. Recorded so the
verdict is visibly chosen.

## The Walk

Seventeen declared inbound edges and two literal references, walked at
`dc673b5`. The question at each: does it reason from run membership, or from
the `informed_by` direction, in a way the new paragraph contradicts?

- **`standing-watch-specification`** (`complements`) — the consumer that was
  waiting. Its Scope section stated this exact precondition; it is amended in
  the same arc (0.1 → 0.2) to read the settled edge. **Edited.**
- **`substrate-native-a2a`** (`extends`, `informed_by`) — Phase 6's first
  checkbox *is* this reconciliation. **Edited** (checkbox and one corrected
  line).
- **`between-sessions-surface-is-real-2026-09-21`** (`references`,
  `informed_by`) — that ruling named the debt and said "this ruling does not
  pay it". Still true as written; the paying is a separate decision it now
  has an inbound edge from. **Holds.**
- **`coordination-claim-specification`** (`complements`) — `held_by` on a run
  is unaffected by how members are declared. **Holds.**
- **`operating-model-specification`** (`extends`) — composes over runs as
  demand instances; says every demand is "instanced as a run" and outputs
  carry `informed_by`. That is the provenance direction and remains true.
  It does not reason about membership. **Holds.**
- **`universal-workflow-methodology`** (`implements`) — the seven stages and
  two shapes; no claim about how artefacts attach to runs. **Holds.**
- **`substrate-floor-development`** (`implements`) — a plan; references the
  spec as a floor target, not its membership semantics. **Holds.**
- **`review-independent-operating-model-2026-08-26-codex`** (`validates`) —
  an external review of the operating model's shape; predates runs carrying
  members at all. **Holds.**
- **`workflow-run-is-the-decomposition-principle-applied-to-processes`**
  (`informs`) — the originating insight: definition and run are two things.
  Membership is a third relation it never needed to name. **Holds.**
- **`cross-domain-handoff-is-verified-external-input`** (`informs`) — about
  imported definitions and pins. **Holds.**
- **`structural-pointers-need-reverse-edge-indexing`** (`informs`) — argues
  singular structural pointers need reverse indexes. Relevant in the
  negative: this ruling deliberately did *not* mint a singular `run:` pointer
  (Option 4 in the decision), so no new reverse index is owed. **Holds, and
  its reasoning was applied.**
- **`a-check-is-only-as-trustworthy-as-who-controls-its-inputs`**,
  **`a-transcribed-identifier-is-unverifiable-by-reading`**,
  **`an-advisory-is-scoped-by-who-can-perform-its-remedy`** (`informs`) —
  all about pins and advisories on runs. **Hold.**
- **`cue-workflow-state-specification-2026-09-19`** (`subject`) — the prior
  cue, answered; its walk was of `stages[].actor`. **Holds.**
- **Literal references** — the two generated indexes; rebuilt in this commit.

**The dark region** — what reasons about run membership *without naming the
spec*: the engineering domain's two loops and its design specs. Read directly
on 2026-09-21: both design specs attach to their runs by `implements` and
carry no `informed_by`. The ruling matches the practice. **Conformant as-is;
nothing to edit there.**

## The Seal

Sealed with two downstream edits (`standing-watch.md`, `substrate-native-a2a`),
both in the same arc. Remaining exposure is the ordinary one — the paragraph
reaches other domains on the next release through `domain-refresh.md`, and a
domain that attaches artefacts to runs some other way will learn from the spec
which edge the floor reads.

*Answered by the framework domain agent under
`framework-agent-closes-settled-cues-2026-09-13`, citing the operator's
ruling `run-membership-is-realisation-2026-09-22`. The operator may overturn
this verdict by editing it — the cue stays on the record either way.*
