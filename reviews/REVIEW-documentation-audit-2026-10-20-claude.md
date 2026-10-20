---
id: review-documentation-audit-2026-10-20-claude
type: artifact
status: stable
authorship: model-session
version: 1.0
created: 2026-10-20
origin: synthesised
exposed: false
tags: [review, documentation, audit, readme, onboarding, vocabulary, records, model-authored]
linked_things:
  - id: review-critical-comparison-2026-10-17-claude
    relation: references
    notes: "That review found the documentation overstated and its vocabulary private; this audit reads the whole documentation surface after the 2026-10-18 positioning fixes, and finds what they did not reach."
  - id: glossary
    relation: informs
    notes: "One row is wrong (porch) and the words that failed the first non-author operator — session, refresh — have no row."
  - id: limitations-guide
    relation: informs
    notes: "Says 'there is no index'; mdllm index exists — it means no search index."
  - id: first-hour-guide
    relation: informs
    notes: "Routes the newcomer to an install pinned seventeen releases back, then prescribes features that install does not contain."
  - id: operator-guide
    relation: informs
    notes: "Written as a v2→v3 delta; carries Explorer claims that are false while it is parked, and adapter verification narrative."
  - id: change-reconciliation-specification
    relation: informs
    notes: "Holds two incompatible models of who walks and who rules; the 2026-10-05 inversion was layered on, not rewritten in."
  - id: session-start-hardening
    relation: informs
    notes: "The generated workspace contract still runs the orient walk eagerly at t=0; no live workspace has the /orient command."
---

# Documentation audit — the shape is buried under the record

*Authorship: written by a model session on 2026-10-20 at the operator's request ("a holistic analysis of the whole documentation"). A Claude Opus 5.5 coordinator inventoried the surface mechanically and dispatched five read-only audits — the front door, the published guides, the agent entry contract, the specification corpus, and the periphery (changelog, evals, explorer, integrations, evidence, reviews). The coordinator re-checked every high-harm claim against the repository at HEAD 46ef499 before writing; the checks are marked ✓. No human has reviewed it.*

## Verdict

The documentation is not short of truth; it is short of shape. Eighty files, about 19,500 lines and 209,000 words, with no broken relative links — the mechanical surface is sound. What a reader meets is a corpus that documented itself while it was being built: release archaeology, incident narratives and verification records sit inside the guides and the contract, and the guides restate one another until the copies disagree. The 2026-10-18 positioning fixes (the README lead, the glossary, limitations, the prior-art section) corrected the claims; they did not touch the structure that keeps generating the problems.

Four things are actively **wrong** and harm a reader today: the published install hands a newcomer a framework seventeen releases old; every live workspace's generated contract contradicts the framework's own session start; the specification that governs the walk gate holds two incompatible models of who decides; and parked or paused products are presented as live. Two things are **missing**: nobody anywhere sees a whole session from start to finish, and the vocabulary wall still stands where it stopped the first non-author operator. Two things are **too much**: the entry contract is three times the size its harness advises and is inherited by every nested workspace, and the README is about 45% shape. One thing is **unfindable**: the record layer — changelog, evidence, reviews — has no index and is not linked from the front door.

The root cause is single: the outward surface has no floor. The specs are validated; the README, the guides' status lines, the install pin, the counts and the generated workspace contract are not, so each drifted at the rate the framework moved — seventeen releases since August.

## The numbers

| Measure | Value |
|---|---|
| Documentation files (excluding things/, reviews/, evidence/, templates/) | 80 files · 19,493 lines · 208,858 words |
| Broken relative links | 0 |
| README | 435 lines · 5,129 words · ~45% shape, ~33% dated record, ~22% copies of agent inventories |
| Tier 0 (`mdllm tokens`) ✓ | 16,177 tokens — AGENTS.md 10,405, kernel.md 5,772 |
| AGENTS.md | 315 lines against Claude Code's advised 200; ~33% contract, ~35% restated, ~14% record, ~18% explanation without instruction |
| Specification corpus | ~95,000 words; ~18,000 (19%) is duplication or history that could leave |
| "domain" vs "workspace" in outward docs | README 78:3 · operator-guide 72:9 · framework-map 50:0 · estate-mechanics 32:2 |
| Live workspaces with the `/orient` command ✓ | 0 of 15 |
| CHANGELOG | 69 entries; v3 entries average ~400 words; one git tag in the repository (`v2.9-pre-floor`) |

## Twelve findings, ranked by harm

**Wrong — tells the reader something false**

