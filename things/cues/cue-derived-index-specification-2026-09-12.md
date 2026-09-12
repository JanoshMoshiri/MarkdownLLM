---
id: cue-derived-index-specification-2026-09-12
type: cue
status: answered
version: 1.0
created: 2026-09-12
subject: derived-index-specification
raised_at: a18600adba60e8e5203d5abf2b7aa3346e56a790
raised_by: "agent — the dark-region walk of 2026-09-12, under the operator's delegated authority for this build"
verdict: not-inflection
verdict_reason: "The spec's own standing rule — any new singular load-bearing pointer must be emitted in the relationships index — was already obeyed mechanically (`subject` is indexed, 12 edges live); only its example list lagged, and now names it."
informed_by:
  - id: unattended-cue-carrier-2026-09-12
    commit: 069007b51977ac9150e1c8d5ffe9d7d9e7d7bfe7
tags: [cue, cue-carrier, change-reconciliation, dark-region]
---

# Cue: `derived-index-specification` was modified — inflection?

## The Change
The spec names the singular structural pointers the `relationships` index
must emit — "(`parent`, `definition`, modelled on `parent`)" — and follows
it with a standing rule: *any future singular load-bearing pointer added to
the schema must also be emitted here, or it becomes an unwalked declared
edge.* `subject` is exactly such a pointer. The rule was already satisfied
(the registry's default reverse-indexes it; the live index carries twelve
`--subject-->` edges), but the example list did not name it. Version 1.2.

## The Question
Does this change alter the logical path — a rule, a workflow, a thing the
domain reasons from — or only how an existing path is expressed?

## The Answer
**Not an inflection.** The rule is unchanged and was never violated; the
mechanism obeyed it by construction. Worth recording rather than passing
over silently, because this is the spec that predicted its own drift and
the prediction came true within one release — the list is an example, and
examples age. The durable protection is the rule, which held.

*Answered by the build session under the operator's delegated authority for
this work; the operator may overturn any verdict here by editing it — the
cue stays on the record either way.*
