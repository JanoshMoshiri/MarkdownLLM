from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


def node_executable() -> str | None:
    if configured := os.environ.get("EXPLORER_NODE"):
        return configured
    if discovered := shutil.which("node"):
        return discovered
    bundled = Path.home() / ".cache" / "codex-runtimes" / "codex-primary-runtime" / "dependencies" / "node" / "bin" / "node.exe"
    return str(bundled) if bundled.is_file() else None


@pytest.mark.system
def test_browser_request_state_rejects_a_after_b_and_isolates_operations(tmp_path):
    node = node_executable()
    if not node:
        pytest.skip("Node runtime is unavailable; browser runtime evidence remains required")
    source_root = Path(os.environ.get("EXPLORER_MUTANT_SOURCE", Path(__file__).parents[1] / "src" / "markdownllm_explorer"))
    module = tmp_path / "state.mjs"
    module.write_text((source_root / "delivery" / "static" / "js" / "state.js").read_text(encoding="utf-8"), encoding="utf-8")
    harness = tmp_path / "oracle.mjs"
    harness.write_text(
        "import {pathToFileURL} from 'node:url';\n"
        "const m = await import(pathToFileURL(process.argv[2]));\n"
        "m.state.source = {id:'s'}; m.state.view = 'skills'; m.state.selectedPath = 'a.md'; m.state.documentMode = 'rendered';\n"
        "const a = m.beginRequest('document', {source:'s',tab:'skills',path:'a.md',mode:'rendered'});\n"
        "const b = m.beginRequest('document', {source:'s',tab:'skills',path:'b.md',mode:'rendered'});\n"
        "if (!a.signal.aborted || m.isCurrent(a) || !m.isCurrent(b)) throw new Error('stale document response accepted');\n"
        "const search = m.beginRequest('search', {source:'s',tab:'skills',query:'a',cursor:null});\n"
        "if (!m.isCurrent(b) || !m.isCurrent(search)) throw new Error('operations were not isolated');\n"
        "m.state.view = 'overview';\n"
        "if (m.isCurrent(b) || m.isCurrent(search)) throw new Error('old tab context remained current');\n"
        "m.state.view = 'skills'; m.state.selectedPath = 'b.md'; m.state.search.query = 'a';\n"
        "const clearable = m.beginRequest('search', {source:'s',tab:'skills',query:'a',cursor:null});\n"
        "m.state.search.query = '';\n"
        "if (m.isCurrent(clearable)) throw new Error('cleared search remained current');\n"
        "const sourceRequest = m.beginRequest('context', {source:'s'}); m.state.source = {id:'other'};\n"
        "if (m.isCurrent(sourceRequest)) throw new Error('old source context remained current');\n"
        "m.abortAllRequests();\n"
        "if (!b.signal.aborted || !search.signal.aborted || !sourceRequest.signal.aborted) throw new Error('transition did not abort requests');\n",
        encoding="utf-8",
    )
    result = subprocess.run([node, str(harness), str(module)], capture_output=True, text=True, timeout=5)
    assert result.returncode == 0, result.stderr
