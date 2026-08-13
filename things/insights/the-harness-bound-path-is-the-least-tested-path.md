---
id: the-harness-bound-path-is-the-least-tested-path
type: insight
status: active
version: 1.0
created: 2026-08-13
session: 2026-08-13
source: field
confidence: high
origin: stated
linked_things:
  - id: portability-claims-need-execution-tests
    relation: supports
    notes: "That insight measures availability per environment; this one names the sibling gap — a path can be available, execute, exit 0, and still not do the thing the operator's contract depends on."
  - id: field-report-2026-08-13-domain-session
    relation: derived-from
    notes: "First instance: the harness-bound --assistant rendering emitted the contract but never attested, so the strict gate fired against the integration that satisfies its intent."
  - id: claude-gate-5r4-acceptance-2026-08-13
    relation: derived-from
    notes: "Second instance, same day, different mechanism: the reconciled root's session-start step exceeded its per-step budget, so orientation truncated silently under surface-and-continue."
---

# The harness-bound path is the least-tested path

## The observation

Two defects surfaced on 2026-08-13, hours apart, in unrelated mechanisms.
Both had the same shape: **the path a harness actually runs diverged from
the path everyone tests, and the divergence was invisible because both
paths exit 0.**

- A live domain session opened through the scaffolded hook, which runs
  `session-start . --assistant`. That rendering emitted the Tier-0 contract
  and returned before writing the attestation, so under
  `session_gate: strict` the gate blocked every commit — firing against the
  one integration that satisfies its own intent. 456 tests passed
  throughout; the plain rendering, which everything tested, attested
  correctly.
- The reconciled framework root's `session-start` step exceeded its
  per-step budget and truncated, so a session began with no orientation.
  The hook still exited 0 by design (`surface-and-continue`).

## Why the usual defences miss it

A harness-bound path is defended by the same tests as the interactive one,
and those tests pass — because they exercise the *function*, not the
*integration*. Three properties conspire:

1. **Advisory-by-design.** A lifecycle hook must never block the operator's
   work, so failure is reported and execution continues. The same rule that
   keeps a hook safe keeps its failure quiet.
2. **The tested path is the ergonomic one.** Humans and tests both run the
   plain command; only the harness runs the variant with the flag, the
   timeout, and the redirected output.
3. **Success is indistinguishable from the failure.** Exit 0 and plausible
   output are produced either way. Only a *consequence* — a blocked commit,
   a missing orientation — reveals it, and consequences appear in live work,
   not in suites.

## The rule

**A harness-bound path earns its own execution test, asserting the
side effect the contract depends on — not merely that the command ran.**

For the gate that means: assert the attestation exists *and* that the clone
clears the gate afterwards. For a budgeted lifecycle: assert the step
completes inside its budget at realistic corpus scale, not that it returns.
The question to ask of any harness integration is not "does it run?" but
"what does the operator's contract depend on it having *done*, and is that
asserted?"

## The wider claim this refines

`portability-claims-need-execution-tests` established that availability is
measured per environment. This adds: **availability is not sufficiency.** A
path can be present, execute, and exit 0 while failing to perform the act
the contract rests on — so an execution test that only proves the command
ran is measuring the weaker fact.
