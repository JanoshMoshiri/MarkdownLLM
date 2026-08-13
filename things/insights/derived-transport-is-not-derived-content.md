---
id: derived-transport-is-not-derived-content
type: insight
status: active
version: 1.0
created: 2026-08-13
session: 2026-08-13
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Parked deliberately. The follow-on generation work (--help into the toolbox table, frontmatter into the spec graph, evidence records into a verified-versus-designed-for page) is not a plan thing yet, and the docs surface is held by a concurrent session. Attach both insights to that plan when it is written."
tags: [derivation, publication, drift, membrane, documentation, restatement]
linked_things:
  - id: public-docs-face-is-derived-not-restated
    relation: informs
    notes: "The decision that satisfies the transport axis cleanly and leaves the content axis open. This insight names the split so the second half does not read as already done."
  - id: a-generated-surface-collapses-its-walk
    relation: informs
    notes: "Restatement count is reconciliation cost — the content axis IS that cost. Transport-derivation does not reduce it by a single walk step."
  - id: every-reader-class-needs-its-own-kernel
    relation: complements
    notes: "Read together: that insight says derive the entry surface; this one says check which half of 'derived' you actually achieved."
  - id: provenance-specification
    relation: references
    notes: "Cross-Domain Imports already splits these axes mechanically — stale is transport, diverged is content — which is the strongest evidence the distinction is real."
---

# Derived Transport Is Not Derived Content

## The Insight

"Derived" splits into two independent axes:

- **Transport** — the copy the reader sees regenerates from tracked state
  rather than being a hand-kept parallel copy.
- **Content** — the state itself is derived from a single owner rather than
  hand-restated from a truth owned elsewhere.

A surface can satisfy one and fail the other. The trap is that **satisfying
transport reads as satisfying both**, because the visible failure mode of a
stale copy disappears while the invisible one — words restating an upstream
owner — survives untouched.

## Three Instances, Already In The Corpus

**The membrane.** `mdllm imports-check` returns two failure directions and
refuses to collapse them: `stale` means the source moved under the pin
(transport), `diverged` means the pin is current but the mirror's content no
longer matches the face (content). The framework worked out this split for
cross-domain imports and mechanised it. It is the same split.

**Publication.** `autopush` transports floor-validated commits, and the
invariant `estate-mechanics.md` states beside it is that autopush *accelerates
transport, never trust*. Validation is structural; it says nothing about whether
the content restates a truth that another surface owns.

**The public docs face (the occasion).** Pages-from-`/docs` derives the site
from the commit — same repo, same hook, same boundary check, same CI. Transport:
satisfied, and the wiki was correctly ruled out for failing exactly this axis.
But the content inside `docs/` is itself hand-restated: `operator-guide.md`'s
toolbox restates `mdllm --help` across roughly twenty-eight rows, and
`framework-map.md` Views 2 and 3 restate `linked_things` frontmatter and that
same `--help`. So the chosen face publishes the corpus's *most*-restated layer,
while its least-restated layer — `kernel.md`, `--help`, `.markdownllm`, the
frontmatter graph — stays unpublished.

## Why It Matters

The tool already learned this lesson inside itself and the guides did not
inherit it. `mdllm --help` stopped claiming completeness after a review-loop
finding caught it describing twelve of twenty-six subcommands under an
unqualified heading; its own text now records the rule — *a hand list drifts;
argparse does not*. That is the content axis, correctly diagnosed, in the one
place it was cheap to see.

Transport-derivation is the cheap half and it feels like the whole job. The
expensive half is asking, per surface, whether the words themselves have exactly
one owner — and that question does not get easier by publishing well.

## How To Apply

Two questions per published surface, never one:

1. **Does this regenerate?** (transport)
2. **Does what it says have exactly one owner?** (content)

Yes to the first and no to the second is the dangerous state: it reads as safe,
passes every mechanical check, and drifts anyway. When a surface fails the
second question and a mechanical source exists, promote the restatement into
derivation — `--help` into the toolbox table, frontmatter into the spec graph,
evidence records into a verified-versus-designed-for page. Where no source
exists, the restatement stands and is counted as walk debt.

## One Live Open Question, Surfaced Not Resolved

[[public-docs-face-is-derived-not-restated]] parks the public *selector* as
"only real once something outside `docs/` wants publishing." Its own
accessibility section names `orchestration.md` (48KB), the manifesto (41KB), and
`domain-specification-guide.md` (40KB) as the entry problem — and all three sit
at root, outside `docs/`, where the largest file is 25KB. The accessibility
argument therefore motivates publishing precisely the files the chosen selector
excludes, which makes the selector question real now rather than later.

That is an operator call about scope, not a defect in the ruling. Recorded here
so it is a decision when it is taken, rather than a discovery at the first
release walk.
