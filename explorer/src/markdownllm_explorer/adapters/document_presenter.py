"""Escaping presenter for parsed Markdown trees."""

from __future__ import annotations

import html

from markdownllm_explorer.core.models import InlineNode, LinkKind, MarkdownTree, ResolvedLink


class DocumentPresenter:
    def render(self, tree: MarkdownTree, resolved: tuple[ResolvedLink, ...]) -> str:
        output: list[str] = []
        for block in tree.blocks:
            if block.kind == "heading":
                output.append(f"<h{block.level}>{self._inline(block.inlines, resolved)}</h{block.level}>")
            elif block.kind == "paragraph":
                output.append(f"<p>{self._inline(block.inlines, resolved)}</p>")
            elif block.kind == "quote":
                output.append(f"<blockquote>{self._inline(block.inlines, resolved)}</blockquote>")
            elif block.kind == "rule":
                output.append("<hr>")
            elif block.kind == "code":
                output.append(f"<pre><code>{html.escape(block.text)}</code></pre>")
            elif block.kind in {"list", "ordered_list"}:
                tag = "ol" if block.kind == "ordered_list" else "ul"
                items = "".join(f"<li>{self._inline(item, resolved)}</li>" for item in block.items)
                output.append(f"<{tag}>{items}</{tag}>")
            elif block.kind == "table" and block.rows:
                rows: list[str] = []
                for row_index, row in enumerate(block.rows):
                    cell_tag = "th" if row_index == 0 else "td"
                    rows.append("<tr>" + "".join(f"<{cell_tag}>{self._inline(cell, resolved)}</{cell_tag}>" for cell in row) + "</tr>")
                output.append("<table><thead>" + rows[0] + "</thead><tbody>" + "".join(rows[1:]) + "</tbody></table>")
        return "\n".join(output)

    def _inline(self, nodes: tuple[InlineNode, ...], links: tuple[ResolvedLink, ...]) -> str:
        parts: list[str] = []
        for node in nodes:
            text = html.escape(node.text)
            if node.kind == "code":
                parts.append(f"<code>{text}</code>")
            elif node.kind == "strong":
                parts.append(f"<strong>{text}</strong>")
            elif node.kind == "emphasis":
                parts.append(f"<em>{text}</em>")
            elif node.kind == "link" and node.link_index is not None:
                link = links[node.link_index]
                if link.href and link.kind is not LinkKind.INERT:
                    external = ' target="_blank" rel="noopener noreferrer external"' if link.kind.value == "external" else ""
                    parts.append(f'<a href="{html.escape(link.href, quote=True)}"{external}>{text}</a>')
                else:
                    # Inert candidates are plain escaped text.  No repository-
                    # supplied class or tag falls outside the presenter allowlist.
                    parts.append(text)
            else:
                parts.append(text)
        return "".join(parts)
