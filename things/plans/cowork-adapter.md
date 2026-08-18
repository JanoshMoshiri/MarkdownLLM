---
id: cowork-adapter
type: plan
status: not-started
version: 1.0
created: 2026-08-18
priority: high
tags: [harness, adapters, cowork, bootstrap, discovery, contract-emission, publication, estate, clean-architecture]
linked_things:
  - id: vendor-harness-adapter-foundation
    relation: extends
    notes: "The third harness through the same ports. That plan's registry promise — 'adding a third harness requires a new adapter, tests, and docs, not another conditional' — gets its first exercise here, and the exercise stretches two port assumptions honestly: the render target is an account-level bundle, not a project file, and currency is evaluated at run time, when the bundle meets the framework it just cloned."
  - id: cowork-integrity-estate-sweep
    relation: extends
    notes: "Phase 10 kept the v0.4.0 plugin as 'the Cowork workspace-assembly layer; not the fail-safe'. This plan is the successor to that verdict: the assembly layer becomes a real adapter — rendered, versioned, currency-checked — while the session gate remains the fail-safe underneath it."
  - id: framework-discovery-specification
    relation: extends
    notes: "Adds the explicit bootstrap route — a harness with no entry-file discovery, where a plugin/skill is the discovery event — as a first-class route beside harness injection. The 2026-06-11 insight asked for exactly this; the operator confirmed it 2026-08-18."
  - id: agents-md-discovery-is-harness-dependent
    relation: implements
    notes: "That insight's open recommendation: 'the explicit bootstrap prompt should be specified in framework-discovery.md as a first-class discovery route, not an improvisation.' Phase 6 lands it."
  - id: a-layered-harness-is-a-co-author-not-a-substrate
    relation: implements
    notes: "The working mitigation that insight names — shrink what must win at the interpretation anchor, move everything that must hold to git-fs — is this plan's design rule. Contract emission and the publication guard move to the floor; the plugin's residue is transport."
  - id: a-consumers-defect-report-names-the-surface-it-met-not-the-one-that-owns-it
    relation: references
    notes: "Both estate findings against the plugin traced to framework-owned generators. The design consequence: everything derivable is derived by the floor at run time; the plugin authors nothing the framework already knows."
  - id: an-environments-reachable-set-is-not-an-architecture
    relation: references
    notes: "The Cowork VM's egress allowlist includes GitHub; that is why the remote transport is clone-over-HTTPS with a PAT. Named as a constraint being worked within, not an architecture being endorsed."
  - id: installation-is-not-activation
    relation: references
    notes: "The plugin is installed at the account level; whether a given session activates it is Cowork's skill-triggering, not a guarantee. Phase 5 verification must observe activation, not installation."
  - id: hook-enforcement-has-three-anchors
    relation: implements
    notes: "Keeps the anchor taxonomy honest in the harness where it matters most: what the bundle runs is harness-session only for the session that invoked it; the floor pieces it calls are git-fs; the residue it prints is interpretation and says so."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "No Cowork compatibility row lands until a real ephemeral-VM run and a real local-session run produce graded evidence records, per the Phase 6 record conventions."
---

# Cowork Adapter — the third harness, built as one

## The determination this rests on

Stated by the operator, 2026-08-18, in session, after reviewing the
v0.4.0 plugin at source:

> This needs to be a Cowork adapter. We have a Claude Code adapter and a
> Codex adapter; now this needs to be a Cowork adapter, and it needs to
> work for Cowork correctly — remote ephemeral VMs and locally. A third
> adapter piece of work, not a little plugin. Clean architecture, SOLID,
> robust. Once we have the plan, the explicit bootstrap route goes into
> framework-discovery.md as a first-class discovery route.

## Where this starts from — v0.4.0 reviewed at source, 2026-08-18

