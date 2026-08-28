"""Dark-region coherence checks — generated-artifact freshness and
catalog/filesystem integrity.

Corpus-general by design: stable-staleness, unused vocabulary, zero-run
workflow definitions, derived-index and domain-kernel drift run on any
corpus; the foundational-spec / TIERS / kernel-drift / example-staleness /
framework-map checks switch on only at a framework root. Runs in the
pre-commit hook.
"""

from __future__ import annotations

import re
import subprocess
import fnmatch
from pathlib import Path

import yaml

from .domain_kernel import build_domain_kernel_blocks, domain_kernel_status
from .indexes import INDEX_FILES, index_drift_findings
from .kernel_gen import build_kernel, normalize_newlines, token_counter
from .model import (CORE_FIELDS, Finding, RESERVED_STATUSES, SEV_ERROR,
                    SEV_INFO, SEV_WARNING, parse_frontmatter, scan)
from .repo import TIERS
from .repository_view import RepositoryView, RepositoryViewError
from .skill_vocabulary import skill_vocabulary_findings
from .yaml_loader import load_yaml

# The framework-map count check reads the file that registers the subparsers
# (truth = the `sub.add_parser(` calls) — the CLI module beside this one.
CLI_REGISTRY_FILE = Path(__file__).resolve().parent / "cli.py"

# Framework-owned record templates live outside a downstream domain schema.
# `artifact` is the framework domain's one additional lifecycle (reviews and
# evidence); reserved types remain tool-owned.
_TEMPLATE_STATUSES = {**RESERVED_STATUSES,
                      "artifact": ["evolving", "stable", "deprecated"]}


def _view_text(path: Path, view: RepositoryView | None) -> str | None:
    """Read ``path`` from the selected candidate, never an adjacent tree."""
    if view is None:
        return path.read_text(encoding="utf-8") if path.is_file() else None
    resolved = path.resolve(strict=False)
    try:
        logical = resolved.relative_to(view.root).as_posix()
    except ValueError:
        # Framework templates referenced by a nested independent domain are
        # outside that domain's repository transaction and remain a live,
        # explicitly external build input.
        return path.read_text(encoding="utf-8") if path.is_file() else None
    return view.read_text(logical) if view.exists(logical) else None


def _view_is_file(path: Path, view: RepositoryView | None) -> bool:
    return _view_text(path, view) is not None


def _glob_matches(rel: str, pattern: str) -> bool:
    """`Path.glob` semantics, not raw `fnmatch`: `*` does NOT cross `/`.

    This matters because the two branches of `_view_glob` below must agree.
    The no-view branch delegates to `Path.glob`, where `*.md` means *this
    directory's* markdown; raw `fnmatch.fnmatchcase` treats `/` as an ordinary
    character, so the view branch answered `*.md` with the entire recursive
    tree — 1978 paths where `Path.glob` returns 25. Found 2026-08-23 when the
    perimeter check spawned one `git log` per match and took two minutes;
    the same call site had been correct without a view and wrong with one.
    """
    parts, pat = rel.split("/"), pattern.split("/")
    return (len(parts) == len(pat)
            and all(fnmatch.fnmatchcase(a, b) for a, b in zip(parts, pat)))


def _view_glob(base: Path, pattern: str,
               view: RepositoryView | None) -> list[Path]:
    if view is None:
        return sorted(base.glob(pattern))
    try:
        relative = base.resolve().relative_to(view.root)
    except ValueError:
        return sorted(base.glob(pattern))
    prefix = "" if relative == Path(".") else relative.as_posix().rstrip("/") + "/"
    out: list[Path] = []
    for logical in view.list_paths():
        raw = logical.as_posix()
        if not raw.startswith(prefix):
            continue
        rel = raw[len(prefix):]
        if _glob_matches(rel, pattern):
            out.append(base.joinpath(*Path(rel).parts))
    return sorted(out)

def _changed_files_recent(root: Path, window: int) -> set[str] | None:
    """Repo-relative POSIX paths MODIFIED in the last `window` commits, or None
    if `root` is not inside a git repo (the check then skips, like provenance).
    Returns all tracked files when there are 0–1 commits (nothing to diff against
    yet — and on the first commit there is no HEAD).

    `--diff-filter=M` deliberately excludes additions: a thing that ARRIVED in
    the window was never "stable, then changed" — it was born. Without the
    filter, delivering framework-shipped `stable` things into a domain (the
    v3.24.0 prompt backfill did exactly this, in nine domains at once) makes
    every one of them report as freshly-churned for the next `window` commits
    — a check firing on healthy state, which is the failure mode
    `a-check-that-always-fires-teaches-the-operator-to-ignore-it` names."""
    cnt = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root,
                         capture_output=True, text=True)
    if cnt.returncode != 0:
        return None
    n = int(cnt.stdout.strip()) if cnt.stdout.strip().isdigit() else 0
    if n <= 1:
        out = subprocess.run(["git", "ls-files"], cwd=root,
                             capture_output=True, text=True)
    else:
        out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=M",
                              f"HEAD~{min(window, n - 1)}", "HEAD"],
                             cwd=root, capture_output=True, text=True)
    if out.returncode != 0:
        return set()
    return {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}


