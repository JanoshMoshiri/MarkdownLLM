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
import threading
import time

from .external_trust import (
    ExternalTrustError, ExternalTrustPolicy, LocalExternalTrustPolicy,
    load_mcp_address_book,
)
from .model import origin_is_external, scan


MAX_EXTERNAL_RESPONSE_BYTES = 2 * 1024 * 1024
MAX_EXTERNAL_STDERR_BYTES = 8 * 1024
DEFAULT_EXTERNAL_TIMEOUT_SECONDS = 10.0
MAX_EXTERNAL_TIMEOUT_SECONDS = 30.0


def _bounded_timeout(value: int | float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        parsed = DEFAULT_EXTERNAL_TIMEOUT_SECONDS
    return min(MAX_EXTERNAL_TIMEOUT_SECONDS, max(0.05, parsed))


def _initialize_message() -> dict:
    from .mcp_server import MCP_PROTOCOL_VERSION
    return {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "mdllm-imports-check", "version": "1"},
        },
    }


def _initialized_message() -> dict:
    return {"jsonrpc": "2.0", "method": "notifications/initialized",
            "params": {}}

def _load_address_book_result(
        consumer_root: Path) -> tuple[dict, str | None]:
    """Distinguish an absent route book from an invalid definition.

    Absence means a source may truthfully receive ``no-address-book-entry``.
    A present-but-malformed file is a different state: no declared route can
    be selected safely, and collapsing it to absence hides definition
    corruption (including duplicate-key shadowing).
    """
    path = Path(consumer_root) / ".mcp.json"
    if not path.exists():
        return {}, None
    try:
        return load_mcp_address_book(consumer_root), None
    except ExternalTrustError as exc:
        return {}, str(exc)


