---
id: framework-continuity-brief
type: continuity-brief
status: live
version: 1.3
created: 2026-06-11
domain: markdownllm-framework
last_updated: 2026-06-12
---

# Framework Continuity Brief

## Open Threads

- **Independent review (2026-06-11, external) — action queue:** full review at
  `reviews/REVIEW-independent-2026-06-11.md` (operator to decide whether the
  file stays in full or reduces to this reference). **Staleness pass done
  2026-06-12 session 1** (detail: WORKLOG 12 Jun). **Week-one prerequisites
  done 2026-06-12 session 2, shipped as 3.5.0:** examples under the floor
  (validate discovers `examples/*` sub-corpora, both declare `_schema.yaml`,
  life-manager populated with a working dataset incl. pinned decision record),
  relation vocabulary pruned 35 → 13 (corpus migrated, templates aligned),
  `first-hour.md` on-ramp created and registered. **Remaining, in priority
  order:** (1) **cold-start scaffold eval — the fortnight's centrepiece**
  (fresh agent + non-author human builds a domain from templates; recruit one
  person from the operator's orbit; observe, don't help; score like the 2×2;
  gaps filed as findings per `fixture-fixes-correct-bugs-not-difficulty`);
  (2) fix what the eval surfaces, then write limitations.md + the "why not
  just CLAUDE.md + a notes folder" answer (trivial to write honestly after
  watching a real newcomer); (3) spec the read-side of quarantine —
  unverified `origin: external` bodies still enter context at load;
  (4) one page on concurrency; (5) consider promoting
  generate-or-validate-or-delete from tactic to stated principle (review
  §Needs More Thinking). Deferred until after the eval: harder VAT fixture,
  multi-harness eval matrix, domain visual map.
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
- Remaining active insights in `things/insights/` inform spec-level detail.

## Pending Decisions

- (none)

## Decisions Made This Session (2026-06-12, session 2)

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