# Placeholder tokens the scaffold substitutes mechanically; anything else in
# square brackets inside a template is authoring work left for the human.
_SUBSTITUTED_TOKENS = {"[domain]", "[Domain]", "[Domain Name]", "[ISO-date]",
                       "[domain-name]"}


def _templates_dir(root: Path,
                   view: RepositoryView | None = None) -> Path | None:
    """The framework templates directory this corpus was scaffolded from:
    local at a framework root, else resolved through the domain's own
    `framework_root` pointer. None (check skips, fails open) when neither
    resolves — a corpus with no reachable templates has nothing to compare."""
    if _view_is_file(root / ".markdownllm", view):
        cand = root / "templates"
        return cand if _view_glob(cand, "*", view) else None
    agents = root / "AGENTS.md"
    atext = _view_text(agents, view)
    if atext is None:
        return None
    meta, _, err = parse_frontmatter(atext, source=agents)
    fr = (meta or {}).get("framework_root") if not err else None
    if not isinstance(fr, str) or not fr:
        return None
    cand = (root / fr / "templates").resolve()
    return cand if cand.is_dir() else None


def _placeholder_tokens(files: list[Path],
                        view: RepositoryView | None = None) -> set[str]:
    """Literal bracket placeholders shipped in the given template files —
    same-builder by construction: the token set IS the template text, so the
    check cannot disagree with what scaffold hands a newborn domain."""
    tokens: set[str] = set()
    for tpl in files:
        try:
            text = _view_text(tpl, view)
        except (OSError, RepositoryViewError):
            continue
        if text is None:
            continue
        for m in re.finditer(r"\[[^\[\]\n]{2,90}\]", text):
            if m.group(0) not in _SUBSTITUTED_TOKENS:
                tokens.add(m.group(0))
    return tokens


def _template_residue_findings(root: Path, corpus,
                               view: RepositoryView | None = None) -> list[Finding]:
    """Unfilled-scaffold sensor (cohesiveness-sensors plan). A `type: skill`
    thing whose body still carries the templates' own bracket placeholders was
    scaffolded and never authored — the drift class the 2026-08-01 estate sweep
    found running unflagged for weeks in live domains, invisible to validate
    (structurally the stubs are valid things). Threshold ≥3 distinct tokens:
    an authored skill that legitimately uses a bracket example (observed in the
    wild) stays quiet; a verbatim template (11–30 tokens) cannot. Info — the
    finding reads "never authored", not "bad skill"; filling it from earned
    insights vs parking the domain is the operator's route."""
    templates = _templates_dir(root, view)
    if templates is None:
        return []
    out: list[Finding] = []
    skill_tokens = _placeholder_tokens(
        _view_glob(templates, "domain-*.skill.md.template", view), view)
    if skill_tokens:
        for t in corpus.things:
            if str(t.meta.get("type")) != "skill":
                continue
            found = sorted(tok for tok in skill_tokens if tok in t.body)
            if len(found) >= 3:
                sample = ", ".join(f"`{tok}`" for tok in found[:3])
                out.append(Finding(SEV_INFO, t.id or t.path.name,
                    f"retains {len(found)} template placeholder(s) ({sample}, …) "
                    f"— scaffolded, never authored. Fill it from the domain's "
                    f"earned insights, or park it deliberately"))
    agents = root / "AGENTS.md"
    agents_tpl = templates / "AGENTS.md.template"
    agents_text = _view_text(agents, view)
    if agents_text is not None and _view_is_file(agents_tpl, view):
        tokens = _placeholder_tokens([agents_tpl], view)
        found = sorted(tok for tok in tokens
                       if tok in agents_text)
        if len(found) >= 3:
            sample = ", ".join(f"`{tok}`" for tok in found[:3])
            out.append(Finding(SEV_INFO, "AGENTS.md",
                f"retains {len(found)} template placeholder(s) ({sample}, …) — "
                f"the entry file was scaffolded and never authored"))
    return out


