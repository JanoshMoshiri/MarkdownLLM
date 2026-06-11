# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Format Change (from v2.3.0 onwards)

Prior entries followed [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) with detailed per-feature breakdowns. From v2.3.0, the changelog adopts a **per-push** format:

- **Each entry corresponds to a push to the remote** — the moment changes land on main in the public repo
- **Entries are concise summaries**, not exhaustive lists — the WORKLOG holds session-level detail
- **Version numbers are incremented per push** (patch for fixes/consistency, minor for new specs or behavioural changes, major for breaking changes)

The WORKLOG is the detailed internal record. The CHANGELOG is the external-facing record of what shipped.

**From v3.0.0 onwards, entries are generated, not hand-written:** draft with `python tools/mdllm.py changelog --since <last-version-tag>`, then set the version, add the one-paragraph summary, prune noise, and commit. Hand-maintaining a surface derivable from the commit stream was one of the drift sources the deletion pass (transformation plan Phase 2) removed.

---

## [3.4.0] - 2026-06-11

**The floor verifies itself.** A comprehensive review found the gaps concentrated where the framework trusted itself without verification — all closed this release. The version sentinel (`.markdownllm`) had silently stayed at 3.0 since v3.1, disarming domain refresh; it is re-synced and `mdllm validate` now enforces sentinel / AGENTS.md / CHANGELOG agreement as an Error, so the pre-commit hook blocks any future drift. The tool itself gains a 30-test pytest suite (run first in CI), `mdllm kernel --check` gates kernel drift, and `provenance` joins the default `index check` signals. Eval Stage 2 hardened ahead of the 2×2 experiment: the bare condition no longer sees the framework checkout, timeouts record as failed trials, numeric-string field values coerce before failing, and `eval --report` aggregates runs into the per-cell table (fairness caveat documented). Domain scaffolding catches up to v3: guide v2.7 adds the deterministic-floor section and `templates/_schema.yaml.template` ships.

---

## [3.3.0] - 2026-06-11

**Eval Stage 2 — the model experiment is runnable.** `mdllm eval --run` seeds an isolated git workspace from a fixture's `seed/`, invokes a fresh headless agent (`claude -p`, json output → score/cost/time/turns per trial), and asserts the result. `--bare` strips AGENTS.md/skills/schema for the no-framework condition; `--trials N` for repeats. First fixture: `evals/vat-quarter-basic.yaml` — a synthetic VAT quarter with known-correct figures and a blocked-entertainment-VAT discriminator. The 2×2 structure-beats-scale protocol (haiku/opus × framework/bare) is documented in `evals/README.md`. Verified: negative test, dry-run seeding both conditions; live agent path untested pending `claude` CLI availability.

Also (v3.2.1 review pass): `mdllm tokens` re-tiered to kernel reality (Tier 0 measured 5,592 tokens); README updated to describe the deterministic floor and provenance to the public.

---

## [3.2.0] - 2026-06-11

Transformation plan Phases 2–7 (same day as 3.0.0; drafted with `mdllm changelog`). The framework now has provenance, a 93%-smaller operative kernel, deterministic evals, and proactive adapters.

**Deletion pass (Phase 2):** REVIEWLOG migrated into `framework-retrospective-2026-05` and deleted; CHANGELOG entries now drafted by `mdllm changelog`; speculative trigger machinery pruned (`trigger-specification.md` v1.2).

**Provenance (Phase 3):** `provenance.md` (draft) — `type: decision` records with inputs pinned to commits via `informed_by`; `origin: external` + `verified` quarantine for ingested content; `mdllm provenance` enforcement; reverse-provenance derived index; first real decision record committed (`decision-status-vocabulary-domain-owned`). `thing.md` v2.12.

**Session memory (Phase 4):** scoped insight-staleness check at session start (`session-memory.md` v1.1, `session-orientation` prompt v1.1) — live insights × things changed since the brief's `last_updated`; the full sweep stays at retrospective.

