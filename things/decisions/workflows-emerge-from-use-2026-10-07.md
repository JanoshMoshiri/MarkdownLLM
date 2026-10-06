---
id: workflows-emerge-from-use-2026-10-07
type: decision
status: made
version: 1.0
created: 2026-10-07
session: 2026-10-05
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [workflow, workflow-definition, workflow-run, carrier, emergence, reckoning, repeatability, organic, floor]
informed_by:
  - id: workflow-state-specification
    commit: 67d236571a3676215e0da63563d59532f997bdf8
  - id: the-reckoning-is-the-digestion-beat-2026-10-05
    commit: 9b58abb27f1ec94f4f2151138d1673d925da4ba6
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    commit: 69dade015b2d6114c706d8539dfb58434e11e488
linked_things:
  - id: workflow-state-specification
    relation: informs
    notes: "Carrier binding and the emergence lifecycle are written into the spec that owns definitions and runs."
  - id: the-reckoning-is-the-digestion-beat-2026-10-05
    relation: extends
    notes: "The other half of the workspace learning: the reckoning lets go of what stopped being used; this locks in what keeps being done. An inferred workflow nothing moves through is dissolved by the reckoning."
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    relation: references
    notes: "The same split: the floor detects and assembles, the agent acts within bounds, the operator rules only on the residue."
  - id: workflows-emerge-from-use
    relation: informs
    notes: "The plan that builds it."
---

# Decision: Workflows Emerge From Use

## Context

Every workspace has one workflow skill and most have none of their process
written as data. The estate read of 2026-10-05 found the opposite of what that
suggests. Where a workspace carries volume, the process exists: the busiest
live domain moved its specification documents through draft, review,
cleared, ruling and approved 255 times across three types, and ran a ticket
loop between two agent seats 74 times in three days. A second domain moved
documents through working, discussion, agreement and export; a third moved
projects through scoping, designing and building. None of these was written
down as a workflow, or it was written down and never instanced. Of 25
explicit runs that moved more than once, 16 made every move on one day, as
bookkeeping after the fact. Three definitions written from observed practice
got no run the next time that work happened. Seven quieter workspaces showed
no repeated process at all, and their retrospectives said so.

## The Ruling

The operator, 2026-10-05:

> "How do we automate the development of the workflow through the work that's
> done, without having to define it? Being a software developer I will
> consider how to pragmatically approach a task and then I might create a
> workflow. In most cases, you can see from the evidence that I don't. I just
> scaffold a domain and I start working. I work in my workspace. And that's
> what I want: usability from a user perspective, for them to pick it up and
> just work, not have to worry about it. The intelligence is in the record of
> what happens, and the accumulative record gives us the ability to act on
> evidence. There are consistent patterns of usage that, in my vision of
> this, don't need to be explicitly defined by the operator. They're
> implicitly defined through usage."

The operator, 2026-10-06:

> "I think it should be completely organic. I think the user shouldn't even
> have to notice that a workflow has been generated. If you keep just working
> in the same way again and again, that's just the way you work. But the
> reason it's sensible for it to be turned into a workflow is so that when the
> LLM is going over that process again and again, they just follow the same
> steps. It's repeatable. There's less interpretation that has to be done and
> less variability, because it's set as steps. So it can be followed, maybe
> even with a more simple model. If somebody wants to create a workflow
> themselves, they're going to craft it in their own way and consciously go
> into it, and that is still going to be left open."

And on the shape, 2026-10-07: "That sounds perfect. Let's turn it into a
spec. Make it durable, make it repeatable. Encode it."

**Workflows emerge from use, organically, and the work is the run.** The
floor mines the record for a path that things of one type keep travelling;
the agent writes the workflow from it, marked as inferred, without asking
anyone. The workflow binds to the type the work travels through, so every
thing of that type is a run by construction and nothing has to be created or
advanced by hand. The agent follows the workflow's steps whenever it works on
that type, which is the repeatability the operator wants. When practice
leaves the path the agent revises the workflow; when nothing moves through it
any more, the reckoning lets it go. An operator who crafts a workflow
deliberately keeps it as theirs: the agent follows it and never rewrites it.

## The Two Lines

Organic does not mean quietly weakening control.

1. **The agent never invents a human gate and never removes one.** A stage
   where the operator approves or rules stays a stage marked as theirs. If
   practice skipped it, the workflow keeps it and the skip shows as a
   departure.
2. **An inferred workflow never replaces an authored one.** Two definitions
   bound to the same type is a contradiction the floor refuses; a departure
   from a workflow the operator wrote is the operator's to rule on.

## Consequences

- `workflow-state.md` gains *Carrier Binding* and *Workflows Emerge From
  Use*: the `carrier` field, runs derived from the carrier's status, the five
  beats (emerge, bind, follow, evolve, dissolve), authored and inferred.
- The floor gains `mdllm workflows`: definitions with their derived runs and
  departures, and with `--emergent` the candidates the record supports, with
  evidence, and an honest none where there is none.
- The reckoning gains the workflow kind: an inferred workflow nothing has
  moved through is dissolved; an authored one is asked about.
- The workspace's entry file carries a generated block naming which
  workflow to follow for which type, so the following does not depend on the
  agent remembering to look.
- Built by `workflows-emerge-from-use`, Claude Code first.