def _mcp_client_read(command: str, args: list, cwd: Path, uris: list[str],
                     timeout: int | float = DEFAULT_EXTERNAL_TIMEOUT_SECONDS,
                     max_response_bytes: int = MAX_EXTERNAL_RESPONSE_BYTES
                     ) -> dict | None:
    # A minimal MCP stdio *client*: spawn the source's server once, read the
    # given resource URIs through the face. Returns {uri: text} for every URI
    # the server answered; None when the spawn itself fails (bad command/path,
    # spawn failure, timeout) — the honest "sync state unknown" answer, never
    # a silent "fresh".
    import json
    import os
    import queue

    deadline = time.monotonic() + _bounded_timeout(timeout)
    responses: queue.Queue[bytes | None] = queue.Queue()
    out_state: dict = {"total": 0, "oversized": False, "failed": False}
    err_state: dict = {"total": 0, "oversized": False, "failed": False}
    proc = None

    def read_stdout(pipe) -> None:
        pending = bytearray()
        try:
            while True:
                chunk = os.read(pipe.fileno(), 64 * 1024)
                if not chunk:
                    break
                out_state["total"] += len(chunk)
                if out_state["total"] > max_response_bytes:
                    out_state["oversized"] = True
                    pending.clear()
                    continue  # drain to keep the child from blocking; retain nothing
                pending.extend(chunk)
                while b"\n" in pending:
                    line, _, remainder = pending.partition(b"\n")
                    pending = bytearray(remainder)
                    responses.put(bytes(line))
            if pending and not out_state["oversized"]:
                responses.put(bytes(pending))
        except Exception:
            out_state["failed"] = True
        finally:
            responses.put(None)

    def drain_stderr(pipe) -> None:
        # Drain without surfacing repository-controlled diagnostics.  Retain no
        # bytes, so secrets in a command's error path cannot enter a prompt.
        try:
            while True:
                chunk = os.read(pipe.fileno(), 64 * 1024)
                if not chunk:
                    break
                err_state["total"] += len(chunk)
                if err_state["total"] > MAX_EXTERNAL_STDERR_BYTES:
                    err_state["oversized"] = True
        except Exception:
            err_state["failed"] = True

    def remaining() -> float:
        return max(0.0, deadline - time.monotonic())

    def next_message() -> dict | None:
        while remaining() > 0:
            try:
                line = responses.get(timeout=max(0.05, remaining()))
            except queue.Empty:
                return None
            if line is None:
                return None
            try:
                value = json.loads(line.decode("utf-8", "replace"))
            except Exception:
                continue
            if isinstance(value, dict):
                return value
        return None

    def encode_frames(frames: list[dict]) -> bytes:
        return ("\n".join(json.dumps(frame) for frame in frames) + "\n").encode(
            "utf-8")

    def stop() -> None:
        if proc is None:
            return
        try:
            if proc.poll() is None:
                proc.kill()
            proc.wait(timeout=1)
        except Exception:
            pass

    try:
        proc = subprocess.Popen(
            [command, *args], cwd=str(cwd), stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        out_thread = threading.Thread(target=read_stdout, args=(proc.stdout,),
                                      daemon=True)
        err_thread = threading.Thread(target=drain_stderr, args=(proc.stderr,),
                                      daemon=True)
        out_thread.start(); err_thread.start()

        # Initialization is a real handshake, not a batch prefix: wait for the
        # response before sending the initialized notification or any request.
        proc.stdin.write(encode_frames([_initialize_message()]))
        proc.stdin.flush()
        init = None
        while remaining() > 0:
            msg = next_message()
            if msg is None:
                stop(); return None
            if msg.get("id") == 1:
                init = msg
                break
        if not init or "result" not in init:
            stop(); return None

        frames = [_initialized_message()]
        for i, uri in enumerate(uris, start=2):
            frames.append({"jsonrpc": "2.0", "id": i,
                           "method": "resources/read", "params": {"uri": uri}})
        payload = encode_frames(frames)
        input_state: dict = {"failed": False}

        def feed_remaining() -> None:
            try:
                proc.stdin.write(payload)
                proc.stdin.close()
            except (BrokenPipeError, OSError):
                input_state["failed"] = True

        input_thread = threading.Thread(target=feed_remaining, daemon=True)
        input_thread.start()
        by_id: dict[int, dict] = {}
        eof = False
        while remaining() > 0 and not eof:
            try:
                line = responses.get(timeout=max(0.05, remaining()))
            except queue.Empty:
                break
            if line is None:
                eof = True
                break
            try:
                msg = json.loads(line.decode("utf-8", "replace"))
            except Exception:
                continue
            if (isinstance(msg, dict) and isinstance(msg.get("id"), int)
                    and msg.get("id", 0) >= 2 and isinstance(msg.get("result"), dict)):
                by_id[msg["id"]] = msg["result"]
        if not eof:
            stop(); return None
        input_thread.join(timeout=1); out_thread.join(timeout=1); err_thread.join(timeout=1)
        try:
            proc.wait(timeout=max(0.05, remaining()))
        except subprocess.TimeoutExpired:
            stop(); return None
        if (proc.returncode != 0 or input_thread.is_alive()
                or input_state["failed"] or out_state["failed"]
                or out_state["oversized"]):
            return None
    except Exception:
        stop()
        return None

    got: dict[str, str] = {}
    for i, uri in enumerate(uris, start=2):
        r = by_id.get(i)
        if r:
            try:
                value = r["contents"][0]["text"]
                if isinstance(value, str):
                    got[uri] = value
            except Exception:
                pass
    return got


def _mcp_http_read(url: str, uris: list[str], timeout: int = 30,
                   headers: dict | None = None,
                   max_response_bytes: int = MAX_EXTERNAL_RESPONSE_BYTES
                   ) -> dict | None:
    # The same face read over Streamable HTTP: one POST per JSON-RPC message
    # (batching left the MCP spec), Accept covering both response shapes the
    # spec allows. A failed initialize is None — "sync state unknown", never a
    # silent fresh; a failed single read just leaves that URI absent, exactly
    # like an error response on stdio.
    import json
    import urllib.error
    import urllib.request
    from urllib.parse import urlsplit
    if urlsplit(url).scheme not in ("http", "https"):
        return None
    session = {"id": None}
    deadline = time.monotonic() + _bounded_timeout(timeout)
    response_budget = {"remaining": max(0, int(max_response_bytes)),
                       "exhausted": False}

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        # Trust pins one exact destination.  A redirect is a second destination
        # and therefore has no authority, even when it is same-origin.
        def redirect_request(self, req, fp, code, msg, headers_, newurl):
            return None

    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), _NoRedirect())

    def post(msg: dict, expect_response: bool = True) -> dict | None:
        req = urllib.request.Request(
            url, data=json.dumps(msg).encode(), method="POST",
            headers={"Content-Type": "application/json",
                     "Accept": "application/json, text/event-stream",
                     **(headers or {})})
        if session["id"]:
            req.add_header("Mcp-Session-Id", session["id"])
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return None
        with opener.open(req, timeout=max(0.05, remaining)) as r:
            sid = r.headers.get("Mcp-Session-Id")
            if sid:
                session["id"] = sid
            ctype = r.headers.get("Content-Type", "")
            declared = r.headers.get("Content-Length")
            if declared:
                try:
                    declared_size = int(declared)
                    if (declared_size < 0
                            or declared_size > response_budget["remaining"]):
                        response_budget["exhausted"] = True
                        return None
                except ValueError:
                    return None
            bounded = r.read(response_budget["remaining"] + 1)
            if len(bounded) > response_budget["remaining"]:
                response_budget["exhausted"] = True
                return None
            response_budget["remaining"] -= len(bounded)
            raw = bounded.decode("utf-8", "replace")
        if time.monotonic() > deadline:
            return None
        if not expect_response:
            return {}
        if ("application/json" not in ctype
                and "text/event-stream" not in ctype):
            return None
        if "text/event-stream" in ctype:  # SSE-wrapped response: last data frame
            frames = [ln[5:].strip() for ln in raw.splitlines() if ln.startswith("data:")]
            raw = frames[-1] if frames else ""
        return json.loads(raw) if raw.strip() else None

    try:
        init = post(_initialize_message())
        if not init or "result" not in init:
            return None
        # MCP lifecycle completion is a notification and therefore has no
        # JSON-RPC response body (the local server returns HTTP 202).
        if post(_initialized_message(), expect_response=False) is None:
            return None
    except Exception:
        return None
    got: dict[str, str] = {}
    for i, uri in enumerate(uris, start=2):
        try:
            resp = post({"jsonrpc": "2.0", "id": i, "method": "resources/read",
                         "params": {"uri": uri}})
            if resp and "result" in resp:
                value = resp["result"]["contents"][0]["text"]
                if isinstance(value, str):
                    got[uri] = value
        except Exception:
            pass
    if response_budget["exhausted"]:
        # A partial face is not a bounded successful operation.  In
        # particular, do not let an omitted oversized URI resemble a source
        # withdrawal while retaining earlier responses from the same read.
        return None
    return got


