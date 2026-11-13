# Review-catch candidates

Repo head `83ad75d008fdc7ad2f96a3f799c9c4327ca01b26`, mined 2026-11-13T22:26:21+00:00.

## Rules

- **fix_subject_regex**: ^fix(\(\|:\|\+\|!\| ) (case-insensitive)
- **since_author_date**: 2026-07-01
- **scope**: tools/**/*.py excluding tools/tests/
- **blame**: git blame -M -C --porcelain -L <old ranges> F^ -- <file>
- **filter_moved_lines**: an old-side line of F whose stripped text (non-empty) equals the stripped text of any line F adds in any scope file is ignored before blame
- **filter_blank_lines**: old-side lines that are blank or whitespace-only are ignored before blame
- **filter_refactor**: an introducing commit whose subject matches ^refactor (case-insensitive) is rejected; such commits are also excluded from controls
- **min_share**: 0.6
- **changed_lines_min**: 10
- **changed_lines_max**: 600
- **changed_lines_basis**: added+removed vs first parent, --no-renames, scope files only
- **controls**: subject not a fix (tight regex), not ^refactor, not a merge, in date and size range, zero blamed lines from any fix on the UNFILTERED tallies (before the moved/blank filters); items use the filtered tallies
- **freeze_controls**: walk chosen items by ascending sha; each takes the unused control with the closest changed_lines (ties: lower sha); one control per item
- **keywords**: review, codex, cold, ci, test, smoke, first, live, operator, use
- **freeze_seed**: 20261113

## Counts

- fix_commits_considered: 58
- fix_merges_skipped: 0
- dropped_by_subject_match: 3
- accepted_fixes: 19
- rejected_fixes: 39
- items: 16
- defects: 26
- controls: 78
- pure_addition_hunks: 118
- old_side_lines: 700
- ignored_moved: 146
- ignored_blank: 10
- blamed_ranges: 329

## Rejections

| reason | count |
|---|---|
| no commit holds >= 60% of blamed lines | 14 |
| introducing commit before 2026-07-01 | 9 |
| no blamed lines (pure additions) | 6 |
| introducing commit size outside 10..600 changed lines | 5 |
| introducing commit is a refactor | 4 |
| only moved or blank lines | 1 |

## What a --freeze would select today

All items, each with its size-matched control (no set.json written).

| item | item lines | control | control lines |
|---|---|---|---|
| `065248158f` | 224 | `5237b9f714` | 227 |
| `27b072371d` | 167 | `99327652af` | 166 |
| `413a082118` | 154 | `a86e328bc2` | 161 |
| `4c2a3ddeec` | 95 | `6de8474be2` | 95 |
| `58212ce776` | 306 | `6d3aa819e7` | 299 |
| `6572fb76ed` | 186 | `8d3a635f49` | 181 |
| `690d75bd17` | 506 | `07590f833a` | 509 |
| `69963094b5` | 421 | `460bb5a8aa` | 415 |
| `8830f3163b` | 433 | `75cf830e04` | 458 |
| `ba65fb5986` | 230 | `ae4e61d0ba` | 229 |
| `d47b86d3ef` | 74 | `9f506ee30d` | 75 |
| `e2bad9f808` | 352 | `0fdc27714c` | 367 |
| `f041d4b4f8` | 565 | `9f0cc58ce6` | 523 |
| `f258b0ebff` | 214 | `89d1e7ad72` | 218 |
| `f29c96e404` | 122 | `927693f572` | 123 |
| `fda4fa8c48` | 443 | `371692df3b` | 399 |

## Items

| commit | date | lines | subject | fix | file | ranges | share | days | moved/blank ignored | keywords |
|---|---|---|---|---|---|---|---|---|---|---|
| `065248158f` | 2026-07-28 | 224 | floor: mdllm estate-sync — the machine axis mechanised; discovery walks root + d | `2bdc60f7fa` fix: make explicit estate freshness route Codex approval | tools/markdownllm/cli.py | 206-206, 209-209 | 0.64 | 21.1 | 4/0 | codex |
|  | | | | `2bdc60f7fa` fix: make explicit estate freshness route Codex approval | tools/markdownllm/sync.py | 154-154, 163-163, 177-178, 188-188, 191-191, 193-193 | 0.64 | 21.1 | 4/0 | codex |
| `27b072371d` | 2026-08-13 | 167 | fix: centralize prefix-aware runtime candidates | `82f2cfc688` fix: bound shared Windows launch resolution | tools/markdownllm/adapters/codex.py | 45-45, 194-195, 198-199, 201-202, 205-209, 212-212 | 0.70 | 0.0 | 0/3 | codex |
|  | | | | `82f2cfc688` fix: bound shared Windows launch resolution | tools/markdownllm/runtime.py | 74-74, 85-85, 106-108, 110-114, 116-119, 121-126 | 0.70 | 0.0 | 0/3 | codex |
|  | | | | `59d023bb87` fix: keep POSIX resolution inside its host boundary | tools/markdownllm/runtime.py | 59-63, 65-68, 75-76, 78-81, 86-86, 115-115, 120-120, 134-135 | 1.00 | 0.0 | 0/0 | codex |
| `413a082118` | 2026-08-21 | 154 | build: mdllm precommit — the hook's four legs, concurrent against one candidate  | `039dd84761` fix: the hook's block message stops advertising --no-verify | tools/markdownllm/precommit.py | 43-44, 47-48 | 1.00 | 21.8 | 0/0 | review, test, operator |
|  | | | | `3daf1d18bc` fix: coordinator children run the entry the hook invoked; CAS fixture  | tools/markdownllm/precommit.py | 61-61, 63-63, 88-88 | 1.00 | 0.0 | 0/0 | test |
| `4c2a3ddeec` | 2026-07-16 | 95 | floor: quarantine flip discipline — born-verified + verified_by attribution chec | `1d841e6e4c` fix: _git_stdout decodes git output as UTF-8, not the platform locale | tools/markdownllm/validation.py | 392-393 | 1.00 | 5.7 | 0/0 | operator, use |
| `58212ce776` | 2026-10-05 | 306 | fix(eval): close the answer-key grant, make committed state the carrier, add the | `374b59657d` fix(eval): the first guarded smoke found three runner bugs — anchor th | tools/markdownllm/evals.py | 148-149, 200-203, 206-207, 209-209, 662-662, 727-727 | 1.00 | 0.0 | 0/0 | smoke, first |
| `6572fb76ed` | 2026-08-13 | 186 | evidence: POSIX floor verified on Linux — resolution, validation, git boundary;  | `244fdfea39` fix: forward unused lifecycle budget to orientation | tools/markdownllm/adapters/codex.py | 283-283 | 0.62 | 0.4 | 8/0 |  |
|  | | | | `244fdfea39` fix: forward unused lifecycle budget to orientation | tools/markdownllm/harness_ports.py | 59-59, 88-89, 95-95 | 0.62 | 0.4 | 8/0 |  |
|  | | | | `244fdfea39` fix: forward unused lifecycle budget to orientation | tools/markdownllm/lifecycle_runner.py | 111-111, 122-123 | 0.62 | 0.4 | 8/0 |  |
| `690d75bd17` | 2026-09-27 | 506 | reconcile: make Codex Cloud a multi-repository workspace | `5359f5bd40` fix: keep Cloud host vocabulary explicit at the architecture gate | tools/markdownllm/cloud_repositories.py | 142-142, 152-152 | 1.00 | 0.4 | 0/0 |  |
| `69963094b5` | 2026-08-11 | 421 | extract: Claude behind the accepted ports — Phase 2C of vendor-harness-adapter-f | `f64480cf01` fix: withdraw false Claude ordering claim | tools/markdownllm/adapters/claude_code.py | 17-20, 61-61, 78-78 | 0.67 | 1.1 | 0/0 |  |
| `8830f3163b` | 2026-10-05 | 433 | floor: mdllm reckon — the reckoning reads every attention item's exit, in three  | `75fd7dc905` fix+reconcile: the Codex review of e5de9fa dispositioned — the composi | tools/markdownllm/reckon.py | 376-376 | 1.00 | 15.1 | 0/0 | review, codex, test, first, operator |
| `ba65fb5986` | 2026-07-28 | 230 | floor: both sync directions become visible consumer-side — imports-check gains D | `0200054786` fix: pin comparison survives YAML int coercion — _pins_match normalise | tools/markdownllm/imports_check.py | 148-148 | 1.00 | 8.7 | 0/0 | ci |
| `d47b86d3ef` | 2026-08-08 | 74 | v3.28.0 — the session gate: a contract-less session becomes loud at its first wr | `a8786c2208` fix(floor): the gate stops crying wolf at fresh clones | tools/markdownllm/validation.py | 716-717 | 1.00 | 0.9 | 8/0 | operator |
| `e2bad9f808` | 2026-09-12 | 352 | build: the cue carrier — `type: cue`, `mdllm cues`, and a session-start line tha | `812f7d7e7d` fix: the cue walk read a bare --since date as "today at now", so the r | tools/markdownllm/touchpoints.py | 353-353 | 1.00 | 0.8 | 0/0 | test |
| `f041d4b4f8` | 2026-08-18 | 565 | build: assemble + the rendered bundle — Phase 3 of cowork-adapter | `f87a9b9b97` fix: refuse to build a bundle the harness would reject at install | tools/markdownllm/adapters/cowork.py | 139-139 | 1.00 | 0.0 | 1/0 | test, first, operator |
|  | | | | `646bf86032` fix: bundle bytes are LF-only and the mechanism hash is EOL-stable | tools/markdownllm/adapters/cowork.py | 104-104, 124-124 | 1.00 | 0.0 | 0/0 |  |
| `f258b0ebff` | 2026-10-30 | 214 | floor+plan: a stalled turn rings — the seat reads unpublished commits and unansw | `bf2d230080` fix: the stall ring is calibrated on the healthy rhythm, not the failu | tools/markdownllm/cli.py | 274-278, 509-509 | 1.00 | 0.0 | 1/0 | test, first, live, operator |
|  | | | | `bf2d230080` fix: the stall ring is calibrated on the healthy rhythm, not the failu | tools/markdownllm/seat.py | 34-37, 51-54, 154-154, 189-189, 191-193, 198-199, 202-202, 206-206, 211-211, 217-218, 253-254, 256-256, 260-260, 317-317, 322-322 | 1.00 | 0.0 | 1/0 | test, first, live, operator |
| `f29c96e404` | 2026-09-22 | 122 | fix: the docs checks take the CLI's inventory from the root instead of reaching  | `446155b893` fix: the toolbox renders on the site — two kramdown differences the bl | tools/markdownllm/docs_blocks.py | 257-257 | 1.00 | 0.2 | 0/0 | test, live, operator |
| `fda4fa8c48` | 2026-09-22 | 443 | derive: the docs learn to read the tool — public-docs-face-build Phase 1 | `f29c96e404` fix: the docs checks take the CLI's inventory from the root instead of | tools/markdownllm/cli.py | 90-90 | 0.92 | 0.0 | 3/0 |  |
|  | | | | `f29c96e404` fix: the docs checks take the CLI's inventory from the root instead of | tools/markdownllm/coherence.py | 704-704 | 0.92 | 0.0 | 3/0 |  |
|  | | | | `f29c96e404` fix: the docs checks take the CLI's inventory from the root instead of | tools/markdownllm/docs_blocks.py | 19-24, 119-120, 122-123, 125-126, 140-141, 200-200, 206-206, 211-211, 240-245, 354-355, 357-357, 359-359, 378-378, 390-391, 395-395, 398-398, 407-407 | 0.92 | 0.0 | 3/0 |  |

## Controls

| commit | date | lines | subject |
|---|---|---|---|
| `031c2ac1d4` | 2026-08-23 | 61 | framework: F8a derive leg — the root's type list stops being hand-written |
| `07590f833a` | 2026-08-28 | 509 | sense(floor): a skill that instructs vocabulary the schema never declared |
| `0c3dc3d839` | 2026-08-10 | 11 | v3.30.1 — the ninth review: a cold read certifies what the author could not, and seven survivors fal |
| `0ca893d317` | 2026-10-27 | 46 | floor+spec: the pin governs drift — a paused workspace accrues no debt from the framework moving ben |
| `0d8974a671` | 2026-08-28 | 43 | sense(floor): a workflow-definition past draft with zero runs is an Info finding |
| `0e3bc6bd3c` | 2026-08-18 | 113 | build: register the cowork adapter — Phase 0 of cowork-adapter |
| `0f403e54ab` | 2026-10-30 | 97 | evals+rule: the runner's half of the eval backlog is done — an aborted trial is void, a launch failu |
| `0fdc27714c` | 2026-10-15 | 367 | floor+spec: the seat — who sits in a clone, a guard on regenerating from behind, and the ticket as a |
| `12ff5ef10b` | 2026-08-26 | 10 | reconcile: bind workflow adoption surfaces to governing revisions |
| `1e6f167893` | 2026-08-21 | 47 | build: quarantine flip checks batch their git reads (F12) |
| `283e9084f6` | 2026-09-24 | 72 | feat:add-openclaw-session-start-adapter-slice |
| `2ed6dfe33f` | 2026-09-27 | 41 | reconcile: close Codex Cloud parity with Cowork |
| `31d98408a8` | 2026-10-07 | 104 | floor: the follow — the entry file names the workflow to follow per type; refresh adds the block onc |
| `371692df3b` | 2026-08-15 | 399 | remove: the assistant-register Phase 0 prototype — the decision cancelled it, so the flag, renderer, |
| `3b255f7e39` | 2026-08-21 | 268 | create: perplexity harness adapter (ambient credentials, two skill surfaces) |
| `3fb2a7f6bb` | 2026-08-06 | 15 | phase-0(assistant-register): leg 3 — one ordering, named; write for the ear |
| `444b4d6a1b` | 2026-08-23 | 107 | framework: F8b — the terms file gets an invariant it cannot have a floor for |
| `460bb5a8aa` | 2026-08-13 | 415 | build: add explicit recognised-legacy adapter refresh |
| `4d373a48e3` | 2026-08-08 | 52 | feat(porch): the probe control — --token gates the HTTP porch behind a per-run bearer token, carried |
| `4e5e2f1c66` | 2026-08-29 | 288 | floor(dispatch): `mdllm dispatch-payload` — the corpus composes the launch text, the scheduler carri |
| `5237b9f714` | 2026-08-20 | 227 | harden: kernel emitted, not instructed — channel-aware Tier-0 delivery (Phase 2) |
| `5767e0b875` | 2026-11-10 | 233 | floor+spec: the wake carries the contract — a ticket's wake hands over its last three turns and two  |
| `57b99b6cd5` | 2026-09-22 | 46 | unblock: the evals were not waiting on isolation — they were waiting on a plan nobody updated |
| `57f52934b8` | 2026-08-23 | 134 | framework: F8b — the perimeter gets an interval, and a latent glob defect goes with it |
| `5862d170b5` | 2026-10-30 | 64 | floor+spec: the wake's broken link, read from the record and fixed twice — a seat-aware self-wake th |
| `5e17ea6506` | 2026-08-05 | 19 | imports-check: two stale species — 'content identical' (pin moved, nothing crossable changed: re-pin |
| `5e4842195b` | 2026-09-12 | 43 | reconcile: the cue carrier, walked against itself — nine cues raised, eight answered, one left open  |
| `69a638d3f3` | 2026-08-09 | 43 | reconcile(generator+prompts): the reading list can no longer omit what the ritual names |
| `6aa23c3f3b` | 2026-11-03 | 66 | floor+loop: the watcher delivers the message — the woken thing's body rides the wake, the role defau |
| `6ada1edf7c` | 2026-07-27 | 53 | floor: session-start surfaces a missing or stale commit hook — .git/hooks is never cloned, so a re-c |
| `6d1adf8238` | 2026-08-26 | 32 | tool: cue untraced workflow fulfilment |
| `6d3aa819e7` | 2026-08-22 | 299 | framework: F5 — adapter duplication collapses into project_hook_emission, byte-identical |
| `6de8474be2` | 2026-09-08 | 95 | floor: the stale-open-conflict Info both specs promised, and the hold marker on conflicts |
| `6e8c9ab5b7` | 2026-08-23 | 42 | framework: F8c probes — and the boundary-terms adder they exposed |
| `70aa7b1883` | 2026-08-11 | 130 | challenge: Codex accepts ports and reopens shared runtime gate |
| `75cf830e04` | 2026-09-24 | 458 | session-end: build reusable Codex Cloud workspace setup |
| `7d0039bac4` | 2026-07-28 | 18 | floor: imports-check summary states coverage, never assurance — stale/fresh/withdrawn counted separa |
| `81b24e07f4` | 2026-07-27 | 39 | feat(scaffold): domains are born with a disclosure boundary — local .boundary-terms from template +  |
| `89d1e7ad72` | 2026-08-18 | 218 | build: guarded publication — Phase 2 of cowork-adapter |
| `8c52a72349` | 2026-10-05 | 18 | spec: change-reconciliation 1.6 → 1.7 — The Walk Runs On Detection; The Driver Names The Residue; or |
| `8d3a635f49` | 2026-09-23 | 181 | build: the between-sessions band gets its actor — a loop heals its own dropped turn, the cue raise i |
| `8d51b6f746` | 2026-09-15 | 98 | build: the scaffold asks for its harness — or refuses with the list — and never chooses for you |
| `903084daf4` | 2026-08-06 | 14 | phase-0(assistant-register): leg 2 findings — the shape passed, the delivery did not |
| `927693f572` | 2026-08-30 | 123 | floor(membrane): the route is proven end-to-end — three defects between the grant and the first read |
| `99327652af` | 2026-10-30 | 166 | workflow+evals: the operator's evidence-led traceability loop is a workflow-definition (eval-cycle), |
| `9ab0820205` | 2026-08-23 | 82 | framework: F8b — two review-9 survivors promoted, two declined on the record |
| `9c968df2a9` | 2026-07-27 | 175 | floor: mdllm boundary — disclosure-boundary check over staged additions, staged filenames, commit me |
| `9e28a4c219` | 2026-08-19 | 33 | reconcile: close adapter foundation public surface gate |
| `9f0cc58ce6` | 2026-11-10 | 523 | floor+decision: vault-map — a generated map folder beside the workspaces for markdown-vault tools, a |
| `9f506ee30d` | 2026-10-16 | 75 | harness: the commit gate runs where the commit lands — a session committing in a nested workspace is |
| `9fbe20fba3` | 2026-08-02 | 282 | floor: calc reads the body table (plan Phase 2) |
| `a14b0c3f94` | 2026-08-20 | 17 | reconcile: seal v3.33 transaction-integrity doctrine |
| `a1924b6f46` | 2026-08-08 | 281 | feat(porch): the transport swap lands — mcp-serve --http serves the same face over Streamable HTTP ( |
| `a86e328bc2` | 2026-09-24 | 161 | "feat:add-openclaw-domain-admission-gate" |
| `ae4e61d0ba` | 2026-10-05 | 229 | floor+harness: the gate demands the walk, not a verdict — cues --staged --raise prefills the dependa |
| `b33f6b4244` | 2026-08-22 | 90 | framework: F5 probe existence-guards — the sprint's one deliberate byte change |
| `b38a62f69e` | 2026-09-22 | 79 | build: a watch watches a run — mdllm watch --run, and the draft corrected by building it |
| `b7df2830ff` | 2026-10-21 | 111 | floor: the README's install pin is generated from the release record — it can no longer lag a releas |
| `b8480b45bd` | 2026-08-11 | 251 | repair: v1.6 return package — service-facing dependencies become declared ports (ShortcutPort, Scaff |
| `baa2320a6c` | 2026-09-26 | 331 | build: a clone that cannot see its history says so — and estate-sync heals it |
| `c10c5a1b73` | 2026-08-23 | 131 | framework: F8a check leg — the catalog and the routing table stop drifting silently |
| `ca958854c9` | 2026-08-21 | 35 | build: corpora validate concurrently over one warmed view (F13) |
| `d1d949420a` | 2026-10-18 | 259 | floor: the session-start digest lands whole on the hook channel — a 9,800-character startup-context  |
| `d492283f84` | 2026-10-05 | 290 | floor: mdllm cues --staged — the gate's question for the commit in hand; a cue raised today covers t |
| `d727e3d4c9` | 2026-08-02 | 48 | floor: validate re-runs every declared derivation (plan Phase 4) |
| `d7e6b8d8f9` | 2026-10-27 | 121 | floor+plan: silence is distinguishable from death — the dispatcher's quiet is one line at every sess |
| `d82db7b0a8` | 2026-10-31 | 144 | floor+spec: a conversation has a turn budget — 120 turns read from the record, a line and a ring at  |
| `d98ce0b56a` | 2026-08-18 | 142 | build: contract emission — Phase 1 of cowork-adapter |
| `ddd17d930f` | 2026-08-02 | 14 | floor: the stable-staleness check counts modifications, not additions (--diff-filter=M) — a stable t |
| `e4b639f50c` | 2026-11-06 | 257 | harness: project the reconciliation and reckoning gate into Codex |
| `e5de9fa408` | 2026-10-20 | 83 | floor+spec: the-reckoning Phase 4 — retention is promotion; scans 5-7 read the reckoning; one hold f |
| `e6ae01da86` | 2026-10-17 | 58 | harness: /orient — the session-start emission lands whole and the walk gets a typed pull (session-st |
| `e8554eacb6` | 2026-10-05 | 322 | harness: the pre-commit lifecycle moment — a gate that refuses the agent's commit until the cue is o |
| `e870acd240` | 2026-11-03 | 208 | floor+spec: a note on a held ticket rings its addressee — the watch keys the things at its role's st |
| `f2da8b72c9` | 2026-10-28 | 284 | floor+conflict: the measurements are the floor's — estate-check --health — and the gate question is  |
| `f9be3fbc42` | 2026-08-21 | 10 | reconcile: the precommit composition walked through its dependent surfaces |
| `fa8211d9f5` | 2026-08-02 | 127 | floor: calc reaches the corpus, and the quarantine law becomes mechanical (plan Phase 3) |
| `fab160fb90` | 2026-08-01 | 19 | floor: register the reserved prompt contract (inputs/outputs/bound_to) in CORE_FIELDS — a domain ado |

## Rejected fixes

| fix | reason | old-side | moved | blank | blamed |
|---|---|---|---|---|---|
| `477afc43e9` | introducing commit size outside 10..600 changed lines | 2 | 0 | 0 | 2 |
| `ff7e8d61f1` | no blamed lines (pure additions) | 0 | 0 | 0 | 0 |
| `5d9987f726` | no commit holds >= 60% of blamed lines | 12 | 5 | 0 | 7 |
| `58212ce776` | no commit holds >= 60% of blamed lines | 39 | 1 | 0 | 38 |
| `cd001d6066` | introducing commit size outside 10..600 changed lines | 1 | 0 | 0 | 1 |
| `38ab1d8643` | no commit holds >= 60% of blamed lines | 2 | 0 | 0 | 2 |
| `e0bc244da5` | no blamed lines (pure additions) | 0 | 0 | 0 | 0 |
| `ebad3d5df4` | no blamed lines (pure additions) | 0 | 0 | 0 | 0 |
| `5701f04f8e` | introducing commit size outside 10..600 changed lines | 11 | 0 | 0 | 11 |
| `2da4d17bb7` | no commit holds >= 60% of blamed lines | 6 | 0 | 0 | 6 |
| `855b6786a0` | no commit holds >= 60% of blamed lines | 2 | 0 | 0 | 2 |
| `d5e281be59` | introducing commit before 2026-07-01 | 2 | 0 | 0 | 2 |
| `fe0c091eea` | only moved or blank lines | 6 | 6 | 0 | 0 |
| `fbe7b52128` | introducing commit size outside 10..600 changed lines | 26 | 7 | 0 | 19 |
| `2ede668338` | no commit holds >= 60% of blamed lines | 137 | 53 | 4 | 80 |
| `3017f64f41` | no commit holds >= 60% of blamed lines | 15 | 3 | 0 | 12 |
| `1afe28390a` | no blamed lines (pure additions) | 0 | 0 | 0 | 0 |
| `3c41f91b5f` | no commit holds >= 60% of blamed lines | 8 | 0 | 0 | 8 |
| `ae5b5bf63c` | introducing commit size outside 10..600 changed lines | 1 | 0 | 0 | 1 |
| `b82061fd3f` | no commit holds >= 60% of blamed lines | 50 | 21 | 0 | 29 |
| `f7acffd3d2` | no commit holds >= 60% of blamed lines | 32 | 17 | 1 | 14 |
| `27b072371d` | no commit holds >= 60% of blamed lines | 46 | 0 | 2 | 44 |
| `905c91413b` | introducing commit before 2026-07-01 | 1 | 0 | 0 | 1 |
| `f512b065b1` | introducing commit is a refactor | 8 | 0 | 0 | 8 |
| `4e1ad73df5` | introducing commit is a refactor | 3 | 0 | 0 | 3 |
| `1c4f9ac4d7` | introducing commit is a refactor | 1 | 0 | 0 | 1 |
| `738c891c4b` | introducing commit is a refactor | 1 | 0 | 0 | 1 |
| `4f7fcd5c1e` | no commit holds >= 60% of blamed lines | 6 | 0 | 0 | 6 |
| `58759211b4` | no commit holds >= 60% of blamed lines | 22 | 0 | 0 | 22 |
| `ea2a35260e` | no blamed lines (pure additions) | 0 | 0 | 0 | 0 |
| `86d5613023` | no commit holds >= 60% of blamed lines | 10 | 1 | 0 | 9 |
| `7d1fe6edbb` | introducing commit before 2026-07-01 | 3 | 2 | 0 | 1 |
| `25739586ca` | introducing commit before 2026-07-01 | 1 | 0 | 0 | 1 |
| `98f86c1244` | no blamed lines (pure additions) | 0 | 0 | 0 | 0 |
| `4121b134f4` | introducing commit before 2026-07-01 | 1 | 0 | 0 | 1 |
| `fd95541773` | introducing commit before 2026-07-01 | 3 | 0 | 0 | 3 |
| `45caef7747` | introducing commit before 2026-07-01 | 1 | 0 | 0 | 1 |
| `c29f3293b7` | introducing commit before 2026-07-01 | 1 | 0 | 0 | 1 |
| `769e6e71ad` | introducing commit before 2026-07-01 | 8 | 5 | 0 | 3 |

## Dropped by the tighter fix-subject match

| commit | touches scope | subject |
|---|---|---|
| `038d084b26` | no | fix-openclaw-current-agent-schema |
| `ae9d598775` | no | Fix-domain-topic-creation |
| `da1eba90f6` | no | fixture(explorer): the public estate now carries references, and the guide describes the increment |
