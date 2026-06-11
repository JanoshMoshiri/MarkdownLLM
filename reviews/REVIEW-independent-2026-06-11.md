---
id: independent-review-2026-06-11-fable
type: artifact
status: stable
created: 2026-06-11
linked_things:
  - id: framework-retrospective-2026-06
    relation: complements
    notes: "External review one release after the first retrospective; action queue registered in continuity 2026-06-11"
  - id: agents-md-discovery-is-harness-dependent
    relation: informs
---

# Independent Review — MarkdownLLM Framework v3.4.0

Full read of all framework specs, kernel, tools, templates, evals, things (insights, conflicts, decisions, retrospectives, continuity), examples, and the three live domains. `mdllm validate .` run against the corpus (46 things, 0 findings). Reviewer: Claude (Fable), 2026-06-11.

## Verdict

This is unusually good work — and unusually honest work. The June retrospective found the framework's central failure (17/17 production things violating its own validation rule, undetected) and the v3 response — move every mechanical check into code, wire it into git, reserve the LLM for judgment — is exactly the right correction, executed well. The eval harness with its fairness caveats is more intellectually honest than most published benchmarks. The kernel is genuinely good context engineering.

The main risks now are different in kind: the framework is mostly a framework about itself (one real production domain, ~18 things, supported by ~8,900 lines of spec prose), several of the files that *new domains are born from* are stale against v3, and a layer of orchestration machinery exists largely on paper. The floor verifies itself; the on-ramp doesn't.

---

## What Works Well

**The self-correction loop.** Failure (silent validation collapse) → diagnosis (`hook-compliance-correlates-with-scope-not-awareness`) → structural fix (deterministic floor, pre-commit hook, schema ownership moved to domains) → verification of the fix (sentinel-sync check after the sentinel itself drifted). The framework noticed its corrective loop was amplifying the disease ("each failure answered with new prose machinery") and broke the loop with code instead of more prose. That is the strongest evidence the methodology works.

**The deterministic floor.** `mdllm.py` is well-scoped: single file, stdlib + PyYAML, 30 tests, CI, pre-commit enforcement. The validate/semantic division of labour ("never re-perform mechanical checks by reasoning") is the clearest, most defensible idea in the framework. "Replacing diligence with construction" is the right slogan and the right design.

**The kernel.** Extracting operative rules from rationale (`<!-- kernel -->` blocks → generated `kernel.md`, 26.5k → 5.3k Tier 0 tokens, drift-gated by `kernel --check`) is the correct answer to the spec-to-data ratio problem, and the generated-not-maintained pattern is correctly applied (same lesson as the CHANGELOG).

**The epistemics.** `confidence`/`origin`/`verified`, conflicts as first-class held tension, drift as Warning not Error, freshness as Info not Error, "spec when foreseeable, deploy when felt." These distinctions are used, not decorative — the status-vocabulary conflict thing and its decision record are a real worked example.

**The evals.** Stage 2 (seeded workspace, headless agent, bare control that genuinely can't see the framework, timeouts counted as failures, per-assertion reporting, the explicit fairness caveat about the `has-deadline` asymmetry) is rigorous. The honest reading — "structure bought determinism, the reasoning claim is still untested" — and the refusal to patch haiku's misses to protect the finding are exactly right.

**Writing and restraint guidance.** The specs are well-written. The over-specification red flags in orchestration.md (>10 prompts, "checklist not procedure manual") and the deploy-when-felt discipline are good self-protective principles — when followed.

**jmtm-software.** The one production domain is a real domain with real stakes (statutory filings), a domain-true status vocabulary, deadline things, and now decision records. It is the proof the model can work.

---

## Contradictions and Staleness (specific)

These matter most because three of them sit in the files new domains are scaffolded from.

1. **`templates/AGENTS.md.template` is pre-v3.** Its Tier 0 loads full `thing.md` + `orchestration.md` and suggests `framework_version_seen: 2.8`. The domain-specification-guide v2.7 says "Load the kernel, not the specs." Every domain scaffolded from this template is born without the kernel pattern the framework just spent a release building.

2. **`framework-discovery.md` (status: stable) is pre-v3.** Its startup sequence eagerly loads four full specs; its `.markdownllm` example shows `version: 2.8` with 6 foundational specs (actual: 3.4.0, 20 specs); its deployment diagram and ".gitignore contract" say `domain/` while `domain-refresh.md` mandates `domains/`. The divergence was patched in the data layer (gitignore and sentinel now carry both) rather than fixed in the specs.

3. **`domain-specification-guide.md:294` invents a fourth hard hook.** "The `session-end:continuity` hard hook fires" — orchestration.md and the root AGENTS.md are explicit that session-end is a *bound prompt*, explicitly invoked, not automatic, and there are exactly three hard hooks. A domain author following the guide will believe session-end continuity is guaranteed machinery; it is the single most skippable ritual in the system.

4. **`examples/` violate the framework's own rules and are invisible to validation.** Neither example AGENTS.md declares `framework_root` (framework-discovery's own validation checklist requires it). No `_schema.yaml`, no `continuity.md`, no knowledge subfolders — both predate v3 entirely. life-manager has *zero things* (your own WORKLOG TODO: "populate life-manager with 12-15 real, messy things"). Meanwhile `DEFAULT_EXCLUDES` in mdllm.py skips `examples/`, so they can rot forever without a finding — and README calls them "working domain implementations" while AGENTS.md tells the agent to reference them. This is `tracking-artifacts-can-drift-from-reality` happening again, one directory over from the validator.

