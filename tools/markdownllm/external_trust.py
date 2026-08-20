"""Clone-local authorization for repository-declared external MCP routes.

``.mcp.json`` is repository content.  It is therefore data to inspect, not
authority to launch a process or contact a network address.  This module is
the application port at that boundary and the Git-directory-backed adapter
used by the CLI.  Approval records contain no configuration or credentials:
they pin a capability set to the hash of one exact server entry in one exact
clone.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Protocol, Sequence
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


class ExternalCapability(str, Enum):
    COMMAND = "command"
    NETWORK = "network"
    HEADERS = "headers"
    BODY_READ = "body-read"


CAPABILITY_NAMES = tuple(cap.value for cap in ExternalCapability)
TRUST_STORE_VERSION = 1
TRUST_STORE_RELATIVE = Path("markdownllm") / "external-trust.json"
MAX_MCP_CONFIG_BYTES = 1024 * 1024
_SENSITIVE_ARG = re.compile(
    r"(?:token|password|passwd|secret|api[-_]?key|credential|authorization|auth)",
    re.IGNORECASE,
)
_FORBIDDEN_HEADER_NAMES = {
    "accept", "connection", "content-length", "content-type", "host",
    "mcp-session-id", "proxy-authorization", "te", "transfer-encoding",
    "upgrade",
}


class ExternalTrustError(ValueError):
    """A declaration or local trust operation is not safe to apply."""


def _json_object_without_duplicates(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ExternalTrustError(f"duplicate JSON key {key!r}")
        value[key] = item
    return value


def load_mcp_address_book(root: Path) -> dict:
    """Load the bounded address book without accepting duplicate-key shadowing."""
    path = Path(root) / ".mcp.json"
    if not path.is_file():
        raise ExternalTrustError(f"no .mcp.json in {Path(root).resolve()}")
    try:
        size = path.stat().st_size
        if size > MAX_MCP_CONFIG_BYTES:
            raise ExternalTrustError(
                f".mcp.json exceeds the {MAX_MCP_CONFIG_BYTES}-byte safety limit")
        raw = path.read_bytes().decode("utf-8")
        data = json.loads(raw, object_pairs_hook=_json_object_without_duplicates)
    except ExternalTrustError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalTrustError(f"cannot read .mcp.json: {exc}") from exc
    book = data.get("mcpServers") if isinstance(data, dict) else None
    if not isinstance(book, dict):
        raise ExternalTrustError(".mcp.json must contain an mcpServers object")
    return book


@dataclass(frozen=True)
class RepositoryIdentity:
    root: Path
    repository_id: str
    git_dir: Path | None


@dataclass(frozen=True)
class TrustDecision:
    repository_id: str
    server: str
    entry_hash: str
    required: frozenset[ExternalCapability]
    granted: frozenset[ExternalCapability]
    errors: tuple[str, ...] = ()
    store_path: Path | None = None

    @property
    def missing(self) -> frozenset[ExternalCapability]:
        return self.required - self.granted

    @property
    def authorized(self) -> bool:
        return not self.errors and not self.missing

    @property
    def command_authorized(self) -> bool:
        return ExternalCapability.COMMAND in self.granted

    @property
    def network_authorized(self) -> bool:
        return ExternalCapability.NETWORK in self.granted

    @property
    def headers_authorized(self) -> bool:
        return ExternalCapability.HEADERS in self.granted

    @property
    def body_read_authorized(self) -> bool:
        return ExternalCapability.BODY_READ in self.granted

    @property
    def state(self) -> str:
        if self.errors:
            return "unevaluable-invalid-config"
        if self.missing:
            return "unevaluable-untrusted"
        return "trusted"


class ExternalTrustPolicy(Protocol):
    """Application port: decide authority without performing external I/O."""

    def evaluate(self, repository: Path, server: str,
                 entry: object) -> TrustDecision:
        ...


def _run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, capture_output=True, text=True,
            timeout=5, check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode:
        return None
    return result.stdout.strip() or None


def repository_identity(root: Path) -> RepositoryIdentity:
    """Return a clone-specific identity and its uncommittable Git directory."""
    requested = Path(root).resolve()
    top = _run_git(requested, "rev-parse", "--show-toplevel")
    repo_root = Path(top).resolve() if top else requested
    git_dir_raw = _run_git(requested, "rev-parse", "--absolute-git-dir")
    if git_dir_raw is None:
        legacy = _run_git(requested, "rev-parse", "--git-dir")
        if legacy:
            candidate = Path(legacy)
            git_dir_raw = str(candidate if candidate.is_absolute()
                              else (requested / candidate).resolve())
    git_dir = Path(git_dir_raw).resolve() if git_dir_raw else None
    # The path makes the grant clone-local even when two clones share a remote;
    # the per-worktree Git directory keeps linked worktrees separate as well.
    material = json.dumps(
        {"root": str(repo_root), "git_dir": str(git_dir) if git_dir else None},
        sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    ).encode("utf-8")
    repo_id = "sha256:" + hashlib.sha256(material).hexdigest()
    return RepositoryIdentity(repo_root, repo_id, git_dir)


def canonical_entry_hash(repository_id: str, server: str, entry: object) -> str:
    """Hash the exact selected declaration plus the clone identity."""
    try:
        raw = json.dumps(
            {"schema": TRUST_STORE_VERSION, "repository_id": repository_id,
             "server": server, "entry": entry},
            sort_keys=True, separators=(",", ":"), ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        # Still return a stable non-authorizing fingerprint for review output.
        raw = repr((repository_id, server, entry)).encode("utf-8", "replace")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _is_loopback_host(host: str | None) -> bool:
    if not host:
        return False
    if host.lower() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def validate_external_entry(entry: object) -> tuple[
        frozenset[ExternalCapability], tuple[str, ...]]:
    """Return the exact capabilities required and declaration errors."""
    if not isinstance(entry, dict):
        return frozenset(), ("server entry must be a JSON object",)
    has_command = "command" in entry
    has_url = "url" in entry
    if has_command == has_url:
        return frozenset(), ("server entry must declare exactly one of command or url",)

    errors: list[str] = []
    required = {ExternalCapability.BODY_READ}
    if has_command:
        required.add(ExternalCapability.COMMAND)
        if not isinstance(entry.get("command"), str) or not entry["command"].strip():
            errors.append("command must be a non-empty string")
        args = entry.get("args", [])
        if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
            errors.append("args must be an array of strings")
        if "env" in entry:
            errors.append("env is not supported; put credentials outside repository config")
    else:
        required.add(ExternalCapability.NETWORK)
        url = entry.get("url")
        if not isinstance(url, str) or not url.strip():
            errors.append("url must be a non-empty string")
        else:
            try:
                parts = urlsplit(url)
                _ = parts.port  # force malformed-port validation
            except ValueError:
                parts = None
                errors.append("url has an invalid port")
            if parts is not None:
                if parts.scheme not in {"http", "https"}:
                    errors.append("url scheme must be https, or http on loopback")
                elif parts.scheme == "http" and not _is_loopback_host(parts.hostname):
                    errors.append("plain HTTP is allowed only for a loopback host")
                if not parts.hostname:
                    errors.append("url must name a host")
                if parts.username is not None or parts.password is not None:
                    errors.append("url userinfo is forbidden; use an authorized header")
                if parts.fragment:
                    errors.append("url fragments are forbidden")
                if any(ord(c) < 32 or c.isspace() for c in url):
                    errors.append("url contains whitespace or control characters")
        headers = entry.get("headers", {})
        if headers is None:
            headers = {}
        if headers:
            required.add(ExternalCapability.HEADERS)
        if not isinstance(headers, dict):
            errors.append("headers must be an object")
        else:
            for key, value in headers.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    errors.append("header names and values must be strings")
                    break
                if (not key.strip() or any(c in key for c in "\r\n:")
                        or key.lower() in _FORBIDDEN_HEADER_NAMES):
                    errors.append(f"header name {key!r} is reserved or invalid")
                if "\r" in value or "\n" in value:
                    errors.append(f"header {key!r} contains a line break")
    return frozenset(required), tuple(dict.fromkeys(errors))


def required_capabilities(entry: object) -> frozenset[ExternalCapability]:
    return validate_external_entry(entry)[0]


def _store_path(identity: RepositoryIdentity) -> Path | None:
    return identity.git_dir / TRUST_STORE_RELATIVE if identity.git_dir else None


def _empty_store(identity: RepositoryIdentity) -> dict:
    return {"schema": TRUST_STORE_VERSION,
            "repository_id": identity.repository_id, "entries": {}}


def _load_store(identity: RepositoryIdentity) -> dict:
    path = _store_path(identity)
    if path is None or not path.is_file():
        return _empty_store(identity)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_store(identity)
    if (not isinstance(value, dict)
            or value.get("schema") != TRUST_STORE_VERSION
            or value.get("repository_id") != identity.repository_id
            or not isinstance(value.get("entries"), dict)):
        return _empty_store(identity)
    return value


def _write_store(identity: RepositoryIdentity, store: dict) -> Path:
    path = _store_path(identity)
    if path is None:
        raise ExternalTrustError(
            "trust cannot be recorded: the consumer is not inside a Git clone")
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(store, indent=2, sort_keys=True) + "\n"
    fd, tmp_name = tempfile.mkstemp(prefix="external-trust-", suffix=".tmp",
                                    dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.chmod(tmp_name, 0o600)
        except OSError:
            pass
        os.replace(tmp_name, path)
    finally:
        try:
            Path(tmp_name).unlink(missing_ok=True)
        except OSError:
            pass
    return path


class LocalExternalTrustPolicy:
    """Evaluate grants stored under this clone's Git directory."""

    def evaluate(self, repository: Path, server: str,
                 entry: object) -> TrustDecision:
        identity = repository_identity(repository)
        required, errors = validate_external_entry(entry)
        digest = canonical_entry_hash(identity.repository_id, server, entry)
        store = _load_store(identity)
        record = store["entries"].get(server)
        granted: set[ExternalCapability] = set()
        if (isinstance(record, dict)
                and record.get("entry_hash") == digest):
            for value in record.get("permissions") or []:
                try:
                    granted.add(ExternalCapability(value))
                except ValueError:
                    continue
        return TrustDecision(
            identity.repository_id, server, digest, required,
            frozenset(granted), errors, _store_path(identity),
        )


