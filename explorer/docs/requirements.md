# MarkdownLLM Explorer — Requirements Specification

**Status:** design-ready; requirements and design cold-read findings reconciled; acceptance approval remains gated by the test trace ledger

**Version:** 0.4

**Date:** 2026-08-27

**Product name:** MarkdownLLM Explorer

**Delivery shape:** standalone, read-only local web application; native Windows installer first, source/Python package retained for development and future platforms

## 1. Purpose

MarkdownLLM domains are inspectable in principle—each is made of Markdown, YAML, directories and git—but are opaque to a stakeholder who does not work through a coding harness. The current estate therefore behaves like a black box to the CEO: there is no obvious entrance, no visual map of the substrate and domains, and no human-oriented way to read the files that define the system.

MarkdownLLM Explorer will make the substrate and its domain estate visible through a familiar, Perplexity-inspired browser interface. It will let a non-technical or technically curious user move from the estate, into a domain, through its file tree, skills, memory and commit history, and read Markdown as a styled document rather than raw source.

This is an exploration surface, not a second source of truth. Markdown files and git remain authoritative.

## 2. Source and evidence basis

This specification is derived from:

- The operator's problem statement and requested workflow on 2026-08-27.
- The observed Windows launch failure on 2026-08-27: `mdllm-explorer` was not installed or on `PATH`, and installing the repository root failed because the installable package lives under `explorer/`. This is the captured current-state evidence for the native-distribution increment.
- The user-supplied Perplexity screenshot `codex-clipboard-a7e4fac0-b4c0-4ffe-b907-ccd6b8e1adf2.png` (SHA-256 `9423dc8c66b6ed004c3ba0ba1fae58a20489dbbf1b014b06f24688b5f0bd81e3`), used as a visual vocabulary for a calm three-pane shell, compact navigation, tabs and dark styling. It is not a pixel-copy requirement and contains no governing instructions.
- MarkdownLLM framework sources pinned at `7bffcb162f01c5cc6afb98756eca58bc5c5f79fe`, especially the manifesto and universal workflow.
- Code Architect domain sources pinned at `c711d2a46225aaca471100e1eec2afceb02e751a`, especially the solution-delivery workflow, Clean Architecture rules, traceability lens, captured-reality principle and UI god-object anti-pattern.

Requirements are treated as hypotheses. Runtime observation and user acceptance may send the work back to requirements or design; that is a valid workflow transition, not a failure of execution.

## 3. Business outcome

The primary outcome is visibility: a stakeholder who does not use the filesystem or a coding harness can form an accurate mental model of what the MarkdownLLM substrate is, which domains exist, what one domain contains, what changed, and how to read its defining material.

The v1 product hypothesis is that a first-time user can, from the launch URL and the labels in the interface:

1. distinguish the substrate from the domain estate;
2. select a domain;
3. understand its recent activity from git commits;
4. find and open a skill;
5. find and open a memory thing such as an insight; and
6. switch theme without losing their place.

The implementation run may demonstrate that these routes exist and are internally coherent; it cannot certify that the CEO or another human formed an accurate mental model. Human usability acceptance remains an explicitly owned follow-up judgement, not an agent-inferred pass.

## 4. Users and jobs

### U1 — Executive explorer

Needs a low-friction way to see that the estate is structured, active and legible without understanding git commands, YAML syntax or repository layout.

### U2 — Domain operator

Needs to move quickly across the substrate and multiple local domain repositories, inspect recent changes, and read source documents without leaving the interface.

### U3 — Technical adopter

Needs a standalone, local-first tool that can point at another conforming MarkdownLLM substrate without being coupled to this repository or a specific harness.

## 5. Product boundaries

### In scope for v1

- Local substrate and nested-domain discovery.
- Read-only estate, tree, commit, skill, memory and Markdown views.
- A responsive browser interface with light and dark themes.
- A self-contained Windows installer and desktop launch surface that does not require an end user to install, update or configure Python.
- The existing Python package and command-line launch surface for development, automation and later non-Windows distribution work.
- Safe operation against real, heterogeneous domains in the local estate.

### Explicitly out of scope for v1

