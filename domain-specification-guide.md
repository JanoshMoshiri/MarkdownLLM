---
id: domain-specification-guide
type: guide
status: evolving
version: 2.1
created: 2026-05-13
linked_things:
  - id: llm-driven-systems-manifesto
    relation: operationalises
  - id: thing-specification
    relation: references
  - id: read-thing-specification
    relation: references
  - id: write-thing-specification
    relation: references
  - id: validate-thing-skill
    relation: references
  - id: git-workflow-specification
    relation: references
  - id: interface-specification
    relation: references
---

# Domain Specification Guide

This guide explains how to create a complete domain specification using the MarkdownLLM framework. The framework uses a **three-layer architecture**: Agent (orchestration) → Skills (reusable capabilities) → Things (data instances).

## The Three-Layer Architecture

### Layer 1: Agent (Orchestration & Discovery)
The **agent file** (`AGENTS.md` or `agent.md`) sits at the root of your domain and serves as the entry point for the LLM. It:
- Is automatically discovered by the tool/harness you're using (GitHub Copilot, Claude Code, Codex CLI, etc.)
- Orchestrates how skills should be loaded and used
- Defines the behavioral rules and protocols for your domain
- Loads once per session and bootstraps all context

**Key insight:** You don't have to manually include or reference the agent. When properly placed at root, it auto-loads. This ensures the vision and protocol are always part of the context, solving the "lost on new session" problem.

### Layer 2: Skills (Reusable Capabilities)
**Skills** are atomic, reusable capabilities that teach the LLM how to work within your domain. Every skill file has:
- **YAML frontmatter** — Metadata (name, description, type, version, applies_to patterns)
- **Markdown body** — Detailed narrative guidance

**Skill types in your domain:**
- **Specification Skill** (`[domain]-specification.skill.md`) — Philosophy, principles, and domain paradigm
- **Read Thing Skill** (`[domain]-read.thing.skill.md`) — How to read and analyze things
- **Write Thing Skill** (`[domain]-write.thing.skill.md`) — How to create and update things
- **Workflow Skill** (`[domain]-workflow.skill.md`) — Process orchestration and execution patterns
- **Definition Skill** (`thing.md`) — Specification for atomic units (shared across all domains)

Skills are agnostic to the tool or LLM—they use standard markdown + YAML, making them portable across Copilot, Claude, Codex, Gemini, etc.

### Layer 3: Things (Data Instances)
**Things** are the actual data your domain works with. Each thing is a markdown file with:
- **YAML frontmatter** — Metadata (id, type, status, created, relationships, etc.)
- **Markdown body** — Narrative content

Things follow the structure defined in `thing.md`. Your domain instantiates this spec for domain-specific thing types (projects, tasks, requirements, analyses, etc.).

---

## How These Three Layers Interact

```
┌─────────────────────────────────────────────────────────────┐
│ AGENT.md (Root)                                              │
│ ├─ Discovered automatically by tool/harness                  │
│ ├─ Orchestrates skills loading                               │
│ ├─ Defines behavioral rules                                  │
│ └─ Sets the vision and protocol for this session              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ SKILLS/ (Reusable Capabilities)                              │
│ ├─ [domain]-specification.skill.md (Philosophy & Principles)  │
│ ├─ [domain]-read.thing.skill.md (Read Guidance)             │
│ ├─ [domain]-write.thing.skill.md (Write Guidance)           │
│ ├─ [domain]-workflow.skill.md (Process Patterns)             │
│ └─ thing.md (Atomic Unit Specification)                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ THINGS/ (Data Instances)                                     │
│ ├─ thing-1.md (e.g., project)                                │
│ ├─ thing-2.md (e.g., task)                                   │
│ ├─ thing-3.md (e.g., requirement)                            │
│ └─ ... (atomic units following thing.md)               │
└─────────────────────────────────────────────────────────────┘
```

**How it works in practice:**

1. **Tool launches** → Finds and loads `AGENTS.md` at root
2. **Agent reads metadata** → Discovers which skills to load and when
3. **Agent loads relevant skills** → Instructions, read/write prompts, workflow patterns
4. **User makes request** → Agent interprets it using loaded skills
5. **Agent loads relevant things** → Reads thing files from `things/` directory
6. **LLM executes** → Using skills to guide reasoning + things to provide context
7. **Updates made** → Things in `things/` are modified/created; changes committed to git

