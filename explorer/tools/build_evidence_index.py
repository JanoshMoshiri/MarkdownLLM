"""Bind retained evidence bytes to one immutable Explorer subject hash."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

from evidence_common import SUBJECT_ALGORITHM, file_sha256, subject_sha256


def evidence_ids(path: Path) -> list[str]:
    if path.suffix != ".json":
        return []
    value = json.loads(path.read_text(encoding="utf-8"))
    if path.name == "mutation-kill-matrix.json":
        return ["analysis::MT-MUTATION-001", *(f"mutation::{item['id']}" for item in value.get("mutants", []) if item.get("status") == "killed")]
    if path.name == "clean-install.json":
        ids = ["system::ST-INSTALL-001"]
        if value.get("offline_install"): ids.append("system::ST-OFFLINE-001")
        if value.get("lifecycle", {}).get("status") == "pass": ids.append("system::ST-CLI-001")
        return ids
    if path.name == "windows-installer.json":
        return [
            "system::ST-WIN-BUNDLE-001", "system::ST-WIN-INSTALL-001",
            "system::ST-WIN-LAUNCH-001", "system::ST-WIN-UPGRADE-001",
            "system::ST-WIN-UNINSTALL-001", "system::AJ-08",
            "system::AJ-09", "system::AJ-10",
        ]
    if path.name == "performance-20-run.json": return ["analysis::PT-SCALE-001"]
    if path.name == "adapter-swap.json": return ["analysis::AT-SWAP-001"]
    if path.name == "immutability.json": return ["analysis::GT-IMMUTABLE-001"]
    if path.name == "browser-runtime.json": return [item["id"] for item in value.get("evidence", []) if item.get("status") == "pass"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--explorer", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--evidence-dir", type=Path)
    arguments = parser.parse_args()
    explorer = arguments.explorer.resolve(); directory = (arguments.evidence_dir or explorer / "tests" / "evidence").resolve()
    artifacts = []
    for path in sorted(directory.iterdir(), key=lambda item: item.name):
        if not path.is_file() or path.name in {"evidence-index.json", "traceability-result.json"}:
            continue
        artifacts.append({
            "path": path.relative_to(explorer).as_posix(), "sha256": file_sha256(path),
            "bytes": path.stat().st_size, "evidence_ids": evidence_ids(path),
        })
    document = {
        "schema": 1,
        "subject": {"algorithm": SUBJECT_ALGORITHM, "sha256": subject_sha256(explorer)},
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool": {"name": "build_evidence_index.py", "version": "1", "python": platform.python_version(), "platform": platform.platform()},
        "artifacts": artifacts,
    }
    output = directory / "evidence-index.json"
    output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"subject": document["subject"]["sha256"], "artifacts": len(artifacts), "evidence_ids": sum(len(item["evidence_ids"]) for item in artifacts)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
