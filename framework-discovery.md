---
id: framework-discovery-specification
type: specification
status: stable
version: 2.0
created: 2026-05-19
linked_things:
  - id: domain-specification-guide
    relation: extends
  - id: thing-specification
    relation: references
  - id: git-workflow-specification
    relation: references
  - id: domain-refresh-specification
    relation: complements
---

# Framework Discovery

## What This Specifies

This document defines how domain agents discover the MarkdownLLM framework root and load the framework's operative rules. Without this mechanism, a domain agent operating inside a nested directory has no way to locate the shared kernel and specifications (kernel.md, thing.md, git-workflow.md, validate.thing.md) that all domains depend on.

## The Problem

A domain lives at a path like `domains/my-domain/` within a MarkdownLLM repository. When the LLM tool discovers and loads that domain's `AGENTS.md`, it has no inherent knowledge of the repository structure above it. The domain agent says "Load thing.md" but doesn't know *where* thing.md lives.

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

| Resource | Resolved Path |
|---------------|---------------|
| kernel.md (Tier 0 — the generated operative kernel) | `{framework_root}/kernel.md` |
| thing.md | `{framework_root}/thing.md` |
| validate.thing.md | `{framework_root}/validate.thing.md` |
| git-workflow.md | `{framework_root}/git-workflow.md` |
| interface.md | `{framework_root}/interface.md` |
| read.thing.md | `{framework_root}/read.thing.md` |
| write.thing.md | `{framework_root}/write.thing.md` |
| the mdllm CLI (validation, hooks, triggers, provenance) | `{framework_root}/tools/mdllm.py` |

### Example

A domain at `domains/my-domain/`:

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
3. Verify framework root exists (check for the `.markdownllm` sentinel)
4. Version check (`session-start:version-check` hard hook): compare the sentinel's `version` against `framework_version_seen` in the domain frontmatter
5. Load `{framework_root}/kernel.md` — the generated operative kernel. Do **not** eagerly load the full foundational specs; load a full spec only when the kernel doesn't settle an ambiguity (see the tier tables in AGENTS.md and `templates/AGENTS.md.template`)
6. Load domain skills from `./skills/` relevant to session intent
7. Read the orient view (`mdllm session-start` emits the open loops), then domain things from `./things/` as the session requires
8. Evaluate triggers

If `framework_root` is missing from frontmatter, the agent should:
1. Look for a `.markdownllm` marker file by walking up the directory tree
2. If found, use that directory as the framework root
3. If not found, warn the user that foundational specs cannot be located

## The `.markdownllm` Sentinel File

The framework root directory contains a `.markdownllm` file. This file serves two roles:

1. **Discovery** — If `framework_root` is not declared in a domain's frontmatter, the agent walks up the directory tree looking for this file. Finding it means you've found the framework root.
2. **Canonical version source** — The `version` field in this file is the authoritative framework version. Domain agents read only this field at session start (via the `session-start:version-check` hard hook in orchestration.md) to detect whether their `framework_version_seen` is stale. Reading a tiny sentinel file instead of CHANGELOG.md keeps Tier 0 context cost negligible.

```yaml
framework: MarkdownLLM
version: 3.4.0
role: canonical-version-sentinel
foundational_specs:
  - thing.md
  - read.thing.md
  - write.thing.md
  - validate.thing.md
  - interface.md
  - git-workflow.md
  # ...the full list lives in the real sentinel; this example is illustrative
domains:
  - domains/  # the documented convention for nested domain repos
  - domain/   # legacy spelling; also excluded by tool and gitignore
```

The example above is abbreviated — the live `.markdownllm` at the framework root is the authoritative copy, including the complete `foundational_specs` list. Don't hand-maintain copies of it elsewhere.

**Important:** `version` in `.markdownllm` is the single source of truth for the framework version. The `version` field in the framework's `AGENTS.md` frontmatter is descriptive metadata. When they diverge, `.markdownllm` is authoritative. Keep them in sync on every version bump by convention.

## Deployment Architecture

The framework supports two deployment modes.

### Nested Repository Model (Recommended)

The standard deployment uses a nested git repository architecture: domains live inside the framework directory but maintain independent git histories.

```
MarkdownLLM/                    ← Framework git repo
├── .gitignore                  ← Contains: domains/
├── thing.md
├── git-workflow.md
├── ...foundational specs...
├── templates/
├── examples/
└── domains/
    ├── DomainA/                ← Independent git repo
    │   ├── AGENTS.md
    │   ├── skills/
    │   └── things/
    └── DomainB/                ← Independent git repo
        ├── AGENTS.md
        ├── skills/
        └── things/
```

**Key properties:**

| Property | Mechanism | Purpose |
|----------|-----------|--------|
| **Isolation** | Framework `.gitignore` excludes `domains/` | Domain commits never appear in framework history |
| **Independence** | Each domain has its own `.git` | Domains version independently with their own branches, tags, remotes |
| **Shared foundation** | `framework_root` in domain AGENTS.md | Domains resolve framework specs via relative path |
| **Read-only relationship** | Domains read framework specs; never write to them | Framework evolves independently of domains |

**Why this architecture:**
1. **Clean separation of concerns** — Framework evolution and domain evolution are decoupled
2. **Independent deployment** — Domains can be extracted to standalone repos at any time
3. **No submodule complexity** — Avoids git submodule pain while achieving the same isolation
4. **Multiple domains, one framework** — Many domains share a single framework installation without conflicts

**The `.gitignore` contract:** The framework's `.gitignore` MUST contain `domains/` (the documented convention). The legacy spelling `domain/` is also excluded by the framework's gitignore and by `mdllm`'s default excludes, for installs that predate the convention. Without the exclusion, domain files appear as untracked files in the framework repo.

### Standalone Domain Deployment

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
| What's the sentinel file? | `.markdownllm` — discovery marker and canonical version source |
| What must be loadable? | kernel.md at Tier 0; the full specs (thing.md, validate.thing.md, git-workflow.md, interface.md, …) on demand |
