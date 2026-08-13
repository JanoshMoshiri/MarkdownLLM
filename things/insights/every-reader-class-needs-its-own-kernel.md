---
id: every-reader-class-needs-its-own-kernel
type: insight
status: active
version: 1.0
created: 2026-08-13
session: 2026-08-13
source: both
confidence: high
origin: synthesised
tags: [accessibility, derivation, kernel, entry-cost, documentation, fractal]
linked_things:
  - id: public-docs-face-is-derived-not-restated
    relation: informs
    notes: "The decision this generalises. It ruled the public surface must be derived; this names why the same shape keeps recurring and what selects it."
  - id: a-generated-surface-collapses-its-walk
    relation: informs
    notes: "The cost model underneath. Accessibility metadata is the highest-restatement-count content in any corpus, so it is the first thing to drift when authored."
  - id: operative-rules-are-a-small-fraction-of-spec-prose
    relation: supports
    notes: "The measurement that produced the agent's kernel — the first instance of this pattern, built for a different reason entirely."
  - id: a-true-primitive-is-discovered-not-authored
    relation: supports
    notes: "Two unrelated pressures — session cost and screen-reader entry — independently selected the same primitive. That is the discovery test passing."
---

# Every Reader Class Needs Its Own Kernel

## The Insight

A reader who cannot hold the whole corpus needs a **derived entry surface**,
not an authored summary. The framework already built one — `kernel.md`, for the
agent, because 350KB of spec will not fit a session. Human accessibility is the
same constraint met by a different reader class, and it takes the same answer.
The recurring primitive is not "documentation"; it is **entry cost** — and
derivation is what makes it affordable to solve more than once.

## Two Names For One Constraint

- **Self-documentation:** one truth, everything else derived → *reconciliation
  cost*.
- **Accessibility:** the reader must enter, navigate, and leave with what they
  came for, whatever their means of reading → *entry cost*.

They are the same constraint approached from opposite ends. An accessible
surface is never one document — it is one truth rendered several ways: an
outline, a nav, a search index, a linear reading order, a screen-reader
description, a small-screen layout, a plain-text fallback. Every one of those
renderings is a restatement if authored and free if derived.

Which explains a failure everyone has seen and nobody has named: hand-maintained
accessible doc sets rot faster than the docs they serve. Accessibility metadata
carries the highest restatement count of any content in a repository — one per
diagram, per heading, per label — so by
[[a-generated-surface-collapses-its-walk]] it drifts earliest and is re-walked
last.

## The Consequence

**Accessibility is a property of the source's structure, not of the published
page.** A build can add nav, search, skip links, sensible measure, and
`prefers-color-scheme`. It cannot invent a document outline that is not in the
headings, alt text that is not in the source, a reading order for a table that
is really a diagram, or a shorter specification. So the entry surface has to be
*generated from tracked state*, exactly as `mdllm kernel` is — and drift-gated
the same way `kernel --check` gates its predecessor.

## Why This Is A Fractal, Not An Analogy

`kernel.md` was never built as an accessibility artifact. It was built because a
session cannot afford the full spec load
([[operative-rules-are-a-small-fraction-of-spec-prose]]). The human case arrived
from an unrelated direction — a screen reader meeting a 48KB file in a blob view
with no persistent nav — and landed on the identical primitive: extract the
operative content mechanically, regenerate on change, gate the drift.

A primitive selected independently by two pressures that share no lineage is
*discovered*, not authored ([[a-true-primitive-is-discovered-not-authored]]).
That is the same test the framework's other atoms passed, and it is why the
recurrence is worth carrying as its own insight rather than as a note on the
publishing decision.

## How To Apply

When a new reader class appears — a screen reader, a phone, a cold evaluator, a
second-vendor agent, a future harness, a reader with no clone — do not write it
a guide. Ask **what tracked state already holds this answer**, and derive that
class's entry surface from it.

Authored entry surfaces remain legitimate in exactly one case: where no source
exists to derive from. `docs/first-hour.md`'s paced sixty minutes and
`docs/estate-mechanics.md`'s synthesis across four specs are both genuinely
unowned elsewhere, and both earn their place. Every authored surface beyond that
is walk debt, and should be counted as such at the moment it is written rather
than discovered at the next release walk.
