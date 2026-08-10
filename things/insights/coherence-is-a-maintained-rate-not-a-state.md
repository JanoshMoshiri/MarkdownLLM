---
id: coherence-is-a-maintained-rate-not-a-state
type: insight
status: active
version: 1.0
created: 2026-08-11
session: 2026-08-11
source: both
confidence: high
origin: synthesised
linked_things:
  - id: cumulative-drift-is-invisible-to-per-change-walks
    relation: supports
    notes: "The perimeter evidence: nine honestly-walked releases and the README still rotted — coherence decays between inspections regardless of per-change discipline"
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: supports
    notes: "Promotion is how the maintained rate is *improved*: each promotion moves a fact from the leaking tier to the zero-defect tier"
  - id: hook-enforcement-has-three-anchors
    relation: supports
    notes: "The anchor gradient is *why* the rate differs by tier: mechanical anchors hold, interpretation anchors leak"
---

# Coherence Is A Maintained Rate, Not A State

## The Insight

The framework's coherence is not a state it achieves and then holds. It is a
rate it maintains — a bounded defect rate per tier, with detection latency set
by inspection cadence. The nine-review record is the measurement: the
mechanical tier (generated surfaces, git-fs controls) ran at zero across every
review and every breached session; the prose tier leaked continuously, at a
rate the reviews caught but the per-change walks did not. "Is the corpus
coherent?" is the wrong question — it has no stable answer. The right
questions are: *which tier do defects fall in, at what rate, and how long
until a scheduled read catches them?*

This is how every mature engineering discipline treats unavoidable failure.
Aircraft do not have parts that never crack; they have inspection intervals
sized to crack-propagation rates. The reviews are the framework's inspection
record, and the record shows exactly what an engineered system under honest
instrumentation looks like: failing where its own theory says it must, and
clean where it paid for enforcement.

## Why It Matters

- **It recalibrates the vision's asymptote.** The dreamer's reading — prose
  that *stays* coherent by diligence — is refuted by the record and by the
  instruction-following literature both. The achievable asymptote is defects
  confined to the tier where a mind must read, at a bounded rate, caught by
  cadence. A defect wave is not a refutation of the thesis; a defect wave *in
  the mechanical tier* would be.
- **It gives success a metric.** Progress is measured by confinement (what
  fraction of defects fall in the irreducible tier) and latency (how long
  drift lives before a scheduled read finds it) — not by defect absence, which
  no prose substrate can promise.
- **It makes cadence a first-class mechanism, not a fallback.** Per-change
  walks bound one axis; sweeps and cold reads bound the other. A surface
  outside every individual blast radius is not unprotected — it is protected
  by an interval, and the interval is a design parameter.

## Context

Surfaced by the external assessment of 2026-08-10
(`reviews/REVIEW-external-2026-08-10.md`, finding F4), commissioned when the
operator asked whether the vision was realistic or a dream after the v3.30.x
defect wave. The nine-review record supplied the measurement; the inspection-
interval frame supplied the reading. Discovered, not invented: the manifesto's
thesis already said the *system* holds what the processor cannot — this names
what "holds" can honestly mean.
