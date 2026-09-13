---
id: framework-retrospective-2026-09
type: retrospective
status: complete
version: 1.0
created: 2026-09-13
period_start: 2026-08-27
period_end: 2026-09-13
domain: markdownllm-framework
tags: [retrospective, cue-carrier, closed-loop, standing-authority, reconciliation, seat-protocol]
linked_things:
  - id: framework-retrospective-2026-08c
    relation: references
    notes: "Prior retrospective (the floor's floor, closing at v3.36). This covers v3.37 through the cue carrier — the arc 08c's open questions on the seat and the un-walked change pointed at."
  - id: cue-carrier
    relation: references
    notes: "The period's central build, and the reason scan 4 has an explicit, empty work list for the first time."
  - id: unattended-cue-carrier-2026-09-12
    relation: references
    notes: "The first of the two rulings the period turns on: the question persists; only a human answers."
  - id: framework-agent-closes-settled-cues-2026-09-13
    relation: references
    notes: "The second: a recorded ruling is a stated ruling; the framework agent answers by citing it. Scan 1's one contradiction was between this and the spec's older box, reconciled in this commit."
  - id: review-external-conflict-lifecycle-2026-09-08
    relation: references
    notes: "The external review whose F5 became the carrier's ruling and whose F1 wired scan 4 to the hand that casts it — this is the first retrospective to run all seven scans by that wiring."
  - id: hard-hook-vocabulary-contradicts-observable-trigger-insight
    relation: references
    notes: "The one standing conflict, held with its proposed ruling for the operator's seat — the seat this retrospective's triage produces, not bypasses."
  - id: reconciliation-candidates-are-detectable-from-the-commit-stream
    relation: implements
    notes: "Promoted by scan 6: the carrier is this insight built."
  - id: cumulative-drift-is-invisible-to-per-change-walks
    relation: implements
    notes: "Promoted by scan 6: the carrier's first reading was the second sweep its condition asked for."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: implements
    notes: "Promoted by scan 6: the exogenous stop is the dispatch prompt's mandatory input."
  - id: a-ruling-triages-more-cheaply-than-a-mechanism
    relation: implements
    notes: "Promoted by scan 6 on its third instance — the morning's one ruling that closed 28 cues."
  - id: feels-automatic-is-persistence-of-the-question
    relation: references
    notes: "The period's harvest that names the shape: persist the question, propagate the ruling, never mechanise the verdict. Read against the operator's retrospective-automation question below."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: references
    notes: "Held by scan 5 as the standing razor the retrospective-automation question must pass."
---

# Framework Retrospective — September 2026: The Question That Waits

**Period:** 2026-08-27 → 2026-09-13, the releases from 3.37.0 to 3.39.0 and
the unreleased cue carrier. **Baseline for the next period's scan 4:**
2026-09-13. **Cadence:** seventeen days — early against the 60-day domain
clock, called by the operator because the period ended on an inflection
that had already been reconciled and wanted its version.

## What We Were Trying To Do

Three things, in sequence. Ship the Explorer's last increment and then
decide what the accessible product actually is (Desktop declared, frozen
three days later, the harness-native onramp ruled in its place). Answer an
external review of the substrate's conflict lifecycle and wire the
retrospective's fourth scan to the ritual that casts it. And — the period's
real subject — close the gap the record had been naming since August:
change lands on reasoned-from things, the boundary asks *inflection?*, and
the question is printed to nobody. Build the carrier that holds the
question; rule on who may answer it; close the backlog.

## What Worked

- **Answering from the record.** The direction question of 6 September
  (Desktop or onramp) and the review verdict of 12 September were both
  answered by reading the corpus rather than by taste — five of the review's
  seven findings were already insights, dated. The second instance of
  `the-record-answers-the-direction-question-first`, inside one period.
- **The carrier, built in a day and walked against itself.** `type: cue`,
  `mdllm cues`, a digest line that waits. Twelve cues on its own commits,
  including one deliberately left open overnight — the first question the
  carrier held for a human, and the one the human's next ruling answered.
