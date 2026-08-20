---
id: session-start-hardening
type: plan
status: in-progress
version: 1.3
created: 2026-08-19
priority: high
tags: [session-start, tier-0, emission, kernel, gates, adapters, hardening, evidence]
linked_things:
  - id: cowork-remote-phase5-evidence-2026-08-19
    relation: references
    notes: "Live proof that preview truncation and marker-only freshness could manufacture a false receipt claim."
  - id: harness-capability-evidence-matrix-2026-08-20
    relation: references
    notes: "Shows which historical live surfaces can be re-probed and why those records do not accept changed definitions."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: implements
  - id: a-prerequisite-declared-only-inside-its-target-cannot-gate-it
    relation: implements
  - id: session-start-loses-to-the-first-request
    relation: implements
  - id: an-honest-ledger-replicates-full-compliance-does-not
    relation: references
  - id: pretooluse-action-boundary-gate
    relation: references
  - id: vendor-harness-adapter-foundation
    relation: references
  - id: orchestration-specification
    relation: references
  - id: partial-coverage-quiets-the-uncovered-steps
    relation: references
---

# Session-Start Hardening

## Current purpose

Tier 0 is now delivered as content or loudly deferred, its computable digest
is mechanical, and the remaining judgement has an explicit `orient` pull. The
plan remains open because changed delivery/attestation definitions require
fresh product events; deterministic tests cannot accept their own harness
projection.

The detailed baseline predictions, phase diaries and reconciliation notes are
preserved in Git:

`git show 27b95e7:things/plans/session-start-hardening.md`.

The forward build/evidence boundary is
[`harness-capability-evidence-matrix-2026-08-20`](../../evidence/harness-capability-evidence-matrix-2026-08-20.md).

## Problem statement

Agents economise instructions that ask them to load more content, and emitted
mechanics can quiet the judgement they do not cover. A successful command or a
fresh timestamp therefore cannot stand in for receipt, reading or compliance.
The system must:

1. put the non-negotiable Tier-0 contract in the delivery channel;
2. distinguish whole delivery, explicit deferral and missing/elided content;
3. bind receipt evidence to the actual contract definition;
4. compute only the digest signals the floor can answer;
5. route the irreducible judgement through an explicit invocation; and
6. grade real consequences, never assurances.

## Completed phases

| Phase | State | Durable result |
|---|---|---|
| 0 — baseline | complete | Five cross-harness/model observations scored the delivery and masking hypotheses before the contract changed |
| 1 — position | complete | Read-side prerequisite moved into the upstream kernel; the gate no longer lives only inside the skill it gates |
| 2 — delivery | complete in code | Direct channels emit the kernel whole with hash/line integrity; budgeted hook channels defer loudly to an openable receipt; contract emission writes definition-bound evidence |
| 3 — digest | complete | Velocity trend, high/critical stall lines and self-answering trigger cues are computed and emitted without pretending to judge the residue |
| 4 — residue | complete | `orient` owns the deep judgement walk; entry contract, prompts and operator probe ladder use one two-voice model |

## Current receipt semantics

- Direct/manual/Codex/bootstrap channels emit the kernel whole and include an
  integrity trailer. A missing trailer or `[truncated]` means the channel did
  not deliver the claimed whole.
- The protected lifecycle-hook channel explicitly defers the kernel and names
  the full file read owed before acting on domain state.
- Preview-truncating routes persist a full receipt artifact rather than
  guessing a product-specific chunk threshold.
- The session attestation records a SHA-256 fingerprint of the operative
  kernel plus domain `AGENTS.md`, together with evidence and delivery levels.
  It does **not** claim `read`, `applied` or `compliant`.
- The session gate checks that contract fingerprint. Unrelated HEAD movement
  does not expire it; a contract change does. Legacy timestamp-only records
  remain usable but warn that contract currency is unknown.

These are implementation statements at the current working boundary, not a
live-harness acceptance. The historical Cowork packet used older marker-only
semantics and remains historical.

## Phase 5 — re-test, disposition and seal

- [ ] Re-run the probe ladder on at least two harnesses: one Claude Code and
  one Codex surface. Record exact build, contract fingerprint, delivery level,
  transcript consequence and any truncation/manual recovery.
- [ ] Confirm the next cold direct session receives Tier 0 whole and the next
  budgeted-hook session defers it loudly before domain-state action.
- [ ] Update `emitted-content-is-read-instructed-content-is-economised` from
  the new evidence; emission remains delivery, not behavioral compliance.
- [ ] Re-score and disposition
  `a-prerequisite-declared-only-inside-its-target-cannot-gate-it`,
  `session-start-loses-to-the-first-request` and
  `partial-coverage-quiets-the-uncovered-steps`.
- [ ] Record the resolved-for-now decision on
  `pretooluse-action-boundary-gate`: emission first; reopen an action gate only
  if live evidence shows an irreversible pre-action failure that Git cannot
  recover.
- [ ] Decide from evidence whether any per-domain skill emission is earned.
  Do not build it merely because the mechanism is imaginable.
- [ ] Reconcile specs/docs/generated kernel, add the release changelog/version,
  and offer per-domain refresh rather than silently migrating the estate.

## Exit condition

A cold session on each accepted harness begins with Tier 0 either landed whole
or explicitly owed, its attestation is bound to the contract actually emitted,
the digest supplies computable attention, and `orient` carries the remaining
judgement. The evidence record states exact builds and does not promote
delivery into a claim of compliance.
