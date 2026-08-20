"""Derived indexes — build, check, rebuild, and drift-detect.

The four opt-in derived views (triggers, schema, relationships, provenance)
under `things/_index/`. `index_drift_findings` is shared with coherence so
the two surfaces agree on what "in sync" means.
"""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path

from .model import Corpus, Finding, SEV_ERROR, SEV_WARNING, parse_frontmatter, scan
from .repo import framework_version, git_short_sha
from .repository_view import RepositoryView
from .structural_refs import REFERENCE_BY_FIELD, iter_structural_references
from .yaml_loader import load_version_sentinel

def build_index_body(corpus: Corpus, signal: str) -> tuple[str, int]:
    """Returns (body, coverage)."""
    lines: list[str] = []
    if signal == "triggers":
        covered = 0
        for t in sorted(corpus.things, key=lambda x: x.id or ""):
            trigs = t.meta.get("triggers") or []
            due = t.meta.get("due_date")
            if not trigs and not due:
                continue
            covered += 1
            lines.append(f"## {t.id}")
            lines.append(f"- status: {t.meta.get('status')}  due_date: {due or '—'}")
            for tr in trigs:
                if isinstance(tr, dict):
                    lines.append("- trigger: " + ", ".join(f"{k}={v}" for k, v in tr.items()))
            lines.append("")
        return "\n".join(lines), covered
    if signal == "schema":
        fields: dict[str, int] = {}
        for t in corpus.things:
            for k in t.meta:
                fields[k] = fields.get(k, 0) + 1
        lines.append("| field | things using it |")
        lines.append("|---|---|")
        for k in sorted(fields, key=lambda x: -fields[x]):
            lines.append(f"| {k} | {fields[k]} |")
        return "\n".join(lines), len(corpus.things)
    if signal == "relationships":
        for t in sorted(corpus.things, key=lambda x: x.id or ""):
            for ref in iter_structural_references(t.meta, reverse_only=True):
                owner = ref.field.split(".", 1)[0]
                if REFERENCE_BY_FIELD[owner].index_signal != "relationships":
                    continue
                lines.append(f"- {t.id} --{ref.relation}--> {ref.target}")
        return "\n".join(lines), len(corpus.things)
    if signal == "provenance":
        # Reverse map: for each knowledge thing, which decisions pin it and
        # which outputs derive from those decisions. See provenance.md.
        dependents: dict[str, list[str]] = {}
        for t in sorted(corpus.things, key=lambda x: x.id or ""):
            for ref in iter_structural_references(t.meta, reverse_only=True):
                owner = ref.field.split(".", 1)[0]
                if REFERENCE_BY_FIELD[owner].index_signal == "provenance":
                    dependents.setdefault(ref.target, []).append(
                        f"{t.id} (pinned @{ref.commit or '?'})")
            for e in t.meta.get("linked_things") or []:
                if isinstance(e, dict) and e.get("relation") == "derived-from":
                    dependents.setdefault(str(e.get("id")), []).append(
                        f"{t.id} (derived-from)")
        for src in sorted(dependents):
            lines.append(f"## {src}")
            for d in dependents[src]:
                lines.append(f"- {d}")
            lines.append("")
        return "\n".join(lines), len(dependents)
    raise SystemExit(f"unknown signal: {signal}")


INDEX_FILES = {"triggers": "triggers.md", "schema": "schema.md",
               "relationships": "relationships.md", "provenance": "provenance.md"}


def _stored_index_payload(body: str) -> str:
    """Remove the generated title without inventing content for an empty index.

    The old ``strip().split("\\n", 1)[-1]`` spelling returned the title itself
    when a legitimately empty index had no second line.  That made an empty
    triggers index report drift immediately after its own rebuild.
    """
    lines = body.strip().splitlines()
    if not lines:
        return ""
    if lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return "\n".join(lines).strip()


def _view_framework_version(root: Path, view: RepositoryView | None) -> str:
    """Read the sentinel from the same repository view when it owns one."""
    if view is not None:
        sentinel = Path(root).resolve() / ".markdownllm"
        try:
            logical = sentinel.relative_to(view.root).as_posix()
        except ValueError:
            logical = ""
        if logical and view.exists(logical):
            data = load_version_sentinel(
                view.read_text(logical), source=logical)
            return str(data.get("version", "unknown"))
    # A downstream domain's framework sentinel lives outside its repository
    # view; that external version dependency remains an explicitly ambient
    # input, while a framework-root candidate never leaks to the worktree.
    return framework_version(root)


