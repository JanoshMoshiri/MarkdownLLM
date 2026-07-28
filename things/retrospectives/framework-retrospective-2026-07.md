---
id: framework-retrospective-2026-07
type: retrospective
status: complete
created: 2026-07-28
period_start: 2026-06-25
period_end: 2026-07-28
domain: markdownllm-framework
linked_things:
  - id: framework-retrospective-2026-06d
    relation: references
    notes: "Prior retrospective (2026-06-24). This covers the month after: v3.16 through v3.23 — the arc where the framework's primitives crossed the domain boundary."
  - id: estate-git-sync
    relation: references
  - id: membrane-attention-cluster
    relation: references
  - id: cross-domain-sync-catchup
    relation: references
  - id: divergence-is-an-unrouted-decision
    relation: references
  - id: source-behind-mirror-is-still-a-consumer-side-read
    relation: references
  - id: origin-external-conflates-ingestion-with-import
    relation: references
    notes: "Evidence-gated in v3.21.0; gate satisfied and shipped in v3.23.0 — the cleanest promote-on-evidence arc the insight machinery has produced."
  - id: a-true-primitive-is-discovered-not-authored
    relation: supports
    notes: "The month's central test, passed: every estate mechanism was an existing primitive re-read at the membrane; zero new ontology."
---

# Framework Retrospective — July 2026: The Estate Month

The period after `framework-retrospective-2026-06d`: v3.16 → v3.23, ~140
commits. The through-line, visible only in hindsight, is one sentence: **the
framework learned that everything it knew about a domain also applies between
domains — and where it deliberately doesn't.** Early July hardened the single
domain (verified-flip discipline, floor-not-installed detection, terminal
statuses, the disclosure boundary); late July applied the same laws to the
inter-domain surface (DIVERGED, estate-check, the machine axis, face
coverage, import triggers, the producer-blindness ruling). Every late-July
mechanism was driven by a felt operator problem, and three shipped versions
landed in a single day (v3.21–v3.23, 2026-07-27/28) without a floor breakage.

## What We Were Trying To Do

Make multi-domain, multi-machine operation as trustworthy as single-domain
operation already was: syncing without toil, attention signals that actually
fire, membrane state that cannot silently read as healthy, and a written
ruling on the estate's most tempting wrong turn (producer-side
instrumentation).

## What Worked

- **Felt-first sequencing.** Nothing this month shipped ahead of its pain.
  The sync toil was felt before estate-sync; the fired-unseen trigger was
  found before `type: import`; the ingestion insight waited at its evidence
  gate until an *independent* review hit the same wall — then shipped the
  same week. Deploy-when-felt is now demonstrably the operating rhythm, not
  an aspiration.
- **The floor defended its own construction.** During the v3.22/3.23 builds
  the pre-commit hook blocked a stale kernel once and the boundary hook
  blocked private names twice (a commit message, then spec examples). The
  mechanism being built was policed by the mechanisms already built —
  the strongest live evidence yet for hardening-at-the-boundary.
- **Discovery-not-invention held under pressure.** The estate surface was
  the biggest temptation yet to mint new ontology (registries, subscriber
  lists, shared work ids, an estate manifest). All were refused; every
  shipped mechanism is an existing primitive re-read at the membrane:
  commit-is-real gained a scope qualifier, quarantine gained a second
  species, triggers gained a state source the floor already computed,
  batching stayed a walk. The one new noun — "estate" — never became a
  thing, an index, or a file.
- **The ruling-first pattern.** Writing producer-blindness down as doctrine
  *before* building (provenance.md → The Membrane's Direction Is a Ruling)
  turned six proposed fixes into three clean builds and three reasoned
  rejections. Cheapest triage this framework has done.

## What Didn't Work

- **The reconciliation set keeps missing the second copy.** Today's
  orchestration.md network-rule amendment missed the parallel passage in
  domain-refresh.md — found hours later by this retrospective's conflict
  sweep, the exact `repeated-drift-promotes-a-fact-into-the-floor` class,
  again. The fact is now stated in two sharpened copies; a third occurrence
  earns the fact a single home.
- **The boundary ruleset shipped with test vocabulary in it.** The first
  history audit ran permanently red on `client-x/y/z` — the floor's own
  synthetic test terms, left in the local terms file from live-testing. A
  red that always fires trains the operator to ignore red; term selection is
  part of the mechanism's correctness, not operator garnish.
- **Spec `stable` labels churn during fast arcs.** git-workflow and
  trigger-specification both changed within the coherence window this month
  and were Info-flagged. Disposition: both labels **stand** — the changes
  were additive sections, not revisions of settled claims — but a
  three-versions-in-a-day cadence sits awkwardly under a label meaning
  "validated through real-world use." The honest reading: the *new sections*
  are days old; watch them.

## The Two Spaces — What Each Teaches the Other

The operator's question this retrospective exists to answer: intra-domain
and inter-domain practice are now both instrumented — what transfers?

**Inter → intra (learned at the membrane, applies at home):**

- **Coverage honesty.** The estate taught that a report must state what it
  could *not* check (COVERAGE n/m, face coverage, ingested clocks). The
  intra-domain floor already had the lesson in one place (triggers'
  not-evaluable list) but not as a law. Candidate rule for any future check:
  *every floor report carries its denominator and its blind spots.*
  `coherence`'s prose-only dark region is the next candidate — it names the
  residue in docs but not in its own output.
- **The staleness clock.** `source_checked` gives ingested mirrors a
  re-check cadence. Intra-domain, `verified: true` is a point-in-time fact
  with no re-verification clock — a verified thing from May carries the same
  authority as one verified yesterday. Open question below; not a build.
- **The dated chase-by** was found on estate triggers but is domain-general
  — any human-gated wait anywhere. Already promoted to a framework pattern;
  the framework repo's own plans should adopt it (estate-git-sync's queued
  autopush conversation is itself an undated wait on the operator).