5. **Token estimates contradict each other.** derived-index.md:146 says trigger evaluation over 50 things costs ~20k tokens of frontmatter; scalability-guide.md:263 says 200 things of frontmatter is 4–8k. That's a 10–20× disagreement, and both are hand-written numbers in a framework that owns `mdllm tokens` and has already learned (CHANGELOG, kernel) that hand-maintained numbers drift. Generate or delete them.

6. **README states the structure-beats-scale claim as a result** ("The result: a smaller model… outperforms…") while evals/README and the continuity brief correctly record the claim as untested. You already know this — it's queued as next session's centerpiece — but as of today the public README overclaims relative to your own evidence.

7. **Minor tensions.** read.thing.md forbids suggesting changes unless asked, while session-start trigger evaluation (a read activity) exists to proactively suggest unblocks and completions. git-workflow's "session-end safety net for uncommitted changes" coexists with a hard hook that makes uncommitted state supposedly impossible — say which is the invariant and which is the backstop. WORKLOG's To-Do list contains items that are actually done (validation honesty → validate.thing.md v2.0; cost honesty → scalability guide's trade-offs section) and one mostly closed by mdllm (referential integrity detection) — stale tracking, in miniature, again.

8. **Manifesto overclaims a standard.** AGENTS.md is a real cross-vendor convention; calling `.skill.md` "an existing standard for packaging reusable LLM capabilities" is a stretch — it's an emerging convention at best. The manifesto's credibility elsewhere is high; don't spend it here.

---

## Over-Engineered

**Orchestration's soft layer is an event system with no runtime.** Hook points, bindings with declaration-order execution semantics, prompts with typed inputs/outputs in frontmatter — none of it executes; all of it depends on the agent remembering, which your own insight says decays with scope. You already deleted the prompt I/O chain-validation as "type-checking for an event system with no runtime" — the same critique applies to much of what remains. Evidence of use: no domain declares more than a couple of bindings; most of the nine framework hook points have never fired anything. The hard hooks earn their place; the soft machinery should shrink toward "a domain may bind a named prompt to session-start/session-end" and stop there until a domain demands more.

**The deferred-spec mass.** thing-lifecycle (473 lines, draft, never deployed), derived-index (one index exists, the rest is design), branching, multi-user, period summaries. Each is individually justified by spec-when-foreseeable — but collectively roughly a quarter of the corpus is designs nobody runs, and every reader (human or agent) pays to route around them. The discipline keeps *deployment* honest; it doesn't keep *reading* cheap. Consider a `deferred/` directory or a status that the kernel/AGENTS.md routing genuinely hides.

**The relation vocabulary.** 35 declared relations, many of them inverse pairs and near-synonyms (`informs`/`informed-by`, `implements`/`implemented-by`, `enforces`/`enforced-by`, `references`/`referenced-by`, `complements` vs `related`). The validator can't reason about inverses; humans can't remember 35. Your own retrospective flagged the proliferation, and "declare the union, prune at next retrospective" was the resolution — the prune is due. ~12 would do.

**Tracking-surface count.** The retrospective counted six; the deletion pass removed one and automated another. WORKLOG + continuity + insights + retrospectives still overlap heavily — the same 2×2 result today appears in evals/README, the continuity brief, an insight, and presumably the next WORKLOG entry. Four copies of one fact is three drift surfaces.

---

## Under-Engineered

**Concurrency.** Acknowledged in the WORKLOG since 19 May, still nothing. Two sessions (or a scheduled trigger run plus an interactive session) on the same domain race on continuity.md, indexes, and the git index itself. Even a one-page "single-writer by convention; here's what happens when that breaks" spec would be more than exists now.

**The read-side of quarantine.** `mdllm provenance` correctly blocks *decisions* from pinning unverified external things — but the unverified thing's *content* still enters context whenever it's loaded, and "things are instructions to every future session" is your own framing of the injection risk. The actual attack surface is reading, not pinning. Consider: unverified `origin: external` things load at L1 only (body excluded) until verified, mechanically — that's a rule the tool could enforce at index/orientation time. Also: `verified: true` is a frontmatter flag any agent can write; nothing distinguishes "human confirmed" from "agent claims human confirmed."

**Schema migration.** "If validation blocks a legitimate change, fix the schema with the human" covers additions. It doesn't cover renames, vocabulary tightening, or what happens to 200 existing things when a status is removed. The WORKLOG TODO exists; the spec doesn't.

**Cross-domain composition.** The manifesto promises "your financial tracking can link to your projects." `linked_things` has no cross-domain addressing, and the validator would flag any attempt as a broken reference. Either spec it or stop promising it.

**Vendor-agnostic claims vs evidence.** The README's support table says "Fully supported" for six tools; only Claude's CLI has ever been exercised (the evals). The framework's entire reliability story above the floor depends on each harness honoring AGENTS.md prose contracts every session — exactly the mechanism your own data shows decays. An eval matrix across two or three harnesses would convert the table from claim to measurement; until then, mark it as designed-for, not verified-on.

**Trigger ownership is murkier than validation's.** validate.thing.md's mechanical/semantic split is crisp. The same split for triggers is not: `mdllm triggers` evaluates time/threshold mechanically, the spec still describes agent-evaluated semantics, and conditions like `stale` don't say where last-modified comes from (file mtime? git? thing-lifecycle defines `last_active` via git, but trigger-specification doesn't reference it). Pin which conditions the tool owns, which the agent owns, and what the data source is.

