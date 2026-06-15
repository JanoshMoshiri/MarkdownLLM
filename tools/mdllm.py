#!/usr/bin/env python3
"""mdllm — the MarkdownLLM deterministic floor.

Mechanical validation and maintenance for MarkdownLLM domains. The division of
labour (validate.thing.md v2.0): this tool guarantees the mechanical checks
(structural, referential, schema); the LLM keeps the semantic ones (Level 4).

Subcommands:
  validate [path]      Levels 1-3 mechanical validation. Exit 1 on Errors.
                       Example domains under <path>/examples/ are validated
                       as their own corpora in the same run.
  triggers [path]      Evaluate time/dependency/threshold trigger conditions.
  index    [path] check|rebuild [--signal triggers|schema|relationships]
  tokens   [path]      Measure spec token costs by loading tier.
  doctor   [path]      Probe the environment: floor prerequisites, hook
                       execution (not just presence), framework version drift.
  scaffold <path>      Deterministic domain birth: instantiated templates,
                       nested git repo, outer .gitignore isolation, hook,
                       first commit. The semantic half stays with the agent.
  install-hook [path]  Install a git pre-commit hook running `validate`.

Requires: Python 3.10+, PyYAML. tiktoken optional (tokens falls back to heuristic).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("mdllm: PyYAML is required (pip install pyyaml)")

# ---------------------------------------------------------------- constants

# Statuses for framework-reserved/internal types. Domains cannot redefine these.
RESERVED_STATUSES = {
    "specification": ["draft", "evolving", "stable", "deprecated"],
    "guide": ["draft", "evolving", "stable", "deprecated"],
    "manifesto": ["draft", "evolving", "stable", "deprecated"],
    "skill": ["draft", "evolving", "stable", "deprecated"],
    "prompt": ["draft", "evolving", "stable", "deprecated"],
    "insight": ["active", "promoted", "dismissed"],
    "continuity-brief": ["live"],
    "conflict": ["open", "resolved"],
    "retrospective": ["draft", "complete"],
    "index": ["live", "stale"],
    "decision": ["made", "superseded"],
    "workflow-definition": ["draft", "evolving", "stable", "deprecated"],
    "workflow-run": ["active", "paused", "completed", "abandoned"],
}

# The universal default workflow vocabulary — applies when no domain schema
# declares a vocabulary for the thing's type.
DEFAULT_STATUSES = ["not-started", "in-progress", "blocked", "paused", "completed", "cancelled"]
TERMINAL_STATUSES = {"completed", "cancelled", "met", "reconciled", "closed", "filed",
                     "resolved", "dismissed", "deprecated", "abandoned"}

DEFAULT_EXCLUDES = {".git", ".claude", "node_modules", "templates", "examples",
                    "domain", "domains", "tools", "adapters", "evals", "outputs",
                    "deliverables"}
NON_THING_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "CONTRIBUTING.md",
                   "CHANGELOG.md", "LICENSE"}

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(Z|[+-]\d{2}:?\d{2})?)?$")

SEV_ERROR, SEV_WARNING, SEV_INFO = "Error", "Warning", "Info"

# ---------------------------------------------------------------- core model


@dataclass
class Thing:
    path: Path
    meta: dict
    body: str

    @property
    def id(self) -> str | None:
        v = self.meta.get("id")
        return str(v) if v is not None else None


@dataclass
class Finding:
    severity: str
    thing: str  # id or relative path
    message: str


@dataclass
class Corpus:
    root: Path
    things: list[Thing] = field(default_factory=list)
    schema: dict | None = None
    skipped: list[Path] = field(default_factory=list)

    def by_id(self) -> dict[str, Thing]:
        out: dict[str, Thing] = {}
        for t in self.things:
            if t.id and t.id not in out:
                out[t.id] = t
        return out


def parse_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """Returns (meta, body, parse_error)."""
    if not text.startswith("---"):
        return None, text, None
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not m:
        return None, text, "unterminated frontmatter block"
    try:
        meta = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        return None, m.group(2), f"YAML parse error: {e}"
    if not isinstance(meta, dict):
        return None, m.group(2), "frontmatter is not a YAML mapping"
    return meta, m.group(2), None


def load_schema(root: Path) -> dict | None:
    for candidate in (root / "_schema.yaml", root / "things" / "_schema.yaml"):
        if candidate.exists():
            with open(candidate, encoding="utf-8") as f:
                return yaml.safe_load(f)
    return None


def scan(root: Path) -> tuple[Corpus, list[Finding]]:
    corpus = Corpus(root=root)
    findings: list[Finding] = []
    try:
        corpus.schema = load_schema(root)
    except yaml.YAMLError as e:
        # An unparseable schema must be a finding, not a crash — otherwise
        # one bad edit to _schema.yaml takes the whole floor down with it.
        corpus.schema = None
        findings.append(Finding(SEV_ERROR, "_schema.yaml",
                                f"schema unparseable — validating without it: {e}"))
    excludes = set(DEFAULT_EXCLUDES)
    if corpus.schema and isinstance(corpus.schema.get("exclude"), list):
        excludes |= set(corpus.schema["exclude"])

    for path in sorted(root.rglob("*.md")):
        rel = path.relative_to(root)
        if any(part in excludes for part in rel.parts):
            continue
        if path.name in NON_THING_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        meta, body, err = parse_frontmatter(text)
        if err:
            findings.append(Finding(SEV_ERROR, str(rel), err))
            continue
        if meta is None:
            corpus.skipped.append(rel)  # not a thing — no frontmatter
            continue
        if not any(k in meta for k in ("id", "type", "status")):
            corpus.skipped.append(rel)  # frontmatter, but not thing-shaped
            continue
        corpus.things.append(Thing(path=path, meta=meta, body=body))
    return corpus, findings


# ---------------------------------------------------------------- validation


def valid_statuses_for(typ: str, schema: dict | None) -> tuple[list[str] | None, bool]:
    """Returns (allowed_statuses, declared). declared=False means default vocabulary."""
    if typ in RESERVED_STATUSES:
        return RESERVED_STATUSES[typ], True
    if schema:
        tdef = (schema.get("types") or {}).get(typ)
        if isinstance(tdef, dict) and isinstance(tdef.get("statuses"), list):
            return [str(s) for s in tdef["statuses"]], True
    return DEFAULT_STATUSES, False


def validate_level1(t: Thing, schema: dict | None) -> list[Finding]:
    f: list[Finding] = []
    name = t.id or str(t.path.name)
    meta = t.meta

    for fld in ("id", "type", "status", "created"):
        if not meta.get(fld):
            f.append(Finding(SEV_ERROR, name, f"missing required field `{fld}`"))

    if t.id:
        if not ID_RE.match(t.id):
            f.append(Finding(SEV_WARNING, name, f"`id` not lowercase-hyphenated: {t.id!r}"))
        check_filename = ((schema or {}).get("options") or {}).get("id_filename_match", True)
        if check_filename and t.path.stem != t.id and t.path.name not in ("continuity.md",):
            f.append(Finding(SEV_WARNING, name, f"`id` does not match filename `{t.path.name}`"))

    typ, status = str(meta.get("type", "")), meta.get("status")
    if typ and status is not None:
        allowed, declared = valid_statuses_for(typ, schema)
        if str(status) not in allowed:
            sev = SEV_ERROR if declared else SEV_WARNING
            f.append(Finding(sev, name,
                     f"status `{status}` not in {'declared' if declared else 'default'} "
                     f"vocabulary for type `{typ}`: {allowed}"))

    for fld in ("created", "due_date", "review_date"):
        v = meta.get(fld)
        if v is not None and not (isinstance(v, (dt.date, dt.datetime)) or
                                  (isinstance(v, str) and ISO_RE.match(v))):
            sev = SEV_ERROR if fld == "created" else SEV_WARNING
            f.append(Finding(sev, name, f"`{fld}` is not ISO 8601: {v!r}"))

    lt = meta.get("linked_things")
    if lt is not None:
        if not isinstance(lt, list):
            f.append(Finding(SEV_ERROR, name, "`linked_things` is not a list"))
        else:
            for i, entry in enumerate(lt):
                if not isinstance(entry, dict) or "id" not in entry or "relation" not in entry:
                    f.append(Finding(SEV_ERROR, name,
                             f"`linked_things[{i}]` must be an object with `id` and `relation`"))

    for fld in ("dependencies", "blocks"):
        v = meta.get(fld)
        if v is not None and (not isinstance(v, list) or not all(isinstance(x, str) for x in v)):
            f.append(Finding(SEV_ERROR, name, f"`{fld}` must be an array of id strings"))

    trig = meta.get("triggers")
    if trig is not None:
        if not isinstance(trig, list):
            f.append(Finding(SEV_ERROR, name, "`triggers` is not a list"))
        else:
            for i, tr in enumerate(trig):
                if not isinstance(tr, dict) or "type" not in tr or "action" not in tr:
                    f.append(Finding(SEV_ERROR, name,
                             f"`triggers[{i}]` must have `type` and `action`"))

    if not t.body.strip():
        f.append(Finding(SEV_WARNING, name, "empty markdown body"))
    elif not t.body.lstrip().startswith("#"):
        f.append(Finding(SEV_WARNING, name, "body does not start with a `#` title heading"))
    return f


def validate_level2(corpus: Corpus) -> list[Finding]:
    f: list[Finding] = []
    ids: dict[str, list[Thing]] = {}
    for t in corpus.things:
        if t.id:
            ids.setdefault(t.id, []).append(t)
    for tid, ts in ids.items():
        if len(ts) > 1:
            paths = ", ".join(str(t.path.relative_to(corpus.root)) for t in ts)
            f.append(Finding(SEV_ERROR, tid, f"duplicate id across files: {paths}"))
    known = set(ids)

    referenced: set[str] = set()
    for t in corpus.things:
        name = t.id or t.path.name
        meta = t.meta
        refs: list[tuple[str, str]] = []
        for entry in meta.get("linked_things") or []:
            if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                refs.append(("linked_things", entry["id"]))
        for fld in ("dependencies", "blocks", "parties"):
            for rid in meta.get(fld) or []:
                if isinstance(rid, str):
                    refs.append((fld, rid))
        if isinstance(meta.get("parent"), str):
            refs.append(("parent", meta["parent"]))
        if isinstance(meta.get("definition"), str):
            refs.append(("definition", meta["definition"]))
        for tr in meta.get("triggers") or []:
            if isinstance(tr, dict):
                watch = tr.get("watch")
                for rid in (watch if isinstance(watch, list) else [watch] if watch else []):
                    if isinstance(rid, str):
                        refs.append(("triggers.watch", rid))
        for fld, rid in refs:
            referenced.add(rid)
            if rid not in known:
                f.append(Finding(SEV_ERROR, name, f"`{fld}` references unknown id `{rid}`"))

        # bidirectional: A blocks B => B depends on A (or links A)
        for blocked in meta.get("blocks") or []:
            target = ids.get(blocked, [None])[0]
            if target:
                deps = target.meta.get("dependencies") or []
                linked = [e.get("id") for e in target.meta.get("linked_things") or []
                          if isinstance(e, dict)]
                if t.id not in deps and t.id not in linked:
                    f.append(Finding(SEV_WARNING, name,
                             f"blocks `{blocked}` but it lists no inverse dependency/link"))

        # contradicts requires a conflict thing listing both parties
        for entry in meta.get("linked_things") or []:
            if isinstance(entry, dict) and entry.get("relation") == "contradicts":
                other = entry.get("id")
                if str(meta.get("type")) == "conflict":
                    continue
                has_conflict = any(
                    str(c.meta.get("type")) == "conflict"
                    and t.id in (c.meta.get("parties") or [])
                    and other in (c.meta.get("parties") or [])
                    for c in corpus.things)
                if not has_conflict:
                    f.append(Finding(SEV_ERROR, name,
                             f"`contradicts: {other}` without a `type: conflict` thing "
                             f"listing both parties"))
            if isinstance(entry, dict) and entry.get("relation") == "supersedes":
                other_t = ids.get(entry.get("id"), [None])[0]
                if other_t:
                    back = any(isinstance(e, dict) and e.get("id") == t.id
                               and e.get("relation") == "superseded-by"
                               for e in other_t.meta.get("linked_things") or [])
                    deprecated = str(other_t.meta.get("status")) == "deprecated"
                    if not back and not deprecated:
                        f.append(Finding(SEV_WARNING, name,
                                 f"supersedes `{entry.get('id')}` but target has no "
                                 f"`superseded-by` link and is not deprecated"))

    # workflow-run cursor integrity (workflow-state.md): a run points at its
    # definition via the structural `definition` field, and `current_stage` must
    # be a stage that definition declares. Pure referential integrity — the
    # floor's job, same class as "linked_things targets must exist". (Transition
    # *legality* across the loop graph stays the agent's Layer-2 judgment.)
    for t in corpus.things:
        if str(t.meta.get("type")) != "workflow-run":
            continue
        name = t.id or t.path.name
        defn_id, cur = t.meta.get("definition"), t.meta.get("current_stage")
        if not isinstance(defn_id, str):
            f.append(Finding(SEV_ERROR, name,
                     "workflow-run missing `definition` (the workflow-definition it instances)"))
            continue
        if cur is None:
            f.append(Finding(SEV_ERROR, name, "workflow-run missing `current_stage`"))
        target = ids.get(defn_id, [None])[0]
        if target is None:
            continue  # unknown id already reported by the referential check above
        if str(target.meta.get("type")) != "workflow-definition":
            f.append(Finding(SEV_ERROR, name,
                     f"`definition` `{defn_id}` is not a workflow-definition"))
            continue
        stage_ids = {s["id"] for s in target.meta.get("stages") or []
                     if isinstance(s, dict) and isinstance(s.get("id"), str)}
        if cur is not None and str(cur) not in stage_ids:
            f.append(Finding(SEV_ERROR, name,
                     f"`current_stage` `{cur}` is not a stage in `{defn_id}` "
                     f"(stages: {sorted(stage_ids)})"))

    # circular dependencies
    graph = {t.id: [d for d in (t.meta.get("dependencies") or []) if isinstance(d, str)]
             for t in corpus.things if t.id}
    state: dict[str, int] = {}

    def visit(node: str, stack: list[str]) -> list[str] | None:
        state[node] = 1
        for nxt in graph.get(node, []):
            if state.get(nxt) == 1:
                return stack + [node, nxt]
            if state.get(nxt, 0) == 0 and nxt in graph:
                cycle = visit(nxt, stack + [node])
                if cycle:
                    return cycle
        state[node] = 2
        return None

    for node in graph:
        if state.get(node, 0) == 0:
            cycle = visit(node, [])
            if cycle:
                f.append(Finding(SEV_ERROR, cycle[0],
                         "circular dependency: " + " -> ".join(cycle)))
                break

    # orphans (Info)
    for t in corpus.things:
        meta = t.meta
        if str(meta.get("type")) in ("continuity-brief", "index"):
            continue
        has_rel = bool(meta.get("linked_things") or meta.get("dependencies")
                       or meta.get("blocks") or meta.get("parent") or meta.get("triggers"))
        if not has_rel and t.id not in referenced:
            f.append(Finding(SEV_INFO, t.id or t.path.name,
                     "orphaned — no relationships, triggers, or inbound references"))
    return f


def version_tuple(v: str) -> tuple[int, int, int]:
    parts = [int(x) for x in re.findall(r"\d+", str(v))[:3]]
    return tuple(parts + [0] * (3 - len(parts)))  # type: ignore[return-value]


def check_version_sync(root: Path) -> list[Finding]:
    """Framework root only: `.markdownllm`, AGENTS.md frontmatter, and the
    latest CHANGELOG entry must agree on the version. The sentinel is what
    domain agents key their refresh off — a stale sentinel silently disables
    domain-refresh for everything shipped since."""
    sentinel = root / ".markdownllm"
    if not sentinel.exists():
        return []
    versions: dict[str, str] = {}
    data = yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}
    if data.get("version"):
        versions[".markdownllm"] = str(data["version"])
    agents = root / "AGENTS.md"
    if agents.exists():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        if meta and meta.get("version"):
            versions["AGENTS.md"] = str(meta["version"])
    changelog = root / "CHANGELOG.md"
    if changelog.exists():
        m = re.search(r"^## \[(\d+(?:\.\d+){1,2})\]",
                      changelog.read_text(encoding="utf-8"), re.MULTILINE)
        if m:
            versions["CHANGELOG.md"] = m.group(1)
    if len({version_tuple(v) for v in versions.values()}) > 1:
        detail = ", ".join(f"{k}={v}" for k, v in sorted(versions.items()))
        return [Finding(SEV_ERROR, "framework-version",
                f"version sentinel out of sync: {detail} — these must be "
                f"bumped together (domain refresh keys off .markdownllm)")]
    return []


def validate_level3(corpus: Corpus) -> list[Finding]:
    f: list[Finding] = []
    schema = corpus.schema
    if not schema:
        return f
    declared_types = set(schema.get("types") or {}) | set(RESERVED_STATUSES)
    relations = schema.get("relations")
    for t in corpus.things:
        name = t.id or t.path.name
        typ = str(t.meta.get("type", ""))
        if typ and typ not in declared_types:
            f.append(Finding(SEV_WARNING, name, f"type `{typ}` not declared in _schema.yaml"))
        tdef = (schema.get("types") or {}).get(typ) or {}
        for req in tdef.get("required_fields") or []:
            if req not in t.meta:
                f.append(Finding(SEV_ERROR, name, f"domain-required field `{req}` missing"))
        if isinstance(relations, list):
            for entry in t.meta.get("linked_things") or []:
                if isinstance(entry, dict) and entry.get("relation") not in relations:
                    f.append(Finding(SEV_WARNING, name,
                             f"relation `{entry.get('relation')}` not in declared vocabulary"))
    return f


def validate_corpus(root: Path) -> tuple[Corpus, list[Finding]]:
    corpus, findings = scan(root)
    for t in corpus.things:
        findings.extend(validate_level1(t, corpus.schema))
    findings.extend(validate_level2(corpus))
    findings.extend(validate_level3(corpus))
    return corpus, findings


def example_corpora(root: Path) -> list[Path]:
    """Example domains live in <root>/examples/<name>/ with their own
    AGENTS.md and _schema.yaml. They are excluded from the root corpus walk
    (separate id space, separate schema) but they are NOT exempt from the
    floor: validate discovers and checks each one as its own corpus, so the
    pre-commit hook covers them in the same run."""
    examples = root / "examples"
    if not examples.is_dir():
        return []
    return sorted(d for d in examples.iterdir()
                  if d.is_dir() and (d / "AGENTS.md").exists())


def cmd_validate(args) -> int:
    root = Path(args.path).resolve()
    reports: list[tuple[Path, Corpus, list[Finding]]] = []
    corpus, findings = validate_corpus(root)
    findings.extend(check_version_sync(root))
    reports.append((root, corpus, findings))
    for sub in example_corpora(root):
        sub_corpus, sub_findings = validate_corpus(sub)
        reports.append((sub, sub_corpus, sub_findings))

    total_errors = 0
    for rpt_root, rpt_corpus, rpt_findings in reports:
        errors = [x for x in rpt_findings if x.severity == SEV_ERROR]
        warnings = [x for x in rpt_findings if x.severity == SEV_WARNING]
        infos = [x for x in rpt_findings if x.severity == SEV_INFO]
        total_errors += len(errors)

        if not args.quiet or errors:
            print(f"## Validation Report — {rpt_root}")
            print(f"schema: {'_schema.yaml found' if rpt_corpus.schema else 'none (default vocabulary, advisory)'}\n")
            for title, group in (("Errors (must fix)", errors),
                                 ("Warnings (should fix)", warnings),
                                 ("Info (worth knowing)", infos)):
                if group:
                    print(f"### {title}")
                    for x in group:
                        print(f"- **{x.thing}**: {x.message}")
                    print()
            print("### Summary")
            print(f"- Things checked: {len(rpt_corpus.things)}")
            print(f"- Errors: {len(errors)}  Warnings: {len(warnings)}  Info: {len(infos)}")
            clean = len(rpt_corpus.things) - len({x.thing for x in rpt_findings})
            print(f"- Clean: {max(clean, 0)}")
            print()
    return 1 if total_errors else 0


# ---------------------------------------------------------------- triggers


def cmd_triggers(args) -> int:
    root = Path(args.path).resolve()
    corpus, _ = scan(root)
    today = dt.date.today()
    by_id = corpus.by_id()
    hits: list[str] = []
    skipped: list[str] = []

    def as_date(v):
        if isinstance(v, dt.datetime):
            return v.date()
        if isinstance(v, dt.date):
            return v
        if isinstance(v, str) and ISO_RE.match(v):
            return dt.date.fromisoformat(v[:10])
        return None

    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        status = str(meta.get("status", ""))
        for tr in meta.get("triggers") or []:
            if not isinstance(tr, dict):
                continue
            ttype, cond, action = tr.get("type"), tr.get("condition"), tr.get("action")
            if ttype == "time":
                if cond == "due_date_passed":
                    due = as_date(meta.get("due_date"))
                    if due and due < today and status not in TERMINAL_STATUSES:
                        hits.append(f"{name}: due_date {due} passed "
                                    f"({(today - due).days}d ago) -> {action}")
                elif cond == "review_date_reached":
                    rd = as_date(meta.get("review_date"))
                    if rd and rd <= today:
                        hits.append(f"{name}: review_date {rd} reached -> {action}")
                elif cond == "stale":
                    thresh = str(tr.get("threshold", "30d")).rstrip("d")
                    mtime = dt.date.fromtimestamp(t.path.stat().st_mtime)
                    if (today - mtime).days > int(thresh):
                        hits.append(f"{name}: unmodified {(today - mtime).days}d "
                                    f"(threshold {thresh}d) -> {action}")
            elif ttype == "dependency":
                watch = tr.get("watch") or []
                watch = watch if isinstance(watch, list) else [watch]
                value = tr.get("value")
                if tr.get("on") == "status_changed_to" and value:
                    states = [str(by_id[w].meta.get("status")) for w in watch if w in by_id]
                    if states and all(s == str(value) for s in states):
                        hits.append(f"{name}: all watched ({', '.join(watch)}) are "
                                    f"`{value}` -> {action}")
            elif ttype == "threshold":
                if cond == "subtasks_complete":
                    subs = [e.get("id") for e in meta.get("linked_things") or []
                            if isinstance(e, dict) and e.get("relation") == "subtask"]
                    if subs and all(str(by_id[s].meta.get("status")) in TERMINAL_STATUSES
                                    for s in subs if s in by_id):
                        hits.append(f"{name}: all subtasks complete -> {action}")
                elif cond == "blocked_duration":
                    skipped.append(f"{name}: `blocked_duration` needs status history "
                                   f"(evaluate via git log) — left to the agent")

    # Deadline scan: every non-terminal date-bearing thing, triggers or not.
    horizon: list[tuple[int, str]] = []
    for t in corpus.things:
        meta, name = t.meta, t.id or t.path.name
        due = as_date(meta.get("due_date"))
        if due and str(meta.get("status", "")) not in TERMINAL_STATUSES:
            days = (due - today).days
            if days < 0 and not meta.get("triggers"):
                hits.append(f"{name}: OVERDUE by {-days}d (due {due}, no trigger declared)")
            elif 0 <= days <= 30:
                hits.append(f"{name}: due in {days}d ({due})")
            elif days > 30:
                horizon.append((days, f"{name}: due {due} ({days}d out)"))

    print(f"## Trigger Evaluation — {root}  ({today})\n")
    if hits:
        for h in hits:
            print(f"- {h}")
    else:
        print("No trigger conditions currently true.")
    if horizon:
        print("\n### Horizon (beyond 30 days)")
        for _, line in sorted(horizon):
            print(f"- {line}")
    if skipped:
        print("\n### Not mechanically evaluable")
        for s in skipped:
            print(f"- {s}")
    return 0


# ---------------------------------------------------------------- indexes


def git_short_sha(root: Path) -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def framework_version(root: Path) -> str:
    p = root
    for _ in range(4):
        f = p / ".markdownllm"
        if f.exists():
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
            return str(data.get("version", "unknown"))
        p = p.parent
    return "unknown"


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


def cmd_index(args) -> int:
    root = Path(args.path).resolve()
    corpus, _ = scan(root)
    signals = [args.signal] if args.signal else ["triggers", "schema",
                                                 "relationships", "provenance"]
    idx_dir = root / "things" / "_index"
    rc = 0
    for signal in signals:
        body, coverage = build_index_body(corpus, signal)
        fname = {"triggers": "triggers.md", "schema": "schema.md",
                 "relationships": "relationships.md",
                 "provenance": "provenance.md"}[signal]
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


# ---------------------------------------------------------------- tokens

TIERS = {
    "Tier 0 (always)": ["AGENTS.md", "kernel.md"],
    "Tier 1 (full specs, load individually on demand)": [
        "thing.md", "orchestration.md", "read.thing.md", "write.thing.md",
        "validate.thing.md", "git-workflow.md"],
    "Tier 2 (on demand)": [
        "domain-specification-guide.md", "scalability-guide.md", "thing-lifecycle.md",
        "llm-driven-systems.manifesto.md", "interface.md", "framework-discovery.md",
        "domain-refresh.md", "session-memory.md", "belief-revision.md",
        "retrospective.md", "trigger-specification.md", "derived-index.md",
        "example-things.md", "reasoning-lenses.md", "provenance.md",
        "change-reconciliation.md", "workflow-state.md", "coordination-claim.md",
    ],
}


def cmd_tokens(args) -> int:
    root = Path(args.path).resolve()
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        count, method = (lambda s: len(enc.encode(s))), "tiktoken o200k_base"
    except ImportError:
        count, method = (lambda s: round(len(s) / 3.8)), "heuristic chars/3.8"
    print(f"Token measurement ({method})  root={root}\n")
    totals = {}
    for tier, files in TIERS.items():
        print(f"## {tier}")
        total = 0
        for name in files:
            p = root / name
            if not p.exists():
                continue
            n = count(p.read_text(encoding="utf-8"))
            total += n
            print(f"  {name:<40} {n:>7,}")
        totals[tier] = total
        print(f"  {'TIER TOTAL':<40} {total:>7,}\n")
    t0 = totals.get("Tier 0 (always)", 0)
    print(f"{'FULL LOAD':<42} {sum(totals.values()):>7,}")
    print(f"{'Tier 0 (AGENTS.md + kernel.md)':<42} {t0:>7,}")
    return 0


# ---------------------------------------------------------------- hook


def cmd_provenance(args) -> int:
    """Mechanical checks for provenance chains (provenance.md)."""
    root = Path(args.path).resolve()
    corpus, _ = scan(root)
    by_id = corpus.by_id()
    findings: list[Finding] = []
    today = dt.date.today()

    def commit_exists(sha: str) -> bool:
        return subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                              cwd=root, capture_output=True).returncode == 0

    def exists_at(sha: str, thing_id: str) -> bool:
        out = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha],
                             cwd=root, capture_output=True, text=True)
        return out.returncode == 0 and any(
            p.endswith(f"{thing_id}.md") for p in out.stdout.splitlines())

    for t in corpus.things:
        name = t.id or t.path.name
        for i, pin in enumerate(t.meta.get("informed_by") or []):
            if not isinstance(pin, dict) or not pin.get("id") or not pin.get("commit"):
                findings.append(Finding(SEV_ERROR, name,
                                f"`informed_by[{i}]` must have `id` and `commit`"))
                continue
            pid, sha = str(pin["id"]), str(pin["commit"])
            if not commit_exists(sha):
                findings.append(Finding(SEV_ERROR, name,
                                f"pinned commit `{sha}` does not exist"))
                continue
            src = by_id.get(pid)
            if src is None and not exists_at(sha, pid):
                findings.append(Finding(SEV_ERROR, name,
                                f"pinned input `{pid}` not found (current corpus "
                                f"or at {sha})"))
            if src is not None:
                if (str(src.meta.get("origin")) == "external"
                        and src.meta.get("verified") is not True):
                    findings.append(Finding(SEV_ERROR, name,
                                    f"pins UNVERIFIED external thing `{pid}` — "
                                    f"quarantine rule violated"))
                rel = src.path.relative_to(root).as_posix()
                log = subprocess.run(["git", "log", "--oneline", f"{sha}..HEAD",
                                      "--", rel], cwd=root, capture_output=True,
                                     text=True)
                if log.returncode == 0 and log.stdout.strip():
                    n = len(log.stdout.strip().splitlines())
                    findings.append(Finding(SEV_INFO, name,
                                    f"input `{pid}` changed in {n} commit(s) since "
                                    f"pin {sha} — decision may be dated"))

        if str(t.meta.get("origin")) == "external" and t.meta.get("verified") is not True:
            created = t.meta.get("created")
            age = ""
            if isinstance(created, (dt.date, dt.datetime)):
                c = created.date() if isinstance(created, dt.datetime) else created
                days = (today - c).days
                age = f" ({days}d old)"
                sev = SEV_INFO if days > 30 else None
            else:
                sev = SEV_INFO
            if sev:
                findings.append(Finding(sev, t.id or t.path.name,
                                f"external thing still unverified{age}"))

    errors = [x for x in findings if x.severity == SEV_ERROR]
    print(f"## Provenance Report — {root}\n")
    if not findings:
        print("No provenance issues found.")
    for title, group in (("Errors", errors),
                         ("Info", [x for x in findings if x.severity == SEV_INFO])):
        if group:
            print(f"### {title}")
            for x in group:
                print(f"- **{x.thing}**: {x.message}")
            print()
    return 1 if errors else 0


def cmd_changelog(args) -> int:
    """Draft a CHANGELOG entry from structured commit messages since a ref."""
    root = Path(args.path).resolve()
    rng = f"{args.since}..HEAD" if args.since else "HEAD"
    out = subprocess.run(["git", "log", "--format=%s", rng], cwd=root,
                         capture_output=True, text=True, check=True).stdout
    groups: dict[str, list[str]] = {}
    for line in out.strip().splitlines():
        prefix = line.split(":", 1)[0].strip() if ":" in line else "other"
        groups.setdefault(prefix, []).append(line)
    order = ["framework", "create", "update", "insight", "retrospective",
             "session-end", "measure", "validate", "fix", "docs", "chore", "other"]
    print(f"## [x.y.z] - {dt.date.today().isoformat()}\n")
    print("<!-- drafted by `mdllm changelog`; set the version, write the one-paragraph")
    print("     summary, prune noise — then commit. WORKLOG holds the detail. -->\n")
    for key in sorted(groups, key=lambda k: order.index(k) if k in order else 99):
        print(f"**{key}:**")
        for line in groups[key]:
            print(f"- {line}")
        print()
    return 0


def cmd_worklog(args) -> int:
    """Generate WORKLOG.md from the commit stream (review #5: generate-or-kill —
    the WORKLOG was the last hand-maintained tracking surface). Sessions are
    delimited by `session-end:` commits; within a session, commits are listed
    in the order the work happened. The narrative detail lives in `git log` —
    this file is the structured session index over it. CHANGELOG stays the
    external per-version record; this is the internal per-session one."""
    root = Path(args.path).resolve()
    fmt = "%H%x1f%ad%x1f%s"
    # Decode git output as UTF-8 explicitly: text=True would use the locale
    # codepage (cp1252 on Windows), which mangles em-dashes in commit subjects.
    out = subprocess.run(["git", "log", "--reverse", "--date=short",
                          f"--format={fmt}", "HEAD"], cwd=root,
                         capture_output=True, encoding="utf-8", errors="replace",
                         check=True).stdout
    commits = [tuple(line.split("\x1f", 2)) for line in out.strip().splitlines() if line]
    if not commits:
        print("mdllm: no commits — nothing to generate")
        return 0

    sessions: list[list[tuple]] = []
    cur: list[tuple] = []
    for c in commits:
        cur.append(c)
        if c[2].startswith("session-end"):
            sessions.append(cur)
            cur = []
    if cur:
        sessions.append(cur)

    L = ["---", "id: framework-worklog", "type: artifact", "status: evolving",
         f"created: {commits[0][1]}",
         "linked_things:",
         "  - id: llm-driven-systems-manifesto",
         "    relation: documents",
         "---", "",
         "# Framework Work Log", "",
         "> Generated by `mdllm worklog` from the commit stream — do not hand-edit.",
         "> Sessions are delimited by `session-end:` commits; full detail is in `git log`.",
         ""]
    for sess in reversed(sessions):
        first_d, last_d = sess[0][1], sess[-1][1]
        closed = sess[-1][2].startswith("session-end")
        title = sess[-1][2] if closed else "in progress"
        label = first_d if first_d == last_d else f"{first_d} → {last_d}"
        L += [f"## {label} — {title}", ""]
        for h, _d, s in (sess[:-1] if closed else sess):
            L.append(f"- `{h[:9]}` {s}")
        L.append("")
    content = "\n".join(L).rstrip() + "\n"
    if args.write:
        (root / "WORKLOG.md").write_text(content, encoding="utf-8", newline="\n")
        print(f"wrote WORKLOG.md — {len(sessions)} sessions from {len(commits)} commits")
    else:
        print(content)
    return 0


def _changelog_versions_since(changelog: Path, seen: str) -> list[str]:
    """Heading lines (`## [x.y.z] - date`) in CHANGELOG.md newer than `seen`."""
    if not changelog.is_file():
        return []
    out = []
    for line in changelog.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## \[([0-9][^\]]*)\] - (.+)$", line.strip())
        if m and (not seen or _version_lt(seen, m.group(1))):
            out.append(f"v{m.group(1)} ({m.group(2)})")
    return out


def cmd_refresh(args) -> int:
    """Floor-only domain refresh (review #7, Option A): the MECHANICAL half of
    domain-refresh.md. Reports the version delta and the CHANGELOG entries the
    domain has not yet seen, so the agent does the SEMANTIC adoption rather than
    diffing by hand. With --seal, bumps `framework_version_seen` AFTER the agent
    confirms adoption. Never rewrites domain skills — that is semantic, and
    stays the agent's job (the floor/agent split)."""
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    if not agents.is_file():
        sys.exit(f"mdllm: {domain} has no AGENTS.md — not a domain")
    text = agents.read_text(encoding="utf-8")
    meta, _, _ = parse_frontmatter(text)
    fr = (meta or {}).get("framework_root")
    if not fr:
        sys.exit("mdllm: AGENTS.md has no framework_root — not a wired domain")
    froot = (domain / fr).resolve()
    sentinel = froot / ".markdownllm"
    if not sentinel.is_file():
        sys.exit(f"mdllm: framework_root `{fr}` does not resolve to a framework "
                 f"(.markdownllm not found at {sentinel})")
    fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}).get("version"))
    seen = str(meta.get("framework_version_seen", "")) if meta else ""

    print(f"## Domain Refresh — {domain.name}\n")
    print(f"  framework_root : {froot}")
    print(f"  framework      : {fv}")
    print(f"  last seen      : {seen or '<unset — treat as fully stale>'}")

    if seen == fv:
        print("\nUp to date. Nothing to refresh.")
        return 0

    deltas = _changelog_versions_since(froot / 'CHANGELOG.md', seen)
    if deltas:
        print("\n  Versions not yet absorbed (semantic adoption is the agent's job):")
        for d in deltas:
            print(f"    - {d}")
        print("\n  Read those CHANGELOG entries + foundational spec versions, adopt new "
              "capabilities into domain skills/AGENTS.md, then re-run with --seal.")
    else:
        print("\n  Framework is ahead but no newer CHANGELOG entries parsed — verify by hand.")

    if args.seal:
        if "framework_version_seen:" in text:
            new = re.sub(r"(?m)^(framework_version_seen:).*$",
                         rf"\g<1> {fv}", text, count=1)
        else:
            new = re.sub(r"(?m)^(framework_root:.*)$",
                         rf"\1\nframework_version_seen: {fv}", text, count=1)
        agents.write_text(new, encoding="utf-8", newline="\n")
        print(f"\nsealed: framework_version_seen → {fv} "
              f"(commit the domain AGENTS.md to record the refresh)")
    return 0


