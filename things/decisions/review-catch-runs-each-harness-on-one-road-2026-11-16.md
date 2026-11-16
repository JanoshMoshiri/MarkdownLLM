---
id: review-catch-runs-each-harness-on-one-road-2026-11-16
type: decision
status: made
version: 1.0
created: 2026-11-16
session: 2026-11-11/16
decided_by: human
confidence: high
origin: stated
exposed: false
tags: [evals, review-catch, cross-vendor, method, isolation, harness, wsl, containers]
informed_by:
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    commit: 589e5b8f409da69431e51388a8b1e23cd760517f
  - id: run-eval-cycle-0-review-catch-baseline-2026-11
    commit: 589e5b8f409da69431e51388a8b1e23cd760517f
  - id: eval-cycle
    commit: 589e5b8f409da69431e51388a8b1e23cd760517f
linked_things:
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    relation: extends
    notes: "That decision opened the live scope to a Codex reviewer 'headless and read-only'. This one replaces 'read-only' and the folder-and-rule design with a whole harness on an isolated machine. Its other five points stand: one programme, its own set, one question, eval-cycle unchanged, nothing concluded."
  - id: run-eval-cycle-0-review-catch-baseline-2026-11
    relation: references
    notes: "The boxed baseline this ruling closes. Its one complete pass is kept as the boxed half of a later comparison."
  - id: review-catch-on-the-road
    relation: informs
    notes: "The plan that builds what this ruling describes."
  - id: eval-cycle
    relation: references
    notes: "The method is unchanged. What moves is what a reviewer is: a vendor's whole package, not a model in a box."
---

# Review-Catch Runs Each Harness Whole, On One Identical Road

## Context

The review-catch programme was designed to give each reviewer a bare
folder and a narrow set of tools, and to void any review that reached
outside it. The first pass ran that way for Claude, with read and search
tools only. Then the Codex reviewer, at extra-high effort, searched the
machine for a Python interpreter and ran the code under review, and was
voided for it.

The operator rejected the design on 2026-11-16:

> That's like me getting two racing cars and taking the engine with the
> most horsepower and saying that one's better. That's not how cars work.
> Cars sit on the road.

> We give it a real problem and we ask it to come up with a solution. And
> we compare the solutions, that's it. [...] There is an expectation that
> Codex was going to step outside of what we'd said, because we'd asked it
> to do a job and it wanted to do it more than us telling it to. [...]
> That pressure is always going to push more than any guardrail, unless
> the guardrail is mechanically added.

The session agreed, with one line kept: every item is a commit that a
later commit fixed, so a reviewer in today's repository can read the fix.
When those changes were reviewed for real, the fix did not exist. The
operator then asked whether a Claude session running the eval skews it,
and which of the variables (model, harness, tools, the machine underneath)
matter. Each vendor's cloud was weighed and set aside. The operator ruled:

> I was starting to feel like a WSL containers is probably the right way
> for best control.

> Yeah, I think that's right. I think that's the correct conclusion.

## Decision

1. **A reviewer is a vendor's whole package.** Model, harness, tools and
   effort together, as the operator uses them: its own command-line
   harness, its normal tools including running code and tests, at extra
   high effort. Nothing it chooses to do voids it. What it did is
   recorded: commands, tests run, time and tokens.
2. **The environment holds the line, not a rule.** Each review runs in
   one container image, identical for both vendors, inside WSL on the
   operator's machine. It holds the whole repository cut at the commit
   under review: every file and the history up to it, nothing later, no
   remote, nothing else on disk. The network reaches each vendor's model
   service and nothing else. A review is void only if the reviewer dies,
   returns nothing parsable, or reads nothing.
3. **Who presses go does not matter; who writes the words does.** The
   launcher is a script. The instruction is cut to the minimum and read
   by the other vendor for anything that favours its author before it is
   frozen again.
4. **Scoring is arithmetic first.** A finding is matched to the lines the
   later fix changed by rule. Findings that land near a defect are ruled
   by the operator, or by an agent from a third vendor, without knowing
   which reviewer made them. The write-up of results is checked by the
   vendor that did not write it.
5. **Held identical:** the machine, the operating system, the network,
   the repository and the effort. **Varied, one per cycle:** the vendor
   package, then a second look by the same model, then the author's
   commit message. Separating a model from its harness is not part of
   this programme, because the operator never runs one vendor's model in
   another's harness.
6. **The boxed run closes.** Its one complete pass is kept, unscored, as
   the boxed half of a later comparison: the same model in a box and on
   the road. That measures how much the harness and tools add.

## Consequences

- `review-catch-on-the-road` builds it. Nothing is run until its image,
  repositories and instruction are checked.
- The operator signs each vendor in inside the image. That is the
  operator's act.
- A new run of `eval-cycle` carries the new baseline and its predictions,
  written before any review runs in the new setup.
- The answer key is public, so training exposure stays a named confound:
  items older than each model's published cutoff are reported apart.

## Considered and set aside

- **Each vendor's own cloud.** The repository and its fixes are public,
  so a cloud reviewer with internet access, or a clone with full history,
  can reach the answer. The two clouds also differ in machine, tools and
  network in ways that cannot be seen, and that is not how the operator
  reviews. Launching 320 reviews through two cloud interfaces is a large
  job of its own.
- **A folder and a rule.** It measured a configuration nobody uses, and
  the rule lost to the reviewer's pressure to finish the job, as the
  operator said it would.
