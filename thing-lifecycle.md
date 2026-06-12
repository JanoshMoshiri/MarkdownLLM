---
id: thing-lifecycle-specification
type: specification
status: draft
version: 0.1
created: 2026-05-23
linked_things:
  - id: thing-specification
    relation: extends
  - id: scalability-guide
    relation: complements
  - id: read-thing-specification
    relation: informs
  - id: write-thing-specification
    relation: informs
  - id: git-workflow-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
---

# Thing Lifecycle

## What This Specifies

This document defines how things transition through lifecycle stages — from active use through disposition to semi-active storage and eventual retrieval. It addresses the hard ceiling on domain thing count by introducing a time-based rolling window with rule-based disposition, enabling domains to grow from hundreds to thousands of things without breaking the agent's reasoning capacity.

This specification is **drafted but not deployed**. It follows the framework principle of *spec when foreseeable, deploy when felt*. The design is captured here so that when a domain hits the scaling ceiling, the solution is ready to activate.

## The Problem

The scalability guide documents the ceiling: at ~200-300 active things, an agent begins to feel friction. At ~1,000, the framework's principle of direct LLM reasoning over unindexed data breaks down. Current approaches (contextual loading, manual summaries, tiered loading) mitigate but don't solve.

The root cause: **every thing occupies the same amount of context regardless of whether it's actively relevant.** A task completed three months ago occupies the same space as one due tomorrow.

## Prior Art

This specification draws from five established paradigms rather than inventing new patterns:

| Pattern | Origin | What we take |
|---|---|---|
| **S3 Lifecycle Policies** | AWS | Declarative, rule-based transitions between tiers based on age |
| **Hierarchical Storage Management** | IBM, 1978 | Transparent retrieval — the user doesn't think about tiers |
| **Log Rotation** | Unix (logrotate) | Periodic maintenance rhythm — check and rotate at session boundaries |
| **Information Lifecycle Management** | Records management | Legal holds (= pin) — exemptions that override normal lifecycle rules |
| **LSM Trees** | Database engineering | Manifest as bloom filter — lightweight "is it there?" checks |

The framework's contribution is not any of these patterns individually. It is how they compose within a markdown-and-git domain where the reasoning engine is an LLM.

## Concepts

### Active Window

The **active window** is the rolling time period within which things remain at full depth — complete frontmatter and narrative body. By default, this is **30 days** from the thing's `last_active` date.

Things inside the active window are loaded, reasoned about, and managed as normal. Nothing changes for them.

### Disposition

**Disposition** is the process of transitioning a thing from active storage to semi-active storage. In Information Lifecycle Management terminology, this is not compression, archival, or deletion — it is the movement of a record from active to semi-active status based on lifecycle rules.

In practice, disposition means: the thing's narrative body is replaced by a summary, and the thing is relocated to the domain's `archive/` directory. The thing remains a valid thing file — individually addressable, with meaningful frontmatter, producing clean git diffs. It is simply lighter.

### Semi-Active Storage

**Semi-active storage** is the state of a thing after disposition. The thing exists as a **stub** — its frontmatter is retained and augmented with lifecycle metadata, but its narrative body has been replaced by a `summary` field.

A semi-active thing:
- Is still a valid thing file (frontmatter + minimal body)
- Is still individually addressable by id
- Is still linkable via `linked_things`
- Produces meaningful git diffs if modified
- Is human-readable in a text editor
- Occupies roughly 10-20% of its original context footprint

### Rehydration

**Rehydration** is the reverse of disposition — restoring a semi-active thing to full active status. The full content is recovered from git history (the commit prior to disposition contains the complete narrative), and the thing is moved back from `archive/` to `things/`.

### Pin

A **pin** exempts a thing from disposition regardless of age. Pinned things remain in active storage indefinitely. This is the equivalent of a legal hold in records management — an override that says "this thing is still relevant despite its age."

## The Stub Format

When a thing is disposed to semi-active storage, its file is transformed into a stub. The stub retains all original frontmatter fields and adds lifecycle-specific fields.

### Added Frontmatter Fields