- **One ruling instead of twenty-eight verdicts.** The operator's response
  to a 27-item backlog was to rule once on *who may answer*, and every one
  of the 27 traced to four rulings already on the record. Closed by
  citation in one commit; the tail closed on itself in one more. The
  formula held: nothing added, just linked.
- **The floor refused its author twice.** A SHA transcribed from its
  abbreviation; a `raised_at` field the pin registry knew but `CORE_FIELDS`
  did not. Both caught at the boundary, both correct, both cheap.
- **The nets, stacked.** The dark-region walk found six prose enumerations
  the registries had outgrown — every one a restated list, the species the
  ninth review named. The census tests caught the new type at four seams.
  Nothing reached the operator that a check could have read.

## What Didn't Work

- **Both nets were down together, for seventeen days.** The insight that
  predicted it (`inflection-candidates-are-computable`, 4 August) was right,
  and the carrier was still five weeks away. 36 un-walked modifications on
  the first reading is the honest cost.
- **The seal has a tail.** A reconciliation pass modifies its dependants,
  and those modifications are themselves candidates; every `reconcile:`
  commit raised its own next cues until the citation link made the tail
  close in one step. Found by doing, not by design — three times.
- **A spec said two things for one day.** After the 13 September ruling,
  change-reconciliation.md's boxed rule (*the agent does not initiate from
  edit-detection; everything runs after the human "go"*) and its new
  who-answers paragraph disagreed. Scan 1 found it on the decision's own
  `extends` edge; reconciled in this commit (v1.4). One day is what the
  scan is for.
- **The commit vocabulary lagged practice by ten prefixes.** `decide`,
  `plan`, `reconcile`, `fix`, `build`, `review`, `record`, `harvest`,
  `retrospective`, `release` — all in heavy use, none in git-workflow.md's
  table. Scan 7's exact species: a skill that drifted by standing still.
- **Line endings.** Python's `write_text` on Windows turned every rewritten
  file CRLF in the worktree; the index stayed LF and git normalised, but a
  byte-copy test caught the one file it compares raw. Cosmetic, recorded so
  the next session writes with `newline="\n"`.

## Patterns We Noticed

- **"Automatic" resolves to persistence.** Every time this period an
  operator asked for something to be automatic — reconciliation, refresh,
  now the retrospective — the honest decomposition was the same: the
  *question* is mechanical and can wait somewhere loud; the *answer* is a
  verdict, and a recorded verdict propagates. `feels-automatic-is-
  persistence-of-the-question` is the period's harvest and the shape of
  every mechanism it built.
- **Backlogs collapse to rulings.** 27 items, four rulings. The seat queue's
  assembly (closed-loop Phase 3) should expect the same ratio for the other
  seat classes, which argues for citation as the queue's primary verb.
- **Restated lists are the drift species.** Six of six dark-region hits;
  four of four census-test failures; the commit table. The corpus already
  knows this (`framework-reserved-types-need-thing-md-as-single-source`,
  the ninth review); it keeps being true because prose enumerations are
  how humans read and registries are how tools do.
- **A recorded ruling is standing authority — and the corpus keeps
  discovering where.** 28 August (settled reasoning), 12 September (an
  agent may answer on a stated ruling), 13 September (a recorded decision
  is a stated ruling). Three rulings, one direction, each occasioned by a
  concrete wait that added no information.

## Reflexive Scans — The Record

**Scan 1 — conflict scan (full-domain).** Scoped to the period's delta and
the 54 shared-target pairs the clustering pre-filter produced, not the full
edge walk 08c performed — recorded as a deviation, with the reason: the
delta is where contradiction enters, and the pre-filter's pairs are where
it hides. One found: the boxed rule vs the who-answers paragraph inside
change-reconciliation.md (above), resolvable in-session under
belief-revision's first branch, so no `type: conflict` thing. Zero standing
contradictions surfaced among the period's 22 insights and four decisions
against their neighbours.

