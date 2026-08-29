---
name: MarkdownLLM Framework
description: A self-describing specification framework for building LLM-driven systems using markdown, YAML, and git
version: 3.37.0
applies_to: "**/*.md"
framework_root: .
git:
  autocommit: true
  branch: main
  # The public repo is a RELEASE surface, not estate working state: pushing it
  # is a version event gated by judgement (reconciliation, changelog, version)
  # with no mechanical completeness gate. Publication is fail-closed everywhere:
  # only literal true authorises the post-commit send; this release surface is
  # explicitly false (autopush-requires-explicit-authority).
  autopush: false
---

# MarkdownLLM Framework Agent

## What This System Is

This is the MarkdownLLM framework — a specification for building LLM-driven systems where humans define domains, LLMs reason within them, and git-versioned markdown files are the persistent state. The framework is self-describing: its own specifications are things within the framework they define.

## A Standing Truth About This Agent

You predict the next move — the next token, sentence, or action — from the stream of what comes next. You cannot predict its *consequence* the same way. Consequence is recoverable only in retrospect, by reasoning back over moves already made; it is not forecastable forward. Being asked to consider consequences does not change this: you can reason about them, you cannot foresee them. So when a move's consequence could not be recovered after the fact — anything that deletes, sends, spends, or otherwise cannot be taken back — that judgement belongs to the human and to the structure, not to a prediction of yours. Reach for the structure; defer the irreversible. This is orientation, not a hook the floor enforces. Full reasoning: `things/insights/consequence-is-recoverable-only-in-retrospect.md`.

This authority principle complements rather than replaces ordinary prospective
risk analysis: a model can compare plausible outcomes, but cannot certify the
future.

## Three-Layer Architecture

Every domain in this framework — including the framework itself — follows the same three-layer pattern:

```
Layer 1: AGENTS.md        ← Entry contract; delivered by the harness route; orchestrates everything
Layer 2: skills/*.md      ← Reusable capabilities loaded by the agent at startup
Layer 3: things/*.md      ← Data instances — the actual content the domain manages
                              ↓
                          Git — accepted state, event stream, and inspectable history
```

| Layer | File Pattern | Purpose |
|---|---|---|
| **Agent** | `AGENTS.md` | Startup instructions, skill inventory, commit conventions, business context |
| **Skills** | `*-specification.skill.md` | Philosophy, principles, reasoning patterns for the domain |
| | `*-read.thing.skill.md` | How to analyse things without modifying them |
| | `*-write.thing.skill.md` | How to create, update, and validate things |
| | `*-workflow.skill.md` | End-to-end process orchestration |
| **Things** | `things/**/*.md` | Data instances — every item the domain tracks |

## Standard Thing Structure

Every thing — regardless of domain or type — shares this YAML frontmatter structure:

```yaml
---
id: unique-kebab-case-identifier
type: <reserved, or declared by the domain's _schema.yaml>
status: <the type's vocabulary — reserved sets are the tool's; domain types declare their own>
version: 1.0
created: YYYY-MM-DD
tags: [tag1, tag2]
priority: <optional>
dependencies: [other-thing-id]     # optional; hard prerequisites — things that must FINISH first (floor-enforced: a terminal thing may not depend on unfinished work); for soft association use linked_things
linked_things:
  - id: related-thing-id
    relation: <the domain's declared vocabulary, plus the reserved relations the floor enforces>
# Plus any domain-specific fields — schema grows with domain needs
---

# Thing Title

Narrative body: context, rationale, current state, next steps, blockers.
This is where the reasoning lives — not just the data.
```

**The enums are deliberately not written above.** `kernel.md` carries every
one of them at Tier 0, on the always-loaded path, and `thing.md` owns them
in full. This file used to restate them, and the restatement did not merely
go stale — it *instructed*: the relation line still advertised `related`
nine weeks after the 2026-06-12 schema prune removed it, a session read the
line, used the relation, and took two validate Warnings for it. The
priority line had carried three values against the kernel's four, and a
session held both readings at once. A pointer cannot drift; an enum copied
into a second file always eventually does.

