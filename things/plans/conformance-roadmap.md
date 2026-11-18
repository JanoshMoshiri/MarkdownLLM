---
id: conformance-roadmap
type: plan
status: not-started
version: 1.0
created: 2026-11-18
priority: critical
origin: stated
exposed: false
tags: [roadmap, conformance, four-pillars, floor, gauges, metabolism, handoff-contract, wake, domain-agents, acceptance-check, dogfooding]
linked_things:
  - id: conformance-not-determinism
    relation: implements
    notes: "The principle and the four pillars this roadmap is organised by."
  - id: work-set-on-trust-has-nothing-to-check-against
    relation: implements
    notes: "Why every phase here opens with its acceptance check, written before the work and out of the builder's reach."
  - id: a-record-that-only-accumulates-has-no-metabolism
    relation: implements
    notes: "Phase 3 builds the missing organ."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: references
    notes: "The standing truth the principle rests on."
  - id: peer-loops
    relation: references
    notes: "Phases 5 to 7 carry that plan's rules and phases forward. Its order of work, the eval first, waits on the operator's ruling in Phase 0."
  - id: a2a-conversations-on-their-own-branch
    relation: references
    notes: "Phase 1 builds the watcher's check at the remote ref. That plan's validated landing stays its own phase."
  - id: review-catch-on-the-road
    relation: references
    notes: "Continues in its own plan as part of Phase 8. Proposed to gate nothing here."
  - id: thing-lifecycle-specification
    relation: references
    notes: "The deferred spec that already holds the expulsion half of Phase 3."
  - id: standing-watch-specification
    relation: references
    notes: "Owns the watcher Phase 1 and Phase 6 change."
  - id: change-reconciliation-specification
    relation: references
    notes: "Owns the gate Phase 1 carries to every repository."
triggers:
  - type: time
    condition: "2026-12-02 reached"
    action: surface
    note: "Two weeks in. Has the operator made the Phase 0 rulings? Is Phase 1's first check committed and approved, and is it green or red? If nothing has moved, say which of the two stopped it: the rulings were not made, or the check was not written. A roadmap that sits is the accumulation Phase 3 exists to end."
---

# The Conformance Roadmap

## What This Is

The forward plan for the framework, organised by one principle and four
pillars the operator named on 2026-11-18
(`conformance-not-determinism`).

The principle: let the model be what it is, non-deterministic and good at
reaching the end of a problem, and catch its result in a reference it cannot
argue with. The rule that follows: **every clause of every contract is either
bound to a mechanical check or assigned to a named human decision.**

The pillars:

1. **The blueprint of operation.** The workflow recipe, with an inspection at
   each station.
2. **The operation substrate.** The record, the floor and the watcher, where
   the gauges live.
3. **The definition of each atomic domain.** What a domain owns, checks and
   publishes.
4. **The communication path.** The handoff contract between domains.

This plan sits above the open plans. It does not replace them. It orders
them, and says which phase each one serves.

## What It Rests On

- Three insights recorded the same day, in the operator's words:
  `conformance-not-determinism`,
  `work-set-on-trust-has-nothing-to-check-against`,
  `a-record-that-only-accumulates-has-no-metabolism`.
- A read-only survey of the estate on 2026-11-18: 19 corpora, 3,228 things,
  6,084 commits, read at committed HEAD. Most specifications are used and
  checked. The weakness is uneven gauges and accumulation: the cue and
  session-end gate is projected in 5 of 19 repositories, `held_by` is on 123
  things and nothing reads it, 113 of 344 decisions are pinned, 1,481 things
  are open.
- Three research reports on cross-vendor agent setups and on testable
  boundaries. They are local working documents and are not yet committed.
  Phase 0 banks them.
- One finding in the code: the watcher reads the remote ref and wakes the
  right seat without ever running the floor on what it read. The check was
  believed built.

Every judgement the research makes about this framework is by analogy to
similar practice. None of it is a measurement of this system. Phase 8 exists
to change that.

## How Every Phase Runs

