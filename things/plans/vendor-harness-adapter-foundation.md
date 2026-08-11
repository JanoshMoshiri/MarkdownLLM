---
id: vendor-harness-adapter-foundation
type: plan
status: not-started
version: 1.1
created: 2026-08-11
priority: high
tags: [harness, adapters, codex, claude-code, diagnostics, portability, clean-architecture]
linked_things:
  - id: orchestration-specification
    relation: implements
    notes: "Turns the per-harness adapter boundary into an extensible port while preserving interpretation and git-fs as the portable floor."
  - id: framework-discovery-specification
    relation: extends
    notes: "Adds execution-tested harness diagnostics without changing AGENTS.md as the domain entry point."
  - id: domain-refresh-specification
    relation: extends
    notes: "Generalises the adapter refresh/install path beyond the current Claude-only operator paste."
  - id: hook-enforcement-has-three-anchors
    relation: implements
    notes: "Keeps harness-session hardening optional and subordinate to the interpretation and git-fs anchors."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Requires a real lifecycle and commit probe before any harness is reported as verified."
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: references
    notes: "Preserves the human/tool gate around automatic powers and operator-owned configuration."
  - id: a-layered-harness-is-a-co-author-not-a-substrate
    relation: references
    notes: "Keeps the adapter thin and prevents a harness operating layer from becoming Definition Zero."
  - id: relative-path-hooks-break-in-nested-domain-repos
    relation: implements
    notes: "Makes stable root and runtime resolution a shared port rather than a per-adapter path convention."
---

# Vendor Harness Adapter Foundation

Preserve the working Claude Code path, add first-class Codex lifecycle
hardening, and create a truthful vendor diagnostic without moving any domain
semantics into a vendor layer.

This is an architecture and rollout plan. It authorises no adapter or domain
configuration changes by itself. Implementation begins only after the operator
accepts the boundary and phase order.

**Current execution boundary:** the Claude Code agent owns Phases 0–2 and must
stop at the cross-harness handoff gate. The Codex agent owns Phases 3–5 only
after accepting that handoff. No inference from phase order is permitted; the
ownership and stop conditions below are part of the plan.

## Assessment verdict

The substrate is **semantically vendor-agnostic but operationally
Claude-coupled at its outer edge**.

The good news is the important boundary already holds. `AGENTS.md`, the
kernel, domain skills, things, schemas, the `mdllm` lifecycle commands, and the
Git validation floor do not depend on Claude. A domain without any harness
adapter remains complete by interpretation plus git-fs enforcement. Codex
does not require a second substrate, a translation of domain skills into
Codex-native skills, or a fork of the domain model.

The coupling that does exist is concentrated in delivery and diagnostics:

| Surface | Coupling | Assessment |
|---|---:|---|
| Domain policy and state | Low | AGENTS/kernel/skills/things contain the operative program; no Claude API or storage dependency. |
| Orchestration contract | Low–medium | The three-anchor model is vendor-neutral, but several explanations and deployment instructions name Claude as the only realised harness adapter. |
| Git floor and lifecycle CLI | Low | Validation, `estate-sync`, and `session-start` are reusable application services. Their interpreter/runtime resolution is not yet seamless from a directly opened nested domain in the Codex managed shell. |
| Scaffold | High | `scaffold.py` constructs `.claude/settings.json` inline, unconditionally creates Claude command files, and prints Claude-specific completion guidance. There is no adapter port. |
| Doctor | High | `doctor.py` hard-codes `.claude/settings.json` and treats `SessionStart` key presence as adapter installation. It cannot report Codex, trust, command resolution, execution, or currency. |
| Refresh and operator guidance | High | The install/refresh story assumes the only permission-bearing adapter file is `.claude/settings.json`; Codex has a different project-trust and hook-review boundary. |
| Tests | Deliberately high | Tests assert the concrete Claude scaffold. These should become the non-regression fixture, not be weakened during extraction. |
| Live domain estate | Distribution coupling | In the 2026-08-11 estate snapshot, 11 of 13 domain repos contain `.claude/settings.json`; 10 contain the standard SessionStart/PostToolUse hardening; one of those deliberately extends session start with a domain-specific flag; none contain a project `.codex` layer. Existing files are estate state, not generated cache to overwrite. |

Three defects fall out of that map:

1. **The Claude adapter exists as repeated knowledge, not as a component.** Its
   lifecycle intent is restated in the example adapter, root settings,
   scaffold code, tests, docs, refresh prose, and deployed domain copies.