def _addressed(cfg) -> bool:
    return bool(isinstance(cfg, dict) and ("command" in cfg or "url" in cfg))


def _mcp_face_read(cfg: dict, cwd: Path, uris: list[str], server: str,
                   policy: ExternalTrustPolicy | None = None
                   ) -> tuple[str, dict | None]:
    # One consumer-side read, either transport — the membrane semantics
    # (unreachable = unknown, per-URI misses tolerated) are identical.  The
    # authority check occurs before selecting either I/O adapter.
    decision = (policy or LocalExternalTrustPolicy()).evaluate(cwd, server, cfg)
    if not decision.authorized:
        return decision.state, None
    if cfg.get("url"):
        # `headers` rides the entry (the ecosystem's .mcp.json convention) —
        # how a tunnelled probe carries its per-run bearer token.
        got = _mcp_http_read(cfg["url"], uris, headers=cfg.get("headers"))
    else:
        got = _mcp_client_read(cfg["command"], cfg.get("args", []), cwd, uris)
    return ("ok", got) if got is not None else ("unreachable", None)


def _face_body(rendered: str) -> str:
    # `thing://` text is `---\n{frontmatter}---\n\n{body}` (_mcp_render_thing).
    if not isinstance(rendered, str):
        return ""
    if rendered.startswith("---\n"):
        parts = rendered.split("---\n", 2)
        if len(parts) == 3:
            return parts[2]
    return rendered


