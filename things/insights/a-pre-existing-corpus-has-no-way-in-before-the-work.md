---
id: a-pre-existing-corpus-has-no-way-in-before-the-work
type: insight
status: active
version: 1.0
created: 2026-11-26
session: 2026-11-25
source: both
confidence: medium
origin: stated
tags: [ingestion, corpus, quarantine, cold-start, provenance, membrane, cross-domain, accumulation]
linked_things:
  - id: origin-external-conflates-ingestion-with-import
    relation: extends
    notes: "That insight split ingestion from import and produced the ingestion triple for one thing; this names the case the triple does not reach — a whole corpus, used before it is verified"
  - id: provenance-specification
    relation: informs
    notes: "The quarantine is all-or-nothing per thing: a decision may not pin an unverified external thing and a corpus selection excludes it, so a corpus is unusable until each item is flipped"
  - id: agentic-workflow-across-tools-needs-a-mechanically-validated-record
    relation: complements
    notes: "That record left open a comparison with vendor layers that read a business's existing data; this is the operator's view after seeing one demonstrated — the two are complementary, and the half the framework lacks is the existing corpus"
---

# A Pre-Existing Corpus Has No Way In Before The Work

## The Insight

The framework's record is built by work. A domain starts empty and fills as
sessions decide things, and everything the framework offers — traceability,
the log, accumulated learning — is about that record. A business does not
start empty. It already holds a corpus in other systems, and the framework
has no answer for taking that corpus in and reasoning from it before the work
that would have produced the record has been done.

The operator, 2026-11-25, in the operator's own words:

> "For me, it's all been about work, the traceability of work and the log.
> And it's that accumulative learning. But how do we take, a pre-existing
> corpus and ingest it and then use it before the work's done? That's
> something I think we haven't solved, which for me is an insight to be taken
> away."

On what a vendor's product, seen demonstrated that day, does that the
framework does not:

> "they connect existing sources in a schema that sits on the tenant where
> those things already exist. So, but I think the complementary nature of
> those two things could be something very interesting for us to do here."

On where the field is going, said earlier in the same session:

> "So through the organic use, the end result of a knowledge graph that can
> be leveraged, and workflows can be laid on top to complete work is like,
> it's just the way the direction of things are going."

And on the two pieces the operator finds missing between domains, said in the
same breath as the corpus question:

> "It was just that linkage to a named person between domains, and the
> traversal through the domains without loading a whole domain. I think
> that's probably the two pieces. They're the piece of the membrane that are
> missing."

## What Is Already There, And Where It Stops

The session checked the operator's "we haven't solved" against
`provenance.md` and found the gap narrower than stated, and exact.

Taking in one external item is specified. An ingested thing carries the
ingestion triple — `source_system`, `source_ref`, `source_checked`, and an
optional `source_hash` — is born `verified: false`, and flips only by a named
human in a separate commit (`provenance.md` → Ingestion Is Not Import).

The corpus case is where it stops, and the stop is deliberate. Two rules in
the same spec do it:

- a decision may not pin a thing with `origin: external` whose `verified` is
  not `true` (the enforcement table's Quarantine row, an Error);
- a `things(...)` selection across the corpus excludes quarantined things,
  naming each one.

Together they make trust all-or-nothing per thing. A corpus of thousands of
documents is either flipped one item at a time by a human or cannot carry any
recorded work. There is no state between unverified and verified in which a
corpus can be read ahead of its verification with the reduced trust marked.
The session read these rules in the spec's text and did not exercise them
against the tool.

A second limit sits beside it. The scalability guide puts the line where the
approach should be reconsidered near 1,000 things, so mirroring a business's
corpus into things would cross that line on the first day, before any work.

## The Session's Reading

These are the session's, offered for the operator's ruling, and none is
decided here.

1. **Reference, do not mirror.** The thing holds the pointer and the hash and
   not a copy of the source. The source stays in the system that owns it and
   is read through the harness's connection at the time of use. This is the
   vendor's "connect, don't copy" applied to the ingestion triple, which
   already has the fields for it.
2. **Verify on touch.** A source earns its human flip when a decision first
   needs to pin it, and not when it is taken in. The corpus is readable from
   the first day; trust is spent only where work lands. The quarantine's two
   rules stay as they are — what changes is when the flip is asked for.
3. **The graph grows from use.** Only what the work touches becomes a thing.
   That keeps the record inside its measured range, and it is the operator's
   own observation about organic use ending in a graph.
4. **"No face to poll" has aged.** The spec calls the comparison of an
   ingested thing with its source permanently impossible, because the floor
   has no access to the external system. A harness with a connection to that
   system can make the comparison. The spec already allows `source_checked`
   to be set by "a harness with access"; nothing yet asks one to.
5. **The two membrane pieces may be the same shape.** A named person that
   several domains refer to is a reference more than one domain points at;
   traversal without loading a domain is an index over such references and
   over the exposed faces. This is a hypothesis. Matching identities across
   systems is hard enough to be one vendor's whole product, and the
   framework's version would have to stay small: ruled by a human, and only
   for identities the work touches.

## Why It Matters

It names the half of the problem the framework does not address. The two
kinds of graph answer different questions: one derived from a business's
existing systems says what the business knows, and the record of work says
where the work got to. The operator's reading is that the two are
complementary. If so, the framework's value to a business that already holds
a corpus depends on a way in for that corpus which does not weaken the
quarantine and does not copy the corpus into the record.

## Context

Said on 2026-11-25, after the operator saw a vendor's product for the legal
sector demonstrated and asked the session to research it. The vendor is not
named here; the session's research rested on the vendor's public pages and
one independent review, and the vendor's own documentation was not readable.
The same conversation produced the operator's judgement that the product's
weakness was evaluation offered as an add-on and an audit trail without pins
beneath it, and that the framework's mechanical floor is the part that
comparison showed to be worth having. This record changes no plan and no
spec.
