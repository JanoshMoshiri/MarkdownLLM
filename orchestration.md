---
id: orchestration-specification
type: specification
status: evolving
version: 1.13
created: 2026-05-20
linked_things:
  - id: thing-specification
    relation: extends
  - id: estate-git-sync
    relation: informs
    notes: "Hard hook 4 (session-start:estate-sync) and the sharpened network-call rule landed from this plan"
  - id: write-thing-specification
    relation: complements
  - id: git-workflow-specification
    relation: complements
  - id: interface-specification
    relation: complements
  - id: llm-driven-systems-manifesto
    relation: implements
  - id: session-memory-specification
    relation: implements
  - id: belief-revision-specification
    relation: implements
  - id: trigger-specification
    relation: complements
  - id: domain-refresh-specification
    relation: implements
  - id: derived-index-specification
    relation: complements
---

# Orchestration

<!-- kernel -->
**Hard hooks — always active by config (enforcement depends on anchor — see below):**
1. `post-write:commit` — after creating/modifying any frontmatter `.md`, commit to the **owning repo** (walk up to the nearest `.git`) before completing the response. The git pre-commit hook (`mdllm install-hook`) mechanically validates on the way in and surfaces the change-reconciliation advisories (cue candidates, serve-side publication notices — advisory, never blocking). **The publication leg:** the post-commit hook then publishes the validated commit (`mdllm autopush`) unless the repo declares `git: autopush: false` (absence = on; release surfaces opt out). Bounded, never forces; a rejected push is divergence on the push side — surfaced, never resolved (`autopush-moves-the-deliberate-act`).
2. `pre-domain-scaffold:isolate` — new domain, in order: `git init` in domain dir → add path to framework `.gitignore` → commit `.gitignore` to framework → commit domain files to domain repo → create remote + push. Never commit domain files to the framework repo. Mechanised: `mdllm scaffold <path>` performs steps 1–4 plus templates and hook; the remote stays human.
3. `session-start:version-check` — two directions, both at session start. **Downward** (domain ← local framework): read `{framework_root}/.markdownllm` version vs `framework_version_seen`; on mismatch surface, run validation, offer `domain-refresh.md`. **Upward** (local framework ← published source): compare the local `.markdownllm` version against the *cached* upstream version (git's remote-tracking state, e.g. `git show origin/main:.markdownllm` — the check itself never requires the network); if behind, surface an **advisory, non-blocking** notice for the operator to act on. `mdllm doctor` reports both.
4. `session-start:estate-sync` — sync before orienting (orientation reads the log sync updates): `mdllm estate-sync` walks root + `domain(s)/*` repos — `git fetch` + `pull --ff-only`, bounded, `GIT_TERMINAL_PROMPT=0`, degrading offline to an advisory line. Reports per repo: synced/up-to-date/ahead-unpushed/DIVERGED/offline/dirty/local-only. Divergence and dirty trees reported, never resolved; never pushes, never merges. Session end: `estate-sync --status` reports publication debt (unpushed commits). A *required* network call at session start stays forbidden; this is a bounded attempt, not a gate.

**Anchor decides enforcement (the primary axis); hard/soft is only config.** Every hook has one **anchor** — the surface that makes it fire: `interpretation` (the agent reads the entry file and acts — portable across every harness, *not* mechanically enforced, the default and sufficient for correctness), `git-fs` (a real git/filesystem mechanism fires — mechanical, universal), or `harness-session` (a harness lifecycle event — enforced only if a per-harness adapter binds it). `hard`/`soft` is config only — always-on vs opt-in — and does **not** imply enforcement: a `hard` + `interpretation` hook is exactly as skippable as a soft one, and is a hardening candidate. Hardening = moving a hook's anchor rightward without touching hard/soft: the **git pre-commit hook** (`mdllm install-hook`) makes validation `git-fs`; optional **per-harness adapters** (`adapters/`) bind `harness-session` hooks to real events. Adapters stay optional — never the difference between working and not.

**Soft orchestration (opt-in per domain):** hook points (session-start, session-end, pre-commit, post-commit, post-write, on-create, on-status-change, on-error, retrospective + domain-defined) · prompts (`type: prompt` — one focused reasoning task) · bindings (`{hook, when?, invoke: [prompts...], anchor?}` in AGENTS.md or workflow skill; declaration order = execution order; `anchor` defaults to `interpretation`).

**Domain hard hooks:** `hard_hooks: [{hook, action, anchor?}]` in domain AGENTS.md — e.g. derived-index maintenance on `post-write` (the maintenance *act* is `interpretation` — nothing mechanical fires on a file write; the `git-fs` part is the pre-commit drift check that catches a stale index at the boundary. Label the act, not its net: a `git-fs` label on an interpretation act licenses skipping work the machine does not do).

**Restraint:** a prompt is a checklist, not a procedure manual; >10 domain prompts = over-specification; don't bind what narrative prose already handles reliably.
<!-- /kernel -->

## What This Specifies

This document defines the orchestration pattern — an **opt-in** tool for domains that need structured reasoning flow beyond what the framework's narrative specs naturally provide.

Orchestration introduces three primitives:

1. **Hook points** — Named moments in the lifecycle where reasoning can be attached
2. **Prompts** — Reusable reasoning templates smaller than skills, more structured than trigger actions
3. **Bindings** — Declarations that connect hook points to prompts

## Enforcement: Three Anchors, Not Two

The hard/soft distinction (next section) is about *configuration* — always-on vs
opt-in. Orthogonal to it, and more important for portability, is a second
question: **what actually makes a hook fire?** Every hook in this spec anchors to
one of three surfaces, and the surface — not the label — decides whether the hook
is enforced and whether it survives a change of harness.

| Anchor | Fires because | Enforced? | Portable? |
|---|---|---|---|
| **Agent interpretation** | the agent reads the entry file (`AGENTS.md`) and acts on the prose | No — relies on the agent | ✅ Universal — every harness loads an entry file and runs an LLM over it |
| **Git / filesystem** | a real mechanism fires (git `pre-commit` hook, a file write) | Yes — mechanical | ✅ Universal — git is present under every harness |
| **Harness session lifecycle** | the harness decides a "session" started or ended | Only if an adapter binds it | ❌ Differs per harness |

**Interpretation is the default, and it is sufficient for correctness.** The
framework was built and run end-to-end under GitHub Copilot before it ever touched
Claude Code; the agent read `AGENTS.md` and executed the prose. *That* is the
portability layer — not git, not any vendor hook. A domain with zero adapters and
zero mechanical hooks still works, because the universal substrate under every
harness is an LLM reading the entry file.

**Hardening is optional, and it is the same move twice.** Where being wrong is
unrecoverable, trade "the agent should" for "the machine guarantees":

- The **git pre-commit hook** (`mdllm install-hook`) hardens validation. It needs
  no adapter because git is universal — which is why the one genuinely
  load-bearing hook (`pre-commit` validation) is also the one that never has to
  know which harness it runs under.
- A **per-harness adapter** (`adapters/`) can harden the session-lifecycle hooks
  by binding them to real harness events (Claude Code's `SessionStart`, `Stop`,
  `PostToolUse`; the equivalent elsewhere). `adapters/claude-code.settings.example.json`
  does exactly this for `post-write` validation.

If a hook can only be hardened by an adapter and you write no adapter, it falls
back to interpretation — which is where it started, and where the framework
already works.

### The Distribution

Every hook and prompt, by anchor. Read the last column to see why interpretation
is safe for almost all of them: git reconstructs state, and validation catches
drift later, so a skipped hook degrades gracefully rather than corrupting.

| Hook / Prompt | Anchor | Enforced by today | If the agent skips it |
|---|---|---|---|
| `pre-commit` validation | git/fs | ⚙️ git hook (mechanical) | **Can't** — commit is blocked |
| `post-write:commit` (the commit act) | interpretation | the agent (git hook validates *if* a commit happens) | **Severe** — work stranded in the working dir |
| `pre-domain-scaffold:isolate` | git/fs | ⚙️ `mdllm scaffold` | Moderate — repo pollution, needs cleanup |
| `session-start:version-check` | interpretation → harness-session (adapter) | interpretation | Low — stale version; validation catches breaks later |
| `session-start:estate-sync` | interpretation → harness-session (adapter) | interpretation (adapters bind it where installed) | Moderate — orientation reads a stale log; an unpulled checkout orients on a past domain |
| `session-start`, `session-end` | harness-session | interpretation | **Moderate** — the state is regenerable from git, but the session *acts on the misread live*: two 2026-08-08 field incidents (an orientation the operator could not follow; a write made without the workflow skill's authorisation step) trace to skipped session-start steps |
| `post-write` | interpretation (act) — git-fs is only the pre-commit drift net | interpretation (`PostToolUse` adapter exists) | Moderate — cascades missed |
| `post-commit` | git/fs | ⚙️ git hook (mechanical — `mdllm autopush`, the publication leg; v3.26.0) | Low — publication debt, surfaced by `estate-sync --status` |
| `on-create`, `on-status-change`, `on-error`, `retrospective` | interpretation (semantic) | interpretation — no mechanical detector possible | Moderate — downstream not cascaded |
| reasoning prompts (`cascade-completion`, `evaluate-triggers`, `surface-attention`, `detect-conflicts`, `session-orientation`, `domain-velocity`, `review-schema-coherence`, `session-end-continuity`) | interpretation | interpretation — they *are* reasoning | Low–Moderate |

Two consequences fall out:

1. **Three git hooks are mechanically enforced today** (`mdllm install-hook`):
   `pre-commit` validation + coherence (blocks), the `commit-msg` disclosure
   boundary (blocks), and `post-commit` autopush (publishes, never blocks). The
   two blocking legs are the ones with unrecoverable consequence — the floor
   still guards exactly what must never be wrong, and the publication leg only
   transports what the blocking legs passed. *(This consequence said "only
   pre-commit" for four releases after the other two legs landed — a
   review-loop finding; the table above is the census, and it was wrong too.)*
2. **Adapters touch only the session-lifecycle rows**, the lowest-consequence rows
   in the table. Keeping adapters optional is not a compromise — it is what keeps
   MarkdownLLM a portable *substrate* rather than a harness-specific tool. The
   moment an adapter became *required*, the framework would stop being
   harness-agnostic.

## Hard Hooks vs Soft Hooks

All hooks described in this document — the bindings, prompts, and domain-level hook points — are **soft hooks**: opt-in, configured per domain, active only when a binding explicitly declares them. A domain that omits orchestration entirely continues to work fine; the narrative specs guide the LLM through reasoning without structural enforcement.

Some behaviors, however, are fundamental to the framework's integrity regardless of domain, configuration, or context. These are **hard hooks** — non-negotiable procedures that fire unconditionally. No binding declaration is needed. No domain configuration enables or disables them. They are part of the agent's standing operating contract with the framework.

### The Distinction

| | Soft Hook | Hard Hook |
|---|---|---|
| **Activation (config)** | Requires a binding declaration | Always active — no configuration needed |
| **Always runs?** | Only if bound | Always *attempted* — never config-disabled |
| **Enforced?** | Depends on **anchor**, not this column | Depends on **anchor**, not this column |
| **Defined by** | Domain AGENTS.md or workflow skill | Framework AGENTS.md |
| **Purpose** | Domain-specific structured reasoning | Framework integrity invariants |

**Hard/soft is the *config* axis — always-on vs opt-in. It says nothing about
enforcement.** Whether a hook actually fires is decided by its **anchor** (see
*Enforcement: Three Anchors, Not Two* above). A `hard` hook anchored to
`interpretation` is always *meant* to run but is skippable in practice until hardened
— which is precisely why the two axes must be read together and never conflated. The
old reading ("hard = never skippable") collapsed them and hid the gap.

### Framework-Level Hard Hooks

These four hard hooks are part of every agent's operating contract with the framework. They fire regardless of whether a domain uses orchestration.

#### `post-write:commit` — Commit Every Thing

**When it fires:** After any `.md` file containing YAML frontmatter is created or modified.

**Anchor:** split — the *commit act* is `interpretation` (only the agent decides to commit), while the validation it triggers is `git-fs` (the pre-commit hook). The act is the hookable-but-skippable half; validation is the mechanical half.

**What must happen:**
1. Identify the owning git repository — walk up the directory tree from the modified file until a `.git` directory is found
2. Stage the modified files: `git add` from that repo's root
3. Commit with a structured message following git-workflow.md conventions
4. Do not complete the response without this step

**Why it's hard:** Git is the framework's state machine. An uncommitted change is a change that doesn't exist yet — the "single source of truth" principle is violated by any thing that exists only in a working directory. This cannot be left to convention or memory.

**Mechanical backstop (v3.0):** the commit boundary is also where the deterministic floor fires — the git `pre-commit` hook (installed via `python tools/mdllm.py install-hook`) runs full mechanical validation and blocks the commit on any Error. The agent does not enforce structural/referential integrity by diligence; the hook does it by construction. See `validate.thing.md` v2.0.

**What failure looks like:** Thing files created in a session but never committed. State that exists in files but not in history. The session ends and the work is only partially real.

#### `pre-domain-scaffold:isolate` — Every Domain Gets Its Own Repo

**When it fires:** When creating a new domain — specifically, when generating a new `AGENTS.md` in a new directory under the framework.

**Anchor:** `git-fs` when run via `mdllm scaffold` (mechanical, exits non-zero on a broken sequence); `interpretation` if performed by hand — the *ordering* is the invariant either way.

**What must happen, in order:**
1. `git init` inside the new domain directory — before any domain files are committed anywhere
2. Add the domain's path to the framework's `.gitignore` — immediately, as part of the same operation
3. Commit the `.gitignore` change to the framework repo — so the framework never tracks the domain
4. Commit the domain files to the domain's own repo
5. Create a remote repository and push

**Mechanised by the `scaffold` subcommand:** `python tools/mdllm.py scaffold <path>` performs steps 1–4 deterministically (plus instantiated templates and the pre-commit hook), and exits non-zero if any step of the sequence fails — running it is the canonical way to satisfy this hook. Step 5 (the remote) stays with the human. The hook still binds when scaffolding by hand: the *ordering* is the invariant, not the tool. (Spec prose does not name framework versions — the sentinel is the only version surface; a hand-written "since vX.Y" drifted here within hours of being written.)

**Why it's hard:** The nested repo isolation pattern is architectural. Domain git history must never appear in framework git history. If domain files are committed to the framework repo first, the separation is compromised — undoing it requires a soft reset, a `.gitignore` update, and re-committing to the right repo. Friction that is entirely avoidable if the isolation happens upfront.

**What failure looks like:** Domain AGENTS.md and skills appearing in `git log` of the framework repo. A remediation session required just to restore the correct structure.

#### `session-start:version-check` — Check Framework Version Before Every Session

**When it fires:** At the start of every session where the agent has `framework_root` declared in its AGENTS.md frontmatter.

**Anchor:** `interpretation` by default; hardened to `harness-session` where a per-harness adapter binds the session-start lifecycle event — the same rule as its sibling `estate-sync` hook, stated the same way (a review-loop finding caught the two session-start hooks carrying inverted default labels with no distinguishing principle; the principle is now uniform: an unadapted session-start hook's operative anchor IS interpretation, and `harness-session` names what an adapter provides, never a default). This remains the framework's prime case of a `hard` hook whose anchor is not mechanically enforced, and the canonical hardening target (see `adapters/`).

This hook checks version drift in **two directions** along the same chain — *published source → local framework → domain*. The downward leg keeps a domain current with the framework copy it inhabits; the upward leg tells the operator when that framework copy is itself behind its published source.

**Downward leg — domain ← local framework (blocking-class: validate before proceeding):**
1. Read `{framework_root}/.markdownllm` — extract the `version` field only (first few lines; tiny file)
2. Compare against `framework_version_seen` in the domain's own AGENTS.md frontmatter
3. If `framework_version_seen` is absent: treat as fully stale — surface to user and offer a full refresh
4. If versions match: proceed normally, no further action
5. If versions differ (framework is newer):
   a. Surface to user: "Framework has updated to v{framework_version} — this domain is on v{framework_version_seen}"
   b. Load `{framework_root}/validate.thing.md` and run validation against all domain things — this catches breaking changes before the session proceeds
   c. Report validation findings to the user
   d. Offer a full refresh via `{framework_root}/domain-refresh.md`

**Upward leg — local framework ← published source (advisory, cached, non-blocking):**
1. Read the local `{framework_root}/.markdownllm` `version`
2. Compare against the *cached* upstream version — git's existing remote-tracking knowledge, read without a network call: `git show origin/main:.markdownllm` (or the configured upstream ref). **The check itself must never require the network** — a session start that cannot complete without connectivity is the `portability-claims-need-execution-tests` trap. The precise rule (shared with `session-start:estate-sync` below): a *required* network call at session start is forbidden; a *bounded, degrade-gracefully* fetch attempt that improves the cached state when the network exists is permitted — and where `estate-sync` runs first, this check reads the tracking refs that sync just refreshed.
3. If the local framework is behind: surface a single advisory line — "Local framework is v{local}; published source is v{upstream} (as of the last fetch) — consider pulling before this session." Then proceed. This is a **notification, not a gate**: the operator decides whether to update.
4. If equal, ahead (unpublished local work), or the upstream ref is unavailable: stay silent (or note "upstream unknown — no recent fetch" only when asked).

`mdllm doctor` reports both legs and is where a deliberate `git fetch` + re-check belongs.

**Why it's hard:** Domains operating on stale framework assumptions may produce invalid things or miss capabilities that now exist. A version mismatch is a known-unknown — the domain knows it doesn't know what changed. Running validation immediately on the downward mismatch ensures existing things remain compliant under updated spec definitions before any new work begins. The upward leg is softer by design — it coordinates humans, it does not protect integrity — so it advises rather than blocks. Catching both at session start, not mid-session, is the only reliable way to surface them.

**Context cost:** Minimal. `.markdownllm` is a tiny file; the upstream read is a single `git show` against already-fetched objects. `validate.thing.md` is only loaded when a downward mismatch is confirmed — not on every session.

**What failure looks like:** A domain continues operating on a stale framework version; or a framework copy silently lags its published source for weeks while operators coordinate updates by hand.

#### `session-start:estate-sync` — Sync the Estate Before Orienting

**When it fires:** At the start of every session, before orientation — at a framework root with nested domain repos, in any single domain worked from more than one machine, and in cloud sessions over a fresh clone (where it is a cheap no-op).

**Anchor:** `interpretation` by default; hardened to `harness-session` where an adapter binds it (e.g. a SessionStart hook running `mdllm estate-sync .` *before* `mdllm session-start .` — ordering is the point: orientation reads the log that sync updates).

**What must happen:**
1. Walk the repos: the root repo plus immediate children of `domain/` / `domains/` that contain `.git` (explicit paths override the walk). This discovery is legitimate where `estate-check`'s is not: the objects here are *repos and their own remotes* — a filesystem walk reveals nothing `ls` doesn't and touches no membrane. Batching-never-an-index still binds: stdout-only, ephemeral, nothing persisted.
2. Per repo: `git fetch` (bounded timeout, `GIT_TERMINAL_PROMPT=0` — never prompt, never hang), then `git pull --ff-only` — full inbound rules in git-workflow.md → The Machine Axis.
3. Report one line per repo: `synced (+n)` / `up-to-date` / `ahead +n (unpushed)` / `DIVERGED (+a/+b)` / `offline` / `dirty` / `local-only` / skipped-state. Divergence and dirty trees are **reported, never resolved** (`divergence-is-an-unrouted-decision`).
4. If any domain moved, advise `mdllm estate-check` over the moved consumers — pulled source commits can flip imports stale/diverged. Advise only; the membrane check stays deliberate.

**Mechanised by `mdllm estate-sync`.** Session end runs the mirror: `estate-sync --status` (no network) reports publication debt — unpushed commits the estate cannot see.

**Why it's hard:** Orientation reads committed state, and in a multi-machine estate committed state partly lives on the remote. A session that orients without syncing reads a stale event stream *silently* — velocity, triggers, and verified-flip surfacing all quietly wrong. The worst outcome of a failed sync is orienting from stale state *and being told so*, which is strictly better than the alternative this hook replaces.

**Why it never blocks:** the network-call rule above — a required network call at session start is forbidden; this hook is a bounded attempt that degrades to an advisory line and proceeds. It never pushes and never merges — publication is the post-commit autopush leg's job, not the sync walk's (git-workflow.md → The Outbound Rules; release surfaces keep the deliberate act).

**What failure looks like:** Two machines each "up to date" in their own eyes, drifting for days; the eventual collision surfacing as a surprise merge conflict instead of a routine `DIVERGED` line at session start; a cloud session planning work the local machine already did.

### Declaring Domain-Level Hard Hooks

Domains can declare their own hard hooks in their AGENTS.md using a `hard_hooks` block. A domain hard hook is a behavior that must fire for that domain's integrity, regardless of context.

```yaml
hard_hooks:
  - hook: session-end
    action: "Commit a rich session-end: message before the session closes (the commit is the backward record)"
  - hook: post-write
    action: "After updating any return thing, check if its companion deadline thing needs updating"
```

Domain hard hooks are scoped to that domain only. They do not propagate to the framework. They are the domain's standing operating procedures — behaviors the domain agent must always perform, with no exceptions.

**Derived index maintenance is declared this way.** A domain that adopts a derived index (see `derived-index.md`) keeps it current by attaching maintenance to the `post-write` event — the one observable, agent-caused moment when the agent is already looking at the changed thing:

```yaml
hard_hooks:
  - hook: post-write
    action: "If the written thing has triggers, update things/_index/triggers.md in the same commit"
  - hook: post-write
    action: "If the written thing introduces a frontmatter field absent from things/_index/schema.md, register it in the same commit"
```

This is deliberately a *domain-level* hard hook, not a new framework-level one: indexes are opt-in and scale-triggered, so the obligation exists only for domains that have chosen to maintain an index. Incremental maintenance is backed by full rebuild — validation (`validate.thing.md` → Index Integrity) detects any drift and the index is regenerable from the things at any time.

---

## When To Use Orchestration

Orchestration is **not mandatory**. The framework's narrative specs (write.thing.md, thing.md triggers, validate.thing.md) already guide LLM reasoning effectively through prose. LLMs naturally calibrate effort from narrative instruction — they reason about whether something is relevant, how deep to go, and whether the context warrants it.

**Use orchestration when:**
- Your domain has strict phase-gated workflows (e.g., compliance, regulated environments)
- Consistency matters more than flexibility (multi-person teams, audit requirements)
- Specific high-consequence moments must never be skipped (pre-deployment checks, approval gates)
- You need repeatable, documented reasoning that fires identically every time

**Don't use orchestration when:**
- Narrative prose in skills and specs is sufficient for the LLM to reason correctly
- Your domain is exploratory or evolving quickly
- Rigidity would slow down natural reasoning and iteration
- The LLM already handles the reasoning well without explicit structure

The difference: narrative prose is a *nudge* — the LLM decides how much attention to pay. A bound prompt is a *procedure* — the LLM executes it completely. Choose accordingly.

## The Primitives

### Why A Separate Specification

Triggers in `thing.md` answer: "When should this *thing* get attention?"

Orchestration answers: "When something happens *anywhere in the system*, what reasoning should fire?"

The distinction is scope. A trigger is scoped to one thing — it watches conditions relevant to that thing. Orchestration is scoped to the *flow* — it watches lifecycle events and binds reasoning to them. A trigger might say "when my dependency completes, surface me." A hook point says "whenever *any* thing completes, evaluate downstream cascades."

Keeping this separate preserves single responsibility:
- `thing.md` — what a thing is
- `orchestration.md` — how reasoning flows between things

## Hook Points

A hook point is a named moment in the system lifecycle where reasoning can be attached. It's not code. It doesn't execute anything. It's a **declared opportunity** — a moment where the agent checks: "Is there a prompt bound to this moment? If so, invoke it."

### Framework-Level Hook Points

These exist in every domain. They fire based on framework mechanics, not domain logic.

The **Anchor** column is the default surface that fires each point (a binding may
harden it rightward via an adapter): `interpretation` relies on the agent reading the
entry file; `git-fs` fires on a real git/filesystem event; `harness-session` fires only
if a per-harness adapter binds the lifecycle event (otherwise it falls back to
interpretation).

| Hook Point | When It Fires | Available Context | Operative Anchor (→ hardened) |
|------------|---------------|-------------------|------------------|
| `session-start` | Agent loads and discovers AGENTS.md | All things, git log since last session | `interpretation` → `harness-session` (adapter) |
| `session-end` | Before the session closes | All modified things, uncommitted changes | `interpretation` → `harness-session` (adapter) |
| `pre-commit` | After changes are staged, before `git commit` | Staged files, changed thing metadata | `git-fs` |
| `post-commit` | After a successful commit | Commit message, changed thing IDs, diffs | `git-fs` |
| `post-write` | After any thing is modified (before commit) | Modified thing, its linked_things, triggers | `interpretation` (act) — the pre-commit drift check is the `git-fs` net beneath it; a `PostToolUse` adapter hardens toward `harness-session` |
| `on-create` | After a new thing is created | New thing, potential parent/linked things | `interpretation` |
| `on-status-change` | After a thing's status field changes | Thing, old status, new status, downstream | `interpretation` |
| `on-error` | When validation or reasoning encounters a conflict | Error context, affected things | `interpretation` |
| `retrospective` | When a `type: retrospective` is being written (periodic reflection) | All things, all indexes, conflicts, insights since last retrospective | `interpretation` |

### Domain-Level Hook Points

Domains define their own hook points for domain-specific lifecycle events. These are declared in the domain's workflow skill.

```yaml
hook_points:
  - name: phase-gate
    fires: "When expert confirms a phase is complete"
    context: [current-phase-report, next-phase-requirements]
    
  - name: expert-review-needed
    fires: "When LLM generates output requiring human judgment"
    context: [generated-output, uncertainties, embedded-questions]
    
  - name: approval-checkpoint
    fires: "When a go/no-go decision point is reached"
    context: [analysis-report, risk-summary, recommendations]
```

Domain hook points follow the same pattern as framework hook points — they're named moments with declared context. The difference is they emerge from domain workflows rather than framework mechanics.

### How Hook Points Relate To Triggers

Triggers and hook points are complementary, not redundant:

- **Triggers** are *conditions* attached to individual things. They're pull-based — evaluated when the agent scans.
- **Hook points** are *events* in the lifecycle. They're push-based — they fire when something happens.

A trigger says: "Check if I'm overdue." A hook point says: "Something just changed — what should happen next?"

In practice, the `session-start` hook is when triggers get evaluated. The `post-write` hook is when dependency triggers cascade. The hook point is the *mechanism* that makes trigger evaluation happen at the right time.

## Prompts

A prompt is a reusable reasoning template. It's smaller than a skill (which is a comprehensive instruction set) and more structured than a trigger action (which is a single word like `surface`).

Think of the hierarchy:

```
Skill (full instruction set, many paragraphs)
  └── Prompt (focused reasoning template, one specific task)
        └── Trigger Action (single-word signal: surface, escalate, cascade)
```

A skill says "here's how to do everything about reading things." A prompt says "here's how to evaluate whether downstream things should be unblocked after a completion." A trigger action says "unblock."

### Prompt Structure

Prompts live in the domain's skills directory or in the framework root. They follow the thing pattern — YAML frontmatter + markdown body — but with `type: prompt`.

```yaml
---
id: cascade-completion
type: prompt
status: stable
version: 1.0
created: 2026-05-20
inputs:
  - name: completed-thing
    description: "The thing that was just completed"
  - name: downstream-things
    description: "Things that have dependency triggers watching the completed thing"
outputs:
  - name: status-changes
    description: "List of things whose status should change"
  - name: notifications
    description: "Things to surface to the user"
---

# Cascade Completion

## Reasoning Template

When a thing is completed, evaluate its downstream impact:

1. Load all things that list the completed thing in their `dependencies` or `triggers.watch`
2. For each downstream thing:
   - Are all its dependencies now satisfied? → Change status from `blocked` to `not-started`
   - Is this the last subtask of a parent? → Suggest parent completion
   - Does this unblock a critical-priority item? → Surface immediately
3. Report what changed and what needs user attention
```

### What Makes A Prompt Different From A Skill

| Aspect | Skill | Prompt |
|--------|-------|--------|
| **Scope** | Comprehensive — covers an entire operation mode | Focused — handles one specific reasoning task |
| **Size** | Many sections, full instructions | One reasoning template, typically under 50 lines |
| **Invocation** | Loaded at session start, always active | Invoked at specific hook points |
| **Composability** | Self-contained | Composable — multiple prompts can fire at one hook point |
| **Inputs/Outputs** | Implicit (reads whole domain) | Explicit (declared in frontmatter) |

### Framework Prompts

These are prompts that ship with the framework and apply to any domain:

- **cascade-completion** — Evaluate downstream impact when a thing completes
- **evaluate-triggers** — Scan active things for trigger conditions that are now true
- **session-orientation** — At session start, summarize what's changed since last session
- **surface-attention** — Determine which things need user attention and in what priority order
- **detect-conflicts** — Check if a proposed change conflicts with existing state (lens conflicts, dependency violations)
- **session-end-continuity** — At session end, extract insights, disposition the standing insights, check for contradictions, manage open-loop things, commit with a rich `session-end:` message (the backward record is git; `mdllm worklog` is an on-demand view, not a committed file), then report publication debt (`estate-sync --status` — after the commit, never elided from this summary: two summaries ended at the commit while every operative surface carried the debt step)
- **domain-velocity** — At session start, read git history as telemetry to surface stalled, churning, or untouched work the current-state snapshot can't see
- **review-schema-coherence** — At retrospective, audit the domain's emergent frontmatter vocabulary (via the schema registry) for fields that have drifted apart in name but converged in meaning

The reflexive prompts — `domain-velocity`, `evaluate-triggers` (against the triggers index), `detect-conflicts` (scan mode), and `review-schema-coherence` — let the agent reason *about* the domain, not just *within* it. Three of the four read a derived index rather than scanning every thing; see `derived-index.md`.

### Domain Prompts

Domains define their own prompts for domain-specific reasoning:

- **generate-phase-report** — (Business Flow) Structure findings into a phase report with embedded questions
- **format-expert-questions** — (Business Flow) Extract uncertainties and format them for expert review
- **apply-compliance-lenses** — (Compliance) Evaluate a change through all regulatory lenses
- **prioritize-by-energy** — (Life Manager) Factor energy cost into priority recommendations

## Bindings

A binding connects a hook point to one or more prompts. It's the declaration that says: "When this moment happens, invoke this reasoning."

### Binding Structure

Bindings are declared in a domain's AGENTS.md or workflow skill.

```yaml
bindings:
  - hook: post-write
    when: "status changed to completed"
    invoke:
      - cascade-completion
      - evaluate-triggers
    
  - hook: session-start
    invoke:
      - session-orientation
      - evaluate-triggers
      - surface-attention
    
  - hook: session-end
    invoke:
      - session-end-continuity
    
  - hook: phase-gate
    when: "expert confirms phase complete"
    invoke:
      - validate-phase-completeness
      - generate-next-phase-report
```

### Reflexive Behaviour Bindings

A domain that wants the agent to reason *about* itself — not just respond to requests —
binds the reflexive prompts. These are the bindings that turn the derived indexes and
the velocity/conflict/schema prompts into routine behaviour:

```yaml
bindings:
  - hook: session-start
    invoke:
      - session-orientation       # what changed since last session
      - domain-velocity           # what should have changed and didn't (reads git)
      - evaluate-triggers         # what is now true (reads the triggers index)
      - surface-attention         # what to tell the user, in priority order

  - hook: on-status-change
    when: "a spec moved to stable, or an insight was promoted"
    invoke:
      - detect-conflicts          # scan mode: do its now-authoritative claims clash with neighbours?

  - hook: retrospective
    invoke:
      - detect-conflicts          # scan mode: full-domain sweep via the relationships index
      - review-schema-coherence   # audit emergent field vocabulary via the schema registry
```

Index *maintenance* is not bound here — it rides the `post-write` hard hook (above).
Bindings cover index *evaluation*: when and how the aggregated signal is read and acted on.

- **hook** — Which hook point this binding attaches to
- **when** (optional) — Additional condition that narrows when the binding fires. Without `when`, the binding fires every time the hook point fires.
- **invoke** — Ordered list of prompts to execute. Order matters — earlier prompts may produce context that later prompts consume.

### Binding Order and Composition

When multiple bindings attach to the same hook point, they execute in declaration order. This is intentional — it means you can reason about what happens at each lifecycle moment by reading the bindings top to bottom.

```yaml
# These all fire at session-start, in this order:
bindings:
  - hook: session-start
    invoke: [session-orientation]      # First: understand what changed
  - hook: session-start
    invoke: [evaluate-triggers]         # Second: check what's now true
  - hook: session-start
    invoke: [surface-attention]         # Third: decide what to tell the user
```

### Binding Scope

Bindings are domain-level declarations. Each domain defines its own bindings
based on what structured reasoning it needs — with one deliberate exception.

**One set of bindings arrives with the domain rather than being authored in
it.** The generated Session Start block (`mdllm domain-kernel`) binds the four
session-start prompts — `session-orientation`, `domain-velocity`,
`evaluate-triggers`, `surface-attention` — as numbered steps in every
scaffolded domain's AGENTS.md, and `mdllm scaffold` delivers the prompt files
into the domain's own `prompts/`. These are **framework-installed standing
bindings**: derived, regenerated on refresh, revisable only by editing the
generator — or by opting out of the managed blocks entirely, since a domain
whose AGENTS.md carries no managed blocks inherits nothing and still boots by
interpretation. *(This supersedes the earlier claim that no framework-level
bindings are inherited — the generated block is exactly such a binding, and
describing it as opt-in left agents free to read the session-start steps as
optional. Substrate reconciliation, 2026-08-09.)*

Everything beyond that set is opt-in and authored: domain hook points,
additional prompts, `when:` conditions, session-end and retrospective
bindings. A domain's bindings live in its workflow skill or AGENTS.md. They
can attach to:
- **Framework hook points** (session-start, post-write, pre-commit, etc.) — these moments exist in every domain
- **Domain hook points** — custom moments defined by the domain's workflow

## Putting It Together

Here's how the three primitives compose during a typical interaction:

```
User: "I finished the data collection task"

1. Agent parses intent → write operation (mark complete)

2. Agent modifies thing: data-collection.status = completed
   └── Hook fires: on-status-change
       └── Binding: on-status-change → [cascade-completion, evaluate-triggers]
           ├── cascade-completion runs:
           │   "data-collection completed → quarterly-review-prep is unblocked"
           └── evaluate-triggers runs:
               "quarterly-review-prep had dependency trigger watching data-collection"

3. Agent commits
   └── git pre-commit hook fires (mechanical, not a prompt):
       "Structural check: ✓ | Referential check: ✓ | Schema check: ✓"
       (Errors here block the commit. Semantic judgement is the agent's
        standing job per validate.thing.md — not a separate pre-commit prompt.)
   └── Hook point fires: post-commit
       (no bindings currently → nothing fires)

4. Agent reports to user:
   "Marked data-collection complete. This unblocked quarterly-review-prep —
    moved it from blocked to not-started. It's now your highest priority item."
```

## Relationship To Existing Specs

Orchestration doesn't replace the narrative specs — it's an additional tool for domains that need more structure:

- **thing.md** triggers remain the primary attention mechanism. They work through natural LLM reasoning without orchestration. Domains that adopt orchestration can use the `post-write` hook to make trigger evaluation more systematic.
- **write.thing.md** already guides the LLM to consider downstream effects through prose. Orchestration is for domains where "consider" isn't reliable enough and "always execute this checklist" is needed.
- **git-workflow.md** commit points are natural moments where orchestration hooks can attach — but they work fine without explicit hooks, driven by the narrative spec alone.
- **Workflow skills** (like a domain's phase gates) are the primary use case for domain-level orchestration — structured workflows where phase transitions need explicit, repeatable reasoning.

## Design Principles

1. **Declarative, not imperative** — Hooks declare *when*, prompts declare *what*, bindings declare *which*. None of them contain code or execution logic.

2. **Composable** — Multiple prompts can bind to one hook. Prompts can be reused across hooks. Domains define their own bindings independently.

3. **Transparent** — Reading the bindings tells you exactly what happens at each lifecycle moment. No hidden behavior, no implicit chains.

4. **LLM-native** — Prompts are natural language reasoning templates, not function signatures. The LLM reads them and reasons accordingly. There is no runtime, no interpreter, no execution engine — just structured attention direction.

5. **Opt-in** — A domain starts with zero orchestration (narrative specs handle everything). As the domain matures and identifies moments where structured reasoning adds value, it can adopt hooks, prompts, and bindings incrementally.

6. **Idempotent** — Running the same prompt at the same hook with the same context produces the same reasoning. No side effects beyond the thing modifications the prompt recommends.

## When To Create A Prompt vs. Leave It Implicit

Not everything needs a prompt. Over-specifying reasoning constrains the LLM rather than enabling it. The framework's strength is that LLMs reason well from narrative prose — prompts should sharpen that reasoning, not replace it.

### Create A Prompt When

- The same reasoning pattern repeats across multiple workflows or domains
- A hook point needs structured thinking that an LLM might skip or handle inconsistently
- The reasoning involves a specific sequence of checks that must happen in order (like validation or cascading)
- Getting it wrong has consequences (missed cascades, broken references, unsurfaced conflicts)

### Leave It Implicit When

- The reasoning is obvious from context and the skill instructions are sufficient
- The LLM naturally handles it without structured guidance
- The prompt would just restate what's already in a skill file
- The scenario is rare or domain-specific enough that a general template wouldn't fit

### Red Flags: Signs Of Over-Specification

Watch for these — they indicate a prompt is becoming too prescriptive:

- **The reasoning template is longer than the narrative prose it replaced.** A prompt should be tighter than a skill paragraph, not more verbose.
- **The template contains conditional branching logic** ("if X but not Y unless Z"). This is programming in prose. The LLM can reason about conditions — it doesn't need them scripted.
- **The prompt duplicates logic from another prompt or skill.** If two prompts cover overlapping territory, merge or eliminate one.
- **The prompt specifies exact output text rather than output structure.** Guide the shape of reasoning, not the words.
- **Domain-level prompts exceed ~10 for a single domain.** This suggests the domain is encoding procedures rather than reasoning guidance. Consider whether some prompts should be absorbed into the workflow skill's narrative.

### The Litmus Test

Read the prompt's reasoning template and ask: "Is this a checklist a competent person would use, or a procedure manual an intern would follow?" If it reads like a procedure manual, it's over-specified. Simplify until it reads like a checklist.

### Quantity Guidance

The framework ships its prompt templates in `templates/prompts/` (the set is
the directory's contents — counts restated in prose have drifted; the four
session-start prompts among them are delivered to every scaffolded domain and
bound by the generated Session Start block). A domain that adopts
orchestration beyond that should typically add 2–5 prompts for its unique
reasoning patterns. If a domain has more than 10 prompts, that's a signal to
review whether some should be consolidated or left implicit.

## File Organization

```
framework-root/
├── orchestration.md              ← this file (the specification — defines the pattern)
├── derived-index.md              ← the derived-index pattern (what the reflexive prompts read)
├── templates/
│   ├── prompts/                  ← starting-point prompt templates
│   │   ├── cascade-completion.md
│   │   ├── evaluate-triggers.md
│   │   ├── session-orientation.md
│   │   ├── surface-attention.md
│   │   ├── detect-conflicts.md
│   │   ├── session-end-continuity.md
│   │   ├── domain-velocity.md
│   │   └── review-schema-coherence.md
│   └── indexes/                  ← starting-point derived-index templates
│       ├── triggers.md.template
│       └── schema.md.template
└── domains/
    └── [domain]/
        ├── skills/
        │   └── [domain]-workflow.skill.md  ← domain hook points + bindings declared here
        └── prompts/                        ← domain-level prompts (copied/adapted from templates or created fresh)
            ├── generate-phase-report.md
            └── format-expert-questions.md
```

Prompts are things. They live in the domain's `prompts/` directory, have
frontmatter, have IDs, and can be linked to other things. They follow the same
structural rules as everything else in the framework. `mdllm scaffold`
delivers the framework's `templates/prompts/` set into every new domain's
`prompts/` (the four session-start prompts are bound by the generated Session
Start block — standing, not optional); beyond that delivered set, domains
copy, adapt, and author what they need.