- Editing, creating, deleting, committing, pulling or pushing files.
- Chatting with an LLM or invoking domain skills.
- Remote repository cloning, authentication or multi-user hosting.
- Replacing the filesystem, git, `mdllm`, a coding harness or domain validation.
- Rendering arbitrary non-Markdown artefacts beyond a safe file summary/download affordance.
- Full-text indexing across the entire estate.
- Administrative settings beyond theme and visible runtime/source information.

## 6. Domain model

- **Substrate:** the configured MarkdownLLM framework root. It is always the top-level source.
- **Domain estate:** the set of discoverable nested repositories under the substrate's configured domain directory.
- **Source:** either the substrate or one domain. A source has a stable UI identifier, exclusive canonical filesystem root, display name, kind and optional git state. `substrate` is the substrate ID. A domain ID is `domain/` plus its domain-root-relative path normalised to NFC, `/` separators and Unicode case-folding, then percent-encoded. Collisions are reported and neither candidate is silently overwritten.
- **Tree node:** a directory or permitted file within a source root.
- **Skill:** a Markdown file within a source's `skills/` directory, when present.
- **Memory:** Markdown things that preserve or govern continuity, initially insights, conflicts, retrospectives and decisions under `things/`.
- **Commit:** a read-only git event belonging to one source repository.
- **Document:** a permitted file selected for inspection; Markdown documents have parsed frontmatter, raw source and rendered HTML.

## 7. Functional requirements

### Estate and source discovery

**FR-EST-001 — Configured root.** The application shall accept an explicit substrate root at launch and shall not depend on the current working directory after configuration.

**FR-EST-002 — Substrate identity.** The configured root shall appear first in navigation, named **MarkdownLLM** regardless of its folder name, beneath the group heading that names its role. Amended 2026-08-28: the source is the MarkdownLLM framework in every estate, so the item names the thing while the heading above it (FR-NAV-001) carries the role. The prior wording spent the item's label on a word already on screen.

**FR-EST-003 — Domain estate.** The application shall discover one directory level of domains from a configurable domain directory, defaulting to `domain/`, and present them by NFC/case-folded display name with original-path tie-breaking under **Domains**.

**FR-EST-004 — Conforming discovery.** A readable directory containing `AGENTS.md` or `.markdownllm` shall be admitted as a domain. A git marker alone is insufficient. Non-directories, reparse points/symlinks and the ignored names in the limits policy shall not appear as domains; an incomplete marked candidate shall receive a non-fatal discovery issue.

**FR-EST-005 — Independent repositories.** Commit history and git status for a domain shall be read from that domain's repository, not from the substrate repository.

**FR-EST-006 — Partial estate resilience.** One unreadable, malformed or non-git domain shall be represented with an actionable status where possible and shall not prevent other sources from loading.

**FR-EST-007 — Exclusive ownership.** Each admitted domain root and all of its descendants shall be excluded from substrate tree, search and document routes. Every path belongs to the most-specific admitted source root; no alternate route, relative link, case/separator variant, symlink, junction or encoded path may return it through another source.

**FR-EST-008 — Stable source identity.** APIs and browser URLs shall use only the source IDs defined in Section 6. Absolute paths shall not appear in identifiers, and source-ID collisions shall return an explicit discovery issue rather than aliasing a source.

### Navigation and source context

**FR-NAV-001 — Persistent estate rail.** The left rail shall provide expandable **Substrate** and **Domains** sections.

**FR-NAV-002 — Source selection.** Selecting the substrate or a domain shall update the main source context without a full browser-page reload.

**FR-NAV-003 — Lazy file tree.** An expanded source shall expose a nested, indented directory tree. Directories shall expand and collapse independently, and the application shall avoid loading file contents merely to build the tree.

**FR-NAV-004 — File selection.** Selecting a permitted file shall open that file in the main pane and retain the selected source and tree context.

**FR-NAV-005 — Location state.** Browser URLs shall contain a source ID, tab, document mode and encoded source-relative path only. Refresh/back/forward shall restore source, tab, file, mode and the file's ancestor expansion. Invalid, deleted or excluded targets shall retain the valid source context and show a stable terminal state.

**FR-NAV-006 — Responsive navigation.** At viewport widths of 900 CSS pixels or more the three regions shall be simultaneously available. Below 900 pixels the estate rail and context panel shall become labelled overlays with focus containment, Escape dismissal and focus return; every desktop capability shall remain reachable at 390×844 and at 320 CSS pixels with 200% zoom.

