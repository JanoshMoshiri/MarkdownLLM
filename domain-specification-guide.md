---
id: domain-specification-guide
type: guide
status: stable
version: 2.9
created: 2026-05-13
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: thing-specification
    relation: references
  - id: read-thing-specification
    relation: references
  - id: write-thing-specification
    relation: references
  - id: validate-thing-specification
    relation: references
  - id: git-workflow-specification
    relation: references
  - id: interface-specification
    relation: references
  - id: session-memory-specification
    relation: references
  - id: belief-revision-specification
    relation: references
  - id: retrospective-specification
    relation: references
  - id: trigger-specification
    relation: references
  - id: reasoning-lenses-specification
    relation: references
  - id: validate-thing-specification
    relation: complements
    notes: "Conflict status-vocabulary-universal-vs-domain resolved 2026-06-11: domains declare their own status vocabularies in things/_schema.yaml; the guide's position survived"
---

# Domain Specification Guide

This guide explains how to create a complete domain specification using the MarkdownLLM framework. The framework uses a **three-layer architecture**: Agent (orchestration) → Skills (reusable capabilities) → Things (data instances).

## Prerequisites

Creating a domain requires an **LLM tool that can traverse file directories, read and write files**, and discover agent files automatically. Each domain is an **agent app** — a self-contained, LLM-driven application — and **the LLM agent is your primary tool for creating it**.

**Compatible tools:** GitHub Copilot (VS Code), Claude Code, OpenAI Codex CLI, Cursor, Windsurf, Gemini CLI — any tool where the LLM has direct file system access and auto-discovers AGENTS.md at the workspace root.

**Not compatible:** Web-based chat interfaces (ChatGPT, Claude web) or raw API calls without a file-access harness. The LLM must be able to navigate directories, read markdown files, and create/modify files.

> **The agent builds the domain with you.** You describe the problem space, make design decisions about workflows and structure, and provide feedback as things take shape. The agent applies the framework patterns, creates the files, and maintains structural integrity. You iterate together — and that iteration doesn't end at creation. You continue to direct, refine, and evolve the domain through use.

## The Framework Is a Domain — And So Is Yours

The framework itself is a domain. It uses the same building blocks it defines — `AGENTS.md`, skills, things with YAML frontmatter, git-backed state. The framework's agent manages the framework: maintaining specs, evolving the system, and scaffolding new domains when you ask.

When you create a domain, you're creating another instance of the same pattern. Your domain gets its own `AGENTS.md`, its own skills, its own things, its own git history — and its own agent. The domain agent knows your domain, operates within it, and evolves it through use.

The key distinction: **the framework agent scaffolds domains; the domain agent operates within them.** You use the framework workspace to create a domain, then you open the domain as its own workspace and work from there. From that point forward, the domain agent is your partner — it discovers the domain's `AGENTS.md` and reasons within the domain's boundaries.

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

> **Note:** The foundational specification `thing.md` lives in the framework root, not in your domain. Your domain discovers it automatically via the `framework_root` mechanism (see framework-discovery.md).

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
│ AGENTS.md (Root)                                             │
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
│ └─ [domain]-workflow.skill.md (Process Patterns)             │
│     ↑ Foundational specs (thing.md, etc.) resolved via       │
│       framework_root — not copied into your domain           │
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

Domains locate framework specs at startup by resolving the `framework_root` relative path declared in their AGENTS.md frontmatter. As a fallback, the agent walks up the directory tree looking for a `.markdownllm` marker file. Standalone domains set `framework_root: .` and co-locate or submodule the framework specs.

See `framework-discovery.md` for the full specification, including the startup sequence, marker file format, nested repository model, and all standalone deployment options.

---

## Domain Structure: What You Need to Create

Every domain requires these essential components in this structure:

