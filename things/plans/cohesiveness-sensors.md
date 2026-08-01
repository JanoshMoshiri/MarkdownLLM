---
id: cohesiveness-sensors
type: plan
status: not-started
version: 1.0
created: 2026-08-01
priority: high
tags: [cohesiveness, drift, floor, sensors, estate, self-describing, awareness]
linked_things:
  - id: divergence-is-an-unrouted-decision
    relation: implements
    notes: "Every sensor here is the divergence primitive given eyes on the self-describing axis — the domain's own definition surfaces (kernel, skills, schema, plans, READMEs) treated as a model that diverges from the reality of usage. New sensors, zero new machinery: detection stays in the floor, routing stays with the agent, deciding stays with the operator."
  - id: mechanical-coherence-checks-backlog
    relation: complements
    notes: "Same gate, same instinct, wider aperture. The two live items there (broken-body-reference, install-hook self-test) stay theirs; this plan does not absorb them."
  - id: judgement-checks-need-a-suppression-list-which-is-itself-drift
    relation: references
    notes: "The admission gate for every sensor in Phase 2: if a check can only stay quiet via a hand-maintained allow-list, it is judgement in mechanical clothing and does not ship. Each sensor below is keyed to a same-builder source."
  - id: a-check-that-always-fires-teaches-the-operator-to-ignore-it
    relation: informs
    notes: "The awareness failure mode this plan must not reproduce: twelve domains of new Info landing at once trains the operator to skim. Sensors must be quiet-when-healthy and ranked-when-loud; the version-MISMATCH line that was surfaced for sessions and never acted on is the proof this matters."
  - id: a-ruling-triages-more-cheaply-than-a-mechanism
    relation: informs
    notes: "Phase 1 routes the live divergences by ruling before Phase 2 builds anything; several sweep findings resolve as rulings (prune, park, accept) and need no sensor at all."
  - id: assistant-register
    relation: complements
    notes: "The delivery surface of awareness. This plan makes session-start and the floor *see* the divergences; assistant-register owns how they are *said*. The boundary: mechanical evaluation lands here, register and rendering land there."
---

# Cohesiveness Sensors — the self-describing axis gets eyes

## The finding (estate sweep, 2026-08-01)

A full-estate sweep — twelve domains plus the framework root, ~660 things —
found that every class of drift the operator had been fixing by hand is a
divergence between a *definition surface* and the reality it models: kernel
prose vs schema, skills vs usage, README vs current state, plan status vs
shipped code, `framework_version_seen` vs the sentinel. The framework routes
divergences diligently on the data axis (imports-check, refresh, the kernel
managed blocks, coherence on generated artifacts). On the self-describing
axis — the fractal claim that definitions are things too — it has almost no
sensors. The sweep's specific findings:

- **The floor is silent where the specs already define findings.** The
  quarantine-age Info (`provenance.md` §Validation, external + unverified
  >30 days) and the retrospective-age Info (`retrospective.md`, 60+ active
  days without one) are specified and unimplemented. 319 things in the
  regulated deployment validate 0/0/0 while carrying both conditions.
- **Nothing detects an unfilled scaffold.** Two domains ran real sessions on
  skill files that were verbatim templates; the regulated deployment fixed
  the same class across five domains only 72 hours before the sweep, by
  hand, its own commit naming the failure mode. The only signal ever emitted
  is one line printed at scaffold time.
- **Session start does not evaluate triggers.** `trigger-specification.md`
  calls session start the primary evaluation point; `orchestration.md`, the
  generated domain kernel (step 6), and the operator guide all assert it;
  the default emitter never imports the triggers module. Only the Phase 0
  `--assistant` path does.
- **The generated kernel instructs every domain to run prompts scaffold
  never delivers** — `templates/prompts/` is copied into no domain.
- **Every scaffolded domain is born without hard hook 4** — the scaffolded
  settings and the adapter example omit estate-sync, and the kernel
  generator's hooks block lists three of four (inconsistent with its own
  session-start block).
- **The ingestion triple is spec-mandated and tool-read but registered
  nowhere** — not in CORE_FIELDS, not in the schema template; a domain that
  adopts the framework's own fields gets flagged for them.
