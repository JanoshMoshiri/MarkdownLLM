# MarkdownLLM Explorer — Test Specification

**Status:** release-candidate gate approved when the coverage and evidence checks in §11 pass

**Version:** 0.4

**Date:** 2026-08-27

**Requirements:** `explorer/docs/requirements.md` v0.4

**Design:** `explorer/docs/design.md` v0.5

## 1. Test position

Explorer is done only when each requirement has a named oracle and retained evidence. A green suite is necessary but insufficient: the suite must also demonstrate that its high-risk controls can detect deliberately broken implementations.

The strategy combines four evidence classes:

- **Tests:** deterministic assertions over code or a running system.
- **Inspections:** architecture, visual or standards evidence with an explicit checklist.
- **Analyses:** reproducible measurements such as performance and mutation results.
- **Demonstrations:** end-to-end acceptance journeys executed against synthetic or real estate shapes.

Human product/usability acceptance is separate from technical verification. The implementation run may mark technical rows pass/fail; only Janosh may accept the product, and only the CEO or a delegated U1 representative may close the executive-usability hypothesis.

## 2. Test layers

| Prefix | Layer | Dependencies permitted | Purpose |
|---|---|---|---|
| `UT` | Unit | core/application + fakes only | Pure policy, identity, state and use-case behaviour |
| `AT` | Architecture fitness | source/AST/import graph | Dependency direction, cohesion and replaceability |
| `CT` | Contract | one port/adapter or API encoder | Shared behavioural contracts and boundary values |
| `GT` | Git/filesystem integration | temporary native files + real git | Captured behaviour of untrusted boundaries |
| `ST` | System/runtime | installed package + real loopback server | CLI, HTTP, security, lifecycle and distribution |
| `BT` | Browser/runtime | packaged UI in available Chromium | Interaction, visual, responsive and accessibility evidence |
| `PT` | Performance | generated scale fixture + isolated processes | Reproducible latency/payload budgets |
| `MT` | Meta/mutation | contract oracles + deliberate mutants | Test the tests and kill false-positive controls |
| `AJ` | Acceptance journey | complete running product | Requirement-spanning technical acceptance |

Pytest markers are `unit`, `architecture`, `contract`, `gitfs`, `system`, `performance`, and `meta`. Browser and acceptance evidence is orchestrated separately but named in the same ledger.

## 3. Fixtures and evidence sources

### F-ESTATE-MIN

A temporary substrate with `AGENTS.md`, a local git repository, eligible root files, and two independent `domain/<name>` repositories. Each domain has its own commits, `AGENTS.md`, `skills/`, `things/insights/` and nested files. Subjects intentionally differ so parent-history fall-through is observable.

### F-ESTATE-IMPERFECT

Extends F-ESTATE-MIN with:

- marker-only non-git domain;
- marker-missing git child;
- NFC/case-fold source-ID collision;
- unreadable candidate where the OS permits it;
- symlink and Windows junction/reparse candidates where the profile permits them;
- encoded traversal/absolute/UNC/device inputs;
- `.env`, credential/token/key/certificate names and ignored build/cache trees;
- malformed/duplicate/alias/tag/deep/large frontmatter;
- UTF-8 BOM, non-UTF-8, NUL/binary, N−1/N/N+1 files; and
- a deterministic replacement hook that changes a file or directory between validation and read.

### F-GIT-SHAPES

Temporary repositories covering normal, independent nested, dirty tracked, unborn, detached, empty, corrupt, merge/topological pagination, external worktree/common-dir, malicious config (pager, external diff, hooks, fsmonitor, alias), missing executable, timeout and promisor/partial-clone configuration. A sentinel process/file records any helper or unexpected executable invocation.

### F-MARKDOWN-GOLDEN

Privacy-safe excerpts structurally representative of the manifesto, requirements, design, thing files and skills: headings, emphasis, nested lists, blockquotes, tables, fenced code, horizontal rules, frontmatter and relative/external links. Expected safe HTML is hand-authored, not produced by the renderer under test.

### F-MARKDOWN-HOSTILE

Script/style/event attributes, raw HTML, malformed tags, encoded/control-character schemes, `javascript:`, `data:`, SVG/image/subresource attempts, cross-domain links, traversal links, external links, YAML alias/merge/recursive/unsupported-tag expansion and response-amplification payloads.

### F-ESTATE-SCALE-V1

Generated from a versioned manifest: one substrate, 13 independent domains, 2,500 eligible paths, 50 commits per repository, deterministic names/content/timestamps and a retained manifest SHA-256. It is created once per benchmark run outside the timed region.