**Emergent schema:** Core fields are fixed. Everything else is added as the domain's complexity requires it. Never over-define upfront.

## How This Agent Works

### On Startup

> **Manual CLI launch — read before the first command.** Here, `mdllm <command>` is notation for this repository's CLI, not an assumption that an executable named `mdllm` is installed. On Windows PowerShell and Codex managed shells, run `& ".\tools\mdllm.ps1" <command>` even when `python` exists: the visible or harness-bundled interpreter may lack PyYAML, and the launcher selects one only after dependency-probing it. Elsewhere, use `python tools/mdllm.py <command>` only with an interpreter that can `import yaml`. Interpret older direct-Python examples below through this route; never infer that a harness-bundled Python is the project runtime. Automatic startup uses plain `estate-sync` and stays non-interactive/best-effort. If an operator explicitly requests a fresh manual estate sync, run `mdllm estate-sync . --require-fresh`; cached or unresolved state then exits nonzero so a restricted Codex task can request one-command network/filesystem approval and rerun the exact wrapper command. A sandbox denial is not evidence that the repository's Git credentials are invalid.

> **[HARD HOOK: `session-start:estate-sync`]** Sync before orienting — orientation reads `git log`, and in a multi-machine estate committed state partly lives on the remote. Run `mdllm estate-sync .` through the route above (root + nested domain repos: fetch + ff-only pull, bounded, degrades offline to an advisory line) *before* reading velocity or evaluating triggers. Divergence and dirty trees are reported, never resolved; it never pushes. The Claude Code SessionStart adapter already runs it ahead of `session-start`; run it by hand in any harness without an adapter. Full spec: `orchestration.md` → Hard Hooks; `git-workflow.md` → The Machine Axis.

> **[READ BOUNDARY: `significant-read:pin`]** A full-corpus review or other significant read must name one immutable `commit:<full-sha>` view; never build conclusions from ambient paths while HEAD can move underneath them. `mdllm session-start` emits the base. Immediately before writing from that read, run `mdllm session-start . --assert-head <full-sha>`; moved HEAD requires reconciliation or a deliberate re-read. This proves byte currency only, not receipt, reading, application, or adherence. Full spec: `orchestration.md` → The Significant-Read Boundary.

> **[BOUND PROMPT: `orient`]** The deep orientation walk — the judgement half of session start: `session-orientation` (with its scoped insight-staleness check), `domain-velocity`'s residue (churn, ignored unblocks, what the stalls the digest names *mean*), `evaluate-triggers`' judgement over the not-mechanically-evaluable set, and `surface-attention`'s ordering. **Explicitly invoked, not automatic** — the operator says "orient", or the agent invokes it the moment intent first touches domain state (the moment the pull exists). The mechanical half needs no invocation: the session-start digest computes and emits version, velocity trend, stall lines, open loops, fired triggers, and self-answering cues — consume those, never recompute them. Rationale: un-pulled judgement at t=0 does not happen on any model tier (`emitted-content-is-read-instructed-content-is-economised`), and every mechanised step quiets the remainder (`partial-coverage-quiets-the-uncovered-steps`) — so the residue is routed to invocation, exactly as `session-end` is. Prompt files: `templates/prompts/`. Full spec: `orchestration.md` → Bindings.

**Determine session intent before loading specs.** Loading all framework specs eagerly costs tens of thousands of tokens — a large share of a model's working context before any work begins. Load only what the session needs. **This economy governs Tier 1 and Tier 2 only — Tier 0 is emitted or owed, never economised** (five sessions across three harnesses recruited this rule to excuse a Tier-0 skip; session-start-hardening Phase 0 closed that reading). (`python tools/mdllm.py tokens` measures the current per-tier split; prose does not restate the figures — restated numbers have drifted three times.)

**Tier 0 — the emitted floor (exempt from the economy rule above):**
- `AGENTS.md` — this file (already loaded)
- `kernel.md` — the generated operative kernel: the rules of thing.md, orchestration.md, read/write/validate.thing.md, and git-workflow.md without their rationale, at a small fraction of the full-spec cost. **Delivered by emission, not instruction** (v3.33): on direct channels (manual CLI runs, bootstraps, Codex sessions) `mdllm session-start` emits it whole with an integrity trailer — line count + sha256; a missing trailer or a `[truncated]` marker means the channel cut it. On the budgeted hook channel it is loudly deferred with the same integrity facts, and the read it names is owed before acting on domain state. Regenerate with `python tools/mdllm.py kernel` after any spec change.

