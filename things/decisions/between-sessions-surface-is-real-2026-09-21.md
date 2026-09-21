---
id: between-sessions-surface-is-real-2026-09-21
type: decision
status: made
version: 1.0
created: 2026-09-21
session: 2026-09-21
decided_by: Janosh Moshiri
confidence: high
origin: stated
tags: [standing-watch, between-sessions, seams, a2a, primitive, placement, watcher]
informed_by:
  - id: substrate-native-a2a
    commit: e0bc244da5572bfe6fef02cf32d0b962222f89e8
  - id: workflow-state-specification
    commit: e0bc244da5572bfe6fef02cf32d0b962222f89e8
  - id: a-mechanism-fails-at-its-seams-not-in-its-body
    commit: e0bc244da5572bfe6fef02cf32d0b962222f89e8
  - id: a-true-primitive-is-discovered-not-authored
    commit: e0bc244da5572bfe6fef02cf32d0b962222f89e8
  - id: transport-follows-corpus-holdability-not-distance
    commit: e0bc244da5572bfe6fef02cf32d0b962222f89e8
linked_things:
  - id: standing-watch-specification
    relation: informs
    notes: "The artefact this ruling authorises: the standing watch gets its own specification, the first in the between-sessions band, rather than a section inside workflow-state.md or orchestration.md."
  - id: substrate-native-a2a
    relation: informs
    notes: "The plan whose Phase 4 surfaced the fan-out defect. Its floor command stays untouched by this ruling; the scope half is recorded there as forward work, built only after the membership edge settles."
  - id: workflow-state-specification
    relation: references
    notes: "The scope of a watch is a run — that spec's own primitive, doing the job it was specified for. What this ruling does NOT do is amend it: the membership-edge disagreement is named here and left for its own reconciliation."
  - id: a-mechanism-fails-at-its-seams-not-in-its-body
    relation: implements
    notes: "The operator's own framing — 'the space between the seams is the new frontier' — is this insight taken one level up: the seam between sessions is where the framework has had no mechanism at all, and the watch is the first one that lives there."
  - id: a-true-primitive-is-discovered-not-authored
    relation: implements
    notes: "The test the ruling was held to. Every reducible part of the watch was named against its existing home before the irreducible residue — duration — was allowed to claim a spec."
  - id: phase-3-run-domain-task-reverted
    relation: references
    notes: "The boundary this ruling keeps: a standing watch is intra-domain turn-taking. Cross-domain agent invocation stays parked for its own deliberately-shaped channel."
---

# Decision: The Space Between Sessions Is Real, and the Standing Watch Is Its First Primitive

## Context

On 2026-09-21 the operator brought a report from the engineering domain's
agent: two clones of the two-agent specification loop on one machine collide,
because `spec-watcher.sh` keeps state and lock under `$HOME`, not under the
clone. The agent's diagnosis was correct on both counts it made — the paths
are per-machine, and `SPEC_DIRS` cannot separate two streams whose specs share
a directory — and its remedy was to patch the shell script with a `SPEC_MATCH`
regex.

Checked against the artefacts, the collision it diagnosed had already been
fixed two days earlier, in the floor: `mdllm watch` keys state and lock at
`<clone>/.git/mdllm-watch/<definition>.<role>.*`, per clone by construction
(`e0bc244`). But the *second* defect — every reviewer wakes on every stream's
turn — was real and identical in both artefacts. Neither had a notion of
scope. The question that opened was where the fix, and the watcher itself,
should be specified. The operator's standing instruction was explicit: *"I
don't want to just make primitives without having a proper think about where
they live."*

## Inputs Considered

- **`substrate-native-a2a`** — Phases 0–3 landed; the plan's own discovery test
  ("after it lands, there is nothing new an agent must do") and its refusals
  (no transport, no new type, no scheduled task, no third agent). Its Phase 4
  had not run a live turn; `spec-watcher.sh` was still armed alongside the
  floor command.
- **`workflow-state.md` 0.7** — `workflow-run` is "one live instance advancing
  through a definition"; `stages[].actor` was promoted on 2026-09-19 on its own
  stated condition. Its *Activation and Fulfilment* section specifies run
  membership as `informed_by` naming the run.