HOOK_BODY = """#!/bin/sh
# mdllm pre-commit: deterministic validation floor (transformation plan Phase 1)
# Portable: repo root and interpreter are resolved at run time, mdllm.py via a
# path relative to the repo root — so the same hook works wherever this repo is
# checked out or mounted (Windows, WSL, CI, sandboxed agent harnesses).
ROOT="$(git rev-parse --show-toplevel)"
MDLLM="$ROOT/{rel}"
# Candidates are executed, not just resolved: on Windows, the Microsoft Store
# ships alias stubs named python/python3 that command -v happily finds but
# that only print an install hint and exit nonzero.
PY=""
for c in python3 python py; do
  if "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
if [ -z "$PY" ] || [ ! -f "$MDLLM" ]; then
  echo "mdllm: validation floor unavailable (python or $MDLLM not found) — commit blocked."
  echo "Install Python 3.10+ with PyYAML, or re-run install-hook from the framework root."
  exit 1
fi
"$PY" "$MDLLM" validate "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: validation Errors — commit blocked. Fix or run with --no-verify (discouraged)."
  exit 1
}}
"""


def check_assertions(fixture: dict, domain_root: Path) -> tuple[int, int, list[str]]:
    """Stage 1: deterministic assertions against a domain's current state.

    `domain_root` is the workspace; if the fixture declares `domain_dir`
    (scaffold-style fixtures, where the agent *creates* the domain in a
    subfolder), thing/status/field/link/validates assertions scan that
    subfolder while file/git assertions stay workspace-relative."""
    ws = domain_root
    droot = (ws / fixture["domain_dir"]) if fixture.get("domain_dir") else ws
    corpus, _ = scan(droot) if droot.is_dir() else (Corpus(root=droot), [])
    by_id = corpus.by_id()
    passed = failed = 0
    lines: list[str] = []

    def report(ok: bool, label: str):
        nonlocal passed, failed
        passed, failed = passed + ok, failed + (not ok)
        lines.append(f"  {'PASS' if ok else 'FAIL'}  {label}")

    for a in fixture.get("assertions") or []:
        if "thing_exists" in a:
            tid = a["thing_exists"]
            report(tid in by_id, f"thing exists: {tid}")
        elif "status" in a:
            s = a["status"]
            t = by_id.get(s["id"])
            actual = str(t.meta.get("status")) if t else "<missing>"
            report(actual == str(s["equals"]),
                   f"status of {s['id']} == {s['equals']} (actual: {actual})")
        elif "field" in a:
            fa = a["field"]
            t = by_id.get(fa["id"])
            actual = t.meta.get(fa["name"]) if t else "<missing>"
            expected = fa["equals"]
            ok = actual == expected
            if not ok and isinstance(expected, (int, float)) and not isinstance(expected, bool):
                # `2500.00` written as the string "2500.00" is semantically
                # correct — coerce before failing a numeric contract.
                try:
                    ok = abs(float(actual) - float(expected)) < 1e-9
                except (TypeError, ValueError):
                    ok = False
            report(ok, f"{fa['id']}.{fa['name']} == {expected!r} (actual: {actual!r})")
        elif "link" in a:
            ln = a["link"]
            t = by_id.get(ln["from"])
            ok = bool(t) and any(
                isinstance(e, dict) and e.get("id") == ln["to"]
                and e.get("relation") == ln["relation"]
                for e in t.meta.get("linked_things") or [])
            report(ok, f"link: {ln['from']} --{ln['relation']}--> {ln['to']}")
        elif "validates_clean" in a:
            findings = []
            for t in corpus.things:
                findings.extend(validate_level1(t, corpus.schema))
            findings.extend(validate_level2(corpus))
            findings.extend(validate_level3(corpus))
            errs = [x for x in findings if x.severity == SEV_ERROR]
            report(not errs, f"validates clean (Errors: {len(errs)})")
        elif "file_exists" in a:
            paths = a["file_exists"]
            paths = [paths] if isinstance(paths, str) else paths
            report(any((ws / p).exists() for p in paths),
                   f"file exists: {' or '.join(paths)}")
        elif "file_contains" in a:
            fc = a["file_contains"]
            f_ = ws / fc["path"]
            ok = f_.is_file() and fc["text"] in f_.read_text(encoding="utf-8")
            report(ok, f"{fc['path']} contains {fc['text']!r}")
        elif "git_repo" in a:
            report((ws / a["git_repo"] / ".git").exists(),
                   f"own git repo: {a['git_repo']}")
        elif "git_commits" in a:
            gc = a["git_commits"]
            tgt = ws / gc["path"]
            n = 0
            if (tgt / ".git").exists():
                out = subprocess.run(["git", "rev-list", "--count", "HEAD"],
                                     cwd=tgt, capture_output=True, text=True)
                if out.returncode == 0 and out.stdout.strip().isdigit():
                    n = int(out.stdout.strip())
            report(n >= gc.get("min", 1),
                   f"git commits in {gc['path']}: {n} (need >= {gc.get('min', 1)})")
        elif "min_things" in a:
            report(len(corpus.things) >= a["min_things"],
                   f"things in domain >= {a['min_things']} (actual: {len(corpus.things)})")
        else:
            report(False, f"unknown assertion: {a}")
    return passed, failed, lines


