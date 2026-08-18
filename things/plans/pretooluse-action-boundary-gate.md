---
id: pretooluse-action-boundary-gate
type: plan
status: paused
version: 1.0
created: 2026-06-27
priority: medium
tags: [pretooluse, hooks, security, action-boundary, irreversibility]
linked_things:
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "The judgment that an action is irreversible belongs to human + structure, not a forward prediction"
  - id: orchestration-specification
    relation: extends
  - id: hard-hooks-require-observable-agent-caused-triggers
    relation: references
  - id: a-layered-harness-is-a-co-author-not-a-substrate
    relation: references
    notes: "Bears directly on this plan's un-park decision: in a layered harness the PreToolUse anchor may itself belong to the platform layer, so the gate's enforcement story must be argued per-harness, not assumed. Standing evidence for why the commit-boundary gate (v3.28.0) was built first."
  - id: an-honest-ledger-replicates-full-compliance-does-not
    relation: references
    notes: "The re-open evidence this plan waits on: if interpretation-layer variance persists across further sessions, the next rightward move is either this gate or mechanical skill emission — the two candidates named at the sweep's close."
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: references
    notes: "The re-open evidence arrived 2026-08-18: variance persisted across two harnesses in one day. The queued fork (this gate vs mechanical skill emission) is live; the evidence favours emission first. Un-parking stays the operator's call."
---

# PreToolUse Action-Boundary Gate

The deliberately-deferred security/risk-reasoning hook — the **action-side analogue
of the pre-commit gate**. The pre-commit hook gates the *state* boundary (validation
before a commit becomes real); this gates the *action* boundary: a clearance check
before an irreversible delete / send / spend. The foundation already leaves
PreToolUse free for exactly this, and the design groundwork is laid (the
"defer the irreversible" standing-truth block + the action/state-boundary asymmetry).

Migrated from continuity on its retirement (`dissolve-continuity-into-reconciliation`).
It was the operator's chosen focus, then **parked** ("probably only needed for
specific domains; things run fine without it") — a per-domain hardening affordance,
not a floor gap. Hence `paused`, not `not-started`.

**To scope when resumed:**
- What it inspects (Bash / action calls).
- What it **blocks** outright vs. **asks** on (the clearance prompt).
- Where the mechanical-vs-interpretation line falls — `consequence-is-recoverable-only-in-retrospect`
  says the irreversibility judgment is human + structure, not a forward prediction,
  so this is likely `interpretation`-anchored with a narrow `git-fs`/mechanical core.
