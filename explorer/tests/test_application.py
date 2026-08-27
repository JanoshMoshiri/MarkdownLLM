from __future__ import annotations

import pytest

from markdownllm_explorer.application.browse_tree import BrowseTree
from markdownllm_explorer.application.get_overview import GetOverview
from markdownllm_explorer.application.get_settings import GetSettings
from markdownllm_explorer.application.list_collection import ListCollection
from markdownllm_explorer.application.read_document import ReadDocument
from markdownllm_explorer.application.search_paths import SearchPaths
from markdownllm_explorer.core.models import (
    BoundaryToken, CollectionItem, CommitRecord, DocumentMode, EntryKind, FrontmatterResult,
    FrontmatterState, GitKind, MarkdownTree, Page, ParsedDocument, RawDocument, RelativePath,
    RepositoryState, Source, SourceCounts, SourceId, SourceKind, SourceSettingsRecord, TreeNode,
)


SOURCE = Source(SourceId("substrate"), SourceKind.SUBSTRATE, "Substrate", BoundaryToken("opaque"), ("AGENTS.md",), GitKind.REPOSITORY)
PAGE = Page((), None, False, "2026-08-27T00:00:00+00:00")


class CatalogueFake:
    def source(self, source_id):
        assert source_id == "substrate"; return SOURCE


class FocusedPortsFake:
    def __init__(self): self.calls = []
    def counts(self, token): self.calls.append(("counts", token)); return SourceCounts(1, 1, 0, False)
    def snapshot(self, token, cursor): self.calls.append(("snapshot", token, cursor)); return RepositoryState("repository"), Page((CommitRecord("a" * 40, "subject", "author", "date"),), None, False, "now")
    def tree(self, token, path, cursor): self.calls.append(("tree", token, path, cursor)); return Page((TreeNode(RelativePath("AGENTS.md"), "AGENTS.md", EntryKind.FILE),), None, False, "now")
    def search(self, token, query, cursor): self.calls.append(("search", token, query, cursor)); return PAGE
    def collection(self, token, kind, cursor): self.calls.append(("collection", token, kind, cursor)); return Page((CollectionItem(RelativePath("skills/a.md"), "A", "skills"),), None, False, "now")
    def settings(self, token): self.calls.append(("settings", token)); return SourceSettingsRecord(SOURCE.id, "authorised", SOURCE.markers, SOURCE.kind, SOURCE.git_kind)
    def read(self, token, path): self.calls.append(("read", token, path)); return RawDocument(SOURCE.id, path, "# Body", 6, "now")
    def parse(self, text): self.calls.append(("frontmatter", text)); return ParsedDocument(FrontmatterResult(FrontmatterState.ABSENT), text)
    def resolve(self, token, document, links): self.calls.append(("resolve", token, document, links)); return ()
    def render(self, tree, resolved): self.calls.append(("render", tree, resolved)); return "<h1>Body</h1>"


class MarkdownFake:
    def parse(self, text): assert text == "# Body"; return MarkdownTree((), ())


@pytest.mark.unit
def test_use_cases_run_against_focused_fakes_without_filesystem_git_http_or_browser():
    catalogue = CatalogueFake(); ports = FocusedPortsFake()
    overview = GetOverview(catalogue, ports, ports).execute("substrate", "cursor")
    tree = BrowseTree(catalogue, ports).execute("substrate", None, "tree-cursor")
    search = SearchPaths(catalogue, ports).execute("substrate", "agent", None)
    collection = ListCollection(catalogue, ports).execute("substrate", "skills", None)
    settings = GetSettings(catalogue, ports).execute("substrate")
    document = ReadDocument(catalogue, ports, ports, MarkdownFake(), ports, ports).execute("substrate", "AGENTS.md", "rendered")
    assert overview.commits.items[0].subject == "subject"
    assert tree.items[0].path.value == "AGENTS.md" and not search.items
    assert collection.items[0].title == "A" and settings.source_path == "authorised"
    assert document.mode is DocumentMode.RENDERED and document.content == "<h1>Body</h1>"
    assert {call[0] for call in ports.calls} >= {"counts", "snapshot", "tree", "search", "collection", "settings", "read", "frontmatter", "resolve", "render"}
