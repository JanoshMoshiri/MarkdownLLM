---
id: framework-retrospective-2026-06b
type: retrospective
status: complete
created: 2026-06-19
period_start: 2026-06-11
period_end: 2026-06-19
domain: markdownllm-framework
linked_things:
  - id: framework-continuity-brief
    relation: informs
  - id: framework-retrospective-2026-06
    relation: references
    notes: "The prior retrospective; this one covers the period that opened where it closed (2026-06-11)."
---

# MarkdownLLM Framework Retrospective — Mid-June 2026 (v3.10 → v3.14)

A second June retrospective, not a re-run of the first. The May–June retrospective
(`framework-retrospective-2026-06`) closed its period on 2026-06-11 and produced
the v3-transformation-plan. This one covers the eight days and five sessions
(7–11) since — a stretch dense enough on its own terms to trip both the *volume*
trigger (~12 new insights, five minor releases) and the *milestone* trigger (the
deterministic floor went from scaffold to enforced). It is also the framework's
**first real insight-triage and composition sweep** — the discipline specified in
`session-memory.md` and bound to retrospective cadence, finally exercised.

## What We Were Trying To Do

Take the transformation plan's deterministic floor from "specified" to "load-bearing,"
and clear the two independent-review queues (the third, 2026-06-15; the
mechanical-census fourth, 2026-06-16) by *shipping*, not debating. Three workstreams
ran in parallel: **harden the floor** (change-reconciliation, coherence, touchpoints,
field-registration, doctor hook-freshness); **make the eval discriminate** (a fixture
whose reasoning core can't be answered without the structure); and **make the
framework arrivable by a human** (one-command installer, halved README, guides to
`docs/`). The standing centrepiece behind all of it remained the cold-start eval
with a real non-author human.

## What Worked

- **The floor stopped being a promise.** `mdllm coherence` mechanised the
  generated-artifact freshness and catalog-coherence slice the fourth review named as
  the real gap; field-registration (`known_fields`) closed the silent mis-keyed-link
  hole; `touchpoints` turned the Assimilate beat into one keystroke; `doctor` now
  tests hook *execution* and body-freshness, not presence. The mechanical/semantic
  line was reviewed end-to-end (session 9) and judged sound from the inside.
- **Reviews were actioned as releases, not arguments.** The third review became
  3.8.0–3.11.0; the fourth became 3.12.0. The throughline the reviews named —
  *harvest from where the framework is already proven* — drove the sequencing.
- **The reasoning discriminator finally discriminated.** `sleeping-bag-fac`, with an
  unleakable synthetic rule, produced the clean result the first 2×2 couldn't:
  structure decided the figures (framework 5/5 both models, bare 0/5 both), model
  tier decided only the link convention. The open eval question from the last
  retrospective is closed.
- **The spine held under pressure.** Every new capability this period was framed as
  an *existing* discipline applied, not a new mechanism: workflow run-state as
  decomposition, insight consolidation as composition, reverse-edge indexing as the
  obligation a forward resolver always implied. "The notation changed, not the
  primitives" did real gatekeeping work.
- **The framework began to shrink.** Session 11's three-anchor reframe (substrate vs
  harness) produced a *deletion*: two orchestration prompts removed. After a history
  of answering every gap with more prose, the framework reduced its own surface.
- **Self-application matured.** The continuity brief is now genuinely load-bearing
  for cross-session work, and this retrospective is the first time the triage and
  composition machinery has been run on the framework's own backlog.

## What Didn't Work

- **The disclosable evidence still hasn't been produced** *(corrected 2026-06-19 —
  see note below)*. The cold-start human eval has happened **informally, with the
  author's brother** — but a clean, sourced, *publishable* writeup is not producible
  now and may never be. The gap is disclosable evidence, not the eval itself; the
  framework had been mis-tracking "done but undisclosable" as "undone."
- **A control was defeated, as foreseen.** An opus-bare trial read the withheld
  method from a seed `AGENTS.md` inside the repo (`withholding-is-not-isolation`).
  Correctly kept as a result rather than re-run away — but the isolation hardening it
  implies is specified and still undeployed.
