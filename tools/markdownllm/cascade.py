"""The post-completion cascade (write.thing.md) as a floor affordance.

Mirror of touchpoints: the outbound/downstream set a completion unblocks —
unblock candidates, partial progress, parent rollup, trigger watchers.
Reports, never applies.
"""

from __future__ import annotations

from pathlib import Path

from .model import TERMINAL_STATUSES, Thing, scan


def cmd_cascade(args) -> int:
    """The post-completion cascade (write.thing.md) as a floor affordance.

    The mirror image of `touchpoints`. Where `touchpoints` gathers the INBOUND
    set ("what did I just put at risk?") for the change-reconciliation Assimilate
    beat, `cascade` gathers the OUTBOUND/downstream set ("what did I just
    unblock?") for the post-write completion cascade — the two directions of one
    index-walk-as-attention-cache pattern. The agent used to walk this by hand
    across three or four corpus queries on every completion; this hands it the
    precomputed chain instead (the kernel rule: never re-perform a mechanical
    walk by reasoning).

    Given a thing that just reached a terminal status, it walks the declared
    dependency edges in BOTH directions (a thing listing the target in its
    `dependencies`, and the ids the target names in its `blocks`), decides per
    candidate whether ALL of that candidate's prerequisites are now terminal,
    and reports unblock candidates (priority-flagged), partial-progress
    candidates, the parent-completion candidate, and trigger watchers.

    Three deliberate properties, two inherited from `touchpoints`:
    (1) It REPORTS candidates; it never applies a status change. Detection is
        mechanical; disposition stays the agent's — the narrative may hold a
        soft blocker no edge declares. No tool mutation of domain state.
    (2) Computed fresh from the live corpus, not a cached index.
    (3) It gathers trigger watchers but does not evaluate them — `mdllm triggers`
        owns trigger evaluation (reuse, don't reimplement, the trigger leg).
    The prerequisite check reads both `dependencies` and the reverse `blocks`
    edge, so it is not blind to a prerequisite declared in either field
    (structural-pointers-need-reverse-edge-indexing)."""
    root = Path(args.path).resolve()
    target = args.id
    corpus, _ = scan(root)
    by_id = corpus.by_id()
    if target not in by_id:
        print(f"mdllm: no thing with id `{target}` in {root}")
        return 1

    tgt = by_id[target]
    tgt_terminal = str(tgt.meta.get("status", "")) in TERMINAL_STATUSES

    # Prerequisite map: prereqs(Y) = Y.dependencies ∪ {Z : Y ∈ Z.blocks}. Both
    # fields declare "Z must finish before Y"; reading only one would go blind
    # to a prerequisite expressed in the other direction.
    blocks_rev: dict[str, list[str]] = {}
    for t in corpus.things:
        for b in t.meta.get("blocks") or []:
            if isinstance(b, str):
                blocks_rev.setdefault(b, []).append(t.id or t.path.name)

    def prereqs(y: Thing) -> list[str]:
        out = [d for d in (y.meta.get("dependencies") or []) if isinstance(d, str)]
        out += blocks_rev.get(y.id or "", [])
        return out

    # Downstream candidates: the things the completed target was a prerequisite
    # for — by their `dependencies` (inbound) or the target's own `blocks`.
    candidates: set[str] = set()
    for t in corpus.things:
        if target in (t.meta.get("dependencies") or []):
            candidates.add(t.id or t.path.name)
    for b in tgt.meta.get("blocks") or []:
        if isinstance(b, str):
            candidates.add(b)
    candidates.discard(target)

    unblock: list[str] = []
    partial: list[str] = []
    for cid in sorted(candidates):
        y = by_id.get(cid)
        if y is None:
            continue  # dangling ref — validate owns that finding, not cascade
        if str(y.meta.get("status", "")) in TERMINAL_STATUSES:
            continue  # already terminal; nothing left to unblock
        pres = prereqs(y)
        unmet = [p for p in pres if p != target
                 and (p not in by_id
                      or str(by_id[p].meta.get("status", "")) not in TERMINAL_STATUSES)]
        if not unmet:
            prio = str(y.meta.get("priority", "")).lower()
            flag = f"  [!] priority {prio}" if prio in ("critical", "high") else ""
            unblock.append(f"{cid} (currently `{y.meta.get('status')}`) — all "
                           f"{len(pres)} prerequisite(s) now terminal{flag}")
        else:
            met = len(pres) - len(unmet)
            partial.append(f"{cid} — {met}/{len(pres)} prerequisite(s) terminal; "
                           f"still waiting on: {', '.join(sorted(unmet))}")

    # Parent rollup: did the target's completion finish its parent's children?
    parent_line = None
    parent = tgt.meta.get("parent")
    if isinstance(parent, str) and parent:
        sibs = [t for t in corpus.things
                if t.meta.get("parent") == parent and (t.id or t.path.name) != target]
        total = len(sibs) + 1  # the siblings plus the target itself
        done = sum(1 for t in sibs
                   if str(t.meta.get("status", "")) in TERMINAL_STATUSES) + int(tgt_terminal)
        verdict = "completion candidate" if done == total else "partial progress"
        parent_line = f"`{parent}` — {done}/{total} child(ren) terminal -> {verdict}"

    # Trigger watchers: a dependency/threshold trigger watching the target.
    # cascade gathers; `mdllm triggers` owns evaluation.
    watchers: list[str] = []
    for t in corpus.things:
        for tr in t.meta.get("triggers") or []:
            if not isinstance(tr, dict):
                continue
            watch = tr.get("watch") or []
            watch = watch if isinstance(watch, list) else [watch]
            if target in watch:
                cond = tr.get("on") or tr.get("condition")
                watchers.append(f"{t.id or t.path.name} — trigger `{tr.get('type')}` "
                                f"(on={cond}, value={tr.get('value')})")

    print(f"## Cascade from `{target}` — {root}")
    if not tgt_terminal:
        print(f"note: `{target}` is `{tgt.meta.get('status')}`, not terminal — the "
              f"downstream below is HYPOTHETICAL until it reaches a terminal status.")
    print(f"({len(unblock)} unblock candidate(s), {len(partial)} partial, "
          f"{len(watchers)} trigger watcher(s))\n")

    print("### Unblock candidates — every prerequisite now terminal")
    for u in unblock or ["- (none)"]:
        print(u if u.startswith("- ") else f"- {u}")
    print("\n### Partial progress — still has open prerequisites")
    for pln in partial or ["- (none)"]:
        print(pln if pln.startswith("- ") else f"- {pln}")
    print("\n### Parent rollup")
    print(f"- {parent_line}" if parent_line else "- (no parent)")
    print("\n### Trigger watchers — evaluate with `mdllm triggers`")
    for w in watchers or ["- (none)"]:
        print(w if w.startswith("- ") else f"- {w}")

    print("\n### Disposition — yours")
    print("The set above is the mechanically-knowable downstream. Applying it is "
          "the agent's call: confirm each candidate's narrative holds no soft "
          "blocker the edges cannot see, then make the status writes and cascade "
          "them onward (write.thing.md -> After every change, cascade).")
    if not candidates and parent_line is None and not watchers:
        print(f"\nNothing depends on `{target}`: a leaf completion propagates "
              f"nowhere (write.thing.md -> the cascade is empty).")
    return 0
