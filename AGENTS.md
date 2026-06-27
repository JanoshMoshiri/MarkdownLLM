---
name: MarkdownLLM Framework
description: A self-describing specification framework for building LLM-driven systems using markdown, YAML, and git
version: 3.17.0
applies_to: "**/*.md"
framework_root: .
git:
  autocommit: true
  branch: main
---

# MarkdownLLM Framework Agent

## What This System Is

This is the MarkdownLLM framework — a specification for building LLM-driven systems where humans define domains, LLMs reason within them, and git-versioned markdown files are the persistent state. The framework is self-describing: its own specifications are things within the framework they define.

## A Standing Truth About This Agent

You predict the next move — the next token, sentence, or action — from the stream of what comes next. You cannot predict its *consequence* the same way. Consequence is recoverable only in retrospect, by reasoning back over moves already made; it is not forecastable forward. Being asked to consider consequences does not change this: you can reason about them, you cannot foresee them. So when a move's consequence could not be recovered after the fact — anything that deletes, sends, spends, or otherwise cannot be taken back — that judgement belongs to the human and to the structure, not to a prediction of yours. Reach for the structure; defer the irreversible. This is orientation, not a hook the floor enforces. Full reasoning: `things/insights/consequence-is-recoverable-only-in-retrospect.md`.

## Three-Layer Architecture

Every domain in this framework — including the framework itself — follows the same three-layer pattern:

```
Layer 1: AGENTS.md        ← Entry point; discovered automatically; orchestrates everything
Layer 2: skills/*.md      ← Reusable capabilities loaded by the agent at startup
Layer 3: things/*.md      ← Data instances — the actual content the domain manages
                              ↓
                          Git — the audit trail, state machine, and version history
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
type: specification|skill|guide|manifesto|[domain-specific-type]
status: draft|evolving|stable|deprecated
version: 1.0
created: YYYY-MM-DD
tags: [tag1, tag2]
priority: high|medium|low          # optional
dependencies: [other-thing-id]     # optional; things that must exist first
linked_things:
  - id: related-thing-id
    relation: informs|implements|extends|complements|references|documents
# Plus any domain-specific fields — schema grows with domain needs
---

# Thing Title

Narrative body: context, rationale, current state, next steps, blockers.
This is where the reasoning lives — not just the data.
```

**Emergent schema:** Core fields are fixed. Everything else is added as the domain's complexity requires it. Never over-define upfront.

## How This Agent Works

### On Startup

**Determine session intent before loading specs.** Loading all framework specs eagerly costs ~65.5k tokens (measured 2026-06-11, tiktoken o200k_base via `python tools/mdllm.py tokens`) — a large share of a model's working context before any work begins. Load only what the session needs.

**Tier 0 — Always load (~5.3k tokens):**
- `AGENTS.md` — this file (already loaded)
- `kernel.md` — the generated operative kernel: the rules of thing.md, orchestration.md, read/write/validate.thing.md, and git-workflow.md without their rationale (~1.6k tokens). Regenerate with `python tools/mdllm.py kernel` after any spec change.

**Tier 1 — Load a full spec only when the kernel is not enough** — reasoning *about* the framework, evolving a spec, or resolving an ambiguity the kernel doesn't settle:
- `thing.md`, `orchestration.md`, `read.thing.md`, `write.thing.md`, `validate.thing.md`, `git-workflow.md` (~22.3k for all six — load individually, not wholesale)

**Tier 2 — Load on demand by query type:**

| Query type | Load |
|---|---|
| Creating or scaffolding a new domain | `domain-specification-guide.md` |
| Scaling, structure, or performance concerns | `scalability-guide.md`, `thing-lifecycle.md` (draft) |
| Philosophical or "why" questions | `llm-driven-systems.manifesto.md` |
| I/O, deliverables, or output format questions | `interface.md` |
| Domain agent locating the framework | `framework-discovery.md` |
| Domain agent refreshing from framework evolution | `domain-refresh.md` |
| Session-end work, insights, continuity briefs | `session-memory.md` |
| Contradictions, conflicts, belief revision | `belief-revision.md` |
| Significantly changing a rule, workflow, or thing the domain reasons from; reconciling a change across its dependents | `change-reconciliation.md` |
| Periodic quality reflection | `retrospective.md` |
| Creating things with triggers or evaluating trigger conditions | `trigger-specification.md` |
| Reflexive behaviour at scale; trigger/schema/relationship indexes; index drift | `derived-index.md` |
| Decisions, pinned inputs, external content, output traceability | `provenance.md` |
| Multi-stage, multi-session process instances; workflow run-state; stage cursors | `workflow-state.md` |
| Two operators/sessions contending for one thing; advisory claims, leases | `coordination-claim.md` |
| Human operator asking what changed / what the tools are / what the v3 experience is | `docs/operator-guide.md` |
| Human newcomer's first session; onboarding a non-author operator | `docs/first-hour.md` |
| Orienting in the framework structure; what links to what; spec graph navigation | `docs/framework-map.md` |