**Tier 1 — Load a full spec only when the kernel is not enough** — reasoning *about* the framework, evolving a spec, or resolving an ambiguity the kernel doesn't settle:
- `thing.md`, `orchestration.md`, `read.thing.md`, `write.thing.md`, `validate.thing.md`, `git-workflow.md` (load individually, not wholesale)

**Tier 2 — Load on demand by query type:**

| Query type | Load |
|---|---|
| Creating or scaffolding a new domain | `domain-specification-guide.md` |
| Scaling, structure, or performance concerns | `scalability-guide.md` |
| Philosophical or "why" questions | `llm-driven-systems.manifesto.md` |
| I/O, deliverables, or output format questions | `interface.md` |
| Domain agent locating the framework | `framework-discovery.md` |
| Domain agent refreshing from framework evolution | `domain-refresh.md` |
| Session-end work, insights, orientation (open loops) | `session-memory.md` |
| Contradictions, conflicts, belief revision | `belief-revision.md` |
| Significantly changing a rule, workflow, or thing the domain reasons from; reconciling a change across its dependents | `change-reconciliation.md` |
| Periodic quality reflection | `retrospective.md` |
| Creating things with triggers or evaluating trigger conditions | `trigger-specification.md` |
| Building a pattern library; teaching by worked examples (`type: example`) | `example-things.md` |
| Applying or defining multi-lens reasoning; surfacing lens conflicts | `reasoning-lenses.md` |
| Reflexive behaviour at scale; trigger/schema/relationship indexes; index drift | `derived-index.md` |
| Decisions, pinned inputs, external content, output traceability | `provenance.md` |
| Multi-stage, multi-session process instances; workflow run-state; stage cursors | `workflow-state.md` |
| Two operators/sessions contending for one thing; advisory claims, leases | `coordination-claim.md` |
| Applying or specialising the universal workflow methodology; the seven stages, the two shapes | `universal-workflow.md` |
| Composing workflow loops — modules, the metabolism, radii, estate-level operating models | `operating-model.md` |
| Human operator asking what changed / what the tools are / what the v3 experience is | `docs/operator-guide.md` |
| Human newcomer's first session; onboarding a non-author operator | `docs/first-hour.md` |
| Orienting in the framework structure; what links to what; spec graph navigation | `docs/framework-map.md` |
| How publication, reconciliation and cadence interact — the three radii, diagrammed | `docs/estate-mechanics.md` |

**Session cost:** the kernel's introduction cut Tier 0 to roughly a fifth of the pre-kernel Tier 0+1 load (the dated measurements live in CHANGELOG 3.2.0). Full-spec loads are per-file and on-demand. Measure with `python tools/mdllm.py tokens`; do not assert costs in prose.

Note: This agent operates in **autocommit mode** (`git.autocommit: true`). All state changes to framework specs are committed automatically.

### On User Request
1. **Route intent** — Identify the query type. Determine which Tier 1 and Tier 2 specs the session needs and load them before proceeding.
2. **Load examples if needed** — Reference `examples/` for concrete demonstrations
3. **Execute** — Reason within the framework's own principles while helping the user

### On Output

> **[HARD HOOK: `post-write:commit`]** After creating or modifying any `.md` file with YAML frontmatter, commit it to the **owning repo** before completing the response. Walk up the directory tree from the modified file to find the correct `.git` root — never assume it is the framework repo. Full spec: `orchestration.md` → Hard Hooks.