This roadmap is built the way it says work should be built. The framework's
own building is the radius of the fractal where the principle slipped
(`work-set-on-trust-has-nothing-to-check-against`), so these rules bind every
phase below.

1. **The check comes first.** A phase opens with its acceptance check
   committed on its own: a test or a fixture that fails today. The operator
   approves that commit before any building starts.
2. **The builder does not touch the check.** Until Phase 1 builds the lock,
   the operator reads the diff of the check's files when the phase closes.
   That reading is a named human decision, not an assumption.
3. **Done is the check passing where the builder cannot reach it.** The
   framework root's CI already runs the floor and the tests on every push.
   A phase closes on a green run there, not on the builder's report.
4. **What cannot be checked is named.** Each phase lists the decisions that
   stay the operator's.
5. **New rules arrive as warnings.** A new floor rule reports first, with
   its count across the estate recorded. It blocks only after the operator
   has seen the count. Counts may then only fall.
6. **Each phase leaves one line of evidence:** the commit where its check
   went green.

The checks written below are specifications of the test, not the test. The
test itself is the first commit of its phase.

## Phases

### Phase 0. Rulings and evidence

*Nothing is built. The operator rules, and the evidence is banked.*

- [ ] **Ruling: the order of work.** `peer-loops` 2.2 says the eval comes
      first and nothing in its Phases 2 to 8 is built until two eval cycles
      have run. This roadmap proposes that the review-catch eval continues in
      its own plan and gates nothing here, because the roadmap no longer
      depends on whether a second vendor beats a second fresh session. The
      operator accepts or rejects that. If accepted, `peer-loops` is revised
      under its own reconciliation.
- [ ] **Ruling: doctrine.** Which specifications are doctrine, kept because
      they state truths and not because a check reads them. Proposed: the
      manifesto, `universal-workflow.md`, `operating-model.md`. Nothing is
      dropped by this roadmap.
- [ ] **Ruling: the open plans.** The table under *The Open Plans* proposes
      which phase each open plan serves. The operator confirms it, and rules
      on the plans this roadmap does not touch: stay paused, or close.
- [ ] **The research is banked.** The two research reports of 2026-11-17 and
      2026-11-18 are committed as review artifacts with pinned inputs, as the
      swarms review was.
      *Check:* both exist under `reviews/`, pass the floor and the disclosure
      boundary, and this plan links them.

### Phase 1. Gauges out of reach

*Pillar 2. The gauge sits where the worker cannot reach it.*

- [ ] **The watcher validates at the remote ref.** Before it wakes a seat,
      the watcher runs the floor on the record as it stands on the remote. A
      record that fails wakes nobody and is reported.
      *Check:* a test builds a remote holding a ticket turn that fails the
      floor, committed with hooks skipped. The watcher exits with a distinct
      refusal and no wake. The same turn made valid wakes the seat.
- [ ] **The gate rides in every repository.** The cue gate and the
      session-end gate apply to any commit, from any vendor's agent, in every
      domain. Today they ride the harness hook and reach 5 of 19
      repositories. The phase first reads why the gate was placed in the
      harness, since the agent's walk and the operator's residue both pass
      through it.
      *Check:* in a scratch domain with no harness settings, a commit that
      changes a definition surface with no cue on record is refused, and a
      `session-end:` commit with the reckoning open is refused.
- [ ] **Protected paths.** The floor's code, the schemas, the hooks, any
      ratchet baseline and every acceptance check in this roadmap cannot be
      changed by a working agent without the operator's approval on record.
      *Check:* a commit from an agent seat that touches a protected path
      with no approval record is refused locally. The same commit made with
      hooks skipped and pushed is caught at the remote, by CI or by the
      watcher, before any seat acts on it.
- [ ] **A remote backstop for every domain.** The framework root's CI runs
      the floor on push. Each live domain gets the same, or the watcher's
      check from the first item stands in where a remote has no CI.
      *Check:* for each domain remote, a commit made with hooks skipped that
      breaks the floor is reported within one watch interval.

*Yours:* the form the approval record takes. No commit in this estate has a
human committer today, so "the operator approved" has no mechanical meaning
until this is decided.

