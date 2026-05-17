# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Coming Soon
- Additional domain examples (project management, knowledge base, financial tracking)
- Tools and utilities for working with the framework
- Integration guides for popular LLMs and platforms

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