def template_source_findings(root: Path,
                             view: RepositoryView | None = None) -> list[Finding]:
    """Check framework birth sources before they multiply into domains.

    This is intentionally narrower than validating unresolved placeholders as
    real things.  It checks facts that are decidable on the source itself:
    frontmatter must actually start at byte zero when a template declares a
    thing, reserved lifecycle words must be valid, relation choices must exist
    in the scaffold schema, and shipped root-relative instructions must not
    point at a path that cannot exist.
    """
    out: list[Finding] = []
    schema_path = root / "templates" / "_schema.yaml.template"
    try:
        schema_text = _view_text(schema_path, view)
        schema = load_yaml(schema_text or "", source=schema_path) or {}
        relations = set(schema.get("relations") or [])
    except (OSError, yaml.YAMLError):
        relations = set()

    sources = _view_glob(root / "templates", "**/*.md.template", view)
    # fnmatch's **/ requires a slash; include root-level templates explicitly.
    sources += _view_glob(root / "templates", "*.md.template", view)
    sources += _view_glob(root / "evidence", "*.md.template", view)
    sources = sorted(set(sources))
    for source in sources:
        text = _view_text(source, view) or ""
        rel = source.relative_to(root).as_posix()
        delim = re.search(r"(?m)^---\s*$", text)
        if not delim:
            continue  # prose/code template, not a thing source
        second = re.search(r"(?m)^---\s*$", text[delim.end():])
        if not second:
            out.append(Finding(SEV_ERROR, rel,
                "template opens YAML frontmatter but never closes it"))
            continue
        front = text[delim.end():delim.end() + second.start()]
        if re.search(r"(?m)^\s*type\s*:", front) and text[:delim.start()].strip():
            out.append(Finding(SEV_ERROR, rel,
                "thing template has content before its opening `---`; the "
                "frontmatter parser will ignore the metadata"))
        typ = re.search(r"(?m)^\s*type\s*:\s*([^#\n]+)", front)
        status = re.search(r"(?m)^\s*status\s*:\s*([^#\n]+)", front)
        if typ and status:
            type_value = typ.group(1).strip()
            status_value = status.group(1).strip()
            allowed = _TEMPLATE_STATUSES.get(type_value)
            if allowed and status_value not in allowed:
                out.append(Finding(SEV_ERROR, rel,
                    f"template gives reserved type `{type_value}` status "
                    f"`{status_value}`; allowed: {', '.join(allowed)}"))
        for raw in re.findall(r"(?m)^\s*relation\s*:\s*([^#\n]+)", front):
            choices = {v.strip() for v in raw.split("|") if v.strip()}
            missing = choices - relations
            if relations and missing:
                out.append(Finding(SEV_ERROR, rel,
                    "template relation choice(s) absent from the scaffold "
                    f"schema: {', '.join(sorted(missing))}"))
        if 'applies_to: "[domain]/' in front:
            out.append(Finding(SEV_ERROR, rel,
                "template applies_to is rooted below the domain name even "
                "though a domain is opened at its own root; use `**/*.md`"))

    for skill in _view_glob(root / "examples", "*/skills/*.md", view):
        if "../thing.md" in (_view_text(skill, view) or ""):
            out.append(Finding(SEV_ERROR, skill.relative_to(root).as_posix(),
                "example skill points at nonexistent `../thing.md`; resolve "
                "`{framework_root}/thing.md` from AGENTS.md"))
    return out


# --- the entry file's two annotated prose sections (F8a check leg) --------
#
# Both sections are AUTHORED prose carrying a derivable annotation, which is
# why they are checked and not generated: the one-line descriptions are the
# sections' actual value, and a generator would delete them to own a fact it
# could have merely verified. Delete > derive > check, and this is the third
# case.
#
# Null-result discipline (`a-check-run-where-it-cannot-see-mints-a-false-
# finding`): each helper distinguishes "nothing wrong" from "could not look".
# A section that cannot be located reports that as a Warning rather than
# returning a clean list, because a silently-skipped check reads exactly like
# a passing one.

_CATALOG_HEADING = "## Framework Specifications (Things)"
_CATALOG_BULLET = re.compile(r"^- \*\*([A-Za-z0-9_./-]+\.md)\*\*", re.M)
_CATALOG_ANNOTATION = re.compile(
    r"\(`type: ([a-z-]+)`, `status: ([a-z-]+)`")
_TIER2_MARKER = "**Tier 2 — Load on demand by query type:**"


