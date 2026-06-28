---
id: mechanical-coherence-checks-backlog
type: plan
status: not-started
version: 1.0
created: 2026-06-27
priority: low
tags: [coherence, floor, drift, tooling, backlog]
linked_things:
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: implements
    notes: "Each check here is a prose-mirror-of-a-mechanical-fact that has drifted ≥2x"
  - id: prose-references-are-mechanically-checkable
    relation: implements
---

# Mechanical Coherence Checks Backlog

Small, deferred floor checks — each a generated-artifact freshness or
prose↔mechanical consistency check that belongs in `mdllm coherence`. Migrated from
continuity Open Threads on its retirement (`dissolve-continuity-into-reconciliation`).

- ~~Stale-WORKLOG freshness check~~ **— moot (resolved by deletion, v3.17).** The
  committed WORKLOG is retired; with no generated-and-committed file there is nothing
  to drift, so the check is unnecessary. The cleaner fix was to delete the duplicate,
  not police it.
- ~~framework-map subcommand count → mechanical check~~ **— done (v3.17.1).** The
  map's subcommand count had drifted twice by hand; `coherence` now compares the map's
  stated count against the live CLI surface (retrospective 06d rec #2).
- ~~Retired-vocabulary reappearance check~~ **— built (v3.17.2) then reverted (v3.17.3).**
  `retired_terms` in `_schema.yaml` + a `coherence` Warning flagged live occurrences of a
  retired name. Removed because it could only stay quiet via a hand-maintained `allow`
  list — judgement in mechanical clothing, with a *silent-failure* surface (an over-broad
  suppression hides real drift, the exact failure `existence-is-not-currency` warns of).
  The retire/rename case is irreducibly semantic, so it stays the human Walk's. Replaced
  by an explicit full-corpus pointer in `change-reconciliation.md` (an inflection walks
  every file, the insight corpus included) — same logic as retiring WORKLOG: delete the
  thing that needs policing, don't police it. See `judgement-checks-need-a-suppression-list-which-is-itself-drift`.
- **Broken-body-reference check.** A prose body reference to a thing id / spec that
  no longer resolves — the literal-tier dark-region check the indexes miss. Unlike the
  reverted retired-vocab check this needs *no* suppression list: it is keyed to the live
  id-set (same-builder), so it cannot disagree with truth — the floor-shaped version of
  the same instinct.
- **install-hook self-test.** Have `install-hook` self-test its emitted script so a
  portability break is caught at install, not at first commit
  (`portability-claims-need-execution-tests`).

Build when felt — none blocks anything today; the payoff is automatic drift
enforcement the day each fact drifts again.
