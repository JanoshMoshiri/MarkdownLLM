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

- **Run the model experiment (next session's centerpiece):** Stage 2 runner is
  now confirmed working end-to-end on Windows (smoke test 2026-06-11, see
  Decisions below) — scored 6/7 on vat-quarter-basic (haiku, framework). The
  2×2 protocol (haiku/opus × framework/bare, ≥5 trials/cell) is in
  `evals/README.md`. Next action: run the full protocol. The remaining 1/7
  (`linked_things` vs `relations` on the has-deadline link) is a known finding,
  not a bug — left as-is per `fixture-fixes-correct-bugs-not-difficulty`.
- **Tier 2 kernel blocks:** session-memory, belief-revision, provenance,
  triggers, derived-index — low priority (demand-loaded anyway).
- **First jmtm decision-record filing:** annual accounts due 2026-07-31 —
  prepare through a `type: decision` with pinned inputs. Register
  `adapters/scheduled-triggers.ps1` in Task Scheduler before then.
- **jmtm orphan records:** 8 expense/profile things unlinked — link them when
  the FY2025 accounts/CT return are prepared.

## Live Insights

- `hook-compliance-correlates-with-scope-not-awareness` — fix missed hooks by
  reducing load, not adding rules; the justification for the deterministic floor.
- `tracking-artifacts-can-drift-from-reality` — motivates generated-not-maintained
  surfaces (Phase 2 deletions).
- `the-notation-changed-not-the-primitives` — the razor for admitting new
  mechanisms; canonical articulation of the paradigm.
- `derived-index-is-attention-cache-not-search-layer` — governs the Phase 5 kernel
  (a derived index over the spec corpus itself).
- `fixture-fixes-correct-bugs-not-difficulty` — when a Stage 2 trial fails,
  fix fixture self-consistency bugs (id templates, schema names) but leave
  genuine model reasoning/attention gaps as findings, not patches.
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
- Stage 2 smoke test (commit `1ada8ed`): fixed two Windows-only bugs in
  `cmd_eval` — (1) `cmd[0]` was never set to the `shutil.which`-resolved path;
  (2) resolving to `claude.CMD` still isn't enough, since invoking the shim
  routes through cmd.exe and mangles `--permission-mode acceptEdits` /
  `Bash(git:*)`. Now resolves to `claude-code/bin/claude.exe` directly. Also
  fixed the vat-quarter-basic id-template mismatch (`vat-return-[YYYY-MM]-to-[MM]`).
  Decided NOT to fix the `linked_things` vs `relations` gap — see
  `fixture-fixes-correct-bugs-not-difficulty`.
