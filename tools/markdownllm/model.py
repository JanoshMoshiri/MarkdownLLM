"""The core model: what a thing is, mechanically.

Thing/Finding/Corpus, frontmatter parsing, corpus scanning, and the constants
that define the universal vocabulary (reserved statuses, core fields,
severities). Imports nothing from the rest of the package — everything else
imports inward to here.
"""

from __future__ import annotations

import re
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

# Terminal statuses for the framework-reserved types. The tool owns these
# vocabularies (RESERVED_STATUSES above), so it owns which of their values
# mean "settled" — a domain cannot redeclare a reserved type, and therefore
# cannot fix these itself.
RESERVED_TERMINAL = {
    "specification": {"stable", "deprecated"},
    "guide": {"stable", "deprecated"},
    "manifesto": {"stable", "deprecated"},
    "skill": {"stable", "deprecated"},
    "prompt": {"stable", "deprecated"},
    "workflow-definition": {"stable", "deprecated"},
    "workflow-run": {"completed", "abandoned"},
    "insight": {"promoted", "dismissed"},
    "conflict": {"resolved"},
    "retrospective": {"complete"},
    "decision": {"made", "superseded"},
    "index": {"live", "stale"},
    "continuity-brief": {"live"},
}


def terminal_statuses_for(schema: dict | None, typ: str | None) -> set[str]:
    """The statuses that mean "settled" for one type — not forward work.

    "Settled" is wider than "finished": it covers both end-of-life states
    (`superseded`, `retired`) and in-force steady states (a signed SOP at
    `approved-current`, a `record-pointer` at `live`). Neither is a loop the
    next session has to close, and counting them as such overstates the work
    outstanding — badly, in domains whose vocabulary is mostly steady-state.

    Resolution order:

    0. `RESERVED_TERMINAL`, for framework-reserved types — the tool owns those
       vocabularies, so a domain cannot override their settled set either.
    1. A domain's own declaration, per type, in `_schema.yaml`:

           types:
             review:
               statuses: [open, actioned, superseded]
               terminal_statuses: [actioned, superseded]

       A declaration REPLACES the universal set for that type rather than
       adding to it — explicit beats implicit, and a domain that has thought
       about its own lifecycle should not inherit surprises. Values outside
       the type's own `statuses` are ignored here; `validate` reports them.
    2. `TERMINAL_STATUSES`, the universal default.

    A type that declares nothing behaves exactly as it did before this
    existed, so no domain changes behaviour until it opts in.
    """
    typ = str(typ) if typ is not None else ""
    # Reserved types first: a domain cannot redeclare their vocabulary, so it
    # cannot redeclare which of their values are settled either. Checking the
    # schema first would let a domain silently override the tool here.
    if typ in RESERVED_TERMINAL:
        return set(RESERVED_TERMINAL[typ])
    if isinstance(schema, dict):
        types = schema.get("types")
        if isinstance(types, dict):
            spec = types.get(typ)
            if isinstance(spec, dict) and isinstance(spec.get("terminal_statuses"), list):
                declared = {str(s) for s in spec["terminal_statuses"]}
                vocab = spec.get("statuses")
                if isinstance(vocab, list):
                    declared &= {str(s) for s in vocab}
                return declared
    return set(TERMINAL_STATUSES)


def is_terminal(schema: dict | None, meta: dict | None) -> bool:
    """Has this thing reached a settled state for its own type?

    Every status check that means "is this still forward work?" goes through
    here, so the answer is consistent across orientation, triggers and
    cascade — and so a domain only has to declare its lifecycle once.
    """
    if not isinstance(meta, dict):
        return False
    status = str(meta.get("status", ""))
    return status in terminal_statuses_for(schema, meta.get("type"))

