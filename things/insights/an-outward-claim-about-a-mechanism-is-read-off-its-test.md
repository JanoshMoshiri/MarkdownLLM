---
id: an-outward-claim-about-a-mechanism-is-read-off-its-test
type: insight
status: active
version: 1.0
created: 2026-10-22
session: 2026-10-22
source: both
confidence: high
origin: inferred
tags: [documentation, outward-floor, readme, gate, restatement, drift]
linked_things:
  - id: holistic-review-rulings-2026-10-21
    relation: supports
    notes: "The worked case: three outward surfaces said 'refused until its dependants are walked'; the gate's own test opens with the cue still unmarked; the operator ruled wording over mechanism."
  - id: review-holistic-substrate-2026-10-21-codex
    relation: references
    notes: "F1 — found by reading touchpoints.py and test_cues.py, not the spec."
  - id: documentation-rulings-2026-10-20
    relation: supports
    notes: "The outward surface has no floor; the install pin was the first instance mechanised, this is the second instance found."
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: extends
    notes: "The same drift class one layer out: not a restated enum but a restated promise about what a mechanism does."
---

# An Outward Claim About A Mechanism Is Read Off Its Test, Not Its Design

## The Insight

The agent that builds a mechanism writes the outward sentence about it from
the design intent — *a change is refused until its dependants are walked* —
and the intent is always a little larger than the mechanism. The gate refuses
until a cue naming the dependants is on record; the marks and the verdict are
the agent's and the human's, and nothing in the floor requires them. Three
surfaces written two days apart (the README's FAQ and "Shown" bullet, the
limitations guide) carried the larger sentence. The review that caught it
read the test, not the spec, and the test says what the gate does with an
open, unmarked cue: it opens.

The generative rule: **an outward sentence about what a mechanism enforces
is transcribed from the test that proves it**, and names only what that test
asserts. The spec says what was meant; the test says what is true; the prose
a stranger reads must be the second. Where the outward surface has no floor —
the README has none — the test is the nearest thing to one, and a claim that
cannot point at a test is a claim about intent.

## Evidence

- F1 of the 2026-10-21 holistic review: `staged_report` accepts a covering
  cue without reading its verdict, and
  `test_staged_raise_writes_the_cue_pinned_to_head_and_opens_the_gate`
  asserts exactly that.
- The install pin (2026-10-20) was the same class one release earlier: a
  README sentence about a mechanism that had stopped being true.
- The author of all three sentences was the agent that built the gate.

## What Changes

When writing or correcting an outward claim about the floor, open the test
first and quote its assertion in plain words. When no test asserts the claim,
either write the test or soften the sentence to the intent it is.
