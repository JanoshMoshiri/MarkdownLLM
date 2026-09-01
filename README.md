# MarkdownLLM

*An operating environment for LLM agents — built from markdown and git.*

Every agent session starts from scratch, so you have to hand the agent its context back — sensibly, cheaply, without burying it. Plenty of tools already do the storing and the retrieving: Obsidian vaults, LLM wiki, file lookups. What they leave open is what happens after hundreds of sessions and a mountain of saved memory — when the question stops being *how do I retrieve this* and becomes *is any of it still true*. That's what MarkdownLLM is about: not storing more, but keeping what's stored coherent.

State lives as plain markdown files — atomic, explicitly linked, version-controlled in git. A deterministic structural floor — one CLI and an installed three-hook Git boundary — checks declared structure, references, and schema against the candidate commit. When the current hook is installed and runnable, mechanical Errors block that commit. A probabilistic agent still interprets meaning; reconciliation and retrospectives route semantic drift for review rather than pretending code can prove truth. Each session, orientation is rebuilt from the accepted state and history recorded in git — not reloaded from a memory file.

A framework discovered by agents, directed by you, and grown together. Its entry contract, markdown state, and Git floor are portable to file-aware LLM tools; discovery and lifecycle support are verified per harness rather than inferred from a product name. A domain is a plain Markdown folder and can be opened in tools such as Obsidian; full vault-compatibility remains an execution-test claim, not an assumption.

**Want to see the estate before opening an agent harness?** [MarkdownLLM
Explorer](explorer/README.md) is the optional, read-only local viewer. Windows
has an installer preview; on macOS the framework agent can bootstrap and open
the portable route directly. It turns the substrate, domains, commits, files,
skills and memory into a visual local interface without changing the files or
becoming a second source of truth.

---

## The Partnership

The agent is the one reading the specs — `thing.md`, `write.thing.md`, `validate.thing.md` are its operating manual. It discovers structure, reasons about it, creates and validates things, and works to reconcile consistency across sessions. The interpreter remains probabilistic; the floor makes only its enumerated structural checks deterministic.

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
AGENTS.md   — Orchestration & discovery (delivered by the harness entry route)
   ↓
SKILLS/     — Reasoning capabilities (.skill.md); foundational specs via framework_root
   ↓
