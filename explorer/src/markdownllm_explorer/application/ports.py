"""Focused ports owned by Explorer use cases."""

from __future__ import annotations

from typing import Protocol

from markdownllm_explorer.core.models import (
    BoundaryToken, CollectionItem, CommitDetail, CommitRecord, EstateSnapshot, FrontmatterResult,
    HistoricalDocument, LinkCandidate,
    MarkdownTree, Page, ParsedDocument, RawDocument, RelativePath, RepositoryState, ResolvedLink,
    Source, SourceCounts, SourceSettingsRecord, TreeNode,
)


class SourceCatalogue(Protocol):
    def discover(self) -> EstateSnapshot: ...
    def source(self, source_id: str) -> Source: ...


class SourceMetrics(Protocol):
    def counts(self, token: BoundaryToken) -> SourceCounts: ...


class TreeReader(Protocol):
    def tree(self, token: BoundaryToken, path: RelativePath, cursor: str | None) -> Page[TreeNode]: ...


class PathSearcher(Protocol):
    def search(self, token: BoundaryToken, query: str, cursor: str | None) -> Page[TreeNode]: ...


class CollectionReader(Protocol):
    def collection(self, token: BoundaryToken, kind: str, cursor: str | None) -> Page[CollectionItem]: ...


class DocumentReader(Protocol):
    def read(self, token: BoundaryToken, path: RelativePath) -> RawDocument: ...


class SettingsReader(Protocol):
    def settings(self, token: BoundaryToken) -> SourceSettingsRecord: ...


class FrontmatterParserPort(Protocol):
    def parse(self, text: str) -> ParsedDocument: ...


class MarkdownParserPort(Protocol):
    def parse(self, text: str) -> MarkdownTree: ...


class LinkResolver(Protocol):
    def resolve(self, token: BoundaryToken, document: RelativePath, links: tuple[LinkCandidate, ...]) -> tuple[ResolvedLink, ...]: ...


class MarkdownPresenter(Protocol):
    def render(self, tree: MarkdownTree, resolved: tuple[ResolvedLink, ...]) -> str: ...


class CommitHistory(Protocol):
    def snapshot(self, token: BoundaryToken, cursor: str | None) -> tuple[RepositoryState, Page[CommitRecord]]: ...


class CommitDetails(Protocol):
    def detail(self, token: BoundaryToken, sha: str) -> CommitDetail: ...
    def historical(self, token: BoundaryToken, sha: str, path: RelativePath) -> HistoricalDocument: ...


class PathAdmission(Protocol):
    """Whether a source would admit a path, decided without touching disk.

    The historical read needs this exact question about files that no longer
    exist in the working tree, so admission cannot be inferred from a
    successful filesystem read.  One implementation answers it for both.
    """

    def admits(self, token: BoundaryToken, path: RelativePath) -> bool: ...
