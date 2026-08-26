---
id: a-verifier-assumes-the-inputs-it-did-not-observe
type: insight
status: active
version: 1.0
created: 2026-08-26
session: 2026-08-26
source: build
confidence: medium
origin: stated
tags: [review, verification, builder-verifier, handover, provenance, failure-modes]
linked_things:
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: extends
    notes: "That one separates builder from checker. This names what the separation still does not cover: the checker may have authored the handover, and will then verify the build against the brief it *intended* rather than the one that was sent."
  - id: a-transcribed-identifier-is-unverifiable-by-reading
    relation: complements
    notes: "Same family — a claim that looks identical whether true or false. There, an identifier written from memory; here, an input asserted from memory of having produced one."
---

# A Verifier Assumes The Inputs It Did Not Observe

## The Insight

A verification record was committed stating that a four-line handover
prompt carried a cross-harness build, and citing that brevity as evidence
of the framework's portability. The claim was false. The operator had
sent a substantially longer, directed brief; the four-line version was
merely the one the verifier had *drafted* in an earlier session.

Nobody lied and nothing was careless. The verifier confused **the
artefact it produced** with **the input that was consumed** — two things
that feel like one when you authored the first and never saw the second.

## Why The Builder/Verifier Split Did Not Catch It

The split was real: the build was executed by a different agent in a
different harness, and the verification attacked it adversarially. But
the same agent had *designed* the sprint and *drafted* the handover. The
separation covered the build; it left the **inputs** uncovered, and the
verifier had a memory in place of an observation exactly where evidence
should have been.

This is the specific residue the builder/verifier doctrine does not
address: separating who builds from who checks says nothing about who
briefed. A designer-verifier can faithfully confirm that a build matches
a design while being the last party able to notice that the build was
briefed from something else.

## The Discipline

**A review states its inputs as observations or not at all.** If the
verifier did not see the prompt, the environment, or the inputs the
builder actually consumed, the record says so — or asks for them before
making claims that rest on them. The tell is a sentence in a review about
something the reviewer never opened.

Cheap corollary, since the cost here was one false published claim
caught only because the operator volunteered the real prompt: when a
review's conclusion turns on an input, **ask for the input**. The
operator has it; the repository usually does not.

## Provenance

2026-08-26, seams verification. The false claim was committed, corrected
the same day when the operator supplied the actual prompt, and the
correction turned out to be the most useful part of the review — the real
prompt explained both defects the review had recorded as unexplained.
Confidence is medium on one instance; a second would settle it.
