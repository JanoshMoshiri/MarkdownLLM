---
id: run-floor-sprint-3-2026-08
type: workflow-run
status: completed
version: 1.0
created: 2026-08-23
definition: substrate-floor-development
current_stage: seal
informed_by:
  - id: run-floor-sprint-2-2026-08
    commit: 4c7383b9221f8dd67748393d49de6d50b8521112
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

At `seal`, complete. Born at `requirements`, same as both predecessors: the `problems`
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

- **C8–C9 / F8c stretch landed** — `tools/tests/test_flow_probes.py`, the
  first probes of the layer `coherence-mechanism-build` Phase 3 names.
  Started only after C1–C7 verified, per the design's gate.

  Three probes, two flows. **Fresh-clone boot:** a cold clone must report
  *setup ordering*, not a validation failure, and must be clean the moment
  the attestation exists. Both directions are asserted inside the one test,
  which is what makes it non-vacuous — the phrase must be present before
  session-start and absent after, so a regression in either direction fails
  it. **Scaffold birth:** the birth commit lands, the managed blocks match a
  fresh generation (a domain born drifted is born lying), and the reasoning
  prompts are delivered *and* graph-stripped — their `linked_things` point
  into the framework's id space, which does not resolve in a domain.
  **The gate's asymmetry:** the second commit is refused without an
  attestation and succeeds with one. That asymmetry is the whole design and
  is regressible in both directions — blocking the birth commit would
  deadlock scaffold against its own output, never blocking would make the
  gate decorative — and only an executed commit can tell them apart. That
  is precisely why it is a probe and not a unit test.

  Probes 3–5 (invariant breach, refresh end-to-end, session close) stay
  owned by `coherence-mechanism-build` for a fourth sprint.

## Verify record (2026-08-23)

**Full suite: 735 passed, 3 skipped, 3:27 under `-n auto`** — against sprint
2's 694/2 in 4:03, so 41 more tests in 36 seconds less. The known F15 flake
(`test_imports_freshness_fresh_then_stale`) did not recur.

Budgets, steady-state per the v1.1 measurement protocol:

| ID | Budget | Measured | Verdict |
|---|---|---|---|
| N1 session-start root | ≤ 5s | 2.0s | met |
| N3 precommit root | ≤ 12s | 4.3s | met |
| N4 precommit domain | ≤ 5s | 3.3s | met |
| N5 validate domain | ≤ 3s | 1.2s | met |
| N7 full suite | ≤ 12min | 3:27 | met |
| N6 focused loop | ≤ 120s | 4–54s across the build's focused runs | met |

N3 was measured after each of the three commits that add hook-path work, as
the design required: **3.7s** after C4, **5.1s** after C6 unbatched, **4.2s**
after batching, **4.3s** after C7. The whole sprint's additions cost about
1s against a 12s budget.

