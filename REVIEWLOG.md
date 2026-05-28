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

## 28 May 2026

### Review — 28 May 2026

**Scope:** Full holistic review of the framework post-v2.5.0. All 15 specifications, AGENTS.md (v2.7), domain-specification-guide, scalability guide, thing-lifecycle (draft), InnoTriage domain (AGENTS.md, WORKLOG, things, skills, test run outputs), all three framework insights, templates, examples, WORKLOG, and CHANGELOG read end-to-end.

**Overall Verdict:** Architecturally mature, philosophically coherent, operationally proven in one domain. The "beautifully specified but underproven" verdict from the 21 May review is shifting — InnoTriage's multiple real test runs provide genuine evidence the pattern works under load. The 27 May session was particularly productive: four primitives addressed real structural gaps and were implemented cleanly in a single day. Current state: spec-heavy, practice-light, but the ratio is improving.

---

#### What Works Well

1. **The three-layer pattern holds under real use** — InnoTriage proves the Agent → Skills → Things pattern works for a non-trivial domain (innovation triage in a regulated environment). It's running real expert interviews, producing real deliverables, and the git trail is genuinely auditable. This is no longer theoretical.

2. **Tiered startup loading was the right move** — The 75% reduction in context cost for Q&A sessions is significant. More importantly, the insight behind it — that tiered reading already existed for things and just needed application to specs — demonstrates the framework's principles are compositionally sound. The idea bootstraps from its own architecture.

3. **The knowledge primitives are well-designed** — `type: insight`, `type: conflict`, and `type: retrospective` each solve a distinct problem. Insights preserve generative reasoning that would otherwise evaporate. Conflicts make disagreement first-class rather than silently accumulating. Retrospectives provide the aggregate pattern-detection that individual sessions can't. The key design decision — conflicts are not sub-types of insight — is correct; they have fundamentally different semantics (additive vs. rupture).

4. **Hard hooks are honest about what matters** — The three hard hooks (`post-write:commit`, `pre-domain-scaffold:isolate`, `session-end:continuity`) are genuinely non-negotiable invariants. They earn their rigidity. The framework's willingness to say "these three things are always mandatory, everything else is opt-in" is the right posture.

5. **The self-correction habit is strong** — The consistency pass at the end of 27 May Session 4 — catching five bugs and two design gaps — demonstrates healthy hygiene. The framework practices what it preaches: validate, surface issues, fix them, commit.

6. **The manifesto aged well** — Reading it after all the operational specs exist: the philosophical claims hold up. "Humans define domains, LLMs reason within them, git-versioned markdown is the persistent state" is exactly what InnoTriage does. The "build on what exists" philosophy is genuinely lived (AGENTS.md convention, YAML frontmatter, markdown, git). The manifesto doesn't make claims the framework can't back.

---

#### What Doesn't Work Well / Tensions

1. **The domain-specification guide is stale** — Already tracked as an insight, but it's worse than a deferred patch — it's the primary onboarding path. A new domain created today won't know about continuity briefs, insights, conflicts, or retrospectives. For a framework that values "the agent arrives ready," having the bootstrapping guide silently skip the knowledge management layer is a real gap.

2. **InnoTriage is still on `framework_version_seen: 2.3.0`** — The domain hasn't absorbed the 2.4.0–2.5.0 changes. It has no `continuity.md`, no `things/insights/`, no `things/conflicts/`. The `session-end:continuity` hook isn't firing there. The most-exercised domain isn't benefiting from the most recent architectural work. The domain-refresh mechanism exists on paper but hasn't been used.

3. **thing-lifecycle.md is a ghost** — A draft spec at root, not listed in AGENTS.md, not referenced by any other spec. It addresses the most important scaling gap the framework has (the 200–300 thing ceiling) but exists in limbo — neither committed as real nor explicitly deferred in a way the framework's own discovery would find. The one file that breaks the "everything discoverable through AGENTS.md" principle.

4. **The "scheduled invocation" problem remains unresolved** — Time-based triggers (`stale`, `due_date_passed`) only fire during active sessions. This dramatically limits their utility for any domain where things sit for days between sessions. The 21 May review flagged this; it's still an open gap with no specification, no reference implementation, and no explicit acknowledgment in the trigger documentation itself.

5. **Cross-domain composition is still zero** — InnoTriage is the only real domain. When a second real domain exists, you'll immediately hit: how do domains share things? Reference each other? Get composed into a larger view? The framework currently has no answer and no spec for this. Given the "spec when foreseeable" principle, this is foreseeable now.

