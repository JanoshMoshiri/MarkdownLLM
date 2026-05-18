# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Coming Soon
- Additional domain examples (project management, knowledge base, financial tracking)
- Tools and utilities for working with the framework
- Integration guides for popular LLMs and platforms

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