---

## Framework Discovery

When a domain is nested inside a MarkdownLLM framework repository (e.g., at `domains/my-domain/`), the domain agent needs to locate the framework's foundational specs. Two mechanisms support this:

### 1. `framework_root` in Frontmatter (Primary)

Declare the relative path from the domain root to the framework root in your AGENTS.md frontmatter:

```yaml
framework_root: ../..
```

The agent resolves this at startup to load `thing.md`, `git-workflow.md`, `validate.thing.skill.md`, and `interface.md`.

### 2. `.markdownllm` Marker File (Fallback)

The framework root contains a `.markdownllm` file. If `framework_root` is not declared, the agent walks up the directory tree looking for this marker. This ensures discovery works even if frontmatter is incomplete.

### Standalone Domains

If your domain is deployed as its own repository (not nested), set `framework_root: .` and either copy the foundational specs into your root or include the framework as a git submodule.

See **framework-discovery.md** for the full specification.

---

## Domain Structure: What You Need to Create

Every domain requires these essential components in this structure:

```
my-domain-repo/              ← Root of deployed domain
├── AGENTS.md                 ← Discovered at startup (orchestration)
├── skills/
│   ├── [domain]-specification.skill.md
│   ├── [domain]-read.thing.skill.md
│   ├── [domain]-write.thing.skill.md
│   └── [domain]-workflow.skill.md (reference to MarkdownLLM spec)
├── things/
│   ├── thing-1.md
│   ├── thing-2.md
│   └── ...
└── docs/ (optional)
    └── Extended documentation
```

---

## Creating Your Agent File (AGENTS.md)

Your `AGENTS.md` at the root defines:
- What this domain is and what it accomplishes
- Which skills to load and when
- Behavioral rules and protocols
- How the LLM should approach problems in this context

**Template structure:**

```markdown
---
name: [Domain Name]
description: What this domain does
version: 1.0
applies_to: "**/*.md"
framework_root: ../..
git:
  autocommit: true
  branch: main
---

# [Domain Name] Agent

## What This System Does
[1-2 sentences describing the vision and capability]

## Framework Principles
[Reference to MarkdownLLM principles applied to this domain]

## How This Agent Works

### On Startup
1. Resolve `framework_root` from frontmatter to locate the MarkdownLLM framework root
2. Load foundational specs from framework root: thing.md, validate.thing.skill.md, git-workflow.md, interface.md
3. Load all skills from ./skills/
4. Register: [domain]-specification.skill.md, [domain]-read.thing.skill.md, [domain]-write.thing.skill.md, [domain]-workflow.skill.md
5. Evaluate triggers — scan things for time-based, dependency, or threshold triggers since last session

### On User Request
1. **Clarify intent:** What operation? (read, write, analyze, etc.)
2. **Load relevant skill:** Match to appropriate skill
3. **Load context:** Load relevant things from ./things/ directory
4. **Execute:** Follow skill guidance while maintaining consistency
5. **Validate:** After writes, invoke validation (structural, referential, domain-specific)
6. **Autocommit:** If `git.autocommit: true`, stage + commit with structured message

### On Output
1. Validate thing files if changes were made
2. **Autocommit** (if enabled): stage changed files + commit with structured `action: description` message
3. Report what changed and why
4. Evaluate triggers (post-write)

## Skills Directory

All reusable capabilities stored as skill files:

- **[domain]-specification.skill.md** — Philosophy and principles
- **[domain]-read.thing.skill.md** — Read and analyze things
- **[domain]-write.thing.skill.md** — Create and update things
- **[domain]-workflow.skill.md** — Process orchestration

## Foundational Specifications

- **thing.md** — Atomic unit specification
- **validate.thing.skill.md** — Validation skill
- **git-workflow.md** — Commit conventions
- **interface.md** — I/O layer

## Triggers (Domain-Specific)

### Time-Based
- [When time-based conditions should fire]

### Dependency
- [When dependency changes should alert]

### Threshold
- [When limits are exceeded]

## Usage Pattern

User Request
  ↓
Load this AGENTS.md (auto-discovered)
  ↓
Evaluate triggers (session start)
  ↓
Load relevant skill from ./skills/
  ↓
Load relevant things from ./things/
  ↓
Execute with consistency checks
  ↓
Validate changes
  ↓
Commit with structured message
  ↓
Evaluate triggers (post-write)
  ↓
Report changes

## Validation Checklist

- [ ] Relevant skill loaded for this operation
- [ ] thing.md patterns followed (id, type, status, created present)
- [ ] linked_things references valid (targets exist)
- [ ] Framework principles maintained
- [ ] Commit message follows `action: description` convention
```

