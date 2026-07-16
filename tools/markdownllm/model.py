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

# Universal frontmatter fields the floor itself reads and understands — the
# built-in half of the field vocabulary (the CORE_FIELDS<->known_fields split
# mirrors RESERVED_STATUSES<->_schema.yaml `types`: the tool owns the universal
# set; each domain owns its emergent extension). Every field listed here is
# read somewhere in the floor (level 1-2 structure, triggers, workflow state,
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
    # provenance (provenance.md) — `verified_by` names the human verifier on a
    # `verified: true` flip (ALCOA attributable; verified-flip-enforcement plan)
    "informed_by", "origin", "verified", "verified_by",
    # insight-lifecycle disposition (session-memory.md) — the orphan check READS
    # `disposition: keep-active` to honour a deliberately-kept standing/parked
    # insight, so these are tool-read and belong in CORE (unlike promoted_to,
    # which the tool only records).
    "disposition", "disposition_reason",
    # cross-domain interface (mcp-serve exposure — docs/plans/mcp-domain-server.md)
    "exposed",
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
