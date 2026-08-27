---
id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
type: insight
status: active
version: 1.0
created: 2026-08-27
session: 2026-08-27
source: both
confidence: high
origin: stated
tags: [dispatcher, closed-loop, scheduling, control-plane, phase-2, design-commitment]
linked_things:
  - id: closed-loop-operating-state
    relation: informs
    notes: "Phase 2's governing design commitment, recorded before the design session runs: the scheduler stays dumb because the schedule is things."
  - id: trigger-specification
    relation: references
    notes: "Triggers already are the inside half of the schedule — declarative, versioned, floor-evaluated. The dispatcher adds only the tick that turns 'fired' into 'a session exists to read it'."
  - id: orchestration-specification
    relation: informs
    notes: "When dispatch doctrine lands, it lands here: the tick is a harness-session anchor, the routing is corpus state, and no judgment crosses into the runner."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: complements
    notes: "That insight gates each launch (exogenous stop conditions); this one gates the layer that launches — both exist so autonomy compounds structure, not error."
  - id: tracking-artifacts-can-drift-from-reality
    relation: supports
    notes: "An external scheduler config is a tracking artifact for the estate's intent; it drifts exactly the way every unversioned mirror drifts. Generate it from the corpus and doctor-check it, never hand-hold it."
---

# A Dispatch Layer Outside the Corpus Is a Second Brain

## The Insight

The moment sessions launch themselves, the launching logic — which loops run,
at what cadence, under what conditions, with what budgets, in what order,
gated by what — wants to become a program. The operator saw it forming and
named the danger: a whole new logic layer. The commitment, stated before
Phase 2 designs anything: **that program must be the corpus, not a peer of
it.** Cadences, routing, conditions, budgets and dependencies live as
declared things — triggers, workflow-definitions, an estate's declared
operating model — and the only artifact outside the repo is a dumb tick:
*start a session; the session asks the floor what is due.*

An external dispatcher that accumulates routing rules, gating conditions and
sequencing knowledge is a **second brain**: unversioned, unvalidated,
unreconciled, unretrospected. Every mechanism the substrate spent months
building — validation, provenance, reconciliation cues, retrospectives,
seats — applies to the schedule *only if the schedule is made of things*.
Outside the corpus it drifts exactly as every mirror drifts, except this
mirror decides what runs.

## Why It Matters

- **The framework already holds the inside half.** Dated triggers with chase
  actions are the schedule, versioned and floor-evaluated; the 08b carrier
  proved the pattern end-to-end. The dispatcher adds one capability only:
  the tick that turns "fired" into "a session exists to read it".
- **Per-substrate variability falls out free.** Every estate's logic layer
  differs — different domains, different loops, different granularities —
  and no runner forks: the program differs because the data differs. The
  runner is identical and dumb everywhere. Self-evolution also falls out
  free: the loops that edit things can edit triggers and definitions too,
  under the same gates (additive flows; redefinitions queue at seats; root
  changes wrapped by the push).
- **The industry converged here after decades.** cron's crontab, CI's
  pipelines-as-files, Kubernetes' declared desired state reconciled by
  generic controllers, GitOps' repo-as-single-source: every mature
  scheduling substrate ended at *versioned declarations + dumb runners*.
  Standing on those shoulders means refusing, at birth, the smart-scheduler
  stage they each had to grow out of.

## Phase 2 Corollaries (mitigations, declared not coded)

- **Recursion and depth guards as declared limits** — a launch caused by a
  launch caused by a launch requires a human tick beyond a declared depth;
  dispatch sessions do not dispatch on commits authored by dispatch
  sessions unless a declared edge says so (CI learned this the hard way).
- **Noisy-trigger quarantine** — a trigger firing more than its declared
  rate is surfaced as a defect, not obeyed
  (`a-check-that-always-fires-teaches-the-operator-to-ignore-it`, one level up).
- **Per-repo serialization by default** — one autonomous session per repo at
  a time; contention beyond that reaches for coordination-claim leases.
- **A dead-man trigger watching the dispatcher itself** — the tick's silence
  must be distinguishable from health; a dated expectation fires when no
  dispatch session has committed within its window.
- **Harness config generated, never authored** — scheduled-task entries and
  allowlists derive from the corpus via the adapter pattern and are
  doctor-checked against it, so the installed schedule cannot silently
  disagree with the declared one.

## Context

2026-08-27, the closed-loop design conversation. The operator, walking the
dispatcher design, saw the scheduler's logical tree becoming "a program in
itself" and asked what becomes unmanageable and what this shape descends
from. The answer generalised the framework's founding move — the definitions
are the program, git is the state — one layer up, to the layer that runs the
layers.

Dismissal condition: absorbed when Phase 2's design lands in
`orchestration.md` (or a dispatch spec) carrying the schedule-is-things rule
and the corollaries above; refuted if a real estate demonstrates a dispatch
need that cannot be expressed as declared corpus state.
