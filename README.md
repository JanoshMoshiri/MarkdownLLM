# MarkdownLLM

A framework for building user-controlled, LLM-powered systems using markdown, YAML, and git.

## What Is This?

This is a specification and template set for creating **LLM-powered applications** where:

- **You define the domain** — the problem being solved, the atomic units of work, and how reasoning should work
- **An LLM reasons within that domain** — understanding context, making connections, suggesting improvements, making decisions
- **Git stores your data** — markdown files with structured metadata that you own completely
- **Multiple interfaces** — your phone, your voice, a chat application, an API—any interface layer you choose

These aren't traditional applications. They're **definition-driven systems** where the structure you define enables the LLM to be the reasoning engine, and you remain in control of all decisions and data.

## Why Does This Matter?

Traditional apps couple interface, logic, and storage tightly together. Change one thing, and you risk breaking others. Data is locked in databases. Logic is locked in code. You're locked into that vendor or platform.

This framework decouples those concerns entirely. Your data is just files. The logic is an LLM that understands your domain. The interface is whatever you want—your phone, a chat app, an API, a web interface.

**Key benefits:**

- **User agency** — You define your application. You're not locked into someone else's design.
- **Portability** — Your data is plain markdown. Move it anywhere. Use any LLM.
- **Composability** — Multiple applications coexist. Your project tracker can link to your knowledge base to your finances.
- **Efficiency** — Well-defined domains let smaller, cheaper LLMs handle complex work effectively.
- **Transparency** — Everything is versioned in git. You see exactly what changed and why.

## Core Principles

1. **Definition-driven** — Everything starts with clear definitions of what things are and how they work
2. **Atomic and composable** — Every unit is atomic; everything relates through explicit references
3. **Minimal core, emergent detail** — Start simple; let the schema grow with your needs
4. **LLM-centric structure** — Optimized for LLM reasoning, not human manual editing
5. **Vendor agnostic** — Use standard conventions so any LLM can understand your system
6. **Version-controlled** — Git is your source of truth for history and audit trail
7. **Transparent** — No black boxes; all rules and reasoning are explicit and readable

## What's Included

### Specification Files (Foundation)

These files define the pattern that applies to any domain:

- **llm-driven-systems.manifesto.md** — The philosophy and conceptual framework. Read this first to understand the paradigm shift.

- **thing.skill.md** — The specification for how atomic units work in this framework. Defines required and emergent metadata, structure, and linking. This is the template for any domain.

- **instructions-guide.md** — Step-by-step guide for creating domain definitions. Explains the complete domain structure: instructions, application, workflow(s), and prompts.

- **read.prompt.md** — Generic guide for Claude to read your system, understand context, and provide insights without modifying anything.

- **write.prompt.md** — Generic guide for Claude to read, reason, and actively update your system based on new information or requests.

- **scalability-guide.md** — Strategies for handling complex systems efficiently as they grow.

### Example Domain: Prototype-to-Production

The `domains/prototype-to-production/` folder shows a real instantiation of this framework applied to analyzing prototypes:

- **prototype-to-production.instructions.md** — Philosophy and principles specific to analyzing prototypes for production readiness.

- **prototype-to-production.application.md** — A thing that defines what the analysis application is and delivers.

- **analysis-workflow.md** — A thing that orchestrates the five-phase analysis process.

- **read.prompt.md** — Prototype-to-production-specific guidance for reading and analyzing things.

- **write.prompt.md** — Prototype-to-production-specific guidance for creating design decisions and requirements.

### How To Use These Files

1. **Understand the foundation** — Read the manifesto, thing.skill.md, and instructions-guide.md
2. **See it in action** — Look at the prototype-to-production domain to see how all five components fit together
3. **Adapt for your domain** — Use instructions-guide.md to create your domain with all five required components
4. **Interact with Claude** — Feed your definition files + data files + the appropriate prompt to Claude

## Getting Started With Your Own Domain

### Step 1: Define Your Domain Philosophy

Create a `domains/[domain]/[domain].instructions.md` file that explains:
- What you're building and why (the paradigm shift)
- The philosophy behind it
- How it differs from traditional approaches
- Key principles guiding your system
- Any domain-specific reasoning patterns (reasoning lenses)

### Step 2: Define Your Domain's Application

