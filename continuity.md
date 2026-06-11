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

- **Transformation plan Phase 1 (next up):** build `tools/mdllm.py` (validate /
  triggers / index / tokens), define the normative per-domain schema, resolve the
  status-vocabulary conflict, wire pre-commit enforcement. Canonical plan:
  `framework-v3-transformation-plan`.
- **Open conflict:** `status-vocabulary-universal-vs-domain` — universal status
  enum vs domain-defined state machines. Resolution designated to Phase 1.
- **Relation vocabulary proliferation** (~18 values in use vs ~8 blessed) — decide
  in Phase 1 whether it becomes declared-and-validated or stays emergent.

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

- `mdllm` packaging: single file in `tools/` (lean) vs sibling repo domains vendor
  (versionable independently).
- Kernel format: one generated `kernel.md` vs delimited operative sections per spec.

## Questions For Next Session

- Confirm Python + PyYAML as the `mdllm` baseline (Python 3.12 confirmed on the
  primary machine, 2026-06-11).
