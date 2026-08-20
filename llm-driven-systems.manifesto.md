---
id: llm-driven-systems-manifesto
type: manifesto
status: evolving
version: 2.9
created: 2026-05-13
linked_things:
  - id: scalability-guide
    relation: informs
  - id: domain-specification-guide
    relation: informs
  - id: divergence-is-an-unrouted-decision
    relation: references
    notes: "v2.6 names the divergence-routing primitive beneath change-reconciliation, belief-revision, provenance, and validate; this insight is its canonical articulation"
  - id: operating-is-programming
    relation: references
    notes: "v2.8 names the second collapse — use and programming are no longer separate acts; this insight is its canonical articulation and carries the evidence"
  - id: the-substrate-is-a-discipline-prosthesis
    relation: references
    notes: "v2.8 widens the thesis's scope note — the floor disciplines both processors; this insight is its canonical articulation"
  - id: expertise-is-an-output-not-a-prerequisite
    relation: references
    notes: "v2.8 states the operator requirement as authority, never credentials; this insight is its canonical articulation"
---

# LLM-Driven Systems Manifesto

## The Paradigm Shift

We are at an inflection point in how humans and machines collaborate on complex systems.

For decades, a program could only do what it was told. Code is a fixed set of instructions, and the processing unit at its center carried them out exactly as written — no more, no less. To change what the system did, you changed the code.

What has changed is the processing unit itself. With an LLM at the centre, a system no longer only executes fixed instructions — a probabilistic interpreter can reason within definitions, propose ideas and inferences, and help identify or repair defects. Those proposals still require tools, authority, and evidence before they become accepted state. That changed collaboration boundary is the paradigm shift.

A new pattern is emerging: **humans define domains, LLMs reason within those domains, and structured data in version control becomes the persistent state.**

This is not about replacing humans or automating everything. It's about inverting the relationship. Instead of building applications that users interact with, we're building definition files that LLMs understand, and then letting the LLM be the active reasoning engine while humans provide direction and oversight.

### The Continuity Beneath The Shift

It is tempting to read all of this as something wholly new. It is not — and seeing why is the key to the whole framework.

A program has only ever been two things: **data structures** — what exists and how it is shaped — and **instructions** — what to do, in what order, under what conditions. Every language that ever compiled, from assembly to C++ to Python, was a notation for expressing those two invariants. The syntax differed wildly; the primitives never did.

This framework is the same two things in a different notation:

- `thing.md` defines the **data structure**.
- The prompts in `templates/prompts/` are the **instructions**.
- The hooks in `orchestration.md` are the **control flow**.
- Git is the **accepted-state machine** — the commit is the moment a candidate becomes the recorded domain state, not the moment the outside world becomes true.

What changed is the notation, and with it the reader of the notation. A compiler-parsable grammar gave way in part to natural language; a deterministic compiler gave way in part to a probabilistic reasoning model. The definitions and their executable behaviour are therefore not literally one artifact: a stochastic interpreter connects them, while deterministic tools enforce the subset expressed as code. Treating the combined system as a program is the useful architectural model, not a claim of compiler equivalence.

This is why the old discipline still governs the new medium. Clean Architecture and SOLID are more than flavour: their boundary, cohesion, and dependency principles apply to this composite artifact even though natural-language interpretation is not compilation. The paradigm did not abolish software engineering. It adds leverage at *making the definition clear enough to reason within* while retaining precise executable checks wherever the invariant is mechanically decidable.

See `the-notation-changed-not-the-primitives` for the canonical articulation.

### The Second Collapse: Operation Is Programming

The continuity above treats the composite artifact as a program. What the notation change does to the *people around* the artifact took longer to see: previous notations often forced programming and use apart. The user speaks in their own nouns; the program is written in another language; so a translator must sit between them. Natural-language definitions lower that translation boundary. Friction stated in the working channel becomes candidate source when it is routed to a seed, spec, insight, or exposed ask; validation checks its mechanical shape, and review plus commit make it durable. **The operator can program the system by operating it** without pretending every utterance is executable or accepted automatically.

