---
id: markdownllm-explorer-code-cold-review-1
type: artifact
status: evolving
version: 1.0
created: 2026-08-27
origin: synthesised
exposed: false
tags: [explorer, code-review, security, architecture, test-evidence]
---

# MarkdownLLM Explorer — Code Cold Review 1

Review target: immutable commit `8d1da7b3c181e471ddbd0962d3000275001f8c15`.

## Verdict

**Reject for acceptance and do not ship.** The implementation is a useful vertical prototype, but it is not the v1 specified by the requirements/design and its green suite materially overstates coverage. The highest-risk gap is epistemic: `61 passed, 1 skipped` is real executable evidence for a narrow happy-path suite, while `tests/traceability.yml` falsely presents that suite as evidence for all 60 requirements and all 16 mutation kills. There is no browser-runtime, installation, immutability, mutation, scale-profile, visual, accessibility or acceptance-journey evidence directory at the pinned commit.

The read-only intent and basic loopback/capability boundary are visible, but the Git process, parser and traversal resource controls do not meet their normative contracts. The browser omits required pagination, current-request isolation and accessibility state machines. These are acceptance blockers, not polish.

## Must fix

1. **Replace the traceability and mutation name ledger with executable evidence.** `tests/test_meta.py:19-28` proves only that each mapped Python function name occurs somewhere in test source; `tests/test_meta.py:32-38` proves only that M01–M16 keys exist and point to existing names. It never runs a mutant or demonstrates that the named test kills it. The mappings are demonstrably unrelated in places: `tests/traceability.yml:10` claims an API DTO test proves the expandable estate rail (FR-NAV-001), line 15 uses the same test for responsive overlays (FR-NAV-006), line 32 uses a health/static-shell test for clean install and offline launch (FR-RUN-001), and line 46 uses a static string inspection for all of NFR-ACC-001. This contradicts test specification §§4 O-TRACE, 5, 6 and 11, and requirements §12/Definition of done. **Correction:** use the required `traceability.yaml`; collect stable test/evidence IDs, dispositions and retained artefacts; implement the independent oracles; execute each subject mutant and retain a kill matrix; fail rows whose stated pass condition was not actually observed.

2. **Implement the specified Git sandbox and bounded process I/O.** `adapters/git_commit_history.py:102-117` still permits repository configuration to influence execution and omits the designed hooks-path/fsmonitor/untracked-cache/index-preload/external-diff controls; `subprocess.run(..., stdout=PIPE, stderr=PIPE)` at lines 119-123 buffers process output without a cap, then checks sizes only after completion at line 127. The code therefore does not satisfy NFR-SAFE-001B, NFR-SAFE-004, design §10, O-GIT-PROCESS or GT-GIT-SAFE-001. It also uses porcelain v1 rather than the specified v2. **Correction:** introduce a capturing process-runner seam with a strict executable/argv/environment allowlist, command-line config that disables every named repository broadening route, combined streaming output capped at 1 MiB, timeout/child sentinel evidence and malicious-config tests.

3. **Fix commit pagination so a new HEAD does not invalidate a pinned page.** `adapters/git_commit_history.py:50-54` rejects every follow-up cursor when current `HEAD` differs from its pinned head. That is the opposite of FR-TAB-002/design §10/test-spec property “adding a new commit after page 1 does not change pinned page 2”. The only cursor test, `tests/test_adapters.py:123-131`, starts with one commit, asserts that no cursor exists and never exercises a second page. **Correction:** validate that the pinned commit still exists, run page 2 against it regardless of a newer current HEAD, and add merge-history/new-commit-between-pages coverage with at least two pages.

4. **Enforce traversal and parser bounds before allocation.** `adapters/confined_source_reader.py:64` and `:275` convert whole directories to lists before applying page/candidate limits; the tree path has no directory-entry cap at all. `adapters/frontmatter_parser.py:34` materialises the full event stream and lines 37-44 compose/load the full YAML graph before checking only the final JSON byte size; the specified depth, scalar, mapping/sequence cardinality and composed-node limits are absent. This violates NFR-SAFE-004, requirements §9, design §§9/11 and CT-TREE/CT-FRONTMATTER boundary contracts. **Correction:** scan only limit+1 entries/candidates, return the specified partial/error state, and enforce YAML depth/scalar/cardinality/node budgets while composing rather than after expansion. Add every N−1/N/N+1 boundary from UT-LIMIT-001.

