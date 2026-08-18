---
id: installation-is-not-activation
type: insight
status: active
version: 1.0
created: 2026-08-18
session: 2026-08-18
source: both
confidence: high
origin: stated
tags: [harness, trust, rollout, diagnostics, activation]
linked_things:
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: extends
    notes: "That insight keeps adapter installation human/tool-owned; this one names the second human boundary that remains after installation — harness-local project and exact-hook trust."
  - id: portability-claims-need-execution-tests
    relation: extends
    notes: "Configuration, launch currency, and a runnable interpreter can all be true while automatic execution remains absent."
  - id: vendor-harness-adapter-foundation
    relation: derived-from
    notes: "The estate rollout installed current Codex projections everywhere, while live domain sessions remained interpretation-only until the operator trusted each workspace."
---

# Installation Is Not Activation

The Codex adapter rollout reached a state that looked complete from the
repository: the framework root and all thirteen domains carried current
`.codex/hooks.json` projections, launch resolution was current, and the runtime
probe could execute. Yet opening an untrusted domain produced no automatic
Codex lifecycle context and no Codex attestation. The files were installed;
the hooks were not active.

Activation required a second, deliberately non-repository act: the operator
opened each domain as its own workspace and trusted its project hook layer and
exact hook definitions through the harness. The framework could explain that
boundary and report `trust=unknown`; it could not infer, grant, or safely
automate the decision. Only a later automatic event plus its contract-bearing
side effects established execution.

So a permission-bearing adapter rollout has three independent axes:

1. **Distribution** — the intended project artifact exists and is current.
2. **Activation** — the human has granted the harness-local trust needed for
   that project and definition.
3. **Execution** — a real harness event performed the side effect the contract
   depends on.

Completing one axis does not promote either of the others. A fleet can be
configuration-complete and activation-incomplete; a trusted definition can
still be execution-untested; a runtime probe can succeed without proving a
hook fired. This is why diagnostics keep configuration, currency, trust,
runtime, and execution as separate facts rather than collapsing them into an
"installed" or "working" verdict.

The practical rule follows: every rollout document needs an explicit
post-install trust walk and an automatic-event verification step. Re-rendering
or reinstalling is not a remedy for missing trust, and global mutation is not a
shortcut — the per-workspace human decision is part of the safety boundary.