This differs from many prior end-user programming approaches by raising the reader toward notation the user already speaks. It does not remove every ceiling or the need for specialist code; it makes many definition changes possible *in the same notation, in the same conversation*. The route is trustworthy only to the extent its boundaries are active and evidenced: an unreviewed or mechanically invalid conversational change is still drift with a good story.

See `operating-is-programming` for the canonical articulation and its evidence.

## The Thesis

Strip the framework to one sentence: **treat the language model as a reasoning processor, and build a loosely-coupled, modular software engine around it — so deterministic structural boundaries and inspectable accepted state make a non-deterministic processor more consistent, auditable, and resistant to drift.**

The goal is not to make the model deterministic. It cannot be, and pretending otherwise is the mistake. The goal is to surround a non-deterministic processor with clear boundaries, modular units, explicit state, version control, and enforced invariants. The deterministic layer can then hold the properties it actually checks; semantic correctness and adherence remain probabilistic outcomes that require evidence and human judgment.

This is a synthesis, not a trade-off. The model brings reasoning over ambiguity, weighing context, and revising an interpretation. Software engineering brings durable accepted state, an audit aid, invariants that do not depend on the processor *remembering* to be careful, and mechanisms that catch enumerated drift — preventing it where the failure is mechanical, surfacing it for correction where the failure is semantic. Git history records decisions and changes that were actually captured; it is not a complete trace of hidden or unrecorded reasoning. The bet is that these combine, and that the whole is worth more than either part.

A scope note the thesis's own words already permit: "integrity that does not depend on the processor remembering to be careful" never specified *which* processor. The floor disciplines the human by exactly the mechanism it disciplines the model — records kept, provenance held, state persisted without anyone remembering to maintain it. For the professional whose field already practices records discipline, the substrate is a recognition of their own profession's demands; for the everyday operator who finds sustained record-keeping too tedious to maintain, the discipline is not a barrier the substrate demands but *the product it delivers*. One floor, two processors, the same prosthesis — and its best-served user is the person every prior tool quietly abandoned, because for them the discipline is not overhead on the value; it is the value. See `the-substrate-is-a-discipline-prosthesis` for the canonical articulation.

There is a reason the processor cannot hold these properties alone: a language model predicts the next move — the next token, the next action — but does not certify its future consequence. It can compare plausible outcomes and risks; actual consequence becomes recoverable only in retrospect. Asking the model to "consider the consequences" is useful prospective analysis, not foresight guaranteed. Irreversible authority therefore belongs to the human and to structures considered ahead of time, alongside ordinary risk analysis. See `consequence-is-recoverable-only-in-retrospect` for the canonical articulation.

That bet is what the framework exists to test. Everything else in this document — the three decoupled layers, atomic things, git as the accepted-state machine, the deterministic floor — is machinery in service of it. To build or extend a domain is to place structure around a reasoning processor and then measure how well the resulting system earns trust over time.

## The Primitive Beneath: A Divergence Is an Unrouted Decision

A domain is a model of a reality it does not control. The thing-graph at a commit is the accepted recorded model; the world is the reality. They will diverge — that is not a defect to engineer away, it is the standing condition of any model-of-reality system. The discipline is not *preventing* divergence; it is **routing every discovered divergence, and never letting one resolve by silent default or by blur.** Each discovered divergence is an *unrouted decision*, and the framework provides three honest routes:

1. **Restore the model** — the divergence is a regression; bring reality back to the spec.
2. **Revise the model** — the spec was wrong or incidental; change it, *with recorded rationale*.
3. **Spawn new work** — the divergence is genuinely new scope; hand it to a requirement-driven process.

The two cardinal sins are the failures to route at all: **silent default** (let it resolve however it falls out) and **blur** (call a regression an improvement, or new scope a bug-fix). Routing is informed by walking the graph both ways — forward for blast radius, backward for the provenance that keeps an incidental behaviour from being mistaken for a contract.

