# Public Inventory

## What this file is

This is the human-readable inventory of the current GitHub-safe public repository surface.
The machine-readable counterpart is [`docs/release_safe_manifest.json`](release_safe_manifest.json).

## Snapshot summary

- catalog version: `2026-05-09`
- family count: `6`
- database count: `7`
- public std-variable cards: `465`
- cross-database public cards: `56`
- total release-safe files listed in the manifest: `2133`
- release version: `0.1.0-dev`
- release tag: `public-method-foundation-2026-04-21`
- release status: `working_tree_snapshot`

## Release governance

- release version: `0.1.0-dev`
- release tag: `public-method-foundation-2026-04-21`
- release label: `public-method-repository-foundation`
- release status: `working_tree_snapshot`
- release date: `2026-04-21`
- changelog: `docs/RELEASE_CHANGELOG.md`
- current changelog heading: `## 0.1.0-dev - 2026-04-21`
- release notes: `docs/releases/public-method-foundation-2026-04-21.md`

## Coverage by family

| family_id | display_name | current database_ids | family playbook | family union count | family shared count |
| --- | --- | --- | --- | --- | --- |
| `MIMIC-IV` | MIMIC-IV family | `MIMIC-IV-3.1`, `MIMIC-IV-ECHO-1.0` | `docs/onboarding/families/MIMIC-IV.md` | `463` | `0` |
| `AmsterdamUMCdb` | AmsterdamUMCdb family | `AmsterdamUMCdb-1.0.2` | `docs/onboarding/families/AmsterdamUMCdb.md` | `58` | `58` |
| `SICdb` | SICdb family | `SICdb-1.0.8` | `docs/onboarding/families/SICdb.md` | `0` | `0` |
| `NWICU` | NWICU family | `NWICU-0.1.0` | `docs/onboarding/families/NWICU.md` | `0` | `0` |
| `eICU-CRD` | eICU-CRD family | `eICU-CRD-2.0` | `docs/onboarding/families/eICU-CRD.md` | `0` | `0` |
| `Zigong` | Zigong family | `Zigong-1.1` | `docs/onboarding/families/Zigong.md` | `0` | `0` |

## Coverage by database/module

| database_id | family | role | version | layer1 | layer4 | layer5 | public cards | onboarding |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `MIMIC-IV-3.1` | `MIMIC-IV` | core_database | `3.1` | published_skeleton_and_public_scripts | public MIMIC source-package boundary contract published; local Layer 4 opening registry built pending owner review | broad reviewed-approved local assets exist and public std-variable cards are published | `463` | `docs/onboarding/MIMIC-IV-3.1.md` |
| `MIMIC-IV-ECHO-1.0` | `MIMIC-IV` | sibling_module | `1.0` | published_skeleton_and_public_scripts | local Layer 4 opening registry built pending owner review; ECHO-specific public opening policy not yet published | database-level local notes exist, but no reviewed-approved retained-variable family has been published yet | `0` | `docs/onboarding/MIMIC-IV-ECHO-1.0.md` |
| `AmsterdamUMCdb-1.0.2` | `AmsterdamUMCdb` | core_database | `1.0.2` | published_skeleton_and_public_scripts | database opening policy registry contract and validator path are published | pilot reviewed-approved local assets exist and public std-variable cards are published for shared variables | `58` | `docs/onboarding/AmsterdamUMCdb-1.0.2.md` |
| `SICdb-1.0.8` | `SICdb` | core_database | `1.0.8` | published_skeleton_initial_intake_only | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved SICdb retained-variable assets yet | `0` | `docs/onboarding/SICdb-1.0.8.md` |
| `NWICU-0.1.0` | `NWICU` | core_database | `0.1.0` | published_skeleton_initial_intake_only | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved NWICU retained-variable assets yet | `0` | `docs/onboarding/NWICU-0.1.0.md` |
| `eICU-CRD-2.0` | `eICU-CRD` | core_database | `2.0` | published_skeleton_initial_intake_only | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved eICU-CRD retained-variable assets yet | `0` | `docs/onboarding/eICU-CRD-2.0.md` |
| `Zigong-1.1` | `Zigong` | core_database | `1.1` | published_skeleton_initial_intake_only | local Layer 4 opening registry built pending owner review; public opening policy not yet published | no reviewed-approved Zigong retained-variable assets yet | `0` | `docs/onboarding/Zigong-1.1.md` |

