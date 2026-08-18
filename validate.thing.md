---
id: validate-thing-specification
type: specification
status: stable
version: 2.7
created: 2026-05-19
linked_things:
  - id: thing-specification
    relation: validates
  - id: orchestration-specification
    relation: validates
  - id: belief-revision-specification
    relation: complements
  - id: derived-index-specification
    relation: validates
  - id: provenance-specification
    relation: validates
  - id: divergence-is-an-unrouted-decision
    relation: implements
  - id: domain-specification-guide
    relation: complements
    notes: "v2.0 resolved the status-vocabulary conflict (status-vocabulary-universal-vs-domain): domains own their vocabularies via the normative schema"
---

# Validate Thing

<!-- kernel -->
**Mechanical validation is the tool's job:** `mdllm validate <path>` through the manual CLI launch route declared in the domain's on-disk AGENTS.md — structure, references, schema conformance, index integrity. On Windows PowerShell and Codex managed shells that route is `tools/mdllm.ps1`, even when `python` exists; never substitute a harness-bundled interpreter that has not dependency-probed PyYAML. Exit 1 = Errors; the pre-commit hook blocks them at the boundary. **Never re-perform mechanical checks by reasoning.** Never bypass the hook (`--no-verify`); if validation blocks a legitimate change, the schema is wrong — fix it with the human.

**Semantic validation is yours:** metadata–narrative consistency · scope (split/merge per decomposition tests) · staleness · trigger coherence · duplicates · *disposition* of insights/conflicts the floor flags as orphaned from session memory — no inbound edge from a live thing (promote/dismiss/link from live work/keep-active). Advisory tone ("I noticed…"), never blocking. (Retrospective cadence and quarantine age moved to the floor in v3.24.0 — Info findings, mechanically computed.)

**Arithmetic is mechanical — never perform it by reasoning.** A figure you derive is declared as a derivation (`computed:`, thing.md) and computed by `mdllm calc`; you transcribe and reason about the result, you do not add up the column. A sum you assert cannot be re-checked by anyone, including you.

**The session gate** (declared per domain — scaffold births every new domain `strict`, so "opt-in" describes the declaration mechanism, not the scaffolded default; the framework root declares `warn`): a domain declaring `options: {session_gate: warn|strict}` requires a fresh `mdllm session-start` attestation for the clone before any commit — absent or >24h old fires Warning (`warn`) or a commit-blocking Error (`strict`), with the remedy named. It proves the Tier-0 contract was *emitted into the session*, not that it was heeded; its job is making a contract-less session loud at the first write, in any harness, with no adapter.

**Severities:** Error = fix now (blocks commit) · Warning = should fix · Info = worth knowing, may be intentional.
<!-- /kernel -->

You are validating things within a domain using the MarkdownLLM framework. Since
v2.0, validation has two layers with a strict division of labour:

> **The tool guarantees the mechanical checks. You perform the semantic ones.
> Never re-perform by reasoning what the tool has already guaranteed by parsing.**

This division exists because the framework's own history proved that LLM-performed
mechanical validation fails silently under context pressure: in June 2026 every
thing in the framework's only production domain violated the then-current status
rule at Error severity, undetected (see conflict `status-vocabulary-universal-vs-domain`,
resolved). Mechanical checks are now code; your reliability budget is reserved for
what only you can do.

## Layer 1: The Mechanical Floor (delegated to `mdllm`)

Run the tool — do not reason through these checks:

```
mdllm validate <domain-path>  # expand through AGENTS.md's manual CLI route
```

The tool enforces, deterministically:

- **Structural (old Level 1):** frontmatter parses; `id`/`type`/`status`/`created`
  present; `id` format and filename match; ISO dates; `linked_things` /
  `dependencies` / `blocks` / `triggers` shapes; body and title presence.
- **Referential (old Level 2):** all referenced ids exist (`linked_things`,
  `dependencies`, `blocks`, `parent`, `parties`, trigger `watch`); no duplicate
  ids; no circular dependencies; bidirectional consistency; orphan detection;
  a terminal-status thing may not depend on unfinished work (terminal deps count
  as resolved); `contradicts` requires a conflict thing listing both parties;
  `supersedes` requires a back-link or deprecation.
