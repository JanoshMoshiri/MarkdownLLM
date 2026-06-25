---
id: mcp-domain-server-design
type: specification
status: draft
version: 0.2
created: 2026-06-25
tags: [cross-domain, mcp, interface, provenance, design-draft]
linked_things:
  - id: interface-specification
    relation: extends
  - id: provenance-specification
    relation: complements
  - id: orchestration-specification
    relation: complements
  - id: change-reconciliation-specification
    relation: complements
  - id: cross-domain-handoff-is-built-inbound-only
    relation: implements
  - id: cross-domain-handoff-is-verified-external-input
    relation: implements
  - id: directional-graph-reads-come-in-inbound-outbound-pairs
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# MCP Domain Server — Design Draft

**Status: design draft, not yet built.** This is the artifact we build from; the
deciding insight (`cross-domain-handoff-is-built-inbound-only`) is already pinned.
We capture the *implementation* insight when it ships, not before.

## What This Designs

The mechanism by which one domain exposes a curated face to another and lets the
other consume it — built on **MCP (Model Context Protocol)**, the established
agent-to-capability standard, so domains can later reach the wider agent community
with no rewrite. It realises the cross-domain federation model: each domain is an
MCP server (its *porch*); the consumer's client config is the *address book*
(operator-wired, per trust zone); the floor still owns provenance and freshness.

The guiding constraint, unchanged: **a domain stays comprehensible by reading only
itself plus its quarantined external imports.** MCP is a process boundary, which
*is* the trust boundary — only typed results and curated resources cross; the
producer's reasoning never flows into the consumer.

## Why MCP, And Why Not "Just HTTP"

The porch maps 1:1 onto MCP's three server primitives:

| Porch | MCP primitive |
|---|---|
| "what I know" (readable face) | **Resources** (read-only, URI-addressed) |
| "what I can do" (needs a live agent) | **Tools** (callable; the call wakes the domain agent) |
| templated workflows (`type: prompt` things) | **Prompts** (parameterised, client-invokable) |

**Transport — local is stdio, not HTTP.** MCP has two transports: **stdio** (the
client spawns the server as a subprocess — no port, no network) and **Streamable
HTTP** (a URL, for remote/other-party agents). Locally, domains are stdio servers
the consumer spawns on demand. Going public later is a **transport swap, not a
rewrite** — same server, same primitives, different pipe. This is the whole reason
to build on MCP now rather than bolt it on later.

**Vanilla MCP is capability exposure, not conversation.** The open-ended
agent-to-agent conversation is a *pattern composed on top* of tool calls (the cheap
manifest/handshake layer is MCP; the expensive conversation is built atop it), not
something the protocol hands you.

## The Subcommand

```
mdllm mcp-serve <domain-path>            # stdio (default) — local
mdllm mcp-serve <domain-path> --http [--port N]   # Streamable HTTP — later
```

A **thin adapter over the existing floor + repo.** The server holds no LLM of its
own; it reads the domain via the same machinery `mdllm` already has, and (for the
one live-agent tool) spawns a domain-scoped agent. Git remains the state machine.

### Resources — the readable face ("what I know")

- `manifest://<domain-id>` — the porch itself: name, liveness, the exposed
  catalog, the capability (tool) list, the address book ("who I know"), and the
  repo HEAD commit. This is the "give me your name, then your catalog" entry point.
  **Shape it as / align it with an MCP Server Card** (the emerging automatic-
  discovery convention, maturing H2 2026) so the organic discovery layer arrives as
  a standard feature rather than a bespoke build.
- `thing://<domain-id>/<thing-id>` — one exposed thing (frontmatter + body).
- `resources/list` enumerates **only exposed things**, never the whole corpus (the
  semi-permeable membrane; see *Exposure Control*).
- Every resource carries `source_commit` in its `_meta` so the consumer can record
  the reference triple and later detect drift.

### Tools — capabilities ("what I can do")

- `query_things(type?, tag?, status?, text?)` → list of `{id, type, status,
  summary, source_commit}` over the **exposed set only**. Bounded discovery into
  the corpus without exposing internals.
- `get_deliverable(id)` → `{content, frontmatter, reference_triple:
  {source_domain, source_id, source_commit}}` — the provenance-stamped fetch; the
  producing-side hand-off. (Browsing is `resources/read`; this is consume-with-
  provenance.)