---

## Creating Skills

Skills are the reusable building blocks of your domain. Each skill is a `.skill.md` file with YAML frontmatter and markdown narrative.

### Specification Skill (`[domain]-specification.skill.md`)

The philosophy and operational charter for your domain.

**Frontmatter:**
```yaml
---
id: [domain]-specification
name: [Domain] Specification
type: specification
status: draft
version: 1.0
created: [ISO-date]
linked_things:
  - id: [domain]-read-thing-skill
    relation: informs
  - id: [domain]-write-thing-skill
    relation: informs
description: Philosophy, principles, and reasoning patterns for [domain]
applies_to: "[domain]/**/*.md"
---
```

**Content sections:**

#### Philosophy
Why does this domain exist? What problem are you solving? Explain the paradigm shift. What traditional approaches fail? How does this framework improve on them?

#### Core Principles
List 4-7 core principles that guide how things work. Be specific enough to inform decisions, universal enough to apply across use cases.

**Examples:**
- "Atomic Units: Everything is a thing. No special cases."
- "Minimal Core, Emergent Detail: Start simple; let the schema grow with your needs."
- "LLM-Centric: Structure optimized for LLM reasoning, not manual editing."

#### Reasoning Patterns
If your domain uses specialized reasoning (lenses, frameworks, decision trees), document them here. Show examples.

#### How It Works
Describe the user interaction loop. How does a user interact with the LLM? What happens? How does data flow?

#### What This System Is / What It Is Not
Set clear boundaries. What is this system NOT trying to do? Integration points? This prevents feature creep.

### Read Thing Skill (`[domain]-read.thing.skill.md`)

Guidance for how LLMs should traverse, understand, and reason about things within your domain.

**Frontmatter:**
```yaml
---
id: [domain]-read-thing-skill
name: [Domain] Read Thing Skill
type: skill
mode: read
status: draft
version: 1.0
created: [ISO-date]
linked_things:
  - id: [domain]-specification
    relation: implements
description: How to read, analyze, and reason about [domain] things
applies_to: "[domain]/**/*.md"
---
```

**Content sections:**

- How to load and traverse things
- What thing types exist in this domain
- Reasoning patterns specific to your domain
- Examples of typical read-mode queries
- How to apply domain-specific analysis

**Base this on:** Generic `read.thing.md`, but tailored to your domain's instructions and workflow.

### Write Thing Skill (`[domain]-write.thing.skill.md`)

Guidance for how LLMs should create, update, and manage things within your domain.

**Frontmatter:**
```yaml
---
id: [domain]-write-thing-skill
name: [Domain] Write Thing Skill
type: skill
mode: write
status: draft
version: 1.0
created: [ISO-date]
linked_things:
  - id: [domain]-specification
    relation: implements
  - id: [domain]-read-thing-skill
    relation: complements
description: How to create, update, and manage [domain] things
applies_to: "[domain]/**/*.md"
---
```

**Content sections:**

- How to create new things with appropriate metadata
- How to update existing things based on user requests
- How to apply domain-specific reasoning (reasoning lenses)
- Decision-making patterns and when to ask for clarification
- Examples of typical write-mode tasks
- Dependencies, impacts, and consequence thinking

**Base this on:** Generic `write.thing.md`, but tailored to your domain's instructions and workflow.

### Workflow Skill (`[domain]-workflow.skill.md`)

Process orchestration and execution patterns for your domain.

**Frontmatter:**
```yaml
---
id: [domain]-workflow-skill
name: [Domain] Workflow
type: skill
mode: workflow
status: draft
version: 1.0
created: [ISO-date]
linked_things:
  - id: [domain]-specification
    relation: implements
  - id: [domain]-read-thing-skill
    relation: orchestrates
  - id: [domain]-write-thing-skill
    relation: orchestrates
description: Processes and orchestration patterns for [domain]
applies_to: "[domain]/**/*.md"
---
```

**Content sections:**

