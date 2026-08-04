---
id: estate-cadence-cluster
type: plan
status: not-started
version: 1.0
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
---

# Estate Cadence Cluster — publication becomes mechanical, retrospection gets a clock

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
- **Build the plan first, talk before executing** — this plan's
  `not-started` status is that ruling recorded.

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

## Decision points held for the pre-execution talk

1. Phase 0 branch reconciliation: rename branches to `main`, or update
   the six configs to say `master`? (The truth-telling fix differs from
   the tidy fix.)
2. Does the push leg live in the hook body (git-fs anchor, works
   everywhere) or the harness adapter (interpretation anchor, richer
   reporting)? The pull side chose the adapter; symmetry argues for the
   same, but a hook-body leg would survive harness absence.
3. Retrospective cadence number: is 60 active days right now that
   domains are this active, or does the estate retrospective want its own
   (shorter?) clock than domain retrospectives?
4. Should the first formal estate retrospective be authored fresh, or is
   the membrane assessment retro-typed (its findings are three days old
   and partly acted on)?

## Success criteria

- A session that commits in any opted-in domain ends with the estate
  seeing that state, with zero operator pushes and zero overrides asked.
- `estate-sync --status` reads clean at session end on a healthy day, and
  anything it shows is genuinely anomalous.
- No session start passes a retrospective-overdue domain silently, and
  the estate sweep shows the debt as one picture.
- The next estate retrospective exists because a trigger fired, not
  because the operator remembered.
