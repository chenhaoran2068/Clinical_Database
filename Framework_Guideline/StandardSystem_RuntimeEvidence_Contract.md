# Standard-System Runtime Evidence Contract

This contract defines the public GitHub-safe runtime-evidence layer for the first governed standard-system MVP executions.

Current scope:

- `validation_report.json`
- `manifest.json`
- `reproducibility_report.json` when a governed rerun comparison is recorded
- runtime stdout/stderr logs when present

These artifacts are the first public machine-readable proof that a governed execution path actually ran and what it ran against.

## Why this contract exists

After the project moved from static specs into governed execution, it was no longer enough to say:

- what the variable means
- how one database maps to it

The system also needs a stable way to say:

- what was checked before execution
- what command path was used
- which specs were in force
- what process batch ran
- whether the run succeeded

Without a runtime-evidence contract, each execution could emit ad hoc JSON files that drift over time.

## Core split

Treat the two JSON artifacts as related but different roles:

- `validation_report.json` = machine-readable pre-run or gate report
- `manifest.json` = machine-readable execution provenance record

Do not collapse them into one file.

## Recommended placement

Public-safe runtime evidence should live under:

- `docs/standard_system_mvp/<variable_id>/runtime/<run_label>/`

Current example:

- `docs/standard_system_mvp/std_heart_rate/runtime/mimic_iv_3_1_first_real_execution/`

When a rerun comparison is recorded, the reproducibility report should normally live in the candidate rerun directory:

- `docs/standard_system_mvp/<variable_id>/runtime/<candidate_run_label>/reproducibility_report.json`

## `validation_report.json` minimum required fields

At minimum, `validation_report.json` should include:

- `artifact_type`
- `artifact_version`
- `contract_ref`
- `generated_at`
- `validation_scope`
- `overall_status`
- `variable_id`
- `database_id`
- `variable_spec_path`
- `mapping_spec_path`
- `spec_hashes`
- `checks`

## `validation_report.json` required semantics

- `artifact_type` should be `validation_report`
- `contract_ref` should point to this contract
- `overall_status` should be one of:
  - `pass`
  - `fail`
- `checks` should be a non-empty list of machine-readable check records
- each check record should include:
  - `check_id`
  - `status`
  - `message`
- if `overall_status = pass`, all check records should currently pass

## `manifest.json` minimum required fields

At minimum, `manifest.json` should include:

- `artifact_type`
- `artifact_version`
- `contract_ref`
- `generated_at`
- `variable_id`
- `database_id`
- `execution_mode`
- `validation_status`
- `variable_spec_path`
- `mapping_spec_path`
- `execution_entrypoint_path`
- `reference_implementation_path`
- `local_input_asset_path`
- `command`
- `process_batch_id`
- `subprocess_return_code`
- `started_at`
- `finished_at`
- `spec_hashes`
- `output_artifacts`
- `output_signatures`
- `build_summary`

## `manifest.json` required semantics

- `artifact_type` should be `execution_manifest`
- `contract_ref` should point to this contract
- `execution_mode` should currently be one of:
  - `validate_only`
  - `dry_run`
  - `execute`
  - `blocked_by_validation`
- `validation_status` should match the paired `validation_report.json`
- `variable_id`, `database_id`, `variable_spec_path`, `mapping_spec_path`, and `spec_hashes` should match the paired `validation_report.json`
- `output_artifacts` should be a machine-readable map of the execute-mode formal output files that this run produced or reaffirmed
- `output_signatures` should record at minimum `sha256` and `size_bytes` for each listed output artifact
- `build_summary` should retain the machine-readable key metrics parsed from governed stdout when that summary is available

## Public-path rule

The runtime evidence is part of the public repository surface.

Therefore these artifacts should avoid machine-bound absolute paths.

Preferred path forms are:

- repo-relative paths for files inside this repository
- workspace-relative paths such as `Methods/Clinical_Database/local_work/...` for sibling local-work evidence outside this repository

Avoid:

- `drive:\...`
- other machine-specific absolute paths

## Execute-mode rule

If `execution_mode = execute`, then the runtime evidence should additionally satisfy:

- `overall_status = pass`
- `validation_status = pass`
- `subprocess_return_code = 0`
- `process_batch_id` is present
- stdout log exists
- stdout log contains the same `process_batch_id`
- stderr log is empty or absent
- `output_artifacts` is non-empty and uses public-safe workspace-relative paths
- `output_signatures` covers the same artifact keys as `output_artifacts`
- the post-run validator can recompute current hashes for those artifacts and confirm they still match the recorded signatures

