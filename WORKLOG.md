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
  - id: validate-thing-specification
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
  - id: orchestration-specification
    relation: documents
  - id: domain-refresh-specification
    relation: documents
---

# Framework Work Log

This file is a running record of work done, decisions made, and work remaining. It is updated at the end of every session. It serves both as a progress tracker and as a historical record for retrospective reflection.

---

## 23 May 2026

### Session 1

#### Topic: Thing Compression & Rolling Window — Design Discussion

Exploratory session discussing a new framework capability to break through the hard ceiling on domain thing count. No spec drafted yet — intentionally staying in design phase.

#### Problem Statement

The scalability guide acknowledges a hard ceiling (~200-300 active things before friction, ~1,000 before breaking). Current approaches (contextual loading, manual summaries, tiered loading) mitigate but don't solve. The domain needs a lifecycle mechanism that automatically manages thing density over time.

#### Proposed Solution: Rolling Window + Compression

- **Rolling window:** Things active within the last 30 days remain at full depth
- **Compression:** Things outside the window are automatically compressed to stubs (frontmatter + summary)
- **Pin mechanism:** `pin: true` in frontmatter exempts a thing from auto-compression regardless of age
- **Reversibility:** Full content preserved in git history and/or archive folder

#### Design Decisions (Agreed)

- **Window size:** 30 days
- **Compression format:** Agent's choice — optimized for LLM scanning + git-friendliness. Current leaning: stub format (frontmatter with added `summary` field, narrative body stripped). Keeps things as valid thing files, just lighter.
- **Pin/bypass:** Yes — `pin: true` prevents auto-compression for things that are old but still relevant (reference material, ongoing paused projects, recurring items)

#### Design Decisions (Open — Suggestions Given)

- **Retrieval mechanism — three options proposed:**
  - **Option A: Query-Time Scan** — Agent always loads all stubs, matches query against summaries. Simplest but doesn't scale past ~1,000 compressed things.
  - **Option B: Manifest Index** — Single `_archive-manifest.md` file listing all compressed things with id, type, status, summary, compressed_date. Agent searches one file instead of opening hundreds.
  - **Option C: Relationship-Triggered** — Active things retain `linked_things` refs to compressed things. When agent follows a dead reference, it auto-retrieves from archive. Organic but doesn't cover "what did I do about X?" queries.
  - **Recommended: B + C combined** — Manifest for user-initiated discovery ("what was that project?"), relationship links for organic graph traversal ("what's blocking this?"). Covers both access patterns.

#### Frontmatter Additions (Proposed)

```yaml
compressed: true
compressed_date: 2026-04-20
summary: "One-line description of what this thing was about"
last_active: 2026-04-18
pin: false
```

#### Capacity Impact (Estimated)

- Active window: ~50-80 things at full depth (current normal capacity)
- Compressed stubs: 500+ things at ~100-150 tokens each
- Net effect: 5-10x capacity increase per domain without breaking context limits

#### Next Steps

- [ ] Decide on retrieval mechanism (B+C recommended)
- [ ] Draft `thing-compression.md` spec (or similar name)
- [ ] Design the compression skill/prompt that performs the maintenance
- [ ] Define rehydration triggers and promotion logic (compressed → active)
- [ ] Update scalability-guide.md to reference the new spec as Approach 4

---

### Session 2

#### Topic: Prior Agent Conversation Review — Compression Design Critique

Reviewed a prior conversation with a different agent that had explored the same rolling window / compression idea. The purpose was to assess whether the prior conversation changed anything in the current design direction.

#### What the Prior Conversation Got Right

- **`decompress_cost` / rehydration token estimate** — Surfacing the approximate token cost of loading a rehydrated thing is genuinely useful. Worth including as a frontmatter field (e.g., `rehydration_tokens`).
- **`references_from_active` in archive frontmatter** — Equivalent to Option C (relationship-triggered retrieval). Valuable because it tells the agent which active things have dependencies on compressed ones, enabling organic graph traversal.
- **Option B (structured prose summary) over binary payloads** — The prior agent correctly favoured human-readable narrative summaries over encoded blobs, which is aligned with the framework's principles.
- **Phase-based implementation** — Sensible sequencing: define the format first, then the compression process, then the retrieval patterns, then a worked proof.

