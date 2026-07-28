---
id: membrane-attention-cluster
type: plan
status: in-progress
version: 1.0
created: 2026-07-28
priority: high
tags: [membrane, triggers, imports, attention, estate, ruling, floor]
linked_things:
  - id: cross-domain-readiness-is-a-shared-signal-not-a-producer-push
    relation: implements
    notes: "The ruling this plan writes into the spec is this insight held under pressure: readiness signals live on the face, never in a producer push"
  - id: origin-external-conflates-ingestion-with-import
    relation: implements
    notes: "The evidence gate is satisfied: an independent estate-vantage review hit the same finding (26 ingested mirrors reporting as could-not-be-checked). The ingestion triple ships here."
  - id: source-behind-mirror-is-still-a-consumer-side-read
    relation: references
    notes: "Same design lens throughout: every new mechanism is a consumer-side or operator-axis read; nothing producer-side is added"
  - id: estate-git-sync
    relation: extends
    notes: "estate-sync supplies the freshness precondition and the repos-not-membranes discovery precedent this plan's estate reads rely on"
  - id: divergence-is-an-unrouted-decision
    relation: references
  - id: trigger-specification
    relation: extends
  - id: provenance-specification
    relation: extends
---

# Membrane Attention Cluster — the ruling, and the reads it unlocks

Two findings arrived from the estate vantage in the same week: an
overview-domain plan (trigger-vocabulary-repair, private estate) showing 15
attention signals the floor cannot evaluate — including one that **fired
unseen** when a source domain's face went from 3 to ~50 exposed things — and
an independent agent review diagnosing the estate as "fully instrumented on
the consume side, blind on the serve side," proposing six fixes, three of
which would have coupled the domains together.

The operator's objection to those three was upheld, and this plan begins by
writing the ruling down so it never needs re-litigating:

## The ruling: producer blindness is a boundary, not a bug

The membrane's direction — *a producer never learns who consumes it, keeps
no consumer registry, and pushes nothing; the consumer polls* — is the
atomicity guarantee, not an unfinished phase. **Publication means committing
honestly to your face. Delivery is the consumer's poll.** Fire-and-forget is
the contract. Consequences:

- No `who_i_know` outbound address book, in any form — even consumer-declared
  variants smuggle discovery back in (the producer must learn which porches
  to ask).
- No un-expose pre-flight — the producer cannot warn consumers it cannot
  know. The humane edge is **etiquette, not machinery**: deprecate on the
  face before withdrawing. A status flip is visible through the face to every
  consumer's next `imports-check`; withdrawal after a deprecation period is a
  courteous breaking change.
- No shared cross-domain work identity — one domain owns a work item; every
  other domain imports it through the face with the triple. Completion
  surfaces at consumers as `stale` on their next check: cross-domain cascade
  without a reverse map.
- No estate manifest — but the `estate-git-sync` precedent (repos, not
  membranes) lets estate tools discover **local clones** as a filesystem
  fact. "N local clones walked" is not a membership claim; a domain not
  cloned here is genuinely absent from this machine's view.

## What ships (all consumer-side or operator-axis)

1. **Face coverage in `imports-check`** — read the manifest of *every*
   address-book source, including those with zero imports, and report
   `offers k, imported j`. Closes the hole where a clean report is achieved
   by not importing (a consumer with an address-book entry and no pulls
   scored 100% coverage while an entire portfolio half was absent). Not
   importing stays legitimate — the line is information, disposition yours.
2. **`type: import` triggers** — the trigger vocabulary learns to name what
   `imports-check` already computes: `state_is` (stale / diverged /
   withdrawn / unreachable) over watched imports, and
   `porch_offers_unimported` for the populated-face case. The
   fired-unseen trigger becomes mechanically evaluable. (Phase 4 of the
   estate's trigger-vocabulary-repair plan, landed framework-side.)
3. **The ingestion triple** — `origin: external` conflates two species; the
   ingestion species (world → domain, no face to poll) gets its own pins:
   `source_system` / `source_ref` / `source_checked` (+ optional
   `source_hash`). `imports-check` reports them as `ingested` with a
   staleness clock ("oldest check …") instead of lumping them into
   could-not-be-checked. Evidence gate on the standing insight: satisfied.
4. **Estate reads discover local clones** — `estate-check` with no roots
   walks the same clone set `estate-sync` walks; `mdllm triggers --estate`
   batches per-domain trigger evaluation with a roll-up. The hand-typed-roots
   omission class (a domain silently absent from every run for a week)
   disappears without any index existing anywhere.
5. **The dated chase-by pattern** — trigger-specification.md documents the
   estate's §4 discipline: a human-gated wait keeps its prose condition and
   gains a dated partner ("by <date>, has this still not happened?"), because
   an undated wait on another person is invisible for as long as it lasts.

## Phases

1. Plan (this thing).
2. Spec: provenance.md — the ruling + etiquette + ingestion triple;
   `mcp_server.py`'s `who_i_know` comment updated from "a later phase" to
   the ruling.
3. Spec: trigger-specification.md — Import-based type + dated chase-by.
4. Floor: `type: import` evaluation + `triggers --estate` + tests.
5. Floor: face coverage + `ingested` species + `estate-check` discovery +
   tests.
6. Docs: operator-guide (ruling, attention sweep, discovery); framework-map
   as coherence demands.
7. Seal v3.23.0 (CHANGELOG, sentinel trio, kernel, full suite, examples);
   record the Phase-1 ruling in the estate's trigger-vocabulary-repair plan
   so its domain-side phases can run.

## Deliberately not done

- Anything producer-side (the ruling).
- The estate's trigger conversions themselves (§1, §3, §4 of
  trigger-vocabulary-repair) — domain-side work, theirs to make.
- `git.autopush` — still deferred (deploy-when-felt); a separate
  conversation the operator has queued.