def seed_run_dir(root: Path, fixture: dict, run_dir: Path, bare: bool) -> None:
    """Stage 2 workspace: copy the seed into an isolated git repo."""
    import shutil
    seed = root / fixture["seed"]
    if not seed.is_dir():
        sys.exit(f"mdllm: fixture seed not found: {seed}")
    shutil.copytree(seed, run_dir)
    if bare:
        # The no-framework condition: same data, no operating system.
        for p in ("AGENTS.md", "CLAUDE.md", "things/_schema.yaml"):
            f = run_dir / p
            if f.exists():
                f.unlink()
        skills = run_dir / "skills"
        if skills.is_dir():
            shutil.rmtree(skills)
    subprocess.run(["git", "init", "-q"], cwd=run_dir, check=True)
    subprocess.run(["git", "add", "-A"], cwd=run_dir, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "seed"], cwd=run_dir, check=True)


def eval_report(root: Path) -> int:
    """Aggregate evals/results/*.json (the committed evidence mirror; legacy
    fallback: evals/runs/*/result.json) into per-cell pass rates."""
    import json as _json
    results = []
    res_dir = root / "evals" / "results"
    paths = sorted(res_dir.glob("*.json")) if res_dir.is_dir() else []
    if not paths:
        runs_dir = root / "evals" / "runs"
        paths = sorted(runs_dir.glob("*/result.json")) if runs_dir.is_dir() else []
    for rj in paths:
        try:
            results.append(_json.loads(rj.read_text(encoding="utf-8")))
        except ValueError:
            print(f"  skipping unparseable {rj}")
    if not results:
        print(f"No run results under {runs_dir}")
        return 1
    cells: dict[tuple[str, str, str], list[dict]] = {}
    for r in results:
        # Legacy runs predate the fixture tag (the 2026-06-11 2x2 was all one
        # fixture); group them under their known name rather than "?".
        fx = str(r.get("fixture", "VAT quarter prep (synthetic, known-correct figures)"))
        cells.setdefault((fx, str(r.get("model")), str(r.get("condition"))), []).append(r)
    print(f"## Eval Report — {len(results)} trials, {len(cells)} cells\n")
    print("| fixture | model | condition | trials | fully passing | assertion pass rate "
          "| mean wall s | mean cost $ |")
    print("|---|---|---|---|---|---|---|---|")
    for (fx, model, cond), rs in sorted(cells.items()):
        full = sum(1 for r in rs if r.get("failed") == 0)
        p = sum(r.get("passed", 0) for r in rs)
        f_ = sum(r.get("failed", 0) for r in rs)
        rate = f"{p}/{p + f_} ({p / (p + f_):.0%})" if p + f_ else "—"
        walls = [r["wall_s"] for r in rs if r.get("wall_s") is not None]
        costs = [r["cost_usd"] for r in rs if r.get("cost_usd") is not None]
        mw = f"{sum(walls) / len(walls):.0f}" if walls else "—"
        mc = f"{sum(costs) / len(costs):.3f}" if costs else "—"
        fx_short = fx if len(fx) <= 40 else fx[:37] + "..."
        print(f"| {fx_short} | {model} | {cond} | {len(rs)} | {full}/{len(rs)} | {rate} "
              f"| {mw} | {mc} |")
    return 0


