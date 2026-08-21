"""One strict YAML boundary for every operative MarkdownLLM definition.

PyYAML's safe loader silently keeps the last value when a mapping repeats a
key.  That behaviour is convenient for loose configuration, but unsafe for a
definition-driven substrate: two ``status`` or ``autopush`` declarations must
be an error, not an invisible choice.  This module is the only place the tool
constructs YAML.

The loader deliberately retains PyYAML's YAML-1.1 scalar rules.  In
particular, a bare ``on`` key is still constructed as ``True`` and the
frontmatter model normalises it at the trigger boundary.  Changing that rule
would be a corpus migration rather than a parser tidy-up.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class LexicalFloat(float):
    """A normal float that also retains the exact YAML source lexeme.

    Existing model consumers, JSON encoders, comparisons, and schema logic
    continue to see a float.  Deterministic calculation can recover the exact
    decimal spelling instead of converting an already-rounded binary value
    back through ``str(float)``.
    """

    def __new__(cls, value: float, lexeme: str):
        obj = float.__new__(cls, value)
        obj.yaml_lexeme = lexeme
        return obj


# The C parser (libyaml) is ~10x faster than the pure-Python scanner and
# produces the same node/mark interface the strict checks below read. The
# duplicate-key rejection and float-lexeme retention both live on the Python
# constructor side, which is identical for either base — so strictness is
# unchanged; only the tokenising is. Falls back cleanly where libyaml is not
# compiled in.
_LOADER_BASE = (yaml.CSafeLoader
                if getattr(yaml, "__with_libyaml__", False)
                else yaml.SafeLoader)


class StrictSafeLoader(_LOADER_BASE):
    """SafeLoader variant that rejects duplicate mapping keys."""

    source_name = "<yaml>"

    def construct_mapping(self, node, deep: bool = False):  # noqa: ANN001
        if not isinstance(node, yaml.MappingNode):
            raise yaml.constructor.ConstructorError(
                None, None, "expected a mapping node", node.start_mark)
        seen: dict[Any, yaml.Node] = {}
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=False)
            try:
                duplicate = key in seen
            except TypeError as exc:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"found unhashable mapping key {key!r}", key_node.start_mark,
                ) from exc
            if duplicate:
                first = seen[key].start_mark
                where = self.source_name
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping", node.start_mark,
                    f"duplicate key {key!r} in {where}; first declared at "
                    f"line {first.line + 1}, column {first.column + 1}",
                    key_node.start_mark,
                )
            seen[key] = key_node
        return super().construct_mapping(node, deep=deep)


def _construct_float(loader: StrictSafeLoader, node: yaml.ScalarNode) -> LexicalFloat:
    # Delegate YAML spellings (.inf, exponent, underscores, sexagesimal) to
    # PyYAML, then retain the original token for exact-decimal consumers.
    # SafeConstructor is the shared constructor base of both loader bases.
    value = yaml.constructor.SafeConstructor.construct_yaml_float(loader, node)
    return LexicalFloat(value, node.value)


StrictSafeLoader.add_constructor(
    "tag:yaml.org,2002:float", _construct_float)

# SafeDumper dispatches by exact type.  Generated YAML does not need to retain
# the source spelling, but it must continue to accept metadata containing our
# float subclass.
yaml.SafeDumper.add_representer(
    LexicalFloat, yaml.representer.SafeRepresenter.represent_float)


def load_yaml(text: str | bytes, *, source: str | Path = "<yaml>") -> Any:
    """Parse one YAML document safely and reject duplicate keys.

    ``source`` is diagnostic provenance only; callers may pass a logical
    repository path even when bytes came from an index or commit view.
    ``yaml.YAMLError`` remains the public exception family so existing command
    boundaries continue to turn parse failures into findings.
    """

    if isinstance(text, bytes):
        text = text.decode("utf-8")
    loader = StrictSafeLoader(text)
    loader.source_name = str(source)
    try:
        return loader.get_single_data()
    finally:
        loader.dispose()


def load_yaml_mapping(
    text: str | bytes, *, source: str | Path = "<yaml>"
) -> dict[Any, Any]:
    """Parse a definition whose document root must be a mapping.

    Sentinels, schemas, fixtures, and configuration files are mapping-shaped
    contracts.  Letting a sequence or scalar reach a caller that immediately
    invokes ``.get`` turns a definition finding into an ``AttributeError``
    traceback.  Raise through the same ``yaml.YAMLError`` family instead so
    every CLI boundary can report it consistently.
    """

    data = load_yaml(text, source=source)
    if not isinstance(data, dict):
        kind = "empty document" if data is None else type(data).__name__
        raise yaml.YAMLError(
            f"{source}: expected a YAML mapping, got {kind}")
    return data


def load_version_sentinel(
    text: str | bytes, *, source: str | Path = ".markdownllm"
) -> dict[Any, Any]:
    """Parse a framework sentinel and require its operative version key.

    A syntactically valid ``{}``, sequence, or ``version: null`` is not a
    usable version sentinel.  Every command that keys framework currency from
    this file should reject the same shapes instead of rendering ``vNone`` or
    silently treating an empty catalog as current.
    """

    data = load_yaml_mapping(text, source=source)
    version = data.get("version")
    if (isinstance(version, bool)
            or not isinstance(version, (str, int, float))
            or not str(version).strip()):
        raise yaml.YAMLError(
            f"{source}: version sentinel requires a non-empty scalar `version`")
    return data