**Operative kernel (Phase 5):** `<!-- kernel -->` blocks in the six Tier 0/1 specs, extracted by `mdllm kernel` into a generated `kernel.md` — measured 1.6k tokens replacing 21.4k of full specs. Tier 0 session cost: 26.5k → ~5.3k.

**Evals (Phase 6, Stage 1):** `mdllm eval --fixture` deterministic assertion engine; `evals/` with the first fixture passing 6/6 against the live jmtm domain as a regression net.

**Adapters (Phase 7):** GitHub Actions workflow (validate + provenance + index drift on every push); `adapters/scheduled-triggers.ps1` (proactive deadline surfacing via Task Scheduler); Claude Code PostToolUse adapter example.

---

## [3.0.0] - 2026-06-11

**The Deterministic Floor.** Major version: mechanical validation moves from LLM honor-system to code, and domains now own their status vocabularies. Driven by the 2026-06-11 full review finding that all 17 things in the live jmtm-software domain violated the Level 1 status rule at Error severity, undetected.

**New tooling:**
- `tools/mdllm.py` — single-file CLI (Python, PyYAML): `validate` (structural + referential + schema checks, exit 1 on Errors), `triggers` (mechanical evaluation of time/dependency/threshold conditions + deadline horizon), `index check|rebuild` (derived-index rebuild-and-diff), `tokens` (tier cost measurement; replaces `measure-tokens.py`), `install-hook` (git pre-commit validation — commits with Errors are blocked by construction)

**New normative schemas:**
- `_schema.yaml` (framework domain) and `domain/[domain]/things/_schema.yaml` — declare thing types, **per-type status vocabularies**, required fields, and the relation vocabulary. The validator enforces what the domain declares.

**Conflict resolved:**
- `status-vocabulary-universal-vs-domain` (opened and resolved 2026-06-11, outcome `superseded`): the domain owns its status vocabulary; the six universal workflow values are the advisory default when no schema declares one. jmtm-software's compliance state machines were declared as correct rather than corrected.

**Specs updated:**
- `validate.thing.md` (v1.5 → v2.0): rewritten around the division of labour — the tool guarantees mechanical checks (old Levels 1–3 + index integrity); the LLM keeps semantic validation only. Prompt input/output chain validation removed (type-checking for an event system with no runtime).
- `thing.md` (v2.10 → v2.11): status field rewritten — domain-declared vocabularies, reserved-type vocabularies fixed
- `domain-specification-guide.md` (v2.5 → v2.6): `things/_schema.yaml` added to domain structure; floor installation added to scaffolding
- `orchestration.md` (v1.7 → v1.8): `post-write:commit` hard hook gains its mechanical backstop note
- `AGENTS.md` (v3.0): validation checklist delegates to the tool; measured token costs

**Baseline (Phase 0, same day):**
- First framework retrospective (`framework-retrospective-2026-06`), first conflict thing, `continuity.md` initialised, token costs measured (T0 13.5k / T0+T1 26.5k / full 65.5k), repo tagged `v2.9-pre-floor`, transformation plan committed as `framework-v3-transformation-plan`

---

## [2.9.0] - 2026-06-08

Reflexive behaviour: the agent can now reason *about* a domain, not only *within* it — domain velocity, systematic trigger evaluation, systematic conflict scanning, and schema-coherence review. These four capabilities are unified under one new primitive rather than built as four bespoke mechanisms.

**Why one primitive:** three of the four reduce to "aggregate a signal across all things, then read the aggregate instead of re-scanning everything." That is a **derived index**. The fourth — velocity — deliberately uses no index because its signal already lives in git (the authoritative event stream); caching it would only add a drift surface. The design was constrained by three prior insights: indexes are made drift-safe by construction (`tracking-artifacts-can-drift-from-reality`), maintenance rides the observable `post-write` event rather than a new hard hook (`hard-hooks-require-observable-agent-caused-triggers`), and the behaviour is opt-in/scale-triggered so it doesn't burden the agent on every session (`hook-compliance-correlates-with-scope-not-awareness`).