**FR-NAV-007 — Region collapse.** At viewport widths of 900 CSS pixels or more, the estate rail and the context panel shall each collapse and restore under an explicit control, yielding their width to the centre region, and the choice shall persist across reload. Collapse is not the sub-900 overlay: a collapsed region covers nothing and shall not adopt dialog role, modal state, sibling inertness or focus containment. Focus shall move to the control that replaces the one being hidden.

**FR-NAV-008 — Centre region overflow.** Content too wide for the centre region shall scroll horizontally within that region; the page body shall not scroll horizontally at any supported width. The split view shall reduce its columns to a declared minimum before the centre begins to scroll.

### Source tabs

**FR-TAB-001 — Overview.** Every source shall have an **Overview** tab showing source identity; counts of eligible files, skills and memory items under the same ownership/eligibility policy; repository state; and the first commit page from that source repository. Counts that hit a limit or cannot be computed shall be labelled partial or unavailable, never presented as complete.

**FR-TAB-002 — Commit evidence.** Commit history shall be newest-first, topologically ordered and reachable from the source repository's `HEAD`. Each row shall carry the full SHA and show a collision-safe abbreviation, subject, author name and ISO-8601 authored time with source offset. Results shall page within the limits table. Unborn, detached, non-git, corrupt, timed-out and empty states shall be explicit; domain history shall never fall through to the parent repository.

**FR-TAB-003 — Skills.** Every source shall have a **Skills** tab listing the Markdown files in `skills/`; if the directory is absent or empty, the interface shall say so without treating it as an error.

**FR-TAB-004 — Memory.** Every source shall have a **Memory** tab that recursively scans eligible Markdown files only beneath `things/insights/`, `things/conflicts/`, `things/retrospectives/` and `things/decisions/`. Folder is the initial group; a valid frontmatter `type` may refine the label. Missing, malformed or mismatched type is shown as an issue on the item rather than silently moving or dropping it. Duplicate IDs remain separate path-addressed documents and receive a visible warning. Absent groups are omitted; no memory things produces an explicit empty state.

**FR-TAB-007 — Commit contents.** Activating a commit shall list the paths that commit changed against its first parent, each classified as added, modified or deleted, ordered by path. Renames shall be reported as a delete beside an add. Each path shall be marked with whether this source may open it; a path git reports but the source excludes shall be listed and unopenable, never silently omitted and never openable. A commit whose file list exceeds the limits table shall be labelled partial. The comparison shall be an explicit revision pair — first parent against commit, or the empty tree against a root commit — so that a merge reports the paths it brought in rather than none. An entry that is not an ordinary file shall be listed and unopenable.

**FR-TAB-008 — Historical document.** Selecting an openable path within a commit shall present that file as that commit left it, as raw text, with the line ranges the commit added marked. The marking shall not depend on colour alone, and the changed line numbers shall be stated in text. Removed lines shall be neither rendered nor returned to the browser, and the view shall say so. Where the commit's change to the file is too large to determine line by line, the file shall still be served and the view shall say that the marking is unavailable, never that nothing changed rather than allowing their absence to read as an absence of removals. Historical content is raw-only: it shall not be rendered as Markdown, and no link within it shall be resolved.

**FR-TAB-009 — Memory grouping and disclosure.** Memory groups shall be presented in descending group order with titles ascending inside a group. Each group shall be an independently collapsible disclosure carrying its expanded state, and that state shall survive re-render and pagination. A collapsed group shall display a live count of its items so that items paged into it remain evidenced.

**FR-TAB-005 — Settings.** Every source shall expose a minimal **Settings** tab showing read-only source path, source kind, detected markers and theme controls. No write-capable repository settings are permitted in v1.

**FR-TAB-006 — Consistent opening.** Selecting a skill or memory item shall open the same document reader used by the file tree; these tabs are curated routes into source files, not duplicated content stores.

### Document reading

**FR-DOC-001 — Styled Markdown.** Markdown shall render as a readable document with headings, paragraphs, emphasis, links, lists, blockquotes, tables, horizontal rules and fenced code blocks.

