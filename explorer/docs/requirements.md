# MarkdownLLM Explorer — Requirements Specification

**Status:** 0.4.1 maintenance correction: persistent service and repaired macOS file reading/stop. The white-label increment remains deferred under the Desktop product decision; actual Mac acceptance and public Windows signing remain open.

**Version:** 0.7

**Date:** 2026-09-05

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
- For v0.5: the white-label plan `things/plans/explorer-white-label-presentation-2026-09.md` revision 1.2 (framework commit `8df56e0`, whose revision 1.1 at `9d77c57` fixed the design intent), the operator's direction of 2026-09-02 that the brand is a property of the organisation's install rather than of any domain, the Code Architect run `run-markdownllm-explorer-white-label-presentation` and its gate decision `white-label-explorer-through-install-local-presentation`, and the operator's chosen test identity: the name *Reverb* and the Reverb project's logo.
- For v0.6: the independent cold review of v0.5 at `8df56e0`, `explorer/reviews/white-label-requirements-cold-review-2026-09-02.md`, whose findings this version reconciles.

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

**White-label outcome (v0.5).** An organisation that adopts MarkdownLLM and reads its own domains through Explorer can present Explorer as its own tool: its name, mark, colours and vocabulary over the whole estate, and each domain under the name and description that domain declares. The brand is a property of the organisation's install, declared in one file at the root of its checkout, and of the build it distributes, declared in a build profile. It is never a property of a domain, never an Explorer control, and never an image taken from a repository. Two things no brand removes: the substrate item keeps the name MarkdownLLM, and the product's own name and version remain visible in Settings and on `/health`.

## 4. Users and jobs

### U1 — Executive explorer

Needs a low-friction way to see that the estate is structured, active and legible without understanding git commands, YAML syntax or repository layout.

### U2 — Domain operator

Needs to move quickly across the substrate and multiple local domain repositories, inspect recent changes, and read source documents without leaving the interface.

### U3 — Technical adopter

Needs a standalone, local-first tool that can point at another conforming MarkdownLLM substrate without being coupled to this repository or a specific harness.

### U4 — Adopting organisation

Runs its own domains on a MarkdownLLM checkout and needs Explorer to carry its identity for the people who read the estate: a name, a mark, colours and vocabulary declared once for the install, and an installer that carries the same identity to staff who never open the checkout.

## 5. Product boundaries

### In scope for v1

- Local substrate and nested-domain discovery.
- Read-only estate, tree, commit, skill, memory and Markdown views.
- A responsive browser interface with light and dark themes.
- A self-contained Windows installer and desktop launch surface that does not require an end user to install, update or configure Python.
- The existing Python package and command-line launch surface for development, automation and later non-Windows distribution work.
- Safe operation against real, heterogeneous domains in the local estate.
- Estate presentation from an install-local root file, declared identity from each domain's entry file, and a packaged default presentation and mark image placed by a build profile (v0.5).

### Explicitly out of scope for v1

- Editing, creating, deleting, committing, pulling or pushing files.
- Chatting with an LLM or invoking domain skills.
- Remote repository cloning, authentication or multi-user hosting.
- Replacing the filesystem, git, `mdllm`, a coding harness or domain validation.
- Rendering arbitrary non-Markdown artefacts beyond a safe file summary/download affordance.
- Full-text indexing across the entire estate.
- Administrative settings beyond theme and visible runtime/source information.
- Images, fonts or stylesheets loaded from a repository; per-user or per-viewer branding; per-domain marks and accents; renaming the frozen executable per brand; naming the macOS launcher's Application Support folder per brand (v0.5 defers these to later increments).

## 6. Domain model

- **Substrate:** the configured MarkdownLLM framework root. It is always the top-level source.
- **Domain estate:** the set of discoverable nested repositories under the substrate's configured domain directory.
- **Source:** either the substrate or one domain. A source has a stable UI identifier, exclusive canonical filesystem root, display name, kind and optional git state. `substrate` is the substrate ID. A domain ID is `domain/` plus its domain-root-relative path normalised to NFC, `/` separators and Unicode case-folding, then percent-encoded. Collisions are reported and neither candidate is silently overwritten.
- **Tree node:** a directory or permitted file within a source root.
- **Skill:** a Markdown file within a source's `skills/` directory, when present.
- **Memory:** eligible Markdown things grouped by their first directory immediately beneath `things/`, so each domain's emergent content structure is visible without product code changes.
- **Commit:** a read-only git event belonging to one source repository.
- **Document:** a permitted file selected for inspection; Markdown documents have parsed frontmatter, raw source and rendered HTML.
- **Declared identity:** the `name` and `description` a domain's `AGENTS.md` frontmatter declares. A domain is presented by them; its identifier, route and ownership are unaffected by them. The substrate's entry file is never read for identity.
- **Presentation:** the shell's identity record: name, tagline, text mark, optional packaged mark image, light and dark accents with their derived soft accents, and a vocabulary of labels for the rail headings, the source-kind line, the overview subtitle, and the Skills and Memory tab, count and empty-state captions.
- **Presentation source:** where each presentation field came from — `root_file` (the presentation file at the substrate root), `packaged_default` (the presentation embedded in the installed package by a build profile) or `product_default` (built into Explorer).

## 7. Functional requirements

### Estate and source discovery

**FR-EST-001 — Configured root.** The application shall accept an explicit substrate root at launch and shall not depend on the current working directory after configuration.

