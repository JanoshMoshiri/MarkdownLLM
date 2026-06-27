---
id: boundary-respect-was-interpretation-not-enforcement
type: insight
status: active
version: 1.0
created: 2026-06-26
session: 2026-06-26
source: both
confidence: high
origin: synthesised
tags: [claims-integrity, enforcement, interpretation, evals, cross-domain]
linked_things:
  - id: hook-enforcement-has-three-anchors
    relation: supports
  - id: first-2x2-measured-convention-following-not-reasoning
    relation: supports
  - id: live-agent-handoff-is-for-new-output-not-known-implementation
    relation: complements
  - id: phase-3-run-domain-task-reverted
    relation: supports
    notes: "This insight's honour-system observation (boundary respect was interpretation, not enforced) is part of the reasoning that reverted run_domain_task"
  - id: llm-driven-systems-manifesto
    relation: challenges
---

# The Agent Respected The Boundary By Interpretation, Not Because The Framework Enforced It

## The Insight

When the consumer agent honoured the cross-domain ownership boundary (declining to
misroute implementation through the producer), that was **interpretation-anchored
reasoning over framework-supplied structure — not mechanical enforcement.** The
framework's contribution was *structural*: it put an explicit, verified,
in-context boundary (`provider`/`consumer`, the ownership section of the spec)
in front of the agent. The *restraint* was the agent reasoning over it. No gate
blocked the call (`hook-enforcement-has-three-anchors`: this is the
`interpretation` anchor, not `git-fs`).

Therefore **"the framework prevented X" is an overclaim.** The honest, defensible
claim is: *the framework makes boundaries explicit, verified, and present in
context, so the agent reasons over real declared structure instead of guessing.*
That is the framework's actual thesis, and it is measurable — but it is not
mechanical enforcement.

## Why It Matters

Claims integrity, before any marketing. A sharp reviewer dismantles
"we enforce boundaries" in one question; "we make boundaries legible so agents
reason over them reliably" survives — *if* backed by a measured delta. Conflating
the two is the exact trap the framework's own honesty (three anchors;
`first-2x2-measured-convention-following-not-reasoning`, which found the
framework's measurable effect was on convention-following, not raw reasoning) was
built to avoid.

**To prove the framework's causal contribution** requires the eval apparatus, not
an anecdote: a fresh session where `run_domain_task` is *available* (this run was
doubly confounded — the tool was absent *and* framework-vs-reasoning was tangled),
running the same already-designed-implementation task in two conditions —
**framework** (explicit boundary in the verified spec) vs **bare** (same task and
tools, no explicit boundary). The behavioural delta (build directly / respect
ownership vs. misroute) **is** the framework's effect. Until that is run, no
boundary-enforcement claim is substantiated.

## Context

> **Reconciled 2026-06-27.** `run_domain_task` has since been reverted in full
> ([[phase-3-run-domain-task-reverted]]). The anecdote's setting (the tool being
> available) is now historical, but the insight's lesson not only holds — it
> *informed the revert*: "boundary respect was interpretation, not enforcement" is
> the same honour-system logic that ruled against keeping dormant execution code
> behind an opt-in flag. The A/B eval named below is now a future-A2A concern.

Surfaced 2026-06-26 when the jmtm agent declined to misuse `run_domain_task`
(see [[live-agent-handoff-is-for-new-output-not-known-implementation]]). The
operator's instinct — discomfort with crediting the framework — was correct: it
read as the framework working, but the mechanism was interpretation. Deferred:
running the framework-vs-bare A/B that would settle it (operator chose not to eval
this session).