**FR-DOC-002 — Frontmatter.** YAML frontmatter shall be parsed separately and shown as structured metadata; it shall not be rendered as an undifferentiated code block. Metadata shall be shown in full: a fixed display cap is not permitted, because it leaves a reader unable to distinguish a short frontmatter from a truncated one. Raw mode shall not repeat the frontmatter disclosure, the block being already on screen in the source itself.

**FR-DOC-003 — Source visibility.** The reader shall provide a user-controlled switch between rendered Markdown and raw source.

**FR-DOC-004 — Context panel.** The right context panel shall summarise the selected source or document using factual metadata: path, file size, modified time, frontmatter fields and source/repository identity. It shall not invent a semantic summary.

**FR-DOC-009 — Reference navigation.** Frontmatter fields that name other things rather than describe this one shall be presented as controls that open the thing they name, carrying the relation or commit the reference declares. Resolution shall not delay the document: it shall run after the document is displayed, and a reference shall not be activatable before its resolution is known. A reference that resolves to nothing, to more than one thing, or whose lookup fails or times out shall settle into an explicitly unresolved state; no reference shall remain pending indefinitely, and a superseded lookup shall not settle chips a newer one is resolving. Where the source's index is incomplete, an unfound reference shall be reported as unchecked rather than as absent, and a source being written while it is read shall yield an incomplete index rather than an error.

**FR-DOC-005 — Unsupported files.** Eligible non-Markdown files shall receive a non-executable raw-text view when UTF-8 text and an explicit unsupported state when binary or non-UTF-8.

**FR-DOC-006 — Links.** Relative links to eligible Markdown files shall navigate inside Explorer only when the final target remains in the same exclusive source. Labelled `http` and `https` links may open externally with no opener or referrer. All other schemes, repository-supplied images/subresources and excluded targets shall be inert.

**FR-DOC-007 — File eligibility.** Only regular files with an eligible name and extension are exposed. Defaults permit `.md`, `.markdown`, `.txt`, `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.cfg`, `.csv`, `.tsv`, `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.jsx`, `.css`, `.html`, `.xml`, `.sh`, `.ps1`, `.bat` and extensionless `AGENTS`, `README`, `LICENSE` or `CHANGELOG` names. Defaults exclude dotfiles other than `.markdownllm`; `.git`, caches/build/dependency directories from the limits policy; environment, credential, token, private-key and certificate name patterns; device files; reparse points/symlinks; and every file outside exclusive ownership. Excluded items disclose no body through tree, search, metadata, error or download routes. v1 has no arbitrary-file opt-in.

**FR-DOC-008 — Encoding and changing files.** UTF-8 and UTF-8 with BOM are the supported text encodings; a NUL byte classifies content as binary. Malformed YAML frontmatter leaves escaped raw source available within limits, while rendered mode shows `frontmatter_invalid` and no inferred metadata. A file missing, replaced, changed to a directory, oversized, unreadable or changed during read returns a distinct stable error without clearing unrelated source context. Binary content is never decoded or embedded.

### Search and filtering

**FR-SRCH-001 — Source-local search.** The user shall be able to filter the active source's known paths by case-insensitive filename/path text.

**FR-SRCH-002 — Keyboard access.** Search, tab selection, tree navigation, theme controls and document mode shall be operable by keyboard.

### Theme and visual language

**FR-UI-001 — Perplexity-inspired shell.** The desktop composition shall use a restrained three-region layout: estate/tree rail, main evidence pane, and contextual detail panel. It shall reproduce the reference's clarity and density without copying unrelated controls or branding.

**FR-UI-002A — Theme choices.** The application shall offer light, dark and system theme choices and render every view in each choice.

**FR-UI-002B — Theme default.** With no saved choice, the application shall follow the browser's system colour-scheme preference.

**FR-UI-002C — Theme persistence.** An explicit light/dark/system choice shall persist in browser-local storage and survive reload without changing source/tab/file location.

**FR-UI-003 — Visual hierarchy.** The selected source, active tab, selected tree item, actionable control, empty state and error state shall be visually distinct in both themes.

**FR-UI-004 — No false controls.** Controls shown in v1 shall work. Placeholder share, usage, account, edit or chat controls shall not be displayed.

### Runtime and error behaviour