**FR-EST-002 — Substrate identity.** The configured root shall appear first in navigation, named **MarkdownLLM** regardless of its folder name, beneath the group heading that carries the presentation's `substrate` label (FR-PRES-004; default **Substrate**). Amended 2026-08-28: the source is the MarkdownLLM framework in every estate, so the item names the thing while the heading above it (FR-NAV-001) carries the role. The prior wording spent the item's label on a word already on screen. Amended 2026-09-02: the heading text is a presentation label; the item's name is not.

**FR-EST-003 — Domain estate.** The application shall discover one directory level of domains from a configurable domain directory, defaulting to `domain/`, and present each by its declared identity (FR-PRES-001), ordered by NFC/case-folded displayed name with original-path tie-breaking, under the group heading that carries the presentation's `domains` label (default **Domain estate**). When two sources' NFC/case-folded displayed names are equal, or a domain's equals the substrate's, each such domain shows its folder name after the declared name in the rail and the overview.

**FR-EST-004 — Conforming discovery.** A readable directory containing `AGENTS.md` or `.markdownllm` shall be admitted as a domain. A git marker alone is insufficient. Non-directories, reparse points/symlinks and the ignored names in the limits policy shall not appear as domains; an incomplete marked candidate shall receive a non-fatal discovery issue.

**FR-EST-005 — Independent repositories.** Commit history and git status for a domain shall be read from that domain's repository, not from the substrate repository.

**FR-EST-006 — Partial estate resilience.** One unreadable, malformed or non-git domain shall be represented with an actionable status where possible and shall not prevent other sources from loading.

**FR-EST-007 — Exclusive ownership.** Each admitted domain root and all of its descendants shall be excluded from substrate tree, search and document routes. Every path belongs to the most-specific admitted source root; no alternate route, relative link, case/separator variant, symlink, junction or encoded path may return it through another source.

**FR-EST-008 — Stable source identity.** APIs and browser URLs shall use only the source IDs defined in Section 6. Absolute paths shall not appear in identifiers, and source-ID collisions shall return an explicit discovery issue rather than aliasing a source.

### Navigation and source context

**FR-NAV-001 — Persistent estate rail.** The left rail shall provide two persistent sections, one for the substrate and one for the domains, headed by the presentation's `substrate` and `domains` labels (defaults **Substrate** and **Domain estate**). Neither section may be hidden by a presentation: each heading always carries a non-empty label, and a rejected or empty label yields the default.

**FR-NAV-002 — Source selection.** Selecting the substrate or a domain shall update the main source context without a full browser-page reload.

**FR-NAV-003 — Lazy file tree.** An expanded source shall expose a nested, indented directory tree. Directories shall expand and collapse independently, and the application shall avoid loading file contents merely to build the tree.

**FR-NAV-004 — File selection.** Selecting a permitted file shall open that file in the main pane and retain the selected source and tree context.

**FR-NAV-005 — Location state.** Browser URLs shall contain a source ID, tab, document mode, an optional document surface (`standalone` or `collection`), an optional full commit identifier and an encoded source-relative path only. A location that is not inside a commit shall not carry a commit identifier; a location without a document shall not carry a document surface. Refresh/back/forward shall restore source, tab, file, mode, document surface and the file's ancestor expansion. A legacy route without surface shall restore Skills/Memory documents into the collection reader and all other documents into the standalone reader. Invalid, deleted or excluded targets shall retain the valid source context and show a stable terminal state.

**FR-NAV-006 — Responsive navigation.** At viewport widths of 900 CSS pixels or more the three regions shall be simultaneously available. Below 900 pixels the estate rail and context panel shall become labelled overlays with focus containment, Escape dismissal and focus return; every desktop capability shall remain reachable at 390×844 and at 320 CSS pixels with 200% zoom.

**FR-NAV-007 — Region collapse.** At viewport widths of 900 CSS pixels or more, the estate rail and the context panel shall each collapse and restore under an explicit control, yielding their width to the centre region, and the choice shall persist across reload. Collapse is not the sub-900 overlay: a collapsed region covers nothing and shall not adopt dialog role, modal state, sibling inertness or focus containment. Focus shall move to the control that replaces the one being hidden.

**FR-NAV-008 — Centre region overflow.** Content too wide for the centre region shall scroll horizontally within that region; the page body shall not scroll horizontally at any supported width. The split view shall reduce its columns to a declared minimum before the centre begins to scroll.

### Source tabs

**FR-TAB-001 — Overview.** Every source shall have an **Overview** tab showing source identity with, beneath the name, the source's declared description or, when none is declared, the presentation's kind label for that source (FR-PRES-001, FR-PRES-004); counts of eligible files, skills and memory items under the same ownership/eligibility policy, labelled with the presentation's `skills` and `memory` labels; repository state; and the first commit page from that source repository. Counts that hit a limit or cannot be computed shall be labelled partial or unavailable, never presented as complete.

**FR-TAB-002 — Commit evidence.** Commit history shall be newest-first, topologically ordered and reachable from the source repository's `HEAD`. Each row shall carry the full SHA and show a collision-safe abbreviation, subject, author name and ISO-8601 authored time with source offset. Results shall page within the limits table. Unborn, detached, non-git, corrupt, timed-out and empty states shall be explicit; domain history shall never fall through to the parent repository.

**FR-TAB-003 — Skills.** Every source shall have a **Skills** tab listing the Markdown files in `skills/`; if the directory is absent or empty, the interface shall say so without treating it as an error.

**FR-TAB-004 — Memory.** Every source shall have a **Memory** tab that recursively scans eligible Markdown files beneath every first-level directory directly inside `things/`. The first-level directory is the group irrespective of frontmatter type; hyphens and underscores become spaces and the label is title-cased. A group with no eligible descendant Markdown is omitted. Missing or malformed frontmatter is shown as an issue rather than dropping the item, while a difference between folder name and frontmatter `type` is not an issue. Duplicate IDs remain separate path-addressed documents and receive a visible warning. The Overview Memory count and collection shall consume the same grouping policy; no memory things produces an explicit empty state.

