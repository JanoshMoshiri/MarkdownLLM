---
id: some-changes-are-verifiable-only-by-publishing
type: insight
status: active
version: 1.0
created: 2026-08-22
session: 2026-08-22
source: both
confidence: high
tags: [ci, floor, verification, publication, sprint, blind-spot]
origin: synthesised
linked_things:
  - id: portability-claims-need-execution-tests
    relation: extends
    notes: "That insight says a claim is verified only by executing in the environment; this names the case where the environment is unreachable until after publication, so the execution cannot happen before the seal."
  - id: run-floor-sprint-2-2026-08
    relation: derived-from
    notes: "The F7 matrix leg needed three published runs to go green; every local instrument reported clean throughout."
  - id: floor-structure-residue
    relation: informs
    notes: "Item 6 (the CI matrix) is the worked instance: the decision was made locally, but the evidence for it could only arrive after a push."
---

# Some Changes Are Verifiable Only By Publishing

## The Insight

The deterministic floor's reach stops at the machine. Validation, coherence,
the pre-commit legs, the full test suite — all of it runs locally, and for
almost every change that is enough: the thing that will execute in
production is the thing that just executed here.

**CI configuration breaks that symmetry.** A workflow file is not executed
by anything the floor can run. Its first execution happens on a hosted
runner, which only happens after a push. So a class of change exists whose
verification is *structurally* unavailable before publication — and for a
release surface that publishes deliberately (`autopush: false`), that means
unavailable before the human gate, too.

The floor reports clean the entire time. Not because it is wrong, but
because the change lies outside what it can look at.

## How It Surfaced

Sprint 2's F7 added a Windows CI leg. Locally: 694 tests green, every budget
met, coherence clean, validation clean. The design recorded the leg as
"authored, unproven," and the verify record deliberately refused to claim
coverage.

It then took **three published runs** to go green:

1. Interpreter setup failed — the pinned Python had no Windows build.
2. The suite ran and produced 56 failures with one cause — the runner's
   workspace and temp directories are on different drives.
3. Green on both legs.

Two real faults, neither findable locally, both found in minutes once
published. The local reproduction of fault 2 was only possible *after*
CI named the cause — a `subst` virtual drive reproduced it, but nothing
would have prompted that experiment beforehand.

## Why It Matters

- **Expect a round-trip loop, and plan for it.** A CI change is not
  "done" when the local suite is green; it is done when a run is green.
  Sequence CI edits so the publication cost is paid once, not once per
  defect — and never seal a sprint on the assumption that a CI leg works.
- **Distinguish "authored" from "verified" in the record.** The sprint's
  verify record claimed only the authored leg; when the first run failed,
  that claim needed no retraction. Had it claimed coverage, the seal would
  have been false and the correction would have cost trust, not just a commit.
- **A red CI run after a green local suite is information, not an
  embarrassment.** It is the only instrument that can see this region.
  Treat the first runs of a new CI surface as the execution probe they are.
- **The blind region has an edge worth naming.** Anything whose runtime is
  supplied by someone else's environment — CI runners, hosted actions,
  vendor harness lifecycles — shares this property. The floor can check
  what those files *say*; only publication checks what they *do*.

## The Rule

Before sealing work that changes a surface the floor cannot execute, say so
in the record: what is authored, what is unproven, and what observation
would settle it. Then treat the first published runs as part of the work,
not as an afterthought that follows it.
