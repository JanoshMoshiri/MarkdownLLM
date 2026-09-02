from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest
import yaml

from tools.verify_evidence import pytest_evidence


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
    # A requirement that is specified but parked carries a dated reason under
    # `deferred` instead of a row: the gate stays exact without pretending
    # evidence exists. An id may not be both traced and deferred.
    deferred = manifest().get("deferred", {})
    assert not set(deferred) & set(traced), set(deferred) & set(traced)
    assert all(row.get("parked") and row.get("reason") for row in deferred.values()), deferred
    assert set(traced) | set(deferred) == requirement_ids and len(requirement_ids) == 79
    tests = collected_test_functions()
    allowed_dispositions = {"automated", "browser", "mixed", "analysis"}
    allowed_prefixes = ("pytest::", "browser::", "system::", "analysis::", "human::")
    required_fields = {
        "method", "fixture", "observable_pass_condition", "evidence", "evidence_location",
        "technical_owner", "acceptance_owner", "disposition", "human_disposition",
    }
    # A requirement whose recorded evidence describes a tree that no longer
    # exists carries a dated reopening note. `disposition` stays the category of
    # verification; it is not the place to record that the evidence is stale.
    optional_fields = {"reopened_2026_08_28", "reclosed_2026_08_28"}
    for requirement_id, row in traced.items():
        assert required_fields <= set(row) <= required_fields | optional_fields, (
            requirement_id, set(row) ^ required_fields,
        )
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
    expected = set(re.findall(r"\bM(?:0[1-9]|1[0-9]|2[01])\b", specification))
    mutants = manifest()["mutants"]
    assert set(mutants) == expected == {f"M{index:02}" for index in range(1, 22)}
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
    deferred = manifest().get("deferred", {})
    assert len(rows) == len(set(rows)) == 79 - len(deferred)


@pytest.mark.meta
def test_pytest_evidence_reads_the_testsuites_container_emitted_by_pytest(tmp_path):
    junit = tmp_path / "pytest.xml"
    junit.write_text(
        '<testsuites><testsuite tests="2" failures="0" errors="0" skipped="0">'
        '<testcase classname="tests.test_alpha" name="test_one" />'
        '<testcase classname="tests.test_alpha" name="test_two" />'
        '</testsuite></testsuites>',
        encoding="utf-8",
    )

    passed, counts = pytest_evidence(junit)

    assert counts == {"tests": 2, "failures": 0, "errors": 0, "skipped": 0}
    assert passed == {
        "pytest::tests/test_alpha.py::test_one",
        "pytest::tests/test_alpha.py::test_two",
    }