def _section_text(text: str, heading: str) -> str | None:
    """The body of one `## ` section, or None when the heading is absent."""
    start = text.find(heading)
    if start < 0:
        return None
    rest = text[start + len(heading):]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def _catalog_annotation_findings(root: Path, atext: str,
                                 view: RepositoryView | None) -> list[Finding]:
    """Each catalog bullet's `(type:, status:)` pair against live frontmatter.

    Error, because it is the same class as kernel drift: a one-line fix, and
    the point is that a spec's status change and its catalog line land in the
    same commit rather than one release apart.
    """
    section = _section_text(atext, _CATALOG_HEADING)
    if section is None:
        return [Finding(SEV_WARNING, "AGENTS.md",
                        f"`{_CATALOG_HEADING}` not found — the catalog "
                        f"annotation check could not run (this is 'could not "
                        f"look', not 'nothing wrong')")]
    findings: list[Finding] = []
    bullets = list(_CATALOG_BULLET.finditer(section))
    if not bullets:
        return [Finding(SEV_WARNING, "AGENTS.md",
                        "no catalog bullets parsed from the spec catalog — the "
                        "annotation check could not run; the bullet format "
                        "changed, or the section moved")]
    for i, m in enumerate(bullets):
        name = m.group(1)
        chunk = section[m.end():
                        bullets[i + 1].start() if i + 1 < len(bullets)
                        else len(section)]
        ann = _CATALOG_ANNOTATION.search(chunk)
        if not ann:          # authored freedom: a bullet may carry no annotation
            continue
        stated_type, stated_status = ann.group(1), ann.group(2)
        text = _view_text(root / name, view)
        if text is None:
            findings.append(Finding(SEV_ERROR, "spec catalog",
                f"`{name}` is listed in the catalog but not present on disk"))
            continue
        meta, _, err = parse_frontmatter(text, source=root / name)
        if err or not isinstance(meta, dict):
            continue         # frontmatter errors are validate's finding, not this one
        actual_type = str(meta.get("type", ""))
        actual_status = str(meta.get("status", ""))
        if actual_type != stated_type or actual_status != stated_status:
            findings.append(Finding(SEV_ERROR, "spec catalog",
                f"`{name}` is annotated (`{stated_type}`, `{stated_status}`) "
                f"but its frontmatter says (`{actual_type}`, "
                f"`{actual_status}`) — fix the catalog line in the commit "
                f"that changed the spec"))
    return findings


def _tier2_routing_findings(root: Path, atext: str,
                            view: RepositoryView | None) -> list[Finding]:
    """Every Tier-2 spec in `TIERS` has a routing row; every routed file exists.

    ONE DIRECTION ONLY, deliberately. The table legitimately routes surfaces
    that are outside both `TIERS` and the `.markdownllm` catalog — the
    human-facing `docs/` guides — so a mirror check would fire on correct
    prose. The reverse direction is already total where it can be:
    `TIERS` <-> catalog, checked both ways below.
    """
    start = atext.find(_TIER2_MARKER)
    if start < 0:
        return [Finding(SEV_WARNING, "AGENTS.md",
                        "the Tier-2 routing table marker was not found — the "
                        "routing completeness check could not run")]
    rows = []
    for line in atext[start:].splitlines()[1:]:
        if line.startswith("|"):
            rows.append(line)
        elif rows:
            break            # the table ended
    if not rows:
        return [Finding(SEV_WARNING, "AGENTS.md",
                        "no Tier-2 routing rows parsed — the completeness "
                        "check could not run")]
    routed = {f for row in rows
              for f in re.findall(r"`([A-Za-z0-9_./-]+\.md)`", row)}
    findings: list[Finding] = []
    for name in sorted(set(TIERS.get("Tier 2 (on demand)", [])) - routed):
        findings.append(Finding(SEV_ERROR, "Tier-2 routing",
            f"`{name}` is a Tier-2 spec in the TIERS map "
            f"(tools/markdownllm/repo.py) but no routing row in AGENTS.md "
            f"names it — a spec nothing routes to is a spec nothing loads"))
    for name in sorted(routed):
        if not _view_is_file(root / name, view):
            findings.append(Finding(SEV_ERROR, "Tier-2 routing",
                f"a routing row names `{name}`, which is not on disk"))
    return findings


# --- perimeter currency (F8b; external review R2) -------------------------
#
# `cumulative-drift-is-invisible-to-per-change-walks`: the surfaces outside
# every individual blast radius are not protected by a sharper per-change
# walk, they are protected by an interval. This makes the interval mechanical.
#
# Same-builder, no suppression list, and NO NEW MARKER: the pin is read from
# git rather than authored, so this check creates no surface of its own to
# drift. For each perimeter file, the version the sentinel carried at that
# file's last-touching commit is the version it was last walked against.
#
# Two minors, not one, because of a real artifact rather than caution: a
# surface reconciled DURING a release cycle is touched before the version
# bump lands, so it reads as exactly one behind while being perfectly
# current. One would fire on correct work every cycle, and
# `a-check-that-always-fires-teaches-the-operator-to-ignore-it` is the
# failure that ends a check's usefulness permanently.
_PERIMETER_MINOR_LAG = 2
_PERIMETER_NEVER = {"AGENTS.md", "kernel.md", "CHANGELOG.md"}


