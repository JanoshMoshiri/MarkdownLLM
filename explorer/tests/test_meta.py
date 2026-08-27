from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml


EXPLORER = Path(__file__).parents[1]


def manifest():
    return yaml.safe_load((EXPLORER / "tests" / "traceability.yaml").read_text(encoding="utf-8"))


def collected_test_functions() -> set[str]:
    found: set[str] = set()
    for path in (EXPLORER / "tests").glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                found.add(f"tests/{path.name}::{node.name}")
    return found


@pytest.mark.meta
def test_traceability_manifest_is_exact_and_well_formed():
    requirement_text = (EXPLORER / "docs" / "requirements.md").read_text(encoding="utf-8")
    requirement_ids = set(re.findall(r"(?:FR|NFR)-[A-Z]+-\d{3}[A-Z]?", requirement_text))
    traced = manifest()["requirements"]
    assert set(traced) == requirement_ids and len(requirement_ids) == 63
    tests = collected_test_functions()
    allowed_dispositions = {"automated", "browser", "mixed", "analysis"}
    allowed_prefixes = ("pytest::", "browser::", "system::", "analysis::", "human::")
    required_fields = {
        "method", "fixture", "observable_pass_condition", "evidence", "evidence_location",
        "technical_owner", "acceptance_owner", "disposition", "human_disposition",
    }
    for requirement_id, row in traced.items():
        assert set(row) == required_fields, (requirement_id, set(row) ^ required_fields)
        assert row["disposition"] in allowed_dispositions and row["technical_owner"] and row["acceptance_owner"] and row["evidence"], requirement_id
        assert row["method"] and row["fixture"] and row["observable_pass_condition"] and row["evidence_location"]
        assert row["human_disposition"] in {"none", "pending-human"}
        assert all(item.startswith(allowed_prefixes) for item in row["evidence"]), requirement_id
        for item in row["evidence"]:
            if item.startswith("pytest::"):
                assert item.removeprefix("pytest::") in tests, (requirement_id, item)


@pytest.mark.meta
def test_mutation_manifest_is_complete_and_targets_real_tests():
    specification = (EXPLORER / "docs" / "test-specification.md").read_text(encoding="utf-8")
    expected = set(re.findall(r"\bM(?:0[1-9]|1[0-6])\b", specification))
    mutants = manifest()["mutants"]
    assert set(mutants) == expected == {f"M{index:02}" for index in range(1, 17)}
    tests = collected_test_functions()
    for mutant_id, row in mutants.items():
        assert row["subject"] and row["evidence"] == f"mutation::{mutant_id}" and row["tests"]
        assert all(test in tests for test in row["tests"]), (mutant_id, row["tests"])


@pytest.mark.meta
def test_supported_python_range_is_declared():
    pyproject = (EXPLORER / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires-python = ">=3.10"' in pyproject
    assert 'PyYAML==6.0.3' in pyproject


@pytest.mark.meta
def test_test_spec_trace_table_has_one_row_per_requirement():
    specification = (EXPLORER / "docs" / "test-specification.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| ((?:FR|NFR)-[A-Z]+-\d{3}[A-Z]?) \|", specification, re.MULTILINE)
    assert len(rows) == len(set(rows)) == 63