**FR-RUN-001 — Standalone distribution.** v1 shall retain the installable `explorer/` Python package for development and automation, and shall add a native Windows installer as the primary operator-facing distribution. Both forms include all browser assets and the pinned YAML runtime. The Windows-installed application shall contain its own Python runtime and dependencies; no system Python, `pip`, Node, CDN or internet access is required after the installer artefact has been obtained. The command-line form shall continue to print the resolved root and capability-bearing loopback URL, reject invalid configuration with non-zero exit, and terminate within five seconds of interrupt.

**FR-RUN-002 — Safe bind and lifecycle.** The server shall bind only to `127.0.0.1` by default, accept `--port` or choose an available port, print the actual URL, reject a non-loopback bind, isolate concurrent instances by launch capability, and never expose itself on all interfaces. A port collision shall exit non-zero rather than selecting a different requested port.

**FR-RUN-003 — Health.** A health endpoint shall report application availability without enumerating private estate contents.

**FR-RUN-004 — Native Windows installation.** Windows v1 shall be delivered as one double-clickable setup `.exe`. It shall install per user without administrator rights, register an uninstaller, validate and retain the selected MarkdownLLM substrate root, and create working Start Menu and Desktop shortcuts. The normal interactive path shall require no command line and shall offer to launch Explorer when setup completes.

**FR-RUN-005 — Desktop application launch.** Activating either installed shortcut shall start the bundled local service without a console window, open the capability-bearing URL in the user's default browser, and expose a notification-area icon with **Open Explorer** and **Exit Explorer** actions. A second activation while the same user instance is running shall ask the existing process to open its browser rather than creating a second server or persisting the capability outside process memory.

**FR-RUN-006 — Upgrade and uninstall.** Re-running the same-or-newer installer shall replace the installed application in place, preserve the selected substrate root and maintain one shortcut of each requested kind. Uninstall shall stop/remove the application, shortcuts, uninstaller registration and Explorer-owned installation settings while leaving the selected substrate and all of its repositories byte-identical.

**FR-ERR-001 — Structured failures.** API failures shall use `{code, message, retryable, source_id?, relative_path?}` and the error/status table in the design, with no document body or absolute path by default. The UI shall render recoverable contextual messages, and retry shall preserve location.

**FR-ERR-002 — Terminal and current loading states.** Every loading operation shall end in content, empty or error state. Older responses shall be cancelled or ignored by request identity and shall not populate a newer source context; there shall be no indefinite spinner after a request settles or times out.

## 8. Quality requirements

**NFR-ARCH-001 — Dependency direction.** Core entities and use cases shall not import HTTP, browser, filesystem, git-subprocess or concrete Markdown-rendering details. Application-owned ports shall define these seams; outer adapters shall implement them.

**NFR-ARCH-002 — Thin delivery layers.** HTTP handlers and browser event handlers shall translate input/output and delegate. Domain discovery, path policy, commit selection and document classification shall not live in controller/view code.

**NFR-ARCH-003 — Replaceability.** A controlled adapter-swap test shall show that replacing the HTTP server, git reader, filesystem reader or Markdown renderer changes no core/application file—only composition, the adapter and its adapter tests. The changed-file set is retained as evidence.

**NFR-SAFE-001A — Observable source immutability.** Explorer shall not alter source bytes or mutation-relevant metadata: names, types, size, content, mtime, mode/ACL where observable, worktree content, index checksum, refs, object set and repository config. Acceptance compares those pre/post snapshots. Access-time and OS-maintained read telemetry are explicitly excluded because ordinary reads may update them outside Explorer's control.

**NFR-SAFE-001B — Constrained git.** The git adapter shall expose an argument-vector allowlist of read-only operations whose arguments are fixed except for a full 40-character object identifier and, where a template requires one, a single source-relative path; a template carrying a path shall re-validate that path against traversal, absolute form, option-leading form, separator and control characters independently of any validation performed by its caller, and shall terminate option parsing before it;  set fixed source cwd, non-interactive environment, `GIT_OPTIONAL_LOCKS=0`, no pager/editor/hooks/external diff, bounded timeout/output and no shell; and prevent global/system/repository configuration from broadening execution. Mutation verbs and arbitrary options are not representable through its port.

**NFR-SAFE-001D — Historical read boundary.** Content read from the repository object store shall be governed by the same rules as a working-tree read: source admission, name eligibility, exclusive ownership, the file-size limit, binary classification and encoding support, reported with the same error codes. Admission shall be decided before any git invocation, because the object store retains every path the repository has ever contained, including paths the working-tree reader excludes today. Historical content shall not be rendered, and its links shall not be resolved, since a link in a historical file resolves against a tree that no longer exists.

