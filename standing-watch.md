---
id: standing-watch-specification
type: specification
status: draft
version: 0.2
created: 2026-09-21
linked_things:
  - id: thing-specification
    relation: extends
  - id: workflow-state-specification
    relation: complements
    notes: "A watch reads a definition's stages and actor table, and its scope is a run. That spec owns all three; this one consumes them and adds none."
  - id: trigger-specification
    relation: complements
    notes: "The wake condition is a dependency trigger (`on: status_changed_to`). This spec adds a fourth evaluation surface — the remote ref, read continuously — not a vocabulary."
  - id: orchestration-specification
    relation: complements
    notes: "The sibling in the between-sessions band. Orchestration specifies moments; this specifies duration. The wake exit is the contract a harness-session adapter binds."
  - id: git-workflow-specification
    relation: complements
    notes: "'Turn-taking is publication, not commit' is that kernel's rule; the standing watch is the mechanism that reads the ref it names."
  - id: coordination-claim-specification
    relation: complements
    notes: "The claim half of turn-taking. Unchanged by this spec; a run-scoped watch reads the claim the run already carries."
  - id: session-memory-specification
    relation: complements
    notes: "That spec preserves knowledge across the gap between sessions. This one preserves process across it. Same gap, the other thing that has to survive it."
  - id: between-sessions-surface-is-real-2026-09-21
    relation: derived-from
    notes: "The ruling that gave this spec its own file rather than a section in workflow-state.md or orchestration.md."
  - id: substrate-native-a2a
    relation: implements
    notes: "The plan that built the command. This spec is the contract the build was carrying in docstrings."
  - id: transport-follows-corpus-holdability-not-distance
    relation: implements
    notes: "The governing constraint: nothing crosses a wire that git does not already send. The only thing on the network is the question 'has the head moved'."
  - id: a-true-primitive-is-discovered-not-authored
    relation: implements
    notes: "Every reducible part is named against its existing home before the residue claims anything."
  - id: hook-enforcement-has-three-anchors
    relation: implements
    notes: "The watch is git-fs; the wake is harness-session; adapters stay optional and interpretation is never promoted to enforcement."
  - id: portability-claims-need-execution-tests
    relation: references
    notes: "Why this spec asserts nothing about the PowerShell route until the GPT-side instance has actually been woken through it."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: references
    notes: "Why a watch never advances the turn it observes. The loop's stop condition belongs to the agent that acts, never to the process that woke it."
  - id: a-mechanism-fails-at-its-seams-not-in-its-body
    relation: informs
    notes: "The seam between sessions had no mechanism at all. This spec is the first one that stands in it."
  - id: a-filter-is-a-missing-instance
    relation: informs
    notes: "The Scope section is this insight's instance: two independent diagnoses reached for a filter, and the scope was a run that already existed unnamed to the mechanism."
  - id: mesh-safety-is-the-floor-not-the-topology
    relation: informs
    notes: "Qualifies the third irreducible. Peers-not-orchestrator is a real property of the shape, and what it buys is a distribution of human authority that holds only where the seat is reached by mechanism."
---

# Standing Watch

## What This Specifies

Every surface the framework has specified so far is **invoked and exits**. A
session starts, orients, works, ends. A hook fires at a moment. A prompt runs
once. The floor validates a candidate and returns. Nothing the framework
describes has, until now, existed *while no session does*.

This specification names that gap and the first thing that lives in it. A
**standing watch** is a process that runs between sessions, observes committed
state on the remote, and wakes an agent when a declared condition becomes true
there. It is the framework's first inhabitant of the **between-sessions
surface** — the space the operator called *"the space between the seams"* —
and this spec is written to hold the band open for the ones that follow.

`session-memory.md` already covers one half of what must survive the gap
between sessions: the knowledge. This covers the other half: the process. Same
gap, the two things that have to cross it.

