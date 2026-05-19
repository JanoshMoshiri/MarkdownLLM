# Work Log

This file is a running record of work done, decisions made, and work remaining. It is updated at the end of every session. It serves both as a progress tracker and as a historical record for retrospective reflection.

---

## 19 May 2026

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
