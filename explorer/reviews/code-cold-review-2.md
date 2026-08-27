---
id: markdownllm-explorer-code-cold-review-2
type: artifact
status: evolving
version: 1.0
created: 2026-08-27
origin: synthesised
exposed: false
tags: [explorer, code-review, security, architecture, test-evidence]
---

# MarkdownLLM Explorer — Code Cold Review 2

Review target: immutable commit `024ab73daf2b74b7033b0ad2ce6e31633bd9b9f4`.

## Verdict

**Reject for acceptance and do not ship.** The reconciliation after cold review 1 made substantial, real improvements: commit pagination now stays pinned across a new `HEAD`; the Git process has fixed argv/environment templates and pre-allocation output capture; frontmatter has event/node/depth/scalar/cardinality limits; application ports are segregated; page controls exist in the browser; HTTP errors and busy responses share hardened headers; and the installed-package and mutation artefacts are no longer name-only placeholders.

Those corrections do not close the acceptance gate. Running the committed evidence verifier against the committed artefacts reports `32` failed and `28` passed requirements. No browser, accessibility, visual, performance, acceptance-journey, adapter-swap or final traceability artefact is committed. More importantly, focused probes found live defects behind several nominally reconciled controls: a request remains current after its tab ceases to be current, a shared-object Git repository reads an object store outside the source root, and an over-limit child process leaves a capture thread blocked forever. The read-only, content-safety, HTTP and accessibility proofs remain materially narrower than the requirements they are mapped to.

## Must fix

1. **Make the trace ledger report evidence, not aspirations, and close the committed evidence gate.** `tests/traceability.yaml` still maps unrelated tests to requirements: FR-EST-005 points to source-ID normalisation at line 7 rather than exact-repository history; NFR-ARCH-003 points to an import-direction test at line 46 rather than `AT-SWAP-001`; and browser/performance rows name evidence that is not present at lines 47–48. The YAML also omits the ledger's required method, fixture, observable pass condition and evidence location. `test_meta.py:29-43` verifies only ID shape/existence. `verify_evidence.py:48-52` trusts any JSON file that self-declares an ID and `status: pass`, without binding it to a target commit or checking the required screenshots/DOM/accessibility/changed-path artefacts. On the pinned tree the verifier deterministically returns `status=fail`, `failed=32`, `passed=28`. **Correction:** use the test-specification ledger schema in full; bind every retained result to the immutable subject and tool/version; verify the actual required artefacts and their hashes; remove false mappings; commit the missing browser, visual, accessibility, performance, adapter-swap, AJ-01–07 and traceability results; keep human decisions `pending-human`.

2. **Reject external Git object stores, including alternates.** `_validate_store` checks only top-level, git-dir and common-dir (`git_commit_history.py:101-116`). A focused shared-clone probe placed `.git/objects/info/alternates` inside the source but pointed it at `C:/Users/Jamos/Projects/MarkdownLLM/.git/objects`; Explorer returned `repository_kind='repository'`, no issue and 50 commits. This violates design §10's external-object-store rejection, NFR-SAFE-001B and the AJ-07 snapshot boundary: Git reads objects that are neither owned by nor snapshotted with the selected source. **Correction:** resolve and validate the effective object database and every alternate/promisor path before any state/history command, fail `git_store_external` when any store escapes, and retain native tests for alternates, worktrees, common dirs, replace refs and lazy-fetch sentinels.

3. **Close the bounded-process capture thread leak.** The reader uses blocking `chunks.put` into a two-slot queue (`process_runner.py:53-66`). When the consumer detects `output_limit` at line 91 it kills the child but never signals, drains or joins the reader; the reader can remain blocked on a full queue. A focused 4,000,000-byte/8-byte-limit probe returned `git_unavailable` and then observed one live `explorer-process-capture` thread. Repeated hostile oversized commit output therefore creates unbounded daemon threads and retained chunks despite the per-call byte cap. **Correction:** make producer cancellation non-blocking, close/drain deterministically, join the capture thread on every exit, and add repeated N+1/output-flood and timeout child-process tests that assert zero surviving threads/processes.

4. **Bind browser response acceptance to live UI context, not only the operation slot.** `state.js:30-33` compares a response only with the request still stored under its operation; it never compares the captured identity with current source/tab/path/mode/query/cursor state. `chooseTab` (`app.js:85-88`) does not abort document, search or context work, and `clearSearch` at line 266 does not abort the search. A focused module probe began a Skills document request, changed live `state.view` to Overview, and `isCurrent(request)` still returned `true`. Thus the old response can render a document over Overview (`app.js:228-237`), a late search can replace another tab, and a late source-context request (`app.js:289-297`) can overwrite document context. The M14 mutation proves only same-operation A-before-B replacement, not O-ASYNC-CURRENT's full-context oracle. **Correction:** maintain one canonical live location identity, abort all invalidated operations on every relevant transition, and accept only an exact match against both the operation request and current state; execute B-before-A across tab, source, path, mode, search-clear, context and load-more routes in a real browser.

