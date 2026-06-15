# Evidence — Closing the Meta-Risk

<!-- A human-facing README (skipped by `mdllm validate`, like every README.md).
     The records produced under it ARE validated things. -->

## Why this directory exists

The framework's strongest evidence — independent cold adoption, sustained real-world use, a downstream marketed MVP — lives entirely *outside* the repository. A cold evaluator (a prospective adopter, a sceptical colleague, an automated review before the author supplies context) sees a self-referential spec corpus that appears never to have touched a real problem. For a framework whose whole ethos is *transparent, auditable, self-describing*, making the case for its own maturity by word of mouth is the sharpest gap the 2026-06-15 independent review found ("The Meta-Risk").

This directory is where that evidence is brought *into* the artifact — sanitised, with all domain-specific and private content stripped — so the repo itself can show what it has done, not just what it claims.

## The two-tier plan

The evidence is built in two tiers, lowest disclosure-risk first (review action #4 → Option B now, Option A when cleared):

1. **Shape-only record (low risk, buildable now).** A real adoption or workflow abstracted to its *shape*: the stage graph, which primitives carried which load, what broke, what was missing, what was fixed — with zero identifying content. Uses `sanitised-validation-record.template.md`. This is mechanically natural now that `workflow-state.md` exists: the shape *is* a redacted `workflow-definition`.
2. **Narrative case study (higher risk, needs disclosure approval).** The cold-start written up as the eval it actually was — problem, incumbent tool displaced, what broke, what was fixed, that it sustained to a marketed MVP. This requires an explicit decision from the author (and the operator) on what may be disclosed. **Held until that conversation has happened.** Do not author it from assumption.

The shape-only record is a strict subset of the narrative, so building tier 1 first wastes no work.

## Disclosure discipline

- Nothing here may name the operator, their client(s), the product, or any domain-specific data.
- When in doubt, abstract harder or leave a placeholder — an empty placeholder is honest; an invented detail is not.
- The shape (stage graph, primitive load-bearing, gaps) is disclosable; the *content* flowing through the shape generally is not.
