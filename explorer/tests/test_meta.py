from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml


EXPLORER = Path(__file__).parents[1]
ROOT = EXPLORER.parent


def manifest():
    return yaml.safe_load((EXPLORER / "tests" / "traceability.yml").read_text(encoding="utf-8"))


@pytest.mark.meta
def test_traceability_is_exact_and_executable():
    requirement_text = (EXPLORER / "docs" / "requirements.md").read_text(encoding="utf-8")
    requirement_ids = set(re.findall(r"(?:FR|NFR)-[A-Z]+-\d{3}[A-Z]?", requirement_text))
    traced = manifest()["requirements"]
    assert set(traced) == requirement_ids
    test_corpus = "\n".join(path.read_text(encoding="utf-8") for path in (EXPLORER / "tests").glob("test_*.py"))
    assert len(requirement_ids) == 60
    for requirement_id, evidence in traced.items():
        assert evidence, requirement_id
        assert all(f"def {test_name}" in test_corpus for test_name in evidence), (requirement_id, evidence)


@pytest.mark.meta
def test_mutation_matrix_is_complete():
    specification = (EXPLORER / "docs" / "test-specification.md").read_text(encoding="utf-8")
    expected = set(re.findall(r"\bM(?:0[1-9]|1[0-6])\b", specification))
    mutants = manifest()["mutants"]
    test_corpus = "\n".join(path.read_text(encoding="utf-8") for path in (EXPLORER / "tests").glob("test_*.py"))
    assert set(mutants) == expected == {f"M{index:02}" for index in range(1, 17)}
    assert all(f"def {test_name}" in test_corpus for test_name in mutants.values())


@pytest.mark.meta
def test_supported_python_range_is_declared():
    pyproject = (EXPLORER / "pyproject.toml").read_text(encoding="utf-8")
    assert 'requires-python = ">=3.10"' in pyproject
    assert 'PyYAML==6.0.3' in pyproject


@pytest.mark.meta
def test_test_spec_trace_table_has_one_row_per_requirement():
    specification = (EXPLORER / "docs" / "test-specification.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| ((?:FR|NFR)-[A-Z]+-\d{3}[A-Z]?) \|", specification, re.MULTILINE)
    assert len(rows) == len(set(rows)) == 60