def _resolve_claude_cli(exe: str) -> str:
    """On Windows, npm installs `claude` as a .CMD shim around a real .exe;
    running the shim via subprocess routes through cmd.exe, whose argument
    quoting mangles flags containing `(`, `)`, `*` (e.g. `Bash(git:*)`,
    `--permission-mode acceptEdits`). Resolve to the underlying binary."""
    p = Path(exe)
    if p.suffix.lower() in (".cmd", ".bat"):
        real = (p.parent / "node_modules" / "@anthropic-ai" / "claude-code"
                / "bin" / "claude.exe")
        if real.is_file():
            return str(real)
    return exe


def cmd_eval(args) -> int:
    """Stage 1 (default): assert a fixture against an existing domain's state.
    Stage 2 (--run): seed an isolated workspace, run a fresh headless agent on
    the fixture's prompt, then assert the result. See evals/README.md."""
    root = Path(args.path).resolve()
    if args.report:
        return eval_report(root)
    if not args.fixture:
        sys.exit("mdllm: eval requires --fixture (or --report)")
    fixture = yaml.safe_load(Path(args.fixture).read_text(encoding="utf-8"))
    sentinel = root / ".markdownllm"
    if sentinel.is_file():
        # Fixtures must not hardcode the framework version (it breaks on the
        # next release) — `{framework_version}` resolves from the sentinel.
        fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {})
                 .get("version"))

        def _subst(o):
            if isinstance(o, str):
                return o.replace("{framework_version}", fv)
            if isinstance(o, list):
                return [_subst(x) for x in o]
            if isinstance(o, dict):
                return {k: _subst(v) for k, v in o.items()}
            return o
        fixture = _subst(fixture)
    name = fixture.get("name", args.fixture)

    if not args.run:
        print(f"## Eval: {name} — {root}\n")
        passed, failed, lines = check_assertions(fixture, root)
        print("\n".join(lines))
        print(f"\n{passed} passed, {failed} failed")
        return 1 if failed else 0

    # ---- Stage 2: agent-in-the-loop -------------------------------------
    if "seed" not in fixture or "prompt" not in fixture:
        sys.exit("mdllm: --run requires `seed` and `prompt` in the fixture")
    prompt = fixture["prompt"]
    if args.bare:
        prompt = (fixture.get("bare_preamble",
                  "You are in a directory of markdown files with YAML "
                  "frontmatter representing business records.") + "\n\n" + prompt)
    import json as _json
    results = []

    def record(run_id: str, run_dir: Path, res: dict) -> None:
        """Run dirs are gitignored workspaces; evals/results/ is the committed
        evidence mirror — the claim and the data travel together."""
        results.append(res)
        payload = _json.dumps(res, indent=2)
        (run_dir / "result.json").write_text(payload, encoding="utf-8")
        res_dir = root / "evals" / "results"
        res_dir.mkdir(parents=True, exist_ok=True)
        (res_dir / f"{run_id}.json").write_text(payload, encoding="utf-8")

    for trial in range(1, args.trials + 1):
        run_id = (f"{dt.datetime.now():%Y%m%d-%H%M%S}-"
                  f"{args.model}-{'bare' if args.bare else 'fw'}-t{trial}")
        run_dir = root / "evals" / "runs" / run_id
        run_dir.parent.mkdir(parents=True, exist_ok=True)
        seed_run_dir(root, fixture, run_dir, args.bare)
        cmd = ["claude", "-p", prompt, "--model", args.model,
               "--output-format", "json", "--permission-mode", "acceptEdits",
               "--allowedTools", fixture.get("allowed_tools",
                                             "Edit Write Read Glob Grep Bash(git:*)")]
        if not args.bare:
            # The seed's framework_root resolves to the framework checkout;
            # the bare condition must NOT see it — that's the control.
            cmd += ["--add-dir", str(root)]
        print(f"## Trial {trial}/{args.trials} — {run_id}")
        if args.dry_run:
            print(f"  workspace: {run_dir}")
            print(f"  would run (cwd=workspace): {' '.join(cmd[:2])} "
                  f"<prompt {len(prompt)} chars> {' '.join(cmd[3:])}")
            continue
        import shutil as _sh
        exe = _sh.which("claude")
        if not exe:
            sys.exit("mdllm: `claude` CLI not on PATH — install "
                     "@anthropic-ai/claude-code or use --dry-run")
        cmd[0] = _resolve_claude_cli(exe)
        t0 = dt.datetime.now()
        try:
            proc = subprocess.run(cmd, cwd=run_dir, capture_output=True, text=True,
                                  timeout=args.timeout, encoding="utf-8")
        except subprocess.TimeoutExpired:
            wall = (dt.datetime.now() - t0).total_seconds()
            n_asserts = len(fixture.get("assertions") or [])
            print(f"  TIMEOUT after {wall:.0f}s — trial recorded as 0/{n_asserts}\n")
            record(run_id, run_dir, {"run_id": run_id, "fixture": name,
                   "model": args.model,
                   "condition": "bare" if args.bare else "framework",
                   "passed": 0, "failed": n_asserts,
                   "wall_s": round(wall), "cost_usd": None,
                   "turns": None, "timeout": True})
            continue
        wall = (dt.datetime.now() - t0).total_seconds()
        # Always persist the agent's raw output — a 2-second 1-turn "trial"
        # is indistinguishable from a real one without it.
        (run_dir / "agent-stdout.json").write_text(proc.stdout or "", encoding="utf-8")
        if proc.stderr:
            (run_dir / "agent-stderr.txt").write_text(proc.stderr, encoding="utf-8")
        cost = turns = None
        try:
            meta = _json.loads(proc.stdout)
            cost, turns = meta.get("total_cost_usd"), meta.get("num_turns")
            if meta.get("is_error") or meta.get("subtype") not in (None, "success"):
                print(f"  AGENT ERROR ({meta.get('subtype')}): "
                      f"{str(meta.get('result'))[:200]}")
        except (ValueError, TypeError):
            pass
        passed, failed, lines = check_assertions(fixture, run_dir)
        print("\n".join(lines))
        score = f"{passed}/{passed + failed}"
        print(f"  score {score} · {wall:.0f}s · cost {cost} · turns {turns}\n")
        record(run_id, run_dir, {"run_id": run_id, "fixture": name,
               "model": args.model,
               "condition": "bare" if args.bare else "framework",
               "passed": passed, "failed": failed,
               "wall_s": round(wall), "cost_usd": cost, "turns": turns})
    if results:
        ok = sum(1 for r in results if r["failed"] == 0)
        print(f"### {name}: {ok}/{len(results)} trials fully passing "
              f"({args.model}, {'bare' if args.bare else 'framework'})")
    return 0


