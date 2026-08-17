# MarkdownLLM

*An operating environment for LLM agents — built from markdown and git.*

Every agent session starts from scratch, so you have to hand the agent its context back — sensibly, cheaply, without burying it. Plenty of tools already do the storing and the retrieving: Obsidian vaults, LLM wiki, file lookups. What they leave open is what happens after hundreds of sessions and a mountain of saved memory — when the question stops being *how do I retrieve this* and becomes *is any of it still true*. That's what MarkdownLLM is about: not storing more, but keeping what's stored coherent.

State lives as plain markdown files — atomic, explicitly linked, version-controlled in git. The difference is that their integrity is non-negotiable. A deterministic floor — one CLI, one git pre-commit hook — checks structure, references, and schema on every commit; a record that doesn't hold together can't be committed at all. A reconciliation pass walks the blast radius of any consequential change; a retrospective sweeps for what slipped through. Each session, orientation is rebuilt from git history — not reloaded from a memory file. The result isn't more memory; it's state you can rely on.

A framework discovered by agents, directed by you, and grown together. It works with any LLM tool that can read and write files — Claude Code, Codex, Cursor, and the like — and a domain is a valid Obsidian vault, so the human GUI comes for free.

---

## The Partnership

The agent is the one reading the specs — `thing.md`, `write.thing.md`, `validate.thing.md` are its operating manual. It discovers structure, reasons about it, creates and validates things, and maintains consistency across sessions.

But you hold the vision. You define what the domain is, shape the orchestration, design the workflows, use the output, and come back to say "this isn't working" or "we need to handle this case." You are the directing intelligence throughout — not just at creation, but in every session and every refinement.

Neither works without the other. An agent without structure produces inconsistent, unreliable output; a human without an agent has to maintain all that structural discipline by hand. Together — with the framework as the shared language — you get something fluid but structured, growing but consistent, definition-driven but never rigid.

Two things follow from that partnership, and they set the scope. **Operating the system is programming it**: the definitions are written in the language you already speak, so friction stated in conversation becomes validated, committed instruction — no translator, no role change, and the floor between your words and the durable state is what keeps that honest. And **no expertise is required at the door**: what the framework asks of its human is authority — standing to say "this is true in my domain" — which everyone holds absolutely over their own affairs. The same unchanged primitives run a regulated quality system and a personal spending tracker; the discipline the diligent bring to record-keeping is exactly what the floor supplies on behalf of everyone who finds it tedious. Expertise isn't the entry fee — it's what the domain accumulates as you use it.

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

**Layer 1 — AGENTS.md.** The agent's entry point, auto-discovered by the LLM harness at session start. It declares what the domain is, where skills live, where the framework root is, and the session protocol. Every session begins by re-reading this structure; the agent rebuilds its bearings from committed state, not from a context window that compaction can erode.

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
| [framework-map.md](docs/framework-map.md) | Visual architecture map — the elevation, the spec graph, the floor mapping, the estate seam |
| [estate-mechanics.md](docs/estate-mechanics.md) | Running more than one domain — the three radii of a change, sync and publication across repos |
| [calculation-reference.md](docs/calculation-reference.md) | The `computed:` expression grammar — declared derivations the floor evaluates |

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
| [session-memory.md](session-memory.md) | Session memory: `type: insight`, graph-keyed liveness, and the session-end extraction ritual. Forward state is the thing graph, surfaced by the generated **orient** view (`mdllm session-start` → "Open loops") — the hand-maintained `continuity.md` is retired (v3.17) |
| [belief-revision.md](belief-revision.md) | Contradiction tracking: `type: conflict`, relation types, belief revision process |
| [retrospective.md](retrospective.md) | Periodic quality reflection: `type: retrospective`, when to write, what it produces — including the estate retrospective |
| [change-reconciliation.md](change-reconciliation.md) | The blast radius of a consequential change — the cue question (asked mechanically at every commit), the Assimilate pass, the Walk |
| [trigger-specification.md](trigger-specification.md) | Declared triggers: conditions the floor evaluates mechanically and conditions the agent judges |
| [derived-index.md](derived-index.md) | Generated index things — precomputed attention caches, rebuilt never hand-edited |
| [workflow-state.md](workflow-state.md) | Processes as things: `type: workflow-definition` and `type: workflow-run` |
| [coordination-claim.md](coordination-claim.md) | Multi-agent coordination — claims over things so concurrent sessions don't collide |
| [reasoning-lenses.md](reasoning-lenses.md) | Domain-declared reasoning lenses applied at read and write time |
| [example-things.md](example-things.md) | Worked example instances the other specs reference |

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

