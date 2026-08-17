---
id: a-shared-worktree-merges-authorship-at-the-index
type: insight
status: active
version: 1.0
created: 2026-08-17
session: 2026-08-17
source: both
confidence: high
origin: synthesised
tags: [coordination, git, multi-agent, event-stream, worktree]
linked_things:
  - id: coordination-claim-specification
    relation: challenges
    notes: "The convention's unit is a thing carrying `held_by`. The git index is not a thing, has no frontmatter, and cannot carry a claim — so the spec cannot reach the resource two concurrent agents actually contend for."
  - id: git-workflow-specification
    relation: references
    notes: "Its ruling that the commit is the domain's event stream is what makes this more than untidiness: a swept commit corrupts the record orientation is rebuilt from."
  - id: divergence-is-an-unrouted-decision
    relation: complements
    notes: "That insight covers two clones diverging, which the floor detects and reports. This is the same estate one level tighter — one clone, two agents — where nothing detects anything."
---

# A Shared Worktree Merges Authorship At The Index

## The Insight

Two agents working one clone do not have two staging areas. Git's index is a
**per-worktree singleton**, so `git add` does not mean *stage my work* — it
means *add to the shared set* — and a bare `git commit` commits everything
anyone has staged. Content, authorship, and commit message decouple silently.

## What happened (2026-08-13, twice within minutes)

The framework was being worked by a Claude session on documentation and a Codex
session on the harness adapter, in one clone.

1. **The near miss.** Claude staged one plan file and committed. The commit was
   **blocked by the boundary hook** — on an entirely unrelated file, a Codex
   evidence document carrying a private term. Had that file been clean, the
   commit would have carried Codex's whole in-flight change set — README, two
   docs, six substrate modules, two test files, the vendor plan, the
   relationships index — under the message
   `plan: hold public-docs-face-build`. It was stopped by a control aimed at a
   different problem entirely. Luck, not design.
2. **The actual sweep.** Minutes later Codex committed with everything staged,
   carrying Claude's plan edit into
   `460bb5a build: add explicit recognised-legacy adapter refresh` — a message
   that describes neither the hold that edit recorded nor the corrected argument
   it carried.

## Why It Matters More Here Than In Ordinary Repos

In most projects a muddled commit is untidiness. In this framework
`git-workflow.md` rules that **the commit is the domain's event stream** —
velocity, orientation, and the backward record are all defined over commit
messages. So a swept commit does not just look wrong; it puts a real state
change (a plan going on hold, with a named release condition) into the log under
a message about something else, where no future session will find it. The
content survived; the *event* did not.

## The Gap This Exposes

[[coordination-claim-specification]] exists for exactly this class — two
operators or sessions contending for one target — and it cannot help. Its unit
is a thing with `held_by` and an optional `held_until` lease. The git index has
no frontmatter, is not in `things/`, and cannot carry a claim. The gap is not a
missing convention; it is that **the contended resource sits outside the thing
graph the convention is defined over.** Nothing in the floor detects it either:
validate, coherence, and the hooks all read content, not authorship.

## How To Apply

**Sequence rather than overlap.** The operator's own call on the day — *hold for
now* — was the correct mitigation and cost nothing. Two agents on one clone
should take turns at the commit boundary even when their files do not overlap,
because the index is shared whether the files are or not.

**Where overlap is genuinely wanted, the mechanism is `git worktree add`** — a
second working tree gives the second agent its own index and HEAD against one
shared object store, which is the actual fix rather than a discipline.

**Partial mitigation, stated honestly:** committing with an explicit pathspec
(`git commit <path>`) limits what *lands* to the named paths. It does not limit
what the hooks *inspect* — the blocked commit above proves the pre-commit path
reads the whole staged set, so a colleague's staged content can still refuse
your commit. Useful, not sufficient.
