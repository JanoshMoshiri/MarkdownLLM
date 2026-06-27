---
id: framework-continuity-brief
type: continuity-brief
status: live
version: 1.25
created: 2026-06-11
domain: markdownllm-framework
last_updated: 2026-06-27
---

# Framework Continuity Brief

## Open Threads

- **[MCP CROSS-DOMAIN SERVER — Phases 1–3 built & tested; Phase 1/2 live-proven
  2026-06-26]** The cross-domain producing side, on MCP. Design:
  `docs/plans/mcp-domain-server.md` (commits are the ledger). **Shipped (framework):**
  `mdllm mcp-serve <domain>` — Phase 1 read-only face (`manifest://` Server-Card +
  `thing://` resources; `query_things`/`get_deliverable`; egress source-scopes the
  producer's graph, `287012b`); `mdllm imports-check` — Phase 2 freshness /
  re-quarantine-on-drift, reads the source's face **via MCP not git** (horizontal reads
  obey the membrane), report-only, offline=unknown, `aa95673`; **per-thing** commit
  pins; `run_domain_task` — Phase 3 live-agent hand-off, async on the Tasks pattern,
  `--tasks` opt-in, real `claude -p` read-and-emit executor on a background thread,
  adapter-optional; `get_task_result` tool to poll; `wait:true` sync mode
  (`1448982`→`8151343`). `exposed` is now a CORE_FIELD. **Cross-repo wiring:**
  code-architect exposes `jmtm-website-architecture` (own repo); jmtm holds the
  quarantined `external-spec` import (triple @78fd68a) + `.mcp.json` address book
  (`--tasks` on) + hook-path fixed. **Live-proven 2026-06-26:** the Phase 1/2 spec→build
  loop end to end — code-architect's verified architecture drove jmtm's real Resend
  contact-form build (tsc clean, next build static; jmtm changes applied, **not yet
  committed** — operator verifying/config). Boundary held; the agent self-corrected
  (declined to misuse `run_domain_task`). **Topology (operator-corrected):** the
  *skilled* domain exposes `run_domain_task`; the consumer calls with input and applies
  the returned deliverable to its own files. **Pending/next:** (1) a *fitting*
  `run_domain_task` live demo — a "design something new" task
  (`live-agent-handoff-is-for-new-output-not-known-implementation`); (2) the
  framework-vs-bare boundary A/B before any enforcement claim
  (`boundary-respect-was-interpretation-not-enforcement`); (3) **Phase 5** — external
  agent over Streamable HTTP + OAuth 2.1 (the marketing gate); (4) Phase 4 prompts
  (minor); (5) jmtm website reply-to gap (operator's content call).
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
