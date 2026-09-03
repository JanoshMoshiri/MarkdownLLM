---
id: interface-specification
type: specification
status: evolving
version: 1.6
created: 2026-05-19
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: provenance-specification
    relation: complements
    notes: "v1.1: the membrane section — a served face is an output route whose consumer is another domain's agent; the hand-off mechanics (reference triple, quarantine, freshness) are provenance.md's"
  - id: thing-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: read-thing-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: explorer-publication-position
    relation: derived-from
    notes: "v1.5 distinguishes an optional read-only inspection surface from the human-to-agent I/O contract this specification owns."
  - id: markdownllm-desktop-is-primary-accessible-product
    relation: derived-from
    notes: "v1.6 distinguishes substrate route-agnosticism from a first-party product choosing to implement one accessible route."
---

# Interface

## What This Specifies

This document defines the I/O layer of the LLM-driven systems framework — how humans communicate with their agent and what comes back out. It completes the three-layer architecture:

- **Storage** — `thing.md` (persistent state as markdown files in git)
- **Processing** — `read.thing.md` / `write.thing.md` (how the LLM reasons within domains)
- **Interface** — this file (how input gets in and output gets delivered)

## The Core Principle: The Substrate Does Not Require One Route

The framework does not require one interface protocol, client, web app, chat widget or custom API
in order to be valid. A Domain remains operable through any compatible route that can receive its
entry contract and bounded context.

That contract does not forbid a product from supplying a route. MarkdownLLM Desktop is the
first-party accessible route: a local application that deliberately owns setup, Domain and
Session journeys while leaving Markdown and Git authoritative. It is still a replaceable pipe;
Claude Code, Codex, Copilot, Obsidian-assisted workflows and other compatible clients can operate
the same Domain without it.

This is a deliberate design choice:

- Interface technology changes faster than anything else in the stack
- A first-party interface creates a platform and maintenance boundary that must earn itself
  through accessibility and acceptance evidence
- Existing routes are already optimised for the interaction patterns you need
- The framework's value is in the domain definition and data layer, not in the I/O mechanism

### Optional inspection is not a new input route

[MarkdownLLM Explorer](explorer/README.md) is an optional local presentation
layer over the files and Git history. It makes a substrate and its domain estate
visible to a human, but it is not a route to an LLM: it does not accept agent
intent, load skills into a model, edit state, synchronise repositories,
validate, reconcile or publish. The underlying Markdown and Git repositories
remain authoritative.

That distinction preserves the interface-agnostic contract. A read-only viewer
may be added, removed, replaced or hosted separately without changing how a
human reaches an agent or how a domain is defined. If a future Explorer begins
carrying human intent to an LLM, that new boundary must be designed and
verified as an input route rather than inferred from the current viewer.

## Input Routes

An input route is any channel through which a human can communicate intent to their agent. The agent lives in the domain repository (AGENTS.md + skills + things); the input route is how you reach it.

### Currently Viable Routes

| Route | How It Works | Discovery / evidence boundary |
|-------|-------------|-------------------------------|
| **VS Code + GitHub Copilot** | Configurable AGENTS.md support; chat or voice input via editor. | Designed/configured route; lifecycle compatibility is unverified and is not inferred from Claude's `.claude` projection or shortcut files. |
| **MarkdownLLM Desktop (Engineering Preview)** | Local setup, Domain/Session management, Explorer and a context-only provider route over ordinary Markdown/Git state. | Windows Preview A is in acceptance; no public-release or live-provider claim is made until its pinned UAT closes. |
| **Claude Code (CLI + desktop)** | `CLAUDE.md` entry pointer imports `AGENTS.md` (`@AGENTS.md`). Core scaffold surface — born with every domain in every `--harness` selection, `none` included. | Automatic pointer route verified 2026-08-17; named lifecycle evidence is separate. |
| **OpenAI Codex CLI / desktop** | Reads AGENTS.md; the optional project adapter binds lifecycle events. | Automatic on the named tested Windows surfaces; CLI lifecycle and Desktop/runtime/Git claims are recorded separately rather than generalized. |
| **Cursor / Windsurf** | Intended AGENTS.md workspace route; editor-based chat. | Designed-for; no framework execution record yet. |
| **Gemini CLI** | Intended AGENTS.md terminal route. | Designed-for; no framework execution record yet. |
| **Mobile chat apps** | A file-aware client or middleware may feed the entry contract and selected context to an LLM API. | Manual bootstrap only; an ordinary web/mobile chat without file access is not a compatible route. |
| **Voice-to-text + any route** | OS-level speech recognition (Windows Speech, macOS Dictation, etc.) feeds text into any of the above routes. | Transparent |

### The entry pointer (harnesses that auto-load a differently named file)

Most routes read `AGENTS.md` directly. A harness that auto-loads a different
filename reaches it through an **entry pointer**: a small file of that name
whose import inlines `AGENTS.md`. Three facts about pointers, each earned by
execution evidence rather than design intent:

