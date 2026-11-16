---
id: review-catch-on-the-road
type: plan
status: not-started
version: 1.0
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
    notes: "That plan's order of work waits on this programme's first two cycles."
---

# Review-Catch On The Road

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

- [ ] **Phase 1 — The road.**
      - [ ] One container image inside the operator's WSL Ubuntu: Linux,
            git, Python and the test tools the repository needs, and both
            vendors' command-line harnesses at recorded versions.
      - [ ] The image cannot see the Windows drive, the operator's other
            repositories, or any memory, session history or settings the
            harnesses keep on the host.
      - [ ] Network out of the container reaches each vendor's model
            service and nothing else. Checked by trying to reach GitHub
            from inside it and failing.
      - [ ] The operator signs each vendor in inside the image. That is
            the operator's act, and no agent does it.

- [ ] **Phase 2 — The repositories.**
      - [ ] For each entry, a repository holding the commit under review
            and its history and nothing after it, with no remote and no
            reflog. Built from the commit's own ancestry, not by deleting
            later commits from a full clone.
      - [ ] A leak check per entry, run before any review: the later fix
            commit is absent, and no object from after the commit exists.
            An entry that fails is not run.
      - [ ] Each repository is mounted fresh for each review and thrown
            away after it, so no review sees another's leftovers.

- [ ] **Phase 3 — The instruction.**
      - [ ] Cut to the minimum: review the change at `HEAD` for defects,
            and the output format, at most five findings.
      - [ ] The other vendor reads it for anything that favours the model
            that wrote it. Changes are recorded, and then it is frozen by
            hash.

- [ ] **Phase 4 — The runner and the scorer.**
      - [ ] The runner launches each harness inside the image, one review
            at a time, and records what the reviewer did: commands, tests
            run, time and tokens. There is no reach rule. A review is void
            only if the reviewer dies, returns nothing parsable, or reads
            nothing.
      - [ ] The scorer keeps its matching rule and its refusal to pool
            across set, instruction, model or effort. Near misses are
            exported without the arm, for the operator or a third
            vendor's agent to rule.
      - [ ] Tests for both, and one dry run per vendor, before any real
            review.

- [ ] **Phase 5 — Pre-registration and smoke.**
      - [ ] A new run of `eval-cycle` for the baseline, pinned to this
            plan, with its predictions written before any review runs in
            the new setup. The boxed run's predictions were written for a
            reviewer that could not run code, and are not reused.
      - [ ] The same-model comparison is written into the predictions
            now: two passes by one model against one pass by each vendor,
            at the same number of reviews.
      - [ ] One unscored smoke review per vendor inside the image.

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