**Intra → inter (domain laws that extended cleanly):**

- **Commit-is-real** → publication debt (the machine axis is the same law
  with a scope qualifier).
- **Quarantine-then-verify** → the reference triple and re-quarantine-on-
  drift; unchanged in spirit, extended in reach.
- **The one deliberate asymmetry: derived indexes stop at the membrane.**
  Inside a domain, an index is a regenerable convenience within one trust
  zone. Across domains it becomes a fact held outside its owner — so the
  estate gets walks, never indexes. This is now the crispest statement of
  *why* the two spaces differ: **mechanism transfers; authority does not.**
  Every crossing is a read the consumer could make alone; nothing at the
  estate level owns anything.

## Patterns We Noticed

- Every mechanism this month moved through the same three steps: felt gap →
  honesty fix in reporting → vocabulary/mechanism. (Triggers: honest-about-
  unevaluable → `type: import`. Imports: COVERAGE → face coverage. Sync:
  felt desync → DIVERGED.) The middle step matters: making the gap *visible*
  preceded closing it, every time.
- Rulings are cheaper than mechanisms and age better. The two written this
  month (producer blindness; repos-not-membranes discovery) resolved more
  proposals than any build did.
- Independent convergence is the strongest promote signal the insight
  machinery has: an agent with no knowledge of the standing
  ingestion-vs-import insight re-derived it from the estate vantage, and the
  gate opened the same week.

## What Should Change

1. **Reconciliation should enumerate restatements mechanically-ish:** when a
   normative rule is amended, grep for its distinctive phrases before
   closing the change (the dark-region walk already prescribes this; it was
   skipped in the day's velocity). No new tooling — discipline, until strike
   three.
2. **Schema finding (from `review-schema-coherence`):** `source` (63 uses —
   informal session/domain attribution on insights) and `source_domain`
   (normative triple member) now share a concept-space with different
   rigor. Not a merge: `source` on a domain-internal insight is birth
   attribution, not an import pin. But the ~4 `origin: external` insights
   carrying only `source` are exactly the pinning pass's residue — when that
   operator-led pass runs, each either gains the full triple (it is an
   import) or an ingestion triple / `origin` correction (it is not).
   Document `source` as deliberate-informal at that point. The `_by` family
   (`verified_by`, `decided_by`, `resolved_by`) is coherent — same role,
   distinct lifecycle moments, keep.
3. **Domain-side work owed, operator-led:** trigger-vocabulary-repair
   Phases 2–5 across the estate; ingestion triples on the register-mirror
   tranche; the pinning pass. The framework arm is done; the floor now
   reports these gaps honestly every run, which is the designed pressure.

## Open Questions Going Forward

- Does `verified` need a clock? (A re-verification cadence for long-lived
  external things, mirroring `source_checked`.) Hold until felt — the
  ingested clock may prove the pattern first.
- `git.autopush` per-domain — conversation queued with the operator; the
  multi-user case (collaborators on the regulated deployment) will decide it.
- Should the estate attention loop (`estate-sync` → `triggers --estate` →
  `estate-check`) become a scheduled session rather than an on-demand one?
  The operator's existing scheduled pull is the natural anchor; watch
  whether the manual loop gets skipped in practice.

## Reflexive Scans (this retrospective's sweep)

- **detect-conflicts (scan mode):** one live contradiction — domain-refresh
  .md still carried the un-sharpened "no fetch at session start" absolute
  after today's orchestration.md amendment. Fixed directly in `5e3dd77`
  (ruled today; no conflict thing needed — belief-revision reserves those
  for contradictions awaiting a ruling). CHANGELOG's historical copies left
  as dated record, correctly. No other contradictions across the swept
  edges; the who_i_know code comment and design doc are consistent with the
  ruling.
- **review-schema-coherence:** findings folded into What Should Change #2.