- **They are core surface, not adapter output.** `templates/entry/` owns them,
  `scaffold` writes every one of them in every harness selection including
  `none`, and no adapter may claim the filename. This is what keeps a domain
  interchangeable between harnesses — and it is load-bearing: in the
  differential no-adapter probe, the pointer-bearing domain had its entry file
  in model context before any tool call, and the pointer-removed control had
  no automatic entry surface at all
  (`claude-no-adapter-entry-probe-2026-08-17`, resolving
  `claude-entry-surface-unprovisioned-for-no-adapter-domains`).
- **A pointer controls presence, never position.** The entry file arrives in
  context at session open, behind the harness's own system prompt and any
  ancestor files — ordering is the harness's, root-down. On Claude Code
  specifically, nested-domain sessions also inherit the *framework root's*
  pointer from the parent directory; the root wrapper therefore routes both of
  its read positions explicitly, and a drift test holds its wording identical
  across the tracked file and both installers.
- **Injection delivers the body only.** YAML frontmatter is stripped on the
  way in (`an-injected-file-arrives-without-its-frontmatter`), so anything an
  agent must know *before its first tool call* belongs in the entry file's
  prose. Frontmatter reaches the agent when it reads the file with a tool —
  which the Tier-0 ritual does regardless.

### The Pattern

Every input route follows the same pattern:

```
Human intent (voice, text, gesture)
    ↓
Input route (VS Code, CLI, mobile, API)
    ↓
Agent discovery (AGENTS.md loaded automatically or manually)
    ↓
LLM receives: agent context + skills + relevant things + user request
    ↓
Processing begins
```

The portable processing contract does not care which route delivered it. The
delivery guarantees do: discovery, trust, lifecycle events, sandbox authority,
and output envelopes are harness capabilities and are never inferred from a
different product's evidence.

### Voice as a First-Class Input

Voice input deserves specific mention. In practice, many interactions with an LLM agent are conversational — you're thinking out loud, explaining context, giving direction. Speech-to-text at the OS level (Windows Speech Recognition, macOS Dictation, mobile voice keyboards) converts voice into text before it reaches any route.

This means voice is not a separate route — it's a transparent layer beneath any route. You speak, the OS transcribes, the text enters VS Code or a CLI or a mobile app. The LLM never knows or cares that the input was spoken.

This has implications:

- **No special voice protocol needed** — OS-level transcription is sufficient
- **Conversational tone is natural** — LLMs handle informal, spoken-style input well
- **Accessibility is built-in** — Voice input works for anyone who can speak, regardless of typing ability
- **Speed advantage** — Speaking is faster than typing for most people; combined with an LLM that reasons about your domain, this creates a rapid feedback loop

## Output Types

The agent produces two fundamentally different categories of output:

### 1. Things (Persistent State)

Things are the agent's memory and working state. They live in the `things/` directory as markdown files with YAML frontmatter. They are:

- **Internal to the system** — the agent reads and writes them to maintain understanding
- **Structured for LLM consumption** — optimised for parsing and reasoning, not human presentation
- **Versioned in git** — complete history, rollback capability, audit trail
- **The source of truth** — everything the agent knows is encoded here

Things are not outputs delivered to the user. They are the persistent substrate the agent operates on.

### 2. Deliverables (Produced Artefacts)

Deliverables are what the LLM produces *for the user* based on its understanding of the domain and the things within it. They are:

- **External to the system** — produced for human consumption or downstream use
- **Generated by the LLM, not the framework** — the framework holds the structure and state; the LLM reasons within that structure and produces deliverables as output. The framework's role is to provide the context that makes the LLM's output informed and consistent.
- **Generated on demand** — created when the user requests them, not maintained as persistent state
- **Derived from things** — the LLM reasons over things and produces deliverables that synthesise, transform, or present that knowledge

### Deliverable Types

The LLM operating within the framework can produce any artefact type it is capable of generating. The framework does not constrain or define output formats — it provides the structured domain context that makes the output meaningful.

Common categories include:

| Category | Examples | Use Cases |
|----------|----------|-----------|
| **Documents** | Word (.docx), PDF, markdown, plain text | Reports, proposals, specifications, letters, summaries |
| **Code** | Source files, scripts, configurations, infrastructure-as-code | Software, automation, tooling, integrations |
| **Data** | CSV, JSON, YAML, spreadsheets | Exports, analysis outputs, structured data |
| **Structured outputs** | Calendar entries, notifications, reminders, emails | Workflow integration, time management |

What the LLM can produce depends on the LLM's own capabilities, not on the framework. A multimodal model might generate images or diagrams; a text-only model produces text-based artefacts. The framework is agnostic to this — its job is to provide the domain structure that informs the output, not to define what output formats are possible.

### The Relationship Between Things and Deliverables

```
Things (persistent state)
    ↓ LLM reasons over them (within the framework's structure)
Understanding (in-context)
    ↓ user requests a deliverable
Deliverable (produced by the LLM)
    ↓ delivered via output route
Human receives the result
```

A deliverable is a *projection* of the LLM's understanding at a point in time. The things remain. The deliverable is a snapshot, a transformation, a synthesis. The framework provided the structure that made the output reliable; the LLM did the work of producing it.