- **Authored kernel prose lags the schema wherever the domain is active.**
  §Thing Types understates the corpus in most working domains; the
  harness-loaded surface is the least-checked surface.
- **Version currency is bimodal and the propagation channel is the laggard.**
  Refresh works when run; six domains sat 5–9 versions behind, one of them
  hard-blocked at the commit boundary by kernel-block drift that doctor
  misattributed to hook failure. The MISMATCH line was surfaced every
  session and never acted on — awareness buried in ritual noise is not
  awareness (the assistant-register finding, confirmed estate-wide).
- **Over-specification is as common as under-specification.** Three domains
  carry detailed machinery (types, pipelines, gate vocabularies) that usage
  never demanded — predicted structure, against the manifesto's emergent-
  detail principle. Prose triggers estate-wide with almost no `triggers:`
  blocks; sixteen declared relationship triggers inert with unfilled
  `on:`/`watch:`.

## Constraints (the ethos, pinned)

1. **Loosely coupled, tightly cohesive.** Every sensor reads local committed
   state only. No domain gains a dependency on another or on framework
   internals; cross-domain stays porch-only. Nothing here binds domains
   tighter to anything.
2. **Detection is the floor's; routing is the agent's; deciding is the
   operator's.** All new findings are advisory (Info, Warning at most) —
   never blocking. Awareness is the engine; the route stays a decision.
3. **Every sensor passes the suppression-list gate.** Keyed to a
   same-builder source or it does not ship.
4. **Quiet when healthy.** A sensor that fires on every domain every session
   is a defect, not a feature.
5. **Discovery, not invention.** No new primitive, no new ceremony — the
   existing divergence discipline applied to surfaces it already claimed to
   govern.
6. **Over-spec is as findable as under-spec.** Prune-or-park is a
   first-class route, not an admission of failure.

## Phase 1 — Estate repair pass (route what is live)

The sweep's per-domain findings were delivered in-session; each repair is a
routed divergence committed in the *owning* repo — this plan tracks only the
classes. Order of felt-ness:

- [ ] **Unblock the commit-blocked domain**: regenerate its domain-kernel
      block and commit. Separately, route its one DIVERGED cross-domain
      import as an inflection — restore or revise, with the rationale
      recorded, never silently re-pinned.
- [ ] **The two stub-skill domains**: route each — fill from earned insights
      where sessions have run, or park the domain explicitly. Never fill
      from the birth-day description (the regulated deployment's lesson:
      skills harvested from insights held; skills written from a stated
      scope reproduced the gap).
- [ ] **Refresh debtors** (five domains, seen 3.14–3.17.5): refresh
      adopt → seal; backfill pre-v3.20 artifacts (boundary file, gitignore)
      where scaffold predates them.
- [ ] **Status-vocabulary reconciliation** in the domain whose skills
      disagree with its schema on every type — a latent commit-blocker;
      revise the skills to the schema (the schema is the ruled surface).
- [ ] **Inert relationship triggers** (16): the regulated deployment already
      owns this as its trigger-vocabulary repair plan's final phase —
      execute there, not here.
- [ ] **Route the aged `framework_promotion: candidate`** sitting 31 days
      unrouted in a meta domain (observation-is-a-distribution claim):
      accept into the framework or decline with rationale.

## Phase 2 — Floor sensors (tool-level; propagate estate-wide on ship)

Each sensor names its same-builder source. Build in this order; each is
independently shippable.

- [ ] **Quarantine age** (`validate`, Info): `origin: external` +
      `verified: false` older than 30 days. Source: the thing's own
      frontmatter. Already specified in `provenance.md`.
- [ ] **Retrospective age** (`validate`, Info): domain with commits in the
      last 60 days and no `type: retrospective` in 60+. Source: git log +
      corpus. Already specified in `retrospective.md`.
- [ ] **Template residue** (`coherence`, Info): a `type: skill` thing whose
      body retains literal placeholder tokens shipped in `templates/`
      (`[Name]`, `[List and briefly describe…]`, …). Source: the template
      set — same-builder by construction; no suppression list possible.
      The finding reads "scaffolded, never authored", not "bad skill".