def _minor_pair(version: str) -> tuple[int, int] | None:
    m = re.match(r"^(\d+)\.(\d+)", version.strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


def _perimeter_files(root: Path, specs: list, view: RepositoryView | None) -> list[str]:
    """Human-facing markdown outside the spec catalog: the release perimeter.

    Derived, not listed. A `type: specification` is excluded because the
    catalog and TIERS checks already own it; `examples/` is excluded because
    the `framework_version_seen` check above already owns it.
    """
    names: list[str] = []
    for base, pattern in ((root, "*.md"), (root / "docs", "*.md")):
        for path in _view_glob(base, pattern, view):
            rel = path.relative_to(root).as_posix()
            if rel in _PERIMETER_NEVER or rel in set(specs):
                continue
            meta, _, err = parse_frontmatter(
                _view_text(path, view) or "", source=path)
            if not err and isinstance(meta, dict) \
                    and str(meta.get("type")) == "specification":
                continue
            names.append(rel)
    return sorted(set(names))


def _perimeter_currency_findings(root: Path, specs: list, current: str,
                                 view: RepositoryView | None) -> list[Finding]:
    now = _minor_pair(current)
    if now is None:
        return []
    files = _perimeter_files(root, specs, view)
    if not files:
        return []
    # ONE history walk for every perimeter file, not one per file (F12's
    # lesson: the cost of this check is process spawns, not computation).
    # `git log --name-only` over all of them at once, newest first; the first
    # block naming a file is that file's last touch.
    try:
        log = subprocess.run(
            ["git", "log", "--format=%x01%H", "--name-only", "--", *files],
            cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60)
    except (OSError, subprocess.SubprocessError):
        return [Finding(SEV_INFO, "perimeter",
            "could not be dated — `git log` was unavailable, so this is "
            "'could not look', not 'current'")]
    if log.returncode != 0:
        return []                             # not a git repo: nothing to date
    last_touch: dict[str, str] = {}
    for block in log.stdout.split("\x01")[1:]:
        lines = block.splitlines()
        if not lines:
            continue
        sha = lines[0].strip()
        for name in lines[1:]:
            name = name.strip()
            if name and name not in last_touch:
                last_touch[name] = sha

    seen: dict[str, str | None] = {}          # sha -> sentinel version there
    findings: list[Finding] = []
    for rel in files:
        sha = last_touch.get(rel, "")
        if not sha:
            continue                          # untracked/new: nothing to date
        if sha not in seen:
            shown = subprocess.run(
                ["git", "show", f"{sha}:.markdownllm"],
                cwd=root, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=20)
            found = None
            if shown.returncode == 0:
                m = re.search(r"^version:\s*(\S+)", shown.stdout, re.M)
                found = m.group(1) if m else None
            seen[sha] = found
        then = _minor_pair(seen[sha] or "")
        if then is None:
            continue
        lag = (now[0] - then[0]) * 1000 + (now[1] - then[1])
        if lag >= _PERIMETER_MINOR_LAG:
            findings.append(Finding(SEV_INFO, "perimeter",
                f"`{rel}` was last touched when the framework was "
                f"{seen[sha]}; it is now {current} — walk it, or accept that "
                f"it teaches an older shape"))
    return findings


# --- review-9 survivor promotions (F8b) -----------------------------------
#
# The ninth review's seven survivors were all hand-restated mirrors of tool
# facts. Two of them promote cleanly into same-builder checks; the rest do
# not, and saying so is part of the promotion — see the run record for the
# ones deliberately declined.


def _redundant_known_fields_findings(corpus) -> list[Finding]:
    """A `known_fields` entry the tool already owns universally.

    Survivor 7 was `CORE_FIELDS` violating its own admission criterion: the
    framework root had been made to register the framework's own vocabulary in
    its schema. This is that fault caught from the inside — whenever a field
    joins `CORE_FIELDS`, every domain that had registered it becomes
    redundant, and nothing told them. Info: a redundant declaration is inert,
    not wrong, and removing it is the domain's call.
    """
    if not corpus.schema:
        return []
    declared = corpus.schema.get("known_fields") or []
    if not isinstance(declared, list):
        return []
    return [Finding(SEV_INFO, "_schema.yaml",
            f"`known_fields` registers `{name}`, which is now universal in "
            f"CORE_FIELDS — the framework owns it; drop the registration")
            for name in sorted({str(n) for n in declared} & set(CORE_FIELDS))]


def _index_signal_enumeration_findings(
        root: Path, specs: list, view: RepositoryView | None) -> list[Finding]:
    """Prose that enumerates the derived-index signals must enumerate them all.

    Survivor 6: the provenance index is a standard derived index the tool
    rebuilds by default, yet five surfaces enumerated three signals. Keyed to
    `INDEX_FILES` — the constant the rebuild loop itself walks — so the check
    cannot disagree with truth, and it needs no suppression list: a sentence
    that mentions "signal" and names two or more of them is enumerating them,
    and an enumeration that stops short is the drift.

    Scoped structurally to LIVE operative surfaces (the entry file, the
    kernel, the catalogued specs). `CHANGELOG.md`, `reviews/` and `things/`
    are excluded because they are historical records, where "three signals"
    was true when written. That exclusion is defined by what a surface *is*,
    not by which findings were inconvenient — the property that separates it
    from the suppression list that sank the retired-vocabulary check.
    """
    signals = sorted(INDEX_FILES)
    findings: list[Finding] = []
    for name in ["AGENTS.md", "kernel.md"] + [str(s) for s in specs]:
        text = _view_text(root / name, view)
        if text is None:
            continue
        for sentence in re.split(r"(?<=[.:])\s+", text):
            if "signal" not in sentence.lower():
                continue
            present = {s for s in signals
                       if re.search(r"\b" + re.escape(s) + r"\b", sentence, re.I)}
            if 2 <= len(present) < len(signals):
                missing = ", ".join(f"`{s}`" for s in sorted(set(signals) - present))
                findings.append(Finding(SEV_WARNING, name,
                    f"enumerates derived-index signals but omits {missing} — "
                    f"`INDEX_FILES` in tools/markdownllm/indexes.py is the "
                    f"authority ({len(signals)} signals); name them all or "
                    f"name none and point at the authority"))
                break        # one finding per surface is enough to act on
    return findings


def coherence_findings(root: Path, window: int,
                       view: RepositoryView | None = None) -> list[Finding]:
    """Mechanical checks over the 'dark region' a hand-walk currently guards
    (AGENTS.md -> Walking the Dark Region). Corpus-general by design: the
    stable-staleness, unused-vocabulary, zero-run-definition, and
    derived-index-drift checks run on
    ANY corpus, so a domain inherits them through the same pre-commit hook; the
    foundational-spec / TIERS / kernel-drift checks switch on only at a framework
    root (where `.markdownllm` is present). None of this is judgment — staleness
    and unused vocabulary are Info *proxies*; the semantic calls (is it *really*
    stable; is that empty type intended) stay the agent's."""
    corpus, _ = scan(root, view)
    findings: list[Finding] = []

    # --- general: stable-staleness (Info) --------------------------------
    changed = _changed_files_recent(root, window)
    if changed is not None:
        for t in corpus.things:
            if str(t.meta.get("status")) != "stable":
                continue
            rel = t.path.relative_to(root).as_posix()
            if rel in changed:
                findings.append(Finding(SEV_INFO, t.id or rel,
                    f"marked `stable` but changed within the last {window} "
                    f"commits — confirm the label still reflects reality"))

    # --- general: unused declared vocabulary (Info) ----------------------
    # A domain's _schema.yaml is its own spec of its types; a declared type that
    # no thing uses is dead vocabulary worth surfacing — but only Info, since the
    # framework explicitly allows foreseen-but-undeployed types.
    if corpus.schema:
        declared = set(corpus.schema.get("types") or {})
        used = {str(t.meta.get("type")) for t in corpus.things}
        for typ in sorted(declared - used):
            findings.append(Finding(SEV_INFO, "_schema.yaml",
                f"declared type `{typ}` is used by no thing — dead vocabulary?"))

    # --- general: zero-run workflow definition (Info) --------------------
    # A defined process with no run governs nothing (estate synthesis
    # 2026-08, F4 / queue row 4): three corpora wrote their method down and
    # then worked beside it, and a nine-domain census re-found the class by
    # hand on 2026-08-28 — exactly the walk this sensor retires. Population
    # is scoped by who can still perform the remedy
    # (an-advisory-is-scoped-by-who-can-perform-its-remedy): `draft` stays
    # silent — draft-until-first-run is a legitimate declared pattern — and
    # `deprecated` is retired, its remedy spent. `stable` is deliberately IN
    # the population although RESERVED_TERMINAL settles it for the
    # *authoring* lifecycle: a definition settled as text with zero runs is
    # the archetype instance ("documentation, not process"), and giving it
    # its first run is still performable. Quiet when healthy: one run of any
    # status, ever, answers it.
    run_targets = {str(t.meta.get("definition")) for t in corpus.things
                   if str(t.meta.get("type")) == "workflow-run"
                   and t.meta.get("definition") is not None}
    for t in corpus.things:
        if str(t.meta.get("type")) != "workflow-definition":
            continue
        status = str(t.meta.get("status"))
        if status not in ("evolving", "stable"):
            continue
        if t.id is not None and str(t.id) in run_targets:
            continue
        findings.append(Finding(SEV_INFO, t.id or t.path.name,
            f"workflow-definition is `{status}` with zero workflow-runs "
            f"pointing at it via `definition:` — a defined process with no "
            f"run governs nothing; give it its first run, or retire/park it "
            f"with the reason recorded"))

    # --- general: a domain registering the framework's own vocabulary ----
    findings.extend(_redundant_known_fields_findings(corpus))

    # --- general: template residue in skills / entry file (Info) ---------
    findings.extend(_template_residue_findings(root, corpus, view))

    # --- general: derived-index drift (Error, deployed indexes only) -----
    findings.extend(index_drift_findings(root, corpus))

    # --- general: domain-kernel drift (Error, kernel-shaped AGENTS.md only) ---
    # Opt-in by construction: only domains whose AGENTS.md carries managed
    # `<!-- generated:NAME -->` blocks are checked. Same builder as
    # `mdllm domain-kernel`, so the check cannot disagree with the generator.
    agents = root / "AGENTS.md"
    atext = _view_text(agents, view)
    if atext is not None:
        ameta, _, aerr = parse_frontmatter(atext, source=agents)
        if not aerr:
            _, dk_drifted = domain_kernel_status(
                atext, build_domain_kernel_blocks(root, ameta or {}, view))
            for name in dk_drifted:
                findings.append(Finding(SEV_ERROR, "AGENTS.md",
                    f"domain-kernel block `{name}` drifted from a fresh build — "
                    f"run `mdllm domain-kernel .` and commit the result"))

    # --- general: operating-layer vocabulary drift (Warning) --------------
    # The skills and the entry file, read against the schema they claim to
    # describe. The one slice of operating-layer drift that is not judgement:
    # a type, status, or field a skill instructs and the corpus never
    # declared is an instruction whose product the floor rejects. Keyed to
    # `_schema.yaml` and the tool's reserved sets, so no suppression list
    # exists or could — see skill_vocabulary.py for the full reasoning.
    findings.extend(skill_vocabulary_findings(corpus, atext))

    # --- framework root only ---------------------------------------------
    if _view_is_file(root / ".markdownllm", view):
        findings.extend(template_source_findings(root, view))

        # The entry file's two annotated prose sections. Checked, not
        # generated — see the helpers above for why.
        if atext is None:
            findings.append(Finding(SEV_WARNING, "AGENTS.md",
                "not readable from the selected view — the entry-file "
                "catalog and routing checks could not run"))
        else:
            findings.extend(_catalog_annotation_findings(root, atext, view))
            findings.extend(_tier2_routing_findings(root, atext, view))

        sentinel = root / ".markdownllm"
        try:
            data = load_yaml(
                _view_text(sentinel, view) or "", source=sentinel) or {}
        except yaml.YAMLError as exc:
            findings.append(Finding(
                SEV_ERROR, ".markdownllm",
                f"sentinel is invalid YAML: {exc}"))
            return findings
        if not isinstance(data, dict):
            findings.append(Finding(
                SEV_ERROR, ".markdownllm",
                "sentinel must be a YAML mapping"))
            return findings
        specs = data.get("foundational_specs") or []

        # foundational_specs <-> filesystem. `kernel` skips a missing spec
        # silently; here a listed-but-absent spec is an Error.
        for name in specs:
            if not _view_is_file(root / name, view):
                findings.append(Finding(SEV_ERROR, "foundational_specs",
                    f"`{name}` listed in .markdownllm but not present on disk"))

        # TIERS <-> foundational_specs: every foundational spec has a tier entry
        # in the loading map. A missing one means tier routing drifted from the
        # catalog — the dark-region class with the worst track record.
        tier_files = ({f for files in TIERS.values() for f in files}
                      - {"AGENTS.md", "kernel.md"})
        for name in specs:
            if name not in tier_files:
                findings.append(Finding(SEV_WARNING, "TIERS",
                    f"foundational spec `{name}` has no entry in the TIERS map "
                    f"(tools/markdownllm/repo.py) — tier routing drifted from the catalog"))

        # ...and the mirror (directional graph reads come in inbound/outbound
        # pairs): every TIERS entry must be in the catalog. A file routed by
        # tier but absent from .markdownllm is loadable-but-uncatalogued —
        # the reverse drift the one-directional check was blind to (review 6,
        # finding 6: thing-lifecycle.md sat exactly there).
        for name in sorted(tier_files):
            if name not in specs:
                findings.append(Finding(SEV_WARNING, "TIERS",
                    f"`{name}` is in the TIERS map (tools/markdownllm/repo.py) but not in "
                    f".markdownllm foundational_specs — loading map drifted "
                    f"from the catalog"))

        # Example staleness: an example's framework_version_seen pins the
        # framework version it was last walked against; a pin behind the
        # sentinel means the example teaches an old shape (review 6: both
        # examples sat at 3.4.0 for thirteen minor versions, invisibly).
        # Same-builder — the sentinel is the only version source — and no
        # suppression list: the only way to quiet it is the walk + re-pin.
        fw_version = str(data.get("version", ""))
        for ex in _view_glob(root / "examples", "*/AGENTS.md", view):
            emeta, _, _ = parse_frontmatter(_view_text(ex, view) or "", source=ex)
            seen = str(emeta.get("framework_version_seen", ""))
            if fw_version and seen and seen != fw_version:
                findings.append(Finding(SEV_WARNING, f"examples/{ex.parent.name}",
                    f"pinned at framework_version_seen {seen} but the framework "
                    f"is {fw_version} — walk the example against the current "
                    f"shape, then re-pin"))

        # Prose that enumerates the derived-index signals must enumerate all
        # of them (review-9 survivor 6, promoted).
        findings.extend(_index_signal_enumeration_findings(root, specs, view))

        # ...and the rest of the perimeter, dated from git rather than from a
        # pin the surface would have to carry (external review R2).
        if fw_version:
            findings.extend(
                _perimeter_currency_findings(root, specs, fw_version, view))

        # kernel drift, via the shared builder (cannot disagree with what
        # `mdllm kernel` would write — same source).
        kpath = root / "kernel.md"
        kbody, _, _, _ = build_kernel(root, specs, token_counter(), view)
        ktext = _view_text(kpath, view)
        if ktext is None:
            findings.append(Finding(SEV_ERROR, "kernel.md",
                "missing — run `mdllm kernel` to generate it"))
        else:
            _, ex_body, _ = parse_frontmatter(ktext, source=kpath)
            if normalize_newlines(ex_body).strip() != kbody.strip():
                findings.append(Finding(SEV_ERROR, "kernel.md",
                    "DRIFT — spec kernel blocks changed since kernel.md was "
                    "generated; run `mdllm kernel` and commit the result"))

        # framework-map subcommand count <-> the actual CLI surface. The map's
        # own "Keeping This Map Honest" note already pins View 3 to `mdllm
        # --help`; this makes that pin mechanical so the hand-drawn count can't
        # silently drift when a subcommand lands — the exact repeat-offender the
        # 2026-06d retrospective said to make checkable. Truth = the subparser
        # registration calls in this file, one per subcommand.
        fmap = root / "docs" / "framework-map.md"
        fmap_text = _view_text(fmap, view)
        cli_text = _view_text(CLI_REGISTRY_FILE, view)
        if fmap_text is not None and cli_text is not None:
            actual = len(re.findall(r"sub\.add_parser\(",
                                    cli_text))
            stated = re.search(r"(\d+)\s+mechanical subcommands",
                               fmap_text)
            if stated and int(stated.group(1)) != actual:
                findings.append(Finding(SEV_WARNING, "framework-map.md",
                    f"says {stated.group(1)} mechanical subcommands but the CLI "
                    f"defines {actual} — update the count and View 3 in the same "
                    f"commit the subcommand landed"))

    return findings


def cmd_coherence(args) -> int:
    root = Path(args.path).resolve()
    mode = getattr(args, "view", "worktree")
    try:
        view = (RepositoryView.index(root) if mode == "index"
                else RepositoryView.worktree(root))
    except RepositoryViewError as exc:
        print(f"mdllm: cannot construct {mode} coherence view: {exc}")
        return 1
    findings = coherence_findings(root, args.window, view)
    errors = [x for x in findings if x.severity == SEV_ERROR]
    warnings = [x for x in findings if x.severity == SEV_WARNING]
    infos = [x for x in findings if x.severity == SEV_INFO]
    if not args.quiet or errors:
        is_fw = _view_is_file(root / ".markdownllm", view)
        print(f"## Coherence Report — {root}")
        print(f"view: {view.identifier}")
        print(f"scope: {'framework root (+ catalog/kernel checks)' if is_fw else 'corpus (general checks only)'}\n")
        if not findings:
            print("No coherence issues found.")
        for title, group in (("Errors (must fix)", errors),
                             ("Warnings (should fix)", warnings),
                             ("Info (worth knowing)", infos)):
            if group:
                print(f"### {title}")
                for x in group:
                    print(f"- **{x.thing}**: {x.message}")
                print()
    return 1 if errors else 0