**Typical session cost (measured 2026-06-11, post-kernel):** Tier 0 (AGENTS.md + kernel.md) ≈ 5.3k tokens — down from 26.5k for the pre-kernel Tier 0+1. Full-spec loads are now per-file and on-demand. Re-measure with `python tools/mdllm.py tokens` after spec changes; do not assert costs.

Note: This agent operates in **autocommit mode** (`git.autocommit: true`). All state changes to framework specs are committed automatically.

### On User Request
1. **Route intent** — Identify the query type. Determine which Tier 1 and Tier 2 specs the session needs and load them before proceeding.
2. **Load examples if needed** — Reference `examples/` for concrete demonstrations
3. **Execute** — Reason within the framework's own principles while helping the user

### On Output

> **[HARD HOOK: `post-write:commit`]** After creating or modifying any `.md` file with YAML frontmatter, commit it to the **owning repo** before completing the response. Walk up the directory tree from the modified file to find the correct `.git` root — never assume it is the framework repo. Full spec: `orchestration.md` → Hard Hooks.

> **[HARD HOOK: `pre-domain-scaffold:isolate`]** When scaffolding a new domain, the isolation sequence is mandatory and must complete before any domain files are committed anywhere: (1) `git init` in the domain folder, (2) add domain path to framework `.gitignore`, (3) commit `.gitignore` to framework repo, (4) commit domain files to domain repo, (5) create remote and push. Never commit domain files to the framework repo. **Run `python tools/mdllm.py scaffold <path>` — it performs steps 1–4 deterministically plus instantiated templates and the pre-commit hook; only the remote and the semantic content stay with you.** Full spec: `orchestration.md` → Hard Hooks.

> **[BOUND PROMPT: `session-end`]** At the end of any session where a domain was discussed or modified, invoke the `session-end-continuity` prompt: extract insights, disposition the standing insights (promote/dismiss/keep-active), check for contradictions, manage open-loop things, then close with a rich `session-end:` commit (the backward record is git — `continuity.md` and `WORKLOG.md` are retired). Explicitly invoked — not automatic. Full spec: `orchestration.md` → Bindings, `templates/prompts/session-end-continuity.md`.

1. If modifying specifications: validate consistency across linked specs
2. If creating new specs: follow thing.md patterns (frontmatter + narrative body)
3. If adding or removing a spec, run `mdllm coherence` — it now mechanically checks the catalog slice of the dark region (`.markdownllm` `foundational_specs` ↔ files on disk, the `TIERS` map in `tools/mdllm.py` ↔ the catalog, and `kernel.md` drift), and it runs in the pre-commit hook so a stale generated artifact blocks the commit. Then walk the **prose-only residue** the tool cannot read (see `change-reconciliation.md` → Walking the Dark Region): the Tier 2 routing table and the spec catalog in this file, and `docs/framework-map.md` (View 1 counts + View 2 node). `mdllm kernel` regen is now caught by coherence rather than left to memory.
4. Commit with a structured message following git-workflow.md conventions (the commit is the backward record)

## Framework Specifications (Things)

The framework defines itself through these interconnected specifications:

### Foundational
- **llm-driven-systems.manifesto.md** — Philosophy, paradigm shift, core principles. The "why." (`type: manifesto`, `status: stable`)
- **thing.md** — The atomic unit specification: schema definition, field reference, cohesion and decomposition principle. (`type: specification`, `status: evolving`)