5. **Close the Markdown link policy gap.** `adapters/safe_markdown_parser.py:100-101` treats `mailto:` as external and `document_presenter.py:49-52` emits it as an active anchor; a focused runtime probe produced `<a href="mailto:test@example.invalid" ...>`. FR-DOC-006 permits only labelled HTTP(S) external links and makes all other schemes inert. The presenter also emits repository-derived `class="language-…"` at `document_presenter.py:24-25`, contrary to design §11's no content-supplied class rule. **Correction:** allow only canonical HTTP/HTTPS after decoded/control-character validation, require same-source eligible Markdown for internal links, render every other scheme inert, and remove repository-derived attributes. Run the hostile corpus through both server output and final browser DOM.

6. **Return the specified HTTP contract on every route.** Success currently returns only `{"data": ...}` (`delivery/http_server.py:116`) instead of `{data, meta:{request_id, observed_at, next_cursor?, partial?}}`; errors at `:139-140` omit optional `source_id`/`relative_path` even when the typed error carries them; `/health` at `:103` omits version. Busy responses at `:49-57` bypass the common security-header/error encoder, and mutation methods at `:81-89` bypass Host/Origin validation. This violates FR-RUN-003, FR-ERR-001, NFR-SAFE-005 and design §12. **Correction:** route all success/error/405/429 paths through one bounded encoder with request ID and required metadata, validate Host/Origin before method dispatch, return static health status/version, and test exact DTO/header/error matrices.

7. **Make browser request identity cover every operation and full context.** `delivery/static/js/state.js:16-20` has one global request counter/controller, while tree/context/load-more and collection-document requests bypass it. In particular `app.js:163-173` allows an older document response to overwrite a newer path/mode in the same source; load-more functions at `:143-160` have no source/tab/cursor identity. This violates FR-ERR-002, design §13 and O-ASYNC-CURRENT. **Correction:** maintain per-operation request state keyed by operation/source/tab/path/mode/cursor, abort obsolete requests, accept responses only on an exact current identity match, preserve location on retry/session expiry, and run the deliberate B-before-A browser oracle (M14).

8. **Implement complete pagination in the browser.** `app.js:85-102` stores only the first tree page and never exposes `next_cursor`; search at `:188-194` does the same. Collection load-more at `:154-160` discards a returned next cursor, so at most two pages are reachable. Users therefore cannot reach valid paths once directory/search/collection pages exceed their limits, contrary to FR-NAV-003, FR-SRCH-001, FR-TAB-003/004 and requirements §9. **Correction:** add accessible load-more controls to each paged view, preserve/validate cursors, append deterministically without duplication, retain focus as design §13 requires, and test N−1/N/N+1 pages in the real browser.

9. **Build the specified keyboard, responsive-overlay and accessibility state machines.** The tree assigns only `role="treeitem"` (`views/navigation.js:28-46`) with no `aria-expanded`, `aria-selected`, roving tabindex or arrow/Home/End behaviour. Tabs are plain buttons with click handlers only (`index.html:42-47`, `app.js:40`), not a tablist. Overlays at `app.js:251-266` trap Tab but provide no dialog role/`aria-modal`/background `inert`; search is removed below 900 px (`context.css:40`). This fails FR-NAV-006, FR-SRCH-002 and NFR-ACC-001/design §13. **Correction:** implement the complete named ARIA/keyboard algorithms, labelled modal overlays with inert background and focus return, keep every desktop capability reachable at narrow/zoom layouts, and retain Chromium DOM/screenshot/accessibility evidence at all required viewports.

