# MarkdownLLM

*Architecture for AI agents.*

**Your agent is smart, but it works without a map. MarkdownLLM gives it one: a traversable knowledge base of structured definitions it can navigate at a sensible context cost, with git history as the persistent memory of everything that's happened.**

Today's agents are capable but unaware — they execute well, yet they can't see the shape of the system they're working in, or what changed before they arrived. MarkdownLLM changes that. You define a *domain* — anything you need to track and reason about over time — as typed, linked things in version control. The agent traverses that structure to reason with precision, and reads git history to know what happened and when. With the whole domain legible to it, the agent does more than execute: it notices drift, catches misalignment, and stays consistent across sessions. The agent handles execution and structural discipline; you bring direction and judgment. What you're left with is vendor-agnostic, fully transparent, and yours.

It's a framework discovered by agents, directed by humans, and grown together.

> **New here?** Your first sixty minutes are mapped, step by step, in [first-hour.md](docs/first-hour.md) — and [operator-guide.md](docs/operator-guide.md) covers every hour after that. Nearly everything else in this repository is written for your agent to read; those two pages are written for you.

---

## The Partnership

The agent is the one reading the specs — `thing.md`, `write.thing.md`, `validate.thing.md` are its operating manual. It discovers structure, reasons about it, creates and validates things, and maintains consistency across sessions.

But you hold the vision. You define what the domain is, shape the orchestration, design the workflows, use the output, and come back to say "this isn't working" or "we need to handle this case." You are the directing intelligence throughout — not just at creation, but in every session and every refinement.

Neither works without the other. An agent without structure produces inconsistent, unreliable output; a human without an agent has to maintain all that structural discipline by hand. Together — with the framework as the shared language — you get something fluid but structured, growing but consistent, definition-driven but never rigid.

---

## The Framework Is a Domain

The framework is self-describing. Its specifications are themselves *things*, written in the same markdown-and-YAML format they define. The framework has its own `AGENTS.md`, its own skills, its own commit conventions — it follows the same pattern every domain follows:

```
AGENTS.md → skills → things → git
```

So the framework is itself the foundational domain, managed by its own agent. And you can have many domains sitting within it — compliance patterns, life management, product workflows — each with its own `AGENTS.md`, skills, things, git history, and agent. The difference between the framework and a domain is scope, not structure.

**The handoff:** you open the framework workspace, tell its agent to create a domain, and once it's built you open the domain folder as its own workspace. From there, that domain's agent is your working partner. The framework agent only returns if you want to create another domain or evolve the framework itself.

---

## The Architecture (For Agents)

The framework gives agents a three-layer model to work within:

```
AGENTS.md   — Orchestration & discovery (auto-loaded at session start)
   ↓
SKILLS/     — Reasoning capabilities (.skill.md); foundational specs via framework_root
   ↓
THINGS/     — Structured data instances (atomic units following thing.md)
```

**Layer 1 — AGENTS.md.** The agent's entry point, auto-discovered by the LLM harness at session start. It declares what the domain is, where skills live, where the framework root is, and the session protocol. Every session begins with full context; the agent never starts cold.

**Layer 2 — Skills.** Instructions *for the agent* — how to think and operate within the domain: a specification skill (philosophy and principles), a read skill, a write skill, and a workflow skill. Foundational specs like `thing.md` live in the framework root, resolved via `framework_root` — see [framework-discovery.md](framework-discovery.md).

**Layer 3 — Things.** The actual data — each a markdown file with YAML frontmatter and a narrative body:

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