def grant_external_trust(repository: Path, server: str, entry: object,
                         permissions: Sequence[str | ExternalCapability],
                         expected_hash: str) -> TrustDecision:
    """Record an explicit hash-confirmed, capability-granular local grant."""
    identity = repository_identity(repository)
    required, errors = validate_external_entry(entry)
    digest = canonical_entry_hash(identity.repository_id, server, entry)
    normalized_hash = expected_hash if expected_hash.startswith("sha256:") \
        else "sha256:" + expected_hash
    if normalized_hash != digest:
        raise ExternalTrustError(
            f"hash mismatch: reviewed {normalized_hash}, current entry is {digest}")
    if errors:
        raise ExternalTrustError("invalid server entry: " + "; ".join(errors))
    try:
        requested = {p if isinstance(p, ExternalCapability)
                     else ExternalCapability(p) for p in permissions}
    except ValueError as exc:
        raise ExternalTrustError(f"unknown permission: {exc}") from exc
    irrelevant = requested - required
    if irrelevant:
        raise ExternalTrustError(
            "permissions not used by this entry: "
            + ", ".join(sorted(p.value for p in irrelevant)))
    if not requested:
        raise ExternalTrustError("at least one --allow permission is required")
    store = _load_store(identity)
    previous = store["entries"].get(server)
    combined = set(requested)
    if isinstance(previous, dict) and previous.get("entry_hash") == digest:
        for value in previous.get("permissions") or []:
            try:
                combined.add(ExternalCapability(value))
            except ValueError:
                pass
    store["entries"][server] = {
        "entry_hash": digest,
        "permissions": sorted(p.value for p in combined),
        "reviewed_at": datetime.now(timezone.utc).isoformat(),
    }
    path = _write_store(identity, store)
    return TrustDecision(identity.repository_id, server, digest, required,
                         frozenset(combined), (), path)