**FR-TAB-007 — Commit contents.** Activating a commit shall list the paths that commit changed against its first parent, each classified as added, modified or deleted, ordered by path. Renames shall be reported as a delete beside an add. Each path shall be marked with whether this source may open it; a path git reports but the source excludes, or that is not an ordinary file, shall be listed and unopenable. A path whose spelling this source cannot represent at all is the one exception and is omitted, because it cannot be addressed by any route. A commit whose file list exceeds the limits table shall be labelled partial. The comparison shall be an explicit revision pair — first parent against commit, or the empty tree against a root commit — so that a merge reports the paths it brought in rather than none. An entry that is not an ordinary file shall be listed and unopenable.

**FR-TAB-008 — Historical document.** Selecting an openable path within a commit shall present that file as that commit left it, as raw text, with the line ranges the commit added marked. The marking shall not depend on colour alone, and the changed line numbers shall be stated in text. Removed lines shall be neither rendered nor returned to the browser, and the view shall say so. Where the commit's change to the file is too large to determine line by line, the file shall still be served and the view shall say that the marking is unavailable, never that nothing changed rather than allowing their absence to read as an absence of removals. Historical content is raw-only: it shall not be rendered as Markdown, and no link within it shall be resolved.

**FR-TAB-009 — Memory grouping and disclosure.** Memory groups shall be presented in descending group order with titles ascending inside a group. Each group shall be an independently collapsible disclosure carrying its expanded state, and that state shall survive re-render and pagination. A collapsed group shall display a live count of its items so that items paged into it remain evidenced.

**FR-TAB-005 — Settings.** Every source shall expose a minimal **Settings** tab showing read-only source path, source kind, detected markers, the identity fact of FR-PRES-001, the presentation facts in FR-PRES-005 and theme controls. No write-capable repository settings are permitted in v1.

**FR-TAB-006 — Consistent opening.** Selecting a skill or memory item shall use the same document-reading pipeline as the file tree while retaining its collection surface. File-tree and search selection use the standalone surface. A rendered local link, frontmatter reference, mode change, refresh, back or forward shall preserve the current surface and shall update the route, visible reader, context and selected tree identity together; these tabs are curated routes into source files, not duplicated content stores.

### Document reading

**FR-DOC-001 — Styled Markdown.** Markdown shall render as a readable document with headings, paragraphs, emphasis, links, lists, blockquotes, tables, horizontal rules and fenced code blocks.

**FR-DOC-002 — Frontmatter.** YAML frontmatter shall be parsed separately and shown as structured metadata; it shall not be rendered as an undifferentiated code block. Metadata shall be shown in full: a fixed display cap is not permitted, because it leaves a reader unable to distinguish a short frontmatter from a truncated one. Raw mode shall not repeat the frontmatter disclosure, the block being already on screen in the source itself.

**FR-DOC-003 — Source visibility.** The reader shall provide a user-controlled switch between rendered Markdown and raw source.

**FR-DOC-004 — Context panel.** The right context panel shall summarise the selected source or document using factual metadata: path, file size, modified time, frontmatter fields and source/repository identity. It shall not invent a semantic summary.

**FR-DOC-009 — Reference navigation.** The frontmatter fields that name other things rather than describe this one — `informed_by`, `linked_things`, `dependencies`, `blocks`, `parent`, `definition` and `parties` — shall be presented as controls that open the thing they name, carrying the relation or commit the reference declares and preserving the current document surface. Resolution shall not delay the document: it shall run after the document is displayed, and a reference shall not be activatable before its resolution is known. A resolved activation shall update the route, visible reader, context and selected tree identity together. A reference that resolves to nothing, to more than one thing, or whose lookup fails or times out shall settle into an explicitly unresolved state; no reference shall remain pending indefinitely, and a superseded lookup shall not settle chips a newer one is resolving. Where the source's index is incomplete, an unfound reference shall be reported as unchecked rather than as absent, and a source being written while it is read shall yield an incomplete index rather than an error.

**FR-DOC-005 — Unsupported files.** Eligible non-Markdown files shall receive a non-executable raw-text view when UTF-8 text and an explicit unsupported state when binary or non-UTF-8.

**FR-DOC-006 — Links.** Relative links to eligible Markdown files shall navigate inside Explorer only when the final target remains in the same exclusive source, preserving the current document surface and updating route, visible reader, context and selected tree identity together. Labelled `http` and `https` links may open externally with no opener or referrer. All other schemes, repository-supplied images/subresources and excluded targets shall be inert.

**FR-DOC-007 — File eligibility.** Only regular files with an eligible name and extension are exposed. Defaults permit `.md`, `.markdown`, `.txt`, `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.cfg`, `.csv`, `.tsv`, `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.jsx`, `.css`, `.html`, `.xml`, `.sh`, `.ps1`, `.bat` and extensionless `AGENTS`, `README`, `LICENSE` or `CHANGELOG` names. Defaults exclude dotfiles other than `.markdownllm`; `.git`, caches/build/dependency directories from the limits policy; environment, credential, token, private-key and certificate name patterns; device files; reparse points/symlinks; and every file outside exclusive ownership. Excluded items disclose no body through tree, search, metadata, error or download routes. v1 has no arbitrary-file opt-in.

