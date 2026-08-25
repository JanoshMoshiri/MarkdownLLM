"""Framework-repo state: git HEAD, the version sentinel, the loading-tier map.

Small shared readers/declarations of the framework's own repo structure —
consumed by indexes, kernel generation, tokens, coherence, refresh, doctor,
and the MCP face. Version comparison lives here for the same reason.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .yaml_loader import load_version_sentinel

def git_short_sha(root: Path) -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=root,
                              capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def framework_version(root: Path) -> str:
    p = root
    for _ in range(4):
        f = p / ".markdownllm"
        if f.exists():
            data = load_version_sentinel(
                f.read_text(encoding="utf-8"), source=f)
            return str(data.get("version", "unknown"))
        p = p.parent
    return "unknown"


def version_lt(a: str, b: str) -> bool:
    """Semver-ish less-than over dotted numeric versions, tolerant of junk."""
    def parts(v: str):
        out = []
        for chunk in str(v).split("."):
            num = "".join(ch for ch in chunk if ch.isdigit())
            out.append(int(num) if num else 0)
        return out
    pa, pb = parts(a), parts(b)
    n = max(len(pa), len(pb))
    pa += [0] * (n - len(pa))
    pb += [0] * (n - len(pb))
    return pa < pb


TIERS = {
    "Tier 0 (always)": ["AGENTS.md", "kernel.md"],
    "Tier 1 (full specs, load individually on demand)": [
        "thing.md", "orchestration.md", "read.thing.md", "write.thing.md",
        "validate.thing.md", "git-workflow.md"],
    # thing-lifecycle.md is deliberately absent: it is a draft rotting against
    # the live tool (review 5) and stays out of the loading map — and out of
    # the .markdownllm catalog — until reconciled. The coherence check enforces
    # that this map and the catalog agree in BOTH directions.
    "Tier 2 (on demand)": [
        "domain-specification-guide.md", "scalability-guide.md",
        "llm-driven-systems.manifesto.md", "interface.md", "framework-discovery.md",
        "domain-refresh.md", "session-memory.md", "belief-revision.md",
        "retrospective.md", "trigger-specification.md", "derived-index.md",
        "example-things.md", "reasoning-lenses.md", "provenance.md",
        "change-reconciliation.md", "workflow-state.md", "coordination-claim.md",
        "operating-model.md", "universal-workflow.md",
    ],
}

