---
id: floor-sprint-3-design-2026-08
type: plan
status: completed
version: 1.0
created: 2026-08-23
priority: high
tags: [design, floor, coherence, derivation, sprint, checks, probes]
linked_things:
  - id: run-floor-sprint-3-2026-08
    relation: informs
    notes: "The run whose design stage this thing satisfies."
  - id: floor-sprint-3-scope-2026-08-23
    relation: derived-from
    notes: "The analysis cut this design realises: necessity F8a/F16, should the three felt F8b checks, stretch F8c probes 1-2."
  - id: coherence-mechanism-build
    relation: implements
    notes: "Phase 1 in full and the felt half of Phase 2; Phase 3 partially (probes 1 and 2)."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Canonical on which checks exist and their same-builder gate; this design decides only their shape and cost."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "The governance surface read before this design: dependency direction, naming-as-architecture, seams named before implementation, conscious shortcuts recorded."
---

# Floor Sprint 3 Design — Derivation

Design read against the code-architect governance surface. Every fact below
was measured on this checkout at design time (HEAD `36211b4`), not assumed.

## What is already there (measured, not assumed)

The splice machinery in `domain_kernel.py` is **already generic**:
`apply_domain_kernel` and `domain_kernel_status` operate on
`(text, blocks)` and know nothing about domains. The coherence check that
consumes them is likewise generic — it fires on *any* `AGENTS.md` carrying
managed `generated:NAME` blocks, framework root included. `load_schema`
already falls back from `things/_schema.yaml` to a root `_schema.yaml`.

So F8a needs **no new mechanism**. What it needs is for the root's entry
file to opt in, and for one builder to learn one optional field. That is
the whole of the "derive" leg, and it is the reason this sprint is small.

Measured today, so the sprint does not rebuild them: catalog-to-disk,
`TIERS`-to-catalog *both ways*, kernel drift, framework-map subcommand
count, and example `framework_version_seen` pins are all live checks.

## The commits, in order

Ordering rule (`prove-identity-before-you-change-bytes`): nothing here is a
byte-identical restructuring, so no identity commits are owed. The order is
instead **subtract before you add** — every deletion lands before the check
that would otherwise have to police what was deleted.

### C1 — F16: `held_by` / `held_until` admitted to `CORE_FIELDS`

- **Touches:** `model.py` (`CORE_FIELDS`, with the criterion cited in the
  comment beside its two existing precedents).
- **Why it is first:** it is the smallest change in the sprint, it is
  independent of everything else, and it clears a Warning this sprint's own
  run is carrying while the sprint runs.
- **Not** a structural-reference field: `held_by` names an operator or
  agent, not a thing, so it does not enter `structural_field_names()` and
  no reverse index changes.
- **Focused tests:** `test_mdllm.py -k field_registration`,
  `test_structural_reference_registry.py`. New: a `workflow-run` carrying
  `held_by` and `held_until` validates clean with no `known_fields`
  declaration.
- **Budget:** none affected.

### C2 — F8a *delete*: the entry file stops restating enums

- **Touches:** `AGENTS.md` only. No code.
- **What goes:** in `## Standard Thing Structure`, the restated `type:`,
  `status:`, `priority:` and relation enums, replaced by pointers to their
  authorities. `## Status Values For Framework Specs` goes the same way —
  it restates `RESERVED_STATUSES` for `specification`.
- **Why deletion beats generation here:** the relation line is not merely
  stale, it is *wrong in a way that instructs* — it still advertises
  `related`, pruned from `_schema.yaml` on 2026-06-12, and a session read
  it, used it, and took two validate Warnings. A generated block would
  make this line correct; deleting it makes the entry file stop teaching
  vocabulary it does not own. `kernel.md` already carries every one of
  these enums at Tier 0, on the always-loaded path.
- **Focused tests:** none (prose). The floor's coherence and validate legs
  run at the commit boundary as usual.

### C3 — F8a *derive*: the Thing Types section becomes a managed block

- **Touches:** `domain_kernel.py` (`_dk_types`), root `_schema.yaml`, root
  `AGENTS.md`.
- **`_dk_types` learns two things:**
  1. an optional per-type `description:` in the schema, rendered after the
     type name;
  2. the *actual* schema path it loaded, instead of the hardcoded
     `things/_schema.yaml` — at the root the file is `_schema.yaml`, and a
     generated block that misnames its own authority is the defect this
     sprint exists to remove.
