---
id: git-workflow-specification
type: specification
status: stable
version: 1.3
created: 2026-05-19
linked_things:
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: estate-git-sync
    relation: informs
    notes: "The Machine Axis section — sync-before-orient, ff-only inbound, publication debt — landed from this plan"
  - id: divergence-is-an-unrouted-decision
    relation: references
    notes: "The inbound rule: a non-fast-forward state is a decision owed, never a mechanism's merge"
  - id: thing-specification
    relation: complements
  - id: interface-specification
    relation: complements
  - id: write-thing-specification
    relation: complements
  - id: validate-thing-specification
    relation: complements
  - id: derived-index-specification
    relation: complements
---

# Git Workflow

<!-- kernel -->
**The commit is the moment state becomes real** — on this machine; publication (push/fetch) makes it real to the estate. Working directory = draft; commit = local truth. Triggers, orientation, and audit all read committed state only.

**Multi-machine sync:** sync before orienting — `mdllm estate-sync`: fetch + `pull --ff-only`, bounded, never prompting, degrading offline to "orienting from last-fetched state". Divergence is reported (`DIVERGED (+a/+b)`), never resolved — routing it is the operator's decision. Never push, never auto-merge, never reset. Session end reports publication debt (`estate-sync --status`: unpushed commits per repo).

**Commit at meaning boundaries:** thing created · status transition · write-session unit · validation fixes · session end (nothing left uncommitted across sessions).

**Message format:** `action: description` of the *domain state change* — `create: vat-return-2026-q1`, `complete: data-collection → unblocks quarterly-review`, never "modified 3 files". Git log is the domain's event stream and telemetry (velocity reads it directly; no index needed).

**Autocommit:** per `git.autocommit` in AGENTS.md frontmatter. Always commit to the owning repo — walk up to the nearest `.git`.
<!-- /kernel -->

## What This Specifies

This document defines how git is used within the LLM-driven systems framework — not just as backup or version control, but as the **state machine** that makes things persistent, auditable, and reactive.

The manifesto establishes *why* git (versioned, portable, transparent). This document establishes *how* git operates within a domain: when to commit, what commit messages mean, who commits, and how git history becomes the event stream that drives triggers and session orientation.

## Git As The State Machine

In a traditional application, writing to the database is the moment state becomes real. A user clicks "save," the database updates, and the new state is persisted.

In this framework, the **commit** is that moment.

Everything before the commit is working state — files on disk, modifications in progress, things the agent has created or changed but not yet persisted. Everything after the commit is truth — versioned, diffable, auditable, rollbackable.

This distinction matters because:

- **Triggers evaluate against committed state** — A dependency trigger watching for `status: completed` fires based on what's been committed, not what's in the working directory
- **Session orientation reads committed history** — When the agent loads at session start, it looks at what commits have happened since last session to understand what changed
- **Audit trails require commits** — A change that was never committed never happened, from the system's perspective
- **Rollback operates on commits** — If the agent makes a bad change, you can revert the specific commit that introduced it

The working directory is draft. The commit is publication.

## When To Commit

Commits should happen at the boundary where domain state changes meaning. Not after every keystroke (noise), not once a day (lost granularity). Each commit should answer: **"What changed in my domain and why?"**

### Natural Commit Points

**After a thing is created**

A new thing exists in the domain. That's a discrete, meaningful state change. Commit it.

```
create: quarterly-review-prep (task, high, due 2026-06-15)
```

**After a status transition**

Status changes are the most significant events in the system. They're what triggers watch for. They represent real progress, real blockers, real decisions. Commit each one.

```
complete: data-collection → unblocks quarterly-review-prep, stakeholder-feedback
```

```
block: design-review — waiting on stakeholder availability
```

**After a write session**

The user asked the agent to do something that modified multiple things — reorganise priorities, break down a project, batch-update statuses. Those changes form a logical unit of work. Commit them together.

```
reprioritize: 3 tasks elevated to high, 2 deferred to next quarter
```

```
split: project-redesign → 4 subtasks created
```

**After validation and fixes**

The agent ran validation, found issues, and fixed them. Commit the fixes as a unit.

```
validate: fixed 2 broken links, added missing status field to task-budget
```

**At session end**

Safety net — the backstop, not the invariant. The `post-write:commit` hard hook is the invariant: every write is committed before the response completes, so in a compliant session there is nothing left to commit here. This check exists for when the invariant was breached anyway — a hook that couldn't fire in the harness, an interrupted session, a missed write. Finding uncommitted changes at session end is a signal worth noting, not routine.

```
session-end: uncommitted changes from session 2 (19 May 2026)
```

