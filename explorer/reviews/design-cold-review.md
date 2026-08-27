# Cold Architecture Review — MarkdownLLM Explorer

## Review basis and decision

Reviewed `explorer/docs/design.md` v0.1 against `explorer/docs/requirements.md` v0.2 from immutable repository view `01f26d1731106c17ddc03cdbc4a93cc04d5ca99d`. The requirements bytes match the design's pinned view `e276ac3b2430a0f0d1844a0806bb155a5bb9620d`. No implementation or other project material was inspected.

**Decision: revise before implementation.** The overall ports-and-adapters shape is credible, but the design does not yet provide implementable mechanisms for several normative safety and pagination claims. In particular, portable path-race closure and byte/metadata immutability are stronger than Python's stated mechanisms can prove.

Severity means: **MUST** blocks implementation or a stated requirement; **SHOULD** is material design debt likely to create rework or weak evidence; **COULD** improves precision or operability.

## MUST findings

### M1 — Observable metadata immutability is not portable as stated

**Conflict:** Requirements NFR-SAFE-001A and AJ-07 require every source byte *and metadata* to remain identical. Design §§9–10 necessarily enumerate and read directories, files, the index and objects, while §14 merely asserts that runtime writes no files. Reads can update access-time or other filesystem metadata on Windows, POSIX and mounted filesystems; Python provides no portable way to suppress this for every operation. The acceptance condition is therefore not realistically achievable.

**Correction:** Narrow NFR-SAFE-001A/AJ-07 to content plus mutation-relevant metadata (names, types, size, mtime, mode/ACL where observable, index checksum, refs, object set and config), explicitly excluding access-time and OS-maintained read telemetry. If access-time preservation is essential, define validated filesystem profiles and native per-platform open flags, and mark unsupported profiles rather than claiming Python-wide portability.

### M2 — A fixed catalogue can expose new or rejected domain roots through the substrate

**Conflict:** Requirements FR-EST-007 and architectural invariant 3 require exclusive, most-specific ownership. Design §8 freezes the catalogue at startup and excludes only *admitted* domain roots. A domain created after startup, or a marked candidate rejected because of a source-ID collision/unreadability, can therefore remain reachable through substrate tree/search/document routes. This also undermines FR-EST-008's collision handling.

**Correction:** Maintain a fail-closed ownership guard independent of navigable sources. At minimum, exclude every observed marked/candidate domain root, including collided or unhealthy candidates, and revalidate the configured domain-directory boundary before every substrate traversal/read. Prefer an atomic catalogue refresh/version used by all use cases; if the directory changes, return `source_changed` and rebuild rather than falling through to substrate ownership.

### M3 — The path-race algorithm does not meet the per-I/O contract

**Conflict:** NFR-SAFE-002B requires the final target *and every parent component* to be checked immediately before and after every enumeration/read. Design §9 describes non-following metadata checks, then path resolution, a file handle check, and final identity/mtime comparisons. Path-based `os.scandir` plus before/after stat does not prove which directory was enumerated after a rename swap; Windows junction handling and final-handle validation require native handle APIs not identified in the package/dependency design. `O_NOFOLLOW` protects only the opened final component unless the entire POSIX walk is dirfd-relative.

**Correction:** Specify two concrete adapters: POSIX `openat`/`dir_fd` component walking with `O_NOFOLLOW`, retained directory descriptors and `fstat`; Windows `CreateFileW` component handles with `FILE_FLAG_OPEN_REPARSE_POINT`/`FILE_FLAG_BACKUP_SEMANTICS`, reparse-tag rejection, file-ID/volume checks and `GetFinalPathNameByHandleW`. Enumerate/read from the retained final handle, then recheck the whole retained chain. If ctypes/native code is rejected, weaken NFR-SAFE-002B to the evidence Python can actually provide and name the residual race.

### M4 — Infrastructure paths cross into the core and the main filesystem port violates interface segregation

**Conflict:** NFR-ARCH-001 says core entities/use cases shall not import filesystem details. Design §5 puts `canonical_root: Path` and `excluded_roots` on core `Source`, then §6 passes that object through application ports. `ConfinedSourceView` also combines counts, directory browsing, search, collections and document reads, so each use case depends on a port with unrelated reasons to change.

