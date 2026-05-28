# MarkdownLLM

A framework discovered by agents, directed by humans, grown together. You define the domain. The agent reasons within it. Together you build definition-driven systems that start from a structured foundation and evolve through use.

## The Core Idea

Every specification in this framework is written for an agent to discover, load, and reason with. The agent is the one reading `thing.md`. The agent is the one following `write.thing.md`. The agent is the one validating against `validate.thing.md`. These files are the agent's operating manual.

But you are the one with the vision. You define what the domain is. You shape the orchestration. You design the workflows. You use the output. You come back and say "this isn't working right" or "we need to handle this case." You are the directing intelligence throughout — not just at creation, but in every session, every refinement, every decision that matters.

**This is the partnership:** The agent handles execution within the framework — discovering specs, reasoning about structure, creating and validating things, maintaining consistency across sessions. You handle direction — defining what matters, making tradeoff decisions, providing feedback, and evolving the system as your understanding deepens.

Neither works without the other. An agent without structure produces inconsistent, unreliable output. A human without an agent has to manually maintain all the structural discipline that makes a system coherent over time. Together — with the framework as the shared language — you create something elegantly extendable: fluid but structured, growing but consistent, definition-driven but never rigid.

---

## The Framework Is a Domain

The framework is self-describing. Its specifications — `thing.md`, `write.thing.md`, `validate.thing.md` — are themselves things, written in the same markdown-and-YAML format they define. The framework has its own `AGENTS.md`, its own skills, its own commit conventions. It follows the same patterns that every domain follows, because it's expressed with the same building blocks.

This means the framework is itself a domain — the foundational domain. It has an agent that manages it, just as every domain has an agent that manages it. The framework agent knows the specifications, maintains them, evolves them, and scaffolds new domains when you ask. But its relationship to the framework is exactly the same as a domain agent's relationship to its domain: it discovers `AGENTS.md`, loads its skills, reasons within its boundaries, and commits its changes.

**Every domain has its own agent.** You can have many domains sitting within the framework — compliance patterns, life management, product workflows — and each one has its own `AGENTS.md`, its own skills, its own things, its own git history, its own agent. The pattern is the same at every level:

```
AGENTS.md → skills → things → git
```

The framework is simply the first instance of this pattern. When you open the framework workspace, the framework agent operates. When you open a domain workspace, that domain's agent operates. Each agent knows its own world and manages its own world. The difference is scope, not structure.

**The handoff when creating a domain:** You open the framework workspace, tell the framework agent to create a domain, and once it's built, you open the domain folder as its own workspace. From that point forward, that domain's agent is your working partner. The framework agent only comes back into play if you want to create another domain or evolve the framework itself.

---

## How It Works

```
You open a workspace containing MarkdownLLM
    |
Your agent discovers AGENTS.md automatically
    |
The agent loads foundational specs (thing.md, skills, guides)
    |
You describe what you want to build
    |
The agent proposes structure — you refine it
    |
The agent creates your domain — skills, things, workflows
    |
You use it, provide feedback, direct evolution
    |
Git captures every state change
    |
Every future session starts from full context — and you continue
```

There is no setup step. There is no installation. The framework is a set of files that an agent discovers and uses.

But "discovers and uses" doesn't mean the agent runs on its own. You are in the loop at every meaningful point: defining what gets built, deciding how workflows should run, using the output, and feeding back what needs to change. The agent provides the structural discipline and reasoning consistency. You provide the direction, the domain expertise, and the judgment.

This is an ongoing relationship, not a one-shot generation. Every session you come back, the agent picks up where you left off — with full context, consistent reasoning, and the ability to act on whatever you need next.

---

## A Domain Being Created

Here's what it looks like in practice — a developer and their agent creating a domain together. Notice how the developer directs, the agent proposes and builds, and both iterate until the structure is right:

