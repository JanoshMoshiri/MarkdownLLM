#!/usr/bin/env python3
"""mdllm — the MarkdownLLM deterministic floor (entry shim).

The public entry point: `python {framework_root}/tools/mdllm.py <cmd>`. This
path is a contract — every domain's AGENTS.md, the installed pre-commit
hooks, and the generated .claude/settings.json all invoke it — so it stays,
while the implementation lives in the `markdownllm/` package beside it
(one module per reason to change; see markdownllm/__init__.py).

The re-exports below are the module's public face for programmatic use
(`import mdllm`): the floor's test suite pins behaviour through exactly
these names.

Requires: Python 3.10+, PyYAML. tiktoken optional (tokens falls back to heuristic).
"""

from __future__ import annotations

import sys

# When run as a script, this file's directory (tools/) is sys.path[0], so the
# package beside the shim resolves with no path manipulation. When imported
# (tests), the importer already put tools/ on sys.path.

from markdownllm.model import (
    RESERVED_STATUSES, DEFAULT_STATUSES, TERMINAL_STATUSES, RESERVED_TERMINAL,
    CORE_FIELDS,
    DEFAULT_EXCLUDES, NON_THING_FILES, ID_RE, ISO_RE,
    SEV_ERROR, SEV_WARNING, SEV_INFO,
    Thing, Finding, Corpus, parse_frontmatter, load_schema, scan,
    terminal_statuses_for, is_terminal,
)
from markdownllm.validation import (
    valid_statuses_for, validate_level1, validate_level2, version_tuple,
    check_version_sync, validate_level3, validate_corpus, example_corpora,
    quarantine_findings, cmd_validate,
)
from markdownllm.repo import git_short_sha, framework_version, _version_lt, TIERS
from markdownllm.triggers import cmd_triggers
from markdownllm.indexes import (
    INDEX_FILES, build_index_body, index_drift_findings, cmd_index,
)
from markdownllm.touchpoints import cmd_touchpoints
from markdownllm.cascade import cmd_cascade
from markdownllm.tokens import cmd_tokens
from markdownllm.provenance import cmd_provenance
from markdownllm.history import cmd_changelog, cmd_worklog
from markdownllm.refresh import _changelog_versions_since, cmd_refresh
from markdownllm.evals import (
    check_assertions, seed_run_dir, eval_report, _resolve_claude_cli, cmd_eval,
)
from markdownllm.kernel_gen import (
    KERNEL_RE, _token_counter, build_kernel, cmd_kernel,
)
from markdownllm.domain_kernel import (
    DOMAIN_KERNEL_BLOCKS, apply_domain_kernel, build_domain_kernel_blocks,
    cmd_domain_kernel, domain_kernel_status,
)
from markdownllm.session import _velocity_signal, _orient_forward, cmd_session_start
from markdownllm.coherence import _changed_files_recent, coherence_findings, cmd_coherence
from markdownllm.scaffold import HOOK_BODY, install_hook, cmd_install_hook, cmd_scaffold
from markdownllm.doctor import _upstream_sentinel_version, cmd_doctor
from markdownllm.mcp_server import (
    mcp_domain_id, mcp_exposed_things, mcp_list_tools, mcp_query_things,
    mcp_get_deliverable, mcp_build_manifest, mcp_list_resources,
    mcp_read_resource, cmd_mcp_serve,
)
from markdownllm.imports_check import imports_freshness, cmd_imports_check
from markdownllm.cli import build_cli, main

if __name__ == "__main__":
    sys.exit(main())
