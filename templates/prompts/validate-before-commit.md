---
id: validate-before-commit
type: prompt
status: stable
version: 2.0
created: 2026-05-20
inputs:
  - name: staged-things
    description: "Thing files that have been modified and are about to be committed"
outputs:
  - name: validation-result
    description: "pass or pass-with-warnings, with specific semantic issues"
bound_to:
  - hook: pre-commit
linked_things:
  - id: orchestration-specification
    relation: implements
  - id: validate-thing-specification
    relation: implements
  - id: git-workflow-specification
    relation: complements
---

# Validate Before Commit

## Purpose

Before committing changes, verify that modified things make semantic sense. This prompt implements the *judgement* subset of `validate.thing.md` optimized for the pre-commit moment.

**Since v3.0, structural and referential validation are not this prompt's job.** The mdllm pre-commit hook (`python {framework_root}/tools/mdllm.py install-hook .`) runs full mechanical validation — YAML well-formedness, required fields, id format, status vocabulary against the schema, reference integrity — deterministically, and blocks the commit on any Error. Never re-perform those checks by reasoning. If the hook is not installed (or cannot run in this environment), say so explicitly and run `mdllm validate .` manually before committing — do not substitute reasoning for the tool.

## Reasoning Template

For each staged thing file, run these checks in order:

### 1. Semantic Validation

Verify that the thing makes logical sense:

- [ ] Status `completed` things don't have unsatisfied dependencies on non-completed things (circular)
- [ ] Status `blocked` things have at least one non-completed dependency or a documented reason
- [ ] Priority is consistent with stated urgency in narrative (flag mismatches, don't auto-correct)

**On failure:** Warn but don't block; surface to the user.

### 2. Consistency Validation

If multiple things are staged together, verify cross-thing consistency:

- [ ] If thing A says it blocks thing B, thing B should acknowledge the dependency (warn if not)
- [ ] If a parent thing is staged, verify its subtask references match actual subtask things
- [ ] Status transitions make sense (e.g., not jumping from `not-started` to `completed` without passing through `in-progress` — warn, don't block)

## Decision Rules

| Severity | Action |
|----------|--------|
| Mechanical issue (structure, references, schema) | The hook blocks the commit; fix the thing (or, with the human, the schema) — never reason around it |
| Semantic warning | Warn but allow commit |
| Cross-thing inconsistency | Warn but allow commit |

## Output Format

```
Pre-commit semantic review:
- Checked: [count] things
- Warnings: [list of non-blocking issues]
- Result: PASS | PASS WITH WARNINGS
```

Mechanical failures surface as hook output at the commit boundary, not in this report.