- **Estate blast radius: zero, by construction.** Both changes are
  byte-stable for every existing domain — none declares `description:`, and
  every domain's schema *is* at `things/_schema.yaml`. This was a design
  constraint, not a happy accident: the discarded alternative (rendering
  tool-owned descriptions for the reserved types) would have drifted all
  thirteen estate domains' managed blocks at once and **blocked their
  commits** with a coherence Error until each was regenerated. Sprint 2's
  F5 drift was advisory; this one would not have been.
- **The reserved types lose their root prose, deliberately.** Their
  descriptions were restatement: `kernel.md` already names the reserved
  set and routes each to its owning spec. That is the *delete* leg
  applying to a section the *derive* leg is otherwise handling.
- **Re-open condition checked:** the scope decision said the block reverts
  to a check if `description:` couples the schema to presentation. It does
  not — a description sits beside `statuses:` and `required_fields:` as
  the schema documenting its own vocabulary. Proceeding with derive.
- **Focused tests:** `test_mdllm.py -k domain_kernel`,
  `test_template_instantiation.py`. New: descriptions render when
  declared; output is byte-identical when they are not (the estate
  guarantee, pinned); the root's block names `_schema.yaml`; the existing
  generic drift check fires at the framework root.

### C4 — F8a *check*: the two annotated prose sections

Both are authored prose carrying a derivable annotation, so both are
checked rather than generated — generation would destroy the one-line
descriptions that are the sections' actual value.

- **Catalog annotations.** Every spec bullet in
  `## Framework Specifications (Things)` carries a parenthetical `type:`
  and `status:` pair; each is compared against that file's live
  frontmatter. 28 bullets parse today and **all 28 agree** — the check
  lands green, pinning truth rather than repairing drift. Severity
  **Error**: same class as kernel drift, a one-line fix, and the whole
  point is that a spec's status change and its catalog line land in the
  same commit.
- **Tier-2 routing completeness.** Every file in `TIERS` Tier 2 must
  appear in the Tier-2 routing table, and every file the table names must
  exist on disk. **One direction only, deliberately:** the table
  legitimately routes four `docs/` guides that are outside both `TIERS`
  and the `.markdownllm` catalog, so a mirror check would fire on correct
  prose. The reverse direction is already covered where it *is* total
  (`TIERS`-to-catalog, both ways). Severity **Error** for a missing spec,
  per the owner's wording; **Error** for a row naming a file that does not
  exist.
- **Touches:** `coherence.py`, framework-root scope only (inside the
  existing `.markdownllm` guard).
- **Focused tests:** `test_coherence_repository_view.py`, plus new cases
  for a drifted catalog status, an unrouted Tier-2 spec, and a row naming
  a missing file — each asserted on a fixture, never on the live corpus.
- **Budget:** first N3 re-measurement point.

### C5 — F8b: the boundary-term evidence check

- **Shape:** an `--audit-terms` leg on `mdllm boundary`. For each entry in
  the local, gitignored `.boundary-terms`, report whether it occurs in the
  repository's own tracked content. A hit means the entry is either noise
  (and is making the history leg permanently red) or a leak already
  committed — both actionable, which is what makes it a check.
- **The constraint that shapes it:** the check reads the file **in place**
  and must never print, copy, log or commit a term. Reports are by count
  and by file, never by term. The scope decision's second re-open
  condition binds here: if the check cannot be built without exposing its
  subject, it is dropped rather than weakened.
- **Why `boundary` and not `coherence`:** the terms file is boundary's own
  subject, and absent-file-is-a-no-op already lives there.
- **Focused tests:** the lifted boundary section. New: a fixture repo with
  a synthetic terms file, asserting the count-only report shape and that
  no term appears in output.
- **Not run in the pre-commit hook** — it is an operator-invoked audit, so
  it spends nothing against N3. That is a deliberate call: the file is
  operator-owned and its contents change between commits for reasons the
  floor cannot see.

### C6 — F8b: the perimeter currency check

- **Shape:** extend the existing example-`framework_version_seen` check to
  the rest of the perimeter — `README.md`, `docs/first-hour.md`,
  `CONTRIBUTING.md` — comparing each surface's declared last-reconciled
  version against the `.markdownllm` sentinel. Info severity: this is a
  *cadence* signal, not a defect, and
  `a-check-that-always-fires-teaches-the-operator-to-ignore-it` applies
  directly.
- **Where the pin lives:** each perimeter surface carries an explicit
  reconciled-at version marker. A surface with no marker is not flagged —
  absence is not drift, and inventing a marker for a file that never had
  one would make the check fire on its own installation.
- **Live evidence it is needed:** both examples are firing right now,
  pinned at 3.33.0 against a 3.34.0 sentinel.
