---
id: estate-cadence-cluster
type: plan
status: completed
version: 1.4
completed: 2026-08-04
created: 2026-08-04
priority: high
tags: [estate, autopush, publication, retrospective, cadence, vantage, multi-domain]
linked_things:
  - id: estate-git-sync
    relation: complements
    notes: "The pull side shipped there (v3.22.0) with autopush explicitly deferred: 'until a collaborator exists (deploy-when-felt)'. This plan lifts that hold — the release condition arrived in a different costume. Phase 1 is the push side of the same machine axis."
  - id: cohesiveness-sensors
    relation: complements
    notes: "The retrospective-cadence sensor was born there (v3.24.0, validate, 60+ active days). Phase 2 does not add a sensor; it moves the existing one's surfacing to the moment and altitude where it can be acted on."
  - id: premature-publish-manufactures-discipline-eroding-urgency
    relation: references
    notes: "The standing counter-argument to any automatic push, engaged head-on in Phase 1's carve-out: that insight's publish is a release event on a judgement surface; autopush transports floor-validated commits to estate remotes. The framework root's public repo stays a deliberate publish."
  - id: divergence-is-an-unrouted-decision
    relation: implements
    notes: "A rejected push is a divergence surfaced, never resolved — the same discipline estate-sync applies to DIVERGED on the pull side, applied on the push side."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: informs
    notes: "Why the push leg never forces and why the public release surface keeps the human: transport of committed state is recoverable; overwriting a remote or publishing a release is not."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: informs
    notes: "Phase 2's constraint: cadence debt must arrive quiet-when-healthy and rolled-up-when-loud, or it trains the operator to skim it exactly as the validate-time warning already has."
  - id: change-reconciliation-specification
    relation: implements
    notes: "v1.1: the deep dive (2026-08-04) reframed this plan as that spec's missing half — Phases 2/3 are the net-beneath-the-net given a clock, Phase 4 is the cue question made mechanical. The build itself is an inflection and commits to running the four beats on itself."
  - id: autopush-requires-explicit-authority
    relation: references
    notes: "Supersedes only this completed plan's default-on publication ruling; the historical build record below remains unchanged."
  - id: inflection-candidates-are-computable
    relation: implements
    notes: "Phase 4's first half is this insight built."
  - id: a-generated-surface-collapses-its-walk
    relation: references
    notes: "Found by running this plan's own Assimilate beat; Phase 4's release-walk half exists because the authored share of the doctrine's ~15 restatements needs a walk, and the walk needs a beat in the release ritual."
---

# Estate Cadence Cluster — publication becomes mechanical, retrospection gets a clock

> **Current doctrine (reconciled 2026-08-20):** this is the historical build
> record for v3.27. Its default-on ruling was later superseded by
> `autopush-requires-explicit-authority`: standing automation remains, but only
> literal `git.autopush: true` authorises a send. The completed retrospective,
> cue, and release-walk work remains current.

## The finding (operator, 2026-08-04)

The estate crossed a dimension line — expected and planned, but now felt.
Work is multi-domain within a single day; domains consume each other's
porches; the same operator is the "collaborator" the v3.22.0 hold was
waiting for, arriving as himself across machines, cloud sessions, and
cross-domain sessions. Two single-domain-era assumptions no longer carry:

1. **Publication as a deliberate act.** In one working day the operator
   overrode the no-push rule repeatedly because unpushed commits had
   become invisible estate state — `imports-check` cannot see them,
   `estate-sync` cannot deliver them, and a consumer polling a face reads
   a past that the producer has already moved beyond. v3.22.0 named the
   principle that decides this: *the commit makes state real on the
   machine that made it; publication makes it real to the estate — and
   orientation reads the estate.* Once orientation reads the estate,
   holding publication back by default is withholding state from the
   thing that orients on it.

2. **Retrospection bound to operator memory.** The v3.24.0 cadence sensor
   exists but fires in `validate` — mid-commit, the moment of least
   receptivity — and per-domain, so at thirteen domains the debt arrives
   as scatter, never as a picture. Retrospectives are not happening, and
   the operator noticing that *is* the sensor working at the wrong
   surface: it reached him through feel, not through the floor.

And one thing the estate already discovered without naming it: the
vantage domain authored `estate-membrane-assessment-2026-08-04` — eleven
findings, seven unmade calls, from the cross-domain vantage. That is an
estate retrospective in everything but type declaration. Discovery, not
invention: the primitive exists in practice; this plan describes it.

## Operator rulings already made

- **Autopush is default-ON with per-domain opt-out** (ruled 2026-08-04,
  voice). Reasoning: the opt-out set is the small one — most usage wants
  captured state published. Absence of config means on; a domain that
  must not push declares `git: autopush: false` and owns that declaration.
- **Build the plan first, talk before executing** — honoured; the talk
  happened 2026-08-04 and closed with "let's go ahead with the plan."