Narrative body — context and reasoning.
```

Things are atomic (self-contained), linked (explicitly related to other things), and versioned (git-tracked). The agent creates, reads, updates, and validates them following the patterns its skills define.

---

## What's In This Repository

### For Humans

The two documents written for the operator rather than the agent, plus the visual map:

| File | Purpose |
|------|---------|
| [first-hour.md](docs/first-hour.md) | A newcomer's first sixty minutes — orientation, scaffolding a first domain, installing the floor |
| [operator-guide.md](docs/operator-guide.md) | The steady state — what the tooling carries for you, recurring scenarios, what remains your job |
| [framework-map.md](docs/framework-map.md) | Visual architecture map — the elevation, the spec graph, the floor mapping |

### Foundational Specifications (Agent-Consumed)

These are the specs the agent loads and reasons with:

| File | Purpose |
|------|---------|
| [thing.md](thing.md) | The atomic unit specification — what a thing is, how it's structured |
| [read.thing.md](read.thing.md) | How agents read and analyze things |
| [write.thing.md](write.thing.md) | How agents create and update things |
| [validate.thing.md](validate.thing.md) | The validation contract: the `mdllm` tool guarantees mechanical checks; the agent performs semantic ones |
| [provenance.md](provenance.md) | Output traceability: `type: decision` records with commit-pinned inputs, quarantine for external content |
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

Small working domains the agent can reference. Each declares its own `_schema.yaml` and is validated by the same deterministic floor as the framework — `mdllm validate` checks every example as its own corpus, so a stale example blocks a commit the same way a stale spec does:

- **[examples/compliance-patterns/](examples/compliance-patterns/)** — Regulatory compliance pattern library (skills + paired pattern/anti-pattern things)
- **[examples/life-manager/](examples/life-manager/)** — Personal life and work management (skills + a small interlinked dataset: a project with subtasks, a goal fed by a recurring habit, live triggers, and a decision record with pinned inputs — fictional data, deliberately including one overdue task so `mdllm triggers` has something to find)

For a domain in production use, the framework's own repository is the working example — it is a domain within itself, with live things, validation, and provenance.

### The Deterministic Floor (`tools/mdllm.py`)

Since v3.0, the framework pairs its specifications with a single-file CLI that guarantees everything mechanical, so the LLM spends its reliability on reasoning:

```bash
python tools/mdllm.py validate <domain>      # structure, references, schema — exit 1 on Errors
python tools/mdllm.py install-hook <domain>  # pre-commit hook: broken things cannot be committed
python tools/mdllm.py doctor <domain>        # environment probe: hook executes? version drift? degraded mode?
python tools/mdllm.py scaffold <new-domain>  # deterministic domain birth: templates, nested repo, isolation, hook
python tools/mdllm.py triggers <domain>      # deadline & trigger evaluation + horizon
python tools/mdllm.py provenance <domain>    # decision pins resolve; no output rests on unverified content
python tools/mdllm.py eval <domain> --fixture evals/x.yaml   # golden-scenario assertions
python tools/mdllm.py kernel                 # regenerate the operative kernel from spec blocks
```

Each domain declares its thing types and **its own status vocabularies** in a normative schema (`things/_schema.yaml`) — the validator enforces what the domain declares. Agents load the generated [kernel.md](kernel.md) (~1.6k tokens of operative rules) at session start instead of ~21k of full spec prose; the full specs remain the canonical elaboration, loaded on demand. Requires Python 3.10+ and PyYAML; `tiktoken` optional for token measurement.

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

## Why It Works — Structure Beats Scale

A well-defined domain makes even a small model powerful; an undefined domain makes even the largest model mediocre. When an agent operates within explicit thing types, known relationships, declared triggers, and validated integrity, it reasons with precision — it isn't inventing the system and reasoning within it at the same time. The cognitive load shifts from "figure out the problem space" to "apply straightforward reasoning within constraints that are already defined."

That's the framework's central hypothesis, **now being tested rather than asserted.** First eval results (2026-06-11; 2×2 model × framework, 20 trials) support part of it: structure bought determinism — the framework + large-model cell was the only one to pass all assertions in all trials — and small-model-with-framework edged out large-model-without (94% vs 89% of assertions) at roughly a quarter of the cost. But the fixture's reasoning core proved too easy to discriminate, so the stronger reasoning-quality claim is still open. See [evals/README.md](evals/README.md) for the honest read.

What holds regardless of the verdict:

- **The domain is the product.** The LLM is replaceable (vendor-agnostic); the domain definition is the durable asset you and your agent build over time.
- **Consistency compounds.** Every session builds on committed state and validated things. Refinements accumulate; nothing is lost.
- **Cost scales with precision, not volume.** Tiered context loading means the agent loads only what it needs, not the whole specification.
- **Transparency throughout.** Every file is readable; you can always see what the agent built, how it reasoned, and what it changed. Validation at the commit boundary keeps the mechanical half honest so reasoning can carry the rest.

---

## Getting Started

One command checks prerequisites, clones the framework, installs PyYAML and the deterministic-floor hook, and verifies the result with `mdllm doctor`:

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/JanoshMoshiri/MarkdownLLM/main/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/JanoshMoshiri/MarkdownLLM/main/install.ps1 | iex
```

