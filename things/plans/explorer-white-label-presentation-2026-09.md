---
id: explorer-white-label-presentation-2026-09
type: plan
status: not-started
version: 1.0
created: 2026-09-02
priority: high
exposed: false
tags: [explorer, white-label, presentation, branding, estate, distribution, sprint]
linked_things:
  - id: explorer-macos-and-navigation-sprint-2026-09
    relation: references
    notes: "The 0.4.0 candidate is the behavioural baseline this plan changes; its Mac acceptance is not a prerequisite, but its shell, routing and safety contracts are the ones amended here."
  - id: explorer-extraction-and-hosting
    relation: complements
    notes: "Tenant-level presentation in a hosted product is phase-two work. The presentation value object designed here is exactly what a tenant record would later carry; nothing here moves Explorer or exposes it to a network."
  - id: explorer-publication-position
    relation: references
    notes: "No publication is implied. A white-label build is a separate, deliberate release act per customer, gated by the same signing position."
  - id: code-architect-governs-substrate-code
    relation: references
    notes: "The development lifecycle runs as a solution-delivery run in the Code Architect domain; this plan is the product-side record of that run's scoping."
---

# Explorer white-label presentation

## Outcome

An organisation that adopts MarkdownLLM, runs its operations as a set of
domains, and reads them through Explorer can make Explorer *look like their
tool*: their name, mark, colours and vocabulary over the whole estate, and each
domain presented under the name and description it declares. The configuration
lives **in the estate, as things under git**, and is read by Explorer the way it
reads everything else: read-only, confined, bounded. There is no admin screen,
no plugin code, and no image bytes from a repository ever rendered.

White-labelling has three radii, and each has a different home:

| Radius | What it changes | Where it is declared | Who reads it |
|---|---|---|---|
| **Domain** | A source's name, description, mark, optional accent | The domain's own `AGENTS.md` identity, refined by `things/presentation.md` | Explorer at discovery |
| **Estate** | The shell: window title, brand mark and name, tagline, accent, rail and tab vocabulary | One `things/presentation.md` with `scope: estate` in the estate | Explorer at discovery |
| **Distribution** | Product name, publisher, executable and shortcut names, icon, packaged logo, embedded default presentation | A build profile consumed by `packaging/windows/build.ps1` | The build, per customer |

A fourth radius — a hosted tenant's presentation — belongs to
`explorer-extraction-and-hosting` and reuses the same value object.

## Current state, observed 2026-09-02

Observed at framework commit `32a576096c44bb0d2c85074c40f2647dfa657e11`
(Explorer `0.4.0`, portable candidate).

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
- **There is no estate manifest, by design.** The tool states four times that
  the local clone set is "a filesystem fact, not an estate manifest". Estate
  discovery is a walk over admitted directories. A white-label file at the
  estate level would be the first estate-radius artefact the framework has, so
  the design puts estate presentation *inside a domain* and lets discovery find
  it, rather than inventing a manifest.
- **The distribution layer names the product in eleven places.** The NSIS
  script, `version-info.txt`, `build.ps1`, `windows_app.py` (tray title, pipe
  and mutex names) and `tools/open-explorer.sh` (Application Support folder)
  all spell *MarkdownLLM Explorer* as a literal.
- **Presentation settings are out of scope today.** Requirements §5 excludes
  "administrative settings beyond theme". This plan keeps that exclusion:
  presentation is *data in the estate*, changed through git by the operator or
  the agent, never through an Explorer control.

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
4. **No estate manifest.** The estate-radius declaration must be discoverable
   from the domains themselves, and contention between two claimants must be
   reported as a discovery issue, exactly as `source_id_collision` is today.
5. **Views stay passive.** The architecture fitness test rejects browser view
   modules that fetch or mutate global state. Labels reach views as values.
6. **Domains own their identity.** An estate presentation may set the shell's
   vocabulary; it may not rename another domain. One owner per fact.

## Presentation contract

### Where it lives

