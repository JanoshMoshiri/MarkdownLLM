---
id: run-floor-sprint-3-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-23
definition: substrate-floor-development
current_stage: design
held_by: claude-code
linked_things:
  - id: run-floor-sprint-2-2026-08
    relation: references
    notes: "The sealed predecessor. Its seal record names this sprint's subject explicitly — 'Sprint 3 (derivation: F8's three phases) starts as a new run of substrate-floor-development when execution resumes, generating from the module layout this sprint settled.'"
  - id: coherence-mechanism-build
    relation: references
    notes: "Problem owner for the whole of F8; its four phases are this sprint's work inventory, and its precondition (a settled module layout) was met at sprint 2's seal."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Phase 2's owner. Canonical on which checks to build and their same-builder gate; this run never restates its items."
  - id: floor-block-requirements-2026-08
    relation: references
    notes: "The requirements surface this sprint is cut from; the requirements stage decomposes F8 there rather than minting a duplicate."
---

# Run: Floor Sprint 3 — derivation

## Where This Is

At `design`. Born at `requirements`, same as both predecessors: the `problems`
stage was satisfied before this run existed. Sprint 2's seal record named
the subject, `coherence-mechanism-build` carries the evidence for every
phase (the eight-round review loop's measurement — derived surfaces held
clean in all eight rounds, hand prose never did), and the plan's
precondition — derive from a settled module layout, not one about to be
reshaped — was discharged by sprint 2's landed structure work. No
aspirational entries.

## What closes with this sprint

Sprint 3 is the floor block's last *buildable* sprint. Of the block's
fifteen requirements: F1 and F9–F13 landed in sprint 1, F3–F7 in sprint 2,
and F8 is this sprint. What remains after it is not buildable here —

- **F2** — owner `evidence-and-eval-backlog` is operator-sequenced and now
  stalled 27 days; surfaced again at this sprint's seal, not absorbed.
- **F14** — left unbuilt on sprint 2's measurement, with a dated re-open
  condition at the requirements ledger.
- **F15** — recorded with mechanism and a proposed shape; widening a product
  config surface needs its own analysis cut.

That matters for sequencing: the operator's order puts the framework
retrospective after the block, and its time trigger fires 2026-08-27.

## Stage record

- **requirements (2026-08-23, efed48d)** — the ledger revised to v1.3: F8
  decomposed into F8a/F8b/F8c because one line covered three phases of
  unequal size; the slice that had already landed through other work named
  so the sprint cannot rebuild it; **F16** added, found while creating this
  run — `held_by`/`held_until` are framework-shipped `workflow-run`
  vocabulary sitting outside `CORE_FIELDS`, so this run took a validate
  Warning for using the framework's own reserved convention. The
  non-functional addition: a new check spends against N3, not a separate
  allowance.
- **analysis (2026-08-23)** — cut committed as
  `floor-sprint-3-scope-2026-08-23`. Necessity F8a + F16; should the three
  felt F8b checks; stretch F8c probes 1 and 2. Residue item 8 (the Node 20
  trust-root bump) routed to seal as a human gate rather than deferred
  silently.

- **design (2026-08-23)** — `floor-sprint-3-design-2026-08`. Nine commits,
  ordered *subtract before you add*: no byte-identical restructuring is in
  this sprint, so the identity-first rule has nothing to order and the
  deletions lead instead. Three facts settled at design time by measurement
  rather than assumption: the managed-block splice machinery is already
  generic (F8a needs no new mechanism, only an opt-in), all 28 catalog
  annotations currently agree with live frontmatter (the check lands green,
  pinning truth), and the Tier-2 routing check is one-directional because
  the table legitimately routes four `docs/` guides outside the catalog.

  The design's sharpest call is C3's **zero estate blast radius**: rendering
  tool-owned descriptions for the reserved types would have drifted all
  thirteen domains' managed blocks at once and *blocked their commits* with
  a coherence Error. The chosen shape is byte-stable for every existing
  domain by construction, and the reserved types' root prose is deleted
  rather than generated — `kernel.md` already owns it.

## Next

Build C1 through C7 in order, recording deviations in this body as they
happen. C8–C9 (probes) are stretch, gated on C1–C7 verifying.
