---
id: code-architect-governs-substrate-code
type: decision
status: made
created: 2026-08-13
session: 2026-08-13
decided_by: human
confidence: high
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: informs
    notes: "Applies from Phase 5R.2 forward, to both agents. Not retrospective: 5R.0/5R.1 code stays as accepted, since retro-refactoring for style would invalidate green gates."
---

# Code-architect governs substrate code work

The operator directed (2026-08-13) that the `code-architect` domain's
skills and principles are read and applied for code work on the framework
substrate, starting from Phase 5R.2 of
[[vendor-harness-adapter-foundation]] and continuing thereafter — by
whichever agent holds the work.

**What this means in practice.** Before writing substrate code, the agent
reads the domain's specification skill (Clean Architecture dependency rule,
SOLID applied rather than recited, cohesion/coupling) and the accumulated
principles and anti-patterns. Where the work earns new architectural
knowledge, it is captured back into that domain as first-class things —
`interface-contracts/` and `architecture/` are currently empty, and the
adapter foundation is generating exactly the material they want.

**Not retrospective.** Phases 5R.0 and 5R.1 are accepted and green. They
already satisfy the domain's core rules — ports as protocols, dependency
direction inward, composition root at the CLI edge, interface segregation
with `isinstance` pass-through, unsupported-is-data rather than exceptions —
and re-opening them for style would trade verified behaviour for tidiness.

**Known debt, recorded rather than silently carried** (the domain's own rule
— a conscious shortcut beats an unconscious one):

- `delivery: Literal["context", "feedback"]` on the neutral port carries
  vocabulary derived from one vendor's delivery semantics;
- the adapter registry requires `Render` + `Inspect` from every entry, which
  will not fit a diagnostic-only vendor;
- `adapter_install.py` (820 lines), `calc.py` (809), `validation.py` (724)
  are past the size where single-responsibility deserves a deliberate
  answer.

**Both agents.** The operator intends to give the same domain knowledge to
the Codex agent, so the standard is shared rather than Claude-local. Reads
are unconstrained; writes into `code-architect` stay coordinated like any
other shared surface.
