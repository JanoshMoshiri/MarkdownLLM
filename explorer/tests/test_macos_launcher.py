from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).parents[2]
LAUNCHER = ROOT / "tools" / "open-explorer.sh"


@pytest.mark.architecture
def test_macos_launcher_contract_is_safe_and_agent_friendly():
    text = LAUNCHER.read_text(encoding="utf-8")
    assert text.startswith("#!/usr/bin/env bash\nset -euo pipefail")
    assert "Library/Application Support/MarkdownLLM Explorer/portable" in text
    assert 'framework_root="$(cd "${script_dir}/.." && pwd -P)"' in text
    assert "sys.version_info >= (3, 10)" in text
    assert '"${framework_root}/explorer"' in text
    assert "mdllm-explorer" in text and "--open-browser" in text and "--stop" in text
    assert 'ps -ww -p "${pid}" -o command=' in text
    assert '"${command_line}" == *"${framework_root}"*' in text
    assert ">/dev/null" in text and 'rm -f "${error_file}"' in text
    assert "sudo" not in text and "LaunchAgent" not in text


@pytest.mark.system
def test_macos_launcher_rejects_non_darwin_without_mutation(tmp_path):
    if os.name == "posix" and os.uname().sysname == "Darwin":
        pytest.skip("non-Darwin rejection requires a non-Mac host")
    bash = str(Path("C:/Program Files/Git/bin/bash.exe")) if os.name == "nt" and Path("C:/Program Files/Git/bin/bash.exe").is_file() else shutil.which("bash")
    if not bash:
        pytest.skip("bash is unavailable on this host")
    environment = dict(os.environ)
    environment["HOME"] = str(tmp_path)

    result = subprocess.run([bash, str(LAUNCHER)], cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=5)

    assert result.returncode == 2 and "for macOS" in result.stderr
    assert list(tmp_path.iterdir()) == []
