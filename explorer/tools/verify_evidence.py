"""Verify the trace ledger against hashed, subject-bound execution evidence."""

from __future__ import annotations

import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

try:
    from .evidence_common import SUBJECT_ALGORITHM, file_sha256, subject_sha256
except ImportError:  # Direct script execution keeps tools/ on sys.path.
    from evidence_common import SUBJECT_ALGORITHM, file_sha256, subject_sha256


def pytest_evidence(junit: Path) -> tuple[set[str], dict[str, int]]:
    root = ET.parse(junit).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("./testsuite"))
    counts = {
        name: sum(int(suite.attrib.get(name, 0)) for suite in suites)
        for name in ("tests", "failures", "errors", "skipped")
    }
    passed: set[str] = set()
    for case in root.iter("testcase"):
        if any(case.find(kind) is not None for kind in ("failure", "error", "skipped")):
            continue
        classname = case.attrib.get("classname", "").replace(".", "/")
        if not classname.startswith("tests/"):
            classname = "tests/" + classname.rsplit("/", 1)[-1]
        name = case.attrib.get("name", "").split("[", 1)[0]
        passed.add(f"pytest::{classname}.py::{name}")
    return passed, counts


def _json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} is not a JSON object")
    return value


def validate_artifact(path: Path, subject: str) -> set[str]:
    """Apply content-specific oracles; IDs are never trusted on declaration alone."""
    if path.name == "mutation-kill-matrix.json":
        value = _json(path); summary = value.get("summary", {})
        if value.get("tool", {}).get("name") != "run_mutations.py" or summary.get("total") != 21 or summary.get("survived") != 0 or summary.get("killed") != 21:
            raise ValueError("mutation matrix is incomplete")
        ids = {
            item.get("id") for item in value.get("mutants", [])
            if item.get("status") == "killed"
            and item.get("changes")
            and all(change.get("before_sha256") and change.get("after_sha256") and change["before_sha256"] != change["after_sha256"] for change in item["changes"])
        }
        if ids != {f"M{index:02}" for index in range(1, 22)}: raise ValueError("mutation identities/source hashes are incomplete")
        return {"analysis::MT-MUTATION-001", *(f"mutation::{item}" for item in ids)}
    if path.name == "clean-install.json":
        value = _json(path)
        if value.get("tool", {}).get("name") != "verify_install.py" or value.get("status") != "pass" or not value.get("offline_install"):
            raise ValueError("clean install evidence failed")
        if not value.get("arbitrary_cwd") or set(value.get("runtime_routes", [])) != {"/health", "/", "/js/app.js", "/api/v1/estate"}:
            raise ValueError("clean install route/cwd probe incomplete")
        if value.get("lifecycle", {}).get("status") != "pass": raise ValueError("CLI lifecycle probe incomplete")
        return {"system::ST-INSTALL-001", "system::ST-OFFLINE-001", "system::ST-CLI-001"}
    if path.name == "windows-installer.json":
        value = _json(path)
        if value.get("tool", {}).get("name") != "verify_windows_installer.py":
            raise ValueError("Windows installer evidence failed")
        if value.get("status") == "blocked":
            blocked = (
                value.get("subject_sha256") == subject
                and value.get("installer", {}).get("sha256")
                and value.get("upgrade", {}).get("status") == "pass"
                and value.get("uninstall", {}).get("status") == "blocked"
                and value.get("uninstall", {}).get("blocked_before_process_start")
                and value.get("uninstall", {}).get("blocker_evidence") == "windows-publication-gate.json"
            )
            if not blocked:
                raise ValueError("Windows installer blocker record is incomplete")
            return set()
        if value.get("status") != "pass":
            raise ValueError("Windows installer evidence failed")
        exercised = value.get("exercised_installer", {})
        if not exercised.get("same_as_release"):
            isolated = (
                exercised.get("identity_only_isolation")
                and str(exercised.get("app_name", "")).startswith("MarkdownLLM Explorer Verification ")
                and exercised.get("instance_identity")
                and value.get("installer", {}).get("sha256")
                and exercised.get("sha256")
            )
            if not isolated:
                raise ValueError("Windows installer isolation is not identity-only and subject-bound")
        environment = value.get("environment", {})
        if not environment.get("per_user") or environment.get("administrator_required"):
            raise ValueError("Windows installer is not verified as per-user")
        if environment.get("system_python_required") or environment.get("system_node_required") or environment.get("network_required_after_setup_obtained"):
            raise ValueError("Windows installer retains an external runtime dependency")
        stages = ("bundle", "install", "launch", "upgrade", "uninstall")
        if not all(value.get(stage, {}).get("status") == "pass" for stage in stages):
            raise ValueError("Windows installer lifecycle is incomplete")
        for stage in ("upgrade", "uninstall"):
            observation = value.get(stage, {})
            if not observation.get("active_process_stopped") or not observation.get("active_request_drain_bounded"):
                raise ValueError(f"Windows {stage} did not prove bounded active-process shutdown")
        if value.get("source_before_sha256") != value.get("source_after_sha256") or value.get("outside_before_sha256") != value.get("outside_after_sha256"):
            raise ValueError("Windows installer changed substrate or outside data")
        return {
            "system::ST-WIN-BUNDLE-001", "system::ST-WIN-INSTALL-001",
            "system::ST-WIN-LAUNCH-001", "system::ST-WIN-UPGRADE-001",
            "system::ST-WIN-UNINSTALL-001", "system::AJ-08",
            "system::AJ-09", "system::AJ-10",
        }
    if path.name == "performance-20-run.json":
        value = _json(path)
        if value.get("tool", {}).get("name") != "run_performance.py" or value.get("runs") != 20:
            raise ValueError("performance run count/tool mismatch")
        if not value.get("fixture_sha256") or not value.get("profile") or not value.get("raw_ms"):
            raise ValueError("performance fixture/profile/raw timings missing")
        if not value.get("summary") or not all(item.get("status") == "pass" and item.get("passes", 0) >= 19 for item in value["summary"].values()):
            raise ValueError("performance threshold failed")
        return {"analysis::PT-SCALE-001"}
    if path.name == "adapter-swap.json":
        value = _json(path)
        swaps = value.get("swaps", [])
        expected = {
            "HTTP server": ["composition.py", "delivery/swap_http_server.py"],
            "Git reader": ["adapters/swap_git_commit_history.py", "composition.py"],
            "Filesystem reader": ["adapters/swap_confined_source_reader.py", "composition.py"],
            "Markdown renderer": ["adapters/swap_presenter.py", "composition.py"],
        }
        observed = {item.get("adapter"): item for item in swaps if isinstance(item, dict)}
        valid = (
            value.get("schema") == 2
            and value.get("status") == "pass"
            and set(observed) == set(expected)
            and all(
                observed[name].get("changed_paths") == paths
                and not observed[name].get("forbidden_inner_changes")
                and observed[name].get("runtime_probe") == "pass"
                for name, paths in expected.items()
            )
        )
        if not valid:
            raise ValueError("adapter swap changed-path proof failed")
        return {"analysis::AT-SWAP-001"}
    if path.name == "immutability.json":
        value = _json(path)
        if value.get("status") != "pass" or value.get("before_sha256") != value.get("after_sha256") or value.get("outside_before_sha256") != value.get("outside_after_sha256"):
            raise ValueError("immutability before/after proof failed")
        if len(value.get("helper_classes", [])) < 8 or value.get("source_entries", 0) < 1:
            raise ValueError("immutability helper/snapshot coverage incomplete")
        return {"analysis::GT-IMMUTABLE-001"}
    if path.name == "operator-acceptance.json":
        value = _json(path)
        if (
            value.get("schema") != 1
            or value.get("status") != "accepted"
            or value.get("accepted_by") != "Janosh Moshiri"
            or value.get("accepted_at") != "2026-08-28"
            or not value.get("statement")
            or not value.get("scope")
            or not isinstance(value.get("requirement_ids"), list)
        ):
            raise ValueError("operator acceptance evidence is incomplete")
        return set()
    if path.name == "browser-runtime.json":
        value = _json(path)
        if value.get("subject_sha256") != subject or value.get("tool", {}).get("name") != "in-app-browser":
            raise ValueError("browser evidence subject/tool mismatch")
        runtime = value.get("runtime", {})
        if not all(runtime.get(key) for key in ("browser", "browser_version", "os", "executed_at")):
            raise ValueError("browser runtime profile incomplete")
        evidence: set[str] = set()
        for item in value.get("evidence", []):
            if item.get("status") != "pass" or not item.get("checks") or not item.get("artifacts"):
                continue
            for artifact in item["artifacts"]:
                artifact_path = path.parents[2] / artifact["path"]
                if not artifact_path.is_file() or file_sha256(artifact_path) != artifact["sha256"]:
                    raise ValueError(f"browser supporting artifact failed: {artifact.get('path')}")
            evidence.add(item["id"])
        required = {"browser::BT-SHELL-001", "browser::BT-NAV-001", "browser::BT-TABS-001", "browser::BT-DOCUMENT-001", "browser::BT-SEARCH-001", "browser::BT-THEME-001", "browser::BT-ASYNC-001", "browser::BT-RESPONSIVE-001", "browser::BT-KEYBOARD-001", "browser::BT-A11Y-001", "browser::BT-VISUAL-001", *(f"system::AJ-0{index}" for index in range(1, 8))}
        if not required <= evidence: raise ValueError(f"browser evidence missing {sorted(required - evidence)}")
        return evidence
    return set()


