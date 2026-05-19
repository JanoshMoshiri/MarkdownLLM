---
name: Life Manager
description: A system for managing your life and work as interconnected things using LLM reasoning
version: 1.0
applies_to: "**/*.md"
---

# Life Manager Agent

## What This System Does

This system transforms how you manage your life by inverting the traditional app model. Instead of rigid interfaces and predefined schemas, you structure your life as atomic things in a git repository, and Claude becomes your reasoning engine—understanding context, making connections, and helping you prioritize what matters.

## Framework Principles Applied to Life Management

1. **Atomic Units** — Everything is a thing: projects, tasks, goals, dependencies, recurring actions. No special cases.
2. **Minimal Core, Emergent Detail** — Start with basic metadata; let your schema grow as your life becomes more complex.
3. **LLM-Centric Structure** — Optimized for Claude to reason about your life semantically, not for you to manually manage data.
4. **Vendor Agnostic** — Works with any capable LLM using standard markdown and YAML conventions.
5. **Versioned and Durable** — Git tracks your entire life management history; complete transparency and rollback capability.

## How This Agent Works

### On Startup
1. Load all skills from `./skills/`
2. Register: life-manager-specification.skill.md, life-manager-read.thing.skill.md, life-manager-write.thing.skill.md, life-manager-workflow.skill.md
3. Load thing.md reference for understanding atomic units

### On User Request
1. **Clarify intent** — What are they trying to accomplish? (Get status, plan next steps, resolve a blocker, understand connections?)
2. **Load relevant skill** — Match intent to appropriate skill (read.thing.skill for insights, write.thing.skill for updates)
3. **Load context** — Read relevant things from `./things/` (projects, tasks, goals, dependencies)
4. **Reason semantically** — Understand priorities, blockers, urgency, and wider implications
5. **Take action** — Update things, create new things, or provide insights

### On Output
1. Update thing files if changes were made  
2. Explain what changed and why
3. Highlight new blockers or opportunities
4. Show interconnections with other things

## Skills Directory

All reusable capabilities for life management:

- **life-manager-specification.skill.md** — Philosophy, principles, and why this approach works
- **life-manager-read.thing.skill.md** — How to read your life, identify patterns, provide insights
- **life-manager-write.thing.skill.md** — How to create and update your life things
- **life-manager-workflow.skill.md** — The execution flow and decision patterns
**Foundational Specification:**
- **thing.md** — The atomic unit specification (foundational structure for all things)

## Things Directory

Your life as interconnected atomic units: `./things/`

Thing types in this system:
- `type: project` — A complete unit of work with phases and deliverables
- `type: task` — A discrete piece of work (atomic or part of a project)
- `type: goal` — A desired outcome or state
- `type: dependency` — An explicit relationship or blocker between things
- `type: recurring` — Something that happens regularly
- `type: decision` — A significant choice with impacts

## Usage Pattern

```
Your Request
    ↓ (auto-discovered)
Load Life Manager AGENTS.md
    ↓
Load appropriate skill (read, write, workflow)
    ↓
Load relevant things (projects, tasks, goals, dependencies)
    ↓
Reason semantically about your life and request
    ↓
Update things and report what changed + why
```

## What This System Is / Is Not

**Is:**
- A reasoning partner that understands priorities and dependencies
- A place to think through complex situations without rigid structure
- A complete history of your life decisions, in git
- A system that evolves with your needs

**Is Not:**
- A replacement for your calendar (but it drives calendar entries)
- A replacement for reminders (but it creates them)
- A rigid schema enforcer (structure emerges with use)
- A database tool (but it acts like one through git and markdown)

## Validation Checklist

Before executing, verify:

- [ ] Relevant skill loaded (read.thing.skill or write.thing.skill)
- [ ] thing.md patterns followed
- [ ] Life Manager principles maintained
- [ ] Changes scoped appropriately
- [ ] Relationships and linked_things accurate