> **[HARD HOOK: `pre-domain-scaffold:isolate`]** When scaffolding a new domain, the isolation sequence is mandatory and must complete before any domain files are committed anywhere: (1) `git init` in the domain folder, (2) add the domain path to the framework `.gitignore`, (3) commit that exact `.gitignore` delta to the framework repo, (4) commit domain files to the domain repo, (5) add a remote and publish only under separate explicit authority. Never commit domain files to the framework repo. **Run `python tools/mdllm.py scaffold <path> --autopush false` — it performs steps 1–4 transactionally plus instantiated templates and the hook set; use `--autopush true` only when the human has deliberately granted standing publication authority. Only the remote and semantic content stay with you.** Full spec: `orchestration.md` → Hard Hooks.

> **[BOUND PROMPT: `session-end`]** At the end of any session where a domain was discussed or modified, invoke the `session-end-continuity` prompt: reconstruct the logical session from surviving dialogue **and its commit range** (compaction is not a session boundary), extract any additional insights, disposition the standing insights (promote/dismiss/keep-active), check for contradictions, manage open-loop things, commit with a rich `session-end:` message (the backward record is git — `continuity.md` and `WORKLOG.md` are retired), then report publication debt (`mdllm estate-sync . --status` — the step after the commit; a summary that ends at the commit ends one step early). Explicitly invoked — not automatic. Full spec: `orchestration.md` → Bindings, `templates/prompts/session-end-continuity.md`.

1. If modifying specifications: validate consistency across linked specs
2. If creating new specs: follow thing.md patterns (frontmatter + narrative body)
3. If adding or removing a spec, run `mdllm coherence` — **run it to see what it covers; the module is the authority and this line is not a list of its checks** (a prose inventory of mechanical checks is the exact restatement class the checks exist to end, and it went stale inside one sprint). It runs in the pre-commit hook, so a stale generated artifact, a catalog annotation disagreeing with its spec's frontmatter, or a Tier-2 spec no routing row names all block the commit. Then walk the **prose-only residue** the tool still cannot read (see `change-reconciliation.md` → Walking the Dark Region): today that is `docs/framework-map.md` (View 1 counts + View 2 node) and the *descriptions* in this file's routing table and spec catalog — their `type`/`status` annotations and their completeness are now mechanical, and only the human-written one-liners remain judgement.
4. Commit with a structured message following git-workflow.md conventions (the commit is the backward record)

## Framework Specifications (Things)

The framework defines itself through these interconnected specifications:

### Foundational
- **llm-driven-systems.manifesto.md** — Philosophy, paradigm shift, core principles. The "why." (`type: manifesto`, `status: evolving`)
- **thing.md** — The atomic unit specification: schema definition, field reference, cohesion and decomposition principle. (`type: specification`, `status: evolving`)
- **universal-workflow.md** — The universal workflow methodology: seven evidence-gated decisions from need to verified outcome, in two shapes (accumulative and repeatable), iterated by feeding each review into the next cycle's current-state assessment. The general problem-approach the framework's own rituals trace; foundation — it reaches domains via the framework version and domain-refresh, and domains specialise it as their own workflow-definitions. (`type: specification`, `status: draft`)

