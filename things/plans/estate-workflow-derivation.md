---
id: estate-workflow-derivation
type: plan
status: in-progress
version: 1.1
created: 2026-08-27
priority: high
tags: [derivation, universal-workflow, workflow-definitions, estate, closed-loop-gate]
informed_by:
  - id: derivation-shape-brief-2026-08
    commit: 016150e76f1ae69aefd41331f9da1aa7fed471e6
  - id: workflow-reconciliation-precedes-new-definitions
    commit: f52b93013b1d40bd120741b8c4c0d866d4c00748
  - id: estate-retrospective-synthesis-2026-08
    commit: e1ad077a01d31bc85c9904a1674cf9669e64cd89
linked_things:
  - id: derivation-shape-settled-2026-08
    relation: implements
    notes: "The settled shape this programme applies estate-wide. The decision rules how; this plan rules where, in what order, and to what gate."
  - id: universal-workflow-methodology
    relation: implements
    notes: "Written through the atom's own seven decisions at programme radius — the accumulative shape, one arc. Applying the method to the work of declaring the method is the honest test of it."
  - id: closed-loop-operating-state
    relation: informs
    notes: "This programme's MVP is the operator-declared gate for that plan's Phase 2b onward: unattended sessions must not execute undeclared process."
  - id: derivation-shape-brief-2026-08
    relation: derived-from
    notes: "The worked specimen, the mapping template, and the edge-asymmetry correction this programme rests on."
  - id: operating-layer-quality-loop
    relation: informs
    notes: "Resumes behind this programme's MVP: its definition is minted following the settled shape, not ahead of it."
  - id: estate-retrospective-synthesis-2026-08
    relation: derived-from
    notes: "F4 supplies the zero-run class and its named candidates; the inventory below is the dated re-count."
triggers:
  - type: time
    condition: "2026-09-10 reached"
    action: "If the MVP is not met, report which definitions remain undispositioned and whether the closed-loop gate should hold or be re-scoped. An undated programme wait is the drift the estate learned to chase."
---

# Estate Workflow Derivation

The programme that takes every workflow definition in the estate from
*undeclared* to *declared against the atom* — written through the atom's own
seven decisions, at programme radius, because applying the method to the work
of declaring the method is the honest test of it.

**Shape: accumulative.** One arc, converging on a goal. Its `review-verify`
feeds the closed-loop programme's current-state assessment, which is the
operator's declared gate.

## 1. define-need — what are we solving, and for who?

Every workflow definition in the estate was authored before
`universal-workflow.md` entered the foundation on 2026-08-25. The atom arrived
after its instances. No domain definition declares how it relates to the base
method, so the estate cannot answer — by reading, which is the only way
composition is auditable — *does this process follow our method, and where
does it deliberately depart?*

Left alone this is untidiness. It stops being untidy because of what comes
next: the closed-loop programme is about to launch unattended sessions that
execute these definitions. **Automating the execution of undeclared process
automates whatever has drifted inside it**, at machine cadence, with no
session present to notice.

Who experiences it: the operator, who must audit composition without reading
every stage table; each domain's agent, which must know a process's relation
to the base before running it; and, for the regulated corpora, an assessor who
must see the method and its deviations without the author in the room.

**Output — problem statement.** The estate's processes are undeclared against
the method they already follow, and unattended execution is imminent.

## 2. assess-current — where are we now?

Inventory, dated 2026-08-27, read from the corpora (framework root at
`commit:016150e76f1ae69aefd41331f9da1aa7fed471e6`, domains at their local
HEADs; domains named by their established substitutions).

