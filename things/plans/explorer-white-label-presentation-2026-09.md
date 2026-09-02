---
id: explorer-white-label-presentation-2026-09
type: plan
status: in-progress
version: 1.2
created: 2026-09-02
priority: high
exposed: false
tags: [explorer, white-label, presentation, branding, estate, install-local, distribution, sprint]
linked_things:
  - id: explorer-macos-and-navigation-sprint-2026-09
    relation: references
    notes: "The 0.4.0 candidate is the behavioural baseline this plan changes; its Mac acceptance is not a prerequisite, but its shell, routing and safety contracts are the ones amended here."
  - id: explorer-extraction-and-hosting
    relation: complements
    notes: "Tenant-level presentation in a hosted product is phase-two work. The presentation value object designed here is exactly what a tenant record would later carry; nothing here moves Explorer or exposes it to a network."
  - id: explorer-publication-position
    relation: references
    notes: "No publication is implied. A white-label build is a separate, deliberate release act per organisation, gated by the same signing position."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "The development lifecycle runs as a solution-delivery run in the Code Architect domain; this plan is the product-side record of that run's scoping."
---

# Explorer white-label presentation

## Outcome

An organisation that adopts MarkdownLLM, runs its operations as a set of
domains, and reads them through Explorer can make Explorer *look like its own
tool*: its name, mark, colours and vocabulary over the whole estate, and each
domain shown under the name and description it declares. The brand is a
property of the **install**: one file at the root of the organisation's
MarkdownLLM checkout, read by Explorer the way it reads everything else,
read-only, confined, bounded. There is no admin screen, no plugin code, and no
image bytes from a repository ever rendered.

**Revision 1.1, operator direction of 2026-09-02.** The white-labelling party
is an organisation, and every domain on its substrate belongs to that
organisation, so the brand must not be pinned to a domain. Revision 1.0 let any
domain claim the shell and policed contention with an exactly-one rule. That
served the framework author's multi-organisation estate, not an adopter, and it
is withdrawn; the alternatives table below records it.

White-labelling has three radii, and each has a different home:

| Radius | What it changes | Where it is declared | Who reads it |
|---|---|---|---|
| **Domain** | A source's name and description | The domain's own `AGENTS.md` frontmatter, which every scaffolded domain already carries | Explorer at discovery |
| **Estate** | The shell: window title, brand mark and name, tagline, accent, rail and tab vocabulary | `presentation.md` at the root of the checkout; install-local, never tracked by the framework | Explorer at discovery |
| **Distribution** | Product name, publisher, executable and shortcut names, icon, packaged logo, embedded default presentation | A build profile consumed by `packaging/windows/build.ps1` | The build, per organisation |

A fourth radius — a hosted tenant's presentation — belongs to
`explorer-extraction-and-hosting` and reuses the same value object.

## Current state, observed 2026-09-02

Observed at framework commit `32a576096c44bb0d2c85074c40f2647dfa657e11`
(Explorer `0.4.0`, portable candidate), reconciled against `27ffd99`.

- **Every brand surface is a literal in code.** `index.html` carries the
  window title, the `M` brand mark and the *MarkdownLLM / Explorer* wordmark;
  `app.js` writes *Framework source* / *Domain source* under the source name;
  `views/navigation.js` hard-codes the rail headings *Substrate* and *Domain
  estate*; `views/overview.js` hard-codes the hero subtitle *Framework
  substrate* / *MarkdownLLM domain*; `app.css` fixes one teal accent per theme.
- **Domains are shown by folder name.** `filesystem_catalogue.py::discover`
  names a domain source `path.name`, so the rail reads `code-architect` while
  the domain's own `AGENTS.md` frontmatter declares `name: Code Architect` and
  a one-line `description`. Every scaffolded domain carries both fields; all
  fourteen domains in the operator's estate do. The identity already exists and
  is simply not read.
- **The substrate is named by rule.** FR-EST-002 names the first source
  *MarkdownLLM* regardless of folder; the rail heading carries the role.
- **Repository bytes never render as an image.** NFR-SAFE-005 fixes the CSP at
  `img-src 'none'`; `http_server.py` serves an exact immutable asset manifest
  from package data and nothing else. The favicon is package data, not source
  data. This is the invariant a white-label logo would collide with.