1. **The install is seventeen releases old.** ✓ README:233-287 pins v3.32.0 (`c863633`, 2026-08-19); that commit has no `templates/commands/orient.md`, no `docs/glossary.md`, no `reckon.py`, no `seat.py`. first-hour:62-70 sends the newcomer there, then first-hour:226-231 tells them to make `/orient` "the first thing you type". README:5 promises the site and the repository are "never two versions"; following the instructions exactly produces the mismatch. README:278's "the next release contains the same exact pin" has been stale for seventeen releases. Nothing checks it, because README.md is outside the floor (`NON_THING_FILES`, `model.py:302`).

2. **Every workspace's contract contradicts the framework's session start.** ✓ The generator `domain_kernel.py:88-89` writes "Run this before responding to the user's first request … resist until these are done", then steps 4-6 run the orient walk eagerly — while AGENTS.md says the walk is "explicitly invoked, not automatic" and the digest is consumed, never recomputed. 0 of 15 live workspaces have `.claude/commands/orient.md`; the hooks block describes session end without the reckoning close or the publication-debt report; 14 of 15 cite `autopush-moves-the-deliberate-act`, which is superseded; the template says "domain" twenty times and "workspace" never; `TIERS` (`repo.py:59-67`) has no `docs/` entry, so no workspace can route to the glossary or the limitations. The root moved in October; the estate did not.

3. **change-reconciliation holds two models of who decides.** ✓ The 2026-10-05 inversion — the agent walks on detection, the operator rules only on the residue — was layered onto the old text without rewriting it. New: :88-94, :180, :450. Old, still standing: :126 "The cue *verdict* is the driver's", :136 the question "waits … until a human answers it", :261, :354 "the Walk is human-backed", :453-455, :511, :535. It spreads: thing.md:96 and README:163 carry the old model. An agent reading the spec can relapse into asking permission before walking — the exact failure the ruling corrected. One role has five names across the corpus: driver, operator, human, expert, seat.

4. **Commit and publication duties contradict each other on the Tier-0 path.** ✓ orchestration:152 says the hard hooks are on regardless of configuration and :185 "do not complete the response without this step"; git-workflow:729 offers `autocommit: false` (the agent stages and waits) and :261 "Agent stages, human commits". git-workflow:70 calls the commit "publication" against its own kernel. The scaffold step in orchestration's kernel block — therefore kernel.md:94 — lists "create remote + push", against the fail-closed publication rule.

5. **Parked and paused products are presented as live.** Explorer has been parked since 2026-09-02, yet README:16-17 says "Windows has an installer preview", README:114 and operator-guide:178-179 (on the site) offer to "install the read-only Windows preview", and installation-guide:16 asks for an `Installer-0.4.1.exe` that exists in no release (the code is 0.4.3). No Explorer document says "parked". operator-guide:189-191 says the service stops after thirty minutes; explorer/README:106-107 says there is no timeout. The onramp is "being built" in first-hour:99 and operator-guide:199-202 while the plan is paused. The Codex Cloud adapter never says both its plans are paused. The OpenClaw README's install command names `@markdownllm/openclaw-adapter@0.1.0`, which the public npm registry does not have ✓ (404).

6. **Small contradictions everywhere a number or a list was copied.** README's spec table misses three specs and calls scalability-guide "tens to thousands" ✓; scalability-guide itself says "50 to 5,000" (:60) and "10,000+" (:203) beside "reconsider past 1,000" (:271) ✓ — and AGENTS.md calls it "the measured document"; README's seven principles diverge from AGENTS.md's nine; thing.md:171 still lists `related` ✓, the very incident AGENTS.md cites as the reason enums are no longer copied; AGENTS.md:101 restates three character counts two lines before :103 says restated numbers drift; estate-mechanics says three radii (:25) and four (:221-232); first-hour and operator-guide say seven scenarios and hold eight; framework-map's View 1 label says 32 while its own accDescr says 34; kernel.md:17 says "23 Tier 1+2 specs", hard-coded in `kernel_gen.py:28` ✓, against 26 in the catalog; the glossary's *porch* row (written 2026-10-18 in this session) defines it as the import, where interface.md:278 defines it as the producer's `mcp-serve` ✓.

**Missing — what the reader needs and does not get**

7. **Nobody sees a whole session.** first-hour gives a session eight lines with no beginning and no end; `/orient` appears only in a footnote; no guide's narrative reaches `/end-session` or the close; the walk gate — the mechanism the README now leads with — appears in no scenario anywhere. The only plain-language walk of a refused commit in the whole surface is limitations:75-88. The README has no "who is it for" and no picture of use.