| Corpus | Definition | Status | Runs | Declared? |
|---|---|---|---|---|
| framework root | `substrate-floor-development` | draft | 4 | **Yes** — same-corpus `implements` edge |
| regulated-qms | `qms-template-document-authoring` | evolving | 2 (1 closed, 1 paused) | Mapped in the brief, not yet written |
| regulated-engineering | `software-development-lifecycle` | draft | 0 | No |
| regulated-overview | `weekly-estate-agenda` | evolving, `exposed` | 1 (closed 08-11) | No |
| regulated-overview | `operating-model-evolution` | draft | 1 (active) | No |
| code-architect | `refactoring-process` | evolving | has runs | No |
| code-architect | `solution-delivery-process` | evolving | 0 | No |

**Seven owned definitions across five corpora; ~15 runs; one declared.**

Two further copies are **imported mirrors, not owned definitions**, and are
out of scope: engineering holds overview's agenda (`origin: external`, full
reference triple, operator-verified 2026-08-25), and overview holds
engineering's lifecycle. A cross-mirroring pair, both properly pinned.

> **Correction, v1.1.** v1.0 counted eight owned definitions and reported
> `weekly-estate-agenda` as **duplicate ownership across two corpora**. That
> finding was false: engineering's copy carries `origin: external` with the
> source triple and an attributed verification — a correctly imported mirror
> of overview's exposed original. The membrane worked exactly as designed;
> what failed was the count, which selected on `type:` alone and never read
> `origin:`. This is the same defect the floor itself carried until v3.27.0,
> when orientation counted every non-terminal thing as an open loop because
> `origin` never entered the computation — *watched is not owned*, re-learned
> by hand one radius out. The inventory above is the corrected read; the
> duplicate-ownership work package is withdrawn.

Two findings survive, which the passes must carry rather than rediscover:

- **Directory convention drift.** `things/workflows/` in three corpora,
  `things/workflow-definitions/` in another, and one domain filing an import
  under `things/workflows/` rather than `things/imports/` — which is precisely
  what made the false finding above easy to mint. Cosmetic in itself; it is
  why a naive inventory both misses definitions and miscounts mirrors.
- **The zero-run class** (synthesis F4, re-confirmed): engineering's
  lifecycle — *mandated as the domain's primary process* — at zero runs, and
  code-architect's delivery process at zero runs. A defined process with no
  run governs nothing.

**Output — current-state assessment and case for change.** The work is small
in count and uneven in risk; the risk is concentrated in definitions with live
runs and in the mandated-but-unrun.

## 3. define-prioritise — where do we need to go, and why?

Priority follows consequence, not convenience:

1. **Definitions with live or paused runs** — a run executing against an
   undeclared process is the live exposure: QMS (one paused at human review),
   overview's operating-model-evolution (one active), code-architect's
   refactoring process.
2. **The mandated-but-unrun** — engineering's lifecycle is declared the
   domain's primary process and has never been instanced. Declaring it is
   secondary to ruling whether it is real: first run or honest retirement.
3. **Exposed definitions** — overview's agenda is `exposed: true` with a live
   consumer, so its declaration crosses the membrane on the next pin move.
   Declare it before it next changes, not after.
4. **Everything else** — declare in the domain's own next session.

**Output — prioritised outcomes.** Live-run definitions first; the mandated
zero-run definition gets a ruling, not a declaration.

## 4. set-mvp-target — the smallest acceptable destination

**Declared by the operator, 2026-08-27, as the gate for the closed-loop work.**

Every owned workflow definition in the estate carries **either** a derivation
declaration — the mapping section naming the seven decisions, collapses
stated, against a pinned framework version — **or** a recorded ruling that it
is retired or parked, with reasoning. *No definition is silent about its
relation to the base.*

Success criteria:

- 8 of 8 owned definitions dispositioned (declared, repaired-then-declared,
  or retired).
- Duplicate ownership resolved to a single owner.
- No live or paused run executing against an undeclared definition.
- The pattern exists as a worked example and reaches domains by refresh.

Deliberately **outside** the MVP: uniform stage vocabulary across domains; a
floor check that computes derivation coverage; any new definition, including
the operating-layer quality loop's. Aspiration stays separate from the
minimum.

