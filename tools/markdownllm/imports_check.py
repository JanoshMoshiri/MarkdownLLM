"""Re-quarantine-on-drift — the consumer-side standing sync check.

The upward version-check generalised from the one privileged source (the
framework) to an arbitrary `source_domain`. Reads the source's exposed face
through MCP — never its git — so the sync signal obeys the same membrane as
content. Report-only: detection is mechanical, the re-quarantine flip is
the agent's disposition.

Both sync directions are consumer-side reads through the face:
- `stale` — the source moved under the pin (mirror behind source).
- `diverged` — the pin is current but the mirror's content no longer matches
  the face (source behind mirror: the loop was bypassed — the mirror was
  edited locally, or the source changed without committing).

`estate-check` is batching over this, never an index: the operator names the
roots explicitly per invocation; nothing is discovered, persisted, or
reverse-mapped, and every read is exactly the read that consumer could make
alone. A domain still cannot enumerate its consumers.

Offline = `unreachable` (sync state unknown), never a silent `fresh`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from .model import scan

def _load_address_book(consumer_root: Path) -> dict:
    # The consumer's `.mcp.json` mcpServers map IS the address book — operator-
    # wired, per trust zone. name -> {command, args}.
    import json
    p = consumer_root / ".mcp.json"
    if not p.is_file():
        return {}
    try:
        return (json.loads(p.read_text(encoding="utf-8")) or {}).get("mcpServers", {}) or {}
    except Exception:
        return {}


def _mcp_client_read(command: str, args: list, cwd: Path, uris: list[str],
                     timeout: int = 30) -> dict | None:
    # A minimal MCP stdio *client*: spawn the source's server once, read the
    # given resource URIs through the face. Returns {uri: text} for every URI
    # the server answered; None when the spawn itself fails (bad command/path,
    # spawn failure, timeout) — the honest "sync state unknown" answer, never
    # a silent "fresh".
    import json
    reqs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}]
    for i, uri in enumerate(uris, start=2):
        reqs.append({"jsonrpc": "2.0", "id": i, "method": "resources/read",
                     "params": {"uri": uri}})
    payload = "\n".join(json.dumps(r) for r in reqs) + "\n"
    try:
        out = subprocess.run([command, *args], input=payload, cwd=str(cwd),
                             capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None
    by_id: dict[int, dict] = {}
    for line in out.stdout.splitlines():
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") and "result" in msg:
            by_id[msg["id"]] = msg["result"]
    got: dict[str, str] = {}
    for i, uri in enumerate(uris, start=2):
        r = by_id.get(i)
        if r:
            try:
                got[uri] = r["contents"][0]["text"]
            except Exception:
                pass
    return got


def _face_body(rendered: str) -> str:
    # `thing://` text is `---\n{frontmatter}---\n\n{body}` (_mcp_render_thing).
    if rendered.startswith("---\n"):
        parts = rendered.split("---\n", 2)
        if len(parts) == 3:
            return parts[2]
    return rendered


def _norm_body(s: str) -> str:
    # Content identity for the divergence compare: trailing whitespace and
    # edge blank lines are transport noise, not edits.
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def imports_freshness(consumer_root: Path) -> list[dict]:
    import json
    corpus, _ = scan(consumer_root)
    book = _load_address_book(consumer_root)
    imports = [t for t in corpus.things if str(t.meta.get("origin")) == "external"]

    # One spawn per source, reading the manifest plus every imported thing's
    # face content in a single pass — the content read is what makes the
    # `diverged` direction visible without ever touching the source's git.
    by_source: dict[str, list[str]] = {}
    for t in imports:
        m = t.meta
        sd, sid, pin = m.get("source_domain"), m.get("source_id"), m.get("source_commit")
        if sd and sid and pin:
            by_source.setdefault(str(sd), []).append(str(sid))
    faces: dict[str, tuple[str, tuple[dict, dict] | None]] = {}
    for sd, sids in by_source.items():
        cfg = book.get(sd)
        if not cfg or not cfg.get("command"):
            faces[sd] = ("no-address", None)
            continue
        uris = [f"manifest://{sd}"] + [f"thing://{sd}/{sid}" for sid in sids]
        got = _mcp_client_read(cfg["command"], cfg.get("args", []), consumer_root, uris)
        man = None
        if got and f"manifest://{sd}" in got:
            try:
                man = json.loads(got[f"manifest://{sd}"])
            except Exception:
                man = None
        faces[sd] = ("ok", (man, got)) if man else ("unreachable", None)

    results = []
    for t in imports:
        m = t.meta
        sd, sid, pin = m.get("source_domain"), m.get("source_id"), m.get("source_commit")
        if not (sd and sid and pin):
            if m.get("source_system") and not sd:
                # The ingestion species (world -> domain): no face to poll, so
                # the import comparison is permanently impossible BY DESIGN —
                # report the staleness clock, never file it as a coverage
                # failure (origin-external-conflates-ingestion-with-import).
                checked = m.get("source_checked")
                results.append({"id": t.id, "state": "ingested",
                                "source": str(m.get("source_system")),
                                "checked": str(checked) if checked else None})
                continue
            results.append({"id": t.id, "state": "incomplete",
                            "detail": "missing source_domain/source_id/source_commit"})
            continue
        state, payload = faces[str(sd)]
        row = {"id": t.id, "source": f"{sd}/{sid}", "pin": pin}
        if state == "no-address":
            row["state"] = "no-address-book-entry"
        elif state == "unreachable":
            row["state"] = "unreachable"  # sync state unknown — the honest answer
        else:
            man, got = payload
            current = next((k.get("source_commit") for k in man.get("knows", [])
                            if k.get("id") == sid), None)
            if current is None:
                row["state"] = "withdrawn"  # no longer exposed by the source
            else:
                row["current"] = current
                if current != pin:
                    row["state"] = "stale"
                else:
                    src_text = got.get(f"thing://{sd}/{sid}")
                    if (src_text is not None
                            and _norm_body(_face_body(src_text)) != _norm_body(t.body)):
                        row["state"] = "diverged"
                    else:
                        row["state"] = "fresh"
        results.append(row)
    return results


def _render_rows(rows: list[dict]) -> None:
    order = {"stale": 0, "diverged": 1, "unreachable": 2, "withdrawn": 3,
             "no-address-book-entry": 4, "incomplete": 5, "fresh": 6, "ingested": 7}
    for r in sorted(rows, key=lambda r: order.get(r["state"], 9)):
        if r["state"] == "stale":
            print(f"- STALE      {r['id']}  ({r['source']})  pinned {r['pin']} -> now {r['current']}")
            print("             re-quarantine: re-read the source, then flip `verified: false`, `status: stale`")
        elif r["state"] == "diverged":
            print(f"- DIVERGED   {r['id']}  ({r['source']})  pin {r['pin']} is current but content differs")
            print("             the loop was bypassed: mirror edited locally, or source changed without committing — route as an inflection")
        elif r["state"] == "fresh":
            print(f"- fresh      {r['id']}  ({r['source']})  @ {r['pin']}")
        elif r["state"] == "unreachable":
            print(f"- UNKNOWN    {r['id']}  ({r['source']})  unreachable — sync state cannot be determined")
        elif r["state"] == "withdrawn":
            print(f"- WITHDRAWN  {r['id']}  ({r['source']})  source no longer exposes `{r['source'].split('/')[-1]}`")
        elif r["state"] == "no-address-book-entry":
            print(f"- NO-ROUTE   {r['id']}  ({r['source']})  no .mcp.json entry for source domain")
        elif r["state"] == "ingested":
            clock = (f"checked {r['checked']}" if r.get("checked")
                     else "no source_checked date — clock missing")
            print(f"- ingested   {r['id']}  ({r['source']})  {clock}")
        else:
            print(f"- INCOMPLETE {r['id']}  {r.get('detail','')}")


def _counts(rows: list[dict]) -> dict:
    n = {s: sum(1 for r in rows if r["state"] == s)
         for s in ("stale", "diverged", "fresh", "withdrawn", "ingested")}
    n["checked"] = n["stale"] + n["diverged"] + n["fresh"] + n["withdrawn"]
    # Ingested things are a different species with their own clock — they are
    # neither checked (no membrane comparison exists) nor unchecked coverage
    # (the comparison is impossible by design, not missed).
    n["unchecked"] = len(rows) - n["checked"] - n["ingested"]
    return n


def _render_summary(rows: list[dict]) -> None:
    # The summary states COVERAGE, not just findings: "0 stale" over zero
    # possible comparisons rendered identically to "everything is fresh", and
    # in a regulated context that line is read as assurance (estate audit
    # FW-2: a domain with 26 imports, all INCOMPLETE, reported "26 import(s);
    # 0 stale."). The docstring's promise — never a silent fresh — belongs to
    # the summary line too.
    n = _counts(rows)
    membrane = len(rows) - n["ingested"]
    print(f"\n{len(rows)} import(s): {n['stale']} stale, {n['diverged']} diverged, "
          f"{n['fresh']} fresh, {n['withdrawn']} withdrawn; {n['unchecked']} could "
          f"not be checked (incomplete/no-route/unreachable). "
          f"COVERAGE: {n['checked']}/{membrane}.")
    if n["ingested"]:
        dates = sorted(r["checked"] for r in rows
                       if r["state"] == "ingested" and r.get("checked"))
        undated = sum(1 for r in rows
                      if r["state"] == "ingested" and not r.get("checked"))
        clock = f"oldest check {dates[0]}" if dates else "no check dates at all"
        tail = f", {undated} undated" if undated and dates else ""
        print(f"{n['ingested']} ingested (world→domain, no face to poll; {clock}{tail}) "
              f"— re-checking is the operator's cadence.")
    if n["checked"] == 0 and membrane:
        print("Nothing was checkable — this report asserts nothing about freshness.")
    print("Freshness is advisory — disposition is yours.")


def face_coverage(consumer_root: Path) -> list[dict]:
    """What every address-book source offers vs what this domain imported.

    Closes the hole coverage cannot see: COVERAGE counts pins that exist, so
    a consumer with an address-book entry and zero imports scores a perfect
    report while an entire face goes unread. This is a consumer-side read of
    the manifest the consumer already fetches — no new state anywhere, and
    nothing tells a producer who is watching. Importing nothing stays a
    legitimate disposition; the line is information, not a finding.
    """
    corpus, _ = scan(consumer_root)
    book = _load_address_book(consumer_root)
    imported: dict[str, int] = {}
    for t in corpus.things:
        if str(t.meta.get("origin")) == "external" and t.meta.get("source_domain"):
            sd = str(t.meta["source_domain"])
            imported[sd] = imported.get(sd, 0) + 1
    out = []
    for sd, cfg in sorted(book.items()):
        if not isinstance(cfg, dict) or not cfg.get("command"):
            continue
        got = _mcp_client_read(cfg["command"], cfg.get("args", []),
                               consumer_root, [f"manifest://{sd}"])
        man = None
        if got and f"manifest://{sd}" in got:
            import json
            try:
                man = json.loads(got[f"manifest://{sd}"])
            except Exception:
                man = None
        if man is None:
            out.append({"source": sd, "state": "unreachable",
                        "offered": None, "imported": imported.get(sd, 0)})
        else:
            out.append({"source": sd, "state": "ok",
                        "offered": len(man.get("knows") or []),
                        "imported": imported.get(sd, 0)})
    return out


def _render_face_coverage(cov: list[dict]) -> None:
    if not cov:
        return
    print("\n### Face coverage (address book)")
    for c in cov:
        if c["state"] == "unreachable":
            print(f"- {c['source']}: unreachable — offering unknown "
                  f"({c['imported']} imported)")
        elif c["offered"] and c["imported"] == 0:
            print(f"- {c['source']}: offers {c['offered']}, imported 0 — "
                  f"nothing pulled; a clean imports report over zero imports "
                  f"asserts nothing about this face")
        else:
            print(f"- {c['source']}: offers {c['offered']}, imported {c['imported']}")
    print("Importing nothing may be correct — disposition is yours.")


def cmd_imports_check(args) -> int:
    root = Path(args.path).resolve()
    rows = imports_freshness(root)
    cov = face_coverage(root)
    if not rows and not cov:
        print(f"imports-check: no external imports in {root.name}")
        return 0
    print(f"## Imports Sync — {root.name}\n")
    if rows:
        _render_rows(rows)
        _render_summary(rows)
    else:
        print("No external imports.")
    _render_face_coverage(cov)
    return 0


def cmd_estate_check(args) -> int:
    # Operator-axis batching over imports_freshness, and nothing more. The
    # doctrine guardrails, by construction: output is stdout-only (no
    # persisted artifact to rot into a registry), and the report is grouped
    # per-consumer (never a per-source reverse map — a domain still cannot
    # enumerate its consumers). Every read here is a read that consumer could
    # make alone; batching adds convenience, not information.
    #
    # Roots: named explicitly per invocation, OR (no args) discovered by the
    # same local-clone walk `estate-sync` uses. Discovery here is repos-not-
    # membranes (the estate-git-sync precedent): enumerating checkouts on
    # THIS machine is a filesystem fact, not an estate manifest — no artifact
    # anywhere claims to be the estate, and a domain not cloned locally is
    # genuinely absent from this machine's view. What stays forbidden is a
    # persisted membership registry, not `ls`.
    discovered = False
    if args.paths:
        roots = [Path(p).resolve() for p in args.paths]
    else:
        from .sync import discover_repos
        roots = discover_repos(Path(".").resolve())
        discovered = True
        if not roots:
            print("estate-check: no local clones found to walk")
            return 0
    missing = [r for r in roots if not r.is_dir()]
    if missing:
        print("estate-check: not a directory: " + ", ".join(str(m) for m in missing))
        return 1
    how = ("local clones walked — a filesystem fact, not an estate manifest"
           if discovered else "named explicitly")
    print(f"## Estate Sync — {len(roots)} consumer(s), {how}\n")
    per_consumer: list[tuple[str, list[dict]]] = []
    for root in roots:
        rows = imports_freshness(root)
        cov = face_coverage(root)
        per_consumer.append((root.name, rows))
        print(f"### {root.name}")
        if not rows and not cov:
            print("- no external imports\n")
            continue
        if rows:
            _render_rows(rows)
            _render_summary(rows)
        else:
            print("- no external imports")
        # The face-coverage read runs even — especially — when rows is empty:
        # the hole it closes is precisely the consumer whose clean report was
        # achieved by not importing.
        _render_face_coverage(cov)
        print()
    total = [r for _, rows in per_consumer for r in rows]
    n = _counts(total)
    attention = n["stale"] + n["diverged"] + n["withdrawn"]
    print(f"### Estate roll-up")
    for name, rows in per_consumer:
        c = _counts(rows)
        print(f"- {name}: {c['stale']} stale, {c['diverged']} diverged, "
              f"{c['fresh']} fresh; coverage {c['checked']}/{len(rows)}")
    print(f"\n{attention} import(s) need attention (stale/diverged/withdrawn); "
          f"{n['unchecked']} could not be checked. "
          f"COVERAGE: {n['checked']}/{len(total)}.")
    print("This view is a batch of per-consumer reads — ephemeral, never an index.")
    return 0
