"""Resolve every traceability evidence ID against retained execution artefacts."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml


def pytest_evidence(junit: Path) -> tuple[set[str], dict[str, int]]:
    root = ET.parse(junit).getroot()
    counts = {name: int(root.attrib.get(name, 0)) for name in ("tests", "failures", "errors", "skipped")}
    passed: set[str] = set()
    for case in root.iter("testcase"):
        if case.find("failure") is not None or case.find("error") is not None or case.find("skipped") is not None:
            continue
        classname = case.attrib.get("classname", "").replace(".", "/")
        if not classname.startswith("tests/"):
            classname = "tests/" + classname.rsplit("/", 1)[-1]
        name = case.attrib.get("name", "").split("[", 1)[0]
        passed.add(f"pytest::{classname}.py::{name}")
    return passed, counts


def external_evidence(directory: Path) -> set[str]:
    passed: set[str] = set()
    mutation = directory / "mutation-kill-matrix.json"
    if mutation.is_file():
        value = json.loads(mutation.read_text(encoding="utf-8"))
        if value.get("summary", {}).get("total") == 16 and value["summary"].get("survived") == 0:
            passed.add("analysis::MT-MUTATION-001")
            passed.update(f"mutation::{item['id']}" for item in value["mutants"] if item.get("status") == "killed")
    install = directory / "clean-install.json"
    if install.is_file():
        value = json.loads(install.read_text(encoding="utf-8"))
        if value.get("status") == "pass":
            passed.add("system::ST-INSTALL-001")
            if value.get("offline_install"):
                passed.add("system::ST-OFFLINE-001")
    performance = directory / "performance-20-run.json"
    if performance.is_file():
        value = json.loads(performance.read_text(encoding="utf-8"))
        if value.get("runs") == 20 and all(item.get("status") == "pass" for item in value.get("summary", {}).values()):
            passed.add("analysis::PT-SCALE-001")
    for filename in ("browser-runtime.json", "evidence-index.json"):
        path = directory / filename
        if path.is_file():
            value = json.loads(path.read_text(encoding="utf-8"))
            passed.update(item["id"] for item in value.get("evidence", []) if item.get("status") == "pass")
    return passed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    manifest = yaml.safe_load(arguments.manifest.read_text(encoding="utf-8"))
    passed, junit_counts = pytest_evidence(arguments.junit)
    passed |= external_evidence(arguments.evidence_dir)
    rows: dict[str, dict[str, object]] = {}
    unresolved: list[str] = []
    for requirement_id, row in manifest["requirements"].items():
        expected = row["evidence"]
        missing = [item for item in expected if item != "analysis::TRACE-001" and item not in passed]
        status = "pending" if row["disposition"] == "human_pending" else "pass" if not missing else "fail"
        rows[requirement_id] = {"status": status, "expected": expected, "missing": missing, "owner": row["owner"], "disposition": row["disposition"]}
        if status == "fail": unresolved.append(requirement_id)
    mutation_missing = [row["evidence"] for row in manifest["mutants"].values() if row["evidence"] not in passed]
    if not unresolved and not mutation_missing and not junit_counts["failures"] and not junit_counts["errors"]:
        passed.add("analysis::TRACE-001")
    else:
        for requirement_id, row in rows.items():
            if "analysis::TRACE-001" in row["expected"]:
                row["status"] = "fail"; row["missing"] = ["analysis::TRACE-001"]
                if requirement_id not in unresolved: unresolved.append(requirement_id)
    report = {
        "schema": 1, "id": "TRACE-001", "status": "pass" if not unresolved and not mutation_missing else "fail",
        "junit": junit_counts, "resolved_evidence_count": len(passed), "requirements": rows,
        "summary": {"requirements": len(rows), "passed": sum(row["status"] == "pass" for row in rows.values()), "pending": sum(row["status"] == "pending" for row in rows.values()), "failed": len(unresolved)},
        "unresolved_requirements": unresolved, "unresolved_mutants": mutation_missing,
    }
    output = arguments.output or arguments.evidence_dir / "traceability-result.json"
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], **report["summary"]}, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
