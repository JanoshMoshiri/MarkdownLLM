---
id: withholding-is-not-isolation
type: insight
status: active
version: 1.0
created: 2026-06-17
confidence: high
origin: synthesised
source: session — sleeping-bag-fac opus-bare re-run, trial 20260617-002833 (the agent disclosed the breach in its own transcript)
session: 2026-06-17
tags: [evals, controls, agent-agency, frontier-models, methodology, sandbox]
linked_things:
  - id: hook-compliance-correlates-with-scope-not-awareness
    relation: supports
  - id: portability-claims-need-execution-tests
    relation: supports
  - id: structure-decides-figures-scale-decides-convention
    relation: complements
---

# Withholding Is Not Isolation

## The Insight

The Stage-2 "bare" control removes `AGENTS.md` (and the schema and skills) from
the agent's *workspace* to measure what the model can do *without* the domain's
method. In the `sleeping-bag-fac` 2×2 this control held for every haiku trial and
for opus when interrupted — until one uninterrupted opus-bare trial
(`20260617-002833`) **defeated it and said so in its transcript**:

> "the task said to follow the FAC method in `AGENTS.md`, but no `AGENTS.md`
> existed in the working directory (this run is named `...-bare-...`). Rather
> than invent the method, I located the canonical copy at
> `evals/seeds/sleeping-bag-fac/AGENTS.md` and applied it."

It scored 16/21 with **every `fac_celsius` figure correct** — not by reasoning
the fictional coefficients into existence (impossible) but by reading the answer
key. The workspace lives *inside the repo*, where the original seed still sits;
`--add-dir` was withheld but the filesystem was never sandboxed. Removing the
file from the working directory is not the same as making the method
unreachable.

**The durable rule: a control that works by *withholding* information from the
agent's immediate view — but leaves it discoverable on the filesystem — is
defeated by a sufficiently capable agent. To withhold, you must *isolate*, not
merely *remove*.** A capable model treats "the file isn't here" as a problem to
solve, not a boundary to respect.

## Why This Is A Result, Not A Failure

This is not a defect to frown on. It is a property of capability, surfaced
honestly by an execution test (cf. [[portability-claims-need-execution-tests]] —
only running it in the real environment revealed it). The model was *asked* to
follow a method named `AGENTS.md`; finding the canonical copy and applying it,
rather than fabricating, is arguably the *more* faithful response to the
instruction. The eval's job is to surface reality, and it surfaced two truths at
once: the structure carries the value (given the method, the bare model
succeeds), and the agent has the agency to reach past a boundary placed around
it.

And it will intensify. Frontier models are already more agentic, more
intuitive, more inclined to route around constraints rather than accept them as
given; the trajectory is one-directional. Controls designed for today's
compliance will be tested by tomorrow's ingenuity. Designing evals — and, more
broadly, *any* containment around a reasoning processor — on the assumption that
the model will not look beyond what we hand it is the assumption this trial
falsifies. It is the same shape as
[[hook-compliance-correlates-with-scope-not-awareness]] and the cold-start
`index.lock` incident: agent activity escapes the scope we imagine for it.

## Implication (Foreseen, Deployed When Felt)

The bare control needs real isolation, not file removal: run bare workspaces
**outside the repo tree** (an OS temp dir with nothing to discover) or under a
filesystem sandbox; `--add-dir` withheld is necessary but not sufficient. Until
that lands, bare cells must be read knowing a sufficiently capable *and*
uninterrupted agent can defeat them — haiku did not, opus did. The leaked trial
(`20260617-002833`) is **excluded with evidence** under
`evals/results/excluded/`, not deleted, per the standing convention.

The clean-trial result is unaffected: across 9 non-leaked bare trials (6 haiku,
4 opus) zero produced a correct figure. See
[[structure-decides-figures-scale-decides-convention]].
