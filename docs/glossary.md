---
id: glossary
type: guide
status: draft
version: 1.0
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
---

# Glossary — the coined words, their plain names, and where each came from

MarkdownLLM names its parts in its own words. Most of those parts are old:
every row below has a standard-industry name and a predecessor with years of
literature behind it. The coined word is kept where it is shorter or more
exact inside the specs; this table is so that nobody has to learn the word to
judge the idea. Where a row says *no found precedent*, it means none was found
in the surveyed field on 2026-10-17 — not that none exists.

| Coined word | Plain name | Nearest prior art | Defined in |
|---|---|---|---|
| **thing** | a typed record: one markdown file with validated YAML frontmatter and a narrative body | Astro content-collection entries; MADR decision records; Backstage catalog entities | `thing.md` |
| **floor** (the deterministic floor) | the pre-commit validator: structural, referential and schema checks run by `mdllm` and installed as git hooks | Astro's build-time schema failure; gbrain `frontmatter-guard`; Backstage's entity validator; `remark-lint-frontmatter-schema` | `validate.thing.md` |
| **definition surface** | a record other records reason from — a spec, a rule, a guide, an insight with dependants | "load-bearing requirement"; a schema or policy document | `change-reconciliation.md` |
| **walk** | impact analysis: reading every dependant of a changed definition and recording whether it still holds | IBM DOORS suspect links; Doyle's truth-maintenance system (1979) | `change-reconciliation.md` |
| **walk gate** (commit gate) | a pre-commit refusal: a change to a definition surface cannot be committed until its walk is on record | *no found precedent at the version-control boundary* — DOORS does this inside a requirements tool | `change-reconciliation.md` |
| **cue** | an open reconciliation item, kept as a file until a human rules | a DOORS suspect-link flag; a Wikidata constraint-violation report | `change-reconciliation.md` |
| **inflection** | a walk's verdict that the change altered a dependant's meaning | a breaking change; an impact-analysis finding | `change-reconciliation.md` |
| **residue** | the items only a human may rule on, after the floor has applied what is mechanical and the agent has decided what is settled | human-in-the-loop arbitration | `orchestration.md`, `change-reconciliation.md` |
| **reckoning** | triage with exit rules: every attention item carries a condition under which it is disposed of, and a session end must dispose of a quota | GitHub `actions/stale`; GTD's weekly review; MemoryBank's forgetting curve | `session-memory.md` |
| **the close** | the session-end quota of the reckoning — the mechanical band applied, ten decisions a day from the oldest, the residue put to the human | end-of-sprint triage | `session-memory.md` |
| **insight** | a retained lesson with an exit rule (promote into a spec, dismiss, or hold with a reason) | a lessons-learned record; Letta's memory block; Hermes's `MEMORY.md` entry | `session-memory.md` |
| **conflict** | a recorded contradiction between two records, open until ruled | AGM belief revision; a TMS contradiction node | `belief-revision.md` |
| **retrospective** | a periodic review that runs the mechanical scans and produces insights and conflicts | a sprint retrospective; Wikidata's bot-generated constraint reports | `retrospective.md` |
| **trigger** | a declared condition the tool evaluates — a date reached, a status held too long, a dependency finished | org-mode `SCHEDULED`/`DEADLINE`; cron | `trigger-specification.md` |
| **quarantine** (`origin: external`, `verified`) | ingested content held as unverified until a named human flips it | Wikipedia's FlaggedRevs sighted versions; Karpathy's immutable `raw/` folder | `provenance.md` |
| **pin** (`informed_by` with a commit) | an input fixed to a full commit SHA so the output can be regenerated when the input moves | W3C PROV `wasDerivedFrom`; DVC and Nix lock hashes | `provenance.md` |
| **decision** | a decision record whose inputs are pinned | Architecture Decision Records (Nygard 2011; MADR) | `provenance.md` |
| **kernel** | the generated digest of operative rules an agent loads first (Tier 0) | a constitution or steering file (spec-kit, Kiro); `CLAUDE.md` | `kernel.md` |
| **Tier 0 / 1 / 2** | progressive disclosure of context: always-loaded, loaded when reasoning about the framework, loaded by query | Agent Skills' metadata → body → linked files; Hermes's three skill levels | `AGENTS.md` |
| **digest** (session-start digest) | the startup report the tool computes — version, velocity, stalls, open loops, cues, fired triggers | a sync-status dashboard (Argo CD); a daily standup report | `orchestration.md` |
| **orient** | the judgement half of session start, invoked by the operator (`/orient` in Claude Code): what the stalls mean, which triggers the floor could not judge, what to look at first | "catch me up"; a standup | `templates/prompts/` |
| **emitted / instructed** | content injected into the prompt before the model reads it, versus content the model is told to go and read | system-prompt injection versus a tool read | `things/insights/emitted-content-is-read-instructed-content-is-economised.md` |
| **domain / workspace** | one nested git repository with its own entry file, skills and records; *workspace* in anything outward-facing | a project; a repository | `domain-specification-guide.md` |
| **estate** | a multi-repository workspace: the framework plus its nested domain repositories, possibly across machines | a meta-repo; a GitOps fleet | `docs/estate-mechanics.md` |
| **face** (served face) | the exported subset of a workspace that other workspaces may import — records flagged `exposed: true`, rendered without their internal references | a published interface; an API contract | `interface.md` |
| **porch** | a cross-workspace handoff: one workspace importing another's face at a pinned commit, re-checked for drift | a dependency pin with an integrity check (`imports-check` ≈ lockfile verification) | `operating-model.md`, `interface.md` |
| **seat** | who sits in a clone — the declared actor and harness behind its commits — plus an advisory claim with a lease when two instances contend | git author identity; an advisory lock or lease | `coordination-claim.md`, `standing-watch.md` |
| **turn** | a change that has reached the remote ref — publication, not commit | GitOps principle 2: the desired state is versioned and pulled | `git-workflow.md` |
| **standing watch** (the doorbell) | a process that polls the remote ref while no session runs and wakes an agent when a declared condition turns true | Argo CD's reconciliation poll; a cron job; Dependabot | `standing-watch.md` |
| **ticket** | a work item passed between agents through the repository, closed when nothing is owed | an issue; a ticket | `standing-watch.md` |
| **dispatcher** | the scheduled, unattended run that applies the mechanical band and drafts the rest | a cron job; a scheduled agent (Hermes cron, Claude routines) | `templates/prompts/dispatch-loop.md` |
| **derived index** | a regenerable cache of one signal across the corpus, rebuilt and diffed at validation | a materialised view; a search index that is never hand-edited | `derived-index.md` |
| **workflow-definition / workflow-run** | stages as data, and an instance with a cursor | a state machine; a BPMN process and its instance | `workflow-state.md` |
| **lens** | a named viewpoint applied to the same record (domain logic, compliance, audit) | de Bono's Six Thinking Hats; role prompting | `reasoning-lenses.md` |
| **example** (`type: example`) | a worked positive or negative pattern the agent learns from | few-shot examples; a pattern language; Specification by Example | `example-things.md` |

Three words are not coined and are used in their ordinary sense: **commit**,
**hook**, **schema**. Two are harness words, not the framework's: **skill**
(a reusable instruction file — the framework's `*.skill.md` predates and
parallels the agentskills.io standard) and **harness** (the agent product:
Claude Code, Codex, Cowork, Copilot).

If you meet a word in the specs that is not here, it is either ordinary
English or a defect in this file — say so, and it gets a row.
