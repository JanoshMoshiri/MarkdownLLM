---
name: MarkdownLLM Framework
description: A self-describing specification framework for building LLM-driven systems using markdown, YAML, and git
version: 2.3
applies_to: "**/*.md"
framework_root: .
git:
  autocommit: true
  branch: main
---

# MarkdownLLM Framework Agent

## What This System Is

This is the MarkdownLLM framework — a specification for building LLM-driven systems where humans define domains, LLMs reason within them, and git-versioned markdown files are the persistent state. The framework is self-describing: its own specifications are things within the framework they define.

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
1. Load all foundational specifications from root (thing.md, interface.md, git-workflow.md, framework-discovery.md, domain-refresh.md)
2. Load operational specs (validate.thing.md, read.thing.md, write.thing.md)
3. Load the manifesto for philosophical grounding (llm-driven-systems.manifesto.md)
4. Load the domain guide for operational context (domain-specification-guide.md)
5. Load supporting specs as needed (scalability-guide.md, orchestration.md)
6. Note: This agent operates in **autocommit mode** (`git.autocommit: true`). All state changes to framework specs are committed automatically.

### On User Request
1. **Clarify intent** — Is the user working on the framework itself? Creating a new domain? Asking about the philosophy? Seeking guidance?
2. **Load relevant specs** — Match intent to the appropriate specification or guide
3. **Load examples if needed** — Reference `examples/` for concrete demonstrations
4. **Execute** — Reason within the framework's own principles while helping the user

### On Output

> **[HARD HOOK: `post-write:commit`]** After creating or modifying any `.md` file with YAML frontmatter, commit it to the **owning repo** before completing the response. Walk up the directory tree from the modified file to find the correct `.git` root — never assume it is the framework repo. Full spec: `orchestration.md` → Hard Hooks.

> **[HARD HOOK: `pre-domain-scaffold:isolate`]** When scaffolding a new domain, the isolation sequence is mandatory and must complete before any domain files are committed anywhere: (1) `git init` in the domain folder, (2) add domain path to framework `.gitignore`, (3) commit `.gitignore` to framework repo, (4) commit domain files to domain repo, (5) create remote and push. Never commit domain files to the framework repo. Full spec: `orchestration.md` → Hard Hooks.

1. If modifying specifications: validate consistency across linked specs
2. If creating new specs: follow thing.md patterns (frontmatter + narrative body)
3. Commit with a structured message following git-workflow.md conventions
4. WORKLOG updated with session activity

## Framework Specifications (Things)

The framework defines itself through these interconnected specifications:

### Foundational
- **llm-driven-systems.manifesto.md** — Philosophy, paradigm shift, core principles. The "why." (`type: manifesto`, `status: stable`)
- **thing.md** — The atomic unit specification. What a thing is, how it's structured, triggers. (`type: specification`, `status: stable`)

### Operational
- **read.thing.md** — How LLMs read and reason about things without modification. (`type: specification`, `status: stable`)
- **write.thing.md** — How LLMs create, update, and manage things. (`type: specification`, `status: stable`)
- **validate.thing.md** — How to validate thing integrity (structural, referential, semantic). (`type: specification`, `status: stable`)
- **interface.md** — The I/O layer: input routes, output types, deliverables vs things. (`type: specification`, `status: stable`)
- **git-workflow.md** — Git as state machine: commit points, conventions, event stream, autocommit mode. (`type: specification`, `status: stable`)
- **orchestration.md** — Hook points, prompts, and bindings: an opt-in pattern for domains that need structured orchestration. (`type: specification`, `status: stable`)
- **framework-discovery.md** — How domain agents locate the framework root and foundational specs. (`type: specification`, `status: stable`)
- **domain-refresh.md** — How domain agents discover framework evolution and update themselves. Deployment architecture (nested repos, .gitignore isolation) and the refresh process. (`type: specification`, `status: stable`)

### Guides
- **scalability-guide.md** — How to scale from tens to thousands of things. (`type: guide`, `status: stable`)
- **domain-specification-guide.md** — How to create a new domain using the framework. (`type: guide`, `status: stable`)

### Examples
- **examples/life-manager/** — Personal life and work management domain
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
8. **Git-Backed** — Git is the state machine, not just version control. Commit messages are the event stream. The WORKLOG captures session narrative.
9. **Elegant Constraint Enables Efficiency** — Well-defined systems let smaller models perform reliably. Structure isn't overhead; it's the mechanism that makes reasoning consistent across sessions and vendors.

## Thing Types In This Domain

- `type: manifesto` — Philosophical vision and paradigm (one instance)
- `type: specification` — Foundational definitions of how things work
- `type: skill` — Reusable capabilities the agent can invoke
- `type: guide` — Operational guidance for using the framework

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

- [ ] Frontmatter present and complete (id, type, status, version, created, linked_things)
- [ ] linked_things references are valid (target specs exist)
- [ ] Status reflects reality (draft if new, evolving if actively changing)
- [ ] Version incremented if substantive change to a stable spec
- [ ] Commit message follows git-workflow.md conventions
- [ ] WORKLOG updated with session activity
