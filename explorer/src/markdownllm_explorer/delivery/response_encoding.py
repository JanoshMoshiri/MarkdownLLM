"""Explicit public DTO encoding; adapter tokens never cross this boundary."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Mapping

from markdownllm_explorer.core.models import BoundaryToken, RelativePath, Source, SourceId


def to_wire(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (SourceId, RelativePath)):
        return value.value
    if isinstance(value, BoundaryToken):
        raise TypeError("boundary tokens are not public DTOs")
    if isinstance(value, Source):
        return {
            "id": value.id.value,
            "kind": value.kind.value,
            "display_name": value.display_name,
            "markers": list(value.markers),
            "git_kind": value.git_kind.value,
        }
    if isinstance(value, Mapping):
        return {str(key): to_wire(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [to_wire(item) for item in value]
    if is_dataclass(value):
        return {field.name: to_wire(getattr(value, field.name)) for field in fields(value) if field.name != "boundary_token"}
    raise TypeError(f"unsupported response value {type(value).__name__}")

