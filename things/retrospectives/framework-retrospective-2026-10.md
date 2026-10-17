---
id: framework-retrospective-2026-10
type: retrospective
status: complete
version: 1.0
created: 2026-10-17
period_start: 2026-09-13
period_end: 2026-10-17
domain: markdownllm-framework
tags: [retrospective, the-reckoning, the-seat, walk-gate, workflows-emerge, standing-watch, closed-loop, dispatcher, actors]
triggers:
  - type: time
    condition: "2026-11-16 reached"
    action: "Retrospective chase (thirty days from period_end 2026-10-17; retrospective-cadence-is-a-dated-chase-2026-09-13). If things/ moved since 2026-10-17: run the mechanical scans now (index rebuild, mdllm cues, the reckoning's bands and held reasons), offer the ritual as this session's first item, or — unattended — draft it and file the rulings to the seat. If nothing moved: re-date this chase. Either way, the retrospective that answers it disarms this trigger and arms its own."
linked_things:
  - id: framework-retrospective-2026-09
    relation: references
    notes: "Prior retrospective (The Question That Waits, closing at the cue carrier). Its three open questions are answered below: the cue count stayed near zero, the first dispatch run raised and drafted, the conflict was ruled."
  - id: the-reckoning
    relation: references
    notes: "The period's central build with the walk gate: disposition gets an actor at the session end and the tick. Scans 5 and 6 here ran as reads of `mdllm reckon` for the first time — Phase 4's first evidence, recorded on the plan."
  - id: the-seat
    relation: references
    notes: "The arc the period ended on: who sits in a clone, the version guard, the ticket as a work item — the record ranking causes above the felt one."
  - id: cue-carrier
    relation: references
    notes: "Phase 7 landed this period: the walk gate at the commit boundary, corrected the same day, then following the commit into a nested workspace."
  - id: closed-loop-operating-state
    relation: references
    notes: "The dispatcher's first digests, Phase 2c closed, Phase 4's first run that worked a trigger — the loop ran once."
  - id: the-walk-runs-on-detection-the-ruling-is-the-residue-2026-10-05
    relation: references
    notes: "The ruling that gave the walk its actor; its first build the same morning answered the wrong half and was superseded within the day."
  - id: the-reckoning-is-the-digestion-beat-2026-10-05
    relation: references
    notes: "The ruling that gave disposition its actor; scan 6 below found its measurement had become a digest line."
  - id: workflows-emerge-from-use-2026-10-07
    relation: references
    notes: "The ruling that workflows are found in the commit stream; scan 7's both-ways question is now also a floor read (`mdllm workflows --emergent`)."
  - id: seats-are-declared-and-a-conversation-is-a-work-item-2026-10-15
    relation: references
    notes: "The ruling the record produced when the operator asked for evidence rather than opinion — the felt cause came fourth of four."
  - id: the-felt-symptom-names-one-cause-the-record-ranks-them
    relation: references
    notes: "The period's last harvest, and its shape: a remedy ruled for the visible cause, then re-ranked by one pinned read."
  - id: a-preserved-question-is-not-a-done-walk
    relation: references
    notes: "The diagnosis that ended the human cue: five backstops, none walked. Every mechanism this period named an actor rather than another backstop."
  - id: a-remembered-step-is-a-missing-actor
    relation: references
    notes: "The pattern under the period: the walk, the reckoning, the tick and the seat each turned a remembered step into a named actor at a boundary."
  - id: a-uniform-answer-is-a-dead-judgment
    relation: implements
    notes: "Promoted by scan 6: the disposition distribution is now a digest line (`reckon --rates`), and this is the second retrospective to produce promotions and a dismissal."
  - id: change-safety-is-defense-in-depth
    relation: implements
    notes: "Promoted by scan 6: the nets, in order, written into change-reconciliation.md → Enforcement at this retrospective."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: implements
    notes: "Promoted by scan 6 into the dispatcher decision that cites it and rules its shape; the tick has since run and done only what the razor allows."
  - id: protecting-one-budget-displaces-the-failure-into-the-other
    relation: references
    notes: "Dismissed by scan 6 on its own condition — no second instance by this retrospective."
  - id: substrate-floor-development
    relation: references
    notes: "The root's one workflow-definition: no run this period while three arcs enacted its shape — scan 7's both-ways finding, carried as residue."
  - id: evidence-and-eval-backlog
    relation: references
    notes: "Takes the next slot after this retrospective, on the operator's 2026-10-17 ruling."