### The Rule

**One commit per meaningful state change.** If you can describe what changed in a single sentence that makes domain sense, that's one commit. If you need two sentences about unrelated changes, that's two commits.

## Commit Message Conventions

Commit messages in this framework are not about files — they're about domain state. They should be readable by a human scanning `git log` and by an agent evaluating what happened since last session.

### Format

```
<action>: <description>
```

### Actions

| Action | When | Example |
|--------|------|---------|
| `create` | New thing created | `create: quarterly-review-prep (task, high, due 2026-06-15)` |
| `complete` | Thing marked completed | `complete: data-collection → unblocks 2 things` |
| `update` | Thing metadata or narrative changed | `update: project-redesign — revised scope and timeline` |
| `block` | Thing became blocked | `block: design-review — waiting on stakeholder input` |
| `unblock` | Thing unblocked | `unblock: quarterly-review-prep — dependencies resolved` |
| `reprioritize` | Priority changes across things | `reprioritize: 3 tasks elevated to high` |
| `split` | Thing broken into sub-things | `split: project-redesign → 4 subtasks` |
| `merge` | Things combined | `merge: task-a + task-b → combined-task` |
| `cancel` | Thing cancelled | `cancel: legacy-migration — no longer needed` |
| `archive` | Thing archived or moved | `archive: q1 completed projects` |
| `validate` | Validation fixes applied | `validate: fixed 3 broken links` |
| `session-end` | Uncommitted changes at session close | `session-end: changes from session 2 (19 May)` |
| `framework` | Changes to skills, agent, or framework files | `framework: update write.thing.md — add trigger evaluation` |

### Multi-Thing Commits

When a single action affects multiple things (a write session, a reprioritisation), list the key changes in the commit body:

```
reprioritize: Q2 realignment — 5 things updated

- quarterly-review-prep: medium → high
- budget-analysis: low → medium  
- legacy-docs: high → low (deferred to Q3)
- team-onboarding: medium → high
- office-move: paused → cancelled
```

### What Makes A Good Commit Message

- **Domain-level language** — "complete: data-collection" not "modify data-collection.md"
- **Consequence-aware** — "complete: data-collection → unblocks 2 things" tells you the impact
- **Scannable** — The first line tells the whole story; details go in the body
- **Consistent action verbs** — Use the standard actions so `git log` is parseable

## Who Commits

### The Recommended Pattern: Agent Commits Locally, Human Pushes

The agent commits freely to the local repository after each meaningful state change. The human reviews commits before pushing to the remote.

**Why this works:**

- **Granular history** — Each state change is a separate commit with a meaningful message
- **No friction** — The agent doesn't pause for human approval on every change
- **Review before publish** — You can scan `git log` before pushing, revert anything you disagree with
- **Rollback capability** — Individual commits can be reverted without affecting others
- **Push is the deliberate gate** — Pushing to remote is the human saying "I'm satisfied with these changes"

**In practice (VS Code + Copilot):**

1. You ask the agent to update things
2. The agent modifies files and commits with structured messages
3. You continue working — more changes, more commits
4. At session end (or whenever you choose), you review the commits: `git log --oneline -10`
5. If everything looks good, push: `git push`
6. If something is wrong, revert the specific commit: `git revert <hash>`

**In practice (CLI tools):**

Same pattern. The agent commits. You push when ready.

### Alternative: Agent Stages, Human Commits

For users who want more control:

1. The agent modifies files and stages them (`git add`)
2. The agent suggests a commit message
3. The human reviews the staged diff, approves or adjusts the message, and commits

This adds friction but gives the human approval over every commit. Useful for sensitive domains (compliance, financial) where every committed change should be deliberately approved.

### What The Agent Should Not Do

- **Never push without explicit human instruction** — Push is always a deliberate human action
- **Never force-push** — History is sacred in this framework
- **Never amend published commits** — Once pushed, commits are immutable
- **Never commit credentials, secrets, or sensitive data** — Things may contain personal or regulated information; the agent should be aware of what's being committed

## The Machine Axis: One Corpus, Several Clones

The commit is the moment state becomes real — **on the machine that made it**.
The moment it becomes real *to the estate* is publication: the push that puts it
on the remote, and the fetch that brings it into every other clone. A domain
worked from two machines (local and cloud), or by two people, is one corpus
whose event stream is only whole on the remote. This section extends
commit-is-real across that axis; it invents nothing — git already solved
distributed state, and the framework only has to decide *when* to read it and
*who* resolves the one case git refuses to.

### Sync Is Orientation, Not Transport Convenience

