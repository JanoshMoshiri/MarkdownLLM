# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Format Change (from v2.3.0 onwards)

Prior entries followed [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) with detailed per-feature breakdowns. From v2.3.0, the changelog adopts a **per-push** format:

- **Each entry corresponds to a push to the remote** — the moment changes land on main in the public repo
- **Entries are concise summaries**, not exhaustive lists — `git log` holds session-level detail (`mdllm worklog` views it by session)
- **Version numbers are incremented per push** (patch for fixes/consistency, minor for new specs or behavioural changes, major for breaking changes)

`git log` is the detailed internal record (the commit messages are the narrative; `mdllm worklog` groups them by session on demand). The CHANGELOG is the external-facing record of what shipped.

**From v3.0.0 onwards, entries are generated, not hand-written:** draft with `python tools/mdllm.py changelog --since <last-version-tag>`, then set the version, add the one-paragraph summary, prune noise, and commit. Hand-maintaining a surface derivable from the commit stream was one of the drift sources the deletion pass (transformation plan Phase 2) removed.

---

## [3.37.0] - 2026-08-28

**The Explorer stops being a window that only reads the present.** Explorer 0.3.0 turns the three fixed regions into ones that yield — either side folds away and hands its width to the reading area, persisted per region, and the centre scrolls sideways within itself so the page never does. A commit is now something you can open: it lists the paths it changed against its first parent, classified, and an openable path is read **as that commit left it**, with the lines it added marked and their numbers named in text so the signal survives without colour. That extends the read boundary past the confined filesystem reader into the object store, so it carries its own envelope — source admission decided before any git invocation, path-bearing argument templates re-validated independently of their caller, literal pathspecs, irregular tree entries refused, and blobs governed by the working-tree limits and error codes. Memory reads the way it is used, descending by group with each group a disclosure that keeps its count while folded. A thing's declared references — `informed_by`, `linked_things`, `dependencies` and their kin — become controls that open what they name, resolved through a source-wide identifier index that is single-flight, keyed on source identity, and honest when a source is being written underneath it: an incomplete index reports a reference as *unchecked*, never as absent.

Two adversarial reviews of the increment raised fifty-two findings; each was reproduced before it was fixed. Merge commits had listed **zero** changed files, because `diff-tree --first-parent` prints nothing for a merge. A 565 KB file — inside the documented read limit — failed with "git unavailable", because a patch carries both sides and had been budgeted like a response body. A filename holding glob characters was read as a pattern, so the marked lines described other files. Ten controls in a closed off-screen drawer stayed in the tab order. An ignored directory was reachable by a spelling the filesystem settles. The specification was corrected wherever this work proved it wrong, including the withdrawal of a confident causal account of `--ignore-cr-at-eol` that could not be reproduced in any configuration.

The trace passes end to end: 70 of 70 requirements technically met, 155 tests, 21 of 21 mutants killed, five performance budgets at nineteen of twenty, a clean offline install of the 0.3.0 wheel, and browser evidence re-executed against the fictional demo estate — which now carries structural references so the feature has a public fixture rather than borrowing the operator's own. The Windows installer is rebuilt on 0.3.0 bytes and its full lifecycle passes under identity-isolated verification, including the uninstall that Smart App Control blocked on 0.2.0; that earlier block is recorded rather than deleted. Operator acceptance is recorded for thirty-three dispositions, with the three Windows journeys deliberately held back as unexercised on this build. The artefacts remain unsigned: signing is the one gate left, and it needs a certificate rather than a change.

## [3.36.0] - 2026-08-26

**A workflow run can now prove which version of its process it followed — and the check that proves it cannot be turned on its author.** `workflow-state.md` v0.6 adds **revision binding**: a run may pin `definition_commit`, the committed revision whose definition governs it. Stay-pinned is the default (a definition change never moves a live run), migration is its own meaning-boundary commit, and resolution is rename-proof — current path first, id scan of the pinned tree as fallback, cached per commit behind one resolver so many runs on one definition pay one revision read. The floor reads stage membership *and* edge legality from the pinned revision, and enforces the **self-authorization guard**: a single commit changing both `definition_commit` and `current_stage` on one run is rejected outright, because a run that controls the check's input controls the check. Unpinned runs keep prior semantics and, while still live, draw an Info adoption cue. The same release adds **activation and fulfilment semantics** on existing references — a run's initiating demand pinned in `informed_by`, produced outputs pinning the run back, with an Info cue for a completed run whose chain is absent — plus doctrine separating **execution responsibility from gate authority** (`workflow-state.md`, `operating-model.md` 0.2) and naming the **consumer-owned consumption contract**, where *addressed* means declared intended relevance and never delivery authority. No new types, fields beyond the pin, or indexes: the seams were closed on primitives that already existed. Domain adoption is optional and additive — nothing is retroactive, and a domain that never pins keeps today's behaviour. The sprint was designed in one harness, built in another, and adversarially verified back in the first: the guard was attacked live on the real pre-commit path (re-pin-and-move, stale-pin edge theft, malformed pin) and held every time, with the legal migrate-then-advance path clean. Post-verification the adoption cue was scoped away from terminal runs, where its remedy was unperformable. Framework and both example corpora validate clean with zero findings at every severity; both examples re-pinned to current; coherence carries no Errors or Warnings; full suite 754 passed, 1 skipped in 32:46.

## [3.35.0] - 2026-08-25

**The universal workflow methodology enters the foundation, and the framework learns how its atoms compose.** The operator's Universal Development Methodology v1.0 — seven evidence-gated decisions from define-need to review-verify, each a question with one named output as its exit gate — lands as `universal-workflow.md`, under its truer name: the method is not development-specific. The same day's dialogue extended it (v1.1–1.2): two shapes of application distinguished by where the review lands — accumulative chains refine the work, repeatable series refine the process — and capacity resolved once at the cut, where "automate it" spawns a child arc whose deliverable is a new repeatable definition, one shape manufacturing the other. A companion spec, `operating-model.md`, defines composition: the module as the unit running many atoms, the metabolism (arcs deliver operating state, repeatable loops maintain it, sensors seed the next arc), fractal radii over `parent`/`dependencies`/`informed_by`, estate-radius composition over served faces, and five declared dimensions that make a composition auditable — adding no mechanism, and carrying its own admission rule: growth only on cross-corpus convergence. A mid-session channel correction is recorded on the spec itself: the methodology was first hosted as an exposed thing, conflating the domain↔domain porch axis with the framework→domain refresh axis; foundation travels by version + domain-refresh, so the atom moved to the spec layer with its id — and every edge — intact. `substrate-floor-development` now names the spec as its parent; a parked plan records the scaffold direction (guided birth walkthrough, not a template drop). Framework and both example corpora validate clean; coherence and generated artifacts current — the coherence check caught the TIERS map lagging the catalog mid-session, exactly as built to. Full suite: 741 passed, 1 skipped (0 failures) in 34:16 — a live measurement of N7's budget breach, recorded on F10 as the signal to pull it into the next sprint.

## [3.34.0] - 2026-08-22

**A fourth harness adapter ships alongside the substrate review's session-start fixes.** The `perplexity` adapter — the fourth registered harness, modeled on Cowork — renders two Perplexity Skill surfaces from one bundle: the full `markdownllm-bootstrap` operator skill (lifecycle, branch map, ambient-credential git transport, `--authorize-once` publish) and the friendly `markdownllm-bootstrap-friendly` skill that greets the operator by domain and hides framework jargon. Bootstrap is ambient-credential only (`gh auth setup-git`), fails closed on any pasted PAT (`GH_PAT` / `MDLLM_GIT_TOKEN`), and never bakes tracked mutations (`domain-kernel`, `session-start`, `publish`) into spin-up; the friendly surface reads an operator-private `FRIENDLY_PROFILE_NAME` / `FRIENDLY_DOMAINS` subset from the gitignored rendered config, so no private identity or domain list is committed to public source. Both skills pass `agentskills validate`; an env-gated leak guard confirms the operator's private identifiers are absent from all committed source. The same release lands the substrate review's session-start remediation — the floor no longer renders unseen state as a definite answer, session-start stops re-reading its own inputs, and the framework-root lifecycle-hook budget is respected — plus the `a-scaffold-cannot-birth-its-own-author` insight. Full suite: 698 passed, 8 skipped (0 failures); framework and both example corpora validate clean; coherence and generated artifacts are current.

## [3.33.0] - 2026-08-20

**Repository state becomes an explicit transaction boundary, and automatic authority now fails closed.** The pre-commit floor freezes one candidate tree for boundary, validation, coherence, and reconciliation cues; worktree, index, and immutable full-commit views now keep validation, provenance, MCP egress, and significant reads attached to the bytes they name, with optimistic HEAD/index checks around writes. A strict YAML boundary and one structural-reference registry remove duplicate-key and cross-consumer drift, while triggers return total typed outcomes, workflow runs cannot self-authorize transitions, strict calculations preserve decimal lexemes, and failed eval legs cannot report success. Repository-supplied command/HTTP imports require clone-local hash-bound trust; scaffold and hook installation preserve unrelated/operator state with explicit recovery; Cowork assembly uses the shared lifecycle/sync ports; distributable templates are instantiated under test; CI, dependencies, installers, and Cowork framework acquisition are pinned. Publication is a deliberate authority boundary: only literal `git.autopush: true` enables standing sends, while false, absent, malformed, or unreadable policy is off and `doctor` explains why; domains that previously relied on absence being on must opt in explicitly. Public claims now distinguish deterministic structure from probabilistic interpretation and separate contract emission, receipt, observed reading, applied evidence, and validated outcome. Historical harness evidence remains build-specific; fresh Claude, Codex, and Cowork acceptance is not implied by this local remediation.

## [3.32.0] - 2026-08-18

**Harness lifecycle support becomes an execution-tested port, and the third adapter reaches a publishable build checkpoint.** The Claude and Codex projections now share neutral lifecycle, runtime-resolution, diagnostics, install/scaffold and no-adapter contracts while keeping trust and permission boundaries vendor-specific; Claude's entry surface was reconciled, and Codex Gate 7.0 closed on a directly opened Windows QMS domain with dependency-probed manual launch, non-cached session orientation, and an `estate-sync --require-fresh` route that turns a restricted task's cached result into the approval signal plain lifecycle sync cannot emit. The QMS pre-commit and autopush consequence passed without changing either harness's hook file, and a later operator-run fresh task independently returned `up-to-date`, full open-loop/trigger orientation, and working Git reads. The same release publishes Cowork adapter Phases 0–3 as an explicitly experimental checkpoint: a third registry projection, full Tier-0 contract emission, guarded publication, neutral workspace assembly, and a framework-rendered/hash-checked private bundle built from the live estate; Cowork local transport, remote/local live evidence, compatibility claims and rollout remain open in Phases 4–7. The release walk covered `interface`, `session-memory`, `git-workflow`, `orchestration`, `validate.thing`, launch/runtime and adapter registries, scaffold/diagnostic/session surfaces, root/template/operator guidance, QMS's authored entry and regenerated kernel/indexes; findings were consistent, while the known `domain-refresh`/README/first-hour capability residue stays owned by vendor Phase 7 and no live-domain estate sweep was performed. Full suite: 515 tests; framework and both example corpora validate clean; coherence and generated artifacts are current.

## [3.31.0] - 2026-08-11

**The review loop — eight cold reads run to the point where the instrument measured itself, and the experiment is the release's real deliverable.** After v3.30.1's single cold review proved author-blindness, the operator commissioned a loop: fresh, unprimed, tier-order adversarial review each round, verify → fix → relaunch against the fixed HEAD, until dry. **It never went dry, and the measured reason why is the finding** (`reviews/REVIEW-loop-2026-08-10.md`; `an-adversarial-review-loop-converges-on-its-own-fix-residue`, exposed). Forty-four confirmed contradictions were found and fixed across eight rounds — among them defects that had shaped real field behavior: the entry file's universal status enum against its own floor note, the pre-write doctrine split between generator and kernel (settled: specification + write skills required, write.thing v2.3), the hook census's pre-v3.26 "only pre-commit is enforced" story, the inverted anchor defaults on the session-start hooks (principle made uniform: an unadapted hook's operative anchor IS interpretation), the kernel's own anchor example licensing skipped index maintenance ("label the act, not its net"), `session-end:`'s ten-release double definition (settled: the ritual's routine closer, stray changes swept and named), and "triggers read committed state only" reclassified from tool mechanics to discipline guarantee (the evaluator reads the tree; the invariant is what makes tree and HEAD coincide). But the curve is the point: finds 6→7→6→6→7→4→3→3 with severity decaying faster than count, core clean from round 5 except where fixes scattered, and fix-residue share rising 1/6 → 1/3 → **3/3** — by round 8 every finding was an incomplete correction from rounds 6–7, because a fact restated on N surfaces and fixed on k leaves N−k contradictions now split against the fix, and nothing enumerates the siblings. Meanwhile the control group held: **derived surfaces (kernel, managed blocks, catalogs, censuses) appeared in zero findings across all eight rounds.** The conclusion, sealed as doctrine in the insight: looping is a measurement instrument, never a resolution mechanism — delete or derive restatements, check them mechanically (`mechanical-coherence-checks-backlog`, hold already lifted), run ONE cold read per substantial release (the measured answer to the response plan's open R3, amended with the dose–response data), and probe the execution flows with runnable scenarios (the fresh-clone doctor probe outperformed every prose read). Round-8's three residues fixed at close; four minors logged in the record, deliberately unchased. Estate regenerated twice in-loop for generator-string corrections; 282 self-tests, validate + coherence clean throughout; review ordinals left unminted pending the operator's ruling on the collision with the concurrent external review.

## [3.30.1] - 2026-08-09

**The ninth review — a cold read certifies what the author could not, and seven survivors fall.** Commissioned by the operator hours after v3.30.0 rolled out estate-wide ("nothing is fixed unless tested"): an independent agent with zero session context and an adversarial brief — recent changes get *more* suspicion, and a clean verdict must name what it verified. It confirmed the reconciliation's seams held where derivation rules (spec↔generator: zero findings; kernel byte-identical; hard hooks, autopush doctrine, reserved statuses, scaffold delivery, spot-checked constants all evidenced consistent) — and found **seven contradictions the author's walk missed, every one in hand-restated prose**: the kernel's always-loaded path still describing insight disposition via the brief retired in v3.17 (validate.thing.md kernel block → v2.5, kernel regenerated); validate.thing.md's Layer-2 table instructing the agent to re-derive the retrospective-cadence check its own kernel says moved to the floor in v3.24.0; thing.md restating the trigger-type count as four, three releases after `type: import` made it five (v2.19 — count removed, authority named); trigger-specification.md's fire conditions predating `terminal_statuses`, so spec-letter and floor disagreed on whether a trigger fires in any domain with a declared settled set (v1.4 — both conditions read through `is_terminal`); example-things.md's four-item "reserved types" list against the tool's thirteen, implying `example` itself is reserved (v1.1); derived-index.md not knowing its own fourth index — provenance, standard and tool-rebuilt since v3.2x — with the CLI docstring and operator guide equally blind (v1.1, five surfaces); and CORE_FIELDS violating its own admission criterion — thing.md's Recommended vocabulary (`priority`/`tags`/`confidence`/`version`) unadmitted, the framework root itself forced to register its own framework's fields, the regression test using `tags` as its flaggable example (fields admitted; test re-pointed at a genuinely non-framework field). Cosmetic residue swept: stale "Level 4" vocabulary, the `mcp-serve` map edge missing `--http`, the `TIERS` pointer at the shim. Full report: `reviews/REVIEW-independent-2026-08-09.md`. The reviewer's structural recommendation — promote restated counts and enumerations into derived surfaces — lands as candidates in `mechanical-coherence-checks-backlog`. 282 self-tests; validate + coherence clean.

## [3.30.0] - 2026-08-09

**The substrate reconciliation — the framework walks its own four beats over itself, and restated facts get one owner.** Two 2026-08-08 field sessions in a layered harness misbehaved while *complying* with everything they were handed; the full-substrate sweep that followed (every spec, guide, template, generator, and the tool surfaces the specs make claims about) traced the defects to the framework root: contradictory contracts held simultaneously, and two floor surfaces mislabelling their own output. **The floor fixes, first because the floor must not lie:** trigger evaluation splits `fired` from `upcoming` end to end — `evaluate()` returns four buckets, `mdllm triggers` prints an Upcoming section, and session-start's orient view stops printing 30-day look-aheads under "Triggers fired" (the label that made one quiet domain's 22 look-aheads read as a backlog under strain); the session gate's no-attestation finding now names the fresh-clone reading alongside the skipped-contract one, and `doctor` attributes a gate-only block as *setup ordering* instead of "validate failing" — the cry-wolf line that fired at every fresh gated clone, field-verified against a 200-thing corpus that validated clean moments later. Enforcement unchanged in both; only the labels were false. **The contradiction walk:** git-workflow.md v1.4 carries autopush through its last three authored holdouts (§Who Commits, the Summary table, §Autocommit-and-publication — the v3.26 walk had missed three restatements in the file it was editing); orchestration.md v1.12 names the generated Session Start block for what it is, a framework-installed standing binding, superseding "no framework-level bindings are inherited"; the guide v2.10 retires its inline hand-written AGENTS.md template (a fifth competing startup sequence, carrier of the twice-drifted hard-hook count) in favour of the managed-blocks shape, and its checklist stops contradicting its own Step 1; framework-discovery v2.1 and domain-refresh v1.4 defer to the generated block and the sentinel catalog (the hand list here had omitted orchestration.md — the spec carrying the hard hooks); session-memory v1.3's ritual is "deliberate", matching its own definition; thing.md v2.18 classifies `skill`/`prompt` (framework-defined, domain-usable, fixed vocabulary) and three differently-incomplete reserved-type lists (validate.thing.md v2.4, root `_schema.yaml`, the scaffold template) now carry the full set and name the tool as authority. **The routing gap, closed in the generator:** tier-routing routes `prompts/` from the filesystem exactly as it routes skills — delivered (v3.24.0) and named (Session Start) but routed nowhere, the prompts were absent from every reading list derived from the entry file, which is how a bootstrap handoff inherited the omission invisibly — and the skills line names the specification and write skills required reading before any write (kernel, `write.thing`), ending the "per intent" contradiction an agent obeyed into an unauthorised write. Scaffold fills managed blocks after `prompts/` lands so the birth commit cannot drift against its own build. Prompt templates catch up with their specs (in_progress_count dead two releases, now gone; import triggers in; terminal-status wording replaces hardcoded status sets). **Sealed:** `substrate-reconciliation-2026-08-09` (`type: decision`, exposed, inputs pinned) records the supersessions and rules the re-open condition spent on derivation, not enforcement — `pretooluse-action-boundary-gate` stays parked because both field agents complied with the contract they were routed, and enforcing a contradictory contract enforces the contradiction. Every scaffolded domain shows domain-kernel DRIFT until it regenerates (`mdllm domain-kernel .`) — the refresh path, by design; the pre-v3.30.0 backfill entry names it. 282 self-tests passing; validate + coherence clean.

