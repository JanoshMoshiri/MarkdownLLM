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


@pytest.mark.system
def test_document_surface_and_activity_state_machines(tmp_path):
    node = node_executable()
    if not node:
        pytest.skip("Node runtime is unavailable; browser runtime evidence remains required")
    source_root = Path(__file__).parents[1] / "src" / "markdownllm_explorer" / "delivery" / "static" / "js"
    app_source = (source_root / "app.js").read_text(encoding="utf-8")
    assert "Ask Claude Code to open it again." in app_source
    modules = {}
    for name in ("state", "routing", "activity"):
        target = tmp_path / f"{name}.mjs"
        target.write_text((source_root / f"{name}.js").read_text(encoding="utf-8"), encoding="utf-8")
        modules[name] = target
    harness = tmp_path / "surface-activity-oracle.mjs"
    harness.write_text(
        "import {pathToFileURL} from 'node:url';\n"
        "const stateModule = await import(pathToFileURL(process.argv[2]));\n"
        "const routing = await import(pathToFileURL(process.argv[3]));\n"
        "const activity = await import(pathToFileURL(process.argv[4]));\n"
        "const routed = routing.routeFromText('#source=s&tab=memory&mode=rendered&path=things%2Fplans%2Fa.md&surface=standalone');\n"
        "if (routed.surface !== 'standalone' || routing.validDocumentSurface('collection') !== 'collection' || routing.validDocumentSurface('wrong') !== null) throw new Error('surface route validation failed');\n"
        "let written = ''; globalThis.history = {pushState:(_a,_b,url)=>{written=url}, replaceState:(_a,_b,url)=>{written=url}};\n"
        "const s = stateModule.state; s.source={id:'s'}; s.view='memory'; s.documentMode='rendered'; s.selectedPath='things/plans/a.md'; s.documentSurface='standalone'; s.commit=null;\n"
        "routing.writeRoute(s); if (!written.includes('surface=standalone') || !written.includes('path=things%2Fplans%2Fa.md')) throw new Error('surface was not persisted');\n"
        "const request = stateModule.beginRequest('document', {source:'s',path:s.selectedPath,surface:'standalone'}); s.documentSurface='collection';\n"
        "if (stateModule.isCurrent(request)) throw new Error('response from the wrong document surface remained current');\n"
        "let clock=0, serial=0, touches=0, expiries=0; const timers=new Map();\n"
        "const setTimer=(callback,delay)=>{const id=++serial; timers.set(id,{callback,due:clock+delay}); return id}; const clearTimer=id=>timers.delete(id);\n"
        "const advance=amount=>{clock+=amount; let ready=[...timers].filter(([,v])=>v.due<=clock); while(ready.length){for(const [id,v] of ready){timers.delete(id); v.callback()} ready=[...timers].filter(([,v])=>v.due<=clock)}};\n"
        "const controller=activity.createActivityController({timeoutMs:100,sendTouch:()=>{touches++},onExpire:()=>{expiries++},now:()=>clock,setTimer,clearTimer,touchIntervalMs:60});\n"
        "controller.start(); advance(50); controller.recordActivity(); advance(70); if (expiries || touches!==1) throw new Error('activity did not renew without early expiry');\n"
        "controller.recordActivity(); if (touches!==2) throw new Error('throttled touch did not resume after interval'); advance(99); if (expiries) throw new Error('renewed lease expired early'); advance(1);\n"
        "if (expiries!==1 || !controller.isExpired()) throw new Error('idle lease did not expire exactly once'); controller.recordActivity(); if(touches!==2) throw new Error('expired controller sent activity');\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [node, str(harness), str(modules["state"]), str(modules["routing"]), str(modules["activity"])],
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0, result.stderr