**NFR-SAFE-001C — Outside-root writes.** The exploration runtime writes no Explorer-owned persistent content state. It may write diagnostic lines to stdout/stderr, ephemeral socket/process state managed by the operating system, interpreter/package bytecode caches outside every source root, and browser theme state in browser-local storage. The Windows installer may write only its per-user application files, uninstall registration, selected substrate-root setting and requested shortcuts. No capability, document content, frontmatter, source path below the configured root, content cache, token, log or database shall be persisted by the application.

**NFR-SAFE-002A — Root configuration confinement.** The launch root shall be an existing readable directory. The configured domain directory shall be source-relative, resolve beneath the launch root and reject absolute, UNC/device or escaping input.

**NFR-SAFE-002B — Per-I/O confinement.** Every directory enumeration and file read shall validate source-relative syntax, canonical ownership and non-link/reparse parent components immediately before I/O, then compare final directory/file identity and mutation metadata after I/O. File reads shall validate the opened native handle's final target where the validated OS exposes that evidence. Traversal, separator/case/encoding variants, symlinks, junctions/reparse points, UNC/device paths and detected replacement fail closed. Evidence names the executed filesystem/OS profiles and the residual race: v1 does not claim protection from a fully privileged local process that can replace path components between all checks.

**NFR-SAFE-003 — Content safety.** All repository strings shall be inserted as text or passed through an allowlist renderer. Raw mode is non-executable text; active repository HTML is never retained. Rendered documents load no repository subresource. Tests include script/event attributes, encoded schemes, SVG/data URLs, remote images and malformed markup.

**NFR-SAFE-004 — Resource limits.** Every traversal/read/process/response shall enforce the normative limits in Section 9. Limit failures have stable error codes; N−1, N and N+1 are tested.

**NFR-SAFE-005 — Local web boundary.** Estate APIs shall require an unguessable per-launch 256-bit capability delivered in the printed launch URL and then sent in a header. Requests shall accept only the launch-selected loopback Host and same Origin (or no Origin), emit no permissive CORS, use CSP `default-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store` and deny framing. Unauthenticated health returns only static availability/version data.

**NFR-PORT-001 — Portability.** Runtime code shall support Python 3.10+ on Windows 10+, macOS 13+ and maintained Linux distributions without assuming POSIX separators. This increment shall execute and retain a Windows 10+ x64 native bundle/installer profile; Linux and macOS native packaging are explicitly deferred rather than synthetically passed. The browser compatibility floor is Chromium 128+, Firefox 128+ and Safari 18+; this implementation run must execute runtime UI evidence in available Chromium and record standards/static inspection, rather than falsely claiming human acceptance on unavailable browsers.

**NFR-OFF-001 — Local-first.** Core exploration and Windows installation from the obtained setup artefact shall require no internet connection, separately installed Python, third-party service, CDN, Node runtime or browser extension.

**NFR-PERF-001 — Reproducible budgets.** Against fixture manifest `estate-scale-v1` (1 substrate, 13 independent domains, 2,500 eligible paths, 50 commits per repository) on a reference profile of at least 4 logical CPU, 8 GiB RAM, SSD and Python 3.10+, measure request start to terminal response in isolated fresh server processes. After one discarded warm-up, at least 19 of 20 runs shall meet: estate + first overview ≤2.0 s; directory page ≤300 ms; filename search ≤500 ms; 1 MiB document ≤500 ms; 50-commit page ≤500 ms. The evidence register records fixture hash, machine/OS/Python, cache conditions and raw timings. The private 2026-08-27 estate is an additional observational probe, not the reproducibility oracle.

**NFR-PERF-002 — Incremental payloads.** Estate, tree, document and commit data shall use separate endpoints so opening the application does not transfer every file body or every repository history.

**NFR-ACC-001 — Accessible interaction.** AJ-01–04 shall be checked against WCAG 2.2 AA for accessible names, semantic roles/states, focus order/visibility, traps and overlay focus return, tree keys, loading/error announcements, contrast/colour independence, 200% zoom, 320 CSS-pixel reflow, 24 CSS-pixel target minimum and reduced motion. Evidence records browser/OS/assistive-tool versions and any accepted exception; automated checks do not constitute a human accessibility ruling.

