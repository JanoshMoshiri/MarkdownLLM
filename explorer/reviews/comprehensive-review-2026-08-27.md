---
id: markdownllm-explorer-comprehensive-review-2026-08-27
type: artifact
status: stable
version: 1.0
created: 2026-08-27
origin: synthesised
exposed: false
confidence: high
tags: [explorer, comprehensive-review, architecture, integration, code, acceptance]
linked_things:
  - id: code-architect-governs-substrate-code
    relation: implements
  - id: markdownllm-explorer-code-cold-review-2
    relation: extends
  - id: markdownllm-explorer-windows-distribution
    relation: references
---

# MarkdownLLM Explorer — Comprehensive Review

## Verdict

**The Explorer is a strong, coherent implementation, but it is not yet technically acceptance-ready.** The previous cold-review blockers were mostly corrected: the core/application boundary is clean, source ownership and Git confinement are substantial, the process runner closes its earlier resource leak, the HTTP and Markdown boundaries are well defended, browser request identity is materially improved, the native Windows shell is kept outside the inner architecture, and the automated suite is broad and green.

Three findings prevent a technical acceptance recommendation:

1. the retained evidence seal does not describe the final Explorer tree, so the committed traceability result says `pass` while the verifier correctly returns `fail` against the reviewed subject;
2. active upgrade and uninstall can begin deleting the frozen application before the running primary process has actually exited; and
3. the claimed adapter-swap proof exercises only the Markdown presenter, not the four replaceable boundaries named by the requirement.

Human user acceptance is **deliberately pending**. The operator stated that a full end-user acceptance run has not yet been performed. This review therefore does not count pending human dispositions as defects, does not claim to have performed UAT, and does not use the absence of UAT to lower the code-quality assessment. The recommendation is: correct the three technical blockers, reseal the technical evidence on the final immutable tree, then conduct the separate operator-owned UAT run.

## Immutable review boundary

- Framework view reviewed: `commit:e1ad077a01d31bc85c9904a1674cf9669e64cd89`.
- Explorer implementation lineage: `3c1b449acf2c927cad3850d55c7b393f3a67f569`.
- The only framework changes between those commits are outside `explorer/`; `git diff 3c1b449..e1ad077 -- explorer` is empty.
- Code Architect view applied: `commit:c711d2a46225aaca471100e1eec2afceb02e751a`.
- Review date and environment: 2026-08-27, Windows 11, Python 3.12.4, Chromium through the in-app browser.

The review covered the Explorer's requirements, design, test specification, source, delivery shell, browser application, Windows integration, packaging, verification utilities, traceability manifest and retained evidence. Executable checks ran from a detached worktree pinned to the Explorer implementation commit; live browser inspection used the same implementation served locally. No product code was changed by this review.

## Code Architect review formulation

Code Architect's delivery loop was used as the review spine:

1. **Requirements:** treat requirements as hypotheses and test whether the stated user, safety and lifecycle outcomes are observable.
2. **Model:** inspect the vocabulary, ownership boundaries, identity rules and invariants independently of transport and storage.
3. **Design:** test dependency direction, ports, replacement seams, failure handling and integration contracts.
4. **Decomposition:** assess single responsibility, change isolation, naming and whole-system graspability.
5. **Build and verification:** replay tests, mutation, performance and evidence verification rather than accepting green artefacts by name.
6. **Acceptance:** separate technical evidence from human judgement and leave unresolved human-owned states visibly pending.

The detailed lenses were single responsibility, dependency direction, replaceability, change isolation, testability, naming, requirements-as-hypothesis, captured behaviour, risk-first sequencing, unresolved-state visibility, failure-cost rigour, traceable definition of done, actionable error ownership and whole-system graspability.

## Evidence replay

| Check | Result | Interpretation |
|---|---:|---|
| Full project-local pytest suite | **109 passed** in 61.11 s | Broad unit, contract, system, architecture and safety coverage is genuinely green. |
| Mutation suite | **16 killed, 0 survived** | The 16 declared mutants are exercised by effective tests. |
| Performance harness | **20 runs passed** across commits, document, estate overview, search and tree | The retained performance categories stayed inside their gates in this environment. |
| Final traceability verifier | **fail** — 14 technical passed, 49 technical failed, 30 human pending | The evidence index is not bound to the current immutable subject. Human pending is expected; the 49 technical failures are caused by the invalid evidence binding. |
| Live technical browser walkthrough | **operational with one route-restoration defect** | Source discovery, repository identity, document reading, responsive layout and overlay accessibility worked; a refreshed Skills deep link lost its curated collection. |

