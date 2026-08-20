---
id: floor-structure-residue
type: plan
status: not-started
version: 1.0
created: 2026-08-20
priority: medium
tags: [clean-architecture, solid, tests, ci, perimeter, refactor, review-residue]
linked_things:
  - id: independent-substrate-review-2026-08-20-claude
    relation: derived-from
    notes: "The review that found each item; its clean-architecture section is this plan's specification."
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: implements
    notes: "The fitness suite's curated allowlist is that blindness in the one place that checks the code itself."
  - id: srp-extraction-is-tier-promotion
    relation: references
    notes: "The god-module and monolith items are that pattern's next instances."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "A single-platform CI beneath the most platform-sensitive machinery is the insight unapplied to the substrate's own pipeline."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "Substrate code changes are read against that governance surface before they are written, not retrofitted after."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Any new mdllm coherence check named here belongs there, under its suppression-list gate — this plan proposes none of its own."
  - id: cumulative-drift-is-invisible-to-per-change-walks
    relation: supports
    notes: "The perimeter restatements below are fresh evidence for the razor: they sat outside every individual blast radius and were found by a cold read."
---

# Floor Structure Residue

Structural and perimeter debt named by the 2026-08-20 independent review. None
of it is a behavioural defect — the floor's guarantees hold. Each item is a cost
the *next* change pays: a duplicated adapter the fourth harness inherits, a gate
that does not cover new modules, a monolith that blocks its own decomposition.

Ordered by leverage, not by size.

## Structure

1. **Invert the fitness suite's vendor gate.** Its structural rules are derived
   and total; its vendor-vocabulary gate runs over a hand-curated list of
   neutral modules, so a newly added neutral module is born ungated — several
   already are. Gate everything outside the adapter package, with documented
   exceptions. This is the highest-leverage item here: it is the check that
   protects every other structural claim.
2. **Collapse the duplication between the two project-bound adapters.** Quoting,
   output-envelope formatting, definition hashing, handler construction and
   probing are near-identical in both. A shared project-hook helper collapses it
   without breaching the rule that vendor vocabulary lives only in adapters —
   the shapes are identical *because* the harnesses converged, and the
   duplication is the rule's unpaid cost.
3. **Move the hook byte contract out of the birth module.** Diagnostics import
   scaffold solely to reach hook bodies and the resolved hooks directory; a leaf
   contract module already exists as the right home. One wrong-direction edge,
   one small move.
4. **Extract a shared test fixture module, then split the monolith.** Three test
   files import helpers from the largest test file, so it cannot be decomposed
   until the shared setup has a home of its own. After that the membrane, sync
   and session-gate sections are coherent files waiting to be lifted out along
   banners that already exist.
5. **Prune during the worktree walk.** Worktree-mode listing enumerates the
   entire tree before exclusions apply, so an interactive command in a working
   checkout pays a walk proportional to everything nested beneath it rather than
   to the corpus. The hook path is index-native and unaffected; the cost lands
   on the commands an operator runs by hand.
6. **Widen the CI matrix, or say why not.** The substrate's most
   portability-sensitive machinery — the Windows command carriers, the shell
   resolver, the line-ending contract — is exercised on one platform only. Either
   the matrix grows, or the limitation is recorded where a portability claim
   would otherwise be read as covering it.

Smaller, same family: two copies of the staged-atomic-write primitive; a
diagnostic that recovers its own floor's result by matching report prose rather
than a structured fact; two adapter inspectors that classify by resemblance to a
path string; dependency pins restated by hand in a bundle template beside the
file that owns them.

## Perimeter

Hand-restated facts that a per-change walk did not reach. The
2026-08-20 dark-region reconciliation closed several; these survived it:

- the calculation reference still states an unevaluable derivation is *always* a
  warning, which strict mode has made an Error (its sibling lexeme claim was
  corrected in that same walk);
- this repository's own installed session-closing commands still teach
  publication as default-on, which the templates already corrected — the
  framework's own ritual currently teaches reversed doctrine;
- the decision template and its worked example still teach abbreviated pins
  against the full-commit rule.

These are cheap to correct and are also the standing argument for the
perimeter-currency check: a cold read found them, and a cold read is the
instrument this class is currently protected by.

## Done when

- [ ] The fitness gate covers by default and excepts by declaration.
- [ ] Items 2–5 are landed or explicitly ruled not-worth-it, in writing.
- [ ] The three perimeter restatements are corrected at their source surfaces.
- [ ] Any check this work argues for is routed to the coherence backlog rather
      than built here.