8. **The vocabulary wall still stands.** By README:27 a newcomer has met floor, walk, harness, estate, substrate, kernel and digest. The glossary has no row for *session* or *refresh* — two of the four words the first non-author operator named as never landing — nor for substrate, membrane, radius, adapter, seal or publication debt; it has no per-term anchors, so no guide can link a word at first use; operator-guide and estate-mechanics contain no glossary link at all; the site lists the glossary last, with no navigation entry. And a blanket domain → workspace rename would collide: "workspace" already means the folder opened in the harness (README:57, first-hour:116, 160-162).

**Too much — record and copies crowding out shape**

9. **The entry contract is three times its advised size, and it is inherited.** AGENTS.md is 315 lines and 10,405 tokens; about a third is instruction. Root CLAUDE.md imports it, so every Claude Code session opened in a nested workspace also loads the framework's contract — 14-19k tokens and 460-640 lines of entry files before the kernel — and CLAUDE.md then tells the agent to disregard what is already in context. The two newest behavioural gates (the walk gate and the reckoning close) exist at Tier 0 only in AGENTS.md prose; kernel.md, the "rules without rationale", carries dated anecdotes (L46, L54, L66, L82). A target of ~110 lines takes Tier 0 from 16.2k to about 8.7k tokens, for every session in the estate.

10. **The guides and specs carry the record.** The README is about a third dated record (Explorer status, the Desktop freeze, 70 lines of Codex verification narrative at 289-358 under which the universal next step "open the folder, tell it what you want" is nested, the June eval numbers at 220 against the no-write-ups direction). operator-guide is written as a v2 → v3 delta for readers who never met v2, and tells the multi-repository story a third time alongside estate-mechanics §2 and framework-map View 5. The specs repeat the disposition rules five times and the session-end steps six; change-reconciliation, universal-workflow, workflow-state, interface and standing-watch open with history or sixty lines of frontmatter before saying what they are. Status labels mislead both ways: validate.thing, belief-revision and retrospective are `stable` while changing structurally; scalability-guide is `stable` and self-contradictory; change-reconciliation, provenance and derived-index are `draft` while enforced in every commit.

**Unfindable**

11. **The record layer has no index and no door.** The README links none of CHANGELOG, `reviews/`, `evidence/`, the OpenClaw integration or the Codex Cloud adapter. CHANGELOG entries average ~400 words with no Added/Changed/Breaking structure, and its own header prescribes `changelog --since <last-version-tag>` in a repository with one tag. `evidence/README.md` describes an adoption case-study plan, not the 36 harness records the folder holds; the compatibility matrix there is stale. `reviews/` has no index, file names still say "independent" and "external", nothing marks a review superseded, and the seven `explorer/reviews/` files are unlabelled.

12. **Privacy, low.** No people's or clients' names were found. "QMS" — the private regulated workspace's shorthand — appears at README:302, 365 and operator-guide:359 ✓; the established substitution is "the regulated deployment". A tracked review (`REVIEW-independent-2026-08-11-codex.md`) carries twenty absolute links to the author's user-profile path, which also break for every other reader; two Explorer evidence JSON files carry the same path.

## Root causes

1. **The outward surface has no floor.** README.md and the guides' status lines, counts, install pin and inventories are hand-maintained and unchecked; the framework that mechanises every other drift lets these drift freely.
2. **The framework documented itself while it was being built.** Each arc wrote its record into the guide it was changing — "since 3.41.0", "until 2026-10-05 this said", "observed live on 2026-08-17" — because there was no rule that a dated sentence belongs in a record.
3. **One rule, many copies.** The session-end steps, the disposition rules, the autopush rule, the hook cap and the spec inventory each live in three to six places; a change lands in one.
4. **The workspace contract is code, and the code was not moved with the root.** `domain_kernel.py` writes every workspace's entry file; October's session-start, reckoning and wording changes reached the root's AGENTS.md and not the generator.

## The target shape

