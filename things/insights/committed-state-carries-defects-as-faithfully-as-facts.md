---
id: committed-state-carries-defects-as-faithfully-as-facts
type: insight
status: active
version: 1.0
created: 2026-07-07
session: 2026-07-06
source: both
confidence: medium
origin: synthesised
tags: [evals, longitudinal, drift, floor, linked-things, known-fields]
linked_things:
  - id: structure-decides-figures-scale-decides-convention
    relation: extends
    notes: "The 2×2's split (structure→figures, scale→convention) now has a longitudinal data point: both halves persist across memoryless sessions"
  - id: mis-keyed-links-pass-the-floor-silently
    relation: challenges
    notes: "Its promotion note says the hole 'is closed' — but the v3.13.0 check is opt-in (`known_fields`), the eval seed doesn't declare it, and the identical failure reproduced verbatim on 2026-07-06"
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "First data from the session-2 pre-work smoke; the full trial run decides whether this holds beyond n=1"
---

# Committed State Carries Defects As Faithfully As Facts

## The Insight

The first longitudinal trial (haiku smoke, `20260706-143232-haiku-fw-t1`,
build → perturb → amend-rule, three fresh memoryless agents on one workspace)
returned a two-sided result:

1. **Every figure and status assertion passed in every session** — the
   perturbation cascade landed both edits and found the assessment through the
   graph; the rule amendment moved exactly the two high camps and left the
   three controls untouched. The drift-resistance half of the thesis got its
   first supporting data point (n=1, one tier).
2. **The one defect present persisted just as faithfully.** Session 1
   reproduced the known haiku convention miss (`relation:` instead of
   `linked_things:` — [[mis-keyed-links-pass-the-floor-silently]]). Sessions 2
   and 3 read the mis-keyed files, worked around them correctly, recomputed the
   figures — and never corrected the key. `validates_clean` stayed green the
   whole chain.

Committed state is a faithful carrier of *both*: structure does not heal, it
preserves. Whatever the floor lets through in session 1 becomes session N's
inherited reality.

## The Inversion That Makes It Sharp

The June insight explained the invented syntax by absence: "the seed gave it
nothing to copy." The longitudinal chain inverts that — session 1's mis-keyed
files became the in-corpus exemplar, so later sessions now have exactly the
*wrong* thing to copy, stabilised by the floor's silence. A convention defect
below the floor's threshold is not noise that washes out over sessions; it is
a fixed point.

## Why The Floor Stayed Silent

The v3.13.0 field-registration check (the promotion of
[[mis-keyed-links-pass-the-floor-silently]]) would have flagged `relation:` —
but it is opt-in per domain via `known_fields` in `_schema.yaml`, and the
`sleeping-bag-fac` seed declares only `types` and `relations`. The hole is
closed *where a domain opts in*; the framework's own eval seed does not, so
the original failure reproduces verbatim thirteen months of versions later.
Not a contradiction of the mechanism — a scope caveat on the closure claim.

**Open question for the operator (session-2 evening):** declare `known_fields`
in the eval seed, or leave it unpatched? [[fixture-fixes-correct-bugs-not-difficulty]]
cuts the same way it did in June — patching the seed hides the very
inheritance behaviour this trial exposed, and per-assertion reporting already
keeps the comparison honest. But an unpatched seed means the longitudinal
link-layer numbers measure the June defect again, not new information.

## What This Does Not Show

n=1, haiku, framework condition only. The full run (≥5 trials, two tiers) is
the operator session; this smoke is a chain-mechanics check that happened to
carry a real finding. Do not cite the drift-resistance half beyond "first
supporting data point" until the trial run lands.
