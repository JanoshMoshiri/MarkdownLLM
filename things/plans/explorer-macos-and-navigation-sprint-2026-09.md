---
id: explorer-macos-and-navigation-sprint-2026-09
type: plan
status: in-progress
version: 1.4
created: 2026-09-01
priority: high
tags: [explorer, macos, navigation, memory, portability, release, sprint]
linked_things:
  - id: explorer-macos-support
    relation: supersedes
    notes: "Absorbs the platform work into the one candidate Aaron will actually evaluate, alongside the two operator-reported navigation corrections."
  - id: explorer-ui-increment-2026-08
    relation: references
    notes: "0.3.0 is the accepted behavioural baseline this sprint changes."
  - id: explorer-publication-readiness
    relation: complements
    notes: "Windows public signing remains its own gate; this sprint must not silently present a macOS wheel as a signed public-native release."
  - id: explorer-extraction-and-hosting
    relation: references
    notes: "Online hosting and repository extraction remain phase-two work and are explicitly outside this fast Mac handoff."
  - id: an-attestation-bound-to-a-whole-tree-hash-is-terminal-by-construction
    relation: informs
    notes: "The final evidence seal follows every code, documentation and packaging change; the sprint does not reseal intermediate candidates."
  - id: an-explanation-committed-to-a-specification-outlives-the-doubt-that-made-it
    relation: informs
    notes: "The Mac runtime premise remains a hypothesis until the actual Mac executes it."
  - id: a-test-anchored-in-source-text-fails-loudly-on-drift-and-silently-on-ambiguity
    relation: informs
    notes: "Any new platform mutation anchor must remain unique and must not multiply ambiguous source-text probes across the Windows and Mac launchers."
---

# Explorer macOS and navigation sprint (0.4.1 maintenance candidate)

## Outcome

Deliver one Explorer candidate Aaron can open through Claude Code against his
existing MarkdownLLM substrate and domains on macOS, containing both operator-requested
navigation corrections:

1. **Memory discovers the domain rather than naming four folders in code.** Every
   eligible first-level content folder beneath `things/` appears as a group.
2. **Related-document navigation works from every opening route.** A document
   opened from the left file tree can follow a rendered Markdown link or a
   resolved frontmatter reference without the URL and reader disagreeing.

The usable-today target is a framework-carried `tools/open-explorer.sh` route
that bootstraps the platform-independent Python package in an isolated user
environment, opens the browser and needs no remembered terminal command. A
double-click `.app`/DMG is a later delivery lane, but it is not allowed to block
Aaron's first use or the two corrections above.
Public native distribution is a later release gate because signing and
notarization require Apple credentials and a Mac build host.

## Current state, observed 2026-09-01

- Explorer is version `0.3.0`; its wheel declares `py3-none-any` and its runtime
  dependency is only PyYAML. Windows-only imports live behind the optional
  Windows desktop launcher.
- The product requirements already claim Python runtime support on macOS 13+,
  but no macOS runtime evidence has executed. The claim is therefore plausible,
  not yet proven.
- Aaron already has the latest MarkdownLLM substrate and at least two domains
  operating on a Mac. He does not have a Mac Explorer installation route.
- The Memory view showed only Retrospectives, Insights, Decisions and Conflicts
  while the selected domain actually contained twelve first-level `things/`
  folders with eligible Markdown, including plans, working documents, design
  specs, workflows and references.
- Live browser reproduction found that a related-file control updates the route
  from `adopt-hybrid-staging-flow` to `interim-code-review-control`, while the
  reader remains on the former document.

## Diagnosed causes

### Fixed Memory policy

The same four-folder map exists independently in
`collection_reader.py::_group` and
`confined_source_reader.py::_memory_group`. One copy chooses collection items;
the other computes the Overview count. Adding one folder to one map can already
make the count and the visible collection disagree.

