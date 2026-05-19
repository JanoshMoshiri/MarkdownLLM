---
id: framework-worklog
type: artifact
status: evolving
version: 2.1
created: 2026-05-13
linked_things:
  - id: llm-driven-systems-manifesto
    relation: documents
  - id: thing-specification
    relation: documents
  - id: read-thing-specification
    relation: documents
  - id: write-thing-specification
    relation: documents
  - id: validate-thing-skill
    relation: documents
  - id: git-workflow-specification
    relation: documents
  - id: interface-specification
    relation: documents
  - id: framework-discovery-specification
    relation: documents
  - id: scalability-guide
    relation: documents
  - id: domain-specification-guide
    relation: documents
---

# Framework Work Log

This file is a running record of work done, decisions made, and work remaining. It is updated at the end of every session. It serves both as a progress tracker and as a historical record for retrospective reflection.

---

## 19 May 2026

### Session 5

#### Completed

- [x] Reviewed all Session 4 (independent review) findings and produced a detailed prioritised plan across 5 priority levels
- [x] Analysed README in full detail — identified 8 specific structural problems with precise line references and rationale for each
- [x] Implemented all 8 README fixes in a single editing pass:
  - Removed placeholder license section (template residue, never filled in)
  - Fixed MIT + "All rights reserved" legal contradiction — removed the phrase
  - Consolidated two Contributing sections into a single pointer to CONTRIBUTING.md
  - Deleted three orphaned application description blocks (Financial Tracking, Health & Fitness, Creative Writing) — no parent heading, no matching example domains in repo
  - Removed second Getting Started sequence and third "Start here:" footer — single on-ramp now
  - Removed duplicate "How This Works With LLMs" and "Elegant Constraint Enables Efficiency" sections — the canonical "The Elegant Constraint" section (added Session 3) already makes the argument better
  - Removed "Using This Framework" (Personal/Team/Org) — unproven scale claims and a vendor-specific "Interact with Claude" reference violating Principle 5
  - Softened FAQ "production-ready" answer to honestly reflect the draft/stable status spread in frontmatter
- [x] Committed per git-workflow.md conventions: `framework: clean README — remove structural debt from independent review`
- [x] Added CONTRIBUTING.md guidelines: per-file versioning note and frozen naming conventions
- [x] Committed: `framework: update CONTRIBUTING — versioning note and frozen naming conventions`
- [x] Reviewed and calibrated CHANGELOG.md tone across all release entries:
  - Removed "no architectural gaps" claim from 2.1.0 (specs carry `status: draft`)
  - Dropped "Operational Excellence" title from 2.2.0 — factual description instead
  - Dropped "Major Additions" from 2.1.0 — additions speak for themselves
  - Acknowledged draft status in 2.1.0 "Why This Matters" section
  - Softened vendor alignment claims in 2.0.0 ("follows similar patterns" not "mirrors")
  - Trimmed stale "Coming Soon" to genuinely planned items; renamed to "Planned"
- [x] Committed: `framework: calibrate CHANGELOG tone — align confidence with actual spec maturity`

#### Decisions Made

- README editing worked from the bottom up to keep line references stable — removed the entire tail section in one replacement, then handled the FAQ independently
- The "Using This Framework" scale section (Personal/Team/Org) was removed entirely rather than trimmed — the scale claims are not backed by any example or specification in the repo, and the vendor-specific reference was a Principle 5 violation. No version of it was worth keeping.
- Contributing section now delegates to CONTRIBUTING.md rather than duplicating guidance — single source of truth for contribution process
- All 8 README changes landed in a single commit with a detailed body listing each change — this is one logical unit of work (README structural cleanup) even though it touched many lines

#### Reflections

- The README had accumulated ~130 lines of duplicate and abandoned content — 28% of the file. This is a normal consequence of iterative writing without a cleanup pass. The independent review was the right trigger for this.
- Having a detailed plan before editing made the implementation fast and confident — no second-guessing which sections to keep.

#### To Do (Remaining from Session 4 Review)

