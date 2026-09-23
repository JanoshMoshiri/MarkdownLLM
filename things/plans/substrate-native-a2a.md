---
id: substrate-native-a2a
type: plan
status: in-progress
version: 1.5
created: 2026-09-19
priority: high
informed_by:
  - id: transport-follows-corpus-holdability-not-distance
    commit: cb1f86bd01866ffea2e5d4ce69cb18859272fe58
  - id: phase-3-run-domain-task-reverted
    commit: cb1f86bd01866ffea2e5d4ce69cb18859272fe58
  - id: workflow-state-specification
    commit: cb1f86bd01866ffea2e5d4ce69cb18859272fe58
tags: [a2a, workflow-state, turn-taking, watcher, harness-ports, discovery]
linked_things:
  - id: workflow-state-specification
    relation: extends
    notes: "Phase 1 fills the slot that spec already reserved: `stages[].actor`, on its own stated condition — two live modules needing automation to consume the modality."
  - id: standing-watch-specification
    relation: informs
    notes: "The spec this plan's Phase 2 was carrying in docstrings. Born 2026-09-21 as its own file — the first of the between-sessions band — on the ruling `between-sessions-surface-is-real-2026-09-21`. Phase 6 below is that spec's scope half, recorded here as forward work."
  - id: a-never-crossed-gate-hides-the-defects-behind-it
    relation: informs
    notes: "Phase 4's trigger asks exactly this insight's question — never armed, armed and never woke, or woke and hand-relayed — because a watch that has never rung cannot distinguish broken from never-run. Linked at session end 2026-09-22 so the razor stays live where it is applied."
  - id: coordination-claim-specification
    relation: references
    notes: "`held_by` is the claim half of turn-taking and needs no change. This plan touches only the wake half."
  - id: trigger-specification
    relation: extends
    notes: "The wake condition is a dependency trigger (`on: status_changed_to`). What is new is the evaluation surface — the remote ref — not the vocabulary."
  - id: git-workflow-specification
    relation: extends
    notes: "Phase 3 adds the turn-taking corollary of `publication makes it real to the estate` to the kernel block."
  - id: transport-follows-corpus-holdability-not-distance
    relation: implements
    notes: "The governing constraint. The wire buys nothing git has not delivered; this plan adds no transport and moves no domain content over one."
  - id: phase-3-run-domain-task-reverted
    relation: references
    notes: "The boundary this plan must not cross. Cross-domain A2A stays parked for a deliberately separate channel; this is intra-domain turn-taking only."
  - id: a-true-primitive-is-discovered-not-authored
    relation: supports
    notes: "Every element below already exists — in a spec's reserved slot, in a trigger vocabulary, in three bash scripts. Nothing here is a new mechanism; the plan names a spine and retires duplication."
  - id: closed-loop-operating-state
    relation: complements
    notes: "That plan's Phase 4 wants one full hands-off cycle at one radius. This loop is one, and will be evidence for it — but it is a different concern and keeps its own plan."
  - id: hook-enforcement-has-three-anchors
    relation: implements
    notes: "The wake is the harness's act, not the framework's. `--exit-on-wake` is the contract an adapter binds; the floor stays at git-fs and adapters stay optional."
triggers:
  - type: time
    condition: "2026-10-10 reached"
    action: "Has Phase 4 run one real writer/reviewer turn through `mdllm watch` in the engineering domain? If not, establish which: the command was never armed, was armed and never woke, or woke and the turn was hand-relayed anyway. The third is the interesting failure — it would mean the doorbell rings and nobody rises, which is a seat problem and not a channel problem. Re-date once answered."
---

# Substrate-Native A2A: The Turn Belongs To The Domain, The Wake Belongs To The Harness

## What This Is

Two agent instances take turns working one thing to completion. Today, in the
engineering domain of the regulated deployment, they do it well: the turn is a `status` field
the floor validates, findings live in separate working-documents, `held_by`
names the holder, and three bash watchers ring the doorbell. That loop was
ruled on 2026-09-19 (`two-agent-specification-loop` v1.0, engineering commit
`bf461896699c75db65cf0a832af661d67de619f8`) and its sibling
`two-agent-review-loop` has ten versions of scar tissue behind it.

This plan lifts the part of that which is **not** engineering's business into
the substrate, and leaves the rest alone.

**The operator's question that opened it** (2026-09-19): whether A2A wanted a
hosted MCP server reachable over a tunnel. Talking it through, he arrived at
the answer himself — *"if I just use the substrate as the communication
channel then I've got native A2A."* That is the right answer, and the record
had already reached it twice independently:

- `transport-follows-corpus-holdability-not-distance` (2026-08-08):
  *"Distance is already solved, at a different anchor... Reaching a peer's
  porch over the wire buys nothing that git has not already delivered — and it
  buys it at the git-fs anchor, which is the sturdier one."*