def _norm_body(s: str) -> str:
    # Content identity for the divergence compare: trailing whitespace and
    # edge blank lines are transport noise, not edits.
    return "\n".join(line.rstrip() for line in s.strip().splitlines())


def _pins_match(a, b) -> bool:
    """Compare two commit pins as strings, whatever YAML made of them.

    An unquoted all-digit short hash (`source_commit: 2399917` — ~1 in 16 of
    them) parses as `int`, and `int != str` false-reported a healthy import
    STALE against its own pin, prescribing a re-quarantine that spends a
    human's attributed flip on nothing. Two consumer domains hit it
    independently and patched it locally by quoting; the framework's own CI
    then flaked on it. Normalise here, at the single comparison seam (v3.27.0)."""
    if a is None or b is None:
        return False
    left, right = str(a).strip(), str(b).strip()
    if left == right:
        return True
    # v3.33 migration: producers now stamp the immutable full commit while
    # existing consumer things legitimately carry the prior 7+-hex short pin.
    # Accept only an unambiguous shape transition, never arbitrary prefixes.
    import re
    hex_re = re.compile(r"^[0-9a-fA-F]+$")
    for short, full in ((left, right), (right, left)):
        if (7 <= len(short) < len(full)
                and len(full) in (40, 64)
                and hex_re.fullmatch(short) and hex_re.fullmatch(full)
                and full.lower().startswith(short.lower())):
            return True
    return False


def imports_freshness(consumer_root: Path) -> list[dict]:
    import json
    corpus, _ = scan(consumer_root)
    book, book_error = _load_address_book_result(consumer_root)
    imports = [t for t in corpus.things if origin_is_external(t.meta)]

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
        if book_error is not None:
            faces[sd] = ("unevaluable-invalid-config", None)
            continue
        cfg = book.get(sd)
        if not _addressed(cfg):
            faces[sd] = ("no-address", None)
            continue
        uris = [f"manifest://{sd}"] + [f"thing://{sd}/{sid}" for sid in sids]
        read_state, got = _mcp_face_read(cfg, consumer_root, uris, str(sd))
        if read_state != "ok":
            faces[sd] = (read_state, None)
            continue
        man = None
        if got and f"manifest://{sd}" in got:
            try:
                candidate = json.loads(got[f"manifest://{sd}"])
                man = candidate if isinstance(candidate, dict) else None
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
        elif state in {"unevaluable-untrusted", "unevaluable-invalid-config"}:
            row["state"] = state
        else:
            man, got = payload
            knows = man.get("knows", [])
            knows = knows if isinstance(knows, list) else []
            current = next((k.get("source_commit") for k in knows
                            if isinstance(k, dict) and k.get("id") == sid), None)
            if current is None:
                row["state"] = "withdrawn"  # no longer exposed by the source
            else:
                row["current"] = current
                if not _pins_match(current, pin):
                    row["state"] = "stale"
                    # Two stale species (v3.27.0): a source-side commit that
                    # touched only what egress strips (triggers, relational
                    # graph) moves the pin with NO crossable change — the full
                    # re-quarantine ritual, which spends a human's attributed
                    # flip, is owed only when the content actually moved.
                    src_text = got.get(f"thing://{sd}/{sid}")
                    if src_text is not None:
                        same = (_norm_body(_face_body(src_text))
                                == _norm_body(t.body))
                        row["species"] = ("content identical" if same
                                          else "content changed")
                else:
                    src_text = got.get(f"thing://{sd}/{sid}")
                    if src_text is None:
                        # Pin current, but the face returned no content for
                        # this thing: the divergence direction — one of the
                        # two the check promises — was unverifiable, and
                        # `fresh` would assert a comparison that never
                        # happened. Same conservatism as the stale branch
                        # above, which omits the species rather than guessing
                        # (substrate-totality-residue #2).
                        row["state"] = "unreachable"
                        row["detail"] = ("pin current, but the content read "
                                         "returned nothing — divergence "
                                         "unverifiable")
                    elif _norm_body(_face_body(src_text)) != _norm_body(t.body):
                        row["state"] = "diverged"
                    else:
                        row["state"] = "fresh"
        results.append(row)
    return results


