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
# (truth = the `sub.add_parser(` calls). Until the cli move lands that is the
# entry shim itself.
CLI_REGISTRY_FILE = Path(__file__).resolve().parents[1] / "mdllm.py"

def _changed_files_recent(root: Path, window: int) -> set[str] | None:
    """Repo-relative POSIX paths changed in the last `window` commits, or None
    if `root` is not inside a git repo (the check then skips, like provenance).
    Returns all tracked files when there are 0–1 commits (nothing to diff against
    yet — and on the first commit there is no HEAD)."""
    cnt = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=root,
                         capture_output=True, text=True)
    if cnt.returncode != 0:
        return None
    n = int(cnt.stdout.strip()) if cnt.stdout.strip().isdigit() else 0
    if n <= 1:
        out = subprocess.run(["git", "ls-files"], cwd=root,
                             capture_output=True, text=True)
    else:
        out = subprocess.run(["git", "diff", "--name-only",
                              f"HEAD~{min(window, n - 1)}", "HEAD"],
                             cwd=root, capture_output=True, text=True)
    if out.returncode != 0:
        return set()
    return {ln.strip() for ln in out.stdout.splitlines() if ln.strip()}


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
                    f"(tools/mdllm.py) — tier routing drifted from the catalog"))

        # ...and the mirror (directional graph reads come in inbound/outbound
        # pairs): every TIERS entry must be in the catalog. A file routed by
        # tier but absent from .markdownllm is loadable-but-uncatalogued —
        # the reverse drift the one-directional check was blind to (review 6,
        # finding 6: thing-lifecycle.md sat exactly there).
        for name in sorted(tier_files):
            if name not in specs:
                findings.append(Finding(SEV_WARNING, "TIERS",
                    f"`{name}` is in the TIERS map (tools/mdllm.py) but not in "
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
