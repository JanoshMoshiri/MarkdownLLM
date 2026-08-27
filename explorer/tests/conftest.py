from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def write(path: Path, content: str | bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-c", f"safe.directory={root}", *args], cwd=root, text=True, capture_output=True, check=True)
    return result.stdout.strip()


@pytest.fixture
def estate(tmp_path: Path) -> Path:
    root = tmp_path / "substrate"
    root.mkdir()
    write(root / "AGENTS.md", "---\nname: Fixture\n---\n# Fixture substrate\n\n[Skill](skills/demo.md)\n")
    write(root / "README.md", "# Read me\n")
    write(root / "skills" / "demo.md", "---\nid: demo\ntype: skill\n---\n# Demo Skill\n\n**Safe** content.\n")
    write(root / "things" / "insights" / "one.md", "---\nid: shared\ntype: insight\n---\n# First insight\n")
    write(root / "things" / "insights" / "two.md", "---\nid: shared\ntype: conflict\n---\n# Second insight\n")
    write(root / ".env", "SECRET=never")
    write(root / "secret-token.md", "never")
    write(root / "binary.md", b"text\x00binary")
    write(root / "latin.md", b"caf\xe9")
    write(root / "script.py", "print('plain text only')\n")
    write(root / "domain" / "demo" / "AGENTS.md", "# Demo domain\n")
    write(root / "domain" / "demo" / "skills" / "domain.skill.md", "# Domain skill\n")
    write(root / "domain" / "demo" / "things" / "decisions" / "choice.md", "# Choice\n")
    write(root / "domain" / "unmarked" / "README.md", "# Not a domain\n")
    write(root / "domain" / "marked-non-git" / ".markdownllm", "version: 1\n")
    git(root, "init", "-b", "main")
    git(root, "config", "user.name", "Fixture User")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "add", ".")
    git(root, "commit", "-m", "fixture: initial")
    demo = root / "domain" / "demo"
    git(demo, "init", "-b", "main")
    git(demo, "config", "user.name", "Domain User")
    git(demo, "config", "user.email", "domain@example.invalid")
    git(demo, "add", ".")
    git(demo, "commit", "-m", "domain: initial")
    return root
