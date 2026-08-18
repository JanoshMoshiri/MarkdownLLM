---
id: operating-layer-quality-loop
type: plan
status: not-started
version: 1.0
created: 2026-08-18
priority: medium
tags: [coherence, skills, retrospective, quality-loop, parked]
linked_things:
  - id: the-operating-layer-has-no-quality-loop
    relation: implements
    notes: "This plan is the insight's remedy shape given a forward carrier; the insight owns the reasoning and is not restated here"
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Owns the skills-directory-vs-artifacts stub check already; the new skill-age-vs-domain-velocity Info should be routed there (or shipped beside it) under the same same-builder gate — file untouched at creation time because its staged state was boundary-blocked"
  - id: retrospective-specification
    relation: references
    notes: "The hook home: the judgement half lands as reflexive scan #6"
  - id: cowork-adapter
    relation: related
    notes: "Deliberate sequencing, not a hard dependency: parked until the vendor-adapter workstream is put to bed, to avoid mixing workstreams"
  - id: vendor-harness-adapter-foundation
    relation: related
    notes: "Same sequencing note as cowork-adapter"
---

# Operating-Layer Quality Loop

**Parked by the operator, 2026-08-18** — deliberately sequenced behind the
vendor-adapter workstream (Codex enablement, Claude Code hardening, Cowork
correctness). The reasoning lives in
`the-operating-layer-has-no-quality-loop`; this plan exists only so the
orient view carries the return path. Resume when the adapter work closes.

## Deliverables (from the insight's remedy shape)

1. **`review-skill-coherence` bound prompt** — `templates/prompts/`, bound to
   the `retrospective` hook; becomes scan #6 in `retrospective.md`'s
   reflexive list (+ `orchestration.md` bindings). Inputs: skill files +
   AGENTS.md, schema index, commit stream since last retrospective. Forces a
   per-skill disposition: confirm-current / update / park / retire. The
   workflow skill gets the bidirectional question (dead vocabulary vs.
   de-facto workflow worth codifying).
2. **Floor Info: skill-age-vs-domain-velocity** — `mdllm coherence`, domain
   scope: a skill untouched since the birth commit while `things/` moved N
   commits. Pure git, no suppression list. Route into
   `mechanical-coherence-checks-backlog` or ship directly beside its stub
   check.
3. **Open the named conflict** — `type: conflict` at the framework root:
   workflow *skill* (Layer 2) vs `workflow-definition` *thing* (Layer 3) as
   two homes for process knowledge.
4. **Retrospective trigger sibling** — extend `retrospective.md`'s "when to
   write one" with a volume-style trigger: skills untouched while the domain
   crossed N commits.

## Exit

The judgement half runs at the next real retrospective on a live domain; the
floor half fires its first Info in the estate. Deliverable 3 is resolved or
explicitly held per `belief-revision.md`.
