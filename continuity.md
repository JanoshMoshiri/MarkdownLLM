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

- **Eval Stage 2 (highest-value next):** the headless agent loop — seed temp
  worktree, run fresh agent on scenario prompt, assert via `mdllm eval`. Unblocks
  the small-vs-large model experiment (the manifesto's testable claim).
- **Tier 2 kernel blocks:** session-memory, belief-revision, provenance,
  triggers, derived-index — low priority (demand-loaded anyway).
- **First jmtm decision-record filing:** annual accounts due 2026-07-31 — prepare
  through a `type: decision` with pinned inputs (provenance.md's first production
  use). Register `adapters/scheduled-triggers.ps1` in Task Scheduler before then.
- **jmtm orphan records:** 8 expense/profile things unlinked — domain agent
  should link them when the FY2025 accounts/CT return are prepared.
- **Push pending:** all of 2026-06-11's commits (framework + jmtm) are local;
  harness blocked direct push — Janosh runs `git push origin main --tags`.

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

- (none — session 2026-06-11 cleared the queue)

## Decisions Made This Session (2026-06-11)

- `mdllm` lives in `tools/`; Python + PyYAML. Relation vocabularies
  declared-and-validated per domain schema. Status vocabularies domain-owned
  (conflict resolved, `superseded` — see `decision-status-vocabulary-domain-owned`,
  the first pinned decision record).
- Kernel format: `<!-- kernel -->` blocks in specs, extracted by `mdllm kernel`
  into generated `kernel.md`. Measured: 1.6k tokens replacing 21.4k (see insight
  `operative-rules-are-a-small-fraction-of-spec-prose`).
