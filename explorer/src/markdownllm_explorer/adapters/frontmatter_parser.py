"""Bounded YAML frontmatter parsing into JSON-safe values."""

from __future__ import annotations

import json
import math
import re

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
            self._validate_event_stream(yaml_text)
            node = yaml.compose(yaml_text, Loader=yaml.SafeLoader)
            values = self._normalise(node, depth=0) if node is not None else {}
            if not isinstance(values, dict):
                raise ValueError("frontmatter must be a mapping")
            encoded = json.dumps(values, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")
            if len(encoded) > self._limits.frontmatter_json_bytes:
                raise ValueError("expanded frontmatter is too large")
            return ParsedDocument(FrontmatterResult(FrontmatterState.VALID, values), body)
        except (yaml.YAMLError, ValueError, TypeError, OverflowError):
            return ParsedDocument(FrontmatterResult(FrontmatterState.INVALID, error_code="frontmatter_invalid"), body)

    def _validate_event_stream(self, yaml_text: str) -> None:
        depth = nodes = 0
        collection_counts: list[list[int]] = []
        for event in yaml.parse(yaml_text, Loader=yaml.SafeLoader):
            if isinstance(event, yaml.events.AliasEvent):
                raise ValueError("aliases are not supported")
            if isinstance(event, (yaml.events.MappingStartEvent, yaml.events.SequenceStartEvent)):
                if collection_counts:
                    collection_counts[-1][1] += 1
                    if collection_counts[-1][1] > collection_counts[-1][0]:
                        raise ValueError("frontmatter collection limit exceeded")
                depth += 1; nodes += 1
                maximum = self._limits.frontmatter_collection_items * (2 if isinstance(event, yaml.events.MappingStartEvent) else 1)
                collection_counts.append([maximum, 0])
                if depth > self._limits.frontmatter_depth:
                    raise ValueError("frontmatter nesting limit exceeded")
                self._validate_tag(event.tag)
            elif isinstance(event, (yaml.events.MappingEndEvent, yaml.events.SequenceEndEvent)):
                depth -= 1; collection_counts.pop()
            elif isinstance(event, yaml.events.ScalarEvent):
                nodes += 1
                if len(event.value.encode("utf-8")) > self._limits.frontmatter_scalar_bytes:
                    raise ValueError("frontmatter scalar limit exceeded")
                self._validate_tag(event.tag)
                if event.tag == "tag:yaml.org,2002:timestamp":
                    raise ValueError("explicit timestamps are not supported")
                if collection_counts:
                    collection_counts[-1][1] += 1
                    if collection_counts[-1][1] > collection_counts[-1][0]:
                        raise ValueError("frontmatter collection limit exceeded")
            if nodes > self._limits.frontmatter_nodes:
                raise ValueError("frontmatter node limit exceeded")

    @staticmethod
    def _validate_tag(tag: str | None) -> None:
        allowed = {
            None, "!", "tag:yaml.org,2002:map", "tag:yaml.org,2002:seq", "tag:yaml.org,2002:str",
            "tag:yaml.org,2002:null", "tag:yaml.org,2002:bool", "tag:yaml.org,2002:int",
            "tag:yaml.org,2002:float", "tag:yaml.org,2002:timestamp",
        }
        if tag not in allowed:
            raise ValueError("unsupported YAML tag")

    def _normalise(self, node: yaml.Node, depth: int) -> object:
        if depth > self._limits.frontmatter_depth:
            raise ValueError("frontmatter nesting limit exceeded")
        if isinstance(node, yaml.MappingNode):
            if len(node.value) > self._limits.frontmatter_collection_items:
                raise ValueError("frontmatter mapping limit exceeded")
            result: dict[str, object] = {}
            for key_node, value_node in node.value:
                if not isinstance(key_node, yaml.ScalarNode) or key_node.tag != "tag:yaml.org,2002:str":
                    raise ValueError("frontmatter keys must be strings")
                key = key_node.value
                if key == "<<" or key in result:
                    raise ValueError("duplicate or merge key")
                result[key] = self._normalise(value_node, depth + 1)
            return result
        if isinstance(node, yaml.SequenceNode):
            if len(node.value) > self._limits.frontmatter_collection_items:
                raise ValueError("frontmatter sequence limit exceeded")
            return [self._normalise(child, depth + 1) for child in node.value]
        if not isinstance(node, yaml.ScalarNode):
            raise ValueError("unsupported YAML node")
        tag, value = node.tag, node.value
        if tag in {"tag:yaml.org,2002:str", "tag:yaml.org,2002:timestamp"}:
            return value
        if tag == "tag:yaml.org,2002:null":
            return None
        if tag == "tag:yaml.org,2002:bool":
            return value.casefold() in {"true", "yes", "on"}
        if tag == "tag:yaml.org,2002:int":
            parsed = yaml.safe_load(value)
            if not isinstance(parsed, int) or isinstance(parsed, bool):
                raise ValueError("invalid integer")
            if not -(2**63) <= parsed < 2**63:
                raise ValueError("integer is outside supported range")
            return parsed
        if tag == "tag:yaml.org,2002:float":
            parsed = yaml.safe_load(value)
            if not isinstance(parsed, float):
                raise ValueError("invalid float")
            if not math.isfinite(parsed):
                raise ValueError("non-finite float")
            return parsed
        raise ValueError("unsupported YAML scalar")
