---
id: recognition-data-must-be-frozen-not-derived
type: insight
status: active
version: 1.0
created: 2026-08-22
session: 2026-08-22
source: both
confidence: high
origin: synthesised
tags: [floor, drift, generator, legacy, migration, recognition, false-negatives]
linked_things:
  - id: existence-is-not-currency
    relation: complements
    notes: "The exact inverse case: for a generated copy, currency is the property to check; for recognition data, currency is the DEFECT — it must match the past, not a fresh build."
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: complements
    notes: "Same family of generator blindness: there the check shadows a wrong generator, here the historical record is computed from the current one."
  - id: run-floor-sprint-2-2026-08
    relation: derived-from
    notes: "Found when the probe existence-guards changed the emitted fragment and the frozen-hash tests failed — the legacy definitions had been following the renderer all along."
---

# Recognition Data Must Be Frozen, Not Derived

## The Insight

Some artefacts exist to **recognise the past**: legacy definitions that
identify an old installed hook so a migration can be offered, fixtures that
pin what a previous version emitted, tables that name superseded formats.
They look like generated artefacts and are easy to build like generated
artefacts — computed from the live renderer, so they "stay in sync."

That is precisely backwards. A generated artefact is correct when it matches
a fresh build of its source; **recognition data is correct when it matches
bytes that will never be built again.** Derive it from the live renderer and
it silently follows every renderer change — so on the day the renderer moves,
the record of what came before moves with it, and the thing that was supposed
to recognise the old install now recognises only the new one. Nothing fails.
The migration path just quietly stops existing.

## How It Surfaced

Sprint 2's existence-guard change altered the emitted sh resolution fragment
— the first renderer change since those definitions were written. Two
frozen-hash tests failed, and the failure was not "the guard is wrong": it
was that the `legacy-output-tail-v1` definitions in both project adapters
had been computing their historical fragment from `SH_RESOLVE` at call time.
For as long as the renderer had not moved, the bug was invisible; the tests
that caught it only *could* catch it because someone had frozen the expected
hashes as literals. The fix was to freeze the v1 fragment as data
(`adapters/legacy/sh-resolve-v1.txt`) and thread it through the legacy
paths, after which the original frozen hashes passed again — which is the
proof the freeze reproduces history rather than re-deriving it.

## Why It Matters

- **The failure mode is a silent false negative**, like every generator
  blind spot in this family: no error, no drift report, just a recognition
  that never fires and a migration nobody is offered.
- **It cannot be caught by a currency check** — the usual instrument. A
  same-builder drift check would report this data as perfectly current,
  because it *is* current; current is the defect.
- **The frozen literal is the only witness.** The hashes-as-literals test
  is what made this visible. Anywhere recognition data exists without a
  frozen expectation beside it, this bug is undetectable by construction.

## The Rule

When an artefact's job is to match something that already happened, freeze
its bytes as data at the moment it is written, and never let it read a live
generator. Ask of any historical table: *if the renderer changes tomorrow,
should this change too?* If the honest answer is no, it must not be able to.
