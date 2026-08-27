from __future__ import annotations

from markdownllm_explorer.core.errors import ExplorerError
from markdownllm_explorer.core.models import DocumentMode, DocumentRecord, FrontmatterResult, FrontmatterState, RelativePath

from .ports import DocumentReader, FrontmatterParserPort, LinkResolver, MarkdownParserPort, MarkdownPresenter, SourceCatalogue


class ReadDocument:
    def __init__(
        self, catalogue: SourceCatalogue, reader: DocumentReader, frontmatter: FrontmatterParserPort,
        markdown: MarkdownParserPort, links: LinkResolver, presenter: MarkdownPresenter,
    ) -> None:
        self._catalogue, self._reader, self._frontmatter = catalogue, reader, frontmatter
        self._markdown, self._links, self._presenter = markdown, links, presenter

    def execute(self, source_id: str, path: str, mode: str):
        try:
            document_mode = DocumentMode(mode)
        except ValueError:
            raise ExplorerError("invalid_request") from None
        source = self._catalogue.source(source_id)
        relative = RelativePath.parse(path)
        raw = self._reader.read(source.boundary_token, relative)
        is_markdown = relative.name.casefold().endswith((".md", ".markdown"))
        parsed = self._frontmatter.parse(raw.text) if is_markdown else None
        frontmatter = parsed.frontmatter if parsed else FrontmatterResult(FrontmatterState.ABSENT)
        actual_mode = document_mode if is_markdown else DocumentMode.RAW
        if actual_mode is DocumentMode.RAW:
            content = raw.text
        else:
            tree = self._markdown.parse(parsed.body if parsed else raw.text)
            resolved = self._links.resolve(source.boundary_token, relative, tree.links)
            content = self._presenter.render(tree, resolved)
        issues = (frontmatter.error_code,) if frontmatter.error_code else ()
        return DocumentRecord(source.id, relative, actual_mode, content, frontmatter, raw.size, raw.modified_at, tuple(issue for issue in issues if issue))
