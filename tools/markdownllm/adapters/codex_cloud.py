"""Codex Cloud distribution edge; separate from project lifecycle hooks."""
from __future__ import annotations

import json
from pathlib import Path


def settings(config) -> dict[str, str]:
    return {
        "repository": config["domain_repo"],
        "workspace_directory": config["workspace_directory"],
        "setup_mode": "Manual",
        "setup_command": "bash .codex/cloud/bootstrap.sh",
        "maintenance_command": "bash .codex/cloud/bootstrap.sh maintenance",
        "agent_internet": "Off (enable only for the task's needs)",
    }


def artifacts(source_root: Path, config) -> dict[str, bytes]:
    templates = source_root / "templates" / "codex-cloud"
    result = {
        ".codex/cloud/environment.json": (json.dumps(config, indent=2) + "\n").encode(),
        ".codex/cloud/bootstrap.py": (source_root / "tools/markdownllm/cloud_bootstrap.py").read_text(encoding="utf-8").encode(),
        ".agents/skills/configure-codex-cloud/SKILL.md": (source_root / ".agents/skills/configure-codex-cloud/SKILL.md").read_text(encoding="utf-8").encode(),
    }
    for source, target in (
        ("bootstrap.sh.template", ".codex/cloud/bootstrap.sh"),
        ("SETUP.md.template", ".codex/cloud/SETUP.md"),
    ):
        text = (templates / source).read_text(encoding="utf-8")
        for key, value in settings(config).items():
            text = text.replace("{{" + key + "}}", value)
        result[target] = text.encode("utf-8")
    return result
