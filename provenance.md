---
id: provenance-specification
type: specification
status: draft
version: 1.1
created: 2026-06-11
linked_things:
  - id: membrane-attention-cluster
    relation: informs
    notes: "The membrane-direction ruling, withdrawal etiquette, and ingestion triple landed from this plan"
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
  - id: change-reconciliation-specification
    relation: complements
    notes: "A stale or diverged cross-domain import is the external-inflection cue entering its four beats"
  - id: mcp-domain-server-design
    relation: complements
    notes: "The reference triple and imports-check defined normatively here; the design record stays there"
  - id: divergence-is-an-unrouted-decision
    relation: implements
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

**The flip discipline (v3.18):** the flip itself is an auditable event, not an
honour-system bit. The floor cannot verify *truth* (whether the human review
was real — that is judgement); it verifies *procedure*, keyed to git:

1. **No born-verified things.** A thing whose most recent `verified: true`
   flip commit is its creation commit had no review window — verification and
   content arrived in one keystroke. Commit external things unverified first;
   flip in a separate commit. A historical offence heals the same way:
   re-quarantine, then re-verify properly.
2. **Every flip names its human.** `verified: true` requires `verified_by` —
   ALCOA "attributable", mechanised. Deliberately forgeable: a false
   attribution is a falsifiable record a named human can deny, which is a
   categorically better failure mode than an anonymous bit.
3. **Every flip is surfaced.** `mdllm session-start` lists the flips since the
   last session-end commit where the operator already looks; a wrong or rogue
   flip cannot hide.

Checks 1–2 run in `validate` (and therefore in the pre-commit hook) at
Warning severity by default; a domain that needs the flip to be *blocking*
declares `options: {quarantine: strict}` in its `_schema.yaml`, which raises
them to Error. A regulated domain opts in; a casual domain never meets the
ceremony.

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

### The Calculation Half, Made Mechanical

Since v3.25.0 the "no calculation" clause is arithmetic rather than prose.
Declared derivations (`computed:`, thing.md) are evaluated by `mdllm calc`, and
the rule binds in two different ways depending on where the inputs come from:

- **Within the thing itself** — computing the totals of an unverified statement
  is *allowed*, because that is precisely how a human comes to verify it.
  Forbidding it would forbid the reconciliation the quarantine exists to
  require. Every line of the report is stamped `UNVERIFIED` instead, so a
  provisional figure cannot be lifted out of its context unseen.
- **Across the corpus** — a `things(...)` selection **excludes** quarantined
  things from the aggregate **and names each one**, citing this rule. Silent
  exclusion would be the worse failure: a total that dropped its evidence
  without saying so reads exactly like a total that had none to drop. A
  `verified: true` external thing is included, which is what the flip is for.

The same instinct governs two neighbouring exclusions: a thing is excluded from
its own selection (a derivation must not draw on the figure it derives), and a
selected thing lacking the field refuses with the ids rather than quietly
returning a smaller denominator.

## Cross-Domain Imports — The Reference Triple

A special case of `origin: external`: content imported from **another domain's
exposed face** (served by `mdllm mcp-serve`; design record:
`docs/plans/mcp-domain-server.md`). Such an import carries the **reference
triple** in its frontmatter — the pin that makes the import sync-checkable:

- `source_domain` — the producing domain, as named in the consumer's
  `.mcp.json` address book (operator-wired, per trust zone)
- `source_id` — the thing's id in the *producer's* id-space
- `source_commit` — the producer-computed commit that last touched the exposed
  thing at import time (per-thing, so unrelated source commits never fire it)

