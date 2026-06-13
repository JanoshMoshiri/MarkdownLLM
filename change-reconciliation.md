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
  - id: consistency-is-maintained-at-change-not-by-sweeping
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
*change* to something the domain already reasons from. So consistency is not
maintained by periodic sweeps that hunt for drift after it accumulates; it is
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

2. **Assimilate** — gather the *complete* affected set in one pass, mechanically.
   The substrate already exists: the `relationships` derived index supplies every
   inbound `linked_things` edge; the `provenance` (reverse) index supplies every
   decision pinned to the changed thing and every output derived from those
   decisions. This is total recall, like a compiler listing every call site — it
   decides nothing, it only reveals the shape.

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

## Enforcement

The split follows the framework's standard division of labour:

| Concern | Owner | Mechanism |
|---|---|---|
| The affected set is complete | Deterministic floor | `relationships` + `provenance` indexes (`derived-index.md`, `provenance.md`) |
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
