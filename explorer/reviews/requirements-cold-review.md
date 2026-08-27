# Cold review — MarkdownLLM Explorer requirements

## Basis and verdict

Independent review of `explorer/docs/requirements.md` v0.1 at commit `e1ef1bf5353de5e69fecf24d40cc6e9172e7e8d2`; the target had no working-tree delta. No design or implementation was inspected.

The business problem is coherent and the v1 boundary is disciplined, but the specification is not yet acceptance-ready. Its highest risks are contradictory source ownership, an untestable read-only/security boundary, an undefined browsable-file policy, and non-reproducible usability, performance and distribution claims. Findings: **12 MUST, 10 SHOULD, 3 COULD**.

## MUST findings

### MUST-01 — Nested roots contradict exclusive source ownership
**Refs:** Section 6; FR-EST-003; FR-NAV-003; FR-DOC-006; invariants 3–4. A domain file is physically beneath both substrate and domain roots, yet each path must belong to one source. **Replace/add:** “**FR-EST-007 — Exclusive ownership.** Each admitted domain root and its descendants shall be excluded from substrate tree/document routes. Assign every path to the most-specific admitted root; no alternate route, relative link, symlink, junction or path spelling may return it through another source.” Verify all four route classes against one domain file.

### MUST-02 — Read-only is not observable and git may still mutate or execute helpers
**Refs:** Product boundaries; NFR-SAFE-001; NFR-OBS-001; invariants 1–2. Blanket avoidance of file-write APIs conflicts with diagnostics and does not constrain git locks, index refresh, pagers, helpers or repository config. **Replace:** “**NFR-SAFE-001A.** Explorer shall not alter any byte or metadata under a source root, including worktree, index, refs, objects and config; acceptance compares pre/post filesystem and git snapshots. **001B.** Git uses a command/argument allowlist, no shell/pager/editor/hooks/external diff or optional locks, fixed cwd, non-interactive environment, timeout and output cap; repository config cannot broaden execution. **001C.** Enumerate permitted outside-root writes; default diagnostics use stderr and no persistent server state.”

### MUST-03 — Loopback is not a confidentiality boundary
**Refs:** FR-RUN-002–003; NFR-SAFE-003; FR-DOC-004; FR-TAB-005. APIs expose private paths/content but have no Host, Origin, CORS, DNS-rebinding or framing policy. **Add:** “**NFR-SAFE-005 — Local web boundary.** Accept only loopback and the launch-selected Host/Origin; reject others, emit no permissive CORS, use restrictive CSP, `frame-ancestors 'none'`, `nosniff` and no-referrer. Estate APIs require an unguessable per-launch capability or equivalently tested defence. Unauthenticated health returns no estate-derived value.”

### MUST-04 — “Permitted file” is undefined and can expose secrets
**Refs:** Sections 5–6; FR-NAV-004; FR-DOC-005; NFR-SAFE-004. Raw-text/metadata views can disclose `.env`, keys and credentials. **Add:** “**FR-DOC-007 — Eligibility.** Only regular files passing a documented source-relative policy are exposed. Defaults exclude repository internals, configured ignores, credential/environment/key files, caches, devices and files outside exclusive ownership. Define name/extension rules and precedence. Excluded files reveal no body through tree, search, metadata, errors or downloads.” Arbitrary-file access needs explicit launch opt-in and separate acceptance.

### MUST-05 — Content safety omits URLs, subresources and raw mode
**Refs:** FR-DOC-001, 003, 005–006; NFR-SAFE-003; invariant 7. Markdown can load remote resources or unsafe schemes; raw text may execute if inserted/served incorrectly. **Replace:** “All repository strings are text-inserted or allowlist-sanitised. Raw mode is non-executable text. Rendered documents load no repository-supplied subresources. Only same-source Explorer links and labelled `http`/`https` links remain active; other schemes are inert. External links send no referrer/opener. Test event attributes, encoded schemes, SVG/data URLs, remote images and malformed markup.”

### MUST-06 — Confinement omits configuration escape and path races
**Refs:** FR-EST-001, 003–004; NFR-SAFE-002; AJ-03. The configurable domain path could escape root, and resolve-then-read can race. **Replace:** “Launch root must be an existing readable directory; domain directory must resolve beneath it and cannot be absolute/escaping. Validate the final native target immediately for each I/O against the exclusive canonical boundary, covering traversal, separator/case variants, symlinks, junctions, UNC/device paths and link replacement. Fail closed if stable-target enforcement is unavailable.” Test each supported OS mechanism.