The collection reader also compares a thing's frontmatter type to the singular
form of its folder name. That happened to approximate `insights` → `insight`,
but it is not a valid rule for emergent folders such as `working-documents`,
`requirement-specs` or mixed-type working areas.

### View identity used as reader identity

Tree selection correctly opens a standalone reader but deliberately leaves the
selected tab unchanged. Link and resolved-reference handlers later decide how
to open their target from `state.view`. If that tab is Memory or Skills, they
call the embedded collection reader even though the DOM now contains a
standalone reader. The route changes, the embedded target does not exist, and
the content remains visibly unchanged. Route restoration has the same ambiguity.

### macOS proof and confinement gap

The portable runtime has no known Windows dependency, but it has not been run
on macOS. In addition, the post-open confinement check implemented with
`GetFinalPathNameByHandleW` on Windows returns no final path on all other
platforms. macOS needs its `fcntl(fd, F_GETPATH)` equivalent before the existing
confinement requirement is honestly evidenced there.

## Scope decisions

### Memory discovery contract

- A Memory group is the **first directory immediately below `things/`** that
  contains at least one eligible `.md` or `.markdown` file at any permitted
  descendant depth.
- Every such group is included. Hidden, ignored, secret, unsafe, depth-exceeded
  and otherwise ineligible paths continue to be excluded by the existing shared
  eligibility and confinement policy.
- Empty directories are omitted: they contain nothing to read and are not
  represented by Git in the normal estate shape.
- A group label is derived deterministically from its directory name by turning
  hyphens and underscores into spaces and title-casing the result.
- Existing group order remains descending and item titles remain ascending.
  Disclosure state, counts, pagination, duplicate-ID warnings and malformed or
  missing frontmatter warnings continue to work.
- Folder name does **not** assert frontmatter type. The current mechanical
  singularisation/mismatch warning is removed because folder structure is
  deliberately domain-emergent.
- Group discovery and Overview Memory counts use one policy, not duplicate maps.
- The tab remains named **Memory** in this sprint. Its broader meaning can be
  reconsidered with evidence from use; renaming it now is unrelated scope.

### Related-document navigation contract

- Browser state gains an explicit document surface: `standalone` or
  `collection`. Tab identity remains the selected navigation tab; it no longer
  doubles as the reader-layout decision.
- File-tree and search openings select `standalone`; Skills and Memory item
  openings select `collection`.
- Rendered Markdown links and resolved frontmatter references preserve the
  current surface unless their own route explicitly declares another one.
- The hash route persists the surface so refresh, back and forward reproduce the
  same reader layout. A legacy route without it keeps the current compatible
  default: a Skills/Memory path opens in the collection, other paths standalone.
- A requested related path must update the route, visible document heading,
  context pane and tree selection together or surface a controlled error.

### macOS delivery contract

- **Immediate route:** carry `tools/open-explorer.sh` in the framework. Claude
  Code runs it from the framework root; the script validates macOS and Python
  3.10+, creates or refreshes an Explorer-only virtual environment beneath the
  user's Application Support directory, installs the current checked-out
  `explorer/` package, starts it against that framework root and opens the
  capability URL in the default browser. It requires no administrator rights.
- The launcher persists only its owned environment and a verified process ID.
  It never persists the capability URL, source-derived content or an Explorer
  log. `--stop` terminates only a process whose command line proves it is the
  Explorer instance for this framework root.
- **Revised 2026-09-05 by Janosh:** remove the 30-minute lease on all launch
  surfaces. Explorer stays available until explicitly stopped or the host/process
  exits. No browser expiry timer or activity heartbeat remains. Windows tray Exit,
  CLI interrupt and the Mac launcher stop/relaunch remain the lifecycle controls.
- Implement and execute the macOS post-open final-path check. Failure to obtain
  the opened path fails closed as `source_unreadable`, matching Windows.
- Record Python version, macOS version and CPU architecture in the Mac evidence.
  The platform-independent wheel avoids guessing Apple Silicon versus Intel.