#### The Critical Flaw — Binary Compression Is Wrong for This Framework

The prior agent proposed actual binary compression: gzip/zstd payloads, base64-encoded blobs in markdown bodies, checksums, and external decompression operations. This is fundamentally incompatible with the framework for several reasons:

1. **LLMs cannot execute decompression.** The framework has no tooling layer. The agent cannot inflate a gzip blob; any "decompression" would require external infrastructure the framework intentionally avoids.
2. **Binary blobs break human-readability.** A core principle of the framework is that every file is readable by a human in a text editor. Base64 payloads violate this.
3. **Git diffs on binary blobs are meaningless.** The audit trail — one of the framework's key values — is destroyed when file bodies become encoded data.
4. **Period archives (e.g. "Q1 2026 = 47 things in one file") lose individual thing identity.** You cannot hot-link to a specific thing inside a bulk archive. The graph of `linked_things` relationships breaks.

The prior agent conflated two different problems: **storage compression** (reducing bytes on disk) and **context compression** (reducing what the LLM loads per session). The framework only needs the second. "Compression" in this context means: narrative stripping — the thing body is summarised into a `summary` frontmatter field, not encoded.

#### Where This Lands

The WORKLOG Session 1 direction is confirmed as correct:

- Each thing remains an individual file
- "Compression" = narrative stub: frontmatter retained, body replaced by a `summary` field
- No binary encoding, no external tooling, no period-container archives
- Still valid markdown things, individually addressable, meaningful git diffs, human-readable

The one idea from the prior conversation worth carrying forward is the **period summary thing** concept — not as a bulk container for compressed things, but as an optional narrative overview of a time window (e.g., a `type: period-summary` thing that captures what happened in a given month). This would complement the individual stubs, not replace them.

#### Three Open Design Tensions (Deferred to Next Session)

The following tensions were identified but not resolved. They should be the starting point of the next design session:

1. **What is a thing's "age"?** `last_active` doesn't exist yet. Does it update on read, on write, or only on explicit human engagement? Recurring items may be old by timestamp but very much alive.
2. **Automatic vs. on-demand compression triggering.** Does the agent compress automatically during normal operation, or only when the user explicitly requests it? Auto is more elegant; on-demand is safer. This tension determines the shape of everything else — resolve it first.
3. **Manifest as a thing vs. special artifact.** If using Option B (manifest index), should `_archive-manifest.md` follow the thing format (uniform system) or be a special framework artifact (simpler to scan and reason about)?

---

### Session 3

#### Topic: Prior Art Research — Established Patterns for Thing Compression

Research session to identify existing, proven paradigms that align with the compression/archival pattern being designed. The framework's philosophy is to conduct existing well-proven patterns in a new arrangement — not to reinvent the wheel.

#### Five Established Patterns Identified

**1. S3 Lifecycle Policies (AWS) — Closest direct match**
- Declarative rule-based transitions: "After 30 days, transition from Standard to Glacier"
- Age is the trigger; multiple tiers (Hot → Warm → Cold → Delete)
- Per-bucket (= per-domain) configuration
- Transparent retrieval from cold storage (just takes longer)
- **What we take**: Declarative config model. Rules declared in domain AGENTS.md, not procedural code.

**2. Hierarchical Storage Management (HSM) — The general paradigm (IBM, 1978)**
- Automatic migration between hot/cold tiers based on access patterns
- Transparent retrieval: user accesses data the same way regardless of tier
- System handles promotion back to hot when cold data is accessed
- **What we take**: Transparency — agent handles tier management invisibly to user.
- **What we heed**: HSM research shows users get frustrated by silent migration → validates `suggest` mode first.

