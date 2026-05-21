---
id: framework-reviewlog
type: artifact
status: evolving
version: 1.0
created: 2026-05-21
linked_things:
  - id: framework-worklog
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: evaluates
  - id: thing-specification
    relation: evaluates
  - id: git-workflow-specification
    relation: evaluates
  - id: interface-specification
    relation: evaluates
  - id: orchestration-specification
    relation: evaluates
---

# Framework Review Log

This file is a running record of independent reviews of the framework's state, cohesion, and direction. It complements the WORKLOG (which tracks what was done) by tracking how well what exists is working and where the gaps are. Reviews are conducted periodically or on request.

---

## 21 May 2026

### Review — 21 May 2026, 14:30

**Scope:** Full holistic review of the framework post-v2.3.0. All 12 specifications, both examples, templates, domain examples, WORKLOG, and CHANGELOG read end-to-end.

**Overall Verdict:** Architecturally sound, internally coherent, philosophically clear. The framework is in the "beautifully specified but underproven" phase — the design decisions are right, the evidence they work under real load is thin.

---

#### What Works Well

1. **"Build on what exists" philosophy** — Not inventing protocols, databases, or interfaces. Defining the composition pattern for proven tools (markdown, YAML, git, LLMs, existing editors). Makes the framework durable — if any single tool disappears, the data is still portable plain text.

2. **Self-describing architecture** — The framework is a domain within itself. AGENTS.md follows its own prescription. Specs have frontmatter. The WORKLOG is a thing. Creates a genuine dogfooding loop where working on the framework tests the framework.

3. **Nudge vs. procedure distinction** — Hard-won from the orchestration demotion (21 May Session 1). Narrative prose as attention guidance the LLM calibrates naturally vs. structured prompts as procedures the LLM must execute completely. This insight is non-obvious, tested, and documented honestly.

4. **Tiered loading model** — Level 1 (metadata) / Level 2 (relationships) / Level 3 (full context) is a simple, elegant answer to finite context windows. Mirrors how humans actually scope attention to match question breadth.

5. **Commit messages as domain events** — Structured `action: description` format makes git log a parseable event stream. Enables temporal reasoning and session orientation without building event infrastructure.

6. **Trigger system design** — Triggers as attention signals, not execution logic. Idempotent evaluation (trigger stays true until condition changes; git provides temporal context for proportional response). Avoids needing "already fired" state machinery.

7. **Orchestration as opt-in** — Positioning hooks/prompts/bindings as a domain-level choice rather than framework-level mandate. The "litmus test" (checklist vs. procedure manual) and 10-prompt cap are pragmatic guardrails.

---

#### What Doesn't Work Well / Tensions

1. **Validation confidence gap** — validate.thing.md is comprehensive and detailed, creating an impression of deterministic rigor. Every check is actually LLM-performed with no guarantee of consistency. For the regulated domains the framework explicitly targets (law, compliance, finance), this gap between appearance and guarantee is a credibility risk. Needs an honest acknowledgment + recommendation to pair with a deterministic YAML linter (~100 lines of Python) for Level 1 checks.

2. **Scalability ceiling acknowledged but unresolved** — The scalability guide honestly states 1,000+ things "breaks," then offers no path beyond "consider whether this framework is the right fit." For a framework positioning itself as generalizable to "any domain," this hard ceiling (~200–500 active things) is lower than many real domains need. The rejection of indexing/search is philosophically defensible but should be framed as a design choice with known consequences, not just a scaling strategy.

3. **"Who actually evaluates triggers" problem** — The trigger system specifies *what* and *when* well, but the "scheduled invocation" mechanism (cron, GitHub Actions, calendar event) is mentioned once and never specified. Without it, time-based triggers (due_date_passed, stale) only fire during active sessions — dramatically reducing their utility. Either spec a reference implementation of scheduled invocation or explicitly acknowledge the limitation.

4. **Multi-domain composition gap** — `framework_root` handles discovery upward (domain → framework). Nothing exists for lateral composition (domain ↔ domain). What happens when Domain A produces things Domain B needs? When two domains share a thing type? When an agent reasons across domain boundaries? No specification exists for domain composition.

5. **Examples don't prove the system** — Compliance-patterns has 2 things. Life-manager has zero things. Neither shows triggers firing, validation catching real errors, tiered loading in action, session-start orientation working, or git log being parsed as an event stream. The included domain examples are specialized and don't demonstrate generalizability.

---

#### What May Be Over-Engineered

