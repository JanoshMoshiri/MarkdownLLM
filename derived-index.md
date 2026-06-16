---
id: derived-index-specification
type: specification
status: draft
version: 1.0
created: 2026-06-08
linked_things:
  - id: thing-specification
    relation: extends
  - id: orchestration-specification
    relation: complements
  - id: trigger-specification
    relation: complements
  - id: belief-revision-specification
    relation: complements
  - id: scalability-guide
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: tracking-artifacts-can-drift-from-reality
    relation: implements
  - id: structural-pointers-need-reverse-edge-indexing
    relation: implements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Derived Index

## What This Specifies

A **derived index** is a regenerable file that aggregates one signal across all the things in a domain, so the agent can evaluate that signal at session start without loading every thing. It is the framework's mechanism for making *reflexive* behaviour — the agent reasoning *about* the domain rather than *within* it — cheap enough to run routinely.

The four reflexive behaviours the framework wants are all the same shape:

| Behaviour | Signal aggregated | Index |
|---|---|---|
| Systematic trigger evaluation | Every active trigger across all things | `triggers` index |
| Schema coherence review | Every domain-specific frontmatter field in use | `schema` registry |
| Systematic conflict scanning | Every declared edge — `linked_things` plus the structural pointers `definition`/`parent` | `relationships` index |
| Domain velocity | *(none — reads git directly)* | no index needed |

The first three are instances of one primitive defined here. The fourth — velocity — is deliberately *not* an index: it reads `git log` (already ground truth), so caching it would add a drift surface for no benefit. See `git-workflow.md` → Git Log As Domain Telemetry.

The `relationships` index aggregates **every declared edge, wherever it lives** — not only `linked_things` relations but the singular structural pointers that earn their own field (`parent`, `definition`, modelled on `parent`). A declared edge in a structural field is no less declared than one in `linked_things`; omitting it would leave a reverse read over the index blind to a parent's children and a definition's runs, which is exactly the recall the change-reconciliation Assimilate beat depends on. The rule is general: any future singular load-bearing pointer added to the schema must also be emitted here, or it becomes an unwalked declared edge. See `structural-pointers-need-reverse-edge-indexing`.

## The Drift Problem This Must Not Repeat

The framework has twice committed work without updating every tracking surface, leaving surfaces that silently disagreed with reality (see `tracking-artifacts-can-drift-from-reality`). An index is, by construction, a second copy of information that lives authoritatively in the things. **Naively, an index is a drift machine.** Everything in this spec exists to make drift *detectable and correctable* rather than silent.

The governing rule:

> **A derived index is a cache, never a source of truth. When the index and the things disagree, the things win and the index is rebuilt.**

## `type: index`

Index files are things with `type: index`. They are framework-internal, generated artifacts — like the WORKLOG, they are not authored by hand as domain content.

- **Status:** index things use `status: live` (current and regenerated) or `status: stale` (known to lag the things — a transitional state validation may set). They do not use workflow or lifecycle statuses.
- **Location:** `things/_index/` within the domain. The leading underscore keeps generated indexes visually and lexically separate from authored things, and lets read operations skip the directory during ordinary thing scans.
- **One per signal per domain.** A domain has at most one `triggers` index, one `schema` registry, one `relationships` index.

## Anatomy

Every derived index carries **provenance frontmatter** — this is what makes staleness detectable:

```yaml
---
id: [domain]-triggers-index
type: index
status: live
index_of: triggers              # which signal this aggregates
created: [ISO-date]
generated: [ISO-datetime]        # when this index was last rebuilt
generated_from: HEAD@[short-sha] # the commit the index reflects
coverage: 47                     # number of things scanned to build it
framework_version: 2.9           # framework version of the generating spec
---
```

| Field | Purpose |
|---|---|
| `index_of` | The signal aggregated. Lets a reader and validator know which rebuild procedure applies. |
| `generated` | Timestamp of last rebuild. With `generated_from`, this is the anchor for staleness checks. |
| `generated_from` | The commit the index reflects. If `HEAD` has moved past this and touched things, the index *may* be stale. |
| `coverage` | How many things were scanned. If the domain now has more things than `coverage`, the index is provably incomplete. |
| `framework_version` | Detects an index generated under an older index spec. |

The body is a compact, scannable aggregation — see the templates in `templates/indexes/`. The body is *not* prose; it is the densest faithful representation of the signal, optimised for the agent to read at session start.

## Maintenance Model

There are two ways an index stays current. Both are necessary; neither alone is sufficient.

### 1. Incremental update — rides the `post-write` event

The `post-write:commit` hard hook already fires whenever the agent modifies a thing — an observable, agent-caused event (the only kind that can carry a hard obligation; see `hard-hooks-require-observable-agent-caused-triggers`). Index maintenance attaches here: in the same operation that writes and commits a thing, if the domain maintains an index whose signal the written thing affects, update that index's relevant entry and `generated`/`generated_from` fields, and include it in the same commit.

This is declared as a **domain-level hard hook**, not a new framework-level one — indexes are opt-in, so the obligation only exists for domains that have adopted them:

