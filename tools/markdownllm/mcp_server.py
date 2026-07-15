"""The cross-domain producing side, on MCP (docs/plans/mcp-domain-server.md).

Phase 1: the read-only face over stdio. The SEMANTIC helpers (manifest/list/
read/query/deliverable) reuse the floor's own `scan()`; the TRANSPORT (a
minimal JSON-RPC stdio loop) is thin and replaceable — swapping stdio for
Streamable HTTP later touches only the loop. Pure stdlib, like the rest of
the floor — the `mcp` SDK is not a dependency.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .model import Corpus, Thing, scan
from .repo import git_short_sha

MCP_PROTOCOL_VERSION = "2025-11-25"  # echoed back to the client if it offers one
MCP_SERVER_VERSION = "0.1"


class _RpcError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code, self.message = code, message


def mcp_domain_id(root: Path) -> str:
    # Phase 1: identity is the domain directory name (kebab). A domain that wants
    # to declare its own id can override this later — kept trivial on purpose.
    return root.name


def mcp_exposed_things(corpus: Corpus) -> list[Thing]:
    # Exposure is opt-in: only `exposed: true` things join the face. Nothing
    # crosses by default — the semi-permeable membrane, curated by the producer.
    return [t for t in corpus.things if t.meta.get("exposed") is True and t.id]


def _mcp_summary(t: Thing) -> str:
    for line in t.body.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip()
    for line in t.body.splitlines():
        if line.strip():
            return line.strip()
    return ""


# A crossing thing carries its descriptive frontmatter, never the producer's
# internal relationship graph: those ids live in the producer's id-space and are
# foreign / unresolvable to any consumer. Stripped on egress so the graph stays
# reasoning-opaque across the boundary (the bright line). A cross-domain link, if
# ever wanted, is a deliberate source-scoped exposure — never a raw leak of
# foreign ids. (Surfaced by the first road test: the consumer tried to resolve a
# producer-local `linked_things` id and found nothing.)
# The rule is "every relational field", not this list's history: `informed_by`
# (provenance pins) and `parties` (conflict members) carry producer-local ids
# just as much as `linked_things` does — they leaked for two versions because
# the list was built from the road test's symptom, not from the rule (review 6,
# finding 2).
_MCP_INTERNAL_GRAPH = ("linked_things", "dependencies", "blocks", "parent",
                       "definition", "triggers", "informed_by", "parties")


def _mcp_egress_meta(meta: dict) -> dict:
    return {k: v for k, v in meta.items() if k not in _MCP_INTERNAL_GRAPH}


def _mcp_render_thing(t: Thing) -> str:
    import yaml
    fm = yaml.safe_dump(_mcp_egress_meta(t.meta), sort_keys=False, allow_unicode=True)
    return f"---\n{fm}---\n\n{t.body.lstrip(chr(10))}"


def _mcp_thing_commit(root: Path, t: Thing) -> str:
    # The pin is *per-thing*: the last commit that touched this exposed thing,
    # not the domain HEAD — so a freshness check fires only when the consumed
    # thing actually changed, not on any commit to the source. Computed
    # source-side; only the resulting commit crosses, never the file path.
    try:
        rel = t.path.relative_to(root)
    except ValueError:
        rel = t.path
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%h", "--", str(rel)],
                             cwd=root, capture_output=True, text=True, check=True)
        return out.stdout.strip() or "unknown"
    except Exception:
        return "unknown"


def mcp_list_tools() -> list[dict]:
    tools = [
        {"name": "query_things",
         "description": "List this domain's exposed things, optionally filtered by "
                        "type, tag, status, or free text. Browse the face.",
         "inputSchema": {"type": "object", "properties": {
             "type": {"type": "string"}, "tag": {"type": "string"},
             "status": {"type": "string"}, "text": {"type": "string"}}}},
        {"name": "get_deliverable",
         "description": "Fetch one exposed thing as a quarantined external "
                        "deliverable, stamped with its provenance reference triple "
                        "(source_domain, source_id, source_commit).",
         "inputSchema": {"type": "object",
                         "properties": {"id": {"type": "string"}},
                         "required": ["id"]}},
    ]
    return tools


def mcp_query_things(corpus: Corpus, typ=None, tag=None, status=None, text=None) -> list[dict]:
    rows = []
    for t in mcp_exposed_things(corpus):
        m = t.meta
        if typ and str(m.get("type")) != str(typ):
            continue
        if status and str(m.get("status")) != str(status):
            continue
        if tag:
            tags = m.get("tags") or []
            if not (isinstance(tags, list) and tag in tags):
                continue
        if text and text.lower() not in (f"{t.id} {_mcp_summary(t)} {t.body}").lower():
            continue
        rows.append({"id": t.id, "type": m.get("type"),
                     "status": m.get("status"), "summary": _mcp_summary(t)})
    return rows


def mcp_get_deliverable(root: Path, corpus: Corpus, domain_id: str, tid: str) -> dict | None:
    # Allowlist lookup by id — never builds a filesystem path from caller input,
    # so the path-traversal / argument-injection class (the 2026 reference-server
    # CVEs) cannot apply. Only an *exposed* id resolves.
    t = {x.id: x for x in mcp_exposed_things(corpus)}.get(tid)
    if t is None:
        return None
    return {"reference_triple": {"source_domain": domain_id, "source_id": tid,
                                 "source_commit": _mcp_thing_commit(root, t)},
            "frontmatter": _mcp_egress_meta(t.meta), "content": t.body}


def mcp_build_manifest(root: Path, corpus: Corpus, domain_id: str) -> dict:
    # Server Card-shaped (the emerging MCP automatic-discovery convention). Each
    # `knows` entry carries the thing's per-thing `source_commit` so a consumer's
    # freshness check reads current pins from the face in one call.
    things = mcp_exposed_things(corpus)
    return {"name": domain_id, "domain_id": domain_id,
            "head_commit": git_short_sha(root),
            "liveness": "corpus",
            "knows": [{"id": t.id, "type": t.meta.get("type"),
                       "status": t.meta.get("status"), "summary": _mcp_summary(t),
                       "source_commit": _mcp_thing_commit(root, t)}
                      for t in things],
            "can_do": [tool["name"] for tool in mcp_list_tools()],
            "who_i_know": []}  # outbound address book — a later phase


def mcp_list_resources(corpus: Corpus, domain_id: str) -> list[dict]:
    res = [{"uri": f"manifest://{domain_id}", "name": f"{domain_id} manifest",
            "description": "Domain porch: identity, exposed catalog, capabilities.",
            "mimeType": "application/json"}]
    for t in mcp_exposed_things(corpus):
        res.append({"uri": f"thing://{domain_id}/{t.id}", "name": t.id,
                    "description": _mcp_summary(t), "mimeType": "text/markdown"})
    return res


def mcp_read_resource(root: Path, corpus: Corpus, domain_id: str, uri: str) -> dict | None:
    import json
    if uri == f"manifest://{domain_id}":
        return {"uri": uri, "mimeType": "application/json",
                "text": json.dumps(mcp_build_manifest(root, corpus, domain_id),
                                    indent=2, default=str)}
    prefix = f"thing://{domain_id}/"
    if uri.startswith(prefix):
        t = {x.id: x for x in mcp_exposed_things(corpus)}.get(uri[len(prefix):])
        if t is None:
            return None
        return {"uri": uri, "mimeType": "text/markdown", "text": _mcp_render_thing(t)}
    return None


def cmd_mcp_serve(args) -> int:
    import json
    root = Path(args.path).resolve()
    if not root.is_dir():
        sys.exit(f"mdllm: not a directory: {root}")
    corpus, _ = scan(root)
    domain_id = mcp_domain_id(root)

    def log(msg: str) -> None:
        print(f"mcp-serve[{domain_id}]: {msg}", file=sys.stderr, flush=True)

    def emit(obj: dict) -> None:  # transport: one JSON-RPC message per line on stdout
        sys.stdout.write(json.dumps(obj, default=str) + "\n")
        sys.stdout.flush()

    def handle(method: str, params: dict):
        if method.startswith("notifications/"):
            return None  # client-side lifecycle notice — nothing to answer
        if method == "initialize":
            return {"protocolVersion": params.get("protocolVersion", MCP_PROTOCOL_VERSION),
                    "capabilities": {"resources": {}, "tools": {}},
                    "serverInfo": {"name": f"mdllm-domain:{domain_id}",
                                   "version": MCP_SERVER_VERSION}}
        if method == "ping":
            return {}
        if method == "resources/list":
            return {"resources": mcp_list_resources(corpus, domain_id)}
        if method == "resources/read":
            c = mcp_read_resource(root, corpus, domain_id, params.get("uri", ""))
            if c is None:
                raise _RpcError(-32002, f"resource not found or not exposed: {params.get('uri')}")
            return {"contents": [c]}
        if method == "tools/list":
            return {"tools": mcp_list_tools()}
        if method == "tools/call":
            name, a = params.get("name", ""), params.get("arguments") or {}
            if name == "query_things":
                rows = mcp_query_things(corpus, a.get("type"), a.get("tag"),
                                        a.get("status"), a.get("text"))
                return {"content": [{"type": "text", "text": json.dumps(rows, indent=2, default=str)}]}
            if name == "get_deliverable":
                d = mcp_get_deliverable(root, corpus, domain_id, a.get("id", ""))
                if d is None:
                    return {"content": [{"type": "text",
                            "text": f"not found or not exposed: {a.get('id')!r}"}], "isError": True}
                return {"content": [{"type": "text", "text": json.dumps(d, indent=2, default=str)}]}
            return {"content": [{"type": "text", "text": f"unknown tool: {name!r}"}], "isError": True}
        raise _RpcError(-32601, f"method not found: {method}")

    log(f"serving {len(mcp_exposed_things(corpus))} exposed thing(s) over stdio "
        f"(MCP {MCP_PROTOCOL_VERSION})")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            log("dropped non-JSON line")
            continue
        method, mid = msg.get("method"), msg.get("id")
        if method is None:  # a response or unknown frame — not ours to answer
            continue
        try:
            result = handle(method, msg.get("params") or {})
            if mid is not None:  # notifications (no id) get no reply
                emit({"jsonrpc": "2.0", "id": mid, "result": result})
        except _RpcError as e:
            if mid is not None:
                emit({"jsonrpc": "2.0", "id": mid, "error": {"code": e.code, "message": e.message}})
        except Exception as e:  # noqa: BLE001 — transport must not die on one bad call
            log(f"error handling {method}: {e}")
            if mid is not None:
                emit({"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(e)}})
    return 0
