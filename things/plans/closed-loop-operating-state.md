---
id: closed-loop-operating-state
type: plan
status: in-progress
version: 1.7
created: 2026-08-27
informed_by:
  - id: estate-workflow-derivation
    commit: cb68dfb8468021db2a2a99b7ff889546b4d8bda4
priority: high
tags: [operating-model, closed-loop, human-seats, dispatcher, gates-census, vision]
linked_things:
  - id: operating-model-specification
    relation: implements
    notes: "This plan works the estate-radius composition that spec describes toward its target state; Phase 5 seals the discovered doctrine back into it."
  - id: universal-workflow-methodology
    relation: implements
    notes: "The plan is itself the methodology applied at the widest radius: current state, desired state, evidence-gated route — and the loop it automates is that spec's own iteration clause."
  - id: framework-retrospective-2026-08c
    relation: derived-from
    notes: "The retrospective's closing open question — a census of gates, not a feeling — is Phase 1 of this plan. The operator's declaration arrived the same night, from the other direction."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: implements
    notes: "The boundary law this plan must never move: the irreversible stays human. The gates census exists to find where that boundary actually runs, not to relocate it."
  - id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
    relation: implements
    notes: "Its own dismissal condition is Phase 2's launch discipline: every automated run carries an exogenous stop condition at launch. Building the dispatcher this way is what would promote it."
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: implements
    notes: "The imperfection budget, already named: the target is not zero defects but a correction rate that exceeds the drift rate, held by the loops."
  - id: operating-layer-quality-loop
    relation: references
    notes: "The sibling plan that gave the operating layer its quality loop; this plan closes the remaining loops around it."
  - id: a-true-primitive-is-discovered-not-authored
    relation: supports
    notes: "Nothing below is a new mechanism. Every phase wires or classifies primitives that already exist; the only genuinely new artifact is the census's verdicts."
  - id: agents-cannot-self-install-permission-bearing-hooks
    relation: implements
    notes: "The doctrinal basis for the operator's irreducible list below: the dispatcher is a permission-bearing installation, so granting its authority is the one constructive act only the human can perform."
  - id: a-dispatch-layer-outside-the-corpus-is-a-second-brain
    relation: implements
    notes: "Phase 2's governing design commitment: the schedule is things, the tick is dumb. This plan keeps the insight in live circulation until Phase 5 absorbs it into doctrine."
  - id: estate-workflow-derivation
    relation: derived-from
    notes: "The operator-declared precondition for Phase 2b, met 2026-08-28 and pinned above: unattended sessions must not execute undeclared process. Seven of seven definitions declared; three carry recorded process gaps, which the gate did not ask about."
  - id: dispatch-digest-home-2026-08-29
    relation: implements
    notes: "Phase 2b's corpus half: where the digest lands, why the root loses, and the dead-man armed below — with its coverage limit stated rather than implied."
  - id: a-records-home-must-not-sit-behind-the-gate-it-reports-on
    relation: informs
    notes: "The pilot's first firing paid for this one. It is the standing design lens on Phase 4's remaining runs: a fail-closed loop that cannot file its own refusal is silent exactly where it is meant to speak."
triggers:
  - type: time
    condition: "2026-09-05 reached"
    action: "Dead-man on the dispatcher. Check whether a dispatch digest has been filed in the pilot repo within the window; if none has, the loop is silent and silence is not health — establish whether the job was never registered, was registered and never fired, or fired and died mid-run (a digest left in-flight with a live claim says the third). Re-date this trigger to the next window once answered. Coverage is honestly partial: this fires into the operator's own session-start orientation at the framework root, so it is read at the operator's session cadence and not before — the chase pattern, not a monitor (dispatch-digest-home-2026-08-29)."
---

# The Closed-Loop Operating State

The target operating state of the substrate, written down as the operator
declared it at the close of 2026-08-27 — and echoed independently the same
day by a collaborator in the estate, whose one-line version is the sharpest:
**"we only need to be involved if something breaks."**

The declaration, in the operator's own arc: every piece of the substrate now
has the pieces it needs to run on its own. A retrospective fires and runs.
From the retrospective comes a plan — because a retrospective plus the
current state yields a desired state and a problem statement. From there the
universal workflow carries it forward, the review feeds the next cycle's
current-state assessment, and the loop closes. The human steps in only where
it is time for a human to be in the loop. This document exists so that the
goal is defined rather than felt — something to work to, tasks to tick off,
a route to discover.

**Exposure: not yet.** Other domains will rest on this through the sealed
doctrine in `operating-model.md` (Phase 5) and through their own refresh —
never on a framework-root plan mid-flight. The condition that changes the
answer is Phase 5 completing.