This is named here as a **recognition, not a new mechanism.** It adds nothing to obey that the framework was not already obeying: it is the single spine beneath machinery that already exists, un-unified. `change-reconciliation` is the forward cascade once a divergence is routed; `belief-revision` is route 2 and the valid state of *holding* a contradiction rather than synthesising a false answer from both; `provenance` is the recorded *why* and the quarantine that refuses to let an unverified divergence inform an output silently; `validate`'s surface-don't-silently-fix rule is the no-silent-default law in mechanical form; and `re-quarantine-on-drift` is the same primitive on the cross-domain axis. Five faces, one primitive. Naming the spine costs no new ceremony — the faces each change at a different rate and rightly stay separate things; what drops is the number of *roots*. See `divergence-is-an-unrouted-decision` for the canonical articulation.

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
- **Reduced vendor coupling** — Plain files and explicit contracts preserve a migration path; equivalent harness behaviour still has to be evidenced per product and build
- **Durability ambition** — The durable state is not owned by one model vendor, while Git hosts, runtimes, adapters, and package sources remain real dependencies
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

The new pattern separates these behind explicit contracts:

**Processing:** An LLM (Claude, GPT, or any capable model) becomes the reasoning engine. The LLM understands context, handles ambiguity, reasons about complexity. It's not rule-based logic—it's semantic understanding.

**Interface:** Your phone, your voice, your preferred chat application. The interface is pure I/O. You talk to the LLM. The LLM sends you notifications and calendar updates. The interface is thin and replaceable.

**Storage:** Git repositories containing markdown files with YAML frontmatter. Your data lives in plain text, versioned, human-readable, completely portable. Not in databases or proprietary formats. In git.

These layers can change at different rates. Plain files make storage migration straightforward; interfaces and models can be replaced when their entry, lifecycle, and capability contracts are compatible. Named harness tests — not the architecture alone — establish whether a particular swap works.

## Discovery: The Partnership Without Configuration

The architecture above only works if an agent can *find it*. This is where discovery comes in — and it's what makes the human-agent partnership effortless.

When you open a workspace, a harness may discover `AGENTS.md` directly, reach it through a pointer, or require an explicit bootstrap/emission. The entry contract then names the skills and `framework_root`. Discovery, whole-contract delivery, reading, application, and validated outcome are distinct evidence levels; support is recorded for exact harness builds rather than inferred from a product name.

When that route is active, the relationship can feel natural: the framework supplies durable context instead of asking the operator to reconstruct it manually. But emitted content is not automatically read or obeyed. Integrity trailers, attestations, `doctor`, and behavioural probes report what the substrate can actually observe.

Discovery is also what makes the system grow without friction. When you add a new skill, the agent picks it up next session. When you commit new things, they're part of the context the agent reads. When the framework itself evolves, domain agents can detect and incorporate those changes through the refresh mechanism. The system expands and the agent adapts — with the human directing where it goes, and the agent handling how to get there.

This is the quiet foundation beneath everything else: a set of file conventions and tested delivery routes that give a file-aware agent a portable way to enter a MarkdownLLM domain. Portability is the contract; compatibility is build-specific evidence.

The same law binds the other direction, and deserves stating symmetrically: **the framework must teach the operator the way it teaches the agent** — through discovery, in the channel, at the moment of relevance, in the operator's own nouns. The agent's entry point is AGENTS.md; the operator's entry point is the orientation the session opens with. An operator cannot ask for what they don't know exists, so the conversational surface carries its own affordances — what can be asked arrives beside what was found, exceptions arrive with their remedy attached, and depth is revealed on demand rather than up front. The manual is the conversation.

### The System as Collaborator

