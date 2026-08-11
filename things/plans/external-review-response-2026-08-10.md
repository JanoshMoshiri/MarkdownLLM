---
id: external-review-response-2026-08-10
type: plan
status: in-progress
version: 1.0
created: 2026-08-11
priority: high
tags: [reconciliation, review-response, coherence, floor, doctrine]
linked_things:
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "R1 and R2 route here — the review's felt evidence lifts the backlog's build-when-felt hold for the same-builder items"
  - id: coherence-is-a-maintained-rate-not-a-state
    relation: references
    notes: "F4 encoded as its own insight — the asymptote claim, discovered in the nine-review record"
  - id: hook-enforcement-has-three-anchors
    relation: references
    notes: "F1's external corroboration lands as an evidence note on the already-promoted insight — one owner, no restatement"
  - id: repeated-drift-promotes-a-fact-into-the-floor
    relation: references
    notes: "The review's central verdict: this insight's rule was known and unpaid; R1 is its execution"
---

# External Review Response — Routing the Tenth Read

`reviews/REVIEW-external-2026-08-10.md` assessed the framework against the
classical canon and the 2025–26 LLM-systems field, and returned five
recommendations. This plan is the walked cascade: every recommendation routed —
restore, revise, or spawn — with nothing resolved by silent default. The review
is external; its literature claims stay unverified until the operator confirms
them, and no route below *rests* on an unverified claim — each is independently
grounded in the repo's own review record.

## Routes

**R1 — Promotion debt → `mechanical-coherence-checks-backlog` (executed).**
Priority raised, review-9 survivor promotions and the perimeter currency check
added as items. The backlog's closing hold ("build when felt") is lifted for
these items by the operator's own words commissioning the review — the lump of
defects is being felt. Building the checks is the next build session's work;
the backlog now says so.

