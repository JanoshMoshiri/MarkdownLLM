---
id: floor-sprint-1-scope-2026-08-21
type: decision
status: made
version: 1.0
created: 2026-08-21
tags: [sprint-scope, floor, moscow, analysis]
informed_by:
  - id: floor-block-requirements-2026-08
    commit: 8521d0d7b99e1a72eb68ca8fa513012ec59b1a6f
  - id: substrate-review-consolidated-remedy-2026-08-20
    commit: 1209f646767c16dfff2a36c574095aca3f97a0a1
  - id: independent-substrate-current-state-review-2026-08-20-codex
    commit: 35de802608d896e4e533ed6c2990d89966948e17
  - id: independent-substrate-review-2026-08-20-claude
    commit: ed5cb3d1f0f8ccd15a30627293c79290dd9cf51c
linked_things:
  - id: run-floor-sprint-1-2026-08
    relation: informs
    notes: "The run this analysis-stage decision scopes."
---

# Decision: Floor Sprint 1 Scope

Made by the agent under the operator's 2026-08-21 execution handover. The cut
is deliberately smaller than the requirement set — one sprint, recordable and
scoped, per the operator's direction not to fix everything in one round.

## The cut

**Necessity** — sprint 1 fails without these:

- **F9** — session-start structural anti-regression tests (repeated-scan and
  N+1-history bounds). Protects the week's measured wins before anything else
  moves; the index-scan bound landed 2026-08-21, session-start's own is owed.
- **F10** — test execution workflow: pytest-xdist parallelism, tier markers,
  documented focused-selection convention; full suite becomes the
  verify-stage gate. Targets N6/N7. The meta-bottleneck: every later sprint
  inherits this loop.
- **F11** — pre-commit leg concurrency against the frozen tree. Targets N3.
- **F1** — perimeter truth corrections (three prose surfaces teaching weaker
  or more permissive behaviour than the floor executes). Small and of high
  epistemic weight — prose must not contradict the executable.

**Should** — taken if the sprint holds its shape:

- **F12** — quarantine git-call batching (with F11, secures N3's margin).
- **F13** — corpora-concurrent validate.
- **F4** — hook-byte contract dependency move (small, sharply bounded).

**Stretch** — started only with necessity + should verified:

- **F2** — eval-isolation machinery (agent pre-work half only).
- **F6** — shared test fixture extraction (only if F10's marker work makes it
  nearly free).

**Deferred, with reasons** — not this sprint:

- **F3** (fitness-gate inversion), **F5** (adapter collapse + hook regen),
  **F6** in full, **F7** (CI matrix) → sprint 2: one coherent structural
  sprint; F5 touches hash-attested surfaces estate-wide and deserves
  undivided verification.
- **F8** (coherence-mechanism build) → sprint 3: sequenced after structure so
  derived surfaces are generated from a settled module layout, not one about
  to be reshaped.

## Why this cut

Sprint 1's theme is *protect and accelerate the loop*: lock the perf gains
behind structural tests, make the development inner loop fast, meet the
budget table where it is currently missed (N3, N6, N7), and stop prose from
teaching falsehoods. Structure (sprint 2) and derivation (sprint 3) then land
on a fast, protected loop instead of paying the 37-minute serial gate on
every iteration. The remedy's settled constraints bind every item: no
transaction weakening, no daemons or persistent caches, typed non-definite
results preserved.

Re-open condition: if design shows F11 cannot meet N3 without F12, F12 is
promoted to necessity rather than the budget being relaxed — budgets moved
only by a recorded decision, never by drift.