- **Install-local root artefacts are the framework's existing answer to "the
  organisation's territory inside a public checkout".** `domain/` is
  gitignored wholesale; `.boundary-terms` is a root file the floor reads on
  every commit and must never track; `.claude/settings.local.json` is
  per-user. The framework deliberately has no estate manifest ("a filesystem
  fact, not an estate manifest"), and an organisation's estate is rebuilt
  elsewhere from the private bootstrap bundle's `config.env`, never from the
  repository. A root presentation file belongs to this family.
- **The distribution layer names the product in eleven places.** The NSIS
  script, `version-info.txt`, `build.ps1`, `windows_app.py` (tray title, pipe
  and mutex names) and `tools/open-explorer.sh` (Application Support folder)
  all spell *MarkdownLLM Explorer* as a literal.
- **Presentation settings are out of scope today.** Requirements §5 excludes
  "administrative settings beyond theme". This plan keeps that exclusion:
  presentation is a file the operator or the agent writes, never an Explorer
  control.

## Diagnosed constraints

These are the facts the design has to respect, not preferences.

1. **Read-only and confined.** Explorer never writes and reads only through
   the confined source reader. The presentation file must be an ordinary
   eligible file inside a source root so that every existing confinement,
   eligibility and size rule applies to it unchanged.
2. **No active content from the estate.** Text is rendered through
   `textContent`; a presentation must be text and numbers only. Colour values
   must be validated to a strict grammar before they touch CSS. Images from a
   repository are excluded by the CSP and stay excluded.
3. **No new persisted state.** NFR-SAFE-001C permits browser-local storage for
   theme and region folds only. Presentation is server-derived on every load
   and stored nowhere.
4. **The substrate root is upstream's repository.** An organisation cannot
   track its brand there without a fork, and a fork fights `mdllm refresh`.
   The file is therefore install-local and gitignored by the framework, and
   carrying it across the organisation's machines is an estate-bootstrap
   concern, exactly as the domain list is today.
5. **Views stay passive.** The architecture fitness test rejects browser view
   modules that fetch or mutate global state. Labels reach views as values.
6. **Domains own their identity.** The estate file sets the shell's
   vocabulary; it may not rename a domain. One owner per fact.

## Presentation contract

### Where it lives

`presentation.md` at the root of the MarkdownLLM checkout, beside `AGENTS.md`.
The name has no leading dot so the eligibility policy admits it; it sits inside
the substrate source root so the confined reader serves it unchanged; it shows
in the substrate's file tree, which is honest. The framework adds
`/presentation.md` to its `.gitignore` and declares `type: presentation` in its
own `_schema.yaml`, so an adopter's file validates cleanly at the root and the
framework itself never ships one. Explorer's product default, *MarkdownLLM*,
lives in code; no file is needed for it.

How it travels: in v1 the operator places it per machine, and the operator
guide says so in one line. A later increment lets `mdllm bundle` copy it into
the private bootstrap bundle and `mdllm assemble` restore it, the route the
organisation's domain list already takes. An organisation may equally keep the
file in its own operations repository and place it on install. It is not
versioned in the framework, by design; the failure cost of losing it is the
default chrome until it is put back.

### Fields

```yaml
---
id: presentation
type: presentation
status: active               # the domain's lifecycle vocabulary; Explorer does not read it
version: 1.0
created: 2026-09-02
name: Kestrel Logistics      # at most 60 characters
tagline: Operations estate   # at most 120 characters, optional
mark: K                      # 1 or 2 printable characters, optional (default: first character of name)
accent: "#8f5a12"            # light-theme accent, #rrggbb only, optional
accent_dark: "#e3a651"       # dark-theme accent, #rrggbb only, optional
labels:                      # optional; only these keys; each at most 32 characters
  substrate: Platform
  domains: Operations
  substrate_kind: Framework source
  domain_kind: Business area
  skills: Playbooks
  memory: Records
---
```

The body is the rationale: whose identity this is, who may change it, and why
it looks the way it does.

### Resolution rules

A **domain's** name is its `AGENTS.md` `name`, falling back to its folder
name; its tagline is the `description`, falling back to the estate's
`domain_kind` label. The substrate stays *MarkdownLLM* (FR-EST-002).

The **estate's** shell is chosen once, at discovery, first present wins:

| Order | Source | When it applies |
|---:|---|---|
| 1 | `presentation.md` at the root of the checkout | Present and valid |
| 2 | The default presentation embedded by a distribution profile | A branded build, against any checkout |
| 3 | The product default | Always |

An invalid field is dropped and reported as a `presentation_field_rejected`
issue carrying the field name and reason; the remaining fields still apply. A
missing, unreadable, oversized or malformed file yields the next source in the
chain, never a failed estate. Presentation, like the source catalogue, is fixed
for one process: restart is the refresh, consistent with design §17.

### Validation grammar (core policy, pure)

- Strings are bounded as above, trimmed, and rejected if they contain control
  or format characters.
- `mark` is one or two characters from the letter, number, symbol or
  punctuation categories; whitespace, control, format and separator characters
  are rejected so a bidirectional override can never enter the brand mark.
- Colours match `^#[0-9a-fA-F]{6}$` exactly. A colour is accepted only if it
  reaches a 4.5:1 contrast ratio against both the panel and page surfaces of
  the theme it applies to, because the accent is used as text (links, commit
  identifiers). A failing colour is rejected with the measured ratio.
- The soft accent (`--accent-soft`) is derived from the accepted accent, never
  supplied.
- Unknown keys are ignored by Explorer; the floor's `known_fields` check is the
  place they are flagged.

### Alternatives considered

| Alternative | Reason not chosen |
|---|---|
| A domain carries the estate presentation and an exactly-one rule polices contention (revision 1.0) | Serves a multi-organisation estate, which is the framework author's case. For an adopter every domain is the organisation's, so the choice of domain is arbitrary and the rule is pure overhead. |
| Build-time white-label only, no runtime file | Every wording or colour change needs a rebuild, and the portable Python and Mac routes stay unbranded. Kept as the distribution radius, where it is the right tool for logos and installer names. |
| A file tracked in the framework repository | Only a fork could carry an adopter's brand, and a fork fights framework refresh. |
| A launch flag naming a presentation file | Per machine and per launcher. Kept as a later option for an estate that hosts several organisations. |
| Presentation fields inside `.markdownllm` | That file is the framework's version sentinel, tracked upstream; an adopter cannot own it. |

## Design allocation

The dependency rule and the adapter-swap fitness test hold: every addition is
one core policy, one port, one adapter, one use-case touch, one DTO field set
and one browser module.

| Layer | Addition | Responsibility |
|---|---|---|
| `core/presentation.py` | `Presentation` value object, `DEFAULT_PRESENTATION`, `PresentationPolicy` | Field bounds, mark categories, colour grammar, contrast arithmetic, the fallback chain; no I/O |
| `application/ports.py` | `PresentationReader(Protocol)`, `IdentityReader(Protocol)` | Read the root presentation record and a source's declared identity, or nothing |
| `application/discover_estate.py` | `DiscoverEstate` composes catalogue, readers and policy | Resolves each source's identity and the estate presentation once, appends issues to the snapshot |
| `adapters/presentation_reader.py` | `ConfinedPresentationReader` | Reads `presentation.md` on the substrate boundary and `AGENTS.md` on each source boundary through the existing confined reader and frontmatter parser; maps to core values via the policy |
| `core/models.py` | `Source` gains `tagline`; `EstateSnapshot` gains `presentation` | Public identity carried where sources already are |
| `delivery/response_encoding.py` | Explicit DTO fields | No dataclass serialisation; the boundary token stays private |
| `delivery/static/js/presentation.js` | `applyPresentation` | Sets `document.title`, brand text via `textContent`, accent via `style.setProperty` on the root element; returns the label map views receive |
| `views/navigation.js`, `views/overview.js`, `app.js`, `views/settings.js` | Take labels and identity as parameters | Headings, kind labels, hero subtitle, tab names; Settings shows which source the presentation came from and any rejected fields |
| `composition.py` | Packaged default | Reads an embedded default presentation from package data when a distribution profile supplied one; otherwise the code default |

`GET /api/v1/estate` carries the estate presentation and per-source identity;
no new route is needed. `GET /api/v1/settings` gains read-only presentation
facts. The Windows and macOS launch surfaces are untouched at this radius.

Setting a CSS custom property through the CSSOM is permitted under
`style-src 'self'`; the CSP header does not change. Nothing from the estate is
ever placed in an inline style attribute, a `<style>` element or an image
request.

## Safety boundary

- **Text only.** Every presentation string reaches the DOM through
  `textContent`. The mutation suite gains an anchor: a name containing an
  image tag with an event handler must render as those literal characters.
- **Colour grammar and contrast in core.** Removing the regex or the contrast
  check must fail a test; both are deliberate-mutant targets.
- **No image from the estate.** `img-src 'none'` stays. A logo enters only as
  **package data through the distribution profile**, which keeps the invariant
  "repository bytes never render as an image" literally true. If an
  organisation requires a logo at the estate radius, that is a CSP decision for
  the operator, not a default of this plan.
- **Confinement inherited.** The reader reuses `ConfinedSourceReader.read`, so
  reparse points, secrets, depth, size and encoding rules apply without a
  second implementation.
- **Terminal states.** Every failure ends in the next source of the chain plus
  an issue; no presentation failure can leave the estate without a shell.

## Distribution profile

`packaging/windows/build.ps1 -Profile <file>` reads one YAML profile:
`product_name`, `publisher`, `executable_name`, `registry_key`, `icon`,
`mark_image`, and an embedded `default_presentation` that the build writes into
package data, so a branded build is branded against any checkout; a root
`presentation.md` still wins when present. The NSIS defines, `version-info.txt`
strings and the frozen executable name are generated from the profile; the
default profile reproduces today's bytes exactly. The single-instance mutex
and pipe names stay keyed on the substrate root, not the product name, so two
differently branded builds against one root cannot run two servers.
`tools/open-explorer.sh` follows the same profile in a later lane; the Mac
route is not blocked by it.

## Traceability

New requirements the design stage writes into `requirements.md`, `design.md`,
`test-specification.md` and `traceability.yaml` before production code:

| Id | Requirement | Observable pass condition |
|---|---|---|
| FR-PRES-001 | Domain identity from `AGENTS.md` | A domain whose entry file declares `name` is listed and titled by it; a domain without one falls back to its folder name |
| FR-PRES-002 | Root presentation file | A valid `presentation.md` at the checkout root brands the shell; each invalid field is reported and the rest apply |
| FR-PRES-003 | Fallback chain | With no root file the packaged default applies; with neither, the product default; a malformed or oversized file yields the next source and an issue, never a failed estate |
| FR-PRES-004 | Vocabulary labels | Rail headings, kind labels, hero subtitle and tab names follow the label map; unknown label keys are ignored |
| FR-PRES-005 | Presentation facts in Settings | Settings shows which source the presentation came from and any rejected fields; no control can change them |
| FR-PRES-006 | Distribution profile | A non-default profile produces an installer, executable, shortcuts, registry key, version strings and embedded default carrying the profile; the default profile reproduces the current bytes |
| NFR-SAFE-006 | Presentation safety | Text-only rendering, colour grammar, contrast rejection and unchanged CSP are each proven by a deliberate mutant that the suite kills |
| Amendments | FR-EST-002, FR-EST-003, FR-NAV-001, FR-TAB-001, FR-TAB-005, FR-UI-001, FR-RUN-004 | Reworded to name presentation as the source of the labels they fix today |

Fixtures: `F-ESTATE-BRANDED` extends `F-ESTATE-MIN` with a valid root file, an
absent file, a malformed file, an oversized file, a failing-contrast colour and
a packaged default without a file. Browser evidence adds `BT-PRESENTATION-001`
(shell, labels, both themes, no image request observed).

## Delivery sequence

Risk first: the least-understood boundary is what a real adopter needs, so the
first increment captures that before the design hardens.

### I0 — Capture the real ask and close the gate

- [x] Record what the first white-label adopter (or the operator's own case)
      needs on day one. Captured 2026-09-02: the operator's own ask is the
      Reverb name and the Reverb logo, so the packaged mark ships with the
      root file rather than after it.
- [x] Operator rulings on the gate questions below. Closed 2026-09-02 and
      recorded in the Code Architect decision
      `white-label-explorer-through-install-local-presentation`: root file
      confirmed; no estate image, logo through the build profile; tabs may be
      relabelled; substrate relabelled but not hidden.

### I1 — Domain identity from the entry file

- [ ] Read `name` and `description` from each admitted source's `AGENTS.md`
      frontmatter at discovery through the confined reader; fall back to folder
      name.
- [ ] Rail, topbar, overview hero and Settings show the declared identity.
- [ ] Traceability rows, adapter and browser evidence; visible on the
      operator's estate immediately; discovery cost measured against the
      catalogue budget.

### I2 — Root presentation file and shell

- [ ] Core policy, ports, reader, DTOs, `presentation.js`, label-driven views,
      Settings facts.
- [ ] Framework side: `/presentation.md` in `.gitignore`, `presentation`
      declared in the root `_schema.yaml`, one operator-guide section on
      white-labelling the Explorer, one line in the first-hour guide.
- [ ] Full suites, mutation anchors, browser evidence in both themes.

### I3 — Distribution profile

- [ ] `build.ps1 -Profile`, generated NSIS defines and version strings,
      packaged mark image and embedded default presentation read at
      composition.
- [ ] Windows lifecycle evidence for one non-default profile; default profile
      byte-equality with the current build inputs.

### I4 — Later lanes, not gating

- [ ] `mdllm bundle` carries the root file and `mdllm assemble` restores it.
- [ ] A launch-time presentation override for estates hosting several
      organisations.
- [ ] Per-domain marks and accents, if an organisation asks.
- [ ] Hosted tenant presentation in `explorer-extraction-and-hosting`.
- [ ] Estate-radius image marks, only with a new CSP decision.
- [ ] Mac launcher product naming from the same profile.

## Acceptance matrix

| Requirement | Automated evidence | Human evidence | Owner |
|---|---|---|---|
| Declared domain names appear | Catalogue and browser tests | Operator reads the rail on the live estate | Technical run / Janosh |
| Root file brands the shell | Policy, adapter, HTTP and browser tests | Operator places a sample file and restarts | Technical run / Janosh |
| Invalid input degrades safely | Adapter and HTTP issue tests | Operator sees the issue in Settings, never a broken shell | Technical run |
| Nothing from the estate executes or renders as an image | Mutation suite, CSP header test, network observation | Reviewer inspects browser evidence | Technical run |
| White-label installer carries the profile | Windows lifecycle tests | Clean-account install of a sample profile | Technical run / Janosh |

## Assumptions and dispositions

| Assumption | Disposition |
|---|---|
| The brand is a property of the install, one per checkout | **Adopted** — operator direction 2026-09-02; estates hosting several organisations are I4's launch-override case |
| A hand-placed root file is acceptable for v1 | **Adopted** — same status as the domain directory itself; bundle carry follows in I4 |
| Adopters want their identity in a file, not in an Explorer settings screen | **Adopted** — keeps Explorer read-only and the framework definition-driven |
| A text mark and a colour satisfy most first asks | **Hypothesis** — I0 tests it; a required logo pulls I3 forward or reopens the CSP |
| Every domain's `AGENTS.md` carries `name` and `description` | **Observed** for all fourteen domains and the scaffold template; fallback covers the rest |
| `presentation.md` is the right name | **Proposed** — non-dot so Explorer admits it; the operator may prefer another |

## Risks and responses

| Risk | Response |
|---|---|
| A presentation string carries markup or a colour carries CSS | Text-only rendering and a strict colour grammar in core, each guarded by a deliberate mutant |
| A chosen accent fails accessibility | Contrast is measured in core against the real surfaces; failing colours are rejected with the ratio, and the theme evidence is re-run per brand |
| The root file is missing on one of the organisation's machines | Default chrome, no error; the operator guide names the file, and I4 carries it in the bootstrap bundle |
| Reading fifteen entry files slows discovery | Bounded frontmatter reads through the existing parser; measured against the 400 ms catalogue budget before I1 closes |
| The white-label build forks the product | The profile parameterises the outer packaging only; the Python package, core and application remain one artefact |
| Labels drift from product vocabulary decisions (the Memory tab) | Labels are per-install overrides; the product default stays the operator's call |
| This plan collides with the in-flight Windows publication work | It starts after the 0.4.0 candidate is the accepted shape and touches no evidence files of that sprint |

## Out of scope

- Any Explorer control that edits presentation; editing is a file the operator
  or the agent writes.
- Images, fonts or stylesheets loaded from a repository.
- Per-user or per-viewer branding, accounts, or hosted tenancy.
- Per-domain marks and accents, until an organisation asks.
- Renaming the product's default vocabulary; overrides are per install.
- Signing or publishing any white-label build; publication stays gated.

## Gate to start — closed 2026-09-02

The operator confirmed the install-local root file, named Reverb with its logo
as the test identity, and started the cycle. Rulings, recorded in the Code
Architect decision `white-label-explorer-through-install-local-presentation`:
no image from the estate, the logo enters through the build profile and the
immutable packaged asset manifest; the tabs may be relabelled; the substrate
may be relabelled but not hidden. The delivery cycle is the operator's stated
sequence: requirements, design and test specification each with an independent
cold review and reconciliation, then implementation with two code reviews,
residual findings stored for a refinement sprint, then technical acceptance
with the Reverb identity. Explorer requirements v0.5 carry the requirement set.