**NFR-TEST-001 — Deterministic core.** Core and use-case tests shall run without a browser, network, live git repository or the user's estate by using explicit fakes/fixtures at ports.

**NFR-TEST-002 — Captured reality.** System tests shall also exercise temporary real git repositories and representative real estate shapes, including independent nested repositories, malformed frontmatter, non-git domains and denied/oversized paths.

**NFR-OBS-001 — Explainable diagnostics.** Runtime log messages shall identify the operation and source without leaking document bodies. Expected per-domain failures shall be warnings; application-fatal failures shall be explicit.

## 9. Normative limits and eligibility defaults

These values are requirements, not implementation hints.

| Limit | Default / maximum |
|---|---:|
| Eligible file body and render input | 1 MiB |
| YAML frontmatter within body | 128 KiB |
| Directory depth below source root | 32 components |
| Directory entries per page | 500 |
| Search results per page | 200 |
| Eligible paths inspected by one count/search/collection operation | 10,000; result becomes partial at the cap |
| Memory candidates per source | 10,000 |
| Commits per page | 50 |
| Git process duration / captured output | 3 seconds / 1 MiB |
| JSON API response body | 2 MiB |
| Concurrent in-flight HTTP requests | 16; excess receives `server_busy` |
| Symlink/junction/reparse traversal | 0 hops; never followed |

Ignored directory names are `.git`, `.hg`, `.svn`, `.venv`, `venv`, `node_modules`, `.next`, `dist`, `build`, `coverage`, `.coverage`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `__pycache__`, `.bundle-build`, `.test-tmp` and `.uv-cache`. Excluded secret-bearing basename patterns, matched case-insensitively, include `.env` and `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`, `id_rsa*`, `id_ed25519*`, `*credential*`, `*secret*`, `*token*` and `*.kdbx`. An excluded name is never returned merely because its extension would otherwise be eligible.

The tree/history/search protocols use explicit `cursor` values and return `next_cursor` when another page exists. Counts become `partial: true` when any traversal limit prevents a complete answer.

## 10. Architectural invariants

1. Source files and git history are authoritative; Explorer maintains no shadow copy of domain content.
2. Selection never grants write authority.
3. A path belongs to exactly one selected source and never crosses that source root.
4. Domain git history is never accidentally read from the parent substrate repository.
5. Curated Skills and Memory views point to the same document identity as the general file tree.
6. Every asynchronous browser request terminates visibly as content, empty or error.
7. Rendering untrusted repository text cannot execute repository-supplied HTML or JavaScript.

## 11. Acceptance journeys

### AJ-01 — Executive-route demonstration

Given the captured local estate and only the launch URL, the tester opens Explorer, sees **Substrate** above **Domains**, selects a domain, identifies that domain as the owner of a shown commit, opens **Skills**, reads a styled skill, opens **Memory** to read an insight, and identifies files/git as read-only authority without using filesystem or git tooling. This demonstrates the intended route; it does not substitute for CEO usability acceptance.

### AJ-02 — Operator filesystem journey

An operator expands nested directories in the substrate tree, opens a Markdown specification, switches to raw source, follows a relative local link, uses browser back, and returns to the same expanded/selected context.

### AJ-03 — Imperfect estate

The estate contains a valid domain, a marked non-git domain, malformed frontmatter, a non-UTF-8 file, a symlink/junction escape, an excluded secret name, a file changed during read and an oversized file. The valid domain remains usable; each exceptional item ends in its specified empty/error/unsupported state; no excluded or outside-root content or metadata is returned.

### AJ-04 — Theme and responsive journey

The tester selects dark theme, reloads, sees dark theme retained, then completes AJ-01 at 1440×900 and 390×844, keyboard-only at 320 CSS pixels/200% zoom, with the accessibility states in NFR-ACC-001 and no lost capability.

### AJ-05 — Independent launch

In a clean Python virtual environment and from outside the MarkdownLLM repository, the tester installs the `explorer/` artefact, launches `mdllm-explorer --root <fixture>` against a temporary conforming substrate and receives the same substrate/domain model without source edits or a JavaScript toolchain. Invalid root, requested-port collision and interrupt behaviour are also observed.

