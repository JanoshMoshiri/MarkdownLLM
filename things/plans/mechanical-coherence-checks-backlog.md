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
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: references
    notes: "The gate for what belongs here: keep checks keyed to a same-builder source (count, broken-body-ref); reject ones that need a suppression list (the reverted retired-vocab check)."
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
- ~~Disclosure-boundary check~~ **— shipped as its own plan (v3.20.0,
  `boundary-disclosure-check`).** Commit messages and staged content checked against a
  LOCAL, never-committed terms file; `install-hook` grew the commit-msg hook that
  pre-commit structurally cannot be. Passes this backlog's suppression-list gate for
  the opposite reason the retired-vocab check failed it: the local file is not an
  allow-list keeping a truth-check quiet — it *is* the check's entire subject,
  operator-owned, and an omission fails open for that term only without ever
  falsifying corpus state.
- **Broken-body-reference check.** A prose body reference to a thing id / spec that
  no longer resolves — the literal-tier dark-region check the indexes miss. Unlike the
  reverted retired-vocab check this needs *no* suppression list: it is keyed to the live
  id-set (same-builder), so it cannot disagree with truth — the floor-shaped version of
  the same instinct.
- **install-hook self-test.** Have `install-hook` self-test its emitted script so a
  portability break is caught at install, not at first commit
  (`portability-claims-need-execution-tests`).
- **The primitive sweep — null-result instance first.** Upstream ask from an
  operating domain's porch (2026-08-06,
  `a-primitive-is-known-once-and-must-be-found-again-at-every-site`): a named
  primitive currently waits to be re-felt at every site it applies to — one
  primitive was recorded in July and violated twice in the substrate's own
  code by August, both caught by use, neither by review. The candidate
  instrument takes a *stated primitive* as input (the currency sweep takes a
  version) and returns candidate sites, not drift. For the null-result
  primitive the question is mechanical enough to state: every function that
  can return an empty or default result — does it distinguish "nothing found"
  from "could not look"? Gate check before building: the general sweep is
  judgement-shaped (which primitives? which sites count?) and may fail this
  backlog's suppression-list test; the null-result instance may pass it as a
  bounded static check. The two immediate sites the ask named were fixed at
  the ask (2026-08-06: `_classify_fetch_failure` undiagnosed state,
  `_where_you_left_off` stated search); the ask's dismissal condition is the
  instrument, not the fixes.

- **Skills-directory-vs-artifacts check (added 2026-08-08, three instances in
  one day).** A domain kernel's Skills Directory claiming "unfilled stubs — the
  framework defaults apply" while all four skill files sit authored at
  `stable v2.0` — found in two domains of the regulated deployment, plus a
  third whose directory carried scaffold-generic one-liners against authored
  skills. Load-bearing in the worst direction: a session trusting the kernel
  rationally *skips* the files carrying the domain's conventions, which is
  behaviourally indistinguishable from the harness breach the estate just
  rectified (and the QMS domain hit the inverse — kernel advertising authored
  skills over byte-identical templates — on 31/07). The mechanical shape is
  same-builder and needs no suppression list: a skill file byte-identical to
  its shipped template (or still carrying the template's placeholder
  description) is *mechanically* a stub; a kernel section saying "unfilled"
  over non-template skills, or authored-sounding descriptions over template
  bodies, is checkable drift either way. Candidate home: `mdllm coherence`,
  domain scope. Fired-when-found instances: engineering `4a3fea4`, overview
  and development same-day commits; also add the check to `imports-check`'s
  cousin question — the INCOMPLETE bucket conflating *unpinnable by design*
  with *defectively unpinned* (cowork-integrity-estate-sweep Phase 10 residue)
  belongs in this backlog under the same same-builder gate.

Build when felt — none blocks anything today; the payoff is automatic drift
enforcement the day each fact drifts again.