## Current process batch format

Current governed MVP runs should use a batch-id pattern compatible with:

- `YYYYMMDDTHHMMSSZ_<database_id>_<variable_id>`

Example:

- `20260423T105032Z_MIMIC-IV-3.1_std_heart_rate`

## Spec hash rule

The runtime evidence should record hashes for the exact spec files used at execution time.

Current minimum:

- hash for `variable_spec.json`
- hash for `mapping_spec.json`

These hashes should be sufficient for a post-run validator to confirm that the recorded runtime evidence still matches the currently referenced public specs.

## Output-signature rule

For execute-mode runtime evidence, spec hashes are not enough.

The runtime evidence should also record signatures for the formal output artifacts themselves.

Current expected output-artifact examples include:

- primary output parquet
- preview CSV
- Layer 5 asset manifest
- knowledge package
- build log for the recorded `process_batch_id`

If a local production builder rotates or clears its own log archive on rerun, the governed runtime layer may capture a frozen runtime-local copy of that build log under the public runtime directory.

That frozen copy is preferred over pointing only to a volatile live log-archive path.

The exact artifact list may vary by variable or database, but the rule is the same:

- if a file is part of the governed formal output surface for that run, it should be listed in `output_artifacts`
- its current `sha256` and `size_bytes` should be recorded in `output_signatures`

## Output-artifact stability classes

For rerun comparison, not every output artifact should be treated the same way.

Current practical classes are:

- `rerun_invariant`
  - examples: primary output parquet, deterministic preview CSV
  - expectation: path and signature should match across reruns
- `latest_state_mutable`
  - examples: live asset manifest, live knowledge package
  - expectation: path should stay stable, but content may legitimately change because it points to the latest local state
- `run_scoped_append_only`
  - examples: build log for a specific `process_batch_id`
  - expectation: each rerun should usually create a different path tied to its own batch id

The validator and rerun gate should compare these classes differently rather than pretending every artifact must be byte-identical across runs.

## `reproducibility_report.json` minimum required fields

At minimum, `reproducibility_report.json` should include:

- `artifact_type`
- `artifact_version`
- `contract_ref`
- `generated_at`
- `comparison_scope`
- `overall_status`
- `variable_id`
- `database_id`
- `baseline_runtime_dir`
- `candidate_runtime_dir`
- `baseline_process_batch_id`
- `candidate_process_batch_id`
- `artifact_role_policy`
- `stable_build_summary_fields`
- `checks`
- `artifact_comparisons`
- `build_summary_comparisons`

## `reproducibility_report.json` required semantics

- `artifact_type` should be `reproducibility_report`
- `comparison_scope` should currently be `rerun_reproducibility_gate`
- baseline and candidate runtime directories should each pass the runtime validator
- `artifact_role_policy` should state which artifact keys are treated as:
  - rerun-invariant
  - latest-state mutable
  - run-scoped append-only
- `stable_build_summary_fields` should identify the summary fields that are expected to match exactly across reruns
- `overall_status = pass` should mean all recorded rerun checks currently pass

## Rerun gate rule

The rerun/reproducibility gate should not compare every field blindly.

Current expected gate logic is:

- exact-match the invariant runtime metadata:
  - variable id
  - database id
  - spec hashes
  - execution entrypoint
  - reference implementation path
  - local input asset path
  - governed command
- exact-match rerun-invariant artifact signatures
- exact-match stable build-summary fields
- allow latest-state mutable artifacts to differ in signature while keeping the same live path
- allow run-scoped append-only artifacts such as build logs to differ by batch id and path

## Post-run validation rule

The project should maintain a dedicated post-run validator for runtime evidence artifacts.

That validator should check at minimum:

- required file presence
- required fields
- cross-file consistency
- current spec-hash consistency
- current output-artifact signature consistency
- process batch id format
- public-path safety
- execute-mode success conditions

## Relationship to other MVP artifacts

This contract does not replace:

- `variable_spec.json`
- `mapping_spec_<database>.json`
- the governed `execution.py` entrypoint

Those artifacts define meaning, mapping, and execution path.

This contract defines how the system proves that a governed run actually happened and what it used.
