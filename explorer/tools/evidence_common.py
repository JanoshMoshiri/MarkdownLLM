"""Shared hashing primitives for the retained Explorer evidence bundle."""

from __future__ import annotations

import hashlib
from pathlib import Path


SUBJECT_ALGORITHM = "explorer-subject-tree-sha256-v1"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def subject_sha256(explorer: Path) -> str:
    """Hash the reviewable product/spec/test subject, excluding generated evidence."""
    explorer = explorer.resolve()
    roots = [explorer / "src", explorer / "tests", explorer / "tools", explorer / "docs"]
    files: list[Path] = [explorer / "pyproject.toml", explorer / "README.md"]
    for root in roots:
        if root.is_dir():
            files.extend(path for path in root.rglob("*") if path.is_file())
    filtered = []
    for path in files:
        relative = path.relative_to(explorer)
        parts = relative.parts
        if "evidence" in parts or "__pycache__" in parts or any(part.endswith((".egg-info", ".pyc")) for part in parts):
            continue
        filtered.append(path)
    digest = hashlib.sha256()
    for path in sorted(set(filtered), key=lambda item: item.relative_to(explorer).as_posix()):
        relative = path.relative_to(explorer).as_posix().encode("utf-8")
        content_hash = bytes.fromhex(file_sha256(path))
        digest.update(len(relative).to_bytes(4, "big")); digest.update(relative); digest.update(content_hash)
    return digest.hexdigest()
