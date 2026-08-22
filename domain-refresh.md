---
id: domain-refresh-specification
type: specification
status: evolving
version: 1.6
created: 2026-05-19
linked_things:
  - id: a-domain-local-ruling-is-invisible-from-the-centre
    relation: implements
    notes: "The estate-sweep rule below: refreshes run per domain, embodied, because a domain's recorded rulings about an adoption are legible only from inside it. Paid for on 2026-08-23, when one domain's parked kernel-shape decision was found and honoured only by the agent oriented in it."
  - id: framework-discovery-specification
    relation: extends
  - id: git-workflow-specification
    relation: references
  - id: domain-specification-guide
    relation: references
  - id: thing-specification
    relation: references
---

# Domain Refresh

## What This Specifies

This document defines how domain agents discover and absorb framework evolution. It covers three concerns:

1. **Deployment Architecture** — The nested git repository model that enables independent domain versioning within a shared framework
2. **Refresh Process** — How a domain agent checks the framework for changes and updates its own understanding accordingly (the *downward* leg: domain ← local framework)
3. **Upstream Propagation** — How a domain agent surfaces when the *local framework copy itself* is behind its published source (the *upward* leg: local framework ← published source)

## Why This Exists

The framework evolves. New specifications are added (e.g., autocommit mode, triggers, self-describing architecture). Domains created before those additions have no mechanism to discover them — they continue operating with stale assumptions about what the framework offers.

The framework is self-describing: its documentation *is* its functionality. When a domain agent reads updated specs, it gains new capabilities. The refresh process formalises this: it is the mechanism by which domains stay current with the framework they inhabit.

## Deployment Architecture

The framework uses a nested git repository architecture: domain repos live inside the framework directory but maintain independent git histories through `.gitignore` isolation. See `framework-discovery.md` for the full deployment architecture specification, including the nested model, key properties, the `.gitignore` contract, and standalone deployment options.

### The `.gitignore` Contract

The framework's `.gitignore` MUST contain:

```
domains/
```

This is not optional. Without it, domain files would appear as untracked files in the framework repo, creating noise and potentially exposing domain-specific data in framework commits.

## The Refresh Process

### When To Refresh

A domain agent should check for framework updates:

1. **Session start** — via the `session-start:version-check` hard hook (see orchestration.md). By default this fires every session by *interpretation* (no configuration). A registered harness adapter may additionally **harden** it so the ritual is delivered mechanically at t=0 — see *Hardening: harness adapters* below. Selecting or updating an adapter is a separate operator-reviewed action, not an automatic consequence of absorbing a framework version.
2. **On explicit request** — When a user says "check the framework", "update yourself from framework", or similar
3. **On validation failure** — When validation surfaces things that don't conform to current spec definitions, a refresh may explain why

### What To Check

The refresh process reads these framework files in order:

| File | Purpose | What To Look For |
|------|---------|------------------|
| `CHANGELOG.md` | What shipped | New features, breaking changes, new specs added |
| `mdllm worklog` (git log view) | How it evolved | Recent session context, decisions made, direction |
| Foundational specs | Current definitions | Version bumps, new sections, changed behaviour |
| `AGENTS.md` | Framework self-description | New skills listed, new spec types, updated workflows |

> **Note:** The version *detection* step (reading `.markdownllm` and comparing to `framework_version_seen`) is handled by the `session-start:version-check` hard hook before the refresh process begins. The steps below assume a mismatch has already been confirmed.

### The Refresh Algorithm

