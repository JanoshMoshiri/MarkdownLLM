---
id: operator-queue-2026-08-28
type: artifact
status: evolving
version: 1.2
created: 2026-08-28
session: 2026-08-28
tags: [operator-queue, seat-protocol, verdicts, closed-loop, one-sitting]
informed_by:
  - id: estate-workflow-derivation
    commit: cb68dfb8468021db2a2a99b7ff889546b4d8bda4
  - id: gates-census-2026-08
    commit: cc86f4568c8e591cfaed9897916a8f2b0b1e88cc
  - id: estate-retrospective-synthesis-2026-08
    commit: e1ad077a01d31bc85c9904a1674cf9669e64cd89
  - id: framework-retrospective-2026-08c
    commit: 7bffcb162f01c5cc6afb98756eca58bc5c5f79fe
linked_things:
  - id: closed-loop-operating-state
    relation: implements
    notes: "Phase 3 — the seat protocol — executed once by hand. The queue is what the desired state says reaches the operator: verdicts-in-waiting, options with evidence, never homework. Building it manually is the prototype for the thing that eventually assembles itself."
  - id: gates-census-2026-08
    relation: derived-from
    notes: "Row 15's verdict is the highest-leverage single ratification here: it downgrades several other rows from operator seat to agent execution."
  - id: estate-retrospective-synthesis-2026-08
    relation: derived-from
    notes: "Its ten-row verdict table is folded in rather than restated; rows that today's census re-evidenced are marked."
  - id: estate-workflow-derivation
    relation: derived-from
    notes: "The three process gaps and two stale mirrors this programme surfaced and deliberately did not close."
triggers:
  - type: time
    condition: "2026-09-10 reached"
    action: "If this queue has not been ruled, report which tier-1 rows remain open and what each is blocking. The queue idles at the operator's seat by design; an undated idle is the drift the estate already learned to chase."
---

# Operator Queue — 2026-08-28

Everything currently waiting on the operator, in one place, each row carrying a
proposed verdict and its evidence. Read base: framework root
`commit:3cea4659260a7195dacb3ee766fe5284d7f2468f`.

**How to use it.** Tier 1 is five rows that gate the loop; nothing else does.
Tier 2 is assent-or-overrule on work already reasoned out. Tier 3 is carried
with a date and needs nothing today — it is listed so the queue is honest about
what exists, not to ask for attention.

The proposals are the agent's. Flipping one is not a defeat: the line between a
gate and a habit is the operator's to draw.

> **Ruling update, v1.1 (2026-08-28, same day).** The operator ruled
> `settled-reasoning-is-standing-authority`: where the corpus already holds
> the evidence and the decided direction, the agent acts without per-row
> assent. Applied to this queue:
>
> - **Executing now:** row 10 (skill orientation exclusion), row 11 (dark
>   obligations), row 12 (zero-run sensor) — launched as one floor wave; the
>   structural-pin check was already building when the ruling was given.
> - **Authorised, sequenced behind the running wave:** row 9 (serve-side
>   freshness counterpart — design-first arc, four sightings), row 15
>   (un-park the operating-layer quality loop), row 16 (author the JMTM
>   write skill from its fifteen months of earned practice — the park
>   precedent applies only where there is nothing to fill from), row 13's
>   reduced list (the two owed domain retrospectives, run as those domains'
>   agents).
> - **Unchanged — still the operator's:** rows 1–5 (the census flip, the
>   dispatcher grant, the push, the verified re-flips, the pilot choice) and
>   every gate that names a human. Rows 6–8 also stay: each is a same-day,
>   single-sighting proposal — below the settled bar, and each is its
>   domain's judgement (row 6 additionally sits behind that domain's own
>   declared approval gate). The bar holding there is the ruling working,
>   not hesitancy returning.

