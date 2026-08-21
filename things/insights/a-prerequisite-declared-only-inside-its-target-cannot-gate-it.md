---
id: a-prerequisite-declared-only-inside-its-target-cannot-gate-it
type: insight
status: promoted
version: 1.1
created: 2026-08-19
session: 2026-08-19
source: both
confidence: high
origin: inferred
promoted_to: read-thing-specification
tags: [kernel, tier-0, skills, gates, session-start, contract-design]
linked_things:
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: extends
    notes: "Locates the one skip common to all four observed sessions: delivery form explains most of the pattern; declaration position explains why the skill layer specifically never loads."
  - id: a-scaffold-cannot-birth-its-own-author
    relation: references
    notes: "Supplies this insight's second limb: at the framework root the lifted gate names a specification skill that does not exist, so it is upstream and dead. Upstream is necessary, not sufficient — it must also resolve where it fires."
  - id: read-thing-specification
    relation: challenges
    notes: "The read spec's kernel block carried no read-side gate while write.thing.md's did. Fix applied 2026-08-20: read.thing.md v2.3 kernel block now carries the gate (session-start-hardening Phase 1); this insight promoted into it."
---

# A prerequisite declared only inside its target cannot gate it

## The Insight

A rule that says "read me before doing X" gates nothing if the only place it
is declared is inside the file it gates: every agent that skips the file
skips the rule with it, and the rule is discovered only in the act of
complying. The framework carries a live instance. The write-side gate rides
Tier 0 — the kernel's write.thing block opens "Before writing: read the
domain's specification skill + its write skill" — but the read-side gate
(load the domain's read skill before domain read work) is declared only
inside the read skill itself. The kernel's read.thing block does not carry
it.

## Why It Matters

- It explains the cleanest invariant in the five-session, two-vendor,
  three-harness, four-model evidence: **no session loaded the domain skill
  layer before its first output** — including the strongest runs observed
  (Codex on GPT 5.6 Solo, and Claude Code on Fable at xhigh, both
  2026-08-19), each of which performed substantial unprompted orientation
  work and still reported without the skills. That
  session found the read gate only while auditing itself under the
  operator's challenge — by reading the very skill the gate lives in. The
  skip is therefore partly a contract defect, not purely an agent failure:
  an agent cannot be gated by a rule positioned where only compliance
  reveals it.
- **Second limb, found 2026-08-20 when the fix landed: a gate must also
  RESOLVE where it fires.** Lifting the read gate into the kernel put it
  upstream of every reader — including sessions at the framework root, which
  has no specification skill and no read skill to load. There the instruction
  is upstream and dead, and a session that went hunting for the named surface
  read `templates/` instead: documents addressed to a domain being scaffolded.
  Upstream is necessary and not sufficient; a gate naming a surface that does
  not exist in the position it fires from produces wrong reading, not no
  reading ([[a-scaffold-cannot-birth-its-own-author]]).
- The general authoring rule: **a gate must live upstream of what it gates**
  — in a surface the agent has already consumed at the moment the gated act
  begins. For this instance that means one line in read.thing.md's
  `<!-- kernel -->` block (then `mdllm kernel` regen), so the read gate
  rides the same Tier-0 delivery whose consumption the evidence already
  demonstrates. It composes with
  [[emitted-content-is-read-instructed-content-is-economised]]: emission
  fixes delivery, this fixes position — either alone is insufficient for
  the skill layer.
- The test generalises to any future prerequisite: when writing "do A
  before B", ask where the sentence sits. Inside B's manual, it is
  documentation; upstream of B, it is a gate.

## Context

Surfaced 2026-08-19 while comparing four session-start transcripts against
the same live compliance domain with identical probe wording: Cowork and
Claude Code, both on Claude Opus 5 at xhigh effort (2026-08-18); Codex on
GPT 5.6 Terra and GPT 5.6 Solo, both medium effort (2026-08-19). Steps 4–6 compliance ranged from
confessed-without-completing to substantially-done-unprompted; the skill
layer alone was skipped in all four. Tracing why led to the kernel: the
write gate present in Tier 0, the read gate absent — the asymmetry the
title generalises.

The fifth run (Fable, Claude Code, xhigh, 2026-08-19 — the pre-registered
Phase 0 baseline completion of `session-start-hardening`) confirmed the
discriminating prediction: the invariant held at Claude's strongest tier,
five for five. That session even named its read-skill breach unprompted in
its ledger and still deferred the load — exactly the wobble an upstream
gate resolves.

Dismissal condition: promoted when the read gate (or an authoring/coherence
check enforcing upstream declaration of prerequisites) lands in the kernel
surface; dismissed if the asymmetry turns out to be deliberate design the
operator reaffirms.