- **README (~150 lines).** What it is in three sentences; who it is for and who it is not (→ limitations); what a session looks like in six lines — you say, the agent writes, the floor refuses, you rule, it commits; one ten-line record; the layout as one small tree; get started — a release pin generated at release, then "open the folder and say what you want", then first-hour; which agent tools work, one status word per row linked to evidence; six words you will meet (→ glossary); what is claimed and what is not (the hypothesis stated as one); read next; a short FAQ that includes "why not `CLAUDE.md` plus a notes folder?". Spec inventory, principles and templates point at AGENTS.md and CONTRIBUTING instead of copying them.
- **AGENTS.md (~110 lines, Tier 0 ~8.7k tokens).** Identity and the standing truth; the launch route in three lines with every example as `mdllm <cmd>`; session start (estate-sync, `/orient`, the owed kernel read, pinned reads); one generated when → file load map replacing both the routing table and the catalog; on output — commit, walk gate, reckoning close, scaffold, `/end-session` — as pointers; the framework-work checklist; the generated types block; one line sending principles, prior art, catalog and history to README, limitations and CHANGELOG.
- **The site's reading path.** Start: limitations, first-hour (ending with one whole session — `/orient`, the work, a refused commit, `/end-session`), glossary. Operate: operator-guide as scenarios plus "what is yours", the toolbox on its own page, one merged "Several workspaces" page. Reference: calculation reference, framework map (Views 1-3). Not on the site: `docs/plans/` moves to `things/`.
- **The records rule.** A dated sentence in a guide is a defect unless it is a link to a record. CHANGELOG: three to eight bullets per release under Added / Changed / Breaking / Upgrade, an optional paragraph of why, every version tagged. `evidence/`: every verification narrative, with a generated index. `reviews/`: authorship, the commit reviewed and `superseded_by`, with a generated index. Status lines in guides derived from the owning plan's frontmatter so they cannot drift.

## Work packages, in dependency order

| # | Package | Effort | Needs the operator? |
|---|---|---|---|
| 1 | **Correctness pass** — Explorer parked banners and README/operator-guide claims; onramp "paused" in first-hour and operator-guide; "tens to thousands" ×3 and scalability-guide's self-contradiction; thing.md `related`; the glossary's porch row plus session, refresh, substrate, membrane rows and anchors; the counts (radii, scenarios, 32/34, 23 specs); the OpenClaw install line; README:220's eval link; the Copilot orient prompt template; site navigation for glossary and limitations; "QMS" substitution; the excluded-results index rows | S–M, one session | No |
| 2 | **Install route** — re-pin to the current release with recomputed installer hashes, and make the release ritual regenerate or gate the pin | S + a release step | Yes: pin now, or generate at release, or a plain tagged clone; version tags are publication |
| 3 | **Workspace contract** — `domain_kernel.py` to the `/orient` model, the reckoning close and publication-debt report in the hooks block, the superseded citation out, the launcher route, `docs/` in `TIERS`, outward wording; then offer each workspace a refresh that projects `/orient` | M + an estate refresh | Refresh is offered per workspace, never swept |
| 4 | **change-reconciliation rewritten as one model**, and git-workflow/orchestration's commit-and-publication contradictions resolved; one name for the human role | M; walks owed | Ruling: which word for the human role |
| 5 | **README to shape** and **first-hour ending in one whole session**; newcomer path made linear | M | Ruling: README depth |
| 6 | **AGENTS.md to ~110 lines** and kernel blocks stripped of anecdote | M; walks owed | No (within the 2026-08-21 handover) |
| 7 | **Spec consolidation** — history out (~5.5k words), duplication out (~10k), one home for the reckoning and disposition, statuses made truthful, universal-workflow and operating-model merged, thing-lifecycle to a paused plan | L; many walks | Ruling: merges and the reckoning split change what a spec is |
| 8 | **Record layer** — CHANGELOG format and tags, generated `evidence/` and `reviews/` indexes, operator-guide split (toolbox page; adapters to evidence), estate-mechanics merged | M–L | Tags are publication |
| 9 | **Mechanise the outward floor** — README and guide status lines, counts and the install pin derived or gated by `mdllm docs` / coherence; the stable-but-changed window widened | M | No |

Package 1 is safe today and removes every false statement a reader can act on. Packages 3 and 4 matter most to agents; 5 and 6 matter most to people; 9 is what stops the next seventeen releases from undoing the rest.

## Rulings this audit cannot make

- **The word for the folder opened in the harness**, before any outward domain → workspace rename — otherwise "open the workspace as its own workspace".
- **The word for the human role** (driver, operator, human, expert, seat → one).
- **README depth**: shape only (~150 lines), or trim the record only (~250).
- **The install route**: re-pin now, generate at release, or replace the verified install with a tagged clone.
- **Spec consolidation scale**: whether the reckoning becomes its own spec, whether universal-workflow and operating-model merge, whether thing-lifecycle retires to a plan.
