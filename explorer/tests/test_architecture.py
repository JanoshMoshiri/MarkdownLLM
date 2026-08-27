from __future__ import annotations

import ast
from pathlib import Path

import pytest


SOURCE = Path(__file__).parents[1] / "src" / "markdownllm_explorer"


def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module: found.add(node.module)
    return found


@pytest.mark.architecture
def test_core_has_no_outer_layer_imports():
    for path in (SOURCE / "core").glob("*.py"):
        assert not any(name.startswith("markdownllm_explorer.application") or name.startswith("markdownllm_explorer.adapters") or name.startswith("markdownllm_explorer.delivery") for name in imports(path)), path


@pytest.mark.architecture
def test_application_has_no_infrastructure_or_delivery_imports():
    for path in (SOURCE / "application").glob("*.py"):
        names = imports(path)
        assert not any(name.startswith("markdownllm_explorer.adapters") or name.startswith("markdownllm_explorer.delivery") for name in names), path
        assert not ({"subprocess", "http.server", "pathlib"} & names), path


@pytest.mark.architecture
def test_filesystem_and_git_mutation_calls_are_absent_from_runtime():
    forbidden = {"write_text", "write_bytes", "unlink", "rmdir", "mkdir", "rename", "chmod"}
    for path in SOURCE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        called = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        assert not forbidden & called, (path, forbidden & called)


@pytest.mark.architecture
def test_static_assets_are_native_and_local_only():
    index = (SOURCE / "delivery" / "static" / "index.html").read_text(encoding="utf-8")
    assert "https://" not in index and "http://" not in index
    assert 'type="module"' in index
    assert 'aria-label="Estate navigation"' in index
    assert 'aria-label="Source and document context"' in index
    app = (SOURCE / "delivery" / "static" / "js" / "app.js").read_text(encoding="utf-8")
    assert '["system", "light", "dark"]' in app
    assert "pushState" in app and "popstate" in app
    assert not (SOURCE / "delivery" / "static" / "node_modules").exists()
