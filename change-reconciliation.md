---
id: change-reconciliation-specification
type: specification
status: draft
version: 1.1
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
  - id: divergence-is-an-unrouted-decision
    relation: implements
  - id: cross-domain-handoff-is-built-inbound-only
    relation: implements
    notes: "The re-opened quarantine it names as the cue is this spec's inbound external-inflection edge"
  - id: mcp-domain-server-design
    relation: complements
    notes: "Its drift path terminates here: stale/diverged imports hand the human an external inflection"
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

The premise is deliberately narrow: consistency risk enters whenever the
accepted corpus changes — **addition, modification, deletion, or rename**. A
fresh leaf may have no inbound dependents yet, but it can still duplicate or
contradict an existing claim, seize an existing identity, or expose a new
publication surface. A deletion can withdraw a load-bearing truth; a rename can
break path identity without changing content. Consistency is therefore
maintained at the moment of corpus change, by reconciling the candidate against
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

### External Inflections — The Inbound Edge

An inflection does not have to originate inside the domain. When a
cross-domain import drifts — `mdllm imports-check` reports it `stale` (the
source moved under the pin) or `diverged` (the mirror no longer matches the
face) — the domain's reasoning may now rest on ground that shifted *outside*
it. That report is the mechanical signal; re-opening the quarantine
(`verified: false`, `status: stale` — `provenance.md` → Cross-Domain Imports)
and entering this pass on the import's dependents is an **external
inflection**.

The cue discipline is unchanged: `imports-check` is report-only, and the
declaration that the drift is consequential enough to reconcile stays the
driver's — exactly as above. The floor makes the drift impossible to not see;
it never dispositions. What the external origin changes is only the *entry
point*: the changed thing walked from is the import itself, and the affected
set is its dependents inside this corpus.

**Scope boundary, stated rather than implied:** the four beats run within a
single corpus. The Assimilate indexes, the textual grep, and the Walk never
cross the membrane — the outside world enters this spec only as a cue, already
quarantined as an `origin: external` thing. Reconciling the *producer's*
corpus is the producer's own pass, in its own repo, if its driver declares
one.

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
     field owned by the tool's structural-reference registry: relation objects,
     list pointers, singular pointers, trigger watches, workflow definitions,
     conflict parties, and other registered reference shapes. The same registry
     drives validation, reverse indexing, candidate relevance, and private egress,
     so adding a structural field cannot silently update only one consumer. The `provenance`
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

- **Declared edges** — every field in the structural-reference registry,
  including `linked_things`, prerequisites, singular pointers, trigger watches,
  conflict parties, workflow definitions, and `informed_by` pins. The
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

**Scope: an inflection walks the whole corpus — every file, the insight corpus
included.** The dark-region tiers above say *how reachable* a dependency is; they
do not narrow *where* to look. The Walk is full-corpus by definition, and the
trap is to reconcile only the surface a change visibly touched (the specs it
edited) while the things it *didn't* touch carry stale references to it. After a
significant inflection — a mechanism dissolved, an artefact retired, a rule
inverted — the part most likely to drift is `things/insights/`: active insights
written *before* the inflection still describe the old model as live, and nothing
in the change's own diff points at them. Do not lean on a mechanical guard to
remember this for you; resist the urge to spec a "retired-term check" or similar.
A check that needs a hand-maintained suppression list to stay quiet is judgement
in mechanical clothing — it adds a silent-failure surface (an over-broad
suppression hides real drift) and a false sense that the Walk is covered. The
floor is for checks that cannot disagree with truth (same-builder drift); the
retire/rename case is irreducibly semantic, so it stays the human Walk's, over
**all** files — see the retrospective's reflexive scan for the periodic net.

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
| The declared affected set is complete | Deterministic floor | `mdllm touchpoints <id>` (live), over the same edges the `relationships` + `provenance` indexes hold (`derived-index.md`, `provenance.md`) |
| Prose references the indexes miss | Deterministic floor (textual) | `mdllm touchpoints` literal tier + corpus grep for the thing's canonical name |
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

The Assimilate beat is exposed as a floor affordance: `mdllm touchpoints <id>`
reports the complete declared inbound set (every reference shape owned by the
canonical structural registry, including provenance pins)
plus the literal textual references, computed fresh from the live corpus — not
from the committed indexes, because assimilation must be complete *and* current.
The subcommand is deliberately **invoked, never hooked**: it makes the blast
radius impossible to not see, but the *Cue* — deciding a change is consequential
enough to run the pass — stays the driver's (see *The Driver Names The
Inflection*). The spec mandates the discipline of running the pass at an
inflection, not the existence of the tool; the tool is the affordance that makes
the discipline cheap.

The floor also asks the **cue question** without answering it
(`inflection-candidates-are-computable`): the pre-commit hook's index-view
`mdllm candidates` advisory reads Git's full A/M/D/R candidate set. A modified
thing that is reasoned-from asks whether its dependents still hold. An addition
asks whether its identity or claim duplicates/contradicts the corpus and whether
new exposure is intended. A deletion asks which dependents lose their target
and whether an exposed truth is being withdrawn. A rename asks whether identity
and path-sensitive references remain honest. The cue *verdict* remains the
driver's, and `touchpoints` remains invoked-never-hooked; what the floor
guarantees is that the truthful question existed at the exact candidate
boundary. Saying no to a named question is a decision, where not being asked was
drift.

## Relationship To Other Specs

- **thing.md** — the unit being reconciled; `linked_things` edges are the
  assimilation substrate.
- **validate.thing.md** — the Walk is its Layer 2 (semantic) validation, now
  given an explicit trigger and scope (the affected set) rather than an open
  "review everything."
- **provenance.md** — the reverse-provenance index and the Freshness check are
  the Assimilate beat's mechanical inputs; a rule-change-as-decision is what
  makes downstream staleness computable. Its Cross-Domain Imports section is
  the inbound edge: a `stale` or `diverged` import re-opens the quarantine and
  enters this pass as an external inflection (see *External Inflections*).
- **derived-index.md** — the `relationships` index is the other Assimilate input;
  reconciliation is one of the reflexive behaviours indexes exist to make cheap.
- **belief-revision.md** — the Seal beat records rule changes through the
  `supersedes`/`superseded-by` protocol.
- **git-workflow.md** — changes are reconciled and sealed at commit boundaries;
  the supersede mark and the revisions ride the same commit as the change.
- **`divergence-is-an-unrouted-decision`** — this spec is the **forward-cascade
  face** of that primitive: once the driver routes a divergence (the inflection),
  the four beats cascade its consequences. The Walk's three outcomes —
  consistent / revise / contradiction — are routing made operational.