KERNEL_RE = re.compile(r"<!--\s*kernel\s*-->\s*\n(.*?)<!--\s*/kernel\s*-->", re.DOTALL)


def cmd_kernel(args) -> int:
    """Generate kernel.md from <!-- kernel --> blocks in foundational specs."""
    root = Path(args.path).resolve()
    sentinel = root / ".markdownllm"
    if not sentinel.exists():
        sys.exit("mdllm: kernel requires a framework root (.markdownllm not found)")
    data = yaml.safe_load(sentinel.read_text(encoding="utf-8"))
    specs = data.get("foundational_specs") or []
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        count = lambda s: len(enc.encode(s))
    except ImportError:
        count = lambda s: round(len(s) / 3.8)

    sections: list[str] = []
    full_total = kernel_total = 0
    for name in specs:
        p = root / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        full_total += count(text)
        blocks = KERNEL_RE.findall(text)
        if not blocks:
            continue
        body = "\n".join(b.strip() for b in blocks)
        kernel_total += count(body)
        sections.append(f"## {name}\n\n{body}\n")
        print(f"  {name:<40} {count(body):>6,} / {count(text):>6,} tokens")

    out = root / "kernel.md"
    body = (
        "# Framework Operative Kernel\n\n"
        "Generated by `mdllm kernel` from the `<!-- kernel -->` blocks in the\n"
        "foundational specs — the rules without the rationale. Load this at Tier 0\n"
        "instead of the full specs; load a full spec only when reasoning *about*\n"
        "the framework or when the kernel says to. Regenerate after any spec change.\n\n"
        + "\n".join(sections))

    if args.check:
        # Drift check: compare the deterministic body (frontmatter carries
        # timestamps/SHAs and is expected to differ between regenerations).
        if not out.exists():
            print("\nkernel.md missing — run `mdllm kernel` to generate it")
            return 1
        _, existing_body, _ = parse_frontmatter(out.read_text(encoding="utf-8"))
        if existing_body.strip() != body.strip():
            print("\nkernel: DRIFT — spec kernel blocks changed since kernel.md "
                  "was generated; run `mdllm kernel` and commit the result")
            return 1
        print("\nkernel: in sync")
        return 0

    content = (
        "---\n"
        "id: framework-kernel\n"
        "type: index\n"
        "status: live\n"
        "index_of: kernel\n"
        f"created: {dt.date.today().isoformat()}\n"
        f"generated: {dt.datetime.now().isoformat(timespec='seconds')}\n"
        f"generated_from: HEAD@{git_short_sha(root)}\n"
        f"coverage: {len(sections)}\n"
        f"framework_version: {data.get('version', 'unknown')}\n"
        "---\n\n"
        + body)
    out.write_text(content, encoding="utf-8")
    print(f"\nwrote kernel.md — {count(content):,} tokens "
          f"(kernel blocks {kernel_total:,} / full specs {full_total:,})")
    return 0


