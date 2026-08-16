---
id: lifecycle-output-allocation-acceptance-2026-08-16
type: artifact
status: evolving
created: 2026-08-16
tags: [harness, lifecycle, truncation, execution-evidence, phase-6r]
linked_things:
  - id: lifecycle-output-truncation-2026-08-14
    relation: implements
    notes: "Records the bounded structural allocation that replaces the global tail slice."
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Deterministic implementation and estate-refresh evidence for Gate 6R; Claude automatic-dispatch acceptance remains pending."
  - id: the-harness-bound-path-is-the-least-tested-path
    relation: supports
    notes: "Acceptance asserts retained orientation sections, not merely exit zero or hook success."
---

# Lifecycle output allocation acceptance — Codex implementation record

This record fixes the boundary identified by
`lifecycle-output-truncation-2026-08-14`: the lifecycle runner remains bounded,
but no longer preserves one global tail at the expense of the operator's
orientation. It is **implementation acceptance**, not yet the independent
Claude automatic-dispatch record required to close Gate 6R.

## The settled boundary

- The inward-owned lifecycle binding declares a 2,200-character total output
  envelope and a 200-character runner reserve.
- Each step declares a protected character share, parallel to its protected
  time share: session-start reserves 450 characters for estate-sync and 1,450
  for orientation; post-write reserves 1,900 for validation.
- A step may consume unused capacity, but it cannot erase the protected
  representation of a later step.
- Compaction recognises only neutral text structure: headings,
  blank-delimited sections, labelled runner blocks, and structurally marked
  top-level list sections. It contains no domain-field or vendor vocabulary.
- Every structural section receives a fair share. Truncation is explicit,
  step labels and return codes survive, and each `StepExecution` retains the
  complete raw stdout and stderr outside the model-visible envelope.
- Both adapters include the complete character-allocation contract in their
  managed definition hashes. The former 5R.5 projection is exact recognised
  legacy data, so its attestations become stale honestly.

## Consequence tests

The deterministic large-report regression uses output above the envelope and
asserts the side effect the session depends on. Within the strict runner bound
it still contains:

- estate state, including a diverged repository signal;
- Version;
- Velocity;
- Open loops; and
- Triggers.

It also asserts both step labels, an explicit truncation marker, complete raw
operation output, and a serialized Codex envelope no larger than the adapter's
2,500-character `additionalContextLimit`.

A read-only probe against a real large regulated-domain report measured 6,060
characters before estate-sync. Passing that report through the production
structural allocator produced 2,042 model-visible characters while retaining
`DIVERGED`, Version, Velocity, Open loops, Triggers, and Upcoming sections. The
probe did not write a session attestation.

## Deterministic verification

- Focused ports, lifecycle runner, Claude contract, Codex adapter, installer,
  and architecture-fitness suite: **128 passed**.
- Complete `tools/tests` suite with an external base directory: **465 passed**
  in 263.98 seconds.
- The only pytest warning was the managed shell's denied repository-local
  `.pytest_cache`; the external test base remained usable and no test failed.

## Reviewed migration and ownership preservation

The root and every one of the 13 nested domains classified both managed
artifacts as exact `legacy-output-tail-v1`. The reviewed refresh path changed
only `.claude/settings.json` and `.codex/hooks.json`, then a second dry run
reported both artifacts current/no-op.

Two domains retained composite operator-owned Claude settings. Three domains
carried an untracked `.claude/settings.local.json`; its SHA-256 was compared
before and after refresh and remained byte-identical. No domain semantics were
changed.

Root post-refresh artifact hashes:

- `.claude/settings.json`:
  `2232dd0c79bef65deb4b0e0e42fdcbbe871b78a6177e75cd5be1081f84bce264`
- `.codex/hooks.json`:
  `433db4b323ce91642d5d5c2c1daa2484c6eab0aff388f5970aea0567383e604f`

Current root definition hashes:

| Adapter | SessionStart | Post-write |
|---|---|---|
| Claude Code | `sha256:df8e8f5f9422754302552bfdbed1d12692c961b8dd244045bf13f0a2a65b4e2a` | `sha256:36fd9fc6350291fea06d6d5cfbd9ca0d0bce7571a7e5bdb9eb80af2097d64da2` |
| Codex | `sha256:f2b78cb9f51a98f3fdaaf4917c9576ddcc501eaef037c6b5e53a1f4cfbe11e76` | `sha256:e95a4046a29adcadac24f8236ff8d3ca228df6b56e07918c45104c6ce20cdb2a` |

Each of the 13 domains committed the two managed adapter artifacts in its own
repository. Exact local commit identifiers and domain names remain estate
state rather than being copied onto the public framework surface. Automatic
domain publication attempts that could not reach GitHub remain visible as
publication debt. The framework root was not pushed.

## Evidence boundary still open

Deterministic execution and direct allocation probes earn designed-for, not
verified-on. Gate 6R remains open until Claude independently accepts the final
framework commit and a real, automatically dispatched large-domain
SessionStart transcript demonstrates every orientation section under the
bound, correlated with a fresh current-definition attestation. No earlier
attestation is reused.
