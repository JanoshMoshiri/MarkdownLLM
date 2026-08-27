from __future__ import annotations

from markdownllm_explorer.core.models import RelativePath

from .ports import SourceCatalogue, TreeReader


class BrowseTree:
    def __init__(self, catalogue: SourceCatalogue, browser: TreeReader) -> None:
        self._catalogue, self._browser = catalogue, browser

    def execute(self, source_id: str, path: str | None, cursor: str | None = None):
        source = self._catalogue.source(source_id)
        return self._browser.tree(source.boundary_token, RelativePath.parse(path), cursor)