**Triage — the open set.** One open conflict,
`hard-hook-vocabulary-contradicts-observable-trigger-insight`. Its proposed
resolution is complete and its alternative rejected with reason; conflict
resolution is a designed operator seat, so it is **held** with a
`disposition_reason` naming exactly that and recommending the proposal.
One sentence from the operator resolves it.

**Scan 2 — schema coherence.** Registry read: 49 fields, five new this
period (`subject`, `raised_at`, `raised_by`, `verdict`, `verdict_reason`),
each reusing an existing shape — a structural pointer, a local pin, an
actor, a receipt. Two clusters worth naming, neither merged: the *actor*
fields (`decided_by`, `raised_by`, `verified_by`, and `source` on insights)
are four names for "who performed this act" with different value spaces —
healthy while four, and the `answered_by` candidate would be a fifth, at
which point one attribution shape is owed; and `resolved_by` on conflicts
is not an actor at all but the surviving party's id, a misnomer with two
uses and a spec that defines it, left alone. `session` (173) and `created`
are the strongest same-value pair and are deliberate. No normalisation.

**Scan 3 — index rebuild.** Run in this commit; anchors reset to the
period's end.

**Scan 4 — change-driven reconciliation.** The first retrospective with a
mechanically enumerable work list: `mdllm cues .` over the baseline
2026-08-27 → **none**. Not because the period reconciled at change — it
did not, for seventeen days — but because the carrier landed, the backlog
was answered by citation under the 13 September ruling, and the tail closed
on itself. The backward pass this scan describes ran on 12–13 September
instead of here; this scan's contribution is to confirm the list is empty
and set the next baseline.

**Scan 5 — insight triage and consolidation.** Orphan findings: none. The
pre-filter produced 54 pairs sharing two or more targets; every one is
dominated by shared *specification* targets (the manifesto, provenance,
change-reconciliation), which is shared authority, not duplication. Judged:
no merges. The three-target pairs
(`cross-domain-handoff-is-built-inbound-only` with
`reconciliation-candidates-…` and with `cross-domain-readiness-…`) are
siblings about one boundary, distinct claims, already related. One new
hold: `a-dispatch-layer-outside-the-corpus-is-a-second-brain`, a standing
razor with no live consumer to key liveness to — and the razor the
operator's retrospective-automation question must pass. Proposal for the
pre-filter itself, recorded not built: weight shared targets by target
type — two insights citing the manifesto is not evidence of overlap; two
citing the same insight is.

**Scan 6 — conditions-met.** 51 held reasons re-read. Four came true:
- `reconciliation-candidates-are-detectable-from-the-commit-stream` —
  *promote when the manual noticing starts to cost.* It cost 36. Promoted
  to change-reconciliation-specification; `mdllm cues` is the insight built.
- `cumulative-drift-is-invisible-to-per-change-walks` — *promote once a
  second sweep confirms the cadence.* The carrier's first reading was that
  sweep. Promoted to change-reconciliation-specification.
- `an-agent-in-a-loop-optimises-the-loop-not-the-goal` — its stop
  condition is the dispatch prompt's mandatory input, carried by two real
  launches. Promoted to dispatch-loop (the reason said "dismiss"; the plan
  said "promote"; promotion is the truer word for a lesson designed in).
- `a-ruling-triages-more-cheaply-than-a-mechanism` — *promote when a third
  ruling resolves a proposal set as cheaply.* The third was this morning's.
  Promoted to framework-agent-closes-settled-cues-2026-09-13.
Re-read and still held, with the condition named: `a-scaffold-cannot-birth-
its-own-author` (its remedy waits on the session-start-hardening
acceptance runs, still open); `the-first-retrospective-is-the-one-the-
floor-cannot-chase` (the cue carrier's 30-day fallback handles the
first-retrospective case for *cues* only — half a mechanism, not the
admission rule the condition names); `the-root-is-not-a-representative-
domain` (the carrier's first reading was root-shaped — plans and decisions
about the framework itself — a fourth sighting is not clean, so not
counted). The remaining 44 hold as written.