**Floor availability.** The pre-commit hook needs Python + PyYAML on whatever machine the agent commits from, and some agent sandboxes can't execute hooks at all. Current behaviour when the floor can't run: silently no floor. A degraded-mode statement (agent must run `mdllm validate` manually and say so) would close the gap.

**The missing `limitations.md`.** Your own TODO since May. The scalability guide's honesty section is a start, but "when not to use this" (high-volume transactional data, multi-writer teams, sub-second latency, genuinely relational queries) deserves the same first-class honesty the evals got. Likewise the comparison/differentiation doc — the obvious question from any newcomer is "why not just CLAUDE.md + a notes folder?" and the corpus never answers it directly.

---

## Needs More Thinking

**The identity question.** Almost all activity is the framework reasoning about itself. One production domain (~18 things, single operator who is also the framework author) cannot validate generalisation, vendor-agnosticism, scale behaviour, or the scaffolding experience — and it systematically *over*-validates self-referential elegance. The single highest-value next experiment isn't a harder VAT fixture; it's a cold-start eval: can a fresh agent + a person who isn't you scaffold a working domain from the templates? (That eval would have caught findings 1–4 above mechanically.)

**The on-ramp.** README → 850-line guide → stale template is the current path. The kernel solved tiered loading for *agents*; nothing equivalent exists for *humans*. The operator-guide is the right instinct — aim a similar document at the first hour, not the steady state.

**Generate-or-validate as a universal rule.** The framework keeps relearning one lesson: any hand-maintained surface drifts (REVIEWLOG, CHANGELOG, sentinel, indexes, WORKLOG TODOs, examples, templates, token numbers). The v3 pattern — generate it, or validate it, or delete it — should be promoted from a tactic to a stated principle, and applied to the remaining unguarded surfaces: templates (a `mdllm validate --templates` mode or scaffold eval), examples (un-exclude or CI job), token figures (emit from `mdllm tokens`), WORKLOG TODOs (move to things with statuses, or accept they're decorative).

---

## Priority Recommendations

1. **Fix the birth-path staleness** (template, framework-discovery, guide line 294). Highest leverage: errors here propagate into every future domain.
2. **Bring examples under the floor** — un-exclude from validation or add a CI job; upgrade both to v3 or delete life-manager until it has things. Stop calling them working implementations until they are.
3. **Soften the README claim** to tested-hypothesis framing (already queued — do it before anything else public-facing).
4. **Run the cold-start scaffold eval** before the harder VAT fixture. It tests the product; the fixture tests the model.
5. **Prune**: relation vocabulary to ~12, soft-orchestration machinery to what's actually bound, hand-written token numbers replaced by generated ones.
6. **Spec the read-side quarantine** (L1-only loading for unverified externals) — small spec, real security payoff for the domains you're targeting.
7. **Write limitations.md and the "why not just a notes folder" answer.**
8. **One page on concurrency**, even if the answer is "don't."

---

The honest summary, in your own idiom: the floor is real and verifies itself; the specs above it are good and mostly honest; the periphery — templates, examples, discovery, claims tables — is where diligence still substitutes for construction, and diligence has a measured failure rate here. Point the v3 medicine at the periphery and at one user who isn't you, and this stops being an elegant self-describing system and starts being a product.