### F-REAL-ESTATE-2026-08-27

Read-only observational probe of the private local estate (substrate + 13 discovered domains). Evidence contains counts, timings, status codes and hashes only—no document bodies, absolute paths, domain names or screenshots. It is never the reproducibility oracle.

### F-WINDOWS-INSTALL

A clean ignored build root, Windows x64, no `mdllm-explorer` on `PATH`, an empty per-user install directory, a temporary conforming substrate and an unrelated sentinel directory. Network access is disabled for installer/runtime execution. Independent probes inspect PE/version metadata, process modules, package assets, HKCU uninstall/application keys, Desktop/Start Menu `.lnk` target/arguments, listener/process counts and pre/post tree hashes. The real user installation is a final separate acceptance target, never the reproducibility oracle.

### Visual reference

The Perplexity screenshot oracle is SHA-256 `9423dc8c66b6ed004c3ba0ba1fae58a20489dbbf1b014b06f24688b5f0bd81e3`. Inspection uses spatial principles (calm three-region shell, density, hierarchy), not pixel identity or brand copying.

## 4. Independent oracles

### O-OWNERSHIP

Build a path-to-source map directly from fixture construction, independent of the catalogue. Query every owned file through its source and all alternate sources/path spellings. Exactly one route may return content; the unconditional substrate `domain/` exclusion must hold even for rejected/new candidates.

### O-IMMUTABILITY

Before and after AJ-01–10, independently snapshot source-relative names/types, content SHA-256, size, mtime, mode/ACL where available; raw `.git/index`, config and packed refs; loose-ref bytes; object-name/content inventory; the unrelated sentinel directory; and Windows installation-owned registry/shortcut paths where applicable. Exclude atime/read telemetry explicitly. No production adapter or uninstaller manifest is used to compute the oracle.

### O-HTML-SAFETY

Parse output with Python's `html.parser` and a separate allowlist. Fail on forbidden tag/attribute, repository `style`/`class`, event attribute, unsafe/encoded scheme, subresource tag or external link lacking no-opener/no-referrer. Also scan the serialised response and DOM after browser insertion.

### O-GIT-PROCESS

A capturing process runner records absolute executable, argv, cwd, environment, timeout and output limit. Real malicious-config fixtures use sentinel helpers. The oracle rejects shell use, non-allowlisted argv/env, source-root executable lookup, lazy fetch, external stores or any child/helper invocation.

### O-ASYNC-CURRENT

A programmable API fixture deliberately returns request B before stale request A. The browser DOM must remain B. The oracle observes selected source/path/mode and visible content, not internal request counters.

### O-TRACE

Extract all `FR-*`/`NFR-*` IDs from requirements, all rows from `tests/traceability.yaml`, and all test IDs from collected tests/evidence manifests. Require exact one-to-one requirement coverage (no duplicate/unknown/missing IDs), at least one executable or inspection evidence ID per row, a pass condition and owner, and no reference to a nonexistent test.

## 5. Test catalogue

### Unit and application

- `UT-ID-001` — source-ID NFC/case-fold/percent-encoding vectors and collision errors.
- `UT-PATH-001` — relative path grammar, platform variants and NUL/drive/UNC/device rejection.
- `UT-ELIG-001` — all eligible extensions/names and every ignore/secret precedence rule.
- `UT-LIMIT-001` — N−1/N/N+1 for bytes, depth, entries, candidates, page sizes, response and concurrency values.
- `UT-USE-001` — each use case with its smallest fake ports; success, empty, partial and typed error states.
- `UT-STATE-001` — browser-independent state/reducer transition vectors mirrored as a browser module test.

### Architecture fitness

- `AT-IMPORT-001` — AST import rules: inner layers cannot import pathlib/os/subprocess/HTTP/YAML/HTML implementations or outer modules; concrete adapters only in composition.
- `AT-PORT-001` — each use case depends only on the minimum segregated protocols declared by design.
- `AT-VIEW-001` — browser views neither call `fetch` nor own global/cross-view state; content responsibilities remain split by view.
- `AT-SWAP-001` — fake replacements for every port require changes only to composition/adapter/tests; retained changed-path manifest proves NFR-ARCH-003.

### Filesystem/catalogue/document contracts