- **The engineering corpus, read directly** — eight `workflow-run` things
  exist, two of which *are* the contended streams
  (`run-imst-instrument-library`, `run-imst-participant-capture-layer`), both
  instancing `software-development-lifecycle` at `current_stage: design`,
  pinned to `definition_commit`. Each design spec attaches to its run via
  `linked_things: {relation: implements}` — not `informed_by`.
- **`a-mechanism-fails-at-its-seams-not-in-its-body`** — every consequential
  defect of 2026-09-13 lived in a join, not a body; the backlog's admission
  question is "does this close a seam, or add a body?"
- **`a-true-primitive-is-discovered-not-authored`** and
  **`transport-follows-corpus-holdability-not-distance`** — the razor and the
  governing constraint.

## Options

1. **Patch `spec-watcher.sh` with `SPEC_MATCH`** (the engineering agent's
   recommendation). Twenty lines; makes four clones work today. Rejected: the
   plan has the script slated for retirement *after* the floor command beats
   it, and already records the duplicated role table as a carried defect. A
   patch deepens exactly that duplication, and lands it in bash — the half of
   the loop the GPT-side instance cannot run under a Codex managed shell.
2. **A `--match` flag on `mdllm watch`.** Operational, not declared: a turn
   rule held in a shell invocation rather than in the substrate — the exact
   class the loop's own v1.8 was written to stop. Rejected as the *shape* of
   the scope, though a flag may still be how the scope is *invoked*.
3. **Specify the scope inside `workflow-state.md`, the watcher inside
   `orchestration.md`, and leave the watch's operational contract in
   `docs/`.** The strongest case against a new spec: the board is
   `stages[]`, the role is `stages[].actor`, the wake condition is a
   dependency trigger, "real on the remote" is already in the git-workflow
   kernel, the claim is `coordination-claim.md`. A watcher spec would restate
   four others — the drift failure the framework keeps paying for.
4. **Its own specification.** On one ground only: the watch is the first
   framework mechanism that runs while no session does. Every other surface is
   invoked and exits. `orchestration.md` specifies *moments*;
   `workflow-state.md` specifies *state*; neither has a home for *duration* —
   liveness, blindness, restart without re-baselining, single-instance, and
   the wake as an exit. Those five decisions are not restatements of anything;
   they are the semantics of a process that outlives the thing that started
   it, and they currently survive only as docstrings.

## Decision

**Option 4, ruled by the operator.** In his words: *"The space between the
sessions … is most definitely real … I definitely think it needs its own
spec. And I think it's the first of many other specs that will sit in the
space between the domains."*

Three consequences were settled with it:

- **The spec is named for the primitive, not the command.** `standing-watch.md`
  — *standing* in the framework's established sense (standing bindings, the
  standing dispatch prompt, standing authority: persists, always-on, not
  per-session). The body positions it as the first specification of the
  between-sessions surface, so that the band exists for the specs the operator
  expects to follow it.
- **The scope of a watch is a run.** Not a regex, not a new field. The two
  streams are two `workflow-run` things already; the artefacts already declare
  membership; the run already carries the definition pin and the coordination
  claim. A run-scoped watch inherits all three. This is the "vertical
  concurrency" the operator named: one run walks a subject through its layers;
  many runs walk many subjects; a watch follows one.
- **The floor is not touched this session.** The watcher is live on current
  work. The spec records the scope as the direction and names its precondition
  — the run-membership edge is specified one way (`informed_by`) and used
  another (`linked_things: implements`), and a filter built before that
  settles reads whichever edge its author happened to pick. The build waits on
  that reconciliation and is recorded as forward work on `substrate-native-a2a`.

## Consequences

- `standing-watch.md` is born `draft` and enters the catalog, the routing
  table, the sentinel, the tool's spec list and the framework map. It matures
  to `evolving` when Phase 4 of `substrate-native-a2a` crosses one real turn
  through the command with no human relay.
- The engineering domain runs the topology the loop already assumes — two
  writers, one reviewer, three clones — until the scope lands. That is the
  engineering agent's own first option, and it works today with no code.
- `workflow-state.md` owes a small reconciliation: which edge is run
  membership. This ruling names the debt and does not pay it.
- The between-sessions surface is now a named place. What the operator called
  "the space between the seams" has a spec standing in it, which is the
  difference between a frontier and a map.
