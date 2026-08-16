---
id: vendor-harness-adapter-foundation
type: plan
status: in-progress
version: 1.20
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
  - id: protecting-one-budget-displaces-the-failure-into-the-other
    relation: references
    notes: "Earned by this plan: Gate 5R.5 protected orientation's time budget and the same truncation reappeared in the character budget at Gate 6R. Both bounds are now allocated per step."
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: references
    notes: "Preserves the human/tool gate around automatic powers and operator-owned configuration."
  - id: a-layered-harness-is-a-co-author-not-a-substrate
    relation: references
    notes: "Keeps the adapter thin and prevents a harness operating layer from becoming Definition Zero."
  - id: relative-path-hooks-break-in-nested-domain-repos
    relation: implements
    notes: "Makes stable root and runtime resolution a shared port rather than a per-adapter path convention."
  - id: codex-port-challenge-2026-08-11
    relation: references
    notes: "Phase 2B evidence: official Codex constraints, accepted port corrections, managed-shell runtime failures, and the Phase 6 checklist."
  - id: codex-final-handoff-audit-2026-08-11
    relation: references
    notes: "Final A/0–2 acceptance evidence: the shared runtime passes real Codex-shell probes, while incomplete service-facing ports and unsafe Claude currency inspection return Phase 2C for correction."
---

# Vendor Harness Adapter Foundation

Preserve the working Claude Code path, add first-class Codex lifecycle
hardening, and create a truthful vendor diagnostic without moving any domain
semantics into a vendor layer.

This is an architecture and rollout plan. It authorises no adapter or domain
configuration changes by itself. Implementation begins only after the operator
accepts the boundary and phase order.

**Current execution boundary:** Phase 5R is complete. Claude independently
accepted Gate 5R.5 at `ea4ea12`: the unchanged PowerShell 5.1 reproduction
passed and a real automatic framework-root session emitted both successful
steps, all four orientation elements, a fresh session-gate attestation, and
current-definition evidence. **Phase 6R is complete and Gate 6R was
independently accepted by Claude on 2026-08-16 at `b82061f`
(`evidence/claude-gate-6r-acceptance-2026-08-16.md`). **The post-6R Codex
root, directly opened nested-domain, PostToolUse and no-adapter records are
complete on Windows CLI 0.147.0
(`evidence/codex-phase6-post-6r-acceptance-2026-08-16.md`).** Estate rollout had
exposed that the neutral runner's 2,200-character global tail slice silently
dropped version, velocity, and open-loop orientation on large domains even
when both lifecycle steps succeeded. The correction allocates bounded output
structurally — per-step protected character shares, Markdown-structural
sections, fair-shared limits, and both edges retained with elision marked —
so no content is declared permanently disposable, and both adapter hashes
carry the corrected semantics, so pre-correction attestations do not count.
Claude has completed native Linux lifecycle dispatch at `3254a99`, and all 13
nested domains are migrated to the one-handler projection and sealed to
v3.31.0. Codex Desktop build `26.803.10989.0` injected AGENTS instructions but
did not dispatch the current project SessionStart hook in a fresh
framework-root task, while Codex CLI has now established positive automatic
generic SessionStart evidence at root and in a directly opened nested domain.
The current attestation does not preserve the normalized source, so no
individual `resume`, `clear`, or `compact` claim is made. Neither harness may
reuse pre-correction attestations. Two earlier
execution probes disproved assumptions that the 438-test gate did not
deterministically exercise: a stderr-writing Python candidate terminates the
Windows PowerShell 5.1 resolver, and current Claude Code runs matching hook
handlers in parallel, so the scaffolded two-handler SessionStart form does not
guarantee `estate-sync` before `session-start`. The framework root and nested
estate now carry both adapters where selected; publication remains the
operator's act.

## Claude acceptance amendments — v1.10 (2026-08-12)

Claude's independent review accepted the v1.9 architecture and identified four
facts that must be explicit before 5R.0 freezes the launch seam. The follow-up
contract audit accepted all four in substance, with two factual corrections:

1. **Claude's Windows shell is documented.** A command hook with `args` uses
   shell-free exec form. Shell form uses `sh -c` on macOS/Linux and Git Bash on
   Windows, falling back to PowerShell when Git Bash is unavailable. An explicit
   `"shell": "powershell"` is supported on Windows and selects PowerShell 7
   with Windows PowerShell 5.1 fallback. The root's field is therefore valid;
   its combined command remains a Windows-specific legacy projection rather
   than the portable current form.
2. **Current command-hook defaults are 600 seconds, not 60.** That correction
   does not weaken the budgeting requirement. Both renderers must declare the
   same explicit 120-second envelope, and the neutral launch/application work
   must fit hierarchically inside it without borrowing a later required step's
   reserve.