**FR-DOC-008 — Encoding and changing files.** UTF-8 and UTF-8 with BOM are the supported text encodings; a NUL byte classifies content as binary. Malformed YAML frontmatter leaves escaped raw source available within limits, while rendered mode shows `frontmatter_invalid` and no inferred metadata. A file missing, replaced, changed to a directory, oversized, unreadable or changed during read returns a distinct stable error without clearing unrelated source context. Binary content is never decoded or embedded.

### Search and filtering

**FR-SRCH-001 — Source-local search.** The user shall be able to filter the active source's known paths by case-insensitive filename/path text.

**FR-SRCH-002 — Keyboard access.** Search, tab selection, tree navigation, theme controls and document mode shall be operable by keyboard.

### Theme and visual language

**FR-UI-001 — Perplexity-inspired shell.** The desktop composition shall use a restrained three-region layout: estate/tree rail, main evidence pane, and contextual detail panel. It shall reproduce the reference's clarity and density without copying unrelated controls or branding. The brand mark, name and small line in the rail, the window title and the accent colour shall be those of the resolved presentation (FR-PRES-003), and the product's own identity is the default. The document title is the presentation name on the estate and `<source display name> — <presentation name>` when a source is selected; it never carries a document path.

**FR-UI-002A — Theme choices.** The application shall offer light, dark and system theme choices and render every view in each choice.

**FR-UI-002B — Theme default.** With no saved choice, the application shall follow the browser's system colour-scheme preference.

**FR-UI-002C — Theme persistence.** An explicit light/dark/system choice shall persist in browser-local storage and survive reload without changing source/tab/file location.

**FR-UI-003 — Visual hierarchy.** The selected source, active tab, selected tree item, actionable control, empty state and error state shall be visually distinct in both themes.

**FR-UI-004 — No false controls.** Controls shown in v1 shall work. Placeholder share, usage, account, edit or chat controls shall not be displayed.

### Presentation and identity

**FR-PRES-001 — Declared domain identity.** A domain shall be presented by the `name` declared in its `AGENTS.md` frontmatter and described by its `description`, both read at discovery through the same confined, bounded reader and frontmatter parser as any document and admitted by the declared-identity grammar in Section 9. A `name` that is absent, not a string scalar or fails the grammar falls back to the folder name; a `description` that is absent, not a string scalar or fails the grammar falls back to the presentation's `domain_kind` label. The description is shown only as the overview subtitle; the topbar kind line always carries the kind label. Declared identity is read for domains only: the substrate's name is fixed by FR-EST-002, its overview subtitle is the presentation's `substrate_kind` label, and its entry-file frontmatter is never read for presentation. Declared identity never changes a source's identifier, route or ownership. Settings states whether a source's name is declared or a fallback and, for a fallback, the reason — `entry_missing`, `frontmatter_invalid`, `frontmatter_too_large` or `name_invalid`; a fallback is a Settings fact, not an estate issue.

**FR-PRES-002 — Root presentation file.** Explorer shall read `presentation.md`, an eligible Markdown file directly at the substrate root and matched exactly as `presentation.md` under the filesystem's own case rule, as the estate's presentation. Its YAML frontmatter may declare `name`, `tagline`, `mark`, `accent`, `accent_dark` and `labels` (a mapping with keys `substrate`, `domains`, `substrate_kind`, `domain_kind`, `skills` and `memory`); its body is ignored. The file is also a framework thing and may carry the thing fields (`id`, `type: presentation`, `status`, `version`, `created`, `tags`); Explorer ignores them and requires none. Each presentation field is validated independently against the presentation grammar in Section 9: a valid field applies; a field that is not a YAML string scalar, trims to empty or otherwise fails the grammar is rejected, and a non-mapping `labels` is rejected as one field; each rejection is reported as a `presentation_field_rejected` estate issue carrying `field`, `reason` and, for a contrast failure, the measured `ratio` and the `surface` it failed against; unknown keys are ignored. A presentation that declares `name` but no `mark` takes the first code point of `name` as its mark when that code point satisfies the mark grammar, else the product mark. A presentation that declares `name` but no `tagline` shows no tagline line. The file cannot declare, enable, replace or suppress an image. It is otherwise an ordinary eligible document: it appears in the substrate tree, search and counts and opens as a document. A `presentation.md` anywhere else, including a domain root, has no presentation effect.

**FR-PRES-003 — Presentation resolution.** The shell presentation shall be resolved once per discovery from three sources named `root_file`, `packaged_default` and `product_default`. The identity group — `name`, `tagline` and the text `mark` — resolves together from the first source that declares a valid `name`, so a name is never shown beside another source's tagline or mark. Every other field resolves independently: for each of `accent`, `accent_dark` and each label, the first source declaring a valid value wins, in the order root file, packaged default, product default, so a field the root file omits or declares invalidly takes the packaged value where one is declared and the product value otherwise. The packaged mark image is a packaged-only field: a root file can neither declare it nor displace it, it stays in the brand-mark slot whether or not a root file is present, and the text mark applies only where no mark image is packaged. A root file whose frontmatter is absent or declares none of the presentation fields contributes nothing and is reported as a `presentation_empty` estate issue. A root entry that is not a regular, readable, eligible file, or a frontmatter the document parser rejects as a whole (duplicate or merge keys, aliases, unsupported tags, exceeded limits, a non-mapping), yields a `presentation_unavailable` estate issue and contributes nothing; an absent file contributes nothing silently; only field-level failures yield `presentation_field_rejected`. No presentation failure shall prevent discovery or leave the shell without a presentation. The estate response shall name, for every field, the source that supplied it. Presentation is fixed for one process, like the source catalogue; it changes by editing the root file or rebuilding the package and restarting Explorer. A document view of an entry file or the root file is a live read, so an edit made while Explorer runs is visible in the document before it is visible in the shell.