Since v3.0, the framework pairs its specifications with a no-package-install CLI (one entry file, a package of single-responsibility modules behind it — Python 3.10+ with PyYAML is the only runtime requirement, and the shared launcher described below handles managed shells where `python` or PyYAML is not otherwise available) that guarantees everything mechanical, so the LLM spends its reliability on reasoning:

```bash
python tools/mdllm.py validate <domain>      # structure, references, schema, declared derivations — exit 1 on Errors
python tools/mdllm.py install-hook <domain>  # git hooks: pre-commit validation + cue, commit-msg boundary, post-commit publication
python tools/mdllm.py doctor <domain> --harness codex  # independent adapter/runtime/trust/execution facts
python tools/mdllm.py adapter-install <domain> --harness codex --dry-run  # exact owned diff, no write
# Exact recognised legacy only: add --refresh-legacy; review with --dry-run first
python tools/mdllm.py scaffold <new-domain> --harness codex  # deterministic birth + selected outer adapter
python tools/mdllm.py triggers <domain>      # deadline & trigger evaluation + horizon; --estate rolls up every local domain
python tools/mdllm.py provenance <domain>    # decision pins resolve; no output rests on unverified content
python tools/mdllm.py calc <domain>          # declared derivations (`computed:`) — the floor does every sum
python tools/mdllm.py estate-sync            # fetch + ff-only pull across the estate's repos; --status = publication debt
python tools/mdllm.py imports-check <domain> # cross-domain imports re-checked against the source's face
python tools/mdllm.py eval <domain> --fixture evals/x.yaml   # golden-scenario assertions
python tools/mdllm.py kernel                 # regenerate the operative kernel from spec blocks
python tools/mdllm.py session-start <domain> # emit the startup ritual + orient view (open loops) for a SessionStart hook to inject at t=0
```

That's the working core — `python tools/mdllm.py --help` lists the full 29-subcommand surface (coherence checks, blast-radius reads, the disclosure boundary, MCP serving, and more; [framework-map.md](docs/framework-map.md) View 3 maps each subcommand to the spec it mechanises). The commit boundary carries three legs: **pre-commit** validates and asks the change-reconciliation cue question, **commit-msg** enforces the local disclosure boundary, and **post-commit** publishes each floor-validated commit (`mdllm autopush`) unless the repo opts out — release surfaces do, so a public release stays a deliberate human act.

Each domain declares its thing types, **its own status vocabularies**, and which of those statuses mean *settled* in a normative schema (`things/_schema.yaml`) — the validator enforces what the domain declares. Agents load the generated [kernel.md](kernel.md) — the operative rules at a small fraction of the full-spec cost (`mdllm tokens` measures the live split; figures are not restated in prose, where they have drifted four times) — at session start; the full specs remain the canonical elaboration, loaded on demand. A harness can deliver that startup ritual *mechanically*: `mdllm session-start` feeds a lifecycle hook so the agent runs version-check + velocity and reads the generated **orient** view — the open loops (non-terminal owned work + open conflicts; imported mirrors file under a separate Watched line) that replace the retired `continuity.md` — at t=0 rather than hoping it surfaces from a long entry file. `scaffold --harness claude|codex|all|none` selects only the outer harness projection; omitting the flag preserves the Claude compatibility default (see *Vendor setup*). Requires Python 3.10+ and PyYAML; `tiktoken` optional for token measurement.

### Templates

Starting structures the agent uses when scaffolding a new domain:

- `templates/AGENTS.md.template` — the domain entry file (operative sections regenerated by `mdllm domain-kernel`)
- `templates/_schema.yaml.template` — the domain's normative schema
- `templates/domain-{specification,read.thing,write.thing,workflow}.skill.md.template` — the four skills
- `templates/prompts/` — orchestration prompt templates (session-end continuity, cascade, conflict/schema scans)
- `templates/commands/` + `templates/copilot-prompts/` — the deliberate `end-session` / `retrospective` rituals as slash commands for Claude Code and Copilot
- `templates/{insight,conflict,decision,retrospective,workflow-definition,workflow-run}.md.template` — reserved-type things
- `templates/boundary-terms.template` — the local, never-committed disclosure boundary

---

## Why It Works — Structure Beats Scale

A well-defined domain makes even a small model powerful; an undefined domain makes even the largest model mediocre. When an agent operates within explicit thing types, known relationships, declared triggers, and validated integrity, it reasons with precision — it isn't inventing the system and reasoning within it at the same time. The cognitive load shifts from "figure out the problem space" to "apply straightforward reasoning within constraints that are already defined."

That's the framework's central hypothesis, **now being tested rather than asserted.** First eval results (2026-06-11; 2×2 model × framework, 20 trials) support part of it: structure bought determinism — the framework + large-model cell was the only one to pass all assertions in all trials — and small-model-with-framework edged out large-model-without (94% vs 89% of assertions) at roughly a quarter of the cost. But the fixture's reasoning core proved too easy to discriminate, so the stronger reasoning-quality claim is still open. See [evals/README.md](evals/README.md) for the honest read.

