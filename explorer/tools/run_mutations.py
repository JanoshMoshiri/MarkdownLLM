"""Execute the 21 specified deliberate mutants against their focused oracles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Replacement:
    relative_path: str
    old: str
    new: str
    count: int = 1


CASES: dict[str, tuple[Replacement, ...]] = {
    "M01": (Replacement("adapters/filesystem_catalogue.py", "SourceBoundary(substrate, self._root, self._domain_root)", "SourceBoundary(substrate, self._root, None)"),),
    "M02": (Replacement("adapters/filesystem_catalogue.py", "    return collisions\n\n\ndef _is_reparse", "    return set()\n\n\ndef _is_reparse"),),
    "M03": (Replacement("adapters/confined_source_reader.py", "        self._reject_reparse_components(boundary, relative)\n", "        # MUTANT: follow a reparse/symlink parent\n", 1),),
    "M04": (Replacement("adapters/confined_source_reader.py", "if len(payload) > self._limits.file_bytes:", "if len(payload) >= self._limits.file_bytes:"),),
    "M05": (Replacement("adapters/frontmatter_parser.py", "            self._validate_event_stream(yaml_text)\n", "            # MUTANT: skip YAML event validation\n"),),
    "M06": (Replacement("adapters/safe_markdown_parser.py", "                elif decoded_url.scheme or \":\" in decoded_target.split(\"/\", 1)[0] or decoded_target.startswith((\"/\", \"//\", \"#\")):\n", "                elif False:\n"),),
    # Anchored on the DocumentRecord branch specifically: the historical-document
    # encoder also carries a "content": value.content pair, and a shorter anchor
    # silently retargeted this mutant at a branch its oracle does not cover.
    "M07": (Replacement(
        "delivery/response_encoding.py",
        '"content": value.content, "frontmatter": to_wire(value.frontmatter), "size": value.size,',
        '"content": {"raw": value.content, "rendered": value.content}, "frontmatter": to_wire(value.frontmatter), "size": value.size,',
    ),),
    "M08": (Replacement("adapters/cursors.py", "            if not hmac.compare_digest(signature, expected):", "            if False:"),),
    "M09": (Replacement("composition.py", "resolve_trusted_git(root)", '"git"'),),
    "M10": (Replacement("adapters/git_commit_history.py", '                "GIT_OPTIONAL_LOCKS": "0",\n', ""),),
    "M11": (Replacement("delivery/http_server.py", "            if target.path.startswith(\"/api/\"):\n                supplied = self.headers.get(\"X-Explorer-Capability\", \"\")\n                if not supplied:\n", "            if target.path.startswith(\"/api/\"):\n                supplied = self.headers.get(\"X-Explorer-Capability\", \"\")\n                if False:  # MUTANT: accept missing capability\n"),),
    "M12": (Replacement("delivery/http_server.py", 'print(f"{level} operation={operation} source={source_id or \'-\'} code={error.code}"', 'print(f"{level} operation={operation} source={source_id or \'-\'} target={self.path} code={error.code}"'),),
    "M13": (Replacement("delivery/http_server.py", "        if not self.capacity.acquire(blocking=False):\n", "        if False:\n"),),
    "M14": (Replacement("delivery/static/js/state.js", "    && request.liveIdentity === identityKey(liveLocationIdentity())", "    && true  // MUTANT: accept obsolete live UI context"),),
    "M15": (Replacement("delivery/static/js/views/navigation.js", "  label.textContent = source.display_name;", "  label.innerHTML = source.display_name;"),),
    "M16": (Replacement("delivery/static/js/views/navigation.js", "export function renderSources", 'fetch("/api/v1/estate");\n\nexport function renderSources'),),
    "M17": (Replacement(
        "application/read_historical_document.py",
        '        if not self._admission.admits(source.boundary_token, relative):\n            raise ExplorerError("path_excluded")\n',
        "        # MUTANT: read history without asking whether the source admits the path\n",
    ),),
    "M18": (Replacement(
        "adapters/git_commit_history.py",
        '    return all(part and part not in {".", ".."} for part in value.split("/"))',
        "    return True  # MUTANT: trust the caller to have validated the path",
    ),),
    "M19": (Replacement(
        "adapters/git_commit_history.py",
        "                and _is_tree_path(arguments[-1])\n            )\n    return False\n",
        "                and _is_tree_path(arguments[-1])\n            )\n    return True  # MUTANT: admit any argument vector\n",
    ),),
    "M20": (Replacement(
        "adapters/thing_index.py",
        "        for identifier in contested:\n            mapping.pop(identifier, None)\n",
        "        # MUTANT: keep whichever file first claimed a contested identifier\n",
    ),),
    "M21": (Replacement(
        "adapters/thing_index.py",
        "        if line.strip() in FRONTMATTER_FENCES:\n            return None\n",
        "        # MUTANT: keep scanning past the closing frontmatter fence\n",
    ),),
}


def mutate(package_root: Path, replacements: tuple[Replacement, ...]) -> list[dict[str, object]]:
    applied: list[dict[str, object]] = []
    for replacement in replacements:
        path = package_root / replacement.relative_path
        source = path.read_text(encoding="utf-8")
        occurrences = source.count(replacement.old)
        if occurrences < replacement.count:
            raise RuntimeError(f"mutation target drifted: {replacement.relative_path}: {replacement.old!r}")
        changed = source.replace(replacement.old, replacement.new, replacement.count)
        path.write_text(changed, encoding="utf-8")
        applied.append({
            "file": replacement.relative_path,
            "before_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "after_sha256": hashlib.sha256(changed.encode()).hexdigest(),
        })
    return applied


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node", default=os.environ.get("EXPLORER_NODE", "node"))
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    explorer = Path(__file__).parents[1]
    output = arguments.output or explorer / "tests" / "evidence" / "mutation-kill-matrix.json"
    manifest = yaml.safe_load((explorer / "tests" / "traceability.yaml").read_text(encoding="utf-8"))
    if set(CASES) != set(manifest["mutants"]):
        raise SystemExit("mutation cases and traceability manifest disagree")
    results: list[dict[str, object]] = []
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="mdllm-explorer-mutants-") as temporary:
        temporary_root = Path(temporary)
        for mutant_id, replacements in CASES.items():
            mutant_root = temporary_root / mutant_id
            package_root = mutant_root / "src" / "markdownllm_explorer"
            shutil.copytree(explorer / "src" / "markdownllm_explorer", package_root)
            applied = mutate(package_root, replacements)
            tests = manifest["mutants"][mutant_id]["tests"]
            environment = dict(os.environ)
            environment["PYTHONPATH"] = str(mutant_root / "src")
            environment["EXPLORER_MUTANT_SOURCE"] = str(package_root)
            environment["EXPLORER_NODE"] = arguments.node
            command = [
                sys.executable, "-m", "pytest", "-q", "-o", "pythonpath=",
                *tests, "--basetemp", str(mutant_root / "pytest"), "-o", f"cache_dir={mutant_root / 'cache'}",
            ]
            tick = time.monotonic()
            completed = subprocess.run(command, cwd=explorer, env=environment, capture_output=True, text=True, timeout=30)
            killed = completed.returncode != 0
            results.append({
                "id": mutant_id, "status": "killed" if killed else "survived", "returncode": completed.returncode,
                "duration_seconds": round(time.monotonic() - tick, 3), "tests": tests, "changes": applied,
                "output_tail": (completed.stdout + completed.stderr)[-4000:],
            })
    document = {
        "schema": 1,
        "tool": {"name": "run_mutations.py", "version": "1"},
        "subject": "actual copied Explorer source with one deliberate defect per run",
        "started_at_epoch": started,
        "duration_seconds": round(time.time() - started, 3),
        "summary": {"total": len(results), "killed": sum(item["status"] == "killed" for item in results), "survived": sum(item["status"] == "survived" for item in results)},
        "mutants": results,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(document["summary"], sort_keys=True))
    return 0 if document["summary"]["survived"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