**3. Log Rotation (logrotate) — The operational pattern**
- Time-based or size-based triggers
- Compress old, keep N recent, delete oldest
- Runs as a scheduled job (cron)
- **What we take**: The maintenance rhythm. Compression runs at session-start as a periodic check, not continuously.

**4. Information Lifecycle Management (ILM) — The lifecycle model**
- Five phases: Creation → Distribution → Use → Maintenance → Disposition
- Records transition: active → semi-active → inactive
- **Legal holds** freeze records at any stage regardless of age
- **What we take**: Legal hold = `pin: true`. Same concept, proven in records management for decades.

**5. LSM Trees (Log-Structured Merge Trees) — The compaction/retrieval model**
- Recent writes in memory (C0), older data compacted to sorted runs on disk (C1, C2...)
- **Bloom filters** provide fast "is it here?" checks without reading full data
- **What we take**: Manifest = Bloom filter. Quick scan to determine if a thing exists in archive without opening individual files.

#### Key Refinement From Research: Age + Eligibility

The most important insight: no established pattern uses age *alone* as the trigger. S3 lifecycle rules filter by tags AND age. ILM uses status AND age. HSM uses access frequency AND time.

Our trigger should be: **age (outside 30-day window) + status eligibility**. Things with active statuses are auto-exempt:

```yaml
compression:
  window: 30d
  mode: suggest
  pin_statuses: [in-progress, blocked, paused]
```

Only `completed` and `cancelled` things are eligible for compression. Active things never compress regardless of age. This eliminates the edge case of compressing something the user is still working on.

#### Design Tensions Resolved

1. **What is a thing's "age"?** → Resolved: `last_active` updates on commit (when the thing's file is committed with changes). Simple, auditable, no ambiguity. Git is the source of truth.
2. **Automatic vs. on-demand?** → Resolved: `suggest` mode first (agent proposes, user approves). Domains can escalate to `auto` once they trust the mechanism. Mirrors the autocommit pattern progression.
3. **Manifest as thing vs. artifact?** → Resolved: Artifact (same category as WORKLOG). Has frontmatter for identification, body is structured index. Not a domain thing.

#### Retrieval Mechanism — Final Design (B+C Combined)

Three retrieval paths, mapped to established patterns:

| Path | Trigger | Pattern Source | Example |
|---|---|---|---|
| Period summary | User asks about a time window | ILM reporting | "What happened in Q1?" |
| Manifest search | User asks about a specific old thing | LSM Bloom filter | "What was that bike task?" |
| Relationship traversal | Agent follows a dead link | HSM auto-promote | "What blocks this?" |

#### Proposed Implementation Plan

**Phase 1: Specification (Draft)**
- Write `thing-lifecycle.md` — the compression spec defining format, rules, triggers, retrieval
- Define the compressed stub format (frontmatter + summary field)
- Define the manifest artifact format
- Define the compression eligibility rules (age + status)
- Define retrieval paths and rehydration behaviour
- Status: `draft`

**Phase 2: Domain Configuration**
- Extend AGENTS.md frontmatter schema with `compression:` block
- Define config options: `window`, `mode` (off/suggest/auto), `pin_statuses`, `pin` field on individual things
- Update domain-specification-guide.md to reference lifecycle configuration

**Phase 3: Compression Skill**
- Create `compress-things.skill.md` (or equivalent domain skill template)
- Defines the maintenance routine: scan things → identify eligible → generate summaries → write stubs → update manifest → commit
- Runs at session-start or on-demand

**Phase 4: Retrieval Skill**
- Create retrieval logic: manifest search, relationship-triggered auto-retrieve, period summary generation
- Define rehydration: how to restore a compressed thing from git history or archive folder
- Define promotion logic: if a compressed thing is accessed N times, auto-restore to active window

**Phase 5: Scalability Guide Update**
- Add as "Approach 4: Lifecycle Compression" to scalability-guide.md
- Position between Approach 2 (manual summaries) and Approach 3 (tiered loading)
- Reference the established patterns as prior art