def _version_lt(a: str, b: str) -> bool:
    """Semver-ish less-than over dotted numeric versions, tolerant of junk."""
    def parts(v: str):
        out = []
        for chunk in str(v).split("."):
            num = "".join(ch for ch in chunk if ch.isdigit())
            out.append(int(num) if num else 0)
        return out
    pa, pb = parts(a), parts(b)
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    return pa < pb


def _upstream_sentinel_version(root: Path):
    """Read the framework version from the *cached* upstream copy of
    `.markdownllm` — git's remote-tracking objects, with no network call
    (orchestration.md → session-start:version-check upward leg). Tries the
    current branch's configured upstream first, then origin/main / origin/HEAD.
    Returns the version string, or None when no fetched copy is available."""
    refs = []
    up = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
                        cwd=root, capture_output=True, text=True)
    if up.returncode == 0 and up.stdout.strip():
        refs.append(up.stdout.strip())
    refs += ["origin/main", "origin/HEAD"]
    for ref in refs:
        show = subprocess.run(["git", "show", f"{ref}:.markdownllm"],
                              cwd=root, capture_output=True, text=True)
        if show.returncode == 0 and show.stdout.strip():
            try:
                data = yaml.safe_load(show.stdout) or {}
            except yaml.YAMLError:
                continue
            v = data.get("version")
            if v is not None:
                return str(v)
    return None


