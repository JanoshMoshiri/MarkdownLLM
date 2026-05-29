---
id: validate-thing-specification
name: Validate Thing
type: specification
status: stable
version: 1.3
created: 2026-05-19
description: Universal validation of thing files and prompt files — structural integrity, referential consistency, semantic coherence, conflict detection, and orchestration graph integrity
applies_to: "**/things/**/*.md"
linked_things:
  - id: thing-specification
    relation: validates
  - id: orchestration-specification
    relation: validates
  - id: belief-revision-specification
    relation: integrates-with
---

# Validate Thing Skill

You are validating thing files within a domain using the LLM-driven systems framework. Your role is to check that things are structurally sound, referentially consistent, and semantically coherent. You report issues clearly so they can be fixed.

## System Context

Before validating:

1. Read `thing.md` — understand the universal required structure for all things
2. Read the domain's `[domain]-specification.skill.md` — understand domain-specific field requirements, valid types, and constraints
3. Load the thing files to be validated

## When Validation Runs

Validation is invoked at three moments:

1. **After writes** — When the agent creates or modifies things, validate before committing. Issues are caught before they persist.
2. **Session start** — Quick scan during orientation. Report: "N things have issues since your last session."
3. **On demand** — User asks "validate my things", "check integrity", or "are my things clean?"

## Validation Levels

Validate in order. Each level builds on the previous. Stop and report at the first level where issues are found, unless the user asks for a full report.

### Level 1: Structural Validation

**What:** Is each thing file well-formed and does it meet the universal minimum requirements defined in `thing.md`?

**Check every thing file for:**

| Check | Rule | Severity |
|-------|------|----------|
| YAML frontmatter exists | File starts with `---` and has a closing `---` | Error |
| YAML is parseable | No syntax errors in the frontmatter block | Error |
| `id` present | Field exists and is not empty | Error |
| `id` format | Lowercase, hyphens only, no spaces (e.g., `my-thing-id`) | Warning |
| `id` matches filename | The `id` value matches the filename (without `.md` extension) | Warning |
| `type` present | Field exists and is not empty | Error |
| `status` present | Field exists and is not empty | Error |
| `status` value valid | One of: `not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled`. **Exception:** `type: specification`, `type: guide`, and `type: manifesto` things use lifecycle statuses: `draft`, `evolving`, `stable`, `deprecated`. `type: insight` things use: `active`, `promoted`, `dismissed`. | Error |
| `created` present | Field exists and is not empty | Error |
| `created` format | Valid ISO 8601 date or datetime | Error |
| `due_date` format | If present, valid ISO 8601 date | Warning |
| `linked_things` structure | If present, each entry has at minimum `id` and `relation` | Error |
| `dependencies` structure | If present, is an array of strings (IDs) | Error |
| `blocks` structure | If present, is an array of strings (IDs) | Error |
| `triggers` structure | If present, each entry has `type` and `action` | Error |
| Markdown body exists | Content exists after the YAML frontmatter closing `---` | Warning |
| Title heading exists | Markdown body starts with a `#` heading | Warning |

**Severity definitions:**
- **Error** — Must be fixed. The thing is malformed and may cause incorrect reasoning.
- **Warning** — Should be fixed. The thing is functional but doesn't follow conventions.

### Level 2: Referential Validation

**What:** Do relationships between things hold? Do referenced IDs point to things that actually exist?

**Requires:** Loading all thing files in the domain (metadata only — Level 1 context window).

| Check | Rule | Severity |
|-------|------|----------|
| `linked_things` IDs exist | Every `id` in `linked_things` corresponds to an existing thing file | Error |
| `dependencies` IDs exist | Every ID in `dependencies` corresponds to an existing thing file | Error |
| `blocks` IDs exist | Every ID in `blocks` corresponds to an existing thing file | Error |
| Trigger `watch` IDs exist | Every ID in trigger `watch` fields corresponds to an existing thing file | Error |
| `parent` ID exists | If `parent` is set, the referenced thing file exists | Error |
| Bidirectional consistency | If A lists B in `blocks`, B should list A in `dependencies` (or at minimum in `linked_things`) | Warning |
| No circular dependencies | Following the dependency chain does not loop back to the starting thing | Error |
| No orphaned things | Thing has at least one relationship, one trigger, or is referenced by another thing. Completely isolated things are flagged. | Info |
| No duplicate IDs | No two thing files in the domain share the same `id` value | Error |

**Severity addition:**
- **Info** — Not necessarily wrong, but worth knowing. Orphaned things may be intentional (new, standalone) or may be forgotten.

