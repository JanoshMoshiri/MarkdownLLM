# MarkdownLLM Explorer — Requirements Specification

**Status:** reviewed draft awaiting cold read  
**Version:** 0.1  
**Date:** 2026-08-27  
**Product name:** MarkdownLLM Explorer  
**Delivery shape:** standalone, read-only local web application shipped with the MarkdownLLM substrate

## 1. Purpose

MarkdownLLM domains are inspectable in principle—each is made of Markdown, YAML, directories and git—but are opaque to a stakeholder who does not work through a coding harness. The current estate therefore behaves like a black box to the CEO: there is no obvious entrance, no visual map of the substrate and domains, and no human-oriented way to read the files that define the system.

MarkdownLLM Explorer will make the substrate and its domain estate visible through a familiar, Perplexity-inspired browser interface. It will let a non-technical or technically curious user move from the estate, into a domain, through its file tree, skills, memory and commit history, and read Markdown as a styled document rather than raw source.

This is an exploration surface, not a second source of truth. Markdown files and git remain authoritative.

## 2. Source and evidence basis

This specification is derived from:

- The operator's problem statement and requested workflow on 2026-08-27.
- The user-supplied Perplexity screenshot, used as a visual vocabulary for a calm three-pane shell, compact navigation, tabs and dark styling. It is not a pixel-copy requirement.
- MarkdownLLM framework sources pinned at `7bffcb162f01c5cc6afb98756eca58bc5c5f79fe`, especially the manifesto and universal workflow.
- Code Architect domain sources pinned at `c711d2a46225aaca471100e1eec2afceb02e751a`, especially the solution-delivery workflow, Clean Architecture rules, traceability lens, captured-reality principle and UI god-object anti-pattern.

Requirements are treated as hypotheses. Runtime observation and user acceptance may send the work back to requirements or design; that is a valid workflow transition, not a failure of execution.

## 3. Business outcome

The primary outcome is visibility: a stakeholder who does not use the filesystem or a coding harness can form an accurate mental model of what the MarkdownLLM substrate is, which domains exist, what one domain contains, what changed, and how to read its defining material.

Success means a first-time user can, without instruction:

1. distinguish the substrate from the domain estate;
2. select a domain;
3. understand its recent activity from git commits;
4. find and open a skill;
5. find and open a memory thing such as an insight; and
6. switch theme without losing their place.

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
- A standalone Python launch surface.
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
- **Source:** either the substrate or one domain. A source has a stable UI identifier, filesystem root, display name, kind and optional git state.
- **Tree node:** a directory or permitted file within a source root.
- **Skill:** a Markdown file within a source's `skills/` directory, when present.
- **Memory:** Markdown things that preserve or govern continuity, initially insights, conflicts, retrospectives and decisions under `things/`.
- **Commit:** a read-only git event belonging to one source repository.
- **Document:** a permitted file selected for inspection; Markdown documents have parsed frontmatter, raw source and rendered HTML.

## 7. Functional requirements

### Estate and source discovery

**FR-EST-001 — Configured root.** The application shall accept an explicit substrate root at launch and shall not depend on the current working directory after configuration.

**FR-EST-002 — Substrate identity.** The configured root shall appear first in navigation as **Substrate**, regardless of its folder name.

**FR-EST-003 — Domain estate.** The application shall discover domains from a configurable domain directory, defaulting to `domain/`, and present them alphabetically under **Domains**.

**FR-EST-004 — Conforming discovery.** A domain candidate shall be admitted when it is a directory within the configured domain directory and has an `AGENTS.md`, `.markdownllm`, or `.git` marker. Non-directories and ignored infrastructure directories shall not appear as domains.

**FR-EST-005 — Independent repositories.** Commit history and git status for a domain shall be read from that domain's repository, not from the substrate repository.

**FR-EST-006 — Partial estate resilience.** One unreadable, malformed or non-git domain shall be represented with an actionable status where possible and shall not prevent other sources from loading.