10. **Restore the approved clean-architecture seams.** `application/ports.py:19-25` collapses metrics, tree, search, collection, document and settings into one `SourceBrowser` interface, so every use case depends on a broad port rather than the minimum segregated protocols in design §6. `ConfinedSourceReader` then owns traversal, collections, frontmatter, Markdown parsing, link resolution and presentation. Core imports `pathlib` (`core/models.py:7`, `core/eligibility.py:7`) despite design §15's explicit architecture rule. The architecture tests only reject outer-package imports and therefore pass these violations (`tests/test_architecture.py:19-31`). This fails NFR-ARCH-001/002/003 and SOLID interface-segregation/single-responsibility goals. **Correction:** reinstate the designed focused ports/adapters/use-case orchestration, prohibit native filesystem modules in core, replace generic dataclass serialization with explicit DTO encoders, and provide the adapter-swap changed-file evidence.

11. **Prove read-only operation instead of scanning for a few method names.** `tests/test_architecture.py:33-42` searches AST attribute names for a small set of write calls; it does not snapshot source bytes/metadata, git index/refs/objects/config, detect child helpers, or exercise AJ-01–07. Repository configuration remains live during Git commands. This does not satisfy NFR-SAFE-001A/001C, O-IMMUTABILITY or AJ-07. **Correction:** implement independent pre/post filesystem and Git snapshots, helper/hook/pager/editor sentinels, outside-root persistent-state inspection and repeated full journeys; retain the evidence and report platform exclusions accurately.

12. **Meet the standalone CLI/distribution contract and verify it from a clean environment.** `__main__.py:14` defaults `--root` to cwd rather than requiring an explicit root, and invalid root/domain/port exceptions are not converted to a controlled diagnostic/non-zero CLI result. Shutdown at `:23-29` closes the listening socket but does not implement the designed bounded join of active requests. No test builds/installs the wheel, launches from an arbitrary cwd offline, checks requested-port collision/interrupt timing, or verifies package data. Mapping FR-RUN-001 to a health test (`tests/traceability.yml:32`) is false coverage. **Correction:** implement explicit configuration/error/lifecycle handling and ST-INSTALL/ST-CLI/ST-OFFLINE in a clean Python 3.10+ environment, retaining artefact/install/launch evidence.

## Should fix

1. **Report all discovery failures instead of silently dropping candidates.** `adapters/filesystem_catalogue.py:78-99` ignores marker-missing git children and converts marker-read errors to an empty marker tuple, so FR-EST-004/006's incomplete/unreadable actionable issues are absent. Add the specified issue taxonomy and native unreadable/reparse fixtures.

2. **Do not mislabel partial overview counts as complete.** `views/overview.js:8-15` renders numeric counts but ignores `overview.counts.partial`, contrary to FR-TAB-001. Render partial/unavailable labels and exercise both conditions.

3. **Use a collision-safe fixed baseline abbreviation.** `views/overview.js:34-49` starts at seven characters although design §10 specifies 12; collision checking is limited to commits already loaded in the DOM. Start at 12 and retain full SHA as accessible text/detail, extending only for actual collisions across the loaded result set.

4. **Separate unsupported document state from raw coercion.** `adapters/confined_source_reader.py:182` silently coerces requested rendered mode for every non-Markdown eligible file to raw. FR-DOC-005/008 calls for an explicit unsupported state for binary/non-UTF-8 and stable mode/location semantics. Make the API/browser state explicit and test refresh/back behaviour.

5. **Keep source-relative errors contextual without leaking paths.** Typed `ExplorerError` supports source/path, but most adapter raises omit them and the HTTP encoder discards them. Populate safe source ID and eligible relative path where authorised; continue using fixed public messages for excluded paths.

6. **Improve fatal diagnostics.** `delivery/http_server.py:126-133` logs typed errors but silently maps unexpected exceptions to `internal_error`. NFR-OBS-001 requires explicit application-fatal diagnostics without content/path leakage. Emit a redacted request/operation/source/request-ID event for all terminal failures.

7. **Resolve CSS/layout duplication.** `app.css` and `context.css` duplicate responsive shell/sidebar rules with different 850/899 breakpoints. Consolidate one breakpoint contract to reduce drift and make the 900-pixel boundary directly testable.

