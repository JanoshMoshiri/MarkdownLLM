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
1. If modifying specifications: validate consistency across linked specs
2. If creating new specs: follow thing.md patterns (frontmatter + narrative body)
3. **Autocommit**: stage changed files + commit with structured message following git-workflow.md conventions

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

1. **Self-Describing** — The framework is a domain within itself. Its specifications are things with frontmatter, relationships, statuses, and versions.
2. **Atomic & Composable** — Each spec is self-contained but explicitly linked to others. You can read any one spec independently, but together they form a complete system.
3. **Evolving** — Specifications have status (`draft`, `evolving`, `stable`). New specs start as drafts and mature through use.
4. **Vendor Agnostic** — This AGENTS.md works with GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, Gemini CLI.
5. **Git-Backed** — All framework evolution is committed with structured messages. The WORKLOG captures session narrative. Git log captures state changes.

## Thing Types In This Domain

- `type: manifesto` — Philosophical vision and paradigm (one instance)
- `type: specification` — Foundational definitions of how things work
- `type: skill` — Reusable capabilities the agent can invoke
- `type: guide` — Operational guidance for using the framework

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