- `CT-CATALOG-001` — root configuration, substrate identity, deterministic domain ordering, marker admission and issue taxonomy.
- `GT-DISCOVERY-001` — F-ESTATE-IMPERFECT remains partially usable across native filesystem outcomes.
- `GT-OWNERSHIP-001` — O-OWNERSHIP, including rejected/new domain candidates and cross-domain relative links.
- `CT-TREE-001` — lazy immediate-directory pages, sorting, cursor signature/fingerprint, inclusive depth/entry N−1/N/N+1 boundaries and visible partial state shared with aggregate traversal.
- `CT-SEARCH-001` — case-insensitive path search, 10,000-candidate cap, pagination and no file-body load.
- `CT-COLLECTION-001` — Skills/Memory folder/type precedence, malformed/mismatch/duplicate ID and empty groups.
- `GT-CONFINE-001` — traversal/case/separator/encoding/link/junction/reparse/replacement tests for the executed OS/filesystem profile.
- `CT-DOCUMENT-001` — UTF-8/BOM/text/binary classification, mode-specific payload, malformed frontmatter and changing-file errors.
- `CT-FRONTMATTER-001` — duplicate/alias/merge/tag/depth/scalar/cardinality/node/normalised-size boundaries.
- `CT-MARKDOWN-001` — every required construct against F-MARKDOWN-GOLDEN.
- `CT-LINK-001` — confined same-source Markdown route, external HTTP(S) attributes and inert unsafe/unresolved/cross-source targets.
- `CT-HTML-001` — O-HTML-SAFETY over F-MARKDOWN-HOSTILE and raw mode.

### Git contracts

- `GT-GIT-ROOT-001` — exact repository root; no parent fall-through; external store rejection.
- `GT-GIT-STATE-001` — normal/unborn/detached/empty/corrupt/timeout states and ISO timestamp/author fields.
- `GT-GIT-PAGE-001` — pinned-head/skip topological pagination with merge history, new commits between pages and 12/full SHA identity.
- `GT-GIT-SAFE-001` — O-GIT-PROCESS, malicious config, no lazy fetch/locks/helpers and absolute executable.
- `GT-IMMUTABLE-001` — O-IMMUTABILITY around every git route.

### HTTP/runtime/distribution

- `ST-INSTALL-001` — build/install package from outside checkout into a clean supported Python environment; no Node; post-install offline launch from arbitrary cwd.
- `ST-CLI-001` — root/domain-dir/port validation, printed fragment-capability URL, requested-port collision, non-zero invalid exits and ≤5-second interrupt shutdown.
- `ST-WIN-BUNDLE-001` — clean PyInstaller one-folder build; executable PE/version/icon metadata, embedded interpreter/dependencies/static assets, no system-Python/Node resolution at runtime, and manifest/hash retained.
- `ST-WIN-INSTALL-001` — NSIS setup is one executable; per-user/no-elevation and offline; valid-root gate; exact install files, selected-root registry value, uninstall registration and singleton Desktop/Start Menu shortcuts with quoted arguments.
- `ST-WIN-LAUNCH-001` — frozen shortcut target starts with no console, reaches health, invokes the browser-opening port, exposes Open/Exit tray commands, reactivation routes `open` to the original process, and exits within five seconds without persisting capability material.
- `ST-WIN-UPGRADE-001` — same-build reinstall while the primary and an active request are running waits for process termination, preserves root, replaces files and leaves one owned shortcut/registration instance.
- `ST-WIN-UNINSTALL-001` — silent and interactive uninstall while the primary and an active request are running wait for process termination and remove only owned files, keys and shortcuts; source/outside O-IMMUTABILITY snapshots remain identical.
- Native lifecycle automation may compile an identity-isolated installer from the exact frozen payload and NSIS source when a real Explorer installation must be preserved. That proves destructive install/upgrade/uninstall logic without touching operator state; publication still requires the final signed release installer itself to run and match the recorded release hash.
- The signed release gate inspects Authenticode on the frozen application, generated uninstaller and setup, then repeats ST-WIN-INSTALL/UPGRADE/UNINSTALL on the signed installer. Missing signature, failed RFC 3161 timestamp or a Windows code-integrity block is a release failure, not an unknown-publisher warning to waive.
- `ST-HTTP-AUTH-001` — exact Host on all routes; Origin policy; missing/wrong/right capability; no CORS; constant-time comparison seam; session-expiry state.
- `ST-HTTP-HEADERS-001` — CSP, frame denial, nosniff, no-referrer, no-store and fixed MIME types on success/error/static/health.
- `ST-HEALTH-001` — unauthenticated health returns only static status/version.
- `ST-API-SCHEMA-001` — endpoint DTO fields/nullability, page metadata, issue vs request error, error code/status/retryability and redaction.
- `ST-API-INCREMENTAL-001` — initial estate response contains no file body/history; document returns exactly one mode; separate endpoints/payload caps.
- `ST-SERVER-BOUND-001` — 16 requests admitted; 17th receives bounded 429 before a thread is created; exact asset manifest; 405 and malformed/oversized request handling.
- `ST-LOG-001` — diagnostics contain operation/source ID/status but no capability, query, absolute path, content, frontmatter or external command output.
- `ST-OFFLINE-001` — installed runtime with blocked network/no Node/CDN/extension still completes AJ-01–03.