**New spec (Tier 2 — demand-loaded):**
- `derived-index.md` (v1.0, `status: draft`) — the derived-index pattern: `type: index` things in `things/_index/` that aggregate triggers, relationships, or schema fields. Provenance frontmatter + validation rebuild-and-diff make drift detectable rather than silent. Incremental maintenance on `post-write`, full rebuild on demand/at validation/at retrospective.

**New prompt templates:**
- `templates/prompts/domain-velocity.md` (v1.0) — reads git history as telemetry at session-start; surfaces stalled, churning, or untouched work
- `templates/prompts/review-schema-coherence.md` (v1.0) — audits emergent frontmatter vocabulary for name-drift at retrospective

**New index templates:**
- `templates/indexes/triggers.md.template`, `templates/indexes/schema.md.template`

**Prompts updated:**
- `evaluate-triggers.md` (v1.0 → v1.1) — reads the triggers index when one exists; direct scan otherwise
- `detect-conflicts.md` (v1.0 → v1.1) — adds **scan mode** (proactive corpus sweep) bound to `on-status-change` and `retrospective`, alongside the original change mode

**Specs updated:**
- `thing.md` (v2.9 → v2.10): `type: index` documented as framework-generated
- `validate.thing.md` (v1.4 → v1.5): new **Index Integrity** validation (provenance, coverage, commit-not-behind, rebuild-and-diff) — the mechanism that catches index drift
- `orchestration.md` (v1.6 → v1.7): new `retrospective` hook point; two new framework prompts; index maintenance documented as a domain-level `post-write` hard hook; reflexive-behaviour binding examples
- `trigger-specification.md` (v1.0 → v1.1): session-start evaluation points at the triggers index at scale
- `belief-revision.md` (v1.0 → v1.1): new "When To Scan For Conflicts" — event-triggered (claims gaining authority) and periodic (retrospective full sweep)
- `retrospective.md` (v1.0 → v1.1): reflexive scans (full conflict scan, schema review, index rebuild) run at retrospective cadence
- `git-workflow.md` (v1.0 → v1.1): "Git Log As Domain Telemetry" — velocity signals read directly from history, no index
- `scalability-guide.md` (v1.1 → v1.2): derived indexes as the scale lever for reflexive behaviour, with explicit reconciliation of the "no indexing" principle
- `AGENTS.md` (v2.8 → v2.9), `.markdownllm` (v2.8 → v2.9): inventory, Tier 2 routing, `type: index`, new Key Innovation

**Insights captured:**
- `reflexive-behaviors-are-indexes-plus-prompts` — the four-into-one unification
- `derived-index-is-attention-cache-not-search-layer` — reconciles derived indexes with the scalability "no indexing" principle (both-valid)

---

## [2.8.0] - 2026-05-29

SRP violation corrections across 8 issues identified in the 29 May review sweep. Two new specs extracted from embedded/duplicated content; six existing specs corrected for structural conformance.

**Why these were extracted rather than fixed inline:** `thing.md` v2.8 added the Thing Cohesion and Decomposition principle — the framework's formal statement that content serving different audiences or changing at different rates belongs in separate specs. The two highest-severity issues (embedded example type spec, duplicated multi-lens reasoning) were direct violations of the rule in the same file that defines it; leaving them would have undermined the principle as a teaching tool. Extraction also improves context economics: content previously embedded in Tier 0 (`thing.md`) and Tier 1 (`read/write.thing.md`) — loaded in every session — is now in Tier 2 specs loaded only on demand. **Baseline context load is lower post-v2.8.0 than pre-v2.8.0.**