def indexed_evidence(explorer: Path, directory: Path) -> tuple[set[str], dict[str, str], dict]:
    index_path = directory / "evidence-index.json"; index = _json(index_path)
    current_subject = subject_sha256(explorer)
    if index.get("subject") != {"algorithm": SUBJECT_ALGORITHM, "sha256": current_subject}:
        raise ValueError("evidence index is not bound to the current immutable subject")
    if index.get("tool", {}).get("name") != "build_evidence_index.py" or not index.get("tool", {}).get("version"):
        raise ValueError("evidence index tool/version missing")
    passed: set[str] = set(); locations: dict[str, str] = {}; seen_paths: set[str] = set()
    for item in index.get("artifacts", []):
        relative = item.get("path", "")
        if relative in seen_paths or not relative.startswith("tests/evidence/"):
            raise ValueError("duplicate or outside evidence path")
        seen_paths.add(relative); path = explorer / relative
        if not path.is_file() or item.get("bytes") != path.stat().st_size or item.get("sha256") != file_sha256(path):
            raise ValueError(f"evidence artifact hash/size mismatch: {relative}")
        verified = validate_artifact(path, current_subject)
        if set(item.get("evidence_ids", [])) != verified:
            raise ValueError(f"indexed IDs do not match verified content: {relative}")
        for evidence_id in verified:
            if evidence_id in locations: raise ValueError(f"duplicate evidence ID: {evidence_id}")
            locations[evidence_id] = relative
        passed |= verified
    return passed, locations, index


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--junit", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--evidence-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    explorer = arguments.manifest.resolve().parents[1]
    manifest = yaml.safe_load(arguments.manifest.read_text(encoding="utf-8"))
    passed, junit_counts = pytest_evidence(arguments.junit)
    locations = {item: "tests/evidence/pytest.xml" for item in passed}
    evidence_errors: list[str] = []
    try:
        external, external_locations, index = indexed_evidence(explorer, arguments.evidence_dir.resolve())
        passed |= external; locations.update(external_locations)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        index = {}; evidence_errors.append(str(error))
    pending_human = {
        requirement_id
        for requirement_id, row in manifest["requirements"].items()
        if row["human_disposition"] == "pending-human"
    }
    accepted_human: set[str] = set()
    if index:
        try:
            acceptance = _json(arguments.evidence_dir.resolve() / "operator-acceptance.json")
            accepted_human = set(acceptance.get("requirement_ids", []))
            outside = sorted(accepted_human - pending_human)
            if outside:
                raise ValueError(f"operator acceptance claims rows that are not human-owned: {outside}")
        except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
            evidence_errors.append(str(error))
    rows: dict[str, dict[str, object]] = {}; unresolved: list[str] = []
    for requirement_id, row in manifest["requirements"].items():
        expected = row["evidence"]
        missing = [item for item in expected if item not in passed]
        misplaced = [item for item in expected if item in locations and locations[item] not in row["evidence_location"]]
        status = "pass" if not missing and not misplaced else "fail"
        human_disposition = row["human_disposition"]
        if human_disposition == "pending-human" and requirement_id in accepted_human:
            human_disposition = "accepted"
        rows[requirement_id] = {
            "status": status, "expected": expected, "missing": missing, "misplaced": misplaced,
            "technical_owner": row["technical_owner"], "acceptance_owner": row["acceptance_owner"],
            "human_disposition": human_disposition, "method": row["method"], "fixture": row["fixture"],
            "observable_pass_condition": row["observable_pass_condition"], "evidence_location": row["evidence_location"],
        }
        if status == "fail": unresolved.append(requirement_id)
    mutation_missing = [row["evidence"] for row in manifest["mutants"].values() if row["evidence"] not in passed]
    technical_pass = not unresolved and not mutation_missing and not evidence_errors and not junit_counts["failures"] and not junit_counts["errors"] and not junit_counts["skipped"]
    report = {
        "schema": 2, "id": "TRACE-001", "status": "pass" if technical_pass else "fail",
        "subject": index.get("subject"), "junit": junit_counts, "evidence_errors": evidence_errors,
        "resolved_evidence_count": len(passed), "requirements": rows,
        "summary": {
            "requirements": len(rows), "technical_passed": sum(row["status"] == "pass" for row in rows.values()),
            "technical_failed": len(unresolved),
            "human_accepted": sum(row["human_disposition"] == "accepted" for row in rows.values()),
            "human_pending": sum(row["human_disposition"] == "pending-human" for row in rows.values()),
        },
        "unresolved_requirements": unresolved, "unresolved_mutants": mutation_missing,
    }
    output = arguments.output or arguments.evidence_dir / "traceability-result.json"
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], **report["summary"]}, sort_keys=True))
    return 0 if technical_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
