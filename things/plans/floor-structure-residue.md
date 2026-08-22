---
id: floor-structure-residue
type: plan
status: in-progress
version: 1.1
created: 2026-08-20
priority: medium
tags: [clean-architecture, solid, tests, ci, perimeter, refactor, review-residue]
linked_things:
  - id: independent-substrate-review-2026-08-20-claude
    relation: derived-from
    notes: "The review that found each item; its clean-architecture section is this plan's specification."
  - id: a-same-builder-check-is-blind-to-a-self-contradictory-builder
    relation: implements
    notes: "The fitness suite's curated allowlist is that blindness in the one place that checks the code itself."
  - id: srp-extraction-is-tier-promotion
    relation: references
    notes: "The god-module and monolith items are that pattern's next instances."
  - id: portability-claims-need-execution-tests
    relation: implements
    notes: "A single-platform CI beneath the most platform-sensitive machinery is the insight unapplied to the substrate's own pipeline."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "Substrate code changes are read against that governance surface before they are written, not retrofitted after."
  - id: mechanical-coherence-checks-backlog
    relation: references
    notes: "Any new mdllm coherence check named here belongs there, under its suppression-list gate — this plan proposes none of its own."
  - id: cumulative-drift-is-invisible-to-per-change-walks
    relation: supports
    notes: "The perimeter restatements below are fresh evidence for the razor: they sat outside every individual blast radius and were found by a cold read."
  - id: a-declaration-is-inert-until-its-mechanism-is-current
    relation: implements
    notes: "Item 7's generalisation: the estate's hooks were three releases stale, so a current autopush declaration would have been unreadable by every installed byte. The item is the tool-side repair; the insight is the rule."
---

# Floor Structure Residue

Structural and perimeter debt named by the 2026-08-20 independent review. None
of it is a behavioural defect — the floor's guarantees hold. Each item is a cost
the *next* change pays: a duplicated adapter the fourth harness inherits, a gate
that does not cover new modules, a monolith that blocks its own decomposition.

Ordered by leverage, not by size.

## Structure

1. ~~**Invert the fitness suite's vendor gate.**~~ **Landed 2026-08-22**
   (floor-sprint-2, commit 4cb9ca9): neutral by construction over everything
   outside `adapters/`, exceptions declared with reasons and
   exactness-tested (a stale exception fails the suite); sync.py's one
   incidental vendor word reworded rather than excepted.
2. ~~**Collapse the duplication between the two project-bound adapters.**~~
   **Landed 2026-08-22** (commit 6d3aa81): `adapters/project_hook_emission`
   owns the converged shape as plain parameterised functions — no base
   class; goldens unchanged proved byte-identity.
3. ~~**Move the hook byte contract out of the birth module.**~~ **Landed
   2026-08-22** (commit fb587a1): `hook_contract.py` owns candidate policy,
   sh fragment, hook bodies, path resolution and contract rendering;
   doctor/session/runtime/adapters consume the leaf, and the fitness
   layering test pins the deleted edges. `LAUNCH_RESOLUTION_SECONDS` stayed
   with its timing family in harness_ports (recorded deviation).
4. **Extract a shared test fixture module, then split the monolith.**
   **Half landed 2026-08-22** (commits 9ed15a2 → 9726711):
   `corpus_harness.py` extracted (cross-file test imports gone), then
   estate-sync+autopush, membrane, and session-gate lifted along their
   banners — monolith 3601 → 2675 lines, collection count 696 invariant
   throughout. Remaining banner sections (mcp-serve, imports-check,
   quarantine flip, disclosure boundary, candidates, retrospective-cadence,
   terminal statuses) stay here for later lifts under the same invariant.
5. **Prune during the worktree walk.** ~~Worktree-mode listing enumerates the
   entire tree before exclusions apply, so an interactive command in a working
   checkout pays a walk proportional to everything nested beneath it rather than
   to the corpus. The hook path is index-native and unaffected; the cost lands
   on the commands an operator runs by hand.~~ **Landed 2026-08-21** — commit
   `3017f64` prunes version-control internals, virtualenvs and build caches
   during the walk (and made WORKTREE and COMMIT modes agree on the logical
   corpus); the same session's follow-up removed session-start's redundant
   rescans and history re-walks, switched the strict YAML boundary to the
   libyaml C parser where compiled in, and parallelised the estate-sync repo
   walk. Framework-root session-start: 67.8s → ~2s measured.
6. ~~**Widen the CI matrix, or say why not.**~~ **Both legs landed
   2026-08-22** (commits 1e400e5, ef07edc): the limitation recorded in the
   suite README + workflow header, then windows-2025 joined the matrix.
   *Post-publication (2026-08-22): the Windows leg's first run failed at
   interpreter setup — 3.12 has no win32-x64 build past 3.12.10 — repaired
   with a per-OS pin in `30ecef1`. Windows CI still has **zero test
   evidence**; the repair is publication-gated too. Not re-opened as an
   item: the matrix decision is made and the remaining work is one
   observation.*