- `two-agent-review-loop` v1.4, quoted by its sibling:
  *"Any state machine built on a substrate it does not own inherits that
  substrate's definitions, not its own."* That loop was built on GitHub's
  primitives and moved off them for exactly this reason.

So the design question was never *what transport*. It was **which of the two
channels are we talking about** — and the loop conflates them nowhere, while
the operator's opening framing did.

## The Distinction This Plan Rests On

| | Message channel | Wake channel |
|---|---|---|
| Carries | what the turn says | *that* a turn happened |
| Wants | versioning, validation, audit, conflict resolution | liveness, low latency |
| Has | **git — already, everywhere** | **nothing durable; correctly so** |
| Loss is | a corruption | recoverable by re-polling |

Git is an excellent message channel and a poor wake channel. A wire is a poor
message channel and a fine wake channel. **Build A2A-over-a-wire as the
message channel and you discard everything the substrate gives you and rebuild
it worse. The wake channel needs no domain content on it at all** — which is
why the security question the operator opened with collapses into "is the git
remote secure", a question already answered.

## The Spine — What Already Exists

Nothing in this column is built by this plan.

| Need | Primitive | Home |
|---|---|---|
| The turn token | `status`, domain-declared vocabulary, floor-validated | `thing.md`; engineering's five values |
| Who holds it | `held_by` (+ optional `held_until`) | `coordination-claim.md` |
| The stage graph as data | `workflow-definition.stages[].to` | `workflow-state.md` |
| The wake condition | dependency trigger, `on: status_changed_to` | `trigger-specification.md` |
| Reading a corpus at an immutable revision | `RepositoryView.commit(root, revision)` | `repository_view.py` |
| Transport, multi-machine | `estate-sync` + `autopush` | `git-workflow.md` |
| The turn is real on the remote | *"publication (push/fetch) makes it real to the estate"* | `git-workflow.md` **kernel** |

That last row is the one worth pausing on. The specification loop rediscovered
it this morning under its own heading — *The handover is not the commit* — and
called it "the rule that has no analogue in the sibling and the one most likely
to bite first." It has an analogue: it is the first sentence of the
git-workflow kernel, which every session already loads at Tier 0. The domain
paid to learn something the substrate already knew, because the substrate said
it about *publication* and never about *turn-taking*. Phase 3 closes that gap
with one sentence.

## The Residue — What This Plan Actually Builds

Three things. Each passes the discovery test: after it lands, there is nothing
new an agent must *do*.

### 1. `stages[].actor` — the slot that came due

`workflow-state.md` already states the condition for this field's existence:

> Both stay proportionate prose in the body — **machine-readable modality
> fields enter only when at least two live modules need automation to consume
> them.**

Two live modules now exist, and **three bash scripts hardcode the role→wake
table** the spec said would become data at this point. The role is already
machine-consumed; it is consumed from a `case` statement in shell. The field
is a promotion of existing fact, not an addition.

Optional, back-compatible, floor-checked only where used: a `--role` must name
an actor the governing definition declares.

### 2. `mdllm watch` — one command, three scripts retired

The floor already evaluates triggers and already reads a corpus at an immutable
revision. `watch` is those two, plus three differences that are the whole point:

- it resolves the **remote ref** (`git ls-remote`) and reads at *that* commit —
  never the working tree, which is whatever the local session is mid-edit on;
- it **loops**, at a poll interval, and one ref read is the whole cost of
  "nothing moved";
- it **exits on this role's entry condition**, which is the contract a harness
  binds a wake to.

It inherits, unchanged, the five load-bearing decisions `spec-watcher.sh`
records — each paid for by a defect in the sibling:

- state, lock and log keyed per role, never shared (eight orphaned instances
  raced on one state file);
- wake **after** state is saved, never from inside the diff loop (an infinite
  re-wake loop);
- a restart resumes from persisted state rather than re-baselining (a change
  landing while down must be reported, not absorbed);
- a failed poll is an emitted event — a blind watcher is a finding, not a quiet
  estate;
- a board read that loses more than a threshold of entries in one poll is a bad
  read, not an empty board.

**Why it must be the floor and not a script.** The bash watcher runs in the
Anthropic session. The operator runs an Anthropic model and a GPT model taking
turns in the same domain — and the GPT side, under a Codex managed shell on
Windows, reaches the floor through `tools/mdllm.ps1`, not bash. **Half this
loop cannot currently ring its own doorbell.** That is the sharpest evidence
for the lift, and it is a portability fact, not a preference.

### 3. One kernel line

The turn-taking corollary of publication, in `git-workflow.md`'s kernel block,
regenerated into `kernel.md`. Tier 0, so every session in every domain meets it
before reaching for a channel — which is exactly what
`transport-follows-corpus-holdability-not-distance` is held `keep-active` to do.