## Could improve

1. Replace `object` fields in `ExplorerUseCases` with explicit protocols/types so composition failures are caught statically.

2. Split compressed one-line CSS and several dense JavaScript statements; this will make accessibility/state review and line-level evidence more reliable.

3. Add a visible, non-sensitive estate issue detail route or disclosure rather than only showing an issue count, so FR-EST-006 is actionable to an operator.

## Test blind spots

- No browser automation or in-app Chromium run; no BT-* executable tests, DOM hostile-content check, screenshots or accessibility scan.
- No acceptance journeys AJ-01–07 and no human-owned pending/accepted dispositions.
- No required `tests/evidence/` artefacts: validation report, performance samples, mutation kill matrix, visual evidence or traceability result.
- No clean build/install/offline/arbitrary-cwd/Python-3.10/runtime-interrupt evidence.
- No O-IMMUTABILITY pre/post snapshot and no malicious Git config/helper/lock/lazy-fetch sentinel.
- No real commit pagination, merge topology, detached/corrupt/timeout/external-store or new-HEAD-between-pages test.
- No directory/search/collection/candidate/frontmatter/response/concurrency N−1/N/N+1 matrix; only file bytes receive that treatment.
- No source-ID NFC/case-fold collision execution, unreadable/reparse domain discovery, Windows junction/native-handle replacement, or alternate-source ownership oracle.
- No independent Markdown golden. Existing tests assert only that a handful of tags occur; they do not verify nested-list/table/fence fidelity or the exact allowlist.
- The single performance test creates 1,200 files, runs once in-process, permits search under three seconds and checks only result count. It is not F-ESTATE-SCALE-V1 or the 20-isolated-run/19-of-20 oracle.
- The suite run for this review passed `61` tests with `1` symlink test skipped when directed to a writable basetemp. A first run without the package on `sys.path` failed collection; the README workflow assumes prior installation, which was not performed because this review was read-only. Neither result supplies the missing acceptance evidence above.

## Positive evidence

- Source roots are hidden behind opaque boundary tokens and the public encoder rejects those tokens (`delivery/response_encoding.py:13-23`).
- The substrate registers the whole configured domain directory as an exclusion, so admitted and rejected descendants do not fall through through ordinary lexical routes (`adapters/filesystem_catalogue.py:69-72`).
- File eligibility has an explicit allowlist and secret-name precedence (`core/eligibility.py:12-46`), and body reads use limit+1 with UTF-8/BOM, NUL and changed-file checks (`adapters/confined_source_reader.py:195-249`).
- The server binds to `127.0.0.1`, generates an in-memory per-launch capability, validates exact Host/Origin for GET/HEAD, applies strong common security headers and admits requests before thread creation (`delivery/http_server.py:35-68`, `:91-124`, `:142-162`).
- Repository strings are generally inserted with `textContent`; rendered HTML comes from an escaping presenter rather than raw repository HTML. Raw document mode uses `textContent` (`views/document.js:19`).
- Static assets are packaged and build-free; PyYAML is exactly pinned and Python `>=3.10` is declared (`pyproject.toml:1-30`).
- Tests do cover useful narrow contracts: basic exclusive substrate/domain reads, secret filtering, file-byte boundaries, binary/encoding errors, cursor signatures, basic Markdown escaping and Host/Origin/capability denial.

## Review method

I read `requirements.md` v0.3, `design.md` v0.3 and `test-specification.md` v0.1 in full from the immutable Git view, then inspected every file under `explorer/src`, every test, `pyproject.toml`, `README.md` and existing review artefacts. The repository significant-read boundary was asserted immediately before writing: HEAD remained `8d1da7b3c181e471ddbd0962d3000275001f8c15`.

Focused execution used the repository virtual environment with `explorer/src` added only to the test process import path and a writable ignored basetemp. Result: `61 passed, 1 skipped in 29.74s`; the skipped test was native symlink creation. A direct parser/presenter probe confirmed `mailto:` becomes an active anchor. No implementation/specification file was modified and no commit was made.