The four longevity qualities, asked of this target state: **maintainable** —
each declaration lives in the definition it describes, one owner, no central
register to drift; **extendable** — a new definition declares at birth, so the
programme does not recur; **manageable** — each domain runs its own pass and
rules its own verdicts; **monitorable** — honestly weak, since coverage is not
computable today, which is why the MVP names a count and a date rather than
relying on a sensor.

**Why this is the gate.** The closed-loop programme's Phase 2b installs
unattended launches. Anything those sessions execute must first be declared,
or automation inherits the drift. This programme completing is the
precondition; it is not a precondition for the census ratification or the
dispatcher's authority grant, which are independent.

## 5. design-plan — how will we get there?

**WP1 — the pattern (framework root).** Run the QMS declaration as the worked
specimen; distil it into a `type: example` thing at the root and a pointer
step in `domain-refresh.md`. Additive; flows under census row 15 with the push
as review.

**WP2 — the per-domain passes.** One pass per corpus, run *inside* that corpus
by its own session, in priority order: regulated-qms → regulated-overview →
code-architect → regulated-engineering. Each pass: map, then declare, repair,
or retire; commit in the owning repo. Reconciliation never crosses the
membrane — the substrate ships the pattern, not the verdicts.

**WP3 — the structural finding.** Directory convention noted per domain, not
enforced estate-wide — including where a domain files an imported mirror
outside `things/imports/`, which is what made v1.0's false finding easy to
mint. Each domain's call; the estate does not standardise paths.

**WP4 — seal.** On the passes' evidence, decide whether anything earns a spec
change (candidate: a birth-time line in `domain-refresh.md` so new definitions
declare at creation) — and whether derivation coverage deserves a floor
sensor. Both admitted only on convergence, per the operating model's own rule.

**Dependencies.** WP1 gates WP2 (the pattern must exist before it travels).
WP4 needs all passes done. WP3 is independent.

**Capacity, resolved at the cut.** WP1–WP3 are agent-runnable inside each
corpus. One operator seat only: the retire-or-run ruling on engineering's
mandated lifecycle. *Automate it* was
considered as the third resolution — a repeatable definition for "reconcile
one definition" — and **declined**: eight instances do not earn a definition,
and manufacturing one here would be the exact over-specification the atom's
proportionate-use rule forbids. If the estate later grows definitions faster
than passes, that resolution returns.

**Output — work packages and sequence**, above.

## 6. execute — how will we deliver it under control?

Not started. Each work package lands as commits in its owning repo, with the
domain's own floor as the boundary. Evidence is the declarations themselves
plus each pass's commit.

## 7. review-verify — did we reach the target state?

Run when the MVP criteria are met: re-count the inventory, confirm every owned
definition is dispositioned, confirm no live run sits against an undeclared
definition, and record residual gaps. The outcome assessment feeds
`closed-loop-operating-state`'s current-state assessment as the gate evidence
— pinned, not asserted.

The same four longevity questions get re-asked of the delivered state, and the
honest one to watch is **monitorable**: if coverage still cannot be read
without a manual count, that is the residual gap WP4 must either fix or record.

## Route

- [x] Stages 1–4 — need, current state, priorities, MVP target. This document.
- [ ] **WP1 — the pattern.** QMS declaration written as the worked specimen;
      example thing + `domain-refresh.md` pointer.
- [ ] **WP2 — per-domain passes.** qms → overview → code-architect →
      engineering; each in its own corpus.
- [ ] **WP3 — structural finding.** Directory convention noted per domain,
      including mirrors filed outside `things/imports/`.
- [ ] **WP4 — seal.** Spec changes and sensor question, on convergence only.
- [ ] **review-verify** — MVP criteria confirmed, outcome pinned into the
      closed-loop plan.

## Done When

- [ ] All seven owned definitions carry a derivation declaration or a recorded
      retire/park ruling.
- [ ] No live or paused run executes against an undeclared definition.
- [ ] The closed-loop plan's Phase 2b can proceed against pinned evidence that
      this gate is met.
