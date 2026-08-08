---
name: Life Manager
description: A system for managing your life and work as interconnected things using LLM reasoning
version: 3.0
applies_to: "**/*.md"
framework_root: ../..
framework_version_seen: 3.29.0
---

# Life Manager Agent

## What This System Does

This system transforms how you manage your life by inverting the traditional app model. Instead of rigid interfaces and predefined schemas, you structure your life as atomic things in a git repository, and the LLM becomes your reasoning engine—understanding context, making connections, and helping you prioritize what matters.

## Framework Principles Applied to Life Management

1. **Atomic Units** — Everything is a thing: projects, tasks, goals, dependencies, recurring actions. No special cases.
2. **Minimal Core, Emergent Detail** — Start with basic metadata; let your schema grow as your life becomes more complex.
3. **LLM-Centric Structure** — Optimized for the LLM to reason about your life semantically, not for you to manually manage data.
4. **Vendor Agnostic** — Works with any capable LLM using standard markdown and YAML conventions.
5. **Versioned and Durable** — Git tracks your entire life management history; complete transparency and rollback capability.
6. **Self-Describing** — This domain is itself a thing within the MarkdownLLM framework. The specifications describe the system they govern.

## How This Agent Works

### On Startup
1. Version check (`session-start:version-check` hard hook): compare `{framework_root}/.markdownllm` version against `framework_version_seen` above
2. Load `{framework_root}/kernel.md` — the framework's operative rules; load a full spec only when the kernel doesn't settle an ambiguity
3. Read the orient view — `python {framework_root}/tools/mdllm.py session-start .` emits the open loops (non-terminal work things + open conflicts) carried from prior sessions; forward state is the thing graph, not a hand-kept brief
4. Load skills relevant to session intent: life-manager-specification.skill.md, life-manager-read.thing.skill.md, life-manager-write.thing.skill.md, life-manager-workflow.skill.md
5. Evaluate triggers — scan things for overdue items, unblocked dependencies, threshold breaches since last session

### On User Request
1. **Clarify intent** — What are they trying to accomplish? (Get status, plan next steps, resolve a blocker, understand connections?)
2. **Load relevant skill** — Match intent to appropriate skill (read.thing.skill for insights, write.thing.skill for updates)
3. **Load context** — Read relevant things from `./things/` (projects, tasks, goals, dependencies)
4. **Reason semantically** — Understand priorities, blockers, urgency, and wider implications
5. **Take action** — Update things, create new things, or provide insights

### On Output
1. Validate semantically if changes were made — statuses truthful, relationships meaningful; the mechanical layer (structure, references, schema) is owned by `mdllm validate` and the pre-commit hook
2. Commit with structured message (e.g., `create: task-buy-groceries`, `update: project-kitchen-reno status`)
3. Explain what changed and why
4. Evaluate triggers — check if writes unblocked dependencies or exceeded thresholds
5. Highlight new blockers or opportunities

## Skills Directory

All reusable capabilities for life management:

- **life-manager-specification.skill.md** — Philosophy, principles, and why this approach works
- **life-manager-read.thing.skill.md** — How to read your life, identify patterns, provide insights
- **life-manager-write.thing.skill.md** — How to create and update your life things
- **life-manager-workflow.skill.md** — The execution flow and decision patterns

## Foundational Specifications

Resolved from the MarkdownLLM framework root via `framework_root` (the kernel covers their operative rules; load a full spec on demand):

- **thing.md** — The atomic unit specification (structure for all things)
- **validate.thing.md** — The validation contract (mechanical layer: `mdllm`; semantic layer: the agent)
- **git-workflow.md** — When and how to commit (git as state machine)
- **interface.md** — I/O layer (input routes and output types)

## Things Directory

Your life as interconnected atomic units: `./things/`

> **Status of this example:** populated with a small fictional but realistic
> dataset — one project with three subtasks (one completed, one overdue, one
> blocked), a goal fed by a recurring habit, a weekly review, and a decision
> record with inputs pinned to git commits. One task is *deliberately* overdue
> so `mdllm triggers` has something to find. The domain validates under
> `mdllm validate` against `_schema.yaml`.

Thing types in this system (status vocabularies declared in `_schema.yaml`):
- `type: project` — A complete unit of work with phases and deliverables
- `type: task` — A discrete piece of work; hierarchy via `parent`, sequencing via `dependencies`/`blocks`
- `type: goal` — A desired outcome or state
- `type: recurring` — Something that happens regularly
- `type: decision` — A significant choice; framework-reserved, inputs pinned via `informed_by` (see `decision-hire-howell-joinery`)

## Triggers

Time, dependency, and threshold conditions are declared on the things
themselves and evaluated mechanically — run
`python {framework_root}/tools/mdllm.py triggers .` from this directory
(the example dataset always has at least one hit, by design). What remains
the agent's:

- **Acting on hits** — a fired trigger is an attention signal; deciding what
  to do with it is reasoning
- **Semantic conditions** — "more than 5 things in-progress, suggest focusing",
  "in-progress for 14+ days, flag it as possibly stale" — judgement calls the
  tool doesn't own
- **Idempotency** — after acting on a `review_date_reached` trigger, advance
  `review_date`; that update is what stops the trigger re-firing

## Usage Pattern

```
Your Request
    ↓ (auto-discovered)
Load Life Manager AGENTS.md
    ↓
Evaluate triggers (session start)
    ↓
Load appropriate skill (read, write, workflow)
    ↓
Load relevant things (projects, tasks, goals)
    ↓
Reason semantically about your life and request
    ↓
Validate semantically (the hook owns the mechanical layer)
    ↓
Commit with structured message
    ↓
Evaluate triggers (post-write)
    ↓
Report what changed + why
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

Mechanical validation (structure, references, declared vocabularies) is owned
by `mdllm validate` and enforced by the pre-commit hook — never re-perform it
by reasoning. Before committing, verify what the tool cannot:

- [ ] Relevant skill loaded (read.thing.skill or write.thing.skill)
- [ ] Statuses truthful, not merely valid
- [ ] Relationships meaningful (the right relation, not just a resolvable id)
- [ ] Changes scoped appropriately; narrative bodies updated to match reality
- [ ] Commit message follows `action: description` convention
