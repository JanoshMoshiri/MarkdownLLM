---
id: inflection-candidates-are-computable
type: insight
status: promoted
version: 1.0
created: 2026-08-04
session: 2026-08-04
source: both
confidence: high
origin: synthesised
promoted_to: change-reconciliation-specification
tags: [change-reconciliation, cue, inflection, floor, sensors, estate]
linked_things:
  - id: change-reconciliation-specification
    relation: complements
    notes: "Refines, does not revise: the spec's 'invoked, never hooked' protects the cue verdict, and this insight keeps that intact. What it adds is that the *candidate* — the fact that a cue question exists — was always mechanical, and the floor can surface the question without touching the answer."
  - id: estate-cadence-cluster
    relation: informs
    notes: "Phase 4's first half is this insight built: the candidate advisory at commit time."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: complements
    notes: "The constraint on building this: candidacy must be selective (fan-in threshold, definition-surface types, modifications only) or the advisory becomes wallpaper and the cue is missed with extra steps."
---

# Inflection candidates are computable — the cue is human, the question is not

**What happened:** the operator reported two facts in one conversation
(2026-08-04): the change-reconciliation pass has never been run on the
framework's own changes, and under multi-domain velocity the cue is being
missed in the domains too — changes to reasoned-from things land
un-walked, and the drift is felt before it is seen. The spec had already
predicted the miss ("an expert will sometimes edit without declaring the
inflection") and routed it to the retrospective as the net beneath the
net — but retrospectives were not happening either, so both nets were
down at once.

**The insight:** the spec's division of labour conflates two things under
"the Cue is human." The cue *verdict* — is this change consequential
enough to walk? — is genuinely human and must stay so. But the cue
*question* — does anything reason from what was just modified? — is a
mechanical predicate, and the floor already holds both of its operands at
commit time: git distinguishes a modification from an addition, and the
relationships index knows the inbound edges. A fresh thing on a clean
slate carries no consistency risk (the spec's own premise), so candidacy
is precisely: **modified ∧ reasoned-from** — with "reasoned-from"
readable as inbound edges above a threshold, or membership in the
definition-surface types (specification, skill, guide, schema, kernel
source) whose entire function is to be reasoned from.

The floor's stated job in this spec is to make the agent "unable to not
see" the shape of what a change disturbs. It currently does that only
*after* the cue — `touchpoints` answers when asked. A candidate advisory
at commit time — one line, naming the fan-in and the command — asks the
question at the moment it exists, and leaves the verdict where it
belongs. Detection mechanical, judgement human: the same shape as every
sensor the floor has grown.

**How to apply:** when a commit modifies a thing that is reasoned-from,
say so, once, quietly. Never block, never auto-run the pass, never score
the change. The advisory is the question made unavoidable; the human
still owns "no, this one isn't consequential" — and saying no to a named
question is a decision, where not being asked was drift.
