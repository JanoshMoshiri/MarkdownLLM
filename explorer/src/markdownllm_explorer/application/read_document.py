from __future__ import annotations

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.models import DocumentMode, RelativePath

from .ports import SourceBrowser, SourceCatalogue


class ReadDocument:
    def __init__(self, catalogue: SourceCatalogue, browser: SourceBrowser) -> None:
        self._catalogue, self._browser = catalogue, browser

    def execute(self, source_id: str, path: str, mode: str):
        try:
            document_mode = DocumentMode(mode)
        except ValueError:
            raise ExplorerError("invalid_request") from None
        source = self._catalogue.source(source_id)
        return self._browser.document(source.boundary_token, RelativePath.parse(path), document_mode)

