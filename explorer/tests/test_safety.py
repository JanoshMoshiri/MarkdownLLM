from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from markdownllm_explorer.composition import build_runtime


def immutable_snapshot(root: Path) -> dict[str, tuple[int, int, int, str]]:
    snapshot: dict[str, tuple[int, int, int, str]] = {}
    for path in sorted(root.rglob("*"), key=lambda item: str(item).casefold()):
        relative = path.relative_to(root).as_posix()
        info = path.lstat()
        digest = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() and not path.is_symlink() else ""
        snapshot[relative] = (info.st_mode, info.st_size, info.st_mtime_ns, digest)
    return snapshot


@pytest.mark.gitfs
@pytest.mark.system
def test_full_acceptance_journeys_leave_source_and_git_state_immutable(estate, tmp_path):
    from conftest import git

    sentinel = tmp_path / "fsmonitor-invoked.txt"
    if os.name == "nt":
        monitor = tmp_path / "hostile-fsmonitor.cmd"
        monitor.write_text(f'@echo invoked>"{sentinel}"\n@exit /b 1\n', encoding="utf-8")
    else:
        monitor = tmp_path / "hostile-fsmonitor.sh"
        monitor.write_text(f'#!/bin/sh\necho invoked > "{sentinel}"\nexit 1\n', encoding="utf-8")
        monitor.chmod(0o755)
    git(estate, "config", "core.fsmonitor", str(monitor))
    before = immutable_snapshot(estate)
    runtime = build_runtime(estate)
    routes = runtime.routes
    for _ in range(2):
        estate_snapshot = routes.dispatch("/api/v1/estate", {})
        for source in estate_snapshot.sources:
            source_query = {"source": [source.id.value]}
            routes.dispatch("/api/v1/overview", source_query)
            routes.dispatch("/api/v1/tree", source_query)
            routes.dispatch("/api/v1/search", {**source_query, "q": ["md"]})
            routes.dispatch("/api/v1/collection", {**source_query, "kind": ["skills"]})
            routes.dispatch("/api/v1/collection", {**source_query, "kind": ["memory"]})
            routes.dispatch("/api/v1/settings", source_query)
        routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["AGENTS.md"], "mode": ["rendered"]})
        routes.dispatch("/api/v1/document", {"source": ["substrate"], "path": ["AGENTS.md"], "mode": ["raw"]})
    assert immutable_snapshot(estate) == before
    assert not sentinel.exists(), "repository-controlled fsmonitor was executed"
