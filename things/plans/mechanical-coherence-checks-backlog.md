---
id: mechanical-coherence-checks-backlog
type: plan
status: in-progress
version: 1.6
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
  - id: an-advisory-is-scoped-by-who-can-perform-its-remedy
    relation: implements
    notes: "The standing scoping test every advisory in this backlog must pass before shipping — population is 'everything that can still reach the right state', never 'everything currently in the wrong one'."
  - id: a-check-run-where-it-cannot-see-mints-a-false-finding
    relation: references
    notes: "The reading-discipline half of this backlog's null-result and INCOMPLETE-conflation items: tool-side fixes live here, but the environment question before the content question stays the reader's."
---

# Mechanical Coherence Checks Backlog

> Status corrected to `in-progress` at the 08c retrospective (2026-08-27):
> floor-sprint-3 (2026-08-23) shipped four items from this backlog — two
> review-9 promotions, the perimeter currency check, the boundary-term audit
> leg — while the frontmatter still said `not-started`. That is the
> tracking-drift class this backlog itself polices, standing in its own
> header. Open items remain: broken-body-reference, install-hook self-test,
> the primitive sweep, the skills-directory-vs-artifacts check.
>
> Structural-pin resolution shipped 2026-08-28 (see the item below); the
> evidence that promoted it was five hand-catches in three days, not the two
> the item was filed on.
>
> The operating-layer vocabulary check shipped the same day, off five
> hand-caught operating-layer defects in three domains — an item that was
> never filed here, because the class was assumed to be judgement-shaped until
> the instances showed three of the five keyed to a declared authority. The
> skill-age Info this backlog was asked to host was declined in the same pass,
> with its lifting condition; both entries are below.

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
- **Workflow-stage vocabulary in skills (added 2026-08-30, routed by
  `operating-layer-staleness-review-2026-08-30`).** The skill-vocabulary check
  keys skills to `_schema.yaml` and the reserved sets — but not to
  workflow-definition `stages`. A domain whose skills instruct stages by name
  (one regulated domain carries five per-stage skills) gets no check that
  those names match the definition's declared stage ids: rename a stage and
  every instructing skill drifts silently, exactly where workflow-driven
  operation concentrates change. Same-builder shaped: stage ids are declared
  data in the definition's own frontmatter, the skill text is scannable, and
  no suppression list is conceivable — a stage name a skill instructs either
  is in the governing definition's declared set or is not. Scoping test:
  the remedy ("rename the stage reference in the skill") is executable by the
  domain that owns both files; population is live skills only.
> **Standing scoping test for every item below (added 2026-08-26).** Before
> shipping any advisory here, write its remedy as an imperative and ask who
> must execute it; if the population includes things that are finished or
> frozen, scope the population down or rewrite the remedy
> (`an-advisory-is-scoped-by-who-can-perform-its-remedy`). The seams sprint
> shipped one cue that failed this test and one that passed it, in the same
> file, on the same day.

- ~~**Structural-pin resolution at the commit boundary (added 2026-08-26, felt —
  twice in one sprint).**~~ **Built 2026-08-28** — `structural_pin_findings`
  (`tools/markdownllm/structural_pins.py`), joined to `validate_corpus`, so it
  runs on the pre-commit `validate --view index` leg against the frozen
  candidate and on every example corpus. **Five instances promoted it, not
  two:** the two the item was filed on (2026-08-26 — the run's `informed_by`
  pin with a wrong tail, caught by hand the same day; the design's
  `informed_by` pin naming a nonexistent commit, which survived five commits
  before the builder caught it at reconcile), plus at least three more on
  2026-08-28, every one caught by hand or narrowly before the commit. A class
  that reaches five hand-catches in three days is not being caught by
  diligence; it is being caught by luck.

  Three design points worth carrying:

  1. **`source_commit` was scoped OUT, and that is the check working.** The
     first run fired on `divergence-is-an-unrouted-decision`, whose
     `source_commit: bd8fc48` names a commit in the **code-architect domain's**
     repository — where it resolves cleanly. Resolving a foreign pin against
     the local object database reports "missing" for a *correct* pin, and its
     remedy written as an imperative — "re-pin to a local commit" — is one no
     honest author could perform. That is this backlog's own standing scoping
     test, and the INCOMPLETE-bucket conflation the skills-directory item names
     (*unpinnable by design* vs *defectively unpinned*), met in the first hour.
     `mdllm imports-check` keeps that resolution.
  2. **The registry states the pin set once.** `structural_refs.py` now
     declares every commit-bearing field with its scope and its resolving
     owner, so the check cannot drift from the fields that exist and
     `definition_commit` (already resolved by the workflow revision binding) is
     recorded rather than silently omitted — one wrong pin cannot yield two
     Errors saying the same thing.
  3. **`git cat-file --batch-check`, not a literal batched `rev-parse`.** The
     one-process constraint holds either way, but rev-parse over many revisions
     aborts at the first unresolvable argument and never reports the rest — a
     corpus with three bad pins would have surfaced one. `--batch-check` emits
     one answer line per input line and exits 0 whatever it finds. The
     degradation is honest: where git cannot be consulted the check says it
     could not look (Warning), and a corpus declaring no pin is silent either
     way.

  The cost the design accepts, recorded at build time rather than discovered
  later: a history rewrite re-hashes every commit, invalidating every pin in
  the corpus at once — terminal things included — and the floor then blocks
  until each is re-pinned. The remedy stays performable on a terminal thing (a
  pin is a factual reference, not a state claim — you look the commit up and
  correct it), which is what keeps this inside the standing scoping test. A
  check that stayed quiet after a rewrite would be asserting a traceability
  the repository no longer has.

  One live defect found: `examples/life-manager` taught the provenance rule
  with a **fabricated** 40-hex pin, while its own body asserted "the commit
  must exist". Re-pinned to the real commit that carries the input. Example
  corpora were never reached by `mdllm provenance` (they are excluded from its
  corpus walk), which is why a teaching fixture could contradict its own
  lesson for eleven weeks.

  Original item, for the record: Every structural pin is a full SHA a human may
  transcribe, and the seams sprint mistranscribed two in two days.
  `definition_commit` is now floor-resolved at
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

