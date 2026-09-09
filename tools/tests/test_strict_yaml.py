"""The definition boundary rejects ambiguous YAML everywhere it matters."""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import mdllm  # noqa: E402
from markdownllm.calc import to_decimal  # noqa: E402
from markdownllm.yaml_loader import load_yaml  # noqa: E402


@pytest.mark.parametrize("key,value", [
    ("status", "draft"),
    ("dependencies", "[]"),
    ("origin", "stated"),
    ("verified", "false"),
    ("autopush", "false"),
    ("types", "{}"),
])
def test_duplicate_definition_keys_are_rejected_with_locations(key, value):
    text = f"{key}: {value}\n{key}: {value}\n"
    with pytest.raises(yaml.YAMLError) as raised:
        load_yaml(text, source="definition.yaml")
    message = str(raised.value)
    assert f"duplicate key {key!r}" in message
    assert "definition.yaml" in message
    assert "line 1, column 1" in message


def test_scan_turns_duplicate_frontmatter_into_a_finding(tmp_path):
    things = tmp_path / "things"
    things.mkdir()
    (things / "ambiguous.md").write_text(
        "---\nid: ambiguous\ntype: note\nstatus: in-progress\n"
        "status: completed\ncreated: 2026-08-20\n---\n\n# Ambiguous\n",
        encoding="utf-8",
    )
    _, findings = mdllm.scan(tmp_path)
    assert len(findings) == 1
    assert findings[0].severity == mdllm.SEV_ERROR
    assert "duplicate key 'status'" in findings[0].message
    assert "things" in findings[0].message and "ambiguous.md" in findings[0].message


def test_schema_duplicate_is_a_finding_not_a_crash(tmp_path):
    (tmp_path / "_schema.yaml").write_text(
        "schema_version: 1\ntypes: {}\ntypes: {}\n", encoding="utf-8")
    corpus, findings = mdllm.scan(tmp_path)
    assert corpus.schema is None
    assert any(f.severity == mdllm.SEV_ERROR
               and "duplicate key 'types'" in f.message for f in findings)


def test_bare_on_trigger_semantics_are_preserved():
    meta, _, error = mdllm.parse_frontmatter(
        "---\nid: t\ntype: task\nstatus: in-progress\ncreated: 2026-08-20\n"
        "triggers:\n  - type: dependency\n    on: status_changed_to\n---\n# T\n")
    assert error is None
    assert meta["triggers"][0]["on"] == "status_changed_to"
    assert True not in meta["triggers"][0]


def test_yaml_float_retains_exact_decimal_lexeme_for_calculation():
    value = load_yaml("amount: 1234567890.123456789012345678\n")["amount"]
    assert isinstance(value, float)  # compatibility with existing model users
    assert to_decimal(value) == Decimal("1234567890.123456789012345678")


def test_lexical_float_remains_safe_dumpable():
    value = load_yaml("amount: 1.2300\n")
    assert "amount:" in yaml.safe_dump(value)


def test_yaml_int_retains_exact_lexeme():
    # YAML 1.1 types `0123456` as octal and `0b00101` as binary; `str()` of
    # the value re-spells them as numbers the source never held. A short
    # commit pin is one of those roughly one draw in a thousand, and CI
    # flaked on that draw (2026-09-09). The int keeps its token, as the
    # float already did for calc; everything else still sees an int.
    cases = {"0123456": 42798, "0b00101": 5, "0000000": 0,
             "2399917": 2399917, "1_000": 1000}
    for lexeme, value in cases.items():
        v = load_yaml(f"pin: {lexeme}\n")["pin"]
        assert isinstance(v, int) and v == value, lexeme
        assert v.yaml_lexeme == lexeme
    assert load_yaml("pin: 0o17\n")["pin"] == "0o17"  # YAML 1.2 octal: a str in 1.1
    assert isinstance(load_yaml("b: true\n")["b"], bool)  # own tag, untouched
    assert not hasattr(load_yaml("b: true\n")["b"], "yaml_lexeme")


def test_lexical_int_remains_safe_dumpable():
    # SafeDumper dispatches by exact type; the subclass must be registered or
    # every egress render of a thing carrying an int field would raise.
    value = load_yaml("coverage: 0123456\n")
    assert yaml.safe_dump(value).strip() == "coverage: 42798"