This partnership runs deeper than discovery. Working within a domain is not a single transaction — it is an accretive process. You don't have to hand the system a complete, finished input. You give it an initial set of data, and the reasoning at the center works from that. As you go, you add more: a new constraint, a fresh consideration, an answer to a question that just came up. The agent pulls together what was already in the domain, what you've just added, and the workflow you're following, and carries the work forward toward an output.

Take a software development life cycle. You start with requirements, then move into design. You examine the constraints the design has to satisfy. As you work through those considerations, questions surface — some of which you'll want to take to your data team, or your infrastructure team. The process doesn't stall waiting for a complete specification up front; it accommodates information as it arrives, in the order it arrives.

This is what changes the nature of the relationship. The system no longer just carries out the process and manages it — it participates in it. A defined system becomes one of the collaborators: an administrator that holds the state, an adviser that raises the questions worth asking, and an expert in whatever domain you've built. And the expertise compounds. The more you work within the domain, the more the agent has to reason from — every thing committed, every decision recorded, every relationship drawn becomes context it can draw on next time. The partnership doesn't just persist; it deepens.

## Why This Works

**LLMs are often effective over semi-structured data.** Many domains do not
need a rigid relational model, but they still need an explicit schema at the
mechanical boundary. YAML frontmatter gives the deterministic parser declared
fields; Markdown gives the probabilistic interpreter narrative context. Neither
format, by itself, guarantees a correct interpretation.

**Markdown + YAML is a widely portable plain-text format.** File-aware LLM
harnesses, people, parsers, and Git can work with it without a proprietary data
store. Whether a particular harness discovers, delivers, reads, or applies the
definitions is still an exact-product evidence question.

**Git is unusually well suited to accepted-state management.** Retained commits
make evolution and rollback inspectable, and Git supplies explicit collaboration
mechanics. History can still be rewritten or lost, merge decisions remain real
decisions, and a local repository is not a backup until an independent copy is
actually maintained.

**Users understand files.** You don't need to learn a new interface paradigm. Files are files. Folders are folders. Git is git.

**The LLM can carry part of the cognitive load.** Instead of encoding every
contextual judgment as branching code, you give a reasoning model structured
context. Deterministic rules and purpose-built interfaces still belong in code
where the consequence or repeatability demands them.

## The Generalization

What started as a life management system is a reusable candidate for **many
domains that require persistent state, relationship management, and LLM
reasoning.** Suitability is demonstrated per domain; self-description is not a
proof of universality.

Examples:

- **Project management:** Things to do become projects, tasks, subtasks. Dependencies and blockers are relationships. Claude reasons about what's critical, what's unblocked, what patterns you're missing.

- **Knowledge management:** Articles, notes, ideas become atomic units. Tags and links create the graph. Claude synthesizes across your knowledge base, identifies gaps, suggests connections.

- **Financial tracking:** Transactions, accounts, budgets become things. Claude reasons about spending patterns, suggests optimizations, flags anomalies.

- **Health and fitness:** Workouts, nutrition, sleep, goals become trackable units. Claude reasons about patterns, suggests adjustments, identifies what's working.

- **Creative projects:** Stories, characters, scenes, arcs. Claude helps develop narrative, track continuity, suggest improvements.

- **Research:** Papers, findings, hypotheses, experiments. Claude synthesizes across your research, identifies patterns, suggests next directions.

The pattern is the same: define your domain in definition files, structure your data as atomic units with metadata and narrative, use git for persistence, invoke the LLM to reason and update.

### The Operator: Authority, Not Credentials

And the operator this pattern asks for is not a professional. Read what the floor actually demands of its human: quarantine requires that *a human confirms*, and the flip names a person — never a credential. The requirement is **authority**: standing to say "this is true in my domain." For a regulated quality system that standing happens to require a profession; for a person's own spending, household, or plans it is automatic and absolute — no professional on earth knows which of your transactions was a gift and which was a mistake. The everyday operator is not a degraded case of the expert operator; they are the purest case of what the substrate requires.

