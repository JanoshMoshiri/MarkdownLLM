---
id: judgement-checks-need-a-suppression-list-which-is-itself-drift
type: insight
status: active
disposition: keep-active
disposition_reason: "Standing razor for whether a proposed coherence check belongs in the floor or the human Walk — gates future check proposals; worked example (the v3.17.2 retired-vocab check) is recent and instructive."
version: 1.0
created: 2026-06-28
session: 2026-06-28
source: both
confidence: high
origin: synthesised
tags: [floor, coherence, change-reconciliation, design-principle, false-positives, drift]
linked_things:
  - id: existence-is-not-currency
    relation: complements
  - id: change-reconciliation-specification
    relation: informs
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: complements
---

# A Check That Needs a Suppression List Is Judgement in Mechanical Clothing

## The Insight

The floor earns its authority from one property: a mechanical check **cannot
disagree with truth**. Kernel, derived-index, and domain-kernel drift all compare
the artefact against a *fresh build from the same source*, so the check has no
false positives — it is exactly as right as the generator it shadows. That is what
makes "never re-perform a mechanical check by reasoning" safe.

A check that produces **false positives** has to suppress them somehow, and the
usual move is a hand-maintained **allow / ignore list**. The moment a proposed
check needs one to stay quiet, that is the tell that **it is not a mechanical
check at all** — it is a semantic judgement wearing a mechanical costume, and the
suppression list is the tailoring that makes the costume fit. The judgement did
not go away; it moved into the list.

And the list is the worst kind of drift surface, because it fails **silently**.
An over-broad entry doesn't nag — it *hides*. A suppression rule that was correct
the day it was written goes on quietly asserting "nothing to see here" over a file
where real drift later appears. That is precisely the failure
[existence-is-not-currency](existence-is-not-currency.md) names: an artefact that
*silently claims to be current*. A loud false positive costs a glance; a silent
false negative costs the whole guarantee, and adds a false sense that the human
Walk it was meant to assist is now covered.

## The Razor

When proposing a `coherence` check, ask: **can it be keyed to a same-builder
source, so it cannot disagree with truth?**

- **Yes** → it is floor-shaped. Ship it (e.g. the framework-map subcommand-count
  check is keyed to the live CLI surface; the broken-body-reference check would be
  keyed to the live id-set). No suppression list, because there are no false
  positives to suppress.
- **No — it needs an allow list to stay clean** → it is not floor-shaped. The
  judgement is irreducible; it belongs to the **human Walk**
  ([change-reconciliation.md](../../change-reconciliation.md)), not the floor.
  Do not police it; document the discipline instead.

## Why It Matters — The Worked Case

This razor was paid for. The v3.17.2 **retired-vocabulary check** (`retired_terms`
in `_schema.yaml`) tried to mechanise "a retired artefact's dead name reappears
live in prose." But "the retired `continuity.md`" (correct) and "lives in
`continuity.md`" (drift) are the *same characters* — the difference is semantic.
To reach a clean baseline it needed an `allow` list of ~15 ids/paths, several of
them broad enough to silence future drift in whole specs. It was reverted in
v3.17.3 by exactly the principle that retired the WORKLOG: **delete the thing that
needs policing; don't police it.** What replaced it was free and complete — an
explicit pointer that an inflection walks the *whole* corpus, insight things
included.

The general shape: [repeated-drift-promotes-a-fact-into-the-floor](repeated-drift-promotes-a-fact-into-the-floor.md)
says *mechanise recurring drift* — but only where the fact has a mechanical
source. This is its precondition, the boundary on the same idea: drift that can
only be adjudicated by reading meaning is not a floor candidate no matter how
often it recurs. Recurrence is necessary, not sufficient; **same-builder
checkability** is the gate.

## Context

Synthesised 2026-06-28 from the operator's own pushback during the v3.17.x
reconciliation. After building the retired-vocab register, the operator's instinct
was that it "had done nothing but add more of a drift surface," and that a plain
documentation pointer "holds more weight and doesn't come with a drift surface."
Naming *why* — the suppression list is the confession that the check isn't
mechanical — turned a felt unease into a reusable gate for the next proposal.
