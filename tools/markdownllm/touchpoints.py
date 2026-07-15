"""The Assimilate beat (change-reconciliation.md) as a floor affordance.

Inbound set for one thing: declared edges, structural pointers, provenance
pins, plus the literal-reference grep tier. Human-invoked, never hooked.
"""

from __future__ import annotations

from pathlib import Path

from .model import scan


def cmd_touchpoints(args) -> int:
    """The Assimilate beat (change-reconciliation.md) as a floor affordance.

    Given a thing id, report the COMPLETE declared inbound set — every
    `linked_things` edge, the singular structural pointers (`parent`,
    `definition`), and provenance pins (`informed_by`) that point AT it — plus
    the literal textual references a corpus grep reaches. One read answers "what
    did I just put at risk?" instead of a remembered three-step stitch.

    Two deliberate properties:
    (1) Human-invoked, never wired into the pre-commit hook. The Cue stays the
        driver's ("The Driver Names The Inflection"); this makes the blast
        radius impossible to not see, it does not decide a change is
        consequential or initiate the pass.
    (2) Computed fresh from the live corpus, not from the committed
        `relationships`/`provenance` indexes (which can drift) — assimilation
        must be complete AND current.
    The conceptual residue (a thing that reasons about the target without
    naming it) is the irreducible human walk; no mechanical pass reaches it."""
    root = Path(args.path).resolve()
    target = args.id
    corpus, _ = scan(root)
    if target not in corpus.by_id():
        print(f"mdllm: no thing with id `{target}` in {root}")
        return 1

    declared: list[str] = []
    declared_srcs: set[str] = set()
    for t in corpus.things:
        src = t.id or t.path.name
        if src == target:
            continue
        hits: list[str] = []
        for e in t.meta.get("linked_things") or []:
            if isinstance(e, dict) and e.get("id") == target:
                hits.append(f"(linked_things) relation `{e.get('relation')}`")
        for fieldname in ("parent", "definition"):
            if t.meta.get(fieldname) == target:
                hits.append(f"(structural) via `{fieldname}`")
        for pin in t.meta.get("informed_by") or []:
            if isinstance(pin, dict) and pin.get("id") == target:
                hits.append(f"(provenance) informed_by @{pin.get('commit', '?')}")
        if hits:
            declared_srcs.add(src)
            for h in hits:
                declared.append(f"{src} -> {target}  {h}")

    literal: list[str] = []
    for t in corpus.things:
        src = t.id or t.path.name
        if src == target or src in declared_srcs:
            continue
        if target in t.body:
            literal.append(src)

    print(f"## Touch points of `{target}` — {root}")
    print(f"({len(declared)} declared edge(s), {len(literal)} literal reference(s))\n")
    print("### Declared edges — the floor guarantees this set is complete")
    for d in sorted(declared) or ["- (none declares an edge to this thing)"]:
        print(d if d.startswith("- ") else f"- {d}")
    print("\n### Literal references — the id appears in another body (grep tier)")
    for src in sorted(literal):
        print(f"- {src}")
    if not literal:
        print("- (none)")
    print("\n### Conceptual residue — the human walk")
    print(f"Walk the set above: does each still hold given the change? Then ask "
          f"what reasons about `{target}` WITHOUT naming it — no mechanical pass "
          f"reaches that tier (change-reconciliation.md -> Walking the Dark Region).")
    if not declared and not literal:
        print(f"\nNothing points at `{target}`: a leaf or fresh thing carries no "
              f"consistency risk (change-reconciliation.md -> the premise).")
    return 0
