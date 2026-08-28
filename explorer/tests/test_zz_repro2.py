from __future__ import annotations
import subprocess
from pathlib import Path
import pytest
from markdownllm_explorer.composition import build_runtime
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.errors import ExplorerError


def git(root: Path, *args: str) -> str:
    r = subprocess.run(["git", "-c", f"safe.directory={root}", *args], cwd=root, text=True, capture_output=True, check=True)
    return r.stdout.strip()


def build(tmp_path):
    root = tmp_path / "substrate"
    root.mkdir()
    (root / "AGENTS.md").write_text("---\nname: F\n---\n# F\n", encoding="utf-8")
    line = ("x" * 63) + "\n"
    (root / "big.md").write_text(line * 16384, encoding="utf-8", newline="")
    git(root, "init", "-b", "main"); git(root, "config", "user.name", "F")
    git(root, "config", "user.email", "f@example.invalid"); git(root, "config", "core.autocrlf", "false")
    git(root, "add", "."); git(root, "commit", "-m", "init")
    return root, git(root, "rev-parse", "HEAD")


def test_patch_budget_starvation_degrades_only_the_marking(tmp_path):
    """Even with the patch budget crushed to 1 byte, the file is still served."""
    root, sha = build(tmp_path)
    runtime = build_runtime(root, limits=ExplorerLimits(diff_output_bytes=1))
    hist = runtime.routes.dispatch("/api/v1/commit-file", {"source": ["substrate"], "sha": [sha], "path": ["big.md"]})
    print("starved patch -> size:", hist.size, "ranges_known:", hist.ranges_known, "ranges:", hist.added_ranges)
    assert hist.size == 1024 * 1024
    assert hist.ranges_known is False and hist.added_ranges == ()


def test_size_gate_is_the_only_producer_of_file_too_large(tmp_path):
    """One byte over: historical refuses with file_too_large, same code as live."""
    root = tmp_path / "substrate"
    root.mkdir()
    (root / "AGENTS.md").write_text("---\nname: F\n---\n# F\n", encoding="utf-8")
    (root / "big.md").write_text("y" * 200, encoding="utf-8", newline="")
    git(root, "init", "-b", "main"); git(root, "config", "user.name", "F")
    git(root, "config", "user.email", "f@example.invalid"); git(root, "config", "core.autocrlf", "false")
    git(root, "add", "."); git(root, "commit", "-m", "init")
    sha = git(root, "rev-parse", "HEAD")
    runtime = build_runtime(root, limits=ExplorerLimits(file_bytes=100))
    codes = {}
    for name, params in (
        ("live", ("/api/v1/document", {"source": ["substrate"], "path": ["big.md"], "mode": ["raw"]})),
        ("hist", ("/api/v1/commit-file", {"source": ["substrate"], "sha": [sha], "path": ["big.md"]})),
    ):
        try:
            runtime.routes.dispatch(*params); codes[name] = "ok"
        except ExplorerError as e:
            codes[name] = e.code
    print("codes:", codes)
    assert codes == {"live": "file_too_large", "hist": "file_too_large"}
