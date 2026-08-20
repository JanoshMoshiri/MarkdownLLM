"""Leaf contracts shared by hook producers and hook executors.

This module deliberately imports no other ``markdownllm`` module.  Runtime and
repository transactions consume immutable expected bytes through this public
contract; neither reaches back into scaffold, the hook producer.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping


MDLLM_ENTRY = Path(__file__).resolve().parents[1] / "mdllm.py"


@dataclass(frozen=True)
class HookByteContract:
    """Exact trusted bytes for zero or more Git hook names."""

    entries: tuple[tuple[str, bytes], ...] = ()

    @classmethod
    def from_mapping(cls, hooks: Mapping[str, bytes]) -> "HookByteContract":
        return cls(tuple(sorted((str(name), bytes(body))
                                for name, body in hooks.items())))

    def expected(self, name: str) -> bytes | None:
        return next((body for hook, body in self.entries if hook == name), None)
