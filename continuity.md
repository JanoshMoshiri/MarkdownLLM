---
id: framework-continuity-brief
type: continuity-brief
status: live
version: 1.5
created: 2026-06-11
domain: markdownllm-framework
last_updated: 2026-06-15
---

# Framework Continuity Brief

## Open Threads

- **Apply change-reconciliation to a twisted live domain (next session's concrete
  use):** a domain changed mid-process before the pass existed — realign it via
  `change-reconciliation.md` → Retrospective Reconciliation (freeze a baseline
  first, reconstruct the delta from git, full-corpus walk, seal to a new
  baseline). Conversational and agent-driven after the domain's refresh; now
  viable on a mid-tier model because the procedure is structure, not improvisation.
- **Independent review (2026-06-11, external) — action queue:** full review at
  `reviews/REVIEW-independent-2026-06-11.md` (operator to decide whether the
  file stays in full or reduces to this reference). **Staleness pass done
  2026-06-12 session 1** (detail: WORKLOG 12 Jun). **Week-one prerequisites
  done 2026-06-12 session 2, shipped as 3.5.0:** examples under the floor
  (validate discovers `examples/*` sub-corpora, both declare `_schema.yaml`,
  life-manager populated with a working dataset incl. pinned decision record),
  relation vocabulary pruned 35 → 13 (corpus migrated, templates aligned),
  `first-hour.md` on-ramp created and registered. **Session 3 (12 Jun,
  3.6.0):** the agent-only rehearsal ran (10/11, 10/11, then 11/11 once the
  guide routed to the new `mdllm scaffold`); `doctor` shipped;
  eco-essentials completed the first real refresh (2.8 → 3.5.0). **Remaining,
  in priority order:** (1) **cold-start eval with a real human — still the
  centrepiece, now de-risked** (recruit one non-author person; observe, don't
  help; the agent-side path and templates are proven; both reviews agree this
  outranks everything); (2) **refresh jmtm-software** (statutory stakes;
  AGENTS still teaches the pre-v3 validation procedure; working tree had
  uncommitted changes mid-session 3 — check whose, finish or refresh
  cleanly) and property-ventures after it; (3) fix what the human eval
  surfaces, then limitations.md + the "why not CLAUDE.md + a notes folder"
  answer; (4) read-side of quarantine; (5) one page on concurrency (the
  jmtm mid-session collision and the trial agent's framework `index.lock`
  are now two live exhibits); (6) generate-or-validate-or-delete as stated
  principle. Deferred until after the eval: harder VAT fixture, multi-harness
  matrix, domain visual map.
- **Second independent review (2026-06-12) — structural observations left
  with the operator:** findings 1–5 fixed in 3.6.0 same-day. Still open as
  *decisions*, not tasks: WORKLOG is ~93KB of hand-maintained prose and "the
  next REVIEWLOG" (generate-or-validate-or-delete applies); review cadence is
  exhausted until new evidence exists (next review after the human eval, not
  before); release cadence vs domain refresh cost — domains sit 1–5 versions
  behind a framework that versions daily (mechanisable: most of a refresh is
  re-copying three boilerplate blocks — scaffold-adjacent); manifesto still
  promises cross-domain linking no spec defines; README "no setup step" story
  vs first-hour's honest prerequisites — pick one.
- **Harness support is now measured, not assumed:** first non-IDE harness
  session (Cowork, 2026-06-11) — no AGENTS.md auto-discovery; the installed
  pre-commit hook couldn't run (machine-absolute path, bare `python`). Hook
  made portable same session (repo-relative, runtime interpreter resolution)
  — and that fix itself failed on the authoring machine next session (Windows
  Store `python3` alias stub resolvable-but-not-executable; fixed `32d5c6f`,
  hook now executes candidates rather than resolving them). Remaining: spec
  the explicit bootstrap line in framework-discovery.md as a first-class
  discovery route (vendor table re-marked designed-for vs verified-on
  2026-06-12); consider `install-hook` self-testing its emitted script. See
  `agents-md-discovery-is-harness-dependent`,
  `portability-claims-need-execution-tests`.
- **Domain visual map:** replicate `framework-map.md` for a live domain
  (eco-essentials or jmtm-software) — same three-view structure (elevation,
  link graph, floor mapping), but domains have skills and live things where
  the framework has specs. Explicitly deferred by the operator (2026-06-11,
  session 7) to a future session.
