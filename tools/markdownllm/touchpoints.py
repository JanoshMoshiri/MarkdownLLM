"""The Assimilate beat (change-reconciliation.md) as a floor affordance.

Inbound set for one thing: declared edges, structural pointers, provenance
pins, plus the literal-reference grep tier. Human-invoked, never hooked.

`candidates` is the companion the deep dive of 2026-08-04 added
(`inflection-candidates-are-computable`): the cue VERDICT stays human and
`touchpoints` stays invoked-never-hooked — but the cue QUESTION (does anything
reason from what was just modified?) is a mechanical predicate, and the
pre-commit hook asks it in one advisory line. Modified ∧ reasoned-from;
additions are skipped by the spec's own premise (a fresh thing on a clean
slate carries no consistency risk). Never blocks, never scores, never runs
the pass.
"""

from __future__ import annotations

import subprocess
from collections import Counter
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


# Types whose entire function is to be reasoned from — modification is a cue
# candidate regardless of fan-in. Data things qualify by fan-in instead.
# `insight` and `decision` joined at v3.26.1: both meet this set's own
# criterion (an insight exists only to be reasoned from; a decision is
# reasoned-from the moment anything cites it), and the operator felt the
# gap live — porch-bound insights modified with no cue (substrate-currency-sweep).
DEFINITION_SURFACE_TYPES = {"specification", "skill", "guide", "manifesto",
                            "prompt", "workflow-definition", "insight",
                            "decision"}
FAN_IN_THRESHOLD = 3  # inbound edges at which an ordinary thing is "reasoned-from"


def _inbound_counts(corpus) -> Counter:
    """Inbound edge count per target id: linked_things + structural pointers +
    provenance pins — the same edge set touchpoints walks, counted."""
    counts: Counter = Counter()
    for t in corpus.things:
        for e in t.meta.get("linked_things") or []:
            if isinstance(e, dict) and e.get("id"):
                counts[e["id"]] += 1
        for fieldname in ("parent", "definition"):
            if t.meta.get(fieldname):
                counts[t.meta[fieldname]] += 1
        for pin in t.meta.get("informed_by") or []:
            if isinstance(pin, dict) and pin.get("id"):
                counts[pin["id"]] += 1
    return counts


def cmd_candidates(args) -> int:
    """Advisory, exit 0 always: for each STAGED MODIFIED thing, say whether a
    cue question exists (reasoned-from) and whether the change publishes
    (exposed on the porch). Saying no to a named question is a decision;
    not being asked was drift."""
    root = Path(args.path).resolve()
    try:
        r = subprocess.run(["git", "diff", "--cached", "--name-status"],
                           cwd=root, capture_output=True, text=True, timeout=20)
    except Exception:
        return 0
    if r.returncode != 0:
        return 0
    modified: list[str] = []
    for line in r.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0].startswith("M") and parts[-1].endswith(".md"):
            modified.append(parts[-1])
    if not modified:
        return 0

    corpus, _ = scan(root)
    by_path = {t.path.resolve(): t for t in corpus.things}
    inbound = None  # computed lazily — most commits touch no reasoned-from thing
    lines: list[str] = []
    for rel in modified:
        t = by_path.get((root / rel).resolve())
        if t is None or not t.id:
            continue
        if t.meta.get("exposed") is True:
            lines.append(f"porch: `{t.id}` is exposed — this change publishes; "
                         f"consumers' pins go stale on their next imports-check.")
        typ = t.meta.get("type")
        if typ in DEFINITION_SURFACE_TYPES:
            reason = f"definition surface (`{typ}`)"
        else:
            if inbound is None:
                inbound = _inbound_counts(corpus)
            n = inbound.get(t.id, 0)
            if n < FAN_IN_THRESHOLD:
                continue
            reason = f"{n} inbound edge(s)"
        lines.append(f"cue: `{t.id}` is reasoned-from ({reason}) — inflection? "
                     f"`mdllm touchpoints {t.id}`")
    if lines:
        print("-- change-reconciliation advisories (never blocking) --")
        for ln in lines:
            print(ln)
    return 0
