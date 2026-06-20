---
id: consequence-is-recoverable-only-in-retrospect
type: insight
status: active
version: 1.0
created: 2026-06-21
session: 2026-06-21
source: both
confidence: medium
origin: stated
tags: [safety, consequence, irreversibility, agentic-actions, harness, guardrails, deterministic-floor, deferred]
linked_things:
  - id: llm-driven-systems-manifesto
    relation: informs
  - id: agents-md-discovery-is-harness-dependent
    relation: extends
  - id: change-safety-is-defense-in-depth
    relation: complements
  - id: provenance-specification
    relation: complements
---

# Consequence Is Recoverable Only in Retrospect, So Irreversible Action Needs a Pre-Made Clearance Gate

## The Insight

A language model predicts the next move from the cognitive stream. It does not — cannot — predict the *consequence* of that move the way it predicts the next token. Consequence is not forward-predictable; it is only **recoverable in retrospect**, by looking back over options the reasoning has already walked through.

Conversation hides this completely, and that is why it goes unnoticed. A conversation is an exploration of options whose forward motion *is* the reasoning; there is always another turn in which a consequence becomes legible after the fact. The retrospective pass is granted for free. **Action removes that net.** The moment the agent stops manipulating memory and reaches out to change the world, there is no next turn in which to realise the consequence — the move is already made.

This yields a precise safety axis, and it is **recoverability, not internal/external and not frequency:**

- The dangerous move is any move that **collapses the retrospective window** — after which consequence can no longer be recovered by looking back. Deleting files outside the repo, sending the email, booking the flight, executing the payment, the shell command that doesn't come back. (A few recoverability-collapsing moves are *internal* — a force-push or history rewrite is as irreversible as a deletion — so the wall isn't the test; recoverability is.)
- **The "it works 98% of the time" framing is a trap.** Frequency is the wrong axis. A move that is fine 98% of the time but unrecoverable the other 2% still needs the gate, because the 2% cannot be undone — and "it usually works" is exactly the reasoning that gets guardrails ignored. Let recoverability decide. The happy consequence: recoverability-collapsing moves are rare anyway, so the gate stays scarce and the agent flows freely almost always — but for the *safe* reason, not the frequency one.

**The commit is not the risk boundary.** A commit is inert: it stores a text file the agent can refer to, update, leave, or retire, with git keeping the retrospective window open forever. It is conversation syntax in another medium — fully reversible, so consequence-blindness does not bite there. The risk is the crossing from reversible medium into irreversible world-effect.

## The Design (Foreseeable, Not Yet Felt)

A guardrail written into a skill or `AGENTS.md` is a **soft ask** — an in-context instruction that competes with everything else, can be reasoned around, and degrades under compaction. The only **hard** mechanism the framework has is the one that lives *outside the model's goodwill*: the deterministic floor at the pre-commit hook, run by git, not by the agent. Safety can only rest on the hard half.

But the hard gate sits at the commit, and the dangerous action (a shell call) doesn't pass through the commit — a topology mismatch you cannot fix by wishing the hook elsewhere. The resolution is to **not drag the floor to the action, but make the action require the floor's output:**

1. **Surface the reasoning into the domain.** The option-exploration that today happens invisibly, driven only by training, is written down as a committed *clearance* artifact: this action, its rationale, its considered consequences. Surfacing is not only for visibility — it is what makes the reasoning *enforceable*. You cannot gate on a thought; you can gate on an artifact.
2. **The floor verifies the artifact, not the behaviour.** "Did the agent obey?" is unverifiable; "does a valid, committed clearance authorising this exact action exist?" is mechanically checkable. That is the whole trick.
3. **The irreversible action is mediated** — wrapped so it refuses to fire unless a matching valid clearance exists. The git-checkable fact becomes the *key* that unlocks the world-affecting move. Floor and action reconnect not through a shared chokepoint but through the artifact the floor blesses.

This is the output-action mirror of `provenance.md`: provenance quarantines external content coming *in*; this gate clears irreversible effects going *out*. The framework guards its input membrane and currently says nothing about what the agent reaches out and *does*.

**The irreducible boundary — the harness is the model's hands.** The model never touches the world directly; it presses keys through whatever tools its harness exposes. So the gate only holds if the agent has **no unmediated path** to the irreversible effect (raw `rm`, raw shell). Closing that path is *confinement*, and confinement is not enforceable from inside markdown — it is a harness/OS property, the same class of honesty the framework already keeps about discovery and hook execution. There is no universal pre-action hook because there is no universal pair of hands:

- **Where it would live:** some harnesses give a real interposition point at the action boundary (Claude Code's `PreToolUse` hook can inspect a Bash call and block it before it runs) — that is the genuine action-side analogue of the pre-commit hook, and where the clearance check would sit. Others have none.
- **Baseline (portable):** the clearance artifact and its schema — what makes a consequence "made legible" enough to clear — plus the requirement that mediated actions consult it. Best-effort without confinement.
- **Hard enforcement (adapter):** per-harness integration that denies unmediated paths and routes irreversible effects through the mediated, clearance-checking tool; or OS sandboxing that makes the raw action impossible.
- **The framework's honest claim:** it can specify the gate, define the clearance artifact, and *probe* whether confinement holds (the way `doctor` probes hook execution) — but it cannot grow hands, so it cannot prevent a bypass. That is a deployment guarantee the operator must supply.

## Why It Matters

It supplies the *cause* the manifesto thesis only gestures at — "integrity that does not depend on the processor remembering to be careful." The reason the processor can't be trusted to be careful is that it is consequence-blind going forward; structure is not hygiene, it is the externalised consequence-vision the model lacks. And it draws the boundary precisely between what the framework can own (the gate, the artifact, the probe) and what belongs to the harness (the hands, the wall), keeping the claim honest.

## Context

Synthesised 2026-06-21 from a human-led exploration: an LLM is truly generative — it predicts the next move but not the consequence of that move. The thread worked through why conversation conceals this (retrospective pass is free), corrected an early mis-anchoring of the risk at the git commit (it is inert memory, not action), relocated the boundary to irreversible world-effect, established recoverability as the true axis over frequency, and landed on the soft-ask-vs-hard-gate distinction and the harness-as-hands constraint.

**Deferred by design — spec when foreseeable, deploy when felt.** It requires nothing in the framework now: the framework's native medium is markdown and git, fully reversible, and the agentic-action surface (an agent that can delete files, book flights, act on a PC or the internet) is not yet in play. Building the gate now would be over-engineering against a pressure that does not exist.

**Revisit when felt:** when a domain's agent is given real, recoverability-collapsing capability on a harness that exposes an action-boundary interposition point — at which the clearance artifact and its mediated-action contract earn specification, and the manifesto thesis earns its `See` pointer here.