### Navigation and source context

**FR-NAV-001 — Persistent estate rail.** The left rail shall provide expandable **Substrate** and **Domains** sections.

**FR-NAV-002 — Source selection.** Selecting the substrate or a domain shall update the main source context without a full browser-page reload.

**FR-NAV-003 — Lazy file tree.** An expanded source shall expose a nested, indented directory tree. Directories shall expand and collapse independently, and the application shall avoid loading file contents merely to build the tree.

**FR-NAV-004 — File selection.** Selecting a permitted file shall open that file in the main pane and retain the selected source and tree context.

**FR-NAV-005 — Location state.** The selected source, tab and file shall be representable in the browser URL so refresh and browser navigation preserve location.

**FR-NAV-006 — Responsive navigation.** On narrow screens the estate rail and context panel may collapse into overlays, but every desktop capability shall remain reachable.

### Source tabs

**FR-TAB-001 — Overview.** Every source shall have an **Overview** tab showing source identity, summary counts and recent commits from that source repository.

**FR-TAB-002 — Commit evidence.** Each commit row shall show at least abbreviated SHA, subject, author and authored time. Empty and non-git histories shall have explicit states.

**FR-TAB-003 — Skills.** Every source shall have a **Skills** tab listing the Markdown files in `skills/`; if the directory is absent or empty, the interface shall say so without treating it as an error.

**FR-TAB-004 — Memory.** Every source shall have a **Memory** tab initially grouping Markdown things from `things/insights/`, `things/conflicts/`, `things/retrospectives/` and `things/decisions/`. Absent groups shall be omitted; a source with no memory things shall have an explicit empty state.

**FR-TAB-005 — Settings.** Every source shall expose a minimal **Settings** tab showing read-only source path, source kind, detected markers and theme controls. No write-capable repository settings are permitted in v1.

**FR-TAB-006 — Consistent opening.** Selecting a skill or memory item shall open the same document reader used by the file tree; these tabs are curated routes into source files, not duplicated content stores.

### Document reading

**FR-DOC-001 — Styled Markdown.** Markdown shall render as a readable document with headings, paragraphs, emphasis, links, lists, blockquotes, tables, horizontal rules and fenced code blocks.

**FR-DOC-002 — Frontmatter.** YAML frontmatter shall be parsed separately and shown as structured metadata; it shall not be rendered as an undifferentiated code block.

**FR-DOC-003 — Source visibility.** The reader shall provide a user-controlled switch between rendered Markdown and raw source.

**FR-DOC-004 — Context panel.** The right context panel shall summarise the selected source or document using factual metadata: path, file size, modified time, frontmatter fields and source/repository identity. It shall not invent a semantic summary.

**FR-DOC-005 — Unsupported files.** Permitted non-Markdown files shall receive a safe metadata/raw-text view when textual and an explicit unsupported state when binary.

**FR-DOC-006 — Relative links.** Relative links between local Markdown files shall navigate within Explorer when the target remains inside the same source root. External HTTP(S) links shall be visually distinguishable.

### Search and filtering

**FR-SRCH-001 — Source-local search.** The user shall be able to filter the active source's known paths by case-insensitive filename/path text.

**FR-SRCH-002 — Keyboard access.** Search, tab selection, tree navigation, theme controls and document mode shall be operable by keyboard.

### Theme and visual language

**FR-UI-001 — Perplexity-inspired shell.** The desktop composition shall use a restrained three-region layout: estate/tree rail, main evidence pane, and contextual detail panel. It shall reproduce the reference's clarity and density without copying unrelated controls or branding.

**FR-UI-002 — Themes.** The application shall support light, dark and system theme choices, default to system preference, and persist the user's explicit choice locally in the browser.

**FR-UI-003 — Visual hierarchy.** The selected source, active tab, selected tree item, actionable control, empty state and error state shall be visually distinct in both themes.