## Current State (honest, evidenced)

- **Every loop exists and has run at least once — but each was pulled, by
  hand or by chase.** The retrospective loop closed on 2026-08-27 from a
  dated trigger (first proof at that radius that the chase pattern works).
  The universal workflow has carried three floor sprints and a seams run as
  pinned workflow-runs, independently verified. Review loops, refresh,
  reconciliation, publication-under-authority: all real, all exercised.
- **The dispatcher exists and has fired twice — and has done no loop work
  yet.** *(Corrected 2026-08-29; this bullet read "There is no dispatcher"
  until that morning.)* The corpus half shipped
  (`mdllm dispatch-payload`, the standing prompt at v1.2), the operator
  registered the job (daily 08:00 Europe/London, scoped to the Phase 4
  pilot), and the pilot repo declared `dispatch-digest` in its own schema.
  Two runs have fired. **Both stopped fail-closed before working a single
  fired trigger** — the first refused at the pilot's pre-commit boundary by
  pre-existing generated-index drift, the second by a missing
  execution-supplied staging location its workflow forbids substituting.
  Both are filed as digests in the pilot repo; seventeen fired carriers
  remain unworked after both.
  What that evidences and what it does not, kept apart deliberately: the
  **refusal path is proven twice** — launch validity, payload integrity,
  scope, the advisory claim, the narrow generated-artifact repair, and the
  leave-the-tree-clean discipline all held on contact. The **work path is
  proven zero times.** A safety property demonstrated is not a liveness
  property demonstrated, and no restatement of this plan may read the two
  firings as a working loop.
- **Judgment beats are invocation-bound by design** — orient, session-end,
  the retrospective's residue — because un-pulled judgment at t=0 does not
  happen on any model tier. Automation must therefore schedule the
  *invocation*, never dilute the judgment.