- A native `.app`/DMG follows only after the portable candidate passes on the
  actual Mac. It needs a Mac build host, menu-bar lifecycle and single-instance
  design, `.icns`, clean install/upgrade/uninstall verification, and—before
  public download—Developer ID signing, notarization and stapling.
- Apple Developer membership is not assumed and is not a gate on Aaron's wheel
  handoff. An unsigned/unnotarized native bundle is not called publishable.

## Delivery sequence

The sequence tests the hardest external premise first but packages only once.

### I0 — Corrected candidate before scarce Mac time

- [x] Choose the agent-invoked portable launcher as the first Mac route and
      defer native packaging until a local Mac build host is available.
- [x] Complete the UI corrections, shared idle lifecycle and launcher before
      asking Aaron to spend time on an actual-host run.
- [ ] If the corrected candidate does not start on Aaron's Mac, retain its real
      diagnostic and return the run to modelling; do not patch by guesswork.

### I1 — Reconcile requirements, design and traceability

- [x] Amend `explorer/docs/requirements.md` for dynamic Memory groups, surface-
      stable related navigation, agent-invoked macOS launch and idle expiry.
- [x] Amend `explorer/docs/design.md` with the shared group policy, explicit
      document-surface state/route and macOS final-path boundary.
- [x] Add exact automated and human journeys to the test specification and
      traceability manifest before production changes.

### I2 — Dynamic Memory groups

- [x] Replace both static maps with one shared first-level `things/` grouping
      policy and make Overview counts consume it.
- [x] Remove folder/type singularisation while retaining real metadata issues.
- [x] Cover arbitrary folder names, nested files, empty/ineligible folders,
      pagination, ordering and count/collection agreement.

### I3 — Stable related-document navigation

- [x] Add explicit reader-surface state and route round-tripping.
- [x] Make body links and structural reference chips use that surface.
- [x] Cover tree→reference, tree→body-link, collection→reference, mode switch,
      refresh and back/forward in browser runtime evidence.

### I4 — macOS confinement parity

- [x] Implement `F_GETPATH` final-path recovery and fail-closed error handling.
- [ ] Exercise normal, symlink/rebinding and unavailable-path vectors on macOS;
      retain Windows and non-macOS behaviour.

### I5 — One candidate, one evidence pass

- [ ] Run the unit, contract, architecture, HTTP, safety and browser suites.
- [x] Run mutation and traceability verification required by the Explorer's
      current release process.
- [x] Build one final `0.4.0` wheel after all implementation and documentation
      changes; record its cryptographic hash and prove the launcher installs the
      same checked-out package contract.
- [x] Execute the launcher's non-Mac rejection and safe process-ownership paths
      locally; reserve successful macOS execution for Aaron's actual host.

### I6 — Aaron acceptance and handoff

- [ ] Aaron can ask Claude Code to open Explorer; the agent runs the tracked
      launcher against his existing substrate without editing domain files.
- [ ] He sees every populated first-level `things/` folder in Memory for an
      agreed domain and can open at least one formerly omitted group.
- [ ] From a file opened in the left tree while Memory is selected, a related
      reference and a valid rendered Markdown link each open their target visibly.
- [ ] Refresh and browser back/forward preserve the expected reader surface.
- [ ] Overview, Skills, Git history, Settings and quit/relaunch still work.
- [ ] More than thirty minutes without browser/API activity leaves the same
      session usable; explicit stop and relaunch work on the actual Mac.
- [ ] Before/after estate and Git observations show no Explorer-authored writes.
- [ ] Aaron reports the candidate usable or names a reproducible failing journey.

### I7 — Native Mac packaging, non-blocking lane

- [ ] Decide whether Aaron actually needs a double-click `.app` after using the
      wheel route.
