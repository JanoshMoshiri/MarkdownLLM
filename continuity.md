---
id: framework-continuity-brief
type: continuity-brief
status: live
version: 1.0
created: 2026-06-11
domain: markdownllm-framework
last_updated: 2026-06-11
---

# Framework Continuity Brief

## Open Threads

- **Transformation plan Phase 2 (next up):** deletion pass — generated CHANGELOG
  (`mdllm changelog`), REVIEWLOG → retrospectives migration, prune speculative
  trigger conditions. Then Phase 3 (provenance). Canonical plan:
  `framework-v3-transformation-plan`.
- **jmtm orphan records:** 8 expense/profile things have no links — real signal
  from the validator; the domain agent should link them to the FY2025 accounts
  or CT return when those are prepared.

## Live Insights

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

- Kernel format (Phase 5): one generated `kernel.md` vs delimited operative
  sections per spec.

## Decisions Made This Session (2026-06-11)

- `mdllm` lives in `tools/` in the framework repo; domains reach it via
  `framework_root`. Python + PyYAML baseline confirmed.
- Relation vocabulary: declared-and-validated (Warning severity) in each domain's
  schema, capturing actual use; prune at retrospectives.
- Status vocabularies: domain-owned via schema (conflict
  `status-vocabulary-universal-vs-domain` resolved, outcome `superseded`).