- [ ] **Incomplete trigger declarations** (`validate`, Warning): a
      `relationship` trigger with unfilled `on:`/`watch:` is structurally
      incomplete — a schema-shaped fact, not a judgement. `triggers` already
      computes this; today it is only visible to whoever runs the
      subcommand.
- [ ] **Session-start evaluates triggers on the default path.** The
      spec-mandated primary evaluation point, mechanically. Phase 0 of
      assistant-register proved the code path; this fold-in is evaluation
      only — rendering and register stay assistant-register's.
- [ ] **Index anchor integrity** (`index check`): `generated_from` must
      resolve; flag `framework_version` staleness on index things — the
      mirror of the check `coherence` already runs for examples. (The
      provenance index currently reports "in sync" over a dangling anchor.)
- [ ] **Doctor truthfulness**: attribute a pre-commit exit 1 to the failing
      check's own report, never "hook failed to execute".
- [ ] **Emitter hygiene**: the two remaining `subprocess` calls in
      `session.py` gain explicit UTF-8; the phantom `--why` leaves the seed.
      Candidate (gate applies): a coherence guard that flags flags named in
      generated prose but absent from the CLI surface — if it needs an
      allow-list, drop it and rely on review.
- [ ] **§Thing Types promoted to a generated block**: derived from
      `_schema.yaml` plus a usage census — repeated drift promotes a fact
      into the floor, and this fact drifted in five-plus domains. Fallback
      if the managed block proves over-mechanism: a coherence set-difference
      check. Decide at build; record the ruling either way.

## Phase 3 — Birth surfaces (future domains born whole)

Existing domains pick these up through refresh; that is the designed channel
and Phase 2's sensors are what make the channel felt.

- [ ] `scaffold` copies `templates/prompts/` — the kernel names four of them
      as session-start steps.
- [ ] Scaffolded `.claude/settings.json` and the adapter example gain
      estate-sync ahead of session-start; `_FRAMEWORK_HARD_HOOKS` in the
      kernel generator gains hook 4.
- [ ] Ingestion-triple fields (`source_system`, `source_ref`,
      `source_checked`, `source_hash`) enter CORE_FIELDS and the schema
      template's `known_fields`.
- [ ] `domain-refresh.md` gains the explicit backfill step for pre-v3.20
      domains (boundary file, gitignore).

## Phase 4 — Spec reconciliation (prose catches up with shipped reality)

- [ ] **`interface.md`** — 64 days stale, the oldest foundational spec; it
      predates the porch entirely. Gains the membrane/face as an output
      route. The Response Register section stays assistant-register's; this
      plan only ends the file's silence about surfaces that shipped.
- [ ] **Manifesto §Composability** still says the cross-domain hand-off is
      "foreseen but not yet specified" — it shipped (v3.22–v3.23). Revise
      with rationale; route 2, recorded.
- [ ] **Operator-guide toolbox** — 4 of 23 subcommands undocumented.
      Candidate mechanical check: extend the existing count check to
      per-command coverage (gate applies).
- [ ] **`domain-specification-guide.md`** names the prune-or-park route for
      declared-but-never-used machinery — emergent detail cuts both ways,
      and the honest route for predicted structure is often to remove or
      explicitly park it, not to manufacture usage.

## Exit

- Each of the sweep's failure classes — unfilled scaffold, silent
  quarantine/retrospective aging, prose-only awareness, born-incomplete
  domains — has either a floor sensor that would have fired or a recorded
  ruling that it stays semantic.
- A re-run of the 2026-08-01 sweep finds no divergence class without a
  sensor or a ruling.

**Ordering:** Phase 1's first item is felt now and goes first; the rest of
Phase 1 is operator-paced. Phase 2 is the leverage — one implementation,
estate-wide propagation — and can start immediately after the unblock.
Phase 3 rides the next scaffold and the refresh channel. Phase 4 lands with
the next spec pass. Deploy-when-felt is satisfied throughout: every sensor
maps to a divergence that actually occurred, this week, in this estate.
