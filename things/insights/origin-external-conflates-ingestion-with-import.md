---
id: origin-external-conflates-ingestion-with-import
type: insight
status: active
version: 1.0
created: 2026-07-28
session: 2026-07-28
source: both
confidence: high
origin: synthesised
disposition: keep-active
disposition_reason: "Evidence-gated hold: the operator's estate pinning pass produces the design input (the legitimately-unpinnable residue). Promote to a floor change when that residue is visible; dismiss if none remains."
tags: [cross-domain, provenance, quarantine, sync, gap]
linked_things:
  - id: provenance-specification
    relation: informs
    notes: "origin: external is one value covering two species with different checkability"
  - id: cross-domain-sync-catchup
    relation: informs
    notes: "Surfaced by the first estate run: 30 of 31 imports read INCOMPLETE, many correctly so"
---

# `origin: external` Conflates Ingestion With Import — Two Species, One Value

## The Insight

`origin: external` covers two different kinds of thing that share a
quarantine but differ in **checkability**:

1. **Cross-domain imports** — content from another domain's exposed face.
   These carry (or should carry) the reference triple and are *sync-checkable
   forever*: `imports-check` can re-read the source and report
   fresh/stale/diverged.
2. **External ingestion** — content from outside any domain: a bank
   statement, a third party's document, a review received over email. There
   is no face to re-read. Quarantine and human verification apply in full;
   *sync-checking is category-inapplicable*.

`imports-check` currently treats every `origin: external` thing as a
candidate import, so species 2 reports `INCOMPLETE — missing
source_domain/source_id/source_commit` alongside genuinely-unpinned species
1. The first estate run made the cost visible: 30 of 31 externals across the
estate read INCOMPLETE, and the coverage denominator cannot distinguish "a
pinning pass is owed here" from "this number will never be 100% and that is
correct."

## Why It Matters

The coverage line was built to be un-misreadable (v3.21.0, FW-2), but a
denominator polluted with never-checkable things quietly re-introduces the
same misreading one level up: a domain could complete its pinning pass and
still show poor coverage, training the operator to ignore the number. The
honest form is probably a three-way split — pinned / unpinned import /
external-non-domain — where the last is declared by the author (an explicit
marker, or simply the absence of any triple field *plus* a declared source
kind), never inferred.

## Status / Next

**Deliberately held for evidence — do not build yet.** The operator's
pinning pass across the estate's consumers comes first; the residue it
leaves (the externals that are legitimately unpinnable) is the design input
for the distinction. Promote to a floor change when that residue exists and
its shape is visible; dismiss if the pinning pass leaves no residue worth a
mechanism.
