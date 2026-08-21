---
id: floor-block-requirements-2026-08
type: plan
status: in-progress
version: 1.0
created: 2026-08-21
priority: high
tags: [requirements, floor, performance, tests, concurrency, sprint]
linked_things:
  - id: run-floor-sprint-1-2026-08
    relation: informs
    notes: "The run whose requirements stage this thing satisfies."
  - id: substrate-review-consolidated-remedy-2026-08-20
    relation: derived-from
    notes: "The finding-to-owner ledger supplies every review-sourced requirement; owners stay canonical there — this thing adds the bottleneck census and the budget table, never duplicate task lists."
  - id: floor-structure-residue
    relation: references
  - id: coherence-mechanism-build
    relation: references
  - id: evidence-and-eval-backlog
    relation: references
  - id: a-sharing-parameter-no-caller-passes-is-a-fix-that-did-not-happen
    relation: references
    notes: "F9's rationale: the structural tests exist because the four-scan fix was landed as an unwired parameter and believed complete for two days."
---

# Floor Block Requirements — 2026-08

The requirement set for the operator's floor block (recorded execution order,
consolidated remedy → Operator Rulings 2026-08-21). Requirements are
problem-driven: every row cites its evidence. Owners named in the remedy's
ledger stay canonical; this thing exists so the block's requirements —
functional and non-functional — are one committed surface a sprint can be cut
from.

## Reference environment

All budgets are measured on and bound to the operator's machine (Windows 11
Pro 10.0.26200, repo at the framework root with 14 nested estate repos, git
process spawn ~300ms cold / ~150ms warm, libyaml compiled in). Budgets are
per-machine facts, not portable claims; a second reference machine gets its
own column when CI supplies one.

## Measured baseline (2026-08-21, commits 2ede668 → fbe7b52)

| Path | Before | After (today) | Evidence |
|---|---|---|---|
| session-start, framework root, warm | 13.5s (67.8s on 2026-08-19) | ~2.1s | commit 2ede668 |
| estate-sync, root, 14 repos, online | ~21s | ~4.8s | commit 2ede668 |
| validate, root, worktree view | ~13s | ~4.5s | commit 2ede668 |
| validate, root, index view (hook path) | 302s | ~8.7s | commit fbe7b52 |
| coherence, root, index view (hook path) | 216s | ~9.6s | commit fbe7b52 |
| pre-commit hook total, root | ~8.7 min | ~20s | fbe7b52, observed |
| validate / session-start, live domain | — | ~0.7s / ~1.3s | measured 2026-08-21 |
| full test suite, serial | 37 min (690 tests) | unchanged | run 2026-08-21 |
| lifecycle hook wrapper probe overhead | ~0.65s per invocation | unchanged | measured 2026-08-21 |

## Functional requirements

Review-sourced (owner in brackets; the remedy ledger is canonical):

- **F1** — Perimeter truth corrections: strict calc severity wording,
  publication-teaching in the installed session-close commands, full-SHA
  decision pins in template + worked example. [floor-structure-residue]
- **F2** — Eval-isolation machinery: agent workspace constructed outside the
  canonical repo, no canonical write channel, byte-identity proof of the seed
  before/after an adversarial run. Machinery only; the rerun is
  operator-gated. [evidence-and-eval-backlog]
- **F3** — Fitness-gate inversion: vendor-vocabulary check total over neutral
  modules by construction, exceptions by declaration. [floor-structure-residue]
- **F4** — Hook-byte contract moved out of the birth module (dependency
  direction). [floor-structure-residue]
- **F5** — Adapter duplication collapse, carrying the probe existence-guard
  (~0.65s per lifecycle hook invocation) into the regenerated hook bodies.
  [floor-structure-residue]
- **F6** — Shared test fixture module extracted; test monolith split along
  its banners. [floor-structure-residue]
- **F7** — CI matrix widened to Windows + Linux, or the single-platform
  limitation recorded where portability claims are read. [floor-structure-residue]
- **F8** — Root AGENTS.md derivable sections generated (types block, catalog
  statuses, routing completeness); admitted mechanical checks; clean-clone
  flow probes. [coherence-mechanism-build]
- **F9** — Structural anti-regression tests for the consolidated derivation
  paths: session-start must fail a test if it regresses to repeated corpus
  scans or N+1 history walks (index-scan spawn bound landed 2026-08-21;
  session-start's own bound is owed). [remedy Phase 0 residue]

Bottleneck-census-sourced (new; evidence measured today):

- **F10** — Test execution workflow: parallel execution (pytest-xdist),
  tier markers (fast unit vs git-fixture integration), and a documented
  focused-selection convention so the inner loop runs affected files only;
  the full suite becomes a verify-stage gate, not an inner loop.
- **F11** — Pre-commit concurrency: boundary/validate/coherence legs run
  concurrently against the same frozen tree (safe by immutability); wall
  time approaches max(legs), not sum.
- **F12** — Remaining per-thing git calls batched (quarantine findings:
  11 spawns ≈ 2.9s at the root today).
- **F13** — Validate's three corpora (root + examples) evaluated
  concurrently.

Constraints carried from the remedy (settled, restated as requirements):
no weakening of the transaction contract; no daemons, persistent caches, or
new framework primitives for speed; typed non-definite results everywhere the
floor could not look.

## Non-functional requirements — the budget table

Budgets any in-scope change must meet and the verify stage must measure.
"Root" = this framework checkout, the estate's worst case.

| ID | Path | Budget | Today | Headroom rationale |
|---|---|---|---|---|
| N1 | session-start, root, warm | ≤ 5s | ~2.1s | hook budget 60s; 3× cold-cache allowance inside 5s |
| N2 | estate-sync, root, online | ≤ 8s | ~4.8s | slowest single fetch ~2s; concurrency holds the sum |
| N3 | pre-commit hook, root | ≤ 12s | ~20s | met by F11 (max ≈ 9.6s) + F12 |
| N4 | pre-commit hook, live domain | ≤ 5s | ~2–4s | the surface a domain operator feels every commit |
| N5 | post-write validate, live domain | ≤ 3s | ~0.7s + wrapper | met further by F5 |
| N6 | focused test loop (one affected file) | ≤ 120s | 30–75s typical | inner-loop tolerability on this machine |
| N7 | full suite | ≤ 12 min | 37 min | F10 parallelism; 8 workers realistic |
| N8 | any lifecycle hook step | ≤ ⅓ of its harness budget at the root | varies | headroom is the requirement — 67.1s/60s must never recur |

## Out of scope for the block

The retrospective (sequenced after, operator's order); sync-scope redesign
(D2 declined for now, dated ruling in the remedy); machine-level remedies
(Defender exclusion is a system security setting — operator-only); any
harness receipt or release work (Phases 5–6 carriers own them).
