---
id: framework-continuity-brief
type: continuity-brief
status: live
version: 1.1
created: 2026-06-11
domain: markdownllm-framework
last_updated: 2026-06-11
---

# Framework Continuity Brief

## Open Threads

- **Independent review (2026-06-11, external) — action queue:** full review at
  `reviews/REVIEW-independent-2026-06-11.md`. Priority order: (1) fix
  birth-path staleness — `templates/AGENTS.md.template` is pre-kernel,
  `framework-discovery.md` is pre-v3 (stable but stale: v2.8 sentinel example,
  `domain/` vs `domains/`), `domain-specification-guide.md:294` names a
  "session-end:continuity hard hook" that doesn't exist (session-end is a bound
  prompt); (2) bring `examples/` under the floor — excluded from validation,
  both pre-v3, no framework_root, life-manager has zero things; (3) cold-start
  scaffold eval (fresh agent + non-author human builds a domain from templates)
  before the harder VAT fixture; (4) prune the relation vocabulary (~35 → ~12)
  and replace hand-written token estimates with generated ones
  (derived-index.md:146 and scalability-guide.md:263 disagree 10–20x);
  (5) spec the read-side of quarantine — unverified `origin: external` bodies
  still enter context at load; (6) limitations.md + differentiation answer;
  (7) one page on concurrency.
- **Harness support is now measured, not assumed:** first non-IDE harness
  session (Cowork, 2026-06-11) — no AGENTS.md auto-discovery; the installed
  pre-commit hook couldn't run (machine-absolute path, bare `python`). Hook
  made portable same session (repo-relative, runtime interpreter resolution).
  Remaining: spec the explicit bootstrap line in framework-discovery.md as a
  first-class discovery route; re-mark the README vendor table designed-for vs
  verified-on. See `agents-md-discovery-is-harness-dependent`.
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

## Decisions Made This Session (2026-06-11, session 6)

- **Review accepted** (status: stable): `reviews/REVIEW-independent-2026-06-11.md`
  — its action queue stands as the top open thread above.
- **First non-IDE harness test run (Cowork):** no AGENTS.md auto-discovery;
  pre-commit hook couldn't execute (machine-absolute path, bare `python`).
  Hook made portable and reinstalled (`fix:` commit); insight
  `agents-md-discovery-is-harness-dependent` records both failure modes.
  Operator to verify the reinstalled `.git/hooks/pre-commit` contains no
  absolute path (it now resolves root and interpreter at run time).
- **Commit authorship convention:** agent commits are authored as the operator's
  standard identity (Janosh Moshiri, GitHub noreply) — no agent-named authors;
  the WORKLOG records which sessions were agent-operated.
- **Session-5 decisions** (full 2×2 results and the unpatched haiku link misses)
  are preserved in WORKLOG 11 June, Session 5 — removed here to keep the brief lean.
