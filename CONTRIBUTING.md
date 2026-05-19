# Contributing

Thank you for your interest in this framework!

## How To Contribute

### Share Your Domain Definitions

If you've built a domain using the framework (AGENTS.md, skills, example things), consider contributing it as an example:

1. Create a folder for your domain (e.g., `examples/project-management/`)
2. Include your AGENTS.md, skills/ directory (specification, read, write, workflow .skill.md files), and things/ directory with examples
3. Ensure all files have YAML frontmatter following `thing.md` patterns
4. Include examples of real thing instances demonstrating your domain's types
5. Submit a pull request

### Improve Framework Specifications

The framework's own specs are things — they have frontmatter, relationships, statuses, and versions. If you see ways to improve them:

1. Fork the repository
2. Make your changes — ensure YAML frontmatter stays valid and relationships remain consistent
3. Run the validation checklist (see AGENTS.md) before submitting
4. Explain your reasoning in the pull request
5. Follow `git-workflow.md` commit conventions in your commit messages

### Report Issues

If something doesn't work or is unclear:

1. Open an issue describing the problem
2. Include examples if relevant
3. Explain what you expected vs. what happened

### Share Insights

If you've used this framework and learned something useful:

1. Share your experience (issue, discussion, or blog post)
2. Document what worked, what didn't, what surprised you
3. Suggest improvements based on real-world use

## Framework Structure

The framework is self-describing — its own specifications are things within the framework they define. The key files:

**Orchestration:**
- `AGENTS.md` — Root agent file (auto-discovered by LLM tools)

**Foundational Specifications (type: specification):**
- `thing.md` — The atomic unit definition (structure, triggers, metadata)
- `interface.md` — The I/O layer (input routes, output types, deliverables)
- `git-workflow.md` — Git as state machine (commit points, conventions, event stream)
- `read.thing.md` — How LLMs read and reason about things
- `write.thing.md` — How LLMs create and manage things

**Skills (type: skill):**
- `validate.thing.skill.md` — Thing validation (structural, referential, semantic)

**Guides (type: guide):**
- `scalability-guide.md` — Scaling from tens to thousands of things
- `domain-specification-guide.md` — How to create a new domain

**Philosophy (type: manifesto):**
- `llm-driven-systems.manifesto.md` — The paradigm shift and core principles

**Examples:**
- `examples/life-manager/` — Personal life and work management domain
- `examples/compliance-patterns/` — Regulatory compliance pattern library

**Templates:**
- `templates/` — Starting-point templates for AGENTS.md and skills

## Guidelines

- **Keep it simple** — The whole point is elegant constraint and clarity. Don't over-complicate things.
- **Everything is a thing** — All files should have YAML frontmatter with at minimum: id, type, status, version, created.
- **Follow git-workflow.md** — Use structured commit messages (`create:`, `update:`, `framework:`, etc.)
- **Follow the pattern** — New domains should follow the three-layer structure (AGENTS.md, skills/, things/).
- **Be respectful** — We're building something together. Assume good intent.
- **Validate before submitting** — Check that linked_things references are valid, required fields are present, and the validation checklist passes.
- **Version numbers are per-file, not global** — A file at `version: 1.0` alongside one at `version: 2.1` is intentional, not inconsistency. Version tracks that file's own change history; `status` (`draft`/`evolving`/`stable`) tracks maturity. Newer specs start at 1.0 when introduced regardless of the overall framework version.
- **Naming conventions are frozen** — The patterns `-specification`, `.thing.`, `.skill.md` stabilised at v2.x and are not subject to further change. Renames are breaking changes to all domains using the framework.

## What We're Looking For

- Domain definitions that show the framework's flexibility
- Improvements to clarity or usability of core specifications
- Examples showing real-world application
- New skills that extend the framework's capabilities
- Documentation improvements

## What We're Not Looking For

- Vendor-specific integrations (we want to stay agnostic)
- Complex code solutions (this is about structure, not code)
- Breaking changes to the core pattern
- Proprietary or closed-source additions

## Getting Started

1. Read the manifesto to understand the philosophy
2. Read `thing.md` to understand the atomic unit
3. Read `domain-specification-guide.md` to understand how domains are created
4. Look at `examples/life-manager/` or `examples/compliance-patterns/`
5. Try building something in your own domain
6. Share what you learn

## Questions?

Open an issue or start a discussion. We're all learning how to do this.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
