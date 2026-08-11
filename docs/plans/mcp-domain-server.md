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

**Status: partially shipped; the rest is ruled, not pending.** (Disposition
2026-08-05, substrate-currency-sweep.) The read face and consuming side shipped
and grew beyond this draft — `mcp-serve`, `imports-check`, `estate-check` (v3.17
→ v3.23); this document remains the design source framework-map View 3 cites for
them. The **Phase 3 live-agent surface (`run_domain_task`) was built and then
reverted in full** (v3.17.0): a live-agent invocation is a different risk class
than the read face, and dormant execution code behind an opt-in flag is the
honour-system control the floor exists to replace. The reference triple and
`exposed` graduated from this draft into `thing.md`/`provenance.md` (v3.21);
the membrane's direction became doctrine in `provenance.md` (v3.23). Read those
specs for the current contract — this draft is kept for the design reasoning.

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
mdllm mcp-serve <domain-path> --http [--port N]   # Streamable HTTP — landed 2026-08-08, loopback-only
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
- ~~`run_domain_task(task, inputs?)`~~ → **DEFERRED, built then reverted** (not a
  shipped tool). The live-agent capability; its design is recorded below and in
  [[decisions/phase-3-run-domain-task-reverted]], but it is **not** part of the read
  face — a live-agent invocation is a different risk class, deferred to a later A2A
  layer.

Internal floor commands (`validate`, `touchpoints`, `cascade`, `index`) are **not**
exposed — they are the domain's private floor. Only the curated face crosses.

### Prompts — templated workflows

- `prompts/list` / `prompts/get` over the domain's `type: prompt` things and skill
  prompt templates, filled with the caller's arguments.

## How `run_domain_task` Hands Off To The Domain Agent — Async, On The Tasks Primitive

