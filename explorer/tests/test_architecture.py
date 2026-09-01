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
    forbidden_path_methods = {
        "write_text", "write_bytes", "touch", "unlink", "rmdir", "mkdir",
        "rename", "chmod", "symlink_to", "hardlink_to",
    }
    forbidden_module_calls = {
        ("os", name) for name in (
            "remove", "unlink", "rename", "replace", "mkdir", "makedirs",
            "rmdir", "removedirs", "chmod", "symlink", "link",
        )
    } | {
        ("shutil", name) for name in (
            "rmtree", "move", "copy", "copy2", "copyfile", "copytree",
        )
    }
    for path in SOURCE.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        called = {node.func.attr for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)}
        assert not forbidden_path_methods & called, (path, forbidden_path_methods & called)
        qualified = {
            (node.func.value.id, node.func.attr)
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
        }
        assert not forbidden_module_calls & qualified, (path, forbidden_module_calls & qualified)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            is_open = isinstance(node.func, ast.Name) and node.func.id == "open"
            is_path_open = isinstance(node.func, ast.Attribute) and node.func.attr == "open"
            if not (is_open or is_path_open):
                continue
            mode_node = node.args[1] if is_open and len(node.args) > 1 else node.args[0] if is_path_open and node.args else None
            for keyword in node.keywords:
                if keyword.arg == "mode":
                    mode_node = keyword.value
            if isinstance(mode_node, ast.Constant) and isinstance(mode_node.value, str):
                assert not set(mode_node.value) & set("wax+"), (path, mode_node.value)


@pytest.mark.architecture
def test_static_assets_are_native_and_local_only():
    index = (SOURCE / "delivery" / "static" / "index.html").read_text(encoding="utf-8")
    assert "https://" not in index and "http://" not in index
    assert 'type="module"' in index
    assert 'aria-label="Estate navigation"' in index
    assert 'aria-label="Source and document context"' in index
    app = (SOURCE / "delivery" / "static" / "js" / "app.js").read_text(encoding="utf-8")
    routing = (SOURCE / "delivery" / "static" / "js" / "routing.js").read_text(encoding="utf-8")
    activity = (SOURCE / "delivery" / "static" / "js" / "activity.js").read_text(encoding="utf-8")
    theme = (SOURCE / "delivery" / "static" / "js" / "theme.js").read_text(encoding="utf-8")
    assert '["system", "light", "dark"]' in theme
    assert "pushState" in routing and "popstate" in app and "documentSurface" in app
    assert "createActivityController" in activity and "setInterval" not in activity
    assert not (SOURCE / "delivery" / "static" / "node_modules").exists()


