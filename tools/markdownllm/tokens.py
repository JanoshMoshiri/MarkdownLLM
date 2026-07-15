"""Token measurement of the loading tiers (`mdllm tokens`).

tiktoken when available, chars/3.8 heuristic otherwise. Prose never restates
the figures — this command is the measurement.
"""

from __future__ import annotations

from pathlib import Path

from .repo import TIERS

def cmd_tokens(args) -> int:
    root = Path(args.path).resolve()
    try:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        count, method = (lambda s: len(enc.encode(s))), "tiktoken o200k_base"
    except ImportError:
        count, method = (lambda s: round(len(s) / 3.8)), "heuristic chars/3.8"
    print(f"Token measurement ({method})  root={root}\n")
    totals = {}
    for tier, files in TIERS.items():
        print(f"## {tier}")
        total = 0
        for name in files:
            p = root / name
            if not p.exists():
                continue
            n = count(p.read_text(encoding="utf-8"))
            total += n
            print(f"  {name:<40} {n:>7,}")
        totals[tier] = total
        print(f"  {'TIER TOTAL':<40} {total:>7,}\n")
    t0 = totals.get("Tier 0 (always)", 0)
    print(f"{'FULL LOAD':<42} {sum(totals.values()):>7,}")
    print(f"{'Tier 0 (AGENTS.md + kernel.md)':<42} {t0:>7,}")
    return 0