- **Focused tests:** `test_coherence_repository_view.py` fixture cases for
  behind / equal / unmarked.
- **Budget:** second N3 re-measurement point.

### C7 — F8b: the review-9 survivor promotions that survive C2/C3

Re-read against the ninth review's actual findings
(`reviews/REVIEW-independent-2026-08-09.md`), not the backlog's summary of
them:

- **Survivor 7 — the `CORE_FIELDS` admission criterion — promotes cleanly
  and inverts into C1.** Check: a `known_fields` entry that is *already*
  in `CORE_FIELDS` is a redundant registration (Info, "already universal —
  drop it"). Same-builder, no suppression list. C1 fixes the outward
  direction of the same fault; this catches the inward one.
- **Survivors 3 and 6 — the trigger-type count and the index-signal
  count — promote as stated-count checks**, the exact shape of the
  framework-map subcommand-count check that already works. Scoped to live
  operative surfaces (the catalog's spec files, `AGENTS.md`, `kernel.md`)
  and *structurally* excluding `CHANGELOG.md`, `reviews/` and `things/` —
  those are historical records, where "four trigger types" was true when
  written. That exclusion is structural, not a suppression list: it is
  defined by what a surface *is*, not by which findings were inconvenient.
- **Survivor 5 — the reserved-set restatements — is judged at build.** If
  no shape exists that keys to `RESERVED_STATUSES` without a
  hand-maintained list of which prose lists "count", it stays with the
  human walk and the reasoning is recorded in place. That is the same
  judgement that sank the retired-vocabulary check, and repeating it
  honestly is cheaper than repeating the check.
- **Survivors 1, 2, 4** are not promotable and are not attempted: each was
  a semantic contradiction between a spec and its own kernel block, which
  is judgement, not a same-builder mirror.
- **Focused tests:** fixture cases per check.
- **Budget:** third N3 re-measurement point.

### C8–C9 — F8c stretch: probes 1 and 2

Started only with C1–C7 verified.

- **Probe 1 — fresh-clone boot.** Clone a gated domain cold; assert doctor
  reports setup-ordering (not blocking) before attestation and clean
  after. Chosen because the plan records this one as having already
  outperformed every cold read; the work is making it repeatable.
- **Probe 2 — scaffold birth.** Scaffold into a temp repo; assert the
  birth commit lands, blocks match a fresh generation, prompts are
  delivered graph-stripped, and the gate blocks the *second* commit
  without attestation. Chosen because this is the flow whose first Windows
  CI execution produced 56 failures from one cause a month after the code
  was believed correct.
- **Home:** `tools/tests/`, so CI runs them for free — the decision the
  owner left open at build time, settled here on that ground.
- **Portability:** both probes construct temp repos, so both inherit the
  `RUNNER_TEMP` lesson from sprint 2 — provoked portably or not at all.

## Budgets and how each is proven

| ID | Budget | Proven by |
|---|---|---|
| N3 pre-commit, root | <= 12s | re-measured after C4, C6, C7 — the three commits that add hook-path work; the run records all three, not just the last |
| N4 pre-commit, live domain | <= 5s | measured once after C7; C3's zero-drift guarantee means a domain's hook path is unchanged, so this is a check on that claim, not on new work |
| N7 full suite | <= 12 min | the verify-stage gate, once |
| N6 focused loop | <= 120s | each commit's own focused set |

`mdllm boundary --audit-terms` is outside the hook path by design and has
no budget row; if that changes, it inherits N3.

## Risks and mitigations

1. **A new Error severity blocks a legitimate commit.** C4 makes catalog
   drift an Error. Mitigation: it is measured green across all 28 bullets
   today, so it cannot block anything that is currently correct; and the
   remedy is a one-line edit named in the finding text.
2. **The count checks over-fire on historical prose.** Mitigated by the
   structural surface scope in C7, and by the rule that if the scope needs
   a per-finding exception the check does not ship.
3. **The boundary audit leaks its subject.** Mitigated by count-and-file
   reporting only, tested by asserting no term appears in output — and by
   the standing instruction to drop rather than weaken.
4. **Sprint sprawl.** C8–C9 are stretch and gated on C1–C7 verifying.
   Probes 3–5 are not in this sprint at all and stay owned by
   `coherence-mechanism-build`.

## What this design deliberately does not do

No new framework primitive. No daemon or persistent cache. No weakening of
the transaction contract. No check that needs a suppression list. And no
attempt to complete `coherence-mechanism-build` — its exit condition
requires a *post-release cold read* returning zero fix-residue-class
findings, which is an operator act after publication, not a sprint
deliverable.