**Correction:** Keep the core/application `Source` as identity, kind, display facts and opaque boundary token. Let an adapter-owned registry map the token to native roots/exclusions. Split the port into `SourceMetrics`, `DirectoryBrowser`, `PathSearch`, `CollectionReader` and `DocumentReader` (shared confinement may remain an internal adapter component). Extend the fitness rule to forbid `pathlib`, `os`, `subprocess`, HTTP and renderer implementation imports in `core/` and `application/`.

### M5 — The document contract cannot satisfy the 2 MiB response limit

**Conflict:** Design §§5 and 12 model both `raw_text` and `rendered_html` in one document result, and `/document` has no mode query. For a permitted 1 MiB file, raw plus rendered text and JSON escaping can exceed NFR-SAFE-004's 2 MiB API cap even before metadata. FR-DOC-003 asks for a user-controlled mode, not simultaneous transfer; NFR-PERF-002 requires incremental payloads.

**Correction:** Make `mode=raw|rendered` part of `ReadDocument` and `/document`, returning exactly one representation. Define the pre-serialisation size check and a bounded `response_too_large` fallback. Keep common metadata in both modes; fetch the other mode on demand and key stale-response guards by source/path/mode.

### M6 — Relative-link ownership is asserted at the wrong boundary

**Conflict:** FR-DOC-006 permits internal navigation only after the final target is proven eligible and within the same exclusive source. Design §11 has `SafeMarkdownRenderer` rewrite links, but the `DocumentRenderer` port in §6 has no source catalogue/confinement capability and cannot safely decide existence, symlink/junction resolution, exclusion or cross-domain ownership.

**Correction:** Have Markdown parsing emit typed link candidates without active URLs. `ReadDocument` must resolve each candidate relative to the source document through a dedicated `LinkResolver`/confined path port, then a presenter emits an Explorer route only for a validated same-source Markdown target. Render all unresolved, excluded and non-HTTP schemes inert. Revalidate on navigation; rendering is not an authority grant.

### M7 — YAML bounds do not bound the JSON/result graph

**Conflict:** NFR-SAFE-003/004 require bounded safe content. Design §11 limits source bytes, aliases and composed nodes, but PyYAML `SafeLoader` can construct non-JSON-native tagged values (dates, sets, binary) and aliases can be duplicated during JSON encoding. A 128 KiB input can therefore fail serialisation or expand beyond the response budget despite the stated node count.

**Correction:** Define a JSON-safe frontmatter value algebra and normalisation rules. Reject unsupported tags/types, cap depth, scalar length, mapping/sequence cardinality and total normalised/serialised bytes, and either reject aliases entirely or account for expanded occurrences. Apply duplicate-key detection before construction and test recursive aliases, merge keys, dates, binary, sets and expansion bombs at N−1/N/N+1.

### M8 — Git non-mutation and non-execution controls are incomplete

**Conflict:** NFR-SAFE-001A/B and AJ-07 prohibit mutation and helper execution. Design §10 disables several known facilities, but does not require an absolute trusted Git executable, `GIT_NO_LAZY_FETCH=1`, clearing repository/worktree environment variables, or discovery/snapshotting of external `--absolute-git-dir` and `--git-common-dir`. A partial-clone read may lazily fetch and write objects; on Windows executable lookup from a source cwd needs an explicit trusted path. A worktree `.git` file may place refs/objects outside the source snapshot.

**Correction:** Resolve and validate the Git executable once before adopting any source cwd and invoke its absolute path. Build an allowlisted environment from scratch, including `GIT_NO_LAZY_FETCH=1` and null system/global config, with all `GIT_DIR`, worktree, object, replace-ref and optional-lock variables absent. Resolve top-level, absolute git dir and common dir with fixed commands; include all repository stores in AJ-07 snapshots or reject external stores. Enumerate the exact argv templates and prove no process other than that executable is spawned.

### M9 — Cursor semantics are internally inconsistent and do not define a stable page