### Phase 2. Conventions become checks

*Pillar 2. What is left to convention today gets a gauge, one rule at a
time, warning first.*

- [ ] **Claims are read.** `held_by` is enforced with an expiry in
      `held_until`: a second writer on a held thing is a finding, and a claim
      past its expiry is released and reported.
- [ ] **Conflicts name their parties.** 16 of 85 do.
- [ ] **Decisions are pinned.** A decision with no `informed_by` is a
      finding. 113 of 344 carry one.
- [ ] **Unverified external content ages.** 208 of 484 external things are
      unverified.
- [ ] **`keep-active` carries a reason and an expiry.** 323 of 446 active
      insights are exempt from the orphan check by it.

*Check, for each rule:* a fixture corpus holding one violating thing yields
the finding. The rule's count across the estate is recorded when it starts
warning and again when it starts blocking.

*Yours:* for each rule, whether the count it reports is acceptable debt, and
when it moves from warning to blocking.

### Phase 3. Metabolism

*Pillars 2 and 3. Inception, processing, expulsion
(`a-record-that-only-accumulates-has-no-metabolism`).*

- [ ] **A lifecycle per type.** Each type declares how a thing is born and
      what it must carry, the states it moves through, how long it may sit
      in each, and how it leaves: closed, superseded, promoted or archived.
- [ ] **The floor ages what does not move.** A thing past its declared time
      in a state is a finding that names its exits.
- [ ] **The rate measures the record, not the queue.** Intake and disposal
      per type and per domain, from the commit history.
- [ ] **`thing-lifecycle.md` is brought back** and rebuilt around this, with
      the floor behind it. It already specifies the rolling window, stubs
      and rehydration.

*Check:* a fixture repository with a known history returns its known intake
and disposal per type. A fixture thing past its state's age yields the
finding. Run on this corpus for the week ending 2026-11-18, the rate reports
the things that week added, where `mdllm reckon --rates` reported none.

*Yours:* the ages and the exits for each type, and the first clearing of
what has accumulated: the stalled plans, the open cues, the abandoned
tickets.

### Phase 4. The blueprint

*Pillar 1. The recipe, with a class on every clause.*

- [ ] **Every operative rule carries its enforcement class:** enforced,
      tested, detectable and routed, human-owned, or doctrine. A rule marked
      enforced names the check that enforces it.
- [ ] **Prose that must happen becomes a check or is relabelled.** The
      kernel, `AGENTS.md`, the skills and the bound prompts are instructions.
      Each "must" in them either gains a check or is marked as guidance.
- [ ] **Workflow definitions take the two shapes.** A repeatable workflow
      fixes its stations and gates each one. An accumulative workflow fixes
      only the gate on its result and on each step that cannot be taken
      back.

*Check:* coherence fails when a kernel rule has no class, or names a check
that does not exist. A generated report lists every operative rule with its
class and its check.

*Yours:* which rules are human-owned, and who owns each.

### Phase 5. The handoff contract

*Pillars 3 and 4. What one domain hands another, and what makes it done.*

- [ ] **One contract shape,** carried by the ticket or beside it: a strict
      schema, acceptance criteria, a proof command, a done condition, a
      fixed handback, a verdict tied to one commit, a version, and who may
      issue and accept. Each clause carries its enforcement class.
- [ ] **The floor holds it.** A ticket handed to another seat without
      criteria and a proof command is refused. A handback without the fixed
      block is refused. A verdict that names a commit other than the head it
      reviewed has lapsed and is reported.
- [ ] **The proof is re-run by someone other than the worker.** The
      worker's report routes the work. It is not the evidence.
- [ ] **Each domain publishes what it accepts and what it returns.**

*Check:* fixture tests for each refusal, and one fixture exchange that
passes end to end.

*Yours:* the verdict vocabulary, the round cap, and who may accept on each
domain's behalf.

### Phase 6. Wakes proved by a commit

*Pillar 4. Delivery is the receiver writing to the record.*

- [ ] **Wakes move to the vendors' own routes** and carry no content: a
      turn is waiting, and nothing more.
