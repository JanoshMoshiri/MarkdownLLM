---
id: substrate-floor-development
type: workflow-definition
status: draft
version: 1.1
created: 2026-08-21
tags: [workflow, floor, development-process, sprint]
stages:
  - id: problems
    to: [requirements]
  - id: requirements
    to: [analysis]
  - id: analysis
    to: [design, requirements]
  - id: design
    to: [build, analysis]
  - id: build
    to: [verify]
  - id: verify
    to: [build, reconcile]
  - id: reconcile
    to: [seal, build]
  - id: seal
    to: []
linked_things:
  - id: workflow-state-specification
    relation: implements
    notes: "First workflow-definition minted at the framework root; the primitive applied to the framework's own development process."
  - id: universal-workflow-methodology
    relation: implements
    notes: "Authored 2026-08-21, before the methodology entered the repo; recognised 2026-08-25 as its floor-development specialisation — the same seven decisions, compressed and hardened, with two substrate-specific gates added (reconcile's consistency walk, seal's human gates). Convergence, not derivation: the general form was operating here before it was written down."
  - id: prove-identity-before-you-change-bytes
    relation: implements
    notes: "The design stage's sequencing rule: split byte-identical restructuring from deliberate behaviour change and order identity first, naming each restructuring commit's proof before writing it."
  - id: some-changes-are-verifiable-only-by-publishing
    relation: implements
    notes: "The seal stage's honesty rule: a surface the floor cannot execute (CI config, vendor lifecycle) is sealed as authored-and-unproven, naming the observation that would settle it — never as verified."
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: references
    notes: "The remedy's phase machinery is the first work inventory this process consumes; the remedy stays the finding ledger, this defines the repeatable process."
---

# Substrate Floor Development

The repeatable process for changing the mechanical floor, born from the
2026-08 lesson: a review handed straight to an executor as "requirements"
skipped the analysis and design stages, and the result ignored performance
until it was unusable. Stages are gates, not ceremony — each exists because
skipping it has already cost a real sprint.

**Not exposed — and no longer the generalisation candidate.** The general
form now lives in the `universal-workflow.md` spec, which reaches every
domain with the framework via domain-refresh; a domain adopting this
discipline specialises that, not this. This
definition stays unexposed as the substrate's own specialisation: its
stage mapping onto the general form is roughly problems+requirements ≈
define-need/assess-current/define-prioritise, analysis ≈ set-mvp-target,
design ≈ design-plan, build ≈ execute, verify+seal ≈ review-verify — with
reconcile and seal's human gates as the floor-specific additions the
general form leaves to proportionate application.

## Stages

**problems** — the inventory. Every requirement is problem-driven: a review
finding, a measured bottleneck, a lived failure. Exit: each problem has
evidence (a review row, a measurement, a commit) — no aspirational entries.

**requirements** — the problem set restated as requirements, including
non-functional ones: tolerable execution speeds, thresholds, and timeout
budgets are first-class requirements with numbers and a named reference
machine, not afterthoughts. Exit: a committed requirements thing.

**analysis** — the cut. Prioritise (necessity / should / stretch), scope one
sprint deliberately smaller than the requirement set, and record the cut as a
`type: decision` with inputs pinned. Exit: the scope decision is committed.
Loop back to requirements if analysis finds the set incomplete.

**design** — proper design, not planning: components touched, how each change
proves its budget, the focused test set per change, commit granularity, risks
with mitigations. The design must show how every in-scope requirement is met
and every budget verified. Where a change set contains both restructuring and
behaviour change, order identity first — byte-identical commits with their
proof named, then the deliberate change against a verified structure
(`prove-identity-before-you-change-bytes`); a commit that does both proves
neither. Exit: a committed design thing. Loop back to analysis if design shows
the cut was wrong.

**build** — implementation in meaning-boundary commits against the design.
Deviations from the design are recorded in the run body as they happen, not
reconstructed later.

**verify** — the focused suites for what changed, budgets measured against
their numbers, then the full suite once at this boundary (the full suite is a
stage gate, not an inner loop). Loop back to build on failure.

**reconcile** — the dark-region walk for anything operative that changed:
specs, docs, kernel regeneration, generated indexes, the routing surfaces.
Semantic consistency is maintained at the point of change. Loop back to build
only if reconciliation exposes a code defect.

**seal** — closure: plan/ledger states updated to truth, changelog/version
judgement, publication debt reported. **Human gates live here and only
here:** the push/release decision, any public claim, anything irreversible.
Where the sprint changed a surface the floor cannot execute — CI config, a
vendor lifecycle, anything whose runtime someone else supplies — seal it as
*authored and unproven*, naming the observation that would settle it
(`some-changes-are-verifiable-only-by-publishing`). Its first published runs
belong to the work, and a red run after a green local suite is the probe
doing its job, not a regression.

## Division of labour

The agent executes every stage and makes the judgement calls within them —
including the analysis cut and the design — recording decisions with pinned
inputs rather than pausing for approval. The human is pulled in at seal
(publication), at any irreversible or authority-bound act (trust grants,
system settings, external claims), and whenever a stage loop repeats twice
without converging — a non-converging loop is a requirements problem, and
requirements problems belong to both.