- **The human seats are undefined by census.** The operator is present at
  many points; nobody has classified which of those points are
  consequence-gated (must stay) and which are familiarity-gated (habits of
  the builder's presence). The 08c retrospective posed exactly this question.
- **Some operator inputs are still understanding-seeking** — prompts for
  explanation, weighing, learning. In the target state those trend toward
  reads of the system's own surfaces; each one today marks a place where the
  system's self-description is thin.

## Desired State (the vision, in the corpus's own vocabulary)

Each loop fires on its own trigger, executes through the universal workflow,
files its outputs as committed things, and surfaces to a human at exactly
four seats:

1. **Option-selection / dissemination** — a retrospective or reconciliation
   has produced genuine alternatives; the system presents options with
   evidence, and the human chooses.
2. **Convergence ambiguity** — a change sits on a boundary (which domain,
   which spec, which side of a membrane) and the structure cannot rule;
   the ambiguity is surfaced as a conflict or decision-in-waiting.
3. **Irreversibility gates** — publication, money, external-party effects,
   seals on stable surfaces. These are seats *by design, not by failure*:
   the human here is not "stepping in", they are the declared authority the
   structure routes to. `consequence-is-recoverable-only-in-retrospect` is
   the law; these gates are its enforcement.
4. **Breakage** — something the loops did not catch. This seat never closes,
   *because* the unknown-unknowns are precisely what cannot be pre-routed.

The system unfolds imperfectly and that is budgeted: the loops capture what
does not work and refine it out each iteration — coherence as a maintained
rate, not a state. Verification is layered (floor validates corpus, hooks
validate commits, reviews validate builds, retrospectives validate the
loops themselves) — and the layering is honestly bounded: **risk is routed,
not eliminated.** Every named failure mode has a loop or a seat; the
residual is the reason seat 4 exists. The corpus's own insights forbid the
stronger claim: a verifier assumes the inputs it did not observe, and a
same-builder check is blind to a self-contradictory builder. Any future
restatement of this vision that says "risk eliminated" is drift against
this document.

**The reframe that dates this document:** *an input creates action.* Inputs
that are questions are the system reporting thin self-description — each
should leave a residue (a surface, an insight, a lens) so its successor is a
read, not a prompt. The measurable trend: operator inputs shift from
explanations toward rulings.

### What It Looks Like, Lived (added v1.1 — the operator asked, so it leaves residue)

The operator does not open sessions; sessions open themselves. Retrospectives
fire on their clocks in each domain, read their current state, write their
findings, birth or advance plans; workflow-runs execute those plans against
pinned definitions; reviews verify; findings feed the next cycle's
current-state assessment. All of it lands in committed state while the
operator is elsewhere.

What reaches the operator is **a queue, and only a queue**: conflicts
carrying proposed directions, option briefs where a loop produced genuine
alternatives, approval requests idling at the irreversible, and — rarely —
a breakage report with its evidence attached. Every item is a
verdict-in-waiting: options with evidence, never homework. Each ruling
becomes a committed decision the loops absorb. The operator's questions
become reads — orient, worklog, retrospectives — surfaces the system
maintains because it knows they will be read. And **silence is a report,
not an absence**: a heartbeat digest says what ran and that nothing needs a
human, because a quiet system must be distinguishable from a blind one
(the null-result discipline: "nothing found" is never "could not look").

Two honesty clauses, so the picture cannot be over-read:

- **The rolling does not stop — it idles at the gates, by design.**
  Everything reversible rolls; everything irreversible waits. Throughput at
  the desired state is bounded by the operator's seat latency, and that is
  the feature: stepping out of the loop does not mean the loop runs away.
  It also means the operator declares a seat cadence — an undated human
  wait is exactly the drift the estate already learned to chase.
- **The loops learn to maintain and refine; they never learn to want.**
  Intent is the one input that never automates. The operator's role at the
  desired state, in one line: **source of intent, judge at gates, reader
  of digests.**

### The Operator's Irreducible List (what "getting there" asks of the human)

1. **Say go on Phase 1.** ✅ *Done 2026-08-28.* The census runs without the
   operator; the verdict table comes back for ratification in one sitting.
   This is the decisive act: it converts habits-of-presence into named
   gates. *(All twenty verdicts confirmed as proposed —
   `gates-census-ratified-2026-08-28`.)*
2. **Grant the dispatcher its authority — once per harness.** ✅ *Done
   2026-08-29, for one harness.* The corpus
   already proved this seat: `agents-cannot-self-install-permission-bearing-hooks`.
   Scheduling autonomous launches is permission-bearing, so the grant is
   the one constructive act only the human can perform. After it, launches
   are structure. *(The pilot harness's job is registered and has ticked
   twice. "Once per harness" means exactly that: this item re-opens
   unspent at every further harness, and the recorded cross-harness intent
   is intent.)*
3. **Declare the seat cadence.** ⬜ *Still owed, and now the sharpest of the
   four.* When the queue gets drained is the
   operator's choice; *that* it has a date is the system's requirement.
   *(The dispatcher now generates seat items on a clock while nothing
   declares when they are read. `operator-queue-2026-08-28` carries a dated
   chase for 2026-09-10 — a chase on the queue, which is not the same as a
   declared cadence for the seat.)*
4. **Stop supplying the middle.** ◐ *Structurally enacted 2026-08-28,
   behaviourally unmeasured.* Getting out of the loop is mostly
   subtraction — stop dispatching by hand, stop pre-empting sessions, route
   understanding-questions into surfaces. The census legitimises the
   not-doing. *(`settled-reasoning-is-standing-authority` converted the
   subtraction from per-instance restraint into a standing grant. Whether
   the behaviour followed the grant is a trend nothing measures yet; the
   plan's own stated metric — operator inputs shifting from explanations
   toward rulings — has no instrument.)*

## Route

- [x] **Phase 0 — Define it.** This document. The goal is written, dated,
      and linked into the graph; the vision can now drift-check its
      restatements against one owner.
- [x] **Phase 1 — The gates census.** *Run 2026-08-27 →
      `gates-census-2026-08`: twenty gate classes, each with a proposed
      verdict — eight consequence-permanent, six designed seats confirmed,
      six familiarity-shaped (four already moved in practice). Ratification
      queued at the operator's next sitting; the Done-When box stays open
      until then.* Walk every point where a session
      currently waits on the operator (the commit stream and the plans'
      human-gated holds are the source material). Classify each:
      consequence-gated (stays, and is named as a seat-3 gate) or
      familiarity-gated (moves to structure, with the mechanism named).
      Output: one small decision per gate, or one batch decision with a
      table — verdicts, not homework. This is the 08c retrospective's
      closing question executed.
- [ ] **Phase 2 — The dispatcher** *(reshaped v1.3, before its design
      session ran: the operator saw the scheduling logic becoming a program
      in itself, and the design commitment landed as
      `a-dispatch-layer-outside-the-corpus-is-a-second-brain` — the schedule
      is things; the second-brain future is refused at birth. The phase
      splits accordingly and shrinks.)*
  - [x] **2a — Declare the schedule (corpus work, agent-runnable now).** A
        design session through the universal workflow produces: the
        estate's operating-schedule declaration (which loops, which radii,
        what cadences — as things), the standing dispatch prompt as a
        versioned `type: prompt`, and the guards as declared state per the
        insight's corollaries (depth, rates, serialization, the dead-man
        trigger) — pointers to the insight, never restatements. Reviewed at
        the push like everything else at the root. *Done 2026-08-27 →
        `dispatch-design-2026-08` (the light traversal and four decisions)
        + `templates/prompts/dispatch-loop.md` (the standing prompt, guards
        in frontmatter). Decision 1 dissolved the central declaration: the
        repos' own triggers are the schedule; the walk is the estate's.*
  - [x] **2b precondition — the derivation gate, met 2026-08-28.**
        `estate-workflow-derivation` (pinned in `informed_by`): every owned
        workflow-definition in the estate now declares its relation to the
        universal workflow, so an unattended session cannot execute an
        *undeclared* process. Honestly bounded — the gate did not ask that
        every declared process be gap-free, and three of the seven carry
        recorded gaps their domains must rule. Two consequences land here:
        the pilot in Phase 4 should avoid a definition with an open gap, and
        the estate's mirror-freshness instrument was found blind
        (`imports-check` coverage 0/101 and 0/43), which matters to any loop
        that will rest on imported state.
  - [x] **2b — Install the tick (adapter work + the one human grant).**
        *Corpus half landed 2026-08-29: `mdllm dispatch-payload` composes the
        launch text read-only (emit, never point), the standing prompt gained
        a `scope` input and the per-repo advisory claim, the digest's home is
        ruled by `dispatch-digest-home-2026-08-29`, and the dead-man is armed
        as this thing's own dated trigger — with its coverage limit stated.*
        **Closed the same day: the operator performed the grant (census row
        7) and registered the job — daily 08:00 Europe/London, scoped to the
        pilot, stop condition stated as work — and the pilot repo declared
        `dispatch-digest` in its own `_schema.yaml`, which was its own act
        as the digest-home ruling requires. The tick is installed and has
        ticked twice.** What 2b does *not* claim: that a launched run
        completes a ritual. That is Phase 4's evidence, and it does not yet
        exist. One further honesty: this single tick was registered **by
        hand** at the host, not generated. The doctor-checked generated-entry
        shape below is therefore owed by any *widening* beyond this one job,
        and is carried forward as a condition on that widening rather than
        left behind as unfinished 2b work — one hand-registered job is an
        install; a hand-maintained fleet of them is the second brain this
        phase refused at birth. The
        outside half is one generated scheduled-task entry per seat —
        written by the adapter pattern, doctor-checked against the declared
        schedule, never hand-authored. It carries no judgment: *start a
        session; the session asks the floor what is due.* Launch discipline
        stays non-negotiable: every automated run carries an exogenous stop
        condition at launch — the loop-optimisation insight's own dismissal
        condition, built in rather than owed; building it promotes that
        insight. The installation grant is the operator's (census row 7).