```
------------------------------------------------------------
Developer -> Agent
------------------------------------------------------------

I want to create a domain for managing compliance patterns.
We deal with GDPR, PCI-DSS, and SOC2. Each pattern should
capture the regulation, the technical requirement, what good
looks like, and common anti-patterns. I need to be able to
run assessments against a codebase and track findings.

------------------------------------------------------------
Agent -> Developer
------------------------------------------------------------

I've read the MarkdownLLM framework specifications. Based on
thing.md and the domain-specification-guide, here's what I'll
create for your compliance-patterns domain:

**Thing types:**
- `compliance-pattern` — The reusable pattern (regulation,
  requirement, good implementation, anti-patterns)
- `assessment-finding` — A specific finding when running a
  pattern against code
- `assessment-run` — Groups findings from a single assessment

**Skills:**
- Specification skill defining your compliance philosophy
- Read skill for analyzing patterns without modification
- Write skill for creating patterns and recording findings
- Workflow skill for the assessment execution flow

**Structure:**

domains/compliance-patterns/
├── AGENTS.md
├── skills/
│   ├── compliance-patterns-specification.skill.md
│   ├── compliance-patterns-read.thing.skill.md
│   ├── compliance-patterns-write.thing.skill.md
│   └── compliance-patterns-workflow.skill.md
└── things/
    ├── patterns/
    └── assessments/

Shall I proceed? Any changes to the thing types or workflow?

------------------------------------------------------------
Developer -> Agent
------------------------------------------------------------

Yeah that looks good. Add a severity field to findings —
critical, high, medium, low. And the workflow should support
batch assessments where I point it at a repo and it checks
all relevant patterns.

------------------------------------------------------------
Agent -> Developer
------------------------------------------------------------

Done. I've created the full domain:

- AGENTS.md — orchestration with framework_root: ../..
- 4 skill files — all tailored to compliance assessment
- Severity levels in the write skill's thing schema
- Batch assessment workflow in the workflow skill
- 1 seed pattern (GDPR data handling) as a working example

The workflow skill defines three modes:
1. Single pattern check (one pattern, one codebase)
2. Batch assessment (all patterns, one codebase)
3. Gap analysis (compare findings across runs)

Everything is committed. Your domain is ready.

Open domains/compliance-patterns/ as its own workspace —
the domain agent will discover its AGENTS.md and you can
start creating patterns or running assessments immediately.
```

That's it. The developer described intent. The framework agent understood the specifications, proposed a structure, incorporated feedback, and built the domain. That's the framework agent's job — scaffolding domains from the framework's patterns.

What comes next is different. The developer opens the domain folder as its own workspace. The domain agent discovers the domain's `AGENTS.md`, loads its skills, and takes over from there — creating patterns, running assessments, refining workflows based on what's actually working. The domain agent knows the domain. It evolves the domain. The framework agent never enters the picture again unless the developer wants to create another domain or work on the framework itself.

---

## The Architecture (For Agents)

The framework gives agents a three-layer model to work within:

```
AGENTS.md (Orchestration & Discovery)
      | auto-discovered at session start
SKILLS/ (Reasoning Capabilities)
      | specifications, prompts, workflows as .skill.md files
      | foundational specs resolved via framework_root
THINGS/ (Structured Data Instances)
      -> atomic units following thing.md specification
```

### Layer 1: AGENTS.md (Discovery & Orchestration)

The agent's entry point. Automatically discovered by the LLM harness at session start. It tells the agent:

- What domain this is and what it does
- Where to find skills (reasoning guidance)
- Where to find the framework root (foundational specs)
- Behavioral rules and session protocol

**Why this matters:** Every session begins with full context. The agent never starts cold. It always knows what domain it's in, what skills are available, and how to reason within the domain's constraints.

### Layer 2: Skills (Agent Reasoning Guidance)

Skills are instructions *for the agent* — they define how to think about and operate within the domain. Each `.skill.md` file is a capability the agent loads when needed:

- **Specification Skill** — The domain's philosophy, principles, and reasoning patterns
- **Read Thing Skill** — How to analyze existing things without modification
- **Write Thing Skill** — How to create, update, and validate things
- **Workflow Skill** — Process orchestration: what steps to follow, in what order, for what purpose

Skills are the agent's expertise. They encode domain knowledge in a form the agent can reason with, consistently, across sessions and across vendors.

