---
id: a-value-cannot-recover-its-own-spelling
type: insight
status: active
version: 1.0
created: 2026-09-11
session: 2026-09-09
source: agent
confidence: high
origin: inferred
disposition: keep-active
disposition_reason: "Standing razor for any check that compares a YAML scalar as text — a pin, an id, a code: normalise at the parse seam by retaining the token, never at the comparison seam by recomputing it."
tags: [yaml, lexeme, pins, floor, comparison, razor]
linked_things:
  - id: thing-specification
    relation: informs
    notes: "Why the kernel's 'exact decimals start from the authored lexeme' rule is not calc-specific: the same loader now keeps int tokens for the reference triple's pin."
  - id: provenance-specification
    relation: informs
    notes: "The cross-domain pin is compared as text; v3.38.1 compares its YAML token, so a short pin that types as octal or binary still matches its source."
---

# A Value Cannot Recover Its Own Spelling

## The Insight

When a scalar's *spelling* is what carries meaning — a commit pin, an
identifier, a code with leading zeros — parsing it into a value is lossy in
one direction only: the value can always be re-spelled, but not always as
the spelling it came from. `2399917` survives the round trip; `0123456`
becomes 42798 and `0b00101` becomes 5, and no `str()` of those integers is
the pin. So a guard that "normalises" at the comparison seam by recomputing
text from the value is complete only for the spellings the value happens to
reproduce. The cure has to sit at the seam that still holds the token — the
parser — and keep it beside the value.

## Why It Matters

The floor had already learned this once, for floats: `LexicalFloat` keeps
the authored decimal so `mdllm calc` never reasons from a rounded binary.
It had not generalised the lesson, so `_pins_match` (v3.27.0) fixed the
decimal-int case with `str()` — which reproduces decimal — and its own
docstring recorded CI flaking on that class. The octal and binary spellings
were the same disease with a non-invertible symptom, latent for six weeks
at one draw in 1069, until the 3.38.0 push drew it on the Linux leg. The
fix that closes the class is the one that does not know which spellings
exist: retain the token (`LexicalInt`), read the token (`scalar_lexeme`),
compare the token. A value-level patch would have cured one more spelling
and left the next.

## Context

Reproduced through the project's own loader (exhaustive over the octal and
binary classes; 187 failures in 200,000 random 7-hex draws) before the fix
was written; deterministic regressions cover every former failure spelling
so the proof no longer depends on a lucky hash. Landed as `2da4d17`,
released 3.38.1. The same draw at `0000000` typed as a falsy zero and filed
a fully-declared import as "incomplete" — presence, too, must be the
token's, not the number's.