### Operational
- **read.thing.md** — How LLMs read and reason about things without modification. (`type: specification`, `status: stable`)
- **write.thing.md** — How LLMs create, update, and manage things. (`type: specification`, `status: stable`)
- **validate.thing.md** — How to validate thing integrity (structural, referential, semantic). (`type: specification`, `status: stable`)
- **interface.md** — The I/O layer: input routes, output types, deliverables vs things. (`type: specification`, `status: stable`)
- **git-workflow.md** — Git as state machine: commit points, conventions, event stream, autocommit mode. (`type: specification`, `status: evolving`)
- **orchestration.md** — Hook points, prompts, and bindings: an opt-in pattern for domains that need structured orchestration. (`type: specification`, `status: evolving`)
- **session-memory.md** — How sessions preserve generative knowledge: `type: insight` things (kept live by the thing graph) and the generated **orient** view of open loops that replaces the retired `continuity.md`. Defines the session-end extraction ritual (invoked via the `session-end-continuity` bound prompt — explicit, not automatic). (`type: specification`, `status: evolving`)
- **belief-revision.md** — How the framework handles contradictions between things: `type: conflict`, `relation: supersedes`/`contradicts`, and the belief revision process. (`type: specification`, `status: stable`)
- **retrospective.md** — Periodic domain quality reflection: `type: retrospective`, when to write one, and how it produces insights, surfaces latent conflicts, and improves reasoning over time. (`type: specification`, `status: stable`)
- **framework-discovery.md** — How domain agents locate the framework root and foundational specs. (`type: specification`, `status: stable`)
- **domain-refresh.md** — How domain agents discover framework evolution and update themselves. Deployment architecture (nested repos, .gitignore isolation) and the refresh process. (`type: specification`, `status: evolving`)
- **trigger-specification.md** — Declarative attention signals: all trigger types, condition values, action values, evaluation semantics, and idempotency. Extends thing.md. (`type: specification`, `status: stable`)
- **derived-index.md** — The derived-index pattern: regenerable caches (`type: index`) that each aggregate one signal across a domain so reflexive behaviour stays cheap at scale (the signal set is the tool's — `mdllm index`). Drift-safe by construction (rebuild-and-diff at validation). Opt-in, deploy-when-felt. (`type: specification`, `status: draft`)
- **provenance.md** — Output traceability: `type: decision` records with inputs pinned to git commits (`informed_by`), `origin: external` quarantine for ingested content, the knowledge → decision → output chain, and the reverse-provenance index that enables diff-driven regeneration. Mechanically enforced by `mdllm provenance`. (`type: specification`, `status: draft`)
- **change-reconciliation.md** — How a domain stays consistent across change: the human declares an inflection, then a scale-free four-beat pass (cue → assimilate → walk → seal) reconciles the change against its blast radius using the relationships and reverse-provenance indexes. Semantic consistency is maintained at the point of change, not by sweeping. (`type: specification`, `status: draft`)
- **workflow-state.md** — Workflow run-state as a primitive: `workflow-definition` (stages as data + allowed transitions) and `workflow-run` (a structural `definition` pointer, optional committed-revision pin, a `current_stage` cursor, resume in the body). The decomposition principle applied to processes; the floor resolves pins and enforces membership and declared edges against the governing revision, while the agent judges whether the work merits an allowed transition. Reserved, and now `evolving` — exercised on a live domain. (`type: specification`, `status: evolving`)
- **coordination-claim.md** — The advisory-claim convention (`held_by` + optional `held_until` lease) for same-target contention: read-and-respected, not a lock; deploy-when-felt on a contended thing. General, not workflow-specific — `workflow-run` is its motivating consumer, and the first live deployment came from elsewhere entirely: the dispatcher's per-repo claim, where two machines share a corpus and no scheduler. (`type: specification`, `status: evolving` — deployed 2026-08-29, validated by use, not yet refined by it)
- **operating-model.md** — How atoms compose: modules running accumulative arcs and repeatable loops, the metabolism between them, fractal radii, estate-radius composition over served faces, and the five declared dimensions that make a composition auditable. Doctrine over existing primitives — adds no mechanism; grows only on cross-corpus convergence. (`type: specification`, `status: draft`)

- **example-things.md** — Full specification for `type: example` things: frontmatter template, when to use examples, and why examples work better than rules for inductive LLM learning. (`type: specification`, `status: stable`)
- **reasoning-lenses.md** — Canonical multi-lens reasoning spec: how to apply lenses in read mode and write mode, compliance domain examples, and how to surface and handle conflicts. (`type: specification`, `status: stable`)

### Guides
- **scalability-guide.md** — How to scale from tens to thousands of things. (`type: guide`, `status: stable`)
- **domain-specification-guide.md** — How to create a new domain using the framework. (`type: guide`, `status: stable`)
- **docs/operator-guide.md** — Human-facing: what working in a domain feels like since v3, the mdllm toolbox with scenarios, and what remains the operator's job. The specs are agent-first; this is the human's walkthrough. (`type: guide`, `status: draft`)
- **docs/first-hour.md** — Human-facing: a newcomer's first sixty minutes — orientation, scaffolding a first domain, installing the floor, one real session. Covers arrival; the operator-guide covers the steady state. (`type: guide`, `status: evolving`)
- **docs/estate-mechanics.md** — Human-facing: how publication, reconciliation and cadence interact at three radii (inside a domain, between domains, at the substrate), diagrammed. (`type: guide`, `status: evolving` — born frontmatter-less; a review-loop finding made it a thing, ending its no-special-cases exemption)
- **docs/framework-map.md** — Visual architecture map (Mermaid): the five-band elevation, the spec-layer dependency graph, and the mdllm subcommand → spec mapping. Derived from frontmatter links, `mdllm --help`, and the tier table; the frontmatter wins on disagreement. (`type: guide`, `status: draft`)

### Deferred (Spec When Foreseeable, Deploy When Felt)
- **thing-lifecycle.md** — Rolling window, disposition to stubs, rehydration from git history, manifest index. Addresses the 200–300 thing ceiling. Deliberately outside the TIERS loading map and the `.markdownllm` catalog until reconciled with the live tool — it predates the mtime→git `stale` fix and the current index mechanics. (`type: specification`, `status: draft`)

### Examples
Each example is its own corpus with its own `_schema.yaml`; `mdllm validate` run at the framework root validates them in the same pass (they are excluded from the framework corpus walk — separate id space — but not from the floor).
- **examples/life-manager/** — Personal life and work management domain (populated demonstration dataset; one deliberately overdue task for `mdllm triggers`)
- **examples/compliance-patterns/** — Regulatory compliance pattern library

### Templates
- **templates/** — Starting-point templates for AGENTS.md, skills, and workflows

## Framework Principles (Applied To Itself)

1. **Definition-Driven** — Humans define the constraints; LLMs reason within them. Not driven by ephemeral chat residue and not fully autonomous: the durable definitions are instructions in the broad technical sense, and the structure is the interface.
2. **Self-Describing** — The framework is a domain within itself. Its specifications are things with frontmatter, relationships, statuses, and versions. That dogfooding demonstrates reflexivity; it does not by itself prove universality or adherence in another harness.
3. **Atomic & Composable** — Each spec is self-contained but explicitly linked to others. You can read any one spec independently, but together they form a complete system.
4. **Minimal Core, Emergent Detail** — Start with the essential structure. Let the schema grow with domain needs. Never over-engineer upfront; add complexity only when it earns its place.
5. **Evolving** — Specifications have status (`draft`, `evolving`, `stable`). New specs start as drafts and mature through use.
6. **Vendor Agnostic by contract** — This AGENTS.md uses no vendor-specific memory store; the framework is the memory. Discovery and lifecycle compatibility are still product capabilities, so public claims remain limited to the exact harness evidence that earned them.
7. **Inspectable & Auditable** — Accepted state changes, recorded decisions, their declared inputs, and byte-level diffs are committed to git. This is a strong audit aid, not a complete trace of hidden or unrecorded model reasoning; vendor models and harness internals remain external trust boundaries.
8. **Git-Backed** — Git is the state machine for accepted recorded domain state, not a claim that the record is true of the outside world. Commit messages are the event stream and carry the session narrative (`mdllm worklog` prints an on-demand view; nothing is committed back).
9. **Elegant Constraint Enables Efficiency (hypothesis, under test)** — Structure makes reasoning consistent across sessions and vendors — that much is demonstrated. The stronger claim that a *smaller* model with structure matches or beats a *larger* model without it is the framework's central **hypothesis**, not a proven result: it rests on one eval whose reasoning core saturated, and stays a hypothesis until a more discriminating fixture tests it. Keep this distinct from the framework's *utility*, which independent adoption evidences directly. (See the manifesto, "Elegant Constraint Enables Efficiency.")

## Thing Types In This Domain

The section below is **generated** — `mdllm domain-kernel .` writes it from
`_schema.yaml` and the tool's reserved set, and `mdllm coherence` fails the
commit if it drifts. It used to be authored, and it lagged its own sources
repeatedly: a review-loop finding caught `artifact` missing here while seven
committed things carried it. The reserved types no longer carry prose
descriptions here at all — `kernel.md` names the reserved set and routes
each type to the spec that owns it, which is where a description belongs.

<!-- generated:types -->
**Declared domain types** (from `_schema.yaml` — the authority; regenerate on schema change):
- `artifact` — A committed record artifact with its own lifecycle — today the independent review records in `reviews/` (statuses: evolving / stable / deprecated)
- `example` — A worked framework pattern distilled from verified execution, teaching by positive and negative contrast (statuses: draft / evolving / stable / deprecated)
- `plan` — A phased, multi-session work plan for evolving the framework; phase checkboxes updated as work lands (statuses: not-started / in-progress / blocked / paused / completed / cancelled)

Framework-reserved types (built into the tool, no declaration needed): `conflict`, `continuity-brief`, `decision`, `guide`, `index`, `insight`, `manifesto`, `prompt`, `retrospective`, `skill`, `specification`, `workflow-definition`, `workflow-run`.
<!-- /generated:types -->

## Key Innovations

1. **Harness-delivered discovery** — AGENTS.md is the one canonical contract. A harness may load it directly, reach it through a core entry pointer, or require explicit bootstrap/emission; automatic discovery is measured, not presumed.
2. **Multi-Lens Reasoning** — Complex decisions are analysed through multiple lenses simultaneously (e.g. Domain Logic, Compliance Logic, Audit Logic). Each lens asks different questions of the same data.
3. **Tiered Context Loading** — Agents choose their context depth based on the query:
   - *Level 1* — Metadata only (frontmatter fields; fast, broad)
   - *Level 2* — Relationships + metadata (linked_things, dependencies)
   - *Level 3* — Full context (complete thing files including narrative body)
4. **Pattern Libraries via Examples** — `type: example` things teach through positive and negative patterns. The agent learns domain conventions by reading worked examples, not just rules.
5. **Nested Repo Isolation** — Domains live as independent git repos nested within the framework directory. The framework's `.gitignore` excludes all domain folders. Domain history is always separate from framework history.
6. **Scalable Structure** — The same three-layer pattern works from 10 things to 10,000. Abstraction layers (type grouping, status filtering, tag taxonomies) emerge as the domain grows.
7. **Reflexive Behaviour via Derived Indexes** — The agent reasons not only *within* a domain but *about* it: domain velocity (git as telemetry), systematic trigger evaluation, conflict scanning, and schema-coherence review. At scale these run against regenerable derived indexes (`derived-index.md`) rather than re-scanning every thing — keeping reflexive work cheap, and drift-detectable through validation.

## Status Values For Framework Specs

*The set itself is not declared here* — `RESERVED_STATUSES` in the tool owns
it and `kernel.md` carries it. What follows is the editorial gloss: what
each status means when it is a **framework spec** wearing it, which is
judgement no authority mechanises.

- `draft` — First version, created but not yet validated through real-world use
- `evolving` — Actively being refined based on use and feedback
- `stable` — Proven through use, unlikely to change structurally
- `deprecated` — Superseded, kept for history

## Usage Pattern

```
User Request (about the framework or a domain)
    ↓ (delivered by the harness entry route)
Load this AGENTS.md
    ↓
Identify: framework work or domain work?
    ↓
Load relevant specifications and skills
    ↓
Reason and execute within framework principles
    ↓
Commit changes following git-workflow.md conventions
```

## Validation Checklist

Before committing framework changes:

- [ ] `python tools/mdllm.py validate .` passes — the pre-commit hook runs this anyway and blocks commits with Errors; running it first means you fix findings in the same operation rather than at the commit boundary
- [ ] Status reflects reality (draft if new, evolving if actively changing) — the tool checks vocabulary validity; *you* check truthfulness
- [ ] Version incremented if substantive change to a stable spec
- [ ] Kernel regenerated (`python tools/mdllm.py kernel`) if any spec's `<!-- kernel -->` block or operative content changed
- [ ] Commit message follows git-workflow.md conventions (rich — the commit is the backward record)

> **The Deterministic Floor (v3.0):** mechanical validation (structural, referential, schema) is owned by `tools/mdllm.py`; when the current pre-commit hook is installed and runnable, mechanical Errors are enforced at that boundary. Never re-perform those checks by reasoning. The agent's validation responsibility is semantic only (validate.thing.md → Layer 2). Domain status vocabularies are declared in `_schema.yaml` / `things/_schema.yaml`, not fixed by the framework.