> **Reconciliation update, v1.2 (2026-08-29).** Written by a
> change-reconciliation pass over the framework root, at the operator's cue.
> **This is a status pass, not a ruling pass** — no row below is ruled here;
> rows are moved only where the framework root holds the evidence, and every
> row whose evidence lives in a domain repository is left exactly where v1.1
> put it. Read base: `commit:85d1ac408ea4fcc2909ea364228aca1cda1eb537`.
>
> **Closed, with the evidence named:**
>
> - **Row 2 — the dispatcher authority grant. Done.** The operator performed
>   the grant and registered the job: daily 08:00 Europe/London, scoped to
>   the pilot, stop condition stated as work. It has fired twice, and both
>   runs filed digests in the pilot repo. This was the row standing between
>   a built loop and a running one, and it no longer is — which does **not**
>   mean the loop works: both firings stopped fail-closed before touching a
>   fired trigger, so the launch is proven and the work is not
>   (`closed-loop-operating-state`, Phase 4).
> - **Row 3 — the release push. Done.** `mdllm estate-sync . --status`
>   reports no unpublished commits across fourteen repos, and the root sits
>   at parity with its remote. The nineteen-commit stack this row was
>   written about is published; row 15's verdict now has the review seat it
>   leans on.
> - **Rows 10, 11, 12 — the floor wave. Shipped**, as the v1.1 block said
>   they would be: the `skill` orientation exclusion, matured obligations on
>   terminal carriers, and the zero-run definition sensor. The structural-pin
>   resolution check that occasioned the standing-authority ruling shipped in
>   the same wave.
> - **Row 15 — un-park the operating-layer quality loop. Done.**
>   `operating-layer-quality-loop` is `completed`; its floor half — the
>   skill-vocabulary check — ships in `mdllm coherence`, and the judgement
>   half landed as a reflexive scan in `retrospective.md`. The skill-age Info
>   it originally proposed was declined, with its lifting condition recorded
>   rather than dropped.
>
> **Still open, and evidenced as still open:**
>
> - **Row 4 — the two stale mirrors.** Not closed. The consuming side still
>   pins the superseded source commit; nothing has been re-synced and no
>   `verified` flip has happened. This remains consequence-permanent and the
>   operator's, and it remains the row nothing mechanical will chase while
>   `imports-check` coverage sits at zero.
> - **Row 9 — the serve-side counterpart to `imports-check`.** Not built.
>   Recorded plainly because the queue's own recommendation was *"build it,
>   and put it ahead of the dispatcher"* — and the dispatcher shipped first.
>   That is a real divergence between what this queue advised and what
>   happened, not an oversight to be quietly re-ordered: every autonomous
>   loop now running rests on the blindness this row names. It is the
>   agent's strongest standing recommendation, unchanged and now overdue by
>   its own argument.
>
> **Not evidenced from this pass, and therefore not moved:** rows 6, 7 and 8
> (the three process gaps — each its domain's judgement), row 13 (the reduced
> retrospective list), row 16 (the write skill), and row 17 (the memory-vs-stream
> question, which is the operator's to answer). This pass is scoped to the
> framework root and deliberately did not reach into domain repositories to
> settle them. **Absence of movement here is absence of evidence, not evidence
> of absence.**
>
> **Tier 3, re-dated:** the three stalls are now 32d, 28d and 24d past their
> last touch. `framework-retrospective-2026-08b`'s dated trigger has fired on
> a terminal carrier — visible only because the matured-obligations fix in
> row 11 shipped, which is that fix earning its keep on its first week.

---

## Tier 1 — the five that gate the loop

| # | Subject | Proposed verdict | What it unblocks |
|---|---|---|---|
| 1 | **Ratify the gates census** (20 rows, `gates-census-2026-08`) | Accept as proposed: 8 consequence-permanent, 6 designed seats, 6 familiarity-shaped | Highest leverage in the queue. Row 15 alone converts ritual spec updates, insight triage and status truthing from operator seats into agent execution with the root push as review — which downgrades several Tier-2 rows below to "already answered". |
| 2 | **Grant the dispatcher its authority** (closed-loop Phase 2b) | Grant, once per harness | The one constructive act only the human can perform (`agents-cannot-self-install-permission-bearing-hooks`). Everything in Phase 2 is built and waiting on it. |
| 3 | **The release push** — root is +19 unpushed | Push when the Explorer arc closes, as one deliberate act | The estate cannot see nineteen commits of substrate work, including the whole derivation programme. Release surfaces stay `autopush: false` by design, so this is yours by construction, not by omission. |
| 4 | **The two stale mirrors** — overview holds engineering's lifecycle pinned at `85f6a78` (moved to `26d102f`); engineering holds overview's agenda, likewise moved | Re-sync both, then re-flip `verified` attributably | Both sides of a cross-mirrored pair changed today, and **nothing will detect it**: `imports-check` returned COVERAGE 0/101 and 0/43, every route unreachable. The flip is your attributed act, so the pass adopted nothing. |
| 5 | **Pilot domain for Phase 4** (one full hands-off cycle) | `regulated-qms` or code-architect's refactoring process | Both are declared *and* gap-free, with real runs behind them. Do not pilot on engineering, overview's agenda, or code-architect's delivery process — each carries an open process gap (Tier 2, rows 6–8). |

**If time is short, rows 1 and 2 are the two that matter.** Row 1 collapses the
queue; row 2 starts the loop. *(Both done. As of 2026-08-29 the sentence reads:
row 4 is the only Tier-1 row left, and row 9 in Tier 2 is the one the agent
would still push hardest.)*

> **Ruled 2026-08-28 (`gates-census-ratified-2026-08-28`).**
> **Row 1 — done.** All twenty census verdicts confirmed as proposed, no row
> flipped; the census is `stable`. Rows 15, 17 and 18 are agent execution from
> today with the push as the review seat, which is what collapses much of
> Tier 2 below.
> **Row 5 — done.** The Phase 4 pilot is `regulated-qms`.
> **Rows 2, 3 and 4 remain open and remain the operator's**: the dispatcher
> authority grant, the release push, and the two `verified` re-flips. Row 2 is
> the one now standing between the built loop and a running one.
>
> *Superseded the next day for two of the three — see the v1.2 block above:
> rows 2 and 3 were performed on 2026-08-29. **Row 4 alone still stands.**
> This paragraph is left as written because it is the dated record of what
> was true at the ratification sitting.*

---

## Tier 2 — assent or overrule

Each has a proposed answer and evidence. A word each.

### The three process gaps the derivation pass surfaced

Recorded, not repaired — each is its domain's judgement.

| # | Where | The gap | Proposal |
|---|---|---|---|
| 6 | engineering lifecycle | Operability and monitorability are asked by **no stage** — on the full track, which is reserved for exactly the changes that *create* operational surface. Corroborated by the domain's own record of erroring, unowned scheduled jobs. | Add a sub-gate at architecture rather than a new stage. Full track only; the short track's collapse is proportionate. |
| 7 | overview weekly agenda | `review-verify` is realised by **no stage**. Input is guarded, output is not — an agenda that silently dropped its coverage header would read exactly as confident as a compliant one. | Declare the operator's reading at the forum to *be* the review, and gate it. Cheaper than a stage, and it matches what already happens. |
| 8 | code-architect delivery process | `set-mvp-target` is made **nowhere**, at the radius where an implicit target costs most — while its own `accept` stage demands criteria that must have been set earlier. | Sub-gate inside `design`. Its first bill comes due at `accept`, and no run has passed `design` yet, so this is cheap to fix now and expensive later. |

Also from the same pass, three smaller ones: the engineering lifecycle declares
only two of four progression outcomes (a dropped run has **no declared exit**);
its run-to-run hand-off runs through a shared as-is map with no declared pin;
and its first-run-or-retire ruling is dated 2026-09-30 but could be taken now.

### Estate synthesis rows re-evidenced today

| # | Subject | Proposal |
|---|---|---|
| 9 | **Serve-side counterpart to `imports-check`** | **Build it, and put it ahead of the dispatcher.** Now four sightings, one of them today's zero-coverage measurement. It blocks row 4, it blocks any relaxation of the verified flip, and every autonomous loop resting on imported state inherits the blindness. This is the recommendation the agent would push hardest. |
| 10 | `skill` missing from the orientation exclusion set | Fix in the floor — 12 phantom loops across 4 domains, verified live. Agent-executable. |
| 11 | Dark obligations (past-dated triggers on terminal carriers vanish) | Fix the bucket asymmetry, or rule it intended and document it. |
| 12 | Zero-run definition sensor | Build the Info. **Today's census is the argument**: it found the zero-run class by hand across nine domains, which is precisely the work a one-line sensor removes. |
| 13 | Retrospective coverage for the six silent domains | **Partly answered by today's census.** Two are dormant with correctly-recorded parks and owe nothing; the others still owe one. Rule the reduced list. |
| 14 | Cadence doctrine, schema trio, absorption tax, aggregation read, `a-well-kept-record…` ratification | As proposed in the synthesis. Most become agent-executable if row 1 passes. |

### New today

| # | Subject | Proposal |
|---|---|---|
| 15 | **The operating layer's defect rate** — four domains in one day: code-architect's write skill instructing an unvalidatable edge, eco-essentials' four unrunnable workflows (parked), career domain's lifecycle written ahead of practice, JMTM's write skill still carrying scaffold placeholders | **Un-park `operating-layer-quality-loop`.** Its hold was the derivation shape, now settled. Four independent instances in a day is the felt evidence the plan was waiting for, and every one was found by a human-directed read that happened to look. |
| 16 | JMTM write skill retains scaffold placeholders | Park it deliberately, per the `agent-architect` precedent, or author it from earned insights. Not both, not neither. |
| 17 | Memory record vs commit stream — life-ops is recorded as in real weekly use since 2026-08-02; the stream shows one week planned, never closed, nothing since 08-08 | Tell the agent which is true. If weekly use happens outside git, **that is the finding** and the domain's instruments are measuring nothing. |

---

## Tier 3 — carried, dated, needs nothing today

- `hard-hook-vocabulary-contradicts-observable-trigger-insight` — the estate's one open conflict, resolution direction already proposed in it (both-valid via the anchor distinction).
- `thing-lifecycle.md` ruling — corpus is inside its own 200–300 ceiling; reconcile or park.
- `deterministic-calculation` closure — unruled across two retrospectives.
- Three stalls past the 21-day line: `evidence-and-eval-backlog` (31d), `response-depth-control` (27d), `cohesiveness-sensors` (23d).
- `regulated-development` keep-or-retire — chased for 2026-09-05; today's census says wait for it rather than pre-empt.
- **The VAT quarter May–Jul 2026, due 7 September.** Not a queue item — a real deadline. The return thing does not exist yet; `statutory-filing-cycle` says it is born when the deadline enters its window, and instancing plus filing are the director's acts.

---

## What the agent will do without being asked

If Tier 1 rows 1 and 2 pass, the following execute without further rulings:
the row-15 class of ritual spec updates, insight triage, the floor fixes in
rows 10–12, and the reduced retrospective coverage in row 13. Everything in
Tier 2 marked as a domain judgement stays with its domain.

Nothing in this queue is executed on assent alone where it touches an
irreversible: the push, the authority grant, the `verified` re-flips, and any
statutory filing remain the operator's acts however the rest is ruled.