6. **The framework is spec-heavy, practice-light** — 15 specifications. 1 real domain with 2 completed test runs. Each new spec is internally consistent and well-reasoned, but the framework's experiential evidence base grows much slower than its specification surface area. The system's confidence in its own architecture outpaces external evidence that the architecture delivers value.

---

#### What May Be Over-Engineered

1. **The trigger YAML taxonomy** — Still over-specified for what the evaluator actually is. Four structured trigger types with detailed YAML schemas produce ceremony that a reasoning engine doesn't need. A simpler natural-language conditions array would achieve the same effect — the LLM interprets meaning, not structure. The structure adds friction for domain authors without improving LLM reasoning quality.

2. **The retrospective spec's activation thresholds** — "Write one after 10 conflicts or 20 insights" is precise threshold guidance for something that is fundamentally a judgment call. A retrospective should be written when accumulated experience warrants reflection — that's a human/agent decision, not a rule. The specificity creates false precision and adds a counting obligation that nobody will track.

3. **validate.thing.md's scope** — At v1.2 with four validation levels, 30+ checks, and three severity tiers, it creates an impression of deterministic rigour that doesn't match reality (LLM-performed checks with no consistency guarantee). The Level 4 Semantic Validation checks are particularly aspirational — "contradicts without conflict thing" requires the agent to detect semantic contradiction, which is the hard problem in belief revision, not a validation check.

4. **The orchestration spec's formal prompt/binding model** — The full hook → prompt → binding → domain lifecycle is a general-purpose orchestration engine. InnoTriage uses orchestration (rightly, for its phase-gated workflow), but through skill-level prose, not through formal prompt/binding declarations. The formal model remains unexercised.

---

#### What May Be Under-Engineered

1. **The onboarding experience** — Still no quickstart. The README was rewritten (2.4.0) to be agent-first — good — but a developer discovering this repo still faces manifesto → thing.md → domain-spec-guide → templates, with no "clone this, open it, see it work" moment. The barrier is high for the claimed benefit of "just use existing tools."

2. **Example domains remain skeletal** — Compliance-patterns has a handful of things. Life-manager has zero things. Neither demonstrates triggers firing, validation catching errors, session-end:continuity producing insights, or the system under real use. InnoTriage is the only evidence — and it lives in `domains/`, not `examples/`.

3. **The confidence/origin fields in practice** — Added to thing.md as recommended fields, documented clearly, but not exercised anywhere. No existing thing in the framework or InnoTriage uses `confidence` or `origin` (except the framework's own insights, which adopted them on creation). These fields solve a real problem (LLM trust calibration), but without examples of them in use within a domain, a domain author won't know when to apply them.

4. **Error recovery patterns** — What happens when the agent makes a bad write? When a trigger cascade loops? When two linked things have contradictory states that validation doesn't catch? The framework says "git revert" but specifies no in-session agent behaviour for encountering unresolvable situations. For a system targeting regulated environments (InnoTriage), this matters.

5. **Thing granularity guidance** — thing.md says "large enough to be meaningful, small enough to be actionable" without concrete examples of too-granular or too-coarse. This is where most new users will struggle in practice.

---

#### Missing From WORKLOG Todos

1. **InnoTriage domain refresh to v2.5.0** — The domain is still on `framework_version_seen: 2.3.0`. Needs continuity.md, `things/insights/`, `things/conflicts/`, and the session-end:continuity ritual activated. Should be tracked as an explicit todo.

2. **thing-lifecycle.md status resolution** — Either list it in AGENTS.md as a draft spec (making it discoverable) or explicitly park it with a "deploy when felt" note. Currently invisible to the framework's own discovery mechanisms.

3. **Practical use priority** — The next value likely comes from using what exists (InnoTriage sessions exercising the knowledge primitives), not specifying more. Worth tracking as a directional note.

---

#### Suggested Priorities

1. Refresh InnoTriage to v2.5.0 — make the most-proven domain benefit from the most recent work
2. Update domain-specification-guide.md — close the known gap so new domains get knowledge primitives from Day 1
3. Resolve thing-lifecycle.md's status — make it visible or explicitly park it
4. Write a quickstart — one page, "clone, open, create a domain, see it work"
5. Prioritise InnoTriage sessions over new specs — shift the spec-to-practice ratio

---

#### Reflections

*To be filled in on retrospective review.*

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
- **Private domain references** — The live domain used to validate the framework is private. In this log it is referred to as **InnoTriage** (an innovation triage and production analysis system for a regulated environment). Do not use its real name in public-facing files.