- `run_domain_task(task, inputs?)` → **a Task handle** (not an inline result) — the
  **live-agent** capability, async by construction. See below.

Internal floor commands (`validate`, `touchpoints`, `cascade`, `index`) are **not**
exposed — they are the domain's private floor. Only the curated face crosses.

### Prompts — templated workflows

- `prompts/list` / `prompts/get` over the domain's `type: prompt` things and skill
  prompt templates, filled with the caller's arguments.

## How `run_domain_task` Hands Off To The Domain Agent — Async, On The Tasks Primitive

The server has no LLM, so a capability that needs reasoning must **spawn the
domain's own agent** — and that agent runs for *minutes* (long-horizon reasoning),
so the call **must be asynchronous**. Build it on MCP's **`Tasks` primitive**
("call-now, fetch-later"), never a synchronous tool call that blocks or times out:

1. `run_domain_task` returns a **Task handle immediately**; the server launches a
   **headless, domain-scoped agent session** (Agent SDK / `claude` headless),
   cwd = the domain repo, loading the domain kernel + `AGENTS.md` — so it reasons
   in *its own* context, not the consumer's.
2. The task moves through MCP task states (`working` / `input_required` /
   `completed` / `failed` / `cancelled`); the consumer polls or subscribes. The
   agent works within its domain (read / reason / write to its own repo, committing
   to its own git) and produces a deliverable.
3. On `completed`, the server returns the deliverable wrapped with the reference
   triple. `input_required` is the **native mid-task elicitation** channel — the
   producer can ask the consumer/operator a clarifying question without breaking
   the boundary — a sliver of the conversation layer, for free.

**This is why the bright line holds:** the producer agent runs in its own process
and context; the consumer receives only the returned deliverable, as quarantined
external input. The producer's reasoning is never visible to the consumer.

> **Not MCP sampling.** MCP `sampling` lets the *server* borrow the *client's* LLM
> — the wrong direction here (it would make the producer think with the consumer's
> head, blurring the boundary). We want the producer's *own* agent, so the server
> spawns it. Worth stating because it is a real MCP design fork.

## Design Guardrails — Hold These From The Ground Up

These do not constrain the local build; they keep "seamless outside interaction"
true later. They are the conditions under which adopting MCP *extends* us rather
than boxing us in. Tracked against the **2025-11-25 MCP spec** (OAuth 2.1) and the
2026 movements (Tasks, Server Cards, the MCP + A2A + WebMCP three-layer consensus).

1. **Floor owns semantics; MCP is only transport.** Provenance, freshness,
   quarantine, exposure live in `mdllm`; the MCP server only *projects* the domain.
   This is the single line that insulates us from MCP's own churn *and* lets an
   **A2A peer layer** (or REST, or whatever supersedes it) sit on top without
   touching a single domain. The tool surface must therefore be **drivable by a
   future peer/conversation layer** — design tools as capabilities A2A can call,
   not as a closed UI.

2. **One authorization model across both transports.** "Who may consume this
   domain / what is exposed" is a **floor concept**, enforced identically over
   stdio and HTTP — so going public is a transport + auth-config swap, not a
   redesign. On HTTP, the standard is **OAuth 2.1** (2025-11-25 spec); no
   long-lived API keys (a named MCP IAM failure mode). Locally, stdio is trusted-
   subprocess, but the *authorization decisions* still route through the same floor
   gate, so nothing is bolted on at the boundary later.

3. **The server is stateless; git is the state.** No session state in the MCP
   layer — every read is computed from the repo at a commit. This matches MCP's own
   stateless-server scaling direction and keeps the HTTP version horizontally
   scalable for free.

### Security Model (in and out)

The MCP boundary *is* the trust boundary; make both directions explicit.

- **Consuming (inbound) — external content is data, never instructions.** A thing
  pulled from another domain is `origin: external`, `verified: false`; nothing
  rests on it until a human confirms (`provenance.md`). This is the structural
  defence against **prompt injection / tool poisoning** — including a remote
  server's *tool descriptions and manifest*, which are equally untrusted. The
  operator-vetted address book is the **supply-chain** control: a domain is reached
  only because the operator wired it, never auto-trusted.
