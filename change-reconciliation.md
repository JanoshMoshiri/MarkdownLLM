---
id: change-reconciliation-specification
type: specification
status: draft
version: 1.0
created: 2026-06-13
linked_things:
  - id: thing-specification
    relation: extends
  - id: belief-revision-specification
    relation: complements
  - id: provenance-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
  - id: validate-thing-specification
    relation: complements
  - id: retrospective-specification
    relation: complements
  - id: consistency-is-maintained-at-change-not-by-sweeping
    relation: implements
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: implements
  - id: structural-pointers-need-reverse-edge-indexing
    relation: implements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Change Reconciliation

## What This Specifies

How a domain stays internally consistent **across change**. Structural validity
is enforced at write time by the deterministic floor; this spec governs the
other half — the semantic consistency that no schema can check, because a
contradiction lives *between* two individually-valid things and is *created*,
never prevented, by a change to one of them.

The premise is deliberately narrow: **a fresh thing on a clean slate carries no
consistency risk** — there is nothing for it to contradict. Risk enters only at
*change* to something the domain already reasons from. So consistency is
maintained at the moment of change, by reconciling that change against
everything it touches. This is change management, applied to knowledge.

After this spec, any meaningful change can answer: **"what did I just put at
risk, and is each of those things still true given what I changed?"**

## The Driver Names The Inflection

The cue is **human, not mechanical.** The framework is supplementary structure
for an expert who holds the domain knowledge; recognising that a change is no
longer a refinement but an *inflection* — a change to the logical path itself,
not merely to how an existing path is expressed — is precisely the judgement
the framework exists to support, not to replace.

> **The reconciliation pass is entered when the driver declares an inflection.
> The agent does not initiate it from edit-detection. Everything mechanical runs
> only after the human "go."**

An agent may *offer* to reconcile when it notices it has changed a thing with
many dependents — but the decision that a change is consequential enough to
reconcile belongs to the person defining the domain. Automating the trigger
would substitute the agent's pattern-following for the expert's knowing, which
inverts the framework's purpose.

## The Four Beats

Once entered, the pass is the same four beats at every scale — one touched
thing or a thousand. The assimilation is **holistic**; the reconciliation is
**serial**. You gather the whole affected set *first*, precisely so the
step-through is stable: if you walked and discovered at once, reconciling one
touch point could be undone by the next, which is the thrash this spec exists to
prevent.

1. **Cue** — the driver declares an inflection: *this change is consequential.*
   This is the only non-mechanical beat, and the only one that initiates.

2. **Assimilate** — gather the *complete* affected set, mechanically, in two
   passes of widening visibility:
   - **Declared edges** — the `relationships` derived index supplies every inbound
     `linked_things` edge *and* every inbound structural pointer (`definition`,
     `parent`) — the singular load-bearing fields that name exactly one target
     without being a `linked_things` relation, so a definition's runs and a parent's
     children are recalled, not just `linked_things` dependents; the `provenance`
     (reverse) index supplies every decision pinned to the changed thing and every
     output derived from it. Total recall over what is *declared*, like a compiler
     listing every call site.
   - **Textual references** — then grep the corpus for the changed thing's `id` and
     its canonical name(s). This lights the dependencies expressed in *prose* that
     carry no declared edge — routing tables, cross-references, restatements: the
     part of the dark region a literal-name search can reach. Like *find in files*
     after *find all references*.

   Both decide nothing; together they reveal the shape. What stays unlit after
   both is the conceptual residue — only the Walk sees that (see Walking the Dark
   Region).

3. **Walk** — step through each touch point in turn, asking one question of each:
   *does this still hold, given what changed?* Three outcomes per point —
   **consistent** (leave it), **revise** (update it in place), or **contradiction**
   (surface it; if the change was a rule change, record the superseding decision
   per `belief-revision.md`). This beat is semantic and is the agent's
   `validate.thing.md` Layer 2 work — never re-perform the mechanical
   assimilation by reasoning.

4. **Seal** — record the resolutions. A change to a rule that governs reasoning
   is written as a `type: decision` that `supersedes` the prior rule, which makes
   "what was produced under the old rule" a computable set rather than a manual
   hunt. Revisions land as commits at meaning boundaries; anything unresolved is
   surfaced, not silently dropped. The edges this pass touched are now explicit —
   so the next change inherits a more connected corpus and assimilates wider. The
   pass builds the connectivity it depends on.

## Fractal By Construction

The four beats are scale-free. A one-line correction to a leaf fact runs the
whole pass in a beat — cue, assimilate finds nothing pointing in, done. A
workflow restructure runs the identical pass with a wall of touch points. There
is no separate "big sweep" procedure and no "small edit" procedure; there is one
pass, sized by the blast radius the change actually has. That self-similarity is
the signal that this is a primitive, not a checklist.

## Walking the Dark Region

The dark region is the set of dependencies a change touches through **prose**
rather than through a declared edge. It is not monolithic — it is tiered by how
reachable each dependency is, and each tier has its own mechanical reach:

- **Declared edges** — `linked_things` relations, the singular structural pointers
  (`definition`, `parent`), and `informed_by`/`derived-from` pins. The
  `relationships` and `provenance` indexes walk these in full — a declared edge is
  walked wherever it lives, whether in `linked_things` or in its own structural field.
- **Literal references** — the thing's `id` or canonical name appearing as text in
  another thing's body: routing tables, cross-references, restatements. A corpus
  grep reaches these (the textual-trace step of Assimilate).
