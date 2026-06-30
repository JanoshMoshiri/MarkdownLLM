---
id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
type: insight
status: active
disposition: keep-active
disposition_reason: "Names the precise blind spot of every same-builder drift check (kernel, derived-index, domain-kernel) and tells the human Walk where to look — emitter source, not just corpus. Fresh, paid for by a real downstream miss; gates how vocabulary retirements are walked."
version: 1.0
created: 2026-06-30
session: 2026-06-30
source: both
confidence: high
origin: synthesised
tags: [floor, coherence, drift, generator, change-reconciliation, false-negatives]
linked_things:
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: complements
    notes: "That insight says a same-builder check is 'exactly as right as the generator it shadows'; this names the failure mode hiding in that clause."
  - id: existence-is-not-currency
    relation: complements
    notes: "A coherence-clean artefact built from a contradictory generator silently claims to be current — the same silent-false-negative this warns of."
  - id: mechanical-coherence-checks-backlog
    relation: informs
    notes: "The retire-vocab Walk this backlog defers to must include emitter source, not only things + specs."
---

# A Same-Builder Check Is Blind to a Self-Contradictory Builder

## The Insight

The floor's authority rests on a single property: a mechanical check compares an
artefact against a *fresh build from the same source*, so it **cannot disagree
with truth** — it is exactly as right as the generator it shadows
([judgement-checks-need-a-suppression-list-which-is-itself-drift](judgement-checks-need-a-suppression-list-which-is-itself-drift.md)).
That clause — *as right as the generator* — carries a blind spot the floor cannot
see past: **if the generator is internally self-contradictory, every artefact it
builds is coherence-clean while being wrong.** The drift check stays green,
because the artefact faithfully reproduces *both halves* of the contradiction. The
floor was never measuring the contradiction; it was measuring fidelity to a source
that already contained it.

The worked case: the v3.17 domain-kernel generator updated its session-start text
to declare `continuity.md` retired, but a *second* emitted surface — the Tier 0
"always load" line — still hardcoded `continuity.md`. Both halves are generator
output. So a regenerated domain `AGENTS.md` declared the file retired in one
sentence and demanded it loaded in the next, and `domain-kernel --check` reported
**in sync** the whole time. As the domain agent put it: *"It's coherence-clean
(matches the generator), but the generator itself missed that spot."* No
same-builder check can catch this, because there is no second builder to disagree
with — the only adjudicator is a human reading meaning *across* the generator's
emitted surfaces.

## Two Things That Make a Generator's Stale Vocabulary Worse Than Prose's

1. **It multiplies.** A retired term left in a prose file is one stale mention in
   one file. A retired term left in an *emitter* is one stale token that prints
   into every downstream artefact on regeneration — N stale mentions, one per
   domain, each manufactured fresh and each coherence-clean.
2. **It self-contradicts silently.** Because a generator emits several surfaces
   from one body of code, a token updated in one surface and missed in another
   produces artefacts that argue with themselves — and the same-builder check,
   comparing each artefact only to its own fresh build, certifies the contradiction
   as in-sync.

## How to Apply

When retiring or renaming vocabulary, the human Walk
([change-reconciliation.md](../../change-reconciliation.md)) must explicitly
include **emitter / generator source** — the functions that synthesise artefacts,
which are *code*, outside the things+specs corpus a "walk the whole corpus" pointer
implies. The emitter is the highest-leverage place a dead name can hide: one miss
there is not one stale file, it is a contradiction stamped into every regenerated
domain, invisible to the floor until something downstream is read by a human or
until the generator is fixed and old artefacts finally drift against the new build.

This is the precondition the same-builder guarantee never states: the guarantee
holds **only to the extent the single source is internally consistent**. Where one
builder emits multiple surfaces, cross-surface consistency is a semantic property,
and like vocabulary retirement itself it stays the human Walk's — it cannot be
floored, because there is no same-builder source to key it to.

## Context

Synthesised 2026-06-30 from a framework session. A domain agent, regenerating its
`AGENTS.md` after a v3.17 refresh, noticed its Tier 0 still demanded the retired
`continuity.md` while the same file's session-start declared it retired, and
escalated it as a framework-not-domain bug. The generator
(`tools/mdllm.py:_dk_tier_routing`) was the source; the fix was one line. The
drift mechanism then worked exactly once it could: with the generator corrected, an
already-refreshed downstream domain (JMTM) registered DRIFT, regenerated, and the
stale Tier 0 fell away. The lesson is the gap *before* that — the months the
contradiction sat in the generator, certified in-sync by the very check meant to
catch drift, because the contradiction lived in the builder, not between builder
and artefact.