- [ ] **Phase 3 — The seat protocol.** Define how the system presents work
      at each seat: dissemination briefs that carry options with evidence;
      conflicts that carry proposed directions; approvals as a queue the
      operator drains at their own cadence. The operator reads verdicts and
      options, never raw homework. (Much of this exists piecemeal — orient,
      conflict things, publication debt reports; the phase names the
      protocol and closes the gaps the census finds.)
      *Prototyped by hand 2026-08-28 as `operator-queue-2026-08-28`: three
      tiers, every row carrying a proposed verdict and its evidence, and it
      worked — two Tier-1 rows were ruled in one sitting and one ruling
      collapsed much of Tier 2. What that prototype does **not** supply is
      the protocol: the queue was assembled by a session that happened to
      look, from sources it happened to hold, and nothing regenerates it or
      notices when a row goes stale. Two dispatch runs have since produced
      seat-shaped output (a breakage item, an unsent irreversible) that
      reached the operator through the digests rather than through any
      queue. The phase stays open on exactly that gap — assembly, not
      shape.*
- [ ] **Phase 4 — One full cycle, hands-off, at one radius.** *Pilot ruled
      2026-08-28 (`gates-census-ratified-2026-08-28`): `regulated-qms`, on the
      stated criterion — declared, gap-free, two real runs behind it, one
      closed with attributable acceptance. The dispatcher installs there
      first, tied to a scheduled run in the harness already taking real work
      off the operator. Cross-harness exercise intended immediately after,
      recorded as intent rather than evidence.* Pick a domain
      and run its loop end to end with the dispatcher live: trigger → run →
      outputs → seats. Measure interventions by seat class. Any intervention
      outside the four seats is a defect — route it as a finding into the
      next retrospective, which is the loop debugging itself. *Proposed
      pilot (v1.3): the estate's smallest domain in real weekly use — low
      stakes, live cadence, retrospectives already running; named at the
      ratification sitting, not in this public-root file.*
      **Started 2026-08-29, no cycle yet completed.** The dispatcher is live
      on the pilot and has fired twice; neither run reached a ritual, so the
      cycle count is zero and the intervention-by-seat measurement has no
      data. What the two firings *did* buy is the first real reading of the
      seat classes under automation: run 1 produced one seat-4 breakage
      (generated-index drift in the pilot, since repaired) and run 2
      produced one seat-4 breakage plus one **idled irreversible** — an
      outbound message the run declined to send, which is seat 3 behaving
      exactly as designed. Zero out-of-seat interventions so far, from a
      sample that did no work: the number is true and means almost nothing
      yet, and must not be quoted as if it did.