> **Foundational specs** (`thing.md`, `validate.thing.md`, etc.) live in the framework root — not in domain skills directories. The agent discovers them via `framework_root` (see [framework-discovery.md](framework-discovery.md)).

### Layer 3: Things (Structured Data)

Things are the actual data — each is a markdown file with YAML frontmatter and narrative body:

```yaml
---
id: unique-identifier
type: domain-specific-type
status: not-started/in-progress/blocked/paused/completed/cancelled
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

Things are atomic (self-contained), linked (explicitly related to other things), and versioned (git-tracked). The agent creates them, reads them, updates them, and validates their integrity — all following the patterns defined in skills.

---

## Why This Works

### The Problem: Without Structure

An agent without domain structure produces inconsistent, unreliable output. It starts every session from zero. It invents schemas on the fly. It contradicts previous work. The human has to re-explain everything, re-establish context, and hope for consistency.

A human without an agent has to manually maintain all the structural discipline: validating relationships, checking integrity, remembering what was decided last session, keeping schemas consistent as things grow. It's possible, but it doesn't scale.

### The Solution: A Shared Framework

MarkdownLLM gives both parties what they need:

**For the agent:**
- **Automatic discovery** — AGENTS.md is found at session start. No human has to remember to "load the context."
- **Persistent knowledge** — Skills encode how to reason. Things encode what's been done. Git encodes what changed and when.
- **Composable structure** — Each spec is self-contained but explicitly linked. The agent loads exactly what it needs.
- **Validated integrity** — `validate.thing.md` gives the agent rules to check its own work against.
- **Continuity across sessions** — At session end, the `session-end-continuity` and `worklog-update` prompts preserve insights and open threads as structured, committed knowledge. The next session picks up exactly where this one left off — not by reloading a conversation, but by reading committed state.

**For the human:**
- **Full transparency** — Every file is readable. You can always see what the agent built, how it reasoned, what it changed.
- **Control at every level** — You define the domain, the orchestration, the workflows. The agent operates within your constraints.
- **Contradiction tracking** — When things in your domain conflict, the agent surfaces them as first-class `type: conflict` things held in explicit tension until resolved. You decide: which view supersedes, whether both are valid in context, or whether the tension should be held until more is known.
- **Cumulative progress** — Every session builds on the last. Your refinements compound. Nothing is lost.

**The result:** A smaller model with a well-defined domain outperforms a larger model with no structure. Structure beats scale. But it's the human-agent partnership that creates and maintains that structure over time.

---

## What's In This Repository

### Foundational Specifications (Agent-Consumed)

These are the specs the agent loads and reasons with:

| File | Purpose |
|------|---------|
| [thing.md](thing.md) | The atomic unit specification — what a thing is, how it's structured |
| [read.thing.md](read.thing.md) | How agents read and analyze things |
| [write.thing.md](write.thing.md) | How agents create and update things |
| [validate.thing.md](validate.thing.md) | How agents validate thing integrity |
| [interface.md](interface.md) | I/O layer: input routes, output types, deliverables vs things |
| [git-workflow.md](git-workflow.md) | Git as state machine: commits, conventions, autocommit |
| [framework-discovery.md](framework-discovery.md) | How domain agents locate the framework root |
| [domain-refresh.md](domain-refresh.md) | How domain agents discover framework evolution |
| [orchestration.md](orchestration.md) | Opt-in hook points, structured prompts, and session-end bindings |
| [scalability-guide.md](scalability-guide.md) | Scaling from tens to thousands of things |
| [session-memory.md](session-memory.md) | Session continuity: `type: insight`, `type: continuity-brief`, and the `session-end-continuity` prompt |
| [belief-revision.md](belief-revision.md) | Contradiction tracking: `type: conflict`, relation types, belief revision process |
| [retrospective.md](retrospective.md) | Periodic quality reflection: `type: retrospective`, when to write, what it produces |

### Philosophy

| File | Purpose |
|------|---------|
| [llm-driven-systems.manifesto.md](llm-driven-systems.manifesto.md) | The paradigm — why definition-driven systems work |
| [domain-specification-guide.md](domain-specification-guide.md) | How agents create new domains (the guide they follow) |

### Examples

Working domain implementations the agent can reference:

- **[examples/compliance-patterns/](examples/compliance-patterns/)** — Regulatory compliance pattern library
- **[examples/life-manager/](examples/life-manager/)** — Personal life and work management

### Templates

Starting structures the agent uses when scaffolding a new domain:

- `templates/AGENTS.md.template`
- `templates/[domain]-specification.skill.md.template`
- `templates/[domain]-read.thing.skill.md.template`
- `templates/[domain]-write.thing.skill.md.template`
- `templates/[domain]-workflow.skill.md.template`
- `templates/prompts/` — Orchestration prompt templates
- `templates/continuity-brief.md.template` — Domain continuity brief
- `templates/insight.md.template` — `type: insight` things
- `templates/conflict.md.template` — `type: conflict` things
- `templates/retrospective.md.template` — `type: retrospective` things

---

## Getting Started

### What You Need

An LLM tool with file system access. That's it.

| Tool | Discovery | Status |
|------|-----------|--------|
| GitHub Copilot (VS Code) | AGENTS.md auto-load | Fully supported |
| Claude Code | CLAUDE.md -> AGENTS.md | Fully supported |
| OpenAI Codex CLI | AGENTS.md auto-load | Fully supported |
| Cursor | AGENTS.md auto-load | Fully supported |
| Windsurf | AGENTS.md auto-load | Fully supported |
| Gemini CLI | AGENTS.md auto-load | Fully supported |

**What does NOT work:** Any interface without file system access (ChatGPT web, Claude web, bare API calls without tool use). The agent must be able to discover files, read them, and write them.

### Step 1: Clone the Framework

```bash
git clone https://github.com/JanoshMoshiri/MarkdownLLM.git
cd MarkdownLLM
```

### Step 2: Talk to Your Agent

Open the workspace in your LLM tool. The agent will discover AGENTS.md automatically. Then just tell it what you want:

> "I want to create a domain for tracking architectural decisions across our microservices. Each decision should capture the context, options considered, decision made, and consequences."

The agent reads the framework specs, proposes a structure, and builds it. You refine through conversation.

### Step 3: The Agent Builds Your Domain

The agent will:
1. Create `domains/your-domain/` with its own git repo
2. Write AGENTS.md with `framework_root: ../..`
3. Create all four skill files tailored to your domain
4. Scaffold initial things as working examples
5. Commit everything

### Step 4: Open Your Domain as Its Own Workspace

Once the domain is created, **open the domain folder as a new workspace** in your editor:

```bash
cd domains/your-domain
code .
```

This is the key transition: you move from the framework workspace (where you created the domain) into the domain workspace (where you'll do all future work). From this point forward:

- The domain's `AGENTS.md` is what your agent discovers at session start
- The domain's `.git/` tracks all your domain-specific commits independently
- The framework specs are still accessible via `framework_root: ../..` — the agent resolves them through the relative path
- You never need to return to the framework workspace for day-to-day domain work

The domain is now a self-contained project with its own repository, its own agent configuration, and its own git history. The framework is the foundation it reads from — not the workspace you operate within.

### Step 5: Work Within Your Domain

This is where the real work happens — and it never stops. Every session in your domain workspace starts with the agent discovering your AGENTS.md, loading your skills, and understanding your things. Full context. Consistent reasoning. Audit trail in git.

But you're not a passenger. You are:
- **Defining workflows** — telling the agent how processes should run
- **Using the output** — consuming what the agent produces, applying it to real work
- **Providing feedback** — "this pattern doesn't capture edge cases well" or "the assessment needs a remediation step"
- **Directing evolution** — new thing types emerge as you discover what you need
- **Making decisions** — when the agent surfaces conflicts or tradeoffs, you decide

The system grows through this loop. Skills refine as you learn what guidance produces better results. Workflows adapt as your process matures. The domain becomes more precise, more useful, more yours — but always structured, always consistent, always traceable.

---

## Vendor Configuration

### GitHub Copilot (VS Code)

Enable AGENTS.md discovery:

```json
{
  "chat.useAgentsMdFile": true,
  "chat.useNestedAgentsMdFiles": true
}
```

### Claude Code

Create a `CLAUDE.md` wrapper at root:

```markdown
---
name: [Domain]
description: What this domain does
---