The plugin (`markdownllm-bootstrap` v0.4.0: one skill, `bootstrap.sh`,
`default-branch.sh`, `push.sh`, `SESSION.md`, `config.env`) is a good
*manual* adapter. Its bootstrap performs the ordered lifecycle duties —
estate-sync before orientation, doctor, session-start, triggers in full,
imports-check with the COVERAGE line — reports the unreachable
`.claude/settings.json` adapter honestly, resolves every default branch
from the remote's own HEAD, and guards the push with refusal-first
mechanics. None of that is discarded; most of it is promoted.

Four structural defects make it a plugin rather than an adapter:

1. **Parallel implementation.** ~300 lines of bash re-perform what
   `harness_ports.py` declares as `LIFECYCLE_BINDINGS` and what the
   neutral runner executes for the other two harnesses — outside the
   test suite, outside version control's reach, drifting whenever either
   side moves.
2. **Authored reading list.** The skill's Step 2b and the bootstrap's
   "required reading" block hand-list Tier 0 — the defect class the
   QMS porch insight holds open, dismissable only when "the plugin
   derives its required-reading list from the domain kernel's routing
   blocks".
3. **Instruction, not injection.** Step 2b names itself "the gate with
   no backstop". The bootstrap tells the agent to read the contract; it
   does not put the contract in the transcript. The session gate is
   therefore satisfiable in Cowork without the contract ever loading —
   `session-start` writes the attestation, and what it emitted was
   ritual and status, not the contract the attestation vouches for.
4. **No currency binding.** The bundle lives at the account level and
   meets the framework only after cloning it. Nothing compares the
   installed bundle against what the framework now expects — staleness
   by construction, the same class the pasteable Claude settings example
   was retired for at Phase 7.

## The architectural fact: a third adapter class

Claude Code and Codex adapters are **project-level and render-time
bound**: artifacts rendered into the domain repo, currency checked by
`doctor` against the same renderer, hash-stamped at install. The Cowork
adapter is **estate-level and run-time bound**:

| | Claude Code / Codex | Cowork |
|---|---|---|
| Artifact | rendered into the domain repo | account-level bundle, outside every repo |
| Binding moment | render/install time | run time — the adapter clones the framework it binds to |
| Scope | one domain | the estate (multi-repo assembly, per-session selection) |
| Entry surface | harness injects the entry file at t=0 | nothing arrives — the skill trigger *is* discovery |
| Credentials | ambient | remote: per-session PAT, command-scoped; local: ambient |
| Publication | autopush (git-fs) | remote: guarded manual leg; local: autopush |

The ports absorb this without breaking: capabilities are data
(`AdapterCapabilities` reports what is and is not bound, honestly);
render produces artifacts (here, bundle files); inspection semantics
(`current` derived from the renderer, never hand-maintained) transfer —
but the comparison runs inside the bootstrap, at the first moment bundle
and framework coexist.

## Design rules

1. **Everything derivable is derived by the floor.** Reading lists,
   handoff text, lifecycle order, branch guards, orientation — the
   framework owns the fact, the floor emits it at run time, the bundle
   transports it. The bundle authors nothing the framework already
   knows. (Both estate findings against v0.4.0 traced upstream; this
   rule is the receiving discipline made structural.)
2. **Inject, don't instruct.** The floor gains a contract-emission
   primitive; the bootstrap's terminal act is printing the Tier-0
   contract *content* into the transcript — kernel plus each selected
   domain's entry file with its derived reading list — so reading has
   happened before acting can start. The attestation then vouches for
   something true in this harness too.
3. **The bash layer shrinks to what must precede the framework.** Token
   intake, framework clone, Python/PyYAML probe, handoff to the floor.
   Everything after the clone is floor-owned, tested Python.
4. **Anchors stay labelled.** What the bundle runs is harness-session
   for the invoking session only; the floor pieces are git-fs; what
   remains interpretation (judging non-evaluable triggers, the exposure
   question, decision recording) is printed as such. The session gate
   stays the fail-safe underneath — the adapter remains optional, never
   the difference between working and not.
5. **Two transports, one adapter.** Remote (ephemeral VM: clone with
   PAT, guarded manual publication) and local (estate already on disk:
   no PAT, autopush live, same contract emission and lifecycle). The
   mode is detected, the duties are identical, the transport differs.
