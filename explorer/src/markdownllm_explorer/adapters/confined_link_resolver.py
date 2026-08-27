"""Resolve Markdown link candidates without granting new filesystem authority."""

from __future__ import annotations

from urllib.parse import quote

from markdownllm_explorer.core.models import BoundaryToken, LinkCandidate, LinkKind, RelativePath, ResolvedLink

from .confined_source_reader import ConfinedSourceReader
from .filesystem_catalogue import BoundaryRegistry


class ConfinedLinkResolver:
    def __init__(self, filesystem: ConfinedSourceReader, registry: BoundaryRegistry) -> None:
        self._filesystem = filesystem
        self._registry = registry

    def resolve(self, token: BoundaryToken, document: RelativePath, links: tuple[LinkCandidate, ...]) -> tuple[ResolvedLink, ...]:
        source = self._registry.by_token(token).source
        resolved: list[ResolvedLink] = []
        for link in links:
            if link.kind is LinkKind.EXTERNAL:
                resolved.append(ResolvedLink(link.label, link.kind, link.raw_target))
            elif link.kind is LinkKind.RELATIVE:
                target = self._filesystem.resolve_markdown_target(token, document, link.raw_target)
                href = f"#source={quote(source.id.value, safe='')}&path={target.quoted()}" if target else None
                resolved.append(ResolvedLink(link.label, LinkKind.RELATIVE if href else LinkKind.INERT, href))
            else:
                resolved.append(ResolvedLink(link.label, LinkKind.INERT))
        return tuple(resolved)

