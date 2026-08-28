"""Operating-layer vocabulary drift — a skill that instructs what the schema
does not declare.

Layer 3 is audited at every commit; Layers 1 and 2 — the entry file and the
skills — have never been. They degrade in a way no change-time walk can catch:
the skills drift by *standing still* while practice moves around them, and
practice is not a thing with edges, so no blast radius ever includes a skill
(`the-operating-layer-has-no-quality-loop`).

Most of that drift is judgement. **A slice of it is not**, and this module
owns exactly that slice: a skill that names a thing type, a status, or a
frontmatter field the corpus does not declare is not a matter of opinion —
it is an instruction whose product the floor rejects at the commit boundary.
Five such defects were found by hand across three domains on 2026-08-28; the
sharpest was a specification skill giving `income-record` four statuses with
**zero overlap** with the schema's two, so every value a session could have
written from that description would have been refused. It had stood for two
and a half months and forty-four `things/` commits, unnoticed because nothing
read the two files against each other.

**Why this needs no suppression list** (`mechanical-coherence-checks-backlog`'s
standing gate, and the reason the retired-vocabulary check was reverted). The
check is keyed to the same builder it polices: `_schema.yaml` is what the
floor enforces on every thing, the tool's reserved sets are the tool's own,
and the skill is *prose about them*. There is no allow-list, no per-file
exemption, and no way to quiet a finding except to make the two agree —
correct the prose, or declare the vocabulary. It therefore cannot disagree
with truth: when the schema moves, the check's answer moves with it.

**Why it is scoped by what it reads, not by what it found.** Four positions
count as an instruction, and nothing else does: a frontmatter template inside
a fenced block; a heading naming a type; a list step or table cell naming
one; and a `status` vocabulary line or **Key fields** list under a type
heading. Running prose that *mentions* a type is never a finding, and neither
is anything inside a parenthetical — "new types (e.g. `type: migration-plan`)
emerge from real need" is correct writing about a type that need not exist,
and a check that fired on it would be teaching the operator to ignore it
(`a-check-that-always-fires-teaches-the-operator-to-ignore-it`). Missing a
case is the cheaper error here, and it is taken deliberately at each step —
a status list stops at the first thing that is not an alternative, a fields
list ends at the next paragraph, and a placeholder value is read as nothing.

Severity is **Warning** throughout, for one class and one reason. This is the
prose sibling of the schema-gated field-registration check, which is itself
advisory: the mechanical twin fires Warning on the *thing*, and prose about a
thing should not be adjudicated more harshly than the thing. It is never
"may be intentional" (so not Info), and blocking every commit in a live
domain on a prose defect would wedge unrelated work for a fix that is not
urgent (so not Error).

Population is scoped by who can perform the remedy
(`an-advisory-is-scoped-by-who-can-perform-its-remedy`): the entry file and
every non-`deprecated` skill. `draft` stays IN — a draft skill is loaded at
session start like any other, and the archetype instance was `draft` while
being read daily. `deprecated` is out: its instructions are withdrawn, and
rewriting a retired file is not a remedy anyone would perform. Generated
managed blocks are stripped before reading, for the same reason — a finding
inside a generator's output names a remedy the operator cannot perform.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .model import (Corpus, Finding, SEV_WARNING, Thing, declared_field_names,
                    declared_type_names, valid_statuses_for)

# A managed block is the generator's, not the author's. Stripped before
# extraction so the check can never name a remedy the operator cannot perform.
_GENERATED_BLOCK = re.compile(
    r"<!--\s*generated:[^>]*-->.*?<!--\s*/generated:[^>]*-->", re.DOTALL)

# Vocabulary tokens: kebab-case for types and statuses, snake_case for fields.
_VALUE = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_FIELD = r"[a-z][a-z0-9]*(?:_[a-z0-9]+)*"

_FENCE = re.compile(r"^\s*(?:```+|~~~+)(.*)$")
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s")
_BULLET = re.compile(r"^(\s{0,3})(?:[-*+]|\d+[.)])\s+(.*)$")
_TABLE_CELL = re.compile(r"^\s*\|\s*`(type|status):\s*(" + _VALUE + r")`\s*\|")
_INLINE_TYPE = re.compile(r"`(type|status):\s*(" + _VALUE + r")`")
_LEADS_WITH = re.compile(r"^`(type|status):\s*(" + _VALUE + r")`")
_YAML_KEY = re.compile(r"^(" + _FIELD + r"):(.*)$")
_YAML_DELIM = re.compile(r"^-{3,}\s*$")

# `- `status` — `open` | `figures-ready` | `submitted``: the per-type
# vocabulary line, and the shape all four 2026-08-28 status defects wore.
_STATUS_LIST = re.compile(r"^`status`\s*[-—–:]*\s*(.*)$")
_ALTERNATIVE = re.compile(r"^\s*`(" + _VALUE + r")`\s*(\([^)]*\))?\s*")
_ALTERNATIVE_SEP = re.compile(r"^\|\s*")

# A parenthetical illustrates; it does not instruct. `(e.g., `type: x`)` is
# correct prose about a type that need not exist, and the one estate mention
# that would otherwise have been a false positive sat inside exactly that.
_PARENTHETICAL = re.compile(r"\([^()]*\)")

# A fields list is read only under its own heading — `**Key fields:**` and
# `Required fields:` are the estate's two forms. Outside such a section a
# leading backticked identifier is as likely to be a code symbol as a field.
_FIELDS_CUE = re.compile(
    r"^\**\s*(?:key|required|core|custom|optional|domain[- ]specific)?\s*"
    r"fields\b[^\n]{0,24}$", re.IGNORECASE)
# `- `period_start`, `period_end` — The quarter`: the leading run only.
_LEADING_FIELDS = re.compile(
    r"^((?:`" + _FIELD + r"`)(?:\s*(?:,|/|and)\s*`" + _FIELD + r"`)*)")
_ONE_FIELD = re.compile(r"`(" + _FIELD + r")`")


@dataclass(frozen=True)
class VocabularyUse:
    """One position where the operating layer instructs a vocabulary item."""
    kind: str                    # "type" | "status" | "field"
    value: str
    type_context: str | None     # the type a status was declared under


def _strip_generated(text: str) -> str:
    return _GENERATED_BLOCK.sub("", text)


def _fenced_frontmatter_uses(lines: list[str]) -> list[VocabularyUse]:
    """Frontmatter templates inside fenced blocks — the literal instruction.

    A session writing a new thing copies this block, so its `type:`, its
    `status:`, and its top-level keys are precisely what the domain will
    carry. A fenced block only counts when it contains a `---` delimiter:
    that is what separates a frontmatter template from an ordinary YAML
    example (a bindings block, a schema excerpt) whose keys are not
    frontmatter at all.
    """
    uses: list[VocabularyUse] = []
    fence: str | None = None
    block: list[str] = []
    for raw in lines + ["```"]:
        opener = _FENCE.match(raw)
        if fence is None:
            if opener:
                fence = raw.strip()[:3]
                block = []
            continue
        if opener and raw.strip().startswith(fence):
            uses.extend(_frontmatter_block_uses(block))
            fence, block = None, []
            continue
        block.append(raw)
    return uses


def _frontmatter_block_uses(block: list[str]) -> list[VocabularyUse]:
    bounds = [i for i, ln in enumerate(block) if _YAML_DELIM.match(ln)]
    if not bounds:
        return []
    start = bounds[0] + 1
    end = bounds[1] if len(bounds) > 1 else len(block)
    keys: dict[str, str] = {}
    order: list[str] = []
    for ln in block[start:end]:
        m = _YAML_KEY.match(ln)
        if not m:
            continue                     # nested key, comment, or list item
        if m.group(1) not in keys:
            order.append(m.group(1))
        keys[m.group(1)] = m.group(2).strip()
    if not order:
        return []
    uses: list[VocabularyUse] = []
    typ = _scalar(keys.get("type"))
    if typ:
        uses.append(VocabularyUse("type", typ, None))
    for status in _scalars(keys.get("status")):
        uses.append(VocabularyUse("status", status, typ))
    uses.extend(VocabularyUse("field", key, None)
                for key in order if key not in ("type", "status"))
    return uses


def _scalar(value: str | None) -> str | None:
    """A clean vocabulary token, or None for a placeholder or an expression.

    Template values are routinely `[thing type]` or `draft|active`; neither
    names one item, and guessing at them is how a check starts inventing.
    """
    values = _scalars(value)
    return values[0] if len(values) == 1 else None


def _scalars(value: str | None) -> list[str]:
    if value is None or "[" in value or "<" in value:
        return []
    parts = [p.strip() for p in value.split("|")]
    return parts if all(re.fullmatch(_VALUE, p or "") for p in parts) else []


def _prose_uses(lines: list[str]) -> list[VocabularyUse]:
    """Headings, list steps, table cells, and the vocabulary lists beneath them.

    A heading naming a type opens a *governing* context that the status and
    fields lists under it are read against, and the next heading closes it.
    A list step that names its own type governs itself, so a status beside it
    is never adjudicated against the section's type instead of its own.
    """
    uses: list[VocabularyUse] = []
    governing: str | None = None         # nearest heading naming a type
    in_fields = False
    fence: str | None = None
    for raw in lines:
        opener = _FENCE.match(raw)
        if fence is not None:
            if opener and raw.strip().startswith(fence):
                fence = None
            continue                     # fenced content is the block reader's
        if opener:
            fence = raw.strip()[:3]
            continue
        line = raw.rstrip()
        bullet = _BULLET.match(line)
        if _HEADING.match(line):
            governing = None
            in_fields = False
            for kind, value in _INLINE_TYPE.findall(line):
                uses.append(VocabularyUse(kind, value, None))
                if kind == "type":
                    governing = value
            continue
        if _FIELDS_CUE.match(line.strip().rstrip(":*")) and line.strip():
            in_fields = True
            continue
        cell = _TABLE_CELL.match(line)
        if cell:
            uses.append(VocabularyUse(cell.group(1), cell.group(2), None))
            continue
        if bullet is None:
            # A blank line does not end a list; any other unindented prose does.
            if line.strip() and not line.startswith((" ", "\t")):
                in_fields = False
            continue
        content = bullet.group(2).strip()
        indented = len(bullet.group(1)) > 0
        lead = _LEADS_WITH.match(content)
        if lead:
            uses.append(VocabularyUse(lead.group(1), lead.group(2), governing))
            continue
        # A list step is an instruction even mid-sentence: "1. Create a
        # `type: product` thing" is what a session enacts. The one exclusion
        # is a parenthetical, which illustrates rather than instructs.
        named = _INLINE_TYPE.findall(_PARENTHETICAL.sub("", content))
        local = next((v for k, v in named if k == "type"), governing)
        for kind, value in named:
            uses.append(VocabularyUse(kind, value,
                                      local if kind == "status" else None))
        status_list = _STATUS_LIST.match(content)
        if status_list and governing:
            uses.extend(VocabularyUse("status", value, governing)
                        for value in _alternatives(status_list.group(1)))
            continue
        if in_fields and not indented:
            uses.extend(VocabularyUse("field", name, None)
                        for name in _leading_fields(content))
    return uses


def _alternatives(tail: str) -> list[str]:
    """The leading run of `` `a` | `b` (≤7 days) | `c` `` — and nothing after it.

    Scanned rather than matched whole, for two reasons the live corpus
    supplies. A value may carry a parenthetical gloss and the run continues
    past it; and the line routinely continues into prose ("**Exactly three.**
    The urgency bands…"), where reading backticks would give a status list
    values nobody declared. The scan stops at the first thing that is not an
    alternative, and never looks inside a gloss.
    """
    rest = tail.strip()
    values: list[str] = []
    while True:
        m = _ALTERNATIVE.match(rest)
        if not m:
            return values
        values.append(m.group(1))
        rest = rest[m.end():]
        sep = _ALTERNATIVE_SEP.match(rest)
        if not sep:
            return values
        rest = rest[sep.end():]


def _leading_fields(content: str) -> list[str]:
    run = _LEADING_FIELDS.match(content)
    return _ONE_FIELD.findall(run.group(1)) if run else []


def vocabulary_uses(text: str) -> list[VocabularyUse]:
    """Every vocabulary item this surface instructs, deduplicated in order."""
    lines = _strip_generated(text).splitlines()
    seen: set[VocabularyUse] = set()
    ordered: list[VocabularyUse] = []
    for use in _fenced_frontmatter_uses(lines) + _prose_uses(lines):
        if use not in seen:
            seen.add(use)
            ordered.append(use)
    return ordered


def _undeclared(uses: list[VocabularyUse], schema: dict | None
                ) -> list[tuple[str, str | None, list[str]]]:
    """(kind, type_context, values) for everything the schema does not admit.

    Each leg stays silent where the corpus declares no authority: no types
    declared, no `known_fields` registered, or a type whose status vocabulary
    is the universal default. That is "could not look", and a check that
    cannot look must say nothing rather than invent a finding
    (`a-check-run-where-it-cannot-see-mints-a-false-finding`).
    """
    types = declared_type_names(schema)
    fields = declared_field_names(schema)
    buckets: dict[tuple[str, str | None], list[str]] = {}
    for use in uses:
        if use.kind == "type":
            if types is None or use.value in types:
                continue
            key: tuple[str, str | None] = ("type", None)
        elif use.kind == "status":
            if not use.type_context:
                continue                 # no type, no vocabulary to check
            allowed, declared = valid_statuses_for(use.type_context, schema)
            if not declared or use.value in (allowed or []):
                continue
            key = ("status", use.type_context)
        else:
            if fields is None or use.value in fields:
                continue
            key = ("field", None)
        bucket = buckets.setdefault(key, [])
        if use.value not in bucket:
            bucket.append(use.value)
    # Sorted values, insertion-ordered buckets: the same surface reports the
    # same line every run, and two surfaces carrying the same defect say it
    # the same way.
    return [(kind, ctx, sorted(values))
            for (kind, ctx), values in buckets.items()]


_REMEDY = {
    "type": ("instructs {n} thing type{s} `_schema.yaml` does not declare",
             "a session following this writes things whose type the floor does "
             "not recognise; correct the prose, or declare the type"),
    "status": ("instructs {n} status value{s} outside the declared vocabulary "
               "for type `{context}`",
               "each is refused at the commit boundary; the schema is the "
               "authority and does not move to protect a description"),
    "field": ("instructs {n} frontmatter field name{s} registered nowhere",
              "writing any of them fires an unregistered-field Warning; "
              "correct the names, or register them in `known_fields`"),
}


def _surface_findings(name: str, text: str, schema: dict | None) -> list[Finding]:
    findings: list[Finding] = []
    for kind, context, values in _undeclared(vocabulary_uses(text), schema):
        what, why = _REMEDY[kind]
        shown = ", ".join(f"`{v}`" for v in values[:4])
        more = ", …" if len(values) > 4 else ""
        findings.append(Finding(
            SEV_WARNING, name,
            what.format(n=len(values), s="" if len(values) == 1 else "s",
                        context=context)
            + f" ({shown}{more}) — {why}"))
    return findings


def _is_operating_layer(thing: Thing, root: Path) -> bool:
    """A skill by declaration or by the layout the tool itself scaffolds.

    `type: skill` alone is not enough: the estate's *specification* skills
    carry `type: specification`, and two of the 2026-08-28 defects lived in
    one of those. `mdllm scaffold` writes `skills/<name>.skill.md` and
    `mdllm domain-kernel` routes exactly that shape, so the layout is the
    tool's own — same-builder, not a list anyone maintains.
    """
    if str(thing.meta.get("type")) == "skill":
        return True
    try:
        relative = thing.path.relative_to(root)
    except ValueError:
        return False
    return "skills" in relative.parts[:-1] or relative.name.endswith(".skill.md")


def skill_vocabulary_findings(corpus: Corpus,
                              entry_text: str | None) -> list[Finding]:
    """Vocabulary the operating layer instructs but the corpus never declared.

    Pure over the corpus and the entry file's text — no filesystem, no git, no
    repository view — so the caller's chosen candidate is the only thing read.
    """
    findings: list[Finding] = []
    for thing in corpus.things:
        if not _is_operating_layer(thing, corpus.root):
            continue
        if str(thing.meta.get("status")) == "deprecated":
            continue
        name = thing.id or thing.path.name
        findings.extend(_surface_findings(name, thing.body, corpus.schema))
    if entry_text is not None:
        findings.extend(_surface_findings("AGENTS.md", entry_text,
                                          corpus.schema))
    return findings