- Major phases or steps in your domain's process
- What happens at each phase
- Roles (if applicable) and checkpoints
- Handoff points and conditions for transition
- How complex domains orchestrate multiple workflows

For simple domains: one workflow describing the main process.
For complex domains: multiple workflow descriptions or reference to workflow things in `things/`.

---

## Creating Things

Things are instances of your atomic unit, following the structure defined in `thing.md`.

**Each thing file includes:**

```yaml
---
id: unique-identifier
type: [domain-specific-type]
status: [not-started/in-progress/blocked/paused/completed/cancelled]
created: ISO-datetime
linked_things:
  - id: related-thing-id
    relation: relationship-type
---

# Thing Title

## Summary
[1-2 sentence overview]

## Content
[Detailed narrative body]
```

Thing types are domain-specific but follow `thing.md` patterns for metadata, relationships, and structure.

---

## Vendor Tooling Integration

Different tools discover agent files differently. Configure your setup based on where your domain lives:

### If Using GitHub Copilot (in VS Code)

Enable AGENTS.md support in VS Code settings:

```json
{
  "chat.useAgentsMdFile": true,
  "chat.useNestedAgentsMdFiles": true
}
```

This tells GitHub Copilot to auto-discover `AGENTS.md` at the root of your workspace and any nested directories.

**Alternatively**, place instructions in `.github/copilot-instructions.md`:
```markdown
@AGENTS.md

[Optional Copilot-specific rules]
```

### If Using Claude Code Directly

Claude Code looks for `CLAUDE.md` at the root:

```markdown
---
name: [Domain]
description: What this domain does
---

# [Domain] - Claude Code Instructions

@AGENTS.md

[Claude Code specific behavior, if needed]
```

The `@AGENTS.md` reference tells Claude Code to read `AGENTS.md` first, then apply any Claude-specific rules.

### If Using OpenAI Codex, Cursor, Windsurf, or Gemini CLI

These tools auto-discover `AGENTS.md` at the root—no configuration needed.

---

## Getting Started: Step-by-Step

### Step 1: Plan Your Domain

Answer these questions:
- What problem does this domain solve?
- What are your atomic units (thing types)?
- What workflows or processes orchestrate them?
- What skills will the LLM need to reason effectively?

### Step 2: Create Your AGENTS.md

Write `AGENTS.md` at the root of your domain repository. This is your entry point—the file that auto-loads every session.

### Step 3: Create Your Skills

In `skills/` directory, create:
- `[domain]-specification.skill.md`
- `[domain]-read.thing.skill.md`
- `[domain]-write.thing.skill.md`
- `[domain]-workflow.skill.md`
- Copy or reference `thing.md` from MarkdownLLM

### Step 4: Understand Your Atomic Unit

Read `thing.md`—this is your specification for how things work. Instantiate it for your domain's thing types.

### Step 5: Create Your First Things

Create a few example things in `things/` following `thing.md` patterns and your domain-specific schema.

### Step 6: Test with Your LLM

Feed your AGENTS.md + skills + things to your LLM and test:
- Does the agent understand the domain?
- Does it follow the workflow?
- Does it reason according to your principles?

### Step 7: Iterate

Update skills and define new thing types as you learn what works. Commit everything to git.

---

## Minimal vs. Complex Domains

### Minimal Domain (1-2 workflows)

Essential skills, can be concise:

- **[domain]-specification.skill.md** — 500-800 words explaining philosophy, principles, and how it works
- **[domain]-read.thing.skill.md** — Domain-tailored read guidance  
- **[domain]-write.thing.skill.md** — Domain-tailored write guidance
- **[domain]-workflow.skill.md** — Single atomic workflow or process description
- **AGENTS.md** — Orchestration entry point

**Example:** Life Manager (simple task tracking), Prototype-to-Production (single five-phase analysis).

### Complex Domain (multiple workflows/processes)

All skills scale to handle complexity:

- **[domain]-specification.skill.md** — More detailed; may define multiple reasoning lenses
- **[domain]-read.thing.skill.md** — More detailed guidance for navigating complex domains
- **[domain]-write.thing.skill.md** — More detailed guidance for creating different thing types
- **[domain]-workflow.skill.md** — Multiple orchestration patterns or reference to workflow things
- **AGENTS.md** — Sophisticated orchestration with conditional logic