- [ ] **Delivery is three facts:** stored, accepted, read. Only read counts,
      and read is the woken seat's commit to the record.
- [ ] **A wake nobody answered raises an alert** to the operator by its
      deadline. It is not resent blind.
- [ ] **Every wake is logged with its three facts.**

*Check:* a test wake that reports success and produces no commit raises the
alert by the deadline. A test wake followed by a commit closes clean.

*Yours:* a hands-on test on the operator's own machines of whether each
vendor's route reaches the session a person has open. The vendors do not
document it, and no test here can stand in for it.

### Phase 7. Two domains, one contract

*All four pillars. The proof nobody has published.*

- [ ] Two real domains, each with its own agent, pass one real piece of
      work under the Phase 5 contract and the Phase 6 wakes.
- [ ] Predictions are written and approved before it runs, as an eval cycle
      is.
- [ ] The run records, from the commit history alone: every turn and its
      acknowledging commit, every handback and its verdict, and each time
      the operator had to step in.

*Check:* the record shows the exchange complete with no turn missing its
acknowledgement and no handback accepted without its proof re-run. The
count of operator interventions is stated against the prediction.

*Yours:* which two domains, which piece of work, and the verdict.

### Phase 8. Measure the framework itself

*The evidence the research could not supply.*

- [ ] **The emitted kernel and the skills:** task outcome and cost with and
      without them.
- [ ] **The walk:** how often an agent's reconciliation walk misses a
      dependant that a fresh session or a person finds.
- [ ] **Wake reliability:** one month of the Phase 6 log.
- [ ] **Review-catch on the road** continues in its own plan.

*Check:* each measurement has its predictions written before it runs.

*Yours:* what is written up, and when. The standing direction of 2026-10-05
holds: nothing is concluded until much more testing.

## The Open Plans

Proposed, from each plan's title and the session-start digest. Each mapping
is confirmed by reading the plan when its phase opens. The operator rules on
the whole table in Phase 0.

| Open plan | Serves |
|---|---|
| `a2a-conversations-on-their-own-branch`, `cue-carrier`, `the-record-holds-unattended` | Phase 1 |
| `mechanical-coherence-checks-backlog`, `floor-structure-residue` | Phases 2 and 4 |
| `the-reckoning` | Phase 3 |
| `workflows-emerge-from-use`, `estate-workflow-derivation`, `session-start-hardening` | Phase 4 |
| `peer-loops`, `substrate-native-a2a` | Phases 5 to 7 |
| `the-seat`, `closed-loop-operating-state` | Phase 6 |
| `review-catch-on-the-road`, `evidence-and-eval-backlog` | Phase 8 |

Not touched by this roadmap, for the operator to keep paused or close:
`codex-cloud-workspace`, `codex-cloud-conversational-launcher`,
`cowork-adapter`, `explorer-macos-and-navigation-sprint-2026-09`,
`explorer-publication-readiness`, `public-docs-face-build`,
`response-depth-control`, `scaffold-carries-the-universal-workflow`,
`scaffold-declares-visibility`, `framework-upward-signal`,
`operator-seat-and-harness-native-onramp`, `coherence-mechanism-build`,
`substrate-review-consolidated-remedy-2026-08-20`, `cold-test-condition-a`.

## What Stays The Operator's

- Every ruling in Phase 0, and approval of each phase's check before
  building starts.
- Reading the diff of each check when its phase closes, until Phase 1's
  lock exists.
- Risk acceptance: when a warning becomes a block, and what debt is
  accepted.
- The ages, the exits and the first clearing in Phase 3.
- The hands-on wake test in Phase 6, and signing in to any vendor.
- Which two domains prove the contract, and the verdict on the proof.
- Whether anything is written up.

## Done When

- [ ] Every phase's check is green on the remote, with its line of evidence
      recorded here.
- [ ] Every operative rule in the kernel carries its class.
- [ ] The rate shows disposal keeping pace with intake across the estate.
- [ ] Two domains have passed one piece of work under the contract with no
      turn carried by the operator.
