"""Loopback-only HTTP server with bounded concurrency and hardened headers."""

from __future__ import annotations

import hmac
import importlib.resources
import json
import socket
import re
import secrets
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import TYPE_CHECKING
from urllib.parse import parse_qs, urlsplit

from markdownllm_explorer import __version__
from markdownllm_explorer.core.errors import ExplorerError

from .response_encoding import to_wire

if TYPE_CHECKING:
    from markdownllm_explorer.composition import ExplorerRuntime


_ASSETS = {
    "/": ("index.html", "text/html; charset=utf-8"),
    "/index.html": ("index.html", "text/html; charset=utf-8"),
    "/app.css": ("app.css", "text/css; charset=utf-8"),
    "/context.css": ("context.css", "text/css; charset=utf-8"),
    "/js/api.js": ("js/api.js", "text/javascript; charset=utf-8"),
    "/js/app.js": ("js/app.js", "text/javascript; charset=utf-8"),
    "/js/state.js": ("js/state.js", "text/javascript; charset=utf-8"),
    "/js/routing.js": ("js/routing.js", "text/javascript; charset=utf-8"),
    "/js/theme.js": ("js/theme.js", "text/javascript; charset=utf-8"),
    "/js/overlays.js": ("js/overlays.js", "text/javascript; charset=utf-8"),
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
        self.active_threads: set[threading.Thread] = set()
        self.active_lock = threading.Lock()
        super().__init__(address, handler)

    def get_request(self):
        request, address = super().get_request()
        request.settimeout(15.0)
        return request, address

    def process_request(self, request, client_address) -> None:
        if not self.capacity.acquire(blocking=False):
            try:
                request_id = secrets.token_hex(16)
                body = json.dumps({"error":{"code":"server_busy","message":"Explorer is busy. Try again.","retryable":True},"meta":{"request_id":request_id,"observed_at":_observed_at()}}, separators=(",", ":")).encode()
                headers = _raw_security_headers(len(body), "application/json; charset=utf-8")
                request.sendall(
                    b"HTTP/1.1 429 Too Many Requests\r\nConnection: close\r\n" + headers + b"\r\n" + body
                )
                # Finish the response half first, then consume the already-sent
                # bounded request headers so Windows does not turn the close into
                # a TCP reset before the client receives the admission response.
                request.shutdown(socket.SHUT_WR)
                request.settimeout(0.2)
                received = 0
                while received < 16 * 1024:
                    try:
                        chunk = request.recv(min(4096, 16 * 1024 - received))
                    except (TimeoutError, OSError):
                        break
                    if not chunk:
                        break
                    received += len(chunk)
            finally:
                self.shutdown_request(request)
            return
        super().process_request(request, client_address)

    def process_request_thread(self, request, client_address) -> None:
        current = threading.current_thread()
        with self.active_lock:
            self.active_threads.add(current)
        try:
            super().process_request_thread(request, client_address)
        finally:
            with self.active_lock:
                self.active_threads.discard(current)
            self.capacity.release()

    def join_active(self, timeout: float) -> None:
        deadline = time.monotonic() + timeout
        with self.active_lock:
            threads = tuple(self.active_threads)
        for thread in threads:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            thread.join(remaining)


class ExplorerHandler(BaseHTTPRequestHandler):
    server_version = "MarkdownLLMExplorer/0.1"
    protocol_version = "HTTP/1.1"

    @property
    def runtime(self) -> ExplorerRuntime:
        return self.server.runtime  # type: ignore[attr-defined]

    def setup(self) -> None:
        super().setup()
        self.request_id = secrets.token_hex(16)

    def do_GET(self) -> None:
        self._handle(False)

    def do_HEAD(self) -> None:
        self._handle(True)

    def do_POST(self) -> None:
        try:
            self._validate_web_boundary()
            if urlsplit(self.path).path.startswith("/api/"):
                supplied = self.headers.get("X-Explorer-Capability", "")
                if not supplied:
                    raise ExplorerError("capability_required")
                if not hmac.compare_digest(supplied, self.runtime.capability):
                    raise ExplorerError("capability_invalid")
            self._error(ExplorerError("method_not_allowed"), False)
        except ExplorerError as error:
            self._error(error, False)

    do_PUT = do_POST
    do_DELETE = do_POST
    do_PATCH = do_POST
    do_OPTIONS = do_POST

    def _handle(self, head: bool) -> None:
        operation = "request"
        source_id: str | None = None
        try:
            self._validate_web_boundary()
            target = urlsplit(self.path)
            operation = target.path.rsplit("/", 1)[-1] or "shell"
            if target.path == "/health":
                self._json(200, {"status": "ok", "version": __version__}, head)
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
                    self.request_source_id = source_id
                candidate_path = query.get("path", [None])[0]
                if isinstance(candidate_path, str) and _safe_relative_context(candidate_path):
                    self.request_relative_path = candidate_path
                result = self.runtime.routes.dispatch(target.path, query)
                self._json(200, {"data": to_wire(result), "meta": self._success_meta(result)}, head)
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
            print(f"error operation={operation} source={source_id or '-'} request_id={self.request_id} code=internal_error", file=sys.stderr, flush=True)
            self._error(ExplorerError("internal_error"), head)

    def _validate_web_boundary(self) -> None:
        host = self.headers.get("Host", "")
        expected_host = f"127.0.0.1:{self.server.server_port}"  # type: ignore[attr-defined]
        if host != expected_host:
            raise ExplorerError("host_forbidden")
        origin = self.headers.get("Origin")
        if origin and origin != f"http://{expected_host}":
            raise ExplorerError("origin_forbidden")

    def _success_meta(self, result: object) -> dict[str, object]:
        meta: dict[str, object] = {"request_id": self.request_id, "observed_at": getattr(result, "observed_at", _observed_at())}
        page = result if hasattr(result, "next_cursor") else getattr(result, "commits", None)
        if page is not None:
            next_cursor = getattr(page, "next_cursor", None)
            if next_cursor is not None:
                meta["next_cursor"] = next_cursor
            meta["partial"] = bool(getattr(page, "partial", False))
        return meta

    def _json(self, status: int, value: object, head: bool) -> None:
        payload = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        if len(payload) > self.runtime.limits.response_bytes:
            raise ExplorerError("response_too_large")
        self._send(status, payload, "application/json; charset=utf-8", head)

    def _error(self, error: ExplorerError, head: bool) -> None:
        details: dict[str, object] = {"code": error.code, "message": error.public_message, "retryable": error.retryable}
        source_id = error.source_id or getattr(self, "request_source_id", None)
        relative_path = error.relative_path or getattr(self, "request_relative_path", None)
        if source_id:
            details["source_id"] = source_id
        if relative_path and error.code != "path_outside_source":
            details["relative_path"] = relative_path
        self._json(error.status, {"error": details, "meta": {"request_id": self.request_id, "observed_at": _observed_at()}}, head)

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

    def send_error(self, code: int, message: str | None = None, explain: str | None = None) -> None:
        mapped = "method_not_allowed" if code == 405 else "invalid_request"
        self._error(ExplorerError(mapped), getattr(self, "command", "") == "HEAD")


def serve(runtime: ExplorerRuntime, port: int = 0) -> tuple[BoundedHTTPServer, str]:
    server = BoundedHTTPServer(("127.0.0.1", port), ExplorerHandler, runtime)
    url = f"http://127.0.0.1:{server.server_port}/#cap={runtime.capability}"
    return server, url


def _observed_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_relative_context(value: str) -> bool:
    return bool(
        0 < len(value) <= 4096
        and not value.startswith(("/", "\\"))
        and "\x00" not in value
        and ":" not in value
        and all(part not in {"", ".", ".."} for part in value.replace("\\", "/").split("/"))
    )


def _raw_security_headers(length: int, content_type: str) -> bytes:
    values = [
        f"Content-Type: {content_type}", f"Content-Length: {length}", "Cache-Control: no-store",
        "Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self'; img-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'; connect-src 'self'",
        "X-Content-Type-Options: nosniff", "X-Frame-Options: DENY", "Referrer-Policy: no-referrer",
        "Permissions-Policy: camera=(), microphone=(), geolocation=()", "Cross-Origin-Resource-Policy: same-origin",
    ]
    return ("\r\n".join(values) + "\r\n").encode("ascii")