```
my-domain/                        ← Root of your domain (its own git repo)
├── AGENTS.md                     ← Discovered at startup (orchestration)
├── skills/
│   ├── [domain]-specification.skill.md   ← Philosophy, principles, reasoning
│   ├── [domain]-read.thing.skill.md      ← How to read and analyze things
│   ├── [domain]-write.thing.skill.md     ← How to create and update things
│   └── [domain]-workflow.skill.md        ← Process orchestration and flow
├── things/
│   ├── _schema.yaml              ← Normative schema: thing types, status vocabularies,
│   │                                required fields, relation vocabulary (read by mdllm)
│   ├── insights/                 ← type: insight things
│   ├── conflicts/                ← type: conflict things
│   ├── retrospectives/           ← type: retrospective things
│   ├── run-1/                    ← Subfolder per workflow run or flow
│   │   ├── thing-1.md
│   │   └── thing-2.md
│   ├── run-2/
│   │   └── thing-3.md
│   └── ...
└── docs/ (optional)
    └── Extended documentation
```

> **You do NOT need `thing.md` in your domain.** It's a foundational framework specification discovered via `framework_root` — see Framework Discovery above.

**The normative schema (`things/_schema.yaml`):** declare your thing types and —
critically — **your own status vocabularies**. The domain owns its state machines:
a tax return that moves `open → figures-ready → submitted → paid → reconciled`
should say so, not squeeze into generic workflow statuses. The deterministic
validator (`{framework_root}/tools/mdllm.py validate`) enforces whatever you
declare; the six universal workflow values apply only as an advisory default when
a type declares nothing. Install the validation floor in every new domain repo:
`python {framework_root}/tools/mdllm.py install-hook <domain-path>` — after that,
things with structural or referential Errors cannot be committed.

**Things subfolders:** In practice, each time you execute a workflow (e.g., analysing a product, processing a batch, running an assessment), the things generated are organised into subfolders within `things/`. This keeps runs separate, traceable, and avoids a flat directory of hundreds of files.

---

## Deployment Model: The Nested Repository Pattern

The recommended way to work with the framework uses a **nested repository architecture** where your domain lives inside the framework's `domains/` folder but maintains its own independent git history.

### How It Works

```
MarkdownLLM/                        ← Framework git repo (cloned from GitHub)
├── .gitignore                       ← Contains: domains/
├── thing.md                         ← Foundational specs (shared, read-only)
├── git-workflow.md
├── validate.thing.md
├── interface.md
├── ...other framework specs...
├── templates/                       ← Starting-point templates
├── examples/                        ← Reference implementations
└── domains/
    └── my-domain/                   ← Your domain git repo (independent)
        ├── .git/                    ← Your own git history
        ├── AGENTS.md               ← framework_root: ../..
        ├── skills/
        ├── things/
        └── docs/
```

### Setup Steps

1. **Clone the framework:** `git clone https://github.com/[org]/MarkdownLLM.git`
2. **Scaffold the mechanical shell:** `python tools/mdllm.py scaffold domains/my-domain` — this performs the entire birth sequence deterministically: instantiated templates (AGENTS.md with `framework_root` and `framework_version_seen` filled in, `things/_schema.yaml`, the four skill files), `git init`, the framework-side `.gitignore` isolation *committed before any domain commit*, the pre-commit hook, and the domain's first commit. It satisfies the `pre-domain-scaffold:isolate` hard hook by construction.
3. **Tell the agent to fill the semantic half** — describe what you want; the agent declares your thing types and vocabularies in `_schema.yaml`, writes the skill bodies, completes AGENTS.md, and creates seed things

### Why This Model

| Property | Mechanism | Purpose |
|----------|-----------|---------|
| **Isolation** | Framework `.gitignore` excludes `domains/` | Your domain files never appear in framework commits |
| **Independence** | Each domain has its own `.git` | Domains version independently with their own branches, tags, remotes |
| **Shared foundation** | `framework_root: ../..` in domain AGENTS.md | Domain agent discovers framework specs via relative path |
| **Read-only relationship** | Domains read framework specs; never write to them | Framework evolves independently |
| **Multiple domains** | Many domains can live under `domains/` | All share one framework installation |

### The `.gitignore` Contract

The framework's `.gitignore` **must** contain `domains/`. Without this, your domain files would appear as untracked files in the framework repo, breaking the isolation model. This is already configured in the framework repository.

See [domain-refresh.md](domain-refresh.md) for the full deployment architecture and refresh process.

---

## Creating Your Agent File (AGENTS.md)

Your `AGENTS.md` is where you design how the agent behaves within your domain. This is not a template to fill in mechanically — it's a design document where you make deliberate decisions about:

