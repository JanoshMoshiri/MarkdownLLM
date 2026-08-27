from __future__ import annotations

import hashlib
import http.client
import json
import os
import subprocess
import threading
from pathlib import Path

import pytest

from markdownllm_explorer.composition import build_runtime
from markdownllm_explorer.delivery.http_server import serve


def _acl_digest(path: Path) -> str:
    if os.name != "nt":
        return "mode-only"
    result = subprocess.run(["icacls", str(path)], capture_output=True, timeout=5)
    return hashlib.sha256(result.stdout.replace(str(path).encode(), b"<path>")).hexdigest()


def immutable_snapshot(root: Path) -> dict[str, tuple[int, int, int, str, str]]:
    snapshot: dict[str, tuple[int, int, int, str, str]] = {}
    for path in sorted(root.rglob("*"), key=lambda item: str(item).casefold()):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() and not path.is_symlink() else ""
        snapshot[relative] = (info.st_mode, info.st_size, info.st_mtime_ns, digest, _acl_digest(path))
    return snapshot


def snapshot_digest(snapshot: dict[str, tuple[int, int, int, str, str]]) -> str:
    return hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def api_get(server, capability: str, target: str) -> dict:
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
    connection.request("GET", target, headers={"Host": f"127.0.0.1:{server.server_port}", "X-Explorer-Capability": capability})
    response = connection.getresponse(); body = response.read(); connection.close()
    assert response.status == 200, (target, response.status, body)
    return json.loads(body)["data"]


@pytest.mark.gitfs
@pytest.mark.system
def test_http_acceptance_journeys_leave_sources_git_acl_and_outside_state_immutable(estate, tmp_path, monkeypatch):
    from conftest import git

    sentinel = tmp_path / "helper-invoked.txt"
    if os.name == "nt":
        monitor = tmp_path / "hostile-helper.cmd"
        monitor.write_text(f'@echo invoked>>"{sentinel}"\n@exit /b 1\n', encoding="utf-8")
    else:
        monitor = tmp_path / "hostile-helper.sh"
        monitor.write_text(f'#!/bin/sh\necho invoked > "{sentinel}"\nexit 1\n', encoding="utf-8")
        monitor.chmod(0o755)
    git(estate, "config", "core.fsmonitor", str(monitor))
    git(estate, "config", "core.pager", str(monitor))
    git(estate, "config", "core.editor", str(monitor))
    git(estate, "config", "diff.external", str(monitor))
    git(estate, "config", "credential.helper", str(monitor))
    git(estate, "config", "core.alternateRefsCommand", str(monitor))
    git(estate, "config", "alias.log", f"!{monitor}")
    hook = estate / ".git" / "hooks" / ("post-index-change" + (".cmd" if os.name == "nt" else ""))
    hook.write_text(monitor.read_text(encoding="utf-8"), encoding="utf-8")
    if os.name != "nt": hook.chmod(0o755)
    outside_cwd = tmp_path / "launch-cwd"; outside_cwd.mkdir(); monkeypatch.chdir(outside_cwd)
    before = immutable_snapshot(estate)
    outside_before = immutable_snapshot(outside_cwd)
    runtime = build_runtime(estate)
    server, _ = serve(runtime); thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    try:
        for _ in range(2):
            snapshot = api_get(server, runtime.capability, "/api/v1/estate")
            for source in snapshot["sources"]:
                source_id = source["id"]
                api_get(server, runtime.capability, f"/api/v1/overview?source={source_id}")
                api_get(server, runtime.capability, f"/api/v1/tree?source={source_id}")
                api_get(server, runtime.capability, f"/api/v1/search?source={source_id}&q=md")
                api_get(server, runtime.capability, f"/api/v1/collection?source={source_id}&kind=skills")
                api_get(server, runtime.capability, f"/api/v1/collection?source={source_id}&kind=memory")
                api_get(server, runtime.capability, f"/api/v1/settings?source={source_id}")
            api_get(server, runtime.capability, "/api/v1/document?source=substrate&path=AGENTS.md&mode=rendered")
            api_get(server, runtime.capability, "/api/v1/document?source=substrate&path=AGENTS.md&mode=raw")
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=3)
    after = immutable_snapshot(estate); outside_after = immutable_snapshot(outside_cwd)
    assert after == before
    assert outside_after == outside_before
    assert not sentinel.exists(), "a repository-controlled helper was executed"
    if evidence_path := os.environ.get("EXPLORER_IMMUTABILITY_EVIDENCE"):
        output = Path(evidence_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            "schema": 1, "id": "GT-IMMUTABLE-001", "status": "pass",
            "tool": {"name": "pytest-immutability-oracle", "version": "1"},
            "oracle": "independent relative path/type/mode-or-ACL/size/mtime/content plus complete .git tree snapshot",
            "platform": os.name, "source_entries": len(before), "outside_entries": len(outside_before),
            "before_sha256": snapshot_digest(before), "after_sha256": snapshot_digest(after),
            "outside_before_sha256": snapshot_digest(outside_before), "outside_after_sha256": snapshot_digest(outside_after),
            "journeys": ["estate", "overview", "tree", "search", "skills", "memory", "settings", "document-rendered", "document-raw"],
            "helper_classes": ["fsmonitor", "pager", "editor", "external-diff", "credential", "alternate-refs", "alias", "hook"],
            "excluded": ["atime", "OS read telemetry"],
        }, indent=2) + "\n", encoding="utf-8")
