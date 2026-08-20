"""Every structural-reference consumer is fed by the canonical registry."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from markdownllm.indexes import build_index_body  # noqa: E402
from markdownllm.mcp_server import _mcp_egress_meta  # noqa: E402
from markdownllm.model import CORE_FIELDS, Corpus, Thing  # noqa: E402
from markdownllm.structural_refs import (  # noqa: E402
    REFERENCE_FIELDS, ReferenceShape, egress_private_fields,
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