The primitive is deliberately narrow. Almost everything a watch touches is
inherited; the proof it is genuine is how little it adds.

## Why It Is a Primitive (running the framework's own razor)

**Reducible — inherited, not reinvented:**

| Need | Primitive | Home |
|---|---|---|
| The board — which things are in play | `workflow-definition.stages[]`, matched against a thing's watched field | `workflow-state.md` |
| The role — who this watch wakes | `stages[].actor` | `workflow-state.md` |
| The wake condition | dependency trigger, `on: status_changed_to` | `trigger-specification.md` |
| The turn is real only on the remote | *"Turn-taking is publication, not commit"* | `git-workflow.md` kernel |
| Who holds the thing | `held_by` (+ `held_until`) | `coordination-claim.md` |
| Reading a corpus at an immutable revision | `RepositoryView.commit(root, revision)` | the floor |
| The scope — which stream this watch follows | `workflow-run` | `workflow-state.md` (see *Scope*) |

None of these is built by this spec. A watch is a *consumer* of every row.

**Irreducibly new — what earns primitive status:**

1. **Duration.** A watch outlives the session that armed it and precedes the
   session it wakes. That gives it a lifecycle no other surface has:
   liveness, blindness, restart, single-instance. The five decisions below are
   the semantics of that lifecycle, and they are not restatements of anything.
2. **The wake as an exit.** A watch does not *do* anything when the condition
   turns true. It records what it saw and exits. What rises on that exit is
   the harness's act — a background process re-invoking, a runtime's notify —
   and the framework's whole claim to being a substrate rather than a
   harness-specific tool rests on keeping that line exactly where it is.
3. **Peers, not orchestrator and child.** An orchestrator spawns and commands;
   the child exists by the parent's decision. Two watches ringing on the same
   ref are peers: neither wakes the other by command, each wakes on committed
   state. That is the difference between a tree and an organism, and it is
   the reason this is not a polling utility.

## The Two Channels

Turn-taking between two agent instances needs two channels, and the design
error the between-sessions surface exists to prevent is conflating them.

| | Message channel | Wake channel |
|---|---|---|
| Carries | what the turn says | *that* a turn happened |
| Wants | versioning, validation, audit, conflict resolution | liveness, low latency |
| Has | **git — already, everywhere** | **nothing durable; correctly so** |
| Loss is | a corruption | recoverable by re-polling |

Git is an excellent message channel and a poor wake channel. A wire is a poor
message channel and a fine wake channel. Build agent-to-agent over a wire as
the *message* channel and you discard everything the substrate gives you and
rebuild it worse. The wake channel carries no domain content at all — which is
why the security question collapses into "is the git remote secure", a
question already answered.

A standing watch is the wake channel, and only the wake channel.

## The Contract — `mdllm watch`

`mdllm watch <path> --role <actor> --definition <id> [--run <id>]
[--field status] [--remote origin] [--branch main] [--interval 60]
[--exit-on-wake] [--once] [--state <file>]`