def revoke_external_trust(repository: Path, server: str | None = None) -> int:
    """Revoke one server's grant, or every local grant when server is absent."""
    identity = repository_identity(repository)
    store = _load_store(identity)
    before = len(store["entries"])
    if server is None:
        store["entries"].clear()
    else:
        store["entries"].pop(server, None)
    removed = before - len(store["entries"])
    if removed:
        _write_store(identity, store)
    return removed


def _safe_url_for_review(value: object) -> str:
    if not isinstance(value, str):
        return repr(value)
    try:
        parts = urlsplit(value)
        host = parts.hostname or ""
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        if parts.port is not None:
            host += f":{parts.port}"
        query = urlencode([(key, "<redacted>")
                           for key, _ in parse_qsl(parts.query,
                                                  keep_blank_values=True)])
        return urlunsplit((parts.scheme, host, parts.path, query, ""))
    except (TypeError, ValueError):
        return "<invalid URL; exact bytes represented by the hash>"


def _safe_args_for_review(args: object) -> list[str]:
    if not isinstance(args, list):
        return [repr(args)]
    shown: list[str] = []
    redact_next = False
    for value in args:
        if not isinstance(value, str):
            shown.append(repr(value))
            redact_next = False
            continue
        if redact_next:
            shown.append("<redacted>")
            redact_next = False
            continue
        if "=" in value and _SENSITIVE_ARG.search(value.split("=", 1)[0]):
            shown.append(value.split("=", 1)[0] + "=<redacted>")
        elif value.startswith("-") and _SENSITIVE_ARG.search(value):
            shown.append(value)
            redact_next = True
        elif "://" in value:
            shown.append(_safe_url_for_review(value))
        else:
            shown.append(value)
    return shown