## [3.29.0] - 2026-08-08

**The porch goes over the wire — Streamable HTTP lands as the promised transport swap, with a probe control sized to exactly what it authorizes.** Phase 1's stdio loop shipped carrying a design promise ("swapping stdio for Streamable HTTP later touches only the loop"); this release cashes it. `mdllm mcp-serve <domain> --http [--port N]` serves the identical exposed face over HTTP: one dispatcher shared by both pipes (error mapping cannot drift between transports), one endpoint — `POST /mcp`, JSON-RPC in, `application/json` out, notifications 202, GET 405, because the porch stays poll-only and git stays the state — and a re-scan per request, so a long-lived server serves the repo as it stands, never as it stood at bind time (design guardrail 3 made mechanical). The consumer side crossed in the same release: the `.mcp.json` address book accepts `url` entries alongside `command`, and `imports-check`/`estate-check` read a served face over the wire with membrane semantics unchanged — unreachable = "sync state unknown", never a silent fresh. **The boundary is a refusal, not a warning:** a non-loopback `--host` exits with the reason — a routable porch without real authorization is an honour-system control, the exact class the Phase 3 revert ruled out — and Origin-carrying requests are checked against loopback origins (the DNS-rebinding defence the Streamable HTTP spec requires). For crossing machines *as the operator*, `--token` mints a per-run bearer token, printed once and dead with the process — never the long-lived key the doctrine bans; possession IS being the operator, and the consumer's url entry carries it as `headers`. **Live-proven, honestly bounded:** jmtm-software read code-architect's face over HTTP end to end locally, and the full probe stack (loopback porch + token + cloudflared quick tunnel) was proven to the public edge — authorized reads served through the tunnel, tokenless requests 401'd at the porch itself. The remaining external-agent test stays open for a reason outside the framework, recorded in the design doc: an Anthropic Cowork VM's egress is a default-deny allowlist that refuses the CONNECT before any packet leaves the VM, and the VM agent's git-backed-face suggestion is noted *against* the decided two-axis rule (horizontal reads cross through the face, never the source's git), not adopted. OAuth 2.1 remains the other-party gate, with the build shape now stated: resource-server-side validation in the floor, an external authorization server when the need is felt — never hand-rolled. Walked: interface.md v1.2 (the porch has two pipes, same membrane), operator-guide, the design draft's Phase 5 split into transport (landed), probe control (landed), authorization (pending). 8 self-tests (282 total); validate + coherence clean.

## [3.28.0] - 2026-08-08

**The session gate — a contract-less session becomes loud at its first write, in any harness, with no adapter.** The gap this closes was lived, not hypothesised: Cowork sessions from 2026-07-22 onward never loaded the Tier-0 contract (AGENTS.md declares itself "always loaded", which is a fact about one harness written as a fact about the world), and nothing said so — the floor stayed green because the only controls those sessions could skip were interpretation-anchored ones, which leave the same evidence skipped as performed. The estate integrity sweep (`cowork-integrity-estate-sweep`) established the extent mechanically (8 of 14 repos, ~163 commits), rectified every affected repo under its own agent's contract, and evaluated three prevention shapes against the anchor taxonomy; this release builds the winner. **Mechanism, two small pieces:** `mdllm session-start` — the command whose output *is* the operative contract — now records a per-clone attestation (`<git-dir>/mdllm-attest`, timestamp + HEAD; uncommittable by construction), and `mdllm validate` gains `session_gate_findings`: a domain declaring `options: {session_gate: warn|strict}` requires a fresh attestation (24h window) before any commit — absent, unreadable or stale fires Warning (`warn`) or a commit-blocking Error (`strict`) whose message names the one-command remedy. The claim is deliberately narrow and stated in the check's own docstring: the attestation proves the contract was *emitted into this clone's session*, not that it was heeded — the heeding residue is the register problem (`assistant-register`), a categorically smaller failure class than never-saw-it. **Anchor discipline preserved:** the gate runs inside the existing pre-commit `validate` leg (git-fs — the class of control that held in every breached session), adapters stay optional (the hardened Cowork bootstrap v0.4.0 keeps workspace assembly; it is no longer the difference between working and not), and the scaffold template now births domains with `session_gate: strict` so the fail-safe is a property of birth rather than a retrofit. Framework root declares `warn` (release/CI flows legitimately commit outside a domain session). **One boundary the first CI run drew for us:** the *birth commit* is exempt — a repo with an unborn HEAD holds no committed contract to have read (the contract files are being created in that very commit), so the gate holds from the second commit onward; without this, scaffold's own first commit was blocked by the strict gate its template had just declared, which CI caught the same day the gate shipped. Spec coverage shipped with the floor change — validate.thing.md v2.3 body + kernel block — because this same release stream fixed v3.19.0's `terminal_statuses`, which shipped enforcement with zero spec coverage and hid for six weeks. 192 floor self-tests (+7); validate + coherence clean across all corpora.

---

## [3.27.0] - 2026-08-05

**Watched is not owned — and the membrane learns to say why.** A regulated estate's vantage domain exposed a build brief on its porch for the framework to pull — the membrane carrying its own bug reports upstream, each ask evidence-backed and re-verified the day of writing. Four asks, all built. **The watched line (Ask 1):** orientation counted any non-terminal, non-knowledge thing as an open loop — `origin` never entered the computation — so a consumer domain's mirrors inflated its count in proportion to how *well* it consumed: the estate measured 58% → 81% distortion in a single session purely by landing the imports it was ruled to take, with owned work unchanged at five. An orientation figure that degrades when the system improves measures the wrong thing, and a number the reader learns to discount stops protecting the real loops inside it. `_orient_forward()` and the assistant register now partition by `origin: external`: **`Open loops (n)`** (forward work this domain can advance) and **`Watched (n)`** (the source's — or the world's — state, restated; freshness via `imports-check`). Exclusion, not hiding; and a fired trigger on a watched thing still reaches attention through the fired-path re-entry, which is exactly how `type: import` triggers keep their voice. Same defect-shape as v3.19.0's `terminal_statuses`, one membrane out. **Pin honesty (Ask 2):** an unquoted all-digit short hash (~1 in 16) parses as YAML `int` and false-reported a healthy import **STALE against its own pin** — prescribing a re-quarantine that spends a human's attributed flip on nothing. Two estate domains hit it independently eight days apart, each patched locally with no shared knowledge (the floor-is-short signal), and the framework's own CI then flaked on it within hours of the brief naming it: three imports tests mint identical commits on CI runners, so one all-digit hash fails all three together. `_pins_match` now normalises both sides to `str` at the single comparison seam; the flake is dead, and the deliberately all-digit regression pin stays. **Two stale species (Ask 4):** a source-side commit touching only what egress strips (a `triggers:` block) moves the pin with no crossable change; `imports-check` now discriminates **`stale (content identical)`** — "update the pin; re-quarantine not owed" — from **`stale (content changed)`**, which keeps the ritual. Re-quarantine is spent only where warranted. **The exposure question (Ask 3, approved 2026-07-28, landed at last):** `write.thing.md` v2.2 asks at creation — *does another domain need to rest on this?* — with three cheap answers: **yes** (`exposed: true`, after checking no other domain owns the fact), **no** (a real answer, not a deferral), **not yet** (in the body, with the condition that would flip it). The evidence for authoring-time: a porch that went 3 → 50 exposed in one retrofit sweep, unread for days, past a trigger written for exactly that event — a cliff where a trickle would have been absorbed. **Recorded unbuilt:** an `mdllm import` command (the brief's observation — 69 hand-authored mirrors in one session, 26 malformed on first pass, every one caught at the boundary); revisit on second independent sighting. 4 self-tests (261 total); validate + coherence clean. Plan: `vantage-brief-cluster`.

## [3.26.1] - 2026-08-05

**The cue set meets its own criterion — `insight` and `decision` join the definition surfaces.** The v3.26.0 cue predicate shipped with `DEFINITION_SURFACE_TYPES` defined by the comment "types whose entire function is to be reasoned from" — and omitted the two reserved types that are *literally* that: an insight exists only to be reasoned from, and a decision is reasoned-from the moment anything cites it. Found felt within a day: the operator worked porch-bound insights in another domain and no cue fired, because an ordinary-thing fan-in ≥ 3 gate was standing in for a membership the set's own definition already granted. Both types now cue on modification with no fan-in requirement; the verdict stays the driver's, the advisory stays non-blocking, fresh things stay silent. Explicitly ruled *not* built (operator, voice, 2026-08-05; recorded in `substrate-currency-sweep`): `exposed: true` cueing unconditionally, and schema-declarable set/threshold à la `terminal_statuses` — both doctrine-compatible, neither yet felt. Shipped alongside the sweep's correction pass: the first unscoped whole-substrate Assimilate since the narrative surfaces last held (README at v3.17.5 + nine releases; the publication-debt step reaching all five end-session surfaces where v3.26.0's walk reached one; a creation template still shipped for the type retired at v3.17). 1 self-test (257 total); validate + coherence clean. Plan: `substrate-currency-sweep`.

## [3.26.0] - 2026-08-04

**Publication becomes mechanical; retrospection gets a clock; the cue question gets asked.** The estate crossed the dimension line v3.22.0 predicted and deferred on ("`git.autopush` deliberately deferred until a collaborator exists"): work went multi-domain within a single day, domains consume each other's porches through floor-driven sync, and the collaborator arrived as the operator himself — across machines, cloud sessions, and cross-domain sessions. In one working day he overrode the no-push rule repeatedly, which is deploy-when-felt's release condition met and also the evidence that per-push deliberation had decayed into ceremony. **The push leg** (`estate-cadence-cluster` Phase 1): the post-commit hook publishes each floor-validated commit via **`mdllm autopush`** — default **ON**, opt-out per repo (`git: autopush: false`; absence means on, ruled by the operator: the opt-out set is the small one). Transport of already-committed, already-validated state — the mirror of estate-sync's fast-forwards, under the same doctrine: bounded (`GIT_TERMINAL_PROMPT=0`, timeout), **`--force` structurally outside the vocabulary**, a rejected push surfaced as **DIVERGED on the push side** and never resolved, offline degrading to publication debt. The `estate-sync --status` report **inverts into an anomaly detector**: under autopush, any `ahead +n` line means something to route, not something to remember. The doctrine revision is a recorded decision (`autopush-moves-the-deliberate-act`): the deliberate act moved *up a level* — from each push to the per-repo declaration and the routing of every non-clean outcome — and `premature-publish-manufactures-discipline-eroding-urgency` **stands unrevised**: a release publish is a different act sharing a verb, so release surfaces (the framework root's public repo) carry `autopush: false`, the default-on rule applied honestly as their own opt-out. **The walked set, recorded per the new release-walk beat:** the first framework-level run of change-reconciliation's Assimilate pass found the push doctrine restated on ~15 surfaces across four layers (specs + kernel extraction, tool strings, thirteen generated domain kernels, authored domain skills and operator docs); 13 of 15 collapsed to **one generator string** — regen reconciles them — and the authored remainder was walked one by one (two outcomes: revise; one class ruled consistent: the sync walk itself still never pushes). Two insights from that single pass: `inflection-candidates-are-computable` (the cue *verdict* is human; the cue *question* — modified ∧ reasoned-from — is a mechanical predicate the floor holds both operands of at commit time) and `a-generated-surface-collapses-its-walk` (walk size is a property of deployment, not of the change: restatement count IS reconciliation cost; promote to derivation when a walk revisits twice). Both built: **`mdllm candidates`** runs in the pre-commit hook — staged *modified* things only (additions carry no risk, the spec's own premise), definition-surface types always, ordinary things at fan-in ≥ 3, one advisory cue line naming `mdllm touchpoints <id>`; plus the **serve-side notice** the membrane always lacked (`exposed: true` modified → "this change publishes"), closing the one membrane direction with no eyes at the exact moment autopush made its silence faster-moving. Never blocks, never scores, never runs the pass — saying no to a named question is a decision, where not being asked was drift. **Retrospection** (Phases 2–3): the v3.24.0 cadence sensor gains the moment and the altitude — one line at **session start** (t=0, where orientation already says what needs the operator) and a **RETROSPECTIVE DEBT roll-up in `triggers --estate`** (first live sweep: one domain flagged, the young/dormant gates silencing the rest); load-bearing, not hygiene, because change-reconciliation routes every missed cue to the retrospective and a net-beneath-the-net with no clock is down exactly when the cue-missing rate is highest. And the **estate retrospective is named, not built** (`retrospective.md` → The Estate Retrospective): a `type: retrospective` authored in the vantage domain, estate as subject, on a 30-day clock against the domain-level 60, consuming domain retrospectives as they consume session-ends — with the **direct-read licence written into the definition** (the membrane cannot be audited through the membrane it audits; every claim still anchors to a hash, a dated output, or a named statement) and the boundary kept (observes everywhere, rules only on the genuinely cross-domain). The discovered instance predates the name — a vantage domain's membrane assessment with every property but the type declaration — and the first formal one is chased by a dated trigger, so it will exist because a trigger fired, not because the operator remembered. **The release walk itself is now a beat** (`git-workflow.md` → The Release Walk): Assimilate estate-wide, Walk (derived by regen, authored by judgement), Seal (decision thing + the CHANGELOG records the walked set), then the still-deliberate publish. Phase 0 pre-flight: six domains' `git: branch` configs corrected to the branch that exists — a mechanism built on a lie mechanises the lie. 15 self-tests (256 total); validate + coherence clean. Plan: `estate-cadence-cluster` (rulings 2026-08-04, operator, voice).