- **What this domain is** — The vision, the problem space, what it accomplishes
- **How the agent should reason** — What skills to load, what principles to follow, what lenses to apply
- **What workflows to orchestrate** — The processes your domain follows, in what order, with what checkpoints
- **What constraints apply** — Behavioral rules, validation requirements, when to ask for human input
- **How to handle conflicts** — When reasoning lenses disagree, when tradeoffs arise, what gets surfaced to you

These are *your* design decisions. The agent operates within whatever you define here. As you use the domain and learn what works, you'll refine these decisions — tightening constraints that are too loose, relaxing ones that are too rigid, adding workflows you didn't anticipate.

**Template structure (starting point — adapt to your needs):**

```markdown
---
name: [Domain Name]
description: What this domain does
version: 1.0
applies_to: "**/*.md"
framework_root: ../..
framework_version_seen: [copy the version field from {framework_root}/.markdownllm]
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
2. Version check (`session-start:version-check` hard hook): compare `{framework_root}/.markdownllm` version against `framework_version_seen`
3. Load `{framework_root}/kernel.md` — the operative rules of the foundational specs (a small fraction of the full-spec cost; `mdllm tokens` measures the current split); load a full spec only when the kernel doesn't settle an ambiguity
4. Load skills relevant to session intent: [domain]-specification.skill.md, [domain]-read.thing.skill.md, [domain]-write.thing.skill.md, [domain]-workflow.skill.md
5. Read the **orient** view (`mdllm session-start` emits it) — the open loops (non-terminal work things + open conflicts) carried from prior sessions. Forward state is the thing graph, not a hand-kept brief; `continuity.md` is retired (v3.17)
6. Evaluate triggers — scan things for time-based, dependency, or threshold triggers since last session

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
5. **Session end:** Explicitly invoke the `session-end-continuity` bound prompt — extract insights, disposition the standing insights, check for conflicts, and manage open-loop things (no `continuity.md` to update — orient reads the thing graph). This is a bound prompt, not a hard hook: "the session is ending" is not an observable, agent-caused event, so it never fires automatically — the agent or human must invoke it. There are exactly three hard hooks (`post-write:commit`, `pre-domain-scaffold:isolate`, `session-start:version-check`); see `orchestration.md`. Full spec: `session-memory.md` and `belief-revision.md`.

## Skills Directory

All reusable capabilities stored as skill files:

- **[domain]-specification.skill.md** — Philosophy and principles
- **[domain]-read.thing.skill.md** — Read and analyze things
- **[domain]-write.thing.skill.md** — Create and update things
- **[domain]-workflow.skill.md** — Process orchestration

## Foundational Specifications

- **thing.md** — Atomic unit specification
- **validate.thing.md** — Validation skill
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

## Knowledge Management

The framework includes primitives that help domains accumulate understanding across sessions. These are available to every domain automatically — you don’t need to configure them.

### The Orient View — Forward State Is The Thing Graph

There is no file to place or maintain. A domain's forward-looking state — open threads, pending work, unresolved conflicts — lives in the **thing graph**, and the generated **orient** view surfaces it: `mdllm session-start` emits the open loops (non-terminal work things + open conflicts) at session start. The hand-maintained `continuity.md` brief is retired (v3.17) — a singleton that drifted and conflated the corpus's two sides; forward state is now things, and the backward record is the commit stream (`mdllm worklog` views it on demand). Nothing to seed: a new domain has session memory from its first commit.

### `type: insight` — Preserved Ideas

Insights are emerging ideas, held views, or hypotheses that surface during a session but aren’t yet ready to become specs or domain things. They live in `things/insights/`. At session end, the agent extracts insights worth preserving and commits them.

Seed from `templates/insight.md.template`.

### `type: conflict` — Contradictions Held Explicitly

When two things in your domain conflict, the agent creates a `type: conflict` thing in `things/conflicts/` rather than silently picking one. Conflicts are held in tension until you resolve them: which view supersedes, whether both are valid, or whether to dismiss.

Seed from `templates/conflict.md.template`.

### `type: retrospective` — Periodic Quality Reflection

After significant activity — typically monthly, or after >10 new conflicts or >20 new insights — write a retrospective to reflect on the domain’s reasoning quality. What’s working? What patterns have emerged? What should change?

Seed from `templates/retrospective.md.template`.

**Full specifications:** `session-memory.md`, `belief-revision.md`, `retrospective.md`.

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

### Step 1: Set Up the Deployment Model

Clone the MarkdownLLM framework repository:

```bash
git clone https://github.com/[org]/MarkdownLLM.git
cd MarkdownLLM
```

Do **not** hand-create the domain directory or its git repo — birth is
mechanical (`mdllm scaffold`, run in Step 3), and the eval record is blunt
about why: hand-rolled birth sequences drop steps. The framework's
`.gitignore` already excludes `domains/`, so your scaffolded domain will have
its own independent git history. See the Deployment Model section above for
details.

### Step 2: Design Your Domain

This is where you think — not the agent. Answer these questions:
- **What problem does this domain solve?** What's the vision?
- **What are your atomic units (thing types)?** What does a "thing" look like here?
- **What workflows or processes orchestrate them?** What sequence of steps matters?
- **What reasoning constraints should the agent follow?** Are there lenses, compliance requirements, quality gates?
- **How will you use the output?** What do you need the agent to produce for you?

You don't need to answer these perfectly upfront. Start with what you know. The agent will help you structure it, and the answers will sharpen through use. But the design intent is yours — the agent executes within whatever you define.

### Step 3: Let the Framework Agent Build It

Open the **framework root** (`MarkdownLLM/`) as your workspace. The framework agent discovers the framework's `AGENTS.md`, knows the specifications, and knows how to scaffold domains. Describe what you want — the agent runs `python tools/mdllm.py scaffold domains/my-domain` for the mechanical shell (templates, `git init`, `.gitignore` isolation, pre-commit hook, first commit — the whole birth sequence, deterministically) and then fills the semantic half inside `domains/my-domain/`:

- `AGENTS.md` at domain root — with `framework_root: ../..` pointing to the framework
- `skills/` directory with the four baseline skills:
  - `[domain]-specification.skill.md`
  - `[domain]-read.thing.skill.md`
  - `[domain]-write.thing.skill.md`
  - `[domain]-workflow.skill.md`
- `things/` directory with initial examples and knowledge sub-folders (`insights/`, `conflicts/`, `retrospectives/`)

> `thing.md` is a framework foundational spec — your domain discovers it automatically via `framework_root`. Do not copy it into your domain.

### Step 4: Open Your Domain as Its Own Workspace

Once the framework agent has scaffolded your domain, open the domain folder as its own workspace:

```bash
cd domains/my-domain
code .
```

This is the handoff. From this point forward, the **domain agent** takes over — it discovers the domain's `AGENTS.md`, loads its skills, and operates within the domain. You don't return to the framework workspace for day-to-day domain work.

### Step 5: Test Your Domain

In your domain workspace, the domain agent should:
- Auto-discover AGENTS.md at root
- Load your skills and understand the domain
- Follow the workflow when you make requests
- Reason according to your principles

If the agent doesn't behave as expected, refine your skills — they're the guidance that shapes reasoning.

### Step 6: Use It, Refine It, Grow It

This is where the real value emerges. You use the domain. You run workflows. You consume the output. And then you come back with feedback:

- "This workflow needs an extra step before the final gate"
- "The write skill should capture rationale, not just decisions"
- "We need a new thing type for tracking remediation actions"
- "The agent is being too conservative — loosen this constraint"

Update skills. Define new thing types. Adjust workflows. The agent picks up every change next session — no reconfiguration needed. Your domain becomes more precise, more useful, more aligned with how you actually work. Commit everything to git — it's your audit trail and the mechanism that makes state persistent.

---

## Minimal vs. Complex Domains

### Minimal Domain (1-2 workflows)

Essential skills, can be concise:

- **[domain]-specification.skill.md** — 500-800 words explaining philosophy, principles, and how it works
- **[domain]-read.thing.skill.md** — Domain-tailored read guidance  
- **[domain]-write.thing.skill.md** — Domain-tailored write guidance
- **[domain]-workflow.skill.md** — Single atomic workflow or process description
- **AGENTS.md** — Orchestration entry point

**Example:** Life Manager (simple task tracking), Business Process Analysis (single five-phase analysis).

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

## The Deterministic Floor (v3): Schema, Hook, Kernel

Since framework v3.0, three mechanical pieces are part of every new domain's
scaffold — they replace diligence with construction:

**1. Declare a normative schema.** Copy `templates/_schema.yaml.template` to
`things/_schema.yaml` and declare your thing types, their status vocabularies,
and your relation vocabulary. Without a schema, `mdllm validate` falls back to
the default workflow vocabulary at advisory (Warning) severity; with one, your
domain's own rules are enforced as Errors. The schema is the contract — status
vocabularies are domain-owned, not framework-fixed.

**2. Install the pre-commit hook.** From the framework root:
`python tools/mdllm.py install-hook <domain-path>`. From then on, things with
structural errors physically cannot be committed. Never re-perform mechanical
checks by reasoning; never bypass the hook — if validation blocks a legitimate
change, the schema is wrong, fix it with the human.

**3. Load the kernel, not the specs.** The domain AGENTS.md "On Startup"
section should load `{framework_root}/kernel.md` (operative rules at a small
fraction of the full-spec cost) instead of the full foundational specs. Load a full spec only when
reasoning *about* the framework or when the kernel doesn't settle an ambiguity.

Two knowledge primitives also matter at scaffold time:

- **Decisions with pinned inputs** (`provenance.md`): when an output's
  correctness depends on a judgement over domain knowledge, record a
  `type: decision` thing in `things/decisions/` with `informed_by: [{id,
  commit}]` pins. `mdllm provenance <domain>` enforces the chain — including
  the quarantine rule: nothing may rest on an unverified `origin: external`
  thing.
- **Behavioural evals** (`evals/README.md`): once a workflow has a contracted
  end state, encode it as a fixture and run `mdllm eval <domain> --fixture
  <file>` as a regression net over committed state.

---

## Getting Started: Complete Checklist

- [ ] **Prerequisites** — Confirm you have an LLM tool with file system access (Copilot, Claude Code, Codex CLI, etc.)
- [ ] **Understand** — Read `llm-driven-systems.manifesto.md` and `thing.md`
- [ ] **Plan** — Answer: What problem? What atomic units? What workflows?
- [ ] **Clone framework** — Clone the MarkdownLLM repository
- [ ] **Create domain folder** — Create your domain inside `domains/` and initialise a git repo
- [ ] **Scaffold domain** — From the framework workspace, tell the framework agent to build your domain (AGENTS.md, skills, example things)
- [ ] **Open domain workspace** — Open the domain folder as its own workspace — the domain agent takes over from here
- [ ] **Nothing to set up for session memory** — forward state is the thing graph (surfaced by the `mdllm session-start` orient view) and the backward record is the commit stream; `continuity.md` and `WORKLOG.md` are retired (v3.17)
- [ ] **Understand thing.md** — The atomic unit specification (including triggers) — do NOT copy it into your domain
- [ ] **Declare the schema** — Copy `templates/_schema.yaml.template` to `things/_schema.yaml`: types, status vocabularies, relations (enforced by `mdllm validate`)
- [ ] **Install the hook** — `python tools/mdllm.py install-hook <domain-path>` so structural errors cannot be committed
- [ ] **Add semantic validation rules** — Judgement-level rules in your specification skill (the agent's layer, per `validate.thing.md` v2.0; the mechanical layer is the tool's)
- [ ] **Define commit conventions** — Follow `git-workflow.md` patterns for structured commit messages
- [ ] **Enable tooling** — Configure GitHub Copilot or Claude Code if needed
- [ ] **Test** — Verify the domain agent auto-discovers AGENTS.md and follows your domain
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
8. **Validation is built in:** `validate.thing.md` checks structural integrity, referential consistency, and semantic coherence. Domain-specific rules live in your specification skill.
9. **Vendor agnostic:** Works across GitHub Copilot, Claude Code, Codex, Cursor, Windsurf, Gemini
10. **Transparent:** Everything versioned in git; all logic explicit and readable; two audit layers (git log — `mdllm worklog` views it; git diff)
11. **Knowledge compounds:** Session insights, contradictions, and retrospectives accumulate as first-class `type: insight`, `type: conflict`, and `type: retrospective` things. The domain learns across sessions, not just within them.
