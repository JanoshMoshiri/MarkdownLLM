---
id: llm-driven-systems-manifesto
type: manifesto
status: stable
version: 2.3
created: 2026-05-13
linked_things:
  - id: scalability-guide
    relation: informs
  - id: domain-specification-guide
    relation: informs
---

# LLM-Driven Systems Manifesto

## The Paradigm Shift

We are at an inflection point in how humans and machines collaborate on complex systems.

For decades, the dominant pattern has been: humans design systems, write code to implement those designs, and then use those systems. Applications are monolithic bundles where interface, logic, and storage are tightly coupled. To change behavior, you change code. To integrate new capabilities, you wire them together through APIs and integrations.

This is breaking down.

A new pattern is emerging: **humans define domains, LLMs reason within those domains, and structured data in version control becomes the persistent state.**

This is not about replacing humans or automating everything. It's about inverting the relationship. Instead of building applications that users interact with, we're building definition files that LLMs understand, and then letting the LLM be the active reasoning engine while humans provide direction and oversight.

### The Continuity Beneath The Shift

It is tempting to read all of this as something wholly new. It is not — and seeing why is the key to the whole framework.

A program has only ever been two things: **data structures** — what exists and how it is shaped — and **instructions** — what to do, in what order, under what conditions. Every language that ever compiled, from assembly to C++ to Python, was a notation for expressing those two invariants. The syntax differed wildly; the primitives never did.

This framework is the same two things in a different notation:

- `thing.md` defines the **data structure**.
- The prompts in `templates/prompts/` are the **instructions**.
- The hooks in `orchestration.md` are the **control flow**.
- Git is the **state machine** — the commit is the moment state becomes real.

What changed is the notation, and with it the reader of the notation. A compiler-parsable grammar gave way to natural language; a deterministic compiler gave way to a reasoning model. The artifact did not become something new — the program is still a program. It is simply written in a notation a mind can reason over rather than one a machine must parse, and so the reader can now hold ambiguity, weigh context, and revise its own understanding, which no compiler ever could.

This is why the old discipline still governs the new medium. Clean Architecture and SOLID are not loose analogies borrowed for flavour — they apply because this is literally the same kind of artifact they were always about. The paradigm did not abolish software engineering. It freed software from the demand that its notation be mechanically parsable, and moved the leverage from *making the syntax precise enough to compile* to *making the definition clear enough to reason within*.

See `the-notation-changed-not-the-primitives` for the canonical articulation.

## Origins and Influences

This framework did not emerge from nothing. It builds upon decades of proven thinking in software architecture and leverages conventions that already exist in the LLM ecosystem.

### Standing On Shoulders

**Clean Architecture** (Robert C. Martin) is a direct ancestor of this thinking. The principle that systems should be organised into layers with clear boundaries, that dependencies should point inward toward core business logic, and that the details (databases, UIs, frameworks) should be plugins — not foundations — informed the three-layer model here. Interface is replaceable. Storage is replaceable. Only the domain reasoning at the centre matters.

**SOLID Principles** (also Robert C. Martin) shaped the atomic, composable nature of things. Single Responsibility: each thing does one thing. Open/Closed: things are extensible through new fields without modifying existing structure. Dependency Inversion: skills depend on abstractions (thing.md), not on specific data instances.

These ideas are not new. What's new is applying them to a world where the "logic layer" is an LLM, the "database" is git, and the "interface" is whatever channel connects you to the LLM.

### Building On What Exists

A core philosophy of this framework is: **do not invent what already exists.** Build upon it.

- **AGENTS.md** — This file convention is an existing standard, adopted across GitHub Copilot, OpenAI Codex, Cursor, Windsurf, Gemini CLI, and stewarded by the Agentic AI Foundation under the Linux Foundation. We didn't create it. We use it.
- **.skill.md** — The skill file convention is an emerging convention for packaging reusable LLM capabilities — not yet a standard with a steward like AGENTS.md, but a pattern converging across agent tooling. We didn't create it. We use it.
- **YAML frontmatter** — A convention used across static site generators, documentation tools, and content management systems for decades. We didn't create it. We use it.
- **Markdown** — The universal plain-text format. Readable by humans, parseable by machines, diffable by git. We didn't create it. We use it.
- **Git** — Decades of proven version control. Branching, merging, history, collaboration, rollback. We didn't create it. We use it.
- **LLMs themselves** — The reasoning engine. We don't build LLMs. We define domains they can reason within.
- **Existing input routes** — VS Code, CLI tools, mobile apps, voice-to-text. We don't build interfaces. We leverage what already connects humans to LLMs.

