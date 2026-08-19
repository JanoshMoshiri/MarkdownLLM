---
id: a-prerequisite-declared-only-inside-its-target-cannot-gate-it
type: insight
status: active
version: 1.0
created: 2026-08-19
session: 2026-08-19
source: both
confidence: high
origin: inferred
tags: [kernel, tier-0, skills, gates, session-start, contract-design]
linked_things:
  - id: emitted-content-is-read-instructed-content-is-economised
    relation: extends
    notes: "Locates the one skip common to all four observed sessions: delivery form explains most of the pattern; declaration position explains why the skill layer specifically never loads."
  - id: read-thing-specification
    relation: challenges
    notes: "The read spec's kernel block carries no read-side gate, while write.thing.md's kernel block carries the write-side one. The fix is one upstream line plus kernel regen — named here, deliberately not applied ahead of the operator's overcoming plan."
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

- It explains the cleanest invariant in the four-session, two-vendor,
  three-harness, three-model evidence: **no session loaded the domain skill
  layer before its first output** — including the strongest run observed
  (Codex, GPT 5.6 Solo, 2026-08-19), which substantially performed the
  orientation walk unprompted and still reported without the skills. That
  session found the read gate only while auditing itself under the
  operator's challenge — by reading the very skill the gate lives in. The
  skip is therefore partly a contract defect, not purely an agent failure:
  an agent cannot be gated by a rule positioned where only compliance
  reveals it.
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
Claude Code on Claude (2026-08-18), Codex on GPT 5.6 Terra and GPT 5.6 Solo
(both medium effort, 2026-08-19). Steps 4–6 compliance ranged from
confessed-without-completing to substantially-done-unprompted; the skill
layer alone was skipped in all four. Tracing why led to the kernel: the
write gate present in Tier 0, the read gate absent — the asymmetry the
title generalises.

Dismissal condition: promoted when the read gate (or an authoring/coherence
check enforcing upstream declaration of prerequisites) lands in the kernel
surface; dismissed if the asymmetry turns out to be deliberate design the
operator reaffirms.