## Public asset classes

| asset class | count | notes |
| --- | --- | --- |
| root files | `2` | repository-level public entry files |
| framework contracts | `22` | governing public contracts in `Framework_Guideline/` |
| core docs | `9` | matrix, inventory, review checklist, and other core public notes |
| standard-system MVP docs | `1530` | early machine-readable MVP drafts and support notes under `docs/standard_system_mvp/` |
| release docs | `2` | changelog and release-process support docs |
| release note docs | `1` | one release note per public release tag |
| public export support files | `1` | README for generated public export artifacts |
| public export docs | `4` | generated repository status and variable-coverage exports |
| onboarding support files | `4` | README and templates for onboarding layers |
| family playbooks | `2` | family-level governance docs |
| database playbooks | `3` | per-database onboarding docs |
| tutorials | `6` | public-safe walkthroughs |
| GitHub workflows | `1` | public CI/smoke workflows |
| public scripts | `35` | GitHub-safe Python scripts under `scripts/` |
| Layer 1 skeleton files | `42` | committed public Layer 1 skeleton contents across supported databases |
| std-variable card support files | `1` | shared README for public cards |
| public std-variable cards | `465` | variable-level public documentation cards |
| test support files | `2` | public-safe fixtures and repository test notes |

## Governed MVP highlights