## What Stays A Limb

Deliberately not lifted:

- **Engineering's five-state vocabulary** (`draft`/`review`/`cleared`/`ruling`/
  `approved`) and its wake text. That is the domain's declaration, ruled by its
  CTO, and the framework has no opinion on it.
- **`review-watcher.sh`.** That loop keys on GitHub's PR primitives by
  deliberate choice for the implementation stage. The spec loop is the
  substrate-native one; the dev loop is not, and should not be made so by this
  plan.
- **The wake itself.** `--exit-on-wake` is the contract; *what* rises on that
  exit is the harness's act — a Claude Code background process re-invoking on
  exit, a Hermes `terminal(background=true, notify=true)`. Adapters stay
  optional and the floor stays at `git-fs`.

## Route

- [x] **Phase 0 — Define it.** This document, committed before the first line
      of code. The durable-state protocol: plan in repo, per-change commits,
      the plan is the source of truth after compaction.

- [x] **Phase 1 — `stages[].actor`.** `workflow-state.md` 0.6 → 0.7; the field,
      its semantics, and the floor check that a named role resolves. Tests.
      *Done when:* a `workflow-definition` may declare actors, an undeclared
      `--role` is an Error, and a definition without the field is untouched.

- [x] **Phase 2 — `mdllm watch`.** The command, in its own module, registered
      in `cli.py`. Remote-ref resolution → `RepositoryView.commit` → trigger
      evaluation for one role → emit-on-change → optional exit-on-wake. Tests
      covering each of the five inherited decisions.
      *Done when:* `mdllm watch` reproduces `spec-watcher.sh`'s behaviour on
      the same board, from Python, on the PowerShell route.

- [x] **Phase 3 — The kernel corollary.** One sentence into `git-workflow.md`'s
      kernel block; `mdllm kernel` regenerated; `mdllm coherence` clean.
      *Done when:* Tier 0 carries the turn-taking rule and the generated kernel
      matches its source.

- [ ] **Phase 4 — Prove it on one real turn.** *In progress — the domain half
      landed 2026-09-19; the live turn has not run yet.*
      - [x] The stage/status disagreement reconciled, ruled by the CTO:
            `drafting → draft`, `reviewing → review`, `blocked` added to the
            three spec types' vocabularies. Loop v1.2, cued and walked
            (inflection; the one live run was checked and instances a
            different definition, which is what made a rename safe rather
            than a migration).
      - [x] `actor` declared on the specification loop, and all three roles
            arm against the real corpus with exactly the wake sets the loop's
            own watcher table documented — writer on `cleared|draft`,
            reviewer on `review`, CTO on `ruling|blocked`. The table now comes
            from the definition rather than from a shell `case` statement.
      - [ ] **One real writer → reviewer → writer turn** through `mdllm watch`,
            with no human relaying it.
      - [ ] The GPT-side instance woken through the PowerShell route — the
            portability claim that motivated the lift, and the one this plan
            must not assert until it is executed
            (`portability-claims-need-execution-tests`).
      - [ ] `spec-watcher.sh` retired — **only** after it has been beaten by
            the thing replacing it. Until then the role table is duplicated in
            two places, which is the defect that produced this phase; the
            residual is recorded rather than quietly carried.

      **The sibling was deliberately not touched.** `two-agent-review-loop`
      keeps its stage ids and gains no `actor`: its board is GitHub's PR
      primitives, not a thing's `status`, so the field would document a table
      no watcher here can consume. That loop's channel was chosen on purpose
      and this plan does not relitigate it.

- [ ] **Phase 5 — Seal.** Harvest what the use taught. Any insight, any
      conflict, any correction to the three artefacts above. `workflow-state.md`
      stays `evolving` — a field validated by one turn is not `stable`.