`things/presentation.md`, directly under a source's `things/` directory,
addressed **by path**, the way the tool finds `things/_schema.yaml` and
`things/_index/`. Tool-discovered artefacts are path-addressed; references
between things are id-addressed. A loose file directly under `things/` is
outside every Memory group (groups are first-level directories) but visible in
the file tree and search, which is the right visibility for configuration-like
content.

The framework root is a source too. The framework, being a domain within
itself, can declare `presentation` in its own `_schema.yaml` and carry
`things/presentation.md` naming *MarkdownLLM* — the substrate brands itself
through the mechanism it offers — with a test asserting that file equals the
code default so the two can never drift.

### Fields

```yaml
---
id: presentation
type: presentation
status: active               # the domain's lifecycle vocabulary; Explorer does not read it
version: 1.0
created: 2026-09-02
scope: estate                # estate | domain (default domain)
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
it looks the way it does. The floor validates the file as a thing: `type:
presentation` is declared in the domain's `_schema.yaml` with `name` required
and the remaining keys registered in `known_fields`. Reserving the type in the
framework is a later convergence question, not a v1 prerequisite.

### Resolution rules

Each field of a **source's** presentation resolves independently, first match
wins:

1. `things/presentation.md` in that source, when present and the field is valid;
2. the source's `AGENTS.md` frontmatter — `name` for the name, `description`
   for the tagline;
3. the folder name for a domain; *MarkdownLLM* for the substrate (FR-EST-002).

The **estate's** presentation is chosen once, at discovery, from the admitted
sources whose presentation declares `scope: estate`:

| Estate-scoped presentations found | Result |
|---:|---|
| 0 | Product default shell (today's chrome) |
| 1 | Applied to the shell |
| more than 1 | Product default shell and a `presentation_contested` estate issue naming every claimant |

An invalid field is dropped and reported as a `presentation_field_rejected`
source issue carrying the field name and reason; the remaining fields still
apply. A missing, unreadable, oversized or malformed file is *no presentation*,
never a failed estate. Presentation, like the source catalogue, is fixed for
one process: restart is the refresh, consistent with design §17.

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

## Design allocation

The dependency rule and the adapter-swap fitness test hold: every addition is
one core policy, one port, one adapter, one use-case touch, one DTO field set
and one browser module.

| Layer | Addition | Responsibility |
|---|---|---|
| `core/presentation.py` | `Presentation` value object, `PresentationScope`, `DEFAULT_PRESENTATION`, `PresentationPolicy` | Field bounds, mark categories, colour grammar, contrast arithmetic, estate resolution rule; no I/O |
| `application/ports.py` | `PresentationReader(Protocol)` | `presentation(token)` returning a record or nothing |
| `application/discover_estate.py` | `DiscoverEstate` composes catalogue and reader | Resolves per-source and estate presentation once, appends issues to the snapshot |
| `adapters/presentation_reader.py` | `ConfinedPresentationReader` | Reads `things/presentation.md` and `AGENTS.md` through the existing confined reader and frontmatter parser; maps to core values via the policy |
| `core/models.py` | `Source` gains `tagline`, `mark`, `accent`, `accent_dark`; `EstateSnapshot` gains `presentation` | Public identity carried where sources already are |
| `delivery/response_encoding.py` | Explicit DTO fields | No dataclass serialisation; the boundary token stays private |
| `delivery/static/js/presentation.js` | `applyEstatePresentation`, `applySourcePresentation` | Sets `document.title`, brand text via `textContent`, accent via `style.setProperty` on the root element; returns the label map views receive |
| `views/navigation.js`, `views/overview.js`, `app.js`, `views/settings.js` | Take labels and identity as parameters | Headings, kind labels, hero subtitle, tab names; Settings shows the presentation source and any rejected fields |

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
  "repository bytes never render as an image" literally true. If the first
  white-label customer requires a logo at the estate radius, that is a CSP
  decision for the operator, not a default of this plan.
- **Confinement inherited.** The reader reuses `ConfinedSourceReader.read`, so
  reparse points, secrets, depth, size and encoding rules apply without a
  second implementation.
- **Terminal states.** Every failure ends in "default plus issue"; no
  presentation failure can leave the estate without a shell.

## Distribution profile

`packaging/windows/build.ps1 -Profile <file>` reads one YAML profile:
`product_name`, `publisher`, `executable_name`, `registry_key`, `icon`,
`mark_image`, and an embedded `default_presentation` used when the served
estate declares none, so a white-label build is branded even against an
unbranded estate. The NSIS defines, `version-info.txt` strings and the frozen
executable name are generated from the profile; the default profile reproduces
today's bytes exactly. The single-instance mutex and pipe names stay keyed on
the substrate root, not the product name, so two differently branded builds
against one root cannot run two servers. `tools/open-explorer.sh` follows the
same profile in a later lane; the Mac route is not blocked by it.

## Traceability

New requirements the design stage writes into `requirements.md`, `design.md`,
`test-specification.md` and `traceability.yaml` before production code:

| Id | Requirement | Observable pass condition |
|---|---|---|
| FR-PRES-001 | Domain identity from `AGENTS.md` | A domain whose entry file declares `name` is listed and titled by it; a domain without one falls back to its folder name |
| FR-PRES-002 | Source presentation file | `things/presentation.md` fields override identity per the resolution order; each invalid field is reported and the rest apply |
| FR-PRES-003 | Estate presentation | Exactly one estate-scoped presentation brands the shell; zero yields the default; two yield the default and a `presentation_contested` issue |
| FR-PRES-004 | Vocabulary labels | Rail headings, kind labels, hero subtitle and tab names follow the label map; unknown label keys are ignored |
| FR-PRES-005 | Presentation facts in Settings | Settings shows the presentation source and rejected fields; no control can change them |
| FR-PRES-006 | Distribution profile | A non-default profile produces an installer, executable, shortcuts, registry key and version strings carrying the profile's names; the default profile reproduces the current bytes |
| NFR-SAFE-006 | Presentation safety | Text-only rendering, colour grammar, contrast rejection and unchanged CSP are each proven by a deliberate mutant that the suite kills |
| Amendments | FR-EST-002, FR-EST-003, FR-NAV-001, FR-TAB-001, FR-TAB-005, FR-UI-001, FR-RUN-004 | Reworded to name presentation as the source of the labels they fix today |

Fixtures: `F-ESTATE-BRANDED` extends `F-ESTATE-MIN` with one estate-scoped
presentation, one domain presentation, one contested pair, one malformed file,
one oversized file and one failing-contrast colour. Browser evidence adds
`BT-PRESENTATION-001` (shell, labels, both themes, no image request observed).

## Delivery sequence

Risk first: the least-understood boundary is what a real adopter needs, so the
first increment captures that before the design hardens.

### I0 — Capture the real ask and close the gate

- [ ] Record what the first white-label adopter (or the operator's own case)
      needs on day one: name, mark, colour, vocabulary, domain names, logo,
      installer name. The answer decides whether I3 precedes I2.
- [ ] Operator rulings on the gate questions below.

### I1 — Domain identity from the entry file

- [ ] Read `name` and `description` from each admitted source's `AGENTS.md`
      frontmatter at discovery through the confined reader; fall back to folder
      name.
- [ ] Rail, topbar, overview hero and Settings show the declared identity.
- [ ] Traceability rows, adapter and browser evidence; visible on the
      operator's estate immediately.

### I2 — Presentation thing and shell

- [ ] Core policy, port, reader, DTOs, `presentation.js`, label-driven views,
      Settings facts.
- [ ] Framework-carried default presentation and the equality test.
- [ ] Domain guide: how to brand a domain and an estate through git.
- [ ] Full suites, mutation anchors, browser evidence in both themes.

### I3 — Distribution profile

- [ ] `build.ps1 -Profile`, generated NSIS defines and version strings,
      packaged mark image and embedded default presentation.
- [ ] Windows lifecycle evidence for one non-default profile; default profile
      byte-equality with the current build inputs.

### I4 — Later lanes, not gating

- [ ] Group scope for a multi-organisation estate (several brands in one estate).
- [ ] Hosted tenant presentation in `explorer-extraction-and-hosting`.
- [ ] Estate-radius image marks, only with a new CSP decision.
- [ ] Mac launcher product naming from the same profile.

## Acceptance matrix

| Requirement | Automated evidence | Human evidence | Owner |
|---|---|---|---|
| Declared domain names appear | Catalogue and browser tests | Operator reads the rail on the live estate | Technical run / Janosh |
| Estate presentation brands the shell | Policy, adapter, HTTP and browser tests | Operator applies a sample presentation to a test domain | Technical run / Janosh |
| Contest and invalid fields degrade safely | Adapter and HTTP issue tests | Operator sees the issue notice, never a broken shell | Technical run |
| Nothing from the estate executes or renders as an image | Mutation suite, CSP header test, network observation | Reviewer inspects browser evidence | Technical run |
| White-label installer carries the profile | Windows lifecycle tests | Clean-account install of a sample profile | Technical run / Janosh |

## Assumptions and dispositions

| Assumption | Disposition |
|---|---|
| Adopters want their identity in the estate, not in an Explorer settings screen | **Adopted** — matches the framework's definition-driven principle and keeps Explorer read-only; revisit if an adopter cannot commit to git |
| A text mark and a colour satisfy most first asks | **Hypothesis** — I0 tests it; a required logo pulls I3 forward or reopens the CSP |
| Every domain's `AGENTS.md` carries `name` and `description` | **Observed** for all fourteen domains and the scaffold template; fallback covers the rest |
| One brand per estate is enough for v1 | **Adopted for v1** — the operator's own estate spans several organisations and is the case I4's group scope serves |
| `things/presentation.md` is the right address | **Proposed** — path-addressed like the tool's other discovered artefacts; the operator may prefer another name |
| The `presentation` type should be framework-reserved now | **Declined for v1** — per-domain declaration adds no framework mechanism; reserve on cross-corpus convergence, per the operating model |

## Risks and responses

| Risk | Response |
|---|---|
| A presentation string carries markup or a colour carries CSS | Text-only rendering and a strict colour grammar in core, each guarded by a deliberate mutant |
| A chosen accent fails accessibility | Contrast is measured in core against the real surfaces; failing colours are rejected with the ratio, and the theme evidence is re-run per brand |
| Two domains both claim the estate | Reported as `presentation_contested`; the default shell stays; no silent winner |
| Reading fifteen entry files slows discovery | Bounded frontmatter reads through the existing parser; measured against the 400 ms catalogue budget before I1 closes |
| The white-label build forks the product | The profile parameterises the outer packaging only; the Python package, core and application remain one artefact |
| Labels drift from product vocabulary decisions (the Memory tab) | Labels are per-estate overrides; the product default stays the operator's call |
| This plan collides with the in-flight Windows publication work | It starts after the 0.4.0 candidate is the accepted shape and touches no evidence files of that sprint |

## Out of scope

- Any Explorer control that edits presentation; editing is a git act.
- Images, fonts or stylesheets loaded from a repository.
- Per-user or per-viewer branding, accounts, or hosted tenancy.
- Renaming the product's default vocabulary; overrides are per estate.
- Signing or publishing any white-label build; publication stays gated.

## Gate to start — open

The operator's rulings needed before the run advances to `model`:

1. Is a **logo image** required at the estate radius in v1, or is a text mark
   plus a packaged logo in the distribution build sufficient?
2. Should `presentation` be declared **per domain** for v1 (recommended), or
   reserved by the framework now?
3. May an estate presentation **relabel the tabs** (Skills, Memory)?
4. May an estate presentation **hide or relabel the substrate** for an
   executive audience? Hiding amends FR-NAV-001.
5. Is a launch-time `--presentation <source-id>` override wanted in v1, or is
   the exactly-one rule enough?
6. May a **domain** carry its own accent, applied while that domain is
   selected?