6. **The disclosure boundary shapes the artifact split.** The public
   framework repo carries the adapter module, templates, and tests —
   naming no private repo. The operator's domain list and identity are
   instantiated at build time from the local estate into the private
   bundle, which is never committed to the framework repo.

## Phases

### Phase 0 — Port fit and registration

- [ ] Register `cowork` in `tools/markdownllm/adapters/` with honest
  `AdapterCapabilities`: which lifecycle moments it binds (session-start
  at bootstrap, per invoking session), which it cannot (post-write
  feedback — writes stay unvalidated until commit; stated, not hidden).
- [ ] Decide and record the port stretches: bundle-as-render-target and
  run-time currency, as data on the existing ports — no new god-object,
  no conditional in neutral modules.
- [ ] `doctor --harness cowork` reports support and the run-time-binding
  caveat; scaffold declares the honest answer (no per-domain artifact to
  render).

**Gate:** registry tests green; the architecture fitness gate's
port-only fake still proves neutral modules call nothing vendor-shaped.

### Phase 1 — Contract emission (floor primitive, harness-agnostic)

- [ ] New floor surface (CLI spelling decided in-phase: `mdllm contract
  <domain>` or a `session-start` mode): emits the Tier-0 contract
  content — the framework kernel and the domain's entry file — plus the
  reading list *derived from the same source `domain-kernel` routes
  from* (skills and prompts from the filesystem, never an authored
  list).
- [ ] Attestation semantics: when emission runs as part of session
  start, the attestation covers contract emission — making the gate's
  claim ("the contract was emitted into this session") true in
  adapterless harnesses, not only injected ones.
- [ ] Output budgeting: bounded like the lifecycle steps, elision marked
  (the Gate 6R lesson — protect every budget, or the failure moves to
  the unprotected one).
- [ ] Tests: derived list completeness (a domain adding a prompt file
  cannot produce a short list), bounded output, framework-root and
  nested-domain positions.

**Gate:** the QMS porch insight's dismissal condition is *satisfiable*
(the derived list exists at the floor); the insight itself is
dispositioned only when the bundle consumes it (Phase 3).

### Phase 2 — Publication leg (floor)

- [ ] Port `default-branch.sh` and `push.sh` guard-for-guard into the
  floor (branch read from `mdllm.defaultbranch`/origin HEAD, never
  typed; checkout must match; remote ref must already exist; ff-only;
  remote tip re-read and compared; credential via command-scoped header
  from an env var, never on disk, redacted in output).
