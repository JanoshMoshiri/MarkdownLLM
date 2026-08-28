"""Canonical registry for thing-to-thing structural references.

The same relationship vocabulary feeds referential validation, reverse
indexes, change touchpoints, cue fan-in, schema field ownership, and MCP
egress privacy.  A new structural field belongs here first; consumers iterate
the registry instead of maintaining their own almost-equal lists.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ReferenceShape(str, Enum):
    LINK_OBJECTS = "link-objects"
    ID_LIST = "id-list"
    ID_SCALAR = "id-scalar"
    TRIGGER_WATCH = "trigger-watch"
    PIN_OBJECTS = "pin-objects"


@dataclass(frozen=True)
class ReferenceField:
    field: str
    shape: ReferenceShape
    cardinality: str
    validate_local_target: bool = True
    reverse_index: bool = True
    index_signal: str = "relationships"
    egress_private: bool = True
    cue_relevant: bool = True


@dataclass(frozen=True)
class StructuralReference:
    field: str
    target: str
    relation: str
    commit: str | None = None


REFERENCE_FIELDS: tuple[ReferenceField, ...] = (
    ReferenceField("linked_things", ReferenceShape.LINK_OBJECTS, "many"),
    ReferenceField("dependencies", ReferenceShape.ID_LIST, "many"),
    ReferenceField("blocks", ReferenceShape.ID_LIST, "many"),
    ReferenceField("parent", ReferenceShape.ID_SCALAR, "zero-or-one"),
    ReferenceField("parties", ReferenceShape.ID_LIST, "many"),
    ReferenceField("definition", ReferenceShape.ID_SCALAR, "zero-or-one"),
    ReferenceField("triggers", ReferenceShape.TRIGGER_WATCH, "many"),
    # A provenance pin may legitimately refer to an input that now exists only
    # at its pinned commit, so provenance owns existence semantics.  It still
    # participates in reverse recall, cues, and egress privacy.
    ReferenceField("informed_by", ReferenceShape.PIN_OBJECTS, "many",
                   validate_local_target=False, index_signal="provenance"),
)

REFERENCE_BY_FIELD = {spec.field: spec for spec in REFERENCE_FIELDS}


# ------------------------------------------------------- commit pins
# A structural pin is a *transcribed* identifier: a human copies a SHA from
# one terminal into another file, and nothing in reading it back can tell a
# correct pin from a wrong one
# (`a-transcribed-identifier-is-unverifiable-by-reading`).  The set of fields
# that carry such a pin is stated ONCE here so the floor's pin-resolution
# check cannot drift from the fields that actually exist — the same
# state-once-and-derive discipline the reference registry above exists for.


class CommitPinScope(str, Enum):
    """Which repository a pin names a commit in.

    The distinction is load-bearing, not decorative: resolving a FOREIGN pin
    against the local object database reports "missing" for a *correct* pin
    and mints a false finding
    (`a-check-run-where-it-cannot-see-mints-a-false-finding`), and its remedy
    written as an imperative — "re-pin to a local commit" — is one no honest
    author could perform.
    """

    LOCAL = "local"
    FOREIGN = "foreign"


class CommitPinShape(str, Enum):
    #: A scalar frontmatter key whose value is the pin (``definition_commit``).
    SCALAR = "commit-scalar"
    #: The ``commit`` key of each entry of a PIN_OBJECTS reference field.
    PIN_OBJECT = "pin-object-commit"


@dataclass(frozen=True)
class CommitPinField:
    field: str
    shape: CommitPinShape
    scope: CommitPinScope
    #: Who resolves this pin — named so a reader can see the whole set and
    #: which part of the floor owns each one, rather than inferring it from
    #: an absence.
    resolved_by: str
    #: True when the pin is already resolved by another floor check; the
    #: commit-boundary check skips it rather than reporting it twice.
    resolved_elsewhere: bool = False


@dataclass(frozen=True)
class CommitPin:
    #: Display label including any index, e.g. ``informed_by[0].commit``.
    field: str
    pin: str
    scope: CommitPinScope
    resolved_elsewhere: bool


COMMIT_PIN_FIELDS: tuple[CommitPinField, ...] = (
    CommitPinField("informed_by", CommitPinShape.PIN_OBJECT,
                   CommitPinScope.LOCAL,
                   "validate (structural-pin resolution)"),
    # Resolved — with stage membership read at the pinned revision — by the
    # workflow revision binding in validation.py.  Registered here so the set
    # is complete; excluded from the boundary check so one wrong pin cannot
    # produce two Errors saying the same thing.
    CommitPinField("definition_commit", CommitPinShape.SCALAR,
                   CommitPinScope.LOCAL,
                   "validate (workflow revision binding)",
                   resolved_elsewhere=True),
    # The cross-domain reference triple pins a commit in the SOURCE domain's
    # repository (`source_domain`), which the consuming repository need not
    # hold at all.  `mdllm imports-check` resolves it where the source clone
    # is reachable and buckets it as could-not-check where it is not.
    CommitPinField("source_commit", CommitPinShape.SCALAR,
                   CommitPinScope.FOREIGN, "mdllm imports-check"),
)

COMMIT_PIN_BY_FIELD = {spec.field: spec for spec in COMMIT_PIN_FIELDS}


def structural_field_names() -> set[str]:
    return set(REFERENCE_BY_FIELD)


def egress_private_fields() -> set[str]:
    return {s.field for s in REFERENCE_FIELDS if s.egress_private}


def commit_pin_field_names() -> set[str]:
    return set(COMMIT_PIN_BY_FIELD)


def iter_commit_pins(meta: dict) -> Iterable[CommitPin]:
    """Yield every declared commit pin in ``meta``, with its scope.

    Extraction only: this decides nothing about resolvability, and — like
    :func:`iter_structural_references` — is total, never raising on a
    malformed edit.  A pin whose value is neither a string nor an integer is
    omitted; its shape is reported by the checks that own field shape.  (The
    integer arm is not defensive padding: an unquoted all-digit short SHA is
    valid YAML for an int, and roughly one abbreviation in sixteen is all
    digits.)
    """

    if not isinstance(meta, dict):
        return
    for spec in COMMIT_PIN_FIELDS:
        value = meta.get(spec.field)
        if spec.shape is CommitPinShape.SCALAR:
            if isinstance(value, (str, int)) and not isinstance(value, bool):
                yield CommitPin(spec.field, str(value), spec.scope,
                                spec.resolved_elsewhere)
        elif spec.shape is CommitPinShape.PIN_OBJECT:
            if not isinstance(value, list):
                continue
            for i, entry in enumerate(value):
                if not isinstance(entry, dict):
                    continue
                pin = entry.get("commit")
                if isinstance(pin, (str, int)) and not isinstance(pin, bool):
                    yield CommitPin(f"{spec.field}[{i}].commit", str(pin),
                                    spec.scope, spec.resolved_elsewhere)


def iter_structural_references(
    meta: dict,
    *,
    validation_only: bool = False,
    reverse_only: bool = False,
    cue_only: bool = False,
) -> Iterable[StructuralReference]:
    """Yield every well-shaped thing id declared by ``meta``.

    Shape errors are intentionally omitted here and reported by
    :func:`structural_shape_errors`; extraction is total and never throws on a
    malformed edit.
    """

    if not isinstance(meta, dict):
        return
    for spec in REFERENCE_FIELDS:
        if validation_only and not spec.validate_local_target:
            continue
        if reverse_only and not spec.reverse_index:
            continue
        if cue_only and not spec.cue_relevant:
            continue
        value = meta.get(spec.field)
        if spec.shape is ReferenceShape.LINK_OBJECTS:
            if not isinstance(value, list):
                continue
            for entry in value:
                if isinstance(entry, dict) and isinstance(entry.get("id"), str):
                    yield StructuralReference(
                        spec.field, entry["id"], str(entry.get("relation", "related")))
        elif spec.shape is ReferenceShape.ID_LIST:
            if not isinstance(value, list):
                continue
            for target in value:
                if isinstance(target, str):
                    yield StructuralReference(spec.field, target, spec.field)
        elif spec.shape is ReferenceShape.ID_SCALAR:
            if isinstance(value, str):
                yield StructuralReference(spec.field, value, spec.field)
        elif spec.shape is ReferenceShape.TRIGGER_WATCH:
            if not isinstance(value, list):
                continue
            for trigger in value:
                if not isinstance(trigger, dict):
                    continue
                watch = trigger.get("watch")
                targets = watch if isinstance(watch, list) else [watch]
                for target in targets:
                    if isinstance(target, str):
                        yield StructuralReference(
                            "triggers.watch", target, "trigger-watch")
        elif spec.shape is ReferenceShape.PIN_OBJECTS:
            if not isinstance(value, list):
                continue
            for pin in value:
                if isinstance(pin, dict) and isinstance(pin.get("id"), str):
                    commit = pin.get("commit")
                    yield StructuralReference(
                        spec.field, pin["id"], "informed-by",
                        str(commit) if commit is not None else None,
                    )


def structural_shape_errors(meta: dict) -> list[tuple[str, str]]:
    """Return deterministic field-shape errors without raising."""

    errors: list[tuple[str, str]] = []
    if not isinstance(meta, dict):
        return errors
    for spec in REFERENCE_FIELDS:
        if spec.field not in meta:
            continue
        value = meta.get(spec.field)
        if spec.shape is ReferenceShape.LINK_OBJECTS:
            if not isinstance(value, list):
                errors.append((spec.field, "must be a list"))
                continue
            for i, entry in enumerate(value):
                if (not isinstance(entry, dict)
                        or not isinstance(entry.get("id"), str)
                        or not isinstance(entry.get("relation"), str)):
                    errors.append((f"{spec.field}[{i}]",
                                   "must be an object with string `id` and `relation`"))
        elif spec.shape is ReferenceShape.ID_LIST:
            if not isinstance(value, list):
                errors.append((spec.field, "must be a list of ids"))
            else:
                for i, target in enumerate(value):
                    if not isinstance(target, str):
                        errors.append((f"{spec.field}[{i}]", "must be a string id"))
        elif spec.shape is ReferenceShape.ID_SCALAR:
            if value is not None and not isinstance(value, str):
                errors.append((spec.field, "must be a string id"))
        elif spec.shape is ReferenceShape.TRIGGER_WATCH:
            if not isinstance(value, list):
                errors.append((spec.field, "must be a list"))
                continue
            for i, trigger in enumerate(value):
                if not isinstance(trigger, dict):
                    errors.append((f"{spec.field}[{i}]", "must be an object"))
                    continue
                if "watch" not in trigger:
                    continue
                watch = trigger.get("watch")
                if not (isinstance(watch, str)
                        or (isinstance(watch, list)
                            and all(isinstance(x, str) for x in watch))):
                    errors.append((f"{spec.field}[{i}].watch",
                                   "must be a string id or list of string ids"))
        elif spec.shape is ReferenceShape.PIN_OBJECTS:
            if not isinstance(value, list):
                errors.append((spec.field, "must be a list"))
            else:
                for i, pin in enumerate(value):
                    if not isinstance(pin, dict) or not isinstance(pin.get("id"), str):
                        errors.append((f"{spec.field}[{i}]",
                                       "must be an object with string `id`"))
    return errors