What holds regardless of the verdict:

- **The domain is the product.** The LLM is replaceable (vendor-agnostic); the domain definition is the durable asset you and your agent build over time.
- **Consistency compounds.** Every session builds on committed state and validated things — not a summarized memory of the last one. Refinements accumulate; nothing is lost to compaction.
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

### Codex support: current tracked projection; live verification still open

The vendor-neutral adapter boundary and project-local Codex renderer are
implemented and covered by unit and integration tests. The renderer produces
`.codex/hooks.json` lifecycle bindings for ordered SessionStart work and
PostToolUse validation; `doctor --harness codex` reports support,
configuration, currency, trust, runtime, and real-event execution as separate
facts. Static inspection and a runnable command never promote execution to
verified.

That is **designed-for evidence, not a completed Codex rollout**. Phase 5R.1
closed the shared Windows/POSIX launch defects and Phase 5R.2 replaced Claude's
parallel legacy projection with one ordered neutral-runner handler. Recognised
legacy Claude fragments can now be refreshed only through the explicit,
reviewed `--refresh-legacy` path; extensions and ambiguity still refuse. Phase
5R.4 used that same generic path to refresh both recognised root legacy forms
atomically. The framework now tracks current `.claude/settings.json` and
`.codex/hooks.json` projections as deliberate self-hosted state; no nested
domain was migrated.

After that repair, Phase 6 still has to install/review the corrected project
layer and observe real framework-root and directly opened domain lifecycle events.
Official documentation assigns exact hook review and trust to `/hooks` in the
**Codex CLI**; the Desktop chat command palette observed during this preflight
did not expose that command, so the plan does not pretend a CLI review happened
inside Desktop. The boundary and execution checklist remain in
[`vendor-harness-adapter-foundation`](things/plans/vendor-harness-adapter-foundation.md).

Use the read-only paths before authorising a project write:

```powershell
./tools/mdllm.ps1 doctor . --harness codex
./tools/mdllm.ps1 adapter-install . --harness codex --dry-run
```

Do not apply that diff while the repair gate is open. Once Phase 5R passes, the
operator may rerun the dry-run against the current renderer, apply the reviewed
diff, and complete the product-specific trust flow on a surface that actually
supports it.
The installer owns only MarkdownLLM's project lifecycle groups; it does not
modify user-global Codex configuration. Ambiguous or unsafe existing state is
refused rather than overwritten.

#### Codex desktop shared runtime compatibility (root and nested verified 2026-08-11)

This runtime compatibility layer was added and tested in the Codex desktop
harness — specifically, not as an untested generalisation. Its PowerShell
command shell had no `python` on `PATH`; its bundled Python was 3.12 but did
not include PyYAML. A repository-local, gitignored `.venv` with PyYAML makes
the deterministic floor available without changing the machine-wide Python
installation:

```powershell
./tools/mdllm.ps1 doctor .
./tools/mdllm.ps1 estate-sync .
./tools/mdllm.ps1 session-start .
./tools/mdllm.ps1 validate .
```

`tools/mdllm.ps1` prefers that local environment, and the checked-in shared
resolver applies the same dependency probe to framework-root and directly
opened nested domain launchers. The Codex desktop evidence includes a
successful framework-root floor invocation, a directly opened live nested
domain resolving the framework runtime, and a fresh nested repository making
a real commit through the generated pre-commit hook. The earlier external
`dirname` dependency and unprobed PowerShell candidates were repaired in the
shared runtime rather than worked around inside the Codex adapter. This
verifies runtime and Git-floor execution on the measured Codex desktop shell;
it does not substitute for Phase 6's real Codex lifecycle/trust evidence.

Then open the folder in your LLM tool, let it discover `AGENTS.md`, and tell it what you want:

> "I want a domain for tracking architectural decisions across our microservices — each decision capturing the context, options considered, decision made, and consequences."

The agent reads the specs, proposes a structure, and builds it; you refine through conversation. Then you open the new domain folder as its own workspace and do all future work there.

**That's the sketch — [first-hour.md](docs/first-hour.md) is the real, paced walkthrough**, including watching the floor catch a deliberate error.

### What works

The framework relies only on the cross-vendor `AGENTS.md` convention plus plain files and git, so it is vendor-agnostic *by design* — but "designed for" is intent, not measurement. Discovery and hook execution are harness properties, and the one non-IDE harness tested so far surfaced real differences. Treat the table as compatibility intent until an eval has exercised each row.