**FR-PRES-004 — Presentation vocabulary.** The label map shall reach exactly: the two rail group headings; the topbar kind line beneath the source name; the overview subtitle where no description is declared; the Skills and Memory tab buttons and count cards; and the Skills and Memory empty-state sentences, which name the label rather than the product word. Defaults are *Substrate*, *Domain estate*, *Framework source*, *Domain source*, *Skills* and *Memory*. Each heading and caption always carries a non-empty label; a rejected or empty label yields the default. Accessible names of relabelled elements are their visible text; no `aria-label` restates a relabelled string. Labels shall not change routes, view identifiers or API identifiers, and all other product copy keeps the product's words.

**FR-PRES-005 — Presentation facts.** The Settings tab shall show, read-only, for every presentation field the value in effect and the source that supplied it, every rejected field with its reason, the presentation-empty and presentation-unavailable states when they occurred, and the identity fact of FR-PRES-001; the estate-issue notice shall count presentation issues. No control shall change presentation.

**FR-PRES-006 — Packaged presentation and mark image.** A build made with a profile may embed a default presentation and one mark image as package data. The embedded presentation is validated at build time against the presentation grammar and contrast floor and the build fails on any rejected field; it is validated again at load, and a field rejected at load is reported with source `packaged_default`. The mark image is served as `image/png` at `/brand-mark.png` as an entry of the immutable packaged asset manifest; when no mark is packaged the route is absent from the manifest and returns `route_not_found`. The favicon route serves the packaged mark when one is packaged and the product icon otherwise; both are manifest entries. A packaged mark is shown in the brand-mark slot; without one, the brand mark is the resolved text mark. Only a build made with a profile embeds a packaged presentation and mark; the framework-carried macOS launcher installs the unprofiled checkout and is branded by a root file alone.

**FR-PRES-007 — Distribution profile.** The Windows build and the portable package build shall accept one profile naming the product, the publisher, the installer output name, the application icon, the mark image and the embedded default presentation, under the profile grammar in Section 9; the build fails closed before generating any source on any violation. The default profile shall reproduce the current build inputs: the generated NSIS defines and version-info are byte-identical to the committed ones. A non-default profile shall produce an installer, install directory, Start Menu folder, shortcuts, registry keys and version strings carrying its `product_name` and `publisher` only through that grammar; the version strings that carry the profile are `ProductName`, `CompanyName` and `FileDescription`, while `OriginalFilename` and `InternalName` stay the product's. The tray icon and tooltip and the native error-dialog title carry the profile's icon and product name; installer copy, the menu verbs **Open Explorer** and **Exit Explorer**, the frozen executable filename and the per-user single-instance mutex and pipe names stay the product's, so for one Windows user only one frozen Explorer runs at a time whatever its brand or root, and a second brand's activation opens the running instance's browser, whichever brand it carries. A differently branded installer neither upgrades nor uninstalls an install of another brand; both may be installed, each under its own directory, registry key and shortcuts. The verification-identity build composes with a profile so a branded build's lifecycle can be proven in isolation.

### Runtime and error behaviour

**FR-RUN-001 — Standalone distribution.** v1 shall retain the installable `explorer/` Python package for development, automation and the portable macOS route, alongside the native Windows installer. Both forms include all browser assets and the pinned YAML runtime. The Windows-installed application shall contain its own Python runtime and dependencies; no system Python, `pip`, Node, CDN or internet access is required after the installer artefact has been obtained. The command-line form shall continue to print the resolved root and capability-bearing loopback URL, shall optionally open that URL without persisting it, shall reject invalid configuration with non-zero exit, and shall terminate within five seconds of an explicit interrupt or stop signal.

**FR-RUN-002 — Safe bind and lifecycle.** The server shall bind only to `127.0.0.1` by default, accept `--port` or choose an available port, print the actual URL, reject a non-loopback bind, isolate concurrent instances by launch capability, and never expose itself on all interfaces. A port collision shall exit non-zero rather than selecting a different requested port. The server shall remain available until explicitly stopped or its host/process exits, with no inactivity shutdown. Closing a tab or leaving it untouched shall not expire the server or browser session. No activity heartbeat or browser expiry timer is required. Windows tray Exit, CLI interrupt and the Mac launcher stop/relaunch shall close their owned service cleanly. This supersedes the 30-minute lease at the operator’s request on 2026-09-05.

**FR-RUN-003 — Health.** A health endpoint shall report application availability without enumerating private estate contents.

**FR-RUN-004 — Native Windows installation.** Windows v1 shall be delivered as one double-clickable setup `.exe`. It shall install per user without administrator rights, register an uninstaller, validate and retain the selected MarkdownLLM substrate root, and create working Start Menu and Desktop shortcuts. The normal interactive path shall require no command line and shall offer to launch Explorer when setup completes. The product name, publisher and output name come from the build profile (FR-PRES-007).

**FR-RUN-005 — Desktop application launch.** Activating either installed shortcut shall start the bundled local service without a console window, open the capability-bearing URL in the user's default browser, and expose a notification-area icon with **Open Explorer** and **Exit Explorer** actions. A second activation while the same user instance is running shall ask the existing process to open its browser rather than creating a second server or persisting the capability outside process memory.

**FR-RUN-006 — Upgrade and uninstall.** Re-running the same-or-newer installer shall replace the installed application in place, preserve the selected substrate root and maintain one shortcut of each requested kind. Uninstall shall stop/remove the application, shortcuts, uninstaller registration and Explorer-owned installation settings while leaving the selected substrate and all of its repositories byte-identical.

