# Contributing

Thank you for your interest in this framework!

## How To Contribute

### Share Your Domain Definitions

If you've built a domain using the framework (AGENTS.md, skills, example things), consider contributing it as an example:

1. Create a folder for your domain (e.g., `examples/project-management/`)
2. Include your AGENTS.md and skills/ directory (specification, read, write, workflow .skill.md files)
3. Include a things/ directory with example instances demonstrating your domain's types
4. Ensure every record has YAML frontmatter following `thing.md` patterns
5. Do NOT include `thing.md` in your domain — it's a foundational framework spec, not domain-specific
6. Submit a pull request

### Improve Framework Specifications

The framework's own specs are things — they have frontmatter, relationships, statuses, and versions. If you see ways to improve them:

1. Fork the repository
2. Make your changes — ensure YAML frontmatter stays valid and relationships remain consistent
3. Run the floor before submitting: `mdllm validate .` and `mdllm coherence .` (on Windows `./tools/mdllm.ps1`, elsewhere `sh tools/mdllm.sh`; the installed pre-commit hook runs both — `mdllm install-hook .` installs it)
4. If you changed a specification, a guide or anything else other records rely on, the commit is refused until its walk is recorded: run `mdllm cues . --staged --raise`, mark each dependant (still holds, revised, or needs a ruling), and commit the answered cue with your change
5. If you changed a spec's `<!-- kernel -->` block, regenerate with `mdllm kernel`; if you changed the CLI, regenerate the docs with `mdllm docs .` — the floor refuses stale generated files
6. Run the tests: `python -m pytest tools/tests -q` from an environment with PyYAML
7. Explain your reasoning in the pull request, and follow `git-workflow.md` commit conventions — the commit message is the record

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

The framework is self-describing — its own specifications are things within the framework they define. This file deliberately does **not** restate the spec inventory (a hand-copied list here drifted for months). The canonical sources:

- **`.markdownllm`** — the machine-read catalog of foundational specs
- **`AGENTS.md`** → *Framework Specifications* — the annotated inventory, with each spec's type and status
- **`docs/framework-map.md`** — the visual architecture map
- **`tools/mdllm.py`** — the mechanical floor (validation, coherence, scaffolding); `python tools/mdllm.py --help` lists the surface
- **`examples/`** — complete example domains; **`templates/`** — starting-point templates

## Guidelines

- **Keep it simple** — The whole point is elegant constraint and clarity. Don't over-complicate things.
- **Every record is a thing** — Records (specs, guides, records under `things/`) carry YAML frontmatter with at minimum: id, type, status, created (see `thing.md`; `version` is convention for specs, not a core field). Tooling, configuration and front-door files such as this one and the README are not things.
- **Follow git-workflow.md** — Use structured commit messages (`create:`, `update:`, `framework:`, etc.)
- **Follow the pattern** — New domains should follow the three-layer structure (AGENTS.md, skills/, things/).
- **Be respectful** — We're building something together. Assume good intent.
- **Validate before submitting** — `mdllm validate .` must pass; it checks frontmatter, references, and schema conformance mechanically.
- **Version numbers are per-file, not global** — A file at `version: 1.0` alongside one at `version: 2.1` is intentional, not inconsistency. Version tracks that file's own change history; `status` (`draft`/`evolving`/`stable`) tracks maturity. Newer specs start at 1.0 when introduced regardless of the overall framework version.
- **Naming conventions are frozen** — The patterns `-specification`, `.thing.`, `.skill.md` stabilised at v2.x and are not subject to further change. Renames are breaking changes to all domains using the framework.

## What We're Looking For

- Domain definitions that show the framework's flexibility
- Improvements to clarity or usability of core specifications
- Examples showing real-world application
- New skills that extend the framework's capabilities
- Documentation improvements

## What We're Not Looking For

- Vendor logic in the neutral tool — vendor-specific code belongs in an adapter under `tools/markdownllm/adapters/`, and the architecture tests refuse it anywhere else
- Code where a declaration would do — prefer a field the floor can check over a mechanism
- Breaking changes to the core pattern
- Proprietary or closed-source additions

## Getting Started

### Prerequisites

You need an **LLM tool with file-system access** — one that can traverse directories, read and write files, and either deliver `AGENTS.md` through a tested entry route or accept an explicit bootstrap. The framework has named execution evidence for Claude Code and Codex surfaces; other file-aware products are designed-for until their own route is exercised. Ordinary web chat without file access will not work.

### Setting Up Your Own Workspace

1. **Install the framework** — follow *Get started* in the README (the verified install of the newest release), or clone the repository if you are contributing
2. **Follow [the first hour](docs/first-hour.md)** — it is written for you; `domain-specification-guide.md` is your agent's reading, not yours
3. **Read the manifesto if you want the why** — `llm-driven-systems.manifesto.md`
4. **Let the agent scaffold** — `mdllm scaffold domains/my-workspace --harness <selection>` performs the whole birth sequence deterministically (templates, `git init`, `.gitignore` isolation, hooks, the selected adapter, first commit). Don't hand-roll it — hand-rolled births drop steps.
5. **Tell your agent to fill the semantic half** — describe what you want to track; the agent declares the record types in `_schema.yaml`, writes the skill bodies, and creates seed records
6. **Explore examples** — look at `examples/life-manager/` or `examples/compliance-patterns/` for reference
7. **Iterate** — refine skills and thing types as you learn what works
8. **Share what you learn** — contribute examples, improvements, or insights back to the framework

## Questions?

Open an issue or start a discussion. We're all learning how to do this.

## License

By contributing, you agree that your contributions are licensed under the MIT License.