- [ ] One publication surface, two credential modes: ambient (local —
  autopush's existing leg unchanged) and env-scoped (remote). The
  refusal messages name the remedy and never invite `--force`.
- [ ] Tests: every refusal path, the stray-branch non-creation
  guarantee, verification failure, redaction.

**Gate:** the guard scripts' behaviour is reproduced under test;
`push.sh`/`default-branch.sh` become thin callers or retire.

### Phase 3 — The bundle as a projection

- [ ] Bundle contents (`SKILL.md`, `SESSION.md`, bootstrap, config)
  become framework-owned templates rendered by a build command; the
  build derives the domain list from the local estate's remotes and
  instantiates operator identity — authored-at-build becomes
  derived-at-build. The built bundle is private output (gitignored
  path), the templates are public and name no private repo.
- [ ] The rendered bootstrap shrinks per design rule 3: token intake →
  framework clone → runtime probe → hand off to the floor's ordered
  lifecycle (estate-sync, session-start, contract emission per selected
  domain) → branch map → handoff residue (the interpretation duties,
  printed as such).
- [ ] Currency at run time: the bundle carries its definition hash; the
  bootstrap compares it against what the freshly-cloned framework's
  renderer would emit now, and reports drift honestly with the remedy
  (rebuild + reinstall) — degradation, not failure.
- [ ] Domain selection, PAT handling, and redaction preserved from
  v0.4.0 behaviour, now under test.

**Gate:** a bundle built from a clean checkout reproduces v0.4.0's
observable duties end-to-end; the two porch insights' dismissal
conditions are met (derived list consumed; handoff derived, not
authored).

### Phase 4 — Local transport

- [ ] Mode detection (configured local estate path exists and is the
  estate) or explicit invocation; no clone, no PAT, ambient
  credentials, autopush live — the publication guard degrades to
  advisory because the git-fs leg already holds.
- [ ] Same contract emission, same lifecycle, same handoff; the
  transport difference is stated in one line of the handoff, not spread
  through it.

**Gate:** one local Cowork session on a real domain runs the full
sequence with zero remote-mode residue (no PAT prompt, no AUTH-FAILED
noise).

### Phase 5 — Live verification (both transports, graded evidence)

- [ ] Remote: a fresh ephemeral-VM session on one operator-selected
  domain — activation observed (not installation), contract emission in
  the transcript before the first write, session gate attestation
  fresh, a real commit published through the guarded leg, currency
  check exercised against a deliberately stale bundle.
- [ ] Local: the Phase 4 gate session, recorded to the same standard.
- [ ] Evidence records in `evidence/` graded per the Phase 6
  conventions: first-hand vs relayed, exact builds, no claim wider than
  the tested surface.

**Gate:** both records exist; defects found route back to their owning
phase, not patched in place.

### Phase 6 — Specification and public surfaces

- [ ] `framework-discovery.md`: the **explicit bootstrap route** as a
  first-class discovery route — a harness class with no entry-file
  discovery, where a plugin/skill/typed prompt is the discovery event,
  and where contract *emission* (not an instruction to read) is the
  arrival criterion. States what the route guarantees and what stays
  interpretation.
- [ ] README compatibility table: a Cowork row, written from the Phase 5
  evidence, no wider.
- [ ] `orchestration.md` anchor notes and `interface.md` if the
  emission primitive touches their vocabulary; kernel regenerated if
  any `<!-- kernel -->` block changes; the dark-region walk run.
- [ ] Disposition the standing insights this plan answers:
  `agents-md-discovery-is-harness-dependent` (route landed), the QMS
  porch pair (conditions met at Phase 3), with the sweep's residual
  framing updated.
- [ ] Coordinate with `vendor-harness-adapter-foundation` Phase 7/8: a
  third registry entry lands while its public-surface sweep is open —
  one owner per surface, no double edits.

**Gate:** validate, coherence, kernel freshness, full suite; the
foundation plan's Phase 7 owner acknowledges the new row.

### Phase 7 — Rollout (owner: operator)

- [ ] Build the real bundle from the live estate; install in Cowork;
  retire/replace v0.4.0 at the account level.
- [ ] PAT hygiene stays the operator's ritual (per-session paste,
  revoke at end) until Cowork ships credential brokering; the wrap-up
  reminder survives from v0.4.0.
- [ ] Decide whether the regulated domains adopt any additional
  session discipline for Cowork work (their own plans own that
  decision).
- [ ] Version, changelog, release act — the deliberate publication of
  the public root stays the operator's.

## Completion criteria

- The Cowork adapter is a registry entry with tests and docs, not a
  conditional anywhere in neutral code.
- Both transports verified live with graded evidence; the compatibility
  row claims exactly that and no more.
- The contract arrives by emission in every Cowork session; the reading
  list cannot be short by construction; the session gate's claim is
  true in this harness.
- The bundle is rendered, hash-stamped, and run-time currency-checked;
  a stale bundle says so and names its remedy.
- The public repo names no private domain at any point in the work.

## Held outside this plan

- Cowork credential brokering (waits on the platform).
- PostToolUse-equivalent write feedback in Cowork — no mechanism exists;
  the honest statement ("writes are validated at commit time") stands.
- `pretooluse-action-boundary-gate` stays paused on its own re-open
  condition; this plan neither advances nor supersedes it.
- Any batch estate migration — domains meet the new bundle at their own
  next session, per the sweep's no-batch-rewrite rule.