1. **Trigger type taxonomy** — Four trigger types (time, dependency, threshold, relationship) with detailed YAML schemas, when the evaluator is a reasoning engine not a rule engine. A simpler "conditions" array with natural language descriptions might achieve the same effect with less specification overhead. The structured YAML adds ceremony the LLM doesn't need.

2. **Prompt/skill/trigger-action hierarchy** — The three-level hierarchy (skill → prompt → trigger action) is elegant on paper but creates ambiguity about where guidance should live. "When a thing completes, check what it unblocks" could be a trigger action (`cascade`), a prompt (`cascade-completion`), a binding (`post-write → cascade-completion`), or a line in write.thing.md. The answer is "depends on your domain" — but that ambiguity is a usability cost for new adopters.

3. **Domain-refresh as a specification** — The refresh process (check CHANGELOG, read WORKLOG, scan versions, compare, report) is specified at the same depth as core architectural decisions. In practice this is "read what's new and update yourself" — something any LLM does naturally when instructed. The specification adds ceremony without proportional clarity.

---

#### What May Be Under-Engineered

1. **Error recovery and conflict resolution** — No guidance for: agent makes a bad write and corrupts a thing; two linked things have contradictory states; a trigger cascade loops. The framework says "git revert" and "validation catches it" — but there's no specification for in-session agent behaviour when encountering an unresolvable conflict. Does it stop? Ask the user? Guess? This matters for unattended/scheduled invocations.

2. **Thing lifecycle beyond status** — Things have status transitions but no guidance on: archival mechanics (when/how completed things get compressed), deletion (can things be deleted? referential integrity?), or within-thing versioning (no `last_modified` field; git tracks it but the thing doesn't self-describe its recency).

3. **Onboarding path** — No quickstart. Domain-specification-guide is 200+ lines of spec. A new user faces manifesto → thing.md → domain-spec-guide → templates with no "run this, see it work" moment. Barrier to entry is high for something that claims existing tools are the only infrastructure needed.

4. **Thing granularity guidance** — thing.md says "large enough to be meaningful, small enough to be actionable" without concrete examples of too-granular or too-coarse. This is where most new users will struggle in practice.

5. **Minimum viable domain weight** — The framework implies you always need AGENTS.md + 4 skill files + things directory (6+ files minimum). For a simple personal domain with 5 things and no relationships, that's significant overhead. No "lightweight mode" or guidance on when the full structure isn't needed.

---

#### Missing From WORKLOG Todos

1. **Adoption persona / theory of change** — Who is the first user? A developer with Copilot? A team lead structuring their domain? The framework speaks to everyone and no one. The quickstart (already identified) needs a target persona to be effective.

2. **Domain maturity model** — Specs have status values (draft → evolving → stable). Domains have no equivalent. When is a domain "mature"? After validation passes? After triggers have fired? After 10 sessions? Would help domain authors know when they're scaffolding vs. operating.

3. **System verification patterns** — How do you know the framework is working correctly in a domain? Not thing validation (exists), but system-level verification: triggers fire when they should, cascades propagate, session orientation is accurate. A "smoke test" pattern for domains.

4. **Degenerate case acknowledgment** — What if someone has a domain with 3 things and no relationships? The framework adds significant ceremony for trivial domains. Worth stating the threshold below which the full framework structure isn't justified.

5. **Scheduled invocation reference implementation** — At least one concrete example of how time-based triggers get evaluated outside active sessions (GitHub Actions workflow, cron + CLI, etc.).

---

#### Reflections

*To be filled in on retrospective review.*

---

## Format Guide

When updating this file:

- **Day blocks** (`## D MMM YYYY`) — one per calendar day. All reviews done that day fall under the same day block. New days are added at the top of the history.
- **Review blocks** (`### Review — D MMM YYYY, HH:MM`) — one per discrete review within a day. Each review gets its own sub-block with a timestamp.
- **Sub-sections** (`####`) — each review block contains:
  - **What Works Well** — Strengths of the current state. Numbered for reference.
  - **What Doesn't Work Well / Tensions** — Problems, gaps, contradictions, credibility risks. Numbered.
  - **What May Be Over-Engineered** — Where specification exceeds the value delivered. Numbered.
  - **What May Be Under-Engineered** — Where gaps exist or guidance is insufficient. Numbered.
  - **Missing From WORKLOG Todos** — Items not yet captured in the WORKLOG's todo list. Numbered.
  - **Reflections** — Left blank at review time; filled in later with hindsight. May remain empty.
- Reviews should be detailed enough to extract actionable items but concise enough to scan. Use numbered points with a bold title + 1–2 sentence explanation.
- Do not delete old entries — this is a historical record.