| Tool | Discovery | Status |
|------|-----------|--------|
| Codex desktop | AGENTS.md auto-load | Root + directly opened nested domain runtime/Git floor verified 2026-08-11; project lifecycle adapter implemented, with Phase 5R runtime/launch repair and Phase 6 live dispatch/trust verification still open ([plan](things/plans/vendor-harness-adapter-foundation.md)) |
| Claude Code | CLAUDE.md → AGENTS.md (scaffolded in every harness selection) | Core framework use verified; automatic framework-root SessionStart/PostToolUse dispatch verified 2026-08-16 on 2.1.229/Windows ([evidence](evidence/claude-phase6-no-adapter-and-root-2026-08-16.md)). Adapter-optionality verified 2026-08-17 on CLI 2.1.233: in a differential `--harness none` probe pair the entry pointer delivered `AGENTS.md` at t=0 and its removal left no automatic surface, with all four floor legs adapter-free ([evidence](evidence/claude-no-adapter-entry-probe-2026-08-17.md)) |
| Codex (VS Code) | AGENTS.md auto-load | Exercised on a real project; not yet eval-measured |
| GitHub Copilot, Codex CLI, Cursor, Windsurf, Gemini CLI | AGENTS.md auto-load | Designed for; not yet exercised |

**What does NOT work:** any interface without file-system access (ChatGPT web, Claude web, bare API calls without tool use). The agent must be able to discover files, read them, and write them.

### Vendor setup

- **Claude Code** — `CLAUDE.md` is written for you: the installer writes one at the framework root, and `scaffold` writes one in every new domain under **every** `--harness` selection, `none` included. It is an entry pointer (`@AGENTS.md`) holding no domain content of its own, so it is either needed or harmlessly redundant; the framework root's wrapper additionally routes its second read position — Claude Code loads ancestor `CLAUDE.md` files into nested-domain sessions, and the inherited pointer must say whose `AGENTS.md` governs — which harness the operator opens is not knowable at scaffold time, and a domain the harness cannot see is a domain that does not run. Delete it if your harness reads `AGENTS.md` directly. Claude remains the compatibility default. New projections use one handler entering the neutral ordered runner; the historical two-handler form is recognised legacy data and refreshes only through the explicit reviewed path. Existing domain settings remain untouched unless their operator chooses that migration.
- **Optional lifecycle hardening** — `scaffold <path> --harness claude|codex|all|none` selects the project adapter(s) for a new domain (`claude-code` is also accepted as the canonical Claude name). Omitting the flag still selects the historical Claude default. `none` leaves the portable `AGENTS.md` interpretation path plus Git floor. Existing projects inspect with `doctor` and review `adapter-install --dry-run`; an exact reported legacy fragment additionally requires `--refresh-legacy`, while extensions and ambiguity remain operator-resolved refusals.
- **GitHub Copilot (VS Code)** — set `"chat.useAgentsMdFile": true` and `"chat.useNestedAgentsMdFiles": true`.
- **Codex** — auto-discovers `AGENTS.md`. The project adapter is implemented and the root tracks its current rendered `.codex/hooks.json`; Phase 6 still owns live verification. The [official Codex hook documentation](https://developers.openai.com/codex/hooks) names `/hooks` as a **CLI** review/trust surface; do not assume it is a Desktop chat command. `doctor . --harness codex` remains `execution: untested` until a matching real event and harness-owned transcript correlate.
- **Cursor, Windsurf, Gemini CLI** — no configuration; they auto-discover `AGENTS.md` at root.

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

**Why not just prompt engineering?** It's not either/or — every session still starts with good prompting. The difference is what that prompting acts on. A prompt on its own is ephemeral: it can't hold state across sessions, version meaningfully, validate itself, or compose. MarkdownLLM gives the agent a persistent, structured world to build its own knowledge base in — so instead of giving directions once, you're giving your agent ground it can map, return to, and extend.

**Why markdown and YAML?** Because agents can read, write, diff, and reason about them, git can version them, and humans can read them too — and that transparency is what makes the collaboration work.

**Why "MarkdownLLM"?** Markup pointed text at a parser; markdown pointed it back at a person; the LLM is the first machine that reads it on human terms — so the name is the format and its reader, finally matched.

**Do I need to understand the specs to use this?** No. The agent understands the specs; you understand your domain. You'll absorb the patterns over time because you can read everything the agent produces — but you never need to study them upfront.

**Is this production-ready?** The architecture is actively used — the framework develops itself as a domain, and a private estate of over a dozen domains runs on it daily (regulated-compliance, finance, and life-operations domains among them, worked across multiple machines and consuming each other's published faces). Specifications range from `draft` to `stable` (check frontmatter); `examples/` are small validated demonstrations, not production load. Your specific domain matures through use — that's by design.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Fork, follow `git-workflow.md` commit conventions, keep YAML frontmatter valid, submit a PR.

## License

MIT License. See [LICENSE](LICENSE). Copyright (c) 2026 Janosh Moshiri.