5. **Finish the keyboard/tree/overlay accessibility state machines and retain runtime evidence.** The ARIA attributes now exist, but behaviour remains incomplete. `toggleDirectory` rerenders the entire tree without restoring focus (`app.js:132-135`); Arrow Right/Left therefore destroys the focused row instead of entering the first child or retaining/moving focus as specified. Arrow Up/Down wrap from the bounds (`navigation.js:75-76`) rather than remaining at the first/last visible item. No committed browser-runtime, accessibility-tree, contrast, target-size, 200%-zoom or screenshots exercise these paths. Static substring assertions in `test_architecture.py:76-92` cannot establish NFR-ACC-001. **Correction:** implement the specified roving-focus algorithm including expand/collapse/removal/load-more focus, test overlays and all keyboard routes in Chromium at the required viewports/zoom, and retain DOM/accessibility/screenshot evidence with human acceptance still pending.

6. **Prove observable immutability over the actual product journeys.** `test_safety.py:12-52` is useful but calls application routes directly, snapshots only the source tree, captures POSIX-style mode rather than observable Windows ACLs, and has only an fsmonitor sentinel. It does not run AJ-01–06 through HTTP/browser, inspect the launch cwd/outside-root for Explorer state, or sentinel hooks, pager, editor, external diff, credentials, lazy fetch and spawned descendants. Naming the test `test_full_acceptance_journeys...` overstates its oracle. **Correction:** implement O-IMMUTABILITY independently around the installed HTTP/browser journeys, include every NFR-SAFE-001A value and outside-root inspection, exercise all helper classes, state platform exclusions precisely, and retain the snapshots/diffs rather than only a green testcase.

7. **Complete the Markdown/link safety contract with an independent hostile oracle.** Unsafe schemes are improved, but `SafeMarkdownParser` validates a percent-decoded URL and then preserves the original target; encoded `https%3A%2F%2F...` is therefore classified external instead of inert (`safe_markdown_parser.py:98-112`). Image syntax is parsed as a leading literal `!` plus an active link, although repository images/subresources must be inert. The presenter emits `<span class="inert-link">` (`document_presenter.py:52`) even though design §11's output allowlist includes neither `span` nor repository-facing classes. Existing tests assert selected strings produced by the implementation and do not run O-HTML-SAFETY against a hand-authored hostile corpus or final browser DOM. **Correction:** parse images and encoded/canonical URL forms explicitly, activate only canonical HTTP(S) and confined Markdown links, keep every other candidate text-only using the declared tag/attribute allowlist, and apply an independent HTML/DOM oracle.

8. **Return the approved HTTP DTO exactly.** Page encoding includes `next_cursor`, `partial` and `observed_at` inside `data` (`response_encoding.py:37`) while `_success_meta` duplicates them in `meta` (`http_server.py:186-192`) and emits absent `next_cursor` as `null`, contrary to design §12's metadata-only/omit-absent contract. The browser API discards `meta` entirely (`static/js/api.js:40`) and depends on the duplicate fields, so correcting the server alone will break pagination. Most typed adapter errors still omit safe `source_id`/eligible `relative_path`. **Correction:** define and contract-test exact success/error DTOs once, move paging fields solely to metadata, omit absent optionals, consume metadata in the client, and exercise every status/header shape including 405/429 and contextual non-secret errors.

## Should fix

1. **Report incomplete discovery candidates.** Marker-missing children are still silently dropped at `filesystem_catalogue.py:107-108`; invalid marker shapes have no distinct issue. This leaves cold-review-1 Should 1 and FR-EST-004/006 open.

2. **Represent unsupported mode without silently rewriting location state.** `read_document.py:28` still coerces every eligible non-Markdown rendered request to raw. Binary/non-UTF-8 are errors rather than a document-level unsupported state, and refresh/back semantics for requested versus actual mode are not exercised.

3. **Complete installed CLI lifecycle evidence.** The clean-install artefact is materially better and its wheel/package-data probes are plausible, but both `test_cli.py:58-59` and `verify_install.py:79` use process termination, not a real interrupt and bounded active-request join. The artefact does not cover invalid root/domain-dir, requested-port collision, Python 3.10 or source-root immutability, and the wheel/dependency files are not retained for independent replay.

4. **Retain the actual adapter-swap changed-path manifest.** Focused protocols and composition-only concrete imports substantially repair Clean Architecture and ISP, but no `AT-SWAP-001` implementation or evidence exists anywhere under `explorer/`. Import inspection is not a replaceability experiment.

5. **Exercise the specified frontmatter edge corpus.** Event-stream limits are a genuine correction, but explicit versus implicit scalar tags are not distinguished and `!!timestamp` is accepted as a string despite design §11 permitting date coercion only from plain scalars. Node/result N−1/N/N+1, explicit tags and response amplification need independent cases.

6. **Finish collection pagination presentation.** `loadMoreCollection` appends items without inserting a new group heading when a page crosses from one memory group to another (`app.js:203-216`), so the visual grouping can mislabel later pages.