- [x] CONTRIBUTING.md: add versioning note (independent versioning is intentional, not inconsistency)
- [x] CONTRIBUTING.md: state naming conventions are frozen
- [ ] validate.thing.skill.md: add validation honesty paragraph (LLM-performed, not deterministic)
- [ ] scalability-guide.md: add cost/performance honesty section (tiered loading reduces but doesn't eliminate cost)
- [x] CHANGELOG.md: tone calibration on "Unreleased" and 2.2.0 sections
- [ ] New: limitations.md — when not to use this framework
- [ ] New: comparison/differentiation section or document
- [ ] New: schema migration mechanics
- [ ] Proof: end-to-end worked example with real token/time data
- [ ] Proof: populate life-manager with 12-15 real, messy, interlinked things

### Session 3

#### Completed

- [x] Full framework review against manifesto principles — all 5 core principles and 2 meta-principles verified as honoured. No violations found.
- [x] Added "The Elegant Constraint" section to README.md — the structure-beats-scale argument is now front and centre, not buried in session notes
- [x] Reworked scalability-guide.md "neural network analogy" section — replaced with actionable "Attention Through Abstraction" section: three concrete rules (match depth to scope, let agent choose level, compress completed work) instead of extended analogy
- [x] Reframed interface.md deliverables section — clarified that the framework holds structure/state; the LLM generates deliverables. Removed visual/audio/video rows that implied the framework produces output. Added explicit statement that output capability depends on the LLM, not the framework.

#### Decisions Made

- "Elegant constraint" is a key differentiator and belongs in the README, not just in session notes — it's the strongest argument for why someone would adopt this framework over unstructured prompting
- Neural network analogy in scalability guide was trimmed to a direct, actionable section — the philosophical depth was valuable during design but the guide should be practical for adopters
- Interface deliverables reframing: the framework defines the system the LLM operates within; it does not itself produce deliverables. This is an important distinction for how the framework is understood externally.

#### To Investigate / Future Work

- **Quickstart guide (QUICKSTART.md)** — A 5-minute on-ramp: clone, create 3 files, interact with agent, see it work. The domain-specification-guide is comprehensive but too dense for first contact. A quickstart that gets someone to a working domain in minutes would dramatically improve adoption.
- **Non-trivial worked example** — The compliance-patterns example has 2 things; life-manager has zero. Neither demonstrates triggers firing, validation catching errors, or git workflow in action. Need an example with 10-15 things showing relationships, triggers, validation, and a session narrative proving the system works end-to-end.
- **Multi-agent / multi-domain patterns** — What happens when domains share things or one agent's output feeds another agent's input? ProducFlow2 hints at this (domain inside framework repo) but there's no specification for domain composition.
- **Migration / evolution strategy** — The manifesto says schemas evolve but there's no concrete guidance for: adding a required field to an existing domain, migrating N things, upgrade paths. This becomes critical once domains grow beyond trivial size.
- **Security and access control** — Any domain with sensitive data (compliance, financial, health) needs guidance on: who can read/write things, secrets handling, PII in git-committed files.
- **Reasoning lenses placement** — Currently embedded in read.thing.md and write.thing.md as optional sections. Only the compliance domain naturally uses them. Worth investigating whether these should move to an advanced patterns appendix to reduce cognitive load in the core read/write specs, or whether they earn their place as domains mature.

#### Reflections

- The framework is internally consistent at v2.2. The gaps are operational (on-ramp, proof, composition) not architectural. Nothing needs restructuring.
- The "elegant constraint" argument — that structure beats scale, and a well-defined domain makes a small model outperform a large unstructured one — is the framework's strongest selling point and wasn't visible in the README until now.
- The interface spec's deliverables section was subtly misframing the framework's responsibility. The framework doesn't generate output; it provides the structure that makes the LLM's output reliable. This distinction matters for how adopters understand what they're building.

### Session 4 — Independent Review Integration

**Context:** This session captures the findings of a full comprehensive review conducted by an independent agent in a separate session (no access to this AGENTS.md or WORKLOG). The review is logged here as a normal session entry per framework convention. No implementation work was done in this session — findings are recorded as todos.

#### Completed

- [x] Received and read full independent review of the MarkdownLLM v2.1 framework
- [x] Extracted all identified gaps and action items into the todo list below
- [x] Noted reviewer corrections to previous under-credits (validation, concurrency, commit discipline, triggers, discovery) — no action required; these were already addressed in prior sessions

#### Decisions Made

- Independent reviews conducted outside this agent's session context are still recorded here as normal sessions — the WORKLOG is the intent record regardless of where the work originated
- Review findings are treated as authoritative input; the distinction between "gaps in spec" and "gaps in presentation/proof" is adopted from the reviewer's framing

#### To Do — From Independent Review

**Priority 1 — Presentation integrity (high credibility impact, fast to fix)**

- [ ] **README reconciliation** — Remove the duplicate `## License` section (the one with unfilled placeholder text `[Your chosen license…]`); resolve the "MIT License … All rights reserved" contradiction (MIT and "all rights reserved" are mutually exclusive); remove the duplicate `## Contributing` section; remove the three orphaned application description paragraphs (Financial Tracking, Health & Fitness, Creative Writing) that appear after the FAQ with no parent heading; consolidate the two "Getting Started" sequences into one
- [ ] **README: production-ready vs. draft contradiction** — README FAQ claims "the framework… is production-ready"; half the foundational specs carry `status: draft` in their own frontmatter. Trust the frontmatter. Soften the README claim to reflect that the architecture is proven but the specs are still maturing.
- [ ] **CHANGELOG tone calibration** — The "Unreleased" tone reads as more triumphant than a v2.x draft-status framework warrants ("the framework now has no architectural gaps"). Align the changelog's prose confidence level with the actual frontmatter status values of the specs it describes.

**Priority 2 — Honesty and transparency additions**

- [ ] **Validation honesty paragraph** — `validate.thing.skill.md` is detailed and rigorous, but every check is still LLM-performed, not deterministic. For the regulated domains the framework explicitly courts (compliance, law, finance, healthcare), one honest paragraph should be added: "Validation is LLM-performed; for high-assurance domains, pair with a deterministic CI check (a YAML/link linter is ~100 lines of Python) outside the framework." Thoroughness of the spec must not imply a stronger guarantee than the mechanism provides.
- [ ] **Cost/performance honesty** — Tiered loading is presented as the scaling answer, but even Level-1 metadata loading across 1,000 things is a large context payload. The scalability guide correctly notes 1,000+ "breaks" without tiering, but there is no measured sense of what a session costs in tokens/latency at a realistic size (e.g. 200 things). The framework's rejection of indexing/search on philosophical grounds is defensible — it should not be presented as cost-free.

**Priority 3 — Missing specifications**

- [ ] **Failure-mode / limitations document** — "When not to use this framework." Real-time systems, high-write-concurrency domains, anything requiring transactional guarantees, anything where LLM reasoning over full state is too slow or expensive. The manifesto's old "What This Is Not" gestured at this; there is no dedicated honest spec. A "don't use it for X" document is expected for any systems-design framework targeting adoption.
- [ ] **Comparison / differentiation section** — How is this different from: plain `AGENTS.md`/`CLAUDE.md` conventions; Obsidian-vault-plus-LLM; spec-driven tools like SpecKit; RAG over a markdown corpus? The differentiator is the `thing` spec + tiered loading + triggers + validation as a coherent whole — this should be stated explicitly. The markdown-as-LLM-state idea is actively converging with other tools; name the difference or readers will assume there isn't one.
- [ ] **Schema migration / evolution mechanics** — `write.thing.md` references `schema_version: 2.0` on things; the manifesto says schemas "emerge" — but there is no spec for what happens when a field is renamed or a new required field is added across hundreds of existing things. `domain-refresh.md` handles framework-version propagation to domains; it is not clear it handles data schema migration. If it does not, that is a gap.

**Priority 4 — Proof and demonstration**

- [ ] **End-to-end worked example** — The framework is entirely specification and static pattern examples. No transcript, no session recording, no "here's a real run: agent loaded, read 12 things, produced this, committed this, here's token count and wall-clock time." The "elegant constraint" claim (small model + structure beats large model without) is asserted in the manifesto and README, never demonstrated. One recorded end-to-end session — real domain, ~15 populated things, a query, the agent's reads, the writes, the commits, the token cost — converts this from "impressive design document" to "framework I'd trust." This may also address the prior session's todo on a non-trivial worked example.
- [ ] **Populate at least one example domain with 12–15 real, messy, interlinked instance things** — overlapping deadlines, broken dependencies, triggers mid-flight — to show the system under realistic load. The compliance pattern pair is good pedagogy; it is not proof the loop runs.

**Priority 5 — Housekeeping**

- [ ] **`.markdownllm` marker file** — Verify its contents match the `version: 2.1` declared in `AGENTS.md`. Listed in the repo file list but content alignment not confirmed.
- [ ] **CONTRIBUTING versioning note** — `AGENTS.md` is `version: 2.1`; some skills are `version: 2.0`; `validate.thing.skill.md` is `version: 1.0`. Independent versioning is a stated framework feature — add a one-line note in `CONTRIBUTING.md` so readers do not interpret the version spread as inconsistency.
- [ ] **Freeze naming conventions in CONTRIBUTING** — The naming conventions (`-specification`, `.thing.`, `.skill.md`) churned across v1.x → v2.x and each rename was a breaking change. The conventions have now stabilised — state explicitly in CONTRIBUTING that they are frozen going forward.

#### Reflections

- The reviewer's central verdict is accurate and matches prior session assessments: the architecture is sound, internally rigorous, and considerably more complete than a first skim suggests. The gaps are presentational and operational, not foundational.
- The two highest-leverage actions from the review are precisely the same two identified in previous sessions: (1) fix the README, (2) produce one real end-to-end demonstration. The independent confirmation strengthens the case for prioritising these.
- The framing of "proof vs. specification" is useful: the framework has more than enough specification; it has no proof. Any new spec work is lower leverage than one working example right now.

---

### Session 2

#### Completed

- [x] Updated all 5 templates to v2.1 patterns: AGENTS.md.template (triggers, validation, git commit, foundational specs), domain-specification.skill.md.template (added id, status, created, linked_things, validation rules, triggers), domain-read.thing.skill.md.template (`type: prompt` → `type: skill` with `mode: read`, full frontmatter, trigger awareness), domain-write.thing.skill.md.template (`type: prompt` → `type: skill` with `mode: write`, post-write validation, git commit, trigger evaluation), domain-workflow.skill.md.template (`type: workflow` → `type: skill` with `mode: workflow`, trigger integration, git commit points, validation checkpoints)
- [x] Updated life-manager example (5 files) to v2.1: AGENTS.md (triggers section, foundational specs, vendor-neutral language), specification skill (full frontmatter, validation rules, triggers), read skill (type: skill, mode: read, trigger awareness), write skill (post-write validation, git commit, trigger evaluation), workflow skill (trigger integration, git commit points)
- [x] Updated compliance-patterns example (6 files) to v2.1: AGENTS.md (triggers, foundational specs, validation checklist), specification skill (full frontmatter, validation rules), read skill (type: skill, mode: read), write skill (post-write validation, git commit), workflow skill (trigger integration, git commit points), both example things (added status: stable, linked_things with cross-references)
- [x] Updated domain-specification-guide.md inline code examples to v2.1: bumped to v2.1, added git-workflow and interface to linked_things, updated AGENTS.md template section, updated all skill frontmatter examples, updated thing creation example status values
- [x] Fixed manifesto stale reference: Principle 5 (Vendor Agnostic) `.instructions.md, .skill.md, .prompt.md` → `AGENTS.md, .skill.md, YAML frontmatter`
- [x] Verified zero remaining `type: prompt` references across entire workspace (grep confirmed)

#### Decisions Made

- All templates and examples updated in lockstep — ensures anyone bootstrapping a new domain from templates gets v2.1 patterns immediately
- Status values in thing creation example changed from `draft/active/complete` to `not-started/in-progress/blocked/paused/completed/cancelled` — aligns with the richer lifecycle model needed for real workflow tracking
- Vendor-neutral language enforced throughout — "Claude" references replaced with "LLM" in all examples to honour Principle 5

#### Reflections

*None recorded.*

### Session 1

#### Completed

- [x] Full review of entire MarkdownLLM 2.0 workspace — all core files, examples, templates, and changelog read end-to-end
- [x] Assessed cohesion of the framework — confirmed three-layer architecture (Agent → Skills → Things) is consistently applied across all documentation and examples
- [x] Identified and fixed minor inconsistencies: README referencing old `Instructions-guide.md` filename (now `domain-specification-guide.md`); `read.thing.md` and `write.thing.md` referencing old `[domain].instructions.md` naming (now `[domain]-specification.skill.md`)
- [x] Created WORKLOG.md in MarkdownLLM repo (this file), adopting the same day/session format proven in ProjectProd
- [x] Captured 10 identified gaps/areas for future work (see To Do and Decisions Made)

#### Decisions Made

- The interface layer is deliberately not specified as a new protocol — the framework leverages existing interface routes (VS Code + GitHub Copilot, Claude Code CLI, mobile chat apps, voice-to-text in OS) rather than inventing a new one. The interface section needs to be *described and defined* in the manifesto/README, not *built*.
- The output side of the framework is broader than just things — the agent can produce documents (Word, PDF), images, software code, videos, audio. This needs explicit documentation as a concept: things are the agent's persistent memory/state; outputs are the agent's deliverables produced from that state.
- WORKLOG adopted for this repo — serves as session history, progress tracker, and captures forward planning. Same format as ProjectProd worklog.
- The framework is cohesive and internally consistent at the specification level; the gaps are operational (how to deploy end-to-end) not architectural.
- The "elegant constraint" argument (smaller models + well-defined domains) is a key differentiator that should be promoted more prominently.

#### Reflections

- The framework has evolved significantly in 6 days (13 May → 19 May) from a single-domain tool to a generalised specification. The rate of iteration is high but the architectural decisions have been sound — the v1→v2 simplification (five components → three layers) was the right call and nothing in the current structure needs further restructuring.
- Having an independent reviewer read the entire workspace cold validated that the writing is clear and the concepts are coherent. The gaps identified are all forward-looking (operational concerns), not foundational.

---

## 15 May 2026

### Session 1

#### Completed

- [x] Reviewed manager conversation (Paul Hill, 14 May) in detail — extracted practical questions on prototype intake and environment
- [x] Identified Phase 0: Intake & Inception as a required precursor to Phase 1 Discovery
- [x] Named the root constraint missed in earlier analysis: prototype cannot touch firm infrastructure until productionised
- [x] Structured Phase 0 into two separate concerns: process design (the steps) and environment design (the infrastructure prerequisites)
- [x] Grouped Paul’s questions into four decision areas: execution environment; transfer and receipt; storage and collaboration; context and intent capture; dependency and cost

#### Decisions Made

- Phase 0: Intake & Inception is part of this process (same `.instructions.md`), not a separate framework — the outputs of Phase 0 (artefact in `Prototype/`, intent document) are what Phase 1 needs to begin
- The prototype cannot be run on firm infrastructure at any stage before productionisation — this is the root constraint driving all intake design decisions
- Static analysis (reading code, configs, architecture) can happen on a firm machine; dynamic analysis (running the prototype) requires an isolated machine with no firm network access
- Environment decisions are infrastructure prerequisites, not process steps — they belong in a separate project-level document once decided
- The next step is a decision register: turn Paul’s open questions into structured decision items before Phase 0 can be written into `.instructions.md`

#### Reflections

*None recorded.*

### Session 2

#### Completed

- [x] Created `DECISIONS.md` — Phase 0 decision register with 8 structured decision areas, root constraint stated, summary table
- [x] Decided Decision 1 (Execution environment): dedicated sandbox physical machine — strong isolation, analyst-controlled, no firm credentials or network
- [x] Decided Decision 2 (Transfer and receipt): private externally-hosted git repository — clean audit trail, developer-familiar workflow, satisfies root constraint
- [x] Decided Decision 3 (Prototype storage): prototype stays on sandbox; analysis outputs stored in a separate external analysis repository and brought into firm infrastructure on completion
- [x] Identified Decision 3 needed splitting — original "storage and collaboration" conflated prototype storage, analysis repo structure, and cross-analyst coordination
- [x] Added Decision 4 (Analysis repository structure, ownership, lifecycle) — open questions on repo count, ownership model, and data retention implications
- [x] Added Decision 5 (Cross-analyst collaboration model) — branch strategy and coordination between two analysts on same prototype
- [x] Added Decision 6 (External party collaboration) — Teams site for creator collaboration; noted firm already uses B2B guest access pattern
- [x] Renumbered original Decisions 4–5 to Decisions 7–8 to accommodate new decisions
- [x] Identified previously unconsidered factors: repo ownership and analyst-departure continuity; data retention obligations for analysis outputs on external repos; Teams conversation history as a retention-liable record; IP and confidentiality of externally-developed prototype code; who creates and owns the prototype repo in Decision 2

#### Decisions Made

- Prototype artefacts stay on the sandbox; analysis outputs are the product of analyst work and can return to firm infrastructure once analysis is complete
- Decision 3 is three concerns, not one: storage (resolved), repository structure (Decision 4), cross-analyst coordination (Decision 5) — these have distinct ownership and lifecycle questions
- Firm B2B guest access in Teams (already standard practice for external clients) is the likely pattern for external creator collaboration — data stays in firm tenant; this is firm infrastructure but in a governed way, which is acceptable for communication
- The Teams collaboration channel and the context/intent capture decision (Decision 7) are linked — the intent capture artefact may naturally emerge from the Teams conversation rather than being a separate step

#### Reflections

*None recorded.*

---

## 14 May 2026

### Session 1

#### Completed

- [x] Reviewed conversation insights on customisation file layering, agent files, and hooks
- [x] Established creation order principle: instructions → prompts → skills → agent files (agent file is the framing layer, built last)
- [x] Documented agent file considerations: coherence, over-generalisation, persona consistency, scope control, adaptability
- [x] Documented hooks governance: complexity, maintenance, reliability, timing
- [x] Amended `customisation-governance.instructions.md` — added Creation Order principle, Hooks Governance section, updated File Boundary Definitions table to include agent files and hooks
- [x] Created `.github/prompts/create-agent.prompt.md` — pre-flight checklist for agent files, mirrors `create-skill.prompt.md`

#### Decisions Made

- Agent files are the framing layer and should be crafted after the components they orchestrate (instructions, prompts, skills) are defined
- Hooks governance is documented proactively in the governance file so considerations are encoded before hooks are adopted
- `create-agent.prompt.md` is a governance checklist (like `create-skill.prompt.md`), not a speculative skill — governance can be proactive, methodology cannot
- Agent file considerations and hooks considerations originate from a voice session conversation — encoded here rather than left only in conversation

#### Reflections

*None recorded.*

### Session 2

#### Completed

- [x] Added outcome-first principle (Check 0) to `create-agent.prompt.md` — outcome and verifiability as prerequisite before any file is written
- [x] Updated creation order in `customisation-governance.instructions.md` to begin with outcome definition
- [x] Developed hook evaluation rubric (four filters) and encoded in Hooks Governance section
- [x] Updated layered loading section — hooks positioned alongside the context stack, not within it
- [x] Restructured Hooks Governance — evaluation rubric added, risks separated under sub-heading, "not yet adopted" note removed
- [x] Updated governance file boundary table to list all current files by exact path
- [x] Created `.github/hooks/post-encoding-commit.hook.md` — git commit hook with no-push rule and graceful failure
- [x] Created `.github/prompts/end-session.prompt.md` — WORKLOG update prompt (to be renamed `update-worklog.prompt.md`)
- [x] Renamed `new-session.prompt.md` → `start-session.prompt.md`
- [x] Updated `start-session.prompt.md` Step 3 to reference end-session prompt and commit hook
- [x] Updated README to reflect current `.github/` structure
- [x] Committed interim framework changes
- [x] Restructured WORKLOG to day → session hierarchy
- [x] Renamed `end-session.prompt.md` → `update-worklog.prompt.md` and updated all references
- [x] Created `.github/hooks/pre-commit-validate.hook.md` — structural validation with four checks (file registration, prompt/hook/instructions frontmatter)
- [x] Created `.github/prompts/review-governance.prompt.md` — qualitative governance review covering all eight governing principles
- [x] Updated `post-encoding-commit.hook.md` — added pre-commit sequence: validate → governance review checkpoint → commit
- [x] Updated governance table and README to include pre-commit-validate and review-governance
- [x] Ran governance review — framework compliant; two monitoring notes recorded
- [x] Fixed `update-worklog.prompt.md` — template and determining-block logic updated to match new day/session WORKLOG format
- [x] Tested post-encoding-commit hook sequence in practice (first real execution)
- [x] Reviewed meeting analysis with manager (Paul Hill) — identified prerequisite process gap: the front-of-process (how a prototype lands in the analysis environment) is not yet designed and is the first place reality will break the framework

#### Decisions Made

- Hook evaluation rubric — four filters: side effect not the work; trigger named and precise; fails gracefully; human review not required
- Hooks operate alongside the context stack, not within it — different axis: what executes unconditionally at trigger points vs what is in context
- WORKLOG update is a prompt (not a hook) — it is the primary work of the update action, not a side effect, and requires human review before committing
- Git commit is the true hook — passes all four filters; side effect of encoding, well-defined trigger, graceful failure, no additional review needed at that point
- post-encoding-commit should not chain to WORKLOG update — start-session's WORKLOG read is the natural validation; no hard block needed in the commit hook
- `end-session.prompt.md` to be renamed `update-worklog.prompt.md` — responsibility is WORKLOG update, not session lifecycle management
- WORKLOG format: day as top-level (`## D MMM YYYY`), sessions as sub-sections (`### Session N`, resetting per day), sub-sections at `####` level
- pre-commit-validate is a hook (mechanical checks, no judgement needed, passes all four filters); governance review is a prompt (requires judgement, must remain a deliberate human action)
- post-encoding-commit now orchestrates a pre-commit sequence — this places it at the Open/Closed boundary; if the sequence grows, extract to a commit-protocol prompt
- Governance review is a checkpoint not a blocker — the commit can proceed whether or not review has been run, but the question must be asked and answered each time
- Next session focus is the prerequisite process — how a prototype moves from its origin (personal machine, external context, recording, partial artefact) into the analysis environment safely; this precedes Phase 1 (Discovery) and may be a new phase, a separate process, or an intake checklist; Paul's framing from the meeting makes clear this is the first real bottleneck and the place the workflow will break in practice if not designed

#### Reflections

*None recorded.*

---

## 13 May 2026

### Session 1

#### Completed

- [x] Explored the prototype-to-production analysis concept and defined the problem space
- [x] Read and understood the Reverb prototype (Phase 1 Discovery completed informally)
- [x] Read the Service Configuration Document template — understood its structure and scope
- [x] Defined the five-phase analysis process (Discovery → Data Flow → Gap Analysis → Production Design → SCD Population)
- [x] Established the priority ordering: Security → Vulnerability → Architecture, applied within and across all phases
- [x] Decided on instructions + prompt + skills architecture for encoding the process
- [x] Created `.instructions.md` — analysis process, firm constraints, phase definitions, SOLID principles in Phase 4
- [x] Created `.github/instructions/customisation-governance.instructions.md` — firm vs project level distinction, layered loading, progressive extraction, single responsibility, versioning, create vs amend rules
- [x] Created `.github/prompts/prototype-analysis.prompt.md` — entry point for running the analysis
- [x] Created `.github/prompts/create-skill.prompt.md` — pre-flight checklist for creating skills
- [x] Created `.github/prompts/new-session.prompt.md` — session orientation protocol
- [x] Created `README.md` — framework overview written from generic, reusable perspective
- [x] Created `.gitignore` — excludes `Prototype/` from version control
- [x] Moved Reverb prototype and SCD template into `Prototype/` folder
- [x] Initialised git repository
- [x] Created remote repository at burgessalmon.ghe.com/Technology/ProjectProd and pushed
- [x] Created `WORKLOG.md` (this file)

#### Decisions Made

- SCD is an output of the process, not an input — populate only after production solution is built and tested
- `Prototype/` is gitignored — working material, not part of the committed framework
- Firm-level content (constraints, governance) separates from project-level content (analysis findings)
- Skills are extracted from proven work, never written speculatively
- SOLID and clean architecture are named evaluation criteria in Phase 4, not background assumptions

#### Reflections

*None recorded.*

---

## To Do

### Framework Gaps (Identified 19 May)

- [x] Document the interface layer — describe how users connect to their agent (VS Code + Copilot, Claude Code CLI, mobile chat, voice-to-text) and clarify that the framework uses existing routes, not a new protocol *(done: interface.md created in v2.1)*
- [x] Document the output layer — things are persistent state; outputs (documents, images, code, video, audio) are deliverables the agent produces from that state. Define this distinction explicitly. *(done: interface.md, things vs deliverables section)*
- [x] Define a trigger/event system — optional fields or patterns for automated re-evaluation (due date passed, dependency resolved, status changed) *(done: triggers section in thing.md, v2.1)*
- [x] Specify the git workflow — commit message conventions, who commits (human vs LLM), branching strategy, PR vs direct-to-main, conflict handling *(done: git-workflow.md created in v2.1)*
- [ ] Address referential integrity — what happens when a thing is deleted or renamed; detection and repair of broken `linked_things` references
- [x] Create a validation/linting specification — schema validation for thing files (required fields present, valid status values, link integrity) *(done: validate.thing.skill.md created in v2.1)*
- [ ] Address context budget vs small model claim — skill compression or inline summaries for constrained-context deployments where 8K-16K tokens is the limit
- [ ] Document concurrency/multi-agent patterns — what happens when two LLM sessions operate on the same domain simultaneously; semantic conflict resolution beyond git merge
- [ ] Define a testing/verification approach for skills — how domain authors verify their skills produce intended behavior
- [ ] Document migration strategy — how to upgrade existing thing files when schema evolves (new required fields, renamed types, restructured relationships)
- [ ] Add security and access control section — acknowledge gap between documented intent (access_control metadata) and enforcement; point toward solutions
- [ ] Add a third example domain — knowledge base or product backlog to further prove the generalisation claim

### Framework Development

- [ ] Add dynamic input variable to `prototype-analysis.prompt.md` for cases where multiple prototypes exist in `Prototype/`
- [ ] Delete personal repo at burgessalmon.ghe.com/Janosh-Moshiri/ProjectProd (no longer needed)
- [ ] Consider migrating firm-level constraints and governance to user-level storage when stable (available across all workspaces)
- [ ] Extract Phase 2 (Data Flow & Security Classification) into a skill once methodology is proven through at least one real execution
- [ ] Extract Phase 3 (Gap Analysis) into a skill once methodology is proven
- [ ] Extract Phase 4 (Production Architecture & Design) into a skill once methodology is proven
- [x] Evaluate whether hooks are useful for enforcing encoding discipline at session end
- [ ] Monitor `post-encoding-commit.hook.md` on next change — if pre-commit sequence grows further, extract orchestration to a commit-protocol prompt (Open/Closed boundary noted in governance review 14 May)
- [x] Create Phase 0 decision register — resolve open questions on execution environment, transfer mechanism, storage, context capture, and dependency handling *(done: all 8 decisions locked, encoded in ProducFlow2 domain)*
- [x] Design prerequisite process — how prototypes are received, transferred, and prepared for analysis *(done: producflow-environment.skill.md created with full Phase 0 workflow)*

### Prototype Analysis — Reverb

- [ ] Phase 2: Data Flow & Security Classification — execute formally against Reverb
- [ ] Phase 3: Gap Analysis — produce gap register for Reverb
- [ ] Phase 4: Production Architecture & Design — design production solution for Reverb
- [ ] Phase 5: SCD Population — populate Service Configuration Document (after production solution is built and tested)

---

## Format Guide

When updating this file:

- **Day blocks** (`## D MMM YYYY`) — one per calendar day. All sessions within a day fall under the same day block. Add a new day block at the top of the history when starting work on a new calendar day.
- **Session blocks** (`### Session N`) — one per discrete working session within a day. N resets to 1 each day. Each session gets its own sub-block.
- **Sub-sections** (`####`) — each session block contains: Completed, Decisions Made, Reflections.
  - **Completed** — `- [x]` per distinct piece of work. Be specific.
  - **Decisions Made** — prose sentences. What was decided and why, not just what was done.
  - **Reflections** — retrospective observations after time has passed. If it belongs in the record immediately, it goes in Decisions Made, not Reflections.
- **To Do** — managed in the `## To Do` section, not within session blocks. Mark items `[x]` when completed; add new items under the relevant heading.
- Do not delete old entries — this is a historical record, not a clean task list.