**Example:**

- Your domain has 30 things representing project tasks, dependencies, blockers, and decisions
- You ask: "Produce me a status report for the steering committee"
- The agent reads the relevant things, reasons about status, and produces a Word document
- The Word document is a deliverable — it doesn't live in `things/`; it's an artefact produced for a specific audience and purpose
- The things that informed it remain unchanged and continue to evolve

### Where Deliverables Live

Deliverables are not things. They don't belong in `things/`. Options:

- **Working directory** — produced in the current workspace for immediate use
- **Dedicated output folder** — `outputs/` or `deliverables/` if you want to track them
- **External systems** — sent directly to email, calendar, file share, or other tools
- **Ephemeral** — some deliverables are consumed immediately and don't need to persist (a verbal summary, a notification)

This is a domain-level decision. Your AGENTS.md or workflow skill can specify where deliverables are placed.

## Output Routes

Output routes mirror input routes — the response travels back through the same channel:

```
Processing complete
    ↓
Output formed (thing updates + optional deliverable)
    ↓
Output route (same channel as input, or specified destination)
    ↓
Human receives: response, deliverable, notification, or confirmation
```

In practice:

- **VS Code + Copilot** — response appears in chat; files created/modified in workspace
- **CLI tools** — response printed to terminal; files written to disk
- **Mobile apps** — response appears in conversation
- **Notifications** — calendar entries, reminders, and alerts pushed to phone/OS

## The Membrane: Another Domain as the Consumer

Not every consumer of a domain's output is the human. Since v3.22.0 a domain
can serve a **face** — the subset of its things marked `exposed: true` — and
another domain's agent can consume across that boundary. This is an output
route like the others: thin, replaceable, and carrying things rather than
prose. What makes it different is that the consumer is itself a reasoning
agent operating a separate id space, so the hand-off is **deliberate, never
implicit**:

- **Exposure is opt-in per thing** (`exposed: true`), and the relational
  graph is stripped on egress — edges do not travel raw across id spaces
  (`thing.md`).
- **The porch** (`mdllm mcp-serve <domain>`) serves the face over MCP —
  stdio (the consumer spawns the server) or Streamable HTTP (`--http`,
  loopback-bound until an authorization leg exists); a consumer wires either
  into its own `.mcp.json` (a `command` or a `url` entry). Same face, same
  membrane — the transport is the only difference.
- **Consumption is an import**: the consumer mirrors the thing, pins it with
  the reference triple (`source_domain`/`source_id`/`source_commit`), and
  quarantines it (`origin: external`, `verified: false`) until a human flips
  it — the same discipline as any external input (`provenance.md`).
- **Freshness is checkable**: `mdllm imports-check` re-checks every pin and
  mirror against the source's face (`fresh`/`stale`/`diverged`/`withdrawn`);
  `estate-check` batches it across consumers.

The direction of the membrane is a ruling, not a default — who consumes whom
is recorded, and a face that offers things a wired consumer never imports is
itself a surfaced fact (`porch_offers_unimported`,
`trigger-specification.md`). The full mechanism lives in `provenance.md`
(reference triple, re-quarantine-on-drift, ingestion vs import); this section
exists so the spec that owns output routes names all of them.

## What This Is Not

- **Not a new protocol** — no WebSocket spec, no REST API, no message format to implement
- **Not an agent-interface framework** — the core contract defines no UI components, rendering logic or display layer; an optional viewer can sit outside it
- **Not platform-specific** — works on any OS, any device, any LLM tool
- **Not prescriptive** — use whatever route suits your context; switch freely

## Design Implications

### For Domain Builders

When creating a domain, you don't need to think about interface. Your AGENTS.md, skills, and things work identically regardless of how the user reaches them. Focus on:

- Clear agent orchestration (AGENTS.md)
- Well-defined skills
- Well-structured things

The interface takes care of itself.

### For the Framework

The framework remains interface-agnostic. A new IDE, CLI, mobile client, or
voice surface becomes a *candidate* route when it can deliver the entry
contract and selected context to an LLM with the required file/tool access. It
becomes a verified route only after that discovery and consequence are
observed; portability of the contract does not certify a product automatically.

This is future-proofing through absence of opinion. The framework doesn't couple to any interface, so it survives all interface changes.

### For Scalability

As systems grow, the interface doesn't change. A domain with 10 things and a domain with 1,000 things use the same routes. The scalability challenge is in the processing layer (context windows, tiered loading) — not in the I/O layer.

## Summary

| Concern | Answer |
|---------|--------|
| How does input get in? | Through any existing route to an LLM (VS Code, CLI, mobile, voice) |
| What does the agent produce internally? | Things (persistent state in git) |
| What does the agent produce for the user? | Deliverables (documents, code, images, video, audio, notifications) |
| Do I need to build an interface? | No. Use what exists. |
| Is voice supported? | Yes, transparently, via OS-level speech-to-text feeding into any route |
| What if a new tool emerges? | It becomes a valid route if it can load AGENTS.md and pass context to an LLM |
