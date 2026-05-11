# Getting Started

## What this repository is

This is a public method repository.

It contains:

- code
- directory contracts
- database skeletons

It does not contain:

- restricted raw source data
- local parquet conversions
- generated patient-level outputs

## What a new user should do

1. Clone this repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Read [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](DATABASE_LINEAGE_AND_VERSION_MATRIX.md) and confirm which database or module you are actually working with.
4. Read [`docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`](STANDARD_SYSTEM_MATURITY_ROADMAP.md) if you need the formal current-state vs target-state roadmap for the standard system itself.
5. Read [`docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`](standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md) to see which variable classes are already identifiable and which rollout order is currently recommended.
6. Read [`docs/standard_system_mvp/README.md`](standard_system_mvp/README.md) for the current governed MVP batch and runtime-evidence landing surface.
7. Read the class-2 bundle under [`docs/standard_system_mvp`](standard_system_mvp/README.md) if you need the current class-2 definition, current class-2 closure, total closure review, MIMIC expansion decision, duration-summary approvals, Amsterdam next ICU and ICU/MCU admission approvals, baseline-snapshot approvals, grouped/proxy split approval, first window-summary approval, Amsterdam first-day urine-output candidate/formal review, Amsterdam hospital-LOS candidate boundary review, and BMI derived-baseline candidate/formal reviews.
8. Read the class-3 and opening class-5 bundle under [`docs/standard_system_mvp`](standard_system_mvp/README.md) if you need the binary-state episode class, the MIMIC and Amsterdam approval path for invasive mechanical ventilation active, the MIMIC respiratory-support single-status expansions through NIV, HFNC, supplemental oxygen, and tracheostomy, the Amsterdam respiratory-support third-layer audit, the cross-database vasopressor-support and RRT active approvals, and the MIMIC plus Amsterdam RRT child split into CRRT-family, non-CRRT, and exact modality episode layers.
9. Read [`docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`](standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md) for the historical first reviewed class-1 batch milestone.
10. Read [`docs/standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`](standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md) and [`docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md`](standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md) for the current broader class-1 approval closure.
11. Read the matching onboarding playbook under [`docs/onboarding`](onboarding/README.md).
12. Obtain database access from the official source.
13. Put the source files into the expected sibling local-work path `Methods/Clinical_Database/local_work/Layer 1/<database>/raw_original` or `raw_unpacked` outside this public repository.
14. Read [`Framework_Guideline/Layer3_Directory_Contract.md`](../Framework_Guideline/Layer3_Directory_Contract.md) before creating retained Layer 3 outputs.
15. Use [`scripts/public_workflow.py`](../scripts/public_workflow.py) to run the first public entrypoints.
16. Run downstream build scripts after the database-specific pipeline is published into this repository.

## Current important paths

