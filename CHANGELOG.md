# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

**Domain Refresh Specification (domain-refresh.md):**
- Defines the nested git repository deployment architecture (framework repo + isolated domain repos, .gitignore contract)
- Specifies the refresh process: how domain agents check CHANGELOG, WORKLOG, and foundational specs for framework evolution
- Refresh algorithm with version tracking via `framework_version_seen` frontmatter field
- Integration points for domain workflow skills and AGENTS.md startup sequences
- Anti-patterns and concrete example (domain discovering autocommit capability)

### Planned
- Migration strategy for evolving thing schemas
- Concurrency and multi-agent patterns
- Limitations and failure-mode documentation

## [2.2.0] - 2026-05-19

### Triggers, Validation, Commit Conventions, and Skill File Standardization

This release adds trigger support, validation patterns, structured git conventions, and standardized skill file format to the existing architecture.

### Added

**Triggers System Implementation:**
- Integrated trigger documentation throughout domain specifications
- Session-start triggers: time-based (due dates, stale items), dependency-based (unblocked work), threshold-based (overload warnings)
- Post-write triggers: validate state changes, cascade effects, notify dependents
- Trigger examples in both example domains (Life Manager, Compliance Patterns)
- Trigger integration with git commit history for temporal reasoning

**Validation Framework:**
- Four-level validation strategy in domain-specification-guide.md: structural, referential, domain-specific, semantic
- Three severity tiers: error, warning, info
- Post-write validation checkpoints and procedures
- Validation checklists in example AGENTS.md files
- Validation sections in all templates and example skill files

**Git Commit Conventions:**
- Structured commit message format: `action: description` (e.g., `create: task-id`, `update: project status`)
- Commit points in workflows: create, status-change, batch operations, phase transitions, archive
- Git log as event stream for trigger evaluation
- Examples of commit conventions in all skill files and workflow documentation

**Skill File Standardization:**
- All skill files now have complete YAML frontmatter: `id`, `type`, `status`, `version`, `created`, `linked_things`
- Updated skill file frontmatter in both example domains (Life Manager, Compliance Patterns)
- Status field shows skill maturity: `draft`, `evolving`, `stable`
- Relationship metadata showing which skills implement/orchestrate/complement each other
- Consistent versioning across all skills

### Changed

**Examples Updated to v2.0:**
- Life Manager AGENTS.md → v2.0 with trigger integration, validation checkpoints, commit conventions
- Compliance Patterns AGENTS.md → v2.0 with dependency triggers, post-write validation, audit trail integration
- All example skill files enhanced with: proper frontmatter, trigger sections, validation rules, commit conventions

**Domain-Specification-Guide Enhanced:**
- Updated to v2.1 with comprehensive trigger documentation
- Added git-workflow and interface-specification as linked references
- Expanded skill file templates with trigger sections, validation checkpoints, commit conventions
- Clarified thing status values: `not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled`
- Added domain-specific validation rules patterns
- Enhanced AGENTS.md template with trigger evaluation flow

**Templates Updated for Standardized Skill Format:**
- AGENTS.md.template — Added trigger section, validation checklist, git commit conventions
- domain-specification.skill.md.template — Added id, status, linked_things frontmatter; added validation rules and triggers sections
- domain-read.thing.skill.md.template — Added skill file frontmatter structure; added trigger checking; enhanced context loading strategy
- domain-write.thing.skill.md.template — Added validation checklist and procedures; added post-write trigger evaluation; structured commit conventions
- domain-workflow.skill.md.template — Added trigger integration, git commit points, validation checkpoints

**Manifesto Updated:**
- Clarified vendor agnostic principle: use AGENTS.md, .skill.md, and YAML frontmatter (not .instructions.md, .prompt.md conventions)

### Refined

- Example compliance patterns enhanced with bidirectional linking (positive patterns ↔ anti-patterns)
- Life Manager thing types standardized with clear status transitions and domain validation rules
- Trigger examples across domains show concrete, actionable conditions (overdue, unblocked, threshold)
- Post-write validation examples demonstrate three-level checks (structural, referential, domain-specific)

## [2.1.0] - 2026-05-19

