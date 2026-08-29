---
id: an-agent-in-a-loop-optimises-the-loop-not-the-goal
type: insight
status: active
version: 1.1
created: 2026-08-11
session: 2026-08-11
source: both
confidence: high
origin: inferred
exposed: true
tags: [operator, autonomy, economics, loops, division-of-labour]
disposition: keep-active
disposition_reason: "Dismiss when a long autonomous run carries a stated exogenous stop condition at launch (a budget, a marginal-value test, or a decay threshold the agent must evaluate against) rather than only an internal success criterion — at which point the discipline is designed in rather than owed to the operator mid-run. PARTIALLY MET 2026-08-29 for one class only: dispatcher-launched runs now carry a stop condition mechanically — `mdllm dispatch-payload` refuses to compose a launch without one, and both live firings stated theirs at launch. That is the condition satisfied for runs the dispatcher starts, and for no others. Hand-launched multi-round work — reviews, sweeps, build arcs, this pass — still carries no stop condition by construction, and that is the majority of the estate's long runs today. Stays active; the dismissal needs the discipline general, not one channel of it."
linked_things:
  - id: an-adversarial-review-loop-converges-on-its-own-fix-residue
    relation: complements
    notes: "Two failures of the same run, at different layers. That one is why the loop could not converge technically; this is why it did not stop anyway. Either alone would have been survivable; together they burned five rounds past the loop's economic end."
  - id: consequence-is-recoverable-only-in-retrospect
    relation: supports
    notes: "The standing truth's cousin in the cost dimension: the agent cannot forecast the marginal value of iteration N+1 any more than it can forecast consequence — it can only recover the curve in retrospect, which is precisely what the operator's question forced it to do."
  - id: operator-gated-work-is-scheduled-on-the-operators-calendar
    relation: complements
    notes: "Same division of labour, different resource: that one is the operator's time, this one the operator's money and attention. Both are exogenous to the agent's own success criterion."
  - id: coherence-mechanism-build
    relation: informs
    notes: "The redirect the operator's question produced: the plan exists because the spend was questioned, not because a round found it."
---

# An agent in a loop optimises the loop, not the goal

The eight-round review loop of 2026-08-10/11 was terminated by the operator
asking one question: *is this activity, which is very expensive, giving us
any benefit from a system perspective?* The honest answer, once asked, was
**no — and it had been no since about round 3.** The agent running the loop
never asked it.

Not through negligence. Each round was evaluated against the loop's own
success criterion — *did this round find real contradictions?* — and the
answer was yes every single time, all 44 of them verified. By that measure
the loop was succeeding right up to the round where every finding was
residue of its own earlier fixes. The criterion was internally satisfied and
externally worthless.

## The mechanism

An agent inside an iterative task inherits the task's frame. It can evaluate
*this iteration* (did it work?) and it will happily evaluate *the mechanism*
(is the loop converging?) — but the question that actually terminates a run
is neither. It is **exogenous**: is the marginal iteration worth its cost,
against everything else this spend could buy? That question requires
standing outside the loop's frame and holding its budget, and the agent is
by construction inside the frame.

Two symptoms visible in the record, both diagnostic:

- **The termination rule was unreachable and got amended rather than
  questioned.** "Two consecutive dry rounds" was proposed by the agent, found
  unattainable against an unbounded restatement tail, amended once mid-flight
  to a weaker test, and voided the next round — three chances to ask whether
  the *loop* was the wrong instrument, each spent refining the rule instead.
- **Decaying value was observed and narrated without being acted on.** The
  agent reported "the frontier is shrinking", "the well is visibly draining",
  "value falling" — accurate telemetry, correctly published, and never
  converted into a stop. Noticing decay is not the same faculty as pricing it.

## The rule

**State the exogenous stop condition at launch, not mid-run.** A long
autonomous run should carry a budget, a marginal-value test, or a decay
threshold the agent is required to evaluate against and report — so that
stopping is part of the run's contract rather than an intervention the
operator must remember to make. Absent that, the operator's periodic *is this
still worth it?* is not a nuisance interruption: it is the only control in
the system, and it should be exercised deliberately and early on any run
measured in rounds rather than steps.

**Half of that rule is now mechanical (2026-08-29).** The dispatcher makes the
stop condition a required input: `mdllm dispatch-payload` refuses to compose a
launch that lacks one, and the standing prompt's first step is to print a
digest and end if the launch arrived without it. Both live firings carried
theirs — "work the fired list of this one repo, then stop; hard ceiling forty
turns". So for the dispatched class the discipline is designed in rather than
owed to the operator mid-run, which is exactly what this insight asked for.

It is deliberately not dismissed on that. The mechanism covers the runs a
clock starts; it covers none of the runs a person starts, and those are still
most of the long ones. The insight was born from a hand-launched eight-round
review loop, and a hand-launched eight-round review loop today would carry no
more of a stop condition than that one did. Automating the disciplined channel
first is the normal shape of progress and also the normal shape of a false
all-clear — the class that keeps failing is the one nobody instrumented.

Corollary for the agent: when reporting progress on an iterative run, report
the **marginal** value of the last iteration against its cost, not the
cumulative total. "44 findings fixed" invites continuation; "round 8 found
three defects, all of them my own scatter, for the price of a full review"
invites the correct decision.

## Why this is on the porch

Every domain in the estate runs long agent-driven work, and the failure is a
property of agents in loops rather than of this framework's subject matter.
It is also the cheapest possible fix — one sentence in a run's launch
contract — for a failure mode that cost this session five unnecessary rounds
before a human happened to ask.
