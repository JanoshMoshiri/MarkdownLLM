---
id: mechanical-coherence-checks-backlog
type: plan
status: not-started
version: 1.2
created: 2026-06-27
priority: high
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
  - id: a-control-that-must-stay-local-has-no-floor
    relation: implements
    notes: "The boundary-term evidence check below is that insight's escape route made concrete: the floor cannot own a list that must never be committed, but it can own an invariant over it."
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: references
    notes: "The reading-discipline half of this backlog's null-result and INCOMPLETE-conflation items: tool-side fixes live here, but the environment question before the content question stays the reader's."
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
- **Structural-pin resolution at the commit boundary (added 2026-08-26, felt —
  twice in one sprint).** Every structural pin is a full SHA a human may
  transcribe, and the seams sprint mistranscribed two in two days: the run's
  `informed_by` pin (wrong tail, caught by hand the same day) and the design's
  `informed_by` pin (nonexistent commit, caught by the builder at reconcile —
  it survived five commits). `definition_commit` is now floor-resolved at
  validation; `informed_by` commits are resolved only when `mdllm provenance`
  is run on demand, so the hook path accepts a pin that names no commit.
  Candidate: resolve every structural pin's commit against the frozen candidate
  at pre-commit (one batched `rev-parse`; Error on no-such-commit). Keyed to
  git itself — same-builder, no suppression list possible. Evidence:
  `a-transcribed-identifier-is-unverifiable-by-reading` (promoted), and the
  seams verification record.
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

- **Review-9 survivor promotions (added 2026-08-11, priority driver).** Every
  one of the ninth review's seven survivors was a hand-restated mirror of a
  same-builder fact — the trigger-type count, the reserved set, the
  index-signal count, the `CORE_FIELDS` admission criterion. Each passes this
  backlog's gate for the same reason the framework-map count did: keyed to a
  tool constant, no suppression list, cannot disagree with truth. Promote each
  into `mdllm coherence` so the *next* drift of the same fact is caught at the
  commit boundary instead of by a cold read. The external assessment's verdict
  (`reviews/REVIEW-external-2026-08-10.md`, R1): this class produced the entire
  survivor list; the restatement is the unit of future drift.

  **Two promoted, two declined — 2026-08-23, floor-sprint-3 (`9ab0820`).**
  Built: the `CORE_FIELDS` admission criterion, caught from the inside (a
  `known_fields` entry already universal is a redundant registration), and
  the index-signal count, keyed to `INDEX_FILES`. The second caught two live
  instances the ninth review's own fix pass missed — `AGENTS.md`'s catalog
  entry and `git-workflow.md`'s velocity paragraph both still omitted
  `provenance`, nine weeks after the review that believed it had fixed all
  five surfaces. Declined, each with its lifting condition: the
  **trigger-type count** has no tool-owned authority to key to (the
  evaluator dispatches on a chain of `elif ttype ==` branches, so a
  constant introduced for the check would itself be a restatement — lift
  when the dispatch reads a declared set), and the **reserved-set
  restatements** fail this backlog's own gate, because a sentence naming two
  reserved types is ordinary prose rather than an enumeration and the shape
  that works for four signals produces noise across thirteen types. That is
  the retired-vocabulary judgement repeated, deliberately.