**Non-steady contexts, recorded as context and not as verdicts** (the
protocol's own instruction):

- **Post-suite** — N1 measured **1.98s** and N3 **4.32s** immediately after
  the full suite, both indistinguishable from steady state. Sprint 1's
  5.5–5.8s cache-eviction transient did not reproduce, for the second sprint
  running. **F14 stays unbuilt on that evidence**, and its re-open condition
  is now two sprints unmet.
- **Mid-suite** — N1 measured 4.98s *while* the full suite was running on
  the same machine. Recorded because it is the reading that would have been
  mistaken for a regression: it is CPU contention, not a code path, and the
  protocol exists so a number taken at the wrong moment does not become a
  finding.

## Loop back: verify → build (2026-08-23)

**The sprint's probes blocked the sprint's own commit, and that is how the
backlog's unattributed adder was found.**

Committing C8–C9 was refused by the disclosure-boundary leg: the probes had
scaffolded a domain named `born`, and `born` was now a boundary term, so
every file containing the word — 56 of them — crossed the boundary. The
fourth block of exactly the class `mechanical-coherence-checks-backlog`
records, on exactly the predicted path (`tools/tests/`), against a commit
that was itself about the problem.

**Cause, found in eleven minutes because the audit leg from C5 existed:**
`scaffold.py` registers every newborn domain's name in the *framework root's*
local `.boundary-terms` — private-by-default at birth, a sound intent. But
`fw_root` is the **running tool's own checkout**, not the target's context,
so a scaffold anywhere on the machine appended to this repo's
operator-owned control file. Every scaffolding test did it, permanently.
The backlog had recorded the adder as unattributed on the reasoning that
"nothing in `boundary.py` writes that file" — a true statement whose search
was scoped to the wrong module.

**Corroboration, and why the cause stayed hidden:**
`test_scaffold_harness_selection.py` already carried an autouse fixture
restoring the framework's terms file after every test, with the comment
"Scaffold birth registers a private name; tests must leave no local state."
One test file had discovered the behaviour and patched its own symptom. That
local patch is exactly why the remaining leaks looked sourceless — the
obvious suspect was already clean.

**Fixed at the source** (verify → build, the loop the definition provides):
the registration now happens only when the newborn is actually nested under
this framework root. The justification bounds itself — a domain outside this
root can never be named by this repo's commits, so registering it buys no
privacy and costs a permanent false positive. Proven by reverting the guard:
the new probe fails against the unfixed tool.

**Classification of what was already there, obtained without reading a
single term** (the audit reports by line number, so this is by hit-path
shape and a set-membership test alone): **all 17 flagged entries appear in
this repository's own tracked content, and not one of them is a live domain
name.** The whole class is accumulated tool output, not operator vocabulary.

Only the entry this session's own probes created was removed —
`.boundary-terms` is an operator-owned control, and an agent deleting from
it on inference would be the floor deciding what the boundary protects. The
other 16 are surfaced at seal with the cause named and a one-command remedy.

## Reconcile record (2026-08-23)

The walk this sprint owed is unusual: it had to correct the entry file's own
account of *what is still walked by hand*, because the sprint moved items
out of the dark region.

- **`AGENTS.md` step 3** named the coherence checks in prose and listed the
  Tier-2 routing table and the spec catalog as prose-only residue. Both are
  now mechanical. Rather than update the list, the line now **points at the
  tool and says so**: a prose inventory of mechanical checks is the exact
  restatement class those checks exist to end, and this one went stale
  inside a single sprint. What remains genuinely human is named precisely —
  the framework-map's counts, and the *descriptions* in the routing table
  and catalog, whose annotations and completeness are now floor-owned.
- **`docs/framework-map.md`**: `coherence` is no longer "the catalog slice"
  of the Walk. Counts unchanged — `--audit-terms` is a leg on an existing
  subcommand, not a new one, so View 3's census and its three restatements
  all still hold (checked mechanically, as it happens).
- **`docs/operator-guide.md`**: the `boundary` row carries `--audit-terms`,
  with the line-number-not-term property stated, and the trigger an operator
  actually feels — "when the boundary starts refusing commits you believe
  are clean".
- **`mechanical-coherence-checks-backlog`**: three items struck with dated
  commits, the two declined promotions recorded with their lifting
  conditions, and the boundary-term item rewritten to name the adder it had
  recorded as unattributed.
- **`coherence-mechanism-build`**: `not-started` → `in-progress` (v1.1),
  with per-phase state. Its own estimate is corrected in place: it predicted
  Phases 1+2 as one session and Phase 3 as a second; one session took
  Phase 1, the felt half of 2, and two thirds of 3 — because the *delete*
  leg removed load the *check* leg would otherwise have had to police.
- **Kernel**: no spec's `<!-- kernel -->` block changed (the `git-workflow.md`
  edit sits outside one), so no regeneration was owed — and coherence proves
  that rather than memory.

**Recorded, not silenced — three standing findings this sprint did not
fix.** Both examples remain pinned at 3.33.0 against a 3.34.0 sentinel; that
is release-cadence work belonging to the operator's walk, and re-pinning
without walking would be a lie told by the very mechanism built to prevent
it. And the perimeter check's own limitation surfaced on day one: a
git-derived pin cannot record *"walked, still correct"* — `CLAUDE.md` is 18
lines of pure routing with nothing to go stale, so its Info will recur every
release. Both are written down at their owners rather than quietly cleared.

