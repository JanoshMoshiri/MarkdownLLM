#!/usr/bin/env python3
"""mdllm — the MarkdownLLM deterministic floor (entry shim).

The public entry file is `{framework_root}/tools/mdllm.py`. A floor-capable
Python may invoke it directly; the Windows manual route (`mdllm.ps1`) and
harness projections resolve and dependency-probe an interpreter before they
invoke the same file. This path is a contract, so it stays, while the
implementation lives in the `markdownllm/` package beside it
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
    declared_field_names, declared_type_names,
)
from markdownllm.repository_view import (
    RepositoryHeadMoved, RepositoryView, RepositoryViewError,
    RepositoryViewMode,
)
from markdownllm.validation import (
    valid_statuses_for, validate_level1, validate_level2, version_tuple,
    check_version_sync, validate_level3, validate_corpus, example_corpora,
    workflow_transition_findings,
    quarantine_findings, retrospective_findings, derivation_findings,
    session_gate_findings, SESSION_GATE_WINDOW_HOURS,
    cmd_validate,
)
from markdownllm.repo import git_short_sha, framework_version, version_lt, TIERS

_version_lt = version_lt  # compatibility for the historical CLI facade
from markdownllm.triggers import (
    TriggerEvaluation, TriggerOutcome, TriggerResult,
    evaluate, evaluate_results, evaluate_typed, cmd_triggers,
)
from markdownllm.indexes import (
    INDEX_FILES, build_index_body, index_drift_findings, cmd_index,
)
from markdownllm.calc import (
    CalcError, Column, Context, Derivation,
    to_decimal, fmt, values_equal, resolve_path, set_path,
    evaluate_expression, evaluate_block, is_quarantined, context_for, cmd_calc,
)
from markdownllm.touchpoints import cmd_touchpoints
from markdownllm.cascade import cmd_cascade
from markdownllm.tokens import cmd_tokens
from markdownllm.dispatch_payload import (
    DispatchLaunch, DispatchPayloadRefused, build_launch, compose_payload,
    declared_input_names, read_dispatch_prompt, resolve_scope,
    cmd_dispatch_payload,
)
from markdownllm.provenance import cmd_provenance
from markdownllm.history import cmd_changelog, cmd_worklog
from markdownllm.refresh import _changelog_versions_since, cmd_refresh
from markdownllm.evals import (
    check_assertions, seed_run_dir, eval_report, _resolve_claude_cli, cmd_eval,
)
from markdownllm.kernel_gen import (
    KERNEL_RE, token_counter, build_kernel, cmd_kernel,
)

_token_counter = token_counter  # compatibility for the historical CLI facade
from markdownllm.domain_kernel import (
    DOMAIN_KERNEL_BLOCKS, apply_domain_kernel, build_domain_kernel_blocks,
    cmd_domain_kernel, domain_kernel_status,
)
from markdownllm.session import _velocity_signal, _orient_forward, cmd_session_start
from markdownllm.coherence import _changed_files_recent, coherence_findings, cmd_coherence
from markdownllm.skill_vocabulary import (
    VocabularyUse, skill_vocabulary_findings, vocabulary_uses,
)
from markdownllm.hook_contract import (
    HOOK_BODY, COMMIT_MSG_HOOK_BODY, FLOOR_DEPENDENCY, SH_RESOLVE,
    InterpreterCandidate,
)
from markdownllm.scaffold import (
    install_hook, cmd_install_hook, cmd_scaffold,
)
from markdownllm.runtime import (
    interpreter_candidates, probe_candidate,
    probe, git_supports_hook_run, execution_test_hook, cmd_runtime_probe,
)
from markdownllm.adapter_install import (
    AdapterInstallTarget, ArtifactDecision, InstallPlan, ApplyResult,
    InstallRefused, InstallStateChanged, AtomicInstallError,
    WholeArtifactPolicy, TopLevelJsonFragmentPolicy,
    target_for_adapter, preflight_install, apply_install,
)
from markdownllm.lifecycle_runner import (
    StepExecution, LifecycleExecution, execute_lifecycle,
    dispatch_lifecycle_event, cmd_harness_event,
)
from markdownllm.boundary import (
    TERMS_FILE, load_terms, load_located_terms, scan_text, self_guard,
    staged_findings, history_findings, term_audit_findings, cmd_boundary,
)
from markdownllm.doctor import _upstream_sentinel_version, cmd_doctor
from markdownllm.mcp_server import (
    mcp_domain_id, mcp_exposed_things, mcp_list_tools, mcp_query_things,
    mcp_get_deliverable, mcp_build_manifest, mcp_list_resources,
    mcp_read_resource, mcp_make_dispatcher, mcp_http_server,
    mcp_host_is_loopback, cmd_mcp_serve,
)
from markdownllm.imports_check import (
    imports_freshness, face_coverage, cmd_imports_check, cmd_estate_check,
)
from markdownllm.external_trust import (
    ExternalCapability, ExternalTrustError, ExternalTrustPolicy,
    LocalExternalTrustPolicy, RepositoryIdentity, TrustDecision,
    canonical_entry_hash, repository_identity, required_capabilities,
    grant_external_trust, revoke_external_trust, review_lines,
    load_mcp_address_book, cmd_external_trust,
)
from markdownllm.sync import (
    PublicationPolicy, PublicationPolicyState, discover_repos,
    publication_policy, sync_repo, cmd_estate_sync,
)
from markdownllm.cli import build_cli, cmd_adapter_install, main

if __name__ == "__main__":
    sys.exit(main())
