---
id: dispatch-design-2026-08
type: plan
status: completed
version: 1.0
created: 2026-08-27
completed: 2026-08-27
priority: high
tags: [dispatcher, closed-loop, phase-2a, design, universal-workflow]
informed_by:
  - id: closed-loop-operating-state
    commit: 926622b64dc3e7a203ba51b548748861b82ff826
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    commit: f1fade782df3a6707bf5257f5794ba8f6a512264
linked_things:
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 2a executed: the design decisions and both deliverables. 2b (the generated tick + the operator's grant) executes against this design."
  - id: universal-workflow-methodology
    relation: implements
    notes: "A light traversal under the proportionate-use rule — low-risk corpus declarations, gated by the root push; each stage a few lines, as the spec licenses."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: implements
    notes: "The governing commitment, executed: every dispatch judgment landed in versioned corpus surfaces; the tick design carries none."
  - id: orchestration-specification
    relation: informs
    notes: "Phase 5 seals the dispatch doctrine here once the pilot has run; until then this design is the working authority and deliberately not a spec change."
---

# Dispatch Design — Phase 2a (2026-08-27)

The universal workflow's seven decisions, run light. Consequence of failure
is low — everything lands at the framework root behind the push gate — so
each stage is a few lines, per the proportionate-use rule.

**Define need.** Loops that run only when a human opens a session leave the
human as the dispatcher. Needed: the tick that turns "trigger fired" into
"session exists", with zero judgment outside the corpus. For: the operator
(out of the loop), the estate (loops that actually cycle).

**Assess current.** Every loop exists and runs when invoked; dated triggers
+ chase proven (08b); the floor evaluates fired sets per repo; estate-sync
walks all repos; publication authority is declared per repo. Missing: only
the tick and the standing instructions a ticked session follows.

**Define & prioritise.** Highest-value gap is the tick at one radius, not a
scheduling framework. Priority: dispatch prompt + guards now; tick at 2b;
everything else deferred to evidence from the pilot.

**MVP target.** One tick, one seat (this machine), one pilot radius; a
week of mandatory digests; zero out-of-seat interventions or every one
routed as a finding. Success criteria are Phase 4's measurements —
deliberately not restated there and here twice.

**Design.** Four decisions, each choosing the smaller thing:

1. **The schedule is distributed, and already exists.** Each repo's
   declared triggers are its schedule; the estate-radius "declaration" is
   the walk itself (root + domain repos), which estate-sync already
   defines. **No central schedule table is created** — a central table
   would be the second brain in data form, drifting against the repos'
   own triggers. The planned "operating-schedule declaration" deliverable
   is satisfied by this ruling plus the dispatch prompt.
2. **The inside half is one prompt file.** `templates/prompts/dispatch-loop.md`
   (id `dispatch-loop`, draft — referenced by path, as bindings reference
   every prompt file; templates/ sits outside the corpus id-space by
   design) carries the entire procedure: launch
   validity, sync-then-orient, per-repo floor queries, strict per-repo
   serialization with skip-dirty/skip-diverged, rituals run under each
   repo's own contract, seat discipline, depth limit 1, stop-on-surprise,
   stop-on-condition, mandatory digest. A prompt, not a
   workflow-definition: the rituals it invokes own their stage graphs;
   adding one above them would be ceremony (restraint rule).
3. **Guards are declared, not coded.** In the prompt's frontmatter
   (`dispatch_guards`): depth_limit 1 — a dispatch session never
   dispatches, chosen stricter than the insight's depth-N for the pilot;
   per-repo serialization; stop condition required at launch (a launch
   without one halts at the digest); the dead-man armed at 2b — a dated
   trigger on the closed-loop plan firing when no dispatch digest has
   been committed within its window. Noisy triggers are reported as
   defects, never obeyed.
4. **The outside half is generated, minimal, and dumb.** At 2b the adapter
   writes one scheduled-task entry per seat: invoke the harness headless
   at the estate root with the dispatch-loop prompt and explicit stop
   values. `mdllm doctor` compares installed entry against this design's
   declared shape. Hand-authoring the entry is a defect by declaration.

**Execute.** Deliverables 1 and 3 landed this session (the prompt with
guards); decision 1 dissolved the third deliverable into a ruling recorded
here. 2b and the dead-man arming await the operator's grant — census row 7,
by design not by gap.

**Review & verify.** The design's own verification is structural (floor
clean, pins verified against rev-parse — after one fabricated-pin defect
was caught and corrected in the census, the third instance of that class).
The delivered state's verification is Phase 4's pilot; its review feeds
`closed-loop-operating-state`'s next assessment (accumulative), while each
dispatch run's digest feeds the prompt's own evolution (repeatable) — the
two shapes interleaving exactly as `operating-model.md` describes.

**Longevity lenses.** Maintainable: one prompt file, one generated entry.
Extendable: new loops join by declaring triggers in their repo — the
dispatcher changes by zero lines. Manageable: every change behind the push
gate; the tick regenerable. Monitorable: the mandatory digest plus the
dead-man; silence distinguishable from blindness by construction.