**Scan 7 — skill coherence.** Enacted practice first, from 119 commits:
`session-end` 23 times — the ritual is the period's most-enacted act — then
`fix` 13, `plan` 9, `release` 6, `decide` 6, `reconcile` 4; every ritual the
entry file binds was enacted this period (estate-sync at every start, the
read boundary asserted before every write from a long read, orient pulled
by intent, session-end invoked, the retrospective called). Dispositions:
- `AGENTS.md` (authored sections): **confirm-current**, one line updated —
  Key Innovation 7 now names the cue carrier among the reflexive
  behaviours. Routing and catalog were walked on 12 September.
- `git-workflow.md`'s commit-action table: **update** (v1.8) — ten
  prefixes the stream had earned, added with meanings and examples, and a
  sentence saying the set is a vocabulary the hook does not read.
- `session-end-continuity`, `dispatch-loop`: **confirm-current** — both
  revised this period from contact, both enacted.
- `detect-conflicts`, `review-schema-coherence`, `review-skill-coherence`:
  **confirm-current** — enacted here; the conflict scan's scoping deviation
  recorded above, not written into the prompt on one sighting.
- `session-orientation`, `surface-attention`, `domain-velocity`,
  `evaluate-triggers`: **confirm-current, finding carried** — they address
  a human reader, and a dispatched run has none; closed-loop
  `Phase 4` holds the finding and the three honest options.
- `cascade-completion`: **confirm-current**; `mdllm cascade` mechanises
  its gather.
- No `skills/` directory exists at the root; the framework's operating
  layer is its prompts and the entry file, which is what was read.

## What Should Change

1. **Version 3.40.0 — this period's release.** A reserved type, a
   subcommand, a digest line, two rulings and a spec at 1.4. Cut after this
   retrospective lands; the push is the operator's.
2. **The retrospective's own cadence, as a dated trigger the session
   reads.** The operator's question (below) passes
   `a-dispatch-layer-outside-the-corpus-is-a-second-brain` in exactly one
   form: the 60-day clock is already a floor check; making it a *trigger
   with an action the session starts on* is the corpus scheduling itself.
   What must not be built is a scheduler that decides. Proposed, not ruled.
3. **Scan 5's pre-filter weights targets by type** — recorded above; build
   on a second retrospective that finds the same noise.
4. **An `answered_by` on cues, when the fifth actor field arrives** — not
   before.
5. **`first-hour.md`** — still teaches the 3.37 shape; the onramp plan's
   Phase 5 owns its rewrite. Perimeter warning accepted until then.

## Open Questions Going Forward

- **Should the retrospective run itself?** The operator's framing: the
  house gets messy while the children play; at the end of the day you tidy.
  The record's answer so far is a split, not a side — the *tidying* is
  mechanical wherever its work list is enumerable (scans 3, 4, and the
  mechanical halves of 5 and 6 already are), and the *rulings* it produces
  are seats by ratified census. A retrospective the session starts on its
  own trigger, runs the enumerable scans of, and hands the operator a queue
  of verdicts with proposals is exactly `closed-loop-operating-state`
  Phase 3's protocol applied to one ritual. Whether that is "automatic" in
  the operator's sense is the question; it is what
  `feels-automatic-is-persistence-of-the-question` predicts they want.
- **Does the cue count stay near zero?** The carrier is two days old. If
  ordinary sessions leave it near zero with the citation link, the shape is
  right; if it climbs and the climb does not trace to rulings, the
  predicate is wrong, not the carrier.
- **When does a dispatch run raise its first cue?** Phase 4 has still not
  reached a ritual. Until it does, the unattended rule is doctrine without
  a data point.
- **The conflict.** One sentence.
