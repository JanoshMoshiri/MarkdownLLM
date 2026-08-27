---
id: estate-mechanics-guide
type: guide
status: evolving
version: 1.5
created: 2026-08-04
linked_things:
  - id: git-workflow-specification
    relation: documents
    notes: "The publication radius: autopush, estate-sync, divergence surfaced never resolved — this guide is their operator-facing picture."
  - id: change-reconciliation-specification
    relation: documents
    notes: "The reconciliation radius: the four beats and the blast radius of a change, diagrammed at the three levels an operator works at."
  - id: retrospective-specification
    relation: documents
    notes: "The cadence radius: the 60-day domain clock and the 30-day estate clock this guide states side by side."
  - id: autopush-requires-explicit-authority
    relation: documents
    notes: "Publication transport is standing automation only under literal git.autopush true; absence never authorizes a send."
  - id: explorer-publication-position
    relation: derived-from
    notes: "v1.5 clarifies that Explorer observes estate state but does not perform any operation in these three radii."
---

# Estate Mechanics — publication, reconciliation and cadence at three radii

How state flows and stays coherent after v3.26.0, told at the three levels
an operator actually works at: inside one domain, between domains, and at
the substrate. The diagrams carry most of the words. One sentence governs
everything below, at every level: **the floor asks questions, gathers
facts, and transports state; the human answers questions, routes
divergences, and decides.** Nothing anywhere auto-edits, auto-merges, or
auto-judges.

The optional [MarkdownLLM Explorer](../explorer/README.md) can display this
estate and its commits, but it sits outside every operational arrow below. It
does not run `estate-sync`, `imports-check`, reconciliation or publication;
its freshness is exactly the freshness of the repositories it reads.

The architect can see these internals from memory. Nobody else can without
reading the specs whole — this page is the shortcut. (Normative sources:
`git-workflow.md`, `change-reconciliation.md`, `retrospective.md`,
`orchestration.md`; decision `autopush-requires-explicit-authority`.)

---

## 1 · Inside a single domain — the life of one commit

Every Git candidate has a truthful change class: addition, modification,
deletion, or rename. A new thing has no inbound dependents yet, but can still
duplicate or contradict an existing claim; a deletion can withdraw a
load-bearing truth. When a candidate is committed, the floor validates the
exact staged tree, asks change-class-specific questions, then the commit-msg
boundary checks disclosure. After the commit lands, publication happens only
under explicit standing authority.

```mermaid
flowchart TD
    accTitle: The life of one commit inside a single domain
    accDescr {
        A left-to-right sequence with two rails. Writing or modifying a thing
        enters the pre-commit floor, which blocks on validation for structure,
        schema and references, then coherence for generated artifacts, all over
        the frozen index candidate. Next come two
        advisories that never block: the cue question asking whether the change
        matches the A/M/D/R change class, and the porch notice that an exposed
        thing would publish. The commit-message disclosure gate then blocks on
        boundary terms. The commit lands; post-commit autopush transports it only
        under literal true policy, with published, disabled, debt or REJECTED
        outcomes. Branching off the mechanical rail, the cue
        advisory feeds a human verdict: no proceeds, yes declares an inflection
        which runs the four beats Cue, Assimilate, Walk, Seal. A REJECTED push
        is divergence on the push side, routed by the operator and never forced.
    }
    W["Add · modify · delete · rename"]
    subgraph FLOOR["Pre-commit — the floor (blocks)"]
        V["validate --view index<br/>structure · schema · refs"] --> C["coherence --view index<br/>generated artifacts fresh"]
    end
    subgraph ADV["Advisories — never blocking"]
        Q["cue: A / M / D / R question"]
        P["porch: exposure publication notice"]
    end
    B["commit-msg — disclosure boundary (blocks)"]
    K["Commit — real on this machine"]
    subgraph AP["Post-commit — fail-closed autopush"]
        O["published · disabled · debt · REJECTED"]
    end
    R["Remote — real to the estate"]
    W --> FLOOR --> ADV --> B --> K --> AP
    AP -->|"only when authorized and accepted"| R
    Q -.-> H["Human verdict:<br/>no → proceed · yes → inflection"]
    H -.-> FB["The four beats:<br/>Cue → Assimilate → Walk → Seal"]
    O -.-> RT["REJECTED = divergence on the push side —<br/>the operator routes it, never forced"]
```

