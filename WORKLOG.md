---
id: framework-worklog
type: artifact
status: evolving
version: 2.3
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
  - id: session-memory-specification
    relation: documents
  - id: belief-revision-specification
    relation: documents
  - id: retrospective-specification
    relation: documents
  - id: thing-lifecycle-specification
    relation: documents
  - id: trigger-specification
    relation: documents
  - id: derived-index-specification
    relation: documents
---

# Framework Work Log

This file is a running record of work done, decisions made, and work remaining. It is updated at the end of every session. It serves both as a progress tracker and as a historical record for retrospective reflection.

---

## 15 June 2026

### Session 1

#### Topic: change-reconciliation — the evolve-phase spec, designed and shipped (v3.7.0)

A long design dialogue on validating *reasoning* (not just structure) converged on
a new extension spec and shipped it end-to-end, then closed with a full coherence
sweep and the session-end ritual.

#### Completed

- [x] **`change-reconciliation.md` (new spec, v3.7.0)**: semantic consistency as a human-cued four-beat pass — cue (human declares the inflection), assimilate (declared edges via indexes, then textual trace via grep), walk (the agent's `validate.thing.md` Layer 2, one question per touch point), seal (revisions + `belief-revision` supersede mark in one commit). Fractal across scale; runs on existing infrastructure.
- [x] **Registered the spec** across every surface: `.markdownllm` foundational_specs, AGENTS catalog + Tier 2 routing table + spec-change checklist, `tools/mdllm.py` TIERS, `framework-map.md` (counts + View 2 node), kernel regen, version bump.
- [x] **Textual-trace tier** added to the Assimilate beat (grep for id + canonical name); the dark region formally tiered (declared / literal / conceptual).
- [x] **Retrospective Reconciliation mode** added to the spec (freeze → reconstruct-from-git → full-corpus walk → seal) for realigning domains twisted before the pass existed.
- [x] **Three insights**: `consistency-is-maintained-at-change-not-by-sweeping`, `mechanical-assimilation-is-blind-to-prose-dependencies`, `change-safety-is-defense-in-depth`.
- [x] **Full coherence sweep**: validate 56/56 (+6 +12 examples), doctor FLOOR ACTIVE @3.7.0, kernel + provenance indexes in sync, 37 tests pass; fixed a pre-existing `framework-map` spec-count drift (23→25, it omitted first-hour + framework-map) caught by the textual trace, not the floor.

#### Decisions

- **The driver names the inflection, not the agent**: the pass is human-cued; mechanical assimilation runs only after the human "go." Recognising an inflection is the expert judgement the framework supplements, not automates.
- **The dark region is structural**: declared edges are walkable, prose dependencies are not — the human is the irreducible backstop. The textual-trace tier narrows it to the conceptual residue but never empties it.
- **Structure beats reasoning** (the session's ethos): retrospective mode written into the spec so a mid-tier model follows rather than improvises.
- **Commit on the human's word, automatically**: the seal (commit + version + changelog) follows the human's approval — the decision is the human's, the commit is mechanical.

#### Deferred

- [ ] **Apply to a twisted live domain**: retrospective reconciliation of a real mid-process domain, conversationally after refresh — next session's concrete use.
- [ ] **Invariants tier**: only if a contradiction-class recurs often enough to outgrow the retrospective.
- [ ] **Proactive cue surface**: agent flagging high-fan-in edits mid-write (the run→evolve transition) — the one unguarded lifecycle boundary, parked.

---

## 12 June 2026

### Session 1

#### Topic: Independent-review staleness pass — all eight findings actioned

Worked the "Contradictions and Staleness" section of `reviews/REVIEW-independent-2026-06-11.md` end to end, then swept the repo for the same disease on adjacent surfaces.

#### Completed

- [x] **Finding 1 — `templates/AGENTS.md.template` to v3:** Tier 0 loads kernel.md + continuity.md (was full thing.md + orchestration.md); version-check via `mdllm validate`; `_schema.yaml` and deterministic-floor sections added; session-end documented as bound prompt; `framework_version_seen` example now 3.4.0
- [x] **Finding 2 — `framework-discovery.md` (v1.2 → v2.0):** startup sequence is kernel-tiered; sentinel example updated to 3.4.0 and marked illustrative (live `.markdownllm` authoritative — no more hand-maintained copies); deployment diagram + `.gitignore` contract corrected `domain/` → `domains/` with the legacy spelling noted
- [x] **Finding 3 — `domain-specification-guide.md` (v2.7 → v2.8):** line 294's phantom fourth hard hook removed — session-end continuity is a bound prompt, explicitly invoked; the three real hard hooks named; embedded template startup aligned to kernel pattern, gains `framework_version_seen`
- [x] **Finding 4 (partial) — examples:** both example AGENTS.md declare `framework_root` + `framework_version_seen`, run the version check, load the kernel; life-manager carries an explicit "skills only, no things yet" status note; README stops calling them working implementations (illustrative structure; the framework repo itself is the working example)
- [x] **Finding 5 — token estimates measured:** derived-index.md and scalability-guide.md (v1.2 → v1.3) disagreed 10–20×; both now derive from one measured basis — ~100–200 tokens per thing's frontmatter (2026-06-12, tiktoken o200k_base, framework corpus + two live domains, per-domain averages 96–204)
- [x] **Finding 6 — README claim softened:** "The result:" → tested-hypothesis framing citing the 2×2 honestly (determinism shown, small+framework beat large+bare at ~¼ cost, reasoning claim untested); Elegant Constraint section states the claim as the hypothesis under measurement; vendor table re-marked verified-in-use (Claude Code) vs designed-for (the other five)
- [x] **Finding 7 — minor tensions:** read.thing.md (v2.1 → v2.2) trigger exception made explicit (a declared trigger is a pre-authorised attention request) — kernel block updated, kernel regenerated and in sync; git-workflow.md (v1.1 → v1.2) names `post-write:commit` the invariant and the session-end commit the backstop; three stale WORKLOG To-Dos marked done (validation honesty superseded by the floor; cost honesty section exists; referential-integrity detection closed by mdllm)
- [x] **Finding 8 — manifesto (v2.2 → v2.3):** `.skill.md` re-described as emerging convention, not existing standard; §elegant-constraint claim restated carefully with first eval results
- [x] **Sweep finds:** orchestration.md "These two hard hooks" → three (section defines three); `templates/prompts/validate-before-commit.md` (v1.0 → v2.0) rescoped — it instructed re-performing mechanical validation by reasoning at the exact boundary the hook now owns; write-skill template and template AGENTS.md validate steps now name the mechanical/semantic split; domain-refresh.md `framework_version_seen` example 2.8 → 3.4.0
- [x] `mdllm validate .` clean (50 things, 0 findings); `mdllm kernel --check` in sync

#### Decisions Made

- The review's staleness section was actioned in full; its larger recommendations (un-exclude examples from validation, populate life-manager, cold-start scaffold eval, relation-vocabulary prune, read-side quarantine, limitations.md, concurrency page) remain in the continuity action queue as operator decisions — they change scope, not just accuracy.
- Token figures now follow the AGENTS.md convention everywhere: carry measurement method and date, instruct re-measurement, never assert.
- The fate of `reviews/REVIEW-independent-2026-06-11.md` itself (keep in full vs reduce to a continuity reference) is deferred to Janosh.

### Session 2

#### Topic: Week one of the post-review push — periphery under the floor (review actions 5, 2, and the on-ramp)

Operator set the fortnight's direction: point the v3 medicine at the periphery and at a user who isn't the author, with the cold-start scaffold eval as the centrepiece. This session cleared the three prerequisites in dependency order — vocabulary first (so everything downstream teaches the final set), then examples, then the on-ramp. Released as **3.5.0**.

#### Completed

- [x] **Relation vocabulary pruned 35 → 13** (`161601c`): 9 semantic (informs, implements, extends, references, complements, documents, validates, supports, challenges) + 4 mechanical (contradicts, supersedes, superseded-by, subtask — each checked by `mdllm validate`/`triggers`). Inverse pairs collapsed to forward direction; the one entry with a `notes:` field had the note moved to the surviving side. 45 link entries migrated by script with per-edit assertions; 14 pure-inverse entries deleted where the forward link already existed; 4 forward links added where it didn't (validate.thing → provenance, scalability-guide → example-things, domain-spec-guide → reasoning-lenses, tracking-artifacts insight → framework-map). thing.md (v2.13) vocabulary guidance rewritten; prompt templates migrated off undeclared relations (`defined-by`, `follows`, `consumes-output-of`); framework-map prose updated. Decomposition relations (instance-of etc.) stay in thing.md as universal guidance — they're a semantic rule, not framework-corpus vocabulary.
- [x] **Examples under the floor** (`bdb9571`): `mdllm validate` gains `example_corpora()` discovery — `examples/*/` with an AGENTS.md validates as its own corpus in the same run, so the pre-commit hook now covers examples (first exercised on that very commit). Both examples declare `_schema.yaml` (types, statuses, lean relations, `id_filename_match: false` for dotted skill filenames).
- [x] **life-manager populated** — 12 things, fictional but realistic: kitchen-renovation project with three subtasks (one completed, one *deliberately* overdue so `mdllm triggers` always demonstrates a hit — verified firing, one task blocked with a dependency trigger watching its blocker), a 10k goal fed by a recurring run, a weekly review with `review_date_reached` idempotency documented, and `decision-hire-howell-joinery` (`c8edb7e`) with `informed_by` pinned to `bdb9571` — `mdllm provenance` verifies clean.
- [x] **Example skills upgraded to v3**: write skill (v3.0) teaching templates now match the declared schema — pre-v3 residue removed (`planning`/`complete` statuses, invented `schema_version` field, dependency-things, quoted ad-hoc relations); hierarchy = `parent`, sequencing = `dependencies`/`blocks`; Post-Write Validation rescoped to the mechanical/semantic split in both domains' write skills; AGENTS checklists rescoped likewise; compliance-patterns phantom pattern references removed.
- [x] **first-hour.md created** (`aaedefa`, `type: guide`, draft v1.0): a newcomer's sixty minutes — look at one real thing before involving the agent, confirm discovery (with the paste-line fallback), scaffold something real-but-small, install the hook and deliberately break a status to watch the floor catch it, one real session. Registered in AGENTS.md Tier 2 + Guides; README gains a For Humans section and a top-of-page pointer.
- [x] `mdllm validate .` clean across all three corpora (50 + 6 + 12 things, 0 findings); kernel regenerated; sentinel/AGENTS/CHANGELOG synced at 3.5.0 (`b1c43f2`)

#### Decisions Made

- Sequencing: prune before examples before on-ramp, so every downstream surface teaches the final vocabulary.
- life-manager populated rather than deleted (the review allowed either): a worked dataset is what the cold-start eval participant will copy, and the example now demonstrates triggers, provenance, and the floor end-to-end.
- `type: dependency` dropped from life-manager: fields (`parent`, `dependencies`, `blocks`) express hierarchy and sequencing; things are for content. The write skill now states this as a rule of thumb.
- Example schemas keep two-to-three domain-specific relations (`supports`, `orchestrates`; `contrasts-with`/`remediated-by`/`demonstrates` in compliance) — declared, lean, and teaching the "declare what you use" habit rather than pretending the canonical nine cover everything.
- The deliberately overdue task is a feature, not stale data — documented as such in the thing body and AGENTS.md so nobody "fixes" it.

### Session 3 — Measure → mechanise → re-measure: the birth path, plus doctor and the first real refresh

#### Topic

Operator authorised four items in one go (none from the standing queue): the agent-only cold-start rehearsal, `mdllm scaffold`, `mdllm doctor`, and the eco-essentials refresh. A second independent review (`reviews/REVIEW-independent-2026-06-12.md`) landed mid-session from a parallel Cowork session; its actionable findings were fixed before close. Released as **3.6.0**.

#### Completed

- [x] **Cold-start scaffold rehearsal** (`6bcc982`, results `8292d12`): fixture `evals/cold-start-scaffold.yaml` + 5 new assertion kinds (file/git/min_things, fixture-scoped `domain_dir`) + per-fixture report grouping. Results (3 informative trials): opus 10/11 — built a structurally perfect domain across 96 turns and *never committed*; haiku 10/11 — committed but skipped the outer `.gitignore` isolation; haiku vs the scaffold-aware guide **11/11**, first commit = the tool's. Insight filed: `agents-drop-mechanical-birth-steps-not-semantic-ones`. Three 2s CLI failures were opaque → runner now persists `agent-stdout.json`/`agent-stderr.txt` per trial.
- [x] **`mdllm scaffold`** (`e90e2f2`): the isolation hard hook as code — templates instantiated (name/dates/`framework_root`/`framework_version_seen`), nested repo, outer-repo `.gitignore` committed *before* the first domain commit, hook installed, first commit; exit 1 on partial birth (review #2 finding 2). Building it caught `_schema.yaml.template` shipping as **unparseable YAML** (placeholder keys) — now valid-on-copy, and an unparseable schema is a validation Error, not a crash. Registered: orchestration v1.9, guide v2.9, AGENTS hard-hook text, framework-map (11 subcommands), operator-guide, README, first-hour.
- [x] **`mdllm doctor`** (`5a6b799`): environment probe — prerequisites, hook *execution* (`git hook run`; resolution is not verification), framework-version drift for domains, explicit degraded-mode verdict (exit 1). Its self-test executes the emitted hook in a fresh repo — the install-hook self-test from the continuity queue.
- [x] **eco-essentials refreshed 2.8 → 3.5.0** (domain commit `c746e0e`): first real five-version refresh through `domain-refresh.md` — floor adopted (`things/_schema.yaml`, hook, 12 things 0 findings, doctor FLOOR ACTIVE), AGENTS v2.0 kernel-tiered with the v3 validation split. Refresh contract held: capabilities updated, things untouched; relation prune + type lifecycles queued for the domain's next retrospective.
- [x] **Second independent review actioned** (`4641264`, findings 1–5): self-tests provision git identity via env and skip the hook execution-test on git < 2.36 (CI was red on `e90e2f2` — caught same-day); scaffold exits non-zero on partial birth; the phantom "since v3.6" reference removed (spec prose no longer names framework versions); eval evidence mirrored to committed `evals/results/` (run workspaces are nested repos and cannot be partially tracked); fixture versions templated from the sentinel via `{framework_version}`.
- [x] 37 floor self-tests passing; `mdllm validate .` clean across all three corpora; sentinel/AGENTS/CHANGELOG synced at 3.6.0; kernel regenerated

#### Decisions Made

- The three 2-second 1-turn trials are excluded from the report as harness failures, not model performances — but their evidence is kept (`evals/results/excluded/`).
- jmtm-software was **not** refreshed this session despite review #2 recommending it next: its working tree showed uncommitted AGENTS/WORKLOG modifications mid-session (likely the operator's parallel session) — refreshing under another writer's feet is exactly the concurrency hazard the queue already names. It stays first in line, before the July filing.
- Review #2's structural observations (WORKLOG size, review cadence exhaustion, release-cadence vs refresh-cost) are queued as operator decisions, not actioned unilaterally.

---

## 11 June 2026

### Session 1

#### Topic: Full framework review → transformation plan → Phase 0 baseline

Independent full review of the framework (all specs, live jmtm-software domain, insights, prior REVIEWLOG) conducted at Janosh's request, followed by a seven-phase transformation plan and immediate execution of Phase 0.

#### Key review findings

- **Enforcement gap is live:** all 17 things in jmtm-software fail `validate.thing.md` Level 1 status checks (Error severity), undetected — LLM-only validation missed a mechanical rule violation in the only production domain.
- **Spec self-contradiction:** Level 1's fixed status enum vs Level 3 / domain-guide's domain-defined state machines. The domain's vocabulary (`open → figures-ready → submitted → paid → reconciled`) is better modelling than the universal enum — the spec is wrong, not the domain.
- **Pattern:** each failure mode answered with new prose machinery → more cognitive load → the documented cause of hook non-compliance. Six tracking surfaces on one repo.
- **Provenance identified as a missing first-class layer** (Janosh built one in a private triage domain; generalising it is Phase 3 — pinned `informed_by: [{id, commit}]` decision records + `origin: external` quarantine).

#### Completed (Phase 0)

- [x] **`framework-v3-transformation-plan` created** (`type: plan`, registered in AGENTS.md) — the canonical seven-phase roadmap: deterministic floor (`mdllm` CLI + normative schemas), deletion pass, provenance spec, insight-staleness check, operative kernel, behavioral evals, new powers (regeneration, proactive triggers, small-model evals, CI)
- [x] **First framework retrospective** (`framework-retrospective-2026-06`) — the framework had never applied `type: retrospective` to itself
- [x] **First conflict thing** (`status-vocabulary-universal-vs-domain`, open) — `contradicts` links added to both parties per belief-revision.md; resolution designated to Phase 1
- [x] **`continuity.md` initialised** for the framework domain (prescribed by session-memory.md; never existed)
- [x] **Token baseline measured** (`tools/measure-tokens.py`, tiktoken o200k_base): Tier 0 = 13.5k, Tier 0+1 = 26.5k, full load = 65.5k. AGENTS.md asserted costs replaced with measured values
- [x] **Repo tagged `v2.9-pre-floor`** — the before-state for everything the plan changes

#### Decisions

- **Domain-owned status vocabularies** (pending Phase 1 implementation): the normative domain schema declares types, required fields, statuses, and transitions; the six universal workflow values become the default when no schema exists.
- **Tooling does mechanical checks; the LLM keeps semantic ones** — validate.thing.md Levels 1–3 delegate to `mdllm` in Phase 1; Level 4 remains LLM reasoning.
- **Measure, don't assert:** token costs in AGENTS.md now carry their measurement method and date.

#### To Do (next session)

- [x] Phase 1 — completed same day, Session 2 below

### Session 2

#### Topic: Transformation plan Phases 1–7 executed (framework v3.0 → v3.2)

Continued directly from Session 1 at Janosh's direction ("keep going until the limit"). Six phases landed in one sitting, each at its own commit boundary.

#### Completed

- [x] **Phase 1 — deterministic floor (v3.0.0):** `tools/mdllm.py` (validate / triggers / index / tokens / install-hook); normative schemas for framework + jmtm; thing.md v2.11 + validate.thing.md v2.0 (tool owns mechanical, LLM owns semantic); conflict `status-vocabulary-universal-vs-domain` resolved (`superseded` — domain owns vocabularies); pre-commit hooks installed in both repos and **verified to block** a broken thing; framework 38/38 clean, jmtm 0 Errors
- [x] **Phase 2 — deletion pass (v3.0.1):** REVIEWLOG migrated verbatim into `framework-retrospective-2026-05` (git tracked it as a rename) and deleted; `mdllm changelog` generator; speculative trigger machinery pruned (trigger-spec v1.2)
- [x] **Phase 3 — provenance (v3.1.0):** provenance.md spec; `type: decision` with `informed_by: [{id, commit}]` pinning; `origin: external` + quarantine; `mdllm provenance` (pin shape/existence, quarantine, freshness); reverse-provenance index; **first real decision record** (`decision-status-vocabulary-domain-owned`) — freshness check fired correctly on it the same day
- [x] **Phase 4:** scoped insight-staleness check — session-memory v1.1 + session-orientation prompt v1.1 (live insights × changed things; sweep stays at retrospective)
- [x] **Phase 5 — operative kernel (v3.2.0):** `<!-- kernel -->` blocks in six Tier 0/1 specs; `mdllm kernel` generates kernel.md; **measured 1.6k tokens replacing 21.4k (93%)**; both AGENTS.md re-tiered (Tier 0 now ≈5.3k vs 26.5k); insight `operative-rules-are-a-small-fraction-of-spec-prose`
- [x] **Phase 6 Stage 1:** `mdllm eval --fixture` assertion engine; first fixture `evals/jmtm-vat-2026q1-filed.yaml` passing 6/6 against the live domain
- [x] **Phase 7 adapters:** GitHub Actions CI (validate + provenance + index drift), `adapters/scheduled-triggers.ps1` (daily toast on trigger hits), Claude Code PostToolUse adapter example
- [x] `.markdownllm` foundational_specs list completed (six specs were missing); version 3.0

#### Decisions

- Kernel = `<!-- kernel -->` blocks extracted to a generated derived index, not a hand-maintained summary
- Eval fixtures double as regression nets when asserted against production state
- Freshness-after-pin is Info, never Error — dated decisions are a judgement call, not a defect

#### To Do (next session)

- [x] Eval Stage 2 — completed same day, Session 3 below
- [ ] Tier 2 kernel blocks (low priority)
- [ ] Register scheduled-triggers.ps1 in Task Scheduler before the accounts deadline window

### Session 3

#### Topic: Coherence review pass + Eval Stage 2 (the model experiment is now runnable)

#### Completed

- [x] **Review pass (v3.2.1):** full floor sweep clean on both repos; caught `mdllm tokens` still measuring pre-kernel tiering (fixed — Tier 0 measured 5,592 tokens, confirming the 5.3k claim) and the public README still describing v2.x (deterministic-floor section, provenance row, validated-integrity bullet updated)
- [x] **Eval Stage 2 runner:** `mdllm eval --run` — seeds an isolated git workspace from the fixture's `seed/`, invokes a headless agent (`claude -p`, json → score/cost/time/turns), runs Stage 1 assertions on the result. Flags: `--model`, `--trials`, `--bare` (strips AGENTS.md/skills/schema for the no-framework condition), `--dry-run`, `--timeout`. Run dirs under `evals/runs/` (gitignored, kept as evidence)
- [x] **First Stage 2 fixture:** `evals/vat-quarter-basic.yaml` + synthetic seed (Meridian Web Studio Ltd, 8 things, validates clean). Known-correct arithmetic: output 2500.00 / input 380.00 / net 2120.00, with a blocked-entertainment-VAT discriminator (naive sum = 430.00 → fail)
- [x] **Verified without an agent:** negative test (6/7 assertions fail against the unworked seed — they discriminate), dry-run workspace seeding for both conditions, bare condition confirmed data-only
- [x] `evals/README.md`: Stage 2 usage + the 2×2 structure-beats-scale protocol (haiku/opus × framework/bare, ≥5 trials/cell)

#### Limits

- `claude` CLI not on PATH in this desktop-app session — the actual agent-invocation path is **untested**. First action next session: install CLI, run one live haiku/framework trial as a smoke test, then the full 2×2.

### Session 4

#### Topic: Comprehensive review → loose-ends fix pass (the floor verifies itself)

Full framework review at Janosh's request (every spec, mdllm.py line-by-line, evals, adapters, live floor run), then immediate remediation of everything found. Verdict: architecture sound, gaps concentrated where the framework trusted itself without verification.

#### Completed

- [x] **Version sentinel bug fixed + made impossible to repeat:** `.markdownllm` and AGENTS.md still said 3.0 while CHANGELOG was at 3.3.0 — domain refresh was silently disarmed for everything shipped since v3.1. Re-synced, and `mdllm validate` now mechanically checks `.markdownllm` / AGENTS.md / latest CHANGELOG entry agree (Error severity → the pre-commit hook physically blocks a version bump that skips the sentinel)
- [x] **mdllm self-test suite:** 30 pytest cases pinning frontmatter parsing, all three validation levels, reserved/declared/default vocabularies, eval assertions (incl. numeric coercion), kernel extraction, provenance index, sentinel sync. The floor was the framework's trust anchor and had zero tests. CI now runs them first
- [x] **Drift gates closed:** `mdllm kernel --check` (rebuild-and-diff on the deterministic body) added to CI; `provenance` added to `index check` default signals — the only deployed index was the only one not being checked
- [x] **Eval runner hardened for the 2×2:** bare condition no longer granted `--add-dir` to the framework checkout (control was contaminable); timeout now recorded as a 0/N trial instead of crashing the loop; `field` assertions coerce numeric strings ("2500.00" vs 2500.00 no longer a false negative); dead `--keep` flag removed; `eval --report` aggregates runs into the per-cell table
- [x] **Fairness note in evals/README:** bare cells are capped below 7/7 by construction (link assertion unstated in bare preamble) — report per-assertion results, figures assertions are the condition-neutral core
- [x] **Guide caught up to v3:** domain-specification-guide v2.7 gains the deterministic-floor scaffold section (schema → hook → kernel, decisions, evals) + checklist items; new `templates/_schema.yaml.template`
- [x] **Hygiene:** `.gitignore` covers `domain/` wholesale (future domains auto-isolated); `mdllm` output UTF-8 on Windows consoles; `.markdownllm` documents the domain/-vs-domains/ layout

#### Decisions Made

- Version discipline is now mechanical, not ritual: the sentinel-sync check lives in `validate`, so the same hook that guards thing integrity guards release integrity. The CHANGELOG version heading is the source the others must match.
- Relations vocabulary prune (33 entries) deliberately deferred to the next retrospective per `_schema.yaml`'s own note — not this session's scope.
- Full domain-specification-guide rewrite still open (tracked by insight `domain-spec-guide-predates-knowledge-primitives`); this session added the v3 addendum rather than rewriting 800 lines in a fix pass.

### Session 5

#### Topic: The full 2×2 ran — and measured convention-following, not reasoning

The structure-beats-scale experiment executed end-to-end: 20 valid trials
(haiku/opus × framework/bare, 5/cell, vat-quarter-basic), ~$7.2 total spend,
all four cells run in parallel.

#### Completed

- [x] **Full 2×2 run:** haiku/bare 86% (0/5 perfect) · haiku/framework 94% (3/5) · opus/bare 89% (1/5) · opus/framework **100% (5/5)** — the only deterministic cell
- [x] **Report hygiene:** pre-fix smoke run (20260611-125556, 1/7 against the pre-fix id template through the broken runner) moved to `evals/runs/_excluded-pre-fix/` so `eval --report` aggregates only valid trials
- [x] **Honest reading recorded:** all 20 trials got the figures right (the blocked-VAT discriminator saturated); the entire variance was the asymmetric `has-deadline` link assertion — insight `first-2x2-measured-convention-following-not-reasoning`, results + reading added to `evals/README.md`
- [x] Continuity brief updated; model-experiment open thread closed

#### Decisions Made

- haiku/framework link misses stay unpatched (per `fixture-fixes-correct-bugs-not-difficulty`): opus+framework 5/5 with identical AGENTS.md is the control proving the instructions are followable — patching would corrupt the measurement.
- The manifesto's declarative claim is not yet supported *or* refuted by this run — the fixture couldn't put the reasoning component under load. Next session: a harder fixture whose condition-neutral core discriminates, plus a claim-language pass (tested-hypothesis framing) in README/manifesto.

### Session 6

#### Topic: External review committed through a new harness — Cowork as the first measured non-IDE data point

An independent full-corpus review (Claude/Fable, run from Anthropic Cowork — a
desktop agent sandbox) was accepted and committed, and the act of committing it
became a live harness test: Cowork does not auto-discover AGENTS.md, and the
installed pre-commit hook could not run there at all.

#### Completed

- [x] **Independent review accepted and filed:** `reviews/REVIEW-independent-2026-06-11.md` (artifact, stable) — verdict, contradictions (birth-path staleness: template/framework-discovery/guide:294), over/under-engineering calls, and a priority queue now registered as the top open thread in `continuity.md`
- [x] **Hook portability fix:** the installed hook hardcoded `C:/Users/...` and bare `python` — unrunnable anywhere but the authoring machine. `install-hook` now emits a portable script (repo root via `git rev-parse`, interpreter via `command -v python3 || python`, relative mdllm path, explicit floor-unavailable error); reinstalled and verified passing in the sandbox
- [x] **Insight recorded:** `agents-md-discovery-is-harness-dependent` — discovery and the floor are harness/environment properties; bootstrap line should become a first-class discovery route in framework-discovery.md
- [x] **Commit test passed:** three structured commits through the validating hook from the sandbox (after clearing a stale `index.lock` via the harness's delete-permission flow); corpus clean at 48 things
- [x] Continuity brief updated; session-end ritual run

#### Decisions Made

- Commits made by agents are authored under the operator's standard git identity, not an agent-named author — uniform log, authorship-by-session recorded here instead.
- The review's action queue is adopted as-is into continuity; first items (birth-path staleness, examples under the floor) are next-session candidates alongside the harder eval fixture.

#### Reflections

- Cowork quirk worth remembering: its file mount can serve stale, truncated views of files *modified* by the harness's file tools (new files are fine). Near git this is dangerous — a truncated file could be staged. Workaround used: write commit-bound modifications through the shell side, which is authoritative.

### Session 7

#### Topic: Visual orientation layer — framework-map.md; the "portable" hook falsified on its own authoring machine

The operator raised that spec frameworks lack the shape-recognition intimacy a
scrollable codebase gives a fifteen-year developer, and asked for a visual map
of the framework. Three views were built interactively (elevation, spec
dependency graph from `linked_things` frontmatter, mdllm subcommand → spec
mapping) and committed as `framework-map.md`. The first commit attempt was
blocked by the session-6 hook — exposing a second portability failure.

#### Completed

- [x] **framework-map.md created** (guide, draft): three Mermaid views — five-band elevation (entry / specs / things / floor / git), the spec layer's what-defines-what graph (manifesto → thing.md ← extensions; kernel-core boundary), and the nine-subcommand floor mapping (solid = enforces/measures, dashed = generates). Includes the compressed mental model ("one atom, six operative rules, everything else is layering"), the navigation rule (start at thing.md, follow one `extends` edge), and a "keeping this map honest" section naming each view's mechanical source of truth
- [x] **Registered in AGENTS.md:** Tier 2 routing row (orienting in the framework structure) + Guides section entry
- [x] **Hook interpreter fix (`32d5c6f`):** `command -v python3 || command -v python` matched the Windows Store alias stub (resolvable, not executable; the real install ships `python` only, so the stub short-circuited the chain) and blocked all commits on the authoring machine. `HOOK_BODY` now executes each candidate (`"$c" -c "import sys"`) before accepting it; hook reinstalled; 30/30 tests pass; both session commits landed through the repaired hook — no `--no-verify`
- [x] **Insight recorded:** `portability-claims-need-execution-tests` — verification by resolution stops one step short of verification by execution; the commit test is the floor's execution probe in any new environment
- [x] Continuity brief updated (v1.2); session-end ritual run

#### Decisions Made

- The framework map is hand-drawn (not generated) for now, with drift risk handled editorially: each view names its mechanical source of truth and frontmatter wins on disagreement. Generating it via a future `mdllm` subcommand stays an open possibility, not a commitment.

#### Deferred

- [ ] **Domain visual map** (eco-essentials or jmtm-software): same three-view structure adapted to a domain's shape (skills and live things instead of specs). Operator explicitly deferred to a future session.

---

## 8 June 2026

### Session 1

#### Topic: Reflexive behaviour — derived indexes + bound prompts (framework v2.9.0)

Worked through four agent capabilities the framework wasn't exploiting (raised by Janosh): git history as queryable event stream, systematic trigger evaluation, systematic conflict scanning, and schema-drift review. Recognised they are one pattern, not four, and built it as a single new primitive.

#### Design constraints honoured (from prior insights)

- **`tracking-artifacts-can-drift-from-reality`** — naively, an index is a drift machine. Resolved by making indexes derived (things are truth), provenance-stamped, and validatable via rebuild-and-diff. The new Index Integrity check *is* the mitigation that insight proposed.
- **`hard-hooks-require-observable-agent-caused-triggers`** — index maintenance rides the existing observable `post-write` event as a domain-level hard hook; no new framework hard hook. Index *evaluation* is a bound prompt.
- **`hook-compliance-correlates-with-scope-not-awareness`** — indexes are opt-in and scale-triggered, not piled onto every session, so they don't degrade compliance on the hooks that matter.

#### Completed

- [x] **`derived-index.md` created** (v1.0, `status: draft`) — anchor spec for the pattern
- [x] **New prompts**: `domain-velocity.md`, `review-schema-coherence.md`; **new index templates**: `triggers.md.template`, `schema.md.template`
- [x] **Prompts updated**: `evaluate-triggers` (v1.1, reads index), `detect-conflicts` (v1.1, scan mode)
- [x] **Specs updated**: `thing.md` (v2.10, `type: index`), `validate.thing.md` (v1.5, Index Integrity), `orchestration.md` (v1.7, retrospective hook + prompts + bindings + maintenance hook), `trigger-specification.md` (v1.1), `belief-revision.md` (v1.1, scan cadences), `retrospective.md` (v1.1, reflexive scans), `git-workflow.md` (v1.1, telemetry), `scalability-guide.md` (v1.2, reconciliation)
- [x] **`AGENTS.md` (v2.9)** and **`.markdownllm` (v2.9)** updated — inventory, Tier 2 routing, `type: index`, new Key Innovation
- [x] **Insights**: `reflexive-behaviors-are-indexes-plus-prompts`, `derived-index-is-attention-cache-not-search-layer`
- [x] **CHANGELOG v2.9.0** written

#### Decisions

- **Velocity uses no index**: its signal already lives in git, the authoritative event stream. An index would only add a drift surface. This makes "does this signal already exist as ground truth?" a design question for any future reflexive behaviour.
- **`derived-index.md` ships as `draft`**: the pattern is sound but unproven in a live domain. Neither eco-essentials nor jmtm-software is near the scale that warrants an index yet — deploy-when-felt. Promote to `evolving` after first real use.
- **Scalability principle kept, not amended**: "no indexing" forbids an opaque query layer the agent reasons over *instead of* the data. A derived index points back *to* the data. Resolved as `both-valid`, recorded as an insight.

#### Deferred / Next

- [ ] **First live index deployment** — when a domain crosses ~100–150 things, deploy a triggers index and validate the maintenance/rebuild loop in practice; promote `derived-index.md` to `evolving`
- [ ] **`relationships` index template** — described in `derived-index.md` but no template yet; add when the conflict-scan full sweep is first run for real
- [ ] **thing-lifecycle.md** (still deferred): promote from draft when a domain approaches ~200 things

---

## 5 June 2026

### Session 1

#### Topic: Priority triage and framework continuity brief evaluation

Reviewed the full backlog across all three active areas (framework, eco-essentials, jmtm-software). Evaluated the two remaining deferred framework items — thing-lifecycle.md and framework continuity.md — and made explicit decisions on both.

#### Completed

- [x] **Full priority list compiled**: Backlog reviewed across all three areas; items ranked by urgency (JMTM annual accounts deadline in 26 days is highest priority)
- [x] **Insight created**: `continuity-briefs-solve-external-state-drift.md` — captures why the pattern applies to domains with external state but not to the framework itself

#### Decisions

- **thing-lifecycle.md stays deferred**: Explicit "feel the pain first" decision. No current domain is near the ~200 thing threshold. Implement when the ceiling is actually approached.
- **Framework continuity.md stays deferred (with concrete rationale)**: Continuity briefs solve real-world state drift — state that changes between sessions outside the agent's control. The framework has no such state; its state is the git history. WORKLOG + REVIEWLOG + AGENTS.md already serve the purpose. Create only if new sessions consistently lose context despite reading those files.

#### Deferred

- [ ] **thing-lifecycle.md**: Promote from draft when a domain approaches ~200 things
- [ ] **Framework continuity.md**: Create only if session orientation becomes noticeably difficult

---

## 2 June 2026

### Session 1

#### Topic: Framework version-check mechanism — diagnosis and fix

Investigated why the domain refresh mechanism wasn't working in practice, identified the root cause, and implemented a complete fix across the framework and both live domains.

#### Problem Diagnosed

The version check existed in documentation (`domain-refresh.md`, eco-essentials AGENTS.md) but was never executing. Root causes:
1. **Pull-based with no hard hook** — Detecting a version mismatch required reading CHANGELOG.md, which required the agent to choose to read CHANGELOG.md. Circular. No hard hook enforced it.
2. **Wrong source file** — CHANGELOG.md is a long narrative document; using it for version detection wastes context on every session, even when nothing has changed.
3. **jmtm-software had no check at all** — domain-refresh.md was Tier 2 only, only loaded on explicit user request.
4. **`.markdownllm` was stale** — The sentinel file showed v2.3 while the framework was at v2.8, proving the double-maintenance problem.

#### Completed

- [x] **`.markdownllm` updated**: version 2.3 → 2.8; `role: canonical-version-sentinel` field added; established as the single authoritative version source
- [x] **`orchestration.md` updated** (v1.5 → v1.6): Added `session-start:version-check` as the third framework-level hard hook. Reads only the `version` field from `.markdownllm` (tiny file, negligible context cost). On mismatch: surface to user, load `validate.thing.md`, run validation against domain things, offer full refresh.
- [x] **`domain-refresh.md` updated** (v1.1 → v1.2): Version source changed from CHANGELOG.md to `.markdownllm`. Refresh algorithm updated — detection step now owned by the hard hook; algorithm begins after mismatch is confirmed. Version tracking section updated to mark `framework_version_seen` as required (not optional).
- [x] **`framework-discovery.md` updated** (v1.1 → v1.2): `.markdownllm` elevated from "discovery marker" to "discovery and version sentinel." Example updated to v2.8. Summary table updated.
- [x] **eco-essentials AGENTS.md**: Tier 0 version check updated — now references `.markdownllm`, not CHANGELOG.md; explicit instruction on mismatch behaviour added.
- [x] **jmtm-software AGENTS.md**: Version check added to Tier 0 for the first time (previously had none).
- [x] **`templates/AGENTS.md.template` updated**: `framework_version_seen` added to frontmatter; startup sequence replaced with full tiered pattern matching current domain AGENTS.md files.
- [x] **Insight created**: `version-mismatch-triggers-validation-cascade.md` — the cascade from version mismatch into validate.thing.md and its generalisation as a Tier 0 check design pattern.
- [x] **LICENSE**: Copyright holder name corrected (JMTM Software Ltd → Janosh Moshiri).
- [x] All changes committed: framework repo (2 commits), eco-essentials repo (1 commit), jmtm-software repo (1 commit).

#### Decisions

- **`.markdownllm` is the canonical version source**: Single source of truth. AGENTS.md `version` field is descriptive metadata only. When they diverge, `.markdownllm` is authoritative.
- **Tiny sentinel over CHANGELOG.md for detection**: CHANGELOG.md is the right place to understand *what* changed; `.markdownllm` is the right place to detect *whether* anything changed. Different jobs, different files.
- **Version mismatch cascades into validate.thing.md**: Not just surfaced — validated. A newer framework version may have changed what valid things look like. Validation answers the urgent question before the session proceeds.
- **`session-start:version-check` as a hard hook, not a startup checklist item**: Checklist items are skipped. Hard hooks are not. The same principle that fixed `session-end:continuity` (28 May Session 2) applies here.

---

## 29 May 2026

### Session 1

#### Topic: Validation Pass + SRP Analysis (Thing Cohesion and Decomposition Review)

Two-part session. First: ran a full validation pass against the newly defined decomposition rules in thing.md (v2.6→v2.8), fixing 9 structural and referential issues across the framework. Second: conducted a full SRP analysis of every framework spec and insight against the three decomposition tests now defined in thing.md.

#### Completed

- [x] **Validation pass run**: 9 issues found and fixed — `origin: both` corrected to `origin: synthesised` in 3 insights; status vocabulary expanded in thing.md v2.8 and validate.thing.md v1.3; missing `linked_things` entries added to orchestration.md, interface.md, domain-specification-guide.md, WORKLOG.md, REVIEWLOG.md; CHANGELOG updated with two missing version entries (v2.6.0, v2.7.0)
- [x] **Full SRP analysis conducted**: All 17 specs, both guides, the manifesto, and 6 insights evaluated against rate-of-change test, consumer test, and relation-signal test
- [x] **8 issues identified and documented in REVIEWLOG**: 2 high, 3 medium, 3 low — none blocking, all actionable
- [x] **REVIEWLOG updated**: New 29 May review entry added with full findings, summary table, and suggested priorities

#### Issues Identified (for next session to action)

| # | Files | Issue | Severity |
|---|---|---|---|
| 1 | `thing.md` | `type: example` embedded; all other reserved types have own specs | High |
| 2 | `read.thing.md` + `write.thing.md` | Multi-lens reasoning duplicated across both | High |
| 3 | `domain-refresh.md` + `framework-discovery.md` | Deployment architecture split between two specs | Medium |
| 4 | `validate.thing.md` | Skill frontmatter fields (`name`, `description`, `applies_to`) on a thing spec | Medium |
| 5 | `write.thing.md` | References `schema_version` field not defined in `thing.md` | Medium |
| 6 | `thing.md` | Framework-internal types (`specification`, `guide`, `manifesto`) undocumented | Low |
| 7 | `scalability-guide.md` | `type: summary` used without definition | Low |
| 8 | `domain-specification-guide.md` | High-detail repetition of framework-discovery content | Low |

#### Decisions

- **Fix #1 and #2 first**: They directly contradict the decomposition principle just added to thing.md — the framework's own rules apply to itself
- **No continuity.md for the framework**: Still deferred (noted in 28 May Session 2 as an open item)

---

## 28 May 2026

### Session 1

#### Topic: Holistic Framework Review and Housekeeping

Full end-to-end review of the framework post-v2.5.0. Read all 15 specs, AGENTS.md, InnoTriage domain, insights, templates, examples, WORKLOG, and CHANGELOG. Created the REVIEWLOG as a new companion artifact (periodic quality reviews, separate from WORKLOG's session narrative). Identified tensions, over/under-engineering, and promoted one stale insight.

#### Completed

- [x] **Created REVIEWLOG.md**: New framework artifact for periodic quality reviews; complements WORKLOG by tracking *how well* things work rather than *what was done*
- [x] **Full framework review written**: Verdict, 6 strengths, 6 tensions, 4 over-engineered areas, 5 under-engineered areas documented
- [x] **Promoted stale insight**: `domain-spec-guide-predates-knowledge-primitives` → status: promoted (the guide already incorporated knowledge primitives at v2.5)
- [x] **Made thing-lifecycle.md discoverable**: Added to AGENTS.md Tier 2 loading table and spec inventory under new "Deferred" heading — fixing the "ghost spec" problem identified in the review

#### Decisions

- **REVIEWLOG as a separate artifact, not a WORKLOG section**: Reviews ask different questions than session logs. Keeping them separate lets each maintain its own rhythm (sessions are per-conversation, reviews are periodic).
- **InnoTriage alias convention**: Used "InnoTriage" as the review alias for the ProducFlow2 domain for readability.

---

### Session 2

#### Topic: Session-End Hook Review and Reclassification as Prompt

Reviewed the insight/session-memory/belief-revision system's practical effectiveness. Identified that `session-end:continuity` was classified as a hard hook but lacked an observable trigger, causing it to drift in practice. Refactored it to its proper classification.

#### Completed

- [x] **Reviewed all 5 framework insights** and assessed how the session-memory system was working in practice
- [x] **Created `templates/prompts/session-end-continuity.md`**: The extraction ritual rewritten as a prompt with declared inputs/outputs, bound to `session-end`
- [x] **Created `templates/prompts/worklog-update.md`**: WORKLOG append as a companion prompt, also bound to `session-end`
- [x] **Refactored orchestration.md** (v1.4 → v1.5): Removed hard hook, added prompts to framework prompts list, added `session-end` binding
- [x] **Updated AGENTS.md**: Replaced hard hook callout with `[BOUND PROMPT: session-end]` block
- [x] **Updated session-memory.md**: Adjusted ritual section to reference prompt-based invocation
- [x] **Updated README.md**: Reflected new classification in spec table and descriptions

#### Decisions

- **Reclassify session-end:continuity as a bound prompt, not a hard hook**: Hard hooks require observable, agent-caused triggers. "Session is ending" is not observable — it depends on external signal. Honest classification fixes the drift problem at its root.
- **Add worklog-update as a second session-end prompt**: WORKLOG updates were implicit before; making them a named prompt alongside continuity extraction gives both equal visibility.
- **No VS Code .prompt.md shortcut**: Decided against creating a Copilot-specific slash command to maintain vendor agnosticism. The natural-language trigger ("end of session") works across all platforms.

#### Deferred

- [ ] **Framework-level continuity.md**: The framework domain itself doesn't have a continuity brief. Should be created to practise what the spec preaches.

---

## 27 May 2026

### Session 1

#### Topic: Session Memory — Bridging Generative Knowledge Across Sessions

Design and implementation session. Identified a structural gap in the framework and closed it with two new primitives and a mandatory ritual.

#### Problem Identified

The framework handles **resolved knowledge** well (specs, decisions, tasks as things) but had no mechanism for **generative knowledge** — the reasoning, emerging views, open questions, and unresolved threads that arise during a session. Every session was starting cold. The WORKLOG captures what was done retrospectively; nothing captured what was still live and needed to return.

#### Completed

- [x] **session-memory.md created** (v1.0, `status: stable`): Full specification defining `type: insight`, `type: continuity-brief`, and the session-end extraction ritual. Covers the preservation test, extraction heuristic, lifecycle of both types, and their relationship to WORKLOG and git.
- [x] **orchestration.md updated** (v1.2 → v1.3): Added `session-end:continuity` as the third framework-level hard hook, alongside `post-write:commit` and `pre-domain-scaffold:isolate`. Hard hook fires at the end of any session involving a domain.
- [x] **thing.md updated**: Added a note to the `type` field documenting `insight` and `continuity-brief` as framework-reserved types with a pointer to `session-memory.md`.
- [x] **templates/continuity-brief.md.template created**: Starting-point template for domain continuity briefs with the four standard sections (Open Threads, Live Insights, Pending Decisions, Questions For Next Session).
- [x] **AGENTS.md updated** (v2.3 → v2.4): Added `session-memory.md` to startup loading (step 5), added `session-end:continuity` as a hard hook in the On Output section, added `session-memory.md` to the Operational specs list, added `insight` and `continuity-brief` to Thing Types.

#### Design Decisions

- **Insight extraction, not conversation logging.** Raw session transcripts were rejected; the framework extracts crystallised insights instead. Aligns with "minimal core, emergent detail" — only non-obvious, future-relevant items are preserved.
- **Continuity brief lives at domain root** (as `continuity.md`), not in `things/`. It's an operational document that the agent always loads at session start — like WORKLOG.md, not like a data instance.
- **`session-end:continuity` is a hard hook**, not a soft binding. The value compounds across sessions only if continuity is maintained reliably; making it optional would undermine the mechanism.
- **WORKLOG and continuity brief are complementary, not redundant.** WORKLOG = retrospective audit trail (always grows). Continuity brief = forward-looking live state (stays lean, resolved items removed).

#### Key Insight From This Session

The framework was strong at structured output and weak at preserving the reasoning that produced it. Generative knowledge — the dialogue, the competing views, the open questions — is often where the real domain intelligence lives. The session-memory primitives make that intelligence first-class rather than ephemeral.

---

### Session 2

#### Topic: Gap Analysis — Confidence/Origin Tracking and Contradiction Detection

Two gaps identified from the cognitive science analysis of the previous session were addressed.

**Gap 2 (Confidence/Origin) — Closed**

- [x] **thing.md updated**: Added `confidence` (`high|medium|low`) and `origin` (`stated|inferred|synthesised`) as recommended fields. Both default-safe (omission = high/stated). Combined `origin: inferred` + `confidence: low` always surfaces for human review. Closes the LLM trust calibration gap — the agent can now distinguish between what a human stated and what it inferred or synthesised.

**Gap 1 (Contradiction Detection) — Closed**

The user confirmed that `type: conflict` should be a first-class type — not a sub-status of insight. A conflict is a clash of perspective with its own identity and lifecycle, independent of whether it resolves.

- [x] **belief-revision.md created** (v1.0, `status: stable`): Full spec defining `type: conflict`, `relation: supersedes` / `relation: contradicts` / `relation: superseded-by`, three resolution outcomes (superseded, both-valid, dismissed), conflict detection (human-stated vs agent-inferred), and the conflict lifecycle. Key principle embedded: holding a contradiction in explicit tension is a valid, meaningful state — not a gap to paper over.
- [x] **thing.md updated**: `conflict` added as third framework-reserved type. `linked_things.relation` extended with `supersedes`, `contradicts`, `superseded-by` as framework-reserved relation values.
- [x] **validate.thing.md updated** (v1.1 → v1.2): Added four conflict-related checks to Level 4 Semantic Validation: `contradicts` without conflict thing (Error), `supersedes` without inverse link (Warning), open conflict not in continuity brief (Warning), stale open conflict (Info).
- [x] **session-memory.md updated**: Added Step 3 (Belief Revision) to the session-end ritual, inserted between insight extraction and continuity brief update.
- [x] **AGENTS.md updated** (v2.4 → v2.5): Added `belief-revision.md` to startup loading, Operational specs list, and Thing Types.

#### Key Design Decision

`type: conflict` is distinct from `type: insight`. An insight is something held by one party; a conflict is a collision between two things already in the domain. The difference matters for how the agent reasons: an insight is additive, a conflict is a rupture that demands explicit handling.

---

### Session 3

#### Topic: Polish Pass — Hook Consistency, Templates, and Retrospective Spec

Addressed four remaining gaps identified in the post-implementation review.

#### Completed

- [x] **orchestration.md updated** (v1.3 → v1.4): `session-end:continuity` hard hook text brought up to date — now explicitly covers both insight extraction (Step 1) and belief revision / conflict detection (Step 2). Previously only referenced session-memory.md; now also references belief-revision.md.
- [x] **templates/insight.md.template created**: Starting-point template for `type: insight` things with all recommended fields pre-populated.
- [x] **templates/conflict.md.template created**: Starting-point template for `type: conflict` things with parties, resolution fields, and five standard body sections.
- [x] **retrospective.md created** (v1.0, `status: stable`): Full spec defining `type: retrospective` — periodic quality reflection on domain reasoning. Defines when to write one (time, volume, milestone triggers), what it produces (insights, latent conflicts surfaced, spec updates), and the metacognitive principle: the difference between a domain that has *run* for a year and one that has *learned* for a year.
- [x] **templates/retrospective.md.template created**: Starting-point template for retrospective things.
- [x] **validate.thing.md updated**: Added "no recent retrospective" as an Info check — domains active for 60+ days without a retrospective are flagged.
- [x] **AGENTS.md updated** (v2.5 → v2.6): `retrospective.md` added to startup loading, Operational specs list, and Thing Types.

#### Priority Order Agreed (Cross-Domain Work Deferred)

Cross-domain pattern transfer was identified as a significant future capability but deliberately deferred until single-domain fundamentals are proven in practice. The agreed order: session memory → belief revision → retrospective → cross-domain (when the time comes).

---

### Session 4

#### Topic: Tiered Startup Loading — Context Window Cost Analysis and Fix

#### Problem Identified

After implementing the four new primitives (session-memory, belief-revision, retrospective, confidence/origin), the "load all specs at startup" instruction in AGENTS.md had grown to **~60,185 tokens** of mandatory load before any user query was processed. That is 30–65% of a typical model's context window (128k–200k) consumed before any domain work begins.

#### Completed

- [x] **AGENTS.md updated** (v2.6 → v2.7): Replaced the flat "load all" startup sequence with an explicit three-tier loading strategy. Tier 0 (always, ~15k): AGENTS.md, thing.md, orchestration.md. Tier 1 (reading/writing sessions, ~33k total): adds read.thing.md, write.thing.md, validate.thing.md, git-workflow.md. Tier 2 (on-demand by query type): all remaining specs loaded only when the session intent requires them. A routing table maps query type to the correct spec.
- [x] **"On User Request" tightened**: Step 1 is now "Route intent — determine which Tier 2 specs the session needs before proceeding." Replaces the vague "clarify intent / load relevant specs" pair.

#### Context Window Impact

| Session type | Before | After |
|---|---|---|
| Q&A / informational | ~60k tokens | ~15k tokens (75% reduction) |
| Standard read/write session | ~60k tokens | ~33k tokens (45% reduction) |
| New domain creation | ~60k tokens | ~60k tokens (unchanged — full load legitimately needed) |

#### Design Decision

The tiered pattern was already present in the framework for *things* (Level 1 metadata / Level 2 relationships / Level 3 full context). Applying the same principle to *spec loading* is a natural extension — not a new idea, just a previously missing application of an existing principle.
#### Consistency Pass — Bugs Fixed

A full review before session close surfaced five bugs and two design gaps.

**Bugs fixed:**
- `orchestration.md` version corrected: 1.3 → 1.4 (WORKLOG said 1.4; frontmatter was never updated)
- `thing.md` version corrected: 2.3 → 2.5 (two rounds of changes since v2.3, neither incremented)
- `thing.md` reserved types: `retrospective` was missing (added to AGENTS.md in Session 3 but not to thing.md)
- `session-memory.md` linked_things: added `belief-revision-specification` (ritual Step 3 depends on it)
- `orchestration.md` linked_things: added `belief-revision-specification` (hook text explicitly references it)

**Design gaps noted (not fixed — deferred):**
- `domain-specification-guide.md` predates session-memory/belief-revision/retrospective; new domains created with current guide won't know these primitives exist
- `thing-lifecycle.md` (draft, v0.1) exists at root but is not listed in AGENTS.md's spec inventory

**CHANGELOG updated to v2.5.0** — covers all four sessions of 27 May 2026.
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
- [x] validate.thing.skill.md: add validation honesty paragraph (LLM-performed, not deterministic) *(superseded by v3: validate.thing.md v2.0 made mechanical validation deterministic via mdllm + pre-commit hook — stronger than the paragraph the review asked for)*
- [x] scalability-guide.md: add cost/performance honesty section (tiered loading reduces but doesn't eliminate cost) *(done: "Cost and Performance Trade-offs" section; figures replaced with measured numbers 2026-06-12)*
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
- [x] Address referential integrity — what happens when a thing is deleted or renamed; detection and repair of broken `linked_things` references *(detection done in v3: `mdllm validate` flags broken references as Errors and the pre-commit hook blocks them from being committed; repair remains a session activity guided by the findings)*
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