Orientation reads committed state: velocity, triggers, verified flips, and the
audit all read `git log`. If the local clone is behind the remote, orientation
reads a stale event stream — silently. So a session in a multi-machine estate
**syncs before it orients**: fetch, then fast-forward, then load the kernel and
read velocity. This is what `mdllm estate-sync` mechanises and the
`session-start:estate-sync` hard hook (orchestration.md) schedules.

### The Inbound Rules

- **Fast-forward only** (`git pull --ff-only`). A fast-forward is pure
  transport of state that is already real elsewhere — safe to take silently.
- **Divergence is reported, never resolved.** If both clones committed since
  the last sync, the merge is a decision, not a mechanism
  (`divergence-is-an-unrouted-decision`): the tool reports `DIVERGED (+a/+b)`
  and the operator routes the resolution. Never auto-merge, never rebase
  automatically, never reset — a force-pushed remote surfaces as divergence
  too, and history stays sacred in both directions.
- **Bounded and degrading.** Sync attempts are time-boxed and never prompt
  (`GIT_TERMINAL_PROMPT=0`); offline or auth failure degrades to one advisory
  line — "orienting from last-fetched state" — and the session proceeds. A
  session start must never *require* the network (orchestration.md, the
  upward version check's doctrine, which this sharpens rather than violates).
- **A dirty working tree is never touched.** Fetch is always safe; the
  fast-forward is skipped and reported. Session-end discipline (nothing left
  uncommitted) makes this rare; the guard makes it harmless.

### Publication Debt

The push stays the human's deliberate act — nothing in this section changes
"never push without explicit human instruction." What changes is visibility:
an unpushed commit is real locally and **invisible to the estate**, and the
other machine's next sync cannot find it. The session-end ritual therefore
reports publication debt — `mdllm estate-sync --status` lists `ahead +n
(unpushed)` per repo from cached tracking refs, no network — turning the push
from something remembered into something surfaced. A harness may carry a
standing per-session push instruction from the operator (the cloud bootstrap
does); that *is* explicit human instruction, held at config level.

When collaborators arrive, the same rules hold — a colleague's push appears at
your next session start as `synced (+n)`, divergence stays a routed decision —
with PR flow on shared repos per Multi-User Domains below.

## Git Log As Event Stream

When commits happen at meaningful state boundaries with structured messages, `git log` becomes a parseable event stream.

### Session Start Orientation

When the agent loads at session start, it can check recent commits to understand what happened since the last session:

```
git log --oneline --since="2026-05-18"
```

Output:
```
a1b2c3d complete: data-collection → unblocks 2 things
e4f5g6h create: stakeholder-feedback (task, high, due 2026-06-01)
i7j8k9l reprioritize: 3 tasks elevated to high
m0n1o2p session-end: changes from session 1 (18 May)
```

The agent immediately knows: data-collection was completed, a new task was created, priorities shifted. This is richer context than just reading the current state of things — it's the *narrative of what happened*.

### Trigger Evaluation Against History

Triggers watch for state changes. Git history records state changes. The connection:

1. Agent loads at session start
2. Scans recent commits for status transitions (`complete:`, `block:`, `unblock:`)
3. Checks: "Do any active triggers watch the things that changed?"
4. If a dependency trigger was watching `data-collection` for completion, and the commit log shows `complete: data-collection`, the trigger fires

Git history is the event log. Triggers are the listeners. The agent is the evaluator.

### Git Log As Domain Telemetry

Session orientation reads the log to answer "what changed since I was last here?" But the
same log answers a sharper, reflexive question: **"what should have changed and didn't?"**
This is *velocity* — the movement of the domain over time — and it is visible only in the
history, never in the current state. A thing parked at `status: in-progress` for six weeks
looks identical to one updated this morning until you consult its commit recency.

Two reads expose it:

```
git log --format="%ad %s" --date=short -- things/      # full cadence of state changes
git log --diff-filter=M --name-only --since="30 days ago" -- things/   # what actually moved recently
```

From these the agent reads velocity signals — stalled in-progress work, untouched
high-priority commitments, churn without completion, unblocks that led nowhere, and the
overall commit cadence (accelerating, steady, gone quiet). This is the reflexive
counterpart to current-state orientation, performed by the `domain-velocity` prompt
(`templates/prompts/domain-velocity.md`) at `session-start`.

**Velocity needs no derived index.** Unlike triggers, schema, and relationships — which are
aggregated into derived indexes to avoid re-scanning every thing (`derived-index.md`) — the
velocity signal already lives in the git log, which is itself the authoritative event
stream. Caching it would only add a surface that can drift from the history it summarises.
Read the log directly.

### Diff As Truth

When the agent needs to verify what actually changed (not just what the commit message says), `git diff` provides byte-level truth:

```
git diff HEAD~1 -- things/quarterly-review-prep.md
```

This shows exactly what fields changed, what narrative was updated, what relationships were added. Useful for:

- Verifying that a "complete" commit actually set `status: completed`
- Understanding the scope of a "reprioritize" batch change
- Auditing what the agent did during a write session

## Two Layers Of Auditability

The framework has two complementary audit layers — both **git**:

| Layer | What It Captures | Granularity | Created By |
|-------|-----------------|-------------|------------|
| **Git log** | The backward record — what changed, in what order, and *why* (the commit message is the narrative) | Commit-level | Agent (commits) |
| **Git diff** | Exact modifications — what bytes changed in which files | Byte-level | Automatic |

These serve different purposes:

- **Git log** answers: "What happened, in what order, and why?" (events, sequence, intent)
- **Git diff** answers: "What exactly changed?" (forensic detail)

Together they provide complete traceability from intent through action to detail. The
**commit message carries the narrative**, so write rich ones — there is no separate
log to hold it.

## Branching (Future Consideration)

For single-user domains, working on `main` is sufficient. But branching has potential for two scenarios that may emerge as the framework matures:

### Speculative Exploration

"What if I reprioritise everything around this new goal?"

1. Create a branch: `git checkout -b explore/q3-reprioritize`
2. Let the agent reorganise things on the branch
3. Review the diff against `main`: `git diff main`
4. If you like it, merge. If not, delete the branch.
5. No risk to your current state.

### Multi-User Domains

When two or more people work within the same domain:

1. Each person works on their own branch (or the agent creates per-session branches)
2. Changes are reviewed via pull request before merging to `main`
3. Conflicts are resolved at merge time — git handles file-level conflicts; the agent can help reason about semantic conflicts (two people updated the same thing's priority differently)
4. `main` is always the agreed-upon truth

This follows the standard git-flow pattern that development teams already know. The framework doesn't need to invent a new collaboration model — git already solved this.

**This is noted for future development. Start with `main` only.**

## Integration With Other Framework Components

### With write.thing.md

The write skill should be aware of commit points. After modifying things, the agent should commit with a structured message. The write workflow becomes: reason → modify → validate → commit.

### With validate.thing.md

Validation can run as a pre-commit check. Before the agent commits, it validates the things being committed. If errors exist, the commit is held until they're resolved. Warnings are noted in the commit message body.

### With Triggers (thing.md)

Triggers evaluate against committed state. A dependency trigger watching for `status: completed` doesn't fire on a file save — it fires when the commit containing that status change is made. This means commit discipline directly affects trigger reliability.

### With interface.md

The push action is an output route decision. When and how you push to remote depends on your interface:

- VS Code: push via source control panel or terminal
- CLI: `git push` when ready
- Automated: a scheduled push (if your domain warrants it)

### With `mdllm worklog`

`mdllm worklog` prints an on-demand, session-grouped *view* of the commit stream
(sessions delimited by `session-end:` commits). It is **not** committed — a committed
WORKLOG was generated *from* git and committed *back into* it (circular duplication,
retired in v3.17; `orient-and-reconciliation-are-the-corpus-two-sides`). The backward
record is git itself, and the narrative lives in the commit messages.

## Summary

| Concern | Answer |
|---------|--------|
| When is state "real"? | At commit time |
| When to commit? | After each meaningful state change (creation, status transition, write session, session end) |
| What do commit messages say? | Domain state changes, not file modifications |
| Who commits? | Agent commits locally; human pushes to remote |
| Who pushes? | Always the human, always deliberate |
| How does history help? | Git log is the event stream; triggers evaluate against it; session orientation reads it |
| What about branching? | `main` only for now; branching for exploration and collaboration later |
| What about rollback? | Revert specific commits; granular commits make this surgical, not destructive |

---

## Autocommit Mode

### The Problem With Manual Commit Prompting

The workflow above describes *when* to commit, but relies on the user explicitly asking the agent to commit. In practice, this creates a gap: the agent modifies things, the user continues working, and uncommitted state accumulates. The git-as-state-machine model breaks down when commits don't happen at state boundaries.

### The Solution: Autocommit Directive

A domain or framework agent can declare **autocommit mode** in its AGENTS.md. When autocommit is active, the agent commits automatically after every meaningful state change — without waiting for user prompting.

#### Declaring Autocommit

In AGENTS.md frontmatter:

```yaml
---
name: My Domain
version: 1.0
applies_to: "**/*.md"
git:
  autocommit: true
  branch: main
---
```

Or in the agent's behavioural rules:

```markdown
## Git Behaviour

This agent operates in **autocommit mode**. After every state change to a thing
(creation, status transition, update, deletion), the agent:

1. Validates the changed things
2. Stages the modified files
3. Commits with a structured message following git-workflow.md conventions
4. Continues with the next operation

No user prompting is required. The commit happens as part of the write operation itself.
```

#### When Autocommit Fires

Autocommit triggers at the same natural commit points defined earlier in this spec:

| Event | Autocommit Action |
|-------|-------------------|
| Thing created | `git add` + `git commit -m "create: {id} ({type}, {status})"` |
| Status transition | `git add` + `git commit -m "complete/block/unblock: {id} → {consequence}"` |
| Thing updated | `git add` + `git commit -m "update: {id} — {what changed}"` |
| Batch operation | `git add` + `git commit -m "{action}: {summary}"` |
| Validation fixes | `git add` + `git commit -m "validate: {summary}"` |
| Session end | `git add` + `git commit -m "session-end: {summary}"` |

#### The Autocommit Sequence

```
Agent modifies thing(s)
    ↓
Validate changed things (structural, referential)
    ↓ (pass)
git add <changed files>
    ↓
git commit -m "<structured message>"
    ↓
Continue to next operation or report to user
```

#### Terminal Execution Note

When executing git commands via tool-based terminals (VS Code Copilot, Cursor, etc.), **run `git add` and `git commit` as separate sequential commands** — not chained with semicolons or `&&`. Some terminal tool implementations simplify or collapse chained commands, causing only the first command to execute. This results in files being staged but never committed (or neither staged nor committed), silently breaking autocommit.

```
# DO — separate commands
git add <files>
git commit -m "<message>"

# DON'T — chained (may be collapsed by terminal tools)
git add <files>; git commit -m "<message>"
git add <files> && git commit -m "<message>"
```

If validation fails:
```
Agent modifies thing(s)
    ↓
Validate changed things
    ↓ (fail)
Fix validation errors
    ↓
Re-validate
    ↓ (pass)
git add + git commit
```

#### Autocommit Does NOT Push

The safety boundary remains: **autocommit commits locally only**. Push is still a deliberate human action. This preserves:

- The ability to review before publishing
- The ability to revert locally without affecting remotes
- The human gate for shared repositories

#### Framework-Level Autocommit

The **framework-level agent** (the AGENTS.md at the repository root) can declare autocommit to ensure that all framework specification changes are persisted immediately:

```yaml
git:
  autocommit: true
  branch: main
```

This means: when working at the framework level, any modification to specifications, guides, skills, or framework configuration is automatically committed. The framework agent acts as the steward of persistent state.

#### Domain-Level Autocommit

Individual domains can independently choose their commit mode:

- **autocommit: true** — Every thing change is automatically committed. Best for domains where state persistence is critical (compliance, audit trails, production analysis).
- **autocommit: false** — Manual commit mode. The agent stages changes but waits for user instruction to commit. Best for exploratory or draft-heavy work.

A domain inherits no commit behaviour from the framework. Each domain declares its own `git` configuration.

#### Batch Awareness

Autocommit is **operation-aware**, not file-aware. If a single user request results in modifications to 5 things (e.g., "reprioritise my Q3 tasks"), the agent:

1. Makes all 5 modifications
2. Validates all 5
3. Commits once with a batch message: `reprioritize: 5 tasks updated for Q3 alignment`

It does NOT commit after each individual file change. The commit boundary is the **logical operation**, not the file save.

#### Scope Boundary: Current Operation Only

Autocommit commits **only the files modified in the current operation**. It does not commit:

- Files left uncommitted from previous sessions (they remain in the working directory)
- Files staged but not modified in this operation
- Files in `.gitignore` or otherwise excluded

This ensures that:
- Stale changes from previous sessions aren't accidentally bundled into new commits
- Each commit reflects exactly what the agent did in the current operation
- You maintain explicit control over leftover uncommitted changes (review or discard them intentionally)

#### Interaction With Triggers

Autocommit strengthens the trigger system. Because commits happen immediately after state changes, triggers that watch for committed state (dependency triggers, threshold triggers) evaluate promptly rather than waiting for the user to remember to commit.

```
Thing A completed → autocommit fires → commit recorded →
    trigger evaluates → Thing B unblocked → autocommit fires → commit recorded
```

This creates a reactive chain where state changes propagate through the system automatically.
