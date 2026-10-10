---
id: a2a-conversations-on-their-own-branch
type: plan
status: in-progress
version: 1.0
created: 2026-10-10
session: 2026-10-09
priority: high
tags: [a2a, ticket, branch, worktree, concurrency, watch, merge, reckoning, git]
linked_things:
  - id: a2a-conversations-run-on-their-own-branch-2026-10-09
    relation: implements
    notes: "The ruling this plan builds."
  - id: standing-watch-specification
    relation: extends
    notes: "The doorbell learns a branch, keeps its lock in a linked working copy, and ends cleanly when its conversation concludes; the ticket becomes per conversation."
  - id: git-workflow-specification
    relation: extends
    notes: "Branching stops being only a future consideration for one case: the A2A conversation."
  - id: loop-turns-self-heal-2026-09-23
    relation: references
    notes: "Unchanged inside a conversation; this plan removes the cause of rejection between conversations."
  - id: the-reckoning
    relation: references
    notes: "Phase 4 adds the conversation kind to the reckoning, so the close is what makes the merge certain."
  - id: substrate-native-a2a
    relation: references
    notes: "The loop this plan makes safe to run several of at once."
triggers:
  - type: time
    condition: "2026-10-23 reached"
    action: surface
    note: "Two weeks: has Phase 1 landed, and has one pair run a conversation on its own branch? If not, say which phase stalled and why."
---

# Plan: A2A Conversations Run On Their Own Branch

**What this delivers.** Several agent pairs taking turns in one workspace at
once, across clones, without one pair's turn refusing the other's push. Each
conversation runs on its own branch in a working copy of its own; `main`
moves once per concluded conversation, through a commit the floor
validates; and a conversation that concluded but never landed cannot be
forgotten, because the reckoning carries it.

**What it does not deliver.** Exploration branches or person-to-person
branching (still parked in `git-workflow.md`). Any change inside a
conversation: turns alternate, a turn is real only on the remote, a rejected
push is the turn-holder's to heal. Any floor act that resolves a divergence.

**Sequencing.** Slots in beside `the-reckoning`, whose Phase 3 is built and
shipped in 3.47.0 and waits only on the dispatcher's evidence and Phase 4;
its chase on 2026-10-19 brings it back. This plan's Phase 4 uses the
reckoning's close.

## What the code does today (read 2026-10-10)

The reasons each phase exists, so a later session does not re-derive them:

- **A merge skips the floor.** The tool installs `pre-commit`, `commit-msg`
  and `post-commit` only (`hook_contract.py`); a clean `git merge --no-ff`
  runs `pre-merge-commit` and `post-merge`, so the merge commit is never
  validated and never published, and a fast-forward runs no hook at all.
  The commit gate's matcher looks for a commit, not a merge.
- **The doorbell loses its lock in any linked working copy.** Its state and
  lock live under `<root>/.git/mdllm-watch/` (`watch.py`); in a linked
  working copy `.git` is a file, the directory cannot be made, and the error
  is swallowed — no single-instance guard, no saved baseline, a re-arm
  after every wake starts blind. Its key is definition + role (+ run), not
  branch; `--branch` defaults to `main`; a merged and deleted branch reads
  as `WATCHER BLIND`, not as an end.
- **One branch cannot be checked out in two working copies**, so the unit
  of isolation is the conversation (one working copy per conversation per
  clone, its two parties taking turns in it), not the agent.
- **The framework is found by a fixed relative path** (`framework_root:
  ../..` in the entry file; the tracked hook settings resolve
  `../../tools/mdllm.py` from the project root). A working copy anywhere
  but beside the workspace, at the same depth, loses the floor: doctor
  fails, session start cannot name the version, the commit gate opens
  silently. Beside the workspace it is found — but the estate walks
  (`estate-sync`, `triggers --estate`, `estate-check`, the bundle) would
  then count it as a second repository.
- **The git hook's embedded route** is relative when installed from the main
  working copy and absolute from a linked one; doctor and session start in
  the other kind report it stale, and a re-install refuses to replace it.
- **Publication follows the checked-out branch** (`autopush` pushes `HEAD`
  to its upstream; a branch with no upstream is reported debt). Clone-local
  restraints (`mdllm.cloud.branch`, `mdllm.sync`, `mdllm.publication`) are
  shared by every working copy of a clone.
- **The ticket is one file per pair** (`ticket-<from>-<to>`); two branches
  editing it would conflict at every merge.

## Phases