@pytest.mark.architecture
def test_windows_packaging_waits_before_replacement_and_keeps_supply_chain_pinned():
    explorer = Path(__file__).parents[1]
    script = (explorer / "packaging" / "windows" / "explorer.nsi").read_text(encoding="utf-8")
    install = script.split('Section "Install" SEC_INSTALL', 1)[1].split("SectionEnd", 1)[0]
    uninstall = script.split('Section "Uninstall"', 1)[1].split("SectionEnd", 1)[0]
    helper_wait = 'ExecWait \'"$PLUGINSDIR\\ExplorerStop\\MarkdownLLM Explorer.exe" --request-exit'
    assert helper_wait in install
    assert install.index(helper_wait) < install.index('RMDir /r "$INSTDIR\\_internal"')
    installed_wait = 'ExecWait \'"$INSTDIR\\MarkdownLLM Explorer.exe" --request-exit'
    assert installed_wait in uninstall
    assert uninstall.index(installed_wait) < uninstall.index('RMDir /r "$INSTDIR"')
    assert install.count("SetErrorLevel 4") == 1 and uninstall.count("SetErrorLevel 4") == 1
    assert all(token in script for token in ("!finalize", "!uninstfinalize", "/fd SHA256", "/tr", "/td SHA256"))

    build = (explorer / "packaging" / "windows" / "build.ps1").read_text(encoding="utf-8")
    assert "56581F90DB321581C5381193D796FFFCF2D24B2F8FED2160A6C6A3BAA67F2C4F" in build
    assert all(token in build for token in ("curl.exe", "--fail", "--location", "nsis-3.12.zip.part"))
    assert build.index("$downloadedNsisHash -ne $expectedNsisHash") < build.index("Move-Item -LiteralPath $nsisDownload")
    assert all(token in build for token in ("SignToolPath", "SignCertificateThumbprint", "TimestampUrl", "SIGN_CERTIFICATE_THUMBPRINT"))


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
    swaps = (
        {
            "adapter": "HTTP server",
            "path": "delivery/swap_http_server.py",
            "source": "from .http_server import serve as _serve\n\ndef serve(runtime, port=0):\n    return _serve(runtime, port)\n",
            "replacements": (
                ("from .delivery.http_server import serve as serve_http", "from .delivery.swap_http_server import serve as serve_http"),
            ),
            "probe": "from markdownllm_explorer.composition import build_runtime, build_server; r=build_runtime(root); s,u=build_server(r,0); assert u.startswith('http://127.0.0.1:'); s.server_close()",
        },
        {
            "adapter": "Git reader",
            "path": "adapters/swap_git_commit_history.py",
            "source": "from .git_commit_history import GitCommitHistory\n\nclass SwapGitCommitHistory(GitCommitHistory):\n    pass\n",
            "replacements": (
                ("from .adapters.git_commit_history import GitCommitHistory, resolve_trusted_git", "from .adapters.git_commit_history import resolve_trusted_git\nfrom .adapters.swap_git_commit_history import SwapGitCommitHistory"),
                ("history = GitCommitHistory(", "history = SwapGitCommitHistory("),
            ),
            "probe": "from markdownllm_explorer.composition import build_runtime; r=build_runtime(root); assert r.routes.dispatch('/api/v1/estate', {}).sources[0].id.value == 'substrate'",
        },
        {
            "adapter": "Filesystem reader",
            "path": "adapters/swap_confined_source_reader.py",
            "source": "from .confined_source_reader import ConfinedSourceReader\n\nclass SwapConfinedSourceReader(ConfinedSourceReader):\n    pass\n",
            "replacements": (
                ("from .adapters.confined_source_reader import ConfinedSourceReader", "from .adapters.swap_confined_source_reader import SwapConfinedSourceReader"),
                ("source_browser = ConfinedSourceReader(", "source_browser = SwapConfinedSourceReader("),
            ),
            "probe": "from markdownllm_explorer.composition import build_runtime; r=build_runtime(root); assert r.routes.dispatch('/api/v1/estate', {}).sources[0].id.value == 'substrate'",
        },
        {
            "adapter": "Markdown renderer",
            "path": "adapters/swap_presenter.py",
            "source": "from .document_presenter import DocumentPresenter\n\nclass SwapPresenter(DocumentPresenter):\n    pass\n",
            "replacements": (
                ("from .adapters.document_presenter import DocumentPresenter", "from .adapters.swap_presenter import SwapPresenter"),
                ("presenter = DocumentPresenter()", "presenter = SwapPresenter()"),
            ),
            "probe": "from markdownllm_explorer.composition import build_runtime; r=build_runtime(root); assert r.routes.dispatch('/api/v1/estate', {}).sources[0].id.value == 'substrate'",
        },
    )
    observations = []
    for index, swap in enumerate(swaps):
        workspace = tmp_path / f"swap-{index}"
        copied_src = workspace / "src"
        package = copied_src / "markdownllm_explorer"
        shutil.copytree(SOURCE, package)
        estate = workspace / "estate"
        estate.mkdir()
        (estate / "AGENTS.md").write_text("# Adapter swap fixture\n", encoding="utf-8")
        before = source_hashes(package)
        adapter_path = package / swap["path"]
        adapter_path.write_text(swap["source"], encoding="utf-8")
        composition = package / "composition.py"
        composition_source = composition.read_text(encoding="utf-8")
        for old, new in swap["replacements"]:
            assert old in composition_source, (swap["adapter"], old)
            composition_source = composition_source.replace(old, new)
        composition.write_text(composition_source, encoding="utf-8")
        after = source_hashes(package)
        changed = sorted(path for path in set(before) | set(after) if before.get(path) != after.get(path))
        assert changed == sorted([swap["path"], "composition.py"])
        assert not any(path.startswith(("core/", "application/")) for path in changed)
        environment = {"PYTHONPATH": str(copied_src), "PYTHONDONTWRITEBYTECODE": "1"}
        for name in ("SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP"):
            if environment_value := os.environ.get(name):
                environment[name] = environment_value
        probe_source = f"from pathlib import Path; root=Path(__import__('sys').argv[1]); {swap['probe']}"
        probe = subprocess.run(
            [sys.executable, "-c", probe_source, str(estate)],
            env=environment, cwd=workspace, capture_output=True, text=True, timeout=15,
        )
        assert probe.returncode == 0, (swap["adapter"], probe.stderr)
        observations.append({
            "adapter": swap["adapter"],
            "changed_paths": changed,
            "forbidden_inner_changes": [],
            "runtime_probe": "pass",
        })
    if evidence_path := os.environ.get("EXPLORER_SWAP_EVIDENCE"):
        output = Path(evidence_path); output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({
            "schema": 2, "id": "AT-SWAP-001", "status": "pass",
            "tool": {"name": "pytest-adapter-swap-oracle", "version": "2"},
            "swaps": observations,
        }, indent=2) + "\n", encoding="utf-8")


@pytest.mark.architecture
def test_browser_state_declares_current_request_pagination_and_accessibility_algorithms():
    static = SOURCE / "delivery" / "static"
    state_js = (static / "js" / "state.js").read_text(encoding="utf-8")
    app_js = (static / "js" / "app.js").read_text(encoding="utf-8")
    activity_js = (static / "js" / "activity.js").read_text(encoding="utf-8")
    overlays_js = (static / "js" / "overlays.js").read_text(encoding="utf-8")
    nav_js = (static / "js" / "views" / "navigation.js").read_text(encoding="utf-8")
    index = (static / "index.html").read_text(encoding="utf-8")
    assert "requests: new Map()" in state_js and "identityKey" in state_js and "abortAllRequests" in state_js and "documentSurface" in state_js
    assert all(operation in app_js for operation in ('beginRequest("view"', 'beginRequest("document"', 'beginRequest("search"', 'beginRequest("context"', "treeCursors", "treePartials"))
    assert all(key in nav_js for key in ("aria-expanded", "aria-selected", "aria-level", "ArrowRight", "ArrowLeft", "Home", "End"))
    assert 'role="tablist"' in index and 'role="tabpanel"' in index
    assert 'aria-modal", "true"' in overlays_js and ".inert = true" in overlays_js
    assert all(event in activity_js for event in ("pointerdown", "keydown", "touchstart", "scroll"))
    assert "setInterval" not in activity_js and "sendTouch" in activity_js
    for view in (static / "js" / "views").glob("*.js"):
        source = view.read_text(encoding="utf-8")
        assert "fetch(" not in source, view
        assert not re.search(r"(?:label|title|path|message)\.innerHTML\s*=", source), view
    composition = (SOURCE / "composition.py").read_text(encoding="utf-8")
    assert "resolve_trusted_git(root)" in composition