### Browser, visual and accessibility

- `BT-SHELL-001` — desktop three-region composition, Substrate above Domains, tabs/context and absence of false controls.
- `BT-NAV-001` — source/tree selection, nested disclosure, document opening, URL refresh/back/forward and same identity from tree/Skills/Memory.
- `BT-TABS-001` — Overview commits/counts/partial labels; Skills/Memory empty/populated/issues; Settings read-only path/markers/theme.
- `BT-DOCUMENT-001` — styled/raw switch fetches on demand, context metadata, safe external/internal links and unsupported states.
- `BT-SEARCH-001` — path filter results, empty state and keyboard activation.
- `BT-THEME-001` — light/dark/system, system default and local persistence without location loss.
- `BT-ASYNC-001` — O-ASYNC-CURRENT plus timeout, retry, abort and terminal content/empty/error states.
- `BT-RESPONSIVE-001` — 1440×900 three-region and 390×844 overlays; 320 CSS px/200% zoom; focus trap/Escape/return; no lost capability.
- `BT-KEYBOARD-001` — tree/tab/search/mode/theme keyboard state machines, collapse focus and paginated focus.
- `BT-A11Y-001` — roles/states/names/live announcements, contrast/colour independence, target size, reduced motion and automated accessibility scan where available.
- `BT-VISUAL-001` — synthetic-fixture screenshots in light/dark desktop and narrow views; inspection against visual-reference principles and clipping/overlap oracle.

### Performance and acceptance

- `PT-SCALE-001` — F-ESTATE-SCALE-V1, one discarded warm-up + 20 isolated runs, raw timings and 19/20 thresholds for all five budgets.
- `PT-REAL-001` — privacy-safe observation on F-REAL-ESTATE-2026-08-27; never substitutes for PT-SCALE-001.
- `AJ-01` through `AJ-10` — execute the exact requirements journeys and retain technical pass/fail evidence; human owners remain pending unless attributable operator acceptance is supplied.

## 6. Test-the-tests mutation programme

Shared oracle functions accept a subject implementation. Production subjects must pass; deliberate mutants must fail. `MT-MUTATION-001` records a kill matrix.

| Mutant | Deliberate defect | Required killer |
|---|---|---|
| `M01` | Remove substrate domain-directory exclusion | `GT-OWNERSHIP-001` |
| `M02` | Resolve source IDs by last-write-wins on collision | `UT-ID-001`, `CT-CATALOG-001` |
| `M03` | Follow a final symlink/reparse point | `GT-CONFINE-001` |
| `M04` | Change `>` to `>=` or omit limit+1 | `UT-LIMIT-001`, boundary contract |
| `M05` | Permit YAML alias/merge/custom tag | `CT-FRONTMATTER-001` |
| `M06` | Pass raw/encoded URL scheme through | `CT-LINK-001`, `CT-HTML-001` |
| `M07` | Return raw and rendered bodies together | `ST-API-INCREMENTAL-001` |
| `M08` | Disable cursor HMAC/fingerprint | `CT-TREE-001`, `GT-GIT-PAGE-001` |
| `M09` | Use PATH lookup after adopting source cwd | `GT-GIT-SAFE-001` |
| `M10` | Omit optional-lock/no-lazy-fetch env | `GT-GIT-SAFE-001`, `GT-IMMUTABLE-001` |
| `M11` | Accept missing capability or hostile Host/Origin | `ST-HTTP-AUTH-001` |
| `M12` | Log raw request target/header/query | `ST-LOG-001` |
| `M13` | Acquire semaphore after creating thread | `ST-SERVER-BOUND-001` |
| `M14` | Accept stale response A after current B | `BT-ASYNC-001` |
| `M15` | Insert repository metadata with `innerHTML` | `CT-HTML-001`, browser DOM safety check |
| `M16` | Let a browser view call `fetch` directly | `AT-VIEW-001` |

Gate: all 16 mutants must be killed. A surviving mutant is evidence of a weak oracle or missing test and blocks implementation acceptance even when production tests are green.

## 7. Property/metamorphic checks

Without adding a property-testing dependency, deterministic generated tables exercise these relations:

- normalising an already normalised source ID/path is idempotent;
- case/Unicode variants either map to the same collision set or remain distinct exactly as the algorithm states;
- adding an excluded file never changes eligible counts/search/collections;
- adding a domain commit never changes substrate history, and adding a substrate commit never changes domain history;
- rendered output contains all visible text (modulo Markdown markers) but never increases the allowed active-tag set;
- switching raw↔rendered changes only mode/content, not source/path/frontmatter identity;
- adding a new commit after commit page 1 does not change pinned page 2;
- changing the selected source/path/mode before a response can only preserve or advance current UI state, never revert it; and
- running any read journey twice produces identical mutation-relevant source snapshots.

Seeds and generated cases are recorded on failure and fixed in CI for reproducibility.

## 8. Platform and environment matrix

| Surface | Required evidence in this run | Claim rule |
|---|---|---|
| Windows 11 / NTFS / Python 3.12 development runtime | Executed unit→system, native reparse/symlink where permitted | May claim executed development profile |
| Windows 10+ x64 frozen runtime / NSIS setup | Clean bundle, install, launch, reactivation, upgrade and uninstall; no system Python/Node/network | May claim executed native-distribution profile |
| Python 3.10 syntax/runtime floor | Compile/AST check plus clean runtime if interpreter available | Otherwise standards-backed, not executed |
| Linux/macOS path adapters | Pure path vectors + code inspection in this run | Must remain unexecuted until CI/profile runs |
| Chromium | In-app runtime interaction and screenshots | May claim executed browser/version recorded |
| Firefox/Safari | Standards/static inspection only | Must remain unexecuted |

No unavailable platform/browser receives a synthetic pass. The validation report labels `pass`, `fail`, `pending-human`, `unexecuted-platform`, or `not-applicable` explicitly.

## 9. Performance procedure

1. Record fixture manifest/hash and machine CPU/RAM/storage/OS/Python.
2. Build F-ESTATE-SCALE-V1 outside timed intervals.
3. Before each retained run on Windows, require two consecutive 500 ms system CPU samples at or below 60%, bounded by a 30-second wait; on the minimum four-core reference profile this leaves at least one logical core of headroom, while an unavailable window fails the profile instead of silently measuring saturation. Run the measured server and inherited Git children at high scheduling priority. Record the observed gate samples and policy in the profile.
4. For each measured route, start a fresh server process, perform one discarded warm-up, then one timed request; repeat until 20 retained samples exist. This avoids silently measuring one long-lived cache state.
5. Measure client request start to terminal complete body with `perf_counter_ns`; validate response correctness during every sample.
6. Retain all raw timings, median, p95-like order statistic (19th of 20), max and threshold verdict. The deterministic floor or a script computes figures; narrative never hand-adds them.
7. Run PT-REAL-001 separately and retain only privacy-safe aggregate evidence.

## 10. Visual and acceptance procedure

Use the in-app browser against the real loopback process; no pasted static mockup counts.

1. Execute AJ-01–02 in light desktop; capture DOM state and screenshot.
2. Repeat document/theme path in dark desktop.
3. Execute AJ-04 at 390×844 and 320 CSS px/200% zoom; capture overlay/focus evidence and screenshot.
4. Execute keyboard-only tree, tabs, search, document mode and theme.
5. Inspect text clipping, overlap, unintended horizontal page scrolling, selected/hover/focus contrast and empty/error states.
6. Execute hostile payloads through the real document/API route and inspect the final DOM, not only server HTML.
7. Record AJ-01–10 technical dispositions. Keep human dispositions pending unless an attributable human actually rules; when supplied, retain that ruling as subject-bound evidence rather than inferring it from a technical walkthrough.

Synthetic fixture screenshots may be committed. Private-estate screenshots/content must remain in gitignored `.test-tmp/explorer-evidence/` and are never publication evidence.

## 11. Traceability gate

The implementation shall include `explorer/tests/traceability.yaml` mirroring the ledger below. `MT-TRACE-001` applies O-TRACE before the first implementation commit and in the final suite.