**Critical path, as of 2026-08-29** *(the 2026-08-27 reading — "the only
human-side blocker is the ratification sitting" — is spent: the sitting
happened, the census was ratified, the grant was given, and the tick was
registered)*: the blocker is no longer human. It is that **no dispatch run
has yet reached a ritual.** Both firings were consumed by preconditions in
the worked repo, one of which the contract has since absorbed (the narrow
generated-artifact repair) and one of which is the pilot domain's own to
supply. Phase 4's evidence begins at the first run that works a fired
trigger and closes its digest having done something; everything downstream
of that — the seat measurements, and Phase 5 — waits on it.
- [ ] **Phase 5 — Seal.** On the census's and cycle's evidence, the seat
      taxonomy and the closed-loop doctrine enter `operating-model.md`
      (operator-gated change to a draft spec expecting exactly this kind of
      convergence). Exposure happens here. Claims stay bounded — routed,
      never eliminated.
      **Judged 2026-08-29: not ready, and the condition is named rather than
      felt.** `operating-model.md` admits doctrine "only on convergence:
      felt independently in more than one live corpus" — its own stated
      razor, which exists precisely to stop a spec growing by design. What
      the last 48 hours produced is one pilot, in one domain, on one host,
      in one harness, whose work path has not executed. That is a *first
      sighting*, not convergence, and a seal taken now would be this spec
      admitting a dimension on the strength of the corpus that invented it.
      **The seal condition, stated so the next session need not re-derive
      it:** the seat taxonomy enters `operating-model.md` when the
      closed-loop shape has been felt in at least one corpus that did not
      author it — a second domain running its own loop and hitting the same
      seat classes, or a second harness exercising the dispatched shape
      (the cross-harness intent already recorded in
      `gates-census-ratified-2026-08-28` as intent, not evidence). Until
      then this plan holds the doctrine and `operating-model.md` stays as it
      is. Recording the non-seal *is* this phase's output for now.

## What This Plan Refuses

- **Autonomy over irreversibles.** No phase moves seat 3 to structure. The
  census may *narrow* it (some gates will prove familiarity in costume),
  but the class is permanent.
- **The completeness claim.** "Mitigated completely" does not survive this
  framework's own doctrine, and a regulated estate rests on that honesty.
- **Automating judgment's content.** The dispatcher schedules invocations;
  it never answers them. Detection mechanical, judgment human — the
  boundary every release this period preserved stays preserved.

## Done When

- [x] The census exists, every gate carries a verdict, and the operator has
      ratified the seat-3 list. *Done 2026-08-28: all twenty verdicts
      confirmed as proposed, no row flipped; the census is `stable`. The
      standing surface is four seats, one push, one feel.*
- [ ] The dispatcher launches at least one loop from its own trigger with a
      stated stop condition, in at least one harness.
      *Half-met 2026-08-29 and deliberately left unticked. The **launch**
      half is evidenced twice: a clock started a session in one harness, the
      stop condition was stated at launch and is refused at composition when
      absent (`mdllm dispatch-payload`), and the payload arrived whole. The
      **loop** half is evidenced zero times: no fired trigger's bound ritual
      has run. The box says "launches at least one loop", and a launch that
      reaches no loop does not tick it. Ticking on the launch alone would be
      the tracking artifact drifting from the reality it tracks.*
- [ ] One radius has run one full cycle with zero out-of-seat interventions,
      or every out-of-seat intervention is routed as a finding.
      *Untouched at 2026-08-29: cycles completed = 0. The two firings are
      not a partial cycle — they are two runs that stopped before the cycle
      began. The "zero out-of-seat interventions" reading of those runs is
      vacuously true and is not evidence for this box.*
- [ ] `operating-model.md` carries the sealed doctrine and this plan's
      remaining content is pointers, not restatements.
      *Judged not ready 2026-08-29 — see Phase 5 for the seal condition:
      the shape must be felt in a corpus that did not author it.*