def _render_rows(rows: list[dict]) -> None:
    order = {"stale": 0, "diverged": 1, "unreachable": 2, "withdrawn": 3,
             "unevaluable-untrusted": 3,
             "unevaluable-invalid-config": 4,
             "no-address-book-entry": 5, "incomplete": 6, "fresh": 7,
             "ingested": 8}
    for r in sorted(rows, key=lambda r: order.get(r["state"], 9)):
        if r["state"] == "stale":
            sp = f"  ({r['species']})" if r.get("species") else ""
            print(f"- STALE      {r['id']}  ({r['source']})  pinned {r['pin']} -> now {r['current']}{sp}")
            if r.get("species") == "content identical":
                print("             pin moved, nothing crossable changed: update `source_commit` to the current pin — re-quarantine not owed")
            else:
                print("             re-quarantine: re-read the source, then flip `verified: false`, `status: stale`")
        elif r["state"] == "diverged":
            print(f"- DIVERGED   {r['id']}  ({r['source']})  pin {r['pin']} is current but content differs")
            print("             the loop was bypassed: mirror edited locally, or source changed without committing — route as an inflection")
        elif r["state"] == "fresh":
            print(f"- fresh      {r['id']}  ({r['source']})  @ {r['pin']}")
        elif r["state"] == "unreachable":
            why = r.get("detail") or "sync state cannot be determined"
            print(f"- UNKNOWN    {r['id']}  ({r['source']})  unreachable — {why}")
        elif r["state"] == "unevaluable-untrusted":
            print(f"- UNTRUSTED  {r['id']}  ({r['source']})  external route was not executed")
            print("             review it with `mdllm external-trust review`; "
                  "trust remains clone-local and hash-bound")
        elif r["state"] == "unevaluable-invalid-config":
            print(f"- INVALID    {r['id']}  ({r['source']})  external route is not safe to evaluate")
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
    book, book_error = _load_address_book_result(consumer_root)
    imported: dict[str, int] = {}
    for t in corpus.things:
        if origin_is_external(t.meta) and t.meta.get("source_domain"):
            sd = str(t.meta["source_domain"])
            imported[sd] = imported.get(sd, 0) + 1
    if book_error is not None:
        return [{"source": ".mcp.json", "state": "unevaluable-invalid-config",
                 "offered": None, "imported": sum(imported.values())}]
    out = []
    for sd, cfg in sorted(book.items()):
        if not _addressed(cfg):
            continue
        read_state, got = _mcp_face_read(
            cfg, consumer_root, [f"manifest://{sd}"], str(sd))
        if read_state != "ok":
            out.append({"source": sd, "state": read_state,
                        "offered": None, "imported": imported.get(sd, 0)})
            continue
        man = None
        if got and f"manifest://{sd}" in got:
            import json
            try:
                candidate = json.loads(got[f"manifest://{sd}"])
                man = candidate if isinstance(candidate, dict) else None
            except Exception:
                man = None
        if man is None:
            out.append({"source": sd, "state": "unreachable",
                        "offered": None, "imported": imported.get(sd, 0)})
        else:
            out.append({"source": sd, "state": "ok",
                        "offered": len(man.get("knows"))
                        if isinstance(man.get("knows"), list) else 0,
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
        elif c["state"] == "unevaluable-untrusted":
            print(f"- {c['source']}: untrusted — route not executed "
                  f"({c['imported']} imported); review with `mdllm external-trust review`")
        elif c["state"] == "unevaluable-invalid-config":
            print(f"- {c['source']}: invalid external route — offering unevaluable "
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