- **Conceptual references** — a thing that reasons about the changed rule *without
  naming it*. No mechanical pass reaches this; only the Walk does.

The indexes plus grep narrow the dark region to that last tier — but never empty
it. This is not a defect to automate away; it is the structural reason the **Walk
is human-backed**. The mechanical assimilate guarantees the *declared* and
*literally-named* sets are complete; the expert is the irreducible backstop for
the conceptual residue the machine cannot read. So when a change is significant,
still ask explicitly: *what reasons about this without naming it?* And shrink the
region over time by promoting prose mentions into declared edges — the same reason
the framework says to link rather than mention. Captured as the insight
`mechanical-assimilation-is-blind-to-prose-dependencies`.

## Retrospective Reconciliation

The four beats assume the pass runs *at* the change. A domain that was already
changed without it — twisted, with contradictions latent in the corpus, whether
a legacy domain not yet under the discipline or a live one where an inflection
went undeclared — needs the same pass in a different mode: **full-corpus,
reconstructed from history**, not delta-scoped from a clean inflection. This is
the `retrospective.md` net catching what the change-time net never saw; the beats
still hold, but their inputs change.

1. **Freeze a baseline.** You cannot reconcile a moving target. Stop the change
   and commit the current state to a known point — *even if it is internally
   inconsistent* — before any sweep. Half-applied changes underneath make every
   check untrustworthy and specifically poison the git-pinned tools. Reconcile
   from a stable baseline to a stable baseline.

2. **Assimilate from history and connectivity, not from a delta.** With no single
   inflection to walk from, reconstruct the affected set two ways: `git log` /
   `git diff` over the range of the twist — and `mdllm provenance`'s Freshness
   check, which walks commits since each pin — supply *what changed*; the
   `relationships` and `provenance` indexes supply *what is load-bearing now* (the
   high-fan-in nodes worth checking regardless). Then the textual trace as in any
   pass: grep for the touched things' ids and names.

3. **Walk the whole field, expecting a larger human share.** Retrospectively you
   are partly reconstructing intent you never recorded, so more touch points
   resolve by judgement than by mechanism. The reconstruction is only as good as
   the git history: well-committed twists are largely recoverable; loose or
   uncommitted ones fall back to a full-corpus consistency scan plus the expert's
   knowledge of the domain.

4. **Seal to a new clean baseline.** Record contradictions through
   `belief-revision.md`; commit the reconciled state as the point future passes
   measure from.

Retrospective reconciliation is not a substitute for the change-time discipline
— it is its **backward-looking mode**, and it runs in two situations. The first
is **one-time realignment**: a domain that accumulated change before the
discipline was adopted is twisted once, swept once, and reconciled at each change
thereafter. The second is **recurring maintenance**: because the Cue is human
(see *The Driver Names The Inflection*), an expert will sometimes edit without
declaring the inflection, and those changes land un-reconciled. The change-time
net cannot catch what was never handed to it, so the same backward pass runs
periodically — bound to the `retrospective` hook (`retrospective.md` →
Reflexive Scans At Retrospective) — as the net beneath the net.

The two uses differ only in scope and cadence, not in kind: both freeze a
baseline, reconstruct the delta from history, walk the affected set, and seal.
The forward pass remains primary — the retrospective is the cost of reconciliation
*skipped*, not a licence to skip it; it is what makes the discipline robust to
the times the cue is missed, not a substitute for giving it.

## Enforcement

The split follows the framework's standard division of labour:

| Concern | Owner | Mechanism |
|---|---|---|
| The declared affected set is complete | Deterministic floor | `relationships` (incl. structural `definition`/`parent` pointers) + `provenance` indexes (`derived-index.md`, `provenance.md`) |
| Prose references the indexes miss | Deterministic floor (textual) | corpus grep for the thing's `id` and canonical name |
| Pinned dependents that are now behind | Deterministic floor | `mdllm provenance` Freshness check (Info) |
| A rule change leaves a supersede mark | Floor (shape) + agent (judgement) | `belief-revision.md` supersede protocol |
| Does each touch point still hold? | **Agent (semantic)** | `validate.thing.md` Layer 2 — the Walk |
| Is this change an inflection at all? | **The human driver** | judgement; not mechanisable |

The floor can guarantee the affected set is *complete* and *current*. It cannot
decide whether a dependent still holds, and it must not decide whether a change
is consequential — those are the semantic and the human layers respectively.
The floor's job here is to make the agent **unable to not see** the shape of
what a change disturbs; the judgement of what to do about it stays where it
belongs.

A domain may expose the Assimilate beat as a single affordance over the two
existing indexes (a "touch points of X" read) without new infrastructure; this
spec does not mandate a new `mdllm` subcommand, only the discipline of running
the pass.

## Relationship To Other Specs

- **thing.md** — the unit being reconciled; `linked_things` edges are the
  assimilation substrate.
- **validate.thing.md** — the Walk is its Layer 2 (semantic) validation, now
  given an explicit trigger and scope (the affected set) rather than an open
  "review everything."
- **provenance.md** — the reverse-provenance index and the Freshness check are
  the Assimilate beat's mechanical inputs; a rule-change-as-decision is what
  makes downstream staleness computable.
- **derived-index.md** — the `relationships` index is the other Assimilate input;
  reconciliation is one of the reflexive behaviours indexes exist to make cheap.
- **belief-revision.md** — the Seal beat records rule changes through the
  `supersedes`/`superseded-by` protocol.
- **git-workflow.md** — changes are reconciled and sealed at commit boundaries;
  the supersede mark and the revisions ride the same commit as the change.
