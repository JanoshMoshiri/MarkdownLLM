---
id: openclaw-adapter-seam-analysis-2026-09-24
type: artifact
status: stable
created: 2026-09-24
origin: synthesised
confidence: high
tags: [openclaw, adapter, plugin, lifecycle, session, wake, evidence]
linked_things:
  - id: openclaw-adapter
    relation: documents
    notes: "Phase 0 evidence for the selected integration seam."
  - id: vendor-harness-adapter-foundation
    relation: extends
    notes: "Applies the existing ports-and-adapters boundary to OpenClaw."
  - id: standing-watch-specification
    relation: references
    notes: "The watch exit remains the framework-owned wake contract."
---

# OpenClaw Adapter Seam Analysis - 2026-09-24

## Snapshot boundary

This is a point-in-time source and documentation inspection, not a future-host
compatibility claim.

- OpenClaw: 2026.9.3 (1391f7c)
- MarkdownLLM read base: 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a
- OpenClaw Plugin SDK status: experimental
- Inspection target: installed public documentation, exported Plugin SDK
  declarations and maintained bundled extensions

Package-relative source references are used deliberately. No private machine
path is part of the adapter contract.

## Verdict

**VALIDATED, with a version boundary.** The narrowest supported seam is a
version-pinned, ordinary non-channel OpenClaw plugin. It projects
MarkdownLLM's logical lifecycle into OpenClaw's existing agent loop; it does
not replace the executor or create a second session runtime.

OpenClaw remains authoritative for agent identity, ordinary session creation,
conversation history, reconnection and resumption. MarkdownLLM remains
authoritative for domain discovery, lifecycle intent, Git state, validation,
workflow state and standing-watch semantics.

## Supported surfaces

| Need | OpenClaw surface | Consequence |
|---|---|---|
| Plugin entry | definePluginEntry and OpenClawPluginApi | Ship a normal external plugin with strict manifest and bounded compatibility. |
| Turn context | before_prompt_build additive context | Deliver existing MarkdownLLM output without replacing the whole system prompt. |
| Policy-aware context | before_prompt_build with requiresToolAuthority | Retrieve after final tool policy where needed; remain additive. |
| Lifecycle observation | session_start, session_end, before_reset, after_compaction, gateway_start, gateway_stop, agent_end | Detect lifecycle moments without treating observation hooks as mutation. |
| Compact session metadata | api.session.state.registerSessionExtension | Store JSON-compatible binding and contract-fingerprint state. |
| Larger adapter state | plugin-owned keyed, blob or SQLite storage | Keep larger records out of OpenClaw's session projection. |
| Session create/resume | Gateway sessions APIs and canonical sessionKey | Do not create ordinary sessions through low-level runtime helpers. |
| Event continuation | documented system-event and heartbeat APIs | Request attention without treating a heartbeat as a logical session boundary. |
| External exact-session invocation | supported OpenClaw agent CLI and Gateway APIs | Wake the designated session without a second scheduler. |

before_prompt_build is the portable target seam. agent_turn_prepare and
durable next-turn injection are not sufficient alone because their current
prompt-path coverage excludes Codex and Copilot.

## Explicit non-seams

The adapter will not depend on:

- an Agent Harness unless a later requirement replaces OpenClaw's executor;
- low-level createSessionEntry for ordinary sessions;
- direct edits to OpenClaw SQLite, transcripts or legacy session JSON;
- hashed dist imports, repository src imports, bundled-only helpers or
  deprecated broad SDK barrels;
- HOOK.md automation as the primary typed integration contract;
- trusted-only api.runtime.gateway.request composition;
- scheduled session turns available only to bundled plugins;
- heartbeat, cron or automation as logical MarkdownLLM session boundaries;
- whole-system-prompt replacement where additive context is sufficient.

## Maintained structural references

- dist/extensions/workboard demonstrates services, lifecycle hooks,
  plugin-owned state and optional tools. Its trusted-only gateway request is
  not a public-plugin seam.
- dist/extensions/active-memory demonstrates policy-aware additive context and
  agent_end cleanup.
- docs/plugins/hooks.md, docs/plugins/building-plugins.md,
  docs/plugins/sdk-overview.md, docs/plugins/sdk-runtime/agent.md,
  docs/plugins/sdk-runtime/state-and-system.md and docs/plugins/sdk-testing.md
  define the inspected public boundary.

## Packaging consequences

A public release needs a built-JavaScript extension entry, OpenClaw peer
dependency, plugin API compatibility floor, root openclaw.plugin.json, strict
configSchema, manifest declarations, focused Plugin SDK imports, a tested host
range and a retest policy. Experimental APIs prohibit an unbounded
forward-compatibility claim.

## Evidence limit

This artifact proves that the selected seam exists in the named build and that
the rejected alternatives are unnecessary or unsupported. It does not prove
live adapter compatibility. Fixture acceptance and a live disposable
OpenClaw profile must earn that claim for every named host version.