### Operational
- **read.thing.md** — How LLMs read and reason about things without modification. (`type: specification`, `status: stable`)
- **write.thing.md** — How LLMs create, update, and manage things. (`type: specification`, `status: stable`)
- **validate.thing.md** — How to validate thing integrity (structural, referential, semantic). (`type: specification`, `status: stable`)
- **interface.md** — The I/O layer: input routes, output types, deliverables vs things. (`type: specification`, `status: stable`)
- **git-workflow.md** — Git as state machine: commit points, conventions, event stream, autocommit mode. (`type: specification`, `status: stable`)
- **orchestration.md** — Hook points, prompts, and bindings: an opt-in pattern for domains that need structured orchestration. (`type: specification`, `status: evolving`)
- **session-memory.md** — How sessions preserve generative knowledge: `type: insight` things and the domain `continuity-brief`. Defines the session-end continuity ritual (invoked via the `session-end-continuity` bound prompt — explicit, not automatic). (`type: specification`, `status: stable`)
- **belief-revision.md** — How the framework handles contradictions between things: `type: conflict`, `relation: supersedes`/`contradicts`, and the belief revision process. (`type: specification`, `status: stable`)
- **retrospective.md** — Periodic domain quality reflection: `type: retrospective`, when to write one, and how it produces insights, surfaces latent conflicts, and improves reasoning over time. (`type: specification`, `status: stable`)
- **framework-discovery.md** — How domain agents locate the framework root and foundational specs. (`type: specification`, `status: stable`)
- **domain-refresh.md** — How domain agents discover framework evolution and update themselves. Deployment architecture (nested repos, .gitignore isolation) and the refresh process. (`type: specification`, `status: evolving`)
- **trigger-specification.md** — Declarative attention signals: all trigger types, condition values, action values, evaluation semantics, and idempotency. Extends thing.md. (`type: specification`, `status: stable`)
- **derived-index.md** — The derived-index pattern: regenerable caches (`type: index`) that aggregate one signal — triggers, relationships, schema fields — across a domain so reflexive behaviour stays cheap at scale. Drift-safe by construction (provenance + validation rebuild-and-diff). Opt-in, deploy-when-felt. (`type: specification`, `status: draft`)
- **provenance.md** — Output traceability: `type: decision` records with inputs pinned to git commits (`informed_by`), `origin: external` quarantine for ingested content, the knowledge → decision → output chain, and the reverse-provenance index that enables diff-driven regeneration. Mechanically enforced by `mdllm provenance`. (`type: specification`, `status: draft`)
- **change-reconciliation.md** — How a domain stays consistent across change: the human declares an inflection, then a scale-free four-beat pass (cue → assimilate → walk → seal) reconciles the change against its blast radius using the relationships and reverse-provenance indexes. Semantic consistency is maintained at the point of change, not by sweeping. (`type: specification`, `status: draft`)
- **workflow-state.md** — Workflow run-state as a primitive: `workflow-definition` (stages as data + allowed transitions) and `workflow-run` (a structural `definition` pointer, a `current_stage` cursor, resume in the body). The decomposition principle applied to processes; the floor enforces `current_stage` ∈ the definition's stages, the agent judges transition legality. Reserved, and now `evolving` — exercised on a live domain. (`type: specification`, `status: evolving`)
- **coordination-claim.md** — The advisory-claim convention (`held_by` + optional `held_until` lease) for same-target contention: read-and-respected, not a lock; deploy-when-felt on a contended thing. General, not workflow-specific — `workflow-run` and `continuity.md` are its consumers. (`type: specification`, `status: draft`)

- **example-things.md** — Full specification for `type: example` things: frontmatter template, when to use examples, and why examples work better than rules for inductive LLM learning. (`type: specification`, `status: stable`)
- **reasoning-lenses.md** — Canonical multi-lens reasoning spec: how to apply lenses in read mode and write mode, compliance domain examples, and how to surface and handle conflicts. (`type: specification`, `status: stable`)

### Guides
- **scalability-guide.md** — How to scale from tens to thousands of things. (`type: guide`, `status: stable`)
- **domain-specification-guide.md** — How to create a new domain using the framework. (`type: guide`, `status: stable`)
- **docs/operator-guide.md** — Human-facing: what working in a domain feels like since v3, the mdllm toolbox with scenarios, and what remains the operator's job. The specs are agent-first; this is the human's walkthrough. (`type: guide`, `status: draft`)
- **docs/first-hour.md** — Human-facing: a newcomer's first sixty minutes — orientation, scaffolding a first domain, installing the floor, one real session. Covers arrival; the operator-guide covers the steady state. (`type: guide`, `status: draft`)
- **docs/framework-map.md** — Visual architecture map (Mermaid): the five-band elevation, the spec-layer dependency graph, and the mdllm subcommand → spec mapping. Derived from frontmatter links, `mdllm --help`, and the tier table; the frontmatter wins on disagreement. (`type: guide`, `status: draft`)

### Deferred (Spec When Foreseeable, Deploy When Felt)
- **thing-lifecycle.md** — Rolling window, disposition to stubs, rehydration from git history, manifest index. Addresses the 200–300 thing ceiling. (`type: specification`, `status: draft`)

