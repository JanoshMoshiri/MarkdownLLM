---
id: lifecycle-budget-allocation-acceptance-2026-08-13
type: artifact
status: evolving
version: 1.0
created: 2026-08-13
tags: [harness, lifecycle, timeout, migration, codex, claude-code]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Codex implementation and deterministic acceptance record for the returned Phase 5R.5 lifecycle-budget defect."
---

# Lifecycle Budget Allocation Acceptance — 2026-08-13

## Scope

This is the Codex implementation record for Phase 5R.5. It does not absorb or
reclassify the separately committed domain-session field report. It begins
from Claude's accepted 5R.4 mechanism at `db4a5dd` and the one returned shared
runtime finding: the framework-root automatic SessionStart measured
`estate-sync` at 59.8 seconds and `session-start` at 36.1 seconds, while the
neutral runner imposed a hard 25-second orientation ceiling and returned 124.

## Correction

`LifecycleStep` now declares `protected_seconds`, not a guessed hard timeout.
The runner holds every later step's protected allocation back from preceding
steps. When a step becomes current, it receives the remaining application
balance and can therefore inherit time unused earlier. The absolute 120-second
handler, 105-second lifecycle, 5-second runner reserve, and 100-second
application deadline remain unchanged.

For the measured root case, estate-sync is still capped at 75 seconds because
orientation's 25 seconds remain protected. If it completes at 59.8 seconds,
orientation receives approximately 40.2 seconds rather than being truncated
at 25. The correction does not make orientation unbounded and does not move
enforcement out of Git pre-commit.

The inward dataclasses reject empty bindings, non-positive protected values,
and protected totals larger than the application budget before execution.
Both adapters serialize the renamed semantic field into their managed
definition hashes, so old fixed-step hooks and attestations cannot be treated
as current.

The earned architectural contract is recorded separately in the owning
code-architect domain as `lifecycle-budget-allocation-boundary`.

## Root Migration

The exact tracked 5R.4 root projections were captured before correction as
immutable recognition data:

- `claude-hooks-root-fixed-step-v1.json`
- `codex-hooks-root-fixed-step-v1.json`

Before apply, both live artifacts inspected as `current=false` with
`legacy-id=legacy-root-fixed-step-v1`. A reviewed all-selected
`adapter-install . --harness all --refresh-legacy --dry-run` proposed exactly
two refreshes. The explicit atomic apply wrote both. Afterward both inspect as
`current=true`, with no legacy ID. The tracked diff changes only the two Claude
hash literals and the corresponding POSIX/Windows Codex hash encodings;
permissions and unrelated operator bytes remain unchanged. No nested domain
projection was migrated.

The managed sandbox could not stage temporary files beneath the protected
root adapter directories; a stack trace stopped in `tempfile.mkstemp` before
either replacement. Both artifacts remained legacy. The same reviewed command
then ran with scoped filesystem permission and atomically applied two writes.
Four staging files created by the interrupted sandbox attempts were removed
after their parent and filename pattern were checked.

## Deterministic Verification

- Focused ports, lifecycle runner, Claude/Codex adapters, install/refresh,
  diagnostics, scaffold selection, architecture fitness, and runtime:
  **173 passed**.
- Complete suite using an external basetemp: **465 passed** in 323.21 seconds.
- An initial in-repository basetemp run produced 463 passes and two expected
  fixture-isolation failures because nominal non-repositories inherited the
  framework's parent `.git`; both passed when rerun outside the repository.
- Framework validation: 189 framework things, 6 compliance examples, and 14
  life-manager examples clean with zero errors, warnings, or informationals.
- Framework coherence: clean after the relationship index rebuild.
- Code-architect validation: 33 things clean. Its relationship and schema
  indexes were rebuilt and the interface contract committed in its owning
  nested repository; coherence retained only the two pre-existing
  informational unused-type notices.

## Remaining Independent Gate

This record earns deterministic/design acceptance only. Claude must rerun the
unchanged native PowerShell 5.1 reproduction because the neutral lifecycle
runner changed, then trigger a real automatic root SessionStart. Acceptance
requires all of the following consequences:

- `estate-sync=0` and `session-start=0` within the declared envelope;
- emitted version, velocity, open-loop, and trigger orientation content;
- a fresh clone-local session-gate attestation;
- harness-owned transcript/debug correlation with the current definition.

Exit zero, `hook_success`, or a generic hash-bound harness execution
attestation alone is insufficient. Phase 6 remains blocked until that return
gate is accepted.
