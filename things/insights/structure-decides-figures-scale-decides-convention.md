---
id: structure-decides-figures-scale-decides-convention
type: insight
status: active
version: 1.0
created: 2026-06-17
confidence: medium
origin: synthesised
source: session — sleeping-bag-fac 2×2 (2026-06-16/17, 20 trials + smoke, one leaked trial excluded)
session: 2026-06-17
tags: [evals, stage-2, structure-beats-scale, reasoning-discriminator, manifesto]
linked_things:
  - id: first-2x2-measured-convention-following-not-reasoning
    relation: supersedes
  - id: withholding-is-not-isolation
    relation: complements
  - id: mis-keyed-links-pass-the-floor-silently
    relation: supports
  - id: llm-driven-systems-manifesto
    relation: references
---

# The FAC 2×2: Structure Decided The Reasoning, Scale Only The Convention

## The Insight

The `vat-quarter-basic` 2×2 saturated — every cell got the figures right, so it
measured convention-following, not reasoning
([[first-2x2-measured-convention-following-not-reasoning]]). The
`sleeping-bag-fac` fixture was built to fix exactly that: an *unleakable*
synthetic rule (the fictional Tarn & Fell coefficients) so the condition-neutral
figures can only be produced by reading the method. It worked. The clean cells:

| model | condition | figures correct | fully passing | note |
|---|---|---|---|---|
| haiku | framework | **5/5 every trial** | 0/6 | links mis-keyed |
| haiku | bare | **0/5** | 0/6 | nothing, or confidently wrong |
| opus | framework | **5/5 every trial** | 5/5 | links canonical |
| opus | bare | **0/5** | 0/4 | all produced nothing |

(One opus-bare trial that breached the control is excluded — see
[[withholding-is-not-isolation]].)

Two clean reads:

1. **Condition decided the reasoning; model tier did not.** Both framework
   models got every figure right, every trial, every trap (hammock inversion,
   snow threshold, `ceil(1.5)=2`, full-800m increments). Both bare conditions
   got zero — producing nothing, or, when haiku fabricated, numbers that were
   confidently and entirely wrong (−19, −20, −11…). The structure supplies the
   definition; without it the task is unanswerable. This is the manifesto's
   reworded thesis in one result: *the processor is not asked to invent the
   system and reason within it at once.*

2. **Model tier showed up only in the convention layer.** Scale made no
   difference to the figures, but it decided whether the agent wrote canonical
   `linked_things` (opus, 21/21) or invented a `relations:` key the floor
   silently ignores (haiku, 16/21 — see
   [[mis-keyed-links-pass-the-floor-silently]]). That is exactly where the
   manifesto (v2.4) now places model-tier superiority: a secondary *corollary*,
   not the spine.

## Why It Matters

This closes the loop the first 2×2 opened. The reasoning discriminator the
manifesto's claim needed now exists and discriminates cleanly: structure is the
deciding variable for correctness, model tier is secondary and lands in
convention-adherence. It strengthens the **thesis** (structure supplies the
domain definition) far more than the demoted **model-tier corollary**, which is
the correct emphasis after the v2.4 reframe.

The honest boundary: this is one fixture, single-shot, and the result is about
*information availability* (the rule lives only in the structure) as much as
reasoning quality — which is precisely the framework's pitch, so the framing is
fair, but it is not yet the *longitudinal* test of drift-resistance the thesis
also claims. The figures axis is condition-neutral and unaffected by the one
excluded leak; the cross-session test remains future work.
