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
  touchpoints <id> [path]  Assimilate beat (change-reconciliation): the declared
                       inbound set + literal references for one thing — "what did
                       I just put at risk?". Human-invoked, never hooked; live.
  coherence [path]     Dark-region checks: generated-artifact (kernel/index)
                       freshness, foundational_specs<->filesystem, stale labels.
                       Corpus-general; framework-only checks switch on at a root
                       with .markdownllm. Runs in the pre-commit hook.
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

# Universal frontmatter fields the floor itself reads and understands — the
# built-in half of the field vocabulary (the CORE_FIELDS<->known_fields split
# mirrors RESERVED_STATUSES<->_schema.yaml `types`: the tool owns the universal
# set; each domain owns its emergent extension). Every field listed here is
# read somewhere in this file (level 1-2 structure, triggers, workflow state,
# provenance) or written onto a generated index/kernel thing. A domain's
# `known_fields` in _schema.yaml extends this set; an in-use field in neither
# is a typo or an unregistered field, which the field-registration check
# (validate_level3) surfaces. Add to this set only when the tool learns to read
# a new structural field — registering the framework's own emergent fields by
# the same discipline domains follow.
CORE_FIELDS = {
    # identity & lifecycle (level 1)
    "id", "type", "status", "created", "due_date", "review_date",
    # relational graph (level 1-2 referential integrity)
    "linked_things", "dependencies", "blocks", "parent", "parties", "definition",
    # triggers & workflow-run cursor
    "triggers", "current_stage", "stages",
    # provenance (provenance.md)
    "informed_by", "origin", "verified",
    # generated-artifact frontmatter (index / kernel things)
    "index_of", "generated", "generated_from", "coverage", "framework_version",
}

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

    # continuity-brief completeness (session-memory.md → The Session-Start
    # Staleness Check, Insight Lifecycle Management). An `active` insight or
    # `open` conflict the live brief does not name is orphaned from session
    # memory: it re-enters no future session and is invisible to the staleness
    # check, which walks only the brief's live ids. The two are a deliberate
    # pair ("the twin of the open-conflict check"). Info, corpus-general;
    # skipped when the corpus has no continuity brief (a fresh scaffold has
    # none yet — absence is not a defect). The brief names live things by id,
    # so an id-substring test over the brief body is the mechanical proxy.
    briefs = [t for t in corpus.things if str(t.meta.get("type")) == "continuity-brief"]
    if briefs:
        brief_text = "\n".join(t.body for t in briefs)
        for t in corpus.things:
            if not t.id or t.id not in known:
                continue
            typ, status = str(t.meta.get("type")), str(t.meta.get("status"))
            if typ == "insight" and status == "active" and t.id not in brief_text:
                f.append(Finding(SEV_INFO, t.id,
                         "active insight not in continuity brief — orphaned from "
                         "session memory; promote, dismiss, or list it live"))
            elif typ == "conflict" and status == "open" and t.id not in brief_text:
                f.append(Finding(SEV_INFO, t.id,
                         "open conflict not in continuity brief — add it as an "
                         "open thread so it returns next session"))
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

    # Field registration (opt-in, like `relations`): when a domain declares a
    # `known_fields` list, any top-level frontmatter key outside CORE_FIELDS ∪
    # known_fields ∪ the per-type required_fields is flagged. This closes the
    # silent-loss hole — a mis-keyed field (e.g. `relations:` typed where
    # `linked_things:` was meant) used to pass clean because the floor only
    # validated the *values* of known fields, never the *set of keys*. Warning,
    # not Error: the whole level-3 family is advisory (schema-gated), and the
    # bug was silence — Warning already ends it. A domain that declares no
    # known_fields gets no field check (no false alarms until it opts in). The
    # descriptive companion is `mdllm index <path> rebuild --signal schema`,
    # which enumerates every field in use — the bootstrap source for the list.
    known_fields = schema.get("known_fields")
    field_allow: set[str] | None = None
    if isinstance(known_fields, list):
        field_allow = set(CORE_FIELDS) | {str(k) for k in known_fields}
        for tdef in (schema.get("types") or {}).values():
            if isinstance(tdef, dict):
                field_allow |= {str(r) for r in (tdef.get("required_fields") or [])}

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
        if field_allow is not None:
            for key in t.meta:
                if str(key) not in field_allow:
                    f.append(Finding(SEV_WARNING, name,
                             f"field `{key}` not in CORE_FIELDS or declared "
                             f"`known_fields` — register it in _schema.yaml or fix "
                             f"the typo"))
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


