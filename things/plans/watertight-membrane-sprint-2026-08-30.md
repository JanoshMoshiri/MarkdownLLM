---
id: watertight-membrane-sprint-2026-08-30
type: plan
status: in-progress
version: 1.0
created: 2026-08-30
session: 2026-08-30
priority: critical
tags: [membrane, imports, serve-side, staleness, closed-loop, sprint]
informed_by:
  - id: operator-queue-2026-08-28
    commit: 26b0777edca4a4a146891e0b52492b8b22ba0f49
  - id: estate-retrospective-synthesis-2026-08
    commit: 26b0777edca4a4a146891e0b52492b8b22ba0f49
linked_things:
  - id: closed-loop-operating-state
    relation: implements
    notes: "The operator's ASAP bar is this plan's reason: domains are closing the loop (the pilot dispatcher runs daily), and every autonomous run rests on the membrane this sprint makes watertight."
  - id: operator-queue-2026-08-28
    relation: derived-from
    notes: "Rows 4 (mirrors) and 9 (serve-side blindness) are Phases A–C. The operator's 2026-08-30 grant: sort both, agent's own sprint list, corpus as context, domains as private data pools."
  - id: cross-domain-readiness-is-a-shared-signal-not-a-producer-push
    relation: informs
    notes: "Governs Phase C's design: freshness is solved consumer-side; awareness is the carved-out facet; nothing here builds a producer push."
  - id: source-behind-mirror-is-still-a-consumer-side-read
    relation: informs
    notes: "Governs Phase C's shape: no global index, no producer enumerating consumers. estate-check batching is the only multi-root form permitted."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: references
    notes: "Stop condition: this sprint ends when the phases below are done or gated; gates are listed for the operator, never worked around."
triggers:
  - type: time
    condition: "2026-09-05 reached"
    action: "If Phase A/B operator gates (verified flips, trust grants) are still unruled, surface them alongside the dispatcher dead-man — the same date, deliberately: both are the closed loop waiting on its human seats."
---

# Watertight Membrane Sprint — 2026-08-30

The operator's grant (2026-08-30, verbatim intent): sort the mirror issue and
the blindness issue; make the operating layer watertight now that domains are
closing the loop; review the staleness-protection mechanism; agent makes its
own sprint list and follows the universal workflow. Domains are used as data
pools under the operator's explicit session grant, and remain private — this
plan names them only by the established public substitutions.

## Current state (evidenced this session)

- **Mirrors (queue row 4):** both sides of the regulated overview↔engineering
  pair pin superseded commits. Both sources moved 2026-08-28 in the same
  universal-workflow derivation pass. Both mirrors sit `verified: true`
  against pins two commits behind — the record claims a currency it no
  longer has.
- **Blindness (queue row 9 + synthesis F5):** one class, four faces — serve-side
  discharge blindness, trusted-but-unwatchable (COVERAGE 0/43),
  unpinned-at-scale (0/120 — the dispatcher pilot's own corpus), and
  quarantine acted-through. Root cause of the zero coverage, established by
  reading the floor: `imports-check` is fully built, but the external-trust
  policy correctly refuses every route because **no clone-local grant has ever
  been executed** — the trust store is empty. The blindness is not a missing
  tool; it is an unperformed trust act plus one address-book defect (the
  engineering-side book launches routes via bare `python`, against the manual
  CLI launch doctrine).
- **Staleness protection:** eight corpus-general coherence checks ride every
  domain's pre-commit hook (stable-staleness, dead vocabulary, zero-run
  definitions, redundant known-fields, template residue, derived-index drift
  Error, domain-kernel drift Error, skill-vocabulary Warning). Hooks present
  in all 13 domain repos; generated AGENTS.md blocks in 12 of 13.
- **Docs sprint:** held by the operator 2026-08-17 on vendor-plan completion;
  every vendor build phase is now complete and only Phase 8 (operator-owned
  rollout/release ruling) remains — the hold has narrowed to an operator
  decision, not agent work.

## Desired state

Every autonomous loop rests on watched, current imports: mirrors fresh and
attributably re-verified; import-freshness routes executing (coverage > 0);
the dispatcher pilot's imports pinned and checkable; the remaining blindness
facet (discharge) designed from the post-routes reality; the operating layer's
staleness floor verified watertight for workflow-driven domains.

## Phases

