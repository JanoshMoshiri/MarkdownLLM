---
id: an-adversarial-review-loop-converges-on-its-own-fix-residue
type: insight
status: active
version: 1.0
created: 2026-08-11
session: 2026-08-11
source: both
confidence: high
origin: inferred
exposed: true
disposition: keep-active
disposition_reason: "Dismiss when the mechanical restatement checks (mechanical-coherence-checks-backlog) have landed AND a subsequent post-release cold read returns zero fix-residue-class findings — at that point the claim is absorbed into practice. Until then this is the standing argument against re-running review loops and for the derivation build."
linked_things:
  - id: mechanical-coherence-checks-backlog
    relation: informs
    notes: "The build this insight argues for, with 44 data points: mechanical restatement checks would have prevented or caught roughly three-quarters of the loop's findings, including every round-8 finding."
  - id: external-review-response-2026-08-10
    relation: informs
    notes: "Supplies the measured answer to that plan's open R3 (cold-read cadence): one cold read after a substantial release earns its cost — rounds 1–3 prove it; a loop past that point decays into self-measurement. The cadence decision stays the operator's; this is its evidence."
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: supports
    notes: "The loop is that insight's rule measured at scale: 8 rounds, 44 findings, and the surviving defect class was in every case a fact restated by hand where the floor owns nothing."
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: supports
    notes: "The asymptote claim, now with a decay curve: finds 6→7→6→6→7→4→3→3, severity falling faster than count, fix-residue share rising 1/6 → 1/3 → 3/3. Zero is not a reachable state; the rate is what the mechanism must own."
---

# An adversarial review loop converges on its own fix residue

Eight cold, unprimed, tier-order coherence reviews were run in a loop against
this substrate (2026-08-10 → 2026-08-11), each against the HEAD the previous
round's fixes produced. Full protocol and data:
`reviews/REVIEW-loop-2026-08-10.md`. Forty-four confirmed contradictions were
found and fixed; the floor stayed green throughout. The loop still could not
terminate — and the reason is the finding.

## The mechanism

A fact restated on N surfaces and corrected on k of them leaves N−k live
contradictions, now split *against the correction*. Nothing enumerates the
sibling surfaces, so every multi-surface prose fix carries residual
probability — and the corrections are made of the same material as the
defects. Measured across the loop: fix-residue was 1 of 6 findings in round
4, 1 of 3 in round 7, and 3 of 3 in round 8. By the eighth round the
instrument was no longer measuring the substrate's original drift; it was
measuring the incompleteness of its own repairs. A loop with that property
does not converge to zero. It converges to self-measurement at constant
cost.

Three corollaries, each carried by the data:

1. **Author-blindness is real**: the loop found 44 contradictions a full
   author sweep had just missed, several adjacent to the author's own edits.
   Cold reads and author walks catch disjoint sets — which is why the first
   cold read after a big change is cheap insurance.
2. **Value decays faster than count**: rounds 1–3 found behavior-shaping
   defects; rounds 7–8 found label precision and scatter. The economic case
   for a loop ends after the early rounds.
3. **Derived surfaces never appeared in any round's findings.** Eight
   adversarial readers each independently verified the kernel, the managed
   blocks, the catalogs, and the censuses clean, while hand prose failed
   every round. The control group could not be cleaner.

## The rule

Looping a review is a **measurement instrument, never a resolution
mechanism**. When a review finds a restated fact drifted, the fix priority
is: *delete* the restatement (defer by reference) · *derive* it (generated
surface) · *check* it mechanically at the commit boundary · and only as a
last resort correct the prose in place — and a prose correction that adds
explanatory annotation has added new restatement surface, not removed any.
Cold reads earn their cost as a **post-release ritual**, once, while the
findings are still behavior-shaping — not as a loop chasing a
contradiction-free state that the substrate's own doctrine says is not a
state at all.

## Why this is on the porch

Every domain in the estate maintains prose that restates facts owned
elsewhere — registers, kernels, skills, guides. Any of them could burn the
same tokens rediscovering this curve. The record and the rule travel
together: measure once, then build the mechanism.
