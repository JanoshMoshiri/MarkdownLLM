"""Bounded YAML frontmatter parsing into JSON-safe values."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping

import yaml

from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import FrontmatterResult, FrontmatterState, ParsedDocument


class FrontmatterParser:
    def __init__(self, limits: ExplorerLimits) -> None:
        self._limits = limits

    def parse(self, text: str) -> ParsedDocument:
        opening = re.match(r"^---\r?\n", text)
        if not opening:
            return ParsedDocument(FrontmatterResult(FrontmatterState.ABSENT), text)
        closing = re.search(r"\r?\n---(?:\r?\n|$)", text[opening.end():])
        if not closing:
            return ParsedDocument(FrontmatterResult(FrontmatterState.INVALID, error_code="frontmatter_invalid"), text)
        yaml_start = opening.end()
        yaml_end = yaml_start + closing.start()
        body_start = yaml_start + closing.end()
        yaml_text = text[yaml_start:yaml_end]
        body = text[body_start:]
        if len(yaml_text.encode("utf-8")) > self._limits.frontmatter_bytes:
            return ParsedDocument(FrontmatterResult(FrontmatterState.INVALID, error_code="frontmatter_too_large"), body)
        try:
            events = list(yaml.parse(yaml_text, Loader=yaml.BaseLoader))
            if any(isinstance(event, yaml.events.AliasEvent) for event in events):
                raise ValueError("aliases are not supported")
            node = yaml.compose(yaml_text, Loader=yaml.BaseLoader)
            self._reject_duplicate_keys(node)
            values = yaml.load(yaml_text, Loader=yaml.BaseLoader) or {}
            if not isinstance(values, Mapping):
                raise ValueError("frontmatter must be a mapping")
            encoded = json.dumps(values, ensure_ascii=False).encode("utf-8")
            if len(encoded) > self._limits.frontmatter_json_bytes:
                raise ValueError("expanded frontmatter is too large")
            return ParsedDocument(FrontmatterResult(FrontmatterState.VALID, dict(values)), body)
        except (yaml.YAMLError, ValueError, TypeError):
            return ParsedDocument(FrontmatterResult(FrontmatterState.INVALID, error_code="frontmatter_invalid"), body)

    def _reject_duplicate_keys(self, node: yaml.Node | None) -> None:
        if isinstance(node, yaml.MappingNode):
            seen: set[str] = set()
            for key, value in node.value:
                key_text = str(getattr(key, "value", ""))
                if key_text in seen or key_text == "<<":
                    raise ValueError("duplicate or merge key")
                seen.add(key_text)
                self._reject_duplicate_keys(value)
        elif isinstance(node, yaml.SequenceNode):
            for child in node.value:
                self._reject_duplicate_keys(child)
