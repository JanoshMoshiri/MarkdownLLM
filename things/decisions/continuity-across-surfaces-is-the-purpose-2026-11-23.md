---
id: continuity-across-surfaces-is-the-purpose-2026-11-23
type: decision
status: made
version: 1.0
created: 2026-11-23
session: 2026-11-18/23
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [continuity, handoff, surfaces, cross-vendor, memory, floor, metabolism, evals, review-catch, purpose]
informed_by:
  - id: conformance-roadmap
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: review-catch-runs-each-harness-on-one-road-2026-11-16
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: review-catch-on-the-road
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
  - id: a-record-that-only-accumulates-has-no-metabolism
    commit: 6d4e504ee2727305d65fae9b303c63698f14311c
linked_things:
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    relation: extends
    notes: "The operator steps away from the one question that decision opened the live scope for. Its boundary for everything else stands, and the scope is not used for that question again without a new decision."
  - id: review-catch-runs-each-harness-on-one-road-2026-11-16
    relation: extends
    notes: "The method and the isolated machine stand as built. The programme they were built for is no longer pursued."
  - id: review-catch-on-the-road
    relation: informs
    notes: "Paused at its Phase 5 by this ruling. What it built is kept."
  - id: conformance-roadmap
    relation: informs
    notes: "Says what pillar 4 is for, and what Phase 7 has to show."
  - id: peer-loops
    relation: informs
    notes: "Its order of work, the eval first, is lifted. Its Phase 4 no longer waits on the programme."
  - id: a-record-that-only-accumulates-has-no-metabolism
    relation: references
    notes: "The record that carries continuity is one that discards as well as creates."
  - id: conformance-not-determinism
    relation: references
    notes: "The floor, not the agent, manages the record a new surface picks up."
---

# Continuity Across Surfaces Is The Purpose

## Context

The conformance roadmap's Phase 0 asked the operator to rule on the order
of work against the "eval first" order in `peer-loops`. In ruling, the
operator went further and restated what the framework is for.

The session read it wrongly twice. Both corrections are kept here, because
the two misreadings are the likely ones.

On 2026-11-21, on the cross-vendor review question:

> "I've been thinking about it more and more, and I don't even know if I
> want to try and prove that the multi-vendor review is what works well. I
> don't even care about, like, if I want to prove that anymore. I think
> I'll use it. I think in some cases it is useful. But especially after
> hearing the evidence that's there [...] I'm kind of siding with just, you
> know, cold reviews, at least holding as much weight, if not more in some
> cases. [...] I'm less interested in trying to test that. I'm more
> interested in enabling cross-vendor communication for logistical reasons.
> You know, sometimes you have a GPT agent, or you have a Gemini agent, or
> you have a Hermes agent [...] And I think the piece of importance is the
> seamless operation of everything in one space, one shared context, one
> validation floor, one source of truth."

The session took "one shared context" to mean one shared conversation
between agents. The operator corrected it the same day:

> "I mean, one shared record. And I think there's real value in that. It's
> the continuity between agents. And that's something that is not just a
> shared MD file. It's a validated and managed memory corpus that is
> managed by the floor, not the agent. It metabolizes, it discards as well
> as creates. I think that's the special offering. And I think we should
> step away from the test and the question of this. You know, does one
> vendor and another vendor give you more vision? I think the ability of
> these agents is increasingly converging, and I think it would be a race
> not worth running, trying to prove that. I think the real offering is,
> how do I have continuity of a domain between vendors? How do I develop my
> application that's going to use a video and I describe my story in Claude
> that builds the application around the video that will run, and I give it
> to my Gemini agent who picks up the story and creates the video. That's,
> I think, the problem I'm trying to solve here."

The session then called this an unmeasured claim, to be tested against an
agent given a good brief. The operator corrected that on 2026-11-23:

> "I understand that an MD file doesn't necessarily make the agent better
> at doing the task than a good prompt. But that's the whole point. The
> whole point is if I'm working on a task or on a job, I want to seamlessly
> be able to move from one surface to the other, whether that surface is a
> brand new VM, whether it's a different LLM, whether it's just a different
> session in the same environment. And it's about continuity between all of
> these points of handoff. You know, a fresh session is always going to
> start cold [...] But it's about being able to pick up on a new surface
> and say, okay, let's carry on with the work we were doing. And as the
> person that's working on it, you can then just continue your stream of
> thought. Now I want to add this and do this. And the point of where
> things got to, the understanding of decisions, the context of the whole
> state of things is known. Because that's the whole point of a memory
> system. [...] My goal is not to prove that MD files curated in a
> structured manner are going to beat a good prompt."

## Decision

1. **The purpose is continuity of the work across every point of handoff.**
   A handoff is any move to a new surface: a new session in the same
   environment, a new machine, a different vendor's agent. Every one of
   them starts cold. What is wanted is that the person carries on their
   stream of thought, and the new surface already knows where things got
   to, what was decided and why, and the state of the whole.
2. **What carries it is one shared record, not one shared context.** Each
   agent keeps its own context. They meet in the same committed record,
   under the same floor: validated and managed by the floor and not by the
   agent, discarding as well as creating.
3. **It is not a claim that a structured record beats a good prompt,** and
   no eval is run to show that it does. A good prompt can do as well for
   one task. The record is there so that nobody has to write that prompt
   again at every handoff.
4. **The cross-vendor review question is no longer pursued.** Review by a
   second vendor is used where the operator finds it useful. Cold review by
   a fresh session holds at least as much weight. Agents of several vendors
   work in one estate for logistical reasons, not as a method of
   validation.
5. **`review-catch-on-the-road` is paused at its Phase 5.** The image, the
   cut repositories, the frozen set, the instruction, the runner and the
   scorer are kept as built. The baseline's one complete pass stays
   unscored. Nothing from the programme is concluded or written up.

## Consequences

- `conformance-roadmap` states the purpose under pillar 4. Its Phase 7 has
  to show continuity across a handoff, not a review result.
- `peer-loops`: the order "the review-catch eval runs first" is lifted, and
  its Phase 4 no longer waits on the programme. Who reviews whom, and
  whether a review starts blind, are settled by the operator's practice.
- The founding framing of a second vendor as validation is retired as a
  claim. It stays as a practice.
- `AGENTS.md` principle 9 already names continuity of work as the claim.
  This ruling sharpens it and does not change its text.

## Not ruled

- Whether `review-catch-on-the-road` closes outright or stays paused with
  the machine kept. The session asked on 2026-11-21 and the operator has
  not answered. It is paused until then.
- The work-continuity ablation in `evidence-and-eval-backlog`. It asks
  which surfaces of the structure carry the weight, which is a different
  question from beating a prompt. The operator has not said whether it
  continues.

## Proposed by the session, for the operator's approval

- **A cold pickup can be gauged against the record itself.** A fresh
  surface, given only the record, states what is open, what was decided and
  why, and what comes next. That statement is compared with what the record
  holds. The record is a reference the receiving agent did not write. This
  is a pass or a fail per surface. It is not a comparison with a prompt.
  The isolated machine built for review-catch is a clean surface to run it
  on. It is offered as the check for the roadmap's Phase 7.
- **Capture is the weak point, more than pickup.** The record carries only
  what was committed. These rulings were spoken on 2026-11-21 and sat in
  one session's conversation until this commit. A different surface opened
  in between would have known none of them.

## Considered and set aside

- **One shared context between agents.** A misreading of the operator's
  words. What is shared is the record.
- **Proving the record against a good prompt.** Not the goal, and not a
  comparison the operator is interested in.