**Phase 6: Proof / Validation**
- Apply to a real domain (ProducFlow2 has enough things to test)
- Validate: compression works, retrieval works, manifest stays accurate, git diffs are clean
- Promote spec from `draft` → `evolving` → `stable`

#### Decision: Spec and Defer

This feature is a real gap but not an immediate blocker. The framework principle of "don't fix until broken" applies. The recommendation is:

- **Spec now** (Phase 1) — capture the design while it's fresh, establish the vocabulary and format
- **Defer deployment** (Phases 2-6) — implement when a domain actually hits the ceiling and needs it

This gives the framework a ready answer when someone hits the scaling wall, without over-engineering the present.

---

### Session 4

#### Topic: Spec and Defer — Terminology Correction, Manifesto Update, Specification Drafted

Final session in the lifecycle design arc. Corrected terminology, added framework evolution principle to manifesto, and drafted the full specification.

#### Completed

- [x] **Terminology correction**: Adopted ILM terminology throughout — "disposition to semi-active storage" instead of "compression." The mechanism is broader than making files smaller; it's a lifecycle transition between storage tiers.
- [x] **Manifesto updated** (v2.1): Added "Spec When Foreseeable, Deploy When Felt" subsection under "Building On What Exists." Captures the framework's evolutionary discipline — design solutions for foreseeable problems, deploy them when the friction is real.
- [x] **thing-lifecycle.md created** (v0.1, status: draft): Full specification covering the rolling window, disposition process, stub format, eligibility rules, manifest artifact, three retrieval paths, rehydration process, domain configuration, period summaries, and capacity impact estimates. Draws explicitly from the five prior art patterns identified in Session 3.
- [x] **git-workflow.md updated** (earlier this session): Added terminal execution note about chained commands being collapsed by tool terminals.

#### Key Terminology Decisions

| Old term | New term | Rationale |
|---|---|---|
| Compression | Disposition | ILM standard term; "compression" implies encoding |
| Compressed thing | Semi-active thing | Describes the storage tier, not the process |
| Decompression | Rehydration | Standard term for restoring from cold/semi-active |
| Archive | Semi-active storage | "Archive" implies finality; semi-active implies retrievability |

#### Decision: Spec and Defer (Confirmed)

Phase 1 (specification) is now complete. Phases 2-6 (deployment) are deferred until a domain encounters the scaling ceiling. The spec sits in the repo as `thing-lifecycle.md` with `status: draft`, ready to activate when needed. The AGENTS.md has **not** been updated to reference this spec — it will be incorporated into the framework's startup loading only when deployed.

---

## 22 May 2026

### Session 1

#### Completed

- [x] Complete rewrite of README.md — reframed from human-instruction-manual style to agent-first-human-directed partnership model
- [x] Added agent-user transcript to README showing a domain being created through conversation
- [x] Updated llm-driven-systems.manifesto.md (v2.0 → v2.1) — added "Discovery: The Partnership Without Configuration" section explaining how auto-discovery of AGENTS.md enables zero-configuration partnership
- [x] Revised manifesto "Getting Started" section to emphasize design intent, feedback loops, and ongoing collaboration (7 steps → 8 steps)
- [x] Updated domain-specification-guide.md (v2.3 → v2.4) — reframed "Creating Your Agent File" as a design document where humans make deliberate decisions about agent behavior, workflows, constraints, and conflict handling
- [x] Renamed guide Step 2 from "Plan Your Domain" to "Design Your Domain" with richer design questions
- [x] Renamed guide Step 5 from "Iterate" to "Use It, Refine It, Grow It" with concrete feedback examples
- [x] Full framework coherence review — all specs checked against new framing
- [x] Updated CHANGELOG with new version entry

#### Decisions Made

