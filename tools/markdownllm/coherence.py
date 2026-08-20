"""Dark-region coherence checks — generated-artifact freshness and
catalog/filesystem integrity.

Corpus-general by design: stable-staleness, unused vocabulary, derived-index
and domain-kernel drift run on any corpus; the foundational-spec / TIERS /
kernel-drift / example-staleness / framework-map checks switch on only at a
framework root. Runs in the pre-commit hook.
"""

from __future__ import annotations

import re
import subprocess
import fnmatch
from pathlib import Path

import yaml

from .domain_kernel import build_domain_kernel_blocks, domain_kernel_status
from .indexes import index_drift_findings
from .kernel_gen import build_kernel, normalize_newlines, token_counter
from .model import (Finding, RESERVED_STATUSES, SEV_ERROR, SEV_INFO,
                    SEV_WARNING, parse_frontmatter, scan)
from .repo import TIERS
from .repository_view import RepositoryView, RepositoryViewError
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
        if fnmatch.fnmatchcase(rel, pattern):
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


def coherence_findings(root: Path, window: int,
                       view: RepositoryView | None = None) -> list[Finding]:
    """Mechanical checks over the 'dark region' a hand-walk currently guards
    (AGENTS.md -> Walking the Dark Region). Corpus-general by design: the
    stable-staleness, unused-vocabulary, and derived-index-drift checks run on
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

    # --- framework root only ---------------------------------------------
    if _view_is_file(root / ".markdownllm", view):
        findings.extend(template_source_findings(root, view))
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
