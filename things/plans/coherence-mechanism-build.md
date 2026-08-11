---
id: coherence-mechanism-build
type: plan
status: not-started
version: 1.0
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

## Sequencing and exit

Order: 1 → 2 → 3 (4 is standing). Phases 1+2 are plausibly one build
session; Phase 3 a second. Exit condition = the loop insight's dismissal
condition: the checks landed AND one post-release cold read returns zero
fix-residue-class findings. At that point this plan completes and the
insight retires into practice.

## What this plan deliberately does not do

No more review loops (the measured argument is the linked insight). No
umbrella restatement of other plans' items (one owner per fact applies to
plans too). No new judgement-shaped checks (the backlog's suppression-list
gate stands).