The mental model: the left rail is mechanical, the right rail is human.
`candidates` makes the cue *question* unavoidable for all four candidate
classes while the
cue *verdict* stays the driver's. Saying no to a named question is a
decision; not being asked was drift. Autopush is transport of
floor-validated state — bounded, never forcing, and enabled only by literal
`git: autopush: true`. False, absence, or malformed policy is disabled.

---

## 2 · Domain to domain — the membrane

The consumer side always had the machinery (estate-sync, imports-check,
quarantine). v3.26.0 gave the producer side a voice and closed the
transport gap: a producer's face is now current the moment it commits, so
drift detection is honest once the producer commit is published; explicit
autopush makes that immediate, while disabled/offline/rejected publication is
named as debt rather than silently treated as current.

```mermaid
flowchart LR
    accTitle: The membrane between a producer domain and a consumer domain
    accDescr {
        Left to right, three zones. In the producer domain, an authoring-time
        human call sets exposed to true, which raises a serve advisory saying
        this change publishes, then the commit is floor-validated and, when
        explicitly authorized, autopushed.
        That reaches the middle zone, the remote face. In the consumer domain,
        estate-sync fetches fast-forward-only at session start, imports-check
        compares against pins and reports stale or DIVERGED, imports land in
        quarantine marked origin external and verified false, and only a named
        human flips verified in its own commit. Transport is accelerated but
        trust is not: the producer never learns who pulls.
    }
    subgraph PROD["Producer domain"]
        E["expose: true<br/><i>authoring-time human call</i>"] --> SA["serve advisory<br/><i>'this change publishes'</i>"]
        SA --> PC["commit — floor validates"] --> PA["autopush<br/><i>only under literal true</i>"]
    end
    F[("the remote<br/>face")]
    subgraph CONS["Consumer domain"]
        S["estate-sync at session start<br/><i>fetch + ff-only</i>"] --> IC["imports-check<br/><i>stale / DIVERGED vs pins</i>"]
        IC --> QU["quarantine<br/><i>origin: external · verified: false</i>"] --> VF["verified flip — human,<br/>named, own commit"]
    end
    PA --> F --> S
```

The invariant that did **not** move: **autopush accelerates transport,
never trust.** Imports still land quarantined; only a named human flips
`verified`, in its own commit. And the producer never learns who pulls —
publication is a commit to the face, not a dispatch.

---

## 3 · The substrate — the framework itself

The framework root states the safe policy explicitly: a
push there is a *release* — outsider-consumed, judgement-gated, with no
mechanical completeness check — so the root declares `autopush: false` and
its push stays the deliberate act. What a release owes first is a walk,
because a release is an inflection *by construction*: it changes the
definition surfaces every domain reasons from.

