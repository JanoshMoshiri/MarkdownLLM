from __future__ import annotations

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.models import ReferenceResolution

from .ports import ReferenceIndex, SourceCatalogue

MAX_IDENTIFIERS = 200
MAX_IDENTIFIER_LENGTH = 200


class ResolveReferences:
    """Turn the identifiers a document's frontmatter names into paths.

    One request answers a whole document's references. Resolving per chip would
    multiply a whole-source question by the number of links on the page, and
    resolving lazily on click would leave a reference that cannot be resolved
    looking exactly like one that can.
    """

    def __init__(self, catalogue: SourceCatalogue, index: ReferenceIndex) -> None:
        self._catalogue, self._index = catalogue, index

    def execute(self, source_id: str, ids: str) -> ReferenceResolution:
        source = self._catalogue.source(source_id)
        requested = _requested(ids)
        resolved, unresolved, partial = self._index.resolve(source.boundary_token, requested)
        return ReferenceResolution(source.id, resolved, unresolved, partial)


def _requested(ids: str) -> tuple[str, ...]:
    seen: list[str] = []
    for candidate in ids.split(","):
        identifier = candidate.strip()
        if not identifier or identifier in seen:
            continue
        if len(identifier) > MAX_IDENTIFIER_LENGTH:
            raise ExplorerError("invalid_request")
        seen.append(identifier)
        if len(seen) > MAX_IDENTIFIERS:
            raise ExplorerError("invalid_request")
    if not seen:
        raise ExplorerError("invalid_request")
    return tuple(seen)