- **The eval is single-shot.** The discriminator result is about information
  availability across one fixture; the *longitudinal* drift-resistance half of the
  thesis — arguably the more important half — remains entirely untested.
- **Domains drifted further behind.** jmtm-software and eco-essentials sit at 3.6,
  property at 2.9, against a framework now at 3.14. The release-cadence-vs-refresh-cost
  tension was named in the last retrospective and is wider now, not narrower.
- **Stale tracking threads outlive the work they describe** *(corrected
  2026-06-19)*. The continuity brief carried the coherence floor as "STAGED FOR PUSH
  on branch `coherence-floor` (not yet on main)" — but that branch was a local-only
  leftover, *fully merged* into main (3.13.0/3.14.0 were built on top of it), and is
  now deleted. The work was never stuck; the *label* was. The real residual drift is
  smaller: `main` is one retrospective commit ahead of `origin/main`, the operator's
  to push.

## Patterns We Noticed

- **The corrective loop reversed polarity.** The May retrospective's sharpest
  self-criticism was that *each failure mode was answered with new prose machinery* —
  the corrective loop amplifying the documented disease (context load). This period
  inverted it: gaps were answered *mechanically and subtractively* — coherence,
  field-registration, and touchpoints each move work off the agent, and the period
  ended by *deleting* two prompts. The framework learned the lesson its own first
  retrospective taught it. This is the single most encouraging pattern of the period.
- **Insights converge into threads, each ending in a synthesis.** The eval thread
  (first-2×2 → mis-keyed → withholding → *structure-decides*), the change-safety
  thread (consistency-at-change → mechanical-assimilation → *defense-in-depth* →
  structural-pointers), the enforcement thread (hook-compliance → hard-hooks →
  *three-anchors*). Each cluster resolves toward a later insight that absorbs or
  supersedes the earlier ones — which is exactly what made this triage tractable.
- **"Deploy when felt" fires mostly off-camera** *(revised 2026-06-19)*. The
  initial read was that the framework defers the same items every session because
  "felt" never arrives. The truer reading, surfaced by the operator: the felt-trigger
  *is* being pulled — inside confidential law-firm work that is the firm's IP and
  cannot enter the public repo. The `workflow-run` primitive's first live use ("a real
  domain, private IP") is the rule, not the exception. So the public repo
  **structurally undercounts deployment**, and the evals are synthetic precisely to be
  a *disclosable proxy* for evidence that exists but can't be shown. Captured as
  `felt-deployment-lands-in-undisclosable-work`. The remaining honest public backlog is
  the disclosable-proxy work (sanitised case study, `limitations.md`), not the
  deployments themselves.
- **The framework keeps catching itself overclaiming.** Model-tier superiority
  demoted (twice), cross-domain linking retracted, the manifesto re-tiered into
  thesis/utility/corollary, the cold-MVP anecdote retired as evidence. A healthy
  reflex — but frequent enough that *evidence-gating should be the default posture
  for any new claim*, not a correction applied after the fact.

## What Should Change

- **Distinguish "undone" from "done but undisclosable" in the tracking.** Per
  `felt-deployment-lands-in-undisclosable-work`: mark privately-exercised threads
  *exercised privately; public artifact unavailable* and stop re-surfacing them.
  Reserve open-thread status for genuinely-undone or disclosable-proxy work. (Push the
  one-commit-ahead `main` to origin when ready — the only real staging residue.)
- **Resolve the two stale `stable` labels.** Coherence flags `llm-driven-systems-manifesto`
  and `session-memory.md` as `stable` but changed within 15 commits. The manifesto's
  v2.4 reword and session-memory's insight-lifecycle additions are structural changes —
  both are candidates for `evolving` (the manifesto label is the operator's call given
  its role as the public thesis).
- **Make the domain-refresh lag a decision, not a recurring lament.** Either a forcing
  function (mechanised refresh is most of the way there) or an explicit, documented
  "domains may trail the framework by N versions; here's when a refresh is owed" policy.
  Two retrospectives is enough to stop treating it as news.