7. **Old-format mdllm hooks are unreachable by the tool.** Found
   2026-08-22 during the estate-wide autopush rollout: every domain's hooks
   predated the `MDLLM_ROUTE` format, and `_managed_for_repo` requires both
   the `# mdllm` marker *and* a matching embedded route — so the tool
   classified thirteen sets of its own stale hooks as operator hooks.
   `install-hook` refuses to replace them and `--uninstall` refuses to
   remove them (same ownership test), and there is no `--force`. The only
   route was hand-deleting hook files after verifying the marker. The
   refusal is right — protecting operator state is the point — but a
   framework that regenerates its own hooks needs a sanctioned upgrade path
   for its own old formats: recognise known historical hook bodies by
   content (the adapters' `legacy_definitions` pattern, applied to git
   hooks) and offer `--refresh-legacy`, refusing only genuinely unknown
   bodies. Until then, a stale-format domain silently loses every hook leg
   added since its install — here, the entire autopush leg.
8. **Decide the Node 20 action bump.** GitHub is deprecating Node 20, which
   both pinned actions run on (`actions/checkout` v4.2.2,
   `actions/setup-python` v5.6.0); the 2026-08-22 run carried the warning.
   Newer majors run Node 24, but bumping means moving **pinned immutable
   trust roots** — the workflow's own comment calls the actions download
   service a mutable trust root, so a SHA bump is a deliberate supply-chain
   decision, not maintenance. Either bump both to reviewed SHAs, or record
   why the deprecation is being carried and until when. Added 2026-08-22.

Smaller, same family: two copies of the staged-atomic-write primitive; a
diagnostic that recovers its own floor's result by matching report prose rather
than a structured fact; two adapter inspectors that classify by resemblance to a
path string; dependency pins restated by hand in a bundle template beside the
file that owns them. ~~Added 2026-08-21 (measured during the perf pass): the
emitted sh interpreter-resolution fragment probes file-path candidates by
spawning `timeout` + python even when the path cannot exist.~~ **Landed
2026-08-22** (commit b33f6b4, riding the F5 regeneration as predicted):
`[ -x ]` on file candidates, `command -v` on PATH names — measured
348→273ms per invocation at the root, 514→311ms in a venv-less domain
repo; the change also exposed and fixed live-computed legacy recognition
data (the v1 fragment is now frozen at `adapters/legacy/sh-resolve-v1.txt`).

## Perimeter

Hand-restated facts that a per-change walk did not reach. The
2026-08-20 dark-region reconciliation closed several; these survived it:

- the calculation reference still states an unevaluable derivation is *always* a
  warning, which strict mode has made an Error (its sibling lexeme claim was
  corrected in that same walk);
- this repository's own installed session-closing commands still teach
  publication as default-on, which the templates already corrected — the
  framework's own ritual currently teaches reversed doctrine;
- the decision template and its worked example still teach abbreviated pins
  against the full-commit rule.

These are cheap to correct and are also the standing argument for the
perimeter-currency check: a cold read found them, and a cold read is the
instrument this class is currently protected by.

## Done when

- [x] The fitness gate covers by default and excepts by declaration.
      *(2026-08-22, floor-sprint-2 F3, commit 4cb9ca9 — with a
      stale-exception exactness test so the list cannot rot.)*
- [x] Items 2–5 are landed or explicitly ruled not-worth-it, in writing.
      *(2026-08-22: 2 and 3 landed whole (6d3aa81, fb587a1); 5 landed in
      sprint 1 (3017f64); 4 half-landed — harness + three section lifts —
      with the remaining sections named above as later work under the same
      collection-count invariant.)*
- [x] The three perimeter restatements are corrected at their source surfaces.
      *(2026-08-21, floor-sprint-1 F1, commit 90f29d3: calculation-reference
      strict severity, the installed end-session command's publication
      doctrine, the decision template + worked example full-SHA pins.)*
- [ ] Items 7 (legacy hook upgrade path) and 8 (the Node 20 action bump) are decided — bumped to reviewed SHAs,
      or carried with a written reason and a date. *Added 2026-08-22 after
      the deprecation warning appeared in a real run; it is a supply-chain
      decision, so it stays open rather than being repaired in passing.*
- [x] Any check this work argues for is routed to the coherence backlog rather
      than built here. *(2026-08-22: sprint 2 proposed no new checks; the
      fitness-gate exactness test is a test-suite invariant, not an
      `mdllm coherence` check.)*
