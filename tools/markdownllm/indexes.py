"""Derived indexes — build, check, rebuild, and drift-detect.

The four opt-in derived views (triggers, schema, relationships, provenance)
under `things/_index/`. `index_drift_findings` is shared with coherence so
the two surfaces agree on what "in sync" means.
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from .model import Corpus, Finding, SEV_ERROR, parse_frontmatter, scan
from .repo import framework_version, git_short_sha

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
            for e in t.meta.get("linked_things") or []:
                if isinstance(e, dict):
                    lines.append(f"- {t.id} --{e.get('relation')}--> {e.get('id')}")
            # Singular structural pointers are declared edges too. They live in
            # their own load-bearing fields (modelled on `parent`), not in
            # `linked_things`, so the loop above is blind to them — which left the
            # change-reconciliation Assimilate beat unable to recall a definition's
            # runs or a parent's children in reverse. Emit them as edges so a
            # reverse read over this index has total recall over what is declared,
            # not just over `linked_things`. (structural-pointers-need-reverse-edge-indexing)
            for field in ("parent", "definition"):
                tgt = t.meta.get(field)
                if isinstance(tgt, str) and tgt:
                    lines.append(f"- {t.id} --{field}--> {tgt}")
        return "\n".join(lines), len(corpus.things)
    if signal == "provenance":
        # Reverse map: for each knowledge thing, which decisions pin it and
        # which outputs derive from those decisions. See provenance.md.
        dependents: dict[str, list[str]] = {}
        for t in sorted(corpus.things, key=lambda x: x.id or ""):
            for pin in t.meta.get("informed_by") or []:
                if isinstance(pin, dict) and pin.get("id"):
                    dependents.setdefault(pin["id"], []).append(
                        f"{t.id} (pinned @{pin.get('commit', '?')})")
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


def index_drift_findings(root: Path, corpus: Corpus) -> list[Finding]:
    """Drift Errors for every *deployed* derived index (one missing is not
    drift — indexes are opt-in). Shares `build_index_body` and the body-vs-stored
    comparison with `index check`, so coherence and the index command agree."""
    out: list[Finding] = []
    idx_dir = root / "things" / "_index"
    for signal, fname in INDEX_FILES.items():
        path = idx_dir / fname
        if not path.exists():
            continue  # not deployed — opt-in, not a defect
        body, _ = build_index_body(corpus, signal)
        _, ex_body, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        if ex_body.strip().split("\n", 1)[-1].strip() != f"{body}".strip():
            out.append(Finding(SEV_ERROR, f"{signal}-index",
                       f"DRIFT — stored body differs from rebuild; run "
                       f"`mdllm index {root} rebuild --signal {signal}`"))
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
            _, ex_body, _ = parse_frontmatter(existing)
            if ex_body.strip().split("\n", 1)[-1].strip() != (f"{body}").strip():
                print(f"{signal}: DRIFT — stored body differs from rebuild; "
                      f"run `mdllm index {root} rebuild --signal {signal}`")
                rc = 1
            else:
                print(f"{signal}: in sync (coverage {coverage})")
    return rc
