---
id: life-manager-specification
name: Life Manager Specification
type: specification
status: stable
version: 2.0
created: 2026-05-18
linked_things:
  - id: life-manager-read-thing-skill
    relation: informs
  - id: life-manager-write-thing-skill
    relation: informs
  - id: life-manager-workflow-skill
    relation: informs
description: Philosophy, principles, and paradigm for life management using LLM reasoning
applies_to: "life-manager/**/*.md"
---

# Life Manager Specification

## Philosophy

This is not an app. It is a paradigm shift in how life management works.

Traditional apps separate concerns: input happens through UI, processing happens in code, output is notifications and data views. You think about wiring these together, building conditional logic, managing state in databases.

This system inverts that model entirely.

**Processing:** Claude (or any capable LLM) becomes your reasoning engine. The agent understands context, makes sense of complexity, handles ambiguity, reasons about priorities and dependencies. This is not rule-based logic—it's semantic understanding.

**Interface:** Your phone is pure interface and notification hub. You talk to your agent. You receive reminders and calendar updates. The phone is how you interact and how you get notified.

**Storage:** Git repository with markdown files is your persistent state. Not because it's clever, but because it's durable, versioned, human-readable to Claude, and completely vendor-agnostic. Your life data lives in markdown. The LLM reads it, reasons about it, updates it.

## The Paradigm Shift

You stop thinking about "how do I build this app" and start thinking about "how do I structure my data so Claude can understand and reason about it."

The complexity doesn't disappear—it just moves. Instead of writing conditional logic and integration code, you're defining how Claude should think about your life. Instead of predefined schemas, you let structure emerge based on what your life actually needs.

## How It Works

1. Your life exists as a collection of "things" in a git repository
2. Each thing is a markdown file with YAML metadata and narrative body
3. When you need help, you talk to Claude (via your phone, via any interface)
4. Claude reads the relevant things, understands the structure and context
5. Claude reasons about what you're asking, what matters, what's next
6. Claude updates your thing files, creates reminders, updates your calendar
7. Your phone notifies you of changes and reminders
8. You talk to Claude again with new information or requests

The loop is: you → Claude → your data → Claude → you

## Why This Works

Claude doesn't need rigid schemas. It understands semi-structured data, can infer relationships, can reason about context. Your metadata defines enough structure for reliable parsing. Your narrative provides enough context for true understanding.

You're not fighting an app's architecture. You're partnering with an intelligence that understands your life as you describe it.

## Core Principles

**Atomic Units:** Everything is a thing. No special cases. A project, a task, a subtask, a dependency—all things. This creates consistency and composability.

**Minimal Core, Emergent Detail:** You start with minimal required metadata. As your life becomes more complex, new fields emerge naturally. Your schema grows with your needs, not ahead of them.

**LLM-Centric Structure:** The metadata and body are optimized for Claude to parse and reason with, not for you to read. Claude is the primary consumer. Readability for humans is secondary.

**Vendor Agnostic:** Uses standard conventions (AGENTS.md, .skill.md files, YAML frontmatter) so any LLM—Claude, Copilot, any other agent—can understand and operate within the system.

**Versioned, Durable:** Git means your entire life management system is versioned, backed up, and transparent. You can see how things evolved. You can roll back if needed.

## Thing Types in Life Manager

- **project** — A complete unit of work with phases and deliverables
- **task** — A discrete piece of work (atomic or part of a project)
- **goal** — A desired outcome or state (personal, professional, health, etc.)
- **dependency** — An explicit relationship, blocker, or prerequisite between things
- **recurring** — Something that happens regularly (weekly, monthly, etc.)
- **decision** — A significant choice with impacts on other things

## What This System Is Not

- Not a replacement for your calendar (but it drives calendar entries)
- Not a replacement for your reminders (but it creates them)
- Not a database (but it acts like one through git and markdown)
- Not rigid or predefined (but it has minimal structure to function)

## What This System Is

A way to externalize your life management to an intelligent partner while keeping your data completely in your control, in a format you can understand, in a repository you own.

## Domain-Specific Validation Rules

Beyond the universal structural checks (id, type, status, created present):

- Things of `type: project` should have at least one `linked_things` entry
- Things of `type: task` should have `priority` set
- Things of `type: goal` should have a narrative body explaining the desired outcome
- Status transitions should be logical: `not-started` → `in-progress` → `completed` (with `blocked`/`paused` as temporary states)

## Triggers

### Time-Based
- **Weekly review** — Every Monday, scan all active things for overdue items and stale work
- **Due date approaching** — 2 days before `due_date`, alert the user

### Dependency
- **Unblocked** — When a blocking thing completes, notify the user about newly unblocked work
- **New blocker** — When something becomes blocked, trace downstream impact

### Threshold
- **Overload** — More than 5 things `status: in-progress` simultaneously → suggest focusing
- **Stale work** — Thing `status: in-progress` for 14+ days without changes → flag for review