The browser walkthrough discovered the substrate plus 13 domains, showed distinct repository heads, opened Skills and rendered frontmatter/context, and stayed free of horizontal overflow at 390×844. The narrow-screen navigation exposed dialog semantics, made background content inert, closed on Escape and returned focus to its opener. These are technical observations, not user acceptance.

## Must fix before technical acceptance

### 1. Reseal evidence on the actual final subject

**Finding.** `tests/evidence/evidence-index.json` and the committed `traceability-result.json` are bound to subject hash `bedd2d8c...`, generated before the final change to `docs/windows-distribution-decision.md`. Commit `3c1b449` then changed that reviewed file without rebuilding the evidence index. The committed traceability result still declares `status: pass`, but rerunning `tools/verify_evidence.py` against the final tree returns:

```text
status=fail
technical_passed=14
technical_failed=49
human_pending=30
evidence_errors=evidence index is not bound to the current immutable subject
```

**Why it matters.** The evidence gate is the technical definition of done. A stale seal makes the retained green result false for the release candidate, even when the changed file is narrative rather than executable. The verifier is behaving correctly; the release sequencing failed to make resealing the last acceptance-affecting move.

**Correction.** Make the final immutable subject the input to one last evidence build and verification pass. Fail CI/release if any tracked Explorer file changes after sealing. Retain the regenerated index and traceability result together, and keep the 30 human-owned dispositions pending until the operator performs UAT.

### 2. Wait for the running application to exit before upgrade or uninstall mutates its files

**Finding.** `packaging/windows/explorer.nsi:133-139` launches `--request-exit` and then immediately removes `_internal` and the installed executable. The same pattern occurs during uninstall at lines 159-167. `WindowsInstanceCoordinator.send` returns after sending the pipe command (`windows_app.py:180-198`); it does not wait for the primary process to finish its server, tray and active-request shutdown. `ExecWait` therefore waits for the short-lived secondary sender, not the installed primary process.

The installer verifier does not expose the race: it performs the upgrade before starting the installed application (`verify_windows_installer.py:169-175`), and it explicitly stops and waits for the application before invoking uninstall (`:197-205`).

**Why it matters.** Upgrade and uninstall are primary user journeys under FR-RUN-006. On Windows, deleting or replacing a running frozen application's files can fail partway, leaving an inconsistent installation or an uninstall that reports success without removing everything.

**Correction.** After requesting exit, wait with a bounded timeout for positive proof that the primary process is gone—for example mutex disappearance plus process-handle termination—before deleting installation files. Abort safely on timeout. Add installed-system tests for upgrade while the tray application is active and uninstall while it is active, including active-request drain and post-operation file/registry/shortcut checks.

### 3. Make the adapter-swap evidence match the replaceability claim

**Finding.** NFR-ARCH-003 names replacement of the HTTP server, Git reader, filesystem reader **or** Markdown renderer. The test specification strengthens this to `AT-SWAP-001 — fake replacements for every port`. The implementation in `tests/test_architecture.py:88-120` creates only `swap_presenter.py`, changes composition and records `"adapter": "Markdown presenter"`. `tests/evidence/adapter-swap.json` retains only that one swap, while traceability marks NFR-ARCH-003 passed.

**Why it matters.** Static dependency direction and the current code structure make replaceability plausible, but the retained proof is narrower than the accepted requirement. The evidence currently widens a one-boundary experiment into a four-boundary claim.

**Correction.** Either execute and retain controlled swaps for the HTTP server, Git reader, filesystem reader and Markdown renderer, or narrow the approved requirement and test specification with explicit human authority. Preserve a changed-path manifest and runtime probe for each swap and keep every core/application path absent from the change set.

## Should fix

### 4. Restore the collection as well as the document on Skills and Memory deep links

**Finding.** Opening a document from a Skills collection uses `openCollectionDocument` and `fetchDocument(..., embedded=true)` (`app.js:243-247`), preserving the split collection/reader view. Reloading the resulting URL follows `restoreRoute` and `openDocument` (`:355-363`), which uses `embedded=false` (`:249-252`). In live Chromium, the source, Skills tab, file, mode and document content returned, but the curated Skills list disappeared: collection and split-view counts both fell to zero.

**Why it matters.** FR-NAV-005 requires refresh/back/forward to restore source, tab, file, mode and ancestor expansion. The literal fields restore, but the visible Skills mental model does not: the active tab says Skills while behaving like a standalone tree document.