def cmd_doctor(args) -> int:
    """Probe the environment the floor depends on. A floor/portability claim
    is verified only by executing the capability in the target environment
    (insight: portability-claims-need-execution-tests) — so the hook check
    *runs* the hook rather than checking the file exists. Exit 1 when the
    floor cannot run here (degraded mode: run `mdllm validate` manually
    before each commit, and say so)."""
    import shutil
    root = Path(args.path).resolve()
    lines: list[str] = []
    floor_ok = True

    def report(status: str, label: str):
        lines.append(f"  {status:4s}  {label}")

    # interpreter + libraries (if we got this far, python and yaml exist)
    py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    if sys.version_info >= (3, 10):
        report("OK", f"python {py}")
    else:
        report("FAIL", f"python {py} — floor requires 3.10+")
        floor_ok = False
    report("OK", f"pyyaml {getattr(yaml, '__version__', '?')}")
    try:
        import tiktoken
        report("OK", f"tiktoken {getattr(tiktoken, '__version__', '?')} — token counts are measured")
    except ImportError:
        report("--", "tiktoken absent — `tokens` falls back to a chars/3.8 heuristic (fine)")

    # git + identity
    git = shutil.which("git")
    if not git:
        report("FAIL", "git not on PATH — the floor and the state machine need git")
        print(f"## Doctor Report — {root}\n" + "\n".join(lines))
        print("\nVerdict: DEGRADED — no git, no floor.")
        return 1
    gv = subprocess.run(["git", "--version"], capture_output=True, text=True)
    report("OK", gv.stdout.strip())
    for key in ("user.name", "user.email"):
        cfg = subprocess.run(["git", "config", key], cwd=root,
                             capture_output=True, text=True)
        if cfg.returncode == 0 and cfg.stdout.strip():
            report("OK", f"git {key} = {cfg.stdout.strip()}")
        else:
            report("WARN", f"git {key} unset — commits will fail until configured")

    # repo + hook (executed, not just resolved)
    inside = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                            capture_output=True, text=True)
    if inside.returncode != 0:
        report("FAIL", "not a git repository — `git init` first")
        floor_ok = False
    else:
        git_dir = (root / inside.stdout.strip()).resolve()
        hook = git_dir / "hooks" / "pre-commit"
        if not hook.is_file():
            report("FAIL", "pre-commit hook not installed — run `mdllm install-hook .`")
            floor_ok = False
        else:
            run = subprocess.run(["git", "hook", "run", "pre-commit"], cwd=root,
                                 capture_output=True, text=True)
            if "is not a git command" in (run.stderr or ""):
                report("WARN", "git < 2.36 — cannot execution-test the hook "
                               "(file present; make one commit to verify)")
            elif run.returncode == 0:
                report("OK", "pre-commit hook EXECUTES (validation currently clean)")
            elif run.returncode == 1 and "Validation" in (run.stdout or run.stderr or ""):
                report("OK", "pre-commit hook EXECUTES (validation currently has Errors "
                             "— it would block a commit, which is the point)")
            else:
                report("FAIL", f"pre-commit hook present but failed to execute "
                               f"(exit {run.returncode}) — resolution is not verification")
                floor_ok = False

    # framework / domain version drift
    sentinel = root / ".markdownllm"
    if sentinel.is_file():
        data = yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}
        local_v = str(data.get("version"))
        report("OK", f"framework root — sentinel version {local_v}")
        # Upstream leg (advisory, cached, non-blocking): compare the local
        # sentinel against the *already-fetched* upstream copy. No live fetch —
        # `git show` reads objects git already has (orchestration.md → upward
        # leg). Never flips floor_ok: this coordinates humans, not integrity.
        upstream_v = _upstream_sentinel_version(root)
        if upstream_v is None:
            report("--", "upstream version unknown — no fetched remote-tracking "
                         "copy of .markdownllm (run `git fetch`, then `mdllm doctor`)")
        elif upstream_v == local_v:
            report("OK", f"framework current with published upstream {upstream_v} "
                         f"(as of last fetch)")
        elif _version_lt(local_v, upstream_v):
            report("WARN", f"local framework is {local_v}; published upstream is "
                           f"{upstream_v} (as of last fetch) — consider pulling. "
                           f"Advisory only; does not block.")
        else:
            report("OK", f"local framework {local_v} is ahead of published upstream "
                         f"{upstream_v} (unpushed work) — as of last fetch")
    else:
        agents = root / "AGENTS.md"
        meta = None
        if agents.is_file():
            meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        fr = (meta or {}).get("framework_root")
        if fr:
            fsent = (root / fr / ".markdownllm").resolve()
            if fsent.is_file():
                fdata = yaml.safe_load(fsent.read_text(encoding="utf-8")) or {}
                fv, seen = str(fdata.get("version")), str(meta.get("framework_version_seen"))
                if fv == seen:
                    report("OK", f"domain current with framework {fv}")
                else:
                    report("WARN", f"domain last saw framework {seen}; framework is {fv} "
                                   f"— run the domain-refresh process")
            else:
                report("FAIL", f"framework_root `{fr}` does not resolve to a framework "
                               f"(.markdownllm not found at {fsent})")
                floor_ok = False
        else:
            report("--", "no .markdownllm and no framework_root in AGENTS.md — "
                         "neither a framework root nor a wired domain")

    print(f"## Doctor Report — {root}\n")
    print("\n".join(lines))
    print(f"\nVerdict: {'FLOOR ACTIVE' if floor_ok else 'DEGRADED'} — "
          + ("mechanical validation is enforced at the commit boundary."
             if floor_ok else
             "run `mdllm validate` manually before each commit, and say so."))
    return 0 if floor_ok else 1


def install_hook(root: Path) -> str:
    """Write the pre-commit validation hook into `root`'s git repo.
    Returns the mdllm path the hook will use (for reporting)."""
    git_dir = root / ".git"
    if not git_dir.is_dir():
        sys.exit(f"mdllm: {root} is not a git repository root")
    mdllm = Path(__file__).resolve()
    hook = git_dir / "hooks" / "pre-commit"
    hook.parent.mkdir(exist_ok=True)
    try:
        import os
        rel = Path(os.path.relpath(mdllm, root)).as_posix()
    except ValueError:  # e.g. different drives on Windows — no relative path exists
        rel = mdllm.as_posix()
    hook.write_text(HOOK_BODY.format(rel=rel), encoding="utf-8", newline="\n")
    try:
        hook.chmod(hook.stat().st_mode | 0o111)
    except OSError:
        pass  # Windows: executability is not a file-mode concern
    return rel


def cmd_install_hook(args) -> int:
    root = Path(args.path).resolve()
    rel = install_hook(root)
    print(f"installed {root / '.git' / 'hooks' / 'pre-commit'} (mdllm via {rel})")
    return 0