Expertise, meanwhile, runs the other direction. Classic expert systems encoded an expert's knowledge so non-experts could consult it — expertise in, answers out. Here the operator brings authority and intent, the substrate brings discipline, and **expertise accumulates in the domain as a product of use**: insights with dispositions, decisions with rationale, the graph of what was learned and why it still holds. A domain, after enough use, knows things about its subject no professional knows and no generic tool could — it becomes the only expert on its subject in existence. The same primitives, unchanged and unsimplified, run the regulated system and the spending tracker; what differs is only the definition, which is data, not code. The app category dissolves into descriptions — and *definition-driven* turns out to have been the right name all along, with "expert" describing what the domain becomes, not what the operator must be. See `expertise-is-an-output-not-a-prerequisite` for the canonical articulation.

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

Any capable file-aware LLM is a portability target for these definitions. Actual discovery, lifecycle execution, and adherence remain harness- and build-specific claims.

### 6. Version-Controlled Everything

Git isn't just for code. It's for your life, your knowledge, your work, your thoughts.

You get temporal history. You can see how things evolved. You can compare versions. You can collaborate. You can migrate. You can audit.

But git is more than version control in this framework — **git is the state machine for accepted recorded state.** In a traditional application, writing to the database is the moment application state becomes durable. Here, the commit is that moment. Everything before the commit is working state. Everything after is persisted and versioned; it is not thereby guaranteed true of the outside world.

This means commit discipline matters. Commits should happen at the boundary where domain state changes meaning: when a thing is created, when a status transitions, when a write session completes. Each commit message should describe the domain state change — not "modified 3 files" but "complete: data-collection → unblocks quarterly-review." Git log becomes a readable narrative of your domain's evolution.

This also means git history becomes the recorded event stream. Triggers that watch for state changes evaluate against committed history. Session orientation reads recent commits to understand what changed. Commit messages and diffs provide strong traceability from recorded intent through accepted modification to bytes, but cannot reconstruct reasoning or events that were never captured.

See `git-workflow.md` for the full operational specification.

### 7. Transparent and Auditable

The framework-owned files and accepted domain state are readable. The LLM's recorded inputs, decisions, and changes can be explained from explicit data; the model's hidden reasoning and the vendor harness remain external black boxes the framework does not claim to expose.

You can see what changed, when, and why (if you document it). You can disagree with the LLM and override it. You remain in control.

### 8. Self-Describing (Fractal)

The system can describe itself within itself. The same pattern — YAML frontmatter, markdown body, relationships, statuses — applies at every scale: to data instances, to domain specifications, to the framework's own definitions.

This is a fractal property. In nature, fractals are patterns that recur at every level of magnification — the same structure whether you look at the whole or any part. This framework has the same quality: a thing is a thing whether it's a task in your life manager, a compliance pattern in your regulatory domain, or a specification that defines how things work.

This is not a requirement imposed on domain builders. It is a property of managed domain knowledge: instances and the definitions that govern them can both be structured, linked, validated, and reasoned about as things. Executable code, configuration, evidence, and release artifacts retain the formats appropriate to their own boundaries.

The implications:

- A framework that can define itself demonstrates reflexivity and exposes gaps under its own rules; it does not prove universality
- Managed knowledge follows the same rules at both framework and domain levels; implementation and distribution artifacts have explicit separate boundaries
- An LLM can reason about the system and about itself within the system using the same skills
- Evolution of the framework is tracked, validated, and auditable just like evolution of domain data

## How It Works In Practice

1. **Define your domain** — Create an AGENTS.md at root that orchestrates how the LLM interacts with your domain. Create skills that define your domain's philosophy, read/write patterns, and workflows.

2. **Define your atomic unit** — Reference thing.md to understand how things are structured. Create domain-specific thing types with appropriate metadata.

3. **Create instances** — Your actual data lives as thing files in `things/`. Each file is an instance of your atomic unit, with YAML metadata and narrative body.