| Requirement | Method | Fixture | Evidence/test IDs | Observable pass condition | Acceptance owner |
|---|---|---|---|---|---|
| FR-EST-001 | test | MIN | CT-CATALOG-001, ST-INSTALL-001 | Explicit root works from arbitrary cwd; invalid root fails | Technical run / Janosh |
| FR-EST-002 | test+demo | MIN | CT-CATALOG-001, BT-SHELL-001 | First source is labelled Substrate independent of folder name | Technical run / Janosh |
| FR-EST-003 | test+demo | MIN | CT-CATALOG-001, BT-SHELL-001 | One-level admitted domains sorted by specified key | Technical run / Janosh |
| FR-EST-004 | test | IMPERFECT | CT-CATALOG-001, GT-DISCOVERY-001 | Only AGENTS/.markdownllm readable directories admitted; issues classified | Technical run |
| FR-EST-005 | test | GIT | GT-GIT-ROOT-001 | Every source history comes from exact local repo, never parent | Technical run |
| FR-EST-006 | test+demo | IMPERFECT | GT-DISCOVERY-001, AJ-03 | Valid sources remain usable beside every bad candidate | Technical run / Janosh |
| FR-EST-007 | test+mutation | IMPERFECT | GT-OWNERSHIP-001, MT-MUTATION-001 | O-OWNERSHIP gives exactly one route and excludes whole domain dir | Technical run |
| FR-EST-008 | test | IMPERFECT | UT-ID-001, CT-CATALOG-001 | Stable relative IDs, no absolute path, collisions surfaced | Technical run |
| FR-NAV-001 | demo | UI | BT-SHELL-001 | Persistent rail exposes Substrate and Domains disclosures | Janosh |
| FR-NAV-002 | demo | UI | BT-NAV-001 | Source changes without page reload and content matches source | Technical run / Janosh |
| FR-NAV-003 | test+demo | MIN | CT-TREE-001, BT-NAV-001 | Nested tree loads per directory without reading bodies | Technical run / Janosh |
| FR-NAV-004 | demo | UI | BT-NAV-001 | Eligible selection opens document and retains context | Technical run / Janosh |
| FR-NAV-005 | demo | UI | BT-NAV-001, AJ-02 | URL/back/forward/refresh restore specified location and ancestors | Technical run / Janosh |
| FR-NAV-006 | demo+inspection | UI | BT-RESPONSIVE-001, AJ-04 | Exact desktop/narrow/zoom layouts retain all capabilities/focus | Technical run / Janosh |
| FR-TAB-001 | test+demo | MIN | ST-API-SCHEMA-001, BT-TABS-001 | Overview has identity/counts/state/first commits and partial labels | Technical run / Janosh |
| FR-TAB-002 | test+demo | GIT | GT-GIT-STATE-001, GT-GIT-PAGE-001, BT-TABS-001 | Required commit fields/order/page/states are exact | Technical run / Janosh |
| FR-TAB-003 | test+demo | MIN | CT-COLLECTION-001, BT-TABS-001 | Skills lists Markdown or explicit empty without error | Technical run / Janosh |
| FR-TAB-004 | test+demo | IMPERFECT | CT-COLLECTION-001, BT-TABS-001 | Memory recursion/group/issues/duplicates/empty follow contract | Technical run / Janosh |
| FR-TAB-005 | test+demo | MIN | ST-API-SCHEMA-001, BT-TABS-001 | Settings shows authorised read-only facts/theme, no write controls | Technical run / Janosh |
| FR-TAB-006 | test+demo | MIN | BT-NAV-001 | Tree/Skills/Memory resolve same document identity/reader | Technical run |
| FR-DOC-001 | test+demo | GOLDEN | CT-MARKDOWN-001, BT-DOCUMENT-001 | All required constructs match independent safe goldens | Technical run / Janosh |
| FR-DOC-002 | test+demo | GOLDEN | CT-FRONTMATTER-001, BT-DOCUMENT-001 | Frontmatter separately structured; invalid never inferred | Technical run / Janosh |
| FR-DOC-003 | test+demo | UI | CT-DOCUMENT-001, BT-DOCUMENT-001 | Raw/rendered switch fetches and shows exactly one mode | Technical run / Janosh |
| FR-DOC-004 | demo | UI | BT-DOCUMENT-001 | Context shows only factual specified metadata | Technical run / Janosh |
| FR-DOC-005 | test+demo | IMPERFECT | CT-DOCUMENT-001, BT-DOCUMENT-001 | UTF-8 text raw; binary/non-UTF-8 explicit unsupported | Technical run |
| FR-DOC-006 | test+demo | HOSTILE | CT-LINK-001, BT-DOCUMENT-001 | Only confined local + labelled HTTP(S) active with protections | Technical run |
| FR-DOC-007 | test+mutation | IMPERFECT | UT-ELIG-001, GT-OWNERSHIP-001, MT-MUTATION-001 | Eligibility/secret precedence holds on every exposure route | Technical run |
| FR-DOC-008 | test | IMPERFECT | CT-DOCUMENT-001, GT-CONFINE-001 | Every encoding/frontmatter/change outcome has stable terminal state | Technical run |
| FR-SRCH-001 | test+demo | SCALE | CT-SEARCH-001, BT-SEARCH-001 | Case-insensitive eligible path filter/pages/partial, no bodies | Technical run / Janosh |
| FR-SRCH-002 | demo+inspection | UI | BT-KEYBOARD-001 | Search/tabs/tree/theme/mode fully keyboard operable | Technical run / Janosh |
| FR-UI-001 | inspection+demo | UI | BT-SHELL-001, BT-VISUAL-001 | Restrained three-region hierarchy matches reference principles | Janosh |
| FR-UI-002A | demo | UI | BT-THEME-001 | Every view renders in light, dark and system modes | Technical run / Janosh |
| FR-UI-002B | test+demo | UI | BT-THEME-001 | No saved mode follows emulated system preference | Technical run |
| FR-UI-002C | test+demo | UI | BT-THEME-001 | Explicit choice persists reload without location loss | Technical run / Janosh |
| FR-UI-003 | inspection | UI | BT-VISUAL-001, BT-A11Y-001 | Selection/action/empty/error distinct in both themes | Janosh |
| FR-UI-004 | inspection+demo | UI | BT-SHELL-001 | No placeholder/irrelevant control; every shown control works | Technical run / Janosh |
| FR-RUN-001 | test | CLEAN/WINDOWS | ST-INSTALL-001, ST-CLI-001, ST-OFFLINE-001, ST-WIN-BUNDLE-001 | Portable package and frozen runtime both launch offline with packaged assets and no Node/system Python | Technical run |
| FR-RUN-002 | test | WEB | ST-CLI-001, ST-SERVER-BOUND-001 | Loopback only, port policy, capability isolation, clean shutdown | Technical run |
| FR-RUN-003 | test | WEB | ST-HEALTH-001 | Health available with static values only | Technical run |
| FR-RUN-004 | test+demo | WINDOWS | ST-WIN-BUNDLE-001, ST-WIN-INSTALL-001, AJ-08 | One setup exe performs valid per-user install with root selection, shortcuts and uninstaller, no command line or Python | Technical run / Janosh |
| FR-RUN-005 | test+demo | WINDOWS | ST-WIN-LAUNCH-001, AJ-09 | Shortcut opens browser/tray; reactivation keeps one service; Exit terminates within five seconds | Technical run / Janosh |
| FR-RUN-006 | test+demo | WINDOWS | ST-WIN-UPGRADE-001, ST-WIN-UNINSTALL-001, AJ-10 | Upgrade preserves root/singletons; uninstall removes owned state and no source/outside bytes | Technical run / Janosh |
| FR-ERR-001 | contract+demo | IMPERFECT | ST-API-SCHEMA-001, BT-ASYNC-001 | Exact redacted shape/status/retry and contextual UI | Technical run |
| FR-ERR-002 | test+mutation | WEB | BT-ASYNC-001, MT-MUTATION-001 | Every request terminates and stale responses cannot win | Technical run |
| NFR-ARCH-001 | inspection+test | SOURCE | AT-IMPORT-001 | No outer/native implementation dependency in core/application | Technical run |
| NFR-ARCH-002 | inspection+test | SOURCE | AT-PORT-001, AT-VIEW-001 | HTTP/browser translate only; policy remains inner/adapter seam | Technical run |
| NFR-ARCH-003 | test+analysis | SOURCE | AT-SWAP-001 | Adapter swap changed-path evidence touches no inner file | Technical run |
| NFR-SAFE-001A | test+analysis | IMPERFECT | GT-IMMUTABLE-001, AJ-07 | O-IMMUTABILITY unchanged for all in-scope values | Technical run |
| NFR-SAFE-001B | test+mutation | GIT | GT-GIT-SAFE-001, MT-MUTATION-001 | Exact executable/argv/env/cwd/time/output; no helper/lazy fetch/lock | Technical run |
| NFR-SAFE-001C | test+inspection | CLEAN/WINDOWS | ST-INSTALL-001, ST-WIN-INSTALL-001, ST-WIN-UNINSTALL-001, AJ-07, AJ-10 | Runtime persists no content/capability; installer writes/removes only declared per-user surfaces | Technical run |
| NFR-SAFE-002A | test | IMPERFECT | UT-PATH-001, CT-CATALOG-001 | Root/domain config rejects absolute/escaping/invalid inputs | Technical run |
| NFR-SAFE-002B | test+analysis | IMPERFECT | GT-CONFINE-001 | Executed native profiles reject detected links/replacements; residual labelled | Technical run |
| NFR-SAFE-003 | test+mutation | HOSTILE | CT-HTML-001, CT-LINK-001, MT-MUTATION-001, AJ-06 | O-HTML-SAFETY passes server response and final DOM | Technical run |
| NFR-SAFE-004 | test+mutation | BOUNDARY | UT-LIMIT-001, ST-SERVER-BOUND-001, MT-MUTATION-001 | Every N−1/N/N+1 limit and stable error/partial state holds | Technical run |
| NFR-SAFE-005 | test+mutation | WEB | ST-HTTP-AUTH-001, ST-HTTP-HEADERS-001, ST-HEALTH-001, MT-MUTATION-001, AJ-06 | Capability/Host/Origin/CORS/headers/health boundary exact | Technical run |
| NFR-PORT-001 | test+inspection | MATRIX/WINDOWS | ST-INSTALL-001, ST-WIN-BUNDLE-001, GT-CONFINE-001 | Windows native profile and Chromium executed; unavailable native profiles explicitly unexecuted | Technical run |
| NFR-OFF-001 | test | CLEAN/WINDOWS | ST-OFFLINE-001, ST-WIN-INSTALL-001 | AJ-01–03 and AJ-08 pass with network blocked and no Python/CDN/Node/extension | Technical run |
| NFR-PERF-001 | analysis | SCALE | PT-SCALE-001 | Manifest/profile/raw timings and 19/20 thresholds all pass | Technical run |
| NFR-PERF-002 | contract | MIN | ST-API-INCREMENTAL-001 | Separate APIs; initial payload no bodies/history; one doc mode | Technical run |
| NFR-ACC-001 | test+inspection | UI | BT-A11Y-001, BT-RESPONSIVE-001, BT-KEYBOARD-001, AJ-04 | Full named WCAG interaction checklist evidenced, limitations labelled | Technical run / Janosh |
| NFR-TEST-001 | test | FAKE | UT-USE-001, AT-IMPORT-001 | Core/use cases pass with no browser/network/live git/user estate | Technical run |
| NFR-TEST-002 | test | IMPERFECT/GIT | GT-DISCOVERY-001, GT-CONFINE-001, GT-GIT-STATE-001 | Temporary real repos cover every named captured shape | Technical run |
| NFR-OBS-001 | test+inspection | WEB | ST-LOG-001 | Useful operation/source severity with zero body/secret/path leakage | Technical run |