# Universal frontmatter fields the floor itself reads and understands — the
# built-in half of the field vocabulary (the CORE_FIELDS<->known_fields split
# mirrors RESERVED_STATUSES<->_schema.yaml `types`: the tool owns the universal
# set; each domain owns its emergent extension). Every field listed here is
# read somewhere in the floor (level 1-2 structure, triggers, workflow state,
# provenance) or written onto a generated index/kernel thing. A domain's
# `known_fields` in _schema.yaml extends this set; an in-use field in neither
# is a typo or an unregistered field, which the field-registration check
# (validate_level3) surfaces.
#
# Two admission criteria, and only two:
#   1. The tool learns to read a new structural field.
#   2. The FRAMEWORK ships the field into a domain as part of a reserved
#      type's contract — a domain must never be made to register the
#      framework's own vocabulary in its schema (that would be the framework
#      reaching into domain schemas: coupling, and a per-domain edit for every
#      framework change). The prompt contract below is this case.
# Registering the framework's own emergent fields by the same discipline
# domains follow.
CORE_FIELDS = {
    # identity & lifecycle (level 1)
    "id", "type", "status", "created", "due_date", "review_date",
    # relational graph (level 1-2 referential integrity)
    "linked_things", "dependencies", "blocks", "parent", "parties", "definition",
    # triggers & workflow-run cursor
    "triggers", "current_stage", "stages",
    # declared derivations (calc.py) — how a figure in this thing was reached,
    # evaluated by `mdllm calc` and re-checked by `validate`. Tool-read and
    # framework-shipped, so a domain never registers it (criterion 2, the same
    # ground as the ingestion triple and the prompt contract below).
    "computed",
    # provenance (provenance.md) — `verified_by` names the human verifier on a
    # `verified: true` flip (ALCOA attributable; verified-flip-enforcement plan);
    # the source triple is the cross-domain import pin `imports-check` reads
    "informed_by", "origin", "verified", "verified_by",
    "source_domain", "source_id", "source_commit",
    # ingestion triple (provenance.md → Ingestion Is Not Import) — the
    # outside-the-estate pin `imports-check` reports as `ingested` with the
    # clock. Tool-read since v3.23.0; unregistered until v3.24.0, so a domain
    # adopting the framework's own mandated fields was flagged for them.
    "source_system", "source_ref", "source_checked", "source_hash",
    # insight-lifecycle disposition (session-memory.md) — the orphan check READS
    # `disposition: keep-active` to honour a deliberately-kept standing/parked
    # insight, so these are tool-read and belong in CORE (unlike promoted_to,
    # which the tool only records).
    "disposition", "disposition_reason",
    # cross-domain interface (mcp-serve exposure — docs/plans/mcp-domain-server.md)
    "exposed",
    # generated-artifact frontmatter (index / kernel things)
    "index_of", "generated", "generated_from", "coverage", "framework_version",
    # reserved `type: prompt` contract (orchestration.md) — read by the agent,
    # not the tool, but SHIPPED by the framework into every domain that adopts
    # the reasoning prompts (criterion 2 above). Unregistered until v3.24.0,
    # which flagged a domain 24 times for the framework's own field names.
    "inputs", "outputs", "bound_to",
    # thing.md's Recommended vocabulary (criterion 2 again — "a domain must
    # never be made to register the framework's own vocabulary"). Unadmitted
    # until the ninth review (2026-08-09) caught the framework root itself
    # forced to register them in its own _schema.yaml.
    "priority", "tags", "confidence", "version",
}

DEFAULT_EXCLUDES = {".git", ".claude", ".codex", "node_modules", "templates", "examples",
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
    # YAML 1.1 parses a bare `on:` key as boolean True — so every trigger that
    # filled its `on:` field arrived at the floor with the field apparently
    # missing, and `tr.get("on")` readers silently saw None. Dependency
    # triggers could therefore NEVER fire, and relationship triggers were
    # reported as unfilled when they weren't (found 2026-08-01 by the
    # cohesiveness sensors' own self-test). Normalize once, at the single
    # entry point every reader shares.
    trigs = meta.get("triggers")
    if isinstance(trigs, list):
        for tr in trigs:
            if isinstance(tr, dict) and True in tr and "on" not in tr:
                tr["on"] = tr.pop(True)
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