THINGS/     — Structured data instances (atomic units following thing.md)
```

**Layer 1 — AGENTS.md.** The agent's canonical entry contract, delivered by the harness either directly, through a core entry pointer, or through an explicit bootstrap. It declares what the domain is, where skills live, where the framework root is, and the session protocol. Every session begins by re-reading this structure; the agent rebuilds its bearings from committed state, not from a context window that compaction can erode.

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

The human-facing guides and visual surfaces:

| File | Purpose |
|------|---------|
| [first-hour.md](docs/first-hour.md) | A newcomer's first sixty minutes — orientation, scaffolding a first domain, installing the floor |
| [operator-guide.md](docs/operator-guide.md) | The steady state — what the tooling carries for you, recurring scenarios, what remains your job |
| [framework-map.md](docs/framework-map.md) | Visual architecture map — the elevation, the spec graph, the floor mapping, the estate seam |
| [estate-mechanics.md](docs/estate-mechanics.md) | Running more than one domain — the three radii of a change, sync and publication across repos |
| [calculation-reference.md](docs/calculation-reference.md) | The `computed:` expression grammar — declared derivations the floor evaluates |
| [Explorer installation guide](explorer/docs/installation-guide.md) | Install the read-only Windows preview |
| [Explorer user guide](explorer/docs/user-guide.md) | Look through the substrate, domains, commits, files, skills and memory |

### Explore the estate visually

MarkdownLLM Explorer is a local companion for people who want a clear way into
the substrate without reading a repository as raw files. It discovers the
framework and nested domain repositories, shows their Git history and tree,
groups skills and memory, and renders Markdown as a document.

Explorer is deliberately observation-only. It does not accept instructions for
an LLM, invoke skills, edit files, synchronise repositories, validate,
reconcile or publish. The framework remains usable without it, and the files
and Git history remain authoritative.

The current public position is an **operator-accepted Windows preview
candidate**. The independent-review corrections are implemented, but public
Windows publication remains gated by Authenticode signing and a final native
lifecycle run on the signed bytes. The source and installer build recipe are
tracked here; the eventual verified `.exe` is attached separately as a release
asset rather than committed to the repository. On macOS, ask the framework
agent to **open MarkdownLLM Explorer**; `tools/open-explorer.sh` creates its
owned portable environment, opens the browser and stops after 30 minutes of
inactivity. Native Mac packaging remains a later actual-Mac lane.
See the [installation
guide](explorer/docs/installation-guide.md), [user
guide](explorer/docs/user-guide.md), and [source/build
notes](explorer/README.md).

### Foundational Specifications (Agent-Consumed)

These are the specs the agent loads and reasons with:

| File | Purpose |
|------|---------|
| [thing.md](thing.md) | The atomic unit specification — what a thing is, how it's structured |
| [read.thing.md](read.thing.md) | How agents read and analyze things |
| [write.thing.md](write.thing.md) | How agents create and update things |
| [validate.thing.md](validate.thing.md) | The validation contract: `mdllm` deterministically runs its enumerated mechanical checks; the agent and human perform semantic ones |
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

Since v3.0, the framework pairs its specifications with a small CLI (one entry file, a package of single-responsibility modules behind it — Python 3.10+ with PyYAML is the runtime requirement, and the shared launcher described below handles managed shells where `python` or PyYAML is not otherwise available). It deterministically evaluates the structural invariants each command declares; it does not certify semantic truth or agent adherence. In the examples, `mdllm` is route-neutral notation: use `./tools/mdllm.ps1` on Windows PowerShell, or `python tools/mdllm.py` elsewhere only with an interpreter that can import PyYAML:

```bash
mdllm validate <domain>      # structure, references, schema, declared derivations — exit 1 on Errors
mdllm install-hook <domain>  # git hooks: pre-commit validation + cue, commit-msg boundary, post-commit publication
mdllm doctor <domain> --harness codex  # independent adapter/runtime/trust/execution facts
mdllm adapter-install <domain> --harness codex --dry-run  # exact owned diff, no write
# Exact recognised legacy only: add --refresh-legacy; review with --dry-run first
mdllm scaffold <new-domain> --harness codex  # deterministic birth + selected outer adapter
mdllm triggers <domain>      # deadline & trigger evaluation + horizon; --estate rolls up every local domain
mdllm provenance <domain>    # decision pins resolve; no output rests on unverified content
mdllm calc <domain>          # declared derivations (`computed:`) — the floor does every sum
mdllm estate-sync            # fetch + ff-only pull; --require-fresh = strict manual state; --status = publication debt
mdllm imports-check <domain> # cross-domain imports re-checked against the source's face
mdllm external-trust review <server> --path <domain> # inspect exact .mcp.json authority before command/network use
mdllm eval <domain> --fixture evals/x.yaml   # golden-scenario assertions
mdllm kernel                 # regenerate the operative kernel from spec blocks
mdllm session-start <domain> # emit the startup ritual + orient view (open loops) for a SessionStart hook to inject at t=0
```

That's the working core — `mdllm --help` lists the full command surface (coherence checks, blast-radius reads, the disclosure boundary, MCP serving, and more; [framework-map.md](docs/framework-map.md) View 3 maps each subcommand to the spec it mechanises). The commit boundary carries three legs: **pre-commit** validates and asks the change-reconciliation cue question, **commit-msg** enforces the local disclosure boundary, and **post-commit** publishes a floor-validated commit (`mdllm autopush`) only when the repo literally declares `git.autopush: true`. False, absent, or malformed values do not publish; this release surface declares false, so a public release stays a deliberate human act.

Each domain declares its thing types, **its own status vocabularies**, and which of those statuses mean *settled* in a normative schema (`things/_schema.yaml`) — the validator enforces what the domain declares. Agents load the generated [kernel.md](kernel.md) — the operative rules at a small fraction of the full-spec cost (`mdllm tokens` measures the live split; figures are not restated in prose, where they have drifted four times) — at session start; the full specs remain the canonical elaboration, loaded on demand. A harness can deliver that startup ritual *mechanically*: `mdllm session-start` feeds a lifecycle hook so the agent runs version-check + velocity and reads the generated **orient** view — the open loops (non-terminal owned work + open conflicts; imported mirrors file under a separate Watched line) that replace the retired `continuity.md` — at t=0 rather than hoping it surfaces from a long entry file. `scaffold --harness <registered>|all|none` selects the outer adapter projection; omission preserves the Claude compatibility default, while a run-time-bound selection may have no project artifact to render (see *Vendor setup*). Requires Python 3.10+ and PyYAML; `tiktoken` optional for token measurement.

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

A well-defined domain can let a smaller model spend more of its capability on the task; an undefined domain asks any model to infer the system and solve within it at once. Explicit thing types, relationships, triggers, and validated structural integrity reduce that ambiguity. Whether a particular model then reasons well is an empirical question, not a property the definitions guarantee.

That's the framework's central hypothesis, **now being tested rather than asserted.** First eval results (2026-06-11; 2×2 model × framework, 20 trials) support a narrower result: the framework + large-model cell was the only one to pass every recorded assertion in every trial, and small-model-with-framework edged out large-model-without (94% vs 89% of assertions) at roughly a quarter of the cost. The fixture's reasoning core proved too easy to discriminate, so neither universal determinism nor the stronger reasoning-quality claim follows. See [evals/README.md](evals/README.md) for the honest read.

What holds regardless of the verdict:

- **The domain is the product.** The domain definition is the durable asset you and your agent build over time. Its contract is vendor-neutral; actual replacement compatibility remains harness- and build-specific evidence.
- **Recorded state compounds.** Every session can build on committed, mechanically validated things rather than depending only on a summary of the last one. State and reasoning that were never recorded can still be lost to compaction.
- **Cost scales with precision, not volume.** Tiered context loading means the agent loads only what it needs, not the whole specification.
- **Inspectable accepted state.** Local framework files, recorded inputs, decision narratives, commits, and diffs are readable. They show what was accepted and changed, but they are an audit aid rather than a complete trace of a model's hidden or unrecorded reasoning. Vendor models and harness internals remain outside this transparency boundary.

---

## Getting Started

Install from an immutable release commit, verify the installer bytes, and then
run the local script. This example pins the published v3.32.0 artifact at
`c86363382b1a66f7be7697410e5b1826c0ab1930`:

```bash
# macOS / Linux
RELEASE_COMMIT=c86363382b1a66f7be7697410e5b1826c0ab1930
INSTALLER_SHA256=a0c4d00c2f4d7f4e336f101f4a3549321b817b88dede390bfdcd73ea6c8d01fa
git init MarkdownLLM
git -C MarkdownLLM config core.autocrlf false
git -C MarkdownLLM remote add origin https://github.com/JanoshMoshiri/MarkdownLLM.git
git -C MarkdownLLM fetch --depth 1 origin "$RELEASE_COMMIT:refs/remotes/origin/verified-release"
git -C MarkdownLLM checkout --detach "$RELEASE_COMMIT"
test "$(git -C MarkdownLLM rev-parse HEAD)" = "$RELEASE_COMMIT"
cd MarkdownLLM
printf '%s  install.sh\n' "$INSTALLER_SHA256" | sha256sum -c -
python3 -m pip install 'PyYAML==6.0.3'
python3 -c 'import yaml; assert yaml.__version__ == "6.0.3"'
./install.sh
```

```powershell
# Windows (PowerShell 7+)
$ReleaseCommit = 'c86363382b1a66f7be7697410e5b1826c0ab1930'
$InstallerSha256 = 'af55ce58cce7c06b369a152d850839320c58564e8f0d9c9937ea38393e33f7d3'
git init MarkdownLLM
git -C MarkdownLLM config core.autocrlf false
git -C MarkdownLLM remote add origin https://github.com/JanoshMoshiri/MarkdownLLM.git
git -C MarkdownLLM fetch --depth 1 origin "${ReleaseCommit}:refs/remotes/origin/verified-release"
git -C MarkdownLLM checkout --detach $ReleaseCommit
if ((git -C MarkdownLLM rev-parse HEAD) -ne $ReleaseCommit) { throw 'release commit mismatch' }
Set-Location MarkdownLLM
if ((Get-FileHash ./install.ps1 -Algorithm SHA256).Hash.ToLowerInvariant() -ne $InstallerSha256) { throw 'installer hash mismatch' }
python -m pip install 'PyYAML==6.0.3'
python -c "import yaml; assert yaml.__version__ == '6.0.3'"
./install.ps1
```

This removes the moving-branch pipe-to-shell path. The remaining bootstrap
trust root is explicit: a trusted copy of this release commit and hash, the
GitHub repository identity/TLS used to fetch it, Git itself, and the platform
package sources the installer offers to use with consent. Releases are not yet
signed, and PyPI remains the source for the exact `PyYAML==6.0.3` pin. The
published v3.32.0 installers predate the in-script dependency pin, so the
verified sequence above installs and checks that version first; do not let the
older script acquire an unspecified `pyyaml` release. The next release contains
the same exact pin inside both installers. If those trust roots are not
acceptable, acquire and verify the source through your own approved channel
before running it.

You need an LLM tool with file-system access, plus `git`, Python 3.10+, and the
verified PyYAML version above. The installer can offer to install the system
tools if they are missing, installs the hooks, and verifies the result with
`mdllm doctor`; for the pinned published artifact, provision Python and PyYAML
before invoking it so its older unpinned dependency fallback is never reached.

### Codex support: verified on named Windows surfaces

The vendor-neutral adapter boundary and project-local Codex renderer are
implemented and covered by unit and integration tests. The renderer produces
`.codex/hooks.json` lifecycle bindings for ordered SessionStart work and
PostToolUse validation; `doctor --harness codex` reports support,
configuration, currency, trust, runtime, and real-event execution as separate
facts. Static inspection and a runnable command never promote execution to
verified.

The projection is no longer only designed-for. Phase 6 verified automatic
framework-root and directly opened domain lifecycle dispatch on Codex CLI
0.147.0 / Windows 11, with definition-hash-bound attestations and
harness-owned transcript correlation. Later QMS work on Codex Desktop
26.810.7004.0 / runner 0.148.0-alpha.9 separately verified the dependency-
probing manual launcher, automatic startup, a full manual rerun, and the
restricted-then-approved `estate-sync --require-fresh` → pre-commit → publish
path. These are exact-surface records, not a claim about every Codex product,
version, operating system, or lifecycle trigger. The full boundary remains in
[`vendor-harness-adapter-foundation`](things/plans/vendor-harness-adapter-foundation.md).

Use the read-only paths before authorising a project write:

```powershell
./tools/mdllm.ps1 doctor . --harness codex
./tools/mdllm.ps1 adapter-install . --harness codex --dry-run
```

Apply only the exact diff you reviewed, then complete the product-specific
trust flow on a surface that actually supports it.
The installer owns only MarkdownLLM's project lifecycle groups; it does not
modify user-global Codex configuration. Ambiguous or unsafe existing state is
refused rather than overwritten.

#### Codex desktop shared runtime compatibility (root and nested; re-verified 2026-08-18)

This runtime compatibility layer was added and tested in the Codex desktop
harness — specifically, not as an untested generalisation. Managed shells may
have no `python` on PATH or expose a bundled interpreter without PyYAML. The
PowerShell launcher dependency-probes domain, framework, then PATH candidates;
a repository-local, gitignored `.venv` can therefore provide the floor without
changing machine-wide Python:

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
lifecycle and trust remain separately evidenced facts.

Then open the folder in your LLM tool, verify the configured entry route
delivers `AGENTS.md`, and tell it what you want:

> "I want a domain for tracking architectural decisions across our microservices — each decision capturing the context, options considered, decision made, and consequences."

The agent reads the specs, proposes a structure, and builds it; you refine through conversation. Then you open the new domain folder as its own workspace and do all future work there.

**That's the sketch — [first-hour.md](docs/first-hour.md) is the real, paced walkthrough**, including watching the floor catch a deliberate error.

### What works

The framework relies on one entry contract plus plain files and git, so it is vendor-agnostic *by design* — but "designed for" is intent, not measurement. Entry discovery and hook execution are harness properties. Each row therefore distinguishes the portable contract from the exact product evidence that has exercised it.

| Tool | Discovery | Status |
|------|-----------|--------|
| Codex desktop | AGENTS.md on the named tested builds | Root + directly opened nested-domain runtime/Git floor verified; QMS automatic startup, manual launcher, strict-sync approval and real publication verified 2026-08-18 on Desktop 26.810.7004.0 / runner 0.148.0-alpha.9. This does not imply every Desktop build or lifecycle trigger ([plan](things/plans/vendor-harness-adapter-foundation.md)) |
| Claude Code | CLAUDE.md → AGENTS.md (scaffolded in every harness selection) | Core framework use verified; automatic framework-root SessionStart/PostToolUse dispatch verified 2026-08-16 on 2.1.229/Windows ([evidence](evidence/claude-phase6-no-adapter-and-root-2026-08-16.md)). Adapter-optionality verified 2026-08-17 on CLI 2.1.233: in a differential `--harness none` probe pair the entry pointer delivered `AGENTS.md` at t=0 and its removal left no automatic surface, with all four floor legs adapter-free ([evidence](evidence/claude-no-adapter-entry-probe-2026-08-17.md)) |
| Codex CLI | AGENTS.md + project lifecycle adapter | Automatic framework-root and directly opened domain lifecycle verified on CLI 0.147.0 / Windows 11 with hash-bound attestations and transcript correlation; no wider OS/version claim |
| Codex (VS Code) | Intended AGENTS.md route | Exercised on a real project; not lifecycle/eval-measured |
| GitHub Copilot, Cursor, Windsurf, Gemini CLI | Intended/configurable AGENTS.md route | Designed for; no framework execution record yet. Claude or Codex evidence does not transfer |

**What does NOT work:** any interface without file-system access (ChatGPT web, Claude web, bare API calls without tool use). The agent must be able to discover files, read them, and write them.

### Vendor setup

- **Claude Code** — `CLAUDE.md` is written for you: the installer writes one at the framework root, and `scaffold` writes one in every new domain under **every** `--harness` selection, `none` included. It is an entry pointer (`@AGENTS.md`) holding no domain content of its own, so it is either needed or harmlessly redundant; the framework root's wrapper additionally routes its second read position — Claude Code loads ancestor `CLAUDE.md` files into nested-domain sessions, and the inherited pointer must say whose `AGENTS.md` governs — which harness the operator opens is not knowable at scaffold time, and a domain the harness cannot see is a domain that does not run. Delete it if your harness reads `AGENTS.md` directly. Claude remains the compatibility default. New projections use one handler entering the neutral ordered runner; the historical two-handler form is recognised legacy data and refreshes only through the explicit reviewed path. Existing domain settings remain untouched unless their operator chooses that migration.
- **Optional lifecycle hardening** — `scaffold <path> --harness <registered>|all|none` selects the adapter(s) for a new domain (`claude-code`, alias `claude`; `codex`; and `cowork` are currently registered). Omitting the flag still selects the historical Claude default. `none` leaves the portable entry contract plus Git floor. Project-bound adapters inspect with `doctor` and review `adapter-install --dry-run`; an exact reported legacy fragment additionally requires `--refresh-legacy`, while extensions and ambiguity remain operator-resolved refusals. Cowork is run-time-bound and renders no project artifact; its live remote/local verification remains open, so registration is not yet a compatibility-table row.
- **GitHub Copilot (VS Code)** — set `"chat.useAgentsMdFile": true` and `"chat.useNestedAgentsMdFiles": true`.
- **Codex** — the named CLI and Desktop records above establish exact entry/lifecycle/runtime facts; the project adapter is implemented and the root tracks its current rendered `.codex/hooks.json`. The [official Codex hook documentation](https://developers.openai.com/codex/hooks) names `/hooks` as a **CLI** review/trust surface; do not assume it is a Desktop chat command. Doctor promotes execution only when a matching real event and harness-owned transcript correlate.
- **Cursor, Windsurf, Gemini CLI** — use the intended direct `AGENTS.md` route, but verify it in the product rather than treating this designed-for line as an execution record.

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

1. **Agent-Consumed, Human-Directed** — every spec is written for agents to reason with; domain vision and irreversible authority remain human, while recorded decisions may be human, agent, or both.
2. **Definition-Driven** — structure emerges from clear definitions, not rigid templates.
3. **Atomic & Composable** — managed domain knowledge is represented as things and linked explicitly; implementation, configuration, release, and evidence artifacts keep their appropriate formats.
4. **Minimal Core, Emergent Detail** — start simple; let the schema grow through use.
5. **Vendor Agnostic by contract** — portable to file-aware LLM harnesses;
   discovery and lifecycle compatibility remain evidence-specific.
6. **Version-Controlled** — git records accepted state and its byte-level history; it does not make that state true of the outside world.
7. **Locally inspectable** — framework logic and managed state are readable; vendor models and harness internals are external trust boundaries, not claimed-away black boxes.

---

## FAQ

**Why not just prompt engineering?** It's not either/or — every session still starts with good prompting. The difference is what that prompting acts on. A prompt on its own is ephemeral: it can't hold state across sessions, version meaningfully, validate itself, or compose. MarkdownLLM gives the agent a persistent, structured world to build its own knowledge base in — so instead of giving directions once, you're giving your agent ground it can map, return to, and extend.

**Why markdown and YAML?** Because agents can read, write, diff, and reason about them, git can version them, and humans can read them too — and that transparency is what makes the collaboration work.

**Why "MarkdownLLM"?** Markup pointed text at a parser; markdown pointed it back at a person; the LLM is the first machine that reads it on human terms — so the name is the format and its reader, finally matched.

**Do I need to understand the specs to use this?** No. The entry route supplies the specs to the agent; delivery and adherence are checked separately where the harness exposes evidence. You understand your domain and can inspect the records it produces without studying every framework spec upfront.

**Is this production-ready?** The architecture is actively used — the framework develops itself as a domain, and a private estate of over a dozen domains runs on it daily (regulated-compliance, finance, and life-operations domains among them, worked across multiple machines and consuming each other's published faces). Specifications range from `draft` to `stable` (check frontmatter); `examples/` are small validated demonstrations, not production load. Your specific domain matures through use — that's by design.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Fork, follow `git-workflow.md` commit conventions, keep YAML frontmatter valid, submit a PR.

## License

MIT License. See [LICENSE](LICENSE). Copyright (c) 2026 Janosh Moshiri.
