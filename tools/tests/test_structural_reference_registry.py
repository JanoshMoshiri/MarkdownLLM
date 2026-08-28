"""Every structural-reference consumer is fed by the canonical registry."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.indexes import build_index_body  # noqa: E402
from markdownllm.mcp_server import _mcp_egress_meta  # noqa: E402
from markdownllm.model import CORE_FIELDS, Corpus, Thing  # noqa: E402
from markdownllm.structural_refs import (  # noqa: E402
    COMMIT_PIN_FIELDS, REFERENCE_FIELDS, CommitPinScope, ReferenceShape,
    commit_pin_field_names, egress_private_fields, iter_commit_pins,
    iter_structural_references, structural_field_names,
)
from markdownllm.touchpoints import _inbound_counts  # noqa: E402
from markdownllm.validation import validate_level2  # noqa: E402


def _value(spec):
    if spec.shape is ReferenceShape.LINK_OBJECTS:
        return [{"id": "target", "relation": "related"}]
    if spec.shape is ReferenceShape.ID_LIST:
        return ["target"]
    if spec.shape is ReferenceShape.ID_SCALAR:
        return "target"
    if spec.shape is ReferenceShape.TRIGGER_WATCH:
        return [{"type": "relationship", "watch": "target", "action": "surface"}]
    if spec.shape is ReferenceShape.PIN_OBJECTS:
        return [{"id": "target", "commit": "abc1234"}]
    raise AssertionError(spec)


def _corpus(spec) -> Corpus:
    root = Path("C:/registry-fixture")
    src = Thing(root / "things" / "source.md", {
        "id": "source", "type": "note", "status": "in-progress",
        "created": "2026-08-20", spec.field: _value(spec),
    }, "# Source\n")
    target = Thing(root / "things" / "target.md", {
        "id": "target", "type": "note", "status": "in-progress",
        "created": "2026-08-20",
    }, "# Target\n")
    return Corpus(root=root, things=[src, target])


def test_registry_owns_schema_and_egress_field_sets():
    fields = structural_field_names()
    assert fields <= CORE_FIELDS
    assert fields == egress_private_fields()
    meta = {field: "private" for field in fields} | {"id": "public"}
    assert _mcp_egress_meta(meta) == {"id": "public"}


def test_every_registered_field_feeds_extraction_validation_indexes_and_cues():
    for spec in REFERENCE_FIELDS:
        corpus = _corpus(spec)
        refs = list(iter_structural_references(corpus.things[0].meta))
        assert [r.target for r in refs] == ["target"], spec.field

        # All current targets exist, so the shared validator must not invent an
        # unknown-id finding for any registered local-reference shape.
        assert not any("unknown id" in f.message for f in validate_level2(corpus)), spec.field

        assert _inbound_counts(corpus)["target"] == 1, spec.field
        body, _ = build_index_body(corpus, spec.index_signal)
        assert "target" in body and "source" in body, spec.field


def test_one_registry_entry_cannot_leak_through_mcp_even_when_malformed():
    meta = {spec.field: {"repository": "private"} for spec in REFERENCE_FIELDS}
    meta["title"] = "crossable"
    assert _mcp_egress_meta(meta) == {"title": "crossable"}


# ------------------------------------------------- commit-pin registry


def test_commit_pin_fields_are_registered_frontmatter_vocabulary():
    # Same admission rule as the reference fields: the floor reads these, so
    # a domain must never be made to register the framework's own vocabulary.
    assert commit_pin_field_names() <= CORE_FIELDS


def test_registry_states_the_pin_set_with_its_scope_and_owner():
    by_field = {spec.field: spec for spec in COMMIT_PIN_FIELDS}
    # `informed_by` is the field the commit-boundary check exists for.
    assert by_field["informed_by"].scope is CommitPinScope.LOCAL
    assert not by_field["informed_by"].resolved_elsewhere
    # `definition_commit` is a local pin the workflow revision binding already
    # resolves — registered so the set is complete, excluded so one wrong pin
    # cannot produce two Errors saying the same thing.
    assert by_field["definition_commit"].resolved_elsewhere
    # `source_commit` names a commit in the SOURCE domain's repository, which
    # this one need not hold; resolving it locally would report "missing" for
    # a correct pin.
    assert by_field["source_commit"].scope is CommitPinScope.FOREIGN
    assert all(spec.resolved_by for spec in COMMIT_PIN_FIELDS)


def test_commit_pin_extraction_covers_both_shapes_and_is_total():
    meta = {
        "informed_by": [
            {"id": "a", "commit": "abc1234"},
            {"id": "b"},                       # no pin — nothing to extract
            "malformed",                       # shape error, owned elsewhere
            {"id": "c", "commit": 2399917},    # all-digit short sha parses int
        ],
        "definition_commit": "d" * 40,
        "source_commit": "abc1234",
    }
    extracted = {(pin.field, pin.pin) for pin in iter_commit_pins(meta)}
    assert extracted == {
        ("informed_by[0].commit", "abc1234"),
        ("informed_by[3].commit", "2399917"),
        ("definition_commit", "d" * 40),
        ("source_commit", "abc1234"),
    }
    # Total: a malformed frontmatter must never raise out of extraction.
    assert list(iter_commit_pins({"informed_by": "not-a-list"})) == []
    assert list(iter_commit_pins(["not", "a", "mapping"])) == []