**Example:** Financial System (with transactions, budgets, investments), Large Enterprise Application (with multiple concurrent workflows).

---

## Domain-Specific Reasoning Patterns (Optional)

For domains with constraints, compliance requirements, or specialized reasoning, define **reasoning lenses** in your instructions skill.

### What Are Reasoning Lenses?

Reasoning lenses are frameworks that guide how LLMs should evaluate decisions. Instead of encoding constraints as rigid rules, you encode them as reasoning patterns the LLM naturally applies.

**Example: Compliance-Heavy Domain**

```markdown
## Reasoning Lenses

When working in this domain, reason through three perspectives:

### Lens 1: Domain Logic
What does this accomplish in the domain's terms? What's the business outcome?

### Lens 2: Compliance Logic
Would this violate GDPR, data residency, audit logs, or regulatory constraints? Can we mitigate?

### Lens 3: Audit Logic
Can we explain this decision to a regulator? Is it traceable and justified?

**All three lenses must align** before proceeding. Surface conflicts to the user.
```

**Why this works:**
- LLMs naturally reason through multiple perspectives
- Lenses encode constraints without becoming rigid rules
- Conflicts become explicit
- Decisions are explainable and traceable

---

## Getting Started: Complete Checklist

- [ ] **Understand** — Read `llm-driven-systems.manifesto.md` and `thing.md`
- [ ] **Plan** — Answer: What problem? What atomic units? What workflows?
- [ ] **Create AGENTS.md** — Your orchestration entry point at root
- [ ] **Create skills/** — Specification, read/write thing skills, workflow
- [ ] **Understand thing.md** — The atomic unit specification (including triggers)
- [ ] **Create examples** — A few things in `things/` to demonstrate your schema
- [ ] **Add validation rules** — Domain-specific required fields and valid types in your specification skill (validated by `validate.thing.skill.md`)
- [ ] **Define commit conventions** — Follow `git-workflow.md` patterns for structured commit messages
- [ ] **Enable tooling** — Configure GitHub Copilot or Claude Code if needed
- [ ] **Test** — Feed agent + skills + things to your LLM and validate
- [ ] **Iterate** — Refine skills as you learn what works
- [ ] **Commit** — Version control everything in git with meaningful messages

---

## The Self-Describing Principle

The MarkdownLLM framework itself is a domain within this framework. Its specifications are things with YAML frontmatter, relationships, statuses, and versions. The framework's AGENTS.md orchestrates its own evolution.

**What this means for you:**

When you create a domain, your AGENTS.md, skills, and even documentation can be things. They can have frontmatter. They can have relationships to each other. They can be validated. They can have statuses (`draft`, `evolving`, `stable`).

This is not required — a minimal domain can have simple skill files without full thing metadata. But as your domain matures, giving your skills and documentation the same structure as your data things creates:

- **Navigability** — The agent can traverse relationships between your specs and your data
- **Maturity tracking** — You can see which skills are stable vs. still evolving
- **Validation** — The same validation skill that checks your things can check your specs
- **Consistency** — One pattern, everywhere, no special cases

This is the fractal nature of the framework: the same structure at every scale, from the framework itself down to a single thing instance.

---

## Key Takeaways

1. **Three layers, one pattern:** Agent (orchestration) → Skills (capabilities) → Things (data)
2. **Agent auto-loads:** No manual includes needed; it's discovered at startup
3. **Skills are composable:** Each skill stands alone but references others
4. **Things follow spec:** All instances follow `thing.md` patterns (including triggers)
5. **Everything is a thing:** Your domain's specs, skills, and data all share the same structure (YAML frontmatter + markdown body). The framework itself follows this pattern — it is self-describing.
6. **Git is the state machine:** Commits are where state becomes real. Commit at meaningful boundaries. Structured messages make git log a domain narrative. See `git-workflow.md`.
7. **Interface is existing routes:** Use VS Code, CLI, mobile, voice — whatever connects you to an LLM. Don't build a new interface. See `interface.md`.
8. **Validation is built in:** `validate.thing.skill.md` checks structural integrity, referential consistency, and semantic coherence. Domain-specific rules live in your specification skill.
9. **Vendor agnostic:** Works across GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, Gemini
10. **Transparent:** Everything versioned in git; all logic explicit and readable; three audit layers (worklog, git log, git diff)