| public asset | current role | release-safe status |
| --- | --- | --- |
| `docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md` | current class-1 approval closure | `listed` |
| `docs/standard_system_mvp/CLASS2_CURRENT_APPROVAL_CLOSURE.md` | current class-2 approval closure | `listed` |
| `docs/standard_system_mvp/CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md` | class-2 total closure review and MIMIC expansion decision | `listed` |
| `docs/standard_system_mvp/CLASS2_NEXT_SMALL_CANDIDATE_SELECTION.md` | class-2 next small MIMIC candidate selection | `listed` |
| `docs/standard_system_mvp/CLASS3_FIRST_MVP_SELECTION.md` | class-3 first MVP selection and execution checklist | `listed` |
| `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 invasive mechanical ventilation active approval | `listed` |
| `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md` | class-3 Amsterdam invasive mechanical ventilation active candidate review | `listed` |
| `docs/standard_system_mvp/STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam invasive mechanical ventilation active formal approval | `listed` |
| `docs/standard_system_mvp/AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md` | class-3 Amsterdam respiratory-support family source-audit closure | `listed` |
| `docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 noninvasive ventilation active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam noninvasive ventilation active formal approval | `listed` |
| `docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 high-flow nasal cannula active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md` | class-3 Amsterdam high-flow nasal cannula active blocked candidate review | `listed` |
| `docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 supplemental oxygen active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md` | class-3 Amsterdam supplemental oxygen active blocked candidate review | `listed` |
| `docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 tracheostomy status active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam tracheostomy status active formal approval | `listed` |
| `docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 vasopressor support active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam vasopressor support active formal approval | `listed` |
| `docs/standard_system_mvp/STD_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 RRT active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam RRT active formal approval | `listed` |
| `docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 CRRT-family active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_CRRT_FAMILY_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam CRRT-family active formal approval | `listed` |
| `docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md` | class-3 non-CRRT RRT active MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_NON_CRRT_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-3 Amsterdam non-CRRT RRT active formal approval | `listed` |
| `docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_FORMAL_APPROVAL_REVIEW.md` | class-5 RRT exact modality episode MIMIC formal approval | `listed` |
| `docs/standard_system_mvp/STD_RRT_MODALITY_EPISODE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-5 Amsterdam RRT exact modality episode formal approval | `listed` |
| `docs/standard_system_mvp/STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md` | class-2 duration-summary approval | `listed` |
| `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md` | class-2 MIMIC hospital-duration approval | `listed` |
| `docs/standard_system_mvp/STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md` | class-2 MIMIC next-hospital-admission duration approval | `listed` |
| `docs/standard_system_mvp/AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md` | Amsterdam hospital-admission bridge feasibility review | `listed` |
| `docs/standard_system_mvp/AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` | Amsterdam next ICU/MCU local-admission duration candidate review | `listed` |
| `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-2 Amsterdam next ICU/MCU local-admission duration formal approval | `listed` |
| `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-2 Amsterdam next ICU admission same-name duration formal approval | `listed` |
| `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md` | class-2 Amsterdam hospital-duration candidate boundary review | `listed` |
| `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md` | class-2 BMI admission-baseline candidate review | `listed` |
| `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md` | class-2 BMI ICU-baseline candidate review | `listed` |
| `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md` | class-2 BMI admission-baseline formal approval | `listed` |
| `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md` | class-2 BMI ICU-baseline formal approval | `listed` |
| `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md` | class-2 exact baseline-snapshot approval | `listed` |
| `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md` | class-2 MIMIC ICU-baseline exact-weight approval | `listed` |
| `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md` | class-2 grouped/proxy baseline approval | `listed` |
| `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md` | class-2 window-summary approval | `listed` |
| `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md` | class-2 Amsterdam window-summary candidate review | `listed` |
| `docs/standard_system_mvp/STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | class-2 Amsterdam window-summary formal approval | `listed` |
| `docs/standard_system_mvp/STD_ICU_URINE_OUTPUT_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` | Amsterdam upstream urine-output event approval | `listed` |
| `docs/standard_system_mvp/AMSTERDAM_GOVERNED_RESULTS_DISTRIBUTION_APPROVAL_REVIEW.md` | Amsterdam governed result-distribution approval across current scoped variables | `listed` |
| `docs/standard_system_mvp/std_icu_urine_output_event/variable_spec.json` | upstream urine-output event variable spec | `listed` |
| `docs/standard_system_mvp/std_icu_urine_output_event/mapping_spec_amsterdamumcdb_1_0_2.json` | upstream urine-output event Amsterdam mapping spec | `listed` |
| `docs/standard_system_mvp/std_first_day_urine_output_summary/variable_spec.json` | window-summary variable spec | `listed` |
| `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_mimic_iv_3_1.json` | window-summary MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_first_day_urine_output_summary/mapping_spec_amsterdamumcdb_1_0_2.json` | window-summary Amsterdam mapping spec | `listed` |
| `docs/standard_system_mvp/std_weight_icu_baseline/variable_spec.json` | ICU-baseline exact-weight variable spec | `listed` |
| `docs/standard_system_mvp/std_weight_icu_baseline/mapping_spec_mimic_iv_3_1.json` | ICU-baseline exact-weight MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_bmi_admission_baseline/variable_spec.json` | BMI admission-baseline variable spec | `listed` |
| `docs/standard_system_mvp/std_bmi_admission_baseline/mapping_spec_mimic_iv_3_1.json` | BMI admission-baseline MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_bmi_icu_baseline/variable_spec.json` | BMI ICU-baseline variable spec | `listed` |
| `docs/standard_system_mvp/std_bmi_icu_baseline/mapping_spec_mimic_iv_3_1.json` | BMI ICU-baseline MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_hospital_los_days/variable_spec.json` | hospital-duration variable spec | `listed` |
| `docs/standard_system_mvp/std_hospital_los_days/mapping_spec_mimic_iv_3_1.json` | hospital-duration MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/variable_spec.json` | invasive mechanical ventilation active variable spec | `listed` |
| `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_mimic_iv_3_1.json` | invasive mechanical ventilation active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json` | invasive mechanical ventilation active Amsterdam approved mapping spec | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/variable_spec.json` | noninvasive ventilation active variable spec | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_mimic_iv_3_1.json` | noninvasive ventilation active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_amsterdamumcdb_1_0_2.json` | noninvasive ventilation active Amsterdam approved mapping spec | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | noninvasive ventilation active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | noninvasive ventilation active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | noninvasive ventilation active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | noninvasive ventilation active Amsterdam approved validation report | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | noninvasive ventilation active Amsterdam approved execution manifest | `listed` |
| `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | noninvasive ventilation active Amsterdam approved rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/variable_spec.json` | high-flow nasal cannula active variable spec | `listed` |
| `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/mapping_spec_mimic_iv_3_1.json` | high-flow nasal cannula active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | high-flow nasal cannula active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | high-flow nasal cannula active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | high-flow nasal cannula active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_supplemental_oxygen_active/variable_spec.json` | supplemental oxygen active variable spec | `listed` |
| `docs/standard_system_mvp/std_supplemental_oxygen_active/mapping_spec_mimic_iv_3_1.json` | supplemental oxygen active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_supplemental_oxygen_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | supplemental oxygen active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_supplemental_oxygen_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | supplemental oxygen active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_supplemental_oxygen_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | supplemental oxygen active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/variable_spec.json` | tracheostomy status active variable spec | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_mimic_iv_3_1.json` | tracheostomy status active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/mapping_spec_amsterdamumcdb_1_0_2.json` | tracheostomy status active Amsterdam approved mapping spec | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | tracheostomy status active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | tracheostomy status active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | tracheostomy status active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | tracheostomy status active Amsterdam approved validation report | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | tracheostomy status active Amsterdam approved execution manifest | `listed` |
| `docs/standard_system_mvp/std_tracheostomy_status_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | tracheostomy status active Amsterdam approved rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/variable_spec.json` | vasopressor support active variable spec | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_mimic_iv_3_1.json` | vasopressor support active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/mapping_spec_amsterdamumcdb_1_0_2.json` | vasopressor support active Amsterdam approved mapping spec | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | vasopressor support active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | vasopressor support active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | vasopressor support active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | vasopressor support active Amsterdam approved validation report | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | vasopressor support active Amsterdam approved execution manifest | `listed` |
| `docs/standard_system_mvp/std_vasopressor_support_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | vasopressor support active Amsterdam approved rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_rrt_active/variable_spec.json` | RRT active variable spec | `listed` |
| `docs/standard_system_mvp/std_rrt_active/mapping_spec_mimic_iv_3_1.json` | RRT active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json` | RRT active Amsterdam approved mapping spec | `listed` |
| `docs/standard_system_mvp/std_rrt_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | RRT active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_rrt_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | RRT active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_rrt_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | RRT active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_rrt_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | RRT active Amsterdam approved validation report | `listed` |
| `docs/standard_system_mvp/std_rrt_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | RRT active Amsterdam approved execution manifest | `listed` |
| `docs/standard_system_mvp/std_rrt_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | RRT active Amsterdam approved rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/variable_spec.json` | CRRT-family active variable spec | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/mapping_spec_mimic_iv_3_1.json` | CRRT-family active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/mapping_spec_amsterdamumcdb_1_0_2.json` | CRRT-family active Amsterdam mapping spec | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | CRRT-family active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | CRRT-family active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | CRRT-family active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | CRRT-family active Amsterdam validation report | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | CRRT-family active Amsterdam execution manifest | `listed` |
| `docs/standard_system_mvp/std_crrt_family_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | CRRT-family active Amsterdam rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/variable_spec.json` | non-CRRT RRT active variable spec | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/mapping_spec_mimic_iv_3_1.json` | non-CRRT RRT active MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/mapping_spec_amsterdamumcdb_1_0_2.json` | non-CRRT RRT active Amsterdam mapping spec | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | non-CRRT RRT active MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | non-CRRT RRT active MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | non-CRRT RRT active MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | non-CRRT RRT active Amsterdam validation report | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | non-CRRT RRT active Amsterdam execution manifest | `listed` |
| `docs/standard_system_mvp/std_non_crrt_rrt_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | non-CRRT RRT active Amsterdam rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/variable_spec.json` | RRT exact modality episode variable spec | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/mapping_spec_mimic_iv_3_1.json` | RRT exact modality episode MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/mapping_spec_amsterdamumcdb_1_0_2.json` | RRT exact modality episode Amsterdam mapping spec | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/runtime/mimic_iv_3_1_first_real_execution/validation_report.json` | RRT exact modality episode MIMIC validation report | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/runtime/mimic_iv_3_1_first_real_execution/manifest.json` | RRT exact modality episode MIMIC execution manifest | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json` | RRT exact modality episode MIMIC rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | RRT exact modality episode Amsterdam validation report | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | RRT exact modality episode Amsterdam execution manifest | `listed` |
| `docs/standard_system_mvp/std_rrt_modality_episode/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | RRT exact modality episode Amsterdam rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/variable_spec.json` | Amsterdam next ICU/MCU admission duration variable spec | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/mapping_spec_amsterdamumcdb_1_0_2.json` | Amsterdam next ICU/MCU admission duration mapping spec | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | Amsterdam next ICU/MCU admission duration validation report | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | Amsterdam next ICU/MCU admission duration execution manifest | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | Amsterdam next ICU/MCU admission duration rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_admission/variable_spec.json` | next ICU admission duration variable spec | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_mimic_iv_3_1.json` | next ICU admission duration MIMIC mapping spec | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_amsterdamumcdb_1_0_2.json` | next ICU admission duration Amsterdam same-name mapping spec | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | Amsterdam next ICU admission duration validation report | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | Amsterdam next ICU admission duration execution manifest | `listed` |
| `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | Amsterdam next ICU admission duration rerun reproducibility report | `listed` |
| `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json` | invasive mechanical ventilation active Amsterdam approved validation report | `listed` |
| `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json` | invasive mechanical ventilation active Amsterdam approved execution manifest | `listed` |
| `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json` | invasive mechanical ventilation active Amsterdam approved rerun reproducibility report | `listed` |
| `docs/std_variable_cards/std_invasive_mechanical_ventilation_active.md` | public invasive mechanical ventilation active cross-database card | `listed` |
| `docs/std_variable_cards/std_noninvasive_ventilation_active.md` | public noninvasive ventilation active card | `listed` |
| `docs/std_variable_cards/std_high_flow_nasal_cannula_active.md` | public high-flow nasal cannula active card | `listed` |
| `docs/std_variable_cards/std_supplemental_oxygen_active.md` | public supplemental oxygen active card | `listed` |
| `docs/std_variable_cards/std_tracheostomy_status_active.md` | public tracheostomy status active card | `listed` |
| `docs/std_variable_cards/std_vasopressor_support_active.md` | public vasopressor support active cross-database card | `listed` |
| `docs/std_variable_cards/std_rrt_active.md` | public RRT active cross-database card | `listed` |
| `docs/std_variable_cards/std_crrt_family_active.md` | public CRRT-family active card | `listed` |
| `docs/std_variable_cards/std_non_crrt_rrt_active.md` | public non-CRRT RRT active card | `listed` |
| `docs/std_variable_cards/std_rrt_modality_episode.md` | public RRT exact modality episode card | `listed` |
| `docs/std_variable_cards/std_first_day_urine_output_summary.md` | public variable card | `listed` |
| `docs/std_variable_cards/std_weight_icu_baseline.md` | public ICU-baseline exact-weight card | `listed` |
| `docs/std_variable_cards/std_hospital_los_days.md` | public hospital-duration card | `listed` |
| `docs/std_variable_cards/std_bmi_admission_baseline.md` | public BMI admission-baseline card | `listed` |
| `docs/std_variable_cards/std_bmi_icu_baseline.md` | public BMI ICU-baseline card | `listed` |
| `docs/std_variable_cards/std_days_to_next_icu_mcu_admission.md` | public Amsterdam next ICU/MCU admission duration card | `listed` |
| `docs/std_variable_cards/std_days_to_next_icu_admission.md` | public next ICU admission duration cross-database card | `listed` |

## Key entrypoints

- `python scripts/public_workflow.py status`
- `python scripts/public_workflow.py status --family-id MIMIC-IV`
- `python scripts/public_workflow.py build-layer1 ...`
- `python scripts/public_workflow.py validate-registry ...`
- `python scripts/public_workflow.py check-public-repository`
- `python scripts/public_workflow.py prepare-release --dry-run`
- `python scripts/public_workflow.py scaffold-public-database --help`
- `python scripts/public_workflow.py export-public-artifacts --artifact release-safe-manifest`
- `python scripts/public_workflow.py export-public-artifacts --artifact public-inventory`
- `python scripts/public_workflow.py export-public-artifacts --artifact release-governance`
- `python scripts/public_workflow.py export-public-artifacts --artifact database-variable-coverage`
- `python scripts/public_workflow.py export-public-artifacts --artifact family-variable-coverage`
- `python scripts/public_workflow.py export-public-artifacts --artifact variable-coverage-summary`

## Full machine-readable inventory

For the complete file-level release-safe list, use [`docs/release_safe_manifest.json`](release_safe_manifest.json).

For public variable-coverage exports, use the generated files under [`docs/public_exports`](public_exports/README.md).