- [x] **A — Mirror repair.** *(Done 2026-08-30: both mirrors re-synced from
  their sources' current per-thing commits via the face render, landed
  `verified: false`, committed and autopublished in their owning repos. The
  two attributable flips are staged for the operator with diff summaries.)* Re-sync both mirrors from their sources at the
  sources' current per-thing commits: content refreshed, `source_commit`
  re-pinned, `verified` dropped to `false` (content changed — the quarantine
  re-opens, per the kernel). Commit in each owning domain repo. Then present
  both content diffs compactly for the operator's two attributable `verified`
  flips. **Gate: the flips are the operator's** (census-ratified,
  consequence-permanent; "trust" is a named true gate).
- [x] **B — Route execution.** *(Done to the gate, 2026-08-30: all six
  consumer address books rewritten off bare `python` onto the doctrine
  launcher, committed and autopublished per repo; all 12 entries reviewed —
  each spawns the estate's own tool against the operator's own clones; the
  hash-bound grant block is assembled and staged. Coverage >0 becomes true at
  the operator's grant. Amended after a live probe of the repaired route:
  two latency defects hid behind the never-crossed trust gate — the
  launcher's ~12s per-spawn probe vs the client's 10s deadline, and a
  3-git-spawns-per-thing manifest build (~33s for 46 things). Both fixed in
  the floor — fast-path substitution through `sys.executable` for entries
  resolving to this installation, and batched head-view reads — end-to-end
  4.3s, proven live.)* Fix the engineering-side address book launch
  route (bare `python` → the doctrine launcher). Run `external-trust review`
  for each consumer×source entry actually used; confirm each entry spawns the
  estate's own tool against the operator's own clones and nothing else;
  assemble the exact hash-bound grant commands as a ready-to-run block.
  **Gate: the grants are the operator's** (permission-bearing;
  `agents-cannot-self-install-permission-bearing-hooks`). After grant:
  `estate-check` proves coverage > 0.
- [x] **C — Pin repair at the pilot.** *(Done 2026-08-30, and cheaper than
  planned: the "unpinned" imports were short-SHA pins, not missing triples.
  All 76 resolved to full SHAs by git in their source repos — zero failures,
  zero ambiguities; the 45 triple-less externals are genuine outside-world
  ingestions, correctly not pinned. Committed and autopublished.)* The dispatcher pilot's imports are
  unpinned (0/120 checkable). For each unpinned import whose body matches the
  source's current face content exactly, backfill the reference triple at the
  source's current per-thing commit — truthful by byte-comparison; any
  mismatch is flagged, never backfilled. Committed in the pilot's repo.
- [x] **D — Serve-side design arc.** *(Done 2026-08-30 — outcome: no build.
  `serve-side-blindness-dissolves-into-composition` records the design: all
  four blindness facets land on already-shipped primitives; what was missing
  was the trust act (Phase B) and the ask-arms-a-watch convention. Reopen
  conditions named.)* With freshness, divergence, and
  face-coverage awareness all live once B lands, the genuinely unbuilt facet
  is **discharge blindness** (an answered ask is the serve-side mirror of a
  stale import). Write the design as a decision/plan thing against the
  post-B reality, honouring the two governing insights (no producer push, no
  global index). Implement only what the design admits; route any new
  coherence check through the mechanical-coherence-checks-backlog gate.
- [x] **E — Staleness watertight review.** *(Done 2026-08-30 —
  `operating-layer-staleness-review-2026-08-30`: hooks byte-identical 13/13,
  generated blocks 12/13 with the parked domain's refresh as its wake-up
  act, one candidate check routed to the backlog's gate, and the `exposed`
  egress leak fixed in the floor with a regression test.)* Verify the eight general checks
  bite estate-wide: hook currency (present ≠ current), the one domain without
  generated blocks (deploy or record its park), and the one candidate gap —
  skills instructing workflow *stage* vocabulary that no check keys to the
  definitions' declared stages. Produce the review as an artifact; route
  check candidates through the backlog's gate; fix what is mechanical now.
- [ ] **F — Report.** Sprint summary with the operator's gate list (flips,
  grants, docs Phase 8 note), publication debt, and the queue rows moved.

## Not in this sprint

The docs sprint stays held (its gate is now the operator's Phase 8 ruling —
reported, not worked). The read-gate downward-direction declaration stays
sequenced behind session-start-hardening Phase 5 so the acceptance baseline
stays comparable. Statutory work stays in its own domain under its own
contract.