- ~~**Skill-age-vs-domain-velocity Info** (routed here by
  `operating-layer-quality-loop`, 2026-08-18).~~ **Declined 2026-08-28, and
  replaced by a sharper check in the same sprint.** The proposal was: a skill
  untouched since its birth commit while `things/` moved N commits. It passes
  the suppression-list gate (pure git) but fails on the *other* standing
  hazard: measured across the estate, at threshold 25 it fires on 12 of 58
  skills at every commit forever, and one specification skill sitting 142
  `things/` commits behind its last touch would never go quiet again. A
  git-derived pin has no way to record "walked, still correct" — the same
  limitation the perimeter currency check accepted for four files at *release*
  cadence, which is a different bargain from a fifth of every domain's
  operating layer at *commit* cadence
  (`a-check-that-always-fires-teaches-the-operator-to-ignore-it`). The signal
  was re-homed rather than dropped: `retrospective.md` → When To Write One now
  carries it as a trigger, where recurrence is the agenda. **Lift when** a
  skill acquires an honest "walked, still current" marker that is not itself a
  hand-maintained surface, or when the retrospective trigger is observed being
  ignored.

- ~~**Operating-layer vocabulary drift (added and built 2026-08-28, felt —
  five hand-catches in three domains in one day).**~~ **Built 2026-08-28** —
  `skill_vocabulary_findings` (`tools/markdownllm/skill_vocabulary.py`),
  joined to `coherence_findings` in the corpus-general section, so every
  domain inherits it through the same pre-commit hook. A skill or entry file
  that instructs a thing type, a status value, or a frontmatter field the
  corpus never declared is naming an instruction whose product the floor
  rejects; Warning severity, one class, one severity.

  Why it passes this backlog's gate where the retired-vocabulary check did
  not: it is keyed to `_schema.yaml`, the tool's reserved sets, and
  `CORE_FIELDS` — the same builder it polices. The skill is *prose about* the
  schema, so no allow-list exists or could: the only way to quiet a finding is
  to make the two agree. And it passes the standing scoping test by scoping
  the population — `deprecated` skills are out (instructions withdrawn),
  `draft` skills are in (the archetype defect was `draft` and read daily), and
  generated managed blocks are stripped before reading so no finding can name
  a remedy that belongs to a generator.

  Three design points worth carrying:

  1. **Precision was bought at the price of recall, deliberately.** Only
     three positions count as an instruction — a frontmatter template inside a
     fenced block, a heading/list-step/table-cell naming a type, and a
     `status`/**Key fields** list beneath one. Inline prose that *mentions* a
     type is never a finding, and a parenthetical never is: `(e.g.,
     \`type: migration-plan\`)` is correct writing about a type that need not
     exist, and it was the estate's one would-be false positive.
  2. **Every leg stays silent where the corpus declares no authority.** No
     types declared, no `known_fields` registered (field registration is
     opt-in and this check inherits that), or a type whose statuses are the
     universal default — each is "could not look", not "nothing wrong".
  3. **`valid_statuses_for` moved into `model.py`** beside
     `terminal_statuses_for`, so the vocabulary authority has one definition
     and two readers. A second copy in the coherence module would have been
     this backlog's own restatement class, introduced by the check meant to
     end it.

  First run across the estate: three domains, ten findings — including one
  no hand pass had found (a write skill's supplier frontmatter template
  instructing `status: active` while the schema declares the universal
  vocabulary). Replayed against the pre-fix blobs it reproduces the promoting
  evidence exactly: the 13 unregistered fields, the four contradicted status
  vocabularies with `income-record` first, and the six undeclared types.

  Two of the five 2026-08-28 instances are **out of scope and stay open**: a
  skill instructing a `linked_things` edge to a framework spec id, and a skill
  instructing a commit of a file the domain deleted. Both are reference drift,
  not vocabulary drift — the broken-body-reference item above is their home.

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