You need an LLM tool with file-system access, plus `git` and Python 3.10+ — the installer offers to install the latter two if they're missing. Prefer to do it by hand? `git clone` the repo and `pip install pyyaml`.

Then open the folder in your LLM tool, let it discover `AGENTS.md`, and tell it what you want:

> "I want a domain for tracking architectural decisions across our microservices — each decision capturing the context, options considered, decision made, and consequences."

The agent reads the specs, proposes a structure, and builds it; you refine through conversation. Then you open the new domain folder as its own workspace and do all future work there.

**That's the sketch — [first-hour.md](docs/first-hour.md) is the real, paced walkthrough**, including watching the floor catch a deliberate error.

### What works

The framework relies only on the cross-vendor `AGENTS.md` convention plus plain files and git, so it is vendor-agnostic *by design* — but "designed for" is intent, not measurement. Discovery and hook execution are harness properties, and the one non-IDE harness tested so far surfaced real differences. Treat the table as compatibility intent until an eval has exercised each row.

| Tool | Discovery | Status |
|------|-----------|--------|
| Claude Code | CLAUDE.md → AGENTS.md | Verified in use (the framework's own development and evals run on it) |
| GitHub Copilot, Codex CLI, Cursor, Windsurf, Gemini CLI | AGENTS.md auto-load | Designed for; not yet exercised |

**What does NOT work:** any interface without file-system access (ChatGPT web, Claude web, bare API calls without tool use). The agent must be able to discover files, read them, and write them.

### Vendor setup

- **Claude Code** — the installer writes a `CLAUDE.md` wrapper (`@AGENTS.md`) for you. If you cloned by hand, add one at root containing `@AGENTS.md`.
- **GitHub Copilot (VS Code)** — set `"chat.useAgentsMdFile": true` and `"chat.useNestedAgentsMdFiles": true`.
- **Codex, Cursor, Windsurf, Gemini CLI** — no configuration; they auto-discover `AGENTS.md` at root.

### Deployment: the nested-repository model

Each domain is its own git repo nested inside the framework, kept out of framework commits via `.gitignore`, resolving foundational specs through `framework_root: ../..`:

```
MarkdownLLM/                     <- Framework git repo
├── .gitignore                   <- Contains: domains/
├── thing.md                     <- Foundational specs
└── domains/
    └── your-domain/             <- Your domain git repo (independent)
        ├── .git/
        ├── AGENTS.md            <- framework_root: ../..
        ├── skills/
        └── things/
```

Framework and domains version independently, and many domains can share one framework installation. See [domain-refresh.md](domain-refresh.md) for the full deployment architecture.

---

## Core Principles

1. **Agent-Consumed, Human-Directed** — every spec is written for agents to reason with; every decision is the human's.
2. **Definition-Driven** — structure emerges from clear definitions, not rigid templates.
3. **Atomic & Composable** — everything is a thing; everything links explicitly.
4. **Minimal Core, Emergent Detail** — start simple; let the schema grow through use.
5. **Vendor Agnostic** — works across any LLM with file-system access.
6. **Version-Controlled** — git is the source of truth.
7. **Transparent** — no black boxes; all logic is explicit and readable.

---

## FAQ

**Why not just prompt engineering?** Prompts are ephemeral — they don't persist across sessions, can't be versioned meaningfully, can't validate themselves, and can't compose. MarkdownLLM gives your agent a persistent, structured, self-validating foundation to reason within. The difference between a prompt and a framework is the difference between giving directions once and building a map.

**Why markdown and YAML?** Because agents can read, write, diff, and reason about them, git can version them, and humans can read them too — and that transparency is what makes the collaboration work.

**Why "MarkdownLLM"?** Markup pointed text at a parser; markdown pointed it back at a person; the LLM is the first machine that reads it on human terms — so the name is the format and its reader, finally matched.

**Do I need to understand the specs to use this?** No. The agent understands the specs; you understand your domain. You'll absorb the patterns over time because you can read everything the agent produces — but you never need to study them upfront.

**Is this production-ready?** The architecture is actively used — the framework develops itself as a domain, and one production domain (statutory company filings) runs on it. Specifications range from `draft` to `stable` (check frontmatter); `examples/` are small validated demonstrations, not production load. Your specific domain matures through use — that's by design.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Fork, follow `git-workflow.md` commit conventions, keep YAML frontmatter valid, submit a PR.

## License

MIT License. See [LICENSE](LICENSE). Copyright (c) 2026 Janosh Moshiri.
