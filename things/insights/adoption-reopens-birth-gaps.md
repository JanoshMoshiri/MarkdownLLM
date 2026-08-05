---
id: adoption-reopens-birth-gaps
type: insight
status: active
version: 1.0
created: 2026-08-05
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Standing rule for every future opt-in transition (kernel adoption, unpark, un-dormant): re-run the withheld-capability list before declaring the transition done. Stays active until the transition rituals carry the re-check themselves."
tags: [rulings, preconditions, backfill, kernel-shape, drift]
linked_things:
  - id: a-ruling-triages-more-cheaply-than-a-mechanism
    relation: extends
    notes: "The cheap ruling has a maintenance cost this names: a ruling is predicated on its subject's state, and the subject can change out from under it silently."
---

# Adoption reopens birth gaps — a withheld capability must be re-delivered when the withholding rationale dies

## The Insight

A capability deliberately withheld under a recorded rationale becomes a
silent defect the moment the rationale stops being true — and nothing
re-checks rationales.

The lived case: on 2026-08-01 three domains outside the kernel shape were
refreshed *without* the reasoning prompts, with the reason recorded in the
commit — "this domain opted out of managed blocks and never referenced them;
delivering them would manufacture usage." Correct that day. On 2026-08-04
one of them **adopted** the kernel shape (itself a good, recorded ruling) —
and instantly became a domain whose generated session-start block names
eight prompts it does not possess: the exact born-incomplete defect class
v3.24.0 eliminated for newborns, re-created by a transition, invisible to
validate, coherence, and doctor alike, because every check saw a valid state
and none saw the *pair* (blocks that name prompts + no prompts directory).

## The general form

Rulings carry preconditions the way triggers carry conditions — but triggers
are re-evaluated and rulings are not. Any transition that changes a
domain's shape (adopt, unpark, resume from dormancy) re-opens every ruling
predicated on the old shape. The transition is precisely the moment to
re-run the withheld list: what did this domain *not* get because of what it
used to be?

Mechanical corollary, deliberately unbuilt for now: `domain-kernel` could
refuse-or-warn when writing a session-start block that names prompts absent
from the domain (same-builder — it generates the names it would check).
One defect class observed once; the ruling threshold
(repeated-drift-promotes-a-fact-into-the-floor) is a second occurrence.
