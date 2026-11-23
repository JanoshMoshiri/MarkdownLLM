---
id: review-catch-on-the-road
type: plan
status: paused
version: 1.2
created: 2026-11-16
priority: high
origin: stated
exposed: false
tags: [evals, review-catch, cross-vendor, wsl, containers, isolation, harness, pre-registration]
linked_things:
  - id: review-catch-runs-each-harness-on-one-road-2026-11-16
    relation: implements
    notes: "The operator's ruling this plan builds: each reviewer whole, on one identical isolated machine."
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    relation: implements
    notes: "The programme and its one question are unchanged."
  - id: run-eval-cycle-0-review-catch-baseline-2026-11
    relation: references
    notes: "The boxed run this replaces. Its frozen review set is reused as it stands; its one pass is kept for the boxed-against-road comparison."
  - id: peer-loops
    relation: informs
    notes: "That plan's order of work waited on this programme's first two cycles until the operator lifted it on 2026-11-21."
  - id: continuity-across-surfaces-is-the-purpose-2026-11-23
    relation: references
    notes: "The ruling that pauses this plan at Phase 5."
---

# Review-Catch On The Road

## Paused

*2026-11-23.* The operator stepped away from the question this plan exists
to answer (`continuity-across-surfaces-is-the-purpose-2026-11-23`):

> "I think the ability of these agents is increasingly converging, and I
> think it would be a race not worth running, trying to prove that."

Phases 1 to 4 stand as built: the image, the cut repositories, the
instruction, the runner and the scorer. Phases 5 to 8 are not run. Nothing
is concluded from the one boxed pass or the two smoke reviews. Whether the
plan closes outright is the operator's, and is not yet ruled. The isolated
machine is proposed as the clean surface for the cold pickup in the
conformance roadmap's Phase 7.

## What This Is

The cross-vendor review eval, rebuilt so that each reviewer runs whole,
as the operator uses it, on one identical machine that holds nothing the
reviewer should not have
(`review-catch-runs-each-harness-on-one-road-2026-11-16`). The question
is unchanged: does review by a different vendor, started without the
author's account, catch more real defects than review by the same model?

The frozen review set is reused as it stands: 32 entries, 16 commits that
a later fix proved defective and 16 matched commits that no fix touched,
hash `c9537dcb…`. What changes is the road each reviewer drives on.

## The Variables

| Variable | Treatment |
|---|---|
| Vendor package: model, harness, tools, effort | Varied, as one, per cycle |
| Effort | Held at extra high (`xhigh`) for both |
| Running code and tests | Allowed for both, as each harness ships |
| Machine, operating system, network | Held identical: one image |
| Repository | The whole repository cut at the commit under review |
| Instruction | Minimal, read by both vendors, frozen by hash |
| Author's commit message | Absent at baseline; its own cycle later |
| Run-to-run variation | Five passes per cell |
| Training exposure | Items before and after each model's cutoff reported apart |
| A second look by the same model | Its own comparison, from the baseline's passes |

## Phases

*Phases 1 to 4 built on 2026-11-17. What was built differs from the first draft in four places, each closing a gap found on the way: the bundles sit in a store only root can read, and one is staged per review and deleted before the reviewer starts; the working folder has a random name, so it does not say which arm a review is in; the reviewer's harness configuration is fingerprinted before and after, and a change stops the arm, except for the folders each harness syncs itself, which stopped the first Claude smoke review; and the blind arms replace the commit message under review with `Change under review.` so `git log` does not show the author's account. Codex read the instruction for bias, found none in its wording, and three ambiguities that could change scoring were fixed: line numbering, an empty answer, and what counts as pre-existing.*

- [x] **Phase 1 — The road.**
      - [x] One container image inside the operator's WSL Ubuntu: Linux,
            git, Python and the test tools the repository needs, and both
            vendors' command-line harnesses at recorded versions.
      - [x] The image cannot see the Windows drive, the operator's other
            repositories, or any memory, session history or settings the
            harnesses keep on the host.
      - [x] Network out of the container reaches each vendor's model
            service and nothing else. Checked by trying to reach GitHub
            from inside it and failing.
      - [x] The operator signs each vendor in inside the image. That is
            the operator's act, and no agent does it.

- [x] **Phase 2 — The repositories.**
      - [x] For each entry, a repository holding the commit under review
            and its history and nothing after it, with no remote and no
            reflog. Built from the commit's own ancestry, not by deleting
            later commits from a full clone.
      - [x] A leak check per entry, run before any review: the later fix
            commit is absent, and no object from after the commit exists.
            An entry that fails is not run.
      - [x] Each repository is mounted fresh for each review and thrown
            away after it, so no review sees another's leftovers.

- [x] **Phase 3 — The instruction.**
      - [x] Cut to the minimum: review the change at `HEAD` for defects,
            and the output format, at most five findings.
      - [x] The other vendor reads it for anything that favours the model
            that wrote it. Changes are recorded, and then it is frozen by
            hash.

- [x] **Phase 4 — The runner and the scorer.**
      - [x] The runner launches each harness inside the image, one review
            at a time, and records what the reviewer did: commands, tests
            run, time and tokens. There is no reach rule. A review is void
            only if the reviewer dies, returns nothing parsable, or reads
            nothing.
      - [x] The scorer keeps its matching rule and its refusal to pool
            across set, instruction, model or effort. Near misses are
            exported without the arm, for the operator or a third
            vendor's agent to rule.
      - [x] Tests for both, and one dry run per vendor, before any real
            review.

- [ ] **Phase 5 — Pre-registration and smoke.**
      - [ ] A new run of `eval-cycle` for the baseline, pinned to this
            plan, with its predictions written before any review runs in
            the new setup. The boxed run's predictions were written for a
            reviewer that could not run code, and are not reused.
      - [ ] The same-model comparison is written into the predictions
            now: two passes by one model against one pass by each vendor,
            at the same number of reviews.
      - [x] One unscored smoke review per vendor inside the image. Ran clean on 2026-11-17: Codex in 3.2 minutes, 35 commands, the tests run, two findings; Claude in 3.0 minutes, 23 commands, the tests run, three findings, $1.54 at list price. Neither reached outside its repository; neither searched the web.

- [ ] **Phase 6 — The Claude baseline.** `claude-opus-5-5` at extra high
      effort, five passes, one per five-hour window. On the boxed setup a
      pass took 101 minutes and $33 at list price; expect more with tests
      being run.

- [ ] **Phase 7 — The Codex cycle.** `gpt-6.1-sol` at extra high effort,
      five passes, its prediction written in its own run before it
      starts.

- [ ] **Phase 8 — Later cycles, each its own run.** The author's commit
      message shown to each reviewer. And the boxed pass against the road
      for Claude: how much the harness and its tools add to the same
      model.

## What Stays The Operator's

- Signing each vendor in inside the image.
- Ruling near misses, or choosing the third vendor that rules them.
- When each pass runs, against the operator's own work and usage.
- Whether any result is written up. The standing direction of
  2026-10-05 holds: nothing is concluded until much more testing.

## Done When

- [ ] The baseline and the Codex cycle each have five clean passes on
      the same image, scored, with near misses ruled blind.
- [ ] The reflection says whether the second vendor caught more than
      the same model looking twice, and it has been checked by the vendor
      that did not write it.