**FR-RUN-007 — Agent-invoked macOS launch.** The framework shall carry `tools/open-explorer.sh` as the immediate macOS operator route. From any current working directory it shall resolve its own framework root, require macOS and Python 3.10+, create or refresh an Explorer-only virtual environment below the user's Application Support directory without administrator rights, install the current checked-out `explorer/` package, replace only a verified prior Explorer process for that same root, launch detached and open the default browser. It shall support `--stop`, persist only its owned environment and PID, never persist the capability URL, document content or a log, and return an actionable non-zero failure when bootstrap or launch fails. Native `.app`/DMG packaging is explicitly deferred and shall not block this route.

**FR-ERR-001 — Structured failures.** API failures shall use `{code, message, retryable, source_id?, relative_path?}` and the error/status table in the design, with no document body or absolute path by default. The UI shall render recoverable contextual messages, and retry shall preserve location.

**FR-ERR-002 — Terminal and current loading states.** Every loading operation shall end in content, empty or error state. Older responses shall be cancelled or ignored by request identity and shall not populate a newer source context; there shall be no indefinite spinner after a request settles or times out.

## 8. Quality requirements

**NFR-ARCH-001 — Dependency direction.** Core entities and use cases shall not import HTTP, browser, filesystem, git-subprocess or concrete Markdown-rendering details. Application-owned ports shall define these seams; outer adapters shall implement them.

**NFR-ARCH-002 — Thin delivery layers.** HTTP handlers and browser event handlers shall translate input/output and delegate. Domain discovery, path policy, commit selection and document classification shall not live in controller/view code.

**NFR-ARCH-003 — Replaceability.** A controlled adapter-swap test shall show that replacing the HTTP server, git reader, filesystem reader or Markdown renderer changes no core/application file—only composition, the adapter and its adapter tests. The changed-file set is retained as evidence.

**NFR-SAFE-001A — Observable source immutability.** Explorer shall not alter source bytes or mutation-relevant metadata: names, types, size, content, mtime, mode/ACL where observable, worktree content, index checksum, refs, object set and repository config. Acceptance compares those pre/post snapshots. Access-time and OS-maintained read telemetry are explicitly excluded because ordinary reads may update them outside Explorer's control.

**NFR-SAFE-001B — Constrained git.** The git adapter shall expose an argument-vector allowlist of read-only operations whose arguments are fixed except for a full 40-character object identifier and, where a template requires one, a single source-relative path; a template carrying a path shall re-validate that path against traversal, absolute form, option-leading form, separator, colon and control characters independently of any validation performed by its caller, shall terminate option parsing before it where the template admits options, and shall be invoked with pathspec globbing disabled so a filename is never read as a pattern;  set fixed source cwd, non-interactive environment, `GIT_OPTIONAL_LOCKS=0`, no pager/editor/hooks/external diff, bounded timeout/output and no shell; and prevent global/system/repository configuration from broadening execution. Mutation verbs and arbitrary options are not representable through its port.

**NFR-SAFE-001D — Historical read boundary.** Content read from the repository object store shall be governed by the same rules as a working-tree read: source admission, name eligibility, exclusive ownership, the file-size limit, binary classification and encoding support, reported with the same error codes. Admission shall be decided before any git invocation, because the object store retains every path the repository has ever contained, including paths the working-tree reader excludes today. Historical content shall not be rendered, and its links shall not be resolved, since a link in a historical file resolves against a tree that no longer exists.

**NFR-SAFE-001C — Outside-root writes.** The exploration runtime writes no Explorer-owned persistent content state. It may write diagnostic lines to stdout/stderr, ephemeral socket/process state managed by the operating system, interpreter/package bytecode caches outside every source root, and browser-local storage holding only viewer preferences — the colour theme and the fold state of each side region. It may hold a source-derived index in memory for the life of the process; nothing derived from a source is written to disk. The Windows installer may write only its per-user application files, uninstall registration, selected substrate-root setting and requested shortcuts. The macOS launcher may write only its Explorer-owned virtual environment and PID beneath the user's Application Support directory; its transient diagnostic file shall be unlinked after launch and no capability-bearing output shall be persisted. No capability, document content, frontmatter, source path below the configured root, content cache, token, durable log or database shall be persisted by the application. Presentation is derived on every discovery and never persisted; the packaged default presentation and mark image are package data written only by the build.

**NFR-SAFE-002A — Root configuration confinement.** The launch root shall be an existing readable directory. The configured domain directory shall be source-relative, resolve beneath the launch root and reject absolute, UNC/device or escaping input.

**NFR-SAFE-002B — Per-I/O confinement.** Every directory enumeration and file read shall validate source-relative syntax, canonical ownership and non-link/reparse parent components immediately before I/O, then compare final directory/file identity and mutation metadata after I/O. File reads shall validate the opened native handle's final target using `GetFinalPathNameByHandleW` on Windows and `fcntl(fd, F_GETPATH)` on macOS; inability to obtain required evidence on either native profile fails closed. Traversal, separator/case/encoding variants, symlinks, junctions/reparse points, UNC/device paths and detected replacement fail closed. Evidence names the executed filesystem/OS profiles and the residual race: v1 does not claim protection from a fully privileged local process that can replace path components between all checks.

**NFR-SAFE-003 — Content safety.** All repository strings shall be inserted as text or passed through an allowlist renderer. Raw mode is non-executable text; active repository HTML is never retained. Rendered documents load no repository subresource. The only images the application ever loads are entries of its immutable packaged asset manifest — the packaged mark and the favicon (FR-PRES-006) — and never bytes read from a source. Tests include script/event attributes, encoded schemes, SVG/data URLs, remote images and malformed markup.

