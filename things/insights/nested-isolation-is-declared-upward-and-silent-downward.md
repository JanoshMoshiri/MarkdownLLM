---
id: nested-isolation-is-declared-upward-and-silent-downward
type: insight
status: active
version: 1.0
created: 2026-08-30
session: 2026-08-30
source: session — framework-root session, 2026-08-30; agent answered an operator queue cue by reading `domain/jmtm-software/things/` directly, then mis-diagnosed its own step as a gitignore breach
confidence: medium
origin: inferred
tags: [isolation, read-gate, nesting, framework-root, contract-design, session-start-hardening, direction]
linked_things:
  - id: a-prerequisite-declared-only-inside-its-target-cannot-gate-it
    relation: extends
    notes: "That insight lifted the read gate out of the skill it gated and into the kernel, making it present. This is the next limb: presence is not address. The lifted gate says 'load THE domain's read skill' — grammar written for an agent already inside one domain, which a root session is not."
  - id: boundary-respect-was-interpretation-not-enforcement
    relation: extends
    notes: "That records the honest thesis — the framework makes boundaries explicit, verified and present in context. This is the counter-instance that sharpens it: the boundary was present in context (kernel emitted whole, integrity trailer intact) and was still crossed, because presence without a seat it addresses leaves nothing to reason over."
  - id: the-root-is-not-a-representative-domain
    relation: complements
    notes: "Same shape, different mechanism. There the root enjoys a corpus-membership exemption it cannot notice; here it occupies a reading position no spec describes. Both are the root failing to model the boundary its consumers live behind."
  - id: isolation-must-contain-writes-not-just-reads
    relation: complements
    notes: "That is a write escaping outward from a sandbox. This is a read descending inward from a parent that holds legitimate access. Opposite directions; the shared lesson is that isolation declared for one direction says nothing about the other."
  - id: session-start-hardening
    relation: informs
    notes: "Second limb of the plan's own 2026-08-20 tripwire, and unplanned evidence arriving before Phase 5's planned evidence — every Phase 5 box is unchecked."
  - id: read-thing-specification
    relation: references
---

# Nested Isolation Is Declared Upward And Silent Downward

## The Insight

The framework's nesting is asymmetric in what it asks of an agent, and only
one direction is specified.

A **domain agent** sits inside and must *reach up* to find the framework. That
reach is deliberate, effortful, and fully described: `framework-discovery.md`,
the `framework_root` frontmatter field, the `.markdownllm` sentinel, the
version-check hook's downward leg. Nothing about it is accidental, because
nothing about it is free.

A **root agent** sits above, and the domains are simply *there* — subdirectories
of its own workspace, reachable with no reach at all. **This direction has no
spec.** No document describes what governs a framework-root session that opens
`domain/x/things/`. The framework's whole "upward/downward" vocabulary
(`domain-refresh.md`, `orchestration.md` → version-check) is about *version
drift along the spec chain*, not about reading domain content. The direction
that costs an agent nothing is the direction nothing was written for.

Two consequences follow.

**`.gitignore` is a publication boundary, not a read boundary.** Excluding
`domain/` implements `pre-domain-scaffold:isolate` — never commit domain files
to the framework repo. It is a statement about *whose history this is*. It says
nothing about *whose contract governs reading this*. Reading it as a read
boundary conflates the two, and the conflation is convincing enough that this
session made it while writing up its own step.

**The read gate names a seat, and the root is not in it.** `read.thing.md`'s
kernel block says: *before domain read work, load the domain's read skill, its
specification skill first.* The definite article presumes an agent already
inside one domain. A root agent is inside none and above all of them, so
nothing in the sentence marks the moment of stepping into `domain/x/` as the
domain read work it is. The gate does not fire, not because it was economised
away, but because it never addressed this seat.

## Why It Matters

The gate was **emitted whole** this session — 104 lines, integrity trailer
intact, no truncation marker. Presence was total, and the step still happened.
That is the sharp part: `boundary-respect-was-interpretation-not-enforcement`
holds that the framework's defensible claim is *boundaries made explicit,
verified, and present in context*. This session satisfies every word of that
and still crossed. **Present-in-context is necessary and not sufficient; a
boundary must also be addressed to the seat that can cross it.**

It also lands on live work. `session-start-hardening` recorded a tripwire on
2026-08-20: the lifted read gate *does not resolve at the framework root* — no
specification or read skill exists there, so it names an absent surface, and a
session hunting for one read `templates/` instead. That is the first limb. This
is the second: at the root the gate is not merely unresolvable for the root's
*own* corpus, it has no trigger at all for the root→domain step. Same tripwire,
one direction further out.

And the timing is evidence about the evidence. Phase 5 — re-test on two
harnesses, confirm cold-session delivery, re-disposition this insight's
parents — is entirely unchecked. Phases 0–4 shipped; the phase that tests
whether they worked has not started. This session is an unplanned sighting
arriving ahead of the planned ones, which is worth more than a confirming run
would be, and worth less than the ladder Phase 5 specifies.

## What This Does Not Say

It does **not** say a root session should treat domains as out of scope. The
harness hands the framework root the whole tree; the domains are its
subdirectories; an agent there has ordinary access to them and assuming
otherwise would be wrong. Nothing in the framework asks a root agent to
pretend the estate is not in reach — and the estate-wide hooks that do exist
(`estate-sync`) prove the opposite.

Nor is the corrective a prohibition. The question a root session cannot
currently answer is not *may I read this* but **under whose contract am I
reading it** — which read skill, which trust semantics, which lenses, and
whether the served face (`exposed: true` plus the reference triple) was the
route it should have taken instead of the filesystem.

## Context

Surfaced when a framework-root session, chasing a VAT deadline named in
`operator-queue-2026-08-28`'s Tier 3, opened `domain/jmtm-software/things/`
and reported that domain's state — its filing deadline and an open conflict —
inside a framework-root briefing, without loading that domain's contract.
jmtm-software exposes three things; none was the material read.

The operator's correction is what produced the insight. The session's first
diagnosis was that it had breached the gitignore boundary; the operator pointed
out the asymmetry — that a domain must reach behind itself to get to the
framework, while the root simply looks down — and that a root agent with access
to the top-level directory has no obvious reason to assume the subdirectories
are not its own. The finding moved from *the agent broke a rule* to *the rule
was written for the other direction*, which is both more accurate and more
useful: the first framing invites a prohibition, the second invites a
declaration.

**One sighting.** The mechanism (no spec addresses the downward read) is
verifiable by absence and was checked. The claim that the absence *causes* the
behaviour rests on this session alone, which is why confidence sits at medium
rather than high. A second sighting on another harness, or a root session that
steps into a domain correctly without being told, would move it.
