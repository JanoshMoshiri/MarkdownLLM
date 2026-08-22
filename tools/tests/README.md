# Floor Test Execution Convention

The full suite is a **verify-stage gate** (sprint verify, release boundary,
CI), never the inner loop. Day-to-day, run the focused set for the modules
you touched. This convention exists because the serial full suite costs
~37 minutes on the reference machine — an inner loop nobody runs is a gate
that only fires after the mistakes are stacked.

## Inner loop — focused selection

Run the test files that own the modules you changed (map below), plus
`test_mdllm.py -k <area>` when the change crosses the CLI surface:

```
python -m pytest tools/tests/test_<owner>.py -q
```

## Verify gate — the full suite, parallel

```
python -m pytest tools/tests -q -n auto
```

`pytest-xdist` is pinned in `requirements-ci.txt`. Tests are
`tmp_path`-isolated; a test that needs serialisation must use
`@pytest.mark.xdist_group("<reason>")` with the reason in a comment — no
silent serialisation.

## Platform coverage

CI (`.github/workflows/validate.yml`) runs the suite on a
**Linux + Windows matrix** (ubuntu-24.04, windows-2025) since sprint 2
(F7). Caveat until the first post-publication green run is observed: the
Windows leg's config has landed but never executed — CI runs only after
the operator's push — so Windows portability claims remain
operator-reference-machine evidence until that run exists. If the hosted
Windows leg proves intolerably slow, dropping it is the operator's call
at the release act.

## Markers

New tests carry one of the registered tiers (`pytest.ini`): `unit` (no
subprocess/git fixtures) or `gitfs` (real repos/processes). Back-marking the
existing suite is deliberate non-work; the tiers grow at the edge.

## Module → owning test files

Derived from imports 2026-08-21; regenerate the mapping when it drifts
(grep `from markdownllm` over `tools/tests/`). `test_mdllm.py` is the broad
CLI/integration surface and matches by `-k` keyword.

| Floor module | Owning test files |
|---|---|
| model, validation | test_mdllm, test_mechanical_state, test_structural_reference_registry, test_template_instantiation |
| repository_view, repository_transaction | test_repository_view, test_repository_transactions, test_coherence_repository_view, test_phase1_4_integration_audit |
| session, session_contract, domain_kernel | test_digest_signals, test_contract_emission, test_residual_totality, test_mdllm, test_session_gate |
| triggers | test_digest_signals, test_mechanical_state, test_mdllm |
| imports_check, mcp_server, external_trust | test_mdllm, test_membrane, test_repository_view, test_external_trust |
| sync, publish, git_transport | test_estate_sync, test_publish, test_residual_totality |
| coherence, indexes, kernel_gen | test_coherence_repository_view, test_template_sources, test_phase1_4_integration_audit |
| calc, yaml_loader | test_calc, test_strict_yaml, test_eval_integrity |
| scaffold, repo, touchpoints | test_mdllm, test_template_instantiation, test_phase1_4_integration_audit |
| adapters/*, harness_ports, lifecycle_runner, harness_diagnostics, adapter_install | test_adapter_cli, test_adapter_contract, test_adapter_install, test_codex_adapter, test_cowork_adapter, test_harness_ports, test_harness_diagnostics, test_lifecycle_runner, test_scaffold_harness_selection, test_architecture_fitness |
| evals | test_eval_integrity, test_residual_totality |
| doctor, refresh, cli | test_adapter_cli, test_residual_totality, test_runtime |
| assemble, bundle_service | test_assemble |
| provenance | test_repository_view, test_mdllm |
