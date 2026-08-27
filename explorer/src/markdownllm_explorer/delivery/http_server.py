"""Loopback-only HTTP server with bounded concurrency and hardened headers."""

from __future__ import annotations

import hmac
import importlib.resources
import json
import socket
import re
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from markdownllm_explorer.composition import ExplorerRuntime
from markdownllm_explorer.core.errors import ExplorerError

from .response_encoding import to_wire


_ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.css": ("app.css", "text/css; charset=utf-8"),
    "/context.css": ("context.css", "text/css; charset=utf-8"),
    "/js/api.js": ("js/api.js", "text/javascript; charset=utf-8"),
    "/js/app.js": ("js/app.js", "text/javascript; charset=utf-8"),
    "/js/state.js": ("js/state.js", "text/javascript; charset=utf-8"),
    "/js/views/navigation.js": ("js/views/navigation.js", "text/javascript; charset=utf-8"),
    "/js/views/overview.js": ("js/views/overview.js", "text/javascript; charset=utf-8"),
    "/js/views/tree.js": ("js/views/tree.js", "text/javascript; charset=utf-8"),
    "/js/views/collection.js": ("js/views/collection.js", "text/javascript; charset=utf-8"),
    "/js/views/document.js": ("js/views/document.js", "text/javascript; charset=utf-8"),
    "/js/views/settings.js": ("js/views/settings.js", "text/javascript; charset=utf-8"),
    "/js/views/context.js": ("js/views/context.js", "text/javascript; charset=utf-8"),
}


class BoundedHTTPServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, address, handler, runtime: ExplorerRuntime) -> None:
        self.runtime = runtime
        self.capacity = threading.BoundedSemaphore(runtime.limits.concurrent_requests)
        super().__init__(address, handler)

    def process_request(self, request, client_address) -> None:
        if not self.capacity.acquire(blocking=False):
            try:
                body = b'{"error":{"code":"server_busy","message":"Explorer is busy. Try again.","retryable":true}}'
                request.sendall(
                    b"HTTP/1.1 429 Too Many Requests\r\nConnection: close\r\nContent-Type: application/json; charset=utf-8\r\nCache-Control: no-store\r\nContent-Length: "
                    + str(len(body)).encode() + b"\r\n\r\n" + body
                )
            finally:
                self.shutdown_request(request)
            return
        super().process_request(request, client_address)

    def process_request_thread(self, request, client_address) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self.capacity.release()


class ExplorerHandler(BaseHTTPRequestHandler):
    server_version = "MarkdownLLMExplorer/0.1"
    protocol_version = "HTTP/1.1"

    @property
    def runtime(self) -> ExplorerRuntime:
        return self.server.runtime  # type: ignore[attr-defined]

    def do_GET(self) -> None:
        self._handle(False)

    def do_HEAD(self) -> None:
        self._handle(True)

    def do_POST(self) -> None:
        self._error(ExplorerError("method_not_allowed"), False)

    do_PUT = do_POST
    do_DELETE = do_POST
    do_PATCH = do_POST
    do_OPTIONS = do_POST

    def _handle(self, head: bool) -> None:
        operation = "request"
        source_id: str | None = None
        try:
            host = self.headers.get("Host", "")
            expected_host = f"127.0.0.1:{self.server.server_port}"  # type: ignore[attr-defined]
            if host != expected_host:
                raise ExplorerError("host_forbidden")
            origin = self.headers.get("Origin")
            if origin and origin != f"http://{expected_host}":
                raise ExplorerError("origin_forbidden")
            target = urlsplit(self.path)
            operation = target.path.rsplit("/", 1)[-1] or "shell"
            if target.path == "/health":
                self._json(200, {"status": "ok"}, head)
                return
            if target.path.startswith("/api/"):
                supplied = self.headers.get("X-Explorer-Capability", "")
                if not supplied:
                    raise ExplorerError("capability_required")
                if not hmac.compare_digest(supplied, self.runtime.capability):
                    raise ExplorerError("capability_invalid")
                query = parse_qs(target.query, keep_blank_values=True, strict_parsing=False, max_num_fields=8)
                candidate_source = query.get("source", [None])[0]
                if isinstance(candidate_source, str) and re.fullmatch(r"(?:substrate|domain/[A-Za-z0-9._~%\-]{1,240})", candidate_source):
                    source_id = candidate_source
                result = self.runtime.routes.dispatch(target.path, query)
                self._json(200, {"data": to_wire(result)}, head)
                return
            if target.query or target.path not in _ASSETS:
                raise ExplorerError("route_not_found")
            asset, content_type = _ASSETS[target.path]
            package = importlib.resources.files("markdownllm_explorer.delivery.static")
            payload = package.joinpath(asset).read_bytes()
            self._send(200, payload, content_type, head)
        except ExplorerError as error:
            level = "error" if error.code == "internal_error" else "warning"
            print(f"{level} operation={operation} source={source_id or '-'} code={error.code}", file=sys.stderr, flush=True)
            self._error(error, head)
        except (ValueError, UnicodeError):
            self._error(ExplorerError("invalid_request"), head)
        except Exception:
            self._error(ExplorerError("internal_error"), head)

    def _json(self, status: int, value: object, head: bool) -> None:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(payload) > self.runtime.limits.response_bytes:
            raise ExplorerError("response_too_large")
        self._send(status, payload, "application/json; charset=utf-8", head)

    def _error(self, error: ExplorerError, head: bool) -> None:
        self._json(error.status, {"error": {"code": error.code, "message": error.public_message, "retryable": error.retryable}}, head)

    def _send(self, status: int, payload: bytes, content_type: str, head: bool) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; connect-src 'self'")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.end_headers()
        if not head:
            self.wfile.write(payload)

    def log_message(self, format: str, *args) -> None:
        return


def serve(runtime: ExplorerRuntime, port: int = 0) -> tuple[BoundedHTTPServer, str]:
    server = BoundedHTTPServer(("127.0.0.1", port), ExplorerHandler, runtime)
    url = f"http://127.0.0.1:{server.server_port}/#cap={runtime.capability}"
    return server, url