- **Harder fixture + claim-language pass (next session's centerpiece):** the
  full 2×2 ran (2026-06-11, 20 trials, see Decisions) but the fixture's
  reasoning core saturated — every cell got the figures right, all variance
  was the asymmetric `has-deadline` link. Two follow-ups: (1) design a
  fixture whose condition-neutral core discriminates (candidates: partial
  exemption, multi-quarter with conflicting/duplicate records, an
  amendment/belief-revision flow, distractor things), then re-run the 2×2;
  (2) soften the declarative structure-beats-scale claim in README.md
  ("The result: ...") and manifesto §elegant-constraint to tested-hypothesis
  framing, citing first results honestly. See
  `first-2x2-measured-convention-following-not-reasoning`.
- **Tier 2 kernel blocks:** session-memory, belief-revision, provenance,
  triggers, derived-index — low priority (demand-loaded anyway).
- **First jmtm decision-record filing:** annual accounts due 2026-07-31 —
  prepare through a `type: decision` with pinned inputs. Register
  `adapters/scheduled-triggers.ps1` in Task Scheduler before then.
- **jmtm orphan records:** 8 expense/profile things unlinked — link them when
  the FY2025 accounts/CT return are prepared.

## Live Insights

- `agents-md-discovery-is-harness-dependent` — discovery and the floor are
  harness/environment properties, not framework properties; the Cowork session
  is the first measured harness data point (partial failure; hook fixed
  in-session).
- `portability-claims-need-execution-tests` — a floor/portability claim is
  verified only by executing the capability in the target environment;
  resolution (command found, path exists) is not verification. The commit
  test is the floor's execution probe in any new environment.
- `first-2x2-measured-convention-following-not-reasoning` — the 2026-06-11
  run's honest reading: structure bought determinism (opus+fw 5/5), the
  diagonal went the manifesto's way at ~23% cost, but the reasoning claim
  remains untested until a fixture's condition-neutral core discriminates.
- `fixture-fixes-correct-bugs-not-difficulty` — when a Stage 2 trial fails,
  fix fixture self-consistency bugs (id templates, schema names) but leave
  genuine model reasoning/attention gaps as findings, not patches.
- `hook-compliance-correlates-with-scope-not-awareness` — fix missed hooks by
  reducing load, not adding rules; the justification for the deterministic floor.
- `tracking-artifacts-can-drift-from-reality` — motivates generated-not-maintained
  surfaces (Phase 2 deletions).
- `the-notation-changed-not-the-primitives` — the razor for admitting new
  mechanisms; canonical articulation of the paradigm.
- `derived-index-is-attention-cache-not-search-layer` — governs the Phase 5 kernel
  (a derived index over the spec corpus itself).
- `consistency-is-maintained-at-change-not-by-sweeping` — semantic consistency is
  maintained at the point of change, not by periodic sweeping; the basis of
  `change-reconciliation.md`.
- `mechanical-assimilation-is-blind-to-prose-dependencies` — declared edges are
  walkable, prose references are the dark region, the human is the backstop;
  caught the routing-table miss on the spec's first live use.
- `change-safety-is-defense-in-depth` — layer overlapping nets (design, static
  trace, textual trace, walk, retrospective); no single net catches every dark
  region, so a miss falls through to a cheaper one.
- Remaining active insights in `things/insights/` inform spec-level detail.

## Pending Decisions

- (none)

## Decisions Made This Session (2026-06-15)

- **`change-reconciliation.md` shipped (v3.7.0):** the evolve-phase gap is filled —
  semantic consistency as a human-cued four-beat pass (cue, assimilate, walk,
  seal), fractal across scale, running on the existing indexes. Designed in
  dialogue; the human drove the two load-bearing reframes (change management not
  sweeping; the driver, not the agent, names the inflection).
- **The dark region is structural, not a defect to automate:** assimilate is
  complete only over declared edges; prose dependencies are the human's backstop.
  The textual-trace (grep) tier was added to narrow it to the conceptual residue,
  and immediately caught a `framework-map` spec-count drift the floor could not see.
- **Retrospective mode written into the spec, not left to the model:** structure
  beats reasoning — capturing freeze→reconstruct-from-git→full-corpus-walk lowers
  the model bar so a mid-tier agent can follow it rather than improvise.
- **Invariants/test-suite tier deferred:** the retrospective is the standing
  backstop; a second mechanism for the same job would be redundant machinery.

## Decisions Made This Session (2026-06-12, session 3)

- **Rehearsal before tool, deliberately:** the pre-scaffold trials were run
  first so the tool's justification would be measured, not assumed — and the
  post-tool trial closed the loop at 11/11. The full protocol and honest
  reading live in `evals/README.md`; the generalisable lesson in
  `agents-drop-mechanical-birth-steps-not-semantic-ones`.
- **jmtm refresh deferred mid-session:** its working tree had uncommitted
  modifications (parallel session suspected) — single-writer-by-convention
  respected rather than raced.
- **Excluded-trial evidence kept:** harness failures are excluded from the
  report but their result.json files are committed under
  `evals/results/excluded/` — exclusion with evidence, not deletion.
- **Spec prose no longer names framework versions** (review #2 finding 3
  generalised): the sentinel is the only version surface.

## Decisions Made Session 2 (2026-06-12)

- **The fortnight's strategy set by the operator:** point the v3 medicine at
  the periphery and at a user who isn't the author. Week one (this session)
  cleared the prerequisites; the cold-start scaffold eval is the centrepiece;
  model-science work (harder fixture, harness matrix) explicitly deferred
  until the eval lands.
- **Sequencing inside week one:** vocabulary prune first so the examples and
  on-ramp teach the final relation set; examples second; on-ramp last.
- **life-manager populated rather than deleted** (the review allowed either):
  the worked dataset is what a cold-start participant copies, and it now
  demonstrates triggers, provenance, and the floor end-to-end — including one
  *deliberately* overdue task so `mdllm triggers` always has a find (a
  feature; documented in-thing so nobody "fixes" it).
- **`type: dependency` dropped from life-manager:** `parent`/`dependencies`/
  `blocks` fields express hierarchy and sequencing; things are for content.
- **Relation prune shape:** 9 semantic + 4 mechanical relations; the
  `supersedes`/`superseded-by` pair survives because the validator itself
  checks the backlink; decomposition relations remain thing.md universal
  guidance rather than framework-corpus vocabulary.
- **Session-1 decisions** (staleness pass, token-figure convention) are
  preserved in WORKLOG 12 June, Session 1 — removed here to keep the brief
  lean.