> **ARCHIVAL — DEFERRED CAPABILITY, NOT SHIPPED.** This section records a design
> that was built (Phase 3a/3b) and then **reverted in full** (see Build Status and
> [[decisions/phase-3-run-domain-task-reverted]]). It is kept as the explored
> reasoning, not as a description of code in the tool. The live-agent hand-off is
> deferred to a later, separate A2A peer layer with its own threat model.

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
3. **`run_domain_task` (live-agent hand-off) — DEFERRED, not on this roadmap.**
   Built and reverted (see Build Status). The live-agent surface is a different
   risk class from the read face; it belongs to a later, separate A2A peer layer
   with its own threat model, not to the cross-domain read face. Left here only as
   the record of the explored design.
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
  content. States: `fresh` / `stale` / `diverged` / `withdrawn` / `unreachable` / `no-address` /
  `incomplete`. **Report-only** — detection is mechanical, the re-quarantine (flip to
  `verified:false` / `status:stale`) is the agent's disposition; the floor never
  mutates a domain's things. **Offline = `unreachable` ("freshness unknown"), never a
  silent `fresh`.** Proven live (jmtm's import of code-architect reports `fresh`) +
  self-tests for fresh→stale, unreachable, and no-route.
- **Phase 3 (`run_domain_task`) — built, then REVERTED at v3.16.x. Not in the tool.**
  3a (async stub) and 3b (real `claude -p` executor on a background thread, plus the
  `get_task_result` poll tool and `wait: true` sync mode) were built and tested
  against a fake `claude -p` — and then **removed in full from `mdllm.py`** (the
  `--tasks` flag, the executor, the task store, the task tools). The live agent path
  **never ran once**. The decision and its reasoning are pinned in
  [[decisions/phase-3-run-domain-task-reverted]]; the design reasoning below is kept
  as the record of what was explored, not as a description of shipped code.
  **Why reverted:** a live-agent invocation is a different *class* of risk from the
  read face — resource exhaustion, agent-injection via task inputs, an unbounded
  compute surface — and the content trust model ("external content is quarantined
  data") was built for the *content* path and does not cover it. Keeping dormant
  execution code behind an opt-in flag is an honour-system control where the floor
  can give a mechanical guarantee instead (the framework's own founding correction):
  removed, the surface cannot be reached at all. Built ahead of felt need, too — one
  real consumer pair, no second. The live-agent hand-off belongs to a **later,
  separate A2A peer layer** with its own threat model, never bolted onto the read
  face. Re-open only when a second real consumer pair exists *and* it earns its own
  project.
- **Phase 5, transport leg — landed (2026-08-08).** `mdllm mcp-serve <domain>
  --http [--port N]` serves the identical face over Streamable HTTP: one
  dispatcher shared with stdio (`mcp_make_dispatcher` — error mapping cannot
  drift between pipes), one endpoint (`POST /mcp`, JSON-RPC in,
  `application/json` out, notifications 202, GET 405 — poll-only, git is the
  state), re-scan per request (a long-lived porch serves the repo as it
  stands, never as it stood at bind time — design guardrail 3 made
  mechanical). The consumer side crossed with it: the `.mcp.json` address
  book accepts `url` entries alongside `command`, and `imports-check` /
  `estate-check` read a served face over the wire with unchanged membrane
  semantics (unreachable = unknown, never a silent fresh). **Loopback-bound
  by refusal, not by warning:** a non-loopback `--host` exits with the reason
  — a routable porch without OAuth 2.1 would be an honour-system control, and
  dormant-capability-behind-a-flag is exactly what the Phase 3 revert ruled
  out. Origin-carrying (browser-borne) requests are checked against loopback
  origins — the DNS-rebinding defence the Streamable HTTP spec requires.
- **Phase 5, probe control — landed (2026-08-08).** `--token` gates every
  HTTP request behind `Authorization: Bearer <token>`; with no value a
  per-run token is minted and printed once to stderr. This is the
  cross-machine *probe* control — the operator carries the token from the
  serving machine to the consuming session themselves, so possession IS the
  authorization, and it dies with the process (never the long-lived API key
  the doctrine bans). The consumer's `url` address-book entry carries it as
  a `headers` map (the `.mcp.json` convention). Scope stated plainly: this
  authorizes *the operator's own trust zone stretched over a tunnel* (e.g.
  a loopback-bound porch behind an ephemeral cloudflared URL), not
  other-party consumers.
- **Phase 5, probe record (2026-08-08).** The cross-machine probe ran as
  designed on the operator side and was blocked on the consumer side by the
  consumer's harness, not by anything here. Proven to the public edge:
  loopback porch + per-run token + cloudflared quick tunnel; authorized
  JSON-RPC reads served through the tunnel, tokenless requests 401'd *at
  the porch* (the tunnel adds no trust). Blocked: an Anthropic Cowork VM's
  egress is a default-deny proxy allowlist (anthropic.com, package
  registries, GitHub, private ranges) — the CONNECT was refused before any
  packet left the VM, and the VM agent verified the deny is
  provider-agnostic (any tunnel host or VPS hits the same 403). So the
  external-agent test remains open for reasons outside the porch: it needs
  a consumer environment whose egress can reach an operator-chosen host.
  **Noted, not adopted:** the VM agent's suggestion of a git-backed face
  (GitHub *is* on the allowlist, and the reference triple is already
  git-shaped) — it collides head-on with the decided two-axis rule
  (horizontal reads cross through the face, never the source's git). If
  VM-resident consumers become a real consumer class, that tension earns
  its own decision; it does not get swapped in quietly because one proxy
  allowed one host.
- **Phase 5, authorization leg (OAuth 2.1) — pending.** This, not the
  transport, is now the external-agent gate: a remote agent connecting over
  the wire, after which the MCP integration can be claimed publicly. The
  transport swap is done; going public is an auth-config swap on top of it,
  exactly as guardrail 2 planned. Hand-rolling an authorization server in
  the floor's stdlib style is the wrong build — when this is felt, lean on
  an external AS; the porch's job stays resource-server-side token
  validation.
- **Phase 4 (prompts)** pending.

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
