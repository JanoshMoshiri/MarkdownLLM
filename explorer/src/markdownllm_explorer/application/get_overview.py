from __future__ import annotations

from markdownllm_explorer.core.models import OverviewRecord

from .ports import CommitHistory, SourceCatalogue, SourceMetrics


class GetOverview:
    def __init__(self, catalogue: SourceCatalogue, browser: SourceMetrics, history: CommitHistory) -> None:
        self._catalogue, self._browser, self._history = catalogue, browser, history

    def execute(self, source_id: str, cursor: str | None = None) -> OverviewRecord:
        source = self._catalogue.source(source_id)
        repository, commits = self._history.snapshot(source.boundary_token, cursor)
        return OverviewRecord(
            source,
            self._browser.counts(source.boundary_token),
            repository,
            commits,
        )