**New specs (Tier 2 — demand-loaded only):**
- `example-things.md` (v1.0) — full specification for `type: example` things; extracted from `thing.md` where it was embedded alongside unrelated schema content (~50 lines removed from Tier 0)
- `reasoning-lenses.md` (v1.0) — canonical multi-lens reasoning spec; extracted from identical duplication in `read.thing.md` and `write.thing.md` (~95 lines removed from Tier 1)

**SRP violations corrected:**
- `thing.md` (v2.8 → v2.9): replaced `type: example` embedded block with pointer to `example-things.md`; added "Framework-Internal Types" note clarifying `specification`, `guide`, `manifesto` are framework-internal and should not be used for domain things
- `read.thing.md` (v2.0 → v2.1): multi-lens section replaced with pointer to `reasoning-lenses.md`
- `write.thing.md` (v2.0 → v2.1): multi-lens section replaced with pointer; removed undefined `schema_version: 2.0` instruction, replaced with guidance on `version` for framework specs
- `validate.thing.md` (v1.3 → v1.4): removed `name`, `description`, `applies_to` skill-convention fields from frontmatter; description incorporated into spec body
- `framework-discovery.md` (v1.0 → v1.1): became canonical for all deployment architecture; nested repository model section added (previously only in `domain-refresh.md`)
- `domain-refresh.md` (v1.0 → v1.1): Deployment Architecture section reduced to 2-sentence summary + link to `framework-discovery.md`
- `domain-specification-guide.md`: Framework Discovery section reduced from ~30-line restatement to 3-sentence orientation + link to `framework-discovery.md`
- `scalability-guide.md` (v1.0 → v1.1): `type: summary` usage clarified — note added distinguishing manual summary things from the formal `thing-lifecycle.md` mechanism

---

## [2.7.0] - 2026-05-29

- `trigger-specification.md` (v1.0, `status: stable`) created as a standalone spec for the trigger system. Previously, trigger documentation lived only in `thing.md` with a forward reference. Now a full specification covering all four trigger types, all condition and action values, evaluation semantics, and idempotency rules. Added to AGENTS.md Tier 2 loading and framework spec inventory.

---

## [2.6.0] - 2026-05-28

**Session-end reclassification:**
- `orchestration.md` (v1.4 → v1.5): `session-end:continuity` removed as third framework hard hook. Reclassified as a bound prompt — hard hooks require observable, agent-caused triggers; "session is ending" does not meet that criterion. The ritual remains mandatory but is invoked explicitly, not via hard hook.
- `AGENTS.md` (v2.7 → v2.8): Replaced hard hook callout with `[BOUND PROMPT: session-end]` block. Updated On Output section accordingly.
- `session-memory.md`: Ritual section updated to reference prompt-based invocation rather than hard hook.

**New prompt templates:**
- `templates/prompts/session-end-continuity.md` — The continuity extraction ritual as a declared prompt with inputs/outputs
- `templates/prompts/worklog-update.md` — WORKLOG append as a companion prompt, both bound to `session-end`

**Discoverability fix:**
- `AGENTS.md`: `thing-lifecycle.md` (draft spec addressing the 200–300 thing scaling ceiling) added to Tier 2 loading table and spec inventory under new "Deferred" heading. Fixes "ghost spec" problem — existed at root since 23 May but was invisible to framework discovery mechanisms.

**New framework artifact:**
- `REVIEWLOG.md` created as a periodic quality review log. Complements the WORKLOG (session narrative) by tracking how well the framework works, not just what was done. First review written: full holistic review post-v2.5.0.

---

## [2.5.0] - 2026-05-27

Four structural gaps in the framework's knowledge management capabilities closed. New specs cover session continuity, contradiction handling, and periodic reflection. Startup loading made context-window-efficient.

**New specs:**
- `session-memory.md` (v1.0) — how sessions preserve generative knowledge; defines `type: insight`, `type: continuity-brief`, and the mandatory session-end extraction ritual
- `belief-revision.md` (v1.0) — how contradictions between things are held and resolved; defines `type: conflict`, `relation: supersedes/contradicts/superseded-by`, three resolution outcomes
- `retrospective.md` (v1.0) — periodic domain quality reflection; defines `type: retrospective`, when to write one, and what it produces

