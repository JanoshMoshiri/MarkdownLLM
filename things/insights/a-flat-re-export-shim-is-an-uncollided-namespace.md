---
id: a-flat-re-export-shim-is-an-uncollided-namespace
type: insight
status: active
version: 1.0
created: 2026-08-04
session: 2026-08-02
source: build
confidence: high
origin: stated
tags: [floor, architecture, srp-extraction, tests, silent-failure, python]
linked_things:
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: complements
    notes: "Same shape one layer down: there, a generated surface agreed with the builder that was wrong about itself; here, an import surface agreed with whichever module imported last. Both are single-source-of-truth structures with no second opinion."
  - id: srp-extraction-is-tier-promotion
    relation: references
    notes: "The package split that created this shim was right. This is the cost it quietly incurred: one module per reason to change, but one namespace for all of them."
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: informs
    notes: "First occurrence, so this stays an insight rather than a check. A second collision is the admission ticket for a uniqueness self-test over the shim's re-export list."
---

# A Flat Re-Export Shim Is An Uncollided Namespace

## The Insight

`tools/mdllm.py` re-exports roughly eighty names from fourteen modules into one
flat namespace, because that namespace is a contract: the test suite pins
behaviour through exactly those names, and the entry path is invoked by every
domain's AGENTS.md, every installed hook, and every generated settings file.

Python resolves a duplicate import by **last-one-wins, silently**. So the shim
has a property nobody chose: adding a module whose function shares a name with
an earlier module's does not fail, does not warn, and does not even change
behaviour where the new name is used. It changes behaviour **somewhere else** —
wherever the shadowed name was already being called.

## How It Was Found

`calc.py` exported `evaluate()`. So does `triggers.py`. The calc import sits
after the triggers import, so `mdllm.evaluate` silently became the calculation
evaluator, and the trigger evaluator became unreachable through the public
surface — while every calc test passed, because the calc tests were exercising
the name that won.

Three trigger tests went red. That is the whole detection mechanism: not a
linter, not an import error, but the coincidence that some *other* module's
behaviour happened to be pinned through the shadowed name. Had `triggers.evaluate`
been less well tested, this would have shipped, and the failure would have
surfaced as "triggers stopped firing" in a domain, months later, with no
connection to the commit that caused it.

## Why It Matters

The package split (one module per reason to change) was correct and this is not
an argument against it. But it created an asymmetry worth naming:

- **Modules are isolated** — that was the point of the split.
- **The shim is not** — it is a single shared namespace that grows every time a
  module is added, and its collision surface grows with it.

The framework's usual defence against silent drift is that some independent
surface disagrees. Here the only independent surface is the test suite's
coverage of the *shadowed* name, which is coverage of something unrelated to the
change being made. That is detection by luck, and the luck runs out as the
namespace fills.

Note also that the generic name is the dangerous one. `evaluate`, `parse`,
`check`, `build`, `report`, `scan` — the names a well-factored module naturally
reaches for are exactly the names another well-factored module already took.
Good factoring makes collisions *more* likely, not less.

## The Route, When It Earns One

A uniqueness self-test over the shim's re-export list — assert that no name is
bound twice, and fail the build if one is. Perhaps ten lines, and it converts
detection-by-luck into detection-by-construction.

Deliberately **not built yet**: this is the first occurrence, and the framework's
own rule is that repeated drift, not first drift, promotes a fact into the floor.
A second collision is the admission ticket. Until then the fix that shipped is
the honest one — `calc.evaluate` was renamed `evaluate_expression`, which is a
better name anyway and pairs with `evaluate_block`.