def _anchor_notes(
    root: Path, meta: dict, signal: str, view: RepositoryView | None = None,
) -> list[str]:
    """Integrity of a stored index's own generation stamp — content parity is
    not the whole story. `generated_from` must still resolve (a history rewrite
    kills the anchor while the body stays "in sync" — found live on the
    framework's own provenance index, 2026-08-01), and `framework_version`
    staleness means the index predates shapes the current floor writes.
    Advisory: a rebuild re-pins both."""
    notes: list[str] = []
    gf = str(meta.get("generated_from", ""))
    sha = gf.split("@", 1)[1].strip() if "@" in gf else ""
    if sha:
        ok = subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                            cwd=root, capture_output=True).returncode == 0
        if not ok:
            notes.append(f"`generated_from` anchor `{gf}` no longer resolves "
                         f"(history rewritten?) — rebuild to re-pin")
    stamped = str(meta.get("framework_version", ""))
    current = _view_framework_version(root, view)
    if stamped and current and stamped != str(current):
        notes.append(f"stamped at framework {stamped}, current is {current} — "
                     f"rebuild to re-pin")
    return notes


def index_drift_findings(root: Path, corpus: Corpus) -> list[Finding]:
    """Drift Errors for every *deployed* derived index (one missing is not
    drift — indexes are opt-in), plus advisory anchor-integrity Warnings.
    Shares `build_index_body` and the body-vs-stored comparison with
    `index check`, so coherence and the index command agree."""
    out: list[Finding] = []
    idx_dir = root / "things" / "_index"
    for signal, fname in INDEX_FILES.items():
        path = idx_dir / fname
        view = corpus.view
        if view is not None:
            logical = path.resolve().relative_to(view.root).as_posix()
            exists = view.exists(logical)
            existing = view.read_text(logical) if exists else None
        else:
            exists = path.exists()
            existing = path.read_text(encoding="utf-8") if exists else None
        if not exists:
            continue  # not deployed — opt-in, not a defect
        body, _ = build_index_body(corpus, signal)
        meta, ex_body, _ = parse_frontmatter(existing or "", source=path)
        if _stored_index_payload(ex_body) != f"{body}".strip():
            out.append(Finding(SEV_ERROR, f"{signal}-index",
                       f"DRIFT — stored body differs from rebuild; run "
                       f"`mdllm index {root} rebuild --signal {signal}`"))
        for note in _anchor_notes(root, meta or {}, signal, corpus.view):
            out.append(Finding(SEV_WARNING, f"{signal}-index", note))
    return out


def cmd_index(args) -> int:
    root = Path(args.path).resolve()
    corpus, _ = scan(root)
    signals = [args.signal] if args.signal else ["triggers", "schema",
                                                 "relationships", "provenance"]
    idx_dir = root / "things" / "_index"
    rc = 0
    for signal in signals:
        body, coverage = build_index_body(corpus, signal)
        fname = INDEX_FILES[signal]
        path = idx_dir / fname
        domain = (corpus.schema or {}).get("domain", root.name)
        title = {"triggers": "Triggers Index", "schema": "Schema Registry",
                 "relationships": "Relationships Index",
                 "provenance": "Provenance Index (reverse)"}[signal]
        content = (
            "---\n"
            f"id: {domain}-{signal}-index\n"
            "type: index\n"
            "status: live\n"
            f"index_of: {signal}\n"
            f"created: {dt.date.today().isoformat()}\n"
            f"generated: {dt.datetime.now().isoformat(timespec='seconds')}\n"
            f"generated_from: HEAD@{git_short_sha(root)}\n"
            f"coverage: {coverage}\n"
            f"framework_version: {framework_version(root)}\n"
            "---\n\n"
            f"# {title} — {domain}\n\n"
            f"{body}\n"
        )
        if args.action == "rebuild":
            idx_dir.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"rebuilt {path.relative_to(root)} (coverage {coverage})")
        else:  # check
            if not path.exists():
                print(f"{signal}: no index at {path.relative_to(root)} — not deployed")
                continue
            existing = path.read_text(encoding="utf-8")
            ex_meta, ex_body, _ = parse_frontmatter(existing)
            if _stored_index_payload(ex_body) != (f"{body}").strip():
                print(f"{signal}: DRIFT — stored body differs from rebuild; "
                      f"run `mdllm index {root} rebuild --signal {signal}`")
                rc = 1
            else:
                print(f"{signal}: in sync (coverage {coverage})")
            for note in _anchor_notes(root, ex_meta or {}, signal):
                print(f"{signal}: ANCHOR — {note}")
    return rc