**NFR-SAFE-004 — Resource limits.** Every traversal/read/process/response shall enforce the normative limits in Section 9. Limit failures have stable error codes; N−1, N and N+1 are tested.

**NFR-SAFE-005 — Local web boundary.** Estate APIs shall require an unguessable per-launch 256-bit capability delivered in the printed launch URL and then sent in a header. Requests shall accept only the launch-selected loopback Host and same Origin (or no Origin), emit no permissive CORS, use CSP `default-src 'self'; img-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: no-referrer`, `Cache-Control: no-store` and deny framing. Same-origin image loads shall be satisfiable only by the immutable packaged asset manifest: no route outside that manifest shall serve an image content type, no manifest entry is backed by source bytes, and the rendered document pipeline emits no image element. Unauthenticated health returns only static availability/version data.

**NFR-SAFE-006 — Presentation safety.** Every presentation and declared-identity string shall reach the DOM as text — through `textContent` or `createTextNode`, or through an escaping function whose removal is a killed mutant. Colours shall be accepted only in the exact `#rrggbb` grammar and only when they reach the contrast floor in Section 9 against every surface on which the accent is rendered as text in their theme, and the non-text floor against the rail surface; the soft accent is derived by the fixed, declared mix in Section 9 and the derivation shall itself satisfy the text floor; a colour that fails on any surface is rejected with the measured ratio and the failing surface named. Marks and strings shall satisfy the grammar in Section 9. Images shall never originate from a repository, and no route outside the packaged asset manifest shall serve an image content type. Deliberate mutants that remove the colour grammar, the contrast check or the text-only rendering, or that add a source-backed route with an image content type, shall be killed by the suite.

**NFR-PORT-001 — Portability.** Runtime code shall support Python 3.10+ on Windows 10+, macOS 13+ and maintained Linux distributions without assuming POSIX separators. This increment shall retain the Windows 10+ x64 native bundle/installer profile, add the portable agent-invoked macOS route and keep Linux/macOS native packaging deferred. Launcher structure and macOS confinement behaviour may be proven off-host, but successful macOS launch remains `unexecuted-platform` until Aaron's actual machine runs it. The browser compatibility floor is Chromium 128+, Firefox 128+ and Safari 18+; this implementation run must execute runtime UI evidence in available Chromium and record standards/static inspection, rather than falsely claiming human acceptance on unavailable browsers.

**NFR-OFF-001 — Local-first.** Core exploration and Windows installation from the obtained setup artefact shall require no internet connection, separately installed Python, third-party service, CDN, Node runtime or browser extension.

**NFR-PERF-001 — Reproducible budgets.** Against fixture manifest `estate-scale-v1` (1 substrate, 13 independent domains, 2,500 eligible paths, 50 commits per repository) on a reference profile of at least 4 logical CPU, 8 GiB RAM, SSD and Python 3.10+, measure request start to terminal response in isolated fresh server processes. After one discarded warm-up, at least 19 of 20 runs shall meet: estate + first overview ≤2.0 s; directory page ≤300 ms; filename search ≤500 ms; 1 MiB document ≤500 ms; 50-commit page ≤500 ms; a commit's changed-path list ≤500 ms; and a historical document read ≤1.0 s. Reference resolution is deliberately outside these budgets and carries its own: the first lookup against a source builds a whole-source index and is measured in seconds, so it runs after the document is displayed and never delays it; subsequent lookups within the revalidation window are immediate. The evidence register records fixture hash, machine/OS/Python, cache conditions and raw timings. The private 2026-08-27 estate is an additional observational probe, not the reproducibility oracle. Every fixture domain carries entry-file frontmatter with `name` and `description`, and the substrate carries a valid root `presentation.md`, so the estate + first overview budget includes the reads FR-PRES-001 and FR-PRES-002 add to discovery.

**NFR-PERF-002 — Incremental payloads.** Estate, tree, document and commit data shall use separate endpoints so opening the application does not transfer every file body or every repository history.

