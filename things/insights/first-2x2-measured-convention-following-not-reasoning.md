---
id: first-2x2-measured-convention-following-not-reasoning
type: insight
status: active
version: 1.0
created: 2026-06-11
confidence: medium
origin: synthesised
source: session — first full 2×2 run (vat-quarter-basic, 20 trials)
session: 2026-06-11
tags: [evals, stage-2, structure-beats-scale, fixture-design, experiment-validity]
linked_things:
  - id: fixture-fixes-correct-bugs-not-difficulty
    relation: extends
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: supports
---

# The First 2×2 Measured Convention-Following, Not Reasoning

## The Insight

The first full structure-beats-scale 2×2 (haiku/opus × framework/bare, 5
trials/cell, vat-quarter-basic, 2026-06-11) produced a clean-looking table:

| model | condition | fully passing | assertion pass rate | mean cost $ |
|---|---|---|---|---|
| haiku | bare | 0/5 | 86% | 0.070 |
| haiku | framework | 3/5 | 94% | 0.096 |
| opus | bare | 1/5 | 89% | 0.417 |
| opus | framework | 5/5 | 100% | 0.858 |

But the designed discriminator never discriminated: **all 20 trials in all
four cells got the financial figures right** (output 2500 / input 380 / net
2120), including the blocked-entertainment-VAT trap. Status, existence, and
validation assertions also passed everywhere. Every point of variance in the
entire experiment was the single `has-deadline` link assertion — which the
evals/README fairness note already flags as asymmetric by construction (the
link contract is stated in the framework's AGENTS.md but not in the bare
preamble).

So as run, the experiment measured *convention-following under structure*,
not *domain reasoning under structure*. The fixture's reasoning core
saturated: 2026 models, even small ones with no framework, handle a
single-quarter VAT calculation with one trap.

## What the Data Does Support

- **Determinism at the top cell:** opus+framework was the only perfectly
  deterministic cell (5/5 at 7/7, 100%). Structure converts a capable model
  from "usually right" to "reliably right" — consistent with the framework's
  actual pitch.
- **The diagonal, weakly:** haiku+framework (94%, 3/5 perfect, $0.096/trial)
  edged opus+bare (89%, 1/5 perfect, $0.417/trial) at ~23% of the cost — the
  manifesto's direction, but the margin is one asymmetric assertion at n=5
  on one fixture. Directional, not decisive.
- **Framework uplift scaled with capability** (haiku +8pts, opus +11pts to
  ceiling), and framework did *not* make haiku deterministic (2/5 trials
  still missed the link despite AGENTS.md documenting it).

## Why It Matters

The manifesto's declarative claim ("a smaller model operating within a
well-defined system will outperform a larger model operating without
structure") is **not yet supported by this experiment** — not because the
data contradicts it, but because the fixture couldn't put the claim under
load. Two consequences:

1. **Claim language should match evidence state:** tested-hypothesis framing
   with first results reported transparently, not settled fact.
2. **The next fixture must make the condition-neutral core discriminate:**
   harder reasoning (partial exemption, multi-quarter with conflicting or
   duplicate records, an amendment/belief-revision flow, distractor things)
   where bare models plausibly get *figures* wrong, so the framework's
   contribution to reasoning — not just to schema conventions — is what's
   measured.

Per [[fixture-fixes-correct-bugs-not-difficulty]], the haiku/framework link
misses stay unpatched: opus+framework passing 5/5 with identical AGENTS.md
is the control proving the instructions are followable — the gap is model
capability under load, which is the measurement, not a documentation bug.

## Context

Run 2026-06-11, ~$7.2 total spend, 20 valid trials. The pre-fix smoke run
(20260611-125556, scored 1/7 against the self-inconsistent fixture before
the id-template and Windows CLI fixes) was moved to
`evals/runs/_excluded-pre-fix/` — it measured a different fixture through a
broken runner. One opus/bare trial spontaneously created the has-deadline
link with no framework present; spontaneous structure is part of what the
fairness note says the asymmetry measures.