- ~~**Perimeter currency check (added 2026-08-11).**~~ **Built 2026-08-23**
  (floor-sprint-3, `57f5293`), with one design change worth carrying: the
  item below proposed comparing each surface's *version pin*. No pin was
  added. A marker would have been a new hand-maintained surface introduced
  by the very check that catches hand-maintained surfaces going stale, and
  three of the four surfaces had no honest first value anyone could supply.
  The pin is read from git instead — the sentinel version at the file's
  last-touching commit — so the check creates no surface of its own, and the
  perimeter set is derived rather than listed. Tolerance is two minors, not
  one, because a surface reconciled *during* a cycle is touched before the
  version bump lands and reads as one behind while being current.

  **Known limitation, found the day it shipped and recorded rather than
  papered over.** A derived pin has no way to record *"walked, still
  correct"*. `CLAUDE.md` fired on its first run; reading it showed 18 lines
  of pure routing with nothing version-specific to go stale, so the honest
  answer is "walked, correct" — and the only way to say so to a git-derived
  pin is to modify the file, which is the authored marker this design
  deliberately refused. The Info therefore recurs each release for any
  surface that is correct *and* rarely edited. That is a real cost, and it
  is the milder half of the trade: the alternative was a marker on every
  perimeter file, drifting. Revisit if the recurrence starts training the
  operator to ignore the line — that is the condition, not a schedule.

  Original item, for the record: A releases-behind signal for
  the surfaces outside every individual blast radius — README, `docs/first-hour.md`,
  `examples/`, `CONTRIBUTING.md`: compare each surface's version pins / stated
  facts' last reconciliation against the tool's current version and fire an
  Info at release time. Same-builder (the version is the tool's own), no
  suppression list. This is `cumulative-drift-is-invisible-to-per-change-walks`'s
  razor executed: the perimeter is protected by an interval, and the interval
  becomes mechanical (R2 of the same review).

- ~~**Boundary-term evidence check (added 2026-08-17, felt — third regression,
  now blocking).**~~ **Built 2026-08-23** as `mdllm boundary --audit-terms`
  (floor-sprint-3, `444b4d6`) — **and it found the adder within the hour.**

  This item recorded the additions as unattributed: "the additions were
  **not** made by the floor (nothing in `boundary.py` writes that file)…
  whatever adds them is unattributed and outlives the fix". The statement was
  true and the conclusion was wrong, because the search had been scoped to
  one module. `scaffold.py` registers every newborn domain's name in the
  **framework root's** terms file — private-by-default at birth, a sound
  intent — but it resolves the framework root from the *running tool's own
  checkout*, not from the target's context. So every scaffold anywhere on
  the machine appended to this repo's operator-owned control file, the test
  suite included, permanently.

  Why it stayed hidden: `test_scaffold_harness_selection.py` already carried
  an autouse fixture restoring the terms file after each test, commented
  "Scaffold birth registers a private name; tests must leave no local
  state." One test file had found the behaviour and patched its own symptom,
  which is precisely why the remaining leaks looked sourceless.

  Fixed at the source in the same sprint (registration only when the newborn
  is nested under this framework root; a domain outside it can never be
  named by this repo's commits, so registering it buys no privacy and costs
  a permanent false positive), with a flow probe that fails against the
  unfixed tool. The audit leg then classified the standing entries without
  reading one: **all 17 appear in this repo's own tracked content and not
  one is a live domain name** — the whole class is accumulated tool output.
  Removal is the operator's, and is one `--audit-terms` run away.

  Original item, for the record: A `.boundary-terms` entry that appears in
  the repository's **own tracked
  content** is not a private identifier: either it is noise, or it is a leak
  already committed. Both outcomes are actionable, which is what makes this a
  check rather than a warning. Same-builder (the corpus is the tool's own), and
  it needs no suppression list — the property that sank the retired-vocabulary
  check — because it reads the local file *in place* and never copies, commits,
  or prints a term. Felt twice: the synthetic test vocabulary was removed
  2026-07-28 for making `boundary --history` permanently red, returned by
  2026-08-13 with a wider set of the same class, and an audit that day returned
  hundreds of hits of which every one was framework test vocabulary. The
  blocking path was simultaneously primed to falsely refuse commits touching
  `tools/tests/`. Reasoning and the escape route — why the usual
  state-once-and-derive promotion is unavailable for content that must never be
  committed, and why an *invariant over* the list is available instead — in
  `a-control-that-must-stay-local-has-no-floor`. Candidate home: `mdllm
  boundary` (a `--audit-terms` leg) rather than `coherence`, since the terms
  file is boundary's own subject and absent-file-is-a-no-op already lives there.

  **Third regression, 2026-08-18 — and the first that cost working time.**
  The same class returned and *blocked three commits in one session*: three
  synthetic scaffold-target names, each coined during that session, each
  entering the local file within minutes of first use, removed under the
  file's own documented remedy, and at least two back afterwards. (They are
  deliberately not named here: writing them into tracked content is the very
  act that would make them permanently red — the note would create the
  condition it describes. The check reads them in place, which is why the
  invariant can exist where the list cannot.) Every blocked commit touched
  `tools/tests/` only — exactly the falsely-refused path the 2026-08-13 note
  predicted, and the fourth block landed on the session-end commit for a
  *prose description of the problem*. Two further facts this instance adds:
  the additions were **not** made by the floor (nothing in `boundary.py`
  writes that file), and manual re-removal does not hold — whatever adds
  them is unattributed and outlives the fix, so the invariant has to be the
  thing that speaks, not the operator.

Build when felt — and as of 2026-08-11 the same-builder items above *are* felt:
the operator named the v3.30.x defect lump as the felt evidence commissioning
the external review, which lifts this hold for the review-9 promotions and the
perimeter currency check (`external-review-response-2026-08-10`). The remaining
items keep the original hold; the payoff is automatic drift enforcement the day
each fact drifts again.