```yaml
hard_hooks:
  - hook: post-write
    action: "If the written thing has triggers, update things/_index/triggers.md in the same commit"
  - hook: post-write
    action: "If the written thing introduces a frontmatter field absent from things/_index/schema.md, register it in the same commit"
```

Incremental update keeps the index current at the one moment the agent is guaranteed to be looking at the changed thing. It is cheap because it touches one entry, not the whole domain.

### 2. Full rebuild — on demand and at validation

Incremental update can still drift: a hand-edited thing, a `git revert`, a file deleted outside the agent, a missed hook under context pressure. So the index is also **fully regenerable** from the things at any time. Full rebuild happens:

- When validation detects drift (below)
- At a retrospective
- On explicit request ("rebuild the indexes")
- When `framework_version` in the index lags the current framework

Rebuild is authoritative: discard the index body, re-scan all things, regenerate, and reset all provenance fields. A rebuild can never be wrong relative to the things — that is the whole point of keeping the things as the source of truth.

## Drift Safety — Validation

`validate.thing.md` gains an **Index Integrity** check. This directly implements the mitigation proposed in `tracking-artifacts-can-drift-from-reality` (validation should detect surfaces that disagree with reality). For each index in `things/_index/`:

| Check | Rule | Severity |
|---|---|---|
| Coverage current | `coverage` equals the current count of in-scope things | Warning |
| Provenance present | `generated`, `generated_from`, `coverage`, `index_of` all present | Error |
| Commit not behind | `generated_from` is `HEAD`, or the commits since it touched no in-scope thing | Warning |
| Rebuild-and-diff | Regenerate the index in memory and compare to the stored body; any divergence is drift | Warning |
| Framework version current | `framework_version` matches the live framework version | Info |

Drift is a **Warning**, not an Error: a stale index doesn't corrupt anything — the things are still correct — it just means the agent should rebuild before trusting it. Validation that finds drift should offer to rebuild.

## When To Deploy An Index

Indexes are **opt-in and scale-triggered.** A small domain does not need them — the agent can scan every thing's frontmatter cheaply, and an index would be pure overhead and an extra drift surface. Adding mandatory index machinery to every domain would also load the agent with reflexive work it doesn't need, degrading compliance on the hooks that matter (see `hook-compliance-correlates-with-scope-not-awareness`).

Deploy an index when **the cost of scanning all things for a signal at session start becomes noticeable** — in practice, past ~100–150 active things, or whenever a domain wants a reflexive behaviour (systematic trigger eval, conflict scanning, schema review) to run on *every* session rather than on demand. This is the same "deploy when felt" discipline the scalability guide applies to summaries and `thing-lifecycle.md`.

## Context Footprint

The point of an index is to convert an O(all things) read into an O(index) read. A thing's frontmatter costs **~100–200 tokens** (measured 2026-06-12, tiktoken o200k_base, across the framework corpus and two live domains — per-domain averages 96–204; re-measure rather than assert, this is the same lesson as `tracking-artifacts-can-drift-from-reality`):

| Operation | Without index | With index |
|---|---|---|
| Trigger evaluation, 50 things | ~5–10k tokens (all frontmatter at ~100–200/thing) | ~1.5–3k (index only) |
| Schema review | full frontmatter scan | ~0.8–1.2k (registry) |
| Conflict scan, 50 things | Level 2 load of all things (~5–10k — L2 is frontmatter-resident) | ~2–4k (relationship index) + targeted Level 2 on suspects |

The write-time cost of incremental maintenance is small and distributed across many sessions. The read-time cost stays roughly flat as the domain grows, because the index aggregates rather than reproduces. This is the same economics as tiered loading, applied to reflexive behaviour.

## Relationship To The Scalability Principle

`scalability-guide.md` states: *"Scale through abstraction, not through search or indexing. Don't build database functionality."* A derived index is reconciled with — not a violation of — that principle:

- It is **transparent**, not hidden state: a git-committed markdown file the human can read and diff.
- It is **regenerable**, not authoritative: it holds no information not present in the things.
- It **directs attention**, it does not answer queries: the agent still reasons over the actual things; the index only tells it *which* things and *which* signal to look at.

The principle forbids an opaque query/database layer that becomes the thing the agent reasons over instead of the data. A derived index is the opposite: a thin, visible, throwaway map that points back at the data. See `derived-index-is-attention-cache-not-search-layer` for the full reconciliation.

## Relationship To Other Specs

- **thing.md** — `index` is a framework-internal type defined here; all other mechanics are inherited.
- **orchestration.md** — Index maintenance is declared as a domain-level hard hook on `post-write`; index evaluation is performed by bound prompts (`evaluate-triggers`, `detect-conflicts`, `review-schema-coherence`) at their respective hook points.
- **validate.thing.md** — Owns the Index Integrity check that makes drift detectable.
- **trigger-specification.md** — The `triggers` index is the scalable substrate for session-start trigger evaluation.
- **belief-revision.md** — The `relationships` index makes systematic conflict scanning affordable.
- **git-workflow.md** — Velocity reads git directly and needs no index; indexes are committed like any other thing, with provenance pinned to a commit.
- **scalability-guide.md** — Indexes are the scale-triggered lever that keeps reflexive behaviour sub-linear.
