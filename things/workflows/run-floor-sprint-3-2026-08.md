---
id: run-floor-sprint-3-2026-08
type: workflow-run
status: active
version: 1.0
created: 2026-08-23
definition: substrate-floor-development
current_stage: build
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

At `build`. Born at `requirements`, same as both predecessors: the `problems`
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

## Build record

- **C1 / F16 landed** (`4c556c9`) — `held_by` and `held_until` admitted to
  `CORE_FIELDS`, criterion 2 cited beside its two existing precedents. The
  regression test was proven before it was trusted: reverted against the
  unfixed tool it fails, which is the only thing that distinguishes a test
  from a comment. Corpus back to 269/269 clean.
- **C2 / F8a delete leg landed** (`d128fa0`) — the Standard Thing Structure
  block's restated enums replaced by pointers, with the harm recorded in
  place rather than quietly corrected, because the harm is the argument for
  the leg. **Deviation 1, recorded as it happened:** the design said
  `## Status Values For Framework Specs` "goes the same way". It does not.
  Those four bullets are editorial definitions of what each status means
  for a *framework spec*, and no authority carries them — the tool and the
  kernel own the reserved *set*, not the gloss. Deleting them would have
  destroyed content rather than a restatement. The section keeps its
  bullets and loses only its implicit claim to own the set. Delete is for
  restatements; a gloss is not one.

