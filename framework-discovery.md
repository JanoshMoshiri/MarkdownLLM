---
id: framework-discovery-specification
type: specification
status: draft
version: 1.0
created: 2026-05-19
linked_things:
  - id: domain-specification-guide
    relation: extends
  - id: thing-specification
    relation: references
  - id: git-workflow-specification
    relation: references
---

# Framework Discovery

## What This Specifies

This document defines how domain agents discover the MarkdownLLM framework root and load foundational specifications. Without this mechanism, a domain agent operating inside a nested directory has no way to locate the shared specifications (thing.md, git-workflow.md, validate.thing.md, interface.md) that all domains depend on.

## The Problem

A domain lives at a path like `domains/ProducFlow2/` within a MarkdownLLM repository. When the LLM tool discovers and loads that domain's `AGENTS.md`, it has no inherent knowledge of the repository structure above it. The domain agent says "Load thing.md" but doesn't know *where* thing.md lives.

This creates a failure mode: the domain agent loads, reads its skills, reads its things — but cannot access the foundational framework specifications it needs to reason correctly.

## The Solution: `framework_root` in Frontmatter

Every domain `AGENTS.md` declares a `framework_root` field in its YAML frontmatter. This field contains the **relative path from the domain root to the MarkdownLLM framework root**.

### Format

```yaml
---
name: My Domain
description: What this domain does
version: 1.0
applies_to: "**/*.md"
framework_root: ../..
---
```

The `framework_root` value is a relative path using POSIX separators (`/`). It points to the directory containing the framework's foundational specifications (thing.md, git-workflow.md, etc.).

### What This Enables

With `framework_root` declared, the domain agent can resolve paths to:

| Specification | Resolved Path |
|---------------|---------------|
| thing.md | `{framework_root}/thing.md` |
| validate.thing.md | `{framework_root}/validate.thing.md` |
| git-workflow.md | `{framework_root}/git-workflow.md` |
| interface.md | `{framework_root}/interface.md` |
| read.thing.md | `{framework_root}/read.thing.md` |
| write.thing.md | `{framework_root}/write.thing.md` |

### Example

A domain at `domains/ProducFlow2/`:

```yaml
framework_root: ../..
```

Resolves `thing.md` to `../../thing.md` → the framework root's `thing.md`.

A domain deployed as a standalone repository:

```yaml
framework_root: .
```

In this case, the framework specs are co-located (copied or submoduled into the domain root).

## Agent Startup Behaviour

When a domain agent loads, its startup sequence becomes:

1. Read own `AGENTS.md` frontmatter
2. Resolve `framework_root` to an absolute path
3. Verify framework root exists (check for `thing.md` as sentinel)
4. Load foundational specifications from framework root:
   - `{framework_root}/thing.md`
   - `{framework_root}/validate.thing.md`
   - `{framework_root}/git-workflow.md`
   - `{framework_root}/interface.md`
5. Load domain skills from `./skills/`
6. Load domain things from `./things/`
7. Evaluate triggers

If `framework_root` is missing from frontmatter, the agent should:
1. Look for a `.markdownllm` marker file by walking up the directory tree
2. If found, use that directory as the framework root
3. If not found, warn the user that foundational specs cannot be located

## The `.markdownllm` Marker File

As a fallback discovery mechanism, the framework root directory contains a `.markdownllm` file. This is a simple YAML file that identifies the directory as a MarkdownLLM framework root:

```yaml
framework: MarkdownLLM
version: 2.1
foundational_specs:
  - thing.md
  - validate.thing.md
  - git-workflow.md
  - interface.md
  - read.thing.md
  - write.thing.md
```

This serves two purposes:

1. **Fallback discovery** — If `framework_root` is not declared in a domain's frontmatter, the agent can walk up directories looking for this marker
2. **Self-documentation** — Tells any agent (or human) what this repository is and what foundational specs are available

## Standalone Domain Deployment

When a domain is deployed as its own repository (not nested inside the framework repo), there are two options:

### Option A: Copy Foundational Specs

Copy the needed framework specs into the domain root. Set `framework_root: .`

Pros: Self-contained, no external dependencies
Cons: Specs may become stale if framework evolves

### Option B: Git Submodule

Include the framework as a git submodule:

```
my-domain/
├── AGENTS.md (framework_root: ./framework)
├── framework/ (git submodule → MarkdownLLM repo)
├── skills/
└── things/
```

Pros: Always current, explicit version tracking
Cons: Requires submodule management

### Option C: Minimal Spec Bundle

Copy only `thing.md` and reference the framework repo for the rest. Acceptable for domains that only need the atomic unit definition.

## Validation

When validating a domain (using validate.thing.md), check:

- [ ] `framework_root` is present in domain AGENTS.md frontmatter
- [ ] The resolved path exists and contains `thing.md`
- [ ] OR a `.markdownllm` marker exists in an ancestor directory

## Summary

| Concern | Answer |
|---------|--------|
| How does a domain find framework specs? | `framework_root` relative path in AGENTS.md frontmatter |
| What's the fallback? | Walk up directories looking for `.markdownllm` marker |
| What if deployed standalone? | Copy specs, use submodule, or minimal bundle |
| What's the sentinel file? | `thing.md` — if it exists at the resolved path, the framework root is valid |
| What specs must be loadable? | thing.md, validate.thing.md, git-workflow.md, interface.md |