This is a deliberate philosophical choice. Every piece of infrastructure this framework relies on is already proven, already understood, already maintained by others. The framework's contribution is **the pattern of how these pieces compose** — not the pieces themselves.

This means:
- **Lower barrier to entry** — Everything here is something people already know
- **No vendor lock-in** — Every component is interchangeable with equivalents
- **Durability** — The framework survives any single tool disappearing because it depends on patterns, not products
- **Focus** — Energy goes into domain definition and reasoning patterns, not infrastructure

The insight is that the LLM era doesn't need new protocols, new databases, or new interface paradigms. It needs a clear architecture for how existing tools compose around a new kind of intelligence. That's what this framework provides.

### Spec When Foreseeable, Deploy When Felt

The framework specs problems when they're foreseeable and deploys solutions when they're felt. A well-understood future problem earns a specification — a documented design ready to activate. But implementation waits until the friction is real. This prevents over-engineering while ensuring the framework has answers ready when domains outgrow their current patterns.

This is the conductor's discipline: know the full score, but only bring in each section when the music calls for it.

## The Three Decoupled Layers

Traditional applications couple three concerns:

1. **Interface** — How input gets in and output gets displayed
2. **Processing** — The logic and reasoning that happens in the middle
3. **Storage** — Where state persists

This coupling creates rigidity. Changing the interface means touching the logic. Adding storage means redesigning. Everything is interdependent.

The new pattern decouples these entirely:

**Processing:** An LLM (Claude, GPT, or any capable model) becomes the reasoning engine. The LLM understands context, handles ambiguity, reasons about complexity. It's not rule-based logic—it's semantic understanding.

**Interface:** Your phone, your voice, your preferred chat application. The interface is pure I/O. You talk to the LLM. The LLM sends you notifications and calendar updates. The interface is thin and replaceable.

**Storage:** Git repositories containing markdown files with YAML frontmatter. Your data lives in plain text, versioned, human-readable, completely portable. Not in databases or proprietary formats. In git.

These three layers are now independent. You can swap the interface without touching storage. You can change which LLM you use without rewriting anything. You can migrate your data by copying files.

## Discovery: The Partnership Without Configuration

The architecture above only works if an agent can *find it*. This is where discovery comes in — and it's what makes the human-agent partnership effortless.

When you open a workspace, the agent discovers `AGENTS.md` at root. This is not something you configure or invoke — it's a convention that LLM tools already support. The agent reads AGENTS.md, finds the skills it should load, resolves `framework_root` to locate foundational specifications, and enters the domain fully oriented. No manual context loading. No "here, read this file first." The agent arrives ready.

This is what enables the relationship to be natural. You don't need to teach the agent how to use the framework — the framework teaches the agent. You don't need to remember what context to provide — the agent discovers it. You just start talking about what you want to do, and the agent is already grounded in the domain's philosophy, structure, and history.

Discovery is also what makes the system grow without friction. When you add a new skill, the agent picks it up next session. When you commit new things, they're part of the context the agent reads. When the framework itself evolves, domain agents can detect and incorporate those changes through the refresh mechanism. The system expands and the agent adapts — with the human directing where it goes, and the agent handling how to get there.

This is the quiet foundation beneath everything else: a set of file conventions that mean an agent can enter any MarkdownLLM domain and immediately understand what it is, how it works, and how to help.

## Why This Works

**LLMs are remarkably good at understanding semi-structured data.** You don't need rigid schemas or normalized databases. YAML frontmatter provides enough structure for reliable parsing. Markdown provides enough narrative context for true semantic understanding.

**Markdown + YAML is a universal format.** Every LLM can read it. Every programmer can read it. Every version control system handles it. It's not locked to a platform or vendor.

**Git is a miracle for state management.** Your entire history is preserved. You can see how things evolved. You can roll back. Collaboration and merging work. Backup is trivial.

**Users understand files.** You don't need to learn a new interface paradigm. Files are files. Folders are folders. Git is git.

**The LLM handles the cognitive load.** Instead of building complex conditional logic in code, you let the LLM reason about context. Instead of designing UIs, you define data structures and let the interface be simple.

## The Generalization

What started as a life management system is actually a generalizable framework for **any domain that requires persistent state, relationship management, and LLM reasoning.**

Examples:

- **Project management:** Things to do become projects, tasks, subtasks. Dependencies and blockers are relationships. Claude reasons about what's critical, what's unblocked, what patterns you're missing.

- **Knowledge management:** Articles, notes, ideas become atomic units. Tags and links create the graph. Claude synthesizes across your knowledge base, identifies gaps, suggests connections.

- **Financial tracking:** Transactions, accounts, budgets become things. Claude reasons about spending patterns, suggests optimizations, flags anomalies.

- **Health and fitness:** Workouts, nutrition, sleep, goals become trackable units. Claude reasons about patterns, suggests adjustments, identifies what's working.

- **Creative projects:** Stories, characters, scenes, arcs. Claude helps develop narrative, track continuity, suggest improvements.

- **Research:** Papers, findings, hypotheses, experiments. Claude synthesizes across your research, identifies patterns, suggests next directions.

The pattern is the same: define your domain in definition files, structure your data as atomic units with metadata and narrative, use git for persistence, invoke the LLM to reason and update.

## Core Principles

### 1. Definition-Driven

Everything starts with clear definition. You define what a thing is. You define how the system works. You define interaction modes. The LLM operates within those definitions.

This is not free-form. It's constrained and intentional. But the constraints are human-readable and can evolve.

### 2. Atomic and Composable

Every unit is atomic. A project is a unit. A task is a unit. A subtask is a unit. They relate to each other through explicit references, not implicit hierarchy.

This enables flexibility. What starts as a task can become a project. What's a subtask can be promoted. Relationships can change without restructuring.

### 3. Minimal Core, Emergent Detail

You start with minimal required structure. ID, type, status, created date. Maybe a few more fields. Everything else emerges as the domain grows.

The schema evolves with your needs. You don't predict what you'll need; you discover it through use. The LLM can suggest new fields. Git preserves the history of that evolution.

### 4. LLM-Centric Structure

The data structure is optimized for the LLM to parse and reason with, not for humans to manually read and edit.

This is a subtle but important inversion. Humans can read it (because markdown is human-readable), but the primary consumer is the LLM. Let that guide your choices.

### 5. Vendor Agnostic

Use standard conventions (AGENTS.md, .skill.md, YAML frontmatter). Don't lock yourself to one LLM vendor or framework.

Any LLM should be able to read your definitions and operate within your system. This gives you optionality and future-proofs your investment.

### 6. Version-Controlled Everything

Git isn't just for code. It's for your life, your knowledge, your work, your thoughts.

You get temporal history. You can see how things evolved. You can compare versions. You can collaborate. You can migrate. You can audit.

But git is more than version control in this framework — **git is the state machine.** In a traditional application, writing to the database is the moment state becomes real. Here, the commit is that moment. Everything before the commit is working state. Everything after is persisted, versioned, auditable truth.

This means commit discipline matters. Commits should happen at the boundary where domain state changes meaning: when a thing is created, when a status transitions, when a write session completes. Each commit message should describe the domain state change — not "modified 3 files" but "complete: data-collection → unblocks quarterly-review." Git log becomes a readable narrative of your domain's evolution.

This also means git history becomes the event stream. Triggers that watch for state changes (a dependency resolved, a due date passed) evaluate against committed history. Session orientation reads recent commits to understand what changed. The three layers — working session narrative (worklog), commit history (git log), and exact modifications (git diff) — together provide complete traceability from intent through action to detail.

See `git-workflow.md` for the full operational specification.

### 7. Transparent and Auditable

Your entire system is readable. No black boxes. The LLM's reasoning can be explained because it's working from clear definitions and explicit data.

You can see what changed, when, and why (if you document it). You can disagree with the LLM and override it. You remain in control.

### 8. Self-Describing (Fractal)

The system can describe itself within itself. The same pattern — YAML frontmatter, markdown body, relationships, statuses — applies at every scale: to data instances, to domain specifications, to the framework's own definitions.

This is a fractal property. In nature, fractals are patterns that recur at every level of magnification — the same structure whether you look at the whole or any part. This framework has the same quality: a thing is a thing whether it's a task in your life manager, a compliance pattern in your regulatory domain, or a specification that defines how things work.

This is not a requirement imposed on domain builders. It's a property that emerges naturally from the design: if everything is a thing, then everything — including the definitions themselves — can be structured, linked, validated, and reasoned about using the same patterns.

The implications:

- A framework that can define itself proves its own universality
- No special cases exist — the rules apply to themselves
- An LLM can reason about the system and about itself within the system using the same skills
- Evolution of the framework is tracked, validated, and auditable just like evolution of domain data

## How It Works In Practice

1. **Define your domain** — Create an AGENTS.md at root that orchestrates how the LLM interacts with your domain. Create skills that define your domain's philosophy, read/write patterns, and workflows.

2. **Define your atomic unit** — Reference thing.md to understand how things are structured. Create domain-specific thing types with appropriate metadata.

3. **Create instances** — Your actual data lives as thing files in `things/`. Each file is an instance of your atomic unit, with YAML metadata and narrative body.

4. **Interact through any route** — Speak, type, or otherwise communicate your intent through any input route (VS Code, CLI, mobile, voice). The agent auto-loads and reasons within your domain.

5. **Let it flow** — The agent produces things (persistent state) and deliverables (documents, code, images, notifications) depending on what you need. Updates flow back through your output route.

6. **Commit at meaningful boundaries** — Each state change is committed with a structured message. Git log becomes your domain's event narrative. Triggers evaluate against committed history.

7. **Iterate** — The loop repeats. Definitions evolve. Schema grows. Triggers catch what needs attention. The system becomes more sophisticated while remaining transparent.

Git preserves all of it. You have a complete audit trail and history.

## What This Enables

**User agency.** You define your system. You're not locked into someone else's design choices. You can fork and modify anything.

**Portability.** Your data is just files. You can move it anywhere. Run it on any LLM. Integrate it with any tool that reads markdown and git.

**Composability.** Multiple domains can coexist — they're all just files under one framework. Within a domain, things compose freely. *Across* domains, composition is deliberate, not implicit: domains are isolated, separate-id-space repos by design, so one domain consuming another's output is a verified hand-off (treated as external input — quarantined until confirmed, see `provenance.md`), not a raw cross-repo link. The full cross-domain hand-off mechanism is foreseen but not yet specified (sketch: `things/insights/cross-domain-handoff-is-verified-external-input.md`); until it ships, treat cross-domain references as an explicit import, not a promise the framework already keeps.

**Evolution.** You're not stuck with your initial design. The schema evolves. Fields emerge. Relationships change. Git preserves the history.

**Collaboration.** If multiple people need to work within the system, git's collaboration tools work naturally. Merge, branch, resolve conflicts using standard git workflows.

**Auditing.** Everything is transparent and versioned at three layers: your session worklog captures intent and decisions; git log captures state changes with structured commit messages; git diff captures the exact modifications. Together, these provide complete traceability — from why a decision was made, through what changed, down to the specific bytes that were modified. No black boxes. No lost context.

## Elegant Constraint Enables Efficiency

There's a common assumption in the LLM space: bigger models are always better. More parameters, more tokens, more compute.

But this pattern inverts that thinking.

When you provide a smaller LLM with a clearly defined domain, explicit rules, structured data, and specific instructions, you're not asking it to figure out the problem space and solve within it simultaneously. You're asking it to read markdown, understand relationships, and apply straightforward reasoning within constraints that are already defined.

That's fundamentally different from asking a model to invent the system and reason within it at the same time.

A smaller model—one that costs less, runs faster, produces lower latency—can handle complex systems effectively when the system itself is well-defined. The cognitive load isn't on the model to figure out what to do. The cognitive load is on the human to define the domain clearly. Then the model executes within those constraints.

This has profound implications:

**Cost.** Smaller models are cheaper to run. If your system is well-designed, you don't need frontier-level reasoning. You need reliable reasoning within constraints.

**Speed.** Smaller models are faster. On a phone, in a real-time application, latency matters. A smaller model that gives you 95% of what you need in half the time is often better than a larger model that's slower.

**Reliability.** Constrained systems with explicit rules have less room for hallucination. The model isn't inventing; it's executing within boundaries.

**Accessibility.** Not everyone needs or can afford the most powerful models. A well-designed system using a smaller model is more accessible to more people.

**Sustainability.** Less compute means less power consumption. It's better for the environment and your infrastructure costs.

The insight is this: **elegant constraint is more powerful than raw capability.** The claim, stated carefully: a smaller model operating within a well-defined system can match or outperform a larger model operating without structure.

Two claims must be kept apart here, because the framework has good evidence for one and not the other:

- **Utility — well-evidenced.** That the framework delivers real value is no longer in question: it is in production use, and at least one independent operator adopted it cold and carried a domain through to a marketed MVP. Structure buying determinism and consistency across sessions and vendors is demonstrated.
- **Model-tier superiority — a hypothesis, still open.** That a *smaller* model with structure beats a *larger* one without it is the framework's central **hypothesis**, not a result. It rests on one eval (2026-06-11, `evals/README.md`) whose reasoning core *saturated* — the task was not discriminating enough to separate the conditions on reasoning quality, only on cost and determinism. The capability half of the claim stays untested until a harder, non-saturating fixture exists. Do not cite it as proven.

This is about shifting the optimization target. Instead of "how do we build more powerful models," ask "how do we design systems that enable smaller models to be effective." The answer is clarity, structure, and constraint.

In this era of LLM scaling, that's counterintuitive. But it's also where the real leverage is.

## What This Is Not

This is not about removing human judgment. The LLM is a reasoning engine, not a decision-maker. Humans remain in control.

This is not about automating away complexity. The complexity moves. Instead of coding complexity, you're defining domain complexity. The LLM helps reason through it.

This is not a replacement for human creativity, values, or direction. It's a tool for executing your intentions more effectively.

This is not a silver bullet. Some domains need real databases. Some problems need specialized code. This pattern is powerful for many things, not all things.

## The Future

As LLMs become more capable, this pattern becomes more powerful. Better reasoning means better handling of ambiguity. Better parsing means richer data structures. Better context windows mean larger, more complex systems can be reasoned over in a single conversation.

The tools will evolve. IDEs will gain better support for working with these systems. Hosting platforms will emerge. Conventions will solidify. Open standards will develop.

But the core insight is stable: humans define domains, LLMs reason within them, and versioned markdown files become the lingua franca.

## Self-Describing Architecture

The framework describes itself within itself. Its own specifications are things — with YAML frontmatter, IDs, types, statuses, versions, and explicit relationships to each other.

This is not circular. It is fractal.

A circular reference is A depends on B depends on A — a loop with no resolution. A fractal is a pattern that recurs at every scale — the same structure appearing whether you look at the whole or any part.

The MarkdownLLM framework defines how things work. The framework's own specifications are things. They have frontmatter. They have relationships. They have statuses (`draft`, `evolving`, `stable`). They can be validated by the same validation skill that validates domain things. They are committed following the same git-workflow conventions that domains follow.

**Why this matters:**

- **Proof of universality** — If the framework can represent itself, it can represent anything. If it couldn't, that would reveal a gap.
- **Dogfooding** — Every principle the framework espouses is tested against itself. "Everything is a thing" is either true or it isn't. It is.
- **Agent-navigable** — The framework's own AGENTS.md lets an LLM reason about the framework itself — understanding which specs exist, how they relate, which are mature, which are drafts.
- **No special cases** — There is no category of "meta-stuff that doesn't follow the rules." The rules apply everywhere, including to themselves.

This is the philosophical endpoint of definition-driven systems: the system that defines itself, manages itself, and evolves itself — with a human directing and an LLM reasoning.

## Getting Started

If you want to build a system using this pattern:

1. **Start small.** Pick a domain you care about. Define it clearly.

2. **Create your AGENTS.md.** This is where you design how the agent should behave within your domain — what skills it loads, what reasoning patterns it follows, what constraints it operates within. The agent discovers this automatically. You're not configuring a tool; you're defining a collaborator's operating principles.

3. **Create your skills.** Specification (philosophy), read (how to analyse), write (how to modify), workflow (process patterns). These are the agent's expertise for your domain — the guidance that makes it reason consistently and well.

4. **Create a few things.** Your actual data. Show the system what you mean by concrete instances with frontmatter and narrative.

5. **Interact.** Through whatever route works — VS Code, CLI, voice, mobile. The agent loads, skills guide reasoning, things provide context. You direct; the agent executes.

6. **Use the output. Provide feedback.** This is not a one-shot generation. You use what the agent produces. You come back with refinements. You say "this workflow needs another step" or "this thing type should capture X." The system grows through this loop.

7. **Commit meaningfully.** Each state change gets a structured commit. Git becomes your domain's event stream and audit trail.

8. **Iterate and share.** Your definitions will evolve. Skills refine. Thing types mature. Workflows adapt. Document the journey. Once you've built something useful, share it — others can fork and adapt for their own domains.

This is the new way of building systems. Not with code and databases and complex integrations. With clear thinking, structured definitions, and an ongoing partnership between human direction and machine reasoning.