3. **The Codex source is official and has a canonical Developers address.**
   [`developers.openai.com/codex/hooks`](https://developers.openai.com/codex/hooks)
   currently redirects to the official Learn page. Repository citations use
   the Developers address so the provenance is immediately recognisable; the
   documented `/hooks` surface remains CLI-specific.
4. **5R.2 and Phase 6 prove different things.** Direct execution of a rendered
   handler is renderer/launch acceptance and earns only `designed-for`.
   Automatic dispatch by the real product, correlated with its transcript and
   hash-bound attestation, is reserved for Phase 6 and alone earns
   `verified-on`.

These amendments add tests and acceptance boundaries, not another abstraction.
If 5R.0 execution shows that exec form or the existing launch specification is
insufficient, the port is settled from that evidence before implementation.

## Amendment record — v1.9 (2026-08-12, live gate reopened)

The operator declared the live findings consequential and requested a proper
replan. The change-reconciliation pass found that the inward lifecycle intent
is sound; the defects sit at three outward/infrastructure seams:

1. **Runtime launch is not yet one owned capability.** The POSIX resolver is
   shared, but Windows candidate probing is repeated in `mdllm.ps1` and the
   Codex renderer, and both can terminate on a failed native probe under
   Windows PowerShell 5.1. Candidate discovery, dependency probing, CLI
   dispatch, timeout, and advisory failure are one neutral launch concern.
   Adapters may encode that concern into vendor schema; they must not invent
   another resolution policy.
2. **The Claude projection preserved bytes, not behaviour.** The Phase 2
   extraction correctly froze the then-current artifact, but current official
   Claude Code documentation says all matching handlers run in parallel and
   handlers run from the current directory. Two handlers in one matcher group
   therefore neither prove ordering nor cwd stability. The frozen bytes remain
   historical/legacy evidence; they are no longer the desired renderer.
3. **Install is safe but refresh is not yet modelled.** The generic service can
   create, merge an absent fragment, preserve a current extension, or refuse.
   It cannot distinguish an exact known legacy managed fragment from an
   arbitrary stale one, so it cannot safely propose an operator-approved
   migration while byte-preserving permissions and unrelated settings.

The corrective architecture is explicit:

```text
LifecycleBinding (policy: steps, order, delivery, failure)
                         |
                lifecycle application service
                         |
       neutral launch service + runtime resolver + attestation
                    /                         \
       Claude schema/output              Codex schema/output
                    \                         /
             read-only inspection + migration proposals
                         |
           generic preflight / atomic apply service
```

The **neutral launch service** owns how an already-declared binding reaches the
resolved framework CLI. It must expose immutable launch data or builders that
both adapters consume, work from a moved session cwd, and preserve the existing
three runtime facts. Claude owns only event/matcher/config and Claude output
envelopes; Codex owns only its event/matcher/config, POSIX/Windows fields,
context bounds, and Codex output envelopes. The CLI composition root resolves
an adapter and injects its output port into the lifecycle service; neutral
execution code must not require knowledge of a concrete adapter or registry.

Known legacy migration becomes a separate, opt-in state transition rather than
weakening the existing refusal rule. An adapter may identify exact historical
managed definitions as data. The generic service owns byte-span replacement,
preflight, atomicity, concurrent-state recheck, and refusal. No adapter may
round-trip or rewrite the composite document itself.

Official contract evidence for this amendment was rechecked on 2026-08-12
against the current [Claude Code hooks reference](https://code.claude.com/docs/en/hooks)
and [Git hook command reference](https://git-scm.com/docs/git-hook). A launcher
mechanism is not accepted merely because it looks portable: the first Phase 5R
gate must execute the proposed invocation on POSIX, PowerShell 7, and Windows
PowerShell 5.1 before its interface is frozen.

### Remaining coupling disposition

The coupling audit separates release blockers from debt so Phase 5R neither
papers over a Claude assumption nor expands into an unbounded rewrite.

| Seam | Disposition | Owner / gate |
|---|---|---|
| two-handler Claude ordering, direct CLI calls, no Claude output port | remove now; one handler must enter the neutral runner | Claude owner, 5R.2 |
| duplicated runtime candidates and PowerShell probe behavior | remove now; executable plus prefix arguments is one neutral candidate value | Codex/shared owner, 5R.1 |
| cwd-relative Claude project path | remove now at the Claude edge using its documented project-root surface | Claude owner, 5R.2 |
| stale-vs-known-legacy ambiguity | remove now with exact legacy data and explicit generic refresh | split ownership, 5R.3 |
| Claude Code lifecycle plus GitHub Copilot prompt shortcuts in one concrete adapter | preserve compatibility, but name it as an adapter bundle or split capability projections before claiming a general vendor registry | Phase 7/8; not a 5R blocker |
| registry requires Render and Inspect from every entry | either declare it specifically as the lifecycle-project-adapter registry or make capabilities optional before onboarding a non-lifecycle diagnostic vendor | architecture debt; gate before third adapter |
| `.claude`, `.codex`, and `CLAUDE.md` exclusions named in the corpus model | replace eventually with an adapter-independent infrastructure-ignore rule; do not import vendor adapters into the domain model | separate model cleanup |
| `mdllm eval --run` launches `claude -p` | keep in the separately owned multi-backend eval scope; lifecycle portability must not be restated as all-tooling portability | existing explicit boundary |
| Claude remains the no-flag scaffold default | retain until the operator's Phase 8 product-policy decision | operator, not an architecture repair |

Legitimate edge details stay vendor-specific: file schema, event names,
matchers, project-root syntax, shell encoding, feedback envelopes, trust/review
semantics, shortcuts, and vendor goldens. Moving those inward would be coupling,
not decoupling.

## Amendment record — v1.8 (2026-08-12, Codex Phases 3–5 complete)

The diagnostic vocabulary is now settled at its consumer as six independent
facts: support, configuration, currency, trust, runtime, and execution;
extensions, findings, ownership, and evidence provenance remain explicit
detail rather than being collapsed into one "active" verdict. Static runtime
success leaves execution untested. Real events write clone-local,
definition-hash-bound attestations, and changed definitions invalidate old
evidence.

The Codex adapter renders only the project `.codex/hooks.json` surface, keeps
SessionStart ordering inside one handler, translates advisory failures through
Codex's structured context channel, and emits cwd-independent POSIX and Windows
commands. The Windows path is tested through both PowerShell 7 and the stock
Windows PowerShell fallback. Trust and exact-hook review remain operator facts;
the implementation neither reads nor mutates global Codex state.

The explicit install service preflights every selected adapter before writing,
preserves bytes outside a clearly owned composite fragment, and refuses
invalid, duplicate, alternate-source, stale, or ambiguous state. A cold audit
expanded that boundary around duplicate JSON keys, concurrent mutation and
rollback, portable path collisions, scaffold/core collisions, formatter
attestation order, diagnostic provenance, and shell injection. Those cases now
have regressions. The final focused adapter/launcher gate passed 67 tests and
the authoritative full run passed 438 tests; its temporary repositories lived
outside the framework Git worktree so non-repository fixtures retained their
intended topology. A separate cold replay accepted every returned blocker and
found no remaining defect. Framework validation then checked 190 things across
the three corpora with zero findings; coherence retained only the pre-existing
informational note about the recently changed stable scalability guide.

## Amendment record — v1.7 (2026-08-11, final handoff accepted)

Claude's v1.6 return package repaired the shared runtime, declared every
service-facing port, and closed the named inspector cases. The Codex cold-read
gate additionally varied a renderer-owned hook field while preserving its
command; the old comparison certified `type: prompt` as current. Currency now
compares the complete managed entry, with command-tail arguments as the sole
explicit extension seam. The architecture fake now opts into and is asserted
through every declared doctor/scaffold presentation port. With 45 focused
tests passing after those corrections, the no-workaround gate is closed and
ownership advances explicitly to the Codex diagnostic, adapter, and install
work package.

## Amendment record — v1.6 (2026-08-11, final Codex handoff audit)

The shared runtime implementation is accepted on behaviour: the framework
root resolved its repository venv and executed the floor; a fresh nested repo
with no domain venv installed and executed the real pre-commit hook; and a
directly opened live nested domain resolved the same framework runtime. The
old `dirname` dependency is gone, every PowerShell candidate is dependency
probed, and `command_executed` is independently reported.

The complete handoff is nevertheless rejected. Neutral scaffold and doctor
code call three Claude-concrete methods that no accepted port declares, while
the architecture gate checks only `RenderPort` and `InspectPort`. A second
adapter can therefore satisfy every declared protocol and still crash both
shared consumers. Claude inspection also admits false-current and
under-reported shapes: token-prefix mutations, extra or duplicate managed
PostToolUse handlers, and an operator-only hook event. Finally, the new
`command_executed` test moves its entry outside the framework runtime and then
assumes PATH supplies PyYAML; it passes in Claude's environment but fails in
the target Codex shell. Exact evidence and the return boundary are recorded in
`evidence/codex-final-handoff-audit-2026-08-11.md`. No project `.codex/` state
was created and Phases 3–5 did not begin.

## Amendment record — v1.5 (2026-08-11, Codex Phase 2B)

The Codex agent challenged the draft ports against the official Codex hooks
shape, in memory only, and created no project `.codex/` state. The render /
inspect / later-probe / later-merge separation survived, with six corrections
recorded in `evidence/codex-port-challenge-2026-08-11.md`: immutable complete
lifecycle bindings, a host-independent render context, pure reusable
rendering, renderer-derived inspection currency, explicit invalid/unreadable
facts, and truthful lifecycle-only capability claims. Phase 2B is closed and
returned to Claude for extraction.

The handoff audit also reopened Phase 1 acceptance. The POSIX hook resolver
uses external `dirname`, which is absent in the Codex managed Git-hook shell;
the PowerShell candidates are not all dependency-probed; and runtime-probe
does not yet return the required command-executed fact. These are shared
runtime defects and are explicitly returned to Claude's Phase 1 slice rather
than bypassed in a Codex adapter. The Phase 0 evidence count was corrected to
the live 11 standard settings + one local settings + one absent shape, and its
two text-normalising golden assertions were strengthened.

## Amendment record — v1.4 (2026-08-11)

Two v1.3 defects fixed before execution began; no scope change.

1. **Phase 1's gate is closable by its own owner again.** v1.3 handed the
   nested-domain managed-shell probe to Codex ("Claude does not self-certify
   that environment") while Phase 1's gate still demanded nested-domain
   execution — so Phase 1 could not close until 2B, inverting the phase
   order. The gate now names the environment: Claude certifies its own
   harness against the live estate's nested domains; the same probe run in
   the Codex managed shell belongs to 2B and final acceptance.
2. Restored the blank line before Phase 1's gate (rendering defect).

## Amendment record — v1.3 (2026-08-11, Codex cold read)

The Codex agent cold-read v1.2 against the live code and documentation before
accepting any implementation work. The new coupling findings were sound, but
five corrections were required to keep the ownership and port boundaries
internally consistent. Each is marked **[v1.3]** where it lands.

1. **The Codex spike changes owner and phase.** v1.2 correctly saw that ports
   extracted from one vendor need a second real shape before they harden, but
   assigned that Codex modelling to the Claude agent while simultaneously
   prohibiting Claude from modelling Codex events. Phase 2 is now an explicit
   Claude draft → Codex challenge → Claude extraction sequence.
2. **The eval coupling is split at its real seam.** Default `mdllm eval` is a
   vendor-neutral deterministic assertion runner used by domains; only
   `mdllm eval --run` shells the Claude CLI. Live-runner portability remains a
   separately owned follow-up, not a reason to describe the whole command as
   development-only.
3. **Inspect, render, and merge stay separate.** Phase 2 no longer asks a
   composite settings file to round-trip through the new-project renderer.
   Inspection is read-only; mutation and byte-preserving merge begin in Phase
   5, where the write path actually exists.
4. **Runtime evidence precedes diagnostic vocabulary.** Phase 1 produces a
   neutral runtime probe result and tests it; Phase 3 owns the user-facing
   doctor vocabulary and presentation.
5. **The prose sweep is named accurately.** It crosses a Tier-1 spec, a Tier-2
   guide, and example skills, so it is a canonical prose-address sweep rather
   than a “Tier-1 spec” sweep. Occurrence counts are deliberately not
   restated—the execution-time search is the source.

## Amendment record — v1.2 (2026-08-11)

v1.1 was reviewed from the Claude Code side against the live tree. The
diagnosis held on every claim checked; six amendments follow, and each is
marked **[v1.2]** at its point of use so the Codex agent can diff intent
without re-reading the whole plan.

1. **Two coupling surfaces were missing from the map** — vendor vocabulary in
   the Tier-1 specs, and the eval harness. Both are now rows in the assessment
   table. The first becomes Phase A; the second is held outside.
2. **Phase A added** — the spec vocabulary sweep, an independent slice that
   needs no port, no adapter, and no handoff.
3. **A throwaway Codex renderer spike enters Phase 1**, so the ports are shaped
   against two real vendor shapes rather than extracted from Claude alone.
4. **The merge-test requirement gets a phase home** (Phase 5, not the Claude
   package), because scaffold cannot reach the merge path at all.
5. **Phase 0 no longer freezes the diagnostic vocabulary** — that contract
   belongs to the phase that has to satisfy it.
6. **Defect 3 is restated more exactly**; the pre-commit hook body, not only
   doctor, is where the runtime fix lands.

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
| Canonical prose address **[v1.3]** | Medium — prose only | *Dependency* is low; *address* is not. `thing.md`, `scalability-guide.md`, and the life-manager example skills repeatedly say “Claude” where they mean “the reasoning agent”. A Codex session reading them is addressed as another vendor. Generated `kernel.md` and `templates/` are already clean, so the fix is prose-layer and cannot regress a scaffold. The execution-time search owns the occurrence list; this plan does not maintain a count. |
| Eval live-runner backend **[v1.3]** | Split | Default `mdllm eval` checks fixture assertions deterministically and is a documented domain capability; it is vendor-neutral. The optional Stage 2 path, `mdllm eval --run`, resolves and shells the Claude CLI. Multi-backend live eval is outside this lifecycle-adapter plan but must be routed to an owned follow-up before “all tooling is vendor-neutral” can be claimed. |
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

   **[v1.2] Stated exactly, from `HOOK_BODY` in `tools/markdownllm/scaffold.py`:**
   the candidate list is `$ROOT/.venv/...` where `ROOT` is the *domain* Git root,
   while `$MDLLM` is `$ROOT/{rel}` resolving *upward* to the framework. The
   framework-root environment is therefore unreachable by construction, not by
   accident of the current shell. Compounding it, the candidate probe is
   `"$c" -c "import sys"` — that proves an interpreter exists, not that PyYAML
   loads, so a bare `python3` passes the probe and then fails at `import yaml`,
   blocking the commit with a message that names neither cause. The fix belongs
   in the emitted hook body, not only in doctor's reporting.

These are adapter-foundation problems, not reasons to alter the substrate or
the domains.

## Requirements and invariants

The build must satisfy all of these simultaneously:

1. **Vendor-neutral core.** Lifecycle policy names framework intents such as
   synchronise estate, orient session, and validate after a write. It never
   names a vendor event or config format.
2. **Claude remains behaviourally stable.** The first extraction preserved the
   historical scaffold bytes before any Codex artifact was introduced. A
   later correction may version a new managed form only after the old bytes
   become an explicit legacy fixture, ordering/cwd/runtime are execution-tested,
   and a safe operator-gated migration path exists. Byte preservation is an
   extraction gate, not permission to preserve disproved behaviour forever.
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
11. **One inward runtime-launch policy.** Candidate order, dependency probes,
    framework CLI dispatch, time budget, and advisory failure semantics are
    neutral application/runtime concerns. Vendor adapters encode the launch;
    they do not fork its policy.
12. **Legacy is data, not a guess.** A stale artifact is migratable only when
    its managed fragment exactly matches an adapter-declared historical form.
    Unknown stale state, duplicate candidates, and local changes remain
    refusals. Migration is explicit and diff-first.
13. **Configuration and clone-local execution infrastructure are separate.** A
    current project adapter plus an absent/stale launch mechanism is reported
    as configured-but-not-runnable, never promoted to current execution.

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

The ordering belongs to the application contract. A vendor event schema does
not earn that ordering merely by placing two handlers in one group. Current
Claude Code and Codex contracts both permit matching handlers to run
concurrently. Each lifecycle moment therefore renders **one matching handler**
which invokes the neutral lifecycle application service once; that service
executes the inward `steps` tuple serially. The adapter owns event matching and
output translation, not the ordered loop.

### Narrow adapter ports

Use small interfaces rather than a single harness god-object:

- **Render port** — produce new-project managed artifacts from a domain
  context (`framework_root`, platform, selected capabilities).
- **Inspect port** — parse existing artifacts without changing them and report
  config shape, managed-fragment currency, and local extensions.
- **Probe port** — execute safe commands and consume lifecycle attestations;
  it may report untested when the harness event cannot be fired mechanically.
- **Lifecycle output port** — translate one neutral execution result into the
  harness's documented context/feedback envelope.
- **Launch service** — turn a binding invocation into a runtime-resolved,
  cwd-stable call to the lifecycle service. It is shared infrastructure, not a
  vendor port, and returns renderable data rather than writing config.
- **Install/merge service** — owns filesystem mutation policy independently of
  vendor schema; creates new files, merges a clearly owned fragment, or stops
  on ambiguity.
- **Legacy-definition port** — optional adapter data naming exact historical
  managed forms. The mutation service, not the adapter, locates and replaces
  their owned byte span after explicit refresh authorisation.

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

For each capability, `mdllm doctor` reports independent facts:

| Dimension | Example values |
|---|---|
| Support | supported / unsupported / unknown |
| Configuration | not-applicable / absent / present / invalid / ambiguous / unknown |
| Currency | not-applicable / current / stale / unknown |
| Trust | not-applicable / unknown / review-required / trusted / managed |
| Runtime | not-applicable / unknown / unresolved / dependency-missing / command-failed / command-runs |
| Execution | not-applicable / untested / passed / failed, with timestamp and attestation source where available |

Extensions, findings, ownership boundaries, remediation, and evidence detail
are reported alongside these facts. They do not silently alter another fact.

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
and [hooks](https://developers.openai.com/codex/hooks). The live execution phase,
not the documentation alone, earns the compatibility claim.

## Claude non-regression boundary

Claude safety is a release gate, not a hope:

1. Capture the current scaffolded `.claude/settings.json`, Claude command
   files, and scaffold messages as golden fixtures before extraction.
2. Extract a Claude adapter whose first output is byte-for-byte identical.
   No event, matcher, command order, path, permission, or default changes in
   that phase. **[v1.9 correction:]** this historical gate passed, but live
   contract review later disproved the preserved ordering assumption. The old
   golden now freezes a recognised legacy form; a new current golden is earned
   only by Phase 5R execution tests.
3. Add merge tests proving existing `permissions` survive and an extended
   SessionStart command remains untouched. The live estate contains both
   cases. **[v1.3] This requirement is gated in Phase 5, not in the Claude
   extraction package.** Scaffold cannot reach the merge path — it exits on a
   non-empty target — so merge only ever executes through the Phase 5
   install/refresh command. Phase 2 owes a read-only inspection property: it
   identifies the managed hook fragment and reports permissions/local
   extensions without rewriting or normalising the source document. It does
   not feed a composite settings file through the new-project renderer; that
   would collapse inspect, render, and merge before a merge use case exists.
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

### Claude Code agent — historical extraction work package (through v1.8)

For the original extraction handoff, the Claude Code agent owned **Phase A,
Phases 0–1, and Phase 2A/2C only**:

- **[v1.3]** sweep vendor address out of the canonical framework prose and
  example skills (Phase A), independently of the adapter implementation;
- freeze the current Claude artifacts and behaviour;
- implement the shared runtime work needed by the extraction;
- draft the narrow ports without moving Claude, then pause for the Codex-owned
  Phase 2B challenge;
- resume only after that challenge and extract Claude behind the accepted
  inward-owned ports without changing its emitted bytes or live behaviour;
- add the architecture fitness test and Claude regression evidence;
- commit the completed work package and stop.

Under that historical work package the Claude Code agent was explicitly **not
authorised** to
create `.codex/`, model Codex events, implement vendor diagnostics, add Codex
scaffold flags, or continue into Phase 3. It must not design the inward
contract as a generalisation of Claude's JSON shape; the lifecycle intents in
this plan are the contract.

### Codex agent — port challenge before extraction

The Codex agent owns **Phase 2B**. It challenges the proposed ports against the
current official Codex lifecycle shape without installing an adapter or
creating project `.codex/` state. Every constraint that changes the port must
survive as a committed contract test or evidence record; a throwaway renderer
may be discarded, but its architectural consequence may not disappear with
it. The Codex agent returns the accepted constraints to Claude and stops while
Claude completes Phase 2C.

### Hard stop — final Codex acceptance before any Codex build

No Phase 3–5 work may begin until the Codex agent independently
accepts the complete Phase A/0–2 handoff. Acceptance requires all of the
following:

1. Phase A is complete: canonical framework prose addresses the reasoning
   agent generically while preserving real Claude-specific harness facts.
2. Claude golden fixtures remain byte-identical and the existing Claude suite
   passes.
3. Vendor-neutral lifecycle, scaffold, diagnostic, and runtime modules contain
   no Claude config paths, environment variables, permission structures, or
   vendor event-schema assumptions. A mechanical architecture test enforces
   the allowed boundary: Claude vocabulary may appear only in the Claude
   adapter, its fixtures/tests, and explicitly vendor-specific documentation.
4. The Codex agent can explain and implement the ports without importing,
   calling, subclassing, or parsing the Claude adapter.
5. Framework-root and directly opened nested-domain runtime/commit probes pass
   in the Codex managed shell, or any failure is routed back as shared-runtime
   work rather than patched inside the future Codex adapter.
6. The Codex review finds no least-common-denominator abstraction or hidden
   Claude ordering assumption in the application contract. **[v1.3]** The
   Codex-owned Phase 2B challenge moves most of this risk into design without
   asking Claude to model the other vendor. This final condition is a
   confirmation that the accepted constraints survived the extraction.

A failed condition returns the work to the Claude extraction package (or the
shared runtime slice). It must never be bypassed with a Codex-side workaround.

### Codex agent — historical diagnostic and Codex work package (through v1.8)

After accepting the original final handoff, the Codex agent owned **Phases
3–5**:

- build the vendor-neutral diagnostic against the accepted ports;
- implement the Codex adapter independently from official Codex contracts;
- add explicit adapter install and scaffold selection;
- preserve every Claude golden and merge-safety test while changing shared
  orchestration surfaces;
- commit the completed work package and stop before rollout.

The Codex agent may change shared interfaces only when Codex evidence exposes
a real missing abstraction. Such a change reopens the Claude regression gate;
it is not permission to edit Claude output for convenience.

### v1.9 corrective ownership — Phase 5R

The live gate supersedes the historical “only” boundaries for the named repair
packages, without broadening either agent into the other's vendor surface:

| Package | Implementing owner | Required independent acceptance |
|---|---|---|
| 5R.0 failing probes and launch-seam prototype | Codex/shared | Claude reruns the same committed red PowerShell 5.1 reproduction and reviews the documented shell/exec matrix |
| 5R.1 neutral launch, runner injection, diagnostics | Codex/shared | Claude reruns that unchanged reproduction green plus its regression suite on the handoff commit |
| 5R.2 Claude projection, output envelope, legacy definitions | Claude | Codex reviews inward ports, cwd stability, and ownership |
| 5R.3 generic refresh service | Codex/shared | Claude owns exact Claude legacy forms; both review byte preservation |
| 5R.4 Codex rerender and test-state disposition | Codex | operator selects root ownership; Claude suite remains green |

Neither implementation owner may self-certify the other harness. The operator
alone authorises root writes, project trust, domain migration, default changes,
and publication.

### Shared verification and operator ownership

- In Phase 6, the Claude Code agent owns the live Claude execution record and
  the Codex agent owns the live Codex execution record. Neither agent can
  self-certify the other harness.
- In Phase 7, the Codex agent leads reconciliation after both execution records
  pass; the Claude Code agent reviews Claude-facing instructions and fixtures.
- Phase 8 belongs to the operator. Harness defaults, estate migration, and
  publication are product decisions, not adapter-agent decisions.

## Phased plan

### Phase A — Sweep vendor address out of framework prose **[v1.3]** (owner: Claude Code agent)

Implementation-independent from every other phase: it touches no adapter, no
port, and no tool control flow, so it may run alongside Phases 0–1. It is still
a final handoff requirement; it cannot be left until after Codex development.
It is the only slice here that changes the substrate's address rather than its
outer edge.

- [x] Replace "Claude" with the settled agent-neutral term wherever framework
  prose means *the reasoning agent*: the Tier-1 `thing.md` specification, the
  Tier-2 `scalability-guide.md`, and the worked example skills under
  `examples/life-manager/`. Preserve every mention that names Claude Code as a
  *specific harness* with a real vendor fact attached; those are true
  statements, not leakage. Generate the execution list with search; do not
  maintain an occurrence count in prose.
- [x] Settle one term first and use it everywhere. The specs already alternate
  between "the agent", "Claude", and passive voice; the sweep is worthless if
  it installs a third variant.
- [x] Regenerate `kernel.md` and confirm the operative blocks are unchanged in
  meaning. The generated kernel is already vendor-clean, which bounds the blast
  radius: if a kernel block changes, the sweep has edited rules, not address.
- [x] Leave `templates/` alone — verified clean, so scaffolded domains are not
  inheriting the vocabulary and no estate migration is implied.

**Gate:** validate and the full suite pass; `kernel.md` regenerates with no
semantic diff; no domain repo requires any change.

**Why it is first-class rather than a Phase 7 docs chore:** every other phase
in this plan makes the *outer edge* vendor-neutral while the canonical inner
specs still address one vendor by name. That is the coupling a Codex operator
meets in the first minute, before any adapter exists to fail.

### Phase 0 — Freeze the contract and evidence (owner: Claude Code agent)

- [x] Record golden Claude scaffold artifacts and current CLI behaviour.
- [x] Add estate-shape fixtures: hooks-only config, permissions-only config,
  permissions-plus-hooks, no settings, and a locally extended startup command.
- [x] Define the minimal lifecycle intents in tests before creating adapter
  classes. **[v1.2] The diagnostic dimensions move to Phase 3** — freezing a
  five-dimension vocabulary here would commit the only agent who never builds
  its consumer to a contract the consumer must live inside. Phase 0 freezes
  what exists and is about to move: Claude's bytes and behaviour.
- [x] Record the current Claude adapter/schema evidence and a Claude live-test
  checklist; do not encode undocumented assumptions. Codex contract evidence
  belongs to the Codex-owned Phase 2B.

**Gate:** the baseline suite passes without changing a generated byte.

### Phase 1 — Repair the shared runtime port (implementer: Claude Code agent; acceptance: Codex agent)

- [x] Give root and nested-domain launchers one runtime-resolution service.
  Resolve both the domain-local environment and the framework-root environment
  derived from the CLI path. **[v1.5 acceptance reopening:]** the implementation
  exists, but its emitted POSIX resolver cannot derive the framework root in
  the Codex managed Git-hook shell because `dirname` is unavailable.
- [x] Keep PowerShell and POSIX entry paths behaviourally equivalent; avoid
  absolute installation paths and vendor cache paths.
- [x] Make `install-hook` execution-test the emitted pre-commit hook where Git
  supports it. Return/test a vendor-neutral runtime probe result that
  distinguishes interpreter-found, dependency-loaded, and command-executed;
  preserve the current doctor presentation until Phase 3 settles the
  user-facing diagnostic vocabulary. **[v1.5:]** execution-testing exists, but
  runtime-probe still lacks the command-executed fact.
- [x] **[v1.2]** Fix the resolution defect in the *emitted hook body*, not only
  in doctor's report: add the framework-root environment (derived from the
  `$MDLLM` path, which is the only place that knows where the framework is) to
  the candidate list, and strengthen the candidate probe from `import sys` to
  one that proves the dependency actually loads. A hook that selects an
  interpreter which cannot import PyYAML blocks the commit while reporting a
  cause that is not the cause.
- [x] Add a reproducible directly-opened nested-domain runtime/commit probe.
  The Codex agent executes it in the managed shell during Phase 2B and again
  at final acceptance; Claude does not self-certify that environment. **[v1.5:]
  the probe now reproduces the shared resolver failure; its existence is
  complete, its acceptance result is not.**

**Gate [v1.4]:** in the Claude-side environment, the framework and a nested
domain both execute validation and a real pre-commit through the same
checked-in resolution policy, including on an interpreter that resolves but
lacks the dependency. The identical probe run in the Codex managed shell is
2B/acceptance evidence, not a Phase 1 closure condition. Runtime facts are
available to Phase 3 without Phase 1 freezing their presentation vocabulary.

**Final Codex acceptance [v1.6]:** the implementation passes the real root,
directly-opened domain, fresh nested-hook, and masked-PATH probes. The remaining
acceptance defect is the fixture rather than the resolver:

- [x] **Claude return item:** make
  `test_probe_reports_command_executed_as_its_own_fact` supply a controlled
  floor-capable candidate after moving the entry, rather than assuming the
  target harness PATH contains Python with PyYAML. Pin dependency probing on
  every PowerShell candidate branch in the same correction.

### Phase 2 — Cross-harness port design, then Claude extraction **[v1.3]**

#### Phase 2A — Draft the ports without moving Claude (owner: Claude Code agent)

- [x] Introduce the smallest draft port types needed by the lifecycle intents,
  but leave the live scaffold and doctor Claude paths in place.
- [x] Express current Claude rendering and inspection expectations as golden
  and read-only contract tests, not as generic port assumptions.
- [x] Commit the draft and pause. Do not create or model Codex artifacts.

**Gate:** the proposed ports compile/test against the frozen Claude evidence,
but no production Claude path has moved.

#### Phase 2B — Challenge the port shape (owner: Codex agent)

- [x] Test the draft against current official Codex lifecycle semantics with a
  non-installed probe or temporary renderer; create no project `.codex/`
  state and do not ship an adapter.
- [x] Record the official Codex hook documentation date and the live-harness
  checklist used by the challenge; do not encode undocumented assumptions.
- [x] Return only constraints evidenced by the second vendor shape. Each
  constraint that changes a port survives as a committed contract test or
  evidence record; discard incidental spike code.
- [x] Stop and return the accepted port contract to the Claude Code agent.

**Gate:** the port can express both vendor shapes without importing either
adapter schema into the application contract.

**Outcome [v1.5]:** passed. The accepted constraints and official evidence are
in `evidence/codex-port-challenge-2026-08-11.md`. This does not pass the
reopened Phase 1 gate or the final A/0–2 handoff gate.

#### Phase 2C — Extract Claude without changing Claude (owner: Claude Code agent)

- [x] Finalise the accepted adapter ports, introduce the registry, and move the
  inline Claude scaffold projection behind a Claude adapter using the Phase
  2B constraints.
- [x] Make scaffold call the registry while preserving its current default and
  exact Claude output for backward compatibility.
- [x] Move doctor’s Claude parsing into the inspect port and report extensions
  rather than flattening them.
- [x] Keep inspection read-only: identify the managed hook fragment and local
  extensions without routing an existing composite settings document through
  the new-project renderer. Phase 5 owns mutation and merge.
- [x] Keep `.claude/commands` as a separate deliberate-shortcut projection;
  do not conflate it with lifecycle hooks.

**Gate:** golden files are byte-identical, all existing tests pass, and an
existing composite Claude settings file is inspected without mutation or
normalisation. The Claude agent then stops; the final cross-harness handoff
gate above must pass before Phase 3.

**Final Codex acceptance [v1.7]: passed. The v1.6 return items were committed
by Claude and the final Codex semantic probe corrections are recorded above:**

- [x] Declare every service-facing dependency as a narrow port (including
  shortcut projection and scaffold presentation), and make doctor consume a
  neutral diagnostic contract instead of a vendor-owned `doctor_line`; do not
  make Codex imitate undocumented Claude methods.
- [x] Strengthen architecture fitness with a minimal registered adapter that
  implements only the declared contracts and is exercised through both
  scaffold and doctor.
- [x] Correct Claude inspection so token-prefix mutations, extra commands in a
  managed group, duplicate matching groups, and operator-only hook events are
  reported respectively as stale/extended/ambiguous/managed-fragment-absent,
  never current.
- [x] Add the four currency/discovery regression cases and rerun the byte
  golden, composite read-only, architecture, focused handoff, and full suites.

### Phase 3 — Build truthful harness diagnostics (owner: Codex agent)

- [x] Add `doctor --harness` capability reports with the six independent
  dimensions above. **[v1.2]** This phase now *settles* that vocabulary as well
  as consuming it — the dimension table above is the design intent, and Phase 3
  owns the final names and value sets because it is the first code that has to
  be honest in them.
- [x] Derive managed-fragment currency from the same adapter renderer used to
  create it; compare semantically where formatting is operator-owned.
- [x] Add execution attestations/probes without claiming that a static probe
  fired a real session event.
- [x] Report remediation commands and ownership boundaries; never auto-fix.

**Gate:** fixtures prove that present-but-invalid, present-but-untrusted,
runnable-but-untested, extended, and verified cannot be conflated.

**Outcome [v1.8]: passed.** The diagnostic tests exercise each independent
state, hash-bound current and stale attestations, provenance, and unknown trust.

### Phase 4 — Add the Codex adapter (owner: Codex agent)

- [x] Render a project `.codex/hooks.json` with one sequential SessionStart
  handler, file-edit PostToolUse validation, stable root resolution, bounded
  output, and Windows/POSIX commands.
- [x] Inspect config, project trust, hook-review state where observable, runtime
  resolution, and managed-fragment currency. Report `unknown` where Codex does
  not expose a stable machine-readable fact.
- [x] Exclude `.codex` from thing-corpus scanning just as `.claude` is excluded.
- [x] Add schema, rendering, merge, cwd/subdirectory, compaction-source, output
  limit, and failure-path tests.

**Gate:** adapter unit/integration tests pass without touching Claude fixtures.

**Outcome [v1.8]: passed.** The official-contract shape is implemented and
tested without installing a live project layer; Phase 6 alone can promote it
from designed-for to verified-on.

### Phase 5 — Expose explicit install and scaffold selection (owner: Codex agent)

- [x] Add an explicit human-invoked adapter install/refresh command that shows
  the owned diff and refuses ambiguous merges.
- [x] **[v1.2]** Land the merge tests deferred from the Claude non-regression
  boundary: existing `permissions` survive byte-for-byte, a locally extended
  SessionStart command is untouched, and an ambiguous fragment produces a diff
  and a refusal. Both surviving cases exist in the live estate; the refusal
  case needs a fixture. These belong here because this command is the first
  code that can merge anything.
- [x] Add repeatable scaffold selection such as `--harness claude`,
  `--harness codex`, `--harness all`, and `--harness none` while preserving the
  no-flag behaviour during this compatibility release.
- [x] Keep AGENTS.md, skills, prompts, schema, and Git hooks identical across
  harness selections; only outer projections vary.
- [x] Do not decide a new default as part of the refactor. A default change is
  a versioned product decision after live evidence, not architecture cleanup.

**Gate:** two scaffolds selected for different harnesses differ only in their
outer adapter artifacts and both validate cleanly.

**Outcome [v1.8]: passed.** No-flag scaffolding remains byte-compatible with
Claude, while `claude`, `codex`, `all`, and `none` vary only their outer
projections; composite installation is lossless or safely refused.

### Phase 5R — Reopen runtime, ordering, and refresh before live acceptance **[v1.9]**

This is a corrective gate, not a rollback of the neutral lifecycle contract.
Phases 3–5 supplied the right separation and exposed the defects honestly; the
live probes now provide the evidence needed to finish the launch and migration
ports. Phase 6 is blocked until every 5R gate below passes.

Execution is deliberately serial at the gates even where coding can be
parallel: freeze the failing probes → select the launch seam → repair shared
runtime/runner → version the Claude projection → add recognised-legacy refresh
→ rerender Codex → run the complete deterministic matrix → enter live harness
tests. No root projection is refreshed while its recogniser or new renderer is
still changing.

#### Phase 5R.0 — Freeze the failures and choose the launch seam (Codex owner; Claude review)

- [x] Add deterministic reproductions for a PATH candidate which exists,
  writes to stderr, and exits non-zero under Windows PowerShell 5.1. Exercise
  both the Codex `commandWindows` path and `tools/mdllm.ps1`; do not depend on
  whether the host happens to expose a Microsoft Store alias.
- [x] Author that PowerShell 5.1 reproduction once as an environment-independent
  committed fixture. Codex records old-red under native `powershell.exe` 5.1;
  before Gate 5R.0, Claude reruns the exact fixture unchanged and records
  `$PSVersionTable.PSVersion`, repository commit, command, and red result.
  PowerShell 7 compatibility mode and a Codex-only invocation are not substitutes.
- [x] Pin the current Claude contract fact that matching handlers run in
  parallel. Replace every production comment/test assertion that a matcher
  group's handler array is sequential with an assertion over **one handler**
  and the neutral runner's ordered steps.
- [x] Pin Claude's documented execution forms before choosing syntax: shell-free
  `command` + `args`; default shell form on POSIX; Windows Git Bash plus its
  PowerShell fallback; and explicit `shell: powershell` with `pwsh` plus native
  PowerShell 5.1 fallback. Use an inert handler to record executable/version,
  argv boundaries, cwd, `${CLAUDE_PROJECT_DIR}`, stdin receipt, source, exit
  status, timestamps, config hash, and the Claude debug transcript. Include
  project/framework paths containing spaces. The selected portable form must be
  executed by real Claude Code on every supported platform/dialect it claims.
- [x] Prototype the neutral launch seam before freezing a new port. It must run
  the same `harness-event <harness> <moment> <root> <definition-hash>` intent
  from a repository subdirectory on POSIX, PowerShell 7, and Windows
  PowerShell 5.1; use no absolute installation path, user-global config, PATH
  Python assumption, or vendor cache path.
- [x] Decide the smallest mechanism from execution evidence. Preferred order:
  an immutable shared launch specification consumed by both adapters; a
  clone-local Git dispatcher only if its invocation works on the supported Git
  floor without hijacking a native hook event or overwriting operator config.
  A custom `git hook run` name is not assumed portable—older supported Git
  versions reject unknown event names.

**5R.0 execution record (Codex, in progress):** commit `8123812` owns the
single shared `stderr-python.cmd` / `floor-python.cmd` fixture and exercises it
through both entry paths. On native Windows PowerShell `5.1.26100.9168` at
pre-fix commit `ba49102`, the exact focused pytest command recorded two expected
failures: `tools/mdllm.ps1` terminated at the first stderr-writing `python`
probe with `NativeCommandError`, and Codex `commandWindows` surfaced the outer
“no floor-capable Python” fallback instead of continuing to its framework
runner. Commit `f64480c` withdraws the false sequential-handler claim while
retaining legacy bytes as migration data; its contract/port suite is 28/28.
Claude's unchanged native-PS5 rerun, real-dispatch shell matrix, and launch-seam
selection remain open, so Gate 5R.0 has not passed and Phase 5R.1 has not begun.

**Claude acceptance return (`a47e897`, 2026-08-12):** Claude reran the exact
committed fixture at `214967a` under native PowerShell `5.1.26100.9168` and
recorded the same two intended failures. Real Claude Code CLI `2.1.173`
dispatch on Windows then proved the default shell form enters Git Bash,
preserves a spaced `${CLAUDE_PROJECT_DIR}` and quoted argument boundary,
receives the lifecycle JSON on stdin, and launches two matching handlers in
parallel—the second-declared handler started first. Transcript attachments and
probe output share the harness session id. This closes the independent-red and
parallel-contract items. POSIX dispatch, exec-form `args`, and the Windows
no-Git-Bash PowerShell fallback remain explicitly unobserved; the execution-form
matrix and launch-seam items therefore remain open.

**Gate 5R.0 — accepted 2026-08-13:** the failing probes failed on the old
implementation in both agents' native PowerShell 5.1 records. Real Claude Code
dispatch pinned shell and exec semantics, proved matching handlers parallel,
and selected sh shell form as the only carrier capable of relative interpreter
discovery plus one lifecycle invocation. Decision
`claude-platform-surface-narrowed` scopes `verified-on` to Windows with Git for
Windows; POSIX consumes the same sh form as `designed-for` until the committed
cross-platform probe earns promotion, and the no-Bash PowerShell fallback is
outside the claim. The chosen inward mechanism is one immutable, vendor-neutral
launch specification with edge-specific encodings; it contains no Claude or
Codex schema vocabulary. Phase 5R.1 may begin.

#### Phase 5R.1 — Repair shared launch/runtime infrastructure (Codex owner)

- [x] Make every PowerShell candidate probe exception-safe: a failed native
  process is one negative candidate fact and resolution continues. Preserve
  `$ErrorActionPreference = 'Stop'` around real control-flow errors.
- [x] Put candidate order, PyYAML probing, framework-root derivation, and the
  lifecycle CLI invocation behind one neutral owner. Cross-language fragments
  may have different encodings, but parity tests must prove the same candidate
  order and outcome semantics. Represent each candidate as executable plus
  immutable prefix arguments so `py -3` is not a string-shaped special case.
- [x] Make the lifecycle application service receive the selected identity and
  `LifecycleOutputPort` from the CLI composition root. The neutral service may
  depend on the port; it must not resolve or import a concrete adapter itself.
- [x] Preserve one total lifecycle deadline, bounded labelled output,
  surface-and-continue behavior, and format-before-success-attestation.
- [x] Render an explicit **120-second handler timeout** in Claude and Codex;
  never inherit a vendor default. Enforce this hierarchy as policy and include
  every value in the managed-definition hash:

  ```text
  launch resolution             <= 10s
  neutral lifecycle application <= 105s
  format / evidence / exit       >= 5s
                                  -----
                                  <= 120s

  SessionStart application: estate-sync <= 75s; session-start <= 25s;
                            runner overhead <= 5s
  PostToolUse application:  validate <= 100s; runner overhead <= 5s
  ```

  An earlier step cannot borrow a later required step's allocation. A timed-out
  or degraded `estate-sync` must still leave the reserved orientation budget.
- [x] Give `estate-sync` a 75-second global deadline in addition to its per-Git
  call ceiling. Clamp each child call to the remaining global budget; after
  exhaustion, continue the estate walk from cached/local state and label every
  unattempted remote honestly as budget-exhausted. Do not pull after a degraded
  fetch, and leave no child Git/interpreter process behind.
- [x] Extend doctor with independent launch currency/runtime facts. A current
  vendor artifact with absent or stale launch infrastructure is configured but
  not runnable; static launch success still leaves execution untested.
- [x] Keep Git pre-commit as the only enforcement boundary. A harness launch
  failure must be visible but must not become a second commit policy.

**Gate 5R.1:** focused runtime, lifecycle-runner, diagnostic, architecture, and
Git-hook tests pass on POSIX, PowerShell 7, and Windows PowerShell 5.1. A
port-only fake can traverse the real command path without importing a vendor.
The installed Git hook is also exercised through Windows Git's shell; a native
shell emulation does not stand in for that boundary. Tests prove the timeout
arithmetic, later-step reservation, global estate deadline, healthy and stalled
remote paths, hash invalidation, and child-process cleanup. Claude then reruns
the exact committed PowerShell 5.1 reproduction green plus its regression suite
on the handoff commit; only then may 5R.2 begin.

**5R.1 implementation handoff (Codex, `82f2cfc`):** `27b0723` centralised
executable-plus-prefix candidates and turned the independently accepted native
PS5 reds green. Shared lifecycle/estate/diagnostic changes landed concurrently
with Claude's POSIX evidence at `6572fb7`: the code keeps the selected output
port at the composition root, hashes the 120/105/5 and 75/25/100 budgets,
reserves later steps, bounds the estate walk globally, and reports independent
launch facts. `59d023b` excludes Windows interop candidates from native POSIX.
`82f2cfc` gives `mdllm.ps1` and Codex one shared Windows resolver with a total
10-second stopwatch and timed-out-probe termination; the sh encoding enforces
the same ceiling through the verified Git-Bash/POSIX timeout surface. Windows
Git-hook execution is covered. Codex's complete Windows suite is 442/442;
validation is 174+6+14 clean and coherence has only the pre-existing
`claude-adapter-baseline` stable-label Info.

**Gate 5R.1 — accepted 2026-08-13** (`claude-gate-5r1-acceptance-2026-08-13`,
at handoff commit `72744f4`): the two independently accepted red fixtures run
green unchanged; the complete suite passes on Windows (442) and on native
Linux (439 + 3 honest Windows-host skips); the installed Git hook exits 0
through Windows Git's real `sh.exe` rather than a PowerShell emulation of it;
and vendor schema vocabulary appears only inside the two adapters, with
`dispatch_lifecycle_event` receiving its output port by injection and adapter
resolution confined to the CLI composition root. The WSL-interop defect
reported in `posix-floor-record-2026-08-13` is closed — Windows-only tests now
skip on host identity rather than executable presence, so a Linux run can no
longer launch Windows PowerShell across the boundary and report it as POSIX
evidence. No neutral port was altered and no missing abstraction was found, so
nothing returns to Codex. Claude-owned Phase 5R.2 may begin. Carried forward
unchanged: live Claude runs require a re-authenticated Claude Code CLI, and a
POSIX live-dispatch record additionally requires natively installed Node and
Claude Code inside the Linux host, so the narrowed surface in
`claude-platform-surface-narrowed` still stands.

#### Phase 5R.2 — Version the Claude projection (Claude owner; Codex acceptance)

- [x] Implement `LifecycleOutputPort` for Claude Code. SessionStart returns
  concise model context; successful PostToolUse is quiet; failed PostToolUse
  uses Claude's documented feedback/error behavior without enforcing the tool
  action.
- [x] Render one SessionStart handler and one PostToolUse handler. Each invokes
  the neutral lifecycle service once with a definition hash derived from the
  full binding, launch definition, and owned vendor fields.
- [x] Anchor the launch to Claude's documented project-root surface and prove
  it after the session cwd moves. Do not retain `python ../../tools/mdllm.py`
  or copy the framework root's PowerShell-only workaround into the portable
  renderer.
- [x] Inspect Claude's real project approval/trust behavior and report it as an
  independent fact. Do not preserve `trust=not-applicable` merely because the
  first adapter did not model the surface.
- [x] Keep `LIFECYCLE_BINDINGS`, domain policy, matcher intent, scaffold default,
  shortcuts, and Git-floor behavior unchanged. Only the projection mechanism
  changes.
- [x] Preserve the v1.8 Claude golden as `legacy-v1`; add a separately named
  current golden. Update the inspector so `current`, `known-legacy`,
  `extended`, and `ambiguous` are distinguishable without treating legacy as
  current.
- [x] Prove renderer acceptance without claiming automatic harness dispatch: a
  fresh Claude scaffold matches the current golden, inspects `current`, and has
  exactly one managed handler per lifecycle moment. Execute each emitted handler
  directly from a moved cwd on native Windows and POSIX; prove ordered steps,
  output translation, bounded advisory failure, definition-hash invalidation,
  and attestation mechanics.
- [x] Label every direct handler or `harness-event` execution as a **launch
  probe**. Any resulting clone-local attestation is test state and inadmissible
  as Phase 6 evidence. Do not promote any compatibility surface to
  `verified-on` during 5R.2.
- [x] If Claude discovers a missing neutral abstraction while implementing its
  projection, return it to 5R.1 under Codex/shared ownership. Claude does not
  alter neutral ports opportunistically inside the vendor package.

**Gate 5R.2:** Claude supplies the implementation and deterministic/native-shell
renderer record; Codex independently accepts the neutral boundary, cwd
stability, byte ownership, and tests. The result is a release-candidate,
`designed-for` renderer—not a verified harness.

**Accepted 2026-08-13 at `a1bccee`.** Codex cold-read the renderer, inspector,
goldens, output port, evidence record, and operator decisions, then exercised
the actual scaffold/doctor/install seams (61 focused tests passed). The current
projection enters the neutral runner once per moment, carries no private
candidate policy, and keeps Claude schema and output envelopes at the edge.
`ManagedFragment.legacy_id` is accepted as recognition data with a strict
non-current invariant; it grants no mutation authority. A broad CLI test first
failed only because an in-repository pytest temporary root inherited the
framework's real stale-floor finding; the exact test passed from an external
temporary root, confirming fixture location rather than 5R.2 behavior. Gate
5R.2 is green and Phase 5R.3 may begin.

#### Phase 5R.3 — Add explicit recognised-legacy migration (Codex service owner; Claude definitions owner)

The migration state machine is closed and ordered:

| Observed state | Default install | Explicit refresh | Ownership result |
|---|---|---|---|
| artifact absent | create after reviewed diff | same | adapter owns the new managed fragment |
| managed fragment current | no-op | no-op | formatting and admitted extensions remain untouched |
| exact adapter-declared legacy fragment | report migration available; write nothing | replace only the owned byte span after reviewed diff | permissions and unrelated settings byte-identical |
| current fragment with admitted local extension | no-op | no-op unless a separate extension-aware migration is designed | operator extension wins |
| legacy fragment with any local extension | refuse | refuse | no inference over mixed ownership |
| unknown stale, duplicate, malformed, unreadable, or ambiguous | refuse | refuse | operator resolves the ambiguity |

- [x] Add an optional narrow legacy-definition port carrying immutable IDs and
  exact semantic forms. It supplies recognition data, never filesystem writes.
- [x] Extend the generic mutation service with an explicit refresh action/flag.
  The service owns JSON span replacement, unified diff, all-target preflight,
  concurrent-state recheck, atomic apply, and rollback.
- [x] Recognise the old standard two-handler scaffold form and the exact tracked
  framework-root combined PowerShell form separately. Do not generalise from
  resemblance. The live `--assistant` extension remains a mandatory refusal.
- [x] Test permissions-only insertion, permissions-plus-known-legacy refresh,
  root permissions preservation, unrelated hook groups, formatting, duplicate
  keys, malformed JSON, unknown commands, local extensions, all-selected
  atomicity, and concurrent mutation.
- [x] Inspect project-local `.claude/settings.local.json` as a read-only
  effective-configuration source. Never mutate it. A competing hook definition
  in that overlay makes inspection and refresh ambiguous and therefore refuses
  with zero writes.
- [x] Keep every existing domain opt-in. Doctor may show the recognised legacy
  ID and exact refresh command; no refresh runs during framework upgrade,
  doctor, scaffold, session start, or estate sync.

**Gate 5R.3:** old/current golden fixtures and every representative estate
shape have an explicit expected state; safe cases preserve all non-owned bytes,
and every ambiguous case proves zero writes by hash.

**Codex implementation handoff — 2026-08-13 at `460bb5a`.** The application boundary now
defines immutable `LegacyDefinition` data plus the optional
`LegacyDefinitionPort`; ordinary install remains unchanged and conservative,
while `--refresh-legacy` separately authorises only an inspection-named exact
form. `TopLevelJsonFragmentPolicy` rechecks the declared legacy semantics and
replaces only the `hooks` value span with renderer-owned bytes inside the
existing all-target atomic transaction. Claude declares `legacy-v1` and the
root-only `legacy-root-powershell-v1`; the live `--assistant` tail withholds an
ID. `.claude/settings.local.json` is read-only and competing hooks make the
whole operation ambiguous. The full suite passes 452 tests. A live read-only
estate pass classified the root as the root-specific legacy, nine domains as
standard legacy, one as extended/refused, one permissions-only artifact as no
managed fragment, and two absent primary artifacts; no estate configuration
was written. Evidence: `codex-5r3-migration-acceptance-2026-08-13`. Phase 5R.3
remains at its cross-harness acceptance boundary until Claude cold-runs the
matrix against the implementation commit.

#### Phase 5R.4 — Reconcile Codex projection and live test state (Codex owner)

- [x] Make the Codex renderer consume the same neutral launch definition rather
  than retaining a private Windows candidate policy. Preserve Codex-specific
  POSIX/Windows fields, matchers, time/context limits, trust boundary, and JSON
  feedback envelope.
- [x] Rerender the framework root's untracked `.codex/hooks.json` only through
  reviewed `adapter-install --dry-run` and explicit apply after all earlier 5R
  gates pass. An old definition hash must invalidate any old attestation.
- [x] Present the operator with the ownership decision: track the corrected
  root project projection as self-hosted framework state (recommended), ignore
  it deliberately as clone-local state, or remove it. Do not leave it
  untracked and undocumented.
- [x] Rerun the complete scaffold matrix (`default`, `claude`, `codex`, `all`,
  `none`) and prove that only adapter projection files differ.
- [x] Recheck the Codex trust contract against the exact product surface used
  for the live test. Official documentation currently assigns hook inspection
  and trust to `/hooks` in the CLI; the Desktop chat command palette observed
  on 2026-08-12 did not expose that command. Do not claim Desktop trust review
  from a CLI-only flow or from config presence.
- [x] If any commit after Claude's 5R.1 acceptance changes launch, runtime, or
  lifecycle-runner code, Claude reruns the exact PowerShell 5.1 reproduction on
  final 5R.4 HEAD. A final-HEAD run may satisfy both gates only when no
  intervening relevant change occurred.

**Gate 5R.4 — mechanism accepted; 5R.5 holds release:** the full suite passes in both the
Codex managed shell and Claude's shell; validation and coherence are clean;
the current plan, README status, operator guide, Claude baseline erratum, and
first-hour guide, archived domain-kernel plan erratum, adapter example, scaffold
guidance golden, session module commentary, and architecture tests describe the
same current/legacy boundary. Production comments and tests no longer encode
the false sequential-handler premise. No domain has been migrated.

**5R.4 disposition — accepted mechanism, execution defect returned
(`db4a5dd`):** Claude independently accepted the atomic reconciliation,
operator-byte preservation, evidence invalidation, tracked Codex state,
scaffold matrix, and clean nested estate. A real automatic root SessionStart
then measured `estate-sync` at 59.8 seconds and `session-start` at 36.1 seconds.
The runner gave orientation a hard 25-second ceiling, returned
`session-start=124`, and quietly omitted version, velocity, open loops, and
triggers. This does not reopen adapter ownership or 5R.4 migration safety; it
returns the inward allocation policy accepted at 5R.1.

#### Phase 5R.5 — Correct lifecycle budget allocation (Codex/shared owner;
Claude acceptance)

- [x] Replace guessed hard per-step ceilings with inward-owned protected
  allocations. Each step declares the minimum application time that preceding
  steps must leave for it; once current, it inherits unused earlier time.
- [x] Preserve the absolute 120/105/5 hierarchy. `estate-sync` still cannot
  consume orientation's protected 25 seconds, and orientation may use the
  remaining balance without exceeding the total application deadline.
- [x] Reject empty bindings, non-positive protected allocations, and protected
  totals larger than the application budget before any subprocess executes.
- [x] Include the renamed allocation semantics in both adapters' managed
  definition hashes. Prior fixed-step artifacts and attestations must become
  stale rather than being certified under changed behavior.
- [x] Freeze the exact 5R.4 root projections as separately named recognition
  data, review one atomic `--refresh-legacy` diff, and refresh both tracked root
  artifacts without changing Claude permissions or unrelated Codex bytes.
- [x] Run focused port, runner, adapter, migration, diagnostic, scaffold, and
  architecture tests plus the complete suite; validate and coherence remain
  clean.
- [x] Claude reruns the exact native PowerShell 5.1 reproduction because the
  neutral lifecycle runner changed, then opens a real automatic root session.
  Acceptance asserts `estate-sync=0` and `session-start=0`, the emitted
  orientation content (version, velocity, open loops, and triggers), and the
  fresh session-gate attestation side effect. Exit zero or a harness execution
  attestation alone is insufficient.

**Gate 5R.5 / release into Phase 6:** Codex supplies the neutral implementation,
immutable pre-repair recognition inputs, atomic root refresh, and deterministic
test record. Claude independently accepts the final commit with the unchanged
PowerShell fixture, full suite, and real root-dispatch side effects. The
corrected projection remains `designed-for` until Phase 6 records the complete
versioned/correlated harness evidence.

**Gate 5R.5 — accepted 2026-08-13 at `ea4ea12`:** Claude Code CLI 2.1.229 on
Windows 11 reran the unchanged native PowerShell 5.1 fixtures green and fired
a real automatic root SessionStart. Both steps returned zero; version,
velocity, open loops, and triggers were emitted; the clone-local session-gate
attestation refreshed; and the correlated harness attestation reported
`definition_current=true`. Evidence:
`claude-gate-5r5-acceptance-2026-08-13`. Phase 6 is released.

**5R.5 implementation handoff (Codex, 2026-08-13):** the inward contract now
names `protected_seconds`, the runner forwards unused earlier budget while
preserving every later allocation, and both adapter hashes carry the semantic
change. Exact pre-repair root projections are immutable recognition inputs;
the reviewed all-selected refresh changed only definition-hash literals and
left Claude permissions/operator bytes intact. Focused gate: 173/173. Complete
external-basetemp suite: 465/465. Evidence:
`lifecycle-budget-allocation-acceptance-2026-08-13`. No nested domain was
migrated. Claude's PowerShell 5.1 and automatic-root side-effect acceptance
remain deliberately unchecked.

### Phase 6R — Correct lifecycle output allocation (Codex/shared owner;
Claude acceptance)

The estate migration found a second resource boundary after the time-budget
correction: the runner bounds all model-visible lifecycle text to 2,200
characters by retaining one global tail. On large domains the hook succeeds
and attests, but version, velocity, and open loops disappear. Raising or
removing the bound is not portable because Codex has a separately declared
context envelope; reversing the slice merely trades triggers for the earlier
sections.

- [x] Add an inward-owned total output envelope and per-step protected
  character allocations, parallel to the accepted time-allocation contract.
  A preceding step may use unclaimed output capacity but cannot erase a later
  step's protected representation.
- [x] Compact within a step by neutral text structure, not by named domain
  fields or a hard-coded list of disposable content. Every structural section
  remains represented; omitted detail is explicit and the full operation stays
  available through its normal command.
- [x] Keep the model-visible output within the existing 2,200-character runner
  ceiling and the Codex adapter's separately declared 2,500-character context
  envelope. Preserve step attribution and failure labels even at tiny limits.
- [x] Include the complete output-allocation semantics in both managed
  definition hashes. Prior 5R.5 projections become exact recognised legacy
  inputs; prior attestations become stale rather than certifying changed
  behaviour.
- [x] Review one atomic root refresh and the selected estate refreshes through
  `--dry-run` before apply. Preserve operator-owned bytes, refuse extensions or
  ambiguity, and leave QMS or any changed tree untouched until its owner clears
  the discrepancy.
- [x] Add deterministic regressions using a report larger than the envelope.
  Assert the bounded result still represents estate state plus version,
  velocity, open loops, and triggers; do not accept exit zero or a generic
  attestation as a substitute.
- [x] Run focused architecture/port/runner/adapter/install/scaffold tests, the
  complete external-basetemp suite, validate, and coherence. Then obtain
  independent Claude acceptance of the same final commit and a real large-domain
  SessionStart side-effect record.
  **Accepted 2026-08-16** at `b82061f` —
  `evidence/claude-gate-6r-acceptance-2026-08-16.md`: focused 128, complete 465
  (external basetemp), validate 197 clean, coherence clean, `git diff --check`
  clean; a fresh automatic SessionStart on the largest migrated domain emitted
  2042/2200 characters carrying both step labels and return codes, estate state,
  Version, Velocity, Open loops and Triggers, with elision marked explicitly and
  `definition_current=true`, `execution=passed`; root and all 13 domains
  re-derived current/no-op with every artifact hashed byte-identical.

Codex implementation evidence through 2026-08-16: the focused boundary suite is
128 passed and the complete suite is 465 passed; the root and all 13 domains
were exact-legacy refreshed and re-preflight as current/no-op. Three untracked
operator-local Claude overlays remained byte-identical. The remaining part of
the final checkbox is the post-commit validation/coherence seal and independent
Claude automatic-dispatch acceptance; it is not inferred from deterministic
tests or direct runner execution.

**Gate 6R — ACCEPTED 2026-08-16.** Codex supplied the neutral implementation,
recognised-legacy migration inputs, reviewed refresh evidence, and
deterministic record. Claude independently accepted the final commit and
proved a real automatic large-domain session contains every orientation
section under the bound. **The remaining Phase 6 Codex source/nested runs are
released.**

### Phase 6 — Execute in real harnesses (split ownership by harness)

Phase 6 is active after accepted Gate 5R.5. The framework root carries tracked,
current Claude and Codex project projections. Their recognised legacy forms
were refreshed atomically at 5R.4; old hash-bound attestations are stale and do
not count as current execution evidence. At Phase 6 opening no nested domain
projection had been migrated; the later estate migration record moved all 13
domains to the one-handler projection before this post-6R Codex record.

Phase 6 is the only phase that earns `verified-on`. Unlike 5R.2's direct launch
probes, these runs must be automatically dispatched by the named product and
correlated with its own transcript/debug output. The records include exact
harness version, OS/platform, repository commit, project-config SHA-256, managed
definition hash, source event, timestamps, and observed outcome.

- [x] Claude non-regression: from the Phase 5R current renderer, scaffold, open,
  observe SessionStart ordering, make a valid edit, observe quiet PostToolUse,
  make a controlled invalid edit, observe advisory feedback, repair it, and
  commit through the floor.
- [ ] Claude framework root: only after an operator-approved recognised-legacy
  refresh, repeat the automatic lifecycle record at root. If the operator does
  not approve that refresh, record root as legacy/unverified and scope the
  Claude verified-on claim to the fresh scaffold; do not reuse the 5R.2 probe.
- [x] Codex Desktop framework-root observation: on Windows build
  `26.803.10989.0`, open a fresh task with the current tracked project layer and
  distinguish automatic dispatch from AGENTS interpretation. AGENTS was
  injected, but no SessionStart lifecycle context or Codex attestation appeared;
  doctor remained `execution=untested`. This is a surface-specific negative
  record, not a universal Desktop-support claim.
- [x] Codex CLI framework root: trust the project layer through the documented
  product-specific human flow, observe automatic generic SessionStart
  injection, make invalid/repaired edits, and commit this evidence through the
  floor. Source normalization is not stored, so this claims generic
  SessionStart only — not separate `resume`, `clear`, or `compact` coverage.
- [x] Codex CLI nested domain: open the domain as its own workspace and repeat
  automatic SessionStart, invalid/repaired PostToolUse, current-definition
  diagnostics, and the Git-floor probe.
- [x] In a disposable no-adapter repo, prove the Codex degradation path:
  AGENTS interpretation remains automatic, the interpretation-prescribed
  session start can establish the strict gate, a valid commit passes the Git
  floor, and an invalid commit is blocked.
- [ ] Repeat the disposable no-adapter proof in Claude Code. This remains
  Claude-owned; Codex does not self-certify another harness.
- [ ] Record exact harness/version/platform evidence and failures. A passing
  unit test earns designed-for; only these runs earn verified-on. Include the
  project configuration SHA-256 and repository commit for every record.
- [ ] For every live event, capture the harness-owned transcript/debug record
  and correlate its time window with the new hash-bound attestation. Directly
  running `harness-event` can mint the same record and is therefore a runtime
  probe, not proof that the harness dispatched it.
- [x] Assert every Codex contract-bearing side effect, not only command completion:
  SessionStart evidence includes the emitted orientation content and a fresh
  clone-local session-gate attestation; post-write evidence includes the
  expected validation result and envelope/silence behavior. Exit zero and a
  generic hook-success record do not establish these effects.
- [x] Either carry the normalized SessionStart source
  (`startup|resume|clear|compact`) into evidence, or narrow the claim to the
  generic SessionStart events actually distinguishable by the record. Never
  infer four verified triggers from one undifferentiated attestation.
- [x] Split Claude Code lifecycle evidence from VS Code Copilot compatibility.
  Shared `.claude/settings.json` bytes or shortcut projections do not make a
  live Claude run evidence for Copilot; report Copilot separately as untested
  until its own contract and execution record exist.

**Gate:** the corrected Claude lifecycle projection and Codex are verified on
the specifically tested surfaces, with no wider claim.

### Phase 7 — Reconcile every public surface (Codex lead; Claude review)

- [ ] Update orchestration, discovery, refresh, operator guide, first-hour,
  domain guide, README compatibility table, scaffold output, and adapter
  examples from the same settled capability vocabulary. **[v1.3]** Phase A has
  already swept the canonical prose-address surfaces; this phase must not
  re-open them for address, only for capability claims that the build changed.
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

- the corrected Claude lifecycle is verified, historical bytes remain explicit
  migration fixtures, and existing Claude project state was not silently
  changed;
- **[v1.2]** the canonical specs address *the agent*, not a vendor, so a Codex
  operator reading `thing.md` is not being spoken to as a Claude user;
- a new Codex-selected domain can be opened directly and run startup,
  post-write feedback, validation, and commit through a resolved runtime;
- the substrate and every domain remain usable with no harness adapter;
- doctor reports support, configuration, trust, runtime, execution, and
  currency without collapsing them;
- existing permission rules and local hook extensions survive or cause a safe
  refusal;
- runtime launch policy has one neutral owner and both adapters consume it;
- both renderers declare the same explicit handler envelope, every inner budget
  fits beneath it with later-step reservation, and degraded estate sync cannot
  suppress orientation or leave child processes behind;
- exact legacy forms are refreshable only through an explicit reviewed diff,
  while unknown stale or extended forms remain zero-write refusals;
- adding a third harness requires a new adapter, tests, and docs—not edits to
  domain policy, scaffold control flow, or doctor control flow;
- compatibility claims name the exact harness and evidence that earned them.
- Claude Code and VS Code Copilot lifecycle claims remain separate unless each
  has its own inspected contract and execution record;
- **[v1.3]** compatibility claims distinguish the vendor-neutral deterministic
  eval assertion path from the Claude-specific optional live-runner backend;
  live eval portability is either implemented or routed to its own owned plan
  before any claim expands from lifecycle portability to “all tooling”.

## Held outside this plan

- Repackaging MarkdownLLM domain skills as Codex-native skills or a Codex
  plugin. The domain files already are the portable program.
- Building a universal hook DSL. The minimal lifecycle intent is enough until
  another adapter proves a richer abstraction is felt.
- Automatically interpreting or resolving Codex trust. Trust is a human or
  managed-policy decision; diagnostics may observe and explain it only.
- Automating the semantic session-end continuity ritual. It remains a
  deliberate reasoning act, not a short cleanup hook.
- **[v1.3] Making the optional `mdllm eval --run` backend multi-vendor.** The
  default eval path checks assertions against domain state and is already
  vendor-neutral; README, the operator guide, and the domain guide correctly
  present it as a domain capability. Stage 2 (`--run`) is the coupled surface:
  it shells `claude -p` and needs a distinct runner/scoring design before
  results from another harness are comparable. That work remains outside this
  lifecycle-adapter plan, but it is not dismissed as development-only. Before
  Phase 8 closes, route it to a separate owned plan or explicitly bound the
  compatibility claim to substrate lifecycle and deterministic evals.
- Claiming Cursor, Windsurf, Gemini, Codex CLI, or any other surface verified
  because Claude or Codex desktop passed. Each claim needs its own execution
  evidence.
