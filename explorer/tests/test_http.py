from __future__ import annotations

import http.client
import json
import threading

import pytest

from markdownllm_explorer import __version__
from markdownllm_explorer.composition import build_runtime
from markdownllm_explorer.delivery.http_server import serve


@pytest.fixture
def live_server(estate):
    runtime = build_runtime(estate)
    server, url = serve(runtime)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, runtime, url
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=2)


def request(server, method, target, headers=None):
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
    connection.request(method, target, headers={"Host": f"127.0.0.1:{server.server_port}", **(headers or {})})
    response = connection.getresponse(); body = response.read(); response_headers = dict(response.getheaders()); connection.close()
    return response.status, response_headers, body


@pytest.mark.system
def test_health_is_minimal_and_static_shell_contains_no_estate_data(live_server):
    server, _, _ = live_server
    status, headers, body = request(server, "GET", "/health")
    assert status == 200 and json.loads(body) == {"status": "ok", "version": __version__}
    status, headers, body = request(server, "GET", "/")
    assert status == 200 and b"MarkdownLLM Explorer" in body and b"Fixture substrate" not in body
    assert "frame-ancestors 'none'" in headers["Content-Security-Policy"]
    assert "Access-Control-Allow-Origin" not in headers
    assert headers["Cache-Control"] == "no-store"
    assert request(server, "GET", "/context.css")[0] == 200
    assert request(server, "GET", "/js/views/context.js")[0] == 200


@pytest.mark.system
def test_api_requires_exact_capability_host_and_origin(live_server):
    server, runtime, _ = live_server
    status, _, body = request(server, "GET", "/api/v1/estate")
    assert status == 401 and json.loads(body)["error"]["code"] == "capability_required"
    status, _, body = request(server, "GET", "/api/v1/estate", {"X-Explorer-Capability": "wrong"})
    assert status == 401 and json.loads(body)["error"]["code"] == "capability_invalid"
    status, _, body = request(server, "GET", "/api/v1/estate", {"X-Explorer-Capability": runtime.capability, "Origin": "https://evil.invalid"})
    assert status == 403 and json.loads(body)["error"]["code"] == "origin_forbidden"
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
    connection.request("GET", "/api/v1/estate", headers={"Host": "evil.invalid", "X-Explorer-Capability": runtime.capability})
    response = connection.getresponse(); payload = json.loads(response.read()); connection.close()
    assert response.status == 403 and payload["error"]["code"] == "host_forbidden"


@pytest.mark.system
def test_authenticated_api_has_public_dto_without_boundary_token(live_server):
    server, runtime, _ = live_server
    status, _, body = request(server, "GET", "/api/v1/estate", {"X-Explorer-Capability": runtime.capability})
    assert status == 200
    assert b"boundary_token" not in body and b"SourceBoundary" not in body
    envelope = json.loads(body); payload = envelope["data"]
    assert payload["sources"][0]["id"] == "substrate"
    assert len(envelope["meta"]["request_id"]) == 32 and envelope["meta"]["observed_at"].endswith("+00:00")
    second = request(server, "GET", "/api/v1/estate", {"X-Explorer-Capability": runtime.capability})
    assert json.loads(second[2])["meta"]["request_id"] != envelope["meta"]["request_id"]


@pytest.mark.system
@pytest.mark.parametrize("target", [
    "/api/v1/document?source=substrate&path=../outside.md",
    "/api/v1/document?source=substrate&path=%2e%2e%2foutside.md",
    "/api/v1/document?source=substrate&path=secret-token.md",
    "/api/v1/document?source=substrate&path=domain/demo/AGENTS.md",
])
def test_http_boundary_attacks_return_stable_public_errors(live_server, target, capsys):
    server, runtime, _ = live_server
    status, _, body = request(server, "GET", target, {"X-Explorer-Capability": runtime.capability})
    payload = json.loads(body)["error"]
    assert status in {400, 403}
    assert payload["code"] in {"invalid_path", "path_excluded"}
    assert "Jamos" not in payload["message"] and "substrate" not in payload["message"].casefold()
    captured = capsys.readouterr().err
    assert "outside.md" not in captured and "secret-token" not in captured and "../" not in captured


@pytest.mark.system
def test_document_api_returns_exactly_one_mode_representation(live_server):
    server, runtime, _ = live_server
    headers = {"X-Explorer-Capability": runtime.capability}
    for mode in ("raw", "rendered"):
        status, _, body = request(server, "GET", f"/api/v1/document?source=substrate&path=AGENTS.md&mode={mode}", headers)
        document = json.loads(body)["data"]
        assert status == 200 and document["mode"] == mode and isinstance(document["content"], str)
        assert set(document) == {"source_id", "path", "mode", "content", "frontmatter", "size", "modified_at", "issues"}


@pytest.mark.system
def test_only_get_and_head_are_allowed(live_server):
    server, runtime, _ = live_server
    headers = {"X-Explorer-Capability": runtime.capability}
    for method in ("POST", "PUT", "PATCH", "DELETE", "OPTIONS"):
        status, _, body = request(server, method, "/api/v1/estate", headers)
        assert status == 405 and json.loads(body)["error"]["code"] == "method_not_allowed"
    status, response_headers, body = request(server, "HEAD", "/api/v1/estate", headers)
    assert status == 200 and body == b"" and int(response_headers["Content-Length"]) > 0


@pytest.mark.system
def test_all_method_and_busy_responses_validate_boundary_and_share_security_headers(live_server):
    server, runtime, _ = live_server
    security = {"Cache-Control", "Content-Security-Policy", "X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Permissions-Policy", "Cross-Origin-Resource-Policy"}
    status, headers, body = request(server, "POST", "/api/v1/estate", {"Origin": "https://evil.invalid"})
    assert status == 403 and json.loads(body)["error"]["code"] == "origin_forbidden" and security <= set(headers)
    server.join_active(1)
    acquired = 0
    try:
        for _ in range(runtime.limits.concurrent_requests):
            assert server.capacity.acquire(blocking=False); acquired += 1
        status, headers, body = request(server, "GET", "/health")
        payload = json.loads(body)
        assert status == 429 and payload["error"]["code"] == "server_busy" and len(payload["meta"]["request_id"]) == 32
        assert security <= set(headers)
    finally:
        for _ in range(acquired): server.capacity.release()


@pytest.mark.system
def test_unknown_static_assets_are_not_directory_served(live_server):
    server, _, _ = live_server
    for target in ("/../pyproject.toml", "/js/../app.css", "/.git/config", "/missing.js"):
        status, _, body = request(server, "GET", target)
        assert status == 404 and json.loads(body)["error"]["code"] == "route_not_found"