- **Serving (outbound) — never act on raw consumer input.** Resolve every requested
  id against the **exposed allowlist**; never construct a filesystem path from a
  consumer-supplied string (the path-traversal / argument-injection class behind
  the 2026 reference-server CVEs). The server serves the curated face and nothing
  outside it, by construction.

## Provenance & Freshness — Owned By The Floor, Not MCP

MCP moves the bytes; **`mdllm` owns the semantics.**

- The consumer records the reference triple (`source_domain` + `source_id` +
  `source_commit`) on import; the imported thing is `origin: external`,
  `verified: false` until a human confirms (`provenance.md` quarantine).
- A floor check — the **generalised upward version-check** (`orchestration.md`),
  lifted from the single privileged source (the framework) to an arbitrary
  `source_domain` — re-reads the source's current `source_commit` (via
  `manifest://` or `resources/read`) and compares it to the pin. **Drift re-opens
  the quarantine** (`verified: false` again), which hands the human an *external
  inflection* → `change-reconciliation` on the consumer's dependents.
- This is `re-quarantine-on-drift`: the standing-check twin of quarantine-on-import
  (`cross-domain-handoff-is-built-inbound-only`). Both consumer-side, because the
  boundary is an isolation boundary only the consumer chose to cross.

## The Address Book — The Client Config

The consumer's host MCP config *is* the address book, operator-wired (the
per-trust-zone address-zero / introducer). For a Claude Code host, e.g.:

```jsonc
// jmtm-software host — who it may consume from
"mcpServers": {
  "property-ventures": { "command": "mdllm", "args": ["mcp-serve", "domain/property-ventures"] },
  "eco-essentials":    { "command": "mdllm", "args": ["mcp-serve", "domain/eco-essentials"] }
}
```

Listing a server here is the intentional, expert-driven linking — discovery is
*not* organic; the operator seeds it. Optional global discovery (a registry/crawl
of manifests) layers on top later and never becomes required.

## Exposure Control — Curating The Face

Nothing crosses by default. A thing joins the exposed face only when its author
opts it in — a frontmatter marker (`exposed: true`, or the existing `interface.md`
deliverable concept). `resources/list` and `query_things` walk the exposed set
only. This enforces the membrane and the comprehensible-alone razor: a domain
publishes a *face it authored about itself*, never its raw interior.

## Worked Flow (real domains)

1. jmtm-software's host config lists `property-ventures` (stdio).
2. jmtm's agent calls `property-ventures.get_deliverable("rental-income-statement-2026")`.
3. The server reads the exposed thing, stamps the reference triple, returns it.
4. jmtm imports it `origin: external`, `verified: false`; operator verifies; it
   feeds the VAT return.
5. property-ventures later revises and re-commits the statement.
6. jmtm's freshness check sees the pinned `source_commit` moved → re-quarantines →
   the VAT return enters change-reconciliation.

## Phasing

1. **Read-only face (stdio).** `manifest://` + `thing://` resources +
   `query_things` + `get_deliverable`. Pure floor adapter, no agent. This alone
   delivers the consumes-from hand-off + the freshness/re-quarantine path — the
   whole consistency facet, end to end.
2. **Freshness check in the floor.** Generalise the upward version-check to
   arbitrary `source_domain`s; re-quarantine-on-drift; wire into change-reconciliation.
3. **`run_domain_task` (live-agent hand-off) — on the Tasks primitive.** Async by
   construction (handle + states), spawning the domain-scoped headless agent;
   `input_required` for mid-task elicitation.
4. **Prompts.**
5. **Streamable HTTP transport + OAuth 2.1.** Reach beyond the local machine —
   transport + auth-config swap, the authorization gate already in the floor from
   Phase 1. Align the manifest to the Server Card convention here for automatic
   discovery; the A2A peer layer composes on top of this surface.

## Build Status

- **Phase 1 — landed.** `mdllm mcp-serve <domain-path>` serves the read-only face
  over stdio: `initialize`, `resources/list` + `resources/read` (`manifest://` is
  Server-Card-shaped, `thing://<domain>/<id>`), `tools/list` + `tools/call`
  (`query_things`, `get_deliverable` with the provenance triple). Pure stdlib, thin
  transport over `scan()`. Egress source-scopes (strips the producer's internal
  graph). The pin is **per-thing** (the exposed thing's last-changed commit, source-
  computed — never over-fires on unrelated source commits) and is carried on each
  manifest `knows` entry.
