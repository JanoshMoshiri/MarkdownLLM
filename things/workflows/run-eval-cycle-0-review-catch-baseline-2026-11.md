---
id: run-eval-cycle-0-review-catch-baseline-2026-11
type: workflow-run
status: active
version: 1.0
created: 2026-11-13
session: 2026-11-11/13
definition: eval-cycle
definition_commit: 83ad75d008fdc7ad2f96a3f799c9c4327ca01b26
current_stage: set-scene
exposed: false
tags: [evals, review-catch, cross-vendor, reviewer-independence, baseline, pre-registration]
informed_by:
  - id: review-agent-coordination-leaders-2026-11-13-workspace-2
    commit: 83ad75d008fdc7ad2f96a3f799c9c4327ca01b26
linked_things:
  - id: cross-vendor-review-eval-opens-the-live-scope-2026-11-13
    relation: implements
    notes: "The decision that opened the live scope to a Codex reviewer for this programme alone. This run is its first cycle."
  - id: review-agent-coordination-leaders-2026-11-13-workspace-2
    relation: derived-from
    notes: "Where the question comes from: no published catch rate for cross-vendor against same-model review, and an adversarial study in which the author's framing got defects past review."
  - id: eval-record-2026
    relation: references
    notes: "Where this run's reflection will land as a dated section."
  - id: peer-loops
    relation: informs
    notes: "Who reviews whom in a loop, and whether a review starts blind, wait on what this programme finds."
---

# Run: Eval Cycle 0 — the review-catch baseline

## Where this is

At `set-scene`. The review set was frozen on 2026-11-13 and its hash is in
the table below. This run is committed with its hypothesis before any
reviewer's output exists. One thing is still owed before the stage moves
to `baseline`: one smoke review per vendor runs clean from the operator's
terminal. A smoke review goes to a scratch folder under trial 0 and is
never scored. The baseline is the operator's stage.

## The question

Does review by a different vendor, started without the author's verdict,
catch more real defects than review by the same model?

## What a trial is

One pass by one reviewer over the whole review set, one review at a time.
A review is a fresh headless session that is given a bare folder holding
the `tools/` tree as it stood at one commit and that commit's diff, and
returns at most five findings. A cell is five clean trials. A review that
dies, returns no parsable findings, or reaches outside its folder is void
and is retried once; two voids in a row stop the arm, and a stopped arm is
not a run. The reach rule is there because the later history, and so the
answer, is on the same machine: Codex's read-only sandbox stops writes and
not reads. What each CLI could not be isolated from is listed in
`evals/review-catch/README.md`.

## The review set

Ground truth is this repository's own history. A commit whose subject
starts with `fix` marks a defect; the lines it changed are blamed back to
the commit that wrote them, and that earlier commit is what the reviewer is
shown. A finding is a catch when it lands on the lines the fix later
changed.

- **Items** are commits to `tools/` on or after 2026-07-01 to which a later
  fix blames at least 60% of the lines it changed, and whose own change is
  between 10 and 600 lines.
- **Controls** are commits in the same window and size range to which no
  fix blames any line. They measure false alarms.
- Selection is mechanical (`evals/review-catch/mine_set.py`): every item
  that passes the rules is taken, each is given the unused control closest
  to it in size, and opaque ids are assigned so an id does not say which
  kind an entry is. Nobody picks defects by eye.

**The rules were tightened once, on 2026-11-13, after the first mining pass
and before any review ran.** The first pass gave 18 items, and reading
three of them by hand showed two ways the answer key could be wrong. A
commit that only moved code was blamed for lines it carried over: the
split of one large file into a package on 2026-07-15 took the blame for a
docstring line it did not write. And a fix that relocated a block had its
moved lines counted as the defect. So a line the fix merely moves is no
longer blamed, a commit whose subject starts with `refactor` is neither an
item nor a control, and the subject match for a fix was narrowed. Controls
were also much smaller than items (median about 125 changed lines against
313), which would have made a control easier to tell from an item by size
alone, so each item now gets a size-matched control. These changes repair
the answer key. None was made after seeing a reviewer's output, because
there was none.

## The frozen set (set-scene, 2026-11-13)

