---
id: provenance-specification
type: specification
status: draft
version: 1.0
created: 2026-06-11
linked_things:
  - id: thing-specification
    relation: extends
  - id: git-workflow-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
  - id: interface-specification
    relation: complements
  - id: belief-revision-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Provenance

## What This Specifies

How a domain makes its outputs *defensible*: the traceable chain from domain
knowledge, through the decisions that interpreted it, to the artefacts those
decisions produced. After this spec, any deliverable can answer: **"which
knowledge, at exactly which version, justified you — and was that knowledge
trusted?"**

The mechanism is two primitives and one rule:

1. **`type: decision`** — a record whose inputs are *pinned* to git commits
2. **`origin: external`** — content from outside the human-agent pair, quarantined
   until verified
3. **The pinning rule** — provenance references name a thing *and* the commit
   whose version of that thing was actually used

Git already provides immutable versioning; provenance is just pinning. No new
storage, no new infrastructure — the commit SHA is the citation.

## `type: decision`

A decision is a framework-reserved type: the durable record of a judgement made
from knowledge. It is ADR-shaped — context, options, choice, consequences — with
one structural addition: `informed_by` pins every input.

```yaml
---
id: [descriptive-decision-id]
type: decision
status: made            # made | superseded
created: [ISO-date]
session: [YYYY-MM-DD]
decided_by: human|agent|both
confidence: high|medium|low
informed_by:
  - id: [knowledge-thing-id]
    commit: [short-sha]      # the committed version actually used
  - id: [another-thing-id]
    commit: [short-sha]
linked_things:
  - id: [produced-output-or-affected-thing]
    relation: informs
---

# [Decision Title]

## Context
[What question or judgement this decision answers, and why it arose.]

## Inputs Considered
[What the pinned knowledge said — brief, since the pins point to the full content.]

## Options
[The realistic alternatives, each with its material trade-off.]

## Decision
[What was decided, by whom, and the reasoning that carried it.]

## Consequences
[What this commits the domain to; what outputs derive from it.]
```

**Statuses:** `made` (in force) and `superseded` (a later decision replaces it —
link the successor with `relation: supersedes` per `belief-revision.md`).

**Location:** `things/decisions/` within the domain.

**When to write one:** whenever an output's correctness depends on a judgement
that interpreted domain knowledge — a filing computed from records, a proposal
triaged against constraints, a design chosen against requirements. Routine
mechanical transformations do not need decision records; judgements do.

## The Chain

```
knowledge thing (pinned at commit) ──informed_by──▶ decision ──derived-from──▶ output
```

- **Decisions pin their inputs** via `informed_by: [{id, commit}]`.
- **Outputs link their decisions**: a thing produced from a decision carries
  `linked_things: [{id: the-decision, relation: derived-from}]`. Deliverables
  that live outside `things/` (documents, code — see `interface.md`) state their
  decision IDs in their own content or metadata block.
- **Walking backwards** from any output: output → decision → exact versions of
  the knowledge that justified it. `git show <commit>:<path>` resolves any pin.
- **Walking forwards** (which outputs does this knowledge support?) is the
  reverse-provenance question — answered by the `provenance` derived index
  (`mdllm index <path> rebuild --signal provenance`), which aggregates every
  `informed_by` and `derived-from` edge. This is what makes **diff-driven
  regeneration** possible: when a knowledge thing changes, the index names every
  decision and output whose pinned version is now behind — candidates for re-run.

## `origin: external` and Quarantine

`thing.md`'s `origin` field gains a fourth value:

| origin | Meaning |
|---|---|
| `stated` | Explicitly said by the human |
| `inferred` | Concluded by the agent from other things |
| `synthesised` | Assembled by the agent from multiple sources |
| **`external`** | **Ingested from outside the human-agent pair** — bank statements, emails, scraped pages, vendor documents, OCR output, third-party data |

**The quarantine rule:** an `origin: external` thing carries `verified: false`
until a human confirms its content (reconciliation, review, spot-check), which
flips it to `verified: true` with a note of how.

> **No decision may pin an unverified external thing. No calculation, filing, or
> generated output may rest on one.**

This is a security and correctness control, not bookkeeping. Things are
instructions to every future session of the agent; a poisoned or simply wrong
external thing is a durable injection into every downstream output. For domains
that file tax returns or generate client deliverables, the quarantine is the
difference between "the agent read it somewhere" and "the record was verified."

The agent may freely *create* external things during ingestion (that is the
point — capture everything), may reason *about* them ("this statement appears to
show…"), and must *surface* unverified things blocking a decision rather than
quietly using them.

## Enforcement

The mechanical parts of this spec are validated by the deterministic floor
(`validate.thing.md` v2.0):

```
python {framework_root}/tools/mdllm.py provenance <domain-path>
```

| Check | Rule | Severity |
|---|---|---|
| Pin shape | Every `informed_by` entry has `id` and `commit` | Error |
| Pin resolves | The pinned commit exists in the domain repo | Error |
| Input exists | The pinned id resolves to a thing (current corpus, or present at the pinned commit) | Error |
| Quarantine | No decision pins a thing with `origin: external` and `verified` not `true` | Error |
| Freshness | A pinned input has changed in commits after the pin — decision may be stale | Info |
| External unverified | `origin: external` things with `verified: false` older than 30 days | Info |

Freshness is **Info, not Error**: a decision made on yesterday's knowledge is not
wrong — it is *dated*, and whether to re-decide is a judgement (the agent's, then
the human's). The semantic questions — does the decision's reasoning actually
follow from its inputs? is a verification credible? — remain the LLM's layer.

## Relationship To Other Specs

- **thing.md** — `decision` joins the framework-reserved types; `origin` gains
  `external`; `verified` is defined here.
- **git-workflow.md** — commits are the citation units; pinning depends on the
  `post-write:commit` hard hook keeping every version addressable.
- **validate.thing.md / mdllm** — owns mechanical enforcement (above).
- **derived-index.md** — the `provenance` index is a standard derived index:
  regenerable, provenance-stamped, drift-checked by rebuild-and-diff.
- **belief-revision.md** — superseding a decision follows the standard
  `supersedes`/`superseded-by` protocol.
- **interface.md** — deliverables are projections of understanding; this spec
  makes the projection citable.