Unlike an `informed_by` pin, which is domain-local ("the pinned commit exists
in the domain repo"), the triple points *across the membrane* — so it is never
resolved against local git. `mdllm imports-check` is the standing check: it
re-reads the source's face **through MCP, never the source's git** (a freshness
read is a horizontal cross-domain read and obeys the same membrane as content),
and reports each import as one of:

| State | Meaning |
|---|---|
| `fresh` | Pin matches the source's current per-thing commit, content matches the face |
| `stale` | The source moved under the pin — mirror behind source |
| `diverged` | Pin is current but the mirror's content no longer matches the face — source behind mirror: the loop was bypassed (mirror edited locally, or source changed without committing) |
| `withdrawn` | The source no longer exposes the thing |
| `unreachable` / `no-address-book-entry` / `incomplete` | The comparison could not be made — counted as unchecked coverage, **never as fresh** |

**Re-quarantine-on-drift:** `stale` or `diverged` is the mechanical signal that
the established hand-off is no longer honest. The disposition — re-read the
source, flip `verified: false`, `status: stale`, and route the change through
the consumer's dependents — is the agent's and the human's, entered as an
**external inflection** under `change-reconciliation.md`. The floor detects;
it never flips a domain's things itself.

Framework version drift stays on the *vertical* axis (git, the sentinel);
peer freshness is *horizontal* and crosses only through the face. Two-axis
rule: vertical → git, horizontal → face. `mdllm estate-check [roots...]`
batches the same per-consumer read — over explicitly named roots, or (no
arguments) over the local clones the `estate-sync` walk discovers, a
filesystem fact, not an estate manifest — ephemeral, grouped per consumer,
never a global index.

### The Membrane's Direction Is a Ruling, Not a Backlog

Everything above is consumer-side, and that asymmetry is **by design and by
operator ruling (2026-07-28)**: *a producer never learns who consumes it,
keeps no consumer registry, and pushes nothing; the consumer polls.* Producer
blindness is the atomicity guarantee — a domain's existence and its audience
are facts held nowhere but where they already live. Consequences, so this is
never re-litigated:

- **Publication means committing honestly to your face. Delivery is the
  consumer's poll.** "Changing an exposed thing is a publication event"
  requires no subscriber list — the event is the commit; `imports-check` is
  the delivery mechanism.
- **No outbound address book** (`who_i_know` stays empty, permanently). Even
  consumer-declared variants smuggle discovery back in, because the producer
  must then learn which porches to ask.
- **Withdrawal etiquette, not withdrawal machinery.** A producer cannot
  pre-flight an un-expose against consumers it cannot know. The courteous
  breaking change is **deprecate on the face first**: flip the thing's status
  to a deprecated/superseded value *while still exposed* — the pin moves,
  every consumer's next `imports-check` reports `stale`, and the re-read
  shows the deprecation — then withdraw later. Withdrawal without a
  deprecation period is legal but discourteous; the consumer's `withdrawn`
  state is the after-the-fact safety net either way.
- **No shared cross-domain work identity.** One domain owns a work item;
  every other domain that tracks it imports it through the face with the
  triple. Completion then surfaces at each consumer as `stale` at its next
  check — cross-domain cascade without a reverse map. Two things in two
  domains linked only by prose is the anti-pattern this replaces.

### Ingestion Is Not Import — The Ingestion Triple

`origin: external` covers two species that must not share a shape:

- **Import** (domain → domain): the source is another domain's face; the
  reference triple pins it; `imports-check` can re-poll it forever.
- **Ingestion** (world → domain): the source is an external system — a
  drive export, an email, a register spreadsheet — with **no face to poll**.
  The comparison `imports-check` makes for imports is *permanently
  impossible* here, and reporting these as could-not-be-checked misfiles a
  design fact as a coverage failure.

An ingested thing carries the **ingestion triple** instead:

- `source_system` — the external system, named plainly (`google-drive`,
  `companies-house`, `email`)
- `source_ref` — the pointer into it (a file path, URL, message id)
- `source_checked` — ISO date the mirror was last compared against the
  source **by a human or a harness with access** — the staleness clock
- `source_hash` *(optional)* — a hash of the ingested text at last check,
  so the next check can diff instead of re-read

`imports-check` reports these as `ingested` with the clock ("checked
2026-07-21" / "no source_checked date") — a species with its own freshness
discipline, not an unchecked import. The quarantine rule is unchanged:
ingested things are born `verified: false` and flip only by attributed human
commit. Re-checking is the operator's cadence to set; the floor's job is to
make the clock's age visible, never to shrug.

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
| Born verified | The most recent `verified: true` flip commit is the thing's creation commit — no review window (`validate`, hook-enforced) | Warning (Error under `quarantine: strict`) |
| Unattributed flip | `verified: true` without `verified_by` naming the human verifier (`validate`, hook-enforced) | Warning (Error under `quarantine: strict`) |
| Flip visibility | `verified: true` flips since the last session-end commit are listed by `session-start` | surfaced, not scored |

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
- **change-reconciliation.md** — a `stale` or `diverged` cross-domain import is
  the mechanical signal for an **external inflection**; the routing of that cue
  through the consumer's dependents is that spec's four beats.
- **interface.md** — deliverables are projections of understanding; this spec
  makes the projection citable.
- **`divergence-is-an-unrouted-decision`** — this spec is the **recorded-why
  face** of that primitive: pinning makes a route-2 revision traceable, and the
  `origin: external` / `verified: false` quarantine refuses to let an unrouted
  external divergence silently inform an output — the no-silent-default law applied
  to ingested reality.