- [ ] If yes, design and build `.app`/DMG on a Mac and verify its full lifecycle.
- [ ] If public distribution is required, obtain Developer ID authority, sign,
      notarize and staple the exact accepted native candidate.

## Build verification — 2026-09-01

Implementation commit `8c7d30a` contains the `0.4.0` portable candidate.

- The complete Python suite passed: **166 passed**.
- Every one of the **21 deliberate safety mutations was killed**.
- A clean offline install of the built wheel passed from an arbitrary working
  directory. The verified wheel SHA-256 is
  `df5086e750451f275d3238c29ca63e1fa4704e84d0cfb5f479a3ab8666c015fb`.
- Targeted live-browser verification on the real local estate showed every
  populated first-level `things/` group and closed both reported navigation
  failures: a tree-opened document followed a resolved reference and a rendered
  body link, with URL, heading, tree selection and back/reload state agreeing.
- The Windows `0.4.0` installer was rebuilt from this checkout and passed its
  isolated per-user install, active upgrade, launch and uninstall lifecycle.
  The installed bundle reported `0.4.0`; the release installer SHA-256 is
  `f37da6d23376536fa668d8cc5eb4580d04c2d998be48a72c7e0ec96786a28e6c`.
  The bytes remain unsigned, so this closes local Windows currency rather than
  the public Windows publication gate.
- The traceability verifier was run and deliberately did **not** reuse the
  `0.3.0` whole-candidate evidence index. Its fail-closed result leaves the full
  browser, performance, Windows-native and human acceptance seal pending for
  this new subject; this is release evidence debt, not a passed release claim.
- Successful launcher execution, Darwin `F_GETPATH` behaviour and inactivity
  expiry on a real Mac remain Aaron's I6 acceptance work.

## Acceptance matrix

| Requirement | Automated evidence | Actual-host evidence | Acceptance owner |
|---|---|---|---|
| All populated first-level `things/` folders appear | Adapter, count and browser tests | Aaron checks a real multi-folder domain | Technical run / Aaron |
| Related links visibly change document from any origin | State/route oracle and browser journeys | Aaron follows tree-origin links | Technical run / Aaron |
| Agent-invoked route works on macOS 13+ | Launcher, CLI and platform-specific confinement tests | Claude launch, read, persistent idle session, explicit stop/relaunch on Aaron's Mac | Aaron |
| Explorer remains usable while idle | Clock-advance HTTP and manual-stop tests | Same tab loads after >30 minutes; explicit stop releases resources | Technical run / Aaron |
| Read-only boundary remains true | Safety suite and source hash comparison | Before/after estate observation | Technical run / Aaron |
| Final artefact is the evidenced artefact | Trace/evidence verifier and wheel hash | Install the recorded hash | Technical run |
| Native package is publishable, if selected | Lifecycle verifier | Gatekeeper launch on a clean account | Technical run / Janosh |

## Assumptions and dispositions

| Assumption | Disposition |
|---|---|
| Core runtime works on macOS | **Unresolved until I6.** Strong static evidence, no runtime claim yet. |
| Aaron has Python 3.10+ | **Launcher checks and explains failure.** His working domains make it likely; do not infer the version. |
| Aaron uses Apple Silicon | **Not needed for the wheel.** Record architecture before native packaging. |
| A native installer is required for first use | **No.** The wheel/CLI is the fastest adequate handoff. Revisit after use. |
| Apple Developer credentials exist | **Unknown and non-blocking.** Required only for public native delivery. |
| “All folders” means first-level content folders under `things/` | **Specified for this sprint.** Deeper folders remain inside their first-level group. |
| Empty folders should display | **No.** Omitted because there is no eligible document to open. |
| Folder name determines thing type | **No.** Domain structure is emergent; frontmatter remains descriptive authority. |
| Hosting is needed to solve Aaron's access | **No.** It remains the separate phase-two product/extraction decision. |

## Risks and responses