### MUST-07 — Resource limits have no values
**Refs:** FR-NAV-003; FR-TAB-001–002; FR-SRCH-001; NFR-SAFE-004; NFR-PERF-002. No maximum governs bytes, depth, entries, commits, processes or concurrency. **Replace:** “A normative, versioned limits table shall give numeric defaults/bounds for file and frontmatter bytes, render input, depth, entries, symlink hops, commits/page, response bytes, concurrent requests and git duration/output. Tree/history paginate within them; limit errors have stable codes. Test N−1/N/N+1.” Values cannot remain design defaults.

### MUST-08 — First-time-user success is not measurable
**Refs:** Section 3; AJ-01; AJ-04; H3. Journeys do not prove “without instruction” or an “accurate mental model”. **Add:** “**NFR-UX-001.** With at least five U1-matching first-time participants given only the launch URL, at least four correctly distinguish substrate/domains, identify a commit’s repository, open one skill and memory item, and explain read-only/source authority. Predefine fixture, wording, permitted prompts, thresholds and evidence.” Otherwise remove those claims from v1 and retain them as hypotheses.

### MUST-09 — Verification completeness is deferred
**Refs:** Section 11; all FR/NFR IDs; Section 13. Range mappings do not give individual pass conditions or evidence. **Replace:** “Before requirements approval, every FR/NFR has one trace row: method (`test`, `inspection`, `analysis`, `demonstration`), fixture, observable pass condition, evidence artefact/location and acceptance owner. Split clauses needing different evidence. Journey-range references do not establish coverage.”

### MUST-10 — Performance cannot be reproduced
**Refs:** NFR-PERF-001–002; captured estate claim. Machine, fixture hash, cache/process state and start/end event are absent; 20 “warm” runs are ambiguous. **Replace:** “Against fixture manifest `<id/hash>` and benchmark profile `<CPU/RAM/storage/OS/Python/browser>`, measure navigation start to terminal overview. After one discarded warm-up, 19/20 isolated runs complete within 2.0 s; state application/filesystem cache conditions and retain raw timings.” Add comparable budgets/fixture sizes for tree, search, document and commit page.

### MUST-11 — Standalone distribution is undefined
**Refs:** Delivery shape; U3; FR-RUN-001; NFR-PORT-001; NFR-OFF-001; AJ-05; H1; “clean process”. Package/script/binary, dependency acquisition and offline boundary are unclear. **Replace:** “v1 ships as `<artefact>` containing server/browser assets. From a defined clean supported account with Python 3.10+ and no Node, `<install step>` yields command `<command>`, runnable from any cwd with `--root`. State whether installation may use a network; post-install launch/exploration may not. Pin dependencies; print URL/resolved root; invalid config exits non-zero; interrupt terminates cleanly.”

### MUST-12 — Malformed/changing file outcomes are missing
**Refs:** FR-DOC-002, 005; FR-ERR-001–002; AJ-03; NFR-TEST-002; H5. Encoding, text/binary detection, malformed frontmatter and list/read races are unspecified. **Add:** “**FR-DOC-008.** Define encodings and deterministic text/binary classification. Malformed frontmatter leaves escaped raw source available within limits, while rendered mode shows a stable parse error and no inferred metadata. Missing/replaced/type-changed/oversized/unreadable files return distinct stable errors without clearing unrelated context. Binary content is never decoded or embedded actively.”

## SHOULD findings

### SHOULD-01 — Domain “conformance” is too permissive
**Refs:** FR-EST-003–004; H4; U3. Any `.git` child qualifies. **Replace:** admit readable `AGENTS.md` or `.markdownllm`; treat `.git` directory/worktree-file alone as a non-conforming repository shown only via explicit option. Enumerate default ignores, marker precedence, recursion depth and incomplete-marker statuses. Otherwise rename this repository discovery, not conforming discovery.

### SHOULD-02 — Stable source identity has no algorithm
**Refs:** Section 6 Source; FR-NAV-005. **Add:** substrate ID is `substrate`; domain IDs derive from canonical source-relative paths with documented case/Unicode normalisation and collision handling, contain no absolute path, and surface collisions rather than overwrite them.

### SHOULD-03 — Git semantics are underspecified
**Refs:** FR-EST-005; FR-TAB-001–002. Define ref (`HEAD`), reachable/first-parent policy, ordering, bounded page size, SHA collision expansion, author/committer timestamps and offset, dirty fields, unborn/detached/corrupt/timeout states, worktrees/submodules and repository-boundary enforcement.