### Interface, Git Workflow, Validation, Triggers, Self-Describing Architecture

This release adds operational specifications that were previously gaps and makes the framework self-describing (fractal). New specs carry `status: draft` and will mature through use.

### Added

**New Specifications:**
- **interface.md** — The I/O layer specification. Documents input routes (VS Code, CLI, mobile, voice), the thin-interface principle (use existing routes, don't build new ones), and the things vs deliverables distinction (things are persistent state; deliverables are produced artefacts like documents, code, images, video, audio).
- **git-workflow.md** — Git as state machine specification. Defines commit points (after creation, status transition, write session, session end), structured commit message conventions (action: description), who commits (agent locally, human pushes), git log as event stream for triggers, and three-layer auditability (worklog → git log → git diff).
- **validate.thing.skill.md** — Universal validation skill. Four-level validation: structural (valid YAML, required fields), referential (link integrity, bidirectional consistency), domain-specific (rules from specification skill), semantic (LLM-reasoned coherence checks). Three severity tiers: error, warning, info.

**Triggers System (in thing.md):**
- Declarative trigger conditions as YAML metadata on things
- Four trigger types: time-based (due_date_passed, stale), dependency-based (watch IDs for status changes), threshold-based (subtasks_complete, blocked_duration), relationship-based (watch connected things)
- Declarative actions: surface, re_evaluate, suggest_completion, unblock, escalate, cascade, notify
- Three evaluation moments: session start, after writes, scheduled invocation
- Idempotent evaluation — no extra state needed; git history provides temporal context

**Self-Describing Architecture:**
- All foundational specs now have YAML frontmatter (id, type, status, version, created, linked_things)
- Root AGENTS.md created — the framework orchestrates itself as a domain
- Framework specs are things within the framework they define (fractal/self-describing property)
- Spec types: `manifesto`, `specification`, `skill`, `guide`
- Spec statuses: `draft`, `evolving`, `stable`, `deprecated`

**WORKLOG.md:**
- Session-based work log adopted for this repository
- Captures completed work, decisions made, reflections, and forward planning
- Complements CHANGELOG (what shipped) with WORKLOG (how it evolved session by session)

### Changed

**Manifesto (llm-driven-systems.manifesto.md):**
- Added "Origins and Influences" section — credits Clean Architecture (Robert C. Martin) and SOLID principles; establishes "build on what exists" philosophy (AGENTS.md, .skill.md, YAML, markdown, git are all existing conventions)
- Added Principle 8: "Self-Describing (Fractal)" — the system describes itself within itself; same pattern at every scale
- Expanded Principle 6: "Version-Controlled Everything" — git as state machine, commit discipline, event stream, three audit layers
- Updated "How It Works In Practice" — references AGENTS.md, triggers, deliverables, commit conventions
- Updated "Getting Started" — reflects current workflow (AGENTS.md first, commit meaningfully, WORKLOG)
- Expanded "Auditing" in "What This Enables" — three-layer auditability model

**Domain Specification Guide (domain-specification-guide.md):**
- Added "The Self-Describing Principle" section — domain specs can themselves be things
- Updated checklist — includes validation, commit conventions, triggers
- Expanded Key Takeaways from 7 to 10 points (git as state machine, interface routes, validation, self-describing)

**CONTRIBUTING.md:**
- Restructured to reflect current framework structure
- Added "Everything is a thing" guideline (all files should have frontmatter)
- Added git-workflow.md conventions for contributors
- Added validation requirement before submitting
- Listed full framework file structure with roles

**Core Spec Fixes:**
- Fixed `read.thing.md` and `write.thing.md` — updated old `[domain].instructions.md` references to `[domain]-specification.skill.md`
- Fixed `README.md` — updated 3 references from `Instructions-guide.md` to `domain-specification-guide.md`

### Why This Matters

The three decoupled layers (Interface, Processing, Storage) each now have explicit specifications, though several carry `status: draft` and are expected to evolve through real-world use. Things can be reactive (triggers). Integrity is verifiable (validation). Git usage is disciplined (workflow). The system describes itself within itself.

The framework composes existing proven tools (AGENTS.md, .skill.md, YAML, markdown, git, LLMs) into a new architectural pattern — it invents no new infrastructure, protocols, or interfaces.
- Integration guides for popular LLMs and platforms

## [2.0.0] - 2026-05-19

### Major Refactoring: Three-Layer Simplification

This release represents a significant architectural refinement, moving from a five-component approach to a three-layer model that follows similar patterns to production LLM agent systems.

### Changed (Breaking)

**Framework Architecture Simplified:**
- Renamed: `[domain]-instructions.skill.md` → `[domain]-specification.skill.md`
  - Clarifies that this is domain philosophy/principles, not instructions to follow
  - Better aligns with industry terminology (AGENTS.md + SKILL.md standards)
  
- Key distinction established: `thing.md` is foundational **specification**, not a skill
  - `thing.md` — Universal atomic unit specification (not a `.skill.md` file)
  - Skills (`.skill.md` files) — Reusable capabilities (specification, read, write, workflow)
  - Previous confusion between "skill files" and "spec files" eliminated

**Updated All References Throughout:**
- Templates: All four domain templates use `specification` and correct file extensions
- Examples: Both `life-manager/` and `compliance-patterns/` restructured with new naming
- Documentation: README, domain-specification-guide, CONTRIBUTING all updated
- Core docs: All skill files now reference `thing.md` (not `thing.skill.md`)

### Architecture Now Fully Cohesive

**Three Clear Layers:**
```
Layer 1: AGENTS.md
  ↓ auto-discovers at root
Layer 2: SKILLS/ 
  (specification, read.thing, write.thing, workflow .skill.md files)
  ↓ reusable capabilities
Layer 3: THING.MD (foundational specification) → THINGS/ (instances)
```

**Vendor-Agnostic Discovery:**
- `AGENTS.md` sits at repository root and is auto-discovered by:
  - OpenAI Codex, GitHub Copilot, Cursor, Windsurf, Gemini CLI (natively)
  - Claude Code (via CLAUDE.md wrapper referencing AGENTS.md)
- Skills are portable across all vendors (standard YAML frontmatter + markdown)
- Domain repos can be deployed independently with their own AGENTS.md

### Documentation Improvements

- **README.md** — Restructured to match three-layer model; removed dated references to "five-component pattern"
- **domain-specification-guide.md** — Renamed from "instructions-guide"; updated all structural diagrams
- **CONTRIBUTING.md** — Updated contribution guidelines to reflect three-layer pattern
- **Template files** — All template filenames and content use consistent naming
- **Example domains** — Both examples now show clean structure with specification.skill.md, not instructions.skill.md

### Why This Matters

The previous framework conflated several concepts (instructions, skills, specs, prompts) in ways that didn't match how actual agent systems work. This version:

- **Follows emerging patterns** — Uses the AGENTS.md + SKILL.md structure adopted by several LLM agent frameworks
- **Eliminates confusion** — Clear distinction between discovery (AGENTS.md), capabilities (skills), definition (thing.md), and instances (things)
- **Improves scalability** — Each domain is fully deployable independently, with clear entry point (AGENTS.md)
- **Enables multi-vendor usage** — Agent files auto-discover across different LLM tools
- **Simplifies onboarding** — New users understand: "Agent loads first, then skills, then things"

### Technical Accuracy

- **Vendor maturity confirmed** — AGENTS.md is now stewarded by the Agentic AI Foundation (under Linux Foundation) with broad cross-tool support
- **Discovery mechanism validated** — Verified Codex walk-from-root-to-cwd behavior and auto-discovery across tools
- **Framework positioning correct** — MarkdownLLM is the library/template specification; domains are deployed separately with their own root AGENTS.md

## [1.4.0] - 2026-05-18

### Added
- **Five-Component Domain Pattern** — Complete framework documentation for building applications
  - Explicit requirements: Instructions, Application, Workflow(s), and Read/Write Prompts
  - Each component has a clear purpose, structure, and interaction pattern
  - Minimal and complex domain patterns documented
- **Application File Specification** — New `[domain].application.md` as atomic thing that answers "what problem does this solve?"
  - Application thing type with standard metadata
  - Explicit problem definition and delivery specification
  - Links to supporting workflows and resources
- **Comprehensive Getting Started Guide** — Expanded `instructions-guide.md` with:
  - Complete five-component workflow for building domains
  - Visual diagram showing component relationships and data flow
  - Detailed sections on each component's purpose and structure
  - Patterns for minimal vs. complex domains
- **Updated README** — Restructured to emphasize the five-component pattern
  - Expanded application examples with structured descriptions
  - Step-by-step guide from understanding principles to implementation
  - Clarified distinction between domain definitions and application instances
- **Prototype-to-Production Reference Domain** — Replaced life-manager as primary example domain
  - Demonstrates the complete five-component pattern
  - Shows how complex workflows are orchestrated

### Changed
- README.md now guides users through the five-component pattern explicitly
- Getting Started section provides concrete steps for each component
- Example domains restructured as Example Applications with consistent documentation
- Clarified terminology: "domain applications" vs. "instances of things"

## [1.3.0] - 2026-05-18

### Added
- **Multi-Lens Reasoning** — Framework support for multi-perspective decision-making
  - Domain Logic Lens: What does this domain require?
  - Compliance Logic Lens: What regulatory/architectural constraints apply?
  - Audit Logic Lens: Can we defend and explain this decision?
  - Lens conflict detection and resolution guidance
  - Auto-generated audit trails encoding reasoning process
- **Example Type System** — New `type: example` for pattern libraries and anti-patterns
  - Teaches LLMs through demonstration (inductive learning)
  - Supports positive patterns and anti-patterns with violations explained
  - Pattern types: `positive-pattern`, `anti-pattern`, and domain-specific variants
  - Examples function as living documentation and behavioral reinforcement
- **domains/compliance-patterns/** — Reference domain for regulated systems
  - Compliance-patterns.instructions.md: Philosophy and usage guidance
  - example-gdpr-compliant-data-handling.md: Concrete GDPR compliance example showing all three lenses aligned
  - example-gdpr-violation-anti-patterns.md: Anti-pattern example showing violations and how to fix them
  - Serves as reference library for law, finance, healthcare domains

### Enhanced
- **thing.skill.md** — Added "Special Type: Example" section explaining:
  - How examples work as inductive learning for LLMs
  - Creating pattern libraries for domain-specific behaviors
  - Using positive + negative examples to teach good practices
- **read.prompt.md** — Added "Multi-Lens Reasoning (Optional)" section with:
  - How to apply multiple lenses to analytical questions
  - Handling lens conflicts (compliance vs. domain efficiency)
  - Learning from examples in the repository
  - Examples of read-mode queries showing multi-lens analysis
- **write.prompt.md** — Added "Multi-Lens Reasoning for Changes (Optional)" section with:
  - Pre-change validation through all lenses
  - Detecting compliance risks before changes propagate
  - Using examples to validate pattern alignment
  - Handling conflicts: when compliance overrides domain preferences
- **instructions-guide.md** — Added "Defining Domain-Specific Reasoning Patterns" section covering:
  - Creating domain-specific lenses
  - Building reasoning patterns for your domain
  - Reinforcing lenses through examples
  - When to use multi-lens vs. simple reasoning

### Framework Improvements
- Enables "compliance-by-design"—regulatory requirements encoded as reasoning lenses, not bolt-on checks
- Scales reasoning complexity with domain complexity (optional lenses, discovered when needed)
- Supports regulated domains (law, finance, healthcare) requiring audit trails and decision justification
- Example-driven learning complements rule-based constraints for more natural LLM behavior
- Aligns with neural network principles: multiple reasoning pathways, conflict resolution, inductive vs. deductive reasoning

### Why This Matters
Real-world systems operate under constraints (GDPR, HIPAA, audit requirements). Previous framework versions could encode domain logic but struggled with compliance thinking. Multi-lens reasoning makes constraints first-class citizens in the reasoning process. Examples teach patterns inductively—how LLMs naturally learn—rather than forcing rule-based compliance. This enables productive LLM systems in heavily regulated environments where every decision must be explainable and defensible.

## [1.2.0] - 2026-05-17

### Added
- **Tiered Context Windows** — Multi-level loading strategy for scalability
  - Level 1: Metadata only (for broad questions and landscape scanning)
  - Level 2: Metadata + relationships (for dependency traversal and critical path analysis)
  - Level 3: Full context (for deep work and detailed reasoning)
- **scalability-guide.md** — Comprehensive guide covering:
  - Philosophy of multi-level abstraction inspired by neural networks
  - Three scaling approaches: Contextual Loading (now), Incremental Summarization (medium-scale), Full Tiered System (long-term)
  - Feel-based signals for when to scale
  - Progressive adoption pattern

### Enhanced
- **thing.skill.md** — Added "Multi-Level Context Windows" section explaining how the same thing file works at different levels of granularity
- **read.prompt.md** — Added "Loading Strategy" section with guidance on choosing context levels and tab-based examples for each level
- **write.prompt.md** — Added "Loading Strategy" section adapted for write operations, emphasizing cascading effects and dependency updates

### Framework Improvements
- Implemented adaptive context loading (LLM determines relevance dynamically, not pre-labeled)
- Aligned scalability approach with neural network principles: multiple abstraction levels, dynamic attention, holistic reasoning
- Enables scaling from 10s to 1000s of things while maintaining framework elegance
- Progressive adoption: users discover tiering naturally when they need it (no forced optimization)

### Why This Matters
The framework now scales efficiently without requiring indexed search or special query languages. By leveraging the LLM's native pattern-matching ability at appropriate levels of abstraction, systems can grow from simple to complex while staying true to the core philosophy: definitions, markdown files, and holistic LLM reasoning.

## [1.1.0] - 2026-05-17

### Changed
- **Restructured core framework files for generalization**
  - `thing.skill.md` — Generalized from "thing to do" specific language to work as a specification for *any* domain's atomic unit
  - `read.prompt.md` — Generalized to work with any domain; removed life-management specific references
  - `write.prompt.md` — Generalized prompt guidance; removed phone/calendar integration specifics
- **README.md** — Updated to clarify distinction between specification files (universal foundation) and instantiated domains (domain-specific examples)

### Added
- **Domain structure** — Created `domains/` folder to organize domain-specific implementations
- **domains/life-manager/** folder containing:
  - `life-manager.instructions.md` — Domain-specific philosophy and principles for life management
  - `read.prompt.md` — Life-management-specific read prompt with concrete examples
  - `write.prompt.md` — Life-management-specific write prompt including phone/calendar integration guidance
- **instructions-guide.md** — Comprehensive guide for creating domain-specific instructions files

### Removed
- Duplicate `life-manager.instructions.md` from root level (consolidated into `domains/` structure)

### Clarified
- Core framework now clearly separates:
  - **Specification** (root level): Universal files that apply to any domain
  - **Implementation** (domains/): Domain-specific instantiations of the framework

## [1.0.0] - 2026-05-17

### Added
- **llm-driven-systems.manifesto.md** — Core philosophy and conceptual framework
- **life-manager.instructions.md** — Example instructions file for a life management system
- **thing.skill.md** — Example skill file defining the "thing to do" atomic unit
- **read.prompt.md** — Prompt template for read-only analysis and insights
- **write.prompt.md** — Prompt template for active system management and updates
- **README.md** — Complete documentation on what this framework is and how to use it
- **CONTRIBUTING.md** — Guidelines for contributing domains and improvements
- **CHANGELOG.md** — This file, tracking project evolution
- **LICENSE** — MIT License with copyright notice

### Framework Principles Established
- Definition-driven system design
- Atomic and composable units
- Minimal core with emergent detail
- LLM-centric data structure
- Vendor-agnostic conventions
- Version-controlled everything
- Transparent and auditable systems

---

## How To Use This Changelog

### For Users
- Check here to see what's new in each release
- Stay informed about breaking changes
- Plan your updates accordingly

### For Contributors
- Add your changes here when making pull requests
- Use the categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Keep it organized and readable

### Versioning
- **MAJOR** version for breaking changes to the framework
- **MINOR** version for new domains, features, or capabilities
- **PATCH** version for clarifications, fixes, documentation improvements

---

**Note:** This project tracks changes to the framework specification itself, not to your individual data files. Your data files live in git and have their own version history.