2. **Presence is being reported as capability.** A JSON key says nothing about
   trust, path resolution, runtime availability, execution, or whether the
   config still expresses the current lifecycle contract.
3. **Runtime resolution crosses the wrong boundary in nested domains.** Git
   hooks resolve the framework CLI through `../../tools/mdllm.py` but prefer a
   virtual environment under the domain Git root. In the current Codex shell,
   the usable environment is at the framework root. A Codex hook alone cannot
   repair the Git floor; the shared runtime port must be fixed first.

These are adapter-foundation problems, not reasons to alter the substrate or
the domains.

## Requirements and invariants

The build must satisfy all of these simultaneously:

1. **Vendor-neutral core.** Lifecycle policy names framework intents such as
   synchronise estate, orient session, and validate after a write. It never
   names a vendor event or config format.
2. **Claude remains behaviourally stable.** The first refactor produces the
   same scaffolded Claude artifacts and preserves all current tests before any
   Codex artifact is introduced.
3. **Adapters remain optional hardening.** Removing `.claude/` or `.codex/`
   must leave AGENTS.md interpretation and the Git floor intact.
4. **Existing domains are never silently migrated.** Adapter installation or
   refresh is an explicit human-invoked tool operation. No estate sweep
   rewrites operator-owned settings.
5. **Composite settings are merged, never replaced.** Permission rules,
   domain-specific hook arguments, and unrelated vendor settings survive
   byte-for-byte where they are outside the managed hook fragment. Ambiguous
   ownership produces a diff and a refusal, not a best guess.
6. **No global Codex mutation.** Framework hooks live in the project
   `.codex/` layer. User-wide `~/.codex` configuration and installed plugins
   remain outside the substrate's authority.
7. **Capability claims are evidence-scoped.** Designed, configured, trusted,
   runnable, executed, and verified are distinct facts. Doctor never promotes
   one into another.
8. **One owner for repeated facts.** Adapter capabilities and lifecycle
   projections are emitted and inspected by the same adapter component. Do
   not add a hand-maintained manifest that can drift from its renderer.
9. **Thin adapters.** Harness-specific code translates events and config only.
   It contains no domain reasoning, thing schema, session-memory policy, or
   alternate validation logic.
10. **No premature command/skill emulation.** Portable reasoning prompts stay
    in `prompts/` and domain skills stay in `skills/`. Vendor-native shortcuts
    are separate optional projections only where the harness has a proven
    equivalent.

## Target architecture

Dependencies point inward:

```text
Claude adapter     Codex adapter     runtime / Git implementation
       \                |                 /
        implements narrow harness and runtime ports
                         ↓
             lifecycle application service
                         ↓
              AGENTS / kernel / domain state
```

The arrows are source dependencies: outer details implement inward-owned
ports; the application service depends on domain policy, never the reverse.

### Application contract

Begin with only the lifecycle intents already felt in production:

- `session-start`: run `estate-sync` and only then `session-start`;
- `post-write`: run quiet validation as feedback;
- deliberate session-end and retrospective prompts remain human-invoked;
- Git pre-commit remains the enforcement boundary.

The ordering belongs to the application contract. How a harness guarantees
that ordering belongs to its adapter. This distinction matters immediately:
Claude's current configuration expresses the two startup commands in one hook
group, while Codex launches multiple matching command hooks for the same event
concurrently. Codex therefore needs one sequential handler; copying the Claude
JSON shape would silently break the contract.

### Narrow adapter ports

Use small interfaces rather than a single harness god-object:

- **Render port** — produce new-project managed artifacts from a domain
  context (`framework_root`, platform, selected capabilities).
- **Inspect port** — parse existing artifacts without changing them and report
  config shape, managed-fragment currency, and local extensions.
- **Probe port** — execute safe commands and consume lifecycle attestations;
  it may report untested when the harness event cannot be fired mechanically.
- **Install/merge service** — owns filesystem mutation policy independently of
  vendor schema; creates new files, merges a clearly owned fragment, or stops
  on ambiguity.

Each adapter declares only the capabilities it implements. Unsupported
capabilities are data, not exceptions. Scaffold and doctor depend on these
ports and a registry, not on Claude or Codex JSON structures.

This applies SOLID directly:

- **Single Responsibility:** lifecycle intent, runtime resolution, vendor
  rendering, config merging, diagnostics, and execution probes change for
  different reasons and live separately.
- **Open/Closed:** a future harness adds an adapter registration; scaffold and
  doctor do not gain another vendor-shaped conditional branch.
