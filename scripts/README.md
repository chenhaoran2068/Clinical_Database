# Scripts

This folder stores public, reusable scripts for the clinical database standardization workflow.

Current rule:

- scripts should avoid local hard-coded machine paths
- scripts should prefer command-line arguments
- only GitHub-safe scripts should be stored here
- follow `Framework_Guideline/Script_Placement_Contract.md`

Boundary note:

- `GitHub-safe` means the script code, interface, and documentation are safe to publish
- some scripts in this tree are still intended to run locally against user-staged sibling local-work assets under `Methods/Clinical_Database/local_work/...`
- when those scripts read local patient-level assets, the outputs remain local and are not themselves part of this public repository

Primary public entrypoint:

- `python scripts/public_workflow.py status`

Current public script files:

- `public_workflow.py`
- `check_public_repository.py`
- `export_public_metadata.py`
- `prepare_public_release.py`
- `scaffold_public_database.py`
- `standard_system_mvp_engine.py`
- `validate_layer3_layout_policy.py`
- `validate_standard_system_reproducibility.py`
- `validate_standard_system_runtime.py`
- `generate_layer4_layer5_excel_templates.py`
- `build_amsterdam_coverage_audit.py`
- `build_class1_to_class9_execution_queue.py`
- `build_amsterdam_q2_direct_candidate_artifacts.py`
- `build_amsterdam_q4_class1_wave1_candidate_artifacts.py`
- `prepare_amsterdam_q4_class1_wave1_owner_review_packet.py`
- `apply_amsterdam_q4_class1_wave1_owner_approval.py`
- `build_amsterdam_q4_and_q3_to_q7_registers.py`
- `layer1/convert_amsterdam_raw_unpacked_to_parquet.py`
- `layer1/convert_mimic_raw_unpacked_to_parquet.py`
- `layer1/unpack_mimic_raw_original_to_raw_unpacked.py`
- `layer1/convert_mimic_echo_raw_unpacked_to_parquet.py`
- `layer1/unpack_mimic_echo_raw_original_to_raw_unpacked.py`
- `layer1/download_mimic_note_to_layer1.py`
- `layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py`
- `layer4/validate_policy_registry.py`
- `layer5/master_index_helper.py`
- `layer5/check_local_id_semantics.py`
- `layer5/export_public_variable_card.py`
- `layer5/export_layer3_filtered_preview.py`
- `layer5/summarize_layer3_numeric_asset.py`
- `layer5/generate_ja_jp_localization_draft.py`
- `layer5/upgrade_layer5_master_index_for_server_catalog.py`

Script-local support docs:

- `layer5/README.md`

Recommended entrypoints:

- `python scripts/public_workflow.py status`
- `python scripts/public_workflow.py status --family-id MIMIC-IV`
- `python scripts/public_workflow.py build-layer1 ...`
- `python scripts/public_workflow.py validate-registry ...`
- `python scripts/public_workflow.py run-standard-mvp --variable-id std_heart_rate --database-id MIMIC-IV-3.1 --validate-only`
- `python scripts/public_workflow.py validate-layer3-layout`
- `python scripts/standard_system_mvp_engine.py` is not normally called directly; it is the shared governed engine used by per-variable `docs/standard_system_mvp/<variable_id>/execution.py` wrappers
- `python scripts/public_workflow.py validate-standard-runtime --runtime-dir "docs\\standard_system_mvp\\std_heart_rate\\runtime\\mimic_iv_3_1_first_real_execution"`
- `python scripts/public_workflow.py check-standard-rerun --baseline-runtime-dir "docs\\standard_system_mvp\\std_heart_rate\\runtime\\amsterdamumcdb_1_0_2_first_real_execution" --candidate-runtime-dir "docs\\standard_system_mvp\\std_heart_rate\\runtime\\amsterdamumcdb_1_0_2_rerun_repro_check"`
- `python scripts/public_workflow.py check-public-repository`
- `python scripts/public_workflow.py check-local-id-semantics --database-id AmsterdamUMCdb-1.0.2`
- `python scripts/public_workflow.py prepare-release --dry-run`
- `python scripts/public_workflow.py scaffold-public-database --help`
- `python scripts/public_workflow.py export-public-artifacts ...`
- `python scripts/public_workflow.py export-public-artifacts --artifact release-governance`
- `python scripts/public_workflow.py export-public-artifacts --artifact release-safe-manifest`
- `python scripts/public_workflow.py export-public-artifacts --artifact public-inventory`
- `python scripts/public_workflow.py export-public-artifacts --artifact database-variable-coverage`
- `python scripts/public_workflow.py export-public-artifacts --artifact family-variable-coverage`
- `python scripts/public_workflow.py export-public-artifacts --artifact variable-coverage-summary`
- `python scripts/build_amsterdam_coverage_audit.py`
- `python scripts/build_class1_to_class9_execution_queue.py`
- `python scripts/build_amsterdam_q2_direct_candidate_artifacts.py`
- `python scripts/build_amsterdam_q4_class1_wave1_candidate_artifacts.py`
- `python scripts/prepare_amsterdam_q4_class1_wave1_owner_review_packet.py`
- `python scripts/apply_amsterdam_q4_class1_wave1_owner_approval.py`
- `python scripts/build_amsterdam_q4_and_q3_to_q7_registers.py`

Local production-only scripts are intentionally not stored here.
Those now live under:

- `Methods/Clinical_Database/local_work/scripts`