- **Schema (old Level 3):** the domain's normative schema (`things/_schema.yaml`
  or root `_schema.yaml`) declares thing types, **status vocabularies**, required
  fields, the relation vocabulary, and (opt-in) the **frontmatter-field
  vocabulary** (`known_fields`). The tool validates against it.
- **Field registration (opt-in, Warning):** the floor reads a fixed set of
  universal structural fields (`CORE_FIELDS`, built into the tool). When a domain
  declares `known_fields` in its schema, any frontmatter key in neither set is
  flagged — closing the silent-loss hole where a mis-keyed field (e.g.
  `relations:` typed where `linked_things:` was meant) used to pass clean because
  only field *values* were checked, never the *set of keys*. Registering a new
  field is a deliberate act (decide it belongs, add it to `known_fields` in the
  same write); the tool never auto-syncs. Enumerate the in-use set to bootstrap
  or audit the list with `mdllm index <path> rebuild --signal schema`.
- **Index integrity:** `mdllm index <path> check` performs the rebuild-and-diff
  drift detection for derived indexes (`derived-index.md`).
- **Session-memory completeness (Info):** an `active` insight or `open` conflict
  with no inbound edge from a live (non-terminal) thing is orphaned from session
  memory — it returns to no future session and is invisible to the session-start
  staleness check (which walks only the live, graph-connected insights). Liveness
  is a **graph property, not presence in a brief** (`continuity.md` is retired);
  a `disposition: keep-active` marker — carrying a `disposition_reason` — keeps a
  standing or parked insight live without an inbound edge, and a `keep-active`
  missing its reason is itself nudged. Detection is mechanical; the *disposition*
  (promote, dismiss, link from live work, or keep-active) is the agent's, driven at
  session-end and retrospective cadence. Corpus-general.
  (`session-memory.md` → Insight Lifecycle Management.)

Exit code 1 means Errors exist. The git `pre-commit` hook (installed via
`mdllm install-hook`) runs the same validation, so things with Errors cannot be
committed. The hard floor is the hook, not your diligence.

### Status Vocabularies — Who Owns Them

**The domain owns its status vocabulary.** The normative schema declares the
statuses (and optionally transitions) valid for each domain thing type. The six
universal workflow values (`not-started`, `in-progress`, `blocked`, `paused`,
`completed`, `cancelled`) are the *default* — they apply, at Warning severity,
only when no schema declares a vocabulary for the type.

Framework-reserved types keep fixed vocabularies that domains cannot redefine
(the tool's `RESERVED_STATUSES` is the authority; this table restates it and
lagged it once — three types missing for two releases — so on any
disagreement, the tool wins):

| Type | Statuses |
|---|---|
| `specification`, `guide`, `manifesto`, `skill`, `prompt` | `draft`, `evolving`, `stable`, `deprecated` |
| `insight` | `active`, `promoted`, `dismissed` |
| `continuity-brief` | `live` |
| `conflict` | `open`, `resolved` |
| `retrospective` | `draft`, `complete` |
| `decision` | `made`, `superseded` |
| `workflow-definition` | `draft`, `evolving`, `stable`, `deprecated` |
| `workflow-run` | `active`, `paused`, `completed`, `abandoned` |
| `index` | `live`, `stale` |

### Severity Semantics (unchanged)

- **Error** — must be fixed; the thing is malformed and blocks commit
- **Warning** — should be fixed; functional but off-convention
- **Info** — observational; may be intentional (e.g. orphaned things)

## Layer 2: Semantic Validation (yours)

This is reasoning, not parsing — the tool cannot do it, and it is why you exist
in this loop. Read things holistically and assess:

| Check | What to look for | Severity |
|---|---|---|
| Metadata-narrative consistency | Status says `completed` but body says "waiting on feedback"; priority `low` but body describes urgency; tags don't match content | Warning |
| Scope appropriateness | Thing doing too much (split it) or trivially small (merge it) — apply thing.md's decomposition tests | Info |
| Staleness | `in-progress` for months with no narrative movement — abandoned rather than active | Info |
| Narrative completeness | Does the body explain what this is and why it matters, or is it an empty title? | Info |
| Trigger coherence | Do declared triggers make sense for this thing? Watching relevant things? Appropriate actions? | Info |
| Duplicate or redundant | Substantial overlap in scope or intent with another thing — a candidate for composition (`thing.md` → The Inverse: Composition) | Info |
| Disposition of a flagged insight/conflict | The floor flags an `active` insight or `open` conflict with no inbound edge from a live thing (Layer 1); deciding whether to promote, dismiss, link it from live work, or mark `keep-active` is yours, at session-end and retrospective cadence | Info |
| Stale open conflict | Open conflict untouched for 30+ days | Info |

*(Retrospective cadence — 60 days active since the last `type: retrospective` —
is **not** in this table: it moved to the floor in v3.24.0
(`retrospective_findings`, mechanically computed from git dates) and re-deriving
it by reasoning violates this spec's own first rule. A ninth-review finding:
this row survived here for two releases after the move.)*

Semantic findings are advisory. Present them as "I noticed…" rather than "Fix this."

### Prompt Semantic Checks

Prompts (`type: prompt`) pass through the mechanical floor like any thing. Your
semantic checks for them:

| Check | What to look for | Severity |
|---|---|---|
| Reasoning template scope | Focused on one reasoning task? Prompts should be tighter than skills | Info |
| Duplication | Template overlaps another prompt or skill prose | Warning |
| Quantity | More than ~10 domain prompts signals over-specification | Info |
| Binding integrity | `bound_to` hooks match hook points declared in `orchestration.md` or the domain workflow skill | Warning (advisory — this is a Layer-2 agent check; the floor reads `bound_to` nowhere, and a severity that "blocks commit" cannot be assigned to a check nothing blocks on. A review-loop finding: this row said Error for two releases against the same table's own "semantic findings are advisory") |

*(v2.0 removed the input/output chain-consistency check between prompts — it was
type-checking for an event system with no runtime, and no domain ever used it.)*

## When Validation Runs

1. **At commit — always, mechanically.** The pre-commit hook runs the tool. This
   is the floor; it does not depend on anyone remembering.
2. **After writes** — you run the tool before committing to see findings early
   and fix them in the same operation.
3. **Session start** — if orientation suggests drift (version mismatch, external
   edits), run the tool and report: "N things have issues since your last session."
4. **On demand** — "validate my things" → run the tool, then add Layer 2 semantic
   review on top. "Deep review of X" → full semantic pass on that thing.

## Reporting

Relay the tool's report (it already groups Errors/Warnings/Info with a summary),
then append your semantic observations under a `### Semantic (LLM review)`
heading. When the user asks you to fix issues, apply `write.thing.md`, re-run the
tool, and confirm clean.

## What You Don't Do

- Do not re-perform mechanical checks by reasoning — run the tool
- Do not silently fix issues — report what you found and changed
- Do not treat Info as Error; do not block work on Warnings
- Do not invent validation rules beyond `thing.md`, `orchestration.md`,
  `derived-index.md`, the domain schema, and this spec
- Do not bypass the pre-commit hook (`--no-verify`) — if validation blocks a
  legitimate change, the schema is wrong: fix the schema, with the human

## The Guarantee, Restated

Mechanical checks are deterministic because they are code: same input, same
result, byte-level parsing, exit codes. Semantic checks are non-deterministic
because they are judgement — that is their value, not their weakness. The
framework's earlier design asked one reasoning system to provide both and got
neither reliably. The split is the fix, and it is also the manifesto's own
principle applied honestly: the LLM is the reasoning engine, not the parser.

This spec is the **no-silent-default face** of the divergence-routing primitive
(`divergence-is-an-unrouted-decision`): "do not silently fix issues — report what
you found and changed" is that law made mechanical. A validation finding is a
model–reality divergence surfaced for routing, never resolved by blur.