4. **Interact through any route** — Speak, type, or otherwise communicate your intent through any file-aware route (editor, CLI, voice-to-text, or an explicit bootstrap). The harness delivers the domain's entry contract directly, through a pointer, or by emission; automatic discovery is a measured product capability, not a universal premise.

5. **Let it flow** — The agent produces things (persistent state) and deliverables (documents, code, images, notifications) depending on what you need. Updates flow back through your output route.

6. **Commit at meaningful boundaries** — Each state change is committed with a structured message. Git log becomes your domain's event narrative. Triggers evaluate against committed history.

7. **Iterate** — The loop repeats. Definitions evolve. Schema grows. Triggers catch what needs attention. The system becomes more sophisticated while remaining transparent.

Git preserves what was committed. You have an inspectable history of accepted
state, not a complete trace of unrecorded reasoning or external reality.

## What This Enables

**User agency.** You define your system. You're not locked into someone else's design choices. You can fork and modify anything.

**Portability.** Your data is plain files that can be moved and inspected widely. File-aware LLMs and tools are compatibility candidates; named build evidence decides which discovery and lifecycle routes actually work.

**Composability.** Multiple domains can coexist — they're all just files under one framework. Within a domain, things compose freely. *Across* domains, composition is deliberate, not implicit: domains are isolated, separate-id-space repos by design, so one domain consuming another's output is a verified hand-off (treated as external input — quarantined until confirmed, see `provenance.md`), not a raw cross-repo link. The full mechanism shipped in v3.22–v3.23: a domain serves a *face* (`exposed: true` things, graph stripped on egress) over the porch (`mdllm mcp-serve`); the consumer mirrors, pins with the reference triple, and quarantines until a human flips; `mdllm imports-check` keeps every pin honest (`fresh`/`stale`/`diverged`/`withdrawn`). See `provenance.md` and `interface.md` → The Membrane.

**Evolution.** You're not stuck with your initial design. The schema evolves. Fields emerge. Relationships change. Git preserves the history.

**Collaboration.** If multiple people need to work within the system, git's collaboration tools work naturally. Merge, branch, resolve conflicts using standard git workflows.

**Auditing.** Accepted state is versioned in git: structured commit messages capture recorded intent and `git diff` captures exact modifications; decision things can pin declared inputs. Together these provide an inspectable accepted-state trail. They do not expose vendor-model internals, recover reasoning that was never recorded, or prevent context from being lost before it is committed.

## Corollary: Elegant Constraint Enables Efficiency

There's a common assumption in the LLM space: bigger models are always better. More parameters, more tokens, more compute.

But this pattern inverts that thinking.

When you provide a smaller LLM with a clearly defined domain, explicit rules, structured data, and specific instructions, you're not asking it to figure out the problem space and solve within it simultaneously. You're asking it to read markdown, understand relationships, and apply straightforward reasoning within constraints that are already defined.

That's fundamentally different from asking a model to invent the system and reason within it at the same time.

A smaller model—one that costs less, runs faster, and produces lower latency—may handle some complex systems effectively when the domain is well-defined. The structure can reduce how much of the problem space the model must infer, but it does not guarantee adherence or eliminate the need for discriminating evaluation.

This has profound implications:

**Cost.** Smaller models are cheaper to run. A well-designed system may need less frontier-level reasoning, but the required capability is an empirical property of the task.

**Speed.** Smaller models are faster. On a phone, in a real-time application, latency matters. A smaller model that gives you 95% of what you need in half the time is often better than a larger model that's slower.

**Reliability.** Explicit constraints reduce ambiguity and create more checkable outcomes. The model still interprets and can ignore or misapply them; the floor catches only the failures expressed as mechanical invariants.

**Accessibility.** Not everyone needs or can afford the most powerful models. A well-designed system using a smaller model is more accessible to more people.

**Sustainability.** Less compute means less power consumption. It's better for the environment and your infrastructure costs.

