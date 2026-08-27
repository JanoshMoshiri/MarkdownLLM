"""Small, dependency-free Markdown parser for Explorer's supported subset."""

from __future__ import annotations

import re

from markdownllm_explorer.core.models import InlineNode, LinkCandidate, LinkKind, MarkdownBlock, MarkdownTree


_LINK = re.compile(r"\[([^\]]+)]\(([^)]+)\)")
_INLINE = re.compile(r"(`[^`]+`|\*\*[^*]+\*\*|__[^_]+__|\*[^*]+\*|_[^_]+_|\[[^\]]+]\([^)]+\))")


class SafeMarkdownParser:
    def parse(self, text: str) -> MarkdownTree:
        lines = text.splitlines()
        blocks: list[MarkdownBlock] = []
        links: list[LinkCandidate] = []
        index = 0
        while index < len(lines):
            line = lines[index]
            if not line.strip():
                index += 1
                continue
            if line.startswith("```"):
                language = line[3:].strip()
                code: list[str] = []
                index += 1
                while index < len(lines) and not lines[index].startswith("```"):
                    code.append(lines[index])
                    index += 1
                index += index < len(lines)
                blocks.append(MarkdownBlock("code", text="\n".join(code), level=0, items=((InlineNode("text", language),),)))
                continue
            heading = re.match(r"^(#{1,6})\s+(.+)$", line)
            if heading:
                blocks.append(MarkdownBlock("heading", self._inlines(heading.group(2), links), level=len(heading.group(1))))
                index += 1
                continue
            if re.match(r"^\s*([-*_])(?:\s*\1){2,}\s*$", line):
                blocks.append(MarkdownBlock("rule"))
                index += 1
                continue
            if line.startswith(">"):
                quote_lines: list[str] = []
                while index < len(lines) and lines[index].startswith(">"):
                    quote_lines.append(lines[index].lstrip("> "))
                    index += 1
                blocks.append(MarkdownBlock("quote", self._inlines(" ".join(quote_lines), links)))
                continue
            if re.match(r"^\s*(?:[-+*]|\d+\.)\s+", line):
                ordered = bool(re.match(r"^\s*\d+\.", line))
                items: list[tuple[InlineNode, ...]] = []
                pattern = r"^\s*(?:\d+\.|[-+*])\s+(.+)$"
                while index < len(lines):
                    match = re.match(pattern, lines[index])
                    if not match:
                        break
                    items.append(self._inlines(match.group(1), links))
                    index += 1
                blocks.append(MarkdownBlock("ordered_list" if ordered else "list", items=tuple(items)))
                continue
            if index + 1 < len(lines) and "|" in line and re.match(r"^\s*\|?\s*:?-+", lines[index + 1]):
                rows: list[tuple[tuple[InlineNode, ...], ...]] = []
                for row_line in (line, *lines[index + 2:]):
                    if "|" not in row_line or not row_line.strip():
                        break
                    cells = [part.strip() for part in row_line.strip().strip("|").split("|")]
                    rows.append(tuple(self._inlines(cell, links) for cell in cells))
                index += len(rows) + 1
                blocks.append(MarkdownBlock("table", rows=tuple(rows)))
                continue
            paragraph = [line]
            index += 1
            while index < len(lines) and lines[index].strip() and not self._starts_block(lines, index):
                paragraph.append(lines[index])
                index += 1
            blocks.append(MarkdownBlock("paragraph", self._inlines(" ".join(paragraph), links)))
        return MarkdownTree(tuple(blocks), tuple(links))

    def _starts_block(self, lines: list[str], index: int) -> bool:
        line = lines[index]
        return bool(
            line.startswith(("#", ">", "```"))
            or re.match(r"^\s*(?:[-+*]|\d+\.)\s+", line)
            or (index + 1 < len(lines) and "|" in line and re.match(r"^\s*\|?\s*:?-+", lines[index + 1]))
        )

    def _inlines(self, text: str, links: list[LinkCandidate]) -> tuple[InlineNode, ...]:
        nodes: list[InlineNode] = []
        cursor = 0
        for match in _INLINE.finditer(text):
            if match.start() > cursor:
                nodes.append(InlineNode("text", text[cursor:match.start()]))
            token = match.group(0)
            link = _LINK.fullmatch(token)
            if link:
                target = link.group(2).strip()
                folded = target.casefold()
                if folded.startswith(("http://", "https://", "mailto:")):
                    kind = LinkKind.EXTERNAL
                elif ":" in target.split("/", 1)[0] or target.startswith(("/", "//", "#")):
                    kind = LinkKind.INERT
                else:
                    kind = LinkKind.RELATIVE
                link_index = len(links)
                links.append(LinkCandidate(link.group(1), target, kind))
                nodes.append(InlineNode("link", link.group(1), link_index=link_index))
            elif token.startswith("`"):
                nodes.append(InlineNode("code", token[1:-1]))
            elif token.startswith(("**", "__")):
                nodes.append(InlineNode("strong", token[2:-2]))
            else:
                nodes.append(InlineNode("emphasis", token[1:-1]))
            cursor = match.end()
        if cursor < len(text):
            nodes.append(InlineNode("text", text[cursor:]))
        return tuple(nodes)

