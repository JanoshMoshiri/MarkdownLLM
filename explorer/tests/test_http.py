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
    status, _, body = request(server, "GET", "/api/v1/estate", {"X-MDLLM-Capability": runtime.capability})
    assert status == 401 and json.loads(body)["error"]["code"] == "capability_required"
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
    assert set(envelope) == {"data", "meta"} and set(envelope["meta"]) == {"request_id", "observed_at"}
    assert "observed_at" not in payload
    assert len(envelope["meta"]["request_id"]) == 32 and envelope["meta"]["observed_at"].endswith("+00:00")
    second = request(server, "GET", "/api/v1/estate", {"X-Explorer-Capability": runtime.capability})
    assert json.loads(second[2])["meta"]["request_id"] != envelope["meta"]["request_id"]


@pytest.mark.system
def test_pagination_metadata_has_one_exact_wire_location_and_omits_absent_cursor(live_server):
    server, runtime, _ = live_server
    headers = {"X-Explorer-Capability": runtime.capability}
    for target in ("/api/v1/tree?source=substrate", "/api/v1/search?source=substrate&q=md", "/api/v1/collection?source=substrate&kind=skills"):
        status, _, body = request(server, "GET", target, headers)
        envelope = json.loads(body)
        assert status == 200 and set(envelope["data"]) == {"items"}
        assert "partial" in envelope["meta"] and "observed_at" in envelope["meta"]
        assert "next_cursor" not in envelope["data"] and "partial" not in envelope["data"] and "observed_at" not in envelope["data"]
        if not envelope["meta"].get("next_cursor"):
            assert "next_cursor" not in envelope["meta"]
    status, _, body = request(server, "GET", "/api/v1/overview?source=substrate", headers)
    envelope = json.loads(body)
    assert status == 200 and set(envelope["data"]["commits"]) == {"items"}
    assert "partial" in envelope["meta"] and "next_cursor" not in envelope["data"]["commits"]


@pytest.mark.system
def test_error_dto_is_exact_contextual_and_redacted(live_server):
    server, runtime, _ = live_server; headers = {"X-Explorer-Capability": runtime.capability}
    status, _, body = request(server, "GET", "/api/v1/document?source=substrate&path=secret-token.md", headers)
    envelope = json.loads(body)
    assert status == 403 and set(envelope) == {"error", "meta"}
    assert set(envelope["error"]) == {"code", "message", "retryable", "source_id", "relative_path"}
    assert envelope["error"]["source_id"] == "substrate" and envelope["error"]["relative_path"] == "secret-token.md"
    assert set(envelope["meta"]) == {"request_id", "observed_at"}
    assert not any("Jamos" in str(value) for value in envelope.values())


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
    assert json.loads(request(server, "POST", "/api/v1/estate")[2])["error"]["code"] == "capability_required"
    assert json.loads(request(server, "POST", "/api/v1/estate", {"X-Explorer-Capability": "wrong"})[2])["error"]["code"] == "capability_invalid"
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

@pytest.mark.system
def test_commit_reference_and_historical_routes_cross_the_http_boundary(live_server):
    """The three new routes and every DTO branch they publish, over real HTTP.

    Exercised end to end rather than through the use cases, because the wire
    encoding is where a field is silently dropped or a boundary token could
    escape, and neither is visible from inside the application layer.
    """
    server, runtime, _ = live_server
    capability = {"X-Explorer-Capability": runtime.capability}

    status, _, body = request(server, "GET", "/api/v1/overview?source=substrate", capability)
    assert status == 200
    sha = json.loads(body)["data"]["commits"]["items"][0]["sha"]
    assert len(sha) == 40

    status, _, body = request(server, "GET", f"/api/v1/commit?source=substrate&sha={sha}", capability)
    assert status == 200
    detail = json.loads(body)["data"]
    assert set(detail) == {"sha", "subject", "author_name", "authored_at", "files", "partial"}
    assert detail["sha"] == sha and detail["partial"] is False
    files = {item["path"]: item for item in detail["files"]}
    assert set(files["AGENTS.md"]) == {"path", "change", "openable", "regular"}
    assert files["AGENTS.md"]["openable"] is True and files["AGENTS.md"]["regular"] is True
    # Git reports these; source admission is what refuses them.
    assert files[".env"]["openable"] is False
    assert files["domain/demo/AGENTS.md"]["openable"] is False

    status, _, body = request(server, "GET", f"/api/v1/commit-file?source=substrate&sha={sha}&path=AGENTS.md", capability)
    assert status == 200
    record = json.loads(body)["data"]
    assert set(record) == {"source_id", "path", "sha", "content", "added_ranges", "size", "ranges_known"}
    assert record["ranges_known"] is True and record["added_ranges"] == [[1, len(record["content"].splitlines())]]
    assert "Fixture substrate" in record["content"]

    status, _, body = request(server, "GET", "/api/v1/references?source=substrate&ids=demo,shared,absent-thing", capability)
    assert status == 200
    resolution = json.loads(body)["data"]
    assert set(resolution) == {"source_id", "resolved", "unresolved", "partial"}
    assert resolution["resolved"] == {"demo": "skills/demo.md"}
    # `shared` is claimed by two fixture files, so it resolves to neither rather
    # than to whichever the walk reached first.
    assert sorted(resolution["unresolved"]) == ["absent-thing", "shared"]

    # No response may carry an internal boundary token.
    for target in (f"/api/v1/commit?source=substrate&sha={sha}", "/api/v1/references?source=substrate&ids=shared"):
        assert b"boundary_token" not in request(server, "GET", target, capability)[2]


@pytest.mark.system
def test_new_routes_reject_unknown_parameters_and_missing_capability(live_server):
    server, runtime, _ = live_server
    capability = {"X-Explorer-Capability": runtime.capability}
    sha = "0" * 40
    for target in (
        f"/api/v1/commit?source=substrate&sha={sha}&extra=1",
        f"/api/v1/commit-file?source=substrate&sha={sha}",
        "/api/v1/references?source=substrate",
    ):
        assert request(server, "GET", target, capability)[0] == 400
    for target in (f"/api/v1/commit?source=substrate&sha={sha}", "/api/v1/references?source=substrate&ids=shared"):
        assert request(server, "GET", target)[0] == 401