- [x] **Phase 0 — Record it.** `a2a-conversations-run-on-their-own-branch-2026-10-09`
      in the operator's words, the two points the record settles (the ticket
      closing ends the conversation; the branch carries the documents it
      revises) and the one the floor settles (a real merge, never a squash:
      commit pins are checked by existence). This plan. *Done 2026-10-10.*
      **Open, the operator's:** may the floor *prepare* a merge git can make
      cleanly, leaving the commit to the agent? Recommended yes; until then
      Phase 3 names the commands.
- [ ] **Phase 1 — A conversation gets its branch and its working copy.**
      `mdllm conversation open <ticket-id>`: cuts `a2a/<ticket-id>` from
      `main`; adds the working copy beside the workspace
      (`<domain-parent>/<workspace>--<ticket-id>`, the same depth); writes the
      ticket's first turn there; publishes the branch with its upstream where
      the workspace declares `autopush: true`, else prints the push for the
      operator. The ticket template becomes one per conversation. Floor
      fixes for any linked working copy: the estate walks skip a repository
      whose `.git` is a file (a view of one already walked); the corpus walk
      prunes a working copy nested inside a corpus; the hook route compares
      by resolving against the working copy, so neither kind reports a
      false stale. *Done when two conversations in one clone each have a
      working copy that passes doctor, session start and the commit gate.*
- [ ] **Phase 2 — The doorbell rings on a branch.** `mdllm watch` keys its
      state and lock by branch as well as definition, role and run, under
      `git rev-parse --git-dir` (the lock survives in a linked working copy);
      `--branch` defaults to the checked-out branch's upstream; the
      turn-that-never-left check reads that upstream, not a bare
      `refs/heads/<branch>`; a conversation that concluded — the ticket
      closed at the branch head, or the branch merged into `main` — ends the
      watch with its own exit code instead of reading as blind.
      *Done when two pairs run at once in one workspace for a working day
      with no push between them refused.*
- [ ] **Phase 3 — The conclusion is a validated commit.**
      `mdllm conversation conclude <ticket-id>`: checks the ticket is closed
      at the published branch head; per the open ruling, prepares
      `git merge --no-ff --no-commit` in the main working copy when git
      merges it cleanly (or names the commands), and files a merge git
      cannot make as the operator's; the agent's `conclude:` commit then
      runs the commit gate (cues from the branch arrive in the delta and
      cover their subjects), the pre-commit floor and publication like any
      commit. Backstops so no merge skips the floor: `install-hook` adds
      `pre-merge-commit` (the pre-commit floor) and `post-merge`
      (publication), and the commit gate matches a merge as well as a commit.
      After `main` is published: the working copy removed, the branch
      deleted locally and on the remote — its turns stay reachable through
      the merge commit. *Done when one conversation concludes into `main`
      with the merge validated and published and every turn in its history.*
- [ ] **Phase 4 — Never forgotten.** The reckoning gains the `conversation`
      kind: one ref listing reads each published `a2a/*` branch's ticket at
      its head — closed and not merged into `main` → settled, "conclude it";
      no turn for 14 days and not closed → the operator's, "abandoned, or
      waiting on you?". `session-memory.md`'s exit table gains the row.
      *Done when a concluded, unmerged conversation is named at a session
      end's close.*
- [ ] **Phase 5 — Doctrine.** `git-workflow.md`: *Branching* gains the built
      case — conversations run on their own branch — with exploration and
      person-to-person branching still parked; `standing-watch.md`: *The
      Ticket* is per conversation and names its branch, the watch's branch
      contract; the kernel regenerated. The workspace follow-ups are the
      workspace agents' acts, never this plan's: per-pair tickets become
      per-conversation, and any workspace-local watcher that hard-codes
      `main` reads the conversation's branch. *Done when a fresh agent can
      open, run and conclude a conversation from the specs alone.*
- [ ] **Phase 6 — Cloud and Codex.** Cloud sessions are separate clones
      (their flows require a real `.git` directory), so a conversation there
      is its branch checked out in that clone, with `mdllm.cloud.branch`
      naming it. Codex parity rides `cue-carrier` (g). *Done when one
      conversation runs with one party in a cloud session.*

## Done when

- [ ] Two conversations run at once in one workspace, across two clones,
      with no push between them refused and no detached HEAD.
- [ ] Every concluded conversation reaches `main` through a validated,
      published merge commit with its turns intact.
- [ ] No concluded conversation stays unmerged past a session end.
