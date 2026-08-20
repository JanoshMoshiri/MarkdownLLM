---
id: hook-enforcement-has-three-anchors
type: insight
status: promoted
version: 1.3
created: 2026-06-19
session: 2026-06-19
source: both
confidence: high
origin: synthesised
promoted_to: orchestration-specification
linked_things:
  - id: orchestration-specification
    relation: informs
    notes: "Distils the 'Enforcement: Three Anchors, Not Two' section into a standing design test"
  - id: agents-md-discovery-is-harness-dependent
    relation: supports
    notes: "Names the interpretation anchor whose portability that insight already proved harness-dependent"
  - id: portability-claims-need-execution-tests
    relation: supports
---

# Every Hook Anchors To One Of Three Surfaces — The Anchor Decides Portability

## The Insight

The hard/soft hook distinction is about *configuration* (always-on vs opt-in).
Orthogonal to it, and more decisive for portability, is what actually makes a
hook fire. Every hook anchors to exactly one of three surfaces:

1. **Agent interpretation** — the agent reads the entry file and acts on the
   prose. This is the portable contract fallback and the default, but it is
   probabilistic: availability of prose is not evidence of receipt, reading,
   application, or outcome correctness. The neutral contract is the portability
   layer; each harness still earns its lifecycle claims through evidence.
2. **Git / filesystem** — a real mechanism fires (the `pre-commit` hook, a file
   write). Mechanical, enforced, and universal because git is present under
   every harness.
3. **Harness session lifecycle** — the harness decides a "session" started or
   ended. Enforced only if a per-harness adapter binds it; differs per harness.

Hardening is optional and is the same move twice: the git pre-commit hook hardens
validation with no adapter; optional `adapters/` entries harden session-lifecycle
hooks. **Adapters must stay optional — the moment one becomes *required*, the
framework stops being a harness-agnostic substrate and becomes a harness-specific
tool.**

## Why It Matters

- **It retires the recurring "is this just a harness?" worry.** A harness is a
  runtime that owns no durable state; MarkdownLLM is durable state + rules that
  any runtime operates over. The overlap that *feels* harness-like is exactly the
  orchestration band — and the three-anchor test is how you keep that band from
  drifting into re-implementing harness primitives it should delegate.
- **It is the test for adding any new hook:** which surface does it key off? If
  the answer is "harness session lifecycle," it needs an adapter to be enforced
  and otherwise falls back to interpretation — which is where the framework
  already works. Only the lowest-consequence hooks live there, so the floor stays
  correctly sized around the one unrecoverable case (`pre-commit` validation).
- **It surfaces dead weight.** A prompt that re-performs a mechanically-enforced
  (git/filesystem) check is redundant by construction — this is what flagged
  `validate-before-commit` and `worklog-update` for removal (2026-06-19).

## External Corroboration (2026-08-11)

The 2025–26 literature independently confirms the gradient this insight names
(external claims, cited in `reviews/REVIEW-external-2026-08-10.md`, unverified
until the operator confirms): instruction-following success decays roughly
exponentially with the number of instructions in context, and long-horizon
procedural execution degrades as context grows ("context rot"). Any control
anchored on "the model remembers" therefore decays by the processor's nature,
not by lapse — and the estate evidence matches: in every breached session the
interpretation-anchored controls vanished silently while every git-fs control
held. Hardening is not a preference; it is a migration direction dictated by
the processor's measured failure mode. No named equivalent of the three-anchor
taxonomy was found in the field.

## Context

Surfaced when the operator asked whether the framework was "just a harness, or
like Hermes / OpenClaw for an agent." Walking the distinction produced the
three-anchor frame, which became the `orchestration.md` "Enforcement: Three
Anchors, Not Two" section and drove a surface reduction (two prompts deleted).
The Copilot-then-Claude-Code build history demonstrates useful operation with
zero adapters. It does not prove that every instruction was received, read, or
applied; later session evidence is exactly what forced that distinction into
the promoted orchestration specification.
