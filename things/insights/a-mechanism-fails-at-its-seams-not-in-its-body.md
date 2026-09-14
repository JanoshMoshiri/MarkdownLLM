---
id: a-mechanism-fails-at-its-seams-not-in-its-body
type: insight
status: active
version: 1.1
created: 2026-09-13
session: 2026-09-13
source: both
confidence: high
origin: synthesised
tags: [floor, coherence, seams, composition, checks, self-repair]
linked_things:
  - id: mechanical-coherence-checks-backlog
    relation: informs
    notes: "The two items added 2026-09-13 are both seam defects, not check defects: which checks the hook composes, and whether one mechanism's output is the right KIND for the next. The backlog's gate should ask of a proposal: does this close a seam, or add a body?"
  - id: floor-structure-residue
    relation: informs
    notes: "Item 9 is the same shape one level out — a correct check that cannot run on the platform the release happens on."
  - id: change-safety-is-defense-in-depth
    relation: extends
    notes: "That insight says the layers catch what each other miss; this one says where the misses live — between the layers, never inside one."
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: supports
    notes: "Its family: a check correct in itself, wrong about where it is standing. The boundary audit's WinError 206 is the environment form of the same seam."
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: supports
    notes: "Why seams go quiet: the covered steps completing makes the gap between them feel covered too."
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: extends
    notes: "Names a tier that model did not: the seams between mechanical controls are neither prose nor check-internals, and nine reviews could not see them because reviews read content, not gate composition."
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: supports
    notes: "Its corollary 3 — derived surfaces never appeared in any round's findings — is the same observation from the other side: what is composed correctly never fails, so the failures live in what is not composed at all."
---

# A Mechanism Fails At Its Seams, Not In Its Body

## The Insight

Across a day of heavy, fast change on the framework's own corpus, **every
defect that reached anywhere it should not have was a seam defect.** Not one
was a check reasoning wrongly inside itself. The checks were individually
correct every single time; what failed was the joins between them.

The four seams, each with its instance from 2026-09-13:

| Seam | What failed | Instance |
|---|---|---|
| **Composition** — which checks a gate runs | `provenance` is not a pre-commit leg, so the quarantine rule cannot block a commit | Three violations rode eighteen commits through every local gate, caught only by CI, after publication |
| **Environment** — where a check can stand | `boundary --history` builds an argument list past the Windows limit | The release pre-flight's own audit could not run on the release platform |
| **Kind** — whether one mechanism's output is the right *type* of thing for the next | A cue's citation is not checked for kind | Two cues cited an external review artifact as if it were a ruling; caught only incidentally, because that artifact was also unverified |
| **Judgement** — which gate a human or agent actually verified | Four CI gates exist; one was checked by hand before a public push | The agent's own failure, not a mechanism's |

## Why It Matters

- **It tells the backlog what to buy.** The instinct when a defect escapes is
  to add a check — a new body. Three of these four are fixed by *joining what
  already exists*: run provenance where the others run, give the audit a
  platform it can stand on, type-check a citation. Only the fourth needs
  judgement, and no check can supply it. A proposal's first question becomes:
  *does this close a seam, or add another body with new seams of its own?*
- **It explains why the misses feel invisible.** `partial-coverage-quiets-the-
  uncovered-steps` names the mechanism: the covered steps completing makes the
  gap between them feel covered. A seam has no owner by construction — each
  side is someone's, the join is nobody's.
- **It is the honest reading of "the substrate is coherent".** It is not that
  the mechanisms are right (they are, mostly, and that is the cheap part). It
  is that the *set* of them, composed, has holes that only show under load —
  and the day's evidence is that the holes are findable, because each one was
  found by a different layer noticing a disagreement. The `--since` defect was
  found because the boundary advisory and the cue carrier disagreed; the
  quarantine violations because CI runs a leg the hook does not; the
  one-day-old contradiction inside a spec because a scan walks edges no author
  re-reads.

## Where This Sits Against The Rate Model

`coherence-is-a-maintained-rate-not-a-state` (2026-08-11) decomposes defects
into two tiers: a **mechanical** tier that ran at zero across nine reviews, and
a **prose** tier that leaks continuously, caught by inspection cadence. Read
carelessly, "mechanical tier at zero" says the floor has no gaps. It does not
say that, and 2026-09-13 shows why: **three of the four seams were in
mechanical territory and none of them was a check computing a wrong answer.**

The reviews measured what the checks *say* — derived surfaces against their
sources, censuses against their registries — and found them clean, repeatedly
and correctly. No review ever asked *which checks the commit gate composes*,
*what platform a check can stand on*, or *whether one mechanism's output is
the right kind for the next*, because a review reads content and a seam is not
content. So the rate model's two tiers want a third between them: the
**composition** tier — mechanically checkable in principle, checked by nobody
in practice, and invisible to the instrument that certified the tier above it.

This does not weaken the rate model; it sharpens its metric. Confinement is
measured against the tiers you have named, so an unnamed tier reads as zero.

## Context

2026-09-13, closing a two-day arc that built the cue carrier, ruled twice on
authority, ran a seven-scan retrospective, cut 3.40.0 and published it. The
pattern was not visible from any one defect; it appeared only when the day's
five repairs were laid beside each other at session end and every one landed
in the same place.

**Dismissal condition:** dismissed if a defect of consequence is found *inside*
a floor check's own reasoning — a check that computes the wrong answer from
correct inputs in an environment it can see. **Promotion:** into the coherence
backlog's admission gate, or `validate.thing.md`'s division-of-labour section,
once a second period's defects sort the same way. One day is one sample, and a
day spent changing the checking machinery is a biased one — the seams were
being moved.