### SHOULD-04 — “Counts” and “recent” are not comparable
**Refs:** FR-TAB-001; Section 3. Enumerate overview counts using the same eligibility/ownership rules; define recent commits as newest N under SHOULD-03 with paging and partial/unavailable labels.

### SHOULD-05 — URL state neither guarantees AJ-02 nor protects paths
**Refs:** FR-NAV-004–005; AJ-02. **Replace:** URLs contain source IDs and encoded relative paths only; refresh/back/forward restore source, tab, file, mode and ancestor expansion. Extra expansions may be session state. Invalid/deleted/excluded targets show a stable state while retaining valid source context.

### SHOULD-06 — Accessibility is broad in title but narrow in evidence
**Refs:** FR-SRCH-002; FR-NAV-003, 006; NFR-ACC-001; AJ-04. **Replace:** scope WCAG 2.2 AA to AJ-01–04 and test focus order/visibility, traps, tree keys, overlay focus return, selected/expanded/loading/error semantics and announcements, contrast/colour independence, 200% zoom, 320 CSS-pixel reflow, target size and reduced motion. Record browser/OS/assistive-tech versions and accepted exceptions.

### SHOULD-07 — Responsive/browser targets are undefined
**Refs:** FR-NAV-006; NFR-PORT-001; AJ-04. Replace “may”, “narrow”, “desktop”, “current” and “Safari-class” with required layouts at named widths/zoom, a breakpoint and labelled overlay behaviour; name minimum browser/OS versions and whether Safari means Safari or a named WebKit runner.

### SHOULD-08 — Error contract and async race handling are absent
**Refs:** FR-ERR-001–002; invariant 6. **Replace:** errors use `{code,message,source_id?,relative_path?,retryable}` plus an enumerated HTTP map, without bodies/absolute paths by default. Older responses are cancelled or ignored by request identity and cannot populate a newer context; retry preserves location.

### SHOULD-09 — Memory discovery is indeterminate
**Refs:** Section 6 Memory; FR-TAB-004; FR-DOC-002. Specify recursion, folder-vs-frontmatter grouping precedence, malformed/missing/mismatched type handling, duplicate-ID display, eligibility/limit application and whether any configurable directories are v1.

### SHOULD-10 — Compound requirements hide partial failure
**Refs:** FR-EST-004; FR-NAV-005; FR-DOC-005–006; FR-UI-002; FR-RUN-001–002; NFR-SAFE-002–004; NFR-ACC-001. Split clauses whenever they need different fixtures/methods/results (for example theme choice/default/persistence, internal/external links, bind/port/exposure). Each ID should have one observable disposition.

## COULD findings

### COULD-01 — Define runtime lifecycle
**Refs:** FR-RUN-001–002. Specify port-collision choice, multiple-instance isolation, shutdown deadline and stale-tab behaviour; print any automatically chosen port.

### COULD-02 — Define freshness while sources change
**Refs:** source authority statement; FR-TAB-001; FR-NAV-003; FR-DOC-004. Add observation time and manual source refresh that consistently invalidates tree/document/count/git caches; detect metadata/body mismatch. Automatic watching may remain out of scope.

### COULD-03 — Make ordering/time deterministic
**Refs:** FR-EST-003; FR-TAB-002; FR-DOC-004. Define Unicode/case/numeric sorting with tie-breaker; API timestamps use ISO 8601 offsets and UI labels source-versus-browser-local time.

## Claim audit and strengths

- Framework and Code Architect commit pins are good evidence anchors. The operator statement and screenshot lack immutable IDs/hashes; add an evidence register. The “substrate plus 13 domains” fixture also needs a privacy-safe manifest, relevant counts and content hash.
- Words including “safe”, “accurate”, “familiar”, “faithfully”, “responsive”, “recent”, “actionable”, “current” and “clean” are design intent until tied to criteria above.
- Make NFR-ARCH-003 inspectable: replacing an adapter changes no core/use-case file, only composition, that adapter and its tests; retain the changed-file evidence. Prove NFR-TEST-001 with an import-boundary test and a run without network or git on `PATH`.
- Confidence is raised by the aligned problem/users/exclusions, authoritative-source and no-false-controls principles, realistic imperfect-estate journey, explicit seams, and intent to build traceability. These strengths do not close the security or verification gaps.

## Decision

Do not approve v1 requirements for acceptance yet. Resolve the 12 MUSTs, then build the trace matrix against revised atomic IDs. The closeable gate is: exclusive source ownership; observable read-only/web/file boundaries; numeric limits; and reproducible usability, performance and distribution evidence.