**What it does.** Resolves the remote ref (`git ls-remote`) and, when the head
has moved, fetches and reads the corpus **at that commit** — never the
worktree, which is whatever the local session is mid-edit on, and a turn read
from it is a turn that has not happened yet. It builds the board (things whose
watched field sits at one of the definition's stages), diffs it against the
board it last saw, emits every change, saves state, and — if a change landed on
a stage this role acts at and `--exit-on-wake` is set — exits 0.

**What it costs when nothing moved.** One ref read. A ref is a single value
that is either fetched or not; there is no partial success to mistake for an
empty estate.

**The discriminator is the previous value, not the current one.** A thing
arriving at `draft` is an author creating it; `review → draft` is a reviewer
sending it back. Those are different events and only one is a turn.

**Arming refusals — the watch will not start if:**

| Refusal | Why it is a refusal, not a warning |
|---|---|
| The definition does not resolve, or is not a `workflow-definition` | A board with no stages is not a board. |
| The definition declares no `stages[].actor` | There is no role to wake for. |
| `--role` names no declared actor | The watch could never wake. |
| No declared status vocabulary contains this role's wake stages | The definition's stage ids and the watched field's vocabulary disagree (`reviewing` against a vocabulary that says `review`). **This watcher polls forever in silence, which is indistinguishable from a healthy estate** — the failure the loop fears most. Checked against the *declared* vocabulary, never against values things currently hold: a reviewer arms precisely when nothing is at `review` yet. |
| Another instance of this role on this definition is live in this clone | See decision 1 below. |

A reserved type never appears on a status-keyed board: a `workflow-definition`
sitting at `draft` would otherwise land on the board of a loop whose first
stage is also `draft` — including its own. A tool-owned lifecycle is never a
domain's turn token.

**Exit codes are the harness contract.**

| Code | Meaning | What a harness bound to `--exit-on-wake` should do |
|---|---|---|
| `0` | This role's turn (or `--once` completed quietly) | Rise. |
| `1` | `--once` and the poll failed | Report; do not rise. |
| `2` | Refused to arm | Fix the declaration; do not rise. |
| `3` | Already watching this role in this clone | Do nothing — the other instance is the watch. **Not 0**, because a harness re-invoking on exit would otherwise wake an agent for a doorbell that never rang. |

**What it never does.** It never writes, never commits, never resolves a
divergence, and never advances a turn. It reads a ref, reports a change, and
exits. The turn stays the agent's act and the ruling stays the human's.

## The Five Inherited Decisions

Each was paid for by a defect in the domain that found it first. They are
carried, not re-derived, with the failure each prevents named at its site —
because a rule whose reason is lost is a rule the next author deletes.

| Decision | Failure it prevents |
|---|---|
| **State, lock and log are keyed per clone, per definition, per role — never shared.** They live under `<clone>/.git/mdllm-watch/`, because they are per-clone, never committed, and disappear with the clone they describe. | Eight orphaned instances raced on one state file under `$HOME`, each absorbing the others' events; the live one saw nothing change and stayed silent. Two clones on one machine collided the same way. |
| **Single-instance per (definition, role, clone) — a live pid lock, keyed exactly as the state is.** A lock whose process is gone is stale and is taken. | State isolation stops two *different* roles colliding; it does not stop two instances of the *same* role. These are two guarantees, not one, and the second was the one actually hit. |
| **Wake after state is saved, never from inside the diff loop.** Record, then signal. | The first version exited from inside its loop, so the poll that woke the reviewer never persisted what it had seen, and every restart re-detected the same change — an infinite wake loop. |
| **A restart resumes from persisted state; it never re-baselines.** | A change that landed while the watch was down must be *reported*, not absorbed — otherwise the one event the channel exists to carry is the one it silently eats. |
| **A failed poll is an emitted event. A board read that loses more than a threshold of entries in one poll is a bad read, not an empty board.** The guard is the *threshold*, never emptiness alone: a one-thing board emptying is a departure, reported as `GONE`. | A blind watcher that says nothing is reporting health it cannot see. A list endpoint once returned fifteen rows then seven under a success status; a corpus scan can do the same for a less exotic reason. *(The scope refined this on 2026-09-22: an earlier form also refused any populated→empty read, which silenced the one event a one-member run-scoped board exists to carry.)* |

Once armed, failures are **emitted, never raised** — a watch that exits on a
failed poll is indistinguishable from a quiet estate.

## Scope — A Watch Watches a Run

*Specified here as the direction. Not yet built; see Maturity Path.*

A definition can be running in more than one stream at once — two subjects, one
loop. A watch scoped to the *definition* sees every stream's board as one
board, so a reviewer armed for one subject wakes on the other's turn, and two
reviewers armed for two subjects both wake on both. That fan-out was found in
the field on 2026-09-21, and it is real in the floor command exactly as it was
in the shell script it replaces.

The scope is not a new field and not a filter pattern. It is the run.

```
                    ── horizontal: the turn ──▶
                    draft → review → cleared → ruling → approved
                    (the loop definition, on the artefact's watched field)

  │  requirement ─── <subject>-requirement     [approved]
  │
ver│  design ──────── <subject>-design          [review]   ◀── this watch
ti │
cal│  test ────────── (not yet)
  │
  ▼  (the lifecycle definition, on run.current_stage)
```

**Horizontal** is the turn: one artefact at one layer, passing between roles.
**Vertical** is the run: one subject walking its layers, pinned to a definition
revision, carrying its claim. A watch follows one run. That is what makes
concurrency work in both directions — many runs, each with its own watch pair,
none of them hearing the others' doorbells.

**The run and the definition are two different definitions.** This is the
point, not a complication. `--run` names the vertical — a run of the
*lifecycle* definition, a subject at `design` on its way to `test`. `--definition`
names the horizontal — the *loop* whose stages are the turn tokens on the
artefact. A watch reads the horizontal's stages for the vertical's members.
The floor therefore does **not** check that the run instances the watched
definition; it usually will not, and refusing would refuse the topology the
scope exists for. It checks only that the run resolves and is a
`workflow-run`.

**Membership is one edge.** A thing is on a run's board when it declares
`linked_things: {id: <run>, relation: implements}` — *I am this run's
realisation* (`workflow-state.md` → Activation and Fulfilment → Membership;
ruled in `run-membership-is-realisation-2026-09-22`). Not `informed_by`: that
says where a thing *came from*, and a thing produced under one run can be the
realisation of another. Membership is function, not origin. No new field on the
artefact, no tag convention, no regex — the live domain already declared it
this way before the spec asked.

Two things fall out for free when the scope is a run, and one that first
looked free was not:

- **The claim.** The run carries `held_by`. The watch is looking at the thing
  that already knows who holds it.
- **The isolation.** State and lock are keyed on the run as well as the
  definition and role, so two reviewers on two runs in one clone are two
  watchers — the same collision the per-clone keying prevents, one axis over.
- **Not the pin — or not the way it first read.** The run's `definition_commit`
  pins the *lifecycle* it instances, not the loop the watch reads stages from.
  A horizontal watch reads the loop at the remote head like everything else.
  Only a *vertical* watch — `--field current_stage --definition <lifecycle>`,
  a single-thing board that is the run's own cursor — reads the definition
  the pin governs. Building the scope is what corrected the draft's first
  claim; that is what `draft` is for.

**Leaving a run is an event.** A thing that stops declaring it realises this
run leaves this watch's board, and the `GONE` line fires exactly as it does for
a deletion — deleted, renamed, or moved off this definition *or run*. The
watch for the run it moved *to* sees it arrive.

## Division of Labour: Floor vs Agent

| Check or act | Owner | What |
|---|---|---|
| Resolve the definition; require declared actors; require this role among them | **floor** (arming) | Referential integrity over declared data. A watch that could never wake is a startup Error, not a running silence. |
| Wake stages ∩ declared vocabulary is non-empty | **floor** (arming) | The silent-forever guard. Against the *declared* vocabulary, never the observed values. |
| One instance per (definition, role, clone) | **floor** (arming) | Exit 3, never 0. |
| Read at the remote head, never the worktree | **floor** (running) | The turn is real on the remote or not at all. |
| Diff, emit, persist, then exit on this role's entry | **floor** (running) | Record, then signal — the ordering is load-bearing. |
| Rise on exit 0 | **harness** | The wake itself. `--exit-on-wake` is the contract; what rises is the adapter's act. Optional, and never the difference between the substrate working and not. |
| Take the turn — read the thing, do the work, move the token, publish | **agent** | Everything after the doorbell. The watch never advances anything. |
| Confirm the turn has *passed* — from the ref, never the local clone | **agent** | A commit can succeed while its push is rejected; the committing side then holds every local indication that it handed over while the other side sees nothing. An instance that cannot publish its turn is blocked and says so. |
| Rule | **human** | The loop exists to make one act better-informed, not to remove it. |

## What This Refuses

Inherited from the plan that built the command, and held here so the
refusals outlive the plan:

- **No transport.** No hosting, no tunnel, no MCP wire, no server. Nothing
  crosses a network that git does not already send.
- **No cross-domain agent-to-agent.** A standing watch is intra-domain
  turn-taking. Cross-domain live invocation is a different risk class from the
  read face, and the membrane that makes the face trustworthy does not cover
  it (`phase-3-run-domain-task-reverted`). When that leg is wanted it gets its
  own deliberately-shaped channel.
- **No new thing type for the turn.** The state already has a carrier. A
  separate handover thing would be a contended singleton across two clones —
  the one object in the design that must never diverge.
- **No scheduled task.** Every run born with permissions on manual, one hang
  blocking everything for a day, and tokens spent to say "nothing moved" — a
  sibling loop paid for that lesson.
- **No third agent to break ties.** Two agents can be confidently wrong
  together. The answer is the human, not a third model.
- **No advancing.** A watch that could move the token would be an orchestrator
  wearing a doorbell.

## Relationship to Other Specifications

- **`thing.md`** — a watch reads things; it creates none. It extends the atom
  only in the sense every extension spec does: it adds a way things are
  *consumed*.
- **`workflow-state.md`** — owns the board (`stages[]`), the role
  (`stages[].actor`), the scope (`workflow-run`), and since 0.8 the
  membership edge (`linked_things: implements`). This spec consumes all four
  and amends none.
- **`trigger-specification.md`** — the wake condition is a dependency trigger.
  That spec lists three evaluation points (session start, after every write,
  scheduled invocation); a standing watch is a fourth: continuous, on the
  remote ref.
- **`orchestration.md`** — the sibling. Orchestration specifies *moments* and
  the three anchors; this specifies *duration* and uses the anchors as given:
  the watch is `git-fs`, the wake is `harness-session`, and nothing here
  promotes interpretation to enforcement.
- **`git-workflow.md`** — "turn-taking is publication, not commit" is the rule;
  the standing watch is what reads the ref that rule names.
- **`coordination-claim.md`** — unchanged. The claim half of turn-taking; a
  run-scoped watch reads it, never takes it.
- **`session-memory.md`** — the other thing that crosses the gap between
  sessions. Knowledge there; process here.

## Maturity Path

The framework's reserve-but-draft ladder, at its first rung:

1. **`draft` — now.** The command exists (`tools/markdownllm/watch.py`), the
   contract above is what it does, the five decisions are carried in it, and
   the scope is built: `--run <id>`, tested against two runs of one loop with
   two reviewers that wake only on their own. The PowerShell route is asserted
   for nothing until a GPT-side instance has been woken through it.
2. **→ `evolving`** when `substrate-native-a2a` Phase 4 crosses one real
   writer → reviewer → writer turn through the command with no human relay.
   A field validated by one turn is not `stable`; it is `evolving`.
3. **The scope landed on 2026-09-22**, one day after it was specified as a
   direction — because the operator ruled the membership edge
   (`run-membership-is-realisation-2026-09-22`) and `workflow-state.md` 0.8
   carries it. Building it corrected the draft's pin claim (above). The
   four-clone topology is now real rather than nearly-real; whether it is
   *used* is the domain's call.
4. **The band fills.** This is the first spec of the between-sessions surface.
   The operator expects others. When a second one arrives, what they share is
   what this section should be rewritten to say — and not before, because a
   band with one member is a spec, not a band.

The engineering domain, meanwhile, runs the topology its loop already assumes
— two writers, one reviewer, three clones — which works today with no code.