- **The README was incorrectly framed.** It read as a human instruction manual ("here's how YOU set it up"). The framework's actual model is: specs are for agents to consume, the human directs and refines, the partnership produces the system. Rewrote to reflect this.
- **"Agent-First" as principle #1 was too exclusive.** Changed to "Agent-Consumed, Human-Directed" in the README — captures both sides of the partnership.
- **write.thing.md does NOT need a partnership preamble.** The agent already understands its role from the instructions themselves. Partnership framing matters in human-facing documents (README, manifesto, guide), not in agent-facing specs.
- **Discovery deserved its own manifesto section.** It's the mechanism that makes the partnership zero-configuration — the thing that means humans don't have to teach agents how to use the framework. The framework teaches the agent.
- **AGENTS.md is a design document, not a template.** The domain-specification-guide was presenting it as "fill this in." It's actually where humans make deliberate design decisions about agent behavior, reasoning style, workflows, and constraints.

#### Key Insight

The framework's framing was subtly wrong — not in what it built, but in how it presented itself. The specs themselves (thing.md, write.thing.md, orchestration.md, read.thing.md) already correctly model the partnership: human defines constraints, agent operates within them, conflicts get surfaced. The gap was in the outward-facing documentation (README, manifesto, guide) which didn't articulate the human's ongoing role clearly enough. The specs were right; the explanation was incomplete.

---

## 21 May 2026

### Session 3

#### Completed

- [x] Conducted full holistic framework review — read all 12 specs, manifesto, examples, templates, domain examples, WORKLOG, and CHANGELOG end-to-end
- [x] Created REVIEWLOG.md — new framework artifact for tracking periodic reviews of framework state, cohesion, and direction. Format mirrors WORKLOG: daily blocks → timestamped review blocks → subsections (works well, tensions, over-engineered, under-engineered, missing from todos, reflections)
- [x] Populated first review entry (21 May 2026, 14:30) with detailed assessment across all subsections

#### Decisions Made

- REVIEWLOG complements the WORKLOG: WORKLOG tracks what was done; REVIEWLOG tracks how well what exists is working. Separate files because they serve different purposes and different reading patterns.
- Review format uses numbered points with bold titles + 1–2 sentence explanations — detailed enough to extract actionable items, concise enough to scan without being overwhelming.
- Reflections section left blank at review time by convention — filled in later with hindsight, maintaining the same pattern as WORKLOG reflections.

---

### Session 2

#### Completed

- [x] Full framework review — checked all specs, README, CONTRIBUTING, WORKLOG, CHANGELOG for consistency against recent changes
- [x] Fixed README: stale status values in thing example (`draft/active/complete` → canonical set from thing.md)
- [x] Fixed README: Foundation Files section now lists all 12 framework specs (was only listing the original 5)
- [x] Fixed README: Templates heading updated from "Future Organization" to reflect current state (templates exist, prompts included)
- [x] Fixed WORKLOG: added `orchestration-specification` and `domain-refresh-specification` to frontmatter `linked_things`
- [x] Fixed CONTRIBUTING: added `orchestration.md`, `framework-discovery.md`, and `domain-refresh.md` to framework structure listing
- [x] Adopted new CHANGELOG format: per-push entries with concise summaries, version numbers retained, WORKLOG handles detail
- [x] Migrated `[Unreleased]` domain-refresh content into `[2.2.1]`; created `[2.3.0]` for this push
- [x] Renamed `validate.thing.skill.md` → `validate.thing.md`: reclassified as `type: specification` with proper frontmatter (`id: validate-thing-specification`, `status: stable`, `created: 2026-05-19`). Updated all 18 files referencing the old name/ID.
- [x] Promoted all 6 framework specs from `status: draft` to `status: stable` — rationale: once pushed to remote, it’s not a draft

#### Decisions Made

- Pre-push review identified 7 items; 5 fixed immediately (README, CONTRIBUTING, WORKLOG). Changelog to be handled separately with a revised approach.

---

### Session 1

#### Completed

