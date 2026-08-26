---
id: an-advisory-is-scoped-by-who-can-perform-its-remedy
type: insight
status: active
version: 1.0
created: 2026-08-26
session: 2026-08-26
source: build
confidence: high
origin: stated
tags: [floor, advisories, scoping, noise, design-test, failure-modes]
linked_things:
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: supports
    notes: "That one names the harm; this one supplies the design test that predicts it before shipping — ask whether the flagged thing can still perform the remedy."
  - id: workflow-state-specification
    relation: informs
    notes: "The adoption advisory is scoped to non-terminal runs for exactly this reason, and the spec now says so rather than leaving the scoping to the code."
---

# An Advisory Is Scoped By Who Can Perform Its Remedy

## The Insight

Two Info-grade advisories shipped in the same sprint. One was correctly
scoped and one was not, and the difference between them is a test you can
apply *before* shipping:

> **Can the thing being flagged still perform the remedy the message
> names?**

- The **adoption cue** ("pin the commit whose definition governs this
  run") fired on every unpinned run, including completed ones. A finished
  run cannot adopt anything: its history is fixed, and retro-pinning it
  would assert a reconstruction rather than record a decision. Three
  permanent findings, uncloseable by any honest act.
- The **fulfilment cue** ("record the activation chain, or state the run
  was self-initiated") fires *only* on completed runs — and there the
  remedy is performable, because the initiating demand is recoverable
  from git and can be pinned as fact.

Same severity, same sprint, same author. One trains the operator to read
findings; the other trains them to ignore findings.

## Why This Is Sharper Than "Don't Cry Wolf"

`a-check-that-always-fires-teaches-the-operator-to-ignore-it` names the
harm, which is only diagnosable after the noise exists. This is the
*predictive* form: an advisory's correct population is not "everything in
the wrong state" but "everything that can still get into the right one."
The two differ exactly at terminal things — and terminal things are
common enough (completed runs, made decisions, sealed records) that the
gap catches real checks.

The corollary matters for adoption cues specifically: **a new mechanism
should nag only what can adopt it.** Everything else is history, and
history's job is to be legible, not compliant with rules written after
it.

## The Test, Stated For Reuse

Before shipping any advisory, write its remedy as an imperative and ask
who must execute it. If the answer includes things that are finished,
frozen, or owned by someone who cannot act — either scope the population
down, or rewrite the remedy so it is performable by whoever receives it.
If neither is possible, the finding is not an advisory; it is a one-time
observation and belongs in a record, not in every future validation run.

## Provenance

2026-08-26, post-seal verification of the operating-model seams sprint.
The mis-scoped cue was found by running the corpus after the release and
noticing three findings no honest act could clear. The correctly scoped
cue sitting beside it in the same file is what made the discriminator
visible.
