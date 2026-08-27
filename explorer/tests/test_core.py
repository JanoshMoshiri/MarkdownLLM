from __future__ import annotations

import base64
import json

import pytest

from markdownllm_explorer.adapters.cursors import CursorCodec, CursorState
from markdownllm_explorer.core.eligibility import EligibilityPolicy
from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.models import RelativePath


@pytest.mark.unit
@pytest.mark.parametrize("path", ["../x", "a/../x", "/absolute", "C:/x", "a\\b", "a//b", "./x", "x\x00y"])
def test_relative_path_rejects_ambiguous_or_outside_forms(path):
    with pytest.raises(ExplorerError) as caught:
        RelativePath.parse(path)
    assert caught.value.code == "invalid_path"


@pytest.mark.unit
def test_relative_path_uses_posix_identity():
    path = RelativePath.parse("things/insights/one.md")
    assert path.parent.value == "things/insights"
    assert path.depth == 3


@pytest.mark.unit
@pytest.mark.parametrize("name", [".env", ".env.local", "server.pem", "private.KEY", "access-token.md", "my_credentials.json", "vault.kdbx"])
def test_secret_names_are_ineligible(name):
    policy = EligibilityPolicy()
    assert policy.is_secret_name(name)
    assert not policy.is_eligible_file(name)


@pytest.mark.unit
@pytest.mark.parametrize("name", [".git", ".github", "node_modules", "__pycache__", ".test-tmp"])
def test_hidden_and_build_directories_are_ignored(name):
    assert EligibilityPolicy().is_ignored_directory(name)


@pytest.mark.unit
def test_only_explicit_extensions_and_names_are_eligible():
    policy = EligibilityPolicy()
    assert policy.is_eligible_file("AGENTS.md")
    assert policy.is_eligible_file("LICENSE")
    assert policy.is_eligible_file("script.py")
    assert not policy.is_eligible_file("photo.png")
    assert not policy.is_eligible_file("arbitrary")


@pytest.mark.unit
def test_cursor_is_signed_and_bound_to_operation_source_and_context():
    codec = CursorCodec(b"k" * 32)
    value = codec.encode(CursorState("tree", "substrate", "skills", 10, "revision"))
    raw = base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))
    assert json.loads(raw[:-16]) == {
        "context": "skills",
        "offset": 10,
        "operation": "tree",
        "revision": "revision",
        "source": "substrate",
    }
    assert codec.decode(value, operation="tree", source="substrate", context="skills").offset == 10
    for operation, source, context in [("search", "substrate", "skills"), ("tree", "domain/x", "skills"), ("tree", "substrate", "things")]:
        with pytest.raises(ExplorerError, match="cursor"):
            codec.decode(value, operation=operation, source=source, context=context)
    with pytest.raises(ExplorerError):
        codec.decode(value[:-2] + "xx", operation="tree", source="substrate", context="skills")