Create a `domains/[domain]/[domain].application.md` thing file that describes:
- What problem this domain solves
- What it delivers (inputs, process, outputs)
- How it works (which workflow(s) orchestrate it)
- Key principles and who uses it
- References to supporting files

### Step 3: Define Your Domain's Workflow(s)

Create one or more things with `type: workflow` or `type: process`:
- For simple domains: one workflow thing describing the main process flow
- For complex domains: multiple workflow/process things, each handling a different aspect
- The application thing references these via `linked_things`

Example: `domains/[domain]/[domain]-workflow.md`

### Step 4: Understand Your Atomic Unit

Read `thing.skill.md` — this is your specification for how things work. You don't need to redefine it; you just need to understand how to instantiate it for your domain.

### Step 5: Create Domain-Specific Prompts

Create two prompt files in `domains/[domain]/`:

- **read.prompt.md** — Tailor the generic read prompt to your domain
  - Explain thing types specific to your domain
  - Describe reasoning patterns (especially reasoning lenses)
  - Show examples of typical read-mode queries
  
- **write.prompt.md** — Tailor the generic write prompt to your domain
  - Explain how to create things with appropriate metadata
  - Describe decision-making patterns
  - Show examples of typical write-mode tasks

Both should reference:
- Your domain's instructions file
- Your domain's application file
- Your workflow thing(s)
- The generic `thing.skill.md` specification
- Domain-specific examples and terminology

### Step 6: Create Your Data

Create markdown files following the structure defined in `thing.skill.md`. Each file is an instance of your atomic unit, with YAML metadata and markdown narrative body.

### Step 7: Interact With Your LLM

Feed your definition files + relevant data files + the appropriate prompt to Claude or your preferred LLM. The LLM reads the definitions, understands the context, and either provides insights or makes updates.

### Step 8: Iterate

Update your definitions as you learn what works. Let the schema emerge. Commit everything to git.

## Example Applications

This framework applies to any domain that needs persistent state, relationship management, and LLM reasoning. Each application consists of five components working together:

### Life Management Application
**What it does:** Organize your life and work as a system of interconnected things

**Thing types:** Projects, tasks, subtasks, goals, recurring actions

**Metadata:** Status, priority, due date, dependencies, tags, energy cost

**Reasoning:** What's blocking progress? What's urgent? What patterns emerge?

**Workflow:** Single primary workflow managing task flow and dependencies

---

### Project Management Application
**What it does:** Plan and track complex projects with explicit dependencies and resource allocation

**Thing types:** Epics, stories, tasks, bugs, dependencies, resources

**Metadata:** Status, assignee, effort, priority, linked items, critical path

**Reasoning:** What's on critical path? What can start now? How do we allocate resources?

**Workflow:** May have multiple workflows (sprint planning, execution, retrospectives)

---

### Prototype-to-Production Analysis Application
**What it does:** Analyze whether a prototype can be safely and compliantly productionized

**Thing types:** Discovery items, data flows, gaps, design decisions, requirements

**Metadata:** Phase, severity, resolvability, three-lens alignment (Security/Compliance/Architecture)

**Reasoning:** Are constraints violated? Can we mitigate risks? Is this a blocker?

**Workflow:** Five-phase orchestration (Discovery → Data Flow → Gaps → Architecture → Outputs)

---

### Knowledge Management Application
**What it does:** Organize and synthesize knowledge from articles, notes, and research

**Thing types:** Articles, notes, ideas, topics, sources, connections

**Metadata:** Tags, related items, source, status (draft/published), topics covered

**Reasoning:** What gaps exist? What connections are there? What's unclear?

**Workflow:** Research intake → synthesis → publication workflow

---

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

1. Read your domain definitions (instructions, application, workflow, thing.skill.md)
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
- Create your definition files (instructions, application, workflow, prompts)
- Create data files as you work
- Interact with Claude using the prompts you've defined
- Own your data completely; your application lives in git

### For Building Team Applications
- Define shared domain applications
- Create shared definition files (instructions, application, workflows)
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
2. Read `thing.skill.md` — understand what a thing is and how it's structured
3. Look at `domains/prototype-to-production/` — see how a complete application is defined
4. Read `instructions-guide.md` — learn the five-component pattern for creating your own application
5. Create your domain following the pattern: instructions → application → workflow(s) → prompts
