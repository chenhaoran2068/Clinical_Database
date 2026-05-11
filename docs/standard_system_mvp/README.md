# Standard-System MVP Drafts

This directory is the public GitHub-safe landing zone for the first machine-readable standard-system MVP artifacts.

These files do not replace the sibling local-work evidence under `Methods/Clinical_Database/local_work/...` outside this public repository.
They are the public machine-readable layer that begins to lock variable identity, source scope, representation, governed execution expectations, and post-run validation expectations in reusable form.

## Interpretation Rule

- files here are governed MVP drafts, not the final universal standard schema
- sibling local-work evidence paths are written as workspace-relative paths such as `Methods/Clinical_Database/local_work/...`
- formal patient-level outputs should not be treated as standard-system outputs until a governed execution path, runtime evidence, and rerun gate also exist

## Reusable Class Skeleton

The first reusable public class skeleton now lives under:

- `variable_classes/event_level_numeric_primary_source/`

The second reusable public class definition now also lives under:

- `variable_classes/baseline_summary_window_numeric/`

The third reusable public class definition now also lives under:

- `variable_classes/binary_state_episode/`

The fourth reusable public class definition now also lives under:

- `variable_classes/treatment_device_io_event_stream/`

The opening fifth reusable public class definition now also lives under:

- `variable_classes/episode_interval_bridge/`

These classes are currently backed by:

- `Framework_Guideline/StandardVariableClass_EventLevelNumericPrimarySource_Contract.md`
- `Framework_Guideline/StandardVariableClass_BaselineSummaryWindowNumeric_Contract.md`
- `Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md`
- `Framework_Guideline/StandardVariableClass_TreatmentDeviceIOEventStream_Contract.md`
- `Framework_Guideline/StandardVariableClass_EpisodeIntervalBridge_Contract.md`
- `Framework_Guideline/StandardSystem_RuntimeEvidence_Contract.md`
- `scripts/standard_system_mvp_engine.py`
- `scripts/validate_standard_system_runtime.py`
- `scripts/validate_standard_system_reproducibility.py`
- `VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`

Current phase interpretation:

- class 1 has governed execute/rerun closure
- class 2 has its first dual-database governed duration-summary closure through `std_icu_los_days`
- class 2 also now has a MIMIC-only hospital-admission duration-summary closure through `std_hospital_los_days`
- class 2 also now has its first MIMIC-only governed baseline-snapshot closure through `std_weight_admission_baseline`
- class 2 also now has a MIMIC-only ICU-baseline exact-weight snapshot closure through `std_weight_icu_baseline`
- class 2 also now has MIMIC-only derived BMI baseline-snapshot closures through `std_bmi_admission_baseline` and `std_bmi_icu_baseline`
- class 2 also now has an Amsterdam-only grouped/proxy ICU-baseline weight closure through `std_weight_icu_baseline_grouped_proxy`, explicitly split away from `std_weight_admission_baseline`
- class 2 also now has its first dual-database governed window-summary closure through `std_first_day_urine_output_summary`
- class 2 next small MIMIC candidate selection has now been promoted into governed approval through `std_days_to_next_hospital_admission`, a post-discharge observed follow-up duration summary
- the Amsterdam hospital-admission bridge feasibility review now records that the current Amsterdam opening layer does not prove hospital-admission/discharge boundaries, so Amsterdam remains blocked for same-name hospital-level duration and next-hospital-admission variables
- the Amsterdam next ICU/MCU local-admission duration candidate review records the safe post-bridge route: ICU-semantic rows support same-name `std_days_to_next_icu_admission`, while MC-inclusive ICU/MCU timing requires a split identity such as `std_days_to_next_icu_mcu_admission`
- that split Amsterdam ICU/MCU route has now been promoted into governed approval through `std_days_to_next_icu_mcu_admission`, with execute/rerun evidence and formal approval while preserving the hospital-level and ICU-only boundaries
- the narrower Amsterdam ICU-only route has now also been promoted into same-name governed approval through `std_days_to_next_icu_admission`, with MC-only rows excluded and the MC-inclusive output kept under `std_days_to_next_icu_mcu_admission`
- Amsterdam now has an approved governed upstream urine-output event layer through `std_icu_urine_output_event`, and that upstream layer has been used to close the Amsterdam `std_first_day_urine_output_summary` summary build
- the current Amsterdam governed result distributions have now passed a cross-variable distribution/plausibility approval review across `std_heart_rate`, `std_icu_los_days`, `std_weight_icu_baseline_grouped_proxy`, `std_icu_urine_output_event`, and `std_first_day_urine_output_summary`
- class 3 now has its first governed binary-state episode closure through `std_invasive_mechanical_ventilation_active` on `MIMIC-IV-3.1`
- Amsterdam same-name feasibility for `std_invasive_mechanical_ventilation_active` has now been promoted from candidate review to reviewed-approved same-name status, with `processitems` itemid `9328` / `Beademen` retained as the narrow approved source and NIV/CPAP adjacent process states excluded from the same-name output
- class 3 respiratory-support-family expansion now closes the base single-status MIMIC respiratory set through governed `MIMIC-IV-3.1` approval of `std_noninvasive_ventilation_active`, `std_high_flow_nasal_cannula_active`, `std_supplemental_oxygen_active`, and `std_tracheostomy_status_active`, each keeping adjacent support states separate
- Amsterdam respiratory-support-family third-layer audit is now closed under current evidence: `std_noninvasive_ventilation_active` and `std_tracheostomy_status_active` are reviewed-approved same-name assets, while `std_high_flow_nasal_cannula_active` and `std_supplemental_oxygen_active` remain explicitly blocked rather than forced into unsupported Class 3 active episodes
- class 3 now also has its first non-respiratory treatment-support active-state closure through `std_vasopressor_support_active`, with governed MIMIC and Amsterdam same-name approval while keeping agent-specific episode, dose, shock, and free-day semantics separate
- class 3 now also has renal-support active-state closure through `std_rrt_active`, with governed MIMIC and Amsterdam same-name approval while keeping CRRT-only, non-CRRT-only, exact modality, access-line, fluid-removal, summary, and phenotype semantics separate
- the MIMIC and Amsterdam RRT child layers are now split and governed: `std_crrt_family_active` and `std_non_crrt_rrt_active` are Class 3 family active flags, while `std_rrt_modality_episode` opens the Class 5 `episode_interval_bridge` skeleton for exact modality episodes with parent links; Amsterdam non-CRRT approval is source-bounded to Hemodialyse active intervals
- class 4 is now opened through `treatment_device_io_event_stream`, with governed MIMIC approval of `std_rrt_fluid_removal_event` as a source-faithful RRT fluid-removal event stream; Amsterdam has a reproducible bounded candidate execution for explicit `CVVH Onttrokken` and `Hemodialyse onttrekken` volume rows, but remains not approved because rate settings, cumulative counters, access lines, active flags, modality episodes, and parent-link gaps must stay outside same-name approval

## Closed Governed MVP Instances

Current governed variable directories:

- `std_heart_rate/`
- `std_icu_los_days/`
- `std_hospital_los_days/`
- `std_glucose/`
- `std_respiratory_rate/`
- `std_sodium/`
- `std_potassium/`
- `std_creatinine/`
- `std_spo2/`
- `std_temp/`
- `std_sbp/`
- `std_dbp/`
- `std_map/`
- `std_weight_admission_baseline/`
- `std_weight_icu_baseline/`
- `std_bmi_admission_baseline/`
- `std_bmi_icu_baseline/`
- `std_weight_icu_baseline_grouped_proxy/`
- `std_first_day_urine_output_summary/`
- `std_days_to_next_hospital_admission/`
- `std_days_to_next_icu_admission/`
- `std_days_to_next_icu_mcu_admission/`
- `std_icu_urine_output_event/`
- `std_invasive_mechanical_ventilation_active/`
- `std_noninvasive_ventilation_active/`
- `std_high_flow_nasal_cannula_active/`
- `std_supplemental_oxygen_active/`
- `std_tracheostomy_status_active/`
- `std_vasopressor_support_active/`
- `std_rrt_active/`
- `std_crrt_family_active/`
- `std_non_crrt_rrt_active/`
- `std_rrt_modality_episode/`
- `std_rrt_fluid_removal_event/`

The historical first-batch content-approval summary is:

- `CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`

The current additional class-1 approval notes are:

- `STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`
- `CLASS1_CURRENT_APPROVAL_CLOSURE.md`

The current class-2 Phase-1 selection note is:

- `CLASS2_FIRST_MVP_SELECTION.md`

The current class-2 approval closure note is:

- `CLASS2_CURRENT_APPROVAL_CLOSURE.md`

The current class-2 total review and MIMIC expansion decision is:

- `CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md`

The current class-2 next small candidate selection note is:

- `CLASS2_NEXT_SMALL_CANDIDATE_SELECTION.md`

The current class-2 post-discharge observed follow-up duration approval note is:

- `STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md`

The current Amsterdam hospital-admission bridge feasibility review is:

- `AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md`

The current Amsterdam next ICU/MCU local-admission duration candidate review is:

- `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md`

The current Amsterdam next ICU/MCU local-admission duration approval note is:

- `STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

The current Amsterdam ICU-only same-name next-admission duration approval note is:

- `STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

The current class-2 formal approval note is:

- `STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`

The current MIMIC hospital-duration approval note is:

- `STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`

The current BMI derived-baseline candidate and formal approval reviews are:

- `STD_BMI_ADMISSION_BASELINE_CANDIDATE_REVIEW.md`
- `STD_BMI_ICU_BASELINE_CANDIDATE_REVIEW.md`
- `STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
- `STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`

The current MIMIC class-2 baseline-snapshot approval note is:

- `STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`

The current MIMIC ICU-baseline exact-weight approval note is:

- `STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`

The current Amsterdam same-name candidate review for that baseline-snapshot variable is:

- `STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`

The current Amsterdam grouped/proxy split-variable approval note is:

- `STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`

The current MIMIC window-summary approval note is:

- `STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`

The current Amsterdam same-name candidate review for that window-summary variable is:

- `STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md`

The current Amsterdam same-name formal approval note for that window-summary variable is:

- `STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

The current Amsterdam upstream urine-output event approval note is:

- `STD_ICU_URINE_OUTPUT_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

The current Amsterdam governed results distribution approval note is:

- `AMSTERDAM_GOVERNED_RESULTS_DISTRIBUTION_APPROVAL_REVIEW.md`

The current Class 3 first-MVP selection and approval notes are:

- `CLASS3_FIRST_MVP_SELECTION.md`
- `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md`
- `STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_NONINVASIVE_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_SUPPLEMENTAL_OXYGEN_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
- `STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_TRACHEOSTOMY_STATUS_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `STD_VASOPRESSOR_SUPPORT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `STD_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `STD_CRRT_FAMILY_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_CRRT_FAMILY_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `STD_NON_CRRT_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- `STD_NON_CRRT_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
- `STD_RRT_MODALITY_EPISODE_FORMAL_APPROVAL_REVIEW.md`
- `STD_RRT_MODALITY_EPISODE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

The current Class 4 first-MVP approval and candidate notes are:

- `STD_RRT_FLUID_REMOVAL_EVENT_FEASIBILITY_REVIEW.md`
- `STD_RRT_FLUID_REMOVAL_EVENT_FORMAL_APPROVAL_REVIEW.md`
- `STD_RRT_FLUID_REMOVAL_EVENT_AMSTERDAM_BOUNDED_CANDIDATE_REVIEW.md`

For the current MIMIC first-wave event-level numeric batch, the following variables now each contain:

- `variable_spec.json`
- `mapping_spec_mimic_iv_3_1.json`
- `execution.py`
- `runtime/mimic_iv_3_1_first_real_execution/validation_report.json`
- `runtime/mimic_iv_3_1_first_real_execution/manifest.json`
- `runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

That batch currently includes:

- `std_heart_rate`
- `std_glucose`
- `std_respiratory_rate`
- `std_sodium`
- `std_potassium`
- `std_creatinine`
- `std_spo2`
- `std_temp`
- `std_sbp`
- `std_dbp`
- `std_map`

Important boundary:

- the historical first-batch note still records the first reviewed 10-variable milestone
- `std_heart_rate` is now also formally closed into the current broader class-1 approval surface rather than remaining only the prototype predecessor outside approval

`std_heart_rate/` additionally includes:

- `mapping_spec_amsterdamumcdb_1_0_2.json`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- a governed rerun reproducibility report on `AmsterdamUMCdb-1.0.2`

`std_icu_urine_output_event/` includes:

- `mapping_spec_amsterdamumcdb_1_0_2.json`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal Amsterdam approval review note

`std_rrt_fluid_removal_event/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note
- an Amsterdam bounded-candidate mapping and reproducible candidate runtime evidence
- an explicit Amsterdam bounded-candidate review keeping rate settings, cumulative counters, access lines, active flags, modality episodes, and parent-link gaps outside same-name approval

`std_first_day_urine_output_summary/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- formal MIMIC and Amsterdam approval review notes

`std_weight_icu_baseline/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note

`std_hospital_los_days/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note
- an Amsterdam candidate boundary review confirming that the current Amsterdam evidence belongs to ICU or ICU/MC stay-duration semantics rather than hospital-admission LOS

`std_days_to_next_hospital_admission/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note
- an explicit Amsterdam boundary note in the formal review requiring a hospital-admission encounter bridge before same-name approval

`std_days_to_next_icu_admission/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json`
- governed validate-only compatibility for `MIMIC-IV-3.1` under the public entrypoint
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal Amsterdam same-name approval review note
- an explicit ICU-only boundary keeping MC-only Amsterdam rows under `std_days_to_next_icu_mcu_admission`

`std_days_to_next_icu_mcu_admission/` includes:

- `mapping_spec_amsterdamumcdb_1_0_2.json`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal Amsterdam approval review note
- an explicit split-identity boundary keeping this MC-inclusive output separate from both hospital-level next-admission timing and ICU-only `std_days_to_next_icu_admission`

`std_bmi_admission_baseline/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note

`std_bmi_icu_baseline/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note

`std_invasive_mechanical_ventilation_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam same-name mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- frozen candidate governed runtime evidence on `AmsterdamUMCdb-1.0.2` preserved as pre-approval audit history
- a formal MIMIC approval review note
- an Amsterdam same-name candidate review that identifies `processitems` itemid `9328` / `Beademen` as the source-audit target and records the accepted conservative first-pass policy
- an Amsterdam formal approval review that approves `9328 / Beademen` under the documented NIV/CPAP exclusion and context-flag rules

`std_noninvasive_ventilation_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam same-name NIV/CPAP mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- an explicit adjacent-state boundary keeping IMV, HFNC, supplemental oxygen, and tracheostomy out of the same-name NIV output

`std_high_flow_nasal_cannula_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note
- an Amsterdam candidate review that blocks same-name approval because no narrow HFNC, high-flow nasal cannula, or Optiflow source was found
- an explicit adjacent-state boundary keeping IMV, NIV, supplemental oxygen, and tracheostomy out of the same-name HFNC output

`std_supplemental_oxygen_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- a formal MIMIC approval review note
- an Amsterdam candidate review that blocks same-name Class 3 episode approval until oxygen route/device/flow evidence has a governed intervalization rule
- an explicit adjacent-state boundary keeping IMV, NIV, HFNC, and tracheostomy out of the same-name supplemental-oxygen output

`std_tracheostomy_status_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam same-name tracheostomy-status mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- an explicit adjacent-state boundary keeping tracheostomy status separate from IMV, NIV, HFNC, and supplemental oxygen

`std_vasopressor_support_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam same-name mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- an explicit boundary keeping vasopressor support active separate from pure inotrope support, agent-specific episodes, norepinephrine-equivalent dose, shock phenotype, and vasopressor-free-day outcomes

`std_rrt_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam same-name mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- an explicit boundary keeping any-RRT active state separate from CRRT-only, non-CRRT-only, exact modality, access-line, fluid-removal, first-day summary, AKI/KDIGO, and renal SOFA semantics

`std_crrt_family_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam same-name CVVH mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- an explicit child-layer boundary keeping umbrella any-RRT active, non-CRRT active, exact modality, fluid-removal, first-day summary, free-day, AKI/KDIGO, and renal SOFA semantics separate

`std_non_crrt_rrt_active/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved source-bounded Amsterdam Hemodialyse mapping
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- an explicit Amsterdam source-coverage caution that peritoneal active intervals are not proven by the opening processitems evidence
- an explicit child-layer boundary keeping umbrella any-RRT active, CRRT-family active, exact modality, fluid-removal, first-day summary, free-day, AKI/KDIGO, and renal SOFA semantics separate

