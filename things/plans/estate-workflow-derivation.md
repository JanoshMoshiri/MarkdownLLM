---
id: estate-workflow-derivation
type: plan
status: in-progress
version: 1.2
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
    action: "The MVP was met 2026-08-28, so this fires on the residuals, not the gate. Report whether the two stale mirrors (residual 2) have been re-synced and re-flipped by the operator — nothing mechanical will detect them while imports-check coverage is 0/101 and 0/43 — and whether the three recorded process gaps have been ruled by their domains. Re-conditioned from the original MVP chase, which its own outcome answered."
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
| code-architect | `solution-delivery-process` | evolving | ~~0~~ **2 active** | No |

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

> **Correction 2, v1.2 — the zero-run premise was stale.** v1.0/v1.1 recorded
> `solution-delivery-process` at zero runs on the estate synthesis's authority
> (F4). That finding was overtaken the day after it was written: two runs pin
> the definition, both `active`. The domain pass refused to write "zero runs to
> date" because it would have been false, and wrote the true residual instead —
> *instanced but never exercised end to end*, since no run has passed `design`.
>
> **Both of this plan's inventory errors have one shape:** a dated report was
> read as current state instead of re-derived from the graph
> (`existence-is-not-currency`). The mirror-as-duplicate error read `type:`
> without `origin:`; this one read a two-day-old synthesis without re-counting
> runs. A synthesis is evidence of what was true when it was written, and an
> inventory is a graph query — the two are not interchangeable, and the cost
> of confusing them here was two false premises, one of which was handed to a
> subagent as an instruction.

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

**Complete, 2026-08-28.** Seven definitions across five corpora, each pass run
inside its owning repo by that corpus's own agent (session-start gate, the
domain's specification and write skills, then the definition), validated to
zero Errors and committed there; the four domain repos autopushed under their
standing authority.

| Corpus | Definition | Shape | Outcome |
|---|---|---|---|
| framework root | `substrate-floor-development` | repeatable | Upgraded from a hedged prose mapping to the full declaration |
| regulated-qms | `qms-template-document-authoring` | repeatable | Declared — the worked specimen |
| regulated-engineering | `software-development-lifecycle` | accumulative | Declared, with two gaps and zero runs named |
| regulated-overview | `weekly-estate-agenda` | repeatable | Declared, with one gap named |
| regulated-overview | `operating-model-evolution` | accumulative | Declared; adopts the reference graph unchanged |
| code-architect | `refactoring-process` | repeatable | Declared, no gap |
| code-architect | `solution-delivery-process` | accumulative | Declared, with one gap named |

Plus WP1 (the worked example + the `domain-refresh.md` backfill line) and one
unplanned repair: code-architect's write skill instructed the next author to
mint a cross-corpus `implements` edge to the methodology — a hard validation
Error. Nothing had broken because no definition had yet followed it; the next
one would have. Fixed in the same sweep.

## 7. review-verify — did we reach the target state?

**The MVP is met.** Seven of seven owned definitions carry a derivation
declaration; none is silent about its relation to the base. No live or paused
run now executes against an undeclared definition. The pattern exists as a
worked example and reaches domains through the refresh channel. The
duplicate-ownership criterion dissolved with correction 1 — there was no
duplicate.

**The finding that justifies the exercise: declaring surfaced process gaps in
three of seven definitions, invisible while undeclared.**

- `software-development-lifecycle` — operability and monitorability are asked
  by no stage, on the very track reserved for changes that *create*
  operational surface; and the run-to-run evidence hand-off runs through a
  shared artefact with no declared pin.
- `weekly-estate-agenda` — `review-verify` is realised by no stage. The input
  is guarded; the output is not. An agenda that silently dropped its coverage
  header would read exactly as confident as a compliant one.
- `solution-delivery-process` — `set-mvp-target` is made nowhere, at the
  radius (whole-system delivery) where leaving the target implicit costs most,
  while its own acceptance stage demands criteria that must have been set
  earlier to be met.

A fourth, weaker pattern: **progression outcomes are under-declared almost
everywhere.** Only the two mature definitions declare all four; two declare
just continuing and revising, leaving a dropped run with no declared exit.

**Residual gaps, carried not closed:**

1. The three process gaps above are *recorded*, not repaired. Each is a
   judgement for its domain — new stage, sub-gate, or accepted deviation.
2. **Two mirrors are now stale and nothing will detect it.** Both sides of a
   cross-mirrored pair changed today; `imports-check` returned **COVERAGE
   0/101** (overview) and **0/43** (engineering) — every route unreachable, so
   the floor correctly asserted nothing. Direct read confirms overview pins
   the lifecycle at `85f6a78` while it has moved to `26d102f`. The re-flip is
   the operator's attributed act, so this pass adopts nothing. This is estate
   synthesis F5 confirmed live: the membrane's return paths are the untooled
   half, and a declaration-only change is exactly the case where a consumer
   most needs the update and least justifies spending a human flip.
3. **Declaring an exposed definition is a publication event.** This programme
   was scoped on "reconciliation never crosses the membrane" — true of the
   *pass*, false of the *effect*. Two of the seven are `exposed: true`, and
   both fired the porch advisory on commit. The scope boundary needs that
   qualification.

**The four longevity qualities, re-asked of the delivered state.**
*Maintainable* and *manageable* held: each declaration lives in the definition
it describes, and each domain ruled its own departures. *Extendable* is
untested until a new definition is minted — though the code-architect repair
suggests the birth path was actively hostile to it. **Monitorable failed, as
predicted at target-setting:** derivation coverage still cannot be read
without a manual count, and residual 2 shows the same blindness on the
membrane. That is WP4's question, and it now has three independent sightings
behind it.

## Route

- [x] Stages 1–4 — need, current state, priorities, MVP target. This document.
- [x] **WP1 — the pattern.** QMS declaration written as the worked specimen;
      `declaring-derivation-from-the-atom` + the `domain-refresh.md`
      pre-v3.35.0 backfill line.
- [x] **WP2 — per-domain passes.** All seven definitions declared across five
      corpora, each run in its own repo as that corpus's agent.
- [x] **WP3 — structural finding.** Recorded: convention varies by corpus, and
      one domain files a mirror outside `things/imports/`, which is what made
      correction 1's false finding easy to mint. Left to each domain; the
      estate does not standardise paths.
- [ ] **WP4 — seal.** Two questions now carrying three sightings each: a
      derivation-coverage sensor, and the serve-side counterpart to
      `imports-check` (residual 2). Admitted only on convergence — which is
      now arguably met for the second.
- [x] **review-verify** — MVP met; three process gaps and three residuals
      recorded above.

## Done When

- [x] All seven owned definitions carry a derivation declaration or a recorded
      retire/park ruling.
- [x] No live or paused run executes against an undeclared definition.
- [x] The closed-loop plan's Phase 2b can proceed against pinned evidence that
      this gate is met — **met 2026-08-28**, with the three residuals above
      named rather than closed. The gate asked that no unattended session
      execute an *undeclared* process; it did not ask that every declared
      process be gap-free, and three are not.
