# MarkdownLLM

A framework for building user-controlled, LLM-powered systems using markdown, YAML, and git.

## What Is This?

This is a specification and template set for creating systems where:

- **You define the domain** — what things exist and how they relate
- **An LLM reasons within that domain** — understanding context, making connections, suggesting improvements
- **Git stores your data** — markdown files with structured metadata that you own completely
- **Your phone is the interface** — you talk to the LLM, receive notifications, see updates

It's not an app. It's a paradigm for how humans and LLMs can collaborate on complex systems.

## Why Does This Matter?

Traditional apps couple interface, logic, and storage tightly together. Change one thing, and you risk breaking others. Data is locked in databases. Logic is locked in code.

This framework decouples those concerns entirely. Your data is just files. The logic is an LLM that understands your domain. The interface is whatever you want—your phone, a chat app, an API.

**Key benefits:**

- **User agency** — You define your system. You're not locked into someone else's design.
- **Portability** — Your data is plain markdown. Move it anywhere. Use any LLM.
- **Composability** — Multiple domains coexist. Your projects can link to your knowledge base to your finances.
- **Efficiency** — Well-defined systems let smaller, cheaper LLMs handle complex work effectively.
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

- **read.prompt.md** — Generic guide for Claude to read your system, understand context, and provide insights without modifying anything.

- **write.prompt.md** — Generic guide for Claude to read, reason, and actively update your system based on new information or requests.

### Example Domain: Life Manager

The `domains/life-manager/` folder shows a real instantiation of this framework applied to life management:

- **life-manager.instructions.md** — The philosophy and principles specific to managing life and work as a system of interconnected things.

- **read.prompt.md** — Life-management-specific guidance for Claude in read-only mode.

- **write.prompt.md** — Life-management-specific guidance for Claude in read-write mode.

### How To Use These Files

1. **Understand the pattern** — Read the manifesto and look at thing.skill.md
2. **See it in action** — Look at the life-manager domain as an example
3. **Adapt for your domain** — Define your own domain following the same structure
4. **Interact with Claude** — Feed your definition files + data files + the appropriate prompt to Claude

## Getting Started With Your Own Domain

### Step 1: Define Your Domain

Create a `domains/[domain]/[domain].instructions.md` file that explains:
- What you're building and why
- The philosophy behind it
- How it differs from traditional approaches
- Key principles guiding your system

### Step 2: Understand Your Atomic Unit

Read `thing.skill.md` — this is your specification for how things work. You don't need to redefine it; you just need to understand how to instantiate it for your domain.

### Step 3: Create Domain-Specific Prompts

Create prompt files in `domains/[domain]/`:
- **read.prompt.md** — Tailor the generic read prompt to your domain
- **write.prompt.md** — Tailor the generic write prompt to your domain

Include references to:
- Your domain's instructions file
- The generic `thing.skill.md` specification
- Domain-specific examples and terminology

### Step 4: Create Your Data

Create markdown files following the structure defined in `thing.skill.md`. Each file is an instance of your atomic unit, with YAML metadata and markdown narrative body.

### Step 5: Interact With Your LLM

Feed your definition files + relevant data files + the appropriate prompt to Claude or your preferred LLM. The LLM reads the definitions, understands the context, and either provides insights or makes updates.

### Step 6: Iterate

Update your definitions as you learn what works. Let the schema emerge. Commit everything to git.

## Example Domains

This framework applies to anything that needs persistent state and reasoning:

### Life Management
- Things: projects, tasks, subtasks, goals, recurring actions
- Metadata: status, priority, due date, dependencies, tags
- Reasoning: what's blocking progress, what's urgent, what patterns emerge

### Project Management
- Things: epics, stories, tasks, bugs, dependencies
- Metadata: status, assignee, effort, priority, linked items
- Reasoning: what's critical path, what can start now, resource allocation

### Knowledge Management
- Things: articles, notes, ideas, topics
- Metadata: tags, related items, source, status (draft/published)
- Reasoning: identify gaps, suggest connections, synthesize across knowledge

### Financial Tracking
- Things: transactions, accounts, budgets, goals
- Metadata: amount, category, date, account, tags
- Reasoning: spending patterns, anomalies, optimization opportunities

### Health and Fitness
- Things: workouts, meals, sleep logs, health goals
- Metadata: date, type, duration, metrics, notes
- Reasoning: patterns, progress toward goals, adjustments needed

### Creative Projects
- Things: stories, characters, scenes, arcs, ideas
- Metadata: status, tags, related items, notes
- Reasoning: continuity, character development, narrative structure

## How This Works With LLMs

You're not asking the LLM to figure out your system and solve your problems simultaneously. You've already defined the system. Now the LLM just needs to:

1. Read your definitions and understand the rules
2. Parse your data and understand the context
3. Apply reasoning within those clear constraints
4. Provide insights or make updates

This is far more reliable and efficient than free-form prompting. A smaller, cheaper LLM can handle complex systems because the system itself provides the structure.

## Elegant Constraint Enables Efficiency

The dominant assumption in the LLM space is: bigger models are always better.

This framework inverts that. When you provide clear domain definitions, explicit rules, and structured data, even smaller LLMs can reason effectively about complex systems. The complexity isn't in the model—it's in how well the system is defined.

A well-designed system using a smaller model beats a poorly-designed system using a larger model.

## Using This Framework

### For Yourself
- Define your domain
- Create your data files
- Interact with Claude or your preferred LLM
- Own your data completely

### For Your Team
- Define shared domains
- Use git for collaboration
- Multiple people can work within the same system
- Merge, branch, resolve conflicts like any git project

### For Your Organization
- Different teams define their own domains
- Teams link across domains
- Shared definitions ensure consistency
- Git audit trail for compliance and transparency

## License

This framework is released under the MIT License. See LICENSE file for details.

Copyright © 2026 JMYM Software Ltd. All rights reserved.

## Contributing

This is a template and specification. Fork it, adapt it, make it your own. If you create domain definitions or examples you think would be useful, consider contributing them back.

## Questions?

This is a new way of thinking about systems and LLM collaboration. Read the manifesto. Try building something small. See what works. Iterate.

Your system will be unique to your needs. That's the point.

---

**Start here:** Read `llm-driven-systems.manifesto.md` to understand the philosophy. Then read `thing.skill.md` to understand the specification. Finally, look at `domains/life-manager/` to see how it's applied to a real domain.