**Conflict:** Requirements §9 requires deterministic cursor pagination. Design §9 says all cursors contain an offset and directory/result fingerprint, while §10 says commit cursors contain the last SHA instead. A last SHA is not a sufficient continuation position for `git log --topo-order`; page-relative abbreviation checks also do not make abbreviations collision-safe across the repository. Directory/search fingerprinting appears to require an unbounded full scan, conflicting with bounded traversal and the latency budgets.

**Correction:** Define cursor schemas per operation. For commits, sign `{version, source, pinned_head, skip}` and rerun `git log <pinned_head> --topo-order --skip=<skip> -n 51`; return `source_changed` only if the contract deliberately requires current HEAD stability. Ask Git for repository-unique abbreviations or show a fixed sufficiently long/full SHA. For tree/search, define a maximum candidate scan and snapshot fingerprint that can be computed within it; otherwise return a documented partial page rather than pretending a stable continuation exists.

### M10 — Capability transport can leak through the server's own request logging

**Conflict:** NFR-SAFE-005 requires an unguessable launch capability; NFR-OBS-001 constrains diagnostics. Design D-005 puts it in `?cap=...`. The initial request therefore sends the secret to `http.server`; the default `BaseHTTPRequestHandler` log includes the request target and can print the capability to stderr before JavaScript removes it.

**Correction:** Print `http://127.0.0.1:<port>/#cap=<value>` so the fragment never reaches HTTP, store it in `sessionStorage`, then replace the URL. Override all access/error logging to structured redacted fields. Compare the single bounded header with `hmac.compare_digest`; use a separate random key for cursors. Apply exact Host validation to static, health and API routes, and define Origin handling per route, including initial navigation/no-Origin.

### M11 — The standard-library server boundary is not actually bounded or contract-complete

**Conflict:** NFR-SAFE-004 caps 16 in-flight requests and FR-ERR-001 requires structured API failures. Design §§12 and D-002 say a semaphore is acquired before dispatch, but `ThreadingHTTPServer` normally creates a thread before handler dispatch. Default parse/size/method errors can be HTML, and no exact static-asset routing rule prevents generic path serving. Filesystem calls can also block indefinitely on problematic mounts despite FR-ERR-002's terminal-state promise.

**Correction:** Define a custom server that acquires a permit non-blockingly *before thread creation* and returns JSON 429 for API routes. Use `BaseHTTPRequestHandler`, never `SimpleHTTPRequestHandler`; serve an exact immutable asset manifest via package resources. Override every API error path, including 405, oversized URI/header and malformed request where controllable. Add browser-side deadlines that terminate visibly. Either isolate filesystem work in killable helper processes or narrow the timeout guarantee because Python threads cannot portably cancel blocked filesystem syscalls.

### M12 — The dependency is ranged, not pinned

**Conflict:** FR-RUN-001 requires a pinned PyYAML dependency. Design §§3 and 14 call `PyYAML>=6.0.3,<7` pinned, but that is a compatibility range and can resolve to different code over time.

**Correction:** Use an exact runtime pin (`PyYAML==<validated version>`) for v1, or change the requirement to a bounded compatible range and retain a lock/constraints file plus wheel/sdist evidence for every validated Python/OS profile. Test the built wheel from a clean environment with networking disabled after dependency installation.

## SHOULD findings

### S1 — Discovery outcomes and ordering need explicit contracts

Design §8 does not allocate FR-EST-003's NFC/case-folded ordering with original-path tie-break, FR-EST-004's ignored-name rule, or FR-EST-006's malformed/unreadable/non-git issue taxonomy. It also applies “extension policy to every component” in §9, which would incorrectly treat directory names as files. **Correction:** specify discovery states/codes and deterministic sort keys; apply extension allowlisting only to final regular files while applying depth/ignored/secret rules to every relevant component.

### S2 — The Markdown adapter has three responsibilities

Design §11 combines frontmatter parsing, Markdown parsing/sanitisation and route rewriting, creating multiple reasons to change and making independent safety evidence harder. **Correction:** split `FrontmatterParser`, safe-subset `MarkdownParser` and link-policy/presentation stages. Prefer a small explicit grammar or a well-audited parser followed by an independent allowlist sanitiser; do not rely on “escape before parsing” alone for encoded/control-character URL cases.

