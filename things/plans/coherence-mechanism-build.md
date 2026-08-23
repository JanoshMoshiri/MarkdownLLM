---
id: coherence-mechanism-build
type: plan
status: in-progress
version: 1.1
created: 2026-08-11
priority: high
tags: [coherence, floor, derivation, probes, sequencing]
linked_things:
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: implements
    notes: "This plan is the insight's rule turned into sequenced work: delete > derive > check > cadence, plus the flow-probe layer the loop showed reading cannot cover."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Phase 2's owner. This plan does not restate its items — the backlog is the authority on which checks to build and their gates; this plan only sequences it and supplies the loop's 44-finding evidence for its priority."
  - id: external-review-response-2026-08-10
    relation: references
    notes: "R3 (cold-read cadence — operator decision, evidence amended 2026-08-11) and R4 (walk attestation — held until Phase 2 lands) stay owned there; Phase 4 here is just their scheduling slot."
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: implements
    notes: "The doctrine this plan operationalises: no phase targets zero contradictions; each phase raises the rate at which drift is caught or lowers the rate at which it is created."
---

# Coherence Mechanism Build

The post-loop plan: the eight-round review loop (2026-08-10/11,
`reviews/REVIEW-loop-2026-08-10.md`) measured where coherence actually comes
from — derived surfaces held clean in all eight rounds while hand prose never
did, prose fixes scattered into their own findings, and the one
execution-layer probe outperformed every cold read. This plan sequences the
response. It owns only what no other thing owns (Phases 1 and 3); Phases 2
and 4 are pointers to their owners.

## Phase 1 — Derive the root's own entry file *(owned here)*

The framework root's AGENTS.md is the only entry file in the estate without
managed blocks, and it produced findings in five of eight loop rounds (type
inventory lagging the schema twice, catalog statuses lagging frontmatter,
routing-table rows missing, enum lines drifting against the kernel). Every
one of those sections is derivable from an authority that already exists:

- **types block** from `_schema.yaml` + `RESERVED_STATUSES` (the domain
  generator's `_dk_types` already does exactly this — point it at the root)
- **catalog status annotations** from the specs' live frontmatter
- **Tier-2 routing table completeness** from the `TIERS` map (rows stay
  authored — the query-type column is judgement — but a missing spec becomes
  a coherence Error)
- the **Standard Thing Structure** enum lines reduced to references into
  thing.md rather than restated pipes

Deliverable: root AGENTS.md carries generated blocks where blocks can own
the fact; the pre-commit coherence check gains root-scope drift enforcement
for them, same as every domain already has. Success test: the sections that
drifted in rounds 1–5 become mechanically incapable of drifting.

**Evidence — the enum drift is not inert (2026-08-19).** The Standard Thing
Structure `linked_things` line still advertises `related`, which the
2026-06-12 review pruned from `_schema.yaml` (35 → 13). A session authoring a
plan read the line, used `related`, and took two `validate` Warnings for it.
So the restatement does not merely sit stale — it actively instructs sessions
into defects the floor then catches, which is the strongest available argument
for deriving the block rather than correcting the word.

## Phase 2 — Build the commit-boundary checks *(owner: `mechanical-coherence-checks-backlog`)*

The backlog's hold is lifted for the felt items (review-9 promotions,
perimeter currency; the skills-vs-artifacts and broken-body-reference checks
queue behind them under the same same-builder gate). Not restated here — the
backlog is the authority. This plan adds only the sequencing fact: Phase 2
follows Phase 1 because deriving a surface deletes checks Phase 2 would
otherwise need (don't build a checker for a restatement Phase 1 removes).

## Phase 3 — Flow probes *(owned here — the layer nothing else covers)*

Executable scenario probes for the execution flows cold reads structurally
cannot verify. Candidate suite, each mechanical, each asserting observable
output — pytest-style, CI-runnable, no suppression lists:

1. **Fresh-clone boot** — clone a gated domain cold; assert doctor reports
   setup-ordering (not blocking) before attestation and clean after (the
   probe that already proved itself, made repeatable).
2. **Scaffold birth** — scaffold into a temp repo; assert the birth commit
   lands, blocks match a fresh generation, prompts are delivered
   graph-stripped, the gate blocks the *second* commit without attestation.
3. **Invariant breach** — dirty a thing without committing; assert a fired
   dependency trigger is distinguishable as tree-state (the discipline-vs-
   mechanics split v3.31.0 documented, made observable).
4. **Refresh end-to-end** — version-bump a scratch sentinel; assert
   session-start surfaces the mismatch, refresh --seal seals, domain-kernel
   regen clears drift.
5. **Session close** — assert the session-end commit delimits `worklog` and
   advances the flip-surfacing window (the round-7/8 double-definition,
   pinned behaviorally).

Deliverable: a probe suite (home: `tools/tests/` or `mdllm probe` — decide at
build; tests keep it in CI for free). Success test: each probe fails if the
behavior it pins regresses, in CI, with no human reading anything.

## Phase 4 — The human rhythm *(owner: `external-review-response-2026-08-10`)*

R3: one cold read per substantial release — the measured cadence; *where the
ritual lives* stays the operator's open decision. R4: the walk-attestation
warning is re-judged only after Phase 2 lands, per its own hold. Nothing to
build here; this phase exists so the sequence is visible in one place.

## State after floor-sprint-3 (2026-08-23)

- **Phase 1 — complete.** The root's entry file no longer restates derivable
  facts, in this plan's own order: the enums *deleted* in favour of pointers
  (`d128fa0`), the types section *derived* into a `generated:types` managed
  block (`031c2ac`), and the catalog annotations plus Tier-2 routing
  completeness *checked* (`c10c5a1`). The one departure from the plan's text
  is where the derive/check line falls: the catalog and routing sections are
  authored prose wrapped around a derivable annotation, so generating them
  would have destroyed the one-line descriptions that are their value. They
  are checked. Where a block could own the whole fact, it does.
- **Phase 2 — the felt items, done.** Perimeter currency, the boundary-term
  evidence check, and two of the four review-9 promotions landed; the other
  two are declined on the record at the backlog with the condition that
  would lift each. The unfelt items keep their original hold.
- **Phase 3 — begun.** Probes 1 and 2 landed as `tools/tests/
  test_flow_probes.py`, plus a third that exists *because* the sprint's own
  probes blocked the sprint's own commit and exposed the boundary-terms
  adder. Probes 3–5 (invariant breach, refresh end-to-end, session close)
  remain owned here.
- **Phase 4 — standing, unchanged.** The exit condition below is unmet by
  construction: it needs a post-release cold read, which is an operator act
  after publication, not a sprint deliverable.

**The estimate was wrong in a useful direction.** This plan predicted
"Phases 1+2 are plausibly one build session; Phase 3 a second." One session
took Phase 1, the felt half of Phase 2, and two thirds of the probe work —
because Phase 1's *delete* leg removed load that Phase 2 would otherwise
have had to police. Subtracting before adding compounds; the sequencing
fact this plan already carried was worth more than it claimed.

## Sequencing and exit

Order: 1 → 2 → 3 (4 is standing). Phases 1+2 are plausibly one build
session; Phase 3 a second.

**Precondition met 2026-08-22.** This plan was sequenced after the structure
sprint so its generated blocks derive from a settled module layout rather
than one about to be reshaped (`floor-sprint-1-scope-2026-08-21`, restated
in `floor-sprint-2-scope-2026-08-22`). Sprint 2 sealed that reshaping: the
leaf contract, the shared adapter emission module, and the inverted fitness
gate are landed and verified. This plan is now unblocked and is the next
sprint's subject. Exit condition = the loop insight's dismissal
condition: the checks landed AND one post-release cold read returns zero
fix-residue-class findings. At that point this plan completes and the
insight retires into practice.

## What this plan deliberately does not do

No more review loops (the measured argument is the linked insight). No
umbrella restatement of other plans' items (one owner per fact applies to
plans too). No new judgement-shaped checks (the backlog's suppression-list
gate stands).
