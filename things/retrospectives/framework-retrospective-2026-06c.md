---
id: framework-retrospective-2026-06c
type: retrospective
status: complete
created: 2026-06-23
period_start: 2026-06-19
period_end: 2026-06-23
domain: markdownllm-framework
linked_things:
  - id: framework-retrospective-2026-06b
    relation: references
    notes: "Prior retrospective; this covers the single build that opened where it closed (v3.14 → v3.15)."
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: "Operationalized this period — anchor became the primary declared axis; insight promoted."
  - id: session-start-loses-to-the-first-request
    relation: references
  - id: existence-is-not-currency
    relation: references
---

# MarkdownLLM Framework Retrospective — v3.14 → v3.15 (Domain Kernel + Harness Hardening)

A single-build retrospective, run because the build tripped the **milestone** trigger:
the entry surface stopped being hand-maintained prose and became a generated artefact,
and the framework gained its first session-lifecycle hardening. Period covers the one
session (2026-06-19 → 2026-06-23) that produced v3.15.0.

## What We Were Trying To Do

Fix a concrete, repeatedly-observed failure: domain agents skip the session-start ritual
(load kernel, version-check, velocity) — **even on Opus in Claude Code**. Diagnose the
cause, then close it without breaking the framework's portability thesis. Five phases,
all additive/opt-in: anchor-primary taxonomy → generated domain kernel → session-start
adapter → deliberate slash commands → rollout via the existing refresh rail.

## What Worked

- **The diagnosis held and reframed the fix.** The skip is structural, not a model-tier
  artefact: session-start fires with the user's first message and loses. That turned the
  fix from "better prose" into "deliver the ritual mechanically at t=0" — captured as
  `session-start-loses-to-the-first-request`.
- **The spine held: every piece was an existing discipline applied.** The domain kernel
  is the `kernel.md` generation move one level down; its drift check is the `coherence`
  kernel/index drift check generalised; the adapter is the sanctioned "hardening is
  optional, same move twice." No new primitive was invented — "the notation changed, not
  the primitives" did its gatekeeping again.
- **Generated, not hand-maintained, by construction.** The entry file's operative
  sections live in managed `<!-- generated:NAME -->` blocks regenerated from `TIERS` +
  frontmatter; authored identity outside them is preserved verbatim. Residue-free the way
  derived indexes are — which let a 5th instance of *existence ≠ currency* close that open
  question (`existence-is-not-currency`).
- **Change-reconciliation earned its keep.** The first edge-walk caught that superseding
  `session-orientation` (the plan-of-the-moment) would have orphaned `surface-attention`'s
  input and contradicted `domain-velocity`'s own "counterpart" definition. The decision
  reversed to keep-and-wire. A second pass caught a self-contradiction the taxonomy edit
  left in the kernel block header ("never skippable"). Both fixed before they shipped.
- **Durable-state protocol survived the long run.** Plan committed in-repo + per-change
  commits + a mid-flight continuity checkpoint meant the build could have resumed cleanly
  after any compaction. First real exercise of the discipline
  `long-running-tasks-lack-pre-compaction-checkpoint` named.

## What Didn't Work / Still Open

- **Not yet tested on a live domain.** Everything is verified mechanically (74 tests,
  validate + coherence clean) and proven on the `jmtm-software` example, but the
  end-to-end "open a real domain, watch the SessionStart hook inject the ritual unprompted"
  test has not run. That is the immediate next step.
- **The other domains still trail.** eco-essentials, property-ventures, code-architect are
  unmigrated to the kernel shape and on older framework versions — they absorb it via the
  `refresh` rail when next opened (felt-when-felt; `felt-deployment-lands-in-undisclosable-work`).
- **The framework's own root `AGENTS.md` (~23k) was not migrated** to kernel shape — out of
  scope this pass; a candidate if it keeps drifting.
- **PreToolUse is untouched** — deliberately. The security/risk-reasoning hooks the operator
  has in mind are the agreed next build; the foundation left PreToolUse free for them.

## Patterns We Noticed

- **The taxonomy lie was the root cause, not a footnote.** "Hard hook" implied enforcement
  the architecture never provided; the anchor was always what decided it. Making *anchor*
  the primary declared axis (and hard/soft a config flag) is the operationalization of
  `hook-enforcement-has-three-anchors` — now promoted. The same insight predicted the
  failure (interpretation-anchored "hard" hooks are skippable) before the build confirmed it.
- **Reconciliation catches what generation cannot.** The two pre-ship fixes were both
  *prose* contradictions (a dangling supersession, a stale header) invisible to the
  mechanical floor — exactly the class `mechanical-assimilation-is-blind-to-prose-dependencies`
  names. Generation removes structural residue; only the edge-walk removes semantic residue.

## What Should Change

- **Test on a live domain next, before PreToolUse.** The mechanical proof is complete; the
  behavioural proof (does a weak model actually run the injected ritual?) is the open half
  and the cheapest high-value next step.
- **Decide the domain-refresh-lag policy** — flagged for the third retrospective running.
  Either a forcing function or a stated "domains may trail by N versions" policy. The
  refresh rail now regenerates the kernel automatically, so the cost side just dropped.

## Open Questions Going Forward

- **Does the SessionStart injection actually change weak-model behaviour in practice?** The
  whole hardening rests on the hypothesis that an injected ritual at t=0 beats a buried one.
  The live-domain test is the first evidence either way.
- **Should the framework's own root `AGENTS.md` become kernel-shaped too** — i.e. is the
  framework a domain of itself for this purpose?

---

*Reflexive scans (2026-06-23):*

- **Validate:** 76 things, **0 Errors / 0 Warnings / 4 Info** across the framework corpus
  (the Info are pre-existing dead-vocabulary / stable-staleness proxies, not regressions).
- **Coherence:** **no issues found** — no kernel, index, domain-kernel, catalog, or
  version-sentinel drift; the version bump (3.14.0 → 3.15.0) is in sync across
  `.markdownllm`, root `AGENTS.md`, and `CHANGELOG.md`.
- **Conflict scan:** **0 new, 0 open.** The `session-orientation` question was resolved
  (kept + wired), not left as a held contradiction.
- **Insight triage:** 29 active. **Created 2** — `session-start-loses-to-the-first-request`
  and `existence-is-not-currency` (the latter closing the 2026-06b open question).
  **Promoted 1** — `hook-enforcement-has-three-anchors` → `orchestration-specification`
  (its claim is now the spec's primary axis). No dismissals; no merges (the new pair are
  distinct facets, correctly cross-linked).
- **Schema coherence:** no new frontmatter fields introduced; the `anchor` attribute added
  this period lives in hook *declarations* (orchestration prose / `hard_hooks`), not thing
  frontmatter, so the thing schema is unchanged.