`std_rrt_modality_episode/` includes:

- `mapping_spec_mimic_iv_3_1.json`
- `mapping_spec_amsterdamumcdb_1_0_2.json` as a reviewed-approved Amsterdam exact-label mapping for `CVVH` and `IHD`
- governed execute-mode runtime evidence on `MIMIC-IV-3.1`
- governed rerun reproducibility evidence on `MIMIC-IV-3.1`
- governed execute-mode runtime evidence on `AmsterdamUMCdb-1.0.2`
- governed rerun reproducibility evidence on `AmsterdamUMCdb-1.0.2`
- a formal MIMIC approval review note
- a formal Amsterdam approval review note
- the opening Class 5 `episode_interval_bridge` skeleton, because exact modality labels and parent links are not a simple Class 3 active flag

The current BMI derived-baseline reviews mean:

- `std_bmi_admission_baseline` and `std_bmi_icu_baseline` have repaired public-card review-date metadata
- both are now governed-approved for `MIMIC-IV-3.1`
- neither is cross-database approved yet
- both remain derived variables dependent on approved upstream weight and height assets

## Current Closure Meaning

What is now true in public form:

- the first reusable standard-variable class skeleton exists
- the shared governed engine exists
- the post-run runtime validator exists
- the rerun reproducibility validator exists
- the first large MIMIC class-1 batch is closed on real governed execution rather than only static specs
- the current approved class-1 surface now includes `std_heart_rate` as well, producing an 11-variable approved `MIMIC-IV-3.1` closure
- `std_heart_rate` also shows governed execute/rerun closure on `AmsterdamUMCdb-1.0.2`
- `std_icu_los_days` now shows the first closed class-2 governed dual-database MVP surface on `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- `std_hospital_los_days` now shows a governed MIMIC hospital-admission duration-summary closure with execute/rerun evidence
- Amsterdam has been explicitly reviewed and not promoted into same-name `std_hospital_los_days`; the current Amsterdam duration evidence remains under ICU/stay-duration semantics
- `std_weight_admission_baseline` now shows a governed MIMIC class-2 baseline-snapshot closure with execute/rerun evidence
- `std_weight_icu_baseline` now shows a governed MIMIC class-2 ICU-baseline exact-weight closure with execute/rerun evidence
- `std_bmi_admission_baseline` and `std_bmi_icu_baseline` now show governed MIMIC class-2 derived-baseline BMI closures with execute/rerun evidence
- the current Amsterdam candidate for `std_weight_admission_baseline` has been reviewed and intentionally not promoted into the same-name public mapping because it is a grouped/proxy ICU-MCU admission-weight asset rather than the current hospital-admission event-baseline contract
- that Amsterdam grouped/proxy asset is instead approved under the separate `std_weight_icu_baseline_grouped_proxy` identity, with its own public spec, Amsterdam mapping spec, governed execute/rerun evidence, reproducibility report, public card, and formal approval review
- `std_first_day_urine_output_summary` now shows the first governed dual-database class-2 window-summary closure, with official MIMIC first-day urine-output reference matching plus Amsterdam summary-specific execute/rerun evidence built from the approved Amsterdam event layer
- the Amsterdam upstream `std_icu_urine_output_event` layer is now approved with governed execute/rerun evidence
- the Amsterdam candidate for `std_first_day_urine_output_summary` has now been promoted to reviewed-approved same-name status after summary-specific mapping, execution, validation, and rerun evidence were built from the approved event stream
- the current five-variable Amsterdam governed result set has now passed distribution-level approval against internal quality evidence, Amsterdam official denominator/LOS references, and public clinical plausibility checks
- `std_invasive_mechanical_ventilation_active` now shows the first governed Class 3 `binary_state_episode` closure, proving the system can handle positive-only binary active-state episodes in addition to numeric event and numeric summary variables
- Amsterdam same-name handling for `std_invasive_mechanical_ventilation_active` is now reviewed-approved after source-audit work, governed execute/rerun evidence, reproducibility validation, and final adjacent-state boundary review
- `std_noninvasive_ventilation_active` now shows the first governed Class 3 respiratory-support-family expansion after invasive ventilation, confirming that the same positive-only episode skeleton generalizes to an adjacent official ventilation status
- `std_high_flow_nasal_cannula_active`, `std_supplemental_oxygen_active`, and `std_tracheostomy_status_active` now close the remaining direct MIMIC official ventilation-status siblings under the same Class 3 positive-only episode skeleton
- `std_vasopressor_support_active` now shows that the same Class 3 positive-only episode skeleton can handle medication-derived treatment-support active states on both MIMIC and Amsterdam without collapsing into agent-specific, dose, or phenotype variables
- `std_rrt_active` now shows that the same Class 3 positive-only episode skeleton can handle renal-support active states on both MIMIC and Amsterdam without collapsing into modality-specific, access-line, fluid-removal, summary, or phenotype variables
- `std_crrt_family_active` and `std_non_crrt_rrt_active` now show the safe RRT child-family split under Class 3 on both MIMIC and Amsterdam, while `std_rrt_modality_episode` opens the first governed Class 5 episode/modality bridge with exact labels and parent links on both databases
- `CLASS2_CURRENT_APPROVAL_CLOSURE.md` records that Class 2 is approved as a bounded current-stage governed class with current representatives for `duration_summary`, `baseline_snapshot`, and `window_summary`, while full class-2 industrialization is still not claimed
- `CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md` records that `std_weight_icu_baseline`, `std_hospital_los_days`, `std_bmi_admission_baseline`, and `std_bmi_icu_baseline` have now completed the controlled MIMIC-IV-3.1 Class 2 expansion path after total closure review
- `CLASS2_NEXT_SMALL_CANDIDATE_SELECTION.md` records why `std_days_to_next_hospital_admission` was selected as the next small Class 2 candidate, and `STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md` records its subsequent governed MIMIC approval
- `AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md` records that Amsterdam's current opening layer does not expose a governed hospital-admission bridge, so `std_hospital_los_days` and `std_days_to_next_hospital_admission` remain MIMIC-only under current evidence
- `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` records that Amsterdam can support next local critical-care admission timing, but MC-inclusive ICU/MCU timing needs a split identity rather than same-name `std_days_to_next_icu_admission`
- `STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` records that the split Amsterdam `std_days_to_next_icu_mcu_admission` route is now reviewed-approved with governed execute/rerun evidence
- `STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md` records that the narrower Amsterdam ICU-only same-name `std_days_to_next_icu_admission` route is now reviewed-approved with governed execute/rerun evidence and explicit MC-only exclusion

In other words:

- the repository is no longer showing only one-off `std_heart_rate` machinery
- it now shows a reusable event-level numeric MVP pattern closed across laboratory, vital-sign, oxygen-saturation, temperature, and blood-pressure-family examples
- it also shows a reusable baseline/summary/window numeric pattern across duration, baseline snapshot, grouped/proxy baseline, and first-day window-summary examples

## Runtime Evidence Expectation

Every governed runtime directory here is expected to pass:

```powershell
python scripts/validate_standard_system_runtime.py --runtime-dir "docs\standard_system_mvp\<variable_id>\runtime\<runtime_name>"
python scripts/validate_standard_system_reproducibility.py --report-path "docs\standard_system_mvp\<variable_id>\runtime\<rerun_name>\reproducibility_report.json"
```

## Practical Reading Order

For the fastest orientation, read in this order:

1. `VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`
2. `variable_classes/event_level_numeric_primary_source/README.md`
3. `variable_classes/baseline_summary_window_numeric/README.md`
4. `variable_classes/binary_state_episode/README.md`
5. `CLASS2_FIRST_MVP_SELECTION.md`
6. `CLASS2_CURRENT_APPROVAL_CLOSURE.md`
7. `CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md`
8. `CLASS2_NEXT_SMALL_CANDIDATE_SELECTION.md`
9. `STD_DAYS_TO_NEXT_HOSPITAL_ADMISSION_FORMAL_APPROVAL_REVIEW.md`
10. `AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md`
11. `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md`
12. `STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
13. `STD_DAYS_TO_NEXT_ICU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
14. `CLASS3_FIRST_MVP_SELECTION.md`
15. `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
16. `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
17. `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
18. `AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md`
19. `STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
20. `STD_NONINVASIVE_VENTILATION_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
21. `STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
22. `STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
23. `STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
24. `STD_SUPPLEMENTAL_OXYGEN_ACTIVE_AMSTERDAM_CANDIDATE_REVIEW.md`
25. `STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
26. `STD_TRACHEOSTOMY_STATUS_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
27. `STD_VASOPRESSOR_SUPPORT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
28. `STD_VASOPRESSOR_SUPPORT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
29. `STD_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
30. `STD_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
31. `STD_CRRT_FAMILY_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
32. `STD_CRRT_FAMILY_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
33. `STD_NON_CRRT_RRT_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
34. `STD_NON_CRRT_RRT_ACTIVE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
35. `STD_RRT_MODALITY_EPISODE_FORMAL_APPROVAL_REVIEW.md`
36. `STD_RRT_MODALITY_EPISODE_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
37. `STD_ICU_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
35. `STD_HOSPITAL_LOS_DAYS_FORMAL_APPROVAL_REVIEW.md`
36. `STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`
37. `STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
38. `STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
39. `STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`
40. `STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`
41. `STD_WEIGHT_ADMISSION_BASELINE_AMSTERDAM_CANDIDATE_REVIEW.md`
42. `STD_WEIGHT_ICU_BASELINE_GROUPED_PROXY_FORMAL_APPROVAL_REVIEW.md`
43. `STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_FORMAL_APPROVAL_REVIEW.md`
44. `STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_CANDIDATE_REVIEW.md`
45. `STD_FIRST_DAY_URINE_OUTPUT_SUMMARY_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
46. `STD_ICU_URINE_OUTPUT_EVENT_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`
47. `AMSTERDAM_GOVERNED_RESULTS_DISTRIBUTION_APPROVAL_REVIEW.md`
48. `CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md`
49. `STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`
45. `CLASS1_CURRENT_APPROVAL_CLOSURE.md`
46. one simple class-1 example such as `std_glucose/`
47. one class-2 ICU-duration example such as `std_icu_los_days/`
48. one class-2 hospital-duration example such as `std_hospital_los_days/`
49. one class-2 post-discharge observed follow-up duration example such as `std_days_to_next_hospital_admission/`
50. one class-2 Amsterdam ICU-only follow-up duration example such as `std_days_to_next_icu_admission/`
51. one class-2 Amsterdam ICU/MCU follow-up duration example such as `std_days_to_next_icu_mcu_admission/`
52. one class-2 exact admission-baseline snapshot example such as `std_weight_admission_baseline/`
53. one class-2 exact ICU-baseline snapshot example such as `std_weight_icu_baseline/`
54. one class-2 derived BMI snapshot example such as `std_bmi_admission_baseline/`
55. one class-2 grouped/proxy baseline example such as `std_weight_icu_baseline_grouped_proxy/`
56. one class-2 window-summary example such as `std_first_day_urine_output_summary/`
57. one governed Amsterdam upstream event example such as `std_icu_urine_output_event/`
58. one class-3 binary-state example such as `std_invasive_mechanical_ventilation_active/`
59. one class-3 Amsterdam respiratory-support approval example such as `std_noninvasive_ventilation_active/` or `std_tracheostomy_status_active/`
60. one later class-3 MIMIC respiratory-support sibling example such as `std_high_flow_nasal_cannula_active/`, `std_supplemental_oxygen_active/`, or `std_tracheostomy_status_active/`
61. one class-3 medication-derived treatment-support example such as `std_vasopressor_support_active/`
62. one class-3 renal-support active-state example such as `std_rrt_active/`
63. one class-3 renal-support child-family active-state example such as `std_crrt_family_active/` or `std_non_crrt_rrt_active/`
64. one class-5 episode/modality bridge example such as `std_rrt_modality_episode/`
65. one multi-source or rule-heavy class-1 example such as `std_temp/` or `std_map/`

## What Is Still Not Claimed

- these are still early reusable classes, not the final schema for all variable families
- later rounds should add new class contracts rather than forcing every future variable into the first class
- the current public layer is strong enough to support governance and rerun evidence for class-1 variables, but it is not yet the full long-term industrial standard system