- **Decision points 1-5 ruled 2026-08-04 (operator, voice: "I concur with
  all your reads"):** (1) configs corrected to reality — the config's job
  is to describe the branch that exists; (2) the push leg lives in the
  hook body — a load-bearing mechanism must not depend on which harness
  is present; (3) 60 active days for domain retrospectives, 30 for the
  estate; (4) the first formal estate retrospective is authored fresh,
  the membrane assessment keeping its provenance as the discovered
  instance; (5) the direct-read licence is written into the
  estate-retrospective's definition.

## Phase 0 — pre-flight: the branch truth

Autopush inherits whatever lies the config already tells. Two are known:

- **Six domains sit on `master` while their AGENTS.md declares
  `git: branch: main`** — the affected set is recorded estate-side, not
  here. The push
  leg must push the *actual* current branch to its upstream — never the
  declared one — and this mismatch should be reconciled (update the
  config to the truth, or rename the branches) before a mechanism starts
  acting on it. A mechanism built on a lie mechanises the lie.
- **One domain has no remote.** Default-on must degrade to a
  single advisory (estate-sync already reports `local-only`), not a
  per-session nag and never an error. No-remote is a legitimate standing
  state — the estate-sync status report is where it stays visible.

## Phase 1 — the push leg (lifts the v3.22.0 hold)

**Config semantics.** `git: autopush: false` in domain AGENTS.md
frontmatter opts out; anything else — including absence — is on. The
judgement moves to configuration time (which domains opt out); the act
becomes mechanical. This is the same shape as every hardening the
framework has done.

**Mechanism.** The `post-write:commit` hard hook gains a push leg where
autopush is on: after the commit lands and the pre-commit floor has
validated it, push the current branch to its upstream. Push is *transport
of already-committed, already-validated state* — the mirror of
estate-sync's fast-forwards, which are safe for exactly the same reason.

**Degrade semantics — surfaced, never resolved.**

- Offline / auth failure → advisory line, session continues; the commit
  stands as publication debt and `estate-sync --status` shows it.
- Rejected push (remote moved) → this is DIVERGED on the push side: an
  unrouted decision. Surface it, never pull-rebase-retry, never force.
  The operator routes it.
- **Never `--force`, structurally.** Overwriting a remote is
  consequence-unrecoverable; it stays outside the mechanism's vocabulary
  entirely.
- Bounded like estate-sync: `GIT_TERMINAL_PROMPT=0`, timeout, degrade to
  advisory. A push must never hang a session.

**The serve-side advisory (v1.1, from the deep dive).** The consume side
has a tool (`imports-check`); the serve side has only discipline — a
change to an `exposed: true` thing has no mechanical voice, and autopush
makes that silence faster-moving. Phase 1 therefore ships a companion
sensor: when a commit modifies a thing carrying `exposed: true`, one
advisory line — *this thing is on the porch; this change publishes*.
Quiet otherwise. This converts autopush's sharpest risk into its own
sensor, and closes the one membrane direction that had no eyes.

**The publication-debt report inverts.** Under autopush, `estate-sync
--status` stops being a to-do list and becomes an anomaly detector: any
`ahead +n` now means something went wrong (offline session, rejected
push, opt-out domain with unpublished work). Quiet when healthy.

**The carve-out — the public release surface keeps the human.**
`premature-publish-manufactures-discipline-eroding-urgency` stands
unrevised: the framework root's public repo is a *release* surface —
pushing there is a version event consumed by outsiders, gated by
judgement (reconciliation, changelog, version), and it has no mechanical
completeness gate the floor can check. Domain autopush transports
floor-validated working state to estate remotes read by the operator's
own orientation. The two are different acts that happen to share a verb.
The framework root therefore ships with `git: autopush: false` — the
default-on rule applied honestly, as an opt-out the root itself declares.

**Doctrine revision, recorded as a decision thing at build time.** The
v3.22.0 line "the push stays the human's deliberate act" is revised, not
deleted: the *deliberate act* moves up one level, from each push to the
per-domain autopush declaration and the routing of every non-clean push
outcome. The decision thing records why the protection the old line gave
(publication as judgement) is preserved at the new level and on the
release surface.

## Phase 2 — retrospective cadence surfaces where it can be acted on

**Why this is load-bearing, not hygiene (v1.1).** Change-reconciliation's
robustness model routes every missed cue to the retrospective: "the same
backward pass runs periodically — bound to the retrospective hook — as
the net beneath the net." A cadence that exists only in operator memory
means the net beneath the net is down exactly when the cue-missing rate
is highest. This phase is that spec's dependency being paid, not a
freestanding nicety.

Zero new sensors. The v3.24.0 cadence check (60+ active days, young and
dormant domains silent) gains two surfacing points:

1. **Session start.** The attention surface at t=0 — where orientation
   already says what needs the user — reports retrospective debt for the
   domain being entered. One line, quiet when healthy.
2. **`triggers --estate` roll-up.** The estate sweep reports cadence debt
   across all clones — one line per overdue domain, one place, so the
   debt arrives as a picture instead of scatter. This is the surface the
   operator's weekly estate loop already reads.

The validate-time warning stays (it is the durable floor anchor) but is
no longer the *only* voice — mid-commit was the wrong moment, and the
operator learning to scroll past it was
`a-check-that-always-fires-teaches-the-operator-to-ignore-it` in action.

## Phase 3 — the estate retrospective is named, not built

The estate's vantage domain (the pattern generalises to any vantage)
already authors cross-domain
assessments. Formalising costs almost nothing because every part exists:

- An estate retrospective is a **`type: retrospective` thing authored in
  the vantage domain** whose scope is the estate.
  `estate-membrane-assessment-2026-08-04` is recognised as the first
  instance in practice; the first formal one declares the type.
- **Cadence is a dated trigger** on a thing in the vantage domain —
  mechanically evaluable since v3.21.0 (embedded ISO dates fire), so the
  floor chases the next one instead of the operator's memory.
  Human-gated waits: date the chase.
- **Per-domain retrospectives feed it**, completing the symmetry the
  system already half-has: session-end harvests a session; a domain
  retrospective checks a domain's epoch; the estate retrospective checks
  the estate's. Each layer consumes the layer below.
- **Boundary, kept from the vantage domain's own kernel:** the estate
  retrospective observes across domains but *rules* only on what is
  genuinely cross-domain. Per-domain findings travel home through the
  porch as imports/briefs — the vantage never becomes everyone's editor.

## Phase 4 — the cue question and the release walk (accepted 2026-08-04, operator, voice)

From the deep dive: the substrate's reconciliation channels are strongest
exactly where they are mechanical (membrane: imports-check + quarantine;
framework→domain generated blocks: regen) and weakest where the cue is
purely human (domain-internal edits to reasoned-from things; the
framework's own internal corpus, where the pass has never formally run).
Two additions, both detection-only:

1. **The cue-candidate advisory.** At commit, a *modified* (never added)
   thing that is reasoned-from — inbound edges above a threshold, or a
   definition-surface type — gets one line: fan-in count plus the
   `mdllm touchpoints <id>` invocation. The cue verdict stays human;
   the question stops being skippable. Saying no to a named question is
   a decision, where not being asked was drift.
   (`inflection-candidates-are-computable`.)

2. **The release walk.** The framework release ritual gains an explicit
   Assimilate/Walk beat: for the surfaces a release changes, run
   `touchpoints`, run the textual tier **estate-wide over local clones**
   (the repos-not-membranes precedent licenses the read), walk the
   authored touchpoints, and let the CHANGELOG entry record the walked
   set. The first live run of this beat — on this plan's own autopush
   inflection — found ~15 restatements of the push doctrine across four
   layers, 13 of which collapse to one generator string
   (`a-generated-surface-collapses-its-walk`); the authored remainder is
   the walk the release ritual currently has no slot for.

Standing principle for both, and for the corpus generally: **prefer
derived restatements over authored ones; promote a restatement into
derivation when a walk revisits it twice.** The walk should get cheaper
as the corpus ages.

## Decision points held for the pre-execution talk

1. ~~Branch reconciliation~~ — ruled: configs to reality (see rulings).
2. ~~Push-leg location~~ — ruled: hook body (see rulings).
3. ~~Cadence numbers~~ — ruled: 60d domain / 30d estate (see rulings).
4. ~~First estate retrospective~~ — ruled: authored fresh (see rulings).
5. ~~Direct-read licence~~ — ruled: written into the definition (see
   rulings).
6. ~~Does Phase 4 belong in this cluster, or split into its own plan?~~
   Resolved 2026-08-04: accepted in place, in this cluster (operator,
   voice — "this all sits very well, in everything"; the fractal reading
   was the operator's own: the same primitive — floor surfaces, driver
   decides — applied at commit, membrane, and epoch radius).

## Build record (2026-08-04, v3.26.0)

Shipped in one release, all four phases plus the pre-flight. Success
criteria verified live at rollout: thirteen domains sealed 3.26.0 and
published themselves through their own post-commit hooks (twelve
`published`, one silent local-only — correct); the publication-debt report
shows exactly one line, the framework root's own +8, which is the release
surface behaving as its opt-out declares; the cue advisory's first firing
was the release commit itself, flagging the two modified definition
surfaces the walk had already covered; the retrospective clock's first
estate sweep flagged one genuinely overdue domain and silenced the young
rest; and the first formal estate retrospective is chased by a dated
trigger (2026-09-03) in the vantage domain. The walked set (~15
touchpoints, 13 collapsed by one generator edit) is recorded in the
CHANGELOG entry per the release-walk beat this plan itself introduced.

## Success criteria

- A session that commits in any opted-in domain ends with the estate
  seeing that state, with zero operator pushes and zero overrides asked.
- `estate-sync --status` reads clean at session end on a healthy day, and
  anything it shows is genuinely anomalous.
- No session start passes a retrospective-overdue domain silently, and
  the estate sweep shows the debt as one picture.
- The next estate retrospective exists because a trigger fired, not
  because the operator remembered.