## [3.25.0] - 2026-08-02

**The floor does every sum.** Two money-shaped domains reached the same wall independently — a derived figure asserted by reasoning, contradicted later by source. One carries a resolved `conflict` whose entire subject is an agent arithmetic chain over 54 transactions that produced a closing balance £89.53 from the bank's; the other carries a `decision` that names the missing tool *in words* ("a deterministic Python tool that computes the totals ... the agent transcribes and reasons; the tool does every sum") and holds itself at `confidence: medium` until it exists. Arithmetic was the last purely mechanical class the framework still left to reasoning, and it fails quietly: a line item changes, the total does not, and nothing can tell — because nothing knew how the total was reached. **The primitive is not maths.** It is the **declared derivation**: `computed: {field-path: expression}` states in the thing how a figure was reached, and the floor evaluates it — on demand via **`mdllm calc`** (the ingestion surface: the tool sums, the agent transcribes) and again at every commit via `validate` (the surface that makes the first one durable). Same two-surface shape `triggers` has had since v2. Expressions reach three sources: frontmatter (including a path *through* a list of mappings, which yields that key's column), **body tables** (`table("Transactions").Amount[Category == "Fuel"]` — resolved by nearest preceding heading, filtered by boolean subscript, with columns matched tolerantly enough that `.Amount` reaches a header written `Amount (£)`), and **the corpus** (`things(type="expense-record", tag="fy2025").net_amount`). Body-table support is what makes "transactions are data in a body, not things" a safe ruling rather than a hopeful one. **`provenance.md`'s "no calculation may rest on an unverified external thing" stops being prose:** within a thing, computing an unverified statement's totals is *allowed* — that is precisely how a human comes to verify it — and every line is stamped `UNVERIFIED`; across the corpus, quarantined things are excluded from the aggregate **and named individually**, because a total that silently dropped its evidence reads exactly like one that had none. Two neighbouring exclusions get the same treatment: a thing is excluded from its own selection, and a selected thing missing the field refuses with the ids rather than returning a smaller denominator. **Money is held properly**: `Decimal` never float (a YAML `16.80` routes through `str`), `£1,200.00`/`(45.60)`/`-£8.50` parse as they arrive, `round()` is HALF_UP not banker's so an operator checking by hand gets the same answer, and there is no implicit tolerance — comparison is exact and rounding is declared. **No `eval`**: expressions are parsed with `ast` and walked node by node against a whitelist (comprehensions, lambdas, conditionals, `**`, attribute access, `__import__` and `open` are each pinned as refused in tests). Every refusal names its reason — the no-silent-default law applied to arithmetic, where a zero standing in for "I could not tell" is the whole failure mode. Disagreement is a **Warning**, **Error** under `options: {computed: strict}`, mirroring `options: {quarantine: strict}` exactly: a filed return whose box is arithmetically odd but is *what was actually filed* must stay recordable. Quiet when healthy — the estate's thirteen domains produce zero new findings, because a domain that declares no derivation gets none. `computed` joins `CORE_FIELDS` on the established second criterion. No new foundational spec: the rule lands as short sections in `thing.md`, `validate.thing.md` and `provenance.md`, and the grammar lands in `docs/calculation-reference.md`, because calculation is invoked rather than ambient and 23 tier-0 specs is enough. 62 self-tests (241 total); validate + coherence clean. Plan: `deterministic-calculation`.

## [3.24.0] - 2026-08-01

**The self-describing axis gets eyes — and the sensors' first catch was the floor itself.** A full-estate sweep (twelve domains + root, ~660 things) found every drift class the operator had been fixing by hand was the same shape: a *definition surface* diverging from the reality of usage — kernel prose behind the schema, verbatim-template skills under weeks of real sessions, prose triggers everywhere with `mdllm triggers` passing vacuously, one domain hard-blocked at the commit boundary by kernel-block drift that `doctor` misattributed to hook failure. The framework routed divergences diligently on the data axis and had almost no sensors on its own fractal claim that definitions are things too. This release is those sensors, plus the birth surfaces that stop the classes recurring — zero new primitives, all advisory, every check same-builder-keyed and quiet-when-healthy. **Floor sensors (`cohesiveness-sensors` plan, Phase 2):** `validate` gains quarantine age (`origin: external` unverified >30d — provenance.md's own row, previously unimplemented), retrospective cadence (60+ active days, young and dormant domains silent), and trigger structural completeness (Warning only when a declaration gives neither the floor anything to evaluate nor the agent anything to judge — prose-`condition` triggers are a legitimate pattern and stay quiet); `coherence` gains the template-residue sensor (a `type: skill` thing or entry file retaining ≥3 scaffold placeholders is "scaffolded, never authored" — the sweep's headline class, previously invisible: stub skills validate clean); `session-start` now *evaluates* triggers on the default path (the spec's "primary evaluation point" was an instruction to the model, never a computation); `index check` verifies the `generated_from` anchor still resolves and the stamped framework version is current (found live: the root provenance index pinned to a commit the July history rewrite destroyed, reporting "in sync" over a dead anchor); `doctor` now attributes a blocking hook to the failing check instead of "failed to execute". **The catch:** the sensors' own self-test exposed that YAML 1.1 parses a bare `on:` trigger key as boolean `True` — every dependency trigger in the estate was silently unfireable, and filled relationship triggers were misreported as unfilled; `parse_frontmatter` now normalizes it at the single shared entry point, and the dependency evaluator gains the honest skip it owed the no-silent-default law. **Birth surfaces (Phase 3):** scaffold finally delivers `templates/prompts/` (the generated session-start block has named `evaluate-triggers`/`surface-attention` since the kernel-shape shipped — no domain ever received them; linked_things stripped on egress, the membrane rule applied to birth); newborn settings and the adapter example run `estate-sync` *ahead of* `session-start` (hard hook 4 — every prior newborn was born without it, and the generator's hooks block now carries all four); AGENTS.md §Thing Types becomes a generated `types` block derived from `_schema.yaml` (the authored list lagged the schema in most active domains — repeated drift promotes a fact into the floor; opt-in, absent blocks skip); `CORE_FIELDS` registers the ingestion triple the spec mandates and the tool already reads; `domain-refresh.md` gains the backfill step for pre-v3.20/pre-v3.24 births. **Spec reconciliation (Phase 4):** `interface.md` (64 days stale, the oldest foundational spec) learns the membrane is an output route whose consumer is another domain's agent; the manifesto's "cross-domain hand-off foreseen but not yet specified" is revised — it shipped two versions ago; the operator guide documents the four subcommands it omitted; `domain-specification-guide.md` names the prune-or-park route for specification that outran usage — emergent detail cuts both ways, and manufacturing usage is not a route. All nine kernel-shaped estate domains regenerated in step. 15 self-tests (176 total); validate + coherence clean. Plan: `cohesiveness-sensors` (from the 2026-08-01 estate sweep).

## [3.23.0] - 2026-07-28

**The membrane's direction becomes a ruling, and attention learns to cross it.** Two estate-vantage findings arrived in one week — a private-estate plan showing 15 trigger conditions the floor cannot evaluate (one had *fired unseen* when a source's face went from 3 to ~50 exposed things), and an independent review diagnosing the estate as "instrumented on the consume side, blind on the serve side" with six proposed fixes, three of which would have coupled the domains. The operator upheld the objection, and `provenance.md` now carries it as doctrine — **The Membrane's Direction Is a Ruling, Not a Backlog**: a producer never learns who consumes it; publication is an honest commit to the face; delivery is the consumer's poll. No outbound address book ever (`who_i_know` stays empty by ruling, and its code comment now says so); withdrawal gets **etiquette, not machinery** (deprecate on the face first — the pin moves, every consumer's next check sees it); a cross-domain work item has **one owner** and everyone else imports it, so completion arrives as `stale` without a reverse map. What the ruling *permits* then shipped, all consumer-side or operator-axis: **face coverage** in `imports-check` (every address-book source read, including those with zero imports — "offers k, imported j" — closing the hole where a consumer scored a perfect report over an unread face, since coverage counts only pins that exist); **`type: import` triggers** (`state_is` over watched imports, `porch_offers_unimported` for the populated-face case — the fired-unseen trigger class is now mechanically evaluable, lazily, one membrane crossing per run); the **ingestion triple** (`source_system`/`source_ref`/`source_checked` — `origin: external`'s second species gets its own staleness clock, reported as `ingested` with oldest-check instead of filing as coverage failure; the standing insight's evidence gate was satisfied by the independent sighting); and **estate reads discover local clones** (`estate-check` with no args, `triggers --estate` with per-domain roll-up) via the v3.22.0 repos-not-membranes precedent — "N local clones walked, a filesystem fact, not an estate manifest" ends the hand-typed-roots omission class with no index existing anywhere. `trigger-specification.md` also promotes the estate's discipline to a pattern: **Human-Gated Waits: Date the Chase** — the honest prose wait keeps its form and gains a dated partner, because an undated wait on a person is invisible for exactly as long as it lasts. The operator loop is now three commands: `estate-sync` → `triggers --estate` → `estate-check`. 10 self-tests (161 total); validate + coherence clean. Plan: `membrane-attention-cluster`.

## [3.22.0] - 2026-07-28

**The machine axis — sync before orienting.** The estate is now worked from more than one machine (local + cloud sessions, collaborators coming), which exposed a scope qualifier commit-is-real had always carried silently: the commit makes state real *on the machine that made it*; publication makes it real to the estate — and orientation reads the estate. Velocity, triggers, and verified-flip surfacing all read `git log`, so a session that orients without fetching reads a stale event stream with no way to know it. New **`mdllm estate-sync`** mechanises the fix as the fourth framework hard hook (`session-start:estate-sync`): walk the root + nested `domain(s)/*` repos, fetch, take fast-forwards silently (pure transport of state already committed elsewhere), and report everything else without resolving it — `DIVERGED (+a/+b)` is `divergence-is-an-unrouted-decision` operationalised (never auto-merge, never reset; a force-pushed remote surfaces the same way), `dirty` skips the pull, `offline`/`auth-failed` degrade to "orienting from last-fetched state" (bounded, `GIT_TERMINAL_PROMPT=0`, never a prompt, never a hang). The no-live-fetch doctrine is sharpened, not violated: a *required* network call at session start stays forbidden; a bounded degrading attempt is the hook's job. The push stays the human's deliberate act — but `estate-sync --status` (no network, cached refs) becomes the session-end **publication debt** report: `ahead +n (unpushed)` per repo, the state the estate cannot see, surfaced instead of remembered. Discovery is deliberately permitted here where `estate-check` refuses it — that guardrail protects relational information (a producer must never enumerate consumers); a walk for `.git` directories is repos-not-membranes and reveals nothing `ls` doesn't; batching-never-an-index still binds (stdout-only, ephemeral). After a sync that moves anything, the tool suggests the `estate-check` possibly owed — pulled source commits can flip a consumer's imports stale; the membrane check itself stays deliberate. Wired on all three surfaces: the Claude Code SessionStart adapter runs it ahead of the (still read-only) `session-start`, AGENTS.md carries the interpretation-floor block, and the generated domain session-start kernel gains step 0 so every domain inherits it through the refresh channel. First live run fast-forwarded two genuinely stale local domains (+2, +3 behind from cloud sessions) — the felt gap, caught on contact. `git.autopush` per-domain config deliberately deferred until a collaborator exists (deploy-when-felt). 8 self-tests (151 total); validate + coherence clean. Plan: `estate-git-sync`.

## [3.21.0] - 2026-07-28

**Domain-to-domain sync becomes floor-driven — both directions, through the face, never an index.** An estate audit of four sealed domains (brief at v3.19.0) found the cross-domain mechanism had outrun its paper, and the operator was feeling the result live: mirrors and sources drifting with no mechanical way to see it. The felt direction — *source behind mirror*, a consumer's copy edited while the pins still agree — is now detectable consumer-side: `imports-check` reads each import's content through the source's face alongside the manifest pin and reports **DIVERGED** (pin current, content differs: the loop was bypassed) beside the existing `stale`; new **`estate-check <roots...>`** batches that read over explicitly named consumer roots with a roll-up — ephemeral, grouped per-consumer, deliberately *batching, never an index*: a domain still cannot enumerate its consumers, and the membrane holds because the content poll crosses the same porch as content. Reporting is now coverage-honest: the summary counts stale/diverged/fresh/withdrawn separately from could-not-check and prints `COVERAGE: n/m` — the audit had found a domain with 26 unpinned imports reading `26 import(s); 0 stale.`, the count of comparisons never made rendered as all-clear. The trigger evaluator stops silently dropping free-text `time` conditions (8 of 28 audited triggers dropped without a word, one 10 days past its embedded date under "No trigger conditions currently true."): an embedded ISO date is evaluated, no date reports as not-mechanically-evaluable, `date` aliases `time`, and OVERDUE is no longer suppressed by a declared trigger — the more carefully authored thing got *less* warning. The paper catch-up: the reference triple + `exposed` graduate from the draft design doc into `thing.md` and `provenance.md` (new Cross-Domain Imports section — the fields were tool-read but spec-unwritten, so a domain author following the specs could not discover the floor's own contract); `change-reconciliation.md` declares its inbound edge (External Inflections, single-corpus scope stated rather than implied — the exact prose-dependency failure its own paired insight predicts, found inside the spec written to catch it); the operator-guide toolbox gains its four missing commands plus *Running More Than One Domain*; framework-map gains **View 4 — the estate seam**, the map's first two-domain view. Kernel regenerated (was stale at 3.17.5); examples walked (no-op absorb) and re-pinned. 8 self-tests (143 total); validate + coherence clean. Plan: `cross-domain-sync-catchup`.

## [3.20.1] - 2026-07-27

