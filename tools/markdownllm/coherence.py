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
from pathlib import Path

import yaml

from .domain_kernel import build_domain_kernel_blocks, domain_kernel_status
from .indexes import index_drift_findings
from .kernel_gen import _token_counter, build_kernel
from .model import Finding, SEV_ERROR, SEV_INFO, SEV_WARNING, parse_frontmatter, scan
from .repo import TIERS

# The framework-map count check reads the file that registers the subparsers
# (truth = the `sub.add_parser(` calls) — the CLI module beside this one.
CLI_REGISTRY_FILE = Path(__file__).resolve().parent / "cli.py"

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


def _templates_dir(root: Path) -> Path | None:
    """The framework templates directory this corpus was scaffolded from:
    local at a framework root, else resolved through the domain's own
    `framework_root` pointer. None (check skips, fails open) when neither
    resolves — a corpus with no reachable templates has nothing to compare."""
    if (root / ".markdownllm").is_file():
        cand = root / "templates"
        return cand if cand.is_dir() else None
    agents = root / "AGENTS.md"
    if not agents.is_file():
        return None
    meta, _, err = parse_frontmatter(agents.read_text(encoding="utf-8"))
    fr = (meta or {}).get("framework_root") if not err else None
    if not isinstance(fr, str) or not fr:
        return None
    cand = (root / fr / "templates").resolve()
    return cand if cand.is_dir() else None


def _placeholder_tokens(files: list[Path]) -> set[str]:
    """Literal bracket placeholders shipped in the given template files —
    same-builder by construction: the token set IS the template text, so the
    check cannot disagree with what scaffold hands a newborn domain."""
    tokens: set[str] = set()
    for tpl in files:
        try:
            text = tpl.read_text(encoding="utf-8")
        except OSError:
            continue
        for m in re.finditer(r"\[[^\[\]\n]{2,90}\]", text):
            if m.group(0) not in _SUBSTITUTED_TOKENS:
                tokens.add(m.group(0))
    return tokens


def _template_residue_findings(root: Path, corpus) -> list[Finding]:
    """Unfilled-scaffold sensor (cohesiveness-sensors plan). A `type: skill`
    thing whose body still carries the templates' own bracket placeholders was
    scaffolded and never authored — the drift class the 2026-08-01 estate sweep
    found running unflagged for weeks in live domains, invisible to validate
    (structurally the stubs are valid things). Threshold ≥3 distinct tokens:
    an authored skill that legitimately uses a bracket example (observed in the
    wild) stays quiet; a verbatim template (11–30 tokens) cannot. Info — the
    finding reads "never authored", not "bad skill"; filling it from earned
    insights vs parking the domain is the operator's route."""
    templates = _templates_dir(root)
    if templates is None:
        return []
    out: list[Finding] = []
    skill_tokens = _placeholder_tokens(
        sorted(templates.glob("domain-*.skill.md.template")))
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
    if agents.is_file() and agents_tpl.is_file():
        tokens = _placeholder_tokens([agents_tpl])
        found = sorted(tok for tok in tokens
                       if tok in agents.read_text(encoding="utf-8"))
        if len(found) >= 3:
            sample = ", ".join(f"`{tok}`" for tok in found[:3])
            out.append(Finding(SEV_INFO, "AGENTS.md",
                f"retains {len(found)} template placeholder(s) ({sample}, …) — "
                f"the entry file was scaffolded and never authored"))
    return out


def coherence_findings(root: Path, window: int) -> list[Finding]:
    """Mechanical checks over the 'dark region' a hand-walk currently guards
    (AGENTS.md -> Walking the Dark Region). Corpus-general by design: the
    stable-staleness, unused-vocabulary, and derived-index-drift checks run on
    ANY corpus, so a domain inherits them through the same pre-commit hook; the
    foundational-spec / TIERS / kernel-drift checks switch on only at a framework
    root (where `.markdownllm` is present). None of this is judgment — staleness
    and unused vocabulary are Info *proxies*; the semantic calls (is it *really*
    stable; is that empty type intended) stay the agent's."""
    corpus, _ = scan(root)
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
    findings.extend(_template_residue_findings(root, corpus))

    # --- general: derived-index drift (Error, deployed indexes only) -----
    findings.extend(index_drift_findings(root, corpus))

    # --- general: domain-kernel drift (Error, kernel-shaped AGENTS.md only) ---
    # Opt-in by construction: only domains whose AGENTS.md carries managed
    # `<!-- generated:NAME -->` blocks are checked. Same builder as
    # `mdllm domain-kernel`, so the check cannot disagree with the generator.
    agents = root / "AGENTS.md"
    if agents.is_file():
        atext = agents.read_text(encoding="utf-8")
        ameta, _, aerr = parse_frontmatter(atext)
        if not aerr:
            _, dk_drifted = domain_kernel_status(
                atext, build_domain_kernel_blocks(root, ameta or {}))
            for name in dk_drifted:
                findings.append(Finding(SEV_ERROR, "AGENTS.md",
                    f"domain-kernel block `{name}` drifted from a fresh build — "
                    f"run `mdllm domain-kernel .` and commit the result"))

    # --- framework root only ---------------------------------------------
    if (root / ".markdownllm").is_file():
        data = yaml.safe_load((root / ".markdownllm").read_text(encoding="utf-8")) or {}
        specs = data.get("foundational_specs") or []

        # foundational_specs <-> filesystem. `kernel` skips a missing spec
        # silently; here a listed-but-absent spec is an Error.
        for name in specs:
            if not (root / name).is_file():
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
        for ex in sorted((root / "examples").glob("*/AGENTS.md")):
            emeta, _, _ = parse_frontmatter(ex.read_text(encoding="utf-8"))
            seen = str(emeta.get("framework_version_seen", ""))
            if fw_version and seen and seen != fw_version:
                findings.append(Finding(SEV_WARNING, f"examples/{ex.parent.name}",
                    f"pinned at framework_version_seen {seen} but the framework "
                    f"is {fw_version} — walk the example against the current "
                    f"shape, then re-pin"))

        # kernel drift, via the shared builder (cannot disagree with what
        # `mdllm kernel` would write — same source).
        kpath = root / "kernel.md"
        kbody, _, _, _ = build_kernel(root, specs, _token_counter())
        if not kpath.exists():
            findings.append(Finding(SEV_ERROR, "kernel.md",
                "missing — run `mdllm kernel` to generate it"))
        else:
            _, ex_body, _ = parse_frontmatter(kpath.read_text(encoding="utf-8"))
            if ex_body.strip() != kbody.strip():
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
        if fmap.is_file():
            actual = len(re.findall(r"sub\.add_parser\(",
                                    CLI_REGISTRY_FILE.read_text(encoding="utf-8")))
            stated = re.search(r"(\d+)\s+mechanical subcommands",
                               fmap.read_text(encoding="utf-8"))
            if stated and int(stated.group(1)) != actual:
                findings.append(Finding(SEV_WARNING, "framework-map.md",
                    f"says {stated.group(1)} mechanical subcommands but the CLI "
                    f"defines {actual} — update the count and View 3 in the same "
                    f"commit the subcommand landed"))

    return findings


def cmd_coherence(args) -> int:
    root = Path(args.path).resolve()
    findings = coherence_findings(root, args.window)
    errors = [x for x in findings if x.severity == SEV_ERROR]
    warnings = [x for x in findings if x.severity == SEV_WARNING]
    infos = [x for x in findings if x.severity == SEV_INFO]
    if not args.quiet or errors:
        is_fw = (root / ".markdownllm").is_file()
        print(f"## Coherence Report — {root}")
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