**R2 — Perimeter currency cadence → same backlog (executed).** Item added:
releases-behind signal for the surfaces outside every individual blast radius.
Same-builder (version pins vs. the tool's own version), no suppression list —
passes the backlog's gate.

**R3 — Cold-read cadence → open, operator decision.** The measured result
(author's walk and cold read catch disjoint sets) says the cold read should
recur, not respond to emergencies. Open question is where the ritual lives:
`retrospective.md`'s cadence doctrine, or a standing note in `reviews/`
practice. Ceremony cost is the operator's call — the framework's restraint rule
(don't bind what prose handles reliably) cuts both ways here, because "prose
handles it reliably" is exactly what the record disputes.

*Evidence amendment (2026-08-11):* the eight-round review loop
(`reviews/REVIEW-loop-2026-08-10.md`;
`an-adversarial-review-loop-converges-on-its-own-fix-residue`) supplies R3's
missing dose–response data: finds decayed 6→7→6→6→7→4→3→3 with severity
falling faster than count, and by round 8 every finding was residue of the
loop's own fixes. The measured shape of the ritual: **one cold read after a
substantial release** (rounds 1–3 were worth their cost; nothing after round
3 was), never a loop. The where-it-lives decision remains open and the
operator's.

**R4 — Walk attestation → spec'd, held.** A session-gate-shaped Warning for
definition-surface commits carrying no recorded walk. Held until R1 lands:
promoting the restatements out of prose removes most of what the walk was
catching, and a warning added while its load is being removed is a cry-wolf
seed (`a-check-that-always-fires-teaches-the-operator-to-ignore-it`). Re-judge
after the promotions ship; deploy when the next skipped walk is *felt*.

**R5 — Doctrine confirmations (executed / open).** Executed: F4 encoded as
`coherence-is-a-maintained-rate-not-a-state`; F1's external corroboration noted
on `hook-enforcement-has-three-anchors`. Open: the manifesto's "Standing On
Shoulders" section predates the canon findings (Parnas, Naur, Lehman, Weinberg
all confirmed as independent rediscoveries) and the field positioning (F3) —
extending it is the operator's voice, routed here, not performed.

## Execution Sequence

**Everything below is staged behind the live review loop.** Operator decision,
2026-08-11: wait until the loop is done. The reason is not caution — it is that
the loop *is generating this plan's input*. Every round it walks turns up more
hand-restated enumerations (round 2: four; round 4: five siblings), and round 2
and round 4 both name this backlog as where the derivation belongs. Building the
checks against a half-harvested census would mean building them twice, on a
corpus still moving under the build.

**Phase 0 — hold (now).** No spec edits, no tool edits, no estate regen from
this thread. The loop owns the working tree. This plan and its review record are
the only surfaces this thread writes, and the loop touches neither.

**Phase 1 — the loop goes dry and seals.** Its terminating record settles the
review-numbering question for both threads (see the ordinal item below). Nothing
here starts before that seal.

**Phase 2 — harvest the census.** Compile every hand-restated fact fixed across
review 9 and every loop round into one candidate list, each with its authority
(the tool constant, schema key, or registry that *owns* the fact). This is the
build spec for Phase 3, and it is read-only work over git history — no
judgement, just enumeration. Known candidates already visible: trigger-family
count (3 surfaces), reserved-type set (5 surfaces), index-signal count (5),
thing-type list vs `_schema.yaml` (2 rounds running), hard-hook count,
subcommand counts (2 surfaces), priority/relation enums, extension-spec count,
`install-hook` hook count, `CORE_FIELDS` re-registration.

**Phase 3 — build, in preference order.** The census will be long, and the
instinct to write one check per entry is wrong — a check is itself a surface
that can drift (`a-generated-surface-collapses-its-walk`). Three instruments,
strictly preferred in this order:

1. **Delete the restatement, name the authority.** Cheapest and permanent — the
   fact stops existing twice. This is what review 9's own fixes chose ("count
   removed; authority named") and it needs no tooling at all.
2. **Generate it.** For lists inside managed blocks (domain kernel, hooks
   block), derive from the authority so the walk collapses to one string.
3. **Check it.** Last resort, for prose that must state the fact in its own
   voice. One generalized enumeration-vs-authority check keyed to a
   phrase→authority registry, *not* a dozen bespoke ones.

Each check ships with a self-test (the suite is at 282 and is the pattern), one
commit per check, and must pass the backlog's standing gate: same-builder
source, no suppression list.

**Phase 4 — R2 perimeter currency**, then **re-judge R4** against the reduced
load. **Phase 5 — R3 and the manifesto extension**, both operator voice.

**Method note for R3.** The instrument to institutionalize is specifically the
one that worked: a *zero-context* read — review 9's cold subagent found in nine
minutes what the author's walk could not see at all, and the loop's round 4
caught its own sealer for the same reason. Whatever cadence home R3 lands in,
the mechanism it schedules should be the blind read, not a general "review".

## Done when

- [x] Review filed (`reviews/REVIEW-external-2026-08-10.md`)
- [x] Backlog reprioritized, R1 + R2 items added
- [x] Rate-not-state insight created
- [x] Anchors insight corroboration note added
- [x] Execution sequence staged behind the live loop (operator decision,
      2026-08-11: wait until the loop is done)
- [ ] Loop seals — Phase 1 gate for everything below
- [ ] Census harvested (Phase 2)
- [ ] R1 built via the preference order: name-the-authority → generate → check
- [ ] R2 perimeter currency check built
- [ ] Operator verifies the review's external claims (quarantine flip on the
      literature findings — or notes which are taken on trust)
- [ ] R3 routed by the operator (cadence home chosen, or consciously declined)
- [ ] R4 re-judged after the R1 promotions ship
- [ ] Manifesto Standing-on-Shoulders extension written or consciously declined
- [ ] Review-ordinal collision resolved by the operator: a concurrent review
      loop (round-1, `4f7fcd5`) and this assessment both landed 2026-08-10 with
      implicit claim to "tenth"; the loop's seal and this record need one
      numbering authority (candidate fix: reviews stop carrying ordinals and
      are identified by date + kind — an ordinal is a hand-restated count)