### S3 — API schemas and error mappings are not sufficiently specified for contract tests

Design §12 names routes and status/code groups but not endpoint DTO fields, nullability, page metadata or error retryability. It says 405 but provides no `method_not_allowed` code; `directory_limit` is ambiguous beside paginated 500-entry pages, and `path_type_changed` is not allocated in §9. **Correction:** add versioned request/response examples or JSON Schemas for every endpoint and a one-to-one exception→HTTP/code/retryable table, including discovery issues versus request errors and redaction rules.

### S4 — Performance budgets are allocated but not designed

NFR-PERF-001 gives end-to-end budgets. `GetOverview` in design §7 can perform counts, repository state and a commit page serially, while each Git process may consume three seconds; full search plus native handle checks and cursor fingerprinting may exceed 500 ms. **Correction:** assign per-stage budgets, minimise Git invocations with exact formats, parallelise independent overview operations behind an overall deadline where safe, and define scan cut-offs/partial semantics before implementation.

### S5 — “Runtime writes no files” ignores interpreter caches

NFR-SAFE-001C permits no persistent application state, while design §14 states an absolute no-file-write claim. Python may create `__pycache__` in a writable installation at runtime. **Correction:** distinguish Explorer-owned state from interpreter/package caches, test a read-only installed package, and either suppress bytecode writes from process start or revise the claim to the mutation evidence actually controlled.

### S6 — Browser accessibility needs state-transition detail

Design §13 names nested lists, roving focus, tabs and dialogs but not `tree`/`treeitem` state, focus when a focused descendant is collapsed/removed, paginated “load more” focus, overlay background inertness or announcement de-duplication. These are central to FR-NAV-006, FR-SRCH-002 and NFR-ACC-001. **Correction:** specify the keyboard/focus state machine and semantic pattern, then trace each behaviour to AJ-04 evidence at both required narrow configurations.

### S7 — Browser module cohesion remains too coarse

The layout in design §4 places overview, commits, collections, settings and document behaviour in one `views/content.js`, despite NFR-ARCH-002 and the cited UI god-object risk. **Correction:** give each tab/document reader a focused view module; keep API calls in `api.js`, state transitions in reducers and DOM-only rendering in views. Add a size/import rule only if it encodes this responsibility boundary rather than an arbitrary line limit.

### S8 — Architecture fitness tests check only one direction

Design §15 rejects core/application imports from adapters/delivery but does not prove adapters implement application-owned protocols without application depending on concrete constructors, nor retain NFR-ARCH-003's changed-file-set evidence. **Correction:** add composition-only concrete imports, forbidden-stdlib checks for inner layers, contract suites run against fake/real adapters, and an explicit adapter-swap fixture whose changed paths are asserted and retained.

## COULD findings

### C1 — Separate internal models from public DTOs

Design §5 carries sensitive roots in `Source`, while FR-TAB-005 intentionally exposes a source path only in authenticated Settings. A dedicated response-mapping layer would make accidental path leakage less likely. Define public DTOs per endpoint and require explicit conversion/redaction.

### C2 — Make process-scoped invalidation visible

Per-process capabilities and cursor keys mean copied cleaned URLs and old cursors fail after restart. Add an explicit `session_expired`/`invalid_cursor` UI route with relaunch guidance rather than collapsing this into a generic authentication error.

### C3 — Name the validated platform matrix

Design §17 correctly limits claims for unavailable browsers; apply the same discipline to filesystem controls. Record which Windows filesystem/reparse variants, macOS filesystem and Linux filesystems were executed, and label the rest standards-backed or unexecuted rather than treating “Windows/POSIX” as one proof.

## Traceability conclusion

The family allocation in design §16 is not yet enough to author the one-row-per-requirement ledger required by requirements §12. After the MUST corrections, the test specification can become the executable contract. Implementation should remain gated until it contains explicit evidence rows for each compound safety clause, especially NFR-SAFE-001A/B, NFR-SAFE-002B, NFR-SAFE-003/004/005, NFR-ARCH-003 and AJ-06/07.
