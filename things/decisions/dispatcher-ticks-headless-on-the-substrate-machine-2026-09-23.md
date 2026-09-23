---
id: dispatcher-ticks-headless-on-the-substrate-machine-2026-09-23
type: decision
status: made
version: 1.0
created: 2026-09-23
session: 2026-09-23
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [dispatcher, closed-loop, retrospective, automation, headless, scheduled-task, seat]
informed_by:
  - id: closed-loop-operating-state
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
  - id: dispatch-design-2026-08
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
  - id: retrospective-cadence-is-a-dated-chase-2026-09-13
    commit: 446155b8936ef32de98af6d713d77a8700f4b4a2
linked_things:
  - id: closed-loop-operating-state
    relation: informs
    notes: "Phase 2's re-host: this is the host, and the shape of the tick."
  - id: dispatch-design-2026-08
    relation: extends
    notes: "Decision 1 there dissolved the central schedule; this keeps it and settles only where and how the one tick runs."
  - id: retrospective-cadence-is-a-dated-chase-2026-09-13
    relation: informs
    notes: "The unattended half of the retrospective was ruled to be the dispatcher's. This is the dispatcher it waited for."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: references
    notes: "Held: one hand-registered task is an install; a fleet of them would be the second brain. Widening still owes the generated, doctor-checked entry."
---

# Decision: The Dispatcher Ticks Headless, on the Machine That Holds the Substrate

## Context

The dispatcher — the actor for everything between sessions — was designed
in August (`dispatch-design-2026-08`), armed on the pilot in one harness's
scheduler, ticked twice, and was deliberately retired on 15 September so
that harness could concentrate on its own development. Since then the
retrospective's unattended half, the mechanical cue raise, and
`closed-loop-operating-state` Phase 4 have all waited on a host. The
2026-09-23 sweep found that every hole the operator feels in coherence is a
missing actor, not a missing check; this is the actor.

## The Ruling

The operator, 2026-09-23:

> "The dispatcher is going to run on the machine where the local files for
> the substrate live."

> "Then we don't need to rely on creating a scheduled task in the harness.
> You just go straight with the headless, which works better."

**One tick per machine, headless.** A scheduled task on the machine that
holds the substrate's working copies runs a plain shell command: compose the
launch with `mdllm dispatch-payload` and hand it to a harness's headless mode
(`claude -p`, `codex exec`). No application need be open; the harness need
only be installed, signed in under the task's user, and pre-trusted for the
tools the run uses. Which harness is a one-line choice in the task's
command.

**One tick walks the repos it holds; scope is a flag, not a second
dispatcher.** The design's default is the estate-wide walk — root plus every
domain — asking each repo's floor what is due and working them one at a
time under a claim. The August pilot was armed with a scope of one repo,
which is why it read as "one dispatcher per domain". It was one tick,
narrowed. Widening is `--scope`.

## Options weighed

1. A scheduled task inside a harness (the retired shape). Ties the tick to
   that harness's scheduler and to that application running; the reason it
   was retired.
2. A cloud routine that assembles the estate fresh from the private repos
   under a token (`mdllm assemble`). Viable, and the only route when no
   machine holds the files; it adds a standing token and a second copy of
   every repo. Not chosen while a machine does hold them.
3. **A native scheduled task launching a headless harness on the substrate
   machine.** Chosen: it is the August design's own line ("invoke the
   harness headless"), it needs no application open, and every prerequisite
   is a grant the operator already understands.

## What stays the operator's

The task registration and the trust grant for the run's tools. One
hand-registered task is an install; any second seat owes the generated,
doctor-checked task entry the design named, so the fleet never becomes a
hand-maintained second brain.

## Consequences

- `tools/dispatch/tick.ps1`: the tick's one command, with a per-clone lock,
  a log under `.git/`, and the harness as a parameter.
- `closed-loop-operating-state` Phase 2 gains 2c (the re-host); Phase 4's
  first hands-off cycle becomes possible; `cue-carrier` Phase 6's dispatch
  half becomes possible.
- The 2026-09 retrospective chase (13 October) is the first ritual the tick
  should draft.
