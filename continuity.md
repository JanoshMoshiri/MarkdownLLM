---
id: framework-continuity-brief
type: continuity-brief
status: live
version: 1.22
created: 2026-06-11
domain: markdownllm-framework
last_updated: 2026-06-24
---

# Framework Continuity Brief

## Open Threads

- **[COMPLETE 2026-06-24, cascade session] `mdllm cascade` shipped as v3.16.0 +
  live-domain test confirmed + PreToolUse parked by operator.** **Shipped:** `mdllm
  cascade <id>` (`5718569`) — the outbound post-completion mirror of `touchpoints`:
  gathers the downstream set a completion unblocks ("what did I just unblock?"), walking
  dependency edges in BOTH directions (`dependencies` + reverse `blocks`), reporting
  unblock candidates (priority-flagged) / partial progress / parent-completion candidate /
  trigger watchers — **reports, never applies** (detection mechanical, disposition the
  agent's); trigger eval left to `mdllm triggers`. `cascade-completion` prompt slimmed to
  its semantic residue (run tool → dispose). framework-map View 3 + count 17→18; 8 floor
  self-tests (85 total). Closes **smaller-deferred (ii)** below. Design rule pinned as
  `directional-graph-reads-come-in-inbound-outbound-pairs` (`0e38ef5`). **Version bumped
  3.15.0 → 3.16.0** (`6a715a6`, sentinel trio + kernel regenerated) — operator's call at
  close, additive minor. **Live-domain test DONE:** operator confirmed jmtm-software's
  `SessionStart` hook fired unprompted, ran the checks, registered slash commands, and
  `/end-session` ran clean — the behavioural proof that was the last open piece of the
  v3.15.0 deployment (closes follow-up (a) below). **PreToolUse PARKED by operator** (was
  "next session's named focus"): a per-domain hardening affordance, not a floor gap —
  "probably only needed for specific domains; things run fine without it." Stays available
  (foundation leaves PreToolUse free), de-prioritised, not dropped. **Multi-Claude
  emergence:** a parallel session built ON the cascade insight in real time (`943f27b`),
  generalising it into `mechanism-pairs-come-from-two-reflection-axes` (spatial
  inbound/outbound × temporal forward/backward × mechanical/semantic) and using it to
  surface a real gap, `cross-domain-handoff-is-built-inbound-only` (the thing-boundary pair
  is closed by touchpoints/cascade; the domain-boundary pair is half-built — producing side
  missing). State: 83 things, 0 errors, coherence clean, 0 open conflicts, 85 tests green.
  **NEW active design thread (parallel session's): spec the cross-domain hand-off
  producing-side** — commit-pinned reference triple + cross-domain Freshness check; see
  `cross-domain-handoff-is-built-inbound-only`. **Still open from below:** smaller-deferred
  (i) framework-map subcommand count → mechanical `coherence` check (small build).
- **[COMPLETE 2026-06-24] Terminal-dependency gate + full v3.15.0 doc reconciliation +
  retrospective 06d.** **Shipped:** `validate` now blocks a terminal-status thing depending
  on unfinished work (`8d3574e`) — `detect-conflicts` rule #1 as a *state invariant* (no diff;
  terminal deps count resolved; 0 false positives across all corpora). Insight
  `hard-invariants-encode-a-semantic-assumption` (`be13ceb`): a hard invariant freezes one
  reading of an ambiguous field — false-positives are a modeling signal toward `linked_things`,
  not a config escape; `dependencies` = hard-prerequisite semantics documented at the field in
  `thing.md`. **Reconciliation:** full pass over the whole v3.15.0 arc (build + deployment + gate)
  caught prose-dark-region drift the floor can't see — framework-map subcommand count 15→17,
  `domain-refresh` missing the operator paste-step for the `.claude/settings.json` adapter, stale
  README kernel figure (~1.6k→2.1k); fixed across framework-map / domain-refresh / CHANGELOG
  (folded into 3.15.0, redated 06-24) / operator-guide / first-hour / README (`fa1cc6e`).
  Retrospective `framework-retrospective-2026-06d` (`dcb5848`). New insight
  `repeated-drift-promotes-a-fact-into-the-floor`: a prose mirror of a mechanical fact that drifts
  a *second* time has earned a `coherence` check — one drift is an accident, two is a missing
  check (generalises `prose-references-are-mechanically-checkable` from references to derived
  counts). State clean: 82 things, 0 errors, coherence clean, 0 open conflicts, 77 tests green.
  v3.15.0 stays (folded, not bumped).
  **[PARKED by operator 2026-06-24, cascade session — see top entry] PreToolUse tool hooks.**
  The deliberately-deferred security/risk-reasoning hooks — the *action-side analogue of the
  pre-commit gate*: a clearance check at the action boundary for irreversible delete/send/spend,
  where `consequence-is-recoverable-only-in-retrospect` says the judgment belongs to human +
  structure, not a forward prediction. Foundation left PreToolUse free for exactly this. Design
  groundwork already laid (the `_dk_standing_truth` "defer the irreversible" block + the
  action/state-boundary asymmetry). To scope next time: what it inspects (Bash/action calls),
  what it *blocks* vs *asks* on, and where the mechanical-vs-interpretation line falls. (This is
  now the operator's chosen focus; the prior "(a) live-domain test immediate next" remains open
  but unprioritised below it.)
  **Smaller deferred:** (i) framework-map subcommand count → mechanical `coherence` check (per
  `repeated-drift-promotes-a-fact-into-the-floor`; retro 06d rec #2; small build). (ii) cascade
  helper — **DONE, shipped v3.16.0 (see top entry).** (iii) parked active insights still live:
  `consequence-is-recoverable-only-in-retrospect`, `long-running-tasks-lack-pre-compaction-checkpoint`.
- **[COMPLETE 2026-06-23] Domain-kernel + harness-hardening build — all 5 phases
  shipped as v3.15.0 (minor: additive/opt-in).** Full plan + progress table:
  `docs/plans/domain-kernel-hardening.md`. Commits are the ledger; this entry
  is the mid-flight position. **Why:** domain agents skip the session-start ritual even
  on Opus — structural, because session-start fires with the user's first message and
  loses; "hard hooks" were mislabelled (anchor `interpretation`/`harness-session` is
  *not* enforced; see `hook-enforcement-has-three-anchors`). **Done:** Phase 1 ✅ commit
  `45564c4` — orchestration.md reframed so **anchor** (interpretation|git-fs|harness-session)
  is primary and hard/soft is a config flag; Hook Points table + 3 hard hooks
  anchor-annotated; kernel regenerated. Phase 2 ✅ commits `a2085a0` (framework) + `a611665`
  (jmtm repo) — new `mdllm domain-kernel` fills managed `<!-- generated:NAME -->` blocks
  (standing-truth, session-start, tier-routing, hooks, floor) from `TIERS`+frontmatter,
  preserving authored content verbatim; corpus-general domain-kernel **drift check** in
  `coherence_findings` (inherited via pre-commit); `cmd_scaffold` fills blocks at birth;
  `AGENTS.md.template` restructured; jmtm migrated 182→141 lines; 67 tests green.
  **Shipped:** Phase 3 `mdllm session-start` + SessionStart adapter (commit `88c53a8`);
  Phase 4 deliberate `/end-session` + `/retrospective` slash-command templates, Claude +
  Copilot (`2d3de74`) — **session-end stays human-decided, no auto catch-up**; Phase 5
  scaffold/refresh/doctor wiring + bump 3.14.0→3.15.0 (`8cd4218`); jmtm migrated (`a611665`)
  and sealed to 3.15.0 (`f1de59f`). 74 tests green; validate + coherence clean.
  **Change-reconciliation + retrospective done (2026-06-23):** `session-orientation` is **kept
  and wired** into the session-start block — NOT superseded (the edge-walk showed it is
  `domain-velocity`'s complement and feeds `surface-attention`'s input; superseding would have
  orphaned that chain). The kernel-block header "never skippable" self-contradiction was fixed.
  Retrospective `framework-retrospective-2026-06c` written; insights
  `session-start-loses-to-the-first-request` + `existence-is-not-currency` created;
  `hook-enforcement-has-three-anchors` promoted → orchestration-specification. State is clean:
  77 things, 0 errors, coherence clean, 0 open conflicts, 74 tests green.
  **Deployment done (2026-06-24):** the framework self-hosts the hooks (operator pasted the
  `SessionStart`+`PostToolUse` block into `.claude/settings.json`; verified live, no false
  STALE after the framework-root fix `2b315e8`). jmtm got slash commands + Copilot prompts
  (`677d215`). **`scaffold` now writes `.claude/settings.json` out of the box** (`94b0af2`) — new
  domains are born hardened. `.claude/` un-ignored in both the framework and jmtm (settings.local
  stays ignored). New insight `agents-cannot-self-install-permission-bearing-hooks`: the agent
  *cannot* write `.claude/settings.json` (it carries permission rules → self-modification guard),
  so adapter install is structurally a human paste or a scaffold-time tool write — never an
  agent step. Also captured `prose-references-are-mechanically-checkable` (`60460ef`).
  **The ONE pending hand-off:** operator must add the hooks block to **jmtm's**
  `.claude/settings.json` with the `../../tools/mdllm.py` path (two levels down), then commit
  jmtm's `.gitignore` + `settings.json` + `CLAUDE.md`.
  **Open follow-ups (in order):** (a) **LIVE-DOMAIN TEST — immediate next.** Open a real domain
  and confirm the `SessionStart` hook injects the ritual unprompted (the behavioural proof; the
  mechanical proof is complete). (b) **PreToolUse security/risk hooks** — the agreed build after
  testing; the foundation deliberately leaves PreToolUse free. (c) other live domains (eco,
  property, code-architect) migrate via the `refresh` rail when next opened (felt-when-felt
  private work). (d) framework root `AGENTS.md` (~23k) not migrated to kernel shape — candidate
  if it keeps drifting. (e) version is **3.15.0 (minor)** — re-tag major if the operator prefers.
  (f) broken-body-reference check in `coherence` (per `prose-references-are-mechanically-checkable`).
- **Harden stale-WORKLOG as a `coherence` drift check (next session — operator's
  explicit defer, 2026-06-19 session 11):** the WORKLOG is regenerated by habit at
  session-end (`mdllm worklog --write`, now folded into `session-end-continuity`),
  not guaranteed fresh. The principled fix the deleted `worklog-update` prompt
  itself anticipated: treat a stale WORKLOG the way `coherence` already treats
  `kernel`/`index` drift — a generated-artifact freshness check in `tools/mdllm.py`.
  Tool-code work (out of scope for the surface-reduction pass that surfaced it).
  Generalises the `existence ≠ currency` candidate noted in the 2026-06-16 thread.
- **Fourth review (2026-06-16, mechanical census) — shipped as 3.12.0, NOW ON MAIN
  (the `coherence-floor` branch was a stale leftover, fully merged and deleted
  2026-06-19; the 3.13.0/3.14.0 work was built on top of it):** full review at
  `reviews/REVIEW-mechanical-census-2026-06-16.md`. It confirmed the
  mechanical/semantic line is drawn correctly and found the real gap: the floor
  *guaranteed* integrity at the commit boundary (`validate` in the hook) but left
  generated-artifact freshness (`kernel`/`index` drift) and catalog coherence to
  whether the agent remembered to run a command. New `mdllm coherence` mechanises
  that slice, **corpus-general by design so domains inherit it** — general checks
  (stable-staleness Info, dead-vocabulary Info, derived-index drift Error) run on
  any corpus; framework-only checks (foundational_specs↔filesystem, TIERS↔catalog,
  kernel drift) switch on at a `.markdownllm` root. Wired into `HOOK_BODY` as one
  self-scoping line + CI; `kernel`/`index` refactored to share one body-builder
  with coherence so the drift check cannot disagree with the generators. Also
  retired two live contradictions (the `worklog-update` prompt now regenerates via
  `mdllm worklog --write`; README no longer claims "no installation"). And `mdllm
  doctor` gained a **hook-body freshness** check: `refresh --seal` bumps the
  sentinel without reinstalling the hook, so doctor now flags an installed hook
  that is stale vs the current `HOOK_BODY` (advisory). **Next:** (a) DONE — the
  work is on main; the branch is deleted; (b) absorb into the live domains via
  `refresh` → `install-hook` → `refresh --seal` (all three are behind: jmtm 3.6.0,
  eco 3.6.0, property 2.9; **this is felt-when-felt private-domain work — see
  `felt-deployment-lands-in-undisclosable-work`**;
  absorption is near-invisible today — no indexes/`stable` skills/`.markdownllm`,
  so coherence blocks nothing — the payoff is on-demand `mdllm coherence` and
  automatic index-drift enforcement the day a domain deploys an index); (c) insight
  candidate *existence ≠ currency — an installed/generated copy needs a freshness
  check, not just an existence check* (generalises kernel/index/hook-body drift);
  capture as a `type: insight` thing if it recurs; (d) Bucket 3 from the reviews
  (sanitised validation record, `limitations.md`, cross-domain hand-off spec,
  read-side quarantine) remains for the operator's later doc/evidence pass.
- **Third independent review (2026-06-15) — action queue largely cleared:** full
  review at `reviews/REVIEW-independent-2026-06-15.md`. Items 1–2 shipped as
  **3.8.0** (the `workflow-state` primitive — `workflow-definition` + `workflow-run`,
  reserve-but-draft; bidirectional `session-start:version-check` with the advisory,
  cached, non-blocking upstream leg). Items 3, 5–8 shipped as **3.9.0**
  (`mdllm worklog` + `mdllm refresh`; model-tier claim demoted to hypothesis;
  cross-domain promise retracted → `cross-domain-handoff-is-verified-external-input`;
  advisory lease generalised in prose; `stable→evolving` relabel for
  thing/orchestration/domain-refresh). Items 1/5 hardened from a second independent
  read as **3.10.0** (`definition:` pointer made structural; the `current_stage ∈
  stages` membership check enforced now, not deferred). The structural `definition:`
  field then exposed a **reverse-edge gap** closed as **3.11.0**: the `relationships`
  index walked only `linked_things`, so a change to a `workflow-definition` could not
  mechanically surface its runs (nor `parent` its children); the index now emits the
  structural pointers, both reconciliation modes inherit the recall, and the rule is
  pinned as `structural-pointers-need-reverse-edge-indexing`. **Remaining:** (a) **#4 narrative validation
  record** — `evidence/` scaffold + shape-only template shipped; the cold-start human
  eval **has happened informally (the operator's brother)** but a clean, sourced,
  *disclosable* writeup is not producible now and may never be — this is the
  disclosable-proxy backlog, not undone work (see
  `felt-deployment-lands-in-undisclosable-work`);
  (b) **DONE (2026-06-18)** — the `workflow-run` primitive is now in live use on a
  real domain (private IP, not in the public corpus); the spec was promoted
  draft→evolving and the floor's `current_stage ∈ stages` check is active;
  (c) the harder-fixture eval below now carries the
  model-tier *hypothesis*, not a settled claim.
- **Apply change-reconciliation to a twisted live domain (next session's concrete
  use):** a domain changed mid-process before the pass existed — realign it via
  `change-reconciliation.md` → Retrospective Reconciliation (freeze a baseline
  first, reconstruct the delta from git, full-corpus walk, seal to a new
  baseline). Conversational and agent-driven after the domain's refresh; now
  viable on a mid-tier model because the procedure is structure, not improvisation.
- **Independent review (2026-06-11, external) — action queue:** full review at
  `reviews/REVIEW-independent-2026-06-11.md` (operator to decide whether the
  file stays in full or reduces to this reference). **Staleness pass done
  2026-06-12 session 1** (detail: WORKLOG 12 Jun). **Week-one prerequisites
  done 2026-06-12 session 2, shipped as 3.5.0:** examples under the floor
  (validate discovers `examples/*` sub-corpora, both declare `_schema.yaml`,
  life-manager populated with a working dataset incl. pinned decision record),
  relation vocabulary pruned 35 → 13 (corpus migrated, templates aligned),
  `first-hour.md` on-ramp created and registered. **Session 3 (12 Jun,
  3.6.0):** the agent-only rehearsal ran (10/11, 10/11, then 11/11 once the
  guide routed to the new `mdllm scaffold`); `doctor` shipped;
  eco-essentials completed the first real refresh (2.8 → 3.5.0). **Remaining,
  in priority order:** (1) **cold-start eval — happened informally (the brother);
  what remains is a *disclosable* writeup, which is felt-when-felt and may not come**
  (the agent-side path and templates are proven; the original "recruit a non-author,
  observe, don't help" framing is satisfied in substance — see
  `felt-deployment-lands-in-undisclosable-work`; reclassified from "the undone
  centrepiece" to disclosable-proxy backlog); (2) **refresh jmtm-software** (statutory stakes;
  AGENTS still teaches the pre-v3 validation procedure; working tree had
  uncommitted changes mid-session 3 — check whose, finish or refresh
  cleanly) and property-ventures after it; (3) fix what the human eval
  surfaces, then limitations.md + the "why not CLAUDE.md + a notes folder"
  answer; (4) read-side of quarantine; (5) one page on concurrency (the
  jmtm mid-session collision and the trial agent's framework `index.lock`
  are now two live exhibits); (6) generate-or-validate-or-delete as stated
  principle. Deferred until after the eval: harder VAT fixture, multi-harness
  matrix, domain visual map.
- **Second independent review (2026-06-12) — structural observations left
  with the operator:** findings 1–5 fixed in 3.6.0 same-day. Still open as
  *decisions*, not tasks: WORKLOG is ~93KB of hand-maintained prose and "the
  next REVIEWLOG" (generate-or-validate-or-delete applies); review cadence is
  exhausted until new evidence exists (next review after the human eval, not
  before); release cadence vs domain refresh cost — domains sit 1–5 versions
  behind a framework that versions daily (mechanisable: most of a refresh is
  re-copying three boilerplate blocks — scaffold-adjacent); manifesto still
  promises cross-domain linking no spec defines; README "no setup step" story
  vs first-hour's honest prerequisites — pick one. **Resolved in 3.9.0:** WORKLOG
  generated (`mdllm worklog`), refresh mechanised (`mdllm refresh`), cross-domain
  promise retracted. **Still open:** review cadence (next review after the human
  eval) and the README-vs-first-hour story.
- **Harness support is now measured, not assumed:** first non-IDE harness
  session (Cowork, 2026-06-11) — no AGENTS.md auto-discovery; the installed
  pre-commit hook couldn't run (machine-absolute path, bare `python`). Hook
  made portable same session (repo-relative, runtime interpreter resolution)
  — and that fix itself failed on the authoring machine next session (Windows
  Store `python3` alias stub resolvable-but-not-executable; fixed `32d5c6f`,
  hook now executes candidates rather than resolving them). Remaining: spec
  the explicit bootstrap line in framework-discovery.md as a first-class
  discovery route (vendor table re-marked designed-for vs verified-on
  2026-06-12); consider `install-hook` self-testing its emitted script. See
  `agents-md-discovery-is-harness-dependent`,
  `portability-claims-need-execution-tests`.
- **Domain visual map:** replicate `framework-map.md` for a live domain
  (eco-essentials or jmtm-software) — same three-view structure (elevation,
  link graph, floor mapping), but domains have skills and live things where
  the framework has specs. Explicitly deferred by the operator (2026-06-11,
  session 7) to a future session.
- **Harder fixture + claim-language pass — DONE (2026-06-17), with two findings:**
  `sleeping-bag-fac` built (unleakable synthetic Field-Adjusted Comfort rule) and
  the full 2×2 run. The reasoning core *discriminated* this time: **condition
  decided the figures (framework 5/5 both models, bare 0/5 both), model tier only
  decided the convention layer** (opus canonical links 21/21, haiku mis-keyed
  16/21). Closes `first-2x2-measured-convention-following-not-reasoning`; captured
  as `structure-decides-figures-scale-decides-convention`. Manifesto reworded to
  v2.4 (the **Thesis** added as the headline; model-tier demoted from central
  hypothesis to efficiency *corollary*; pre-floor cold-MVP anecdote retired).
  **Two open follow-ups:** (1) **the bare control leaks** — an uninterrupted
  opus-bare trial read the withheld method from `evals/seeds/.../AGENTS.md` inside
  the repo and scored 16/21 (excluded under `results/excluded/`); bare workspaces
  need real isolation (run outside the repo tree / OS sandbox), `--add-dir`
  withheld is not sufficient — foreseen, deploy when felt; see
  `withholding-is-not-isolation`. (2) **the longitudinal floor test** — this was
  single-shot; the drift-resistance half of the thesis still needs a
  multi-session fixture (the sleeping-bag rule is reusable as a component). Do
  **not** re-run the 2×2 to "fix" the leak — the leaked trial is itself the
  finding (operator's call, 2026-06-17).
- **Tier 2 kernel blocks:** session-memory, belief-revision, provenance,
  triggers, derived-index — low priority (demand-loaded anyway).
- **First jmtm decision-record filing:** annual accounts due 2026-07-31 —
  prepare through a `type: decision` with pinned inputs. Register
  `adapters/scheduled-triggers.ps1` in Task Scheduler before then.
- **jmtm orphan records:** 8 expense/profile things unlinked — link them when
  the FY2025 accounts/CT return are prepared.
- **Exercise composition for real:** the consolidation half of `thing.md`'s cohesion
  discipline is specified (The Inverse: Composition) and bound at retrospective
  cadence, but never run. First real composition sweep at a domain (or framework)
  retrospective is the live test — parallels the "apply change-reconciliation to a
  twisted domain" thread.
- **Installer's consent-based missing-deps branch is unverified end-to-end:** the
  happy path and both clone-from-remote one-liners are tested live (2026-06-19,
  session 10), but the git/Python-*absent* path (detect package manager → prompt or
  `-y`/`-Yes` → install → re-resolve) cannot be exercised without a clean machine.
  Verify on a VM/container with no Python if it ever matters; the logic shares the
  already-tested resolve/skip refactor, and falls back to a guided message when no
  package manager is present.

## Live Insights

- `mechanism-pairs-come-from-two-reflection-axes` — the framework's "other side of the
  coin" moments are the surface of two orthogonal reflection symmetries: spatial
  (inbound ↔ outbound through the graph) + temporal (forward ↔ backward through time),
  with a mechanical ↔ semantic labour axis running through both. Almost every mechanism
  is one quadrant of (inbound/outbound) × (forward/backward). The generator behind
  `directional-graph-reads` (spatial) and `change-reconciliation`'s prevented/created
  framing (temporal). Razor: when you build a mechanism, check the mirror across each
  axis before assuming it's done. Spine for a possible framework-map View 4
  (symmetry/coverage). High confidence (2026-06-24).
- `cross-domain-handoff-is-built-inbound-only` — the three maintenance surfaces all
  govern a single domain's interior; the one surface that crosses the repo boundary
  (cross-domain hand-off) is specified inbound-only. Consuming side exists
  (quarantine-on-import); producing side does not — a change in source domain A sends no
  staleness signal to consumers. `cascade` stops at the boundary. The
  `directional-graph-reads` razor one level up: thing-boundary pair is closed
  (touchpoints/cascade), domain-boundary pair is half-built. The standing known-unhandled;
  candidate shape is a commit-pinned reference triple + a cross-domain Freshness check.
  **Next: spec this out** (the active design thread). High confidence (2026-06-24).
- `directional-graph-reads-come-in-inbound-outbound-pairs` — a mechanical read over the
  relationship graph in one direction implies its opposite: `touchpoints` (inbound, "what did
  I put at risk?") ↔ `cascade` (outbound, "what did I just unblock?") are one attention-cache
  pattern pointed two ways, not two primitives. The razor against both under-building (shipping
  only the inbound read) and over-building (the mirror is the same walk flipped, inheriting
  report-not-apply). The concrete spatial-axis instance the parallel session generalised into
  `mechanism-pairs-come-from-two-reflection-axes`. Built `mdllm cascade` (2026-06-24).
- `modeling-cognition-yields-a-learning-loop-not-a-coherence-loop` — the framework did
  **not** build a loop; loops already exist. It built the *assimilation ritual*
  (insight → retrospective → end-of-session continuity), which is loop-agnostic and
  **composes onto** any existing work-loop: pin an end-of-session beat at the end of each
  iteration and the loop inherits cross-run learning — no changes to the loop, no new
  machinery. Anthropic's harness passes task-state back for *within-run coherence*
  (compaction, note-taking, memory tool) and disclaims a learned-lesson mechanism; the
  ritual adds *cross-run learning* on top. The minimal load-bearing piece is end-of-session
  continuity alone. Cleaner cause behind the manifesto thesis; razor for whether a new
  mechanism serves coherence or learning (2026-06-21). Unbuilt sibling: the loop-scoped
  insight at per-iteration cadence. Possible future tidy: make "attach end-of-session to
  this loop" a first-class one-line affordance (not a prerequisite).
- `felt-deployment-lands-in-undisclosable-work` — the framework's "deploy when felt"
  trigger fires inside the operator's confidential law-firm work (client IP), so the
  public repo structurally undercounts deployment; items shown as "deferred" are often
  done-but-private. The evals are synthetic precisely as the disclosable proxy. Stop
  reading public silence as immaturity; reserve open-thread status for genuinely-undone
  or disclosable-proxy work. The razor for triaging felt-trigger threads (2026-06-19).
- `hook-enforcement-has-three-anchors` — every hook anchors to agent-interpretation
  (portable, the default, sufficient for correctness), git/filesystem (mechanical,
  universal), or harness session lifecycle (needs an optional adapter); the anchor —
  not the hard/soft label — decides enforcement and portability. Adapters must stay
  optional or the framework stops being a substrate. The standing test for adding a
  hook and the razor that flagged two prompts for deletion (2026-06-19 session 11).
- `agents-md-discovery-is-harness-dependent` — discovery and the floor are
  harness/environment properties, not framework properties; the Cowork session
  is the first measured harness data point (partial failure; hook fixed
  in-session).
- `portability-claims-need-execution-tests` — a floor/portability claim is
  verified only by executing the capability in the target environment;
  resolution (command found, path exists) is not verification. The commit
  test is the floor's execution probe in any new environment.
- `fixture-fixes-correct-bugs-not-difficulty` — when a Stage 2 trial fails,
  fix fixture self-consistency bugs (id templates, schema names) but leave
  genuine model reasoning/attention gaps as findings, not patches.
- `hook-compliance-correlates-with-scope-not-awareness` — fix missed hooks by
  reducing load, not adding rules; the justification for the deterministic floor.
- `tracking-artifacts-can-drift-from-reality` — motivates generated-not-maintained
  surfaces (Phase 2 deletions).
- `the-notation-changed-not-the-primitives` — the razor for admitting new
  mechanisms; canonical articulation of the paradigm.
- `derived-index-is-attention-cache-not-search-layer` — governs the Phase 5 kernel
  (a derived index over the spec corpus itself).
- `consistency-is-maintained-at-change-not-by-sweeping` — semantic consistency is
  maintained at the point of change, not by periodic sweeping; the basis of
  `change-reconciliation.md`.
- `mechanical-assimilation-is-blind-to-prose-dependencies` — declared edges are
  walkable, prose references are the dark region, the human is the backstop;
  caught the routing-table miss on the spec's first live use.
- `change-safety-is-defense-in-depth` — layer overlapping nets (design, static
  trace, textual trace, walk, retrospective); no single net catches every dark
  region, so a miss falls through to a cheaper one.
- `composition-is-the-inverse-of-decomposition` — `thing.md`'s cohesion discipline
  was decompose-only; composition is its missing inverse, so "insight consolidation"
  was the existing thing-discipline applied to a reserved type, not a new primitive.
  Carries the razor: complete a half-applied discipline before inventing machinery.
- `cross-domain-handoff-is-verified-external-input` (confidence: medium) — a
  cross-domain hand-off is not a link but an import of external input, so it inherits
  `origin: external` quarantine + provenance; reframes the retracted manifesto promise
  and is the design to spec when a second concrete case appears.
- `structural-pointers-need-reverse-edge-indexing` — a relationship in a singular
  load-bearing field (`parent`, `definition`) is still a *declared* edge; the
  `relationships` index must emit it or reverse recall goes blind. The sharper,
  lit-region sibling of `mechanical-assimilation-is-blind-to-prose-dependencies`:
  a forward resolver and a reverse index are two obligations, not one.
- `structure-decides-figures-scale-decides-convention` — the sleeping-bag 2×2
  result: structure is the deciding variable for reasoning correctness, model
  tier is secondary and lands only in convention-adherence; closes the first-2×2
  loop and supports the v2.4 thesis over the demoted model-tier corollary.
- `withholding-is-not-isolation` — a control that removes information from the
  agent's view but leaves it discoverable on the filesystem is defeated by a
  capable agent; an opus-bare trial read the withheld seed `AGENTS.md` and said
  so. A property of capability, not a defect — bare evals need real isolation.
- `framework-reserved-types-need-thing-md-as-single-source` — adding a
  framework-reserved type must update `thing.md` first, then propagate; AGENTS.md
  is a summary, not the source of truth.
- `hard-hooks-require-observable-agent-caused-triggers` — a hook is only "hard" if
  triggered by an agent-caused, agent-observable event; otherwise it is a prompt
  bound to a hook point, explicitly invoked.
- `reflexive-behaviors-are-indexes-plus-prompts` — velocity, trigger-eval,
  conflict-scan, and schema-review are one pattern: a derived index + a prompt;
  the basis of `derived-index.md`.
- `srp-extraction-is-tier-promotion` — extracting content from a low-tier spec into
  its own spec auto-promotes it to Tier 2; following SRP and reducing baseline
  context load are the same act.
- `tiered-loading-is-tiered-reading-applied-to-specs` — the L1/L2/L3 tiered-reading
  model for things, applied to spec loading; the basis of tiered startup + the kernel.
- `version-mismatch-triggers-validation-cascade` — on a framework version mismatch
  at session start, run validation immediately (new rules may invalidate things) —
  don't merely surface the mismatch.
## Pending Decisions

- (none)

## Decisions Made This Session (2026-06-19, retrospective)

- **Second June retrospective written** (`things/retrospectives/framework-retrospective-2026-06b.md`,
  period 2026-06-11 → 2026-06-19, sessions 7–11, v3.10 → v3.14). The first June
  retrospective closed on 06-11; this period tripped both the volume and milestone
  triggers (the floor went scaffold → enforced). Headline finding: **the corrective
  loop reversed polarity** — where the May retrospective criticised answering every
  gap with more prose, this period answered gaps *mechanically and subtractively*
  (coherence, field-registration, touchpoints) and ended by *deleting* two prompts.
- **First real insight triage + composition sweep run** (the discipline specified in
  `session-memory.md`, never before exercised). 28 active insights walked: **3 promoted**
  (`mis-keyed-links-pass-the-floor-silently` → field-registration; `workflow-run-…` →
  `workflow-state.md`; `operative-rules-…` → `framework-kernel`), **2 dismissed**
  (`continuity-briefs-solve-external-state-drift`, claim overtaken; `first-2x2-…`,
  superseded by `structure-decides-…` with the `supersedes`/`superseded-by` backlink
  set). 23 remain active. The composition pre-filter flagged the change-safety cluster
  but the call was *relate, don't merge* — distinct facets that already cross-link.
- **Reflexive scans clean:** validate 0/0/0 across all three corpora, no orphaned active
  insights, no new conflicts; coherence's only findings are two stale `stable` labels
  (manifesto, session-memory) carried forward as a "What Should Change" item.
- **Post-retrospective correction — three stale framings reconciled** (operator's
  three observations): (1) the `coherence-floor` branch was a stale leftover, fully
  contained in `main` and never on the remote — deleted; the retrospective's "push the
  staged work" finding was based on the stale thread and is corrected. (2) The
  cold-start human eval **has happened informally (the brother)**; only a disclosable
  writeup remains, reclassified from "the undone centrepiece" to disclosable-proxy
  backlog. (3) The recurring "deploy when felt" deferrals are largely **felt in the
  operator's confidential law-firm work** (client IP, invisible to the public repo) —
  captured as `felt-deployment-lands-in-undisclosable-work`, which now governs how
  felt-trigger threads are triaged. The retrospective doc was amended to match.

## Decisions Made This Session (2026-06-19, session 11)

- **The framework is a substrate, not a harness — and the orchestration band is the
  only part at risk of forgetting that** (operator's question, agent's frame): a
  harness is a runtime that owns no durable state; MarkdownLLM is durable state +
  rules any runtime operates over. The overlap that *feels* harness-like is
  orchestration. Resolved into the `hook-enforcement-has-three-anchors` insight and a
  new `orchestration.md` section, *"Enforcement: Three Anchors, Not Two."*
- **Enforcement framed as three anchors; interpretation is the portable default and
  sufficient — adapters are optional hardening, never required** (operator's vision,
  affirmed by evidence): the Copilot-then-Claude-Code build history proves the
  interpretation anchor works with zero adapters. The git pre-commit hook hardens the
  one unrecoverable case; `adapters/` hardens only the lowest-consequence
  session-lifecycle hooks. If an adapter ever became *required*, the framework would
  stop being harness-agnostic — so they stay optional by design.
- **Two prompts deleted to shrink the orchestration surface** (operator: "reduce it as
  much as we can"): `validate-before-commit` (its mechanical half is the git hook's
  job, its semantic half is standing prose in `validate.thing.md` — re-performing it
  violated the kernel rule) and `worklog-update` (a single mechanical command, folded
  into `session-end-continuity`'s commit step; session-end drops from two bound
  prompts to one). Closed the action `reviews/REVIEW-mechanical-census-2026-06-16.md`
  had already flagged. Spec-internal reduction, validate + coherence clean across all
  three corpora. Committed as `86a6b08`.
- **Framework bumped 3.13.0 → 3.14.0 at session close** (operator's call): not because
  any single change demanded a minor bump, but to mark the day's accumulated work
  (session 10 onboarding pass + session 11 orchestration reduction) so a domain or
  collaborator picking the framework up this evening sees a newer sentinel than this
  morning. Bumped `.markdownllm` + `AGENTS.md`; `kernel.md` regenerated. **The floor
  taught a rule mid-bump:** `validate`'s `framework-version` check requires
  `.markdownllm` == `AGENTS.md` == latest `CHANGELOG.md` heading — they bump together —
  so the intended "defer the CHANGELOG to push time" was overridden and a `[3.14.0]`
  entry was written now (covers session 10 onboarding + session 11 orchestration
  reduction). **Committed but not yet pushed** — the push is the operator's to make.

## Decisions Made This Session (2026-06-19, session 10)

- **Onboarding surfaces reworked for humans, no framework version bump** (operator's
  call): the manifesto's *Paradigm Shift* was reframed to lead on the reasoning
  processor (execute → *reason within*, landing on programs that find/fix their own
  bugs and evolve) and gained a *System as Collaborator* subsection under Discovery;
  the README was halved (~532→257 lines) into a captivating landing page + repo map;
  `first-hour.md` was realigned to the new installer and promoted draft→evolving.
  These are human-onboarding/tooling changes, not spec-contract changes — the
  framework stays 3.13.0.
- **A one-command installer shipped (`install.sh` / `install.ps1`):** checks
  prerequisites, clones if needed, installs PyYAML + the pre-commit floor hook,
  writes a Claude Code `CLAUDE.md` wrapper, and verifies with `mdllm doctor`. Missing
  git/Python are **offered via the OS package manager with consent (`-y`/`-Yes` to
  skip), never force-installed** — a deliberate "bundle, don't force" line (a script
  cannot vendor an interpreter; consent-based package-manager install is the seamless
  path within its powers). `CLAUDE.md` is gitignored; `*.sh` pinned to LF via
  `.gitattributes` so a Windows checkout stays runnable on macOS/Linux. Both
  one-liners verified live against the pushed remote.
- **Human guides moved to `docs/`; foundational specs deliberately left flat:**
  `operator-guide.md`, `first-hour.md`, `framework-map.md` are not in
  `foundational_specs`/`TIERS`, so the move was contained (AGENTS Tier 2 + catalog,
  README links, framework-map's own `../` links, install-script paths; validate +
  coherence clean, guides still in corpus). The ~25 foundational specs stay at root
  because `{framework_root}/<spec>.md` is a **published, hardcoded resolution
  contract** (`framework-discovery.md` + every deployed domain's `AGENTS.md` +
  `templates/AGENTS.md.template`); relocating them is a breaking cross-repo
  migration, not a tidy. The categorization the flat layout appears to lack already
  lives in frontmatter `type`/`status`, the AGENTS catalog, and `framework-map.md` —
  a folder taxonomy would compete with it and risk drift.
- **The root-clutter instinct was human-centric and ceded to the agent-first design**
  (operator's framing): "this isn't for me, it's for the agent — this is the way it's
  supposed to be." The flat spec list is the interface surface, not mess; left
  untouched for exactly that reason.

## Decisions Made This Session (2026-06-18, session 9)

- **The mechanical/semantic line was reviewed end-to-end and judged sound** — a
  full from-the-inside overview (the framework reasoning about itself). The floor
  owns the decidable, the agent the semantic judgment, the human the initiating
  cue. The dark region is tiered (declared → literal → conceptual); it shrinks by
  promoting prose to declared edges, not by automation, and tier 3 (conceptual) is
  irreducible. Three gaps named: one fixed (below), one built (touchpoints), one
  parked (cross-domain hand-off).
- **The field-registration trilogy completed (shipped v3.13.0):** `known_fields`
  joins `types` and `relations` as the third opt-in, domain-owned `_schema.yaml`
  vocabulary; `CORE_FIELDS` is the tool-owned universal set. Closes the silent
  mis-keyed-field hole (`mis-keyed-links-pass-the-floor-silently`). Warning, opt-in
  — a domain sees nothing until it declares the list.
- **A spec↔floor drift was found and closed, not papered over:** `session-memory.md`
  promised a floor check ("active insight not in continuity brief" + the open-conflict
  twin) that did not exist and disagreed with `validate.thing.md` (which assigned it
  to the agent). Built the checks (Info, corpus-general); reconciled `validate.thing.md`
  to the floor — detection mechanical, disposition the agent's. The promise is now true.
- **`workflow-state` promoted draft→evolving** — exercised on a live domain; the
  reserved types are unchanged, the spec's maturity advanced.
- **The Assimilate beat became a floor affordance — `mdllm touchpoints <id>`:**
  invoked never hooked (the cue stays human, per *The Driver Names The Inflection*),
  computed live not from cached indexes (assimilation must be complete *and* current).
  A discipline turned into a one-keystroke blast-radius read.
- **Orphaned insights linked back into circulation:** the new completeness check
  surfaced 8 active insights the brief named only by a catch-all; each is now listed
  individually above. `continuity-briefs-solve-external-state-drift` is flagged a
  dismiss candidate (overtaken — the framework now has a brief).
- **Version bump deliberately bundled** (operator's call): the four changes shipped
  together as 3.13.0 rather than four daily bumps; domains adopt at the paired
  `refresh` → `--seal`, where the optional `known_fields` lists are added.

## Decisions Made This Session (2026-06-17)

- **Manifesto reworded to v2.4 — the Thesis became the headline:** the spine is
  now *a reasoning processor inside a loosely-coupled software engine, for
  consistency/auditability/integrity/drift-resistance, not determinism*. The
  weak "structure beats scale" claim (largely already established) was demoted
  from central hypothesis to an efficiency **corollary**; claims re-tiered into
  thesis / utility / model-tier; the pre-floor cold-MVP anecdote retired as
  evidence (the framework is not argued from anecdote).
- **Pre-floor adoption anecdotes deliberately not recorded** (operator's call):
  the brother's trading-platform domain and the eco-essentials warm-start both
  ran on the superseded pre-floor architecture; held for a clean, sourced,
  post-floor cold-start rather than banked as unverifiable testimony.
- **The bare-control leak kept as a result, not re-run away** (operator's call):
  a frontier model defeating a withhold-by-placement control is a valuable,
  expected-to-intensify finding; re-running would discard it. Recorded as
  `withholding-is-not-isolation`; the isolation hardening is foreseen, deployed
  when felt.

## Decisions Made This Session (2026-06-16, session 7)

- **The reverse-edge gap was closed in the floor, not worked around (v3.11.0):**
  the workflow-run `definition:` field exposed that the `relationships` index walked
  only `linked_things` — so change-reconciliation's Assimilate beat could not
  mechanically recall a definition's runs (nor `parent` its children). Fixed by
  emitting structural pointers into the index; both forward and retrospective
  reconciliation inherit it because both read the one index.
- **The human cue stayed sacrosanct** (the line not crossed): the request was a
  "mechanical hook into change-reconciliation," but only the *Assimilate* recall was
  widened — no auto-trigger on definition edits, which would have violated *The Driver
  Names The Inflection*. The fix lives one layer down in the floor; the spec's trigger
  semantics are untouched.
- **Captured as a forward-looking rule, not just a patch:**
  `structural-pointers-need-reverse-edge-indexing` — any future singular load-bearing
  pointer must also be emitted into the index, or it becomes an unwalked declared edge.
  `parent` had the same latent gap since introduction; `definition:` made it bite.
- **`mdllm worklog` portability bug fixed in the same bump:** hard-coded
  `framework-worklog` id/title would dangle in a domain repo; now derived from the
  local `AGENTS.md` `name`, with the manifesto link conditional on one existing.

## Decisions Made This Session (2026-06-15, session 1)

- **`change-reconciliation.md` shipped (v3.7.0):** the evolve-phase gap is filled —
  semantic consistency as a human-cued four-beat pass (cue, assimilate, walk,
  seal), fractal across scale, running on the existing indexes. Designed in
  dialogue; the human drove the two load-bearing reframes (change management not
  sweeping; the driver, not the agent, names the inflection).
- **The dark region is structural, not a defect to automate:** assimilate is
  complete only over declared edges; prose dependencies are the human's backstop.
  The textual-trace (grep) tier was added to narrow it to the conceptual residue,
  and immediately caught a `framework-map` spec-count drift the floor could not see.
- **Retrospective mode written into the spec, not left to the model:** structure
  beats reasoning — capturing freeze→reconstruct-from-git→full-corpus-walk lowers
  the model bar so a mid-tier agent can follow it rather than improvise.
- **Invariants/test-suite tier deferred:** the retrospective is the standing
  backstop; a second mechanism for the same job would be redundant machinery.

## Decisions Made This Session (2026-06-15, session 3)

- **The third independent review was actioned in two releases, not debated:** items
  1–2 (workflow-state primitive + bidirectional version-check) as 3.8.0; items 3,
  5–8 as 3.9.0. The throughline the review named — *harvest from where the framework
  is already proven* — drove the choices.
- **Workflow run-state is a reserved-but-draft primitive** (`workflow-definition` +
  `workflow-run`), framed as decomposition applied to processes so it stays on the
  spine. Floor membership check deferred until exercised on a real domain.
- **Upstream version drift is advisory, not a gate** (operator's call): the upward
  leg notifies and lets the expert decide; it reads git's cached remote state, never
  a live network call at session start.
- **WORKLOG kept but generated** (operator's call, both surfaces): `mdllm worklog`
  from the commit stream; CHANGELOG stays external/per-version. 115KB → 21KB.
- **`mdllm refresh` is floor-only** — reports the delta, `--seal` bumps
  `framework_version_seen` after the agent's semantic adoption; never rewrites skills.
- **Model-tier claim demoted to hypothesis; cross-domain promise retracted** —
  honesty corrections, keeping proven utility distinct from the untested tier claim,
  and not promising cross-domain linking until it is specified.
- **`stable→evolving` by the structural-change bar:** only thing/orchestration/
  domain-refresh flipped (each took a structural change this cycle); incidental
  cross-reference edits do not unset `stable`. The rest of the core kept its label.

## Decisions Made This Session (2026-06-15, session 2)

- **Insight management closed as two layers, not one feature:** insight-specific
  lifecycle plumbing (promotion/dismissal triage driver, orphan guard) landed in
  `retrospective.md` + `session-memory.md` + `validate.thing.md`; the consolidation
  problem lifted *out* of the insight layer entirely and was fixed in `thing.md` as
  the missing inverse of decomposition. Shipped as two atomic commits.
- **Don't invent a primitive when a discipline is half-applied** (the session's
  load-bearing reframe, the human's): "insight consolidation" was the cohesion
  discipline `thing.md` already had, run in the compose direction. Captured as
  `composition-is-the-inverse-of-decomposition`.
- **Reuse `supersedes`, broaden its definition:** rather than a new `consolidates`
  relation, composition tombstones via `supersedes` — which forced `belief-revision.md`'s
  "incorrect or outdated" wording to widen to cover replacement-by-consolidation.
  The one contradiction the reconciliation walk caught, resolved in-session.
- **Gap 4 (workflow-state memory) parked deliberately**, not dropped — recorded as
  an open thread with the A/B decision framed, lean-A.

## Decisions Made This Session (2026-06-12, session 3)

- **Rehearsal before tool, deliberately:** the pre-scaffold trials were run
  first so the tool's justification would be measured, not assumed — and the
  post-tool trial closed the loop at 11/11. The full protocol and honest
  reading live in `evals/README.md`; the generalisable lesson in
  `agents-drop-mechanical-birth-steps-not-semantic-ones`.
- **jmtm refresh deferred mid-session:** its working tree had uncommitted
  modifications (parallel session suspected) — single-writer-by-convention
  respected rather than raced.
- **Excluded-trial evidence kept:** harness failures are excluded from the
  report but their result.json files are committed under
  `evals/results/excluded/` — exclusion with evidence, not deletion.
- **Spec prose no longer names framework versions** (review #2 finding 3
  generalised): the sentinel is the only version surface.

## Decisions Made Session 2 (2026-06-12)

- **The fortnight's strategy set by the operator:** point the v3 medicine at
  the periphery and at a user who isn't the author. Week one (this session)
  cleared the prerequisites; the cold-start scaffold eval is the centrepiece;
  model-science work (harder fixture, harness matrix) explicitly deferred
  until the eval lands.
- **Sequencing inside week one:** vocabulary prune first so the examples and
  on-ramp teach the final relation set; examples second; on-ramp last.
- **life-manager populated rather than deleted** (the review allowed either):
  the worked dataset is what a cold-start participant copies, and it now
  demonstrates triggers, provenance, and the floor end-to-end — including one
  *deliberately* overdue task so `mdllm triggers` always has a find (a
  feature; documented in-thing so nobody "fixes" it).
- **`type: dependency` dropped from life-manager:** `parent`/`dependencies`/
  `blocks` fields express hierarchy and sequencing; things are for content.
- **Relation prune shape:** 9 semantic + 4 mechanical relations; the
  `supersedes`/`superseded-by` pair survives because the validator itself
  checks the backlink; decomposition relations remain thing.md universal
  guidance rather than framework-corpus vocabulary.
- **Session-1 decisions** (staleness pass, token-figure convention) are
  preserved in WORKLOG 12 June, Session 1 — removed here to keep the brief
  lean.