- **Adopt evidence-gating as default claim discipline.** Given the recurring honesty
  corrections, new declarative claims in the manifesto/specs should ship in
  tested-hypothesis framing until an eval supports them — encode the habit rather than
  re-discovering it.
- **Harden stale-WORKLOG as a coherence drift check** (already an open thread): treat a
  stale generated WORKLOG the way coherence treats kernel/index drift. Generalises the
  *existence ≠ currency* candidate.

## Open Questions Going Forward

- **Can the framework's confidential evidence ever be made disclosable — and if not,
  what is the strongest *public* proof it can stand on?** The cold-start eval happened
  privately; the real deployments are client IP. The honest answer may be that synthetic
  evals + sanitised case studies are the permanent public ceiling, and that is fine —
  but it should be a stated position, not a perpetual "todo."
- **What is the longitudinal drift-resistance test?** The thesis's untested half needs
  a multi-session fixture; `sleeping-bag-fac` is reusable as a component.
- **What is the standing domain-refresh policy?** (Feeds "What Should Change" above.)
- **Is `existence ≠ currency` a general enough principle to spec?** It now underwrites
  kernel drift, index drift, hook-body freshness, and stale-WORKLOG — four instances of
  one idea.

---

*Reflexive scans (2026-06-19):*

- **Validate:** clean across all three corpora (framework 69, compliance-patterns 6,
  life-manager 14; 0 Errors / 0 Warnings / 0 Info). No orphaned active insights.
- **Index rebuild:** no derived indexes deployed in the framework domain except
  `provenance` (in sync, coverage 3); nothing to rebuild.
- **Coherence:** two Info findings only — the stale `stable` labels above. No catalog,
  kernel, or `foundational_specs↔filesystem` drift.
- **Conflict scan:** no new standing contradictions surfaced. The one supersession
  (first-2×2 → structure-decides) is a resolved progression, not a held conflict.
- **Insight triage:** 28 active insights walked. **Promoted 3** —
  `mis-keyed-links-pass-the-floor-silently` (→ field-registration in `validate.thing.md`),
  `workflow-run-is-the-decomposition-principle-applied-to-processes` (→ `workflow-state.md`,
  now evolving), `operative-rules-are-a-small-fraction-of-spec-prose` (→ `framework-kernel`).
  **Dismissed 2** — `continuity-briefs-solve-external-state-drift` (claim overtaken;
  the heuristic survives in `session-memory.md`) and
  `first-2x2-measured-convention-following-not-reasoning` (superseded by
  `structure-decides-figures-scale-decides-convention`). 23 remain active, each a live
  razor or open-question carrier.
- **Composition pre-filter:** the mechanical ≥2-shared-target scan flagged the
  change-safety cluster (`change-safety-is-defense-in-depth`, `mechanical-assimilation…`,
  `structural-pointers…`, `consistency-is-maintained-at-change…`). Agent judgement:
  *relate, don't merge* — these are distinct facets (meta-frame, dark-region tier,
  lit-region sibling, foundational principle) that already cross-link correctly. The one
  genuine consolidation was the eval thread's first-2×2 → structure-decides supersession,
  handled above.

---

*Correction note (2026-06-19, same day):* immediately after this retrospective was
first written, the operator's review corrected three findings that had rested on stale
continuity-brief threads. (1) The `coherence-floor` branch was not staged work awaiting
a push — it was a local-only leftover fully merged into `main`, now deleted. (2) The
cold-start human eval had already happened informally (the operator's brother); only a
*disclosable* writeup is outstanding. (3) The recurring "deploy when felt" deferrals are
largely felt inside confidential law-firm work (client IP) invisible to the public repo.
The affected sections above were revised in place and the realisation captured as
`felt-deployment-lands-in-undisclosable-work`. The meta-finding stands and is sharpened:
the framework's *tracking* drifts stale faster than its *work* does — which is exactly
the class of problem a retrospective exists to catch.