def cmd_scaffold(args) -> int:
    """The pre-domain-scaffold:isolate hard hook, mechanised. Owns the
    deterministic sequence of domain birth: directories, templates with
    mechanical placeholders substituted (name, dates, framework_root,
    framework_version_seen), a nested git repo, the outer repo's .gitignore
    isolation (added and committed BEFORE the domain's first commit, per the
    hard hook's ordering), the pre-commit hook, and the first commit.
    What remains semantic — thing types and vocabularies in _schema.yaml,
    skill content, AGENTS.md sections, the first real things — stays with
    the agent and the human, where it belongs."""
    import os
    fw_root = Path(__file__).resolve().parents[1]
    sentinel = fw_root / ".markdownllm"
    if not sentinel.is_file():
        sys.exit("mdllm: scaffold requires a framework checkout (.markdownllm not found)")
    fw_version = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {})
                     .get("version"))
    target = Path(args.path).resolve()
    name = target.name
    if not ID_RE.match(name):
        sys.exit(f"mdllm: domain folder name must be kebab-case (got {name!r})")
    if target.exists() and any(target.iterdir()):
        sys.exit(f"mdllm: {target} exists and is not empty")
    templates = fw_root / "templates"
    title = " ".join(w.capitalize() for w in name.split("-"))
    today = f"{dt.date.today():%Y-%m-%d}"
    try:
        rel_fw = Path(os.path.relpath(fw_root, target)).as_posix()
    except ValueError:
        rel_fw = fw_root.as_posix()

    def instantiate(text: str) -> str:
        text = (text.replace("[domain]", name)
                    .replace("[Domain Name]", title)
                    .replace("[Domain]", title)
                    .replace("[ISO-date]", today))
        text = re.sub(r"framework_root: \[[^\]]*\]", f"framework_root: {rel_fw}", text)
        text = re.sub(r"framework_version_seen: \[[^\]]*\]",
                      f"framework_version_seen: {fw_version}", text)
        return text

    (target / "things").mkdir(parents=True, exist_ok=True)
    (target / "skills").mkdir(exist_ok=True)
    written: list[str] = []
    (target / "AGENTS.md").write_text(
        instantiate((templates / "AGENTS.md.template").read_text(encoding="utf-8")),
        encoding="utf-8", newline="\n")
    written.append("AGENTS.md")
    (target / "things" / "_schema.yaml").write_text(
        (templates / "_schema.yaml.template").read_text(encoding="utf-8")
        .replace("[domain-name]", name),
        encoding="utf-8", newline="\n")
    written.append("things/_schema.yaml")
    for t in sorted(templates.glob("domain-*.skill.md.template")):
        out_name = t.name.replace("domain-", f"{name}-", 1)
        out_name = out_name[:-len(".template")]
        (target / "skills" / out_name).write_text(
            instantiate(t.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        written.append(f"skills/{out_name}")

    # Isolation, in the hard hook's order: (1) domain repo exists,
    # (2)+(3) outer repo ignores the domain BEFORE any domain commit,
    # (4) domain's first commit. Step 5 (remote) stays with the human.
    subprocess.run(["git", "init", "-q"], cwd=target, check=True)
    broken: list[str] = []  # any partial birth = exit 1; this hook's whole
    #                         point is that incomplete sequences cannot pass silently
    outer = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           cwd=target.parent, capture_output=True, text=True)
    isolated_in = None
    if outer.returncode == 0 and outer.stdout.strip():
        outer_root = Path(outer.stdout.strip())
        rel_t = Path(os.path.relpath(target, outer_root)).as_posix() + "/"
        gi = outer_root / ".gitignore"
        existing = gi.read_text(encoding="utf-8") if gi.is_file() else ""
        if rel_t.rstrip("/") not in {ln.strip().rstrip("/") for ln in existing.splitlines()}:
            gi.write_text(existing.rstrip("\n") + ("\n" if existing else "")
                          + f"{rel_t}\n", encoding="utf-8", newline="\n")
            subprocess.run(["git", "add", ".gitignore"], cwd=outer_root, check=True)
            commit = subprocess.run(
                ["git", "commit", "-q", "-m", f"chore: isolate domain {rel_t} (scaffold)"],
                cwd=outer_root, capture_output=True, text=True)
            if commit.returncode != 0:
                broken.append(f"outer .gitignore updated but commit failed in "
                              f"{outer_root}: {commit.stderr.strip() or commit.stdout.strip()}")
        isolated_in = outer_root

    hook_via = install_hook(target)
    subprocess.run(["git", "add", "-A"], cwd=target, check=True)
    first = subprocess.run(
        ["git", "commit", "-q", "-m", f"scaffold: {name} — framework v{fw_version}"],
        cwd=target, capture_output=True, text=True)
    if first.returncode != 0:
        broken.append(f"first domain commit failed — configure git user.name/"
                      f"user.email, then commit. "
                      f"({first.stderr.strip() or first.stdout.strip()})")

    print(f"## Scaffolded {name} — {target}\n")
    for w in written:
        print(f"  wrote {w}")
    print(f"  git repo initialised; pre-commit hook installed (mdllm via {hook_via})")
    if isolated_in:
        print(f"  isolated: {isolated_in / '.gitignore'} ignores the domain")
    if first.returncode == 0:
        print(f"  first commit made (framework_version_seen: {fw_version})")
    for b in broken:
        print(f"  FAIL  {b}")
    print("\nStill yours (and your agent's) — the semantic half:")
    print("  - AGENTS.md: name, description, principles, thing types")
    print("  - things/_schema.yaml: declare your types and status vocabularies")
    print("  - skills/: fill the four skill bodies with the domain's reasoning")
    print("  - things/: create the first real things")
    print("  - a remote, if the domain should have one")
    if broken:
        print("\nBIRTH SEQUENCE INCOMPLETE — the isolation invariant did not "
              "fully hold; fix the FAIL lines before using the domain.")
    return 1 if broken else 0


# ---------------------------------------------------------------- main


def main() -> int:
    # Windows consoles default to a legacy codepage; spec prose is UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(prog="mdllm", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    v = sub.add_parser("validate", help="Levels 1-3 mechanical validation")
    v.add_argument("path", nargs="?", default=".")
    v.add_argument("--quiet", action="store_true", help="only print on Errors")
    v.set_defaults(fn=cmd_validate)

    t = sub.add_parser("triggers", help="evaluate trigger conditions")
    t.add_argument("path", nargs="?", default=".")
    t.set_defaults(fn=cmd_triggers)

    i = sub.add_parser("index", help="check or rebuild derived indexes")
    i.add_argument("path", nargs="?", default=".")
    i.add_argument("action", choices=["check", "rebuild"])
    i.add_argument("--signal", choices=["triggers", "schema", "relationships", "provenance"])
    i.set_defaults(fn=cmd_index)

    pv = sub.add_parser("provenance", help="validate provenance chains (provenance.md)")
    pv.add_argument("path", nargs="?", default=".")
    pv.set_defaults(fn=cmd_provenance)

    k = sub.add_parser("tokens", help="measure spec token costs by tier")
    k.add_argument("path", nargs="?", default=".")
    k.set_defaults(fn=cmd_tokens)

    ev = sub.add_parser("eval", help="check a golden-scenario fixture against domain state")
    ev.add_argument("path", nargs="?", default=".")
    ev.add_argument("--fixture")
    ev.add_argument("--run", action="store_true",
                    help="Stage 2: seed workspace + headless agent + assert")
    ev.add_argument("--model", default="haiku")
    ev.add_argument("--trials", type=int, default=1)
    ev.add_argument("--bare", action="store_true",
                    help="no-framework condition: strip AGENTS.md/skills/schema")
    ev.add_argument("--report", action="store_true",
                    help="aggregate evals/runs/*/result.json into per-cell pass rates")
    ev.add_argument("--dry-run", action="store_true")
    ev.add_argument("--timeout", type=int, default=900,
                    help="seconds per trial (default 900)")
    ev.set_defaults(fn=cmd_eval)

    kn = sub.add_parser("kernel", help="generate kernel.md from spec kernel blocks")
    kn.add_argument("path", nargs="?", default=".")
    kn.add_argument("--check", action="store_true",
                    help="drift check: compare kernel.md against a fresh build")
    kn.set_defaults(fn=cmd_kernel)

    c = sub.add_parser("changelog", help="draft a CHANGELOG entry from commits")
    c.add_argument("path", nargs="?", default=".")
    c.add_argument("--since", help="ref to start from (e.g. a version tag)")
    c.set_defaults(fn=cmd_changelog)

    wl = sub.add_parser("worklog", help="generate WORKLOG.md from the commit stream")
    wl.add_argument("path", nargs="?", default=".")
    wl.add_argument("--write", action="store_true", help="write WORKLOG.md (else print)")
    wl.set_defaults(fn=cmd_worklog)

    rf = sub.add_parser("refresh", help="floor-only domain refresh: report version "
                                        "delta + unseen CHANGELOG; --seal bumps seen")
    rf.add_argument("path", nargs="?", default=".", help="the domain directory")
    rf.add_argument("--seal", action="store_true",
                    help="after adoption: bump framework_version_seen in domain AGENTS.md")
    rf.set_defaults(fn=cmd_refresh)

    d = sub.add_parser("doctor", help="probe the environment: floor prerequisites, "
                                      "hook execution, framework version drift")
    d.add_argument("path", nargs="?", default=".")
    d.set_defaults(fn=cmd_doctor)

    sc = sub.add_parser("scaffold", help="deterministic domain birth: templates, "
                                         "nested repo, .gitignore isolation, hook, "
                                         "first commit")
    sc.add_argument("path", help="folder to create (its name becomes the domain name)")
    sc.set_defaults(fn=cmd_scaffold)

    h = sub.add_parser("install-hook", help="install git pre-commit validation hook")
    h.add_argument("path", nargs="?", default=".")
    h.set_defaults(fn=cmd_install_hook)
    # Hook body is portable since v3.4.1: root/interpreter resolved at run time.

    args = p.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
