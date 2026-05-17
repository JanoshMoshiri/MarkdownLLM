# LLM-Driven Systems Manifesto

## The Paradigm Shift

We are at an inflection point in how humans and machines collaborate on complex systems.

For decades, the dominant pattern has been: humans design systems, write code to implement those designs, and then use those systems. Applications are monolithic bundles where interface, logic, and storage are tightly coupled. To change behavior, you change code. To integrate new capabilities, you wire them together through APIs and integrations.

This is breaking down.

A new pattern is emerging: **humans define domains, LLMs reason within those domains, and structured data in version control becomes the persistent state.**

This is not about replacing humans or automating everything. It's about inverting the relationship. Instead of building applications that users interact with, we're building definition files that LLMs understand, and then letting the LLM be the active reasoning engine while humans provide direction and oversight.

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

Use standard conventions (.instructions.md, .skill.md, .prompt.md). Don't lock yourself to one LLM vendor or framework.

Any LLM should be able to read your definitions and operate within your system. This gives you optionality and future-proofs your investment.

### 6. Version-Controlled Everything

Git isn't just for code. It's for your life, your knowledge, your work, your thoughts.

You get temporal history. You can see how things evolved. You can compare versions. You can collaborate. You can migrate. You can audit.

### 7. Transparent and Auditable

Your entire system is readable. No black boxes. The LLM's reasoning can be explained because it's working from clear definitions and explicit data.

You can see what changed, when, and why (if you document it). You can disagree with the LLM and override it. You remain in control.

## How It Works In Practice

1. **Define your domain** — Create an instructions file that explains what you're building and why. Create a skill file that defines your atomic unit.

2. **Define interaction** — Create prompt files for different modes (read, write, analyze, whatever makes sense for your domain).

3. **Create instances** — Your actual data lives in files. Each file is an instance of your atomic unit, with metadata and narrative body.

4. **Invoke the LLM** — Feed the definition files and relevant data files to the LLM with a prompt. The LLM reads, understands, reasons, and either provides insights or makes updates.

5. **Let it flow** — Updates from the LLM feed to your interface (phone notifications, calendar entries, dashboard updates). You interact and provide new direction.

6. **Iterate** — The loop repeats. Over time, your definitions evolve. Your schema grows. The system becomes more sophisticated.

Git preserves all of it. You have a complete audit trail and history.

## What This Enables

**User agency.** You define your system. You're not locked into someone else's design choices. You can fork and modify anything.

**Portability.** Your data is just files. You can move it anywhere. Run it on any LLM. Integrate it with any tool that reads markdown and git.

**Composability.** Multiple domains can coexist. Your life manager and your knowledge base can reference each other. Your financial tracking can link to your projects. They're all just files.

**Evolution.** You're not stuck with your initial design. The schema evolves. Fields emerge. Relationships change. Git preserves the history.

**Collaboration.** If multiple people need to work within the system, git's collaboration tools work naturally. Merge, branch, resolve conflicts using standard git workflows.

**Auditing.** Everything is transparent and versioned. You can see exactly what changed, when, and trace the reasoning.

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

The insight is this: **elegant constraint is more powerful than raw capability.** A smaller model operating within a well-defined system will outperform a larger model operating without structure.

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

## Getting Started

If you want to build a system using this pattern:

1. **Start small.** Pick a domain you care about. Define it clearly.

2. **Create your definition files.** Instructions, skills, prompts. Be explicit about the rules of your system.

3. **Create a few instances.** Your actual data. Show the LLM what you mean by concrete examples.

4. **Interact with the LLM.** Use the prompts you defined. Let the LLM read your data and reason about it.

5. **Iterate.** Your definitions will evolve. Your schema will grow. Document the changes and commit to git.

6. **Share and adapt.** Once you've built something useful, share the definitions. Others can fork and adapt them for their own domains.

This is the new way of building systems. Not with code and databases and complex integrations. With clear thinking, structured data, and partnership with intelligence.
