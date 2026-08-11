---
id: codex-port-challenge-2026-08-11
type: artifact
status: stable
created: 2026-08-11
origin: synthesised
tags: [harness, adapters, codex, ports, phase-2b, evidence]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: documents
    notes: "Phase 2B deliverable: official Codex constraints, accepted neutral port changes, managed-shell findings, and the later live-test checklist."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "The in-memory shape probe earns designed-for only; verified-on remains reserved for Phase 6 lifecycle execution."
---

# Codex Port Challenge — Phase 2B (2026-08-11)

The Codex-owned challenge of the Phase 2A draft. It used the official Codex
lifecycle shape and this managed shell without installing an adapter or
creating project `.codex/` state. The result is an accepted inward port
contract plus shared-runtime work returned to Claude's owned slice.

## External contract checked

Documentation evidence date: **2026-08-11**. The pages expose no stable page
revision date, so this is the retrieval and verification date, not a claimed
publication date.

- [Codex hooks](https://learn.chatgpt.com/docs/hooks) — project hook locations,
  concurrency, trust review, JSON shape, Windows command override, working
  directory, matchers, output limits, and event input/output behaviour.
- [Codex AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
  — root-to-working-directory instruction discovery remains the portable
  entry path; hooks harden that path but do not replace it.

The second-vendor facts that constrain the adapter are:

1. All matching hook sources run, and multiple matching command handlers for
   one event launch concurrently. The ordered `estate-sync` → `session-start`
   policy therefore needs one Codex SessionStart handler.
2. SessionStart matches `startup`, `resume`, `clear`, and `compact`; a compact
   start runs before the next model request. Startup output is model context.
3. Command handlers support both `command` and `commandWindows`, run with the
   session working directory, and should resolve repo-local paths from the Git
   root because a session may begin in a subdirectory.
4. `additionalContextLimit` bounds model-visible startup context. The default
   timeout for most hooks is too broad for this advisory work, so the adapter
   must set a positive bounded timeout.
5. PostToolUse can match `Edit|Write` for `apply_patch`. Plain stdout is ignored
   for PostToolUse, so the adapter must translate quiet validation into the
   documented JSON feedback channel. Tool-hook coverage has exceptions, so
   this remains advisory and the Git hook remains the floor.
6. A project may contain `hooks.json`, inline `config.toml` hooks, or both; both
   sources are loaded and the dual-source case warns. Inspection must report
   multiple fragments and ambiguity rather than flattening them.
7. Project config trust and exact non-managed hook-definition review are
   separate human gates. The documented `/hooks` flow is observable to the
   operator, but the docs provide no stable project API from which this
   framework may infer either state. A future probe reports `unknown` where it
   cannot obtain a stable machine-readable fact.

## Accepted port constraints

The Phase 2A separation survives: render, read-only inspect, later probe, and
later install/merge remain different responsibilities. Six corrections were
required before Claude extraction:

1. Lifecycle policy now owns immutable ordered steps, argument vectors,
   context-versus-feedback delivery, and the non-enforcing failure policy.
   `LIFECYCLE_INTENTS` remains as the Phase 0-compatible derived view.
2. The render context contains only a framework path relative to the domain
   Git root and immutable bindings. It carries no host platform or absolute
   domain path; an adapter emits every supported target command variant.
3. Render is explicitly pure and reusable to derive desired bytes for
   currency comparison. Existing files still go only through inspect or the
   later merge service.
4. Inspection receives the same context used by rendering. Currency is not
   permitted to rest on a second hand-maintained expected command list.
5. Artifact presence, managed-fragment presence, readability, structural
   validity, currency, extensions, and cross-fragment findings are separately
   representable. Expected unreadable/malformed/schema-invalid config returns
   a report rather than raising.
6. Lifecycle capabilities name inward moments only. Deliberate shortcuts are
   a separate projection and cannot be claimed by a renderer that did not emit
   them; free-text notes never determine diagnostic status.

The retained in-memory probe proves that these ports can express one Codex
SessionStart handler, both command variants, Git-root resolution, bounded
context, the supported PostToolUse alias, feedback delivery, and two active
project config sources. It creates no files and is not a shipped adapter.

## Constraints handed to Phase 2C

Claude extraction must preserve these challenge results in production tests:

- Inspector currency comes from the adapter renderer. Formatting-only changes
  remain semantically current; a wrong framework path, matcher, argument,
  ordering, or managed field is stale; extra sibling hook groups are reported
  as extensions. No `_EXPECTED` command duplicate survives extraction.
- Malformed JSON, wrong-schema JSON, unreadable config, permissions-only
  config, composite config, and locally extended startup all return read-only
  reports without normalising source bytes.
- The final architecture fitness test covers every declared neutral lifecycle,
  scaffold, diagnostic, and runtime module. It forbids importing vendor
  adapters and confines vendor config paths, environment variables,
  permissions, and event schemas to vendor packages/tests/docs. The Phase 2A
  one-file string scan is evidence scaffolding, not that final gate.
- The scaffold default and every Claude artifact remain byte-identical. The
  strengthened baseline checks compare settings as bytes and the completion
  guidance as an exact line rather than normalised whitespace.

## Managed-shell findings returned to the shared slice

Phase 1 does **not** pass Codex acceptance yet:

- The emitted POSIX hook derives the framework root using external `dirname`.
  `dirname` is absent from this managed Git-hook PATH, so a directly opened
  domain without its own usable environment cannot reach the framework venv.
- The PowerShell launcher executes the first repository `.venv` and the
  `py -3` fallback without first proving PyYAML loads, so its policy is not
  equivalent to the emitted POSIX resolver.
- `runtime-probe` records interpreter-found and dependency-loaded, but not the
  required command-executed fact. Importing PyYAML alone cannot prove that the
  selected interpreter can execute the floor command.
- The existing tests mostly inspect resolver text or allow a PATH interpreter
  to mask framework-venv selection. The directly opened no-domain-venv case
  must execute a real emitted hook in the managed shell.
- `mdllm coherence` reports the Phase 1 CLI cascade still open:
  `docs/framework-map.md` says 26 mechanical subcommands while the parser now
  exposes 27 after `runtime-probe`. Reconcile that public map with the repaired
  Phase 1 command before final handoff acceptance.

These are shared runtime defects. They are returned to Phase 1 and must not be
worked around in the Codex adapter.

The Phase 0 estate record also needed a factual correction: the live snapshot
has 11/13 standard `.claude/settings.json` files, one
`.claude/settings.local.json`, and one absence. Across both filenames the
shapes are hooks-only ×8, permissions-only ×2, permissions-plus-hooks ×1,
extended startup ×1, and absent ×1.

## Live Codex checklist reserved for Phase 6

Static tests earn **designed-for**, not **verified-on**. Record exact Codex
surface/version, platform, date, project layer, and hook hash for each run.

1. Trust the project `.codex/` layer through the documented human flow, then
   review the exact command hooks through `/hooks`.
2. From the framework root, observe startup, resume, clear, and compact each
   run one handler whose visible order is estate-sync then session-start.
3. Confirm compact injection reaches the immediate continuation before its
   next model request and stays within the configured context limit.
4. Start from a repository subdirectory and confirm both POSIX and Windows
   projections resolve the Git root rather than the session cwd.
5. Apply a file edit and confirm PostToolUse returns quiet validation as JSON
   feedback without claiming enforcement or undoing the edit.
6. Commit through the Git floor using the same resolved runtime.
7. Open a nested domain directly as its own workspace and repeat steps 1–6.
8. Change the hook definition and confirm Codex requires review of the new
   hash; where trust/review cannot be read mechanically, doctor stays
   `unknown` and names the operator flow.
9. Delete `.codex/` and confirm AGENTS.md interpretation plus the Git floor
   remain complete.

## Evidence boundary

Passing Phase 2B means the neutral port can express the documented second
vendor without importing either vendor schema. It does not accept Phase 1,
complete Claude extraction, install a Codex adapter, or authorise Phases 3–5.