This corollary follows from the thesis. If the structure carries the domain's definition, explicit rules, and state, the processor is not asked to invent the system and reason within it at once — so a smaller, cheaper, faster model can do work an unstructured larger model cannot do reliably. **Elegant constraint can substitute for raw capability.** But this is a corollary about efficiency, not the spine — and it must not be mistaken for the central claim.

Three claims must be kept apart, because the framework has different evidence for each:

- **The thesis — partially evidenced.** That structure gives a reasoning processor stronger consistency, auditability, integrity, and drift-resistance is the central claim. The mechanical half is demonstrated for the floor's enumerated checks when the active commit boundary runs; its self-test suite exercises those checks. The longitudinal half — that a structured domain resists and corrects drift *across many sessions* where an unstructured one rots — is designed but not yet measured by a multi-session eval. Claim it as far as the floor and exact harness evidence reach; no further.
- **Utility — evidenced on named use surfaces.** The framework is in production use across live domains and hosts its own development as a domain. That demonstrates practical value and reflexivity. Cross-session and cross-vendor consistency claims remain bounded to the recorded domains, fixtures, harnesses, and builds that earned them.
- **Model-tier superiority — a secondary, still-open hypothesis.** That a *smaller* model with structure beats a *larger* one without it is the efficiency corollary above — and its general form is already well-supported in the broader literature, so re-proving it adds little. The framework's own test of it rests on one eval (2026-06-11, `evals/README.md`) whose reasoning core *saturated*: the task separated the conditions only on cost and determinism, not reasoning quality. It stays untested until a harder, non-saturating fixture exists. Do not cite it as proven.

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

- **Evidence of reflexivity** — Representing itself exercises the same managed-knowledge pattern and reveals gaps; it does not prove the pattern represents every domain.
- **Dogfooding** — The framework subjects its own managed specifications and plans to its thing rules. Code, configuration, evidence, and release artifacts keep separate, explicit formats.
- **Agent-navigable** — The framework's own AGENTS.md lets an LLM reason about the framework itself — understanding which specs exist, how they relate, which are mature, which are drafts.
- **No hidden exemption for managed knowledge** — Framework specifications follow the same thing rules they define; other artifact classes declare their own boundaries rather than being mislabeled as things.

This is the philosophical endpoint of definition-driven systems: the system that defines itself, manages itself, and evolves itself — with a human directing and an LLM reasoning.

## Getting Started

If you want to build a system using this pattern:

1. **Start small.** Pick a domain you care about. Define it clearly.

2. **Create your AGENTS.md.** This is where you design how the agent should behave within your domain — what skills it loads, what reasoning patterns it follows, what constraints it operates within. Configure or verify the harness route that delivers it; automatic discovery is a measured capability, not a universal assumption.

3. **Create your skills.** Specification (philosophy), read (how to analyse), write (how to modify), workflow (process patterns). These are the agent's expertise for your domain — the guidance that makes it reason consistently and well.

4. **Create a few things.** Your actual data. Show the system what you mean by concrete instances with frontmatter and narrative.

5. **Interact.** Through whatever route works — VS Code, CLI, voice, mobile. The agent loads, skills guide reasoning, things provide context. You direct; the agent executes.

6. **Use the output. Provide feedback.** This is not a one-shot generation. You use what the agent produces. You come back with refinements. You say "this workflow needs another step" or "this thing type should capture X." The system grows through this loop.

7. **Commit meaningfully.** Each state change gets a structured commit. Git becomes your domain's event stream and audit trail.

8. **Iterate and share.** Your definitions will evolve. Skills refine. Thing types mature. Workflows adapt. Document the journey. Once you've built something useful, share it — others can fork and adapt for their own domains.

This is one way of building systems: sometimes alongside code, databases, and integrations, and sometimes without them. Its distinctive material is clear thinking, structured definitions, deterministic structural boundaries, and an ongoing partnership between human direction and probabilistic machine reasoning.
