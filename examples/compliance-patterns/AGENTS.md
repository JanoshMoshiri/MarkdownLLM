---
name: Compliance Patterns Library
description: Reference patterns for encoding compliance as verifiable reasoning using multi-lens frameworks
version: 3.0
applies_to: "**/*.md"
framework_root: ../..
framework_version_seen: 3.27.0
---

# Compliance Patterns Library Agent

## What This System Does

This is a reference library for domain builders creating systems that operate under regulatory constraints (GDPR, HIPAA, financial regulations, etc.). It demonstrates how to encode compliance as verifiable reasoning patterns and examples, rather than as abstract rules.

## Framework Principles Applied to Compliance

1. **Verifiable Reasoning** — Compliance tasks have clear right/wrong answers; use examples to make reasoning verifiable
2. **Multi-Lens Decision Making** — Every decision should be reasoned through domain logic, compliance logic, and audit logic
3. **Contrast Creates Clarity** — Show both compliant patterns AND violations (with consequences) so the LLM can learn the boundary
4. **Atomic Patterns** — Each example is self-contained; they compose into a searchable pattern library
5. **Git as Audit Trail** — All changes and decisions are versioned; compliance documentation is built-in
6. **Self-Describing** — Patterns are things with full frontmatter; the library validates itself

## What This IS and IS NOT

**This is:**
- A reference library for studying compliance patterns
- Examples you can adapt for your own regulated domain
- A demonstration of how to encode multi-lens reasoning
- A starting point that you'll extend with domain-specific examples

**This is NOT:**
- Legal or regulatory advice
- A complete compliance solution (compliance is domain-specific)
- A substitute for actual legal/compliance expertise
- Production code (it's documentation and examples)

## How This Agent Works

### On Startup
1. Version check (`session-start:version-check` hard hook): compare `{framework_root}/.markdownllm` version against `framework_version_seen` above
2. Load `{framework_root}/kernel.md` — the framework's operative rules; load a full spec only when the kernel doesn't settle an ambiguity
3. Read the orient view — `python {framework_root}/tools/mdllm.py session-start .` emits the open loops (non-terminal work things + open conflicts) carried from prior sessions; forward state is the thing graph, not a hand-kept brief
4. Load skills relevant to session intent: compliance-patterns-specification.skill.md, compliance-patterns-read.thing.skill.md, compliance-patterns-write.thing.skill.md, compliance-patterns-workflow.skill.md
5. Evaluate triggers — check for patterns referencing outdated regulations or unlinked anti-patterns

### On User Request
1. **Clarify intent** — Are they studying patterns, creating their own domain, or auditing compliance?
2. **Load relevant skill** — Match intent to appropriate skill
3. **Load relevant examples** — Read pattern things from `./things/`
4. **Reason about patterns** — Show how positive examples, anti-patterns, and reasoning lenses work
5. **Generate guidance** — Help them apply patterns to their context

### On Output
- Validate new patterns semantically (all three lenses present? remediation linked? verifiable?) — the mechanical layer (structure, references, `_schema.yaml` vocabularies) is owned by `mdllm validate` and the pre-commit hook
- Commit with structured message (e.g., `create: pattern-new-id`, `update: example-id`)
- Reference specific examples and reasoning lenses
- Explain the multi-lens approach
- Show how to extend patterns for their domain

## Skills Directory

All reusable capabilities for compliance pattern documentation:

- **compliance-patterns-specification.skill.md** — Philosophy and approach to encoding compliance
- **compliance-patterns-read.thing.skill.md** — How to read and learn from compliance examples
- **compliance-patterns-write.thing.skill.md** — How to create and document new patterns
- **compliance-patterns-workflow.skill.md** — How domain builders integrate these patterns

## Foundational Specifications

Resolved from the MarkdownLLM framework root via `framework_root` (the kernel covers their operative rules; load a full spec on demand):

- **thing.md** — The atomic unit specification (structure for all things)
- **validate.thing.md** — The validation contract (mechanical layer: `mdllm`; semantic layer: the agent)
- **git-workflow.md** — When and how to commit (git as state machine)
- **interface.md** — I/O layer (input routes and output types)

## Things Directory

Example patterns of compliance: `./things/`

Thing types:
- `type: pattern` — A verifiable compliance pattern
- `type: anti-pattern` — A violation with explanations
- `type: example` — A concrete scenario showing multi-lens reasoning
- `type: decision-tree` — A framework for making verified decisions

## Triggers

### Dependency
- **Orphaned anti-pattern** — When a `type: anti-pattern` has no `linked_things` entry with relation `remediated-by`, flag it for linking
- **Incomplete example** — When a `type: example` doesn't show all three lenses (domain, compliance, audit), flag it

### Relationship
- **Pattern update cascade** — When a `type: pattern` is updated, check all `type: anti-pattern` things that reference it for consistency

## Key Concept: Multi-Lens Reasoning

Every compliance decision can be evaluated through three lenses:

**Lens 1: Domain Logic** — What does this accomplish in the domain's terms?
**Lens 2: Compliance Logic** — Does this respect regulatory constraints?
**Lens 3: Audit Logic** — Can we trace and explain this decision?

All three lenses must align before proceeding. If they conflict, the conflict becomes explicit for human resolution.

## Usage Pattern

```
Domain Builder or Auditor
    ↓ (auto-discovered)
Load Compliance Patterns Agent
    ↓
Evaluate triggers (orphaned patterns, incomplete examples)
    ↓
Load relevant skills (read, write, or workflow)
    ↓
Load relevant pattern things from ./things/
    ↓
Reason about patterns and apply to domain
    ↓
Validate new/modified patterns
    ↓
Commit with structured message
    ↓
Document new patterns or reference existing ones
```

## Validation Checklist (Authoring)

Mechanical validation (structure, references, declared vocabularies) is owned
by `mdllm validate` and enforced by the pre-commit hook — never re-perform it
by reasoning. Before committing a new or changed pattern, verify what the tool
cannot:

- [ ] Pattern has all three lenses documented (domain, compliance, audit)
- [ ] Anti-patterns link to their remediation pattern (`remediated-by`)
- [ ] Examples show concrete scenarios (not abstract rules)
- [ ] Example is verifiable (yes/no, true/false, not subjective)
- [ ] Commit message follows `action: description` convention

## Adoption Checklist (Using a Pattern in Your Domain)

- [ ] Pattern clearly shows compliant behavior
- [ ] Anti-pattern clearly shows violation + consequence
- [ ] Multi-lens reasoning is explicit (domain/compliance/audit)
- [ ] Applicable to your domain context — adapt fields to your regulatory regime
