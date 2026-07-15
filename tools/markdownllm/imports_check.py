"""Re-quarantine-on-drift — the consumer-side standing freshness check.

The upward version-check generalised from the one privileged source (the
framework) to an arbitrary `source_domain`. Reads the source's exposed face
through MCP — never its git — so the freshness signal obeys the same membrane
as content. Report-only: detection is mechanical, the re-quarantine flip is
the agent's disposition.
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


def _mcp_client_manifest(command: str, args: list, cwd: Path, source_domain: str,
                         timeout: int = 30) -> dict | None:
    # A minimal MCP stdio *client*: spawn the source's server, read its manifest
    # through the face. Returns the parsed manifest, or None when the source is
    # unreachable (bad command/path, spawn failure, timeout, malformed) — the
    # honest "freshness unknown" answer, never a silent "fresh".
    import json
    reqs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "resources/read",
             "params": {"uri": f"manifest://{source_domain}"}}]
    payload = "\n".join(json.dumps(r) for r in reqs) + "\n"
    try:
        out = subprocess.run([command, *args], input=payload, cwd=str(cwd),
                             capture_output=True, text=True, timeout=timeout)
    except Exception:
        return None
    for line in out.stdout.splitlines():
        try:
            msg = json.loads(line)
        except Exception:
            continue
        if msg.get("id") == 2 and "result" in msg:
            try:
                return json.loads(msg["result"]["contents"][0]["text"])
            except Exception:
                return None
    return None


def imports_freshness(consumer_root: Path) -> list[dict]:
    corpus, _ = scan(consumer_root)
    book = _load_address_book(consumer_root)
    manifests: dict[str, tuple[str, dict | None]] = {}  # spawn each source once
    results = []
    for t in corpus.things:
        m = t.meta
        if str(m.get("origin")) != "external":
            continue
        sd, sid, pin = m.get("source_domain"), m.get("source_id"), m.get("source_commit")
        if not (sd and sid and pin):
            results.append({"id": t.id, "state": "incomplete",
                            "detail": "missing source_domain/source_id/source_commit"})
            continue
        if sd not in manifests:
            cfg = book.get(sd)
            if not cfg or not cfg.get("command"):
                manifests[sd] = ("no-address", None)
            else:
                man = _mcp_client_manifest(cfg["command"], cfg.get("args", []),
                                           consumer_root, sd)
                manifests[sd] = ("ok", man) if man else ("unreachable", None)
        state, man = manifests[sd]
        row = {"id": t.id, "source": f"{sd}/{sid}", "pin": pin}
        if state == "no-address":
            row["state"] = "no-address-book-entry"
        elif state == "unreachable":
            row["state"] = "unreachable"  # freshness unknown — the honest answer
        else:
            current = next((k.get("source_commit") for k in man.get("knows", [])
                            if k.get("id") == sid), None)
            if current is None:
                row["state"] = "withdrawn"  # no longer exposed by the source
            else:
                row["current"] = current
                row["state"] = "fresh" if current == pin else "stale"
        results.append(row)
    return results


def cmd_imports_check(args) -> int:
    root = Path(args.path).resolve()
    rows = imports_freshness(root)
    if not rows:
        print(f"imports-check: no external imports in {root.name}")
        return 0
    print(f"## Imports Freshness — {root.name}\n")
    order = {"stale": 0, "unreachable": 1, "withdrawn": 2, "no-address-book-entry": 3,
             "incomplete": 4, "fresh": 5}
    for r in sorted(rows, key=lambda r: order.get(r["state"], 9)):
        if r["state"] == "stale":
            print(f"- STALE      {r['id']}  ({r['source']})  pinned {r['pin']} -> now {r['current']}")
            print("             re-quarantine: re-read the source, then flip `verified: false`, `status: stale`")
        elif r["state"] == "fresh":
            print(f"- fresh      {r['id']}  ({r['source']})  @ {r['pin']}")
        elif r["state"] == "unreachable":
            print(f"- UNKNOWN    {r['id']}  ({r['source']})  unreachable — freshness cannot be determined")
        elif r["state"] == "withdrawn":
            print(f"- WITHDRAWN  {r['id']}  ({r['source']})  source no longer exposes `{r['source'].split('/')[-1]}`")
        elif r["state"] == "no-address-book-entry":
            print(f"- NO-ROUTE   {r['id']}  ({r['source']})  no .mcp.json entry for source domain")
        else:
            print(f"- INCOMPLETE {r['id']}  {r.get('detail','')}")
    stale = sum(1 for r in rows if r["state"] == "stale")
    print(f"\n{len(rows)} import(s); {stale} stale. Freshness is advisory — disposition is yours.")
    return 0
