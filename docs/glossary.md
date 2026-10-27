---
id: glossary
type: guide
status: draft
version: 1.2
created: 2026-10-18
tags: [glossary, vocabulary, prior-art, onboarding, positioning]
linked_things:
  - id: operator-guide
    relation: complements
    notes: "The operator guide uses the terms; this file translates them."
  - id: first-hour-guide
    relation: complements
    notes: "The newcomer meets most of these words in the first hour; the 90-minute onboarding wall was this cost measured once."
  - id: review-critical-comparison-2026-10-17-claude
    relation: derived-from
    notes: "The prior-art column is that review's rulings; eight coined terms appear roughly two thousand times across the root with no glossary — this is the glossary it asked for."
  - id: the-onramp-is-the-operators-own-sentence
    relation: references
    notes: "The vocabulary did not land on the first non-author operator; a translation table is the cheapest remedy, not a replacement for the sentence-first route."
  - id: documentation-rulings-2026-10-20
    relation: implements
    notes: "v1.1 carries the wording ruling: workspace outward, 'the folder' for what you open, 'your workspaces' for the estate, operator for the human role."
---

# Glossary — the coined words, their plain names, and where each came from

MarkdownLLM names its parts in its own words. Most of those parts are old:
every row below has a standard name and a predecessor with years of literature
behind it. The coined word is kept where it is shorter or more exact inside the
specs; this table is so that nobody has to learn the word to judge the idea.
Where a row says *no found precedent*, it means none was found in the surveyed
field on 2026-10-17 — not that none exists. Each row has an anchor, so a guide
can link a word at its first use (`glossary.md#walk`).

## The words you meet first

| Word | Plain name | Nearest prior art | Defined in |
|---|---|---|---|
| <a id="workspace"></a>**workspace** | one record repository with its own entry file, skills and records — the thing you keep. The specs call it a *domain*; outward text says workspace | a project repository | `domain-specification-guide.md` |
| <a id="the-folder"></a>**the folder** | what you open in your agent tool. It is the workspace's own folder — the same thing, so it has no separate term | — | — |
| <a id="your-workspaces"></a>**your workspaces** (*estate* in the specs) | the framework plus all your workspace repositories, possibly across machines | a meta-repo; a GitOps fleet | `docs/estate-mechanics.md` |
| <a id="operator"></a>**operator** | you: the person who owns a workspace's truth and rules on what the agent may not settle. Older specs also say *driver*, *human* or *expert* for the same role | the product owner; the human in the loop | `orchestration.md` |
| <a id="session"></a>**session** | one conversation with your agent in a workspace, from opening the folder to the close | a working session | `session-memory.md` |
| <a id="harness"></a>**harness** | the agent product you work in: Claude Code, Codex, Cowork, Copilot | an IDE or agent client | `interface.md` |
| <a id="thing"></a>**thing** | a typed record: one markdown file with validated YAML frontmatter and a narrative body | Astro content-collection entries; MADR decision records; Backstage catalog entities | `thing.md` |
| <a id="floor"></a>**floor** (the deterministic floor) | the pre-commit validator: structural, referential and schema checks run by `mdllm` and installed as git hooks | Astro's build-time schema failure; gbrain `frontmatter-guard`; Backstage's entity validator; `remark-lint-frontmatter-schema` | `validate.thing.md` |
| <a id="orient"></a>**orient** | the start of a session, typed as `/orient` in Claude Code: the rules and the workspace's state put in front of the agent whole, then what matters today in your words | "catch me up"; a standup | `templates/commands/orient.md` |
| <a id="the-close"></a>**the close** | the end of a session (`/end-session`): lessons kept, ten open items decided, the ones only you can rule on put to you in one prompt | end-of-sprint triage | `session-memory.md` |
| <a id="refresh"></a>**refresh** | bringing a workspace's generated parts up to the framework's current version (`mdllm refresh`) | a dependency upgrade | `domain-refresh.md` |
| <a id="substrate"></a>**substrate** | the framework itself — the specs, the tool and the floor every workspace stands on | a platform; a runtime | `README.md` |
| <a id="training-harness"></a>**training harness** (for its operator) | the human-readable record a generic model is given at session start in place of being trained on its operator; the model is not changed. What is specific here: contemporaneous reasons, pinned inputs, held contradictions, human-ruled settlement, and inspection by the operator | in-context learning; RAG; agent memory tools | `llm-driven-systems.manifesto.md` → The Accumulation |