```yaml
# Lifecycle fields (added at disposition)
lifecycle:
  state: semi-active          # active | semi-active
  disposed_date: 2026-04-20   # when disposition occurred
  last_active: 2026-04-18     # last commit date when the thing was modified
  rehydration_tokens: ~850    # estimated token cost to restore full content
  summary: "Fixed rear derailleur alignment — replaced hanger, indexed gears, test ride confirmed"
```

### What Is Retained

- All original frontmatter fields (`id`, `type`, `status`, `created`, `priority`, `tags`, `linked_things`, `dependencies`, `blocks`, etc.)
- The lifecycle block above

### What Is Removed

- The full narrative body (markdown content below the frontmatter)

### What Replaces It

A minimal body referencing the summary:

```markdown
# [Original Title]

*This thing is in semi-active storage. See `lifecycle.summary` for overview. Full content is recoverable from git history.*
```

### Example: Before Disposition

```markdown
---
id: fix-bike-derailleur
type: task
status: completed
created: 2026-03-10
priority: medium
tags: [bike, maintenance]
linked_things:
  - id: spring-bike-service
    relation: subtask
---

# Fix Bike Derailleur

The rear derailleur has been skipping gears under load, particularly
in the 3rd and 4th cogs. This started after the chain replacement
last month.

## Investigation

Checked cable tension — within spec. Checked limit screws — fine.
Found the derailleur hanger is slightly bent, likely from the fall
on the gravel path last week.

## Resolution

Ordered a replacement hanger (Shimano RD-M786 compatible). Installed
and re-indexed all gears. Test ride confirmed smooth shifting across
all 10 speeds under load.

## Parts Used

- Derailleur hanger: £12.99
- Cable end caps (replaced while there): £1.50
```

### Example: After Disposition

```markdown
---
id: fix-bike-derailleur
type: task
status: completed
created: 2026-03-10
priority: medium
tags: [bike, maintenance]
linked_things:
  - id: spring-bike-service
    relation: subtask
lifecycle:
  state: semi-active
  disposed_date: 2026-04-20
  last_active: 2026-03-15
  rehydration_tokens: ~850
  summary: "Fixed rear derailleur alignment — replaced bent hanger (£12.99), re-indexed all gears, test ride confirmed smooth shifting across all 10 speeds"
---

# Fix Bike Derailleur

*This thing is in semi-active storage. See `lifecycle.summary` for overview. Full content is recoverable from git history.*
```

## Eligibility Rules

Not every thing outside the active window is eligible for disposition. Eligibility is determined by **age AND status**.

### Age Rule

A thing is age-eligible when its `last_active` date (or `created` date if `last_active` is not set) is older than the configured window (default: 30 days).

### Status Rule

Only things with terminal or settled statuses are eligible:

| Status | Eligible | Rationale |
|---|---|---|
| `completed` | Yes | Work is done |
| `cancelled` | Yes | Work was abandoned |
| `not-started` | No | May still be acted on |
| `in-progress` | No | Actively being worked |
| `blocked` | No | Waiting on resolution |
| `paused` | No | Intentionally deferred but still alive |

Domains can configure additional eligible or exempt statuses via their AGENTS.md.

### Pin Override

Any thing with `pin: true` in its frontmatter is exempt from disposition regardless of age or status.

```yaml
---
id: reference-architecture
type: resource
status: completed
created: 2025-06-01
pin: true
---
```

### Effective Rule

A thing is eligible for disposition when ALL of the following are true:
1. `last_active` is outside the rolling window (> 30 days ago)
2. `status` is in the eligible set (`completed`, `cancelled`)
3. `pin` is not `true`

## Defining "Last Active"

`last_active` is the date of the most recent commit that modified the thing's file. This is simple, auditable, and uses git as the source of truth.

`last_active` updates when:
- The thing's content or frontmatter is modified and committed
- The thing is explicitly referenced and modified during a session

`last_active` does NOT update when:
- The agent scans the thing's metadata during a Level 1 load
- The agent reads the thing during relationship traversal without modifying it
- Another thing that links to this one is modified

This ensures that routine scanning doesn't reset the clock. Only meaningful engagement — resulting in a committed change — extends a thing's active window.

## Domain Configuration

Domains configure lifecycle behaviour in their AGENTS.md frontmatter:

```yaml
---
name: My Domain
version: 1.0
applies_to: "**/*.md"
git:
  autocommit: true
  branch: main
lifecycle:
  enabled: true
  window: 30d
  mode: suggest          # off | suggest | auto
  pin_statuses:
    - in-progress
    - blocked
    - paused
    - not-started
  archive_path: archive/
---
```

### Mode Options

| Mode | Behaviour |
|---|---|
| `off` | Lifecycle management is disabled. All things remain active. |
| `suggest` | At session start, the agent identifies eligible things and suggests disposition. The user approves before any action is taken. |
| `auto` | The agent automatically disposes eligible things during session-start maintenance. The user is informed but not asked for approval. |

The recommended progression: start with `suggest`, escalate to `auto` once the domain operator trusts the mechanism. This mirrors the autocommit pattern.

## The Disposition Process

### When It Runs

Disposition is a **session-start maintenance step**. Like logrotate running as a cron job, the agent checks for eligible things at the beginning of each session — not continuously during normal operation.

### Sequence (Suggest Mode)

```
Session start
    ↓
Agent scans all things in things/ directory (Level 1 — metadata only)
    ↓
Identify things where: age > window AND status ∈ eligible AND pin ≠ true
    ↓
Report to user: "5 things are eligible for disposition. [list with ids and summaries]"
    ↓
User approves (all, some, or none)
    ↓
For each approved thing:
    1. Generate summary from narrative body
    2. Add lifecycle block to frontmatter
    3. Replace narrative body with stub text
    4. Move file from things/ to archive/
    5. Update manifest
    ↓
git add (changed files)
    ↓
git commit -m "lifecycle: dispose 5 things to semi-active storage"
```

### Sequence (Auto Mode)

Same as above, but steps 4-5 (report and approve) are replaced with an informational message after disposition is complete.

### Summary Generation

The agent generates the `lifecycle.summary` field by reading the full narrative body and producing a concise summary that captures:
- What the thing was about (one sentence)
- Key outcomes or decisions
- Any data that would be needed to determine relevance in a future search

The summary should be **one to three sentences**. It is not a compression of the full narrative — it is a signal that helps the agent (and humans) decide whether to rehydrate.

## The Manifest

The manifest is a framework artifact (not a thing) that provides a lightweight index of all semi-active things in the domain.

### Location

`archive/_manifest.md`

### Format

```markdown
---
id: archive-manifest
type: artifact
entries: 47
last_updated: 2026-05-20
---

# Archive Manifest

| id | type | status | disposed_date | summary |
|---|---|---|---|---|
| fix-bike-derailleur | task | completed | 2026-04-20 | Fixed rear derailleur alignment — replaced hanger, indexed gears |
| q1-budget-review | project | completed | 2026-04-15 | Quarterly budget review and reallocation, approved by finance |
| legacy-migration | project | cancelled | 2026-04-10 | Database migration cancelled — vendor provided API instead |
```

### Purpose

The manifest serves as the domain's **bloom filter** — a single file the agent can scan to determine whether a relevant semi-active thing exists, without opening individual stub files. For most recall queries ("what was that thing about X?"), the manifest table is sufficient to identify candidates for rehydration.

### Maintenance

The manifest is updated automatically whenever disposition or rehydration occurs. It is committed as part of the same transaction.

## Retrieval and Rehydration

### Three Retrieval Paths

| Path | When it triggers | How it works |
|---|---|---|
| **Manifest search** | User asks about something not in the active window | Agent scans `archive/_manifest.md`, matches query against summaries, identifies candidates |
| **Relationship traversal** | Agent follows a `linked_things` reference to a semi-active thing | Agent detects the target is a stub (`lifecycle.state: semi-active`), retrieves full content from git history |
| **Period summary** | User asks about a time window | Agent loads a `type: period-summary` thing (if one exists) for narrative overview, then drills into manifest if needed |

### The Rehydration Process

When a semi-active thing needs to be restored to full active status:

1. **Locate the disposition commit** — find the commit where the thing was disposed (the `lifecycle.disposed_date` narrows the search)
2. **Recover the full content** — `git show <commit>~1:things/<filename>` retrieves the file as it was before disposition
3. **Restore the file** — move from `archive/` back to `things/`, replace stub content with recovered full content
4. **Update frontmatter** — set `lifecycle.state: active`, update `last_active` to today
5. **Update manifest** — remove the entry
6. **Commit** — `lifecycle: rehydrate <id> — returned to active storage`

### Promotion Logic

If a semi-active thing is accessed (rehydrated for reference) multiple times within a short period, the agent should suggest or automatically promote it back to active storage. This mirrors HSM's automatic promotion of frequently-accessed cold data to hot storage.

A reasonable threshold: if a semi-active thing is rehydrated **3 or more times within a 7-day window**, it should be promoted to active.

## Period Summaries

Period summaries are an optional complement to the manifest. They are regular things (not artifacts) that capture a narrative overview of what happened during a time window.

### Format

```markdown
---
id: period-summary-2026-q1
type: period-summary
status: completed
created: 2026-04-01
covers: 2026-01-01/2026-03-31
thing_count: 47
---

# Q1 2026 Summary

## Projects Completed (3)
- Project A: shipped on time, 5 people, £200k budget
- Project B: shipped late due to feedback iterations, 3 people, £80k
- Project C: cancelled mid-project due to strategic shift

## Key Themes
- Feedback loops need defined windows
- Strategic alignment should happen earlier in the process

## What It Unblocked
- Q2 product roadmap now has clear inputs
- 2 team members freed for Q2 initiatives
```

Period summaries are **not required** for lifecycle management to function. They are a convenience for domains that want high-level temporal narratives in addition to the individual stubs in the manifest.

## Capacity Impact

### Estimated Token Budget

| Component | Things | Tokens per thing | Total tokens |
|---|---|---|---|
| Active window (full depth) | 50-80 | ~500-2,000 | ~25,000-160,000 |
| Manifest (index scan) | 500 | ~30-50 | ~15,000-25,000 |
| Period summaries | 4-8 | ~300-500 | ~1,200-4,000 |

### Net Effect

A domain using lifecycle management can sustain **500-1,000+ total things** while keeping per-session context within the range that currently supports 50-80 things. This is a **5-10x capacity increase** without changing the data format, the file structure, or the framework's principle of direct LLM reasoning over data.

## Integration With Other Specifications

### With thing.md

Thing.md defines the atomic unit. This specification adds optional lifecycle fields (`lifecycle` block, `pin`) to the frontmatter schema. These fields are not required — things without lifecycle fields are treated as active.

### With read.thing.md

The read specification's tiered loading model (Level 1: metadata, Level 2: relationships, Level 3: full context) is complemented by lifecycle state. Semi-active things are always loaded at Level 1 (via the manifest). Rehydration is essentially a Level 3 load from git history.

### With write.thing.md

The write specification's post-modification checks should evaluate whether a rehydrated thing should remain active or return to semi-active after the current operation.

### With git-workflow.md

Disposition and rehydration are commit-worthy events. They follow the same commit conventions:
- `lifecycle: dispose 5 things to semi-active storage`
- `lifecycle: rehydrate fix-bike-derailleur — returned to active storage`

Autocommit mode applies to lifecycle operations.

### With scalability-guide.md

This specification should be referenced as **Approach 4: Lifecycle Management** in the scalability guide, positioned between Approach 2 (manual summaries) and Approach 3 (tiered loading). When deployed, the scalability guide should be updated with a cross-reference.

## Deployment Checklist

When a domain is ready to activate lifecycle management:

- [ ] Add `lifecycle:` block to domain AGENTS.md frontmatter
- [ ] Create `archive/` directory in domain root
- [ ] Create initial `archive/_manifest.md` with empty table
- [ ] Add lifecycle awareness to domain read/write skills
- [ ] Run first disposition cycle in `suggest` mode
- [ ] Validate: stubs are readable, manifest is accurate, git diffs are clean
- [ ] Validate: rehydration works from git history
- [ ] Escalate to `auto` mode when confident

## Status

This specification is `draft` — designed but not yet validated through real-world use. It will be activated and promoted to `evolving` when a domain encounters the scaling ceiling that motivates it.
