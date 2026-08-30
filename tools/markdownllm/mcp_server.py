"""The cross-domain producing side, on MCP (docs/plans/mcp-domain-server.md).

Phase 1: the read-only face over stdio. The SEMANTIC helpers (manifest/list/
read/query/deliverable) reuse the floor's own `scan()`; the TRANSPORT is thin
and replaceable — one dispatcher, two pipes.

Phase 5 (transport leg): the same face over Streamable HTTP (`--http`) — the
promised transport swap, touching only the loop. Loopback-bound only: a
loopback port is the same trust zone as a spawned subprocess (the operator's
own machine), so the floor's authorization stance is unchanged. Binding a
routable interface is REFUSED, not flagged — public exposure arrives with
OAuth 2.1 (the 2025-11-25 spec's authorization model), never with an
honour-system `--host 0.0.0.0`. Pure stdlib, like the rest of the floor —
the `mcp` SDK is not a dependency.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .model import Corpus, Thing, parse_frontmatter, scan
from .repository_view import (
    RepositoryView, RepositoryViewError, RepositoryViewMode,
)
from .structural_refs import egress_private_fields

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
# `exposed` is not structural, but it is equally the producer's: it marks
# membership of the *producer's* served face. A consumer that lands the face
# render verbatim would inherit `exposed: true` and silently re-export the
# import onto its own face — exposure decided by copy, not by the consumer's
# own exposure call. Surfaced live 2026-08-30: both mirrors of the first
# mirror re-sync arrived carrying the producer's flag.
_EGRESS_PRODUCER_MARKERS = frozenset({"exposed"})


def _mcp_egress_meta(meta: dict) -> dict:
    private = egress_private_fields() | _EGRESS_PRODUCER_MARKERS
    return {k: v for k, v in meta.items() if k not in private}


def _mcp_render_thing(t: Thing) -> str:
    import yaml
    fm = yaml.safe_dump(_mcp_egress_meta(t.meta), sort_keys=False, allow_unicode=True)
    return f"---\n{fm}---\n\n{t.body.lstrip(chr(10))}"


def _mcp_logical_path(view: RepositoryView, t: Thing) -> Path:
    try:
        return t.path.relative_to(view.root)
    except ValueError:
        return t.path


# One head view per served root per process, its blob and last-commit reads
# prefetched in two batch spawns. The per-thing form re-created the commit
# view and spawned `git show` + `git log -1` for every thing in a manifest —
# measured 2026-08-30 at ~33s for one 46-thing manifest on Windows, past the
# membrane client's 10s deadline, so a granted route still read as
# unreachable. A server process serves one client session, so the head is a
# session snapshot by construction — the same atomicity the per-thing reads
# only pretended to have (each created its own view, so a mid-session HEAD
# move already produced a mixed answer; one shared view removes that too).
_SHARED_HEADS: dict[str, RepositoryView] = {}


def _shared_head(root: Path, corpus: Corpus) -> RepositoryView:
    key = str(Path(root).resolve())
    head = _SHARED_HEADS.get(key)
    if head is None:
        head = RepositoryView.commit(root)
        head.prefetch(_mcp_logical_path(corpus.view or head, t)
                      for t in corpus.things)
        head.prefetch_last_commits()
        _SHARED_HEADS[key] = head
    return head


def _mcp_source(root: Path, corpus: Corpus, t: Thing) -> tuple[Thing, dict]:
    """Describe the exact provenance of the bytes parsed into ``t``.

    A full last-touch commit is returned only when those bytes came from an
    immutable commit view or are byte-identical to the current HEAD view.  A
    draft/index candidate remains usable on the local porch, but it is marked
    ``uncommitted`` and cannot masquerade as a reference triple.
    """
    root = Path(root).resolve()
    view = corpus.view or RepositoryView.worktree(root)
    logical = _mcp_logical_path(view, t)
    source = t.source_text.encode("utf-8") if t.source_text is not None else None

    if view.mode is RepositoryViewMode.COMMIT:
        if source is None or not view.exists(logical) or view.read_bytes(logical) != source:
            return t, {"state": "unknown", "source_commit": "unknown",
                       "view": view.identifier}
        view.prefetch_last_commits()   # memoised: one walk serves every thing
        commit = view.last_commit_for(logical)
        if commit:
            return t, {"state": "committed", "source_commit": commit,
                       "view": view.identifier}
        return t, {"state": "unknown", "source_commit": "unknown",
                   "view": view.identifier}

    try:
        head = _shared_head(root, corpus)
    except RepositoryViewError:
        return t, {"state": "unknown", "source_commit": "unknown",
                   "view": view.identifier}

    committed_source = head.read_bytes(logical) if head.exists(logical) else None
    # A Windows checkout may expose CRLF while Git's immutable blob is LF.
    # Treat only that one safe transport normalization as equivalent, then
    # substitute the actual committed bytes for egress.  We never stamp the
    # ambient worktree rendering and merely hope the content is the same.
    matches = bool(source is not None and committed_source is not None and (
        source == committed_source or source.replace(b"\r\n", b"\n") == committed_source
    ))
    if matches:
        commit = head.last_commit_for(logical)
        if commit:
            text = committed_source.decode("utf-8")
            meta, body, err = parse_frontmatter(text)
            if err is None and meta is not None:
                t = Thing(path=t.path, meta=meta, body=body, source_text=text)
                return t, {"state": "committed", "source_commit": commit,
                           "view": f"commit:{head.commit_sha}"}

    state = "candidate" if view.mode is RepositoryViewMode.INDEX else "uncommitted"
    return t, {"state": state, "source_commit": "uncommitted",
               "base_commit": head.commit_sha, "view": view.identifier}


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
    source_root = corpus.view.root if corpus.view is not None else corpus.root
    for exposed in mcp_exposed_things(corpus):
        # Query results cross the same membrane as deliverables.  Resolve the
        # exact source before reading row fields so a clean CRLF worktree uses
        # the committed blob, while a draft/index value stays usable only with
        # its explicit uncommitted/candidate label.
        t, source = _mcp_source(source_root, corpus, exposed)
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
                     "status": m.get("status"), "summary": _mcp_summary(t),
                     "_mcp_source": source})
    return rows


def mcp_get_deliverable(root: Path, corpus: Corpus, domain_id: str, tid: str) -> dict | None:
    # Allowlist lookup by id — never builds a filesystem path from caller input,
    # so the path-traversal / argument-injection class (the 2026 reference-server
    # CVEs) cannot apply. Only an *exposed* id resolves.
    t = {x.id: x for x in mcp_exposed_things(corpus)}.get(tid)
    if t is None:
        return None
    t, source = _mcp_source(root, corpus, t)
    return {"reference_triple": {"source_domain": domain_id, "source_id": tid,
                                 "source_commit": source["source_commit"]},
            "source_state": source,
            "frontmatter": _mcp_egress_meta(t.meta), "content": t.body}


def mcp_build_manifest(root: Path, corpus: Corpus, domain_id: str) -> dict:
    # Server Card-shaped (the emerging MCP automatic-discovery convention). Each
    # `knows` entry carries the thing's per-thing `source_commit` so a consumer's
    # freshness check reads current pins from the face in one call.
    things = mcp_exposed_things(corpus)
    states = {t.id: _mcp_source(root, corpus, t)[1] for t in things}
    view = corpus.view or RepositoryView.worktree(root)
    if view.mode is RepositoryViewMode.COMMIT:
        head_commit = view.commit_sha
    else:
        try:
            head_commit = RepositoryView.commit(root).commit_sha
        except RepositoryViewError:
            head_commit = "unknown"
    return {"name": domain_id, "domain_id": domain_id,
            "head_commit": head_commit,
            "liveness": view.identifier,
            "knows": [{"id": t.id, "type": t.meta.get("type"),
                       "status": t.meta.get("status"), "summary": _mcp_summary(t),
                       "source_commit": states[t.id]["source_commit"],
                       "source_state": states[t.id]["state"]}
                      for t in things],
            "can_do": [tool["name"] for tool in mcp_list_tools()],
            # Deliberately empty, permanently — operator ruling 2026-07-28:
            # producer blindness is a boundary, not a backlog. A producer never
            # learns who consumes it; publication is an honest commit to the
            # face, delivery is the consumer's poll. Do not "finish" this.
            # (provenance.md -> The Membrane's Direction Is a Ruling.)
            "who_i_know": []}


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
        t, source = _mcp_source(root, corpus, t)
        return {"uri": uri, "mimeType": "text/markdown",
                "sourceState": source["state"],
                "sourceCommit": source["source_commit"],
                "text": _mcp_render_thing(t)}
    return None


def mcp_make_dispatcher(root: Path, domain_id: str, corpus_provider):
    """One method dispatcher, any transport. `corpus_provider` decides the
    read's currency: stdio scans once (a client spawn IS a fresh read),
    HTTP scans per request (the server is stateless; git is the state —
    every read computed from the repo as it stands, per design guardrail 3)."""

    import json

    def handle(method: str, params: dict):
        corpus = corpus_provider()
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

    return handle


def _dispatch_message(handle, msg: dict, log) -> dict | None:
    """Run one already-parsed JSON-RPC message through the dispatcher.
    Returns the response object, or None when nothing is owed (notifications,
    frames that aren't requests). Shared by both transports so error mapping
    cannot drift between them."""
    method, mid = msg.get("method"), msg.get("id")
    if method is None:  # a response or unknown frame — not ours to answer
        return None
    try:
        result = handle(method, msg.get("params") or {})
        if mid is None:  # notifications (no id) get no reply
            return None
        return {"jsonrpc": "2.0", "id": mid, "result": result}
    except _RpcError as e:
        if mid is None:
            return None
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": e.code, "message": e.message}}
    except Exception as e:  # noqa: BLE001 — transport must not die on one bad call
        log(f"error handling {method}: {e}")
        if mid is None:
            return None
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32603, "message": str(e)}}


# ------------------------------------------------------------- transports

_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def mcp_host_is_loopback(host: str) -> bool:
    h = (host or "").strip().lower().strip("[]")
    return h in _LOOPBACK_HOSTS or h.startswith("127.")


def _origin_allowed(origin: str | None) -> bool:
    # DNS-rebinding defence (Streamable HTTP spec): a browser-borne request
    # carries an Origin, and only loopback origins may speak to a loopback
    # porch. Non-browser clients send none — that is the normal MCP case.
    if not origin:
        return True
    from urllib.parse import urlsplit
    return mcp_host_is_loopback(urlsplit(origin).hostname or "")


def mcp_http_server(root: Path, domain_id: str, host: str, port: int, log=None,
                    token: str | None = None):
    """Build (not run) the Streamable HTTP transport: one endpoint (`/mcp`),
    POST carries a JSON-RPC message, the reply is `application/json`.
    Stateless by design — no sessions, no server-initiated stream (GET is
    405), every request re-reads the repo. Returned unstarted so tests can
    drive it on an ephemeral port; `cmd_mcp_serve` runs it forever.

    `token` gates every request behind `Authorization: Bearer <token>` —
    the probe control for tunnelled cross-machine reads: per-run (dies with
    the process, so never the long-lived API key the doctrine bans), held
    only by the operator who started the server. Possession of the token IS
    being the operator; OAuth 2.1 remains the gate for other-party
    consumers."""
    import hmac
    import json
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    log = log or (lambda msg: print(f"mcp-serve[{domain_id}]: {msg}",
                                    file=sys.stderr, flush=True))
    handle = mcp_make_dispatcher(root, domain_id, lambda: scan(root)[0])

    class _Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt, *args):  # route http.server chatter to our log
            log(f"http {self.address_string()} {fmt % args}")

        def _send(self, code: int, body: bytes = b"", extra: dict | None = None) -> None:
            self.send_response(code)
            if body:
                self.send_header("Content-Type", "application/json")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)

        def _authorized(self) -> bool:
            if not token:
                return True
            got = self.headers.get("Authorization", "")
            return got.startswith("Bearer ") and hmac.compare_digest(got[7:].strip(), token)

        def do_POST(self):
            if not self._authorized():
                return self._send(401, b'{"error":"missing or wrong bearer token"}',
                                  extra={"WWW-Authenticate": "Bearer"})
            if self.path.rstrip("/") != "/mcp":
                return self._send(404, b'{"error":"the MCP endpoint is /mcp"}')
            if not _origin_allowed(self.headers.get("Origin")):
                return self._send(403, b'{"error":"origin not allowed: loopback origins only"}')
            try:
                length = int(self.headers.get("Content-Length") or 0)
                msg = json.loads(self.rfile.read(length))
                if not isinstance(msg, dict):
                    raise ValueError("one JSON-RPC message per POST (batching left the spec)")
            except Exception as e:  # noqa: BLE001
                return self._send(400, json.dumps({"error": f"bad request: {e}"}).encode())
            resp = _dispatch_message(handle, msg, log)
            if resp is None:  # notification / non-request frame — accepted, no body
                return self._send(202)
            self._send(200, json.dumps(resp, default=str).encode())

        def do_GET(self):
            # No server-initiated stream: the porch is poll-only, state is git.
            self._send(405, b'{"error":"no server stream; POST JSON-RPC to /mcp"}')

        do_DELETE = do_GET  # no sessions to terminate either

    return ThreadingHTTPServer((host, port), _Handler)


def cmd_mcp_serve(args) -> int:
    import json
    root = Path(args.path).resolve()
    if not root.is_dir():
        sys.exit(f"mdllm: not a directory: {root}")
    domain_id = mcp_domain_id(root)

    def log(msg: str) -> None:
        print(f"mcp-serve[{domain_id}]: {msg}", file=sys.stderr, flush=True)

    if getattr(args, "http", False):
        host = getattr(args, "host", "127.0.0.1") or "127.0.0.1"
        if not mcp_host_is_loopback(host):
            # Refused, not warned: a routable porch without OAuth 2.1 is the
            # honour-system control the floor exists to replace. The public
            # leg arrives as auth + transport together, or not at all.
            sys.exit(f"mdllm: refusing to bind non-loopback host {host!r} — "
                     "the HTTP porch is loopback-only until the OAuth 2.1 "
                     "authorization leg exists (docs/plans/mcp-domain-server.md, Phase 5)")
        token = getattr(args, "token", None)
        if token == "auto":
            import secrets
            token = secrets.token_urlsafe(32)
            log(f"bearer token (per-run; dies with this process): {token}")
        server = mcp_http_server(root, domain_id, host, int(getattr(args, "port", 8765)),
                                 log, token=token)
        corpus, _ = scan(root)
        bound = server.server_address
        log(f"serving {len(mcp_exposed_things(corpus))} exposed thing(s) over "
            f"Streamable HTTP at http://{bound[0]}:{bound[1]}/mcp "
            f"(MCP {MCP_PROTOCOL_VERSION}; loopback-only; re-read per request; "
            f"{'bearer-token gated' if token else 'no token — loopback trust'})")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            log("stopped")
        finally:
            server.server_close()
        return 0

    # stdio (default): the client spawns us; scan once — the spawn is the read.
    corpus, _ = scan(root)
    handle = mcp_make_dispatcher(root, domain_id, lambda: corpus)

    def emit(obj: dict) -> None:  # transport: one JSON-RPC message per line on stdout
        sys.stdout.write(json.dumps(obj, default=str) + "\n")
        sys.stdout.flush()

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
        resp = _dispatch_message(handle, msg, log)
        if resp is not None:
            emit(resp)
    return 0