- [x] Evaluated orchestration layer after real-world testing in a domain workflow
- [x] Concluded: framework-level orchestration made LLM reasoning too rigid — lost the natural flow that narrative specs provide
- [x] Refactored orchestration to opt-in domain-level pattern:
  - Moved `prompts/` → `templates/prompts/` (templates, not mandatory reasoning)
  - Removed orchestration.md from AGENTS.md startup loading
  - Reframed AGENTS.md description: "opt-in pattern for domains that need structured orchestration"
  - Updated orchestration.md (v1.0 → v1.1): added "When To Use / When Not To Use" section, removed inherited framework bindings, updated file organization and design principles
- [x] Committed: `framework: make orchestration opt-in, move prompts to templates`

#### Decisions Made

- **Framework-level orchestration creates rigidity, not value.** Testing in a domain workflow showed that binding prompts to lifecycle hooks universally caused the LLM to execute reasoning mechanically rather than calibrating naturally. The analysis workflow lost its natural reasoning flow — responses became formulaic and rigid.
- **Narrative specs are the right primary mechanism.** write.thing.md's "consider what else needs updating" is a nudge — the LLM decides how much attention to pay. A bound prompt is a procedure — the LLM executes it completely. Nudges produce better reasoning for most domains.
- **Orchestration earns its place at domain level, not framework level.** Domains with strict phase gates (compliance, regulated environments, multi-person teams) benefit from explicit hook/prompt/binding declarations. Simpler domains get bogged down by them.
- **Prompts become templates, not mandates.** The 6 prompt files are valuable as starting points for domains that opt into orchestration — they show the pattern and provide a foundation to adapt. But they should never fire universally.
- **The framework's principle of progressive complexity is validated.** Start simple (narrative specs), add structure only when a domain's needs demand it. The orchestration spec remains available — it just doesn't impose itself.

#### Key Insight

The distinction between a *nudge* and a *procedure* is the critical finding. Narrative prose lets the LLM reason proportionally — it naturally calibrates depth based on context. Structured orchestration (hooks + prompts + bindings) forces complete execution regardless of context. For framework-level concerns, nudges are almost always better. For domain-level concerns with high-consequence moments, procedures earn their place.

#### Reflections

- This is the framework's first real-world feedback loop producing a rollback. The orchestration layer was well-designed in theory but too rigid in practice. The healthy response is to demote it, not delete it — the concepts are sound, the scope was wrong.
- The fact that testing caught this within a day validates the framework's "draft → evolving → stable" status system. orchestration.md was correctly marked as draft; it evolved through use.

---

## 20 May 2026

### Session 1

*Note: This entry was written retroactively on 21 May 2026.*

#### Completed

- [x] Created orchestration.md — new foundational specification defining the orchestration layer: hook points (named lifecycle moments like session-start, post-write, pre-commit), prompts (reusable reasoning templates), and bindings (declarations connecting hooks to prompts). Formalises what was previously implicit across thing.md triggers, git-workflow.md commit points, and domain workflow phase gates into composable, portable orchestration primitives.
- [x] Updated AGENTS.md to reference orchestration.md in the framework specifications list
- [x] Committed: `framework: add orchestration.md — hook points, prompts, and bindings`
- [x] Created 6 framework prompt templates in prompts/ directory:
  - cascade-completion.md — propagate progress when things complete
  - evaluate-triggers.md — scan for trigger conditions that are now true
  - validate-before-commit.md — structural/referential/semantic pre-commit checks
  - session-orientation.md — orient the agent at session start
  - surface-attention.md — prioritise and filter what the user hears about
  - detect-conflicts.md — catch logical/lens/dependency conflicts before changes land
  - Each prompt is a thing (type: prompt) with explicit inputs, outputs, and bound_to declarations linking to orchestration.md hook points
- [x] Committed: `framework: create framework prompt templates (6 prompts)`
- [x] Reinforced orchestration.md guardrails:
  - Expanded "When To Create A Prompt" with create/leave-implicit criteria
  - Added red flags section for over-specification detection
  - Added litmus test and quantity guidance (6 framework, 2–5 per domain)