### AJ-06 — Hostile local-web boundary

The tester attempts missing/wrong capabilities, hostile Host and Origin values, permissive CORS, framing, unsafe Markdown/URL payloads, excluded secret paths, encoded traversal and a cross-domain file through the substrate route. Every request is denied or safely inert as specified; health reveals no estate value.

### AJ-07 — Read-only observation

The tester snapshots fixture source contents and mutation-relevant metadata from NFR-SAFE-001A, git index, refs, object set and config; runs AJ-01–06 plus commit browsing; and compares the post-run snapshot. Those values are identical and no git helper, hook, pager, editor, lazy fetch or shell was invoked. Access-time and OS-managed read telemetry are recorded as excluded rather than falsely asserted unchanged.

### AJ-08 — Windows first installation

On a Windows profile with no usable `mdllm-explorer` command and with network blocked, the tester double-clicks the setup artefact, selects a temporary conforming substrate, completes a per-user install without elevation, and observes exactly one Desktop shortcut, one Start Menu shortcut and one Add/Remove Programs entry. Launching from the completion page opens the working Explorer in the default browser without consulting system Python.

### AJ-09 — Desktop relaunch and single instance

With Explorer installed, the tester activates the Desktop shortcut, observes the browser open and the notification-area icon appear, uses **Open Explorer**, then activates the Desktop shortcut again. The existing instance opens the UI and the listening-process count remains one. **Exit Explorer** closes the server and notification-area icon within five seconds.

### AJ-10 — Upgrade and uninstall

The tester installs the same build over itself, verifies the selected substrate root and singleton shortcuts are preserved, then uninstalls. Installed files, shortcuts, registration and Explorer-owned settings are removed; the substrate and an unrelated outside directory match independent pre/post snapshots.

## 12. Verification and acceptance ownership

The test specification is the approval ledger and must contain one row for every individual `FR-*` and `NFR-*` ID: verification method (`test`, `inspection`, `analysis` or `demonstration`), fixture, observable pass condition, test/evidence identifier, evidence location and acceptance owner. Journey ranges or a green suite alone do not establish coverage. Any compound clause that needs separate evidence receives separate test cases or is split here before implementation.

Requirements status remains **design-ready, not acceptance-approved** until that ledger has no uncovered ID. The design may proceed because its purpose is to decide how to satisfy the requirements; implementation may not begin until the test specification closes this gate.

Technical verification is owned by the implementation run and its retained evidence. Product acceptance is owned by Janosh Moshiri. CEO usability acceptance is owned by the CEO or a delegated U1 representative; the agent shall report it as pending unless that human judgement is actually supplied.

## 13. Assumptions and open hypotheses

- **H1 — Python remains the implementation language, not an end-user prerequisite.** It maximises reuse of the substrate's runtime knowledge. The Windows installer must bundle that runtime behind a native application boundary; Go remains unjustified unless the bundled result fails measured distribution, startup or support requirements.
- **H2 — Read-only is sufficient for first value.** Visibility is the named business problem; editing would introduce authority, validation and concurrency concerns before the visibility hypothesis is tested.
- **H3 — Perplexity's spatial model transfers.** The familiar rail/tabs/context layout should lower orientation cost, but user acceptance must judge this rather than visual similarity alone.
- **H4 — `domain/` plus markers describes the estate.** Discovery must be configurable because public adopters may use another directory name.
- **H5 — Lightweight Markdown support is enough only if it renders the substrate's real documents faithfully.** The renderer shall be tested against captured representative files, including tables, fenced code and frontmatter.

## 14. Definition of done

The v1 increment is done only when:

- the requirements, design and test specifications have completed their requested cold-read cycles;
- every requirement is implemented, explicitly deferred, or rejected with rationale;
- automated unit, contract, integration, security and UI tests pass;
- runtime tests exercise the captured real estate and temporary independent estates;
- the ten acceptance journeys have recorded technical pass/fail evidence and human-owned judgements are labelled accepted or pending;
- visual inspection has been completed in light and dark themes at desktop and narrow viewports;
- two cold code-review passes have been reconciled;
- the Windows setup artefact installs offline, creates valid shortcuts, opens the browser, handles reactivation, upgrades and uninstalls from a clean process; and
- the working tree is committed with no unexplained changes.
