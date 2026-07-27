---
id: phase-3-run-domain-task-reverted
type: decision
status: made
created: 2026-06-27
session: 2026-06-27
decided_by: both
confidence: high
informed_by:
  - id: mcp-domain-server-design
    commit: fcd1c11
  - id: cross-domain-handoff-is-verified-external-input
    commit: 2d4f6d4
linked_things:
  - id: mcp-domain-server-design
    relation: informs
    notes: "Phase 3 re-marked from 'landed' to 'reverted, deferred'; design kept as archival reasoning"
  - id: cross-domain-handoff-is-built-inbound-only
    relation: supports
    notes: "The read-only membrane is the property being protected"
  - id: cross-domain-handoff-is-verified-external-input
    relation: supports
    notes: "Quarantine defends the content path — not a live-agent invocation"
---

# Decision: Phase 3 (`run_domain_task`) Built, Then Reverted In Full

## Context

The cross-domain MCP arc shipped a read-only face (Phase 1) and a
re-quarantine-on-drift freshness check (Phase 2), both proven live on the real
jmtm-software ↔ code-architect consumer pair. Phase 3 then went further: a
live-agent hand-off, `run_domain_task`, exposed behind an opt-in `--tasks` flag.

- **Phase 3a** (`1448982`) — async stub executor; `tools/call` returns a task
  handle, the caller polls.
- **Phase 3b** (`669b82a`) — the real executor: spawns `claude -p` (headless,
  read-and-emit) in the producer domain on a background thread.
- **`addb1c4`** — `get_task_result` poll tool. **`8151343`** — `wait: true`
  synchronous mode.

All of it was tested only against a fake `claude -p`. **The live agent path never
ran once.**

## The Decision

Remove Phase 3 in full from `mdllm.py` — the `--tasks` flag, the `run_domain_task`
and `get_task_result` tools, the executor (`_mcp_run_agent` / `_mcp_agent_*`), the
session task store, and the `tasks/get` method — and its tests. The MCP design
draft keeps the Phase 3 reasoning as **archival** (clearly marked deferred/reverted),
not as a description of shipped code. The capability is parked toward a future,
**separate** agent-to-agent (A2A) peer layer.

## Why

1. **Different risk class, wrong trust model.** A live-agent invocation is not the
   read face. The membrane that makes the read face trustworthy — only typed
   results and curated resources cross, the producer's reasoning never reaches the
   consumer — is an *information-flow* property. `run_domain_task` does not breach
   that flow (the producer's agent edits its own files; the consumer applies the
   returned deliverable). What it adds is a different class of exposure entirely:
   resource exhaustion, agent-injection via task inputs, an unbounded compute
   surface. The framework's content trust model — `origin: external`,
   `verified: false` quarantine — was built for the *content* path and genuinely
   defends it. It says nothing about a live agent invocation. Phase 3 smuggled a new
   risk class in under a banner ("data, never instructions") that does not cover it.

2. **Dormant code is still surface — and that's the honour-system failure.** Behind
   an opt-in flag, the execution path still exists in the tool; "we agree not to
   call it" is an honour-system control. This framework's founding correction was
   exactly that move: replace honour-system validation with a mechanical floor that
   holds when the agent forgets. *Removing* the code is the mechanical guarantee —
   the surface cannot be reached at all. A freeze is not; removal is.

3. **Built ahead of felt need.** Phases 1–2 were felt-validated on one real consumer
   pair. Phase 3 was built for the *same single* pair, with no second consumer and
   no live run. By the framework's own "deploy when felt" razor, this is the clearest
   instance of spec/code generation outrunning evidence in the whole arc.

## Consequences

- `mdllm mcp-serve` is read-only again: `query_things` + `get_deliverable` +
  resources. 96 tests pass (the 5 Phase 3 tests removed).
- The live-agent hand-off is **deferred to a later A2A peer layer** with its own
  threat model — not bolted onto the read face. Re-open only when (a) a second real
  consumer pair exists, and (b) it earns its own project with that threat model.
- The design reasoning is not lost: it lives in `mcp-domain-server.md` (archival
  section) and in the inbound-only / verified-external-input insights, which remain
  the live record of the cross-domain thinking.

## Reversibility

Fully reversible — the build is in git history (`1448982`, `669b82a`, `addb1c4`,
`8151343`). This decision deliberately removes it from the working tree so the
surface is absent by default, not so the work is forgotten.
