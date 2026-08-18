---
id: live-eval-scope-bounded-to-claude
type: decision
status: made
created: 2026-08-18
session: 2026-08-18
decided_by: human
confidence: high
informed_by:
  - id: vendor-harness-adapter-foundation
    commit: c199002
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Discharges the completion criterion that had no checkbox: the compatibility claim is bounded rather than the live runner made multi-vendor. Phase 8 can close against this decision."
  - id: evidence-and-eval-backlog
    relation: informs
    notes: "Scopes the eval programme: the live-runner surface stays Claude-harness/Claude-model by declaration, and any expansion arrives as its own explicit decision with its own eval set."
---

# Live eval scope is bounded to the Claude harness — expansion is its own decision

The operator resolved the last unchecked completion criterion of
`vendor-harness-adapter-foundation` (2026-08-18): **bound the claim, do not
widen the tool.**

## The decision

The framework's vendor-neutrality claim covers the **substrate lifecycle**
(AGENTS.md interpretation, the Git floor, the lifecycle adapters) and the
**deterministic eval path** (`mdllm eval` checking fixture assertions against
domain state). It does not cover the live-runner backend, and stops claiming
otherwise implicitly: `mdllm eval --run` shells the Claude CLI, and today's
evals are **deliberately focused on the Claude harness and Claude models** —
that is their design scope, not a portability gap awaiting repair.

## The expansion boundary, stated as the operator framed it

When evals should cover another harness or model family (the Codex harness,
GPT models), that happens **on an explicit decision, made for its own sake**
— never as a side effect of expanding the substrate or the harness-adapter
capabilities. At that point:

- a **new set of evals and structures** is written for the added surface,
  because results across harnesses are only comparable by design, not by
  accident;
- refactoring extracts **reusable parts** where they genuinely exist,
  following the same clean-architecture and SOLID boundaries the adapter
  foundation used — ports inward, vendor edges outward;
- the decision gets its own record, superseding this one's boundary.

## What this discharges

The plan's completion criterion — *"live eval portability is either
implemented or routed to its own owned plan before any claim expands from
lifecycle portability to 'all tooling'"* — is discharged by bounding: no
claim expands. Public surfaces describing evals state the deterministic
path as the vendor-neutral capability and the live runner as
Claude-scoped by design. No new plan is opened; deploy-when-felt applies,
and the felt signal will be someone actually needing another backend.