- [ ] **Phase 6 — Scope: a watch watches a run.** *Added 2026-09-21, from the
      field.* Two clones of the reviewer on one machine collided; the engineering
      agent's diagnosis found the `$HOME` state path (already fixed here, per
      clone by construction) and then the real gap: a watch scoped to the
      *definition* sees every stream's board as one board, so a reviewer armed
      for one subject wakes on the other's turn. `mdllm watch` has this gap
      exactly as `spec-watcher.sh` does. The scope is the `workflow-run` — the
      two streams already *are* two runs, the artefacts already declare
      membership, and the run already carries the pin and the claim. Specified
      as the direction in `standing-watch.md` → *Scope*.
      - [x] **`workflow-state.md` settles the membership edge** — 0.8, ruled
            2026-09-22 (`run-membership-is-realisation-2026-09-22`): membership
            is `linked_things: {relation: implements}` — *I am this run's
            realisation* — and `informed_by` stays provenance. Cued and walked
            (`cue-workflow-state-specification-2026-09-22`, seventeen edges; the
            live corpus was already conformant).
      - [x] `--run <id>` on `mdllm watch`: the board becomes the things that
            realise that run, at the named definition's stages. Arming refuses
            a run that does not resolve or is not a `workflow-run`. **It does
            not check that the run instances the watched definition** — the
            line above originally said it should, and building it showed why
            not: the run is the vertical (`software-development-lifecycle`),
            the loop is the horizontal (`two-agent-specification-loop`), and a
            watch reads the horizontal's stages for the vertical's members.
            Nor is the run's `definition_commit` read for the loop; it pins the
            lifecycle, and only a vertical watch on `current_stage` reads that.
            State and lock gain the run as a third key.
      - [x] Tests: two runs of one definition, two reviewers, each wakes only
            on its own; provenance is not membership; a thing leaving its run is
            `GONE` for that run's watch and arrives on the other's. (The line
            above first said "fires across runs"; it does not, by design — a
            watch never had the other run's things on its board.)
      - [ ] The engineering domain chooses its topology — three clones, which
            the loop already assumes, or four now that the scope is real. That
            is the domain's call and the operator's; nothing here arms it.
            **The floor was deliberately not touched on 2026-09-21**; it was on
            2026-09-22, additively, under the operator's grant — an unscoped
            watch behaves exactly as before.

## What The Build Found — Phase 4's First Input

**The engineering definition's stage ids and its own board table disagree.**
`two-agent-specification-loop` declares stages `drafting` / `reviewing` /
`cleared` / `ruling` / `blocked` / `approved`, while its *own* "five states,
one field" table — and the domain's declared `design-spec` status vocabulary —
say `draft` / `review` / `cleared` / `ruling` / `approved`. Two of the five
turn tokens do not match the stage that names them.

Nothing was broken by this, because the shell watcher never consulted the
stages block; it carried its own `case` statement. That is precisely the
duplication `stages[].actor` retires, and moving the table into the definition
is what surfaced the disagreement.

`mdllm watch` refuses to arm on it rather than polling in silence: a watcher
whose wake values cannot appear in the watched field's declared vocabulary
would be indistinguishable from a healthy estate, which is the failure the
loop fears most. **Reconciling the two is the domain's call, not the
framework's** — the stage ids can move to match the statuses, or the loop can
carry its turn on a `workflow-run` cursor instead. Phase 4 raises it; the
domain rules on it.

**A second, smaller find, fixed in the floor:** a `workflow-definition` whose
own `status` collides with one of its stage ids (`draft` is both) appeared on
the board it defines. A reserved type's status is a tool-owned lifecycle and is
never a domain's turn token, so reserved types are now excluded from a
status-keyed board.

## What This Plan Refuses

- **No hosting. No tunnel. No MCP transport. No server.** Nothing crosses a
  wire that git does not already send.
- **No cross-domain A2A.** `phase-3-run-domain-task-reverted` stands: a
  live-agent invocation is a different risk class from the read face, and the
  membrane that makes the face trustworthy does not cover it. When that leg is
  wanted it gets its own deliberately-shaped channel — the operator said so
  himself, and this plan holds him to it.
- **No new thing type for the turn.** The specification loop already checked
  this and found the state had a carrier. A separate handover thing would be a
  contended singleton across two clones — the one object in the design that
  must never diverge.
- **No scheduled task.** `two-agent-review-loop` v1.6 paid for that lesson:
  every run born with permissions on manual, one hang blocking everything for
  twenty-three hours, and tokens spent to say "nothing moved".
- **No third agent to break ties.** The sibling's rule, inherited: two agents
  can be confidently wrong together, and the answer is the human, not a third
  model.

## Done When

- [x] `workflow-definition` carries `stages[].actor`, floor-checked where used.
- [x] `mdllm watch` exists and is tested (22 cases); the PowerShell route is
      exercised in Phase 4.
- [x] The git-workflow kernel carries the turn-taking corollary.
- [x] A turn that never left wakes its own side — the silent drop-off seen in
      the field is loud where it can be seen (`loop-turns-self-heal-2026-09-23`,
      built 2026-09-23; the heal itself stays the agent's).
- [ ] One real turn has crossed in a live domain with no human relay, woken by
      the command and not by a script. *(The board is ready and armed; the turn
      itself waits on the two instances working.)*
- [ ] `spec-watcher.sh` is retired in favour of the command — and not before.
- [x] The watch has a specification of its own — `standing-watch.md`, `draft`,
      the first of the between-sessions band (2026-09-21).
- [x] A watch can be scoped to one run, and two reviewers on two runs never hear
      each other's doorbell (2026-09-22, `--run`; tested).