**FR-UI-004 — No false controls.** Controls shown in v1 shall work. Placeholder share, usage, account, edit or chat controls shall not be displayed.

### Runtime and error behaviour

**FR-RUN-001 — Standalone launch.** A user with supported Python shall be able to launch the application with one documented command and an optional root/path argument.

**FR-RUN-002 — Safe defaults.** The server shall bind to loopback by default, choose or accept a port, and never expose itself on all interfaces unless a future explicit option adds that authority.

**FR-RUN-003 — Health.** A health endpoint shall report application availability without enumerating private estate contents.

**FR-ERR-001 — Structured failures.** API failures shall return a stable error shape and suitable HTTP status; the UI shall render recoverable, contextual messages rather than hanging or silently clearing state.

**FR-ERR-002 — Terminal loading states.** Every loading operation shall end in content, empty or error state. There shall be no indefinite spinner state after a request settles.

## 8. Quality requirements

**NFR-ARCH-001 — Dependency direction.** Core entities and use cases shall not import HTTP, browser, filesystem, git-subprocess or concrete Markdown-rendering details. Application-owned ports shall define these seams; outer adapters shall implement them.

**NFR-ARCH-002 — Thin delivery layers.** HTTP handlers and browser event handlers shall translate input/output and delegate. Domain discovery, path policy, commit selection and document classification shall not live in controller/view code.

**NFR-ARCH-003 — Replaceability.** Replacing the HTTP server, git reader, filesystem reader or Markdown renderer shall require changes only in composition and the relevant adapter, plus its adapter tests.

**NFR-SAFE-001 — Read-only operation.** Application code shall not expose or call file write, git mutation, shell interpolation or subprocess APIs other than an argument-vector, read-only git invocation.

**NFR-SAFE-002 — Root confinement.** Every requested path shall be resolved and verified as remaining within its selected source root. Traversal segments, absolute-path injection and symlink/junction escape shall be rejected.

**NFR-SAFE-003 — Content safety.** Rendered Markdown and frontmatter values shall be escaped/sanitised so local documents cannot execute script or inject active HTML in the Explorer origin.

**NFR-SAFE-004 — Resource limits.** Directory traversal shall skip `.git`, dependency/build caches and configured ignored names. Individual file reads and API result sizes shall have explicit limits with visible error states.

**NFR-PORT-001 — Portability.** The supported baseline shall be Python 3.10+ and current Chromium, Firefox and Safari-class browsers on Windows, macOS and Linux. Path logic shall not assume POSIX separators.

**NFR-OFF-001 — Local-first.** Core exploration shall require no internet connection, third-party service, CDN, Node runtime or browser extension.

**NFR-PERF-001 — Bounded discovery.** On the captured 2026-08-27 local estate (substrate plus 13 domains), initial estate discovery and overview data shall complete within 2 seconds at the 95th percentile over 20 warm local runs on the development machine.

**NFR-PERF-002 — Incremental payloads.** Estate, tree, document and commit data shall use separate endpoints so opening the application does not transfer every file body or every repository history.

**NFR-ACC-001 — Accessible interaction.** Interactive controls shall have accessible names, visible focus, semantic roles and contrast suitable for WCAG 2.2 AA text/UI criteria. Colour shall not be the only carrier of selection or error state.

**NFR-TEST-001 — Deterministic core.** Core and use-case tests shall run without a browser, network, live git repository or the user's estate by using explicit fakes/fixtures at ports.

**NFR-TEST-002 — Captured reality.** System tests shall also exercise temporary real git repositories and representative real estate shapes, including independent nested repositories, malformed frontmatter, non-git domains and denied/oversized paths.

**NFR-OBS-001 — Explainable diagnostics.** Runtime log messages shall identify the operation and source without leaking document bodies. Expected per-domain failures shall be warnings; application-fatal failures shall be explicit.

## 9. Architectural invariants

