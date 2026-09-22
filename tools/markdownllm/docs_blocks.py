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

Layer: the generator/adapter edge. Reads argparse (the CLI's own inventory),
spec frontmatter, and the two docs; writes the two docs. Imports nothing from
a vendor. The CLI is imported *lazily* in `subcommand_rows`, because `cli.py`
is the composition root that imports `coherence`, which imports this module —
an import-time cycle otherwise. A generator asking the composition root for
its inventory at call time is the accepted shape for that.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from .domain_kernel import apply_domain_kernel, domain_kernel_status
from .kernel_gen import normalize_newlines
from .model import Finding, SEV_ERROR, SEV_WARNING, parse_frontmatter
from .repository_view import RepositoryView

OPERATOR_GUIDE = "docs/operator-guide.md"
FRAMEWORK_MAP = "docs/framework-map.md"

# Which managed blocks each doc carries. The registry is the one place the
# fact lives; `cmd_docs`, the drift check, and the tests all read it.
DOCS_BLOCKS: dict[str, tuple[str, ...]] = {
    OPERATOR_GUIDE: ("toolbox",),
    FRAMEWORK_MAP: ("spec-edges",),
}

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


def subcommand_rows() -> tuple[SubcommandRow, ...]:
    """Every registered subcommand, alphabetically — argparse is the source.

    Alphabetical rather than registration order: inserting a parser mid-file
    is a code-layout choice, and a derived surface must not drift on it.
    """
    from .cli import build_cli  # composition root; lazy to avoid the cycle
    parser = build_cli()
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


def subcommand_names() -> set[str]:
    return {r.name for r in subcommand_rows()}


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


def _db_toolbox(root: Path, view: RepositoryView | None) -> str:
    """The toolbox table, wholly mechanical: name, exact usage, the tool's
    own help. The authored half — when you'd reach for it — lives in the
    bullets below the block and is checked for completeness, not generated."""
    lines = ["| Subcommand | Usage | The tool's own description |",
             "|---|---|---|"]
    for r in subcommand_rows():
        lines.append(f"| `{r.name}` | `{_cell(r.usage)}` | {_cell(r.help)} |")
    return "\n".join(lines)


def _db_spec_edges(root: Path, view: RepositoryView | None) -> str:
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


def build_docs_blocks(root: Path,
                      view: RepositoryView | None = None) -> dict[str, dict[str, str]]:
    """Canonical body for every managed block, keyed by doc then block name.
    Shared by `mdllm docs` and the coherence drift check — one source."""
    return {rel: {name: _DB_BUILDERS[name](root, view) for name in names}
            for rel, names in DOCS_BLOCKS.items()}


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


def docs_block_findings(root: Path,
                        view: RepositoryView | None = None) -> list[Finding]:
    """The coherence leg: block drift (Error) plus the three completeness
    checks over the authored halves. Framework root only — the caller gates."""
    findings: list[Finding] = []
    blocks = build_docs_blocks(root, view)
    texts = {rel: _read(root, rel, view) for rel in DOCS_BLOCKS}
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
    names = subcommand_names()
    if texts[OPERATOR_GUIDE] is not None:
        findings.extend(_toolbox_findings(texts[OPERATOR_GUIDE], names))
    if texts[FRAMEWORK_MAP] is not None:
        findings.extend(_view3_findings(texts[FRAMEWORK_MAP], names))
        findings.extend(_view2_findings(texts[FRAMEWORK_MAP], spec_set(root, view)))
    return findings


# --------------------------------------------------------------- the command


def cmd_docs(args) -> int:
    """Regenerate the derived blocks in docs/, or `--check` them for drift."""
    root = Path(args.path).resolve()
    if not (root / ".markdownllm").is_file():
        sys.exit("mdllm: docs requires a framework root (.markdownllm not found)")
    blocks = build_docs_blocks(root)

    if args.check:
        findings = docs_block_findings(root)
        errors = [f for f in findings if f.severity == SEV_ERROR]
        for f in findings:
            print(f"  {f.severity:<8} {f.thing}: {f.message}")
        if errors:
            print(f"docs: {len(errors)} Error(s) — run `mdllm docs {args.path}` "
                  "for block drift; the completeness findings are authored fixes")
            return 1
        print(f"docs: in sync ({sum(len(b) for b in blocks.values())} block(s), "
              f"{len(subcommand_names())} subcommands)")
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