- **Liskov Substitution:** every adapter returns the same honest diagnostic
  dimensions; an unsupported or untrusted hook is a valid report, not a fake
  success.
- **Interface Segregation:** a harness that supports discovery but no lifecycle
  events does not implement render/probe methods it cannot honour.
- **Dependency Inversion:** application services depend on the ports; Claude
  and Codex config schemas depend on the lifecycle contract.

### Diagnostic model

For each capability, `mdllm doctor` reports independent dimensions:

| Dimension | Example values |
|---|---|
| Support | supported / unsupported / unknown |
| Configuration | absent / present-current / present-stale / invalid / extended |
| Trust | not-applicable / unknown / review-required / trusted / managed |
| Runtime | unresolved / command-runs / dependency-missing |
| Execution | untested / passed / failed, with timestamp or attestation source |

The existing floor verdict remains independent. A missing adapter can be
reported alongside `FLOOR ACTIVE`; an installed-but-untrusted Codex hook is not
reported as active. `doctor --harness claude|codex|all` supplies the vendor
diagnostic; the existing command without the option remains compatible and
inspects what is present.

## Codex projection

The first Codex adapter should be deliberately small and project-local:

- write `.codex/hooks.json`, not global config;
- bind `SessionStart` for `startup|resume|clear|compact`, so compaction restores
  the same Tier-0 ritual before the next model request;
- use one SessionStart command that performs the ordered two-step application
  intent;
- bind `PostToolUse` to the file-edit aliases supported by Codex and keep it
  advisory—the Git hook remains the complete enforcement boundary;
- provide a POSIX `command` and a Windows `commandWindows`, both resolving from
  the Git root rather than assuming the session cwd;
- keep hook output concise and within the model-visible context budget;
- report project-layer trust and per-hook hash review as an operator step;
- do not bind semantic session-end continuity: Codex SessionEnd is advisory,
  cannot steer the closed session, and has a short timeout;
- do not install a Codex skill or plugin merely to host these project hooks.