Gate checks:

1. exactly 63 unique requirements rows exist;
2. extracted requirements IDs equal trace rows exactly;
3. every evidence/test ID exists in collected tests or the browser/inspection manifest;
4. every row has an observable pass condition and owner;
5. all technical rows have a final disposition before completion; and
6. human-owned rows remain `pending-human` unless a subject-bound attributable human decision names their exact scope.

For the 2026-08-27 candidate, `tests/evidence/operator-acceptance.json` records Janosh's explicit product acceptance and names the exact human-owned rows it closes. The verifier rejects that record if its scope differs from the pending-human set; technical pass/fail remains independent.

## 12. Execution order and stop rules

1. `MT-TRACE-001` — coverage gate before implementation.
2. Unit + architecture fitness.
3. Adapter contracts + mutation kills.
4. Git/filesystem captured-reality tests.
5. Installed-package HTTP/system/security tests.
6. Clean Windows bundle → setup → launch/reactivation → upgrade → uninstall lifecycle.
7. Performance on synthetic fixture.
8. Browser runtime, visual and accessibility evidence.
9. AJ-01–10 and final trace disposition.
10. Full suite again from the committed candidate.

Stop and loop back to requirements/design when:

- a requirement has no feasible oracle;
- a safety mutant survives;
- a real boundary behaves differently from the design;
- meeting a performance budget would violate ownership/safety;
- the browser route needs business logic that has no application use case; or
- an acceptance journey exposes an ambiguous human decision.

## 13. Evidence retention

Public, privacy-safe evidence is written to `explorer/tests/evidence/`:

- `validation-report.md` — environment, suite counts, trace dispositions and limitations;
- `performance.json` — fixture/profile/raw timings and computed verdicts;
- `mutation-kills.json` — mutant → killer outcome;
- `windows-installer.json` — frozen-build/setup hashes, environment, install/shortcut/launch/upgrade/uninstall observations and AJ-08–10 dispositions;
- `visual-light.png`, `visual-dark.png`, `visual-narrow.png` — synthetic estate only; and
- `traceability-result.json` — coverage and evidence-ID audit.
- `operator-acceptance.json` — attributable human UAT decision and exact human-owned requirement scope.

Private live-estate observations go only to gitignored `.test-tmp/explorer-evidence/`, contain no bodies/names/absolute paths and are summarised privacy-safely in the public report.
