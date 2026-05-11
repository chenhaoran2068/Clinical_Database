# Clinical Database

车同轨，书同文，行同伦。

This repository is the public method repository for the clinical database standardization project.

It provides:

- directory contracts
- policy-registry contracts
- database-specific critical semantics contracts
- Layer 3 retained-output layout governance
- database lineage and version tracking
- onboarding playbooks
- public workflow entrypoints
- release governance and release-note surfaces
- generated public exports and coverage summaries
- GitHub-safe public variable-card contracts
- early standard-system MVP draft specs
- public database scaffolding entrypoints
- reusable scripts
- Layer 1 database skeletons
- public tutorials
- detailed public review checklists

It does not provide:

- raw database files
- local parquet copies
- patient-level Layer 2 to Layer 5 outputs

## Start Here

1. Read [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md).
2. Check [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md).
3. Read [`docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`](docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md) to understand how the current repository baseline grows into a stricter standard system.
4. Read [`docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`](docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md) for the current variable-class map and rollout order.
5. Read [`docs/standard_system_mvp/README.md`](docs/standard_system_mvp/README.md) for the current governed MVP batch and runtime-evidence surface.
6. Read the class-2 bundle under [`docs/standard_system_mvp`](docs/standard_system_mvp/README.md), including the class definition, current closure, total closure review, MIMIC expansion decision, duration-summary approvals, Amsterdam next ICU and ICU/MCU admission approvals, baseline-snapshot approvals, grouped/proxy split approval, first window-summary approval, Amsterdam first-day urine-output candidate/formal review, Amsterdam hospital-LOS candidate boundary review, and BMI derived-baseline candidate/formal reviews.
7. Read the class-3 and opening class-5 bundle under [`docs/standard_system_mvp`](docs/standard_system_mvp/README.md), including the first binary-state approval, Amsterdam same-name candidate/formal review for invasive mechanical ventilation active, the MIMIC respiratory-support single-status expansions through NIV, HFNC, supplemental oxygen, and tracheostomy, the Amsterdam respiratory-support third-layer audit, the cross-database vasopressor-support and RRT active approvals, and the MIMIC plus Amsterdam RRT child split into CRRT-family, non-CRRT, and exact modality episode layers.
8. Read [`docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`](docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md) for the first formal content-approval closure of the reviewed `MIMIC-IV-3.1` class-1 batch.
9. Read [`docs/standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md) for the current formal approval review of `std_heart_rate`.
10. Read [`docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md`](docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md) for the current broader 11-variable class-1 closure state.
11. Install dependencies with `pip install -r requirements.txt`.
12. Place your officially obtained source data into the expected sibling local-work path `Methods/Clinical_Database/local_work/Layer 1/<database>/...` outside this public repository.
13. Read [`Framework_Guideline/Layer3_Directory_Contract.md`](Framework_Guideline/Layer3_Directory_Contract.md) before creating retained Layer 3 outputs.
14. Run the public workflow entrypoints in [`scripts/public_workflow.py`](scripts/public_workflow.py).
15. Use `prepare-release`, `validate-layer3-layout`, and `check-public-repository` to keep the public release surface coherent.

## Main References

- [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md)
- [`docs/CURRENT_STAGE_COMPLETION_STANDARD.md`](docs/CURRENT_STAGE_COMPLETION_STANDARD.md)
- [`docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md`](docs/DATABASE_LINEAGE_AND_VERSION_MATRIX.md)
- [`docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md`](docs/STANDARD_SYSTEM_MATURITY_ROADMAP.md)
- [`docs/standard_system_mvp/README.md`](docs/standard_system_mvp/README.md)
- [`docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`](docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md)
- [`docs/standard_system_mvp/variable_classes/baseline_summary_window_numeric/README.md`](docs/standard_system_mvp/variable_classes/baseline_summary_window_numeric/README.md)
- [`docs/standard_system_mvp/CLASS2_FIRST_MVP_SELECTION.md`](docs/standard_system_mvp/CLASS2_FIRST_MVP_SELECTION.md)
- [`docs/standard_system_mvp/CLASS2_CURRENT_APPROVAL_CLOSURE.md`](docs/standard_system_mvp/CLASS2_CURRENT_APPROVAL_CLOSURE.md)
- [`docs/standard_system_mvp/CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md`](docs/standard_system_mvp/CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md)
- [`docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md`](docs/standard_system_mvp/AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md)
- [`docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`](docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md)
- [`docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`](docs/standard_system_mvp/CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md)
- [`docs/standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`](docs/standard_system_mvp/STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md)
- [`docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md`](docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md)
- [`docs/standard_system_mvp/variable_classes/event_level_numeric_primary_source/README.md`](docs/standard_system_mvp/variable_classes/event_level_numeric_primary_source/README.md)
- [`docs/standard_system_mvp/std_heart_rate/variable_spec.json`](docs/standard_system_mvp/std_heart_rate/variable_spec.json)
- [`docs/standard_system_mvp/std_heart_rate/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_heart_rate/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_heart_rate/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_heart_rate/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_heart_rate/execution.py`](docs/standard_system_mvp/std_heart_rate/execution.py)
- [`docs/standard_system_mvp/std_icu_los_days/variable_spec.json`](docs/standard_system_mvp/std_icu_los_days/variable_spec.json)
- [`docs/standard_system_mvp/std_icu_los_days/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_icu_los_days/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_icu_los_days/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_icu_los_days/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_icu_los_days/execution.py`](docs/standard_system_mvp/std_icu_los_days/execution.py)
- [`docs/standard_system_mvp/std_hospital_los_days/variable_spec.json`](docs/standard_system_mvp/std_hospital_los_days/variable_spec.json)
- [`docs/standard_system_mvp/std_hospital_los_days/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_hospital_los_days/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_hospital_los_days/execution.py`](docs/standard_system_mvp/std_hospital_los_days/execution.py)
- [`docs/standard_system_mvp/std_days_to_next_icu_admission/variable_spec.json`](docs/standard_system_mvp/std_days_to_next_icu_admission/variable_spec.json)
- [`docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_days_to_next_icu_admission/execution.py`](docs/standard_system_mvp/std_days_to_next_icu_admission/execution.py)
- [`docs/standard_system_mvp/std_weight_admission_baseline/variable_spec.json`](docs/standard_system_mvp/std_weight_admission_baseline/variable_spec.json)
- [`docs/standard_system_mvp/std_weight_admission_baseline/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_weight_admission_baseline/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_weight_admission_baseline/execution.py`](docs/standard_system_mvp/std_weight_admission_baseline/execution.py)
- [`docs/standard_system_mvp/std_weight_icu_baseline/variable_spec.json`](docs/standard_system_mvp/std_weight_icu_baseline/variable_spec.json)
- [`docs/standard_system_mvp/std_weight_icu_baseline/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_weight_icu_baseline/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_weight_icu_baseline/execution.py`](docs/standard_system_mvp/std_weight_icu_baseline/execution.py)
- [`docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/variable_spec.json`](docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/variable_spec.json)
- [`docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/execution.py`](docs/standard_system_mvp/std_weight_icu_baseline_grouped_proxy/execution.py)
- [`docs/standard_system_mvp/std_first_day_urine_output_summary/variable_spec.json`](docs/standard_system_mvp/std_first_day_urine_output_summary/variable_spec.json)
- [`docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_first_day_urine_output_summary/execution.py`](docs/standard_system_mvp/std_first_day_urine_output_summary/execution.py)
- [`docs/standard_system_mvp/std_noninvasive_ventilation_active/variable_spec.json`](docs/standard_system_mvp/std_noninvasive_ventilation_active/variable_spec.json)
- [`docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_noninvasive_ventilation_active/execution.py`](docs/standard_system_mvp/std_noninvasive_ventilation_active/execution.py)
- [`docs/standard_system_mvp/std_high_flow_nasal_cannula_active/variable_spec.json`](docs/standard_system_mvp/std_high_flow_nasal_cannula_active/variable_spec.json)
- [`docs/standard_system_mvp/std_high_flow_nasal_cannula_active/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_high_flow_nasal_cannula_active/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_high_flow_nasal_cannula_active/execution.py`](docs/standard_system_mvp/std_high_flow_nasal_cannula_active/execution.py)
- [`docs/standard_system_mvp/std_supplemental_oxygen_active/variable_spec.json`](docs/standard_system_mvp/std_supplemental_oxygen_active/variable_spec.json)
- [`docs/standard_system_mvp/std_supplemental_oxygen_active/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_supplemental_oxygen_active/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_supplemental_oxygen_active/execution.py`](docs/standard_system_mvp/std_supplemental_oxygen_active/execution.py)
- [`docs/standard_system_mvp/std_tracheostomy_status_active/variable_spec.json`](docs/standard_system_mvp/std_tracheostomy_status_active/variable_spec.json)
- [`docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_tracheostomy_status_active/execution.py`](docs/standard_system_mvp/std_tracheostomy_status_active/execution.py)
- [`docs/standard_system_mvp/std_vasopressor_support_active/variable_spec.json`](docs/standard_system_mvp/std_vasopressor_support_active/variable_spec.json)
- [`docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_vasopressor_support_active/execution.py`](docs/standard_system_mvp/std_vasopressor_support_active/execution.py)
- [`docs/standard_system_mvp/std_rrt_active/variable_spec.json`](docs/standard_system_mvp/std_rrt_active/variable_spec.json)
- [`docs/standard_system_mvp/std_rrt_active/mapping_spec_mimic_iv_3_1.json`](docs/standard_system_mvp/std_rrt_active/mapping_spec_mimic_iv_3_1.json)
- [`docs/standard_system_mvp/std_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json`](docs/standard_system_mvp/std_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json)
- [`docs/standard_system_mvp/std_rrt_active/execution.py`](docs/standard_system_mvp/std_rrt_active/execution.py)
- [`docs/database_catalog.json`](docs/database_catalog.json)
- [`docs/layer3_directory_policy.json`](docs/layer3_directory_policy.json)
- [`docs/release_safe_manifest.json`](docs/release_safe_manifest.json)
- [`docs/PUBLIC_INVENTORY.md`](docs/PUBLIC_INVENTORY.md)
- [`docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md`](docs/PUBLIC_REPOSITORY_DETAILED_REVIEW_CHECKLIST.md)
- [`docs/public_exports/README.md`](docs/public_exports/README.md)
- [`docs/onboarding/README.md`](docs/onboarding/README.md)
- [`docs/onboarding/families/README.md`](docs/onboarding/families/README.md)
- [`docs/tutorials/README.md`](docs/tutorials/README.md)
- [`docs/NEXT_STAGE_PUBLIC_METHOD_REPOSITORY_CHECKLIST.md`](docs/NEXT_STAGE_PUBLIC_METHOD_REPOSITORY_CHECKLIST.md)
- [`Framework_Guideline/Layer1_Directory_Contract.md`](Framework_Guideline/Layer1_Directory_Contract.md)
- [`Framework_Guideline/Layer3_Directory_Contract.md`](Framework_Guideline/Layer3_Directory_Contract.md)
- [`Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md`](Framework_Guideline/CrossDatabase_Variable_Harmonization_Contract.md)
- [`Framework_Guideline/Database_Critical_Semantics_Contract.md`](Framework_Guideline/Database_Critical_Semantics_Contract.md)
- [`Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md`](Framework_Guideline/Database_Family_NewVersion_Admission_Contract.md)
- [`Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md`](Framework_Guideline/AmsterdamUMCdb_TimeSemantics_Contract.md)
- [`Framework_Guideline/ID_Normalization_Contract.md`](Framework_Guideline/ID_Normalization_Contract.md)
- [`Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md`](Framework_Guideline/MIMICIV_SourcePackageAndModuleBoundary_Contract.md)
- [`Framework_Guideline/Layer5_PublicVariableCard_Contract.md`](Framework_Guideline/Layer5_PublicVariableCard_Contract.md)
- [`Framework_Guideline/PolicyRegistry_Contract.md`](Framework_Guideline/PolicyRegistry_Contract.md)
- [`Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md`](Framework_Guideline/ReleaseSafe_Manifest_ReleaseGovernance_Contract.md)
- [`Framework_Guideline/Script_Placement_Contract.md`](Framework_Guideline/Script_Placement_Contract.md)
- [`Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`](Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md)
- [`Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md`](Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md)
- [`Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md`](Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md)
- [`docs/std_variable_cards/README.md`](docs/std_variable_cards/README.md)
- [`docs/RELEASE_CHANGELOG.md`](docs/RELEASE_CHANGELOG.md)
- [`docs/releases/README.md`](docs/releases/README.md)
- [`requirements.txt`](requirements.txt)
- [`scripts/public_workflow.py`](scripts/public_workflow.py)
- [`scripts/check_public_repository.py`](scripts/check_public_repository.py)
- [`scripts/export_public_metadata.py`](scripts/export_public_metadata.py)
- [`scripts/prepare_public_release.py`](scripts/prepare_public_release.py)
- [`scripts/scaffold_public_database.py`](scripts/scaffold_public_database.py)
- [`scripts/standard_system_mvp_engine.py`](scripts/standard_system_mvp_engine.py)
- [`scripts/validate_standard_system_reproducibility.py`](scripts/validate_standard_system_reproducibility.py)
- [`scripts/validate_standard_system_runtime.py`](scripts/validate_standard_system_runtime.py)
- [`scripts/layer5/check_local_id_semantics.py`](scripts/layer5/check_local_id_semantics.py)
- [`scripts/layer1/convert_amsterdam_raw_unpacked_to_parquet.py`](scripts/layer1/convert_amsterdam_raw_unpacked_to_parquet.py)
- [`scripts/generate_layer4_layer5_excel_templates.py`](scripts/generate_layer4_layer5_excel_templates.py)
- [`scripts/layer1/download_mimic_note_to_layer1.py`](scripts/layer1/download_mimic_note_to_layer1.py)
- [`scripts/layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py`](scripts/layer1/reconstruct_mimic_note_raw_unpacked_from_parquet.py)
- [`scripts/layer1/unpack_mimic_raw_original_to_raw_unpacked.py`](scripts/layer1/unpack_mimic_raw_original_to_raw_unpacked.py)
- [`scripts/layer1/convert_mimic_raw_unpacked_to_parquet.py`](scripts/layer1/convert_mimic_raw_unpacked_to_parquet.py)
- [`scripts/layer1/unpack_mimic_echo_raw_original_to_raw_unpacked.py`](scripts/layer1/unpack_mimic_echo_raw_original_to_raw_unpacked.py)
- [`scripts/layer1/convert_mimic_echo_raw_unpacked_to_parquet.py`](scripts/layer1/convert_mimic_echo_raw_unpacked_to_parquet.py)
- [`scripts/layer4/validate_policy_registry.py`](scripts/layer4/validate_policy_registry.py)
- [`scripts/layer5/export_layer3_filtered_preview.py`](scripts/layer5/export_layer3_filtered_preview.py)
- [`scripts/layer5/summarize_layer3_numeric_asset.py`](scripts/layer5/summarize_layer3_numeric_asset.py)