- `requirements.txt`
- `docs/CURRENT_STAGE_COMPLETION_STANDARD.md`
- `docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`
- `docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`
- `docs/standard_system_mvp/README.md`
- `docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`
- `docs/standard_system_mvp/variable_classes/baseline_summary_window_numeric/README.md`
- `docs/standard_system_mvp/CLASS2_FIRST_MVP_SELECTION.md`
- `docs/standard_system_mvp/CLASS2_CURRENT_APPROVAL_CLOSURE.md`
- `docs/standard_system_mvp/CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md`
- `docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md`
- `docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`
- `docs/standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md`
- `docs/standard_system_mvp/variable_classes/event_level_numeric_primary_source/README.md`
- `docs/standard_system_mvp/std_heart_rate/variable_spec.json`
- `docs/standard_system_mvp/std_heart_rate/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_heart_rate/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_heart_rate/execution.py`
- `docs/standard_system_mvp/std_icu_los_days/variable_spec.json`
- `docs/standard_system_mvp/std_icu_los_days/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_icu_los_days/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_icu_los_days/execution.py`
- `docs/standard_system_mvp/std_hospital_los_days/variable_spec.json`
- `docs/standard_system_mvp/std_hospital_los_days/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_hospital_los_days/execution.py`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/variable_spec.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/execution.py`
- `docs/standard_system_mvp/std_weight_admission_baseline/variable_spec.json`
- `docs/standard_system_mvp/std_weight_admission_baseline/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_weight_admission_baseline/execution.py`
- `docs/standard_system_mvp/std_weight_icu_baseline/variable_spec.json`
- `docs/standard_system_mvp/std_weight_icu_baseline/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_weight_icu_baseline/execution.py`
- `docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/variable_spec.json`
- `docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/execution.py`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/variable_spec.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_first_day_urine_output_summary/execution.py`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/variable_spec.json`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/execution.py`
- `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/variable_spec.json`
- `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/execution.py`
- `docs/standard_system_mvp/std_supplemental_oxygen_active/variable_spec.json`
- `docs/standard_system_mvp/std_supplemental_oxygen_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_supplemental_oxygen_active/execution.py`
- `docs/standard_system_mvp/std_tracheostomy_status_active/variable_spec.json`
- `docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_tracheostomy_status_active/execution.py`
- `docs/standard_system_mvp/std_vasopressor_support_active/variable_spec.json`
- `docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_vasopressor_support_active/execution.py`
- `docs/standard_system_mvp/std_rrt_active/variable_spec.json`
- `docs/standard_system_mvp/std_rrt_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_rrt_active/execution.py`
- `docs/standard_system_mvp/std_crrt_family_active/variable_spec.json`
- `docs/standard_system_mvp/std_crrt_family_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_crrt_family_active/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_crrt_family_active/execution.py`
- `docs/standard_system_mvp/std_non_crrt_rrt_active/variable_spec.json`
- `docs/standard_system_mvp/std_non_crrt_rrt_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_non_crrt_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_non_crrt_rrt_active/execution.py`
- `docs/standard_system_mvp/std_rrt_modality_episode/variable_spec.json`
- `docs/standard_system_mvp/std_rrt_modality_episode/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_rrt_modality_episode/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_rrt_modality_episode/execution.py`
- `docs/database_catalog.json`
- `docs/release_safe_manifest.json`
- `docs/PUBLIC_INVENTORY.md`
- `docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md`
- `docs/public_exports/README.md`
- `docs/onboarding/README.md`
- `docs/onboarding/families/README.md`
- `docs/tutorials/README.md`
- `docs/NEXT_STAGE_PUBLIC_METHOD_REPOSITORY_CHECKLIST.md`
- `Framework_Guideline/Layer1_Directory_Contract.md`
- `Framework_Guideline/Layer3_Directory_Contract.md`
- `Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md`
- `Framework_Guideline/Database_Critical_Semantics_Contract.md`
- `Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md`
- `Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`
- `Framework_Guideline/ID_Normalization_Contract.md`
- `Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md`
- `Framework_Guideline/Layer5_PublicVariableCard_Contract.md`
- `Framework_Guideline/PolicyRegistry_Contract.md`
- `Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md`
- `Framework_Guideline/Script_Placement_Contract.md`
- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`
- `Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md`
- `Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md`
- `docs/std_variable_cards/README.md`
- `docs/RELEASE_CHANGELOG.md`
- `docs/releases/README.md`
- `scripts/public_workflow.py`
- `scripts/check_public_repository.py`
- `scripts/prepare_public_release.py`
- `scripts/scaffold_public_database.py`
- `scripts/standard_system_mvp_engine.py`
- `scripts/validate_standard_system_reproducibility.py`
- `scripts/validate_standard_system_runtime.py`
- `Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-3.1/`
- `Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-ECHO-1.0/`
- `Methods/Clinical_Database/local_work/Layer 1/AmsterdamUMCdb-1.0.2/`
- `scripts/layer1/convert_amsterdam_raw_unpacked_to_parquet.py`
- `scripts/generate_layer4_layer5_excel_templates.py`
- `scripts/layer1/unpack_mimic_raw_original_to_raw_unpacked.py`
- `scripts/layer1/convert_mimic_raw_unpacked_to_parquet.py`
- `scripts/layer1/unpack_mimic_echo_raw_original_to_raw_unpacked.py`
- `scripts/layer1/convert_mimic_echo_raw_unpacked_to_parquet.py`
- `scripts/layer1/download_mimic_note_to_layer1.py`
- `scripts/layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py`
- `scripts/layer4/validate_policy_registry.py`
- `scripts/layer5/export_layer3_filtered_preview.py`
- `scripts/layer5/summarize_layer3_numeric_asset.py`

## Path interpretation rule

- GitHub-facing prose should avoid machine-specific absolute paths and prefer forward-slash relative paths
- paths inside this repository should stay repo-relative
- sibling local-work paths are written as workspace-relative paths such as `Methods/Clinical_Database/local_work/...`
- shell examples may use shell-native repo-root-relative paths such as `../../Methods/Clinical_Database/local_work/...` so they stay machine-independent

## Supported database IDs right now

- `MIMIC-IV-3.1`
- `MIMIC-IV-ECHO-1.0`
- `AmsterdamUMCdb-1.0.2`

Use [`docs/database_catalog.json`](database_catalog.json) as the machine-readable source of truth and [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](DATABASE_LINEAGE_AND_VERSION_MATRIX.md) as the human-readable overview.

## Canonical ID rule

Use [`Framework_Guideline/ID_Normalization_Contract.md`](../Framework_Guideline/ID_Normalization_Contract.md) as the global identifier dictionary.

Short version:

- `subject_id` = patient-level identifier
- `hadm_id` = hospital-admission-level identifier
- `stay_id` = ICU-stay-level or ICU-semantic stay-equivalent identifier

Do not assign these names by raw source spelling alone.
Assign them by semantic layer.

## Public workflow entrypoints

Current entrypoint shape:

```powershell
python scripts/public_workflow.py status
python scripts/public_workflow.py status --family-id MIMIC-IV
python scripts/public_workflow.py build-layer1 --database-id MIMIC-IV-3.1 --action unpack --layer1-root "..\..\Methods\Clinical_Database\local_work\Layer 1\MIMIC-IV-3.1"
python scripts/public_workflow.py validate-registry --registry "path\to\PolicyRegistry.json"
python scripts/public_workflow.py run-standard-mvp --variable-id std_heart_rate --database-id MIMIC-IV-3.1 --validate-only
python scripts/public_workflow.py validate-layer3-layout
python scripts/public_workflow.py validate-standard-runtime --runtime-dir "docs\standard_system_mvp\std_heart_rate\runtime\mimic_iv_3_1_first_real_execution"
python scripts/public_workflow.py check-standard-rerun --baseline-runtime-dir "docs\standard_system_mvp\std_heart_rate\runtime\amsterdamumcdb_1_0_2_first_real_execution" --candidate-runtime-dir "docs\standard_system_mvp\std_heart_rate\runtime\amsterdamumcdb_1_0_2_rerun_repro_check"
python scripts/public_workflow.py export-public-artifacts --artifact release-governance
python scripts/public_workflow.py export-public-artifacts --master-index "path\to\Layer5_StdVariable_MasterIndex.xlsx" --all-reviewed-approved --output-dir "docs\std_variable_cards"
python scripts/public_workflow.py export-public-artifacts --artifact release-safe-manifest
python scripts/public_workflow.py export-public-artifacts --artifact public-inventory
python scripts/public_workflow.py export-public-artifacts --artifact family-summary --family-id MIMIC-IV
python scripts/public_workflow.py export-public-artifacts --artifact database-variable-coverage
python scripts/public_workflow.py export-public-artifacts --artifact variable-coverage-summary
python scripts/public_workflow.py prepare-release --dry-run
python scripts/public_workflow.py scaffold-public-database --database-id NEW-DB-1.0 --family-id NEW-FAMILY --version 1.0 --dry-run
python scripts/public_workflow.py check-public-repository
```

These wrappers are intentionally lightweight.
They make the public workflow legible without hiding the underlying Layer 1, Layer 4, and Layer 5 scripts.

The relative examples above assume the current shell is at the repository root.

The newer governance-oriented entrypoints are:

- `prepare-release`
- `scaffold-public-database`
- `run-standard-mvp`
- `validate-standard-runtime`
- `check-standard-rerun`

## Onboarding playbooks

Start from:

- [`docs/onboarding/families/MIMIC-IV.md`](onboarding/families/MIMIC-IV.md)
- [`docs/onboarding/families/AmsterdamUMCdb.md`](onboarding/families/AmsterdamUMCdb.md)
- [`docs/onboarding/MIMIC-IV-3.1.md`](onboarding/MIMIC-IV-3.1.md)
- [`docs/onboarding/MIMIC-IV-ECHO-1.0.md`](onboarding/MIMIC-IV-ECHO-1.0.md)
- [`docs/onboarding/AmsterdamUMCdb-1.0.2.md`](onboarding/AmsterdamUMCdb-1.0.2.md)

## Representative tutorials

The first public-safe tutorials live under [`docs/tutorials`](tutorials/README.md).

## Public exports

The narrower generated public export set lives under [`docs/public_exports`](public_exports/README.md).

## MIMIC-IV-ECHO placement

`MIMIC-IV-ECHO v1.0` is governed as a sibling module, not as a permanent child of `MIMIC-IV-3.1`.

Practical rule:

1. stage core `hosp` / `icu` / `ed` / `note` material under `Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-3.1/`
2. stage ECHO material under `Methods/Clinical_Database/local_work/Layer 1/MIMIC-IV-ECHO-1.0/`
3. compare or align them through `subject_id`, `study_id`, `measurement_id`, and explicit time-alignment notes rather than directory nesting

## Script placement rule

Follow `Framework_Guideline/Script_Placement_Contract.md`.

Short version:

1. `Shared/scripts` only for truly shared cross-project tools
2. `Github/Clinical_Database/scripts` only for GitHub-safe reusable method scripts
3. `Methods/Clinical_Database/local_work/scripts` for local production and local admin scripts

## MIMIC Layer 1 note caveat

Current MIMIC Layer 1 has two possible note paths:

1. preferred path:
   - stage the official PhysioNet note source
   - use the normal Layer 1 MIMIC scripts
2. fallback path:
   - reconstruct a local note `csv.gz` proxy from existing note parquet
   - use `scripts/layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py`

The fallback path is operationally valid for local ETL continuity, but it is not equivalent to a fully staged official raw note delivery.