- [x] Extended validate.thing.skill.md (v1.0 → v1.1) with Prompt Validation section:
  - Structural checks: inputs/outputs/bound_to presence and format
  - Referential checks: hook existence, orphan/missing prompt detection, I/O chain consistency
  - Semantic checks: scope focus, duplication detection, quantity threshold
  - Added linked_things to frontmatter (thing-spec, orchestration-spec)
- [x] Committed: `framework: reinforce guardrails + add prompt validation`
- [x] Fixed typo in README.md
- [x] Committed: `Typo fix in readme`

#### Decisions Made

- The orchestration layer sits between the existing specs (thing.md triggers, git-workflow.md commit points) and formalises the implicit reasoning patterns into explicit, portable primitives — hook points, prompts, and bindings
- Prompt templates are things themselves (type: prompt) — they follow the same frontmatter + narrative body pattern as all other framework specifications, keeping the system self-describing
- Six framework-level prompts is the right quantity — covers the core lifecycle moments without over-specifying. Domain-specific prompts should add 2–5 more per domain.
- Validation was extended to cover prompts because they are now first-class things in the system — structural, referential, and semantic checks mirror the existing thing validation patterns

#### Reflections

- The orchestration spec closes the last major architectural gap — the framework now has explicit definitions for when reasoning fires, what reasoning runs, and how they connect. This was previously scattered implicitly across triggers, commit points, and workflow skills.
- The prompt templates demonstrate the framework eating its own dogfood: each prompt is a thing, validated by the same validation skill, committed per the same git workflow.

---

## 19 May 2026

### Session 1

#### Completed

- [x] Full review of entire MarkdownLLM 2.0 workspace — all core files, examples, templates, and changelog read end-to-end
- [x] Assessed cohesion of the framework — confirmed three-layer architecture (Agent → Skills → Things) is consistently applied across all documentation and examples
- [x] Identified and fixed minor inconsistencies: README referencing old `Instructions-guide.md` filename (now `domain-specification-guide.md`); `read.thing.md` and `write.thing.md` referencing old `[domain].instructions.md` naming (now `[domain]-specification.skill.md`)
- [x] Created WORKLOG.md in MarkdownLLM repo (this file), adopting the day/session format
- [x] Captured 10 identified gaps/areas for future work (see To Do and Decisions Made)

#### Decisions Made

- The interface layer is deliberately not specified as a new protocol — the framework leverages existing interface routes (VS Code + GitHub Copilot, Claude Code CLI, mobile chat apps, voice-to-text in OS) rather than inventing a new one. The interface section needs to be *described and defined* in the manifesto/README, not *built*.
- The output side of the framework is broader than just things — the agent can produce documents (Word, PDF), images, software code, videos, audio. This needs explicit documentation as a concept: things are the agent's persistent memory/state; outputs are the agent's deliverables produced from that state.
- WORKLOG adopted for this repo — serves as session history, progress tracker, and captures forward planning.
- The framework is cohesive and internally consistent at the specification level; the gaps are operational (how to deploy end-to-end) not architectural.
- The "elegant constraint" argument (smaller models + well-defined domains) is a key differentiator that should be promoted more prominently.

#### Reflections

- The framework has evolved significantly in 6 days (13 May → 19 May) from a single-domain tool to a generalised specification. The rate of iteration is high but the architectural decisions have been sound — the v1→v2 simplification (five components → three layers) was the right call and nothing in the current structure needs further restructuring.
- Having an independent reviewer read the entire workspace cold validated that the writing is clear and the concepts are coherent. The gaps identified are all forward-looking (operational concerns), not foundational.

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
- **Multi-agent / multi-domain patterns** — What happens when domains share things or one agent's output feeds another agent's input? No specification exists for domain composition across boundaries.
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

- [x] Evaluate whether hooks are useful for enforcing encoding discipline at session end

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