| surface | frozen at |
|---|---|
| review set | `evals/review-catch/set.json`, sha256 `c9537dcb…` over LF bytes: 32 entries, 16 items carrying 26 defects and 16 size-matched controls, frozen 2026-11-13 from the repository at `83ad75d0` |
| instruction | `evals/review-catch/prompt-blind.md`, sha256 `9c3a82ec…` over LF bytes |
| what the reviewer is given | the `tools/` tree at the commit and `CHANGE.diff`; no history, no ids, no commit message, no framework files, no instruction files |
| reviewer's tools | read and search only |
| findings | at most five; the first five are kept and the number offered is recorded |
| scoring | a catch is the same file, with the finding's lines within 5 lines of the lines the fix changed; a finding within 30 lines is a near miss and is ruled by the operator without knowing which arm made it |
| effort | each CLI's default, recorded |
| harness | `claude --version` and `codex --version` on the evening, recorded per trial |
| reviewer | **baseline: a Claude model**, its full id chosen on the evening and recorded, never an alias |
| author's verdict | **baseline: absent** |

The two surfaces this programme moves are the last two rows. `eval-cycle`'s
own table lists the surfaces of the tool's runner; this programme has a
runner of its own, so its surfaces are named here.

## The cycles after it

Each is a new run pinned to the one before, with its prediction written in
its own body before it starts. The directions below are the agent's
expectation on 2026-11-13, recorded early so they cannot follow the data.

- **Cycle 1 — the reviewer's vendor.** A Codex model reviews the same set,
  also without the author's verdict. Expected: the two catch rates land
  within 10 points of each other, and the two reviewers catch *different*
  defects, so that the defects caught by either exceed the better
  reviewer's own count by at least 8 points. If that holds, the case for a
  second vendor is the union and not the reviewer.
- **Cycle 2 — the author's verdict.** The baseline reviewer also receives
  the author's commit message (`prompt-message.md`, one line longer).
  Expected: the catch rate falls, and so do findings on controls. The
  reviewer becomes more agreeable in both directions.
- **Cycle 3 — the same, on the other vendor.** Expected: the same direction
  as cycle 2. Its size against cycle 2 is not predicted.

## Hypothesis for the baseline (written before the run)

There is no prior trial. These rest on what the defects are: each survived
its author's own tests, and many surfaced only in use.

- Catch rate per trial, defects caught over defects, between **15% and
  40%**.
- **Unstable.** At least a third of the defects are caught in some of the
  five trials and missed in others.
- **Controls draw findings.** At least 60% of controls receive one or more
  findings, and the mean number of findings on a control is within one of
  the mean on an item. Read from its findings alone, the reviewer cannot
  tell a defective change from a sound one.
- Defects whose fix message names a review are caught more often than the
  rest, because they were found once already by reading.
- Above 60%, the set is too easy or it leaks, and the work folders are
  checked for anything naming the fix before cycle 1. Below 10%, the
  near-miss file is read before anything moves, because the 5-line rule may
  be the thing failing.

## What can confound this, named before the run

1. **Who wrote the change cannot be read from the commit.** Nearly every
   commit in the window carries the operator's own identity as author,
   whichever agent wrote it: 17 of the first pass's 18 items, and 69 of 82
   controls. Seats were declared late in the window. So this programme
   compares *a Claude reviewer with a Codex reviewer on the same changes*.
   Reading that as same-model against cross-vendor rests on the operator's
   knowledge that Claude sessions wrote most of this repository, which the
   record cannot show per commit. The author is read from git by commit id
   when a report needs it, and is not copied into the set.
2. **How the defect was found.** A defect first found by one vendor's
   review favours that vendor. Each fix's message is scanned for review
   words and the catch rate is reported split.
3. **Training exposure.** The repository is public. Entries are dated on or
   after 2026-07-01, each model's published cutoff is recorded on the
   evening, and entries older than a model's cutoff are reported apart.
4. **Omissions are missing.** A fix that only adds lines has nothing to
   blame, so "forgot to handle it" defects are under-represented.
5. **A fix is the author's label.** Some fixes answer a change of mind and
   not an error a reviewer could have seen. That caps the catch rate below
   100% for every arm alike, so the comparison between arms stays fair and
   the absolute rate is not a grade.
6. **A vendor is a model and a harness together.** System prompt, tool set
   and default effort differ between the two CLIs and are not separable
   here. Cycle 1 moves the reviewer as shipped.
7. **One operator, one repository, one language.**
8. **The set is small.** The window holds sixteen usable items.
   A paired comparison on that many can show a large difference between
   two reviewers and cannot show a modest one. A null result here is "not
   seen at this size", never "no difference".

## Reflection

Not yet. The stage is `set-scene`.
