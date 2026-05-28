---
id: hook-compliance-correlates-with-scope-not-awareness
type: insight
status: active
version: 1.0
created: 2026-05-28
confidence: medium
origin: both
source: session — holistic framework review
session: 2026-05-28
tags: [hooks, compliance, context-pressure, agent-behaviour]
linked_things:
  - id: orchestration-specification
    relation: informs
  - id: tiered-loading-is-tiered-reading-applied-to-specs
    relation: supports
---

# Hook Compliance Correlates With Scope, Not Awareness

## The Insight

Domain agents follow hard hooks consistently. The framework agent drifts — missing `post-write:commit` in this session being the observed instance. The difference isn't awareness (both agents have the hooks in their AGENTS.md) — it's context pressure. Domain agents have tight scope: one domain, focused skills, limited thing types. The framework agent juggles 15+ specs, meta-reasoning about its own structure, and broad session intent.

This means the fix for missed hooks is **reducing cognitive load** (tiered loading, focused sessions), not adding more metacognitive instructions or self-monitoring rules. We considered adding a verbal-trigger self-check ("if you say 'noted', check whether a hook should fire") and decided against it — the agent already knows the hooks exist, it just has too much competing for attention.

## Why It Matters

Informs future decisions about "should we add another rule to AGENTS.md to fix compliance?" The answer is likely no if the agent already knows the rule. The lever is scope management, not rule proliferation. This also validates that tiered loading (the 75% context reduction for Q&A sessions) was the right architectural move — it directly addresses the root cause.

## Context

Observed during 28 May session: `post-write:commit` was not fired after modifying REVIEWLOG.md and an insight file. The agent verbally acknowledged the miss ("noted for this session") without recording it — itself an instance of the pattern. Domain agent (InnoTriage) does not exhibit this drift in its test runs.
