from __future__ import annotations

import pytest

from markdownllm_explorer.adapters.document_presenter import DocumentPresenter
from markdownllm_explorer.adapters.frontmatter_parser import FrontmatterParser
from markdownllm_explorer.adapters.safe_markdown_parser import SafeMarkdownParser
from markdownllm_explorer.core.limits import ExplorerLimits
from markdownllm_explorer.core.models import FrontmatterState, LinkKind, ResolvedLink


@pytest.mark.unit
def test_frontmatter_valid_absent_and_malformed_states():
    parser = FrontmatterParser(ExplorerLimits())
    valid = parser.parse("---\nid: sample\ntags: [one, two]\n---\n# Body")
    assert valid.frontmatter.state is FrontmatterState.VALID
    assert valid.frontmatter.values["id"] == "sample"
    assert parser.parse("# Body").frontmatter.state is FrontmatterState.ABSENT
    assert parser.parse("---\nid: [\n---\n# Body").frontmatter.state is FrontmatterState.INVALID


@pytest.mark.unit
@pytest.mark.parametrize("yaml_text", ["a: &x value\nb: *x", "id: one\nid: two", "base: &x {a: b}\n<<: *x"])
def test_frontmatter_rejects_aliases_duplicate_and_merge_keys(yaml_text):
    parsed = FrontmatterParser(ExplorerLimits()).parse(f"---\n{yaml_text}\n---\n# Body")
    assert parsed.frontmatter.state is FrontmatterState.INVALID
    assert parsed.frontmatter.error_code == "frontmatter_invalid"


@pytest.mark.unit
def test_frontmatter_byte_budget_is_enforced():
    parsed = FrontmatterParser(ExplorerLimits(frontmatter_bytes=8)).parse("---\nvalue: too-long\n---\nbody")
    assert parsed.frontmatter.error_code == "frontmatter_too_large"


@pytest.mark.unit
@pytest.mark.parametrize(("limit", "value", "valid"), [(7, "123456", True), (6, "123456", True), (5, "123456", False)])
def test_frontmatter_scalar_budget_n_minus_one_n_n_plus_one(limit, value, valid):
    parsed = FrontmatterParser(ExplorerLimits(frontmatter_scalar_bytes=limit)).parse(f"---\nvalue: {value}\n---\nbody")
    assert (parsed.frontmatter.state is FrontmatterState.VALID) is valid


@pytest.mark.unit
@pytest.mark.parametrize(("items", "valid"), [(2, True), (3, True), (4, False)])
def test_frontmatter_collection_budget_n_minus_one_n_n_plus_one(items, valid):
    values = ", ".join(str(index) for index in range(items))
    parsed = FrontmatterParser(ExplorerLimits(frontmatter_collection_items=3)).parse(f"---\nvalues: [{values}]\n---\nbody")
    assert (parsed.frontmatter.state is FrontmatterState.VALID) is valid


@pytest.mark.unit
@pytest.mark.parametrize(("depth", "valid"), [(2, True), (3, True), (4, False)])
def test_frontmatter_depth_budget_n_minus_one_n_n_plus_one(depth, valid):
    nested = "value"
    for _ in range(depth - 1):
        nested = f"[{nested}]"
    parsed = FrontmatterParser(ExplorerLimits(frontmatter_depth=3)).parse(f"---\nroot: {nested}\n---\nbody")
    assert (parsed.frontmatter.state is FrontmatterState.VALID) is valid


@pytest.mark.unit
def test_frontmatter_rejects_unsupported_tags_and_non_finite_or_wide_numbers():
    parser = FrontmatterParser(ExplorerLimits())
    for value in ("!python/object value", ".inf", str(2**64)):
        parsed = parser.parse(f"---\nvalue: {value}\n---\nbody")
        assert parsed.frontmatter.state is FrontmatterState.INVALID


@pytest.mark.unit
def test_markdown_raw_html_and_unsafe_links_are_inert():
    tree = SafeMarkdownParser().parse("# Safe\n\n<script>alert(1)</script> [bad](javascript:alert(1)) [mail](mailto:test@example.invalid) [good](guide.md) [web](https://example.invalid)")
    resolved = tuple(
        ResolvedLink(link.label, LinkKind.INERT) if link.kind is LinkKind.INERT else ResolvedLink(link.label, link.kind, "#safe")
        for link in tree.links
    )
    rendered = DocumentPresenter().render(tree, resolved)
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "javascript:" not in rendered
    assert '<span class="inert-link">bad</span>' in rendered
    assert "mailto:" not in rendered and '<span class="inert-link">mail</span>' in rendered
    assert "language-" not in rendered


@pytest.mark.unit
def test_supported_markdown_structures_render_without_client_parser():
    source = "# Heading\n\n**bold** and `code`\n\n- one\n- two\n\n> quote\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n```py\nprint('x')\n```"
    tree = SafeMarkdownParser().parse(source)
    rendered = DocumentPresenter().render(tree, ())
    for tag in ("<h1>", "<strong>", "<code>", "<ul>", "<blockquote>", "<table>", "<pre>"):
        assert tag in rendered
