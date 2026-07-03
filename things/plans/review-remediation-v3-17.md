---
id: review-remediation-v3-17
type: plan
status: completed
version: 1.0
created: 2026-07-02
session: 2026-07-02
priority: high
tags: [remediation, reviews, drift, egress, triggers, docs]
linked_things:
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: implements
    notes: "Item 1 is the predicted failure realised; its regression test cross-checks emitted subcommands against the parser registry — a different artifact, so the blindness breaks"
  - id: a-crossing-thing-carries-its-producers-private-graph
    relation: implements
    notes: "Item 2 applies the insight's own rule to the two relational fields it missed"
  - id: directional-graph-reads-come-in-inbound-outbound-pairs
    relation: implements
    notes: "Item 6 adds the missing mirror direction to the TIERS<->catalog check"
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: implements
    notes: "Item 4 is the third strike on the kernel token figure; resolution is deletion of the duplicates, not a police check (WORKLOG precedent)"
---

# Review Remediation — v3.17.3 Findings (Reviews 5 + 6)

**Completed 2026-07-03, shipped as v3.17.4** — all twelve items, ten
commits, five new floor tests (102 total). The deferred list below is
still live; the stopping-rule recommendation still awaits the operator's
decision (queued for evidence session 1).

The combined mechanical queue from the fifth review (2026-07-02, committed b940f82)
and the sixth (Cowork sitting, committed 3b8d469). All twelve items verified against
HEAD before this plan was written. Agent-executable in full — no operator gate.
Each item: fix + test where floor-shaped + its own commit.

## Tool fixes (tools/mdllm.py)

- [x] **1. Phantom `mdllm orient`.** `_dk_session_start` (≈:1908) emits
  "`mdllm session-start` / `mdllm orient`"; no `orient` subcommand exists. Fix the
  builder; add a regression test that every `` `mdllm <word>` `` token emitted by the
  `_dk_*` builders resolves against the live parser registry — registry and prose are
  different artifacts, so this test sees what the same-builder drift check cannot.
- [x] **2. MCP egress leak.** Add `informed_by` and `parties` to
  `_MCP_INTERNAL_GRAPH` (≈:2818); both carry producer-local ids across the boundary.
  Update the bright-line comment; test that an egressed decision/conflict ships neither.
- [x] **3. Silent relationship-trigger skip.** `cmd_triggers` evaluates
  time/dependency/threshold and reports `blocked_duration` as not mechanically
  evaluable, but `type: relationship` falls through with no output line. Give it the
  honest "needs event history — left to the agent" line in the skipped section; test.
- [x] **5. `stale` trigger reads mtime, not git.** (Fifth review.) mtime is wrong
  across clones and touched files; use last git commit date for the file, mtime as
  fallback when git is unavailable. Note: this is also the live half of the
  thing-lifecycle.md contradiction (its `last_active`-from-git definition).
- [x] **6. Reverse TIERS check.** Coherence verifies catalog→TIERS only; add
  TIERS→catalog. It will fire once: `thing-lifecycle.md` is in Tier 2 but not in
  `.markdownllm`. Disposition: remove it from TIERS — it is a draft rotting against
  the live tool (fifth review) and does not belong in the loading map until
  reconciled. Its reconciliation is a separate, judgement-shaped piece of work.

## Prose / docs

- [x] **4. Kernel token figure, third strike.** Live figure is 2,077 (`mdllm tokens`);
  ~1.6k survives in AGENTS.md:79, framework-discovery.md:89,
  domain-specification-guide.md:277 and :777. Per the three-strike razor this promotes
  to the floor — but a prose-figure check needs pattern judgement (suppression-list
  smell), so apply the WORKLOG precedent instead: **delete the duplicates, don't police
  them.** The figure lives once (README, already corrected); every other site points at
  `mdllm tokens`.
- [x] **7. Duplicate birth path.** domain-specification-guide.md Step 1 (≈:627) still
  teaches manual `mkdir` + `git init`; the eval data says agents drop mechanical birth
  steps when hand-rolling. Route Step 1 through `mdllm scaffold`; one birth path.
- [x] **8. Stale CONTRIBUTING.** (Fifth review.) Refresh, including its third manual
  birth variant — same single-path rule as item 7.
- [x] **9. git-workflow "Three Layers" heading** over two-layer text. (Fifth review.)
- [x] **10. session-memory live-voice continuity-brief reference.** (Fifth review;
  continuity.md is retired — the live voice must not still teach it.)
- [x] **11. workflow-definition template `instance-of` residue**, plus the surviving
  body instance in examples/life-manager/home-renovation-process.md. (Fifth review +
  sixth's addendum.)
- [x] **12. Examples pinned at 3.4.0.** Refresh examples to v3.17 shape; add the
  example-staleness coherence check (compare example `framework_version_seen` against
  `.markdownllm` version — same-builder, no suppression list, so it qualifies).

## Explicitly deferred (not lost)

- thing-lifecycle.md reconciliation with the live tool — judgement work, own session.
- Obsidian vault claim execution test (`portability-claims-need-execution-tests`) —
  belongs with the evidence pass, see `evidence-and-eval-backlog`.
- Root-AGENTS.md kernel question + razor index — one decision, flagged for the
  operator in `evidence-and-eval-backlog`'s session agenda.

## Recommendation carried from both reviews

Adopt the stopping rule: no further internal full reviews until the longitudinal
eval, a second human reader, or a second harness exists. Recorded here as a
*recommendation* — it becomes a decision thing only when the operator makes it.