## Seal record (2026-08-23)

**Ledgers set to truth.** `floor-block-requirements-2026-08` carries a
seal-status section: F1, F9–F13, F3–F7, F8a, F8b, F16 and two thirds of F8c
met, with every N1–N8 budget measured green at each sprint's verify.
`mechanical-coherence-checks-backlog` has three items struck with dated
commits and two declines recorded with their lifting conditions.
`coherence-mechanism-build` is `in-progress` with per-phase state — it
cannot complete here, because its exit condition needs a post-release cold
read, which is an operator act after publication.

**What the sprint actually delivered, against what it planned.** All of
necessity, all of should, and the stretch. Three things it did not plan:
the `_view_glob` semantic split (two branches of one function answering the
same question differently), the boundary-terms adder (a four-week
"unattributed" defect, named), and two live index-signal enumerations the
ninth review's own fix pass had missed. Each was found by a mechanism this
sprint built, which is the sprint's own thesis holding under its own weight.

**Left honestly open:** probes 3–5; the two examples pinned at 3.33.0; the
perimeter check's inability to record "walked, still correct"; F14's
twice-unmet re-open condition; F15.

## Human gates — all at this boundary, none pre-empted

1. **Publication.** The framework root declares `autopush: false`, so all
   **15 unpushed commits** are local truth awaiting a deliberate push. The
   CHANGELOG entry and version judgement belong to that release act.
2. **The Node 20 action bump** (`floor-structure-residue` item 8), routed
   here by the analysis cut rather than deferred silently. Moving
   `actions/checkout` and `actions/setup-python` to reviewed SHAs changes
   pinned immutable trust roots — an authority-bound act, not agent
   judgement. The alternative is a dated record of why the deprecation is
   being carried and until when.
3. **The 16 standing `.boundary-terms` entries.** Cause now identified and
   fixed at the source, so the class cannot grow. All 16 appear in this
   repo's own tracked content and none is a live domain name — but deleting
   from an operator-owned control on the agent's inference is exactly the
   move the floor should not make. `mdllm boundary . --audit-terms` lists
   them by line number.
4. **F2's owner, 27 days stalled** (`evidence-and-eval-backlog`). Third
   consecutive surfacing. Two sprints have now declined to absorb it, which
   is the honest move and also the reason it has not moved.
5. **The retrospective fires 2026-08-27** — four days. The operator's
   recorded order sequences it after the block, and the block's buildable
   remainder is now empty.

**Sealed as authored-and-unproven where the floor cannot execute:** nothing
in this sprint touches CI configuration or a vendor lifecycle, so unlike
sprint 2 there is no publication-gated proof owed. Everything claimed here
was executed locally, and the full suite is the evidence.

## Activation and fulfilment (recorded 2026-08-26, retrospectively)

Added when the fulfilment advisory (F17) shipped and named this run.

- **Initiating demand:** sprint 2's seal, pinned in `informed_by` above.
  Its commit is the last state of `run-floor-sprint-2-2026-08` before
  this run was created (`f39547f`, 2026-08-23), and its record names this
  sprint's subject explicitly — "Sprint 3 (derivation: F8's three phases)
  starts as a new run of substrate-floor-development when execution
  resumes." The pin records a demand recoverable from git, not a
  reconstructed judgement.
- **Produced evidence:** the F8a/F8b/F8c commits and the coherence checks
  they landed. None carries an `informed_by` pin back to this run,
  because outputs predate the convention; that half of the chain stays
  prose and is deliberately not backfilled.

**Recorded retrospectively, and the retrospection is the point.** This
run is the last one that ran without F17, so half its chain is pinnable
and half is not — which is precisely the gap the semantics exist to
close for every run after it.

## Next

Nothing — the run is complete. Sprint 4, if it happens, is probes 3–5
(`coherence-mechanism-build` Phase 3) — but the operator's order puts the
retrospective first, and the block's buildable requirements are done.
