---
id: framework-root-tracks-both-adapters
type: decision
status: made
created: 2026-08-13
session: 2026-08-13
decided_by: human
confidence: high
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Settles the Phase 5R.4 ownership question for the framework root's .codex/hooks.json. Execution stays Codex-owned: rerender through reviewed adapter-install, then track."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "Same principle at the estate level: the framework demonstrates its own rules rather than asserting them."
---

# The framework root tracks both harness adapters

The operator decided (2026-08-13) that the framework root's
`.codex/hooks.json` is **tracked repository state**, symmetric with the
already-tracked `.claude/settings.json`.

**Why.** The framework eats its own dog food: a repo that ships an adapter
mechanism should demonstrate it, not merely describe it. A tracked Codex
projection is evidence a cold evaluator can read; an untracked one is
invisible to everyone but the operator of one machine. The plan's own
prohibition — do not leave it untracked and undocumented — is satisfied by
tracking rather than by ignoring or deleting.

**What this decision does NOT authorise.** The bytes currently on disk are
pre-5R.1 preflight test state: `currency=stale`, `launch-currency=stale`,
`execution=untested`. They must not be committed as-is — tracking a stale
projection would dogfood a broken example, the opposite of the intent.

**Execution sequence, Codex-owned (Phase 5R.4):**

1. rerender through reviewed `adapter-install --dry-run` + explicit apply,
   after the earlier 5R gates pass;
2. commit the rerendered artifact as tracked framework state;
3. an old definition hash must invalidate any old attestation.

A plain install refuses today, correctly: the on-disk fragment diverges from
the current renderer and unknown-stale state is a refusal, not an
overwrite. The explicit refresh that can replace a *recognised* historical
form is the Phase 5R.3 deliverable. Deleting the file to dodge the refusal
would be a workaround around a gate that is doing its job, and was declined
for that reason.