### Level 3: Domain-Specific Validation

**What:** Does this thing satisfy the rules defined in the domain's specification skill?

**Requires:** Reading `[domain]-specification.skill.md` to discover domain constraints.

**What to look for in the domain spec:**

1. **Valid types** — The spec lists thing types for this domain (e.g., `project`, `task`, `goal`, `pattern`). Check that each thing's `type` matches one of the declared types.

2. **Required domain fields** — The spec may declare fields that are mandatory in this domain beyond the universal core. For example, a compliance domain might require `data_classification` on every thing, or a project management domain might require `assigned_to`.

3. **Valid relationship types** — The spec may define which `relation` values are valid in `linked_things` for this domain (e.g., `subtask`, `blocks`, `supports`, `contrasts-with`).

4. **Status transitions** — If the spec defines a state machine (valid transitions between statuses), check that the current status is reachable. For example, a domain might say things cannot go directly from `not-started` to `completed` without passing through `in-progress`.

5. **Domain reasoning lenses** — If the spec defines reasoning lenses (e.g., domain logic, compliance logic, audit logic), check that things of certain types have the metadata those lenses require. For example, if the compliance lens requires `audit_logging_enabled`, flag things that handle personal data but lack this field.

**If no domain spec exists** (e.g., validating things in a domain that hasn't defined a specification skill), skip Level 3 entirely. Universal validation (Levels 1-2) still applies.

| Check | Rule | Severity |
|-------|------|----------|
| Type is declared | Thing's `type` matches a type listed in the domain spec | Warning |
| Domain-required fields present | All fields the domain spec marks as required are present | Error |
| Relationship types valid | `relation` values in `linked_things` match domain-defined types | Warning |
| Status transition valid | If domain defines a state machine, current status is reachable | Warning |
| Lens-required fields present | If domain defines reasoning lenses with field requirements, those fields exist on applicable things | Warning |

### Level 4: Semantic Validation

**What:** Does the thing make sense as a whole? Does the narrative match the metadata? Is it well-scoped?

**Requires:** Full context (Level 3 context window — complete thing files with narrative body).

This level uses your reasoning, not mechanical checks. Read the thing holistically and assess:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Metadata-narrative consistency | Status says `completed` but body says "waiting on feedback". Priority says `low` but body describes an urgent deadline. Tags don't match the content. | Warning |
| Scope appropriateness | Is this thing trying to do too much? Should it be split into sub-things? Is it so small it should be merged with a parent? | Info |
| Staleness | Status is `in-progress` but `created` date is months ago with no recent narrative updates. May be abandoned rather than active. | Info |
| Narrative completeness | Does the body explain what this thing is and why it matters? Or is it just a title with empty metadata? | Info |
| Trigger coherence | Do the triggers make sense for this thing? Is it watching things that are relevant to it? Are the actions appropriate? | Info |
| Duplicate or redundant | Does this thing substantially overlap with another thing in scope or intent? | Info |
| `contradicts` without conflict thing | A `linked_things` entry has `relation: contradicts` but no `type: conflict` thing exists listing both parties | Error |
| `supersedes` without update | A `linked_things` entry has `relation: supersedes` but the referenced thing has no corresponding `superseded-by` link or `status: deprecated` | Warning |
| Open conflict not in continuity brief | A `type: conflict` thing with `status: open` exists but is not listed in `continuity.md` | Warning |
| Stale open conflict | A `type: conflict` thing has `status: open` and has not been updated in more than 30 days | Info |
| No recent retrospective | The domain has been active for more than 60 days since the last `type: retrospective` thing (or has none at all) | Info |

**Important:** Level 4 is advisory. These are observations, not errors. Present them as "I noticed..." rather than "Fix this."

## How To Validate

### Scoping: What To Validate

| User Request | Scope |
|-------------|-------|
| "Validate my things" | All things in `things/` — Levels 1-3, Level 4 if few enough things |
| "Validate this thing" | Single thing — all four levels |
| "Quick check" | All things — Level 1 only |
| "Check my links" | All things — Level 2 only |
| "Deep review of X" | Single thing — all four levels with detailed narrative |
| "Are my things clean?" | All things — Levels 1-2, summary of issues |
| After a write operation | The thing(s) just modified — Levels 1-2 |

### Reporting Format

Report validation results grouped by severity, then by thing:

```
## Validation Report

### Errors (must fix)
- **thing-id-1**: Missing required field `status`
- **thing-id-2**: `linked_things` references `nonexistent-id` — no matching thing file found
- **thing-id-3**: YAML syntax error on line 5 — unexpected character

### Warnings (should fix)
- **thing-id-4**: `id` contains uppercase characters — convention is lowercase-hyphenated
- **thing-id-5**: Status is `completed` but narrative body says "still waiting on approval"
- **thing-id-6**: Blocks `thing-id-7` but `thing-id-7` doesn't list it as a dependency

### Info (worth knowing)
- **thing-id-8**: Orphaned — no relationships, not referenced by any other thing
- **thing-id-9**: Created 3 months ago, status `in-progress`, no narrative updates — may be stale

### Summary
- Things checked: 24
- Errors: 3
- Warnings: 3
- Info: 2
- Clean: 16
```

### Fixing Issues

When reporting issues, suggest the fix:

- For missing fields: "Add `status: not-started` to the frontmatter"
- For broken links: "Either create a thing with id `nonexistent-id`, or remove the reference from `linked_things`"
- For bidirectional inconsistency: "Add `dependencies: [thing-id-6]` to `thing-id-7`'s frontmatter, or add a `linked_things` entry"
- For semantic issues: "The body mentions waiting on approval but status is `completed` — consider updating status to `blocked` or updating the narrative"

If the user asks you to fix issues (not just report them), apply the write.thing skill to make corrections. Validate again after fixing to confirm resolution.

## What You Don't Do

- Do not silently fix issues without reporting them — always tell the user what you found and what you changed
- Do not enforce domain rules when no domain spec exists — fall back to universal rules only
- Do not treat Info-level observations as errors — they are advisory
- Do not block the user from working because of warnings — report and move on
- Do not invent validation rules beyond what `thing.md`, `orchestration.md`, and the domain spec define

## Prompt Validation

Prompts (`type: prompt`) are things and pass through all four validation levels above. They also have additional checks specific to their role in the orchestration layer.

### Prompt Structural Checks

These extend Level 1 for prompt things:

| Check | Rule | Severity |
|-------|------|----------|
| `type` is `prompt` | Confirm the thing is declared as a prompt | Error |
| `inputs` present | Array of input declarations exists in frontmatter | Warning |
| `inputs` structure | Each entry has `name` and `description` | Warning |
| `outputs` present | Array of output declarations exists in frontmatter | Warning |
| `outputs` structure | Each entry has `name` and `description` | Warning |
| `bound_to` present | At least one binding declaration exists | Warning |
| `bound_to` structure | Each entry has `hook` field | Error |
| Reasoning template exists | Markdown body contains a reasoning template section | Warning |

### Prompt Referential Checks

These extend Level 2 by validating the orchestration graph:

| Check | Rule | Severity |
|-------|------|----------|
| `bound_to` hooks exist | Each `hook` value matches a hook point declared in `orchestration.md` or a domain workflow skill | Error |
| No orphaned prompts | Prompt has at least one valid binding — a prompt that binds to nothing never fires | Warning |
| No missing prompts | All prompt IDs referenced in binding declarations (in AGENTS.md, orchestration.md, or workflow skills) have corresponding prompt files | Error |
| Input/output chain consistency | If prompt A's output feeds prompt B's input (same hook, B runs after A), B's declared input names should match A's declared output names | Warning |

### Prompt Semantic Checks

These extend Level 4 with orchestration-specific observations:

| Check | What to look for | Severity |
|-------|-----------------|----------|
| Reasoning template scope | Is the template focused on one reasoning task, or does it try to do too much? Prompts should be tighter than skills. | Info |
| Duplication across prompts | Does this prompt's reasoning template overlap significantly with another prompt or with prose in a skill file? | Warning |
| Quantity check | Are there more than 10 domain-level prompts? This signals potential over-specification. | Info |

### Prompt Validation Scope

| Trigger | What to check |
|---------|--------------|
| After creating or modifying a prompt | That prompt — structural + referential |
| "Validate my prompts" | All prompts — structural + referential + semantic |
| Session start (if prompts changed since last session) | Changed prompts — structural + referential |
| "Validate the orchestration" | All prompts + all bindings + hook point consistency |

## Key Principles

- **Errors are structural** — they mean the thing is broken and the agent may reason incorrectly over it
- **Warnings are conventional** — they mean the thing works but doesn't follow best practice
- **Info is observational** — they mean something is worth the user's attention but may be intentional
- **Validation is helpful, not hostile** — the goal is to catch problems early, not to gatekeep
- **Universal rules are fixed; domain rules are discovered** — read the domain spec to know what extra rules apply

## Validation Examples

Concrete examples anchor the agent's reasoning. Use these as reference patterns when validating.

### Clean Thing (Passes All Levels)

```yaml
---
id: quarterly-review-prep
type: task
status: in-progress
created: 2026-05-10
due_date: 2026-06-15
priority: high
linked_things:
  - id: data-collection
    relation: depends-on
  - id: stakeholder-feedback
    relation: depends-on
dependencies: [data-collection, stakeholder-feedback]
triggers:
  - type: dependency
    watch: [data-collection, stakeholder-feedback]
    condition: all_completed
    action: suggest_completion
---

# Quarterly Review Prep

## Summary
Prepare the Q2 quarterly review presentation for leadership.

## Current State
Data collection is complete. Waiting on stakeholder feedback before finalising slides.

## Next Steps
- Incorporate feedback once received
- Draft executive summary
- Schedule review meeting
```

**Why it passes:**
- Level 1: All required fields present, valid YAML, correct status value, ISO date format
- Level 2: `data-collection` and `stakeholder-feedback` exist as thing files; dependencies match linked_things; no circular references
- Level 3: `type: task` is a declared domain type; priority field present per domain spec
- Level 4: Narrative matches metadata — status says `in-progress`, body confirms work is underway but not complete

### Level 1 Failure: Structural

```yaml
---
id: Budget Analysis
type: task
status: active
created: last week
linked_things:
  - data-collection
---

```

**Violations:**
| Check | Issue | Severity |
|-------|-------|----------|
| `id` format | Contains uppercase and space — should be `budget-analysis` | Warning |
| `status` value | `active` is not a valid status (should be `in-progress`) | Error |
| `created` format | `last week` is not ISO 8601 | Error |
| `linked_things` structure | Entry is a bare string, not an object with `id` and `relation` | Error |
| Markdown body | No content after frontmatter — empty thing | Warning |

### Level 2 Failure: Referential

```yaml
---
id: design-review
type: task
status: blocked
created: 2026-05-12
dependencies: [client-sign-off, legacy-migration]
blocks: [launch-prep]
linked_things:
  - id: client-sign-off
    relation: depends-on
  - id: legacy-migration
    relation: depends-on
  - id: launch-prep
    relation: blocks
---

# Design Review

## Summary
Final design review before launch.

## Blocked By
Waiting on client sign-off and legacy migration to complete.
```

**Violations (assuming domain context):**
| Check | Issue | Severity |
|-------|-------|----------|
| `dependencies` ID exists | `legacy-migration` — no thing file with this ID exists in the domain | Error |
| Bidirectional consistency | This thing lists `blocks: [launch-prep]` but `launch-prep` does not list `design-review` in its `dependencies` | Warning |

### Level 4 Concern: Semantic Mismatch

```yaml
---
id: onboarding-docs
type: task
status: completed
created: 2026-03-01
priority: low
---

# Onboarding Documentation

## Summary
Create onboarding docs for new team members.

## Current State
Still drafting the technical setup section. Need input from DevOps on 
the CI/CD pipeline before this can be finalised. Hoping to have a first 
draft ready by end of month.
```

**Observations:**
| Check | Issue | Severity |
|-------|-------|----------|
| Metadata-narrative mismatch | Status says `completed` but body says "still drafting" and "hoping to have a first draft ready" — this thing is clearly `in-progress`, not `completed` | Warning |
| Staleness | Created 2026-03-01, status `completed`, but narrative describes ongoing work — likely the status was updated prematurely or the narrative is stale | Info |

## Validation Guarantee

Every check in this skill is LLM-performed. The agent reads YAML, follows relationships, and reasons about coherence — but it is not a deterministic parser. The examples above anchor the agent's pattern-matching and make results highly consistent in practice, but they remain non-deterministic. Structural checks (Levels 1-2) are reliable because the examples provide clear positive/negative anchors. Semantic checks (Level 4) are inherently subjective and advisory.

**For domains requiring auditable assurance** — compliance, finance, healthcare, or any domain subject to regulatory scrutiny — pair this skill with deterministic procedural checks outside the framework:

- **Levels 1-2 (structural, referential):** A YAML linter and link-integrity checker (~100 lines of Python) can run as a pre-commit hook or CI step, providing byte-level deterministic parsing that an LLM cannot guarantee.
- **Levels 3-4 (domain-specific, semantic):** These remain the LLM's strength — reasoning about coherence, scope, and intent is something code cannot replicate.

The intended division of labour: procedural scripts guarantee the mechanical checks; this skill provides the reasoning checks. Together they cover what neither can alone.
