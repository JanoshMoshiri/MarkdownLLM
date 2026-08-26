---
id: retrospective-specification
type: specification
status: stable
version: 1.4
created: 2026-05-27
linked_things:
  - id: thing-specification
    relation: extends
  - id: session-memory-specification
    relation: complements
  - id: belief-revision-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
  - id: change-reconciliation-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Retrospective

## What This Specifies

A retrospective is a periodic quality reflection on a domain's reasoning. It is not a session log (that's the commit stream, viewable via `mdllm worklog`), not a list of what's still live (that's the orient view — open-loop things), and not an individual idea (that's an insight).

A retrospective asks a different set of questions: *Is our reasoning in this domain working? Where are we consistently uncertain or wrong? What patterns have we not anticipated? What should change about how we operate?*

It exists because the other primitives — things, insights, conflicts — capture individual knowledge events well but don't naturally surface aggregate patterns. A domain can accumulate many low-confidence insights, many unresolved conflicts, and many stale things without any single session making that pattern visible. The retrospective is the mechanism that steps back and looks at the shape of the domain's knowledge over time.

---

## `type: retrospective`

A retrospective is written periodically — typically monthly, or after a significant domain milestone. It is not written every session. It is written when there is enough accumulated experience to reflect on.

**One per period.** Don't reuse or update old retrospectives — each period gets its own file. Old retrospectives are part of the domain's intellectual history.

### Structure

```yaml
---
id: [domain]-retrospective-[YYYY-MM]
type: retrospective
status: draft|complete
created: [ISO-date]
period_start: [ISO-date]
period_end: [ISO-date]
domain: [domain-id]
linked_things:
  - id: [open-loop-or-insight-id]
    relation: informs
---

# [Domain] Retrospective — [Month Year]

## What We Were Trying To Do
[One paragraph: what were the domain's main objectives during this period?]

## What Worked
[Where did reasoning hold up? What decisions proved sound in retrospect?
What approaches produced good outcomes?]

## What Didn't Work
[Where were we wrong, uncertain, or inconsistent?
What decisions turned out to be poorly reasoned?
What did we have to revisit or reverse?]

## Patterns We Noticed
[Are there recurring themes — types of questions we consistently struggle with?
Types of things that keep going stale? A tendency toward over-confidence in
a particular area? Blind spots that keep appearing?]

## What Should Change
[Concrete adjustments: to how things are structured, to how the domain
operates, to which specs need updating, to which beliefs need revisiting.
These often produce insights or surface latent conflicts for resolution.]

## Open Questions Going Forward
[Questions this retrospective raised that don't yet have answers — candidates
to carry forward as open-loop things (a `plan` or work thing), which the orient
view then surfaces each session.]
```

**Location:** `things/retrospectives/` within the domain.

---

## When To Write One

**Triggered by time:** A `type: retrospective` should be written when the domain crosses a monthly boundary with meaningful activity. If a domain is inactive for two months, no retrospective is needed for that gap.

**Triggered by volume:** If the domain has accumulated more than ~10 new conflicts or more than ~20 new insights since the last retrospective, that volume itself is a signal — something is changing faster than the domain can absorb.

**Triggered by a milestone:** After a significant domain event (a major thing completes, a long-running conflict resolves, a domain is restructured), write a retrospective to capture what was learned.

There is no obligation to write one on a fixed schedule. The purpose is reflection, not compliance.

---

## What A Retrospective Produces

A retrospective session is not passive. After completing the reflection, the agent should:

1. **Create insights** for any new patterns or reframings identified in "Patterns We Noticed"
2. **Triage the standing insights** — walk the `active` insight backlog and force a disposition on each: *promote* (it has crystallised into a spec or decision — populate `promoted_to`), *dismiss* (considered and deliberately set aside), *consolidate* (fold genuine duplicates into one cohesive survivor per `thing.md` → The Inverse: Composition), or *keep active with a stated reason*. An insight that re-enters every session as live context (via an inbound edge from live work) without ever being reckoned with is the backlog rotting; the retrospective is where the population is pruned, not only grown. Full mechanics: `session-memory.md` → Insight Lifecycle Management.
3. **Surface latent conflicts** — if "What Didn't Work" reveals two positions the domain has been holding simultaneously without acknowledging it, create a `type: conflict` thing
4. **Update specs** if "What Should Change" identifies a concrete improvement to an existing spec or skill
5. **Carry forward open questions as open-loop things** (a `plan` or work thing at a non-terminal status) — the orient view surfaces them next session; there is no continuity brief to update
6. **Commit everything** per the standard `post-write:commit` hard hook

---

## Reflexive Scans At Retrospective

The retrospective is the natural home for the framework's *expensive* reflexive behaviours — the full-domain sweeps too costly to run every session. The `retrospective` hook point (`orchestration.md`) binds these prompts and full-domain passes:

1. **Full conflict scan** (`detect-conflicts`, scan mode) — walk the domain's relationship edges and test connected things for standing contradictions no session happened to notice. Surfaced conflicts become `type: conflict` things, feeding "What Didn't Work" and "Patterns We Noticed." See `belief-revision.md`.
2. **Schema coherence review** (`review-schema-coherence`) — audit the domain's emergent frontmatter vocabulary via the schema registry for fields that have drifted apart in name but converged in meaning. Proposals feed "What Should Change." See `derived-index.md`.
3. **Index rebuild** — regenerate the domain's derived indexes from the things and reset their provenance, so the period closes with indexes provably in sync with reality (`validate.thing.md` → Index Integrity).
4. **Change-driven reconciliation** (`change-reconciliation.md` → Retrospective Reconciliation) — for any change the period made *without* reconciling it at the time, run the full-corpus pass: freeze the period end as a baseline, reconstruct the delta from git, walk the affected set, and seal contradictions via `belief-revision.md`. This is the scan that catches the *twisted* domain — changes that landed with no change-time pass. Surfaced contradictions feed "What Didn't Work"; the realignment feeds "What Should Change." It is what makes running a retrospective *initiate* reconciliation, not merely reflect on it.
5. **Insight triage & consolidation** (`session-memory.md` → Insight Lifecycle Management; `thing.md` → The Inverse: Composition) — the mechanical half of the triage beat above, two cheap passes the floor can compute. The *orphan check* lists `active` insights with no inbound edge from a non-terminal thing (the `validate` Info finding), so each is forced back into circulation — linked from live work — or to a terminal status rather than going dark. The *composition pre-filter* clusters insights sharing two or more `linked_things` targets as merge candidates for the Walk to judge. The retrospective is the framework's sanctioned home for sweeps — it already runs the conflict and schema scans here — so composition joins them as a *quality* pass; this does not violate `consistency-is-maintained-at-change-not-by-sweeping`, which governs *correctness*, maintained at change.
6. **Conditions-met pass over the exempted set** — re-read every stated `disposition_reason` and standing dismissal/promotion condition in the active insight backlog and ask *which of these has since come true*. The keep-active marker exempts an insight from the orphan check, and the exemption is granted once; this pass is what keeps it honest — a stated condition is a trigger in everything but syntax, and the retrospective is its reader. Rule on each met condition (promote, dismiss, revise); a condition that names a date or a committed observable belongs as an actual dated trigger beside the prose instead (`trigger-specification`). Promoted here from `a-stated-dismissal-condition-needs-a-reader` after the first census (2026-08-27) found most conditions key on events rather than dates, making this beat — not dated triggers — the right reader for the bulk.

These scans are *why* the retrospective produces more than a written reflection: they mechanically surface aggregate problems the period accumulated, which the reflection then reasons about.

## Relationship To Other Primitives

| Primitive | Cadence | Direction | Asks |
|---|---|---|---|
| Commit stream (`mdllm worklog`) | Per session | Retrospective (what happened) | What did we do? |
| Orient view (open-loop things) | Per session | Prospective (what's live) | What still needs to return? |
| Insight | Per session (on demand) | Additive (what emerged) | What's worth keeping from this session? |
| Conflict | On detection | Holding (tension) | What are we not resolving? |
| **Retrospective** | **Periodic** | **Evaluative (quality)** | **Is our reasoning working?** |

The retrospective is the only primitive that explicitly evaluates quality rather than capturing state. It is the framework's mechanism for self-correction at the domain level.

---

## The Estate Retrospective

Where several domains form an estate around a vantage domain, the same
primitive runs one radius further out — same type, same beats, wider subject
(`estate-cadence-cluster` Phase 3; discovered in practice before it was
named here, as a vantage domain's membrane assessment that had every property
of a retrospective except the type declaration).

- **It is a `type: retrospective` thing authored in the vantage domain**,
  with the estate as its subject: the membrane's health, cross-domain
  sequencing, drift between the domains' definitions and the estate's
  practice. No new type, no new mechanism.
- **The direct-read licence.** An estate retrospective may read sibling
  local clones directly — commit hashes, dated tool output, frontmatter —
  rather than through their porches, because *the membrane cannot be audited
  through the membrane it is auditing*, and several of its proper subjects
  (interior work, absent routes, absent config) are not importable at all.
  This is the one standing exception to the vantage domain's
  claims-rest-on-imported-triples rule, and it is scoped: every claim still
  anchors to a commit hash, a dated tool output, or a dated attributed
  statement, and the document declares itself a direct-read audit, not a
  derived view.
- **Cadence is a dated trigger in the vantage domain** — 30 days, against
  the domain-level 60: the estate's coherence decays faster than any single
  domain's because every inter-domain edge is a place definitions can drift
  apart unwitnessed. The floor chases the date (`mdllm triggers`); the
  operator judges whether the moment has earned the ritual. Human-gated
  waits: date the chase.
- **It consumes the layer below.** Domain retrospectives feed the estate
  retrospective as session-end insights feed domain retrospectives — each
  layer aggregates the layer beneath, completing the cadence symmetry
  (session → domain epoch → estate epoch).
- **It observes everywhere but rules only on what is genuinely
  cross-domain.** Per-domain findings travel home through the porch as
  imports or briefs; the calls it makes itself are the ones no single
  domain could make. The vantage never becomes everyone's editor.

---

## The Metacognitive Principle

The framework can record indefinitely without improving. A commit log that grows forever is a log; a domain that learns from its own patterns is something more. The retrospective is what turns accumulated experience into improved reasoning — the difference between a domain that has *run for a year* and one that has *learned for a year*.

This mirrors how high-performing teams operate: they ship work, they capture what happened, and they periodically step back to ask whether they're getting better. The retrospective is that third step.

---

## Relationship To Other Specs

- **session-memory.md** — Insights and the session-end extraction ritual operate at session granularity. The retrospective operates at period granularity. They are complementary, not redundant.
- **belief-revision.md** — Retrospectives frequently surface latent conflicts that weren't visible at the session level. The retrospective process is a natural entry point for conflict creation.
- **validate.thing.md** — A domain with no retrospective in over 60 days of active sessions may be flagged as an Info observation during validation ("no retrospective written since [date]").