```
1. (Already done by hard hook) Version mismatch confirmed:
   → domain framework_version_seen < {framework_root}/.markdownllm version
   → validate.thing.md was run against domain things; findings reported to user

2. Read {framework_root}/CHANGELOG.md
   → Identify entries newer than framework_version_seen
   → Flag: new specifications, breaking changes, new capabilities

3. Run `mdllm worklog {framework_root}` (or `git -C {framework_root} log`) — recent sessions only
   → Understand current framework direction and recent decisions

4. Scan foundational specs for version changes:
   → the specs named in {framework_root}/.markdownllm `foundational_specs`
     (the sentinel is the catalog — orchestration.md included; a list
     hand-maintained here drifted, omitting the spec that carries the
     hard hooks)
   → Any NEW specs not previously known

5. Compare against domain's current understanding:
   → Does the domain AGENTS.md reference capabilities it doesn't use?
   → Are there new framework features the domain should adopt?
   → Are there breaking changes that require domain updates?

6. Report findings to the user:
   → New capabilities available
   → Breaking changes requiring action
   → Recommended updates to domain skills or AGENTS.md

7. If authorised, update domain files:
   → Update domain AGENTS.md to reference new framework capabilities
   → Run `mdllm domain-kernel .` through the manual CLI launch route in the
     domain's on-disk AGENTS.md — the
     absorbed version may have changed the generated managed blocks, and
     the domain's own pre-commit coherence check flags drift until the
     regen is committed
   → Update domain skills to use new patterns
   → Commit with message: refresh: absorbed framework v{version} changes
   → (operator step) inspect any selected harness independently:
     `mdllm doctor . --harness <name>`
   → if that adapter owns project artifacts, review its exact proposed diff:
     `mdllm adapter-install . --harness <name> --dry-run`
     Apply only after review; when doctor names an exact legacy ID, add
     `--refresh-legacy` to both the dry run and the reviewed apply.
   → (backfill) a domain born before a scaffold artifact existed never
     received it — refresh is where it catches up. Check and backfill:
     · pre-v3.20.0 births: the disclosure boundary (.boundary-terms from
       templates/boundary-terms.template, gitignored) and a domain .gitignore
     · pre-v3.24.0 births: prompts/ (templates/prompts/ — the reasoning
       prompts the generated session-start block names) and the `types`
       managed block in AGENTS.md (templates/AGENTS.md.template shows
       placement; `mdllm domain-kernel .` fills it). Do not infer project
       adapter state from the birth version; inspect the selected harness
       through doctor and the renderer-backed install flow above.
     · pre-v3.30.0 births: the prompt templates changed (fired/upcoming
       split, import triggers, terminal-status wording — the substrate
       reconciliation) — diff the domain's prompts/ against
       templates/prompts/ and re-adopt; the tier-routing managed block now
       routes prompts/, so the domain-kernel regen above is not optional
```

### Refreshing The Estate: Per Domain, Embodied

When several domains are refreshed in one operation, run each **as that
domain's agent in its own context** — reading its `AGENTS.md`, orienting
through its own session-start — never as a loop over directories from the
framework root. Two reasons, both paid for on 2026-08-23:

1. **A domain can record a decision that changes what the correct step is.**
   One domain carried an operator ruling parking kernel-shape adoption with
   an explicit unpark condition; only the agent oriented inside it saw the
   ruling, skipped the regeneration, and named the skip in its commit. A
   central loop would have overwritten the decision with every mechanical
   check still reporting clean (`a-domain-local-ruling-is-invisible-from-the-centre`).
2. **Sequential embodiment in one context degrades into a composite.** By the
   ninth domain, an agent holding the previous eight is no longer reading the
   ninth. Parallel isolated contexts are both faster and more faithful.

Practical shape: one agent per domain, each given the walk and the hard
constraints (no adapter installs — that boundary stays the operator's; no
manual pushes; never `--no-verify`); each reports status back; the
coordinating session verifies seals and publication afterwards. Also
reinstall the domain's hooks in the same pass when a policy change depends
on them (`a-declaration-is-inert-until-its-mechanism-is-current`), and
rebuild derived indexes in dependency order — an index that is itself a
thing (`triggers`) must be rebuilt *before* the indexes that must cover it
(`schema`), or the first commit attempt is blocked by drift the rebuild
itself created.

### Hardening: Harness Adapters (Operator, Optional)

The adapter registry projects the framework's neutral lifecycle intents onto
specific harness surfaces. Claude Code and Codex are **project-bound** adapters:
their renderers produce path-instantiated, definition-hash-bound project
artifacts. Cowork is **run-time bound**: its registered adapter renders no
project artifact and binds through an account-level bundle when a session
activates it. Registration is a capability statement, not live compatibility
evidence; each public execution claim still names the exact product surface
and record that earned it.