**NFR-ACC-001 — Accessible interaction.** AJ-01–04 shall be checked against WCAG 2.2 AA for accessible names, semantic roles/states, focus order/visibility, traps and overlay focus return, tree keys, loading/error announcements, contrast/colour independence, 200% zoom, 320 CSS-pixel reflow, 24 CSS-pixel target minimum and reduced motion. Evidence records browser/OS/assistive-tool versions and any accepted exception; automated checks do not constitute a human accessibility ruling. AJ-12's branded shell in both themes is included, with the accent checked at 3:1 as a non-text indicator (active tab underline, selected-source bar, focus ring) against the rail and panel surfaces.

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
| Changed paths listed for one commit | 500; the list becomes partial at the cap |
| Git process duration / captured output | 3 seconds / 1 MiB |
| Captured output for a commit patch read only for its hunk headers | 8 MiB; beyond it the file is served unmarked |
| JSON API response body | 2 MiB |
| Concurrent in-flight HTTP requests | 16; excess receives `server_busy` |
| Symlink/junction/reparse traversal | 0 hops; never followed |
| Presentation and declared-identity strings | YAML string scalars, NFC-normalised, measured in Unicode code points after trimming; invalid if empty after trimming, or if any code point is of general category Cc, Cf, Cs, Co, Cn, Zl or Zp, or is whitespace other than U+0020 |
| Presentation `name` / `tagline` / each label / declared `description` | 1–60 / 1–120 / 1–32 / 1–200 code points |
| Presentation `mark` | 1 or 2 code points of general category L, N, P or S after NFC normalisation; the source glyph is the first grapheme cluster of the displayed name |
| Presentation `accent` / `accent_dark` | exactly `#rrggbb`; contrast ≥ 4.5:1 against every surface on which the accent is text in its theme — the page, the panel, the hover surface and the derived soft accent — and ≥ 3:1 against the rail surface; the soft accent is the accent mixed into the theme's panel colour at 14% (light) or 16% (dark) |
| Product default presentation | name **MarkdownLLM**, tagline **Explorer**, mark **M**, accent `#2d6a57`, accent_dark `#8dc5ad`, labels as FR-PRES-004 |
| Root presentation file | the eligible file body limit above; frontmatter limits as for any document |
| Packaged mark image | PNG by magic bytes, ≤ 256 KiB, ≤ 512×512 px, package data only |
| Profile `product_name` / `publisher` / `output_name` stem | 1–60 printable code points; no path separator; none of `"` `'` `$` `\` `/` `:` `*` `?` `<` `>` or the vertical bar; no leading or trailing dot or space; not a reserved Windows device name |
| Profile `icon` / `mark_image` / `embedded_presentation` | paths resolved relative to the profile file and inside its directory, that exist and pass magic-byte checks (`.ico`; PNG as above; a presentation file that passes the grammar and contrast floor) |

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
8. Presentation is data: an estate can change Explorer's words and colours, never its code, its images or its routes.
9. A brand cannot broaden authority: single-instance behaviour, root selection, ownership and confinement are independent of any profile or presentation.

## 11. Acceptance journeys

### AJ-01 — Executive-route demonstration

Given the captured local estate and only the launch URL, the tester opens Explorer, sees the substrate heading above the domains heading (defaults **Substrate** and **Domain estate**), selects a domain, identifies that domain as the owner of a shown commit, opens **Skills**, reads a styled skill, opens **Memory** to read an insight, and identifies files/git as read-only authority without using filesystem or git tooling. This demonstrates the intended route; it does not substitute for CEO usability acceptance.

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

### AJ-11 — Agent-invoked Mac session

On Aaron's macOS 13+ machine with the current framework checkout, the tester asks Claude Code to open MarkdownLLM Explorer. Claude runs `bash tools/open-explorer.sh`; the default browser opens without elevation, Aaron selects a real domain, sees every populated first-level `things/` group, opens a formerly omitted item and follows both a body link and reference from a tree-origin document. After more than 30 minutes without browser or API activity, the same page can still load a document. The tester explicitly stops Explorer through the launcher, confirms service exit, then opens it again successfully. The tester records macOS/Python/architecture, before/after source observations and any actionable launcher failure; successful Mac execution is not inferred before this journey occurs.

### AJ-12 — White-label journey

Prerequisites: the framework ignores `/presentation.md` and declares `type: presentation`, so the tester's file neither blocks the framework's next commit nor validates as an undeclared thing (H8). Against a conforming substrate whose domains declare names and descriptions, the tester first observes the product default presentation (Section 9) and the declared domain names. The tester then places a root `presentation.md` carrying the Reverb identity — name, tagline, text mark, light and dark accents and a relabelled vocabulary — restarts Explorer, and sees the window title, brand mark and name, rail headings, source-kind lines, overview labels, tab captions and empty-state sentences follow it in both themes, with Settings naming the root file as the source of every field it supplied. The tester replaces the accent with a colour that fails the contrast floor, restarts, and sees the packaged accent — or, in a build without a packaged default, the product accent — retained beside a rejected-field issue that names the field, the ratio and the failing surface, with every other field still applied. The tester removes the file, restarts, and sees the product default presentation. The tester installs a package built with the Reverb profile against a checkout that carries no root file and sees the embedded Reverb identity, the packaged Reverb mark image in the brand slot and the Reverb favicon; then places a root file that relabels one tab and sees the packaged mark and identity retained beneath the relabelled tab. Throughout, a document containing an image tag renders no image and no request outside the packaged asset manifest returns an image content type. The tester's placement, replacement and removal of `presentation.md` are the only changes to any source: after each such edit and before each launch the tester takes a fresh AJ-07 snapshot of the substrate, every comparison taken after an Explorer run is identical to the snapshot taken before it, and the domain sources are snapshotted once and identical throughout.

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
- **H6 — An install-local root file is an acceptable home for an organisation's brand.** It has the same status as the domain directory: not tracked by the framework, carried by the organisation's own bootstrap. If organisations lose it across machines, the bootstrap bundle carries it in a later increment.
- **H7 — A packaged mark image satisfies the logo need.** The first captured ask (the operator's own, with the Reverb logo) is met by the build profile. If an adopter requires a logo from the estate, that is a separate content-security ruling, not a default of this increment.
- **H8 — The framework side lands before the journey.** The framework ignores `/presentation.md` and declares `type: presentation` in its own schema before AJ-12 runs on a live checkout; until then the floor reports a root file as an undeclared thing, and Explorer is unaffected.

## 14. Definition of done

The v1 increment is done only when:

- the requirements, design and test specifications have completed their requested cold-read cycles;
- every requirement is implemented, explicitly deferred, or rejected with rationale;
- automated unit, contract, integration, security and UI tests pass;
- runtime tests exercise the captured real estate and temporary independent estates;
- the twelve acceptance journeys have recorded technical pass/fail evidence and human-owned judgements are labelled accepted or pending;
- the presentation requirements have trace rows, executed evidence in both themes, and killed mutants for the text-only rendering, colour grammar and contrast check;
- visual inspection has been completed in light and dark themes at desktop and narrow viewports;
- two cold code-review passes have been reconciled;
- the Windows setup artefact installs offline, creates valid shortcuts, opens the browser, handles reactivation, upgrades and uninstalls from a clean process; and
- the working tree is committed with no unexplained changes.
