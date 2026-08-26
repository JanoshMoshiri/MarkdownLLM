---
id: a-transcribed-identifier-is-unverifiable-by-reading
type: insight
status: promoted
version: 1.1
created: 2026-08-26
session: 2026-08-25/26
source: build
confidence: high
origin: stated
promoted_to: workflow-state-specification
tags: [provenance, pins, transcription, floor, failure-modes]
linked_things:
  - id: workflow-state-specification
    relation: informs
    notes: "Revision binding now requires log-transcribed full SHAs and the floor resolves the commit plus governing definition; the workflow-specific lesson has crystallised into the operative contract."
  - id: a-wrong-sum-is-indistinguishable-from-a-right-one
    relation: supports
    notes: "The same failure shape on a different surface — an output whose correctness has no surface features. The remedies diverge, which is the useful part: a sum must refuse, a pin can simply be resolved."
---

# A Transcribed Identifier Is Unverifiable By Reading

## The Insight

Writing a provenance pin, I produced a full SHA from memory rather than
from the log. It was wrong. It was also **completely convincing**: forty
hex characters, the right prefix, the right shape, sitting in the right
field of a thing that validated clean. It survived a commit. It was
caught only because a later pin sent me back to `git log`, where the
tails disagreed.

This is `a-wrong-sum-is-indistinguishable-from-a-right-one` on a
different surface. A number carries no evidence of the denominator it was
drawn from; an identifier carries no evidence of the object it was drawn
from. Both are outputs where reading tells you nothing, so the only
evidence of correctness is the process that produced it.

## Where The Two Diverge

The remedies are **not** the same, and the difference is worth holding:

- **A sum cannot be checked after the fact** — the inputs are gone. So
  the floor must *refuse* rather than approximate.
- **A pin can always be checked** — git holds the answer, permanently and
  cheaply. So the floor should *resolve* it, at the commit boundary,
  rather than trusting the transcription.

An identifier that a machine could resolve and a human must instead
proof-read is a check waiting to be built, not a discipline waiting to be
taught.

## The Discipline Until Then

**Pins are transcribed from the log, never recalled.** Read the SHA in
the same action that writes it. The rule is in `workflow-state.md`'s
activation section for exactly this reason — and the sprint that wrote
that section is the sprint that broke the rule while writing it, which is
the strongest argument available that the discipline alone is not enough.

## Provenance

2026-08-26, mid-sprint, on `run-operating-model-seams-2026-08`'s own
`informed_by` pin. Corrected in its own commit; the floor leg that would
have caught it mechanically sits in the same sprint's stretch scope.

## Disposition

**Promoted (operating-model seams seal, 2026-08-26).** The workflow-specific
lesson is now operative in `workflow-state.md`: pins are transcribed from Git,
the floor resolves the object and definition, and the self-application plus
worked example exercise the rule. The broader provenance validator already
checks commit/input resolution; no second mechanism or open insight is owed.