For an existing domain, start read-only:

```text
mdllm doctor . --harness <name>
mdllm adapter-install . --harness <name> --dry-run
```

`doctor` keeps support, project configuration, currency, trust, runtime, and
real-event execution independent. For a project-bound adapter, the second
command is the operator's mutation boundary: it shows the renderer-owned diff
and applies nothing. Run it without `--dry-run` only after review. If doctor
recognises an exact historical managed span it names the legacy ID and the
additional `--refresh-legacy` flag; unknown stale forms, extensions, and
ambiguity refuse rather than being overwritten. A run-time-bound adapter has
no project install target, so project configuration and currency are reported
as not applicable; its bundle/bootstrap plan owns installation and live proof.

An agent may report these facts and prepare the review, but it must not
self-install a permission-bearing project adapter. The operator invokes or
approves the reviewed mutation (see
`things/insights/agents-cannot-self-install-permission-bearing-hooks.md`). Never
paste or hand-edit a generated hook block, and never adjust a copied Python
path: the renderer and the repository's manual CLI launch route own both.
Claude Code lifecycle evidence and VS Code Copilot lifecycle compatibility are
separate claims even where their surrounding project files or shortcuts
overlap.

Every adapter remains optional. With no adapter, the entry contract and Git
floor still operate; hardening removes reliance on interpretation for only the
lifecycle moments the selected harness actually binds.

### What The Domain May Update

After a refresh, the domain agent may modify:

- **Domain AGENTS.md** — Add references to new framework capabilities, update startup sequence
- **Domain skills** — Incorporate new patterns (e.g., adding trigger evaluation when triggers were added to the framework)
- **The refresh commit** — Record what was discovered and adopted in a rich commit message (the backward record is git)

The domain MUST NOT modify:

- Framework files (read-only relationship)
- Domain things (refresh is about capabilities, not data)
- Harness project artifacts such as `.claude/settings.json` or
  `.codex/hooks.json` (operator-owned and potentially permission-bearing; the
  agent surfaces `doctor` plus the renderer-backed dry run, and the operator
  invokes or approves any apply)

### Version Tracking

To know whether a refresh is needed, the domain tracks the last-known framework version via the `framework_version_seen` field in its AGENTS.md frontmatter:

```yaml
---
name: My Domain
framework_root: ../..
framework_version_seen: 3.4.0   # copy the version field from {framework_root}/.markdownllm
---
```

**The canonical version source is `{framework_root}/.markdownllm`.** This is a tiny file; domain agents read only its `version` field at session start (via the `session-start:version-check` hard hook). They do not read CHANGELOG.md to detect a mismatch — that would waste context on every session regardless of whether anything changed.

When `framework_version_seen` is lower than the `.markdownllm` version, a refresh is indicated. The hard hook surfaces this automatically and triggers validation. If this field is absent from a domain's frontmatter, treat the domain as fully stale — run a full refresh and add the field afterward.

This specification is foundational — it defines the *what* and *why* of domain refresh. Domain agents operationalise it through their workflow skill.

### Integration Point: Domain Workflow Skill

The domain's `[domain]-workflow.skill.md` should include a **Refresh** workflow that implements this specification. The workflow skill template should add:

```markdown
## Refresh Workflow

### Trigger
- Session start (as part of orientation)
- Explicit user request: "check framework", "refresh from framework", "what's new in the framework"

### Steps
1. Resolve `framework_root` from AGENTS.md frontmatter
2. Read `{framework_root}/CHANGELOG.md` — identify entries after `framework_version_seen`
3. Run `mdllm worklog {framework_root}` (on-demand view of git) — recent sessions only
4. Scan foundational spec versions (thing.md, git-workflow.md, etc.)
5. Compare: what does this domain not yet use that the framework now offers?
6. Report to user with recommendations
7. If authorised: update domain AGENTS.md and skills
8. Update `framework_version_seen` in domain frontmatter
9. Commit: `refresh: absorbed framework v{version} changes`

### Commit Convention
- `refresh: absorbed framework v{version} changes`
- `refresh: updated skills for {capability}`
```

