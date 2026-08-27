from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


SOURCE = Path(os.environ.get("EXPLORER_MUTANT_SOURCE", Path(__file__).parents[1] / "src" / "markdownllm_explorer"))


def imports(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import): found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module: found.add(node.module)
    return found


def source_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*.py")
    }


@pytest.mark.architecture
def test_core_has_no_outer_layer_imports():
    for path in (SOURCE / "core").glob("*.py"):
        names = imports(path)
        assert not any(name.startswith("markdownllm_explorer.application") or name.startswith("markdownllm_explorer.adapters") or name.startswith("markdownllm_explorer.delivery") for name in names), path
        assert not ({"pathlib", "os", "subprocess", "http.server"} & names), path


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


@pytest.mark.architecture
def test_use_cases_depend_on_focused_ports_and_public_encoding_is_explicit():
    ports = (SOURCE / "application" / "ports.py").read_text(encoding="utf-8")
    for protocol in ("SourceMetrics", "TreeReader", "PathSearcher", "CollectionReader", "DocumentReader", "SettingsReader"):
        assert f"class {protocol}(Protocol)" in ports
    assert "class SourceBrowser" not in ports
    reader = (SOURCE / "adapters" / "confined_source_reader.py").read_text(encoding="utf-8")
    assert "def collection(" not in reader and "SafeMarkdownParser" not in reader and "DocumentPresenter" not in reader
    encoder = (SOURCE / "delivery" / "response_encoding.py").read_text(encoding="utf-8")
    assert "asdict" not in encoder and "is_dataclass" not in encoder and "unsupported response value" in encoder
    routes = (SOURCE / "delivery" / "api_routes.py").read_text(encoding="utf-8")
    assert ": object" not in routes


@pytest.mark.architecture
def test_adapter_swap_changes_only_composition_and_outer_adapter(tmp_path):
    copied_src = tmp_path / "src"; package = copied_src / "markdownllm_explorer"
    shutil.copytree(SOURCE, package)
    before = source_hashes(package)
    (package / "adapters" / "swap_presenter.py").write_text(
        "from .document_presenter import DocumentPresenter\n\nclass SwapPresenter(DocumentPresenter):\n    pass\n",
        encoding="utf-8",
    )
    composition = package / "composition.py"
    value = composition.read_text(encoding="utf-8").replace(
        "from .adapters.document_presenter import DocumentPresenter",
        "from .adapters.swap_presenter import SwapPresenter",
    ).replace("presenter = DocumentPresenter()", "presenter = SwapPresenter()")
    composition.write_text(value, encoding="utf-8")
    after = source_hashes(package)
    changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
    assert changed == ["adapters/swap_presenter.py", "composition.py"]
    assert not any(path.startswith(("core/", "application/")) for path in changed)
    environment = {"PYTHONPATH": str(copied_src), "PYTHONDONTWRITEBYTECODE": "1"}
    for name in ("SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP"):
        if value := os.environ.get(name): environment[name] = value
    probe = subprocess.run(
        [sys.executable, "-c", "from pathlib import Path; from markdownllm_explorer.composition import build_runtime; r=build_runtime(Path(__import__('sys').argv[1])); assert r.routes.dispatch('/api/v1/estate', {}).sources[0].id.value == 'substrate'", str(tmp_path)],
        env=environment, cwd=tmp_path, capture_output=True, text=True, timeout=15,
    )
    assert probe.returncode == 0, probe.stderr
    if evidence_path := os.environ.get("EXPLORER_SWAP_EVIDENCE"):
        output = Path(evidence_path); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            "schema": 1, "id": "AT-SWAP-001", "status": "pass", "adapter": "Markdown presenter",
            "tool": {"name": "pytest-adapter-swap-oracle", "version": "1"},
            "changed_paths": changed, "forbidden_inner_changes": [], "runtime_probe": "pass",
        }, indent=2) + "\n", encoding="utf-8")


@pytest.mark.architecture
def test_browser_state_declares_current_request_pagination_and_accessibility_algorithms():
    static = SOURCE / "delivery" / "static"
    state_js = (static / "js" / "state.js").read_text(encoding="utf-8")
    app_js = (static / "js" / "app.js").read_text(encoding="utf-8")
    nav_js = (static / "js" / "views" / "navigation.js").read_text(encoding="utf-8")
    index = (static / "index.html").read_text(encoding="utf-8")
    assert "requests: new Map()" in state_js and "identityKey" in state_js and "abortAllRequests" in state_js
    assert all(operation in app_js for operation in ('beginRequest("view"', 'beginRequest("document"', 'beginRequest("search"', 'beginRequest("context"', "treeCursors"))
    assert all(key in nav_js for key in ("aria-expanded", "aria-selected", "aria-level", "ArrowRight", "ArrowLeft", "Home", "End"))
    assert 'role="tablist"' in index and 'role="tabpanel"' in index
    assert 'aria-modal", "true"' in app_js and ".inert = true" in app_js
    for view in (static / "js" / "views").glob("*.js"):
        source = view.read_text(encoding="utf-8")
        assert "fetch(" not in source, view
        assert not re.search(r"(?:label|title|path|message)\.innerHTML\s*=", source), view
    composition = (SOURCE / "composition.py").read_text(encoding="utf-8")
    assert "resolve_trusted_git(root)" in composition