def review_lines(repository: Path, server: str, entry: object,
                 policy: ExternalTrustPolicy | None = None) -> list[str]:
    decision = (policy or LocalExternalTrustPolicy()).evaluate(
        repository, server, entry)
    lines = [
        f"Server: {server!r}",
        f"Repository: {repository_identity(repository).root}",
        f"Entry hash: {decision.entry_hash}",
        "Required permissions: "
        + (", ".join(sorted(p.value for p in decision.required)) or "none"),
        "Granted permissions: "
        + (", ".join(sorted(p.value for p in decision.granted)) or "none"),
        f"Decision: {decision.state}",
    ]
    if isinstance(entry, dict) and "command" in entry:
        lines.append(f"Command: {entry.get('command')!r}")
        lines.append("Arguments: " + json.dumps(
            _safe_args_for_review(entry.get("args", [])), ensure_ascii=False))
        lines.append(
            "Execution boundary: this command runs with the current OS "
            "user's authority; the trust record authorizes it but does not "
            "sandbox it")
    elif isinstance(entry, dict) and "url" in entry:
        lines.append(f"URL: {_safe_url_for_review(entry.get('url'))}")
        headers = entry.get("headers") or {}
        names = sorted(str(k) for k in headers) if isinstance(headers, dict) else []
        lines.append("Header names (values never shown): "
                     + (json.dumps(names, ensure_ascii=False) if names else "none"))
    if decision.errors:
        lines.append("Configuration errors: " + "; ".join(decision.errors))
    return lines


def _load_address_book_for_cli(root: Path) -> dict:
    return load_mcp_address_book(root)


def cmd_external_trust(args) -> int:
    """Review, hash-confirm, or revoke clone-local external authority."""
    root = Path(getattr(args, "path", ".")).resolve()
    action = args.action
    server = getattr(args, "server", None)
    try:
        book = _load_address_book_for_cli(root) if action != "revoke" else None
        if action == "review":
            selected = [server] if server else sorted(book)
            missing = [name for name in selected if name not in book]
            if missing:
                raise ExternalTrustError("unknown server: " + ", ".join(missing))
            for index, name in enumerate(selected):
                if index:
                    print()
                print("\n".join(review_lines(root, name, book[name])))
            return 0
        if action == "trust":
            if not server:
                raise ExternalTrustError("trust requires a server name")
            if server not in book:
                raise ExternalTrustError(f"unknown server: {server}")
            expected_hash = getattr(args, "expected_hash", None)
            if not expected_hash:
                raise ExternalTrustError(
                    "trust requires --hash from a prior `external-trust review`")
            permissions = getattr(args, "allow", None) or []
            print("\n".join(review_lines(root, server, book[server])))
            decision = grant_external_trust(
                root, server, book[server], permissions, expected_hash)
            print("Trust recorded locally at " + str(decision.store_path))
            print("Decision: " + decision.state)
            if decision.missing:
                print("Still missing: "
                      + ", ".join(sorted(p.value for p in decision.missing)))
            return 0
        if action == "revoke":
            removed = revoke_external_trust(root, server)
            scope = f"server {server!r}" if server else "all servers"
            print(f"Revoked {removed} local trust record(s) for {scope}.")
            return 0
        raise ExternalTrustError(f"unknown action: {action}")
    except ExternalTrustError as exc:
        print(f"external-trust: {exc}")
        return 2
