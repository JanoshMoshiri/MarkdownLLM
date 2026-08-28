---
id: a-test-anchored-in-source-text-fails-loudly-on-drift-and-silently-on-ambiguity
type: insight
status: active
version: 1.0
created: 2026-08-28
session: 2026-08-28
source: execution
confidence: high
origin: observed
tags: [mutation-testing, evidence, coupling, silent-failure, explorer]
linked_things:
  - id: a-verifier-assumes-the-inputs-it-did-not-observe
    relation: complements
    notes: "That one is about confusing a produced artefact with a consumed input; this is about a check whose target moved while its report stayed green."
  - id: explorer-ui-increment-2026-08
    relation: derived-from
---

# A test anchored in source text fails loudly on drift and silently on ambiguity

## The observation

The Explorer's mutation programme applies each deliberate defect by
string replacement: a mutant names an exact fragment of source, swaps it
for a broken variant, and the oracle must then fail. Two of those anchors
were disturbed by one increment, and the two failures could not have been
more different.

**M21's anchor drifted.** The line it named no longer existed, the runner
could not find it, and it stopped with `mutation target drifted` and the
fragment it wanted. Thirty seconds to fix.

**M07's anchor became ambiguous.** It named `"content": value.content,` —
unique when written. A new encoder branch for historical documents
introduced a second occurrence, earlier in the file. `str.replace(old,
new, 1)` took the first. The mutation still applied, the tests still ran,
and the mutant was still reported *killed* — against a branch its oracle
does not cover. The kill matrix read 21 of 21 while one mutant had
quietly stopped testing the thing it claimed to test.

It surfaced only because the same increment made the *other* branch fail
independently, which forced a look at why M07 survived that run.

## Why the asymmetry is structural, not incidental

An anchor is a **coupling to source text**, and text can move in two ways:

- **It can disappear.** The coupling breaks, the tool cannot proceed, and
  the failure is loud because absence is checkable.
- **It can multiply.** The coupling still resolves — to something else.
  Nothing is absent, so nothing is checkable, and every downstream signal
  stays green.

Only the first has a natural detector. The second requires the tool to
know that the fragment was *supposed* to be unique, which is an intent no
string carries. A count is not a match, and a match is not the match you
meant.

## What generalises

Any check that identifies its target by content rather than by identity
inherits this asymmetry: mutation anchors, `sed` edits in scripts,
snapshot fixtures keyed on a substring, a patch applied by context. The
rule of thumb that follows:

> A textual anchor should assert its own uniqueness. Replacing "find this
> string" with "find this string, and there must be exactly one" converts
> the silent failure into the loud one.

The framework already knows the general shape of this — a restated enum
drifts from its source, a duplicate mapping key resolves by last-key-wins
— but those are about *authored* duplication. This is about duplication
arriving from somewhere else entirely, in a file the anchor's author
never edited.

## What it cost, and what it bought

One mutant testing nothing for the length of an increment, in a programme
whose entire purpose is to prove the tests would notice. The remedy was
to re-anchor on a longer fragment unique to the intended branch. The
cheaper permanent remedy — asserting `count == 1` at application time —
is not yet implemented, and is the obvious next move for this tool.