**Correction.** Route restoration should load the collection shell first for Skills/Memory and then open the selected document inside it. Add browser tests for refresh, back and forward on overview, tree document, Skills document and Memory document routes.

### 5. Reconcile the accepted design with the implementation

**Finding.** Several accepted design statements no longer describe the code:

- `docs/design.md:44` specifies `X-MDLLM-Capability`; implementation, client, tests and tools use `X-Explorer-Capability`.
- Design line 272 specifies POSIX `O_NOFOLLOW`/`fstat` and a Windows `CreateFileW` identity wrapper; the current reader uses Python file opening plus pre/post resolution and identity checks rather than that platform-specific design.
- The design module map and browser contract name `context_panel.js`; the implementation uses `views/context.js`.
- Cursor examples in the design do not match the current operation/source/context/offset/revision cursor model.

**Why it matters.** The implementation's present safety posture is defensible under its documented privileged-race exclusion, and the header name is internally consistent. The defect is contract drift: the design can no longer be trusted as an exact guide for maintenance, threat review or adapter replacement.

**Correction.** Reconcile design to the accepted implementation where behaviour is intentional; change code only where the stronger design remains a required safety property. Add exact contract tests for security header naming and cursor schema so the drift cannot recur silently.

### 6. Use one observable directory-depth boundary across tree and aggregate traversal

**Finding.** `ConfinedSourceReader.tree` rejects only when `path.depth > directory_depth` (`confined_source_reader.py:53-56`), so it can expose immediate children at the configured depth. `_walk` skips a directory when `depth >= directory_depth` (`:200-206`), so counts, search and curated collections omit those same children without a partial indication. The test specification requires depth N−1/N/N+1 coverage, but the adapter tests cover directory entry count rather than directory depth.

**Why it matters.** A path can be discoverable in the tree and absent from search, overview counts and collections. That weakens the user's model of the estate and makes the limit's inclusive/exclusive meaning dependent on the route.

**Correction.** Choose one inclusive boundary, use it in both traversal paths, return a visible partial/stable limit state when content is intentionally omitted, and add N−1/N/N+1 tests across tree, search, counts and collections.

### 7. Decompose the browser orchestration before the next feature tranche

**Finding.** View modules are usefully passive and contain no fetching or cross-view state, but `delivery/static/js/app.js` still owns source selection, tree paging, tabs, documents, collections, search, routing, theme, overlays, error presentation and request lifecycle in one 388-line module. It is the main cascade point for unrelated changes; the route-restoration defect is one symptom of two document-opening workflows living in that central coordinator.

**Why it matters.** This is manageable at the present size, not a current reliability blocker. It will become a change-isolation and testability problem as UAT produces interaction refinements.

**Correction.** Split orchestration by user workflow—source/tree, collection/document, search, routing and chrome/theme—around the existing shared state/API primitives. Keep view modules presentation-only and add behavioural contracts at the controller seams.

## Could improve

1. **Separate commit SHA and subject in the DOM.** `views/overview.js:35` appends the SHA span and subject text without a text separator. CSS supplies visual spacing, but the accessible heading name can read as one concatenated token. Add a literal space or separately labelled subject element.

2. **Make the documented test command independent of working directory.** The full suite passed from `explorer/` with `PYTHONPATH=src`, but invoking the absolute test path from the framework root resolves imports such as `tools.verify_evidence` against the framework's `tools` package and fails collection. State the required working directory in the README or package test helpers under an unambiguous Explorer namespace.

3. **Broaden the read-only static fitness check.** The architectural test catches selected `Path` mutation methods, while the stronger system immutability oracle carries most of the real proof. Extending the static rule to built-in write modes and common filesystem mutation APIs would make accidental source writes fail earlier and more locally.

## Code Architect lens assessment