```mermaid
flowchart TD
    accTitle: How a change to the framework root becomes a release
    accDescr {
        Top to bottom. The framework root is a release surface declaring git
        autopush false, so a spec or tool change there is an inflection by
        construction. It runs three beats in sequence. First Assimilate, using
        touchpoints plus an estate-wide grep. Then Walk, where generated
        surfaces reconcile by regeneration - every managed domain kernel from one
        string - and authored surfaces are judged one by one. Then Seal, which
        writes a decision thing and records the walked set in the CHANGELOG. Only then
        does a human publish, because the walk earns the push. Publication
        flows into distribution - refresh, seal, domain-kernel regen and hooks -
        which reaches the domains, whose kernel blocks regenerate from one
        source. Each domain then carries two cadence clocks: a 60-day domain
        clock checked at session start and by the estate sweep, and a 30-day
        estate clock held as a dated trigger in the vantage domain.
    }
    RT["Framework root — release surface<br/><i>git: autopush: false</i>"]
    CH["A spec or tool change —<br/>an inflection by construction"]
    A["Assimilate<br/><i>touchpoints + estate-wide grep</i>"] --> WK["Walk<br/><i>generated → one regen source<br/>authored → judged</i>"]
    WK --> SE["Seal<br/><i>decision thing · CHANGELOG<br/>records the walked set</i>"] --> PB["Publish — human<br/><i>the walk earns the push</i>"]
    RT --> CH --> A
    PB --> D["Distribution — refresh · seal ·<br/>domain-kernel regen · hooks"]
    D --> DOMS["the domains<br/><i>kernel blocks regenerate from one source</i>"]
    DOMS --> CK1["Domain clock — 60 days<br/><i>session start + estate sweep</i>"]
    DOMS --> CK2["Estate clock — 30 days<br/><i>dated trigger in the vantage domain</i>"]
```

The Walk's cost model is the load-bearing idea
(`a-generated-surface-collapses-its-walk`): a truth stated once and
*derived* everywhere reconciles by regeneration — one generator string
reconciles every managed domain kernel — while a truth
*restated by hand* costs a judged walk step per restatement, forever.
Restatement count **is** reconciliation cost; promote a restatement into
derivation when a walk revisits it twice.

### The root pointer's second position

One more substrate↔domain interaction, observed live on 2026-08-17: Claude
Code loads `CLAUDE.md` files from every directory *above* the workspace,
root-down, so a session opened in a nested domain inherits the framework
root's entry pointer alongside its own. The two then behave differently by
documented harness rule: the domain pointer's `@AGENTS.md` resolves inside
the workspace and expands, while the inherited root pointer's resolves
*outside* it and is gated as an external import — delivered as literal
text, its target unloaded. That outcome is the right one (a domain session
must not inherit the framework's own entry file), but until 2026-08-17 it
held only by the gate staying unapproved. The wrapper now routes both of
its positions explicitly, and a drift test holds the wording identical
across the tracked root file and both installers. Domain pointers need no
equivalent — nothing nests beneath a domain.

---

## 4 · The interconnection — one primitive at four radii

There are not three systems to hold in your head. There is one split,
repeated at every radius — and the radii nest as safety nets: what one
misses falls to the net beneath.

| Radius | The floor — asks · gathers · transports | The human — decides · routes |
|---|---|---|
| **Commit** | `candidates` asks the cue · `autopush` transports | cue verdict · route rejected pushes |
| **Membrane** | `estate-sync` freshens · `imports-check` detects drift | exposure call · verified flip |
| **Epoch** | cadence clocks (60d domain / 30d estate) · dated triggers | retrospectives · estate rulings, routed home via porch |
| **Release** | release-walk Assimilate, estate-wide | walk judgement · the deliberate push |

```mermaid
flowchart TD
    accTitle: The four radii nesting as safety nets
    accDescr {
        A single chain of four stages, each catching what the one before it
        missed. An unwalked change at the commit radius surfaces as drift at
        the membrane radius, reported as stale or DIVERGED. What drift cannot
        see falls to the epoch radius and its retrospective clocks. Epochs in
        turn feed the release radius, where the walk resets the substrate. One
        split repeated at every radius: detection mechanical, judgement human.
    }
    C1["Commit radius —<br/>an unwalked change"] -->|"surfaces as drift"| M1["Membrane radius —<br/>stale / DIVERGED"]
    M1 -->|"what drift can't see"| E1["Epoch radius —<br/>the retrospective clocks"]
    E1 -->|"epochs feed"| R1["Release radius —<br/>the walk resets the substrate"]
```

Detection mechanical, judgement human, verdicts never scored — the
boundary every v3.24–v3.26 change preserved, which is the strongest
evidence it is drawn where reality wants it.
