#!/usr/bin/env python3
"""Measure actual token costs of framework specs, grouped by loading tier.

Phase 0 of the framework-v3-transformation-plan: replace asserted tier costs
in AGENTS.md with measured ones. Becomes `mdllm tokens` in Phase 1.

Uses tiktoken (o200k_base) when available; falls back to a chars/3.8 heuristic
(typical for English markdown) and labels the output accordingly.

Usage: python tools/measure-tokens.py [framework-root]
"""

import sys
from pathlib import Path

TIERS = {
    "Tier 0 (always)": [
        "AGENTS.md",
        "thing.md",
        "orchestration.md",
    ],
    "Tier 1 (read/write/commit sessions)": [
        "read.thing.md",
        "write.thing.md",
        "validate.thing.md",
        "git-workflow.md",
    ],
    "Tier 2 (on demand)": [
        "domain-specification-guide.md",
        "scalability-guide.md",
        "thing-lifecycle.md",
        "llm-driven-systems.manifesto.md",
        "interface.md",
        "framework-discovery.md",
        "domain-refresh.md",
        "session-memory.md",
        "belief-revision.md",
        "retrospective.md",
        "trigger-specification.md",
        "derived-index.md",
        "example-things.md",
        "reasoning-lenses.md",
    ],
}


def get_counter():
    try:
        import tiktoken

        enc = tiktoken.get_encoding("o200k_base")
        return lambda text: len(enc.encode(text)), "tiktoken o200k_base"
    except ImportError:
        return lambda text: round(len(text) / 3.8), "heuristic chars/3.8"


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    count, method = get_counter()

    print(f"Token measurement ({method})  root={root}\n")
    grand_total = 0
    tier_totals = {}

    for tier, files in TIERS.items():
        print(f"## {tier}")
        tier_total = 0
        for name in files:
            path = root / name
            if not path.exists():
                print(f"  {name:<40} MISSING")
                continue
            tokens = count(path.read_text(encoding="utf-8"))
            tier_total += tokens
            print(f"  {name:<40} {tokens:>7,}")
        tier_totals[tier] = tier_total
        grand_total += tier_total
        print(f"  {'TIER TOTAL':<40} {tier_total:>7,}\n")

    print(f"{'FULL LOAD (all tiers)':<42} {grand_total:>7,}")
    t0 = tier_totals.get("Tier 0 (always)", 0)
    t1 = tier_totals.get("Tier 1 (read/write/commit sessions)", 0)
    print(f"{'Tier 0 alone':<42} {t0:>7,}")
    print(f"{'Tier 0 + Tier 1':<42} {t0 + t1:>7,}")


if __name__ == "__main__":
    main()
