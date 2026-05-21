---
id: validate-before-commit
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: staged-things
    description: "Thing files that have been modified and are about to be committed"
  - name: all-thing-ids
    description: "Index of all thing IDs in the domain for referential checks"
outputs:
  - name: validation-result
    description: "pass or fail with specific issues"
  - name: auto-fixes
    description: "Issues that were automatically corrected"
  - name: blocking-issues
    description: "Issues that prevent commit and require user input"
bound_to:
  - hook: pre-commit
linked_things:
  - id: orchestration-specification
    relation: defined-by
  - id: validate-thing-specification
    relation: implements
  - id: git-workflow-specification
    relation: integrates-with
---

# Validate Before Commit

## Purpose

Before committing changes, verify that modified things maintain structural and referential integrity. Catch errors before they become part of the committed state. This prompt implements a focused subset of `validate.thing.md` optimized for the pre-commit moment.

## Reasoning Template

For each staged thing file, run these checks in order:

### 1. Structural Validation

Verify the thing is well-formed:

- [ ] YAML frontmatter present and parseable
- [ ] Required fields exist: `id`, `type`, `status`, `created`
- [ ] `id` is lowercase, hyphenated, no spaces
- [ ] `status` is a valid value for the domain
- [ ] `created` is valid ISO 8601 date
- [ ] Markdown body exists below frontmatter

**On failure:** Auto-fix if possible (e.g., add missing `created` from git history). If not fixable, block commit and report.

### 2. Referential Validation

Verify that references point to real things:

- [ ] All IDs in `dependencies` array exist in the domain
- [ ] All IDs in `blocks` array exist in the domain
- [ ] All IDs in `linked_things[].id` exist in the domain
- [ ] `parent` ID exists if specified
- [ ] All IDs in `triggers[].watch` arrays exist

**On failure:** Report broken references. Do not auto-fix — the user may have forgotten to create the referenced thing.

### 3. Semantic Validation

Verify that the thing makes logical sense:

- [ ] Status `completed` things don't have unsatisfied dependencies on non-completed things (circular)
- [ ] Status `blocked` things have at least one non-completed dependency or a documented reason
- [ ] Priority is consistent with stated urgency in narrative (flag mismatches, don't auto-correct)
- [ ] No duplicate IDs across the staged set

**On failure:** Warn but don't block unless it's a duplicate ID (which always blocks).

### 4. Consistency Validation

If multiple things are staged together, verify cross-thing consistency:

- [ ] If thing A says it blocks thing B, thing B should acknowledge the dependency (warn if not)
- [ ] If a parent thing is staged, verify its subtask references match actual subtask things
- [ ] Status transitions make sense (e.g., not jumping from `not-started` to `completed` without passing through `in-progress` — warn, don't block)

## Decision Rules

| Severity | Action |
|----------|--------|
| Auto-fixable structural issue | Fix silently, note in commit |
| Broken reference | Block commit, report to user |
| Semantic warning | Warn but allow commit |
| Duplicate ID | Block commit |
| Cross-thing inconsistency | Warn but allow commit |

## Output Format

```
Pre-commit validation:
- Checked: [count] things
- Auto-fixed: [list of fixes applied]
- Warnings: [list of non-blocking issues]
- Blocked: [list of blocking issues, if any]
- Result: PASS | FAIL
```

If FAIL, the agent reports the blocking issues and asks the user how to proceed before committing.