**New templates:** `insight.md.template`, `conflict.md.template`, `retrospective.md.template`, `continuity-brief.md.template`

**Behavioural changes:**
- `orchestration.md` (v1.3 → v1.4): `session-end:continuity` added as third framework hard hook; covers both insight extraction and belief revision / conflict detection
- `AGENTS.md` (v2.3 → v2.7): startup sequence replaced with tiered loading (Tier 0 ~15k / Tier 1 ~33k / Tier 2 on demand); eliminates up to 75% of startup context cost on Q&A sessions
- `thing.md` (v2.3 → v2.5): four framework-reserved types (`insight`, `continuity-brief`, `conflict`, `retrospective`); framework-reserved relation values (`supersedes`, `contradicts`, `superseded-by`); new recommended fields `confidence` and `origin`
- `validate.thing.md` (v1.1 → v1.2): conflict-integrity checks added to Level 4 Semantic Validation; retrospective staleness Info check

**Bug fixes (consistency pass):**
- `orchestration.md` frontmatter version corrected (1.3 → 1.4)
- `thing.md` version corrected (2.3 → 2.5); `retrospective` added to reserved types list
- `session-memory.md` linked_things: added `belief-revision-specification`
- `orchestration.md` linked_things: added `belief-revision-specification`

**Known gaps (deferred):** `domain-specification-guide.md` does not yet reference the new knowledge primitives (continuity.md, insight, conflict, retrospective). A new domain created with the current guide starts without awareness of these. Tracked for a future patch.

---

## [2.4.0] - 2026-05-22

- Rewrote README.md: reframed from human instruction manual to agent-first, human-directed partnership model. Added agent-user transcript showing domain creation through conversation.
- Updated llm-driven-systems.manifesto.md (v2.0 → v2.1): added "Discovery: The Partnership Without Configuration" section. Revised Getting Started to emphasize design intent, feedback loops, and ongoing collaboration.
- Updated domain-specification-guide.md (v2.3 → v2.4): reframed AGENTS.md creation as design decisions (not template-filling). "Plan Your Domain" → "Design Your Domain". "Iterate" → "Use It, Refine It, Grow It" with concrete feedback examples.
- Core framing clarification: specs are written for agents to consume; humans direct, design, use, and refine; the partnership produces the system. No structural/architectural changes — the specs already modelled this correctly.

---

## [2.3.0] - 2026-05-21

- Made orchestration opt-in: demoted from framework-level to domain-level pattern after real-world testing showed it made LLM reasoning rigid
- Moved prompt files from `prompts/` to `templates/prompts/` (templates, not mandates)
- Updated orchestration.md (v1.0 → v1.1): added "When To Use / When Not To Use" guidance
- Renamed `validate.thing.skill.md` → `validate.thing.md`, reclassified as `type: specification` (matches read.thing.md / write.thing.md pattern)
- Promoted all framework specs from `status: draft` to `status: stable` — pushed to remote = not draft
- Fixed consistency gaps: README now lists all 12 framework specs, CONTRIBUTING lists newer specs, WORKLOG frontmatter updated
- Fixed README stale status values (`draft/active/complete` → canonical thing.md values)
- Fixed README "Templates (Future Organization)" → reflects current state
- Adopted per-push changelog format (this change)

---

## [2.2.1] - 2026-05-19

**Domain Refresh Specification (domain-refresh.md):**
- Defines the nested git repository deployment architecture (framework repo + isolated domain repos, .gitignore contract)
- Specifies the refresh process: how domain agents check CHANGELOG, WORKLOG, and foundational specs for framework evolution
- Refresh algorithm with version tracking via `framework_version_seen` frontmatter field
- Integration points for domain workflow skills and AGENTS.md startup sequences

---

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
- **Reference Domain** — Added as primary example domain
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
