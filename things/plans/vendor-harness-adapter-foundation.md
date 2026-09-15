---
id: vendor-harness-adapter-foundation
type: plan
status: in-progress
version: 1.36
created: 2026-08-11
priority: high
tags: [harness, adapters, codex, claude-code, diagnostics, portability, clean-architecture]
linked_things:
  - id: orchestration-specification
    relation: implements
    notes: "Owns the optional harness-session hardening above the interpretation and git-fs floor."
  - id: framework-discovery-specification
    relation: extends
    notes: "Separates entry discovery, framework discovery and optional lifecycle delivery."
  - id: domain-refresh-specification
    relation: extends
    notes: "Existing projections refresh through inspected, managed fragments rather than replacement."
  - id: hook-enforcement-has-three-anchors
    relation: implements
    notes: "Adapters may move an action to the harness-session anchor without becoming the portable substrate."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "Every verified row remains bound to an exact product surface and execution record."
  - id: installation-is-not-activation
    relation: references
    notes: "Keeps distribution, trust activation and live execution as separate rollout facts."
  - id: a-generated-contract-change-is-an-estate-migration
    relation: references
    notes: "Generated adapter and entry-contract changes adopt per domain; they are never a silent estate rewrite."
  - id: an-injected-file-arrives-without-its-frontmatter
    relation: references
    notes: "Anything required at t=0 belongs in delivered body content, not entry frontmatter."
  - id: protecting-one-budget-displaces-the-failure-into-the-other
    relation: references
    notes: "Both time and character envelopes receive explicit protected allocations."
  - id: harness-capability-evidence-matrix-2026-08-20
    relation: references
    notes: "Forward-readable capability boundary over the committed Claude, Codex and Cowork evidence."
  - id: claude-phase6-no-adapter-and-root-2026-08-16
    relation: references
  - id: claude-no-adapter-entry-probe-2026-08-17
    relation: references
  - id: codex-phase6-post-6r-acceptance-2026-08-16
    relation: references
  - id: codex-gate-7-0b-qms-operator-acceptance-2026-08-18
    relation: references
---

# Vendor Harness Adapter Foundation

## Current purpose

The shared adapter boundary is built. This plan remains open only for the
operator-owned rollout decision and its deliberate version/release act. The
long amendment narrative that previously lived here is preserved in Git; the
stable execution records and the
[`harness-capability-evidence-matrix-2026-08-20`](../../evidence/harness-capability-evidence-matrix-2026-08-20.md)
are the forward route into the evidence.

Historical body at the compaction boundary:
`git show 27b95e7:things/plans/vendor-harness-adapter-foundation.md`.

## Settled architecture

- `AGENTS.md` is the canonical entry contract. Core entry pointers survive
  `--harness none`; an adapter is optional lifecycle hardening, never
  Definition Zero.
- The application owns lifecycle intent, ordering, time/output envelopes,
  attestations and diagnostics. Harness adapters own only rendering,
  inspection and product-specific evidence extraction.
- Claude Code and Codex are project-bound projections. A run-time-bound
  adapter may render an account-level bundle and no project file; Cowork is
  that exercised third shape.
- Runtime resolution, launch policy and lifecycle execution have one neutral
  owner. Nested workspaces and managed Windows shells use the same resolved
  route as framework-root sessions.
- Adapter installation is an explicit, inspected mutation. Known legacy
  fragments can be refreshed; extensions, overlays and ambiguity refuse.
- Configuration presence, trust, currency, launchability, execution and the
  Git floor are independent diagnostic facts.
- SessionStart output is bounded structurally with protected per-step shares.
  Git pre-commit remains the enforcement boundary; post-write feedback stays
  advisory.
- Publication and estate freshness are floor services, not adapter powers.
  Sync is bounded and ff-only; divergence is surfaced, never resolved.

## Completed gates

| Gate | State | Durable consequence |
|---|---|---|
| Vendor-neutral prose and baseline | complete | Canonical specs address the agent; Claude golden artifacts froze the existing behavior |
| Shared runtime and port design | complete | Root/nested launch resolution, narrow ports, registry and architecture fitness tests |
| Claude extraction | complete | Managed Claude projection preserved and migration-aware |
| Diagnostics and Codex adapter | complete | Independent capability facts plus project `.codex/hooks.json` rendering/inspection |
| Explicit install and scaffold selection | complete | `claude-code`, `codex`, `all`, `none`, and run-time-bound registration through one service |
| Runtime repair (5R) | complete | Neutral runner, protected deadlines, execution-tested PowerShell/POSIX launch and recognised legacy refresh |
| Output repair (6R) | complete | Structural compaction retains every section inside the lifecycle envelope |
| Live Phase 6 | complete on named surfaces | Claude Code CLI 2.1.229/2.1.233 and Codex CLI 0.147.0 records; Codex Desktop 26.803.10989.0 remains a narrow negative |
| Manual runtime/Git authority (7.0a/b) | complete | Nested wrapper parity and strict `estate-sync --require-fresh` approval routing |
| Public-surface reconciliation | complete | Discovery, orchestration, refresh, guides, scaffold and framework map use the same boundary vocabulary |

The exact builds, grades and exclusions are in the capability matrix. A
deterministic test is implementation evidence; only a real product event earns
a compatibility claim.

## Phase 8 — rollout and release decision (operator-owned)

- [x] **Decide the harness default.** *Ruled 2026-09-15
  (`scaffold-harness-is-an-explicit-selection-2026-09-15`): omission no
  longer selects the historical Claude compatibility default. `scaffold`
  asks — a selection from the registered list when a human is at the
  keyboard, a refusal that prints the list when nobody is. The build is a
  floor change under code-architect's skills, sequenced before the release
  in the third box; until it lands the shipped default does not change.*
  - [ ] Build: the prompt, the non-interactive refusal, tests for both, and
    the `--harness` help text inverted.
- [ ] **Offer existing domains an opt-in `doctor` plus managed-fragment
  diff.** Do not batch-install permission-bearing project configuration.
  *Surveyed 2026-09-15: thirteen of the fourteen domains on this clone
  report `currency=stale` for both the Claude Code and Codex managed
  fragments (one is current). The owned diff, as `adapter-install
  --dry-run` shows it, is the same everywhere: the launcher probe gains
  existence guards (`-x`, `command -v`) before probing a candidate Python,
  and the fragment hash moves with it. Both fragments are tracked files, so
  each refresh is one commit in that domain's repo, autopushed, after which
  Claude Code re-asks the human to approve the project hooks on the next
  session there — the human-observed trust the doctor line names. The
  opt-in is per domain; a pass that runs domain by domain with each diff
  shown is not a batch install. Awaiting the operator's word: run the pass
  now, or leave each domain to adopt at its next refresh.*
- [ ] Version and changelog the settled decision, then perform the deliberate
  framework release/publish act. Root `autopush: false` remains controlling.

## Completion criteria

- Core entry plus Git floor works with no lifecycle adapter.
- Adding a harness adds an adapter, tests and truthful documentation—not a
  vendor conditional in neutral services.
- Live claims name the exact harness surface, build and evidence that earned
  them; Desktop/CLI and Claude/Copilot are not conflated.
- Runtime launch, sync, validation and publication each have one owner.
- The operator selects rollout and release scope explicitly.

## Outside this plan

- Repackaging domain skills as product-native skills or building a universal
  hook DSL.
- Automatically interpreting project trust or installing permission-bearing
  configuration.
- Claiming untested operating systems, products or lifecycle sources.
- Cowork local/stale-bundle acceptance, owned by `cowork-adapter`.
