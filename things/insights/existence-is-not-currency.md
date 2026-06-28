---
id: existence-is-not-currency
type: insight
status: active
version: 1.1
created: 2026-06-23
session: 2026-06-23
source: both
confidence: high
origin: synthesised
linked_things:
  - id: derived-index-is-attention-cache-not-search-layer
    relation: supports
    notes: "Index drift was an early instance of the same principle."
  - id: tracking-artifacts-can-drift-from-reality
    relation: supports
  - id: hook-enforcement-has-three-anchors
    relation: informs
---

# Existence Is Not Currency — A Generated Copy Needs A Freshness Check, Not An Existence Check

## The Insight

For anything **generated from, or installed against, a source** — `kernel.md`, derived
indexes, the pre-commit hook body, the domain-kernel managed blocks —
verifying that the artefact *exists* is not enough: it can exist and be **stale**. The
floor must check *currency* — does the artefact match a fresh build of its source? —
and that check is mechanizable as a drift comparison against the same builder that
produced it.

## Why It Matters

- It unifies what are otherwise four separate checks under one principle: kernel drift,
  derived-index drift, hook-body freshness (`doctor`), and domain-kernel block drift
  (`coherence`). Seeing them as one idea gives a **standing test for
  any future generated artefact**: ship a `--check`/coherence drift check alongside the
  generator, sharing a single body-builder so the check cannot disagree with what it
  guards.
- It distinguishes the two failure modes a generated surface has — *absent* (caught by
  an existence check) and *stale* (caught only by a currency check) — and says the
  second is the dangerous one, because a stale artefact silently claims to be current.
- It closes the open question carried from the 2026-06b retrospective ("is existence ≠
  currency general enough to spec?") — by v3.15.0 it had reached five instances with a
  consistent mechanization, so it is a standing principle, not a candidate. (WORKLOG, one
  of those five, was retired at v3.17 — its stale-check became *moot by deletion*, itself
  a clean turn of the same principle; the live set is now four.)

## Context

The 2026-06b retrospective flagged "existence ≠ currency" as a candidate principle with
four instances (kernel/index/hook-body/WORKLOG) and asked whether it generalised. The
v3.15.0 domain-kernel work added a fifth — managed-block drift detection in
`coherence_findings`, sharing `build_domain_kernel_blocks` with the generator exactly as
`kernel`/`index` already do — plus `doctor` reporting domain-kernel and adapter freshness.
That tipped it from candidate to principle. Generalises [[tracking-artifacts-can-drift-from-reality]]
to *generated* (not just hand-tracked) artefacts.
