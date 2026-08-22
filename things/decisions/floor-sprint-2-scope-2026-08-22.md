---
id: floor-sprint-2-scope-2026-08-22
type: decision
status: made
version: 1.0
created: 2026-08-22
tags: [sprint-scope, floor, moscow, analysis, structure]
informed_by:
  - id: floor-block-requirements-2026-08
    commit: f6dccaf9ed4c3309fd871ce622715a6528fe7d12
  - id: floor-structure-residue
    commit: e98cdd9a8cdcb3f40cc5eed936f7b3c9a485d656
  - id: run-floor-sprint-1-2026-08
    commit: 967773cb50f2dc9b9f661f8309c7aaacded8f4f1
  - id: floor-sprint-1-scope-2026-08-21
    commit: 967773cb50f2dc9b9f661f8309c7aaacded8f4f1
linked_things:
  - id: run-floor-sprint-2-2026-08
    relation: informs
    notes: "The run this analysis-stage decision scopes."
---

# Decision: Floor Sprint 2 Scope

Made by the agent under the operator's execution handover. Sprint 1's scope
decision already named this sprint's shape — "one coherent structural
sprint" — and its seal record left the inventory honestly open. This cut
formalises it against the requirements ledger's v1.1 revision.

## The cut

**Necessity** — sprint 2 fails without these:

- **F3** — fitness-gate inversion: the vendor-vocabulary check becomes total
  over neutral modules by construction, exceptions by declaration. Highest
  leverage in the residue — it is the check that protects every other
  structural claim, and the reshaping below (F4/F5) lands *under* the
  inverted gate rather than being born ungated.
- **F5** — adapter duplication collapse (shared project-hook helper), carrying
  the probe existence-guards into the regenerated hook bodies (~0.65s per
  lifecycle hook invocation; the sh fragment's ~330ms dead spawn rides the
  same regeneration).
- **F4** — hook-byte contract moved out of the birth module. Rides F5's
  reshaping per sprint 1's recorded layering evidence (`SH_RESOLVE` in
  runtime imports the leaf); landing it alone was ruled a half-inversion.

**Should** — taken if the sprint holds its shape:

- **F6** — shared test fixture module extracted, then the test monolith split
  along its existing banners. Unblocks all future test decomposition and
  sharpens F10's focused-selection convention.
- **F7 (record leg)** — the single-platform limitation recorded where
  portability claims are read. This leg is prose + config and completes
  within the sprint.

**Stretch** — started only with necessity + should verified:

- **F7 (matrix leg)** — the Linux CI workflow authored. Its *proof* (a green
  run) is publication-gated — CI executes only after the operator's push — so
  the sprint can land the config but never verify it; the verify record must
  say so rather than claim coverage.
- **F14** — worktree-walk residual bounded (index-assisted corpus listing or
  deeper pruning; post-suite session-start approaches steady state).

**Deferred, with reasons** — not this sprint:

- **F8** (root AGENTS.md derivation, admitted checks, flow probes) → sprint 3,
  per sprint 1's sequencing rationale: derived surfaces should be generated
  from a settled module layout, and this sprint is the one reshaping it.
- **F2** (eval-isolation machinery) — its owner (`evidence-and-eval-backlog`)
  is operator-sequenced and now 25 days stalled; pulling it into a structure
  sprint would neither fit the theme nor un-stall the plan. Surfaced to the
  operator at seal instead.
- Smaller same-family residue items (duplicate staged-atomic-write, the
  prose-matching diagnostic, resemblance-classifying inspectors, hand-restated
  pins) — folded into F5/F6 *only where the reshaping touches them anyway*;
  otherwise they stay owned at `floor-structure-residue`, unstarted, not
  silently absorbed.

## Why this cut

The theme is *make the structure honest before deriving from it*: invert the
one gate that protects structural claims, collapse the duplication that gate
should have caught, fix the dependency direction, and give the test corpus a
shape that can be decomposed. Sprint 3's derivation work (F8) then generates
from a settled layout. The remedy's settled constraints bind every item: no
transaction weakening, no daemons or persistent caches, typed non-definite
results preserved.

Re-open condition: if design shows the F5 reshaping cannot carry F4 without
breaching the adapter vendor-vocabulary rule, F4 reverts to deferred rather
than the rule bending — the rule is what F3 exists to enforce.