7. **Consolidate the responsive contract.** The primary narrow breakpoint is now 899 px and search remains reachable, but `context.css:27` retains an overlapping `min-width:851px` rule and the 900-pixel boundary still has no runtime layout oracle.

## Could improve

1. Return a dedicated stable error for Git output-limit exhaustion instead of collapsing it into `git_unavailable`; this would make resource diagnostics and retry policy accurate.

2. Add a privacy-safe estate-issue detail view so the issue count is actionable without revealing excluded paths.

3. Replace test names such as `test_full_acceptance_journeys...` with the exact boundary they exercise; evidence names should narrow claims, not widen them.

## First-review correction disposition

- **Substantially corrected:** pinned commit pagination; focused application ports/core native-import rule; 12-character collision-aware SHA display; partial overview labels; common HTTP security headers for normal/busy/method paths; browser load-more controls; explicit required CLI root and controlled startup errors.
- **Partially corrected but still blocking:** traceability/evidence; Git sandbox; bounded process resources; parser/Markdown hostile bounds; exact HTTP DTO; full-context async identity; keyboard/accessibility; read-only proof; installed lifecycle proof.
- **Still open from Should findings:** discovery issue taxonomy, unsupported-document state, contextual typed errors, complete fatal diagnostics evidence, and single responsive-breakpoint contract.

## Test and evidence observations

- Full committed suite replay from an extracted immutable tree with the pinned `src` on `PYTHONPATH`: **89 passed in 39.44 s**.
- Committed evidence verifier replay: **fail — 32 failed, 28 passed, 0 pending of 60 requirements**.
- Mutation runner replay: **16 killed, 0 survived**. The mutations alter copied production source and their recorded pre-mutation SHA-256 values match the pinned source (M14's second replacement correctly starts from its first replacement). This is genuine executable evidence for those 16 narrow mutants.
- The committed clean-install JSON records a built wheel hash, exact PyYAML 6.0.3 wheel, arbitrary cwd and four live routes. It was not independently replayable from committed bytes because neither wheel is retained; it also does not prove the missing lifecycle/platform clauses above.
- Shared-object-store probe: Explorer accepted an outside-root alternates object database as a normal repository and returned commits.
- Process-output probe: after an over-limit result, one `explorer-process-capture` thread remained alive.
- Browser-state probe: after changing live tab from Skills to Overview, the prior Skills document request remained current.

## Test blind spots

- No committed real-browser BT-* execution, final hostile DOM check, screenshots, accessibility tree/scan, contrast, target-size, zoom/reflow or Firefox/Safari execution.
- No AJ-01–07 technical evidence and no human-owned acceptance dispositions.
- No `PT-SCALE-001` 20-process artefact; the sole pytest performance test remains a 1,200-file, once-in-process smoke test with a three-second search allowance.
- No `AT-SWAP-001` changed-path evidence.
- No merge-topology, corrupt/detached/timeout/promisor/alternates/external-object-store Git matrix.
- No repeated oversized-output/thread/process cleanup oracle.
- No complete directory/search/collection/frontmatter/response/concurrency N−1/N/N+1 matrix.
- No Windows ACL snapshot, native handle replacement race fixture or complete hook/helper/pager/editor/lazy-fetch sentinel set.
- No clean Python 3.10 execution or real Ctrl+C/active-request shutdown timing.
- No independent Markdown golden/hostile corpus; current HTML assertions share implementation assumptions.

## Positive evidence

- Source and boundary tokens remain separated, public encoding is explicit, and core/application no longer import filesystem/subprocess/HTTP concrete implementations.
- The whole configured domain directory is excluded from substrate ownership before discovery, and ordinary secret/symlink/reparse routes fail closed in the tested fixtures.
- Git argv templates are allowlisted; global/system config, optional locks, lazy fetch, hooks, fsmonitor, untracked cache, index preload, external diff, credentials, LFS filters, file protocol, pager/editor/askpass and replace objects receive explicit controls.
- Commit page 2 remains pinned after a new commit and the focused test now exercises a genuine multi-page route.
- File reads use limit+1, UTF-8/BOM/NUL classification and pre/open/post identity/size/mtime comparisons; traversal and frontmatter scans no longer materialise unbounded result sets before their primary caps.
- The browser now has page controls for tree/search/collections/commits, per-operation AbortControllers, tab/tree ARIA state, responsive modal/inert mechanics and partial-count labels. These are meaningful foundations even though the runtime algorithms and evidence are incomplete.
- The retained `pytest.xml` matches the replayed 89-test suite, and the mutation matrix was independently reproducible.

## Review method

I read `requirements.md` v0.3, `design.md` v0.3, `test-specification.md` v0.1 and cold code review 1 in full from the immutable Git view. I then inspected every committed Explorer implementation, browser asset, test, tool, packaging file and evidence artefact at the target commit. Conclusions were written only after `mdllm session-start . --assert-head 024ab73daf2b74b7033b0ad2ce6e31633bd9b9f4` confirmed the significant-read boundary.

Execution used an extracted copy of the pinned tree in a temporary workspace path, removed after probing. No implementation, specification or test file was modified, and no commit was made.