## How change is kept honest

| Word | Plain name | Nearest prior art | Defined in |
|---|---|---|---|
| <a id="definition-surface"></a>**definition surface** | a record other records reason from — a spec, a rule, a guide, an insight with dependants | "load-bearing requirement"; a schema or policy document | `change-reconciliation.md` |
| <a id="walk"></a>**walk** | impact analysis: reading every dependant of a changed definition and recording whether it still holds | IBM DOORS suspect links; Doyle's truth-maintenance system (1979) | `change-reconciliation.md` |
| <a id="walk-gate"></a>**walk gate** (commit gate) | a pre-commit refusal: a change to a definition surface cannot be committed until its walk is on record | *no found precedent at the version-control boundary* — DOORS does this inside a requirements tool | `change-reconciliation.md` |
| <a id="cue"></a>**cue** | an open reconciliation item, kept as a file until its walk is recorded; the agent answers it, the operator rules only on what the agent may not settle | a DOORS suspect-link flag; a Wikidata constraint-violation report | `change-reconciliation.md` |
| <a id="inflection"></a>**inflection** | a walk's verdict that the change altered a dependant's meaning | a breaking change; an impact-analysis finding | `change-reconciliation.md` |
| <a id="seal"></a>**seal** | the last step of a walk: the revisions and the answered cue committed together | closing a change ticket | `change-reconciliation.md` |
| <a id="residue"></a>**residue** | the items only the operator may rule on, after the floor has applied what is mechanical and the agent has decided what is settled | human-in-the-loop arbitration | `orchestration.md`, `change-reconciliation.md` |
| <a id="radius"></a>**radius** | how far a change reaches — inside one workspace, between workspaces, the framework | blast radius | `docs/estate-mechanics.md` |
| <a id="reckoning"></a>**reckoning** | triage with exit rules: every attention item carries a condition under which it is disposed of, and each session end disposes of a quota | GitHub `actions/stale`; GTD's weekly review; MemoryBank's forgetting curve | `session-memory.md` |
| <a id="insight"></a>**insight** | a retained lesson with an exit rule (promote into a spec, dismiss, or hold with a reason) | a lessons-learned record; Letta's memory block; Hermes's `MEMORY.md` entry | `session-memory.md` |
| <a id="conflict"></a>**conflict** | a recorded contradiction between two records, open until ruled | AGM belief revision; a TMS contradiction node | `belief-revision.md` |
| <a id="retrospective"></a>**retrospective** | a periodic review that runs the mechanical scans and produces insights and conflicts | a sprint retrospective; Wikidata's bot-generated constraint reports | `retrospective.md` |
| <a id="trigger"></a>**trigger** | a declared condition the tool evaluates — a date reached, a status held too long, a dependency finished | org-mode `SCHEDULED`/`DEADLINE`; cron | `trigger-specification.md` |
| <a id="quarantine"></a>**quarantine** (`origin: external`, `verified`) | ingested content held as unverified until a named person flips it | Wikipedia's FlaggedRevs sighted versions; Karpathy's immutable `raw/` folder | `provenance.md` |
| <a id="pin"></a>**pin** (`informed_by` with a commit) | an input fixed to a full commit SHA so the output can be regenerated when the input moves | W3C PROV `wasDerivedFrom`; DVC and Nix lock hashes | `provenance.md` |
| <a id="decision"></a>**decision** | a decision record whose inputs are pinned | Architecture Decision Records (Nygard 2011; MADR) | `provenance.md` |

## How the agent is given its context

