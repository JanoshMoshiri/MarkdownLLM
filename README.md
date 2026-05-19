# MarkdownLLM

A specification and framework for building definition-driven, LLM-powered systems using markdown, YAML, and git.

## What Is This?

MarkdownLLM enables you to create **LLM-powered systems where**:

- **You define the domain** — atomic units, workflows, and reasoning patterns
- **An LLM reasons within that domain** — understanding context, making connections, suggesting improvements
- **Git stores your data** — markdown files with structured metadata that you control completely
- **Discovery works automatically** — your agent file loads at startup; skills auto-resolve; context persists

These systems work across vendor boundaries—use Claude, Codex, Gemini, or any LLM. The framework itself is vendor-agnostic.

## The Architecture: Three Layers

MarkdownLLM is built on a simple, elegant model:

```
AGENT.md (Orchestration & Discovery)
      ↓ auto-loads at startup
SKILLS/ (Reusable Capabilities)
      ↓ specifications, prompts, workflows as .skill.md files
THING.md (Foundational Specification)
      ↓ atomic unit definition
THINGS/ (Data Instances)
      → instances following thing.md structure
```

### Layer 1: Agent (Orchestration & Discovery)

Your **AGENTS.md** file sits at the root of your domain and is automatically discovered by the LLM tool/harness when a session starts. It:

- **Auto-loads** — No manual includes needed; the discovery mechanism finds it
- **Orchestrates** — Tells the LLM which skills to load and how to use them
- **Sets the protocol** — Defines behavioral rules and reasoning patterns
- **Bootstraps context** — Ensures the vision and structure persist across sessions

This solves the "lost context on new session" problem: the agent is always the entry point.

### Layer 2: Skills (Reusable Capabilities)

**Skills** are atomic, reusable capabilities. Each `.skill.md` file contains:

- **YAML frontmatter** — Metadata (name, type, applies_to patterns, dependencies)
- **Markdown narrative** — Detailed guidance for that capability

**Skill types in your domain:**

- **Specification Skill** (`[domain]-specification.skill.md`) — Philosophy, principles, domain paradigm, reasoning patterns
- **Read Thing Skill** (`[domain]-read.thing.skill.md`) — How to analyze things without modification
- **Write Thing Skill** (`[domain]-write.thing.skill.md`) — How to create and update things
- **Workflow Skill** (`[domain]-workflow.skill.md`) — Process orchestration and execution flow
- **Foundational Specification** (`thing.md`) — Specification for atomic units (works across all domains, not a skill file)

Skills are completely vendor-agnostic—they use standard markdown + YAML. This means they work across GitHub Copilot, Claude Code, OpenAI Codex, Cursor, Windsurf, and Gemini CLI.

### Layer 3: Things (Data Instances)

**Things** are your actual data—each is a markdown file with YAML frontmatter and narrative:

```yaml
---
id: unique-identifier
type: domain-specific-type
status: draft/active/complete
created: ISO-datetime
linked_things:
  - id: related-id
    relation: relationship-type
---

# Thing Title

## Summary
Brief overview

## Content
Detailed narrative
```

All things follow `thing.md` patterns. Your domain instantiates it for specific types (projects, requirements, analyses, etc.).

---

## Why This Structure?

### Problem: Context Loss Across Sessions

Traditional LLM-powered systems rely on manual includes or context passing. When you start a new session, you have to remember to load the system definition. Worse, you might load partial definitions, leading to inconsistent behavior.

**MarkdownLLM solves this:** AGENTS.md is automatically discovered at root. It loads first. Every session has the complete orchestration and can resolve all skills.

### Solution: Automatic Discovery + Composable Skills

- **Agent files are discovered**, not included — They're the entry point by design
- **Skills are composable** — Each skill stands alone but references others; no complex dependency chains
- **Things are atomic** — Each instance is self-contained but links to related instances through explicit relationships

This is how leading AI systems (OpenAI, Anthropic, Google) structure agent frameworks. MarkdownLLM applies that pattern to any domain you want to build.

---

## What's Included

### Foundation Files

These files define the pattern; they apply to any domain:

- **llm-driven-systems.manifesto.md** — The philosophy. Read this first to understand why this works.

- **thing.md** — The specification for the atomic unit. Defines metadata, structure, linking, and relationships.

- **domain-specification-guide.md** — Complete guide for creating a domain using the three-layer model. Step-by-step with templates.

- **read.thing.md** — Generic guidance for how LLMs should read your system (get insights without modifying data).

- **write.thing.md** — Generic guidance for how LLMs should read, reason, and update your system.

- **scalability-guide.md** — Strategies for handling complex systems as they grow.

### Example Domains

Example instantiations showing how to apply the framework:

- **examples/compliance-patterns/** — Shows how to structure a domain around regulatory compliance (GDPR example)
- **examples/life-manager/** — Shows how to structure a domain for personal task and project management

Each example has:
- Its own skills directory (specification, read/write prompts, workflow)
- Thing files demonstrating the domain's atomic units
- Comments showing how the pieces fit together

### Templates (Future Organization)

As you create your own domains, you'll use templates:
- `templates/AGENTS.md.template` — Starting point for orchestration
- `templates/[domain]-specification.skill.md.template` — Starting point for philosophy/principles
- `templates/[domain]-read.thing.skill.md.template` — Starting point for read guidance
- `templates/[domain]-write.thing.skill.md.template` — Starting point for write guidance
- `templates/[domain]-workflow.skill.md.template` — Starting point for process patterns

---

## How To Use This Framework

### Step 1: Understand the Foundation

Read these in order:
1. **llm-driven-systems.manifesto.md** — Understand the philosophy
2. **thing.md** — Understand the atomic unit
3. **domain-specification-guide.md** — Understand how to create domains

### Step 2: See It In Action

Explore `examples/life-manager/` or `examples/compliance-patterns/`:
- Look at how the specification skill defines philosophy
- See how read/write prompts tailor guidance to the domain
- Notice how thing files instantiate the spec

### Step 3: Create Your Domain Repository

For your own domain, create a new repository (or directory) with:

```
my-domain-repo/
├── AGENTS.md              ← Discovered at startup
├── thing.md               ← Foundational spec (from MarkdownLLM)
├── skills/                ← Reusable capabilities
│   ├── [domain]-specification.skill.md
│   ├── [domain]-read.thing.skill.md
│   ├── [domain]-write.thing.skill.md
│   └── [domain]-workflow.skill.md
├── things/                ← Data instances
│   ├── thing-1.md
│   ├── thing-2.md
│   └── ...
└── docs/
    └── Extended documentation (optional)
```

### Step 4: Define Your Domain

Using **domain-specification-guide.md** as your template:

1. **Create AGENTS.md** — Orchestration entry point
2. **Create skills/** — All four skill types for your domain
3. **Create things/** — Examples of your atomic units
4. **Enable tooling** — Configure your LLM tool (GitHub Copilot, Claude Code, etc.)

### Step 5: Interact With Your LLM

Feed your AGENTS.md + relevant skills + relevant things to your LLM. The LLM:
- Reads the agent for orchestration
- Loads skills for guidance
- Reads things for context
- Executes with consistency

### Step 6: Iterate and Grow

As you work:
- Update skills when you learn what works better
- Add new thing types when your schema evolves
- Commit everything to git (it's your audit trail)
- Let structure emerge from use

---

## Vendor Tooling Integration

The framework works across different LLM tools. Configure based on what you use:

### GitHub Copilot (in VS Code)

Enable AGENTS.md support in your VS Code settings:

```json
{
  "chat.useAgentsMdFile": true,
  "chat.useNestedAgentsMdFiles": true
}
```

This tells Copilot to auto-discover AGENTS.md at your workspace root.

### Claude Code (Standalone)

Claude Code looks for `CLAUDE.md` at root. You can create a simple wrapper:

```markdown
---
name: [Domain]
description: What this domain does
---

# [Domain] - Claude Code Instructions

@AGENTS.md

[Optional Claude-specific rules]
```

### OpenAI Codex, Cursor, Windsurf, Gemini CLI

These tools auto-discover `AGENTS.md` at root—no special configuration needed.

---

## The Elegant Constraint

A well-defined domain makes even a small model powerful. An undefined domain makes even the largest model mediocre.

This is the framework's core insight: **structure beats scale.** When an LLM operates within a clearly defined domain — with explicit thing types, known relationships, declared triggers, and validated integrity — it reasons with precision and consistency. Without that structure, the same LLM produces vague, inconsistent, and unreliable output regardless of its parameter count.

What this means in practice:

- A **smaller, cheaper model** with a well-defined MarkdownLLM domain will outperform a larger, expensive model with no structure — because the domain constrains reasoning to what matters and eliminates ambiguity
- **Consistency compounds** — every session builds on committed state, validated things, and structured history. The agent doesn't start from zero; it starts from a rich, reliable context
- **Cost scales with precision, not volume** — tiered context loading means the agent loads only what it needs. A broad question scans metadata. A deep question loads full context. You pay for what you use
- **The domain is the product** — the LLM is replaceable (vendor agnostic); the domain definition is the durable asset. Your investment is in defining the domain well, not in picking the right model

This is why the framework exists. Not to add complexity, but to provide the minimal structure that makes LLM reasoning reliable across sessions, across vendors, and across scale.

---

## Core Principles

These principles guide everything in MarkdownLLM:

1. **Definition-Driven** — Structure emerges from clear definitions, not from rigid templates
2. **Atomic & Composable** — Everything is a thing; everything links explicitly
3. **Minimal Core, Emergent Detail** — Start simple; let the schema grow with use
4. **LLM-Centric** — Optimized for how LLMs reason, not for manual editing
5. **Vendor Agnostic** — Works across Claude, Codex, Gemini, and others
6. **Version-Controlled** — Git is your source of truth
7. **Transparent** — No black boxes; all logic is explicit and readable

---

## Frequently Asked Questions

### "Why not just prompt engineering?"

Prompt engineering works for small, one-off tasks. But as systems grow:
- You lose context across sessions (frameworks prevent this)
- You have inconsistent reasoning patterns (skills formalize patterns)
- You can't reuse logic across domains (skills are composable)
- You can't audit what changed (git gives you a complete history)

MarkdownLLM takes proven patterns from enterprise LLM systems and applies them to *any* domain.

### "Why markdown and YAML?"

- **Markdown** is human-readable, version-control friendly, and LLM-friendly
- **YAML** is simple enough for humans to edit, rich enough for structure
- **Git** gives you free versioning, diffing, blame, and history
- Together, they're portable across any LLM and any tool

### "Can I use this with [favorite model/tool]?"

If it supports markdown and YAML, yes. MarkdownLLM is vendor-agnostic. It works with:
- OpenAI Codex ✓
- GitHub Copilot ✓
- Anthropic Claude (direct API) ✓
- Claude Code ✓
- Google Gemini CLI ✓
- Cursor ✓
- Windsurf ✓
- Any LLM that can read files ✓

### "How do I version and update skills?"

Skills have a `version` field in their frontmatter. As skills evolve:
- Update the version number
- Git tracks the change
- Your thing files continue working with old skills until you deliberately update

This lets you evolve guidance without breaking existing data.

### "Is this production-ready?"

The framework itself is production-ready (and used in production systems). The examples are complete and usable, but you'll adapt them to your specific domain.

---

## Getting Started

1. **Read** `llm-driven-systems.manifesto.md` (10 min)
2. **Read** `thing.md` (10 min)
3. **Read** `domain-specification-guide.md` (30 min, reference as you build)
4. **Explore** one example domain: `examples/life-manager/` or `examples/compliance-patterns/`
5. **Create** your own domain repository using the structure described above
6. **Build** your first domain with AGENTS.md, skills, and things
7. **Interact** with your LLM and iterate

---

## Contributing

This is a specification, not a closed system. If you:
- Create a domain using this framework
- Discover patterns that should be documented
- Find gaps or unclear guidance
- Want to add examples

You're invited to contribute back. The goal is for MarkdownLLM to grow with real-world use.

---

## License

[Your chosen license—typically MIT or similar for frameworks]

---

## Questions?

See `domain-specification-guide.md` for comprehensive guidance, or open an issue with questions about how to apply the framework to your domain.

### Financial Tracking Application
**What it does:** Track spending, budgets, and financial patterns; enable data-driven financial decisions

**Thing types:** Transactions, accounts, budgets, goals, categories

**Metadata:** Amount, category, date, account, tags, recurring status

**Reasoning:** What spending patterns exist? Where can we optimize? What anomalies?

**Workflow:** Transaction capture → categorization → analysis workflow

---

### Health & Fitness Application
**What it does:** Track health and fitness activities; reason about patterns and progress

**Thing types:** Workouts, meals, sleep logs, health goals, metrics

**Metadata:** Date, type, duration, metrics, intensity, notes

**Reasoning:** What patterns exist? Progress toward goals? What adjustments needed?

**Workflow:** Data capture → pattern analysis → adjustment recommendation workflow

---

### Creative Writing Application
**What it does:** Structure and develop stories while keeping narrative free-form

**Thing types:** Stories, characters, scenes, arcs, plot points, ideas, notes

**Metadata:** Status, tags, related items, word count, emotional tone, continuity notes

**Reasoning:** Character consistency? Plot continuity? Narrative flow? Pacing?

**Workflow:** Ideation → outlining → drafting → revision → publication workflow

## How This Works With LLMs

You're not asking the LLM to figure out your application and solve your problems simultaneously. You've already defined the application. Now the LLM just needs to:

1. Read your domain definitions (AGENTS.md, skills/, thing.md structures)
2. Understand the atomic units and reasoning patterns
3. Parse your data (instances) and understand the context
4. Apply reasoning within those clear constraints
5. Provide insights or make updates according to the domain rules

This is far more reliable and efficient than free-form prompting. A smaller, cheaper LLM can handle complex applications because the application itself provides the structure and boundaries.

## Elegant Constraint Enables Efficiency

The dominant assumption in the LLM space is: bigger models are always better.

This framework inverts that. When you provide clear domain definitions, explicit rules, and structured data, even smaller LLMs can reason effectively about complex systems. The complexity isn't in the model—it's in how well the system is defined.

A well-designed system using a smaller model beats a poorly-designed system using a larger model.

## Using This Framework

### For Building Personal Applications
- Define a domain and its application
- Create your definition files (AGENTS.md, specification.skill.md, read/write.skill.md, workflow.skill.md)
- Create data files as you work
- Interact with Claude using the prompts you've defined
- Own your data completely; your application lives in git

### For Building Team Applications
- Define shared domain applications
- Create shared definition files (AGENTS.md at root, shared skills/, shared things/)
- Use git for collaboration on both definitions and data
- Multiple people can work within the same application
- Merge, branch, resolve conflicts like any git project
- Shared definitions ensure consistency across team

### For Building Organizational Applications
- Different teams define their own applications and domains
- Teams link applications together (project manager links to knowledge base links to financials)
- Shared definitions at the organizational level ensure consistency
- Git audit trail for compliance, governance, and transparency
- Applications can be composed and integrated without tight coupling

## License

This framework is released under the MIT License. See LICENSE file for details.

Copyright © 2026 JMYM Software Ltd. All rights reserved.

## Contributing

This is a template and specification. Fork it, adapt it, make it your own. If you create domain definitions or examples you think would be useful, consider contributing them back.

## Questions?

This is a new way of thinking about systems and LLM collaboration. Read the manifesto. Try building something small. See what works. Iterate.

Your system will be unique to your needs. That's the point.

---

**Start here:**

1. Read `llm-driven-systems.manifesto.md` — understand the philosophy and paradigm shift
2. Read `thing.md` — understand what a thing is and how it's structured
3. Look at `examples/life-manager/` or `examples/compliance-patterns/` — see how a complete domain is structured
4. Read `domain-specification-guide.md` — learn the three-layer pattern (Agent → Skills → Things) for creating your own domain
5. Create your domain repository following the pattern: AGENTS.md at root, then skills/ and things/ directories