# ---------------------------------------------------------------- touchpoints


def cmd_touchpoints(args) -> int:
    """The Assimilate beat (change-reconciliation.md) as a floor affordance.

    Given a thing id, report the COMPLETE declared inbound set — every
    `linked_things` edge, the singular structural pointers (`parent`,
    `definition`), and provenance pins (`informed_by`) that point AT it — plus
    the literal textual references a corpus grep reaches. One read answers "what
    did I just put at risk?" instead of a remembered three-step stitch.

    Two deliberate properties:
    (1) Human-invoked, never wired into the pre-commit hook. The Cue stays the
        driver's ("The Driver Names The Inflection"); this makes the blast
        radius impossible to not see, it does not decide a change is
        consequential or initiate the pass.
    (2) Computed fresh from the live corpus, not from the committed
        `relationships`/`provenance` indexes (which can drift) — assimilation
        must be complete AND current.
    The conceptual residue (a thing that reasons about the target without
    naming it) is the irreducible human walk; no mechanical pass reaches it."""
    root = Path(args.path).resolve()
    target = args.id
    corpus, _ = scan(root)
    if target not in corpus.by_id():
        print(f"mdllm: no thing with id `{target}` in {root}")
        return 1

    declared: list[str] = []
    declared_srcs: set[str] = set()
    for t in corpus.things:
        src = t.id or t.path.name
        if src == target:
            continue
        hits: list[str] = []
        for e in t.meta.get("linked_things") or []:
            if isinstance(e, dict) and e.get("id") == target:
                hits.append(f"(linked_things) relation `{e.get('relation')}`")
        for fieldname in ("parent", "definition"):
            if t.meta.get(fieldname) == target:
                hits.append(f"(structural) via `{fieldname}`")
        for pin in t.meta.get("informed_by") or []:
            if isinstance(pin, dict) and pin.get("id") == target:
                hits.append(f"(provenance) informed_by @{pin.get('commit', '?')}")
        if hits:
            declared_srcs.add(src)
            for h in hits:
                declared.append(f"{src} -> {target}  {h}")

    literal: list[str] = []
    for t in corpus.things:
        src = t.id or t.path.name
        if src == target or src in declared_srcs:
            continue
        if target in t.body:
            literal.append(src)

    print(f"## Touch points of `{target}` — {root}")
    print(f"({len(declared)} declared edge(s), {len(literal)} literal reference(s))\n")
    print("### Declared edges — the floor guarantees this set is complete")
    for d in sorted(declared) or ["- (none declares an edge to this thing)"]:
        print(d if d.startswith("- ") else f"- {d}")
    print("\n### Literal references — the id appears in another body (grep tier)")
    for src in sorted(literal):
        print(f"- {src}")
    if not literal:
        print("- (none)")
    print("\n### Conceptual residue — the human walk")
    print(f"Walk the set above: does each still hold given the change? Then ask "
          f"what reasons about `{target}` WITHOUT naming it — no mechanical pass "
          f"reaches that tier (change-reconciliation.md -> Walking the Dark Region).")
    if not declared and not literal:
        print(f"\nNothing points at `{target}`: a leaf or fresh thing carries no "
              f"consistency risk (change-reconciliation.md -> the premise).")
    return 0


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
    # Identity comes from the repo this runs in, not hard-coded framework values:
    # the WORKLOG is generated in the framework and in domain repos alike. Read the
    # local AGENTS.md frontmatter for the system name; fall back to the folder name.
    name = root.name
    agents = root / "AGENTS.md"
    if agents.is_file():
        ameta, _b, _e = parse_frontmatter(agents.read_text(encoding="utf-8"))
        if isinstance(ameta, dict) and isinstance(ameta.get("name"), str) and ameta["name"].strip():
            name = ameta["name"].strip()
    slug = re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-")
    worklog_id = f"{slug}-worklog" if slug else "worklog"
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

    # Auto-link to a local manifesto thing if the repo has one (the framework
    # does; most domains don't). Hard-coding a framework-only id here would
    # dangle — and fail validation as an unknown reference — in a domain repo.
    corpus, _ = scan(root)
    manifesto = next((t.id for t in corpus.things
                      if str(t.meta.get("type")) == "manifesto" and t.id), None)

    L = ["---", f"id: {worklog_id}", "type: artifact", "status: evolving",
         f"created: {commits[0][1]}"]
    if manifesto:
        L += ["linked_things:", f"  - id: {manifesto}", "    relation: documents"]
    L += ["---", "",
          f"# {name} Work Log", "",
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

    # Migration rail: regenerate the domain-kernel managed blocks so framework
    # improvements to the generated operative sections land as part of absorbing
    # the new version. Mechanical and idempotent — only the managed blocks change.
    present, _ = domain_kernel_status(text, build_domain_kernel_blocks(domain, meta or {}))
    if present:
        new_ag, written, _ = apply_domain_kernel(
            text, build_domain_kernel_blocks(domain, meta or {}))
        if new_ag != text:
            agents.write_text(new_ag, encoding="utf-8", newline="\n")
            text = new_ag  # keep --seal's regex operating on the fresh text
            print(f"\n  regenerated domain-kernel blocks: {', '.join(written)} "
                  f"(commit AGENTS.md)")
        else:
            print("\n  domain-kernel blocks already in sync.")

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
# Coherence: generated-artifact freshness (kernel/index drift) + spec-catalog
# integrity. Self-scoping — at a domain root (no .markdownllm) only the general
# checks run, so the same hook is correct in the framework and in every domain.
"$PY" "$MDLLM" coherence "$ROOT" --quiet || {{
  echo ""
  echo "mdllm: coherence Errors — a generated artifact (kernel/index) or the spec catalog is stale. Regenerate and re-commit, or --no-verify (discouraged)."
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

KERNEL_HEADER = (
    "# Framework Operative Kernel\n\n"
    "Generated by `mdllm kernel` from the `<!-- kernel -->` blocks in the\n"
    "foundational specs — the rules without the rationale. Load this at Tier 0\n"
    "instead of the full specs; load a full spec only when reasoning *about*\n"
    "the framework or when the kernel says to. Regenerate after any spec change.\n\n"
)


def _token_counter():
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        return lambda s: len(enc.encode(s))
    except ImportError:
        return lambda s: round(len(s) / 3.8)


def build_kernel(root: Path, specs: list[str], count) -> tuple[str, list[tuple], int, int]:
    """The deterministic kernel body (sans frontmatter) plus per-spec token
    detail. Shared by `kernel` (generate / --check) and `coherence` (drift
    check) so the two cannot disagree about what the kernel *should* contain —
    a single source for the very fact the drift check guards."""
    sections: list[str] = []
    detail: list[tuple] = []
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
        detail.append((name, count(body), count(text)))
    return KERNEL_HEADER + "\n".join(sections), detail, full_total, kernel_total


def cmd_kernel(args) -> int:
    """Generate kernel.md from <!-- kernel --> blocks in foundational specs."""
    root = Path(args.path).resolve()
    sentinel = root / ".markdownllm"
    if not sentinel.exists():
        sys.exit("mdllm: kernel requires a framework root (.markdownllm not found)")
    data = yaml.safe_load(sentinel.read_text(encoding="utf-8"))
    specs = data.get("foundational_specs") or []
    count = _token_counter()
    body, detail, full_total, kernel_total = build_kernel(root, specs, count)
    for name, kb, fb in detail:
        print(f"  {name:<40} {kb:>6,} / {fb:>6,} tokens")

    out = root / "kernel.md"

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
        f"coverage: {len(detail)}\n"
        f"framework_version: {data.get('version', 'unknown')}\n"
        "---\n\n"
        + body)
    out.write_text(content, encoding="utf-8")
    print(f"\nwrote kernel.md — {count(content):,} tokens "
          f"(kernel blocks {kernel_total:,} / full specs {full_total:,})")
    return 0


# ---------------------------------------------------------------- domain kernel
#
# The domain entry file (AGENTS.md) is the harness-loaded surface. Its operative
# sections are GENERATED into managed `<!-- generated:NAME -->` blocks so the
# session-start imperative is never buried and cannot accumulate residue across
# refreshes — the same drift-safe-by-construction property as derived indexes and
# kernel.md. The generator owns ONLY the managed blocks; frontmatter and authored
# identity outside them are preserved verbatim. Anchor vocabulary follows
# orchestration.md. Opt-in: a domain whose AGENTS.md has no managed blocks is left
# untouched and still boots by interpretation.

DOMAIN_KERNEL_BLOCKS = ("standing-truth", "session-start", "tier-routing",
                        "hooks", "floor")

_FRAMEWORK_HARD_HOOKS = (
    "- `post-write:commit` — commit every created/modified frontmatter `.md` to the "
    "owning repo before completing the response. Anchor: `git-fs` (validation via the "
    "pre-commit hook) + `interpretation` (the commit act itself).\n"
    "- `session-start:version-check` — performed in **Session Start** above. "
    "Anchor: `harness-session`.\n"
    "- `pre-domain-scaffold:isolate` — new domains are born via `mdllm scaffold`. "
    "Anchor: `git-fs`.")


def _gen_block_re(name: str) -> "re.Pattern":
    return re.compile(
        r"(<!--\s*generated:" + re.escape(name) + r"\s*-->[ \t]*\n)"
        r"(.*?)"
        r"(\n[ \t]*<!--\s*/generated:" + re.escape(name) + r"\s*-->)",
        re.DOTALL)


def _dk_standing_truth(domain: Path, meta: dict) -> str:
    return (
        "You predict the next move — the next token, sentence, or action — from the "
        "stream of what comes next. You cannot predict its *consequence* the same way. "
        "Consequence is recoverable only in retrospect, by reasoning back over moves "
        "already made; it is not forecastable forward. Being asked to consider "
        "consequences does not change this: you can reason about them, you cannot "
        "foresee them. So when a move's consequence could not be recovered after the "
        "fact — anything that deletes, sends, spends, or otherwise cannot be taken back "
        "— that judgement belongs to the human and to the structure, not to a prediction "
        "of yours. Reach for the structure; defer the irreversible. This is orientation, "
        "not a hook the floor enforces. Full reasoning: "
        "`{framework_root}/things/insights/consequence-is-recoverable-only-in-retrospect.md`.")


def _dk_session_start(domain: Path, meta: dict) -> str:
    return (
        "**Run this before responding to the user's first request — the live request "
        "will pull you toward itself; resist until these are done.**\n\n"
        "1. Load `{framework_root}/kernel.md` — the operative kernel (rules without "
        "rationale). The hard hooks it carries are always active.\n"
        "2. Load `continuity.md` if it exists — open threads, live insights, and pending "
        "decisions from the last session.\n"
        "3. **Version check** — `session-start:version-check` (anchor `harness-session`). "
        "Read `{framework_root}/.markdownllm` `version`; compare to `framework_version_seen` "
        "in this file's frontmatter. On mismatch: surface it, run "
        "`python {framework_root}/tools/mdllm.py validate .`, then offer "
        "`{framework_root}/domain-refresh.md`.\n"
        "4. **Orientation** — `session-orientation`: summarise what changed since last "
        "session (new things, status transitions) and run the scoped insight-staleness "
        "check (live insights in `continuity.md` × things changed since its `last_updated`).\n"
        "5. **Velocity** — `domain-velocity`, the counterpart to orientation: read `git log` "
        "over `things/` for what *should* have moved and hasn't (stalls, churn, untouched "
        "commitments). One line if the domain is healthy.\n"
        "6. **Triggers + attention** — `evaluate-triggers` then `surface-attention` (which "
        "consumes orientation's snapshot): scan things (or `things/_index/triggers.md` at "
        "scale) for fired conditions and order what needs the user.\n"
        "7. Then await intent.")


def _dk_tier_routing(domain: Path, meta: dict) -> str:
    t1 = TIERS["Tier 1 (full specs, load individually on demand)"]
    t2 = TIERS["Tier 2 (on demand)"]
    skills = (sorted(p.name for p in (domain / "skills").glob("*.skill.md"))
              if (domain / "skills").is_dir() else [])
    t1_specs = " · ".join(f"`{{framework_root}}/{n}`" for n in t1)
    skills_line = (" · ".join(f"`skills/{s}`" for s in skills)
                   if skills else "_(none yet)_")
    t2_specs = " · ".join(f"`{{framework_root}}/{n}`" for n in t2)
    return (
        "**Tier 0 — always:** `AGENTS.md` (this file) · `{framework_root}/kernel.md` · "
        "`continuity.md`\n\n"
        "**Tier 1 — load a full spec only when the kernel doesn't settle it:** "
        + t1_specs + "\n\n"
        "**Domain skills — load those relevant to session intent:** " + skills_line + "\n\n"
        "**Tier 2 — on demand:** " + t2_specs)


def _dk_hooks(domain: Path, meta: dict) -> str:
    parts = ["**Framework hard hooks (always active by config; anchor decides "
             "enforcement):**\n" + _FRAMEWORK_HARD_HOOKS]
    dh = meta.get("hard_hooks") or []
    if isinstance(dh, list):
        lines = []
        for h in dh:
            if not isinstance(h, dict):
                continue
            action = str(h.get("action", "")).rstrip()
            if action and not action.endswith((".", "!", "?")):
                action += "."
            lines.append(f"- `{h.get('hook', '?')}` — {action} "
                         f"Anchor: `{h.get('anchor', 'interpretation')}`.")
        if lines:
            parts.append("**Domain hard hooks:**\n" + "\n".join(lines))
    parts.append(
        "**Deliberate rituals — you invoke these; they never fire automatically:**\n"
        "- Session end → `session-end-continuity` (extract insights, detect conflicts, "
        "update `continuity.md`, regenerate WORKLOG). Invoke via `/end-session` or natural "
        "language *when you judge the session worth harvesting* — the operator decides "
        "when a session is worth it, not the floor.\n"
        "- Retrospective → `detect-conflicts` (scan) + `review-schema-coherence`, when "
        "writing a `type: retrospective`.")
    return "\n\n".join(parts)


def _dk_floor(domain: Path, meta: dict) -> str:
    return (
        "Structure (`id`/`type`/`status`/`created`), reference integrity, and schema "
        "conformance are owned by `python {framework_root}/tools/mdllm.py validate .` and "
        "enforced by the git pre-commit hook — never re-perform them by reasoning. Your "
        "validation duty is semantic only (metadata–narrative consistency, scope, "
        "staleness, duplicates); see `{framework_root}/validate.thing.md`.")


_DK_BUILDERS = {
    "standing-truth": _dk_standing_truth,
    "session-start": _dk_session_start,
    "tier-routing": _dk_tier_routing,
    "hooks": _dk_hooks,
    "floor": _dk_floor,
}


def build_domain_kernel_blocks(domain: Path, meta: dict) -> dict:
    """Canonical body for each managed block — the single source the generator
    writes and the drift check compares against, so the two cannot disagree."""
    return {name: _DK_BUILDERS[name](domain, meta) for name in DOMAIN_KERNEL_BLOCKS}


def domain_kernel_status(text: str, blocks: dict) -> tuple[list, list]:
    """(present_block_names, drifted_block_names) for an AGENTS.md text."""
    present, drifted = [], []
    for name, body in blocks.items():
        m = _gen_block_re(name).search(text)
        if not m:
            continue
        present.append(name)
        if m.group(2).strip() != body.strip():
            drifted.append(name)
    return present, drifted


def apply_domain_kernel(text: str, blocks: dict) -> tuple[str, list, list]:
    """Splice canonical bodies into the managed blocks. Returns (new_text,
    written, missing). Everything outside the blocks is preserved verbatim."""
    written, missing = [], []
    out = text
    for name, body in blocks.items():
        rx = _gen_block_re(name)
        if not rx.search(out):
            missing.append(name)
            continue
        out = rx.sub(lambda m: m.group(1) + body + m.group(3), out, count=1)
        written.append(name)
    return out, written, missing


def cmd_domain_kernel(args) -> int:
    """Generate/refresh the managed operative blocks in a domain's AGENTS.md."""
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    if not agents.is_file():
        sys.exit(f"mdllm: no AGENTS.md in {domain}")
    text = agents.read_text(encoding="utf-8")
    meta, _, err = parse_frontmatter(text)
    if err:
        sys.exit(f"mdllm: AGENTS.md frontmatter error — {err}")
    blocks = build_domain_kernel_blocks(domain, meta or {})

    if args.check:
        present, drifted = domain_kernel_status(text, blocks)
        if not present:
            print(f"domain-kernel: no managed blocks in {agents.name} — not kernel-shaped "
                  f"(opt-in; nothing to check)")
            return 0
        if drifted:
            print("domain-kernel: DRIFT — managed blocks differ from a fresh build: "
                  + ", ".join(drifted)
                  + f"\n  run `mdllm domain-kernel {args.path}` and commit the result")
            return 1
        print(f"domain-kernel: in sync ({len(present)} block(s))")
        return 0

    new_text, written, missing = apply_domain_kernel(text, blocks)
    if not written:
        print(f"domain-kernel: no `<!-- generated:NAME -->` blocks found in {agents.name}.\n"
              f"  Add the managed blocks (see templates/AGENTS.md.template) where you want "
              f"the generated operative sections, then re-run. Authored content outside the "
              f"blocks is always preserved.")
        return 1
    if new_text != text:
        agents.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"domain-kernel: wrote {len(written)} block(s) into {agents.name}: "
          + ", ".join(written))
    if missing:
        print("  blocks not present (skipped): " + ", ".join(missing))
    return 0


# ---------------------------------------------------------------- session start
#
# The mechanical half of the session-start ritual, emitted to stdout for a harness
# SessionStart hook to inject (Claude Code; Copilot in VS Code agent mode — both
# inject `additionalContext` at session start). This is the HARDENING for the
# `session-start:version-check` hook whose anchor is `harness-session`: a weak (or
# distracted) model receives the ritual at t=0 instead of having to recall it from
# a buried entry file. Optional — the AGENTS.md prose stays the interpretation
# floor where no adapter is installed. Read-only; safe on every session.


def _velocity_signal(domain: Path) -> str:
    things = domain / "things"
    if not things.is_dir():
        return "no `things/` directory yet."
    last = subprocess.run(["git", "log", "-1", "--format=%cr|%s", "--", "things"],
                          cwd=domain, capture_output=True, text=True)
    if last.returncode != 0 or not last.stdout.strip():
        return "no committed history over `things/` yet."
    when, _, subj = last.stdout.strip().partition("|")
    cnt = subprocess.run(["git", "rev-list", "--count", "--since=30.days", "HEAD",
                          "--", "things"], cwd=domain, capture_output=True, text=True)
    n = cnt.stdout.strip() if cnt.returncode == 0 else "?"
    return (f"last `things/` change {when} (\"{subj.strip()}\"); {n} commit(s) in 30d. "
            f"Read `git log -- things/` for the full picture.")


def cmd_session_start(args) -> int:
    domain = Path(args.path).resolve()
    agents = domain / "AGENTS.md"
    meta = {}
    if agents.is_file():
        meta, _, _ = parse_frontmatter(agents.read_text(encoding="utf-8"))
        meta = meta or {}

    out = ["# MarkdownLLM — Session Start (run before the user's first request)", "",
           "The live request will pull you toward itself; do these first, then await intent:",
           "1. Load `kernel.md` (operative kernel) and `continuity.md` if it exists.",
           "2. Act on the version + velocity status below.",
           "3. Evaluate triggers and surface what needs the user.", ""]

    fr = meta.get("framework_root")
    if (domain / ".markdownllm").is_file():
        # This IS a framework root (it carries the sentinel), not a downstream
        # domain — `framework_root: .` points at itself, so the domain
        # version-check does not apply.
        fv = str((yaml.safe_load((domain / ".markdownllm").read_text(encoding="utf-8"))
                  or {}).get("version"))
        out.append(f"- **Version:** framework root (v{fv}) — not a downstream domain; "
                   f"no refresh applies.")
    elif not fr:
        out.append("- **Version:** n/a — no `framework_root` in AGENTS.md.")
    else:
        sentinel = (domain / fr).resolve() / ".markdownllm"
        if not sentinel.is_file():
            out.append(f"- **Version:** unknown — `framework_root` `{fr}` has no .markdownllm.")
        else:
            fv = str((yaml.safe_load(sentinel.read_text(encoding="utf-8")) or {}).get("version"))
            seen = str(meta.get("framework_version_seen", ""))
            if not seen:
                out.append(f"- **Version: STALE** — framework v{fv}; domain has no "
                           f"`framework_version_seen`. Run `mdllm refresh .` and adopt.")
            elif version_tuple(seen) != version_tuple(fv):
                out.append(f"- **Version: MISMATCH** — framework v{fv}; domain last saw "
                           f"v{seen}. Validate the domain, then `mdllm refresh .` → adopt "
                           f"→ `--seal`.")
            else:
                out.append(f"- **Version: in sync** (framework v{fv}).")

    out.append(f"- **Velocity:** {_velocity_signal(domain)}")

    if agents.is_file():
        _, drifted = domain_kernel_status(
            agents.read_text(encoding="utf-8"),
            build_domain_kernel_blocks(domain, meta))
        if drifted:
            out.append(f"- **Domain kernel: DRIFT** in {', '.join(drifted)} — run "
                       f"`mdllm domain-kernel .` and commit.")

    print("\n".join(out))
    return 0


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
            # Body freshness: the installed hook is a copy frozen at install
            # time. A domain that sealed to a newer framework but never re-ran
            # install-hook keeps an older HOOK_BODY — the version sentinel then
            # claims an enforcement level the hook does not actually run (e.g.
            # `coherence` missing). Compare the copy against what install-hook
            # would write now. Advisory, not fatal: the hook still runs
            # `validate`, so the floor is active — just not current.
            import os
            try:
                rel = Path(os.path.relpath(Path(__file__).resolve(), root)).as_posix()
            except ValueError:
                rel = Path(__file__).resolve().as_posix()
            installed = hook.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            if installed != HOOK_BODY.format(rel=rel).replace("\r\n", "\n").strip():
                report("WARN", "pre-commit hook body is STALE vs the current mdllm "
                               "HOOK_BODY — re-run `mdllm install-hook` to pick up "
                               "newer checks (the sentinel may claim enforcement the "
                               "hook does not run)")
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

    # domain-kernel freshness + harness adapter (advisory; existence != currency)
    agents_p = root / "AGENTS.md"
    if agents_p.is_file():
        import json
        atext = agents_p.read_text(encoding="utf-8")
        ameta, _, _ = parse_frontmatter(atext)
        present, drifted = domain_kernel_status(
            atext, build_domain_kernel_blocks(root, ameta or {}))
        if not present:
            report("--", "AGENTS.md has no domain-kernel managed blocks "
                         "(opt-in; the entry file runs by interpretation)")
        elif drifted:
            report("WARN", f"domain-kernel blocks STALE ({', '.join(drifted)}) — "
                           f"run `mdllm domain-kernel .` and commit")
        else:
            report("OK", f"domain-kernel in sync ({len(present)} blocks)")
        has_ss = False
        settings = root / ".claude" / "settings.json"
        if settings.is_file():
            try:
                has_ss = "SessionStart" in (json.loads(
                    settings.read_text(encoding="utf-8")).get("hooks") or {})
            except (ValueError, OSError):
                has_ss = False
        report("OK" if has_ss else "--",
               "SessionStart adapter installed (.claude/settings.json)" if has_ss
               else "no SessionStart adapter — session-start runs by interpretation "
                    "(opt-in: adapters/claude-code.settings.example.json)")

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

    # Fill the domain-kernel managed blocks now that skills exist, so the entry
    # file is born in sync — otherwise the pre-commit coherence check would flag
    # the template's placeholder blocks as drift and block the first commit.
    ag = target / "AGENTS.md"
    ag_text = ag.read_text(encoding="utf-8")
    ag_meta, _, _ = parse_frontmatter(ag_text)
    ag_filled, _, _ = apply_domain_kernel(
        ag_text, build_domain_kernel_blocks(target, ag_meta or {}))
    ag.write_text(ag_filled, encoding="utf-8", newline="\n")

    # Deliberate-ritual slash commands (inert until the operator invokes them) —
    # Claude Code `.claude/commands/` and Copilot `.github/prompts/`. The
    # auto-firing SessionStart/PostToolUse adapter stays opt-in (hint printed below).
    cmd_dir = target / ".claude" / "commands"
    prm_dir = target / ".github" / "prompts"
    if (templates / "commands").is_dir():
        cmd_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted((templates / "commands").glob("*.md")):
            (cmd_dir / src.name).write_text(
                instantiate(src.read_text(encoding="utf-8")),
                encoding="utf-8", newline="\n")
            written.append(f".claude/commands/{src.name}")
    if (templates / "copilot-prompts").is_dir():
        prm_dir.mkdir(parents=True, exist_ok=True)
        for src in sorted((templates / "copilot-prompts").glob("*.prompt.md")):
            (prm_dir / src.name).write_text(
                instantiate(src.read_text(encoding="utf-8")),
                encoding="utf-8", newline="\n")
            written.append(f".github/prompts/{src.name}")

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
    print("  - optional hardening: copy adapters/claude-code.settings.example.json → "
          ".claude/settings.json to fire session-start + post-write validation "
          "automatically (Claude Code / VS Code Copilot agent mode). Opt-in — the "
          "domain kernel already drives these by interpretation.")
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

    tp = sub.add_parser("touchpoints", help="Assimilate beat: what a thing's change "
                                            "disturbs (declared edges + literal refs)")
    tp.add_argument("id", help="the thing id to assimilate around")
    tp.add_argument("path", nargs="?", default=".")
    tp.set_defaults(fn=cmd_touchpoints)

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

    dk = sub.add_parser("domain-kernel",
                        help="generate/refresh a domain AGENTS.md's managed operative blocks")
    dk.add_argument("path", nargs="?", default=".")
    dk.add_argument("--check", action="store_true",
                    help="drift check: compare managed blocks against a fresh build")
    dk.set_defaults(fn=cmd_domain_kernel)

    ss = sub.add_parser("session-start",
                        help="emit the session-start ritual (version + velocity) for a "
                             "harness SessionStart hook to inject")
    ss.add_argument("path", nargs="?", default=".")
    ss.set_defaults(fn=cmd_session_start)

    co = sub.add_parser("coherence", help="dark-region checks: generated-artifact "
                                          "freshness, catalog/filesystem, stale labels")
    co.add_argument("path", nargs="?", default=".")
    co.add_argument("--window", type=int, default=15,
                    help="stable-staleness lookback in commits (default 15)")
    co.add_argument("--quiet", action="store_true", help="only print on Errors")
    co.set_defaults(fn=cmd_coherence)

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
