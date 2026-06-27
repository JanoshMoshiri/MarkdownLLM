---
id: framework-retrospective-2026-06d
type: retrospective
status: complete
created: 2026-06-24
period_start: 2026-06-23
period_end: 2026-06-24
domain: markdownllm-framework
linked_things:
  - id: framework-retrospective-2026-06c
    relation: references
    notes: "Prior retrospective; covered the v3.15.0 build through commit a21513b. This covers the deployment harvest and the terminal-dependency gate that landed after it, plus the doc reconciliation that closed the gap."
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: references
  - id: hard-invariants-encode-a-semantic-assumption
    relation: references
  - id: prose-references-are-mechanically-checkable
    relation: references
  - id: mechanical-assimilation-is-blind-to-prose-dependencies
    relation: references
---

# MarkdownLLM Framework Retrospective — v3.15.0 Deployment + Gate (the arc after the build)

A reconciliation-driven retrospective. Yesterday's `framework-retrospective-2026-06c`
closed at the *build* (commit `a21513b`) — but v3.15.0 kept moving: the hooks were
self-hosted and deployed, `scaffold` learned to write `.claude/settings.json`, and
today a floor gate landed. This pass ran a full change-reconciliation sweep over
everything since the build retrospective and fixed the downstream doc drift it found.
Version folds into the unreleased 3.15.0 (no tag exists yet).

## What This Covers

- **Deployment harvest (2026-06-23/24):** framework self-hosts its `SessionStart` +
  `PostToolUse` hooks; `scaffold` writes the adapter so new domains are born hardened
  (`94b0af2`); framework-root-is-not-a-stale-domain fix (`2b315e8`); insights
  `agents-cannot-self-install-permission-bearing-hooks` and
  `prose-references-are-mechanically-checkable`.
- **Terminal-dependency gate (2026-06-24):** `validate` blocks a terminal-status thing
  that depends on unfinished work (`8d3574e`); insight
  `hard-invariants-encode-a-semantic-assumption` (`be13ceb`).
- **Doc reconciliation (this pass):** `framework-map`, `domain-refresh`, `CHANGELOG`,
  `operator-guide`, `first-hour`, `README`.

## What Worked

- **The gate shipped clean and minimal.** `detect-conflicts` rule #1 became a state
  invariant — no diff machinery, ~12 lines in the existing cross-reference loop, 0
  false positives across all corpora. The mechanical half of conflict-detection was
  sitting in plain sight; mechanising it cost almost nothing.
- **Change-reconciliation earned its keep — again.** The scan caught real drift the
  floor is blind to: `framework-map`'s subcommand count stuck at 15 (actual 17,
  missing `domain-kernel` + `session-start`), `domain-refresh` missing the operator
  paste-step entirely, and a stale kernel token figure in the README (~1.6k → ~2.1k).
  All prose-dark-region drift — exactly the class
  `mechanical-assimilation-is-blind-to-prose-dependencies` names.
- **The self-install guard reshaped the deployment story correctly.** Discovering that
  an agent *cannot* write `.claude/settings.json` (permission-bearing → self-modification
  guard) turned the refresh path from "agent updates files" into "agent surfaces a
  one-time operator paste" — now documented in `domain-refresh`, `first-hour`, and the
  README rather than left as tribal knowledge.
- **The design tension got named, not papered over.** The gate freezes the
  prerequisite reading of `dependencies`; rather than hide that, `hard-invariants-encode-a-semantic-assumption`
  captures it, with the principled response (remodel onto `linked_things`; reserve a
  schema escape for the honest-but-too-strict case) written into `thing.md` at the field.

## What Didn't Work / Still Open

- **Doc drift accumulated silently between the build retrospective and now.** The build
  retro declared "clean," but deployment work generates downstream doc obligations a
  *build* retrospective doesn't capture. The lesson: reconcile docs as part of
  deployment, not as a later sweep.
- **Still no live-domain test** (carried from `06c`) — the behavioural proof that the
  `SessionStart` injection actually changes weak-model behaviour. Mechanically proven;
  behaviourally unproven. Still the cheapest high-value next step.
- **PreToolUse untouched** — deliberate, the agreed next build.
- **The cascade helper is scoped but unbuilt.** The mechanical downstream-set gathering
  for `cascade-completion` was deliberately deferred — the operator is weighing it
  against overengineering. The gate shipped alone, as intended.

## Patterns We Noticed

- **Mechanisation creates a doc-reconciliation debt.** Every time a behaviour moves from
  interpretation to mechanism (scaffold writes settings.json; validate gains the gate),
  the prose describing the old division drifts. The floor cannot see prose drift; only
  the edge-walk removes it. The `framework-map` subcommand count has now drifted this way
  more than once — it is the repeat offender.
- **A hard invariant is a semantic claim in mechanical clothing.** The deeper pattern of
  the period: hardening a rule is also freezing one reading of the data, universally and
  unoverridably — a good trade when the field has one honest meaning, a trap when it is
  overloaded. The discipline is to point false-positives at the right remodel.

## What Should Change

- **Make the `framework-map` subcommand count mechanically checkable.** `coherence`
  already guards kernel/index drift; the `mdllm --help` count is a natural next dark-region
  check, and `prose-references-are-mechanically-checkable` points the same direction. This
  is the recurring drift; it has earned a mechanical guard.
- **Fold doc reconciliation into deployment commits**, so a build retrospective can
  truthfully claim "clean" without a follow-up sweep.

---

*Reflexive scans (2026-06-24):*

- **Validate:** 80 things (framework) + 6 + 14 (examples), **0 Errors / 0 Warnings /
  3 Info**. The Info are all the session-memory "active insight not in continuity brief"
  proxy — `consequence-is-recoverable-only-in-retrospect`,
  `long-running-tasks-lack-pre-compaction-checkpoint`, and the new
  `hard-invariants-encode-a-semantic-assumption`. Disposition: **list live** — all three
  are active design notes (two parked-deferred, one this period's), none warrant
  promote-or-dismiss; the continuity brief should pick them up at session-end.
- **Coherence:** no kernel, index, domain-kernel, catalog, or version-sentinel drift; the
  3.15.0 sentinel is in sync across `.markdownllm`, root `AGENTS.md`, and `CHANGELOG.md`.
  The only note is stable-staleness on `thing.md` + `validate.thing.md` (edited this pass)
  — judged to **remain `stable`**: a single enforced invariant and a field clarification
  do not change the specs' core contracts.
- **Conflict scan (detect-conflicts, scan mode):** swept the new insight edges against
  their neighbours. **0 new, 0 open.** `hard-invariants-encode-a-semantic-assumption`
  *complements* `consistency-is-maintained-at-change-not-by-sweeping` (distinct facets —
  *when* semantic checks run vs *what* a hard check silently asserts), correctly
  cross-linked, not contradicting.
- **Insight triage:** **31 active.** Three added across the period
  (`prose-references-are-mechanically-checkable`,
  `agents-cannot-self-install-permission-bearing-hooks`,
  `hard-invariants-encode-a-semantic-assumption`); no dismissals, no merges — the trio are
  distinct facets, cross-linked.
- **Schema coherence:** no new frontmatter fields. The gate reads existing fields
  (`status`, `dependencies`); the thing schema is unchanged.
