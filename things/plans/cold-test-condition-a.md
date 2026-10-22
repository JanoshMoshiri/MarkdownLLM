---
id: cold-test-condition-a
type: plan
status: not-started
version: 1.0
created: 2026-10-22
session: 2026-10-22
priority: medium
tags: [review, cold-test, discoverability, independence, evidence]
linked_things:
  - id: review-holistic-substrate-2026-10-21-codex
    relation: derived-from
    notes: "The A/B/C design (v1.2): A is the baseline against the existing entry route, run before any discovery workflow; the brief, controls, assessment and interpretation are specified there and not restated here."
  - id: holistic-review-rulings-2026-10-21
    relation: references
    notes: "Ruling 3: the discovery route (condition C) is not built now; a future first pass excludes both reviews. Condition A is the baseline that ruling presupposes."
  - id: cold-read-of-the-seams-release
    relation: references
    notes: "Cancelled 2026-10-17 because the critical comparison 'performed' the cold read; the review names that comparison's brief as a category confound, so this is the cold read that plan asked for, with the framing controlled."
  - id: the-public-corpus-is-the-self-description-the-use-is-private
    relation: implements
    notes: "Why the run's result is read as evidence about the public face: the insight predicts under-identification from the public corpus alone, and a run is the test of that prediction."
---

# Cold Test — Condition A: One Fresh Broad-Brief Review Of The Public Face

**What this delivers.** One observation the record does not have: how a
fresh reviewer, given a broad identification brief and no author coaching,
identifies the substrate from the public corpus at a pinned release. It is
the baseline the holistic review's A/B/C design puts first; B and C wait on
it. One run demonstrates a case, not general discoverability.

**The operator's intent (2026-10-22).** The operator said they may take a
fresh clone and run "the repository examination experiment" the review
recommends. This plan carries the conditions so they are not reconstructed
from the review's appendix when the moment comes.

## Conditions

1. **A fresh clone at a new path** — not a session started from the
   framework folder: this harness keys its project memory to the folder
   path, and that memory now names the gate's true condition, the rulings
   and both reviews. A new path has no memory. Codex, or a cloud session
   from the pushed branch, are equivalent clean runners.
2. **Pinned** at a release commit (`68a1d30` today; 3.50.0's successor when
   there is one), the pin recorded in the review record the run produces.
3. **Excluded from the first pass:** `reviews/`, the two review records'
   ids, and `things/decisions/holistic-review-rulings-2026-10-21.md`.
   Ordinary entry instructions and documentation stay — they are the product
   under test.
4. **The brief verbatim** from the review's "Proposed cold test" section,
   condition A; the initial brief and the reviewer's initial assumptions
   recorded before reading.
5. **The initial account committed before any clarification** — as a
   `reviews/REVIEW-cold-a-<date>-<seat>.md` record — and only then the
   comparison with the holistic review and a table of what changed and why.
6. **Assessment fixed before the output is read:** the review's criteria —
   trace accuracy, justified classifications, discovery of F1 and F6 (the
   two public-snapshot findings), handling of unknowns — never vocabulary or
   agreement with the author.

## Done when

The initial account is committed at the pin with its brief, assumptions and
reading budget; the comparison note is committed after it; and
`the-public-corpus-is-the-self-description-the-use-is-private` is revised up
or down by what the run found.

## What this plan refuses

Building condition C (the discovery workflow) — ruled not now. Running A
from this folder. Scoring the use of the framework's own words.
