"""Single composition root for the Explorer executable."""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from pathlib import Path

from .adapters.confined_source_reader import ConfinedSourceReader
from .adapters.collection_reader import CuratedCollectionReader
from .adapters.confined_link_resolver import ConfinedLinkResolver
from .adapters.cursors import CursorCodec
from .adapters.document_presenter import DocumentPresenter
from .adapters.filesystem_catalogue import BoundaryRegistry, FilesystemSourceCatalogue
from .adapters.frontmatter_parser import FrontmatterParser
from .adapters.git_commit_history import GitCommitHistory, resolve_trusted_git
from .adapters.safe_markdown_parser import SafeMarkdownParser
from .application.browse_tree import BrowseTree
from .application.discover_estate import DiscoverEstate
from .application.get_commit import GetCommit
from .application.get_overview import GetOverview
from .application.get_settings import GetSettings
from .application.list_collection import ListCollection
from .application.read_document import ReadDocument
from .application.read_historical_document import ReadHistoricalDocument
from .application.search_paths import SearchPaths
from .core.eligibility import EligibilityPolicy
from .core.limits import ExplorerLimits
from .delivery.api_routes import ApiRoutes, ExplorerUseCases
from .delivery.http_server import serve as serve_http


@dataclass(frozen=True)
class ExplorerRuntime:
    routes: ApiRoutes
    capability: str
    limits: ExplorerLimits


def build_runtime(root: Path, domain_dir: str = "domain", *, limits: ExplorerLimits | None = None) -> ExplorerRuntime:
    active_limits = limits or ExplorerLimits()
    policy = EligibilityPolicy()
    registry = BoundaryRegistry()
    catalogue = FilesystemSourceCatalogue(root, domain_dir, registry, policy, active_limits)
    cursors = CursorCodec(secrets.token_bytes(32))
    frontmatter = FrontmatterParser(active_limits)
    markdown = SafeMarkdownParser()
    presenter = DocumentPresenter()
    source_browser = ConfinedSourceReader(registry, policy, active_limits, cursors)
    collections = CuratedCollectionReader(source_browser, registry, frontmatter, cursors, active_limits)
    link_resolver = ConfinedLinkResolver(source_browser, registry)
    history = GitCommitHistory(registry, cursors, active_limits, resolve_trusted_git(root))
    catalogue.discover()
    use_cases = ExplorerUseCases(
        DiscoverEstate(catalogue), GetOverview(catalogue, source_browser, history),
        BrowseTree(catalogue, source_browser), SearchPaths(catalogue, source_browser),
        ListCollection(catalogue, collections), GetSettings(catalogue, source_browser),
        ReadDocument(catalogue, source_browser, frontmatter, markdown, link_resolver, presenter),
        GetCommit(catalogue, history, source_browser),
        ReadHistoricalDocument(catalogue, history, source_browser),
    )
    return ExplorerRuntime(ApiRoutes(use_cases), secrets.token_urlsafe(32), active_limits)


def build_server(runtime: ExplorerRuntime, port: int = 0):
    """Compose the replaceable HTTP delivery adapter at the outer boundary."""

    return serve_http(runtime, port)