**Session-start surfaces a missing floor.** Git hooks live in `.git/hooks/`, which is never cloned — so a re-cloned domain silently loses its git-fs anchor and orients perfectly cleanly the next session, while the one command that would say so (`doctor`) requires already suspecting it. `session-start` now reports **Floor: NOT INSTALLED** when either hook is absent, and **Floor: STALE** when an installed body predates the current framework; quiet when healthy. Deliberately cheap — presence and body-freshness only, no `git hook run` (that stays doctor's deep probe) — because this runs on every session start. Found live: a domain with 104 commits of work had lost its pre-commit hook to a re-clone; its corpus validated 0/0 throughout because the harness PostToolUse adapter was still firing, which is the two-anchor design working as designed. 4 self-tests (135 total).

## [3.20.0] - 2026-07-27

**The disclosure boundary — the floor's first check that must never reach CI.** A repo declares, in a local gitignored `.boundary-terms` file, terms that must not cross into committed state — client names, personal names, internal identifiers; `mdllm boundary` blocks any commit whose staged additions, staged filenames, or commit message contains one, suggesting the approved substitute when the file names one (`term ==> replacement`). The invariant inverts the floor's usual hardening direction: the framework ships the capability, never the vocabulary — no terms, no hashed terms (short-string hashes are dictionary-recoverable), no counts in committed artifacts — so where no terms file exists (every fresh clone, all CI) the check no-ops silently, and a self-guard errors if the file is ever tracked. `install-hook` now writes a **commit-msg hook** alongside pre-commit — the commit message is a surface pre-commit structurally cannot see, and it is where honour-system disclosure failures actually live. `scaffold` births every domain with its own local terms file (per-repo boundaries) and registers the newborn's name in the framework root's file: private-by-default, publication an explicit operator decision. Passes the backlog's suppression-list gate because the local file is not an allow-list keeping a truth-check quiet — it is the check's entire subject, operator-owned; an omission fails open for that term only. 9 self-tests (131 total), synthetic vocabulary throughout. Plan: `boundary-disclosure-check`.

## [3.19.0] - 2026-07-26

**A domain declares which of its own statuses mean "settled" — the open-loop count stops overstating the work.** The gap: `TERMINAL_STATUSES` was a single hardcoded set (`completed`, `cancelled`, `resolved`, …) applied to every type in every domain, while `_schema.yaml` has always let a domain declare its own status vocabulary. The two never met. A domain whose lifecycle is mostly steady-state paid for it every session: signed controlled documents at `approved-current`, `record-pointer`s at `live`, draft-documents at `exported`, reviews at `actioned` — all finished or in force, all counted by `session-start` as "forward work still in flight". Measured on the three private domains the count read 11/28/60 against a true 5/8/12, overstating outstanding work by ~2.5x; the genuinely urgent items (an overdue risk-treatment review, a change request due in two days) sat inside that noise looking exactly like eighteen signed SOPs. **New optional per-type field:** `terminal_statuses`, alongside the existing `statuses`. A declaration *replaces* the universal set for that type rather than extending it (explicit beats implicit); values outside the type's own vocabulary are ignored and reported at Warning, as is any attempt to declare them on a framework-reserved type. **The tool now owns the reserved types' settled sets too** (`RESERVED_TERMINAL`) — a domain cannot redeclare `skill` or `conflict`, so it could never have fixed `stable`-means-done itself. Every status check that asks "is this still forward work?" — orientation, `triggers` (overdue scan, `subtasks_complete`), `cascade` (unblock candidates, prerequisite roll-up, parent rollup) — routes through one `is_terminal(schema, meta)`, so a domain declares its lifecycle once and all three agree. **Deliberately NOT rewired:** the insight-orphan check's liveness test, which asks a different question — "settled" and "dead" are not the same, and an insight linked from a signed SOP or a standing oversight view has not fallen out of session memory (the first cut of this change fired on five healthy insights the moment a domain opted in; the universal set is correct there and the reasoning is pinned in a comment). Fully backwards compatible: a type that declares nothing behaves exactly as before, so no existing domain changes behaviour until it opts in. 122 floor self-tests (+7); validate + coherence clean across all corpora.

---

## [3.18.0] - 2026-07-16

**The verified flip becomes an auditable event — quarantine flip discipline in the floor (review 7's #1 under-engineered finding, closed before QMS ratification).** The gap: `verified: true` — the stated no-shadow-AI control — was frontmatter any agent could write, in the same commit as the content it supposedly gated. The floor cannot verify *truth* (whether the human review was real; judgement never wears mechanical clothing), so it now verifies *procedure*, keyed to git: **born-verified** (most recent flip commit == creation commit ⇒ no review window existed; also fired pre-commit for working-tree things not yet in HEAD) and **unattributed flip** (`verified: true` without `verified_by` naming the human — ALCOA attributable, deliberately forgeable: a false attribution is a falsifiable record, categorically better than an anonymous bit). Warning by default; `options: {quarantine: strict}` in `_schema.yaml` raises both to Error so the hook blocks — regulated domains opt in, casual domains never meet the ceremony. Third leg: `session-start` surfaces every flip since the last session-end commit, so no flip is silent. Historical findings heal (re-quarantine, re-flip attributably — the newest flip then postdates creation). **The check's first firing was its own builder:** the framework's one cross-domain import (`divergence-is-an-unrouted-decision`, the MCP road test) was born verified at `aae0712` with no verifier named — re-quarantined and re-verified attributably in this release, its reference triple pinned (clearing the standing imports-check INCOMPLETE). `verified_by` + the source triple join CORE_FIELDS (both tool-read). Kernel regenerated (thing.md quarantine block now carries the operative flip rule at Tier 0). 115 floor self-tests (+10); validate + coherence clean across all corpora.

---

## [3.17.5] - 2026-07-15

**The tool sheds its single-file exemption — `mdllm.py` split into the `tools/markdownllm/` package behind an unchanged entry shim (review 7's over-engineering finding, done inside the pre-ratification window before QMS-AUTO-001 fixes the shape in place).** Behaviour-preserving by construction: the 105-test floor suite ran green *unmodified* throughout (the shim re-exports every pinned symbol), a 47-capture golden run of all read-only subcommands + argparse help surfaces diffed empty after every move, and the public contract — `python tools/mdllm.py <cmd>`, cited by every domain AGENTS.md and installed pre-commit hook — never moved. Twenty moves, cut by reason to change: `model` (imports nothing) at the centre, one module per command, `repo.py` for the shared repo-state readers (git sha, sentinel, TIERS), `cli.py` as pure argparse wiring; dependency rule held (`cmd_*` never imported laterally, library functions may be — doctor stays the sanctioned aggregator). Largest module is now validation.py at 446 lines, down from one 3,444-line file. Run under code-architect's `refactoring-process` (its first end-to-end run — the process graduates draft→evolving on it): one route-1 regression caught by 38 red tests and restored; one route-2 revision recorded (coherence warnings naming TIERS' old home). Three `Path(__file__)` traps (framework-map count check, hook body, scaffold root) pinned via `CLI_REGISTRY_FILE`/`MDLLM_ENTRY`. Zero-install, stdlib-only, and the hook path survive untouched; examples re-pinned (nil domain-facing delta — the refresh for domains is a no-op absorb). 105 floor self-tests; validate + coherence clean across all corpora.

---

## [3.17.4] - 2026-07-03

**The reviews-5+6 mechanical remediation — twelve verified findings fixed, each with a floor-shaped regression test where one qualifies.** Tool: the generated session-start block no longer names the phantom `mdllm orient` (parser construction extracted to `build_cli()` so generated prose is tested against the live registry — a *second* artifact, breaking the same-builder blindness that hid the bug exactly as `a-same-builder-check-is-blind-to-a-self-contradictory-builder` predicted); MCP egress now strips `informed_by` + `parties` (the strip list had been built from the road test's symptom, not the every-relational-field rule); `triggers` reports `type: relationship` — and any unrecognised type — as not-mechanically-evaluable instead of silence; the `stale` trigger keys on git history with mtime as fallback (mtime is clone-local noise); and the TIERS↔catalog coherence check gained its mirror direction, which fired exactly once — `thing-lifecycle.md`, now deliberately outside the loading map until the draft is reconciled with the live tool. Prose: kernel/tier token figures deleted from prose per the third-strike razor (`repeated-drift-promotes-a-fact-into-the-floor`; a prose-figure checker would need a suppression list, so the WORKLOG precedent applies — delete the duplicates, don't police them; `mdllm tokens` measures, CHANGELOG 3.2.0 keeps the dated history, README keeps the one narrative figure); one birth path (Getting Started Step 1 and CONTRIBUTING both route through `scaffold`; CONTRIBUTING's months-stale hand-copied spec inventory became pointers to the canonical sources); plus the Two-Layers heading fix, the live-voice continuity-brief residue, and the pre-v3.10 `instance-of` teaching in the workflow-definition template and home-renovation example. Examples walked to v3.17 shape (the orient step was the substantive delta) and re-pinned, guarded by a new example-staleness coherence Warning comparing every `examples/*/AGENTS.md` pin against the sentinel — same-builder, no suppression list, only the walk quiets it. The evidence backlog is reframed as **operator-gated sessions** (`evidence-and-eval-backlog` v2.0) per review 6's diagnosis: the loop can only produce artifacts the agent can produce; the missing evidence needs the operator's calendar, not another backlog row. 102 floor self-tests; validate + coherence clean across all corpora.

---

## [3.17.3] - 2026-06-28

**The v3.17.2 retired-vocabulary register is reverted — a check that needs a hand-maintained suppression list isn't floor-shaped.** Building it surfaced the flaw: "the retired `continuity.md`" (correct) and "lives in `continuity.md`" (drift) are the same characters, so the check could only reach a clean baseline through an `allow` list of ~15 ids/paths — several broad enough to *silently* suppress future drift in whole specs, the exact silent-failure mode `existence-is-not-currency` warns of. That is judgement in mechanical clothing; the floor is for checks keyed to a same-builder source that cannot disagree with truth. Removed by the same principle that retired WORKLOG — **delete the thing that needs policing, don't police it** — and replaced by what holds more weight with no surface to rot: an explicit pointer in `change-reconciliation.md` that an inflection walks the **whole corpus, the insight corpus included** (the tier the v3.17.0 sweep actually skipped). The subcommand-count check (v3.17.1) stays — it is keyed to the live CLI surface, has no suppression list, and is genuinely floor-shaped. Three insights capture the lessons: `judgement-checks-need-a-suppression-list-which-is-itself-drift` (the design razor — same-builder-checkable belongs in the floor, suppression-list-dependent belongs to the human Walk); `the-rough-true-account-is-generative-infrastructure` (the consequential value-principle — a true record of dead ends, reversals, and overreaches is what the next builder stands on; transparency is forward infrastructure, not backward confession); and `premature-publish-manufactures-discipline-eroding-urgency` (its in-session instance, framed symmetrically: v3.17.0 was published before reconciliation finished and the agent then pushed past its boundary twice under the manufactured urgency — the same haste on each side of the loop, recorded plainly rather than smoothed over). validate + coherence clean across all corpora; 97 floor self-tests (the 4 retired-vocab tests removed with the feature).

---

## [3.17.2] - 2026-06-28

**A retired-vocabulary registry — the textual-trace step of the dark-region Walk, made standing for the *retire* case.** The v3.17.1 reconciliation exposed the systemic gap: when a change retires a named artefact, the dead name can linger live in prose anywhere in the corpus, and nothing mechanical watches for it. New `retired_terms` in `_schema.yaml` (corpus-general, opt-in by data) plus a `coherence` check (Warning, non-blocking) flag a live literal occurrence of a retired name — mechanising the grep, not the judgement: the check cannot tell *"X is retired"* (correct) from *"lives in X"* (drift), so disposition stays the agent's, and each entry carries an `allow` list of id/path substrings where the term legitimately survives (history, the thing that retired it, specs announcing the retirement). **Tuned to a clean baseline, it becomes a forward regression guard** — the next *unacknowledged* mention is the drift. Two precision lessons are baked in: matching is **case-sensitive** (the dead `WORKLOG.md` file vs the live `worklog` subcommand) and uses a **hyphen-aware boundary** (the retired `continuity.md` must not match inside the live `session-end-continuity.md`). The framework dogfoods it, registering `WORKLOG.md` + `continuity.md` against a clean baseline. From a domain's view this is near-zero friction: invisible unless the domain declares its own retired terms (e.g. a renamed concept), never blocks a commit, and adds no new command — a key in a file it already maintains. Also marks the framework-map count check (v3.17.1) resolved in the coherence backlog. 4 floor self-tests added (101 total); validate + coherence clean across all corpora.

---

## [3.17.1] - 2026-06-28

**Post-v3.17 drift reconciliation over the insight corpus, plus a mechanical guard against the recurring count-drift.** The v3.17.0 sweep reconciled the live spec surface but did not walk `things/insights/` — the dark-region walk an inflection demands (`change-reconciliation`) skipped the corpus's own memory. Four active insights still named the now-retired continuity brief / WORKLOG as *live*: `existence-is-not-currency` counted WORKLOG as a fifth generated-artifact instance (corrected to four; the deletion is itself a turn of the principle), `modeling-cognition…` named the continuity brief as the loop's retrieve step (re-keyed to graph-liveness + session-start orientation), `mechanism-pairs…` held continuity↔WORKLOG up as a live example pair (annotated as retired — the symmetry survived its instances), and `long-running-tasks…` still pointed its checkpoint at the deleted `continuity.md` (its frontmatter already knew better). Separately, `framework-map.md` had drifted to "18 mechanical subcommands" against an actual 20 (`mcp-serve`, `imports-check` missing from the count and View 3) — the exact repeat-offender the 06d retrospective flagged. Fixed, and pinned: a new **`coherence` check compares the map's stated subcommand count against the live CLI surface**, so this class can no longer drift silently. validate + coherence clean across all corpora; 97 floor self-tests pass.

---

## [3.17.0] - 2026-06-27

**Continuity dissolved into orientation — the hand-maintained session brief is retired.** `continuity.md` — a per-domain mutable singleton that had grown to 733 lines — conflated the corpus's two sides in one file, and both halves had better homes. Backward content (what was done) was always the commit stream's; forward content (what's still live) is now the **thing graph**, surfaced by a generated **orient** view: `mdllm session-start` emits the open loops (non-terminal work things + open conflicts), the session-memory counterpart to change-reconciliation's work-content state (`orient-and-reconciliation-are-the-corpus-two-sides`). Insight **liveness is re-keyed off file-presence onto the graph** — an `active` insight is live iff a non-terminal thing has an inbound edge to it; an insight with only outbound edges has discharged itself (a promotion signal). A new **`disposition: keep-active`** marker keeps standing-razor / parked insights live without a prose crutch, and **end-session gains a mandatory insight-disposition pass** (the brake, paired with capture, so the insight population can't grow faster than it's reckoned with). The orphan backlog the re-key surfaced was worked to zero (3 promoted, 1 dismissed, 1 linked, 5 kept-active). The `continuity-brief` type is marked retired/deprecated; its floor teardown is a tracked follow-on. The **committed `WORKLOG.md` is retired** by the same principle — it was generated *from* git and committed *back into* it (circular duplication); `mdllm worklog` now prints an **on-demand, uncommitted** session view of the commit stream, and the backward record is git alone. Also: the **MCP Phase 3 `run_domain_task` live-agent surface was reverted in full** — a live-agent invocation is a different risk class than the read face, and dormant execution code behind an opt-in flag is the honour-system control the floor exists to replace.

---

## [3.16.0] - 2026-06-24

**`mdllm cascade` — the outbound completion read, mirror of `touchpoints`.** The post-completion cascade (`write.thing.md`: *after every change, cascade*) becomes a floor affordance instead of a hand-walked prompt. `mdllm cascade <id>` gathers the downstream set a thing's completion unblocks — *"what did I just unblock?"* — the exact mirror of `touchpoints`' inbound *"what did I just put at risk?"*: two directions of one index-walk-as-attention-cache pattern, so the agent reads a precomputed chain instead of re-deriving it by reasoning (the kernel rule). It walks dependency edges in **both** directions (`dependencies` and the reverse `blocks`, so it is blind to neither) and reports **unblock candidates** (every prerequisite now terminal, priority-flagged), **partial-progress** candidates, the **parent-completion** candidate, and **trigger watchers** — and it **reports only, never applies**: detection is mechanical, disposition stays the agent's (the narrative may hold a soft blocker no edge declares). Trigger *evaluation* is left to `mdllm triggers` (gather, don't reimplement). The `cascade-completion` prompt is slimmed to its semantic residue — run the tool, then dispose — shedding the mechanical 3-step walk it used to carry. The design rule is pinned as the insight `directional-graph-reads-come-in-inbound-outbound-pairs` (a one-direction floor read implies its opposite; the mirror is the same walk flipped, not a second feature). `framework-map` View 3 + subcommand count updated (17 → 18); 8 floor self-tests added (85 total); validate + coherence clean across all corpora.

---

## [3.15.0] - 2026-06-24

**Domain kernel + session-start hardening — the entry surface becomes generated, and the taxonomy stops conflating config with enforcement.** Root cause addressed: domain agents skipped the session-start ritual (load kernel, version-check, velocity) *even on Opus in Claude Code* — structural, because session-start fires with the user's first message and the live request wins, while the imperative sat buried in a long, reference-heavy `AGENTS.md`. **Taxonomy (additive):** `orchestration.md` reframed so **anchor** (`interpretation` | `git-fs` | `harness-session`) is the primary axis that decides enforcement, and **hard/soft is config only** — a `hard` hook anchored to `interpretation` is exactly as skippable as a soft one (the old "hard = never skippable" cell was the lie). The three framework hard hooks and the Hook Points table are now anchor-annotated; bindings/`hard_hooks` gain an optional `anchor`. **Domain kernel:** new `mdllm domain-kernel` makes `AGENTS.md` a slim, *generated* entry — operative sections live in managed `<!-- generated:NAME -->` blocks (standing-truth, session-start-first, tier-routing from `TIERS`, anchor-annotated hooks, floor), regenerated from frontmatter + skills while authored identity outside the blocks is preserved verbatim. Residue-free by construction, like derived indexes; `coherence` gains a corpus-general domain-kernel **drift check** inherited via the pre-commit hook. **Session-start hardening:** new `mdllm session-start` emits the ritual (downward version-check + git velocity + drift advisory) to stdout for a harness `SessionStart` hook to inject at t=0; `adapters/claude-code.settings.example.json` gains a `SessionStart` hook — one Claude-format file covers Claude Code **and** Copilot in VS Code (agent mode), which reads `.claude/settings.json` directly. **Deliberate rituals:** `templates/commands/` (Claude) + `templates/copilot-prompts/` (Copilot) ship `end-session` and `retrospective` slash commands — human-invoked by design; session-end harvesting happens only when the operator judges the session worth it, never automatically. **Rollout rides existing rails:** `scaffold` fills the kernel + deploys slash commands at birth; `refresh` regenerates the kernel when absorbing a version bump; `doctor` reports kernel staleness + adapter presence. Everything opt-in/additive — a domain with no kernel/adapter still boots by interpretation; Copilot cloud/CLI covered by that floor. PreToolUse security/risk hooks deliberately left for later. **Self-hosted and deployed:** the framework now runs its own `SessionStart` + `PostToolUse` hooks, and `scaffold` writes `.claude/settings.json` so new domains are **born hardened** — but an agent cannot self-install that block (it carries permission rules, so writing it is a self-modification the agent is barred from), making adapter install a one-time operator paste, captured as the insight `agents-cannot-self-install-permission-bearing-hooks`; `domain-refresh.md` gains the matching operator paste-step for existing domains, and a framework root is no longer mistaken for a stale downstream domain at session start. **Floor gate added:** `validate` now blocks a terminal-status thing that depends on unfinished work — `detect-conflicts` rule #1 mechanised as a state invariant (terminal dependencies count as resolved) — with the `dependencies` = hard-prerequisite semantics clarified at the field in `thing.md` and the design principle captured as the insight `hard-invariants-encode-a-semantic-assumption` (a hard invariant freezes one reading of an ambiguous field; false-positives are a modeling signal toward `linked_things`, not a reason for a config escape). Also `prose-references-are-mechanically-checkable` from the deployment harvest. validate + coherence clean across all corpora; 77 floor self-tests.

---

## [3.14.0] - 2026-06-19

**Orchestration surface reduced, enforcement reframed as three anchors, bundled with the day's human-onboarding pass.** The session that asked "is this framework just a harness?" answered it in the spec: a harness is a runtime that owns no durable state; MarkdownLLM is durable state + rules any runtime operates over; the only part that *feels* harness-like is orchestration. `orchestration.md` gains an **"Enforcement: Three Anchors, Not Two"** section with a full hook/prompt distribution table — every hook fires by **agent interpretation** (portable across every harness and sufficient for correctness; the default, proven by the framework's Copilot-then-Claude-Code build history), **git/filesystem** (mechanical and universal — the one pre-commit hook that never needs a vendor adapter), or **harness session lifecycle** (enforced only by an optional `adapters/` entry). Adapters are optional hardening for the lowest-consequence hooks, never required: the moment one became required, the framework would stop being a harness-agnostic substrate. That frame drove a **reduction** — two prompts deleted: `validate-before-commit` (its mechanical half is the git hook's job, its semantic half is standing prose in `validate.thing.md`; re-performing it violated the kernel rule "never re-perform mechanical checks by reasoning") and `worklog-update` (a single mechanical command, folded into `session-end-continuity`'s commit step, dropping session-end from two bound prompts to one) — closing an action the 2026-06-16 mechanical-census review had flagged, and captured as the insight `hook-enforcement-has-three-anchors`. Bundled with the preceding **onboarding/tooling pass** (no spec-contract change): a one-command cross-platform installer (`install.sh` / `install.ps1`) that checks prerequisites, installs the floor hook, writes a Claude Code `CLAUDE.md` wrapper, and verifies with `mdllm doctor` — missing git/Python offered via the OS package manager with consent, never force-installed; the README halved into a landing page + repo map; the manifesto's *Paradigm Shift* reframed on the reasoning engine; and human guides moved to `docs/` while the ~25 foundational specs stay flat at root as a published, hardcoded resolution contract. validate + coherence clean across all corpora.

---

## [3.13.0] - 2026-06-18

**The vocabulary trilogy completed, a spec↔floor drift closed, and the Assimilate beat made a tool.** Four bundled changes from a session that reviewed the mechanical/semantic line end-to-end and judged it sound. **Field registration (`known_fields`)** joins `types` and `relations` as the third opt-in, domain-owned `_schema.yaml` vocabulary, with a tool-owned `CORE_FIELDS` universal set; a top-level frontmatter key in neither set is flagged (Warning), closing the silent-loss hole where a mis-keyed field (e.g. `relations:` typed where `linked_things:` was meant) passed clean because only field *values* were ever checked, never the *set of keys*. Opt-in by design — a domain sees nothing until it declares the list (bootstrap with `mdllm index --signal schema`). **A real spec↔floor drift, closed at the floor:** `session-memory.md` (a stable spec) promised a `validate` check — "active insight not in continuity brief," plus its open-conflict twin — that did not exist in the tool and disagreed with `validate.thing.md`, which had assigned the same work to the agent. The checks are now built (Info, corpus-general) and `validate.thing.md` reconciled to the floor; detection is mechanical, disposition stays the agent's at retrospective cadence. **`mdllm touchpoints <id>`** makes the change-reconciliation Assimilate beat a floor affordance: one read returns a thing's complete declared inbound set (every `linked_things` edge, the structural `parent`/`definition` pointers, `informed_by` pins) plus literal textual references — "what did I just put at risk?". Deliberately invoked-never-hooked (the human cue stays sovereign per *The Driver Names The Inflection*) and computed fresh from the live corpus, not cached indexes (assimilation must be complete *and* current). **`workflow-state` promoted draft → evolving** — exercised on a live domain; the reserved types are unchanged, the spec's maturity advanced. Floor gains 8 self-tests (58 total); validate + coherence clean across all corpora.

---

## [3.12.0] - 2026-06-16

**The enforcement gap the mechanical census named — closed at the boundary.** A targeted review confirmed the mechanical/semantic line is drawn correctly but found the floor's reach stopped short of its own commit gate: `validate` ran in the pre-commit hook, while `kernel --check`, `index check`, and the catalog↔filesystem invariants of the dark-region walk were fully mechanical yet only ran when an agent remembered to invoke them. A stale generated artifact is a pure mechanical fact, like a failed build, and the git history proved it leaks exactly there (the past "framework-map spec count 23→25" drift). New `mdllm coherence` subcommand mechanises that slice, and is **corpus-general by design** so domains inherit the guard rather than the framework keeping a privilege its domains can't have: the general checks — stable-staleness (Info, a truthfulness *proxy*; the judgment stays the agent's), dead declared vocabulary (Info), and derived-index drift (Error) — run on any corpus, so a domain's skills, `_schema.yaml`, and deployed indexes are checked the same way; the framework-only checks — `foundational_specs` ↔ files on disk (Error; `kernel` previously skipped a missing spec silently), `TIERS` ↔ catalog (Warning), and kernel drift (Error) — switch on only at a `.markdownllm` root. It is wired into `HOOK_BODY` as a single self-scoping line (no `.markdownllm` → only the general checks run), so the same hook is correct in the framework and in every domain repo, and into CI. `kernel` and `index` were refactored to share one body-builder with `coherence`, so the drift check cannot disagree with what the generators produce — a single source for the very fact it guards. Existing domains pick up the new hook through the `mdllm refresh` + `install-hook` channel already built for framework evolution — and because `refresh --seal` bumps the version sentinel without reinstalling the hook, `mdllm doctor` now also checks **hook-body freshness** (the installed pre-commit copy vs the current `HOOK_BODY`), so a domain that sealed to a newer framework but kept an older hook is flagged (advisory — the hook still runs `validate`, so the floor is active, just not current) instead of the sentinel silently claiming enforcement the hook does not run. The deliberately-left residue is the prose-only dark region a tool cannot read (framework-map prose counts, routing-table semantics) — kept human per `change-reconciliation.md` → Walking the Dark Region. Floor gains seven self-tests (50 total). Separately retires two live contradictions the reviews flagged: the `worklog-update` prompt now regenerates `WORKLOG.md` via `mdllm worklog --write` (it has been generated since 3.9.0; the hand-append instruction was the stale mechanism), and the README no longer claims "no installation" — the floor's prerequisites (git, Python 3.10+, PyYAML, the hook) are stated and routed to `first-hour.md`. validate + coherence clean across all corpora.

---

## [3.11.0] - 2026-06-16

**The reverse-edge gap the workflow primitive exposed — closed in the floor.** Giving `workflow-run` a singular `definition:` field (v3.10.0, #1) made a latent blindness bite: the `relationships` index was built solely from `linked_things`, so it walked neither `definition` nor the older `parent` pointer. A change to a `workflow-definition` therefore could not *mechanically* surface its runs — the change-reconciliation Assimilate beat promised "total recall over what is declared, like a compiler listing every call site," but for structural pointers that recall silently degraded to whatever the textual-trace grep happened to catch. This is a blindness in the **lit** region (a declared, machine-readable edge the index wasn't taught to walk), distinct from and sharper than the prose dark-region of `mechanical-assimilation-is-blind-to-prose-dependencies`. The fix: `build_index_body`'s `relationships` signal now emits the singular structural pointers (`parent`, `definition`) as edges alongside `linked_things`, so a reverse read recalls a definition's runs and a parent's children. Forward referential checks (does `definition` resolve? is `current_stage` a member?) already existed; this adds the reverse direction — the same forward-resolver-plus-reverse-index shape as the bidirectional version-check. Both the forward and retrospective reconciliation modes inherit the recall for free because both read the one index. The trigger stays human: only the mechanical Assimilate recall widened, not the cue (`change-reconciliation.md` → The Driver Names The Inflection is untouched). Made operative in `change-reconciliation.md` (Assimilate beat, Dark Region tiers, Enforcement table) and `derived-index.md` (the `relationships` index aggregates every declared edge wherever it lives), with the durable rule captured as insight `structural-pointers-need-reverse-edge-indexing`: *any future singular load-bearing pointer must also be emitted into the index, or it becomes an unwalked declared edge.* Floor gains one self-test (44 total). Separately, a **`mdllm worklog` bug fix**: the generator hard-coded `framework-worklog` as id and "Framework Work Log" as title, which would dangle (and fail validation as an unknown reference) in a domain repo; it now derives both from the local `AGENTS.md` `name` field — falling back to the folder name — and auto-links to a local `manifesto` thing only if one exists, so the command is portable across the framework and domain corpora alike. validate clean across all three corpora.

---

## [3.10.0] - 2026-06-16

**The workflow primitive, hardened against an independent second read.** A parallel review of the v3.8.0 workflow work (two agents converging on the same design was itself the signal it was load-bearing) surfaced five sharp critiques; four are actioned here, one held with reasons. **Definition pointer is now structural (#1):** a `workflow-run` names its definition with a singular `definition:` field modelled on `parent`, not an `instance-of` relation — the floor resolves exactly one definition deterministically, and the decomposition framing still justifies the *separation*. **The membership check is enforced now, not deferred (#5):** `mdllm validate` errors on a missing/unresolved `definition`, a `definition` that isn't a `workflow-definition`, or a `current_stage` the definition doesn't declare — this is referential integrity (the floor's core job), distinct from transition *legality* (which stays the agent's Layer-2 judgment); a typo'd cursor no longer validates clean. **Status vocab fixed (#4):** `complete → completed` so terminal detection (now including `abandoned`) actually fires; `blocked` is deliberately omitted — a run is a cursor and is `active` even while its underlying work is stuck, so blockage is read from the work things, not the cursor (the kitchen example corrected to match). **`to: []` defined as terminal by fiat (#3):** no ambiguous "edges unwritten" third state. **The coordination claim is decomposed out (#2):** new micro-spec `coordination-claim.md` owns the general advisory `held_by` + optional `held_until` lease convention (read-and-respected, not a lock; deploy-when-felt) — it changes for its own reasons, so it does not belong inside `workflow-state.md` or `thing.md`; `workflow-run` and `continuity.md` are consumers, and the spec records working-tree contention as the adjacent unspecified concern (the live `index.lock` collision during this very review being exhibit A). Floor gains a `definition` referential field, the workflow-run cursor check, and two self-tests (42 total); `workflow-state.md` → v0.3. validate clean across all three corpora.

---

## [3.9.0] - 2026-06-15

**Harvesting from where the framework is already proven — the review's back half, actioned.** Six follow-on decisions from the 2026-06-15 independent review land together. **Tracking surfaces (#5):** the WORKLOG was the last hand-maintained surface and the largest file in the repo (~115KB of prose the framework's own generate-or-validate-or-delete principle condemned); new `mdllm worklog` generates it from the commit stream (sessions split on `session-end:` commits, detail left to `git log`), cutting it to ~21KB with zero hand-maintenance — CHANGELOG stays the external per-version record, WORKLOG becomes the internal per-session one, both now generated. **Domain refresh (#7):** new `mdllm refresh <domain>` mechanises the floor half of domain-refresh.md — reports the version delta and the CHANGELOG entries a domain has not yet absorbed, and with `--seal` bumps `framework_version_seen` after the agent does the semantic adoption; it never rewrites domain skills (that stays the agent's job). **Honesty (#8):** the model-tier claim is demoted from spine assertion to explicit hypothesis in the manifesto and AGENTS principle 9 — utility is well-evidenced by real adoption; the *smaller-model-beats-larger* claim rests on one saturated eval and stays untested until a discriminating fixture exists. The two claims are now kept distinct. **Cross-domain (#6):** the manifesto's unspecified "domains reference each other" promise is retracted and reframed as a deliberate, verified import (`origin: external` quarantine), with the full design captured as draft insight `cross-domain-handoff-is-verified-external-input` — the workflow-run hand-off is its first concrete consumer. **Concurrency (#3):** the advisory `held_by` claim shipped with `workflow-run` in 3.8.0 is generalised in prose — `held_by` + an optional `held_until` lease, ready to adopt for `continuity.md` and other singletons when felt (reserved, not yet deployed). **Meta-risk (#4):** new `evidence/` directory with a README and a shape-only validation-record template — the container for bringing the framework's external proof (independent adoption, a downstream MVP) into the artifact; the shape-only record is buildable now, the narrative case study waits on an explicit disclosure decision. Floor gains four self-tests (`_version_lt`, `_changelog_versions_since`, reserved workflow types); validate clean across all three corpora. **Status truthfulness (#5b):** the three specs that took genuine *structural* changes this cycle — `thing.md` (gained two reserved types), `orchestration.md` (gained the upstream version-check leg), `domain-refresh.md` (gained the upstream-propagation section) — are relabelled `stable → evolving` per the framework's own "stable = unlikely to change structurally" definition; the rest of the core, which saw only incidental cross-reference edits, keeps its label.

---

## [3.8.0] - 2026-06-15

**Workflow run-state becomes a primitive, and version-drift becomes bidirectional.** The third independent review moved one gap from theoretical to felt: the framework modelled knowledge state richly but had no first-class representation of a *workflow run* — the state of a multi-stage, multi-session process instance as it advances. New draft spec `workflow-state.md` adds it as the decomposition principle applied to *processes*: two framework-reserved types, `workflow-definition` (stages expressed as data, with allowed transitions — a graph with cycles, not a linear sequence) and `workflow-run` (one live instance: a `current_stage` cursor, an advisory `held_by` coordination claim, and a resume narrative in the body). The primitive is deliberately narrow — almost everything is inherited (`instance-of` is the definition pointer, decisions pin via provenance, the commit log *is* the `stage_history`); only the cursor, the claim, and the per-instance resume point are new. Division of labour follows the floor/agent split: the floor checks `current_stage ∈ definition.stages` (reserve-but-draft — that membership check lands *when felt*), the agent judges whether a transition was legal given the loops. Run-state decomposition also dissolves most of the concurrency problem — different instances are different files, which git merges freely. Ships with two `templates/` skeletons and a filled instance exercised on the life-manager example (`home-renovation-process` + `run-kitchen-renovation`); paired insight `workflow-run-is-the-decomposition-principle-applied-to-processes`. Separately, the `session-start:version-check` hard hook gains an **upward leg**: alongside the existing downward check (is this domain behind its local framework?), it now surfaces whether the *local framework copy itself* is behind its *published source* — advisory, cached (reads git's already-fetched remote-tracking copy via `git show`, no live network call), and non-blocking. `mdllm doctor` reports both legs; `domain-refresh.md` documents the upward leg as the softest of the version checks (it coordinates humans, it does not protect integrity).

---

## [3.7.0] - 2026-06-13

**Consistency becomes a change-management discipline, not a sweep.** A new extension spec, `change-reconciliation.md`, names how a domain stays internally consistent across change. A fresh thing on a clean slate carries no contradiction risk, so risk enters only at *change* to something the domain already reasons from — and is contained at that moment, not hunted for later by a periodic sweep. The driver, not the agent, declares an inflection; once declared, a scale-free four-beat pass runs: **cue** (human), **assimilate** (mechanical, two passes — the `relationships` and reverse-`provenance` indexes surface the declared affected set, then a corpus grep lights the prose references they miss), **walk** (the agent's semantic `validate.thing.md` layer, one question per touch point: does this still hold?), **seal** (revisions and a `belief-revision` supersede mark ride the same commit). The mechanical layer's job is not to judge risk but to make the agent unable to *not see* the shape a change disturbs; the judgement stays with the expert. No new infrastructure — the pass runs on the indexes already built. Paired insight: `consistency-is-maintained-at-change-not-by-sweeping`. Ships `status: draft`, Tier 2 (on-demand, ~1.7k tokens — no session-start cost). This release was itself sealed by running the pass on its own addition — which immediately exposed a *dark-region* touch point the indexes cannot walk (the `AGENTS.md` Tier 2 routing table that decides whether a domain agent loads the spec), caught by the operator and fixed. That lesson is now captured three ways: an operative rule (`change-reconciliation.md` → Walking the Dark Region), a spec-change checklist item in `AGENTS.md`, and the insight `mechanical-assimilation-is-blind-to-prose-dependencies`. The spec also gains a **Retrospective Reconciliation** mode (freeze a baseline, reconstruct the delta from git, full-corpus walk) for realigning a domain that was twisted before the pass existed, and the session's change-safety model is captured as `change-safety-is-defense-in-depth`. A full coherence sweep closed the session: floor + indexes + kernel + 37 tests clean, with one pre-existing `framework-map.md` spec-count drift (23→25) caught by the new textual trace and fixed. Finally, `retrospective.md` (v1.2) is wired to invoke change-reconciliation's retrospective mode as a fourth reflexive scan — so running a retrospective now *initiates* a full-corpus reconciliation rather than only reflecting on the period, with a reciprocal declared edge so the link is operational, not prose-only.

---

## [3.6.0] - 2026-06-12

**Birth becomes deterministic, and the floor learns to check itself into new environments.** The cold-start scaffold rehearsal ran the same day its lesson was mechanised: pre-tool trials scored 10/11 twice with *different* mechanical misses (96 turns, zero commits; clean commits, no isolation), and the first trial against the scaffold-aware guide scored 11/11 at a fraction of the cost (`evals/README.md`, insight `agents-drop-mechanical-birth-steps-not-semantic-ones`). Three new subcommands: `scaffold` (the `pre-domain-scaffold:isolate` hard hook as code — instantiated templates, nested repo, outer `.gitignore` isolation committed first, hook, first commit; exit 1 on any partial birth), `doctor` (floor prerequisites probed by *execution*, not resolution — hook actually runs, framework-version drift reported, degraded mode named), and eval-harness hardening (scaffold-style assertions, per-fixture report grouping, agent output persisted per trial, evidence mirrored to committed `evals/results/`, fixture versions templated from the sentinel). Building `scaffold` caught `_schema.yaml.template` shipping as unparseable YAML; an unparseable schema is now a validation Error, not a crash. eco-essentials completed the first real five-version domain refresh (2.8 → 3.5.0): floor adopted, AGENTS v2.0 kernel-tiered, 12 things clean. A second independent review landed same-day; its findings 1–5 (environment-dependent self-tests that had CI red, phantom version reference, gitignored evidence) are fixed in this release — spec prose no longer names framework versions.

---

## [3.5.0] - 2026-06-12

**The periphery comes under the floor.** The review's verdict — diligence still substituted for construction at the edges newcomers touch first — actioned on three fronts. Examples are no longer exempt: `mdllm validate` discovers `examples/*` as sub-corpora in the same run (so the pre-commit hook covers them), both examples declare `_schema.yaml`, and life-manager goes from zero things to an interlinked demonstration dataset — a project with subtasks, a goal fed by a recurring habit, live triggers (one deliberately overdue so `mdllm triggers` always has a find), and a decision record with commit-pinned inputs verified by `mdllm provenance`; example skills and AGENTS files rescoped to the v3 division of labour, pre-v3 residue (phantom statuses, an invented `schema_version` field, dependency-things) replaced. The relation vocabulary is pruned 35 → 13: inverse pairs collapsed to their forward direction (`supersedes`/`superseded-by` kept — the validator checks that backlink), near-synonyms merged, all 45 affected link entries migrated and prompt templates aligned. And the on-ramp exists: `first-hour.md` walks a newcomer's first sixty minutes; the README gains a For Humans section. Groundwork for the cold-start scaffold eval, which is next.

---

## [3.4.0] - 2026-06-11

**The floor verifies itself.** A comprehensive review found the gaps concentrated where the framework trusted itself without verification — all closed this release. The version sentinel (`.markdownllm`) had silently stayed at 3.0 since v3.1, disarming domain refresh; it is re-synced and `mdllm validate` now enforces sentinel / AGENTS.md / CHANGELOG agreement as an Error, so the pre-commit hook blocks any future drift. The tool itself gains a 30-test pytest suite (run first in CI), `mdllm kernel --check` gates kernel drift, and `provenance` joins the default `index check` signals. Eval Stage 2 hardened ahead of the 2×2 experiment: the bare condition no longer sees the framework checkout, timeouts record as failed trials, numeric-string field values coerce before failing, and `eval --report` aggregates runs into the per-cell table (fairness caveat documented). Domain scaffolding catches up to v3: guide v2.7 adds the deterministic-floor section and `templates/_schema.yaml.template` ships.

---

## [3.3.0] - 2026-06-11

**Eval Stage 2 — the model experiment is runnable.** `mdllm eval --run` seeds an isolated git workspace from a fixture's `seed/`, invokes a fresh headless agent (`claude -p`, json output → score/cost/time/turns per trial), and asserts the result. `--bare` strips AGENTS.md/skills/schema for the no-framework condition; `--trials N` for repeats. First fixture: `evals/vat-quarter-basic.yaml` — a synthetic VAT quarter with known-correct figures and a blocked-entertainment-VAT discriminator. The 2×2 structure-beats-scale protocol (haiku/opus × framework/bare) is documented in `evals/README.md`. Verified: negative test, dry-run seeding both conditions; live agent path untested pending `claude` CLI availability.

Also (v3.2.1 review pass): `mdllm tokens` re-tiered to kernel reality (Tier 0 measured 5,592 tokens); README updated to describe the deterministic floor and provenance to the public.

---

## [3.2.0] - 2026-06-11

Transformation plan Phases 2–7 (same day as 3.0.0; drafted with `mdllm changelog`). The framework now has provenance, a 93%-smaller operative kernel, deterministic evals, and proactive adapters.

**Deletion pass (Phase 2):** REVIEWLOG migrated into `framework-retrospective-2026-05` and deleted; CHANGELOG entries now drafted by `mdllm changelog`; speculative trigger machinery pruned (`trigger-specification.md` v1.2).

**Provenance (Phase 3):** `provenance.md` (draft) — `type: decision` records with inputs pinned to commits via `informed_by`; `origin: external` + `verified` quarantine for ingested content; `mdllm provenance` enforcement; reverse-provenance derived index; first real decision record committed (`decision-status-vocabulary-domain-owned`). `thing.md` v2.12.

**Session memory (Phase 4):** scoped insight-staleness check at session start (`session-memory.md` v1.1, `session-orientation` prompt v1.1) — live insights × things changed since the brief's `last_updated`; the full sweep stays at retrospective.

**Operative kernel (Phase 5):** `<!-- kernel -->` blocks in the six Tier 0/1 specs, extracted by `mdllm kernel` into a generated `kernel.md` — measured 1.6k tokens replacing 21.4k of full specs. Tier 0 session cost: 26.5k → ~5.3k.

**Evals (Phase 6, Stage 1):** `mdllm eval --fixture` deterministic assertion engine; `evals/` with the first fixture passing 6/6 against the live jmtm domain as a regression net.

**Adapters (Phase 7):** GitHub Actions workflow (validate + provenance + index drift on every push); `adapters/scheduled-triggers.ps1` (proactive deadline surfacing via Task Scheduler); Claude Code PostToolUse adapter example.

---

## [3.0.0] - 2026-06-11

**The Deterministic Floor.** Major version: mechanical validation moves from LLM honor-system to code, and domains now own their status vocabularies. Driven by the 2026-06-11 full review finding that all 17 things in the live jmtm-software domain violated the Level 1 status rule at Error severity, undetected.

**New tooling:**
- `tools/mdllm.py` — single-file CLI (Python, PyYAML): `validate` (structural + referential + schema checks, exit 1 on Errors), `triggers` (mechanical evaluation of time/dependency/threshold conditions + deadline horizon), `index check|rebuild` (derived-index rebuild-and-diff), `tokens` (tier cost measurement; replaces `measure-tokens.py`), `install-hook` (git pre-commit validation — commits with Errors are blocked by construction)

**New normative schemas:**
- `_schema.yaml` (framework domain) and `domain/[domain]/things/_schema.yaml` — declare thing types, **per-type status vocabularies**, required fields, and the relation vocabulary. The validator enforces what the domain declares.

**Conflict resolved:**
- `status-vocabulary-universal-vs-domain` (opened and resolved 2026-06-11, outcome `superseded`): the domain owns its status vocabulary; the six universal workflow values are the advisory default when no schema declares one. jmtm-software's compliance state machines were declared as correct rather than corrected.

**Specs updated:**
- `validate.thing.md` (v1.5 → v2.0): rewritten around the division of labour — the tool guarantees mechanical checks (old Levels 1–3 + index integrity); the LLM keeps semantic validation only. Prompt input/output chain validation removed (type-checking for an event system with no runtime).
- `thing.md` (v2.10 → v2.11): status field rewritten — domain-declared vocabularies, reserved-type vocabularies fixed
- `domain-specification-guide.md` (v2.5 → v2.6): `things/_schema.yaml` added to domain structure; floor installation added to scaffolding
- `orchestration.md` (v1.7 → v1.8): `post-write:commit` hard hook gains its mechanical backstop note
- `AGENTS.md` (v3.0): validation checklist delegates to the tool; measured token costs

**Baseline (Phase 0, same day):**
- First framework retrospective (`framework-retrospective-2026-06`), first conflict thing, `continuity.md` initialised, token costs measured (T0 13.5k / T0+T1 26.5k / full 65.5k), repo tagged `v2.9-pre-floor`, transformation plan committed as `framework-v3-transformation-plan`

---

## [2.9.0] - 2026-06-08

Reflexive behaviour: the agent can now reason *about* a domain, not only *within* it — domain velocity, systematic trigger evaluation, systematic conflict scanning, and schema-coherence review. These four capabilities are unified under one new primitive rather than built as four bespoke mechanisms.

**Why one primitive:** three of the four reduce to "aggregate a signal across all things, then read the aggregate instead of re-scanning everything." That is a **derived index**. The fourth — velocity — deliberately uses no index because its signal already lives in git (the authoritative event stream); caching it would only add a drift surface. The design was constrained by three prior insights: indexes are made drift-safe by construction (`tracking-artifacts-can-drift-from-reality`), maintenance rides the observable `post-write` event rather than a new hard hook (`hard-hooks-require-observable-agent-caused-triggers`), and the behaviour is opt-in/scale-triggered so it doesn't burden the agent on every session (`hook-compliance-correlates-with-scope-not-awareness`).

**New spec (Tier 2 — demand-loaded):**
- `derived-index.md` (v1.0, `status: draft`) — the derived-index pattern: `type: index` things in `things/_index/` that aggregate triggers, relationships, or schema fields. Provenance frontmatter + validation rebuild-and-diff make drift detectable rather than silent. Incremental maintenance on `post-write`, full rebuild on demand/at validation/at retrospective.

**New prompt templates:**
- `templates/prompts/domain-velocity.md` (v1.0) — reads git history as telemetry at session-start; surfaces stalled, churning, or untouched work
- `templates/prompts/review-schema-coherence.md` (v1.0) — audits emergent frontmatter vocabulary for name-drift at retrospective

**New index templates:**
- `templates/indexes/triggers.md.template`, `templates/indexes/schema.md.template`

**Prompts updated:**
- `evaluate-triggers.md` (v1.0 → v1.1) — reads the triggers index when one exists; direct scan otherwise
- `detect-conflicts.md` (v1.0 → v1.1) — adds **scan mode** (proactive corpus sweep) bound to `on-status-change` and `retrospective`, alongside the original change mode

**Specs updated:**
- `thing.md` (v2.9 → v2.10): `type: index` documented as framework-generated
- `validate.thing.md` (v1.4 → v1.5): new **Index Integrity** validation (provenance, coverage, commit-not-behind, rebuild-and-diff) — the mechanism that catches index drift
- `orchestration.md` (v1.6 → v1.7): new `retrospective` hook point; two new framework prompts; index maintenance documented as a domain-level `post-write` hard hook; reflexive-behaviour binding examples
- `trigger-specification.md` (v1.0 → v1.1): session-start evaluation points at the triggers index at scale
- `belief-revision.md` (v1.0 → v1.1): new "When To Scan For Conflicts" — event-triggered (claims gaining authority) and periodic (retrospective full sweep)
- `retrospective.md` (v1.0 → v1.1): reflexive scans (full conflict scan, schema review, index rebuild) run at retrospective cadence
- `git-workflow.md` (v1.0 → v1.1): "Git Log As Domain Telemetry" — velocity signals read directly from history, no index
- `scalability-guide.md` (v1.1 → v1.2): derived indexes as the scale lever for reflexive behaviour, with explicit reconciliation of the "no indexing" principle
- `AGENTS.md` (v2.8 → v2.9), `.markdownllm` (v2.8 → v2.9): inventory, Tier 2 routing, `type: index`, new Key Innovation

**Insights captured:**
- `reflexive-behaviors-are-indexes-plus-prompts` — the four-into-one unification
- `derived-index-is-attention-cache-not-search-layer` — reconciles derived indexes with the scalability "no indexing" principle (both-valid)

---

## [2.8.0] - 2026-05-29

SRP violation corrections across 8 issues identified in the 29 May review sweep. Two new specs extracted from embedded/duplicated content; six existing specs corrected for structural conformance.

**Why these were extracted rather than fixed inline:** `thing.md` v2.8 added the Thing Cohesion and Decomposition principle — the framework's formal statement that content serving different audiences or changing at different rates belongs in separate specs. The two highest-severity issues (embedded example type spec, duplicated multi-lens reasoning) were direct violations of the rule in the same file that defines it; leaving them would have undermined the principle as a teaching tool. Extraction also improves context economics: content previously embedded in Tier 0 (`thing.md`) and Tier 1 (`read/write.thing.md`) — loaded in every session — is now in Tier 2 specs loaded only on demand. **Baseline context load is lower post-v2.8.0 than pre-v2.8.0.**

**New specs (Tier 2 — demand-loaded only):**
- `example-things.md` (v1.0) — full specification for `type: example` things; extracted from `thing.md` where it was embedded alongside unrelated schema content (~50 lines removed from Tier 0)
- `reasoning-lenses.md` (v1.0) — canonical multi-lens reasoning spec; extracted from identical duplication in `read.thing.md` and `write.thing.md` (~95 lines removed from Tier 1)

**SRP violations corrected:**
- `thing.md` (v2.8 → v2.9): replaced `type: example` embedded block with pointer to `example-things.md`; added "Framework-Internal Types" note clarifying `specification`, `guide`, `manifesto` are framework-internal and should not be used for domain things
- `read.thing.md` (v2.0 → v2.1): multi-lens section replaced with pointer to `reasoning-lenses.md`
- `write.thing.md` (v2.0 → v2.1): multi-lens section replaced with pointer; removed undefined `schema_version: 2.0` instruction, replaced with guidance on `version` for framework specs
- `validate.thing.md` (v1.3 → v1.4): removed `name`, `description`, `applies_to` skill-convention fields from frontmatter; description incorporated into spec body
- `framework-discovery.md` (v1.0 → v1.1): became canonical for all deployment architecture; nested repository model section added (previously only in `domain-refresh.md`)
- `domain-refresh.md` (v1.0 → v1.1): Deployment Architecture section reduced to 2-sentence summary + link to `framework-discovery.md`
- `domain-specification-guide.md`: Framework Discovery section reduced from ~30-line restatement to 3-sentence orientation + link to `framework-discovery.md`
- `scalability-guide.md` (v1.0 → v1.1): `type: summary` usage clarified — note added distinguishing manual summary things from the formal `thing-lifecycle.md` mechanism

---

## [2.7.0] - 2026-05-29

- `trigger-specification.md` (v1.0, `status: stable`) created as a standalone spec for the trigger system. Previously, trigger documentation lived only in `thing.md` with a forward reference. Now a full specification covering all four trigger types, all condition and action values, evaluation semantics, and idempotency rules. Added to AGENTS.md Tier 2 loading and framework spec inventory.

---

## [2.6.0] - 2026-05-28

**Session-end reclassification:**
- `orchestration.md` (v1.4 → v1.5): `session-end:continuity` removed as third framework hard hook. Reclassified as a bound prompt — hard hooks require observable, agent-caused triggers; "session is ending" does not meet that criterion. The ritual remains mandatory but is invoked explicitly, not via hard hook.
- `AGENTS.md` (v2.7 → v2.8): Replaced hard hook callout with `[BOUND PROMPT: session-end]` block. Updated On Output section accordingly.
- `session-memory.md`: Ritual section updated to reference prompt-based invocation rather than hard hook.

**New prompt templates:**
- `templates/prompts/session-end-continuity.md` — The continuity extraction ritual as a declared prompt with inputs/outputs
- `templates/prompts/worklog-update.md` — WORKLOG append as a companion prompt, both bound to `session-end`

**Discoverability fix:**
- `AGENTS.md`: `thing-lifecycle.md` (draft spec addressing the 200–300 thing scaling ceiling) added to Tier 2 loading table and spec inventory under new "Deferred" heading. Fixes "ghost spec" problem — existed at root since 23 May but was invisible to framework discovery mechanisms.

**New framework artifact:**
- `REVIEWLOG.md` created as a periodic quality review log. Complements the WORKLOG (session narrative) by tracking how well the framework works, not just what was done. First review written: full holistic review post-v2.5.0.

---

## [2.5.0] - 2026-05-27

Four structural gaps in the framework's knowledge management capabilities closed. New specs cover session continuity, contradiction handling, and periodic reflection. Startup loading made context-window-efficient.

**New specs:**
- `session-memory.md` (v1.0) — how sessions preserve generative knowledge; defines `type: insight`, `type: continuity-brief`, and the mandatory session-end extraction ritual
- `belief-revision.md` (v1.0) — how contradictions between things are held and resolved; defines `type: conflict`, `relation: supersedes/contradicts/superseded-by`, three resolution outcomes
- `retrospective.md` (v1.0) — periodic domain quality reflection; defines `type: retrospective`, when to write one, and what it produces

**New templates:** `insight.md.template`, `conflict.md.template`, `retrospective.md.template`, `continuity-brief.md.template`

**Behavioural changes:**
- `orchestration.md` (v1.3 → v1.4): `session-end:continuity` added as third framework hard hook; covers both insight extraction and belief revision / conflict detection
- `AGENTS.md` (v2.3 → v2.7): startup sequence replaced with tiered loading (Tier 0 ~15k / Tier 1 ~33k / Tier 2 on demand); eliminates up to 75% of startup context cost on Q&A sessions
- `thing.md` (v2.3 → v2.5): four framework-reserved types (`insight`, `continuity-brief`, `conflict`, `retrospective`); framework-reserved relation values (`supersedes`, `contradicts`, `superseded-by`); new recommended fields `confidence` and `origin`
- `validate.thing.md` (v1.1 → v1.2): conflict-integrity checks added to Level 4 Semantic Validation; retrospective staleness Info check

**Bug fixes (consistency pass):**
- `orchestration.md` frontmatter version corrected (1.3 → 1.4)
- `thing.md` version corrected (2.3 → 2.5); `retrospective` added to reserved types list
- `session-memory.md` linked_things: added `belief-revision-specification`
- `orchestration.md` linked_things: added `belief-revision-specification`

**Known gaps (deferred):** `domain-specification-guide.md` does not yet reference the new knowledge primitives (continuity.md, insight, conflict, retrospective). A new domain created with the current guide starts without awareness of these. Tracked for a future patch.

---

## [2.4.0] - 2026-05-22

- Rewrote README.md: reframed from human instruction manual to agent-first, human-directed partnership model. Added agent-user transcript showing domain creation through conversation.
- Updated llm-driven-systems.manifesto.md (v2.0 → v2.1): added "Discovery: The Partnership Without Configuration" section. Revised Getting Started to emphasize design intent, feedback loops, and ongoing collaboration.
- Updated domain-specification-guide.md (v2.3 → v2.4): reframed AGENTS.md creation as design decisions (not template-filling). "Plan Your Domain" → "Design Your Domain". "Iterate" → "Use It, Refine It, Grow It" with concrete feedback examples.
- Core framing clarification: specs are written for agents to consume; humans direct, design, use, and refine; the partnership produces the system. No structural/architectural changes — the specs already modelled this correctly.

---

## [2.3.0] - 2026-05-21

- Made orchestration opt-in: demoted from framework-level to domain-level pattern after real-world testing showed it made LLM reasoning rigid
- Moved prompt files from `prompts/` to `templates/prompts/` (templates, not mandates)
- Updated orchestration.md (v1.0 → v1.1): added "When To Use / When Not To Use" guidance
- Renamed `validate.thing.skill.md` → `validate.thing.md`, reclassified as `type: specification` (matches read.thing.md / write.thing.md pattern)
- Promoted all framework specs from `status: draft` to `status: stable` — pushed to remote = not draft
- Fixed consistency gaps: README now lists all 12 framework specs, CONTRIBUTING lists newer specs, WORKLOG frontmatter updated
- Fixed README stale status values (`draft/active/complete` → canonical thing.md values)
- Fixed README "Templates (Future Organization)" → reflects current state
- Adopted per-push changelog format (this change)

---

## [2.2.1] - 2026-05-19

**Domain Refresh Specification (domain-refresh.md):**
- Defines the nested git repository deployment architecture (framework repo + isolated domain repos, .gitignore contract)
- Specifies the refresh process: how domain agents check CHANGELOG, WORKLOG, and foundational specs for framework evolution
- Refresh algorithm with version tracking via `framework_version_seen` frontmatter field
- Integration points for domain workflow skills and AGENTS.md startup sequences

---

## [2.2.0] - 2026-05-19

### Triggers, Validation, Commit Conventions, and Skill File Standardization

This release adds trigger support, validation patterns, structured git conventions, and standardized skill file format to the existing architecture.

### Added

**Triggers System Implementation:**
- Integrated trigger documentation throughout domain specifications
- Session-start triggers: time-based (due dates, stale items), dependency-based (unblocked work), threshold-based (overload warnings)
- Post-write triggers: validate state changes, cascade effects, notify dependents
- Trigger examples in both example domains (Life Manager, Compliance Patterns)
- Trigger integration with git commit history for temporal reasoning

**Validation Framework:**
- Four-level validation strategy in domain-specification-guide.md: structural, referential, domain-specific, semantic
- Three severity tiers: error, warning, info
- Post-write validation checkpoints and procedures
- Validation checklists in example AGENTS.md files
- Validation sections in all templates and example skill files

**Git Commit Conventions:**
- Structured commit message format: `action: description` (e.g., `create: task-id`, `update: project status`)
- Commit points in workflows: create, status-change, batch operations, phase transitions, archive
- Git log as event stream for trigger evaluation
- Examples of commit conventions in all skill files and workflow documentation

**Skill File Standardization:**
- All skill files now have complete YAML frontmatter: `id`, `type`, `status`, `version`, `created`, `linked_things`
- Updated skill file frontmatter in both example domains (Life Manager, Compliance Patterns)
- Status field shows skill maturity: `draft`, `evolving`, `stable`
- Relationship metadata showing which skills implement/orchestrate/complement each other
- Consistent versioning across all skills

### Changed

**Examples Updated to v2.0:**
- Life Manager AGENTS.md → v2.0 with trigger integration, validation checkpoints, commit conventions
- Compliance Patterns AGENTS.md → v2.0 with dependency triggers, post-write validation, audit trail integration
- All example skill files enhanced with: proper frontmatter, trigger sections, validation rules, commit conventions

**Domain-Specification-Guide Enhanced:**
- Updated to v2.1 with comprehensive trigger documentation
- Added git-workflow and interface-specification as linked references
- Expanded skill file templates with trigger sections, validation checkpoints, commit conventions
- Clarified thing status values: `not-started`, `in-progress`, `blocked`, `paused`, `completed`, `cancelled`
- Added domain-specific validation rules patterns
- Enhanced AGENTS.md template with trigger evaluation flow

**Templates Updated for Standardized Skill Format:**
- AGENTS.md.template — Added trigger section, validation checklist, git commit conventions
- domain-specification.skill.md.template — Added id, status, linked_things frontmatter; added validation rules and triggers sections
- domain-read.thing.skill.md.template — Added skill file frontmatter structure; added trigger checking; enhanced context loading strategy
- domain-write.thing.skill.md.template — Added validation checklist and procedures; added post-write trigger evaluation; structured commit conventions
- domain-workflow.skill.md.template — Added trigger integration, git commit points, validation checkpoints

**Manifesto Updated:**
- Clarified vendor agnostic principle: use AGENTS.md, .skill.md, and YAML frontmatter (not .instructions.md, .prompt.md conventions)

### Refined

- Example compliance patterns enhanced with bidirectional linking (positive patterns ↔ anti-patterns)
- Life Manager thing types standardized with clear status transitions and domain validation rules
- Trigger examples across domains show concrete, actionable conditions (overdue, unblocked, threshold)
- Post-write validation examples demonstrate three-level checks (structural, referential, domain-specific)

## [2.1.0] - 2026-05-19

### Interface, Git Workflow, Validation, Triggers, Self-Describing Architecture

This release adds operational specifications that were previously gaps and makes the framework self-describing (fractal). New specs carry `status: draft` and will mature through use.

### Added

**New Specifications:**
- **interface.md** — The I/O layer specification. Documents input routes (VS Code, CLI, mobile, voice), the thin-interface principle (use existing routes, don't build new ones), and the things vs deliverables distinction (things are persistent state; deliverables are produced artefacts like documents, code, images, video, audio).
- **git-workflow.md** — Git as state machine specification. Defines commit points (after creation, status transition, write session, session end), structured commit message conventions (action: description), who commits (agent locally, human pushes), git log as event stream for triggers, and three-layer auditability (worklog → git log → git diff).
- **validate.thing.skill.md** — Universal validation skill. Four-level validation: structural (valid YAML, required fields), referential (link integrity, bidirectional consistency), domain-specific (rules from specification skill), semantic (LLM-reasoned coherence checks). Three severity tiers: error, warning, info.

**Triggers System (in thing.md):**
- Declarative trigger conditions as YAML metadata on things
- Four trigger types: time-based (due_date_passed, stale), dependency-based (watch IDs for status changes), threshold-based (subtasks_complete, blocked_duration), relationship-based (watch connected things)
- Declarative actions: surface, re_evaluate, suggest_completion, unblock, escalate, cascade, notify
- Three evaluation moments: session start, after writes, scheduled invocation
- Idempotent evaluation — no extra state needed; git history provides temporal context

**Self-Describing Architecture:**
- All foundational specs now have YAML frontmatter (id, type, status, version, created, linked_things)
- Root AGENTS.md created — the framework orchestrates itself as a domain
- Framework specs are things within the framework they define (fractal/self-describing property)
- Spec types: `manifesto`, `specification`, `skill`, `guide`
- Spec statuses: `draft`, `evolving`, `stable`, `deprecated`

**WORKLOG.md:**
- Session-based work log adopted for this repository
- Captures completed work, decisions made, reflections, and forward planning
- Complements CHANGELOG (what shipped) with WORKLOG (how it evolved session by session)

### Changed

**Manifesto (llm-driven-systems.manifesto.md):**
- Added "Origins and Influences" section — credits Clean Architecture (Robert C. Martin) and SOLID principles; establishes "build on what exists" philosophy (AGENTS.md, .skill.md, YAML, markdown, git are all existing conventions)
- Added Principle 8: "Self-Describing (Fractal)" — the system describes itself within itself; same pattern at every scale
- Expanded Principle 6: "Version-Controlled Everything" — git as state machine, commit discipline, event stream, three audit layers
- Updated "How It Works In Practice" — references AGENTS.md, triggers, deliverables, commit conventions
- Updated "Getting Started" — reflects current workflow (AGENTS.md first, commit meaningfully, WORKLOG)
- Expanded "Auditing" in "What This Enables" — three-layer auditability model

**Domain Specification Guide (domain-specification-guide.md):**
- Added "The Self-Describing Principle" section — domain specs can themselves be things
- Updated checklist — includes validation, commit conventions, triggers
- Expanded Key Takeaways from 7 to 10 points (git as state machine, interface routes, validation, self-describing)

**CONTRIBUTING.md:**
- Restructured to reflect current framework structure
- Added "Everything is a thing" guideline (all files should have frontmatter)
- Added git-workflow.md conventions for contributors
- Added validation requirement before submitting
- Listed full framework file structure with roles

**Core Spec Fixes:**
- Fixed `read.thing.md` and `write.thing.md` — updated old `[domain].instructions.md` references to `[domain]-specification.skill.md`
- Fixed `README.md` — updated 3 references from `Instructions-guide.md` to `domain-specification-guide.md`

### Why This Matters

The three decoupled layers (Interface, Processing, Storage) each now have explicit specifications, though several carry `status: draft` and are expected to evolve through real-world use. Things can be reactive (triggers). Integrity is verifiable (validation). Git usage is disciplined (workflow). The system describes itself within itself.

The framework composes existing proven tools (AGENTS.md, .skill.md, YAML, markdown, git, LLMs) into a new architectural pattern — it invents no new infrastructure, protocols, or interfaces.
- Integration guides for popular LLMs and platforms

## [2.0.0] - 2026-05-19

### Major Refactoring: Three-Layer Simplification

This release represents a significant architectural refinement, moving from a five-component approach to a three-layer model that follows similar patterns to production LLM agent systems.

### Changed (Breaking)

**Framework Architecture Simplified:**
- Renamed: `[domain]-instructions.skill.md` → `[domain]-specification.skill.md`
  - Clarifies that this is domain philosophy/principles, not instructions to follow
  - Better aligns with industry terminology (AGENTS.md + SKILL.md standards)
  
- Key distinction established: `thing.md` is foundational **specification**, not a skill
  - `thing.md` — Universal atomic unit specification (not a `.skill.md` file)
  - Skills (`.skill.md` files) — Reusable capabilities (specification, read, write, workflow)
  - Previous confusion between "skill files" and "spec files" eliminated

**Updated All References Throughout:**
- Templates: All four domain templates use `specification` and correct file extensions
- Examples: Both `life-manager/` and `compliance-patterns/` restructured with new naming
- Documentation: README, domain-specification-guide, CONTRIBUTING all updated
- Core docs: All skill files now reference `thing.md` (not `thing.skill.md`)

### Architecture Now Fully Cohesive

**Three Clear Layers:**
```
Layer 1: AGENTS.md
  ↓ auto-discovers at root
Layer 2: SKILLS/ 
  (specification, read.thing, write.thing, workflow .skill.md files)
  ↓ reusable capabilities
Layer 3: THING.MD (foundational specification) → THINGS/ (instances)
```

**Vendor-Agnostic Discovery:**
- `AGENTS.md` sits at repository root and is auto-discovered by:
  - OpenAI Codex, GitHub Copilot, Cursor, Windsurf, Gemini CLI (natively)
  - Claude Code (via CLAUDE.md wrapper referencing AGENTS.md)
- Skills are portable across all vendors (standard YAML frontmatter + markdown)
- Domain repos can be deployed independently with their own AGENTS.md

### Documentation Improvements

- **README.md** — Restructured to match three-layer model; removed dated references to "five-component pattern"
- **domain-specification-guide.md** — Renamed from "instructions-guide"; updated all structural diagrams
- **CONTRIBUTING.md** — Updated contribution guidelines to reflect three-layer pattern
- **Template files** — All template filenames and content use consistent naming
- **Example domains** — Both examples now show clean structure with specification.skill.md, not instructions.skill.md

### Why This Matters

The previous framework conflated several concepts (instructions, skills, specs, prompts) in ways that didn't match how actual agent systems work. This version:

- **Follows emerging patterns** — Uses the AGENTS.md + SKILL.md structure adopted by several LLM agent frameworks
- **Eliminates confusion** — Clear distinction between discovery (AGENTS.md), capabilities (skills), definition (thing.md), and instances (things)
- **Improves scalability** — Each domain is fully deployable independently, with clear entry point (AGENTS.md)
- **Enables multi-vendor usage** — Agent files auto-discover across different LLM tools
- **Simplifies onboarding** — New users understand: "Agent loads first, then skills, then things"

### Technical Accuracy

- **Vendor maturity confirmed** — AGENTS.md is now stewarded by the Agentic AI Foundation (under Linux Foundation) with broad cross-tool support
- **Discovery mechanism validated** — Verified Codex walk-from-root-to-cwd behavior and auto-discovery across tools
- **Framework positioning correct** — MarkdownLLM is the library/template specification; domains are deployed separately with their own root AGENTS.md

## [1.4.0] - 2026-05-18

### Added
- **Five-Component Domain Pattern** — Complete framework documentation for building applications
  - Explicit requirements: Instructions, Application, Workflow(s), and Read/Write Prompts
  - Each component has a clear purpose, structure, and interaction pattern
  - Minimal and complex domain patterns documented
- **Application File Specification** — New `[domain].application.md` as atomic thing that answers "what problem does this solve?"
  - Application thing type with standard metadata
  - Explicit problem definition and delivery specification
  - Links to supporting workflows and resources
- **Comprehensive Getting Started Guide** — Expanded `instructions-guide.md` with:
  - Complete five-component workflow for building domains
  - Visual diagram showing component relationships and data flow
  - Detailed sections on each component's purpose and structure
  - Patterns for minimal vs. complex domains
- **Updated README** — Restructured to emphasize the five-component pattern
  - Expanded application examples with structured descriptions
  - Step-by-step guide from understanding principles to implementation
  - Clarified distinction between domain definitions and application instances
- **Reference Domain** — Added as primary example domain
  - Demonstrates the complete five-component pattern
  - Shows how complex workflows are orchestrated

### Changed
- README.md now guides users through the five-component pattern explicitly
- Getting Started section provides concrete steps for each component
- Example domains restructured as Example Applications with consistent documentation
- Clarified terminology: "domain applications" vs. "instances of things"

## [1.3.0] - 2026-05-18

### Added
- **Multi-Lens Reasoning** — Framework support for multi-perspective decision-making
  - Domain Logic Lens: What does this domain require?
  - Compliance Logic Lens: What regulatory/architectural constraints apply?
  - Audit Logic Lens: Can we defend and explain this decision?
  - Lens conflict detection and resolution guidance
  - Auto-generated audit trails encoding reasoning process
- **Example Type System** — New `type: example` for pattern libraries and anti-patterns
  - Teaches LLMs through demonstration (inductive learning)
  - Supports positive patterns and anti-patterns with violations explained
  - Pattern types: `positive-pattern`, `anti-pattern`, and domain-specific variants
  - Examples function as living documentation and behavioral reinforcement
- **domains/compliance-patterns/** — Reference domain for regulated systems
  - Compliance-patterns.instructions.md: Philosophy and usage guidance
  - example-gdpr-compliant-data-handling.md: Concrete GDPR compliance example showing all three lenses aligned
  - example-gdpr-violation-anti-patterns.md: Anti-pattern example showing violations and how to fix them
  - Serves as reference library for law, finance, healthcare domains

### Enhanced
- **thing.skill.md** — Added "Special Type: Example" section explaining:
  - How examples work as inductive learning for LLMs
  - Creating pattern libraries for domain-specific behaviors
  - Using positive + negative examples to teach good practices
- **read.prompt.md** — Added "Multi-Lens Reasoning (Optional)" section with:
  - How to apply multiple lenses to analytical questions
  - Handling lens conflicts (compliance vs. domain efficiency)
  - Learning from examples in the repository
  - Examples of read-mode queries showing multi-lens analysis
- **write.prompt.md** — Added "Multi-Lens Reasoning for Changes (Optional)" section with:
  - Pre-change validation through all lenses
  - Detecting compliance risks before changes propagate
  - Using examples to validate pattern alignment
  - Handling conflicts: when compliance overrides domain preferences
- **instructions-guide.md** — Added "Defining Domain-Specific Reasoning Patterns" section covering:
  - Creating domain-specific lenses
  - Building reasoning patterns for your domain
  - Reinforcing lenses through examples
  - When to use multi-lens vs. simple reasoning

### Framework Improvements
- Enables "compliance-by-design"—regulatory requirements encoded as reasoning lenses, not bolt-on checks
- Scales reasoning complexity with domain complexity (optional lenses, discovered when needed)
- Supports regulated domains (law, finance, healthcare) requiring audit trails and decision justification
- Example-driven learning complements rule-based constraints for more natural LLM behavior
- Aligns with neural network principles: multiple reasoning pathways, conflict resolution, inductive vs. deductive reasoning

### Why This Matters
Real-world systems operate under constraints (GDPR, HIPAA, audit requirements). Previous framework versions could encode domain logic but struggled with compliance thinking. Multi-lens reasoning makes constraints first-class citizens in the reasoning process. Examples teach patterns inductively—how LLMs naturally learn—rather than forcing rule-based compliance. This enables productive LLM systems in heavily regulated environments where every decision must be explainable and defensible.

## [1.2.0] - 2026-05-17

### Added
- **Tiered Context Windows** — Multi-level loading strategy for scalability
  - Level 1: Metadata only (for broad questions and landscape scanning)
  - Level 2: Metadata + relationships (for dependency traversal and critical path analysis)
  - Level 3: Full context (for deep work and detailed reasoning)
- **scalability-guide.md** — Comprehensive guide covering:
  - Philosophy of multi-level abstraction inspired by neural networks
  - Three scaling approaches: Contextual Loading (now), Incremental Summarization (medium-scale), Full Tiered System (long-term)
  - Feel-based signals for when to scale
  - Progressive adoption pattern

### Enhanced
- **thing.skill.md** — Added "Multi-Level Context Windows" section explaining how the same thing file works at different levels of granularity
- **read.prompt.md** — Added "Loading Strategy" section with guidance on choosing context levels and tab-based examples for each level
- **write.prompt.md** — Added "Loading Strategy" section adapted for write operations, emphasizing cascading effects and dependency updates

### Framework Improvements
- Implemented adaptive context loading (LLM determines relevance dynamically, not pre-labeled)
- Aligned scalability approach with neural network principles: multiple abstraction levels, dynamic attention, holistic reasoning
- Enables scaling from 10s to 1000s of things while maintaining framework elegance
- Progressive adoption: users discover tiering naturally when they need it (no forced optimization)

### Why This Matters
The framework now scales efficiently without requiring indexed search or special query languages. By leveraging the LLM's native pattern-matching ability at appropriate levels of abstraction, systems can grow from simple to complex while staying true to the core philosophy: definitions, markdown files, and holistic LLM reasoning.

## [1.1.0] - 2026-05-17

### Changed
- **Restructured core framework files for generalization**
  - `thing.skill.md` — Generalized from "thing to do" specific language to work as a specification for *any* domain's atomic unit
  - `read.prompt.md` — Generalized to work with any domain; removed life-management specific references
  - `write.prompt.md` — Generalized prompt guidance; removed phone/calendar integration specifics
- **README.md** — Updated to clarify distinction between specification files (universal foundation) and instantiated domains (domain-specific examples)

### Added
- **Domain structure** — Created `domains/` folder to organize domain-specific implementations
- **domains/life-manager/** folder containing:
  - `life-manager.instructions.md` — Domain-specific philosophy and principles for life management
  - `read.prompt.md` — Life-management-specific read prompt with concrete examples
  - `write.prompt.md` — Life-management-specific write prompt including phone/calendar integration guidance
- **instructions-guide.md** — Comprehensive guide for creating domain-specific instructions files

### Removed
- Duplicate `life-manager.instructions.md` from root level (consolidated into `domains/` structure)

### Clarified
- Core framework now clearly separates:
  - **Specification** (root level): Universal files that apply to any domain
  - **Implementation** (domains/): Domain-specific instantiations of the framework

## [1.0.0] - 2026-05-17

### Added
- **llm-driven-systems.manifesto.md** — Core philosophy and conceptual framework
- **life-manager.instructions.md** — Example instructions file for a life management system
- **thing.skill.md** — Example skill file defining the "thing to do" atomic unit
- **read.prompt.md** — Prompt template for read-only analysis and insights
- **write.prompt.md** — Prompt template for active system management and updates
- **README.md** — Complete documentation on what this framework is and how to use it
- **CONTRIBUTING.md** — Guidelines for contributing domains and improvements
- **CHANGELOG.md** — This file, tracking project evolution
- **LICENSE** — MIT License with copyright notice

### Framework Principles Established
- Definition-driven system design
- Atomic and composable units
- Minimal core with emergent detail
- LLM-centric data structure
- Vendor-agnostic conventions
- Version-controlled everything
- Transparent and auditable systems

---

## How To Use This Changelog

### For Users
- Check here to see what's new in each release
- Stay informed about breaking changes
- Plan your updates accordingly

### For Contributors
- Add your changes here when making pull requests
- Use the categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Keep it organized and readable

### Versioning
- **MAJOR** version for breaking changes to the framework
- **MINOR** version for new domains, features, or capabilities
- **PATCH** version for clarifications, fixes, documentation improvements

---

**Note:** This project tracks changes to the framework specification itself, not to your individual data files. Your data files live in git and have their own version history.
