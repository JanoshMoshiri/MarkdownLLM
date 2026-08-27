from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from markdownllm_explorer.core.models import OverviewRecord

from .ports import CommitHistory, SourceCatalogue, SourceMetrics


class GetOverview:
    def __init__(self, catalogue: SourceCatalogue, browser: SourceMetrics, history: CommitHistory) -> None:
        self._catalogue, self._browser, self._history = catalogue, browser, history

    def execute(self, source_id: str, cursor: str | None = None) -> OverviewRecord:
        source = self._catalogue.source(source_id)
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="explorer-overview") as executor:
            counts_future = executor.submit(self._browser.counts, source.boundary_token)
            history_future = executor.submit(
                self._history.snapshot, source.boundary_token, cursor
            )
            repository, commits = history_future.result()
            counts = counts_future.result()
        return OverviewRecord(
            source,
            counts,
            repository,
            commits,
        )