| Risk | Response |
|---|---|
| The corrected runtime fails on macOS for an unobserved reason | I6 is the first honest runtime claim; capture Aaron's failure as new model input rather than guessing remotely. |
| An operator leaves Explorer running when resources are scarce | Persistent service is now deliberate; document explicit stop and keep request concurrency bounded. |
| A stale PID points at an unrelated process | Verify the PID's command contains both `mdllm-explorer` and this framework root before sending a signal; otherwise discard only the stale PID file. |
| Case-sensitive filesystems expose path assumptions hidden on Windows | Include mixed-case and POSIX path vectors and execute the real estate journey on Mac. |
| `F_GETPATH` availability or semantics differ by macOS/Python build | Feature-detect narrowly and fail closed; prove against the supported Mac profile. |
| Dynamic collection enumeration diverges from Overview count | One shared policy and an agreement test; no second folder map. |
| Reader surface and route drift on refresh/back | Persist surface explicitly and test every route transition as a state model. |
| Native menu-bar lifecycle stalls on the Cocoa main-thread requirement | Do not gate Aaron on native packaging; spike lifecycle on Mac before building a DMG. |
| Gatekeeper blocks a shared native bundle | Never promise public native delivery without Developer ID signing and notarization. |
| Evidence describes bytes changed afterwards | Build and seal once at the end; any later change invalidates and repeats the seal. |

## Out of scope

- Hosting Explorer on a website or extracting it to a separate product repository.
- Editing files, cloud storage, synchronisation, authentication or multi-user use.
- Renaming the Memory tab or redesigning its visual presentation.
- Windows Authenticode publication and purchase of signing credentials.
- Claiming Safari or a public notarized Mac artefact without executed evidence.
- Opportunistic refactoring unrelated to the shared group policy, reader state or
  macOS boundary.

## Gate to start — closed 2026-09-01

The operator selected the agent-invoked portable route, deferred native Mac
packaging, confirmed that Memory means every populated first-level folder below
`things/`, and authorised the UI corrections plus shared 30-minute activity
lease. Implementation may proceed; successful macOS execution and Aaron's
usability ruling remain acceptance gates rather than inferred facts.


## Operator correction — 2026-09-05

Janosh withdrew the resource-saving inactivity shutdown and reported that the
Mac trial showed a failure. The exact error and Mac/Python profile were not yet
provided, so the reported incident is not treated as causally closed.

The 0.4.1 correction removes the server monitor and browser activity/expiry
machinery. It also repairs a definite Mac bug: `fcntl.fcntl` returns a bytes
buffer; the implementation and its fake had incorrectly assumed `ioctl`-style
in-place mutation. A contract-correct regression failed against the previous
implementation before the production fix. The native Mac test exercises the
real syscall and a document read when run on macOS; it must remain skipped on
Windows, never reported as a Mac pass. Source confinement still fails closed
on unavailable or empty final-path evidence.

Detached shell jobs can inherit SIGINT as ignored. The CLI now explicitly
handles SIGINT/SIGTERM, and the launcher uses untruncated process arguments when
checking ownership. Background stop/relaunch has a POSIX regression test and
still needs actual Mac execution. Earlier 0.4.0 build/idle evidence above is
historical and does not attest to 0.4.1.

The existing Mac acceptance loop remains open for exact error capture, launch,
file reading, persistent idle use and explicit stop/relaunch. This correction
does not reopen the deferred white-label, hosting or native Mac packaging lanes.


Maintenance verification is recorded in
`explorer/tests/evidence/maintenance-0.4.1.json`: the full Windows-hosted suite,
mutation programme, clean offline wheel install and isolated native Windows
install/launch/upgrade/uninstall passed. The browser smoke loaded real estate
documents and followed a related link. The record pins code and artefact hashes;
it explicitly leaves actual Mac execution and the older full release evidence
index unclaimed. No separate insight is needed: the fake/API-contract failure
and its remedy are already preserved in this plan and the corrected regression.
