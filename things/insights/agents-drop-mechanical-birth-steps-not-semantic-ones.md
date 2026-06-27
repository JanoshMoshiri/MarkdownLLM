---
id: agents-drop-mechanical-birth-steps-not-semantic-ones
type: insight
status: promoted
version: 1.1
created: 2026-06-12
promoted_to: orchestration-specification
confidence: medium
origin: synthesised
source: session — cold-start scaffold rehearsal (evals/cold-start-scaffold.yaml, 3 informative trials)
session: 2026-06-12
tags: [scaffolding, hard-hooks, deterministic-floor, evals]
linked_things:
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: supports
    notes: "First birth-path measurement of the same decay: 96 turns of scaffolding, zero commits"
  - id: orchestration-specification
    relation: informs
    notes: "Motivated mechanising pre-domain-scaffold:isolate as mdllm scaffold (orchestration v1.9)"
---

# Agents Drop Mechanical Birth Steps, Not Semantic Ones

> **Promoted 2026-06-27 → `orchestration.md`.** The lesson crystallised into the
> shipped `pre-domain-scaffold:isolate` hard hook + `mdllm scaffold` (the mechanical
> birth steps the agent kept dropping are now the floor's, not the agent's). The
> insight discharged itself: it had only outbound edges and nothing live pointed
> back, which the graph-keyed liveness check surfaced (dissolve-continuity Phase B).
> Kept for audit; its assertions now live in the spec.

## The Insight

When a fresh agent scaffolds a domain from the framework's templates, the
*semantic* output is reliably good — declared schema, four coherent skills,
interlinked seed things, validates clean. What fails is the *mechanical
sequence around* that output, and each trial drops a different step: one
built everything across 96 turns and never made a single commit; another
committed properly but skipped the outer repo's `.gitignore` isolation. The
quality of the content gives no warning about the integrity of the procedure.

## Why

The `pre-domain-scaffold:isolate` hard hook is a five-step ordered procedure
held in attention across a long, generative session — exactly the conditions
under which `hook-compliance-correlates-with-scope-not-awareness` predicts
decay. The agent isn't unaware of the hook (both trials did *most* of it);
it loses one step in the noise of forty file-writes. A procedure whose
correctness depends on nothing being dropped is a procedure for code.

## Evidence

Rehearsal of 2026-06-12 (`evals/README.md` § cold-start scaffold rehearsal):
pre-tool trials scored 10/11 (opus, missed all commits, $6.43) and 10/11
(haiku, missed isolation, $0.52). With the guide routing to `mdllm scaffold`
(same day), the next trial scored 11/11 ($0.45) — its domain's first commit
is the tool's deterministic scaffold commit, with the agent's semantic work
layered on top. n=3: a pattern consistent with the prior insight, not an
independent proof.

## How To Apply

Any multi-step mechanical procedure the framework asks an agent to perform
("in this order, never skip") is a candidate for the same treatment as
validation and birth: give the steps to a tool, leave the judgement to the
agent. The remaining candidates worth watching: session-end ritual mechanics,
domain-refresh bookkeeping (`framework_version_seen` updates), index rebuilds.
