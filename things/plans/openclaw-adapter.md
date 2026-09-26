---
id: openclaw-adapter
type: plan
status: in-progress
version: 1.0
created: 2026-09-24
priority: high
tags: [openclaw, adapter, plugin, lifecycle, sessions, public-release]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: extends
    notes: "Uses the neutral lifecycle ports, bounded runner and evidence discipline."
  - id: orchestration-specification
    relation: implements
    notes: "Binds OpenClaw lifecycle moments without promoting hooks to enforcement."
  - id: framework-discovery-specification
    relation: extends
    notes: "Maps one designated OpenClaw agent workspace to one domain."
  - id: standing-watch-specification
    relation: implements
    notes: "Binds watch exit to an exact OpenClaw session."
  - id: openclaw-adapter-seam-analysis-2026-09-24
    relation: references
    notes: "Pins the OpenClaw 2026.9.3 seam evidence."
---

# OpenClaw Adapter

## Purpose

Build and release a reusable public OpenClaw adapter for MarkdownLLM. A
designated OpenClaw agent must enter, continue and wake as the correct
MarkdownLLM domain agent while each product keeps its authority:

- OpenClaw owns its agent loop, agent identity, ordinary sessions,
  conversation history and runtime resumption.
- MarkdownLLM owns domain discovery, lifecycle intent, durable domain state,
  validation, workflow state and standing-watch semantics.
- The adapter translates at those boundaries. It is not a scheduler, business
  state store, executor replacement or BookRite integration.

Adapter acceptance is fixture-based and independent. BookRite begins only
after this plan's acceptance gate passes and supplies no adapter evidence.

## Settled architecture

1. **One OpenClaw agent maps to one MarkdownLLM domain.** The configured
   OpenClaw workspace is the domain entry. The adapter verifies discovery
   rather than accepting a prompt path as identity.
2. **A native non-channel plugin owns lifecycle translation.** It observes
   typed hooks, invokes the neutral MarkdownLLM lifecycle runner, and adds
   bounded output through before_prompt_build.
3. **Session identity stays native.** OpenClaw's agentId and sessionKey remain
   the runtime identifiers. A plugin-owned runtime gate records only the
   lifecycle fingerprint satisfied for that process generation. Restart,
   reset and compaction invalidate or recreate that bounded state.
4. **The existing runner owns order.** estate-sync then session-start remains
   one neutral lifecycle intent. The plugin does not duplicate the order or
   invent a second prompt source.
5. **The Git floor remains enforcement.** Plugin feedback is bounded and
   advisory. Pre-commit validation remains the hard write boundary.
6. **mdllm watch remains the doorbell.** A thin bridge translates exit 0 into
   an exact OpenClaw agent/session invocation and restarts the watch after the
   turn. It never reads or advances workflow state itself.
7. **The package is version-bounded.** OpenClaw Plugin SDK APIs are
   experimental; claims name exact tested host versions.

8. **Domain selection precedes domain startup.** An owner-visible command
   resolves a registered domain to its dedicated agent and workspace, verifies
   that workspace's `AGENTS.md`, and reuses or creates a separately routed
   Telegram topic. It never changes the current agent's working directory or
   rebinds the current conversation.

## Adapter contract

| ID | Requirement | Acceptance evidence |
|---|---|---|
| OCA-01 | Bind a configured OpenClaw workspace to exactly one discoverable MarkdownLLM domain; refuse absent, ambiguous or mismatched roots. | Valid root, nested entry, missing sentinel, mismatch and two-agent isolation tests. |
| OCA-02 | Invoke the framework-owned session-start lifecycle intent in declared order through shared launch policy. | Spy-runner tests prove estate-sync precedes session-start and no vendor order enters neutral services. |
| OCA-03 | Satisfy startup once per logical session generation and re-evaluate on reset, compaction, plugin restart or changed contract fingerprint. | State-transition tests cover duplicate suppression and recovery. |
| OCA-04 | Deliver bounded, integrity-marked context additively and preserve deferred-read obligations when the full kernel does not fit. | Hook tests prove bounds, section retention, integrity facts and no system-prompt replacement. |
| OCA-05 | Preserve OpenClaw session ownership and keep only bounded plugin-owned lifecycle state; never edit OpenClaw session or transcript storage directly. | State-machine tests prove once-per-generation behavior, invalidation and canonical session reuse. |
| OCA-06 | Surface lifecycle failures honestly, keep advisory failures distinct from enforcement and retain definition-hash-bound evidence. | Matrix covers timeout, missing runtime, stale framework, malformed output and attestation. |
| OCA-07 | Bind mdllm watch outcomes to the exact agent/session, honour exit codes 0/1/2/3 and never duplicate state or advancement. | Two-role loop tests cover wake, quiet/blind polls, refusals, duplicate watch and unpublished-turn recovery. |
| OCA-08 | Isolate domains, agents, sessions and plugin state so concurrent loops cannot cross-load or cross-wake. | Multi-domain concurrency tests use distinct fixtures and session keys. |
| OCA-09 | Install publicly without private paths, repositories or trusted-only APIs; publish bounded compatibility. | Clean-profile install, manifest, package-content and host-version CI checks. |
| OCA-10 | Prove the adapter with public fixtures and supported commands only. | Acceptance evidence has no BookRite or private-estate prerequisite. |
| OCA-11 | Make the active MarkdownLLM domain visible and selectable before startup without cross-domain workspace or session mutation. | Owner-gated status/list/open command tests prove explicit topic-to-agent routing, target `AGENTS.md` admission, existing-topic reuse, persistence and rollback. |

