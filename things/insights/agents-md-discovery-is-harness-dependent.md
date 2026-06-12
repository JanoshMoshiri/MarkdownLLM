---
id: agents-md-discovery-is-harness-dependent
type: insight
status: active
version: 1.0
created: 2026-06-11
session: 2026-06-11
source: both
confidence: high
origin: stated
linked_things:
  - id: framework-discovery-specification
    relation: challenges
    notes: "Discovery assumes the harness injects AGENTS.md; a growing class of harnesses does not"
---

# AGENTS.md Discovery — And The Floor — Are Harness-Dependent

## The Insight

The framework's two load-bearing assumptions — (1) the harness auto-discovers
AGENTS.md at session start, and (2) the git pre-commit hook can execute where
the agent commits — are properties of the *harness and environment*, not of the
framework. Both failed, observably, in the first session run from a harness the
framework had never met (Anthropic Cowork, 2026-06-11): AGENTS.md was not
injected into context (the agent bootstrapped manually because the task
required reading the corpus), and the installed pre-commit hook could not run
at all (it hardcoded one machine's absolute Windows path and a bare `python`
interpreter; the session's sandbox had neither).

## Why It Matters

- Every hard hook, tier rule, and behavioural contract exists only if AGENTS.md
  reaches the model's context. On harnesses without AGENTS.md discovery
  (Cowork today; likely other agent platforms of its class — desktop agents,
  OpenClaw/Hermes-style frameworks), the framework is inert until a human types
  a bootstrap line. The explicit bootstrap prompt ("Act as the framework agent:
  read AGENTS.md, then {framework_root}/kernel.md") should be specified in
  framework-discovery.md as a first-class discovery route, not an improvisation.
- The README's vendor table claims "Fully supported" for six tools; this
  session is the first measured data point for any harness, and it was a
  partial failure. Distinguish *designed-for* from *verified-on*.
- The floor degrades silently when its environment is missing. The hook was
  made portable in the same session (repo-relative path, runtime interpreter
  resolution, explicit failure message when python/mdllm are absent) — but
  "what happens when the floor cannot run" deserves a spec-level answer, not
  just a better error message.

## Context

Surfaced when the operator asked whether a Cowork session would "spin up from
the agent's file" like other harnesses. It does not. The same session then ran
the commit test that exposed the hook's machine-specificity, fixed it, and
recorded this insight. Evidence: reviews/REVIEW-independent-2026-06-11.md
(§Under-Engineered → "Floor availability", "Vendor-agnostic claims vs evidence").