# [Domain] - Claude Code Instructions

@AGENTS.md
```

### Codex, Cursor, Windsurf, Gemini CLI

No configuration needed — these auto-discover AGENTS.md at root.

---

## The Deployment Model

The recommended structure is the **nested repository model**:

```
MarkdownLLM/                        <- Framework git repo
├── .gitignore                       <- Contains: domains/
├── thing.md                         <- Foundational specs
├── ...other framework specs...
└── domains/
    └── your-domain/                 <- Your domain git repo (independent)
        ├── .git/
        ├── AGENTS.md               <- framework_root: ../..
        ├── skills/
        ├── things/
        └── docs/
```

- Framework and domain version independently
- `framework_root: ../..` lets the domain agent discover foundational specs
- Multiple domains can share the same framework installation
- The framework's `.gitignore` keeps domains out of framework commits

See [domain-refresh.md](domain-refresh.md) for the full deployment architecture.

---

## The Elegant Constraint

A well-defined domain makes even a small model powerful. An undefined domain makes even the largest model mediocre.

**Structure beats scale.** When an agent operates within a clearly defined domain — with explicit thing types, known relationships, declared triggers, and validated integrity — it reasons with precision and consistency. Without that structure, the same agent produces vague, inconsistent output regardless of its parameter count.

- **The domain is the product.** The LLM is replaceable (vendor agnostic); the domain definition is the durable asset. And the domain is something you and your agent build together over time.
- **Consistency compounds.** Every session builds on committed state, validated things, and structured history. Your refinements accumulate. Nothing is lost.
- **Cost scales with precision, not volume.** Tiered context loading means the agent loads only what it needs.

This is why the framework exists. Not to add complexity, but to provide the minimal structure that makes a true human-agent partnership productive — across sessions, across vendors, and across scale.

---

## Core Principles

1. **Agent-Consumed, Human-Directed** — Every specification is written for agents to load and reason with. Every decision is made by the human who directs the system.
2. **Definition-Driven** — Structure emerges from clear definitions, not rigid templates.
3. **Atomic & Composable** — Everything is a thing; everything links explicitly.
4. **Minimal Core, Emergent Detail** — Start simple; let the schema grow through use.
5. **Vendor Agnostic** — Works across any LLM with file system access.
6. **Version-Controlled** — Git is the source of truth.
7. **Transparent** — No black boxes; all logic is explicit and readable. You can always see what the agent did and why.

---

## FAQ

### "Why not just prompt engineering?"

Prompts are ephemeral. They don't persist across sessions, can't be versioned meaningfully, can't validate themselves, and can't compose. MarkdownLLM gives your agent a persistent, structured, self-validating foundation to reason within. The difference between a prompt and a framework is the difference between giving directions once and building a map.

### "Why markdown and YAML?"

Because agents can read them, write them, diff them, and reason about them. Because git can version them. Because humans can read them too — and that transparency is what makes the human-agent collaboration work. You can always see what your agent built, verify it, and refine it.

### "Do I need to understand the specs to use this?"

No. The agent understands the specs. You understand your domain. You describe what you want; the agent applies the framework. Over time you'll naturally absorb the patterns because you can read everything the agent produces — but you never need to study the specs upfront.

### "Can I use this with [model/tool]?"

If your LLM tool can read files, write files, and navigate directories — yes. The framework is vendor-agnostic by design. Switch models, switch tools, your domain persists unchanged.

### "Is this production-ready?"

The architecture is proven and actively used. Specifications range from `draft` to `stable` (check frontmatter). The examples are working domains. Your specific domain will mature through use — that's by design.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Fork, follow `git-workflow.md` commit conventions, keep YAML frontmatter valid, submit a PR.

---

## License

MIT License. See [LICENSE](LICENSE).

Copyright (c) 2026 JMTM Software Ltd.