| Lens | Assessment | Basis |
|---|---|---|
| Dependency direction | Strong | Core and application avoid delivery/adapters; concrete construction is isolated in composition. |
| Single responsibility | Strong inside, mixed in browser shell | Use cases and ports are focused; `app.js` has accumulated orchestration responsibilities. |
| Replaceability | Structurally credible, evidence incomplete | Presenter swap succeeds; the named HTTP/Git/filesystem swaps are not retained. |
| Change isolation | Good with two weak points | Windows installer lifecycle and central browser orchestration have wider failure surfaces. |
| Testability | Strong | Focused fakes, contract/system tests, mutation and performance runners are all present. |
| Naming and vocabulary | Mostly strong | Stable source IDs and typed errors are clear; design/header/module vocabulary has drifted. |
| Requirements as hypotheses | Strong specification, one overclaim | Requirements are observable and unusually exact; traceability currently overstates two proofs. |
| Captured behaviour | Strong | Git, filesystem, HTTP, browser and Windows behaviours are represented in executable fixtures. |
| Risk-first sequencing | Strong | Safety, resource bounds, hostile input and packaging risks received early dedicated work. |
| Unresolved-state visibility | Correct for UAT, incorrect for technical seal | Human acceptance stays pending; committed traceability still presents a stale technical pass. |
| Failure-cost rigour | Strong except active installer lifecycle | Typed failures and redaction are good; upgrade/uninstall needs positive exit proof. |
| Traceable definition of done | Blocking defect | Final evidence binding fails, so the release candidate is not sealed. |
| Errors handled where actionable | Strong | Outer layers translate infrastructure errors into stable public states without leaking private paths. |
| Whole-system graspability | Good | Three-layer architecture and explicit composition are legible; design drift should be reconciled. |

## Integration assessment

### Framework and estate integration

The source catalogue correctly separates substrate ownership from one-level domain repositories, excludes the domain tree from substrate traversal and reports imperfect candidates without hiding valid sources. Distinct Git heads are shown for the substrate and Code Architect domain. Stable source IDs, private boundary tokens and explicit public DTO encoding keep repository identity separate from filesystem paths and prevent internal capabilities from crossing the wire.

### Filesystem, Git and safety integration

The Explorer remains observational: eligible/excluded names are explicit, traversal is bounded, reparse/symlink parents are rejected, Git uses fixed argv and environment, external/lazy object stores are rejected, process output/deadlines are bounded, and the repeated-flood test asserts no surviving capture threads or child processes. The full HTTP acceptance-journey safety oracle snapshots sources, Git state and outside state. No new source mutation was observed during this review.

### HTTP and browser integration

Capability, Host and Origin checks are consistent in the implementation; public DTOs omit private boundary values; method, busy and normal responses receive security headers; Markdown rendering uses an allowlist and inert unsafe links. Current-request identity, abort behaviour, pagination and responsive overlays are materially improved. The collection deep-link restoration defect is bounded and reproducible rather than systemic.

### Windows and distribution integration

The PyInstaller/NSIS outer driver preserves the clean inner architecture and removes Python as an end-user prerequisite. Per-user settings, shortcuts, tray control, single-instance activation and installed runtime probes are all present. The remaining active-process race is important precisely because the overall distribution path is now real enough to be the product's primary user path.

## UAT boundary and recommended acceptance run

The operator should own the final human dispositions after the technical blockers are corrected. The UAT run should use the actual installer and an immutable candidate, then execute AJ-01 through AJ-09 from `docs/requirements.md`, with particular attention to:

- first installation and root selection without Python knowledge;
- relaunch from Desktop and Start Menu, tray Open/Exit and single-instance behaviour;
- source switching, tree search, Skills/Memory deep links, refresh/back/forward and raw/rendered mode;
- imperfect or partially readable estates and whether failure messages are understandable;
- 1440×900, 390×844 and keyboard-only 320 CSS-pixel/200% zoom interaction;
- active upgrade and active uninstall after their lifecycle correction; and
- confirmation that the selected substrate and every repository remain byte-identical.

The human result should remain `pending-human` until that run occurs. A technical browser walkthrough by an engineering agent is supporting evidence, not a substitute for the user's acceptance decision.

## Recommended correction order

1. Correct and system-test active upgrade/uninstall shutdown synchronisation.
2. Complete the four-boundary adapter-swap experiment or formally narrow the requirement.
3. Fix Skills/Memory route restoration and the directory-depth inconsistency.
4. Reconcile the design contract and make the test command unambiguous.
5. Run the full suite, mutation, performance, installer and browser evidence against one final immutable Explorer tree.
6. Build the evidence index last and verify the retained traceability result from a clean checkout.
7. Perform the separate operator-owned UAT run and record the human dispositions.

## Final recommendation

**Do not label the current commit accepted or release-ready.** It is a credible acceptance candidate after focused corrections, not a rebuild. The architecture is sound enough to preserve; the work now is to make lifecycle behaviour and retained proof match the quality already present in most of the code.

## Exposure

No. This is a project-specific review of the MarkdownLLM Explorer. The review method comes from Code Architect, but the findings and acceptance recommendation depend on this implementation and its pinned evidence.