1. Source files and git history are authoritative; Explorer maintains no shadow copy of domain content.
2. Selection never grants write authority.
3. A path belongs to exactly one selected source and never crosses that source root.
4. Domain git history is never accidentally read from the parent substrate repository.
5. Curated Skills and Memory views point to the same document identity as the general file tree.
6. Every asynchronous browser request terminates visibly as content, empty or error.
7. Rendering untrusted repository text cannot execute repository-supplied HTML or JavaScript.

## 10. Acceptance journeys

### AJ-01 — CEO first look

Given the captured local estate, a first-time user opens Explorer, sees **Substrate** above **Domains**, selects a domain, reads its recent commits, opens **Skills**, reads a styled skill and opens **Memory** to read an insight without using filesystem or git tooling.

### AJ-02 — Operator filesystem journey

An operator expands nested directories in the substrate tree, opens a Markdown specification, switches to raw source, follows a relative local link, uses browser back, and returns to the same expanded/selected context.

### AJ-03 — Imperfect estate

The estate contains a valid domain, a non-git domain, a malformed Markdown file, a symlink/junction escape and an oversized file. The valid domain remains usable; each exceptional item ends in a specific empty/error/unsupported state; no outside-root content is returned.

### AJ-04 — Theme and responsive journey

The user selects dark theme, reloads, sees dark theme retained, then uses the application at desktop and narrow viewport widths with keyboard-only navigation and no lost capability.

### AJ-05 — Independent launch

From outside the MarkdownLLM repository, a user launches Explorer against a temporary conforming substrate path and receives the same substrate/domain model without changing source code or installing a JavaScript toolchain.

## 11. Requirement-to-acceptance map

| Acceptance journey | Primary requirements |
|---|---|
| AJ-01 | FR-EST-001–006, FR-TAB-001–006, FR-DOC-001–004, FR-UI-001 |
| AJ-02 | FR-NAV-001–006, FR-DOC-001–003, FR-DOC-006, FR-SRCH-001 |
| AJ-03 | FR-EST-006, FR-DOC-005, FR-ERR-001–002, NFR-SAFE-001–004, NFR-TEST-002 |
| AJ-04 | FR-UI-002–004, FR-SRCH-002, NFR-ACC-001 |
| AJ-05 | FR-RUN-001–003, NFR-PORT-001, NFR-OFF-001, NFR-ARCH-001–003 |

The test specification must expand this into a requirement-level trace matrix. No functional or quality requirement may remain without at least one verification method and one acceptance disposition.

## 12. Assumptions and open hypotheses

- **H1 — Python is the right delivery language.** It maximises reuse of the substrate's runtime knowledge and enables a one-command local server. This remains subject to implementation evidence; Go is not justified unless Python fails a measured distribution or performance requirement.
- **H2 — Read-only is sufficient for first value.** Visibility is the named business problem; editing would introduce authority, validation and concurrency concerns before the visibility hypothesis is tested.
- **H3 — Perplexity's spatial model transfers.** The familiar rail/tabs/context layout should lower orientation cost, but user acceptance must judge this rather than visual similarity alone.
- **H4 — `domain/` plus markers describes the estate.** Discovery must be configurable because public adopters may use another directory name.
- **H5 — Lightweight Markdown support is enough only if it renders the substrate's real documents faithfully.** The renderer shall be tested against captured representative files, including tables, fenced code and frontmatter.

## 13. Definition of done

The v1 increment is done only when:

- the requirements, design and test specifications have completed their requested cold-read cycles;
- every requirement is implemented, explicitly deferred, or rejected with rationale;
- automated unit, contract, integration, security and UI tests pass;
- runtime tests exercise the captured real estate and temporary independent estates;
- the five acceptance journeys have recorded pass/fail evidence;
- visual inspection has been completed in light and dark themes at desktop and narrow viewports;
- two cold code-review passes have been reconciled;
- launch and usage documentation works from a clean process; and
- the working tree is committed with no unexplained changes.