- **Phase 2 — landed.** `mdllm imports-check <consumer>` is re-quarantine-on-drift,
  the consumer-side standing check. For each `origin: external` import it reads the
  source's **exposed face via MCP** (a minimal stdio client, spawning the source
  server through the `.mcp.json` address book) — **never the source's git**: a
  freshness read is a horizontal cross-domain read and obeys the same membrane as
  content. States: `fresh` / `stale` / `withdrawn` / `unreachable` / `no-address` /
  `incomplete`. **Report-only** — detection is mechanical, the re-quarantine (flip to
  `verified:false` / `status:stale`) is the agent's disposition; the floor never
  mutates a domain's things. **Offline = `unreachable` ("freshness unknown"), never a
  silent `fresh`.** Proven live (jmtm's import of code-architect reports `fresh`) +
  self-tests for fresh→stale, unreachable, and no-route.
- **Phase 3a — landed.** `mdllm mcp-serve <domain> --tasks` exposes `run_domain_task`
  (opt-in — the first write/compute-capable surface). It is standard MCP tool-use with
  an *agent* executor, made async via the **Tasks pattern**: `tools/call` returns a
  task handle, the caller polls `tasks/get` for the deliverable. Phase 3a ships a
  **stub executor** (no live agent, no writes) that proves the handle→poll round-trip;
  session-scoped in-memory task store (stdio). Proven live (jmtm calls
  code-architect's `run_domain_task`, gets a handle, polls the result). The Tasks
  *wire* isn't finalised upstream (H2 2026) — the pattern is kept thin in the transport
  to align later.
  **Topology (corrected, operator-reasoned):** the *skilled* domain exposes
  `run_domain_task` (code-architect — it owns the design/codegen skill); the consumer
  calls it with input (jmtm: "here's the website + the change I need"); the executor's
  agent works **in its own context** and returns the change as a deliverable; the
  **consumer applies it to its own files** (jmtm's agent writes the website). Neither
  domain reaches into the other — the owning domain's agent always edits its own files.
- **Phase 3b — landed.** The stub is replaced by the real executor: `run_domain_task`
  spawns **`claude -p`** (headless, read-and-emit) in the producer domain on a
  **background thread** — returns `working` immediately, the deliverable lands on
  `tasks/get`. Runtime overridable via `MDLLM_AGENT_BIN`, and **adapter-optional**: a
  missing runtime degrades to a clear `failed` (`no-agent-runtime`), never a crash.
  The read-and-emit prompt has the agent *produce* the change (not commit its own
  repo); the consumer applies it to its own files. Tested against a fake `claude -p`
  (real async `working`→`completed`) + the no-runtime path. **Live run is operator-
  driven** (needs `claude` auth + real tokens/minutes).
- **Phase 4 (prompts), 5 (Streamable HTTP + OAuth 2.1)** pending — Phase 5 is the
  external-agent test: a remote agent connecting to a domain over the wire, after
  which the MCP integration can be claimed publicly.

**Why MCP, not git, for the freshness read (decided):** the framework version-check
reads git (`.markdownllm`) because that's the **vertical/substrate** axis — public
substrate every domain inherits. Peer freshness is the **horizontal** axis, which
obeys the membrane: everything a consumer learns about a peer crosses through the
porch, including "have you changed?". git-direct would breach the boundary *and*
re-introduce the id-space leak (it needs the source's internal file path). Two-axis
rule: vertical → git, horizontal → face.

## Open Questions

- ~~Exposure marker~~ **Resolved: `exposed: true` frontmatter** (opt-in; default
  false). Note the floor already excludes `deliverables/` from `scan()` (interface
  deliverables are outputs, not things), so exposed things live under normal thing
  dirs — `interface.md` deliverable *files* are a separate, later concern.
- Does `get_deliverable` duplicate `resources/read`, or should the consumer stamp
  the triple itself from resource `_meta`? (Leaning: keep both — browse vs. consume.)
- Headless-agent runner: Agent SDK vs. `claude -p` headless vs. a generic adapter
  per harness (anchor: this should stay harness-optional, like other adapters).
- Where the freshness check fires: session-start (like the framework version-check),
  retrospective cadence, or invoked (`mdllm imports-check`). Likely all three tiers.
