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
(F7).

**Windows CI has still produced no green run.** Two failures so far, both
environmental, neither a floor defect:

1. *Interpreter setup* (first run): the shared pin `3.12.13` has no
   win32-x64 build — `actions/python-versions` ships Windows builds of 3.12
   only through 3.12.10. Fixed by pinning per OS (Linux 3.12.13, Windows
   3.12.10). The legs now run different patch levels of a security-only
   branch; that is recorded rather than hidden.
2. *Drive mismatch* (second run): 56 failures, **one cause**. Hosted Windows
   runners put the workspace on `D:` and `TEMP` on `C:`, so every test that
   scaffolds into `tmp_path` hit scaffold's deliberate refusal to embed an
   absolute machine-specific adapter route. Fixed by pointing pytest's
   `--basetemp` at `RUNNER_TEMP`, which shares the workspace drive.

**Running the suite on Windows requires the temp tree and the checkout to
share a drive.** If yours differ, pass `--basetemp` explicitly to a
directory on the checkout's drive (outside the repo, so scaffolded
fixtures stay out of the corpus walk). Cross-drive scaffolding is refused
by design, not broken — `test_unrelatable_framework_path_refuses_before_
target_creation` pins that guard on every platform.

Until a green Windows leg is observed, **Windows portability claims rest on
operator-reference-machine measurement alone**. If the hosted Windows leg
proves intolerably slow once it does run, dropping it is the operator's
call.

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