### Examples
Each example is its own corpus with its own `_schema.yaml`; `mdllm validate` run at the framework root validates them in the same pass (they are excluded from the framework corpus walk — separate id space — but not from the floor).
- **examples/life-manager/** — Personal life and work management domain (populated demonstration dataset; one deliberately overdue task for `mdllm triggers`)
- **examples/compliance-patterns/** — Regulatory compliance pattern library

### Templates
- **templates/** — Starting-point templates for AGENTS.md, skills, and workflows

## Framework Principles (Applied To Itself)

1. **Definition-Driven** — Humans define the constraints; LLMs reason within them. Not prompt-driven, not fully autonomous — definition-driven. The structure is the interface.
2. **Self-Describing** — The framework is a domain within itself. Its specifications are things with frontmatter, relationships, statuses, and versions.
3. **Atomic & Composable** — Each spec is self-contained but explicitly linked to others. You can read any one spec independently, but together they form a complete system.
4. **Minimal Core, Emergent Detail** — Start with the essential structure. Let the schema grow with domain needs. Never over-engineer upfront; add complexity only when it earns its place.
5. **Evolving** — Specifications have status (`draft`, `evolving`, `stable`). New specs start as drafts and mature through use.
6. **Vendor Agnostic** — This AGENTS.md works with GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, Gemini CLI. No vendor-specific memory stores required — the framework is the memory.
7. **Transparent & Auditable** — Every decision, every state change, every reasoning step is committed to git. Full history is always available.
8. **Git-Backed** — Git is the state machine, not just version control. Commit messages are the event stream and carry the session narrative (`mdllm worklog` prints an on-demand view; nothing is committed back).
9. **Elegant Constraint Enables Efficiency (hypothesis, under test)** — Structure makes reasoning consistent across sessions and vendors — that much is demonstrated. The stronger claim that a *smaller* model with structure matches or beats a *larger* model without it is the framework's central **hypothesis**, not a proven result: it rests on one eval whose reasoning core saturated, and stays a hypothesis until a more discriminating fixture tests it. Keep this distinct from the framework's *utility*, which independent adoption evidences directly. (See the manifesto, "Elegant Constraint Enables Efficiency.")

## Thing Types In This Domain

- `type: manifesto` — Philosophical vision and paradigm (one instance)
- `type: specification` — Foundational definitions of how things work
- `type: skill` — Reusable capabilities the agent can invoke
- `type: guide` — Operational guidance for using the framework
- `type: insight` — An emerging idea, held view, or hypothesis from a session, preserved for future context (framework-reserved)
- `type: continuity-brief` — The domain's live forward-looking session-continuity document; one per domain (framework-reserved)
- `type: conflict` — A documented contradiction between two things, held as a first-class thing until resolved (framework-reserved)
- `type: retrospective` — A periodic quality reflection on domain reasoning; one per period, not per session (framework-reserved)
- `type: decision` — A judgement made from knowledge, inputs pinned to git commits via `informed_by`; the provenance chain's middle link (framework-reserved)
- `type: index` — A regenerable cache aggregating one signal (triggers, relationships, schema) across a domain's things, in `things/_index/`; the things are the source of truth (framework-generated)
- `type: workflow-definition` — A reusable process skeleton with stages as data and the transitions allowed between them (framework-reserved)
- `type: workflow-run` — One live instance advancing through a `workflow-definition`: a `current_stage` cursor, an advisory `held_by` claim, and a resume narrative (framework-reserved)
- `type: plan` — A phased, multi-session work plan for evolving the framework; uses workflow statuses; phase checkboxes updated as work lands (domain-specific to the framework domain)

## Key Innovations

1. **Automatic Discovery** — AGENTS.md is discovered at workspace open. No manual includes, no configuration. The agent finds its own context.
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

- `draft` — First version, created but not yet validated through real-world use
- `evolving` — Actively being refined based on use and feedback
- `stable` — Proven through use, unlikely to change structurally
- `deprecated` — Superseded, kept for history

## Usage Pattern

```
User Request (about the framework or a domain)
    ↓ (auto-discovered)
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

> **The Deterministic Floor (v3.0):** mechanical validation (structural, referential, schema) is owned by `tools/mdllm.py` and enforced by the git pre-commit hook — never re-perform those checks by reasoning. The agent's validation responsibility is semantic only (validate.thing.md → Layer 2). Domain status vocabularies are declared in `_schema.yaml` / `things/_schema.yaml`, not fixed by the framework.