Current official Codex documentation is the external contract to verify again
at implementation time: [AGENTS.md discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
and [hooks](https://learn.chatgpt.com/docs/hooks). The live execution phase,
not the documentation alone, earns the compatibility claim.

## Claude non-regression boundary

Claude safety is a release gate, not a hope:

1. Capture the current scaffolded `.claude/settings.json`, Claude command
   files, and scaffold messages as golden fixtures before extraction.
2. Extract a Claude adapter whose first output is byte-for-byte identical.
   No event, matcher, command order, path, permission, or default changes in
   that phase.
3. Add merge tests proving existing `permissions` survive and an extended
   SessionStart command remains untouched. The live estate contains both
   cases.
4. Keep the existing Claude tests and add semantic execution tests; do not
   replace concrete assertions with generic adapter-only mocks.
5. A Codex renderer or probe failure must not prevent the Claude adapter from
   rendering or being inspected.
6. Existing domains receive no adapter rewrite during framework upgrade.
   Doctor may recommend an explicit command and show a diff; only the operator
   runs it.
7. Any shared runtime or Git-hook change runs the existing Claude/Windows and
   POSIX hook suite before release.

## Ownership and cross-harness handoff gate

Ownership here means responsibility for implementing and evidencing a work
package. It does not make either vendor the owner of shared substrate policy.
The inward lifecycle contract remains vendor-neutral and both agents review it
from their own harness side.

### Claude Code agent — extraction work package

The Claude Code agent owns **Phases 0–2 only**:

- freeze the current Claude artifacts and behaviour;
- implement the shared runtime work needed by the extraction;
- extract Claude behind the inward-owned adapter ports without changing its
  emitted bytes or live behaviour;
- add the architecture fitness test and Claude regression evidence;
- commit the completed work package and stop.

The Claude Code agent is explicitly **not authorised** by this work package to
create `.codex/`, model Codex events, implement vendor diagnostics, add Codex
scaffold flags, or continue into Phase 3. It must not design the inward
contract as a generalisation of Claude's JSON shape; the lifecycle intents in
this plan are the contract.

### Hard stop — Codex acceptance before any Codex build

No Phase 3 or Phase 4 work may begin until the Codex agent independently
accepts the Phase 0–2 handoff. Acceptance requires all of the following:

1. Claude golden fixtures remain byte-identical and the existing Claude suite
   passes.
2. Vendor-neutral lifecycle, scaffold, diagnostic, and runtime modules contain
   no Claude config paths, environment variables, permission structures, or
   vendor event-schema assumptions. A mechanical architecture test enforces
   the allowed boundary: Claude vocabulary may appear only in the Claude
   adapter, its fixtures/tests, and explicitly vendor-specific documentation.
3. The Codex agent can explain and implement the ports without importing,
   calling, subclassing, or parsing the Claude adapter.
4. Framework-root and directly opened nested-domain runtime/commit probes pass
   in the Codex managed shell, or any failure is routed back as shared-runtime
   work rather than patched inside the future Codex adapter.
5. The Codex review finds no least-common-denominator abstraction or hidden
   Claude ordering assumption in the application contract.

A failed condition returns the work to the Claude extraction package (or the
shared runtime slice). It must never be bypassed with a Codex-side workaround.

### Codex agent — diagnostic and Codex work package

After accepting the handoff, the Codex agent owns **Phases 3–5**:

- build the vendor-neutral diagnostic against the accepted ports;
- implement the Codex adapter independently from official Codex contracts;
- add explicit adapter install and scaffold selection;
- preserve every Claude golden and merge-safety test while changing shared
  orchestration surfaces;
- commit the completed work package and stop before rollout.

The Codex agent may change shared interfaces only when Codex evidence exposes
a real missing abstraction. Such a change reopens the Claude regression gate;
it is not permission to edit Claude output for convenience.

### Shared verification and operator ownership

- In Phase 6, the Claude Code agent owns the live Claude execution record and
  the Codex agent owns the live Codex execution record. Neither agent can
  self-certify the other harness.
- In Phase 7, the Codex agent leads reconciliation after both execution records
  pass; the Claude Code agent reviews Claude-facing instructions and fixtures.
- Phase 8 belongs to the operator. Harness defaults, estate migration, and
  publication are product decisions, not adapter-agent decisions.

## Phased plan

### Phase 0 — Freeze the contract and evidence (owner: Claude Code agent)

- [ ] Record golden Claude scaffold artifacts and current CLI behaviour.
- [ ] Add estate-shape fixtures: hooks-only config, permissions-only config,
  permissions-plus-hooks, no settings, and a locally extended startup command.
- [ ] Define the minimal lifecycle intents and diagnostic dimensions in tests
  before creating adapter classes.
- [ ] Record current Codex hook documentation date and a live-harness test
  checklist; do not encode undocumented assumptions.

**Gate:** the baseline suite passes without changing a generated byte.

### Phase 1 — Repair the shared runtime port (implementer: Claude Code agent; acceptance: Codex agent)

- [ ] Give root and nested-domain launchers one runtime-resolution service.
  Resolve both the domain-local environment and the framework-root environment
  derived from the CLI path.
- [ ] Keep PowerShell and POSIX entry paths behaviourally equivalent; avoid
  absolute installation paths and vendor cache paths.
- [ ] Make `install-hook` execution-test the emitted pre-commit hook where Git
  supports it, and teach doctor to distinguish interpreter-found from
  dependency-loaded and command-executed.
- [ ] Test a directly opened nested domain in the Codex managed shell before
  relying on lifecycle hooks.

**Gate:** the framework and a nested domain both execute validation and a real
pre-commit through the same checked-in resolution policy.

### Phase 2 — Extract Claude without changing Claude (owner: Claude Code agent; acceptance: Codex agent)

- [ ] Introduce the adapter ports/registry and move the inline Claude scaffold
  projection behind a Claude adapter.
- [ ] Make scaffold call the registry while preserving its current default and
  exact Claude output for backward compatibility.
- [ ] Move doctor’s Claude parsing into the inspect port and report extensions
  rather than flattening them.
- [ ] Keep `.claude/commands` as a separate deliberate-shortcut projection;
  do not conflate it with lifecycle hooks.

**Gate:** golden files are byte-identical, all existing tests pass, and an
existing composite Claude settings file round-trips without loss. The Claude
agent then stops; the cross-harness handoff gate above must pass before Phase 3.

### Phase 3 — Build truthful harness diagnostics (owner: Codex agent)

- [ ] Add `doctor --harness` capability reports with the five independent
  dimensions above.
- [ ] Derive managed-fragment currency from the same adapter renderer used to
  create it; compare semantically where formatting is operator-owned.
- [ ] Add execution attestations/probes without claiming that a static probe
  fired a real session event.
- [ ] Report remediation commands and ownership boundaries; never auto-fix.

**Gate:** fixtures prove that present-but-invalid, present-but-untrusted,
runnable-but-untested, extended, and verified cannot be conflated.

### Phase 4 — Add the Codex adapter (owner: Codex agent)

- [ ] Render a project `.codex/hooks.json` with one sequential SessionStart
  handler, file-edit PostToolUse validation, stable root resolution, bounded
  output, and Windows/POSIX commands.
- [ ] Inspect config, project trust, hook-review state where observable, runtime
  resolution, and managed-fragment currency. Report `unknown` where Codex does
  not expose a stable machine-readable fact.
- [ ] Exclude `.codex` from thing-corpus scanning just as `.claude` is excluded.
- [ ] Add schema, rendering, merge, cwd/subdirectory, compaction-source, output
  limit, and failure-path tests.

**Gate:** adapter unit/integration tests pass without touching Claude fixtures.

### Phase 5 — Expose explicit install and scaffold selection (owner: Codex agent)

- [ ] Add an explicit human-invoked adapter install/refresh command that shows
  the owned diff and refuses ambiguous merges.
- [ ] Add repeatable scaffold selection such as `--harness claude`,
  `--harness codex`, `--harness all`, and `--harness none` while preserving the
  no-flag behaviour during this compatibility release.
- [ ] Keep AGENTS.md, skills, prompts, schema, and Git hooks identical across
  harness selections; only outer projections vary.
- [ ] Do not decide a new default as part of the refactor. A default change is
  a versioned product decision after live evidence, not architecture cleanup.

**Gate:** two scaffolds selected for different harnesses differ only in their
outer adapter artifacts and both validate cleanly.

### Phase 6 — Execute in real harnesses (split ownership by harness)

- [ ] Claude non-regression: scaffold, open, observe SessionStart ordering,
  edit a thing, observe PostToolUse feedback, and commit through the floor.
- [ ] Codex framework root: trust the project layer through the documented
  human flow, start/resume/compact, observe injection, edit, validate, commit.
- [ ] Codex nested domain: open the domain as its own workspace and repeat the
  lifecycle and Git-floor probes.
- [ ] Record exact harness/version/platform evidence and failures. A passing
  unit test earns designed-for; only these runs earn verified-on.

**Gate:** Claude remains verified and Codex is verified on the specifically
tested surfaces, with no wider claim.

### Phase 7 — Reconcile every public surface (Codex lead; Claude review)

- [ ] Update orchestration, discovery, refresh, operator guide, first-hour,
  domain guide, README compatibility table, scaffold output, and adapter
  examples from the same settled capability vocabulary.
- [ ] Replace “the adapter” where it means Claude with a generic rule plus
  named vendor projections. Preserve vendor-specific instructions where the
  distinction is real.
- [ ] Add a framework-map adapter/diagnostic node if the new CLI surface lands.
- [ ] Run the change-reconciliation dark-region walk; do not rely only on grep
  or generated checks for semantic claims.

**Gate:** validate, coherence, kernel freshness where applicable, the full
suite, and the Claude/Codex execution records all pass.

### Phase 8 — Rollout and migration decision (owner: operator)

- [ ] Decide, with the operator, whether future scaffolds retain Claude as the
  compatibility default, require explicit harness selection, or emit more than
  one adapter by default.
- [ ] Offer existing domains an opt-in diagnostic and managed-fragment diff;
  never batch-rewrite the estate.
- [ ] Version and changelog the decision, then close this plan with exact
  evidence and remaining unsupported harnesses.

## Completion criteria

This plan is complete only when:

- Claude scaffold output and live lifecycle behaviour have not regressed;
- a new Codex-selected domain can be opened directly and run startup,
  post-write feedback, validation, and commit through a resolved runtime;
- the substrate and every domain remain usable with no harness adapter;
- doctor reports support, configuration, trust, runtime, execution, and
  currency without collapsing them;
- existing permission rules and local hook extensions survive or cause a safe
  refusal;
- adding a third harness requires a new adapter, tests, and docs—not edits to
  domain policy, scaffold control flow, or doctor control flow;
- compatibility claims name the exact harness and evidence that earned them.

## Held outside this plan

- Repackaging MarkdownLLM domain skills as Codex-native skills or a Codex
  plugin. The domain files already are the portable program.
- Building a universal hook DSL. The minimal lifecycle intent is enough until
  another adapter proves a richer abstraction is felt.
- Automatically interpreting or resolving Codex trust. Trust is a human or
  managed-policy decision; diagnostics may observe and explain it only.
- Automating the semantic session-end continuity ritual. It remains a
  deliberate reasoning act, not a short cleanup hook.
- Claiming Cursor, Windsurf, Gemini, Codex CLI, or any other surface verified
  because Claude or Codex desktop passed. Each claim needs its own execution
  evidence.