| Word | Plain name | Nearest prior art | Defined in |
|---|---|---|---|
| <a id="kernel"></a>**kernel** | the generated digest of operative rules an agent loads first (Tier 0) | a constitution or steering file (spec-kit, Kiro); `CLAUDE.md` | `kernel.md` |
| <a id="tiers"></a>**Tier 0 / 1 / 2** | progressive disclosure of context: always loaded, loaded when reasoning about the framework, loaded by query | Agent Skills' metadata → body → linked files; Hermes's three skill levels | `AGENTS.md` |
| <a id="digest"></a>**digest** (session-start digest) | the startup report the tool computes — version, velocity, stalls, open loops, cues, fired triggers | a sync-status dashboard (Argo CD); a daily standup report | `orchestration.md` |
| <a id="emitted"></a>**emitted / instructed** | content injected into the prompt before the model reads it, versus content the model is told to go and read | system-prompt injection versus a tool read | `things/insights/emitted-content-is-read-instructed-content-is-economised.md` |
| <a id="adapter"></a>**adapter** | the small per-harness file that wires the floor's lifecycle steps into a harness — Claude Code's settings, Codex's hooks file | an editor plugin; a CI integration | `orchestration.md` |
| <a id="lens"></a>**lens** | a named viewpoint applied to the same record (domain logic, compliance, audit) | de Bono's Six Thinking Hats; role prompting | `reasoning-lenses.md` |
| <a id="example"></a>**example** (`type: example`) | a worked positive or negative pattern the agent learns from | few-shot examples; a pattern language; Specification by Example | `example-things.md` |

## Between workspaces and between agents

| Word | Plain name | Nearest prior art | Defined in |
|---|---|---|---|
| <a id="face"></a>**face** (served face) | the exported subset of a workspace that other workspaces may import — records flagged `exposed: true`, rendered without their internal references | a published interface; an API contract | `interface.md` |
| <a id="membrane"></a>**membrane** | the boundary between workspaces: only the face crosses it, and an import is pinned to a commit and re-checked for drift (`imports-check`) | a module boundary with a lockfile | `interface.md` |
| <a id="porch"></a>**porch** | the producer's side of the membrane: `mdllm mcp-serve` serving a workspace's face to other agents over MCP | a read-only API endpoint; an MCP server | `interface.md` |
| <a id="seat"></a>**seat** | who sits in a clone — the declared actor and harness behind its commits — plus an advisory claim with a lease when two agents contend | git author identity; an advisory lock or lease | `coordination-claim.md`, `standing-watch.md` |
| <a id="turn"></a>**turn** | a change that has reached the remote — publication, not commit | GitOps principle 2: the desired state is versioned and pulled | `git-workflow.md` |
| <a id="publication-debt"></a>**publication debt** | commits made locally and not yet pushed | "ahead of origin" | `git-workflow.md` |
| <a id="standing-watch"></a>**standing watch** (the doorbell) | a process that polls the remote while no session runs and wakes an agent when a declared condition turns true | Argo CD's reconciliation poll; a cron job; Dependabot | `standing-watch.md` |
| <a id="ticket"></a>**ticket** | a work item passed between agents through the repository, closed when nothing is owed | an issue; a ticket | `standing-watch.md` |
| <a id="dispatcher"></a>**dispatcher** | the scheduled, unattended run that applies the mechanical band and drafts the rest | a cron job; a scheduled agent (Hermes cron, Claude routines) | `templates/prompts/dispatch-loop.md` |
| <a id="derived-index"></a>**derived index** | a regenerable cache of one signal across the records, rebuilt and diffed at validation | a materialised view | `derived-index.md` |
| <a id="workflow"></a>**workflow-definition / workflow-run** | stages as data, and an instance with a cursor | a state machine; a BPMN process and its instance | `workflow-state.md` |

Three words are not coined and are used in their ordinary sense: **commit**,
**hook**, **schema**. One is a harness word, not the framework's: **skill** (a
reusable instruction file — the framework's `*.skill.md` predates and
parallels the agentskills.io standard).

If you meet a word in the specs that is not here, it is either ordinary
English or a defect in this file — say so, and it gets a row.
