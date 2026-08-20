"""Leaf helpers for identifying the operative session contract.

The session emitter and validation gate both need this calculation. It is
independent of either service so validation never imports the orchestrator
merely to compare two content fingerprints.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from .hook_contract import MDLLM_ENTRY


def kernel_path() -> Path:
    """Return the framework kernel associated with the installed CLI."""
    return MDLLM_ENTRY.resolve().parents[1] / "kernel.md"


def contract_fingerprint(domain: Path) -> str:
    """Fingerprint the operative Tier-0 definition, not unrelated HEAD."""
    digest = hashlib.sha256()
    for label, path in (("framework-kernel", kernel_path()),
                        ("domain-agents", domain / "AGENTS.md")):
        try:
            raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        except (OSError, UnicodeError):
            raw = "<missing>"
        payload = raw.encode("utf-8")
        digest.update(label.encode("utf-8") + bytes(1))
        digest.update(str(len(payload)).encode("ascii") + bytes(1))
        digest.update(payload)
    return digest.hexdigest()