- **C3 / F8a derive leg landed** — the root's `## Thing Types In This
  Domain` is now a `generated:types` managed block, and the framework root
  becomes the last entry file in the estate to carry one. Three proofs
  rather than three assertions:
  1. **Zero estate drift, measured, not argued.** The `_dk_types` output
     was computed for all 13 estate domains before and after the change and
     compared byte-for-byte: 0 changed. That is the design's central claim,
     and it was the reason reserved-type descriptions were rejected — they
     would have drifted every domain's block at once and blocked commits on
     a coherence Error, where sprint 2's F5 drift was merely advisory.
  2. **The root drift check fires.** Tampering one generated line and
     running `mdllm coherence .` produced the expected Error at
     `AGENTS.md`; restoring cleared it. The generic check needed no
     framework-root special case — it was already general.
  3. **The block cites the schema it actually read.** `schema_source` now
     supplies the path from the same candidate tuple `load_schema` walks,
     so the root's block says `_schema.yaml` and a domain's says
     `things/_schema.yaml`. The old hardcoded citation would have named an
     authority the root had not read — precisely the defect class this
     sprint exists to end, reproduced inside the fix for it.
  204 focused tests green. Also observed and honoured: changing `AGENTS.md`
  expired the session gate's contract fingerprint, exactly as designed —
  re-attested rather than committed through.

- **C4 / F8a check leg landed** — the two annotated prose sections are now
  mechanically checked, and F8a is complete. The catalog's `(type, status)`
  pair is compared against each spec's live frontmatter (Error), and every
  Tier-2 spec in the `TIERS` map must be named by a routing row (Error), as
  must every routed file exist. Both land **green on the live corpus** —
  all 28 catalog bullets already agree — so the check pins truth rather
  than repairing drift, which is the honest outcome for a check written
  after a reconciliation rather than before one.

  Two shape decisions worth the record. The routing check runs **one
  direction only**: the table legitimately routes four human-facing `docs/`
  guides that sit outside both `TIERS` and the catalog, so a mirror check
  would fire on correct prose — and the reverse direction is already total
  where it can be (`TIERS` to catalog, both ways, since review 6). And both
  helpers **report when they cannot look**: a missing section or an
  unparseable table is a Warning naming that fact, never a clean return,
  because a silently-skipped check reads exactly like a passing one
  (`a-check-run-where-it-cannot-see-mints-a-false-finding`).

  17 coherence tests green, 7 of them new. **N3 re-measured: 3.7s** against
  a 12s budget (3.3s before the leg) — the first of the three budget
  checkpoints the design named.

- **C5 / F8b boundary-term evidence check landed** — `mdllm boundary
  --audit-terms`. The backlog's most-felt item: three regressions, the third
  of which blocked four commits in one session and cost working time, with
  the blocking path primed to falsely refuse anything touching
  `tools/tests/`. The control could not be promoted the usual way because
  the list it reasons over must never be committed — so the floor owns an
  *invariant over* the list instead
  (`a-control-that-must-stay-local-has-no-floor`).

  **It reports by line number, never by term** — a deliberate departure from
  the module's other legs, which do print terms. The difference is what the
  finding means: the staged and message legs refuse a specific edit and the
  operator needs to see which word to change; this leg reports a word that
  is *already in tracked content*, where naming it adds exposure without
  adding anything the operator cannot get by opening the file at the line
  named. A test asserts no term reaches the output.

  **It paid for itself before it shipped: 16 findings on the live repo**,
  every one classifiable without reading a term (by hit-path shape alone:
  fifteen are framework test vocabulary, one also reaches `README.md`).
  Surfaced to the operator at seal and *not acted on* — `.boundary-terms`
  is an operator-owned control, and an agent editing it would be the floor
  quietly deciding what the boundary protects.

- **C6 / F8b perimeter currency check landed** — the external review's R2,
  the razor `cumulative-drift-is-invisible-to-per-change-walks` executed:
  the surfaces outside every individual blast radius are protected by an
  interval, and the interval is now mechanical.

  **Deviation 2, and the better design it forced:** the design said each
  perimeter surface would carry a reconciled-at version marker. It carries
  none — the pin is read from git instead (the sentinel version at the
  file's last-touching commit). A marker would have been a *new hand-
  maintained surface introduced by the check that exists to catch hand-
  maintained surfaces going stale*, and three of them would have needed an
  honest first value nobody could supply. Reading git needs no marker, and
  the perimeter set is derived too: root and `docs/` markdown, minus the
  catalog, minus anything `type: specification` (the catalog and TIERS
  checks already own those).

  **Two minors of tolerance, not one, for a measured artifact:** a surface
  reconciled *during* a release cycle is touched before the version bump
  lands, so it reads as exactly one behind while being perfectly current.
  One would fire on correct work every cycle and teach the operator to
  ignore it. At two, the live corpus yields exactly two findings —
  `CLAUDE.md` (3 behind) and `CONTRIBUTING.md` (2 behind).

- **A latent defect found by the cost, not by the check** (recorded here
  because it is the sprint's most instructive find). The first run of the
  perimeter check took **two minutes**. Cause: `_view_glob`'s two branches
  answered the same question differently. The no-view branch delegates to
  `Path.glob`, where `*` stops at a separator; the view branch used raw
  `fnmatch`, where it does not — so `*.md` meant *this directory* without a
  view and *the entire recursive tree* with one, 25 paths versus 1978. The
  new check then spawned one `git` process per match. Fixed at the source
  with segment-wise matching and a regression test asserting the two
  branches agree, rather than worked around at the call site. Two paths
  claiming to be the same and quietly disagreeing is this sprint's own
  subject, found inside its own tooling.

  **N3 re-measured: 5.1s, then 4.2s.** The first figure is the honest
  unbatched cost; the second is after collapsing eleven `git log` spawns
  into one `--name-only` walk (F12's lesson — the cost of this check is
  process spawns, not computation). Budget 12s.

- **C7 / F8b review-9 promotions landed — two built, two declined, and the
  declining is part of the promotion.**

  **Built.** *Survivor 7's inverse:* a `known_fields` entry that is already
  in `CORE_FIELDS` is reported as a redundant registration (Info). C1 fixed
  the outward direction of that fault; this catches the inward one, and it
  matters precisely because C1 happened — whenever a field joins
  `CORE_FIELDS`, every domain that had registered it becomes redundant and
  nothing told them. *Survivor 6:* prose that enumerates the derived-index
  signals must enumerate all of them, keyed to `INDEX_FILES` — the constant
  the rebuild loop itself walks.

  **It caught two live instances the ninth review's own fix pass missed.**
  `AGENTS.md`'s catalog entry for `derived-index.md` and `git-workflow.md`'s
  velocity paragraph both still enumerated three signals and omitted
  `provenance` — nine weeks after the review that found five surfaces doing
  exactly this and believed it fixed them all. Both repaired here (by
  pointing at the authority rather than by adding the fourth name), so the
  check lands green. This is the argument for promotion in a single
  observation: the cold read found the class, and only the mechanism finds
  the *rest* of the class.

  **Declined, with the condition that would lift each.** *Survivor 3, the
  trigger-type count:* there is no tool-owned authority to key to. The
  evaluator dispatches on a chain of `elif ttype == ...` branches, so any
  `TRIGGER_TYPES` constant introduced for the check would itself be a
  restatement — the branches would remain the real authority and the
  constant could drift from them silently. Lift the decline when the
  dispatch itself reads a declared set; making it do so is evaluator
  surgery, which is its own ordered work and not a should-scope item.
  *Survivor 5, the reserved-set restatements:* a sentence naming two
  reserved types is ordinary prose, not an enumeration, so the shape that
  works for four index signals produces noise across thirteen reserved
  types. That is the retired-vocabulary judgement repeated, and repeating
  it honestly is cheaper than repeating the check.
  *Survivors 1, 2, 4* were never candidates: each was a semantic
  contradiction between a spec and its own kernel block.

  24 coherence tests green, 4 new. **N3 re-measured: 4.3s** against 12s —
  the third and last budget checkpoint the design named.

## Next

Verify: full suite, budgets, then the stretch decision on C8–C9.
