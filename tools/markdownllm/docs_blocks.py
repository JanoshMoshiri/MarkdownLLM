"""Derived blocks in the human-facing docs — `public-docs-face-build` Phase 1.

Two surfaces under `docs/` restated a mechanical source by hand and drifted
against it: the operator guide's toolbox table restated `mdllm --help`, and
the framework map restated spec frontmatter. Each restatement was a walk step
per CLI change (`a-generated-surface-collapses-its-walk`): one flag cost four
hand edits on 2026-08-13 and eight on 2026-09-15. This module makes the
mechanical half of those surfaces *generated*, drift-gated at the commit
boundary, and leaves the authored half authored — but *checked* for
completeness against the same mechanical source.

The split follows the precedent `coherence-mechanism-build` Phase 1 set for
the entry file: generate where a block can own the whole fact; check where
authored prose wraps a derivable one. A mermaid diagram cannot host a managed
block (HTML comments break the renderer), so both map views are checked, not
generated, and the map gains a generated *companion* — every declared edge,
as data — beside the curated drawing.

Layer: the generator/adapter edge. Reads spec frontmatter and the two docs;
writes the two docs. **The CLI's inventory is injected, never imported.**
`cli.py` is the composition root — it imports `coherence`, which imports this
module — so this module reaching back for `build_cli` would close a cycle,
and the architecture gate refuses cycles even through a function-local
import (initialization order becomes observable). Instead the root hands the
parser's rows down: `rows_from_parser` is a pure walk over an argparse
object, and every builder and check that needs the inventory takes `rows`.
A call without them says so as a Warning ("could not look"), never a pass.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .domain_kernel import apply_domain_kernel, domain_kernel_status
from .kernel_gen import normalize_newlines
from .model import Finding, SEV_ERROR, SEV_WARNING, parse_frontmatter
from .repository_view import RepositoryView

OPERATOR_GUIDE = "docs/operator-guide.md"
FRAMEWORK_MAP = "docs/framework-map.md"
README = "README.md"
SITE_CONFIG = "docs/_config.yml"

# Which managed blocks each doc carries. The registry is the one place the
# fact lives; `cmd_docs`, the drift check, and the tests all read it.
DOCS_BLOCKS: dict[str, tuple[str, ...]] = {
    OPERATOR_GUIDE: ("toolbox",),
    FRAMEWORK_MAP: ("spec-edges",),
}

# The README's verified-install block (documentation arc, package 2). It is
# built from the release record rather than from a file: the newest commit
# whose subject is `release: X.Y.Z`, and the sha256 of that commit's two
# installers. It is optional per root — a root without a README, or a README
# without the marker, carries no install block — so it lives beside the
# registry, not in it. Until 2026-10-20 this block was hand-kept and pinned
# v3.32.0 for seventeen releases: nothing tied it to a release.
INSTALL_BLOCK = "install"
_RELEASE_SUBJECT = re.compile(r"^release: (\d+\.\d+\.\d+)\b")
_SITE_REPOSITORY = re.compile(r"^repository:\s*([\w.-]+/[\w.-]+)", re.MULTILINE)
_INSTALL_MARKER = f"<!-- generated:{INSTALL_BLOCK} -->"

# Blocks that cannot be built without the CLI inventory.
_NEEDS_ROWS = {"toolbox"}

# The spec layer the map draws: root + docs/ files whose frontmatter type is
# one of these. Mirrors the map's own "Keeping This Map Honest" rule for
# View 1, so the two cannot disagree about what counts as a spec.
SPEC_TYPES = ("specification", "guide", "manifesto")

# The authored half of the toolbox: one bullet per subcommand, under this
# heading, in this shape. Parsed by the completeness check.
WHEN_HEADING = "### When you'd type each one yourself"
_WHEN_BULLET = re.compile(r"^- \*\*`([a-z0-9-]+)`\*\*\s+—", re.MULTILINE)

_STATUS_TAG = re.compile(r"\((draft|evolving|stable|deprecated)\)\s*$")
_MERMAID_NODE = re.compile(r'^\s*([A-Za-z][A-Za-z0-9_]*)\["([^"]*)"\]', re.MULTILINE)


# --------------------------------------------------------------- readers


def _read(root: Path, rel: str, view: RepositoryView | None) -> str | None:
    """One text under a view, newline-normalised. None when absent."""
    p = root / rel
    if view is None:
        if not p.is_file():
            return None
        return normalize_newlines(p.read_text(encoding="utf-8"))
    logical = p.resolve().relative_to(view.root).as_posix()
    if not view.exists(logical):
        return None
    return normalize_newlines(view.read_text(logical))


def _list_md(root: Path, sub: str, view: RepositoryView | None) -> list[str]:
    """Relative `.md` paths directly under `root/sub` (sub may be '')."""
    if view is None:
        base = root / sub if sub else root
        if not base.is_dir():
            return []
        return sorted((f"{sub}/{p.name}" if sub else p.name)
                      for p in base.iterdir() if p.suffix == ".md" and p.is_file())
    prefix = f"{sub}/" if sub else ""
    out = []
    for logical in view.list_paths(suffix=".md"):
        s = logical.as_posix()
        if not s.startswith(prefix):
            continue
        rest = s[len(prefix):]
        if "/" in rest:
            continue
        out.append(s)
    return sorted(out)


# --------------------------------------------------------------- the CLI's inventory


@dataclass(frozen=True)
class SubcommandRow:
    name: str
    usage: str      # `mdllm <name> ...` — exact, from argparse, `[-h]` dropped
    help: str       # the subparser's own one-line help


def _clean_usage(name: str, raw: str) -> str:
    text = " ".join(raw.split())
    marker = f" {name} "
    at = text.find(marker)
    tail = text[at + len(marker):] if at >= 0 else ""
    tail = tail.replace("[-h] ", "").replace(" [-h]", "").strip()
    return f"mdllm {name}" + (f" {tail}" if tail else "")


def rows_from_parser(parser) -> tuple[SubcommandRow, ...]:
    """Every registered subcommand of an argparse parser, alphabetically.

    A pure walk over the parser object: this module never imports the
    composition root that builds it. Alphabetical rather than registration
    order — inserting a parser mid-file is a code-layout choice, and a
    derived surface must not drift on it.
    """
    subs = next(a for a in parser._actions
                if a.__class__.__name__ == "_SubParsersAction")
    helps = {c.dest: (c.help or "") for c in subs._choices_actions}
    rows = []
    for name in sorted(subs.choices):
        sp = subs.choices[name]
        rows.append(SubcommandRow(
            name=name,
            usage=_clean_usage(name, sp.format_usage()),
            help=" ".join((helps.get(name) or "").split())))
    return tuple(rows)


def subcommand_names(rows: tuple[SubcommandRow, ...]) -> set[str]:
    return {r.name for r in rows}


# --------------------------------------------------------------- the spec layer


@dataclass(frozen=True)
class SpecRef:
    rel: str            # e.g. "docs/first-hour.md"
    basename: str       # "first-hour.md"
    stem: str           # "first-hour"
    id: str
    type: str
    status: str
    edges: tuple[tuple[str, str], ...]   # (relation, target id)

    @property
    def label_keys(self) -> set[str]:
        """Strings a map node label may use to name this spec."""
        keys = {self.basename, self.stem}
        if self.type == "manifesto":
            keys.add("the manifesto")
        return keys


def spec_set(root: Path, view: RepositoryView | None = None) -> tuple[SpecRef, ...]:
    """The spec layer: every root or docs/ `.md` typed specification, guide or
    manifesto — read from frontmatter, the same rule the map states for
    itself. Sorted by relative path."""
    out: list[SpecRef] = []
    for rel in _list_md(root, "", view) + _list_md(root, "docs", view):
        text = _read(root, rel, view)
        if text is None:
            continue
        meta, _, err = parse_frontmatter(text, source=root / rel)
        if err or not isinstance(meta, dict):
            continue
        typ = str(meta.get("type", ""))
        if typ not in SPEC_TYPES:
            continue
        edges = []
        for e in meta.get("linked_things") or []:
            if isinstance(e, dict) and isinstance(e.get("id"), str):
                edges.append((str(e.get("relation", "")), e["id"]))
        base = rel.rsplit("/", 1)[-1]
        out.append(SpecRef(rel=rel, basename=base, stem=base[:-3],
                           id=str(meta.get("id", "")), type=typ,
                           status=str(meta.get("status", "")),
                           edges=tuple(edges)))
    return tuple(sorted(out, key=lambda s: s.rel))


# --------------------------------------------------------------- builders


def _cell(text: str) -> str:
    return text.replace("|", "\\|")


def _db_toolbox(root: Path, view: RepositoryView | None,
                rows: tuple[SubcommandRow, ...]) -> str:
    """The toolbox table, wholly mechanical: name, exact usage, the tool's
    own help. The authored half — when you'd reach for it — lives in the
    bullets below the block and is checked for completeness, not generated."""
    lines = ["| Subcommand | Usage | The tool's own description |",
             "|---|---|---|"]
    for r in rows:
        lines.append(f"| `{r.name}` | `{_cell(r.usage)}` | {_cell(r.help)} |")
    return "\n".join(lines)


def _db_spec_edges(root: Path, view: RepositoryView | None,
                   rows: tuple[SubcommandRow, ...] | None) -> str:
    """Every declared edge between specs, from frontmatter — the companion
    to the curated View 2 drawing, which shows load-bearing edges only."""
    specs = spec_set(root, view)
    by_id = {s.id: s for s in specs if s.id}
    lines = []
    for s in specs:
        groups: dict[str, list[str]] = {}
        outside = 0
        for rel, target in s.edges:
            t = by_id.get(target)
            if t is None:
                outside += 1
                continue
            groups.setdefault(rel, []).append(f"`{t.basename}`")
        parts = [f"{rel} → {', '.join(targets)}"
                 for rel, targets in sorted(groups.items())]
        tail = f" · +{outside} edge(s) outside the spec layer" if outside else ""
        body = "; ".join(parts) if parts else "no edges to other specs"
        lines.append(f"- **`{s.rel}`** (`{s.type}`, `{s.status}`): {body}{tail}")
    return "\n".join(lines)


_DB_BUILDERS = {
    "toolbox": _db_toolbox,
    "spec-edges": _db_spec_edges,
}


def latest_release(root: Path, revision: str = "HEAD") -> tuple[str, str] | None:
    """(full commit id, version) of the newest `release: X.Y.Z` commit
    reachable from `revision`, or None when there is no such record (not a
    repository, no release yet). At a release commit's own pre-commit the
    newest release is the previous one, so the block it carries names the
    previous release; the first commit after the release regenerates it."""
    try:
        r = subprocess.run(
            ["git", "log", "--format=%H%x09%s", "--end-of-options", revision],
            cwd=root, capture_output=True, text=True, encoding="utf-8")
    except OSError:
        return None
    if r.returncode != 0:
        return None
    for line in r.stdout.splitlines():
        sha, _, subject = line.partition("\t")
        m = _RELEASE_SUBJECT.match(subject)
        if m:
            return sha.strip().lower(), m.group(1)
    return None


def _db_install(root: Path, view: RepositoryView | None) -> str | None:
    """The verified-install block for the newest release, or None when the
    release record, the public repository identity or an installer cannot
    be read — the caller reports that as could-not-look, never as clean."""
    revision = getattr(view, "commit_sha", None) or "HEAD"
    release = latest_release(root, revision)
    config = _read(root, SITE_CONFIG, view)
    repo = _SITE_REPOSITORY.search(config) if config else None
    if release is None or repo is None:
        return None
    sha, version = release
    try:
        at = RepositoryView.commit(root, sha)
        sh = hashlib.sha256(at.read_bytes("install.sh")).hexdigest()
        ps = hashlib.sha256(at.read_bytes("install.ps1")).hexdigest()
    except Exception:
        return None
    url = f"https://github.com/{repo.group(1)}.git"
    return "\n".join([
        f"The newest release is **{version}**, commit `{sha[:12]}`. Fetch exactly",
        "that commit, check the installer's bytes, then run it:",
        "",
        "```bash",
        "# macOS / Linux",
        f"RELEASE_COMMIT={sha}",
        f"INSTALLER_SHA256={sh}",
        "git init MarkdownLLM",
        "git -C MarkdownLLM config core.autocrlf false",
        f"git -C MarkdownLLM remote add origin {url}",
        'git -C MarkdownLLM fetch --depth 1 origin "$RELEASE_COMMIT:refs/remotes/origin/verified-release"',
        'git -C MarkdownLLM checkout --detach "$RELEASE_COMMIT"',
        'test "$(git -C MarkdownLLM rev-parse HEAD)" = "$RELEASE_COMMIT"',
        "cd MarkdownLLM",
        "printf '%s  install.sh\\n' \"$INSTALLER_SHA256\" | sha256sum -c -",
        "./install.sh",
        "```",
        "",
        "```powershell",
        "# Windows (PowerShell 7+)",
        f"$ReleaseCommit = '{sha}'",
        f"$InstallerSha256 = '{ps}'",
        "git init MarkdownLLM",
        "git -C MarkdownLLM config core.autocrlf false",
        f"git -C MarkdownLLM remote add origin {url}",
        'git -C MarkdownLLM fetch --depth 1 origin "${ReleaseCommit}:refs/remotes/origin/verified-release"',
        "git -C MarkdownLLM checkout --detach $ReleaseCommit",
        "if ((git -C MarkdownLLM rev-parse HEAD) -ne $ReleaseCommit) { throw 'release commit mismatch' }",
        "Set-Location MarkdownLLM",
        "if ((Get-FileHash ./install.ps1 -Algorithm SHA256).Hash.ToLowerInvariant() -ne $InstallerSha256) { throw 'installer hash mismatch' }",
        "./install.ps1",
        "```",
    ])


def build_docs_blocks(root: Path, view: RepositoryView | None = None,
                      rows: tuple[SubcommandRow, ...] | None = None,
                      ) -> dict[str, dict[str, str]]:
    """Canonical body for every managed block that can be built with what
    was supplied, keyed by doc then block name. Shared by `mdllm docs` and
    the coherence drift check — one source. Blocks that need the CLI
    inventory are omitted when `rows` is None; the check reports that. The
    README's install block joins only where the README carries its marker
    and the release record can be read."""
    out: dict[str, dict[str, str]] = {}
    for rel, names in DOCS_BLOCKS.items():
        out[rel] = {name: _pad(_DB_BUILDERS[name](root, view, rows)) for name in names
                    if rows is not None or name not in _NEEDS_ROWS}
    readme = _read(root, README, view)
    if readme is not None and _INSTALL_MARKER in readme:
        body = _db_install(root, view)
        if body is not None:
            out[README] = {INSTALL_BLOCK: _pad(body)}
    return out


def _pad(body: str) -> str:
    """A blank line inside each marker. GitHub's renderer ends an HTML
    comment block at its own line; kramdown (the Pages build) does not, and
    swallows a table or list that follows the marker directly into one raw
    paragraph — the first live build of the operator guide showed the whole
    toolbox as unbroken text. Padding is part of the canonical body, so the
    same-builder drift check keeps it there."""
    return f"\n{body}\n"


# --------------------------------------------------------------- checks


def _mermaid_section(text: str, heading: str) -> str | None:
    """The first ```mermaid``` fence under a `## heading` line."""
    at = text.find(f"\n## {heading}")
    if at < 0:
        return None
    start = text.find("```mermaid", at)
    if start < 0:
        return None
    end = text.find("\n```", start + 10)
    return text[start:end] if end > 0 else text[start:]


def _when_bullets(text: str) -> set[str] | None:
    at = text.find(WHEN_HEADING)
    if at < 0:
        return None
    section = text[at + len(WHEN_HEADING):]
    nxt = re.search(r"\n#{1,3} ", section)
    if nxt:
        section = section[:nxt.start()]
    return set(_WHEN_BULLET.findall(section))


def _toolbox_findings(text: str, names: set[str]) -> list[Finding]:
    bullets = _when_bullets(text)
    if bullets is None:
        return [Finding(SEV_WARNING, OPERATOR_GUIDE,
                        f"`{WHEN_HEADING}` not found — the toolbox annotation "
                        "completeness check could not run")]
    out = []
    for n in sorted(names - bullets):
        out.append(Finding(SEV_ERROR, OPERATOR_GUIDE,
            f"subcommand `{n}` has no authored line under "
            f"`{WHEN_HEADING}` — say when a human would type it, or "
            f"the guide is silently incomplete"))
    for n in sorted(bullets - names):
        out.append(Finding(SEV_ERROR, OPERATOR_GUIDE,
            f"`{WHEN_HEADING}` annotates `{n}`, which is not an mdllm "
            f"subcommand — remove the line or the guide documents a ghost"))
    return out


def _view3_findings(text: str, names: set[str]) -> list[Finding]:
    """Every subcommand has a node in View 3's `cli` subgraph, and every node
    there is a subcommand. The spec each one serves stays judgement."""
    section = _mermaid_section(text, "View 3")
    if section is None:
        return [Finding(SEV_WARNING, FRAMEWORK_MAP,
                        "View 3's mermaid block not found — the subcommand "
                        "node check could not run")]
    cli_at = section.find("subgraph cli")
    cli_end = section.find("\n    end", cli_at) if cli_at >= 0 else -1
    if cli_at < 0 or cli_end < 0:
        return [Finding(SEV_WARNING, FRAMEWORK_MAP,
                        "View 3 has no `subgraph cli` — the subcommand node "
                        "check could not run")]
    nodes = set()
    for _, label in _MERMAID_NODE.findall(section[cli_at:cli_end]):
        nodes.add(label.split("<br")[0].strip())
    out = []
    for n in sorted(names - nodes):
        out.append(Finding(SEV_ERROR, FRAMEWORK_MAP,
            f"View 3 has no node for subcommand `{n}` — add it to `subgraph "
            f"cli` and draw the one edge to what it serves"))
    for n in sorted(nodes - names):
        out.append(Finding(SEV_ERROR, FRAMEWORK_MAP,
            f"View 3 draws `{n}`, which is not an mdllm subcommand"))
    return out


def _view2_findings(text: str, specs: tuple[SpecRef, ...]) -> list[Finding]:
    """Every spec on disk has a node in View 2, and any status tag a node
    carries matches the spec's frontmatter. Absence of a tag is not a claim;
    unknown nodes are not checked (the manifesto's label is prose)."""
    section = _mermaid_section(text, "View 2")
    if section is None:
        return [Finding(SEV_WARNING, FRAMEWORK_MAP,
                        "View 2's mermaid block not found — the spec node "
                        "check could not run")]
    labels = []
    for _, label in _MERMAID_NODE.findall(section):
        first = label.split("<br")[0].strip()
        m = _STATUS_TAG.search(first)
        tag = m.group(1) if m else None
        name = _STATUS_TAG.sub("", first).strip() if m else first
        labels.append((name, tag))
    out = []
    for s in specs:
        hits = [(name, tag) for name, tag in labels if name in s.label_keys]
        if not hits:
            out.append(Finding(SEV_ERROR, FRAMEWORK_MAP,
                f"View 2 has no node for `{s.rel}` — every spec on disk "
                f"belongs on the map (add it to its band)"))
            continue
        for name, tag in hits:
            if tag and tag != s.status:
                out.append(Finding(SEV_ERROR, FRAMEWORK_MAP,
                    f"View 2 tags `{name}` as `({tag})` but `{s.rel}` is "
                    f"`{s.status}` — fix the label in the commit that "
                    f"changed the spec"))
    return out


def docs_block_findings(root: Path, view: RepositoryView | None = None,
                        rows: tuple[SubcommandRow, ...] | None = None,
                        ) -> list[Finding]:
    """The coherence leg: block drift (Error) plus the three completeness
    checks over the authored halves. Framework root only — the caller gates.
    Without the CLI inventory the inventory-dependent checks say they could
    not look; they never pass by omission."""
    findings: list[Finding] = []
    blocks = build_docs_blocks(root, view, rows)
    texts = {rel: _read(root, rel, view) for rel in (*DOCS_BLOCKS, *blocks)}
    readme = _read(root, README, view)
    if readme is not None and _INSTALL_MARKER in readme and README not in blocks:
        findings.append(Finding(SEV_WARNING, README,
            "the install block could not be built — no `release: X.Y.Z` commit, "
            f"no `repository:` in {SITE_CONFIG}, or an installer missing at the "
            "release — so the pin was not checked"))
    for rel, bodies in blocks.items():
        text = texts[rel]
        if text is None:
            findings.append(Finding(SEV_WARNING, rel,
                "not readable from the selected view — its derived blocks "
                "could not be checked"))
            continue
        present, drifted = domain_kernel_status(text, bodies)
        for name in sorted(set(bodies) - set(present)):
            findings.append(Finding(SEV_ERROR, rel,
                f"managed block `{name}` is missing — add "
                f"`<!-- generated:{name} -->…<!-- /generated:{name} -->` and "
                f"run `mdllm docs .`"))
        for name in drifted:
            findings.append(Finding(SEV_ERROR, rel,
                f"managed block `{name}` drifted from a fresh build — run "
                f"`mdllm docs .` and commit the result"))
    if rows is None:
        findings.append(Finding(SEV_WARNING, OPERATOR_GUIDE,
            "the CLI's subcommand inventory was not supplied to this call — "
            "the toolbox drift and annotation checks, and View 3's node "
            "check, could not run (`mdllm coherence` and `mdllm docs --check` "
            "supply it)"))
    else:
        names = subcommand_names(rows)
        if texts[OPERATOR_GUIDE] is not None:
            findings.extend(_toolbox_findings(texts[OPERATOR_GUIDE], names))
        if texts[FRAMEWORK_MAP] is not None:
            findings.extend(_view3_findings(texts[FRAMEWORK_MAP], names))
    if texts[FRAMEWORK_MAP] is not None:
        findings.extend(_view2_findings(texts[FRAMEWORK_MAP], spec_set(root, view)))
    return findings


# --------------------------------------------------------------- the command


def cmd_docs(args, rows: tuple[SubcommandRow, ...] | None = None) -> int:
    """Regenerate the derived blocks in docs/, or `--check` them for drift.
    `rows` is injected by the CLI (the composition root) — see the module
    docstring for why this module never fetches it."""
    root = Path(args.path).resolve()
    if not (root / ".markdownllm").is_file():
        sys.exit("mdllm: docs requires a framework root (.markdownllm not found)")
    if rows is None:
        sys.exit("mdllm: docs needs the CLI's subcommand inventory — run it as "
                 "`mdllm docs`, which supplies it")
    blocks = build_docs_blocks(root, None, rows)

    if args.check:
        findings = docs_block_findings(root, None, rows)
        errors = [f for f in findings if f.severity == SEV_ERROR]
        for f in findings:
            print(f"  {f.severity:<8} {f.thing}: {f.message}")
        if errors:
            print(f"docs: {len(errors)} Error(s) — run `mdllm docs {args.path}` "
                  "for block drift; the completeness findings are authored fixes")
            return 1
        print(f"docs: in sync ({sum(len(b) for b in blocks.values())} block(s), "
              f"{len(rows)} subcommands)")
        return 0

    total = 0
    for rel, bodies in blocks.items():
        p = root / rel
        if not p.is_file():
            print(f"docs: {rel} not found — skipped")
            continue
        text = p.read_text(encoding="utf-8")
        new_text, written, missing = apply_domain_kernel(text, bodies)
        if new_text != text:
            p.write_text(new_text, encoding="utf-8", newline="\n")
        total += len(written)
        print(f"docs: {rel} — wrote {len(written)} block(s)"
              + (f"; not present: {', '.join(missing)}" if missing else ""))
    if not total:
        print("docs: no managed blocks found — add the markers, then re-run")
        return 1
    return 0
