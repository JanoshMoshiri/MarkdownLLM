---
id: hard-invariants-encode-a-semantic-assumption
type: insight
status: active
version: 1.0
created: 2026-06-24
session: 2026-06-24
source: both
confidence: high
origin: synthesised
tags: [validation, invariants, dependencies, schema, design-principle, change-management]
linked_things:
  - id: validate-thing-specification
    relation: informs
  - id: thing-specification
    relation: references
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: complements
---

# A Hard Invariant Encodes a Semantic Assumption

## The Insight

When you mechanise a semantic rule as a blocking invariant, you freeze one
reading of an otherwise ambiguous field — and you freeze it universally, in the
tool, where no domain can see or override it. The terminal-dependency gate
(`completed ⇒ every dependency is terminal`) reads like a structural check, but
it is really a *claim* that `dependencies` means a **hard prerequisite** ("must
finish before this"). Any domain that used `dependencies` to mean "builds on" or
"relates to" now fails at the commit boundary. The invariant is a semantic
assertion wearing mechanical clothing.

So a false-positive from such an invariant is genuinely ambiguous between two
diagnoses, and the whole discipline turns on choosing correctly:

1. **The data is wrong** — the edge was never a prerequisite; it was a soft
   relationship miskeyed as a `dependency`. Fix: remodel onto `linked_things`.
   The gate did its job by surfacing the misuse. This is the default, and it
   covers most cases (loose-semantics domains, "informs"-style edges).
2. **The invariant is wrong** — the model is honest and the rule overreaches.
   The real cases: a *recurring* prerequisite whose status cycles back to active
   after the dependent completed; a *reopened* prerequisite (state-based,
   corpus-wide validation means reopening B retroactively invalidates completed
   A and blocks a commit that only touched B — the block lands on the wrong
   change); threshold / "done-enough" completion where `completed` is a judgement
   rather than "all deps closed."

The decision rule: **default to remodeling; earn the escape hatch.** A blanket
per-domain config opt-out is *not* the answer — it is exactly how the kernel's
"if validation blocks a legitimate change, the schema is wrong, fix it with the
human" discipline rots. A narrow schema escape is justified only by a real
honest-model case (diagnosis 2), never granted preemptively.

## Why It Matters

Every mechanical check the floor gains is a piece of the agent's semantic burden
made unskippable — but it also quietly promotes one interpretation of the data
to law. That is a *good* trade when the field has a single honest meaning
(`id` is unique, dates are ISO) and a *trap* when the field is overloaded in
practice (`dependencies`, `parent`, `blocks`). Before hardening a semantic rule,
ask which field it is asserting a meaning *about*, and whether that meaning is
genuinely singular. If it is not, the hardening is still worth it — but its
false-positives are a *modeling signal*, and the framework must point them at the
right remodel (the looser edge) rather than reach for a toggle.

## Context

Surfaced 2026-06-24 while shipping the terminal-dependency gate that mechanises
`detect-conflicts` rule #1. The build itself was clean; the insight came from the
human pushing on "when would I *not* want this to fire in a domain?" — which
exposed that the gate encodes the prerequisite reading of `dependencies`, that
the principled release valve is remodeling onto `linked_things` rather than a
config flag, and that the one earned exception is the honest-but-too-strict case.
