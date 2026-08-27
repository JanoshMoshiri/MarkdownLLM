"""Opaque, operation-specific cursor encoding."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass

from markdownllm_explorer.core.errors import ExplorerError


@dataclass(frozen=True)
class CursorState:
    operation: str
    source: str
    context: str
    offset: int
    revision: str


class CursorCodec:
    def __init__(self, secret: bytes) -> None:
        self._secret = secret

    def encode(self, state: CursorState) -> str:
        payload = json.dumps(state.__dict__, separators=(",", ":"), sort_keys=True).encode()
        signature = hmac.new(self._secret, payload, hashlib.sha256).digest()[:16]
        return base64.urlsafe_b64encode(payload + signature).decode().rstrip("=")

    def decode(self, value: str | None, *, operation: str, source: str, context: str) -> CursorState:
        if not value:
            return CursorState(operation, source, context, 0, "")
        try:
            raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
            payload, signature = raw[:-16], raw[-16:]
            expected = hmac.new(self._secret, payload, hashlib.sha256).digest()[:16]
            if not hmac.compare_digest(signature, expected):
                raise ValueError
            data = json.loads(payload)
            state = CursorState(**data)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            raise ExplorerError("invalid_cursor") from None
        if state.operation != operation or state.source != source or state.context != context or state.offset < 0:
            raise ExplorerError("invalid_cursor")
        return state