---

# Framework Retrospective — October 2026: Every Step Gets Its Actor

**Period:** 2026-09-13 → 2026-10-17, the releases from 3.40.0 to 3.48.0 —
nine of them in thirty-five days. **Baseline for the next period's scan 4:**
2026-10-17. **Cadence:** thirty-four days, called by the chase the 2026-09
retrospective carried (fired for 2026-10-18; the operator answered it a day
early at the previous session's close). **Significant-read base:**
`c26ce3b91daf71acdfeca0f5b376ee93d9d584a9`, the 3.48.0 release commit, pinned
with `--assert-head` before this was written.

## What We Were Trying To Do

The 2026-09 retrospective closed on a question that waited: the cue carrier
held the reconciliation question, a human answered it, and the retrospective
was the net. This period set out to give that question — and every other
step the record said "more often than not doesn't happen" — an actor at a
boundary the harness owns. In sequence: the between-sessions surface got its
first specification and its doorbell (`standing-watch.md`, `mdllm watch`),
then the ticket for messages with no artefact behind them; the public docs
learned to read the tool and went up; a cloud session found a shallow clone
lying to the floor and taught the floor to ask; two more harness adapters
reached release (Codex Cloud, OpenClaw); and then, in four days of October,
three rulings with one shape — the floor detects and assembles, the agent
acts within bounds, the operator rules on the residue: the walk runs on
detection at the agent's commit; the reckoning gives disposition an actor at
every session end and every tick; workflows emerge from use. The period ended
on the seat: the operator asked why agent-to-agent loops had been hard to run
and wanted evidence, and one pinned read of the busiest workspace's history
ranked the causes — clone drift, turns never published, two agents in one
working copy — above the one the felt remedy addressed.

## What Worked

- **The record ranked the causes.** The branch-per-conversation remedy was
  sound for the cause visible from inside a turn, ruled within a day, and
  then placed fourth of four by one read of the workspace's whole history at
  a pinned commit. The seat, the version guard and the published-turn check
  fixed the first three in the substrate; the branch plan now follows them.
  Third instance in three periods of `the-record-answers-the-direction-
  question-first`; the new insight names the shape.
- **The gate refused its author.** The walk gate's first live act was to
  refuse the session that built it, with the four owed surfaces named. It has
  held since — six walks against five definition-surface changes in the last
  seven days (`reckon --rates`), and the cue count the 2026-09 retrospective
  asked about stayed near zero: five unraised at period end, every one a
  progress record on a plan, every one not-inflection.
- **The first close was ten decisions, not a wall.** The reckoning's attended
  half ran on 2026-10-08: four promotions, five holds with a look-again date,
  one trigger acted on; 45 → 35 and the `session-end:` commit passed the
  gate's close leg. The unattended half drafted five decisions on 2026-10-11,
  applied none, and said the bindings belong to an attended session because
  they change a definition surface — the bounds respected by a run nobody was
  watching.
- **The loop ran once.** The dispatcher's tick, re-hosted on the operator's
  machine 2026-09-23, filed digests from 2026-10-04; run 3 worked a fired
  trigger end to end and run 5 skipped a DIVERGED workspace and said so.
  `closed-loop-operating-state` Phase 2c closed on exactly the condition its
  ruling named.
- **Corrected by first use, within the day.** The gate asked the operator
  first (superseded by noon). The unattended close hid the list it exists to
  draft (fixed the same day). The watch inherited four of five decisions it
  claimed (the lock, found a day later). The first Pages build showed three
  defects the blob view could not. In every case the first use was the test
  and the record kept both halves.
- **Nine releases, every one walked.** Every release commit this period names
  its touchpoints, its cues and its floor run; the dark-region residue is
  listed where it was not walked.

## What Didn't Work

- **The felt remedy was ruled before the evidence ranked it.** The branch
  plan was decided and phased on 2026-10-09; the read that placed its cause
  fourth came on 2026-10-14 only because the operator asked for evidence
  rather than anyone's view. Nothing in the ritual asked for the read first.
  `the-felt-symptom-names-one-cause-the-record-ranks-them` is the harvest; the
  next direction question should begin with the pinned read, not end with it.
- **A second seat's commits carried no convention at all.** The OpenClaw
  contributor's session landed `"feat:add-…"`, `Fix-domain-…`, two reverted
  scaffold commits in a pytest temp dir — none in `action: description` form,
  one with a bare carriage return that crashed `session-start` on every clone
  until 3.46.0. The commit vocabulary is interpretation-anchored; it reached
  the seat that read it and no other. Recorded in `git-workflow.md` 1.14.
- **The vocabulary table lagged again — by eight.** `floor`, `spec`,
  `harness`, `reckon`, `cue`, `advance`, `close`, `correct`: all in use, none
  in the table, one period after the table gained ten. The rate is now
  known: a prefix a week.
- **The stall population grew to thirteen.** Thirteen high- or critical-
  priority plans untouched past 21 days, four past 55 — Explorer (two),
  Cowork, the substrate-review remedy, session-start hardening at 0 of 9
  boxes after 48 days. The reckoning's settled band names eighteen work items
  with "pause, or say what it waits on". The honest status for most is
  `paused`; the attention went to the new arcs. The close owes these ten a
  day; this retrospective records that the queue is long, not that it is
  wrong.
- **The agent's own memory drifted.** The framework agent's vendor-side notes
  said on 2026-10-01 the dispatcher "ticks daily but does nothing"; by
  2026-10-07 it had worked a fired trigger, and the corpus said so. A note
  outside the corpus is `tracking-artifacts-can-drift-from-reality` in
  miniature; corrected on the agent's side.
- **The external review is 39 days unverified.** `review-external-conflict-
  lifecycle-2026-09-08` was acted on within four days (its F5 became the
  carrier's ruling, its F1 wired scan 4) and never flipped `verified` —
  a human act, owed below.

## Patterns We Noticed

- **Every mechanism this period named an actor, not a check.** The walk had
  five backstops and no walker; the reckoning had a prompt and no boundary;
  the dispatcher had a design and no tick; the loop had turns and no one
  checking they left. Each fix is the same move: name who acts, at which
  boundary the harness already owns, within what bounds. `a-remembered-step-
  is-a-missing-actor` (2026-09-24) predicted it; the four rulings since are
  its instances.
- **The question persists as a file — 145 of them.** Cues are now the
  largest type in the corpus (158 of 541 things), 145 created this period
  against 9 insights and 16 decisions, almost all answered not-inflection by
  citation. The carrier works exactly as designed, and its exhaust is a file
  per question. `thing-lifecycle.md` — deferred "until felt" — names a
  200–300 thing ceiling this corpus passed some time ago; answered cues are
  terminal and inert, but validation walks them. Whether this is felt yet is
  the operator's call (open question below).
- **One meaning, two field sets.** A hold on an insight is `disposition:
  keep-active` + `disposition_reason`; a hold on a plan written by `reckon
  --keep` is `settles_when` + `disposition_reason`, no `disposition`. The
  registry shows it as 61 reasons against 60 dispositions. Scan 2's one
  finding, and the first time the schema review caught a drift the tool
  itself introduced.
- **Backlogs still collapse to rulings.** 83 of 125 cues closed by citation
  at 3.47; five of five here. The ratio the 2026-09 retrospective measured
  held for a second period — on the root corpus again, so the held insight
  stays held.
- **The root is not a representative domain, mechanically now.** `mdllm
  workflows --emergent` on the root returns none: no type travels a
  three-stage path. The root's process is prefixes in a commit stream, not
  statuses on a carrier; a domain's is the reverse. The insight's claim, read
  by a tool.

## Reflexive Scans — The Record

**Scan 1 — conflict scan.** Scoped to the period's delta (9 insights, 16
decisions, 8 plans) checked against their neighbours, plus the 39 pairs the
composition pre-filter produced — the second retrospective running to take
this shape, so the scoping is now written into `detect-conflicts` 1.2 as the
sanctioned form where the carrier has walked the period. Zero standing
contradictions requiring a `type: conflict` thing. One held tension noted
and left as the insight that records it: `mesh-safety-is-the-floor-not-the-
topology` is the agent's counter-position to the operator's stated view
(organism over orchestrator), offered 2026-09-22 and not ruled on. It is a
position against a statement, not a thing against a thing; belief-revision
has nothing to seal until the operator's view is a record. The same-day
supersession (`the-verdict-is-asked-where-the-change-lands` by `the-walk-
runs-on-detection`) is marked, both records kept.

**Triage — the open set.** Zero open conflicts. The one the 2026-09
retrospective held was ruled `both-valid` the same day on the operator's
delegation.

**Scan 2 — schema coherence.** Registry read at 541 things: 51 fields, one
new this period (`settles_when`, 10 — the reckoning's per-item exit rule in
trigger shape, deliberately the same shape as `triggers` with the opposite
role). The actor cluster stands at four (`decided_by`, `raised_by`,
`verified_by`, `source`) with `resolved_by` still a party's id, not an actor;
`answered_by` has not arrived — cues carry the answer in `verdict_reason`
and `informed_by` — so no fifth field and no normalisation owed. **One
overlap found:** the hold written by `reckon --keep` on work (`settles_when`
+ `disposition_reason`) and the hold on an insight (`disposition:
keep-active` + `disposition_reason`) are one meaning in two field sets; the
mismatch is visible as 61 `disposition_reason` against 60 `disposition`.
Propose canonical: every hold carries `disposition: keep-active`, and the
tool writes it. Migration: one plan (`operator-seat-and-harness-native-
onramp`) and the `--keep` writer. Loss: none — `settles_when` stays as the
look-again date. Recorded for `the-reckoning` Phase 4, not applied here: it
is a floor change.

**Scan 3 — index rebuild.** Run in this commit; the four indexes' anchors
reset to the period's end.

**Scan 4 — change-driven reconciliation.** `mdllm cues .` over the baseline
2026-09-13: **five unraised**, zero open. Raised mechanically (`cues
--raise`) and walked here, each with its declared and literal tiers from
`mdllm touchpoints` and its conceptual residue read: `the-reckoning` (seven
commits of phase progress), `cue-carrier` (box 7(h)), `closed-loop-
operating-state` (the dead-man answered, 2c closed, Phase 4's first
evidence), `estate-workflow-derivation` (an edge and a re-conditioned
trigger), `evidence-and-eval-backlog` (a sequencing sentence). All five
**not-inflection** — progress records on plans, which the commit gate does
not read because a plan is fan-in, not a definition surface. That is the
carrier working as specified: the gate takes the definition surfaces at the
boundary, the retrospective takes the fan-in subjects from the baseline, and
between them nothing waited more than a period. The walk's one finding is on
`retrospective.md` itself: scans 5 and 6 reason about the reckoning without
naming it, and Phase 4 of `the-reckoning` owns rewriting them.

**Scan 5 — insight triage and consolidation.** Orphan findings: none among
insights. The one orphan in the corpus is an artifact —
`markdownllm-explorer-code-cold-review-1`, a code review of a frozen
product whose citing plan is blocked on the operator; linking it from a
blocked plan would be manufacturing an edge, so it stands as an accepted
Info, as it has since 3.47. The composition pre-filter produced 39 pairs
sharing two or more targets, weighted this time so a shared specification
counts for less than a shared insight or decision: the strongest pair is
the same sibling pair the 2026-09 retrospective judged
(`cross-domain-handoff-is-built-inbound-only` with `cross-domain-readiness-
is-a-shared-signal-not-a-producer-push`, distinct claims about one
boundary); the three-insight cluster around `vendor-harness-adapter-
foundation` + `portability-claims-need-execution-tests` (seat visibility,
consumer-defined interface, installation is not activation) are three
claims about harness acceptance, each cited for a different reason. Judged:
no merges. **The pre-filter proposal is now built-when-felt by its own
condition** — "build on a second retrospective that finds the same noise" —
and this is that retrospective; recorded on `the-reckoning` Phase 4 as scope.
**The reckoning's settled band supplied the rest of the triage list:** five
insights cited live for 122–124 days and never promoted. Four were already
in the operating layer and are promoted with the spec named
(`composition-is-the-inverse-of-decomposition` → thing.md;
`structural-pointers-need-reverse-edge-indexing` → derived-index.md;
`cross-domain-handoff-is-verified-external-input` → provenance.md); two are
eval evidence the entry file's principle 9 says is insufficient, and are
held with the polar-station-htc run as their look-again
(`structure-decides-figures-scale-decides-convention`,
`withholding-is-not-isolation`).

**Scan 6 — conditions-met.** 57 held reasons re-read. Four came true:
- `a-uniform-answer-is-a-dead-judgment` — *until a retrospective produces
  the first promote/dismiss, or the distribution becomes something a
  retrospective reads mechanically.* Both: 2026-09 promoted four; `reckon
  --rates` is the distribution as a digest line. Promoted to
  session-memory.md → The Reckoning.
- `protecting-one-budget-displaces-the-failure-into-the-other` — *dismiss at
  the 2026-10-13 retrospective if no second instance.* None. Dismissed.
- `change-safety-is-defense-in-depth` — *promote as a "The Nets" paragraph
  in change-reconciliation.md at its next enforcement change.* Two
  enforcement changes this period, paragraph unwritten. Written here
  (change-reconciliation 1.10 → Enforcement → The Nets); promoted.
- `a-dispatch-layer-outside-the-corpus-is-a-second-brain` — *promote when a
  second automation proposal is shaped by it on the record.* The dispatcher
  decision of 2026-09-23 cites it and rules its shape; the tick has run.
  Promoted into that decision; the sentence the hold wanted in
  orchestration.md's adapter doctrine is owed at that spec's next adapter
  change (What Should Change, 6).
Re-read and still held, with the condition named and current:
`a-scaffold-cannot-birth-its-own-author` (hardening at 0 of 9, 48 days);
`the-first-retrospective-is-the-one-the-floor-cannot-chase` (the 60-day
guard in `validation.py` still precedes the never-written branch; the cue
window's 30-day fallback is half a mechanism); `the-corpus-answers-faster-
than-it-is-asked` (a second period, same ratio, same biased sample — the
root; the next sample must be a domain); `a-remote-fetched-before-and-not-
found-now-is-a-credential-change` (three repos said "not found" at this
session's start and estate-sync still files them `undiagnosed` — the check
is cheap and owed, What Should Change 5); `fixture-fixes-correct-bugs-not-
difficulty` and `boundary-respect-was-interpretation-not-enforcement` (the
eval slot is now dated); `agents-md-discovery-is-harness-dependent` and
`portability-claims-need-execution-tests` (the onramp is paused, 2026-10-17);
`the-orchestrators-premises-are-the-least-reliable-input` (the 2026-10-11
run declined to bind, which is a run respecting its bounds, not correcting
its launcher). The remaining 44 hold as written.

**Scan 7 — skill coherence.** Enacted practice first, from 82 commits over
`things/` (114 in all): `fix` 16, `session-end` 12, `reconcile` 10,
`release` 9, `decide` 8, `build` 7, `floor` 5, `plan` 5 — every ritual the
entry file binds was enacted (estate-sync at every start; the read boundary
asserted before every write from a long read, including this one;
session-end twelve times; the retrospective called by its chase). The
period's shape, read from the stream alone: *decide → plan → floor/build →
spec → walk → release → session-end*, three times over (the walk gate, the
reckoning, the seat), with `fix` interleaved at the rate of one per two
days. Floor findings taken as given: none (coherence clean). Dispositions:
- `AGENTS.md` (authored sections): **confirm-current** — the routing table
  gained the reckoning and workflows rows this period at their commits; the
  seat's own line is deliberately held for the release after 3.48.0 (the
  seat plan's corrected Phase 5), so its absence is the record, not drift.
- `session-end-continuity` 1.7: **confirm-current** — revised this period to
  run the close; enacted twelve times.
- `dispatch-loop` 1.6: **confirm-current** — enacted by the tick's runs 2–5
  and the 2026-10-10/11/13 reckonings.
- `detect-conflicts`: **update** (1.2) — the scoped retrospective form,
  written on its second sighting.
- `review-skill-coherence`: **update** — `draft` → `evolving`; enacted at
  two retrospectives, and this one found the second seat's commits, which
  is the drift class it was written for.
- `review-schema-coherence`: **confirm-current** — enacted here; found one
  overlap the tool introduced.
- `session-orientation`, `surface-attention`, `domain-velocity`,
  `evaluate-triggers`: **confirm-current, finding carried** — they address
  a human reader; the tick now has runs, and closed-loop Phase 4 still holds
  the finding that a dispatched run reads them with no one to tell.
- `cascade-completion`: **confirm-current** — `mdllm cascade` mechanises it.
- `git-workflow.md`'s commit table: **update** (1.14) — eight prefixes
  added, the lag rate recorded, the second seat's unprefixed commits named.
- **The workflow definition, both ways.** The root's one definition,
  `substrate-floor-development` (draft, authored, no carrier, four explicit
  runs from the August sprints): **(a) enacted?** No run this period — the
  three October arcs each travelled its stages and declared none. **(b) de
  facto process?** `mdllm workflows --emergent` says none, honestly: the
  root's arcs run through plans whose statuses do not travel a stage path,
  so the emergence read sees nothing. The shape is real and the floor cannot
  see it. The remedy on the record is `carrier: plan` on the definition
  (`workflow-state.md` 0.9) — which would make every plan a run and put the
  floor's membership check on every plan's status, a change of meaning and
  the operator's. Carried as residue below, not ruled.

## What Should Change

1. **This retrospective lands unpushed.** The root is 3.48.0 and published;
   this commit and the walk cues are the operator's next push, not a
   release.
2. **`the-reckoning` Phase 4 is next on the framework side** — scans 5 and 6
   as reads of the reckoning (done here by hand, so the rewrite has its
   evidence), the composition pre-filter in the reckoning's reads, and the
   hold on work and on insights written with one field set. Then
   `evidence-and-eval-backlog`, on the operator's 2026-10-17 ruling.
3. **Thirteen stalled plans owe a status.** The close takes them ten a day;
   most will be `paused` with a `--keep`. The retrospective's contribution is
   the count and the observation that `in-progress` has become the status of
   record for work nobody is doing.
4. **`detect-conflicts` 1.2, `review-skill-coherence` → evolving,
   `git-workflow.md` 1.14, `change-reconciliation.md` 1.10** — done in this
   commit; the two specs' walks are the gate's and ride with it.
5. **estate-sync names the credential case.** A remote fetched before and
   "not found" now is a credential change in every instance on record; the
   check is whether the remote-tracking ref already exists. Three repos said
   it this morning. Belongs in `mechanical-coherence-checks-backlog` when
   that plan is next opened (34 days untouched).
6. **orchestration.md's adapter doctrine owes one sentence** — the schedule
   is things, the tick is dumb — at its next adapter change; the razor is
   promoted into the dispatcher decision meanwhile.
7. **A conversation's commits should carry the seat, not infer it.** The
   second seat's unprefixed commits are the case for `mdllm seat` landing
   its entry-file line in the release after 3.48.0, as the seat plan says.

## Open Questions Going Forward

- **Should `plan` be the carrier of `substrate-floor-development`?** The
  floor would then see the root's arcs as runs and enforce stage membership
  on every plan's status. It is the honest reading of what the root does;
  it is also a change of meaning on 40-odd plans and the operator's to make.
  The alternative is to accept that the root's process is a commit-stream
  shape and leave the definition for explicit runs.
- **Is the cue exhaust felt?** 158 cue files, 145 this period, nearly all
  answered and inert. `thing-lifecycle.md` has waited deferred since June for
  a ceiling this corpus passed. If the operator feels it — validation time,
  the orient view's noise, a clone's size — the rolling window and
  disposition-to-stubs it specifies have their first consumer; if not, the
  files stand as the audit trail they are.
- **One human act owed:** verify `review-external-conflict-lifecycle-
  2026-09-08` (`verified_by` in its own commit) or record why it stays
  quarantined. Its findings were acted on within four days; the flip was
  never made.
- **The estate retrospective fires tomorrow** (`estate-retrospective-
  synthesis-2026-08`, 2026-10-18). It consumes this one; its subject is the
  membrane, and the dispatcher's two workspaces now have digests to read.
- **The seat for this clone** is undeclared. `mdllm seat . --set <actor>
  --agent <harness>` is one line and the operator's identity to give.