## Delivery sequence

### Phase 0 - seam and contract

- [x] Inspect MarkdownLLM lifecycle, adapter, session-contract and watch
  boundaries at 8d3a635f49dfb5a58e3b44ebe4facd50e7e36c5a.
- [x] Inspect supported OpenClaw plugin, session, context, state and wake
  surfaces at 2026.9.3 (1391f7c).
- [x] Select the native-plugin seam and record explicit non-seams.
- [x] Define requirement IDs OCA-01 through OCA-11.

### Phase 1 - executable contract

- [x] Add a minimal public fixture domain with deterministic discovery and
  lifecycle output.
- [x] Add failing acceptance tests for binding, ordered startup, idempotence,
  context projection, failure behaviour and isolation.
- [x] Freeze plugin manifest, configuration and package goldens.

### Phase 2 - thin lifecycle slice

- [x] Register openclaw in the MarkdownLLM adapter registry without adding
  vendor conditionals to neutral lifecycle services.
- [x] Implement the public plugin entry, strict manifest and typed config.
- [x] Project the existing session-start result through additive
  before_prompt_build context.
- [x] Keep lifecycle state bounded and plugin-owned; add a projected session
  extension only when a public writable SDK route can support it.
- [x] Add owner-gated `/domain`, `/domain list` and `/domain open`
  commands that establish a dedicated Telegram topic route before the target
  domain's lifecycle context loads.

### Phase 3 - wake and recovery slice

- [x] Implement the external bridge around mdllm watch --exit-on-wake.
- [x] Target exact agentId and sessionKey through supported CLI or Gateway
  session surfaces.
- [x] Exercise watch exit codes 0/1/2/3 without advancing workflow state.
- [x] Exercise unpublished/diverged local-turn recovery end to end without
  resolving Git in the adapter.

### Phase 4 - deterministic acceptance

- [ ] Pass OCA-01 through OCA-11 on Windows and POSIX-supported paths.
- [x] Add fitness tests forbidding private imports, direct session-store
  mutation and duplicate lifecycle ownership.
- [x] Produce a requirement-to-test evidence matrix.

### Phase 5 - live compatibility

- [x] Install into a disposable clean OpenClaw 2026.9.3 profile on Windows.
- [x] Prove fresh and continued sessions, reset/compaction recovery and
  Gateway/plugin restart against Windows OpenClaw 2026.9.3.
- [ ] Prove live two-domain isolation and exact-session wake.
- [ ] Prove `/domain open` through a live Telegram forum and confirm the
  first target-topic message starts the selected domain.
- [x] Record exact version, platform, commands, observations and exclusions.
  Static tests earn designed-for; live runs earn verified-on.

#### Live lifecycle evidence - 2026-09-25

The Windows proof ran against OpenClaw 2026.9.3 (1391f7c) on Node.js
24.21.0 in the disposable adapter profile. The package suite passed 29/29,
and `npm pack --ignore-scripts --json` contained the 18 intended files.
The installed managed-generation `dist/index.js` SHA-256 matched the built
artifact.

Captured model requests carried the MarkdownLLM session-start marker in the
sequence `true, false, true, false, false, true, true`: fresh, continued,
post-reset, two compaction-preparation turns, post-compaction and post-Gateway
restart. OpenClaw compacted the exact session to two lines before the
post-compaction turn.

The supported Windows archive-update path remains excluded from this proof:
OpenClaw hit `EPERM` creating its host `openclaw` peer symlink. The lifecycle
proof used the same tarball in the existing disposable managed npm generation
and verified byte identity. `npm run test:install` built successfully but did
not complete within the external 300-second cap on this host. OCA-09 therefore
remains open for a supported clean-profile Windows install without that
fallback.

#### Domain-routing increment - 2026-09-27

Commit `96da9d7` adds the explicit domain registry and owner-gated
`/domain`, `/domain list` and `/domain open` flow. The package suite
passed 31/31 and its dry-run tarball contained the 21 intended public files.
Tests cover current-route status, unbound refusal, target-agent and
`AGENTS.md` admission, existing-topic reuse, topic creation, config
persistence and rollback.

The current domain-routing build has not yet passed the managed Windows
clean-profile smoke. The external run timed out after 240 seconds while npm
was still resolving the OpenClaw peer dependency tree; no plugin-load result
was produced. No process remained and the exact disposable profile was
removed. No live Telegram topic was created, so OCA-11 remains deterministic
only.

### Phase 6 - public release gate

- [x] Document install, config, trust, security, compatibility, troubleshooting
  and removal.
- [x] Add CI, package-content checks, licence and contribution guidance.
- [ ] Version and changelog the accepted contract.
- [ ] Request the operator's deliberate release/publish authorization. Root
  autopush false remains controlling.

## Acceptance gate

The adapter is accepted only when every OCA requirement has deterministic
evidence, each claimed host/platform has a clean-profile live run, no
unsupported or trusted-only seam is required, removal leaves the domain and
Git floor whole, the package contains no private path or BookRite data, and
compatibility wording names only versions actually tested.

Only then may the agentic business operating model begin BookRite.

## Exposure

**Not yet.** Another domain should not rest on this evolving implementation
plan. Expose the stable contract and installation guide after acceptance, when
their public semantics have execution evidence.

## Immediate next move

Close the remaining Phase 5 evidence: pass the supported Windows clean-profile
installer without a symlink fallback, prove `/domain open` in a disposable
Telegram forum, then prove live two-domain isolation and exact-session wake.
Observe the configured Windows and Ubuntu CI matrix, reconcile any defects,
and update the matrix before requesting publication authority.
