"""Normative Explorer limits."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ExplorerLimits:
    file_bytes: int = 1024 * 1024
    frontmatter_bytes: int = 128 * 1024
    frontmatter_json_bytes: int = 256 * 1024
    frontmatter_depth: int = 20
    frontmatter_scalar_bytes: int = 64 * 1024
    frontmatter_collection_items: int = 2_000
    frontmatter_nodes: int = 10_000
    directory_depth: int = 32
    directory_page: int = 500
    search_page: int = 200
    candidate_scan: int = 10_000
    memory_candidates: int = 10_000
    commit_page: int = 50
    commit_files: int = 500
    git_seconds: float = 3.0
    git_output_bytes: int = 1024 * 1024
    # A patch carries both sides of every change, so it is roughly twice the
    # file it describes. It is parsed for hunk headers and discarded, never
    # served, so budgeting it as if it were a response body refused files well
    # inside the read limit.
    diff_output_bytes: int = 8 * 1024 * 1024
    response_bytes: int = 2 * 1024 * 1024
    concurrent_requests: int = 16
    browser_seconds: float = 10.0
    idle_seconds: float = 30 * 60