### Integration Point: Domain AGENTS.md

In a scaffolded domain, refresh awareness is already part of the **generated
Session Start block** (`mdllm domain-kernel`) — step 3 of that block is the
version check, and the block is the canonical startup sequence (this spec no
longer carries its own competing enumeration; the 2026-08-09 substrate
reconciliation retired four such restatements). The upward leg — local
framework vs its cached upstream — is one advisory, non-blocking line, and
`mdllm doctor` is its deliberate fetch-and-recheck home.

## Upstream Propagation (The Upward Leg)

The refresh process above is the *downward* leg: it keeps a domain current with the framework copy it inhabits. There is a symmetric concern one hop up the chain — *is the local framework copy itself behind its published source?* A framework that versions daily can drift weeks ahead of any given install, and today operators coordinate that update by hand.

The fix is the same primitive, applied upward, and it is deliberately the **softest** of the version checks:

- **Advisory, not blocking.** The downward leg protects *integrity* — stale assumptions can produce invalid things, so it validates before proceeding. The upward leg protects nothing; it only *coordinates humans*. It therefore surfaces a notification and lets the operator (the domain's expert) decide. It never gates a session.
- **Cached, not live.** The check compares the local `.markdownllm` version against git's already-fetched remote-tracking copy (`git show origin/main:.markdownllm`). The check itself never requires the network — a session start that cannot complete without connectivity is the `portability-claims-need-execution-tests` trap. The precise rule (orchestration.md, sharpened with `session-start:estate-sync`): a *required* network call at session start is forbidden; a bounded, degrade-gracefully fetch attempt is permitted — where `estate-sync` runs first, this check reads the tracking refs sync just refreshed. `mdllm doctor` remains the deliberate fetch-and-recheck home.
- **Surfaced at session start.** The `session-start:version-check` hard hook (orchestration.md) runs both legs. The upward result is one advisory line when the local framework is behind: *"Local framework is v{local}; published upstream is v{upstream} (as of last fetch) — consider pulling."*

### Mechanisation

`mdllm doctor`, run at a framework root, reports the upstream leg directly: it reads the local sentinel, reads the cached upstream sentinel via `git show`, and prints OK / WARN / `--` (unknown — no fetched copy). It is the natural home for a deliberate fetch-and-recheck, because `doctor` is already the floor's "probe the environment" command and already reports the *downward* drift for wired domains.

This leg intentionally adds no new persistent state and no new sentinel field: the local `.markdownllm` is the only version surface, and git's remote-tracking refs are the cache.

## Relationship To Other Specifications

- **framework-discovery.md** — Defines *how* domains find the framework. This spec defines *what domains do* once they've found it and it has changed.
- **git-workflow.md** — Provides the session-start orientation pattern that refresh extends. Also defines the commit conventions refresh uses.
- **domain-specification-guide.md** — The guide for creating domains. Should reference this spec as the mechanism for keeping domains current.
- **thing.md** — Foundational spec. When its version changes, domains need to know.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|---------------|------------------|
| Domain auto-refreshes silently | User loses visibility of what changed | Always report findings before modifying |
| Domain modifies framework files | Violates read-only relationship | Domains only read framework; humans evolve framework |
| Refresh rewrites domain things | Conflates capability updates with data changes | Refresh updates skills and AGENTS.md only |
| Skipping CHANGELOG, reading only specs | Misses context, breaking changes, and intent | CHANGELOG is the primary signal; specs are verification |

## Example: A Domain Discovers Autocommit

Before refresh, a domain's AGENTS.md says:
```markdown
### On Output
1. Validate thing files
2. Report what changed
```

The framework added autocommit mode in v2.1.0. After refresh:

```markdown
### On Output
1. Validate thing files
2. **Autocommit** (if `git.autocommit: true`): stage + commit with structured message
3. Report what changed
```

The domain gained a capability by reading updated framework specs and updating its own operational definition. The documentation *was* the upgrade.
