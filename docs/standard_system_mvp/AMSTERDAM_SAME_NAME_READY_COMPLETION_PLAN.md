# Amsterdam Same-Name Ready Completion Plan

Last updated: 2026-05-04

## Purpose

This note converts the Amsterdam full coverage audit into an execution queue.

The governing audit is:

- `docs/standard_system_mvp/AMSTERDAM_FULL_VARIABLE_COVERAGE_AUDIT.md`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.csv`

Superseding execution-order note:

- `docs/standard_system_mvp/CLASS1_TO_CLASS9_BUILD_FIRST_APPROVAL_LATER_PLAN.md`

The same-name-ready queue remains useful, but owner approval is now intentionally deferred until broader Class 1-9 buildable work has been completed and packaged for review.

## Current Same-Name Ready Set

The current audit marks `56` variables as `same_name_ready`.

This does not mean all 56 still need new work:

- `41` are already public-covered in Amsterdam
- `15` remain to be executed and approved

The practical completion target is therefore the remaining `15` same-name-ready variables.

## Already Covered

These `41` Amsterdam variables are already public-covered and should be treated as complete for the current same-name-ready campaign:

- `std_bicarbonate_bg`
- `std_bun`
- `std_chloride`
- `std_creatinine`
- `std_crrt_family_active`
- `std_days_to_next_icu_admission`
- `std_days_to_next_icu_mcu_admission`
- `std_dbp`
- `std_first_day_urine_output_summary`
- `std_glucose`
- `std_heart_rate`
- `std_hematocrit`
- `std_hemoglobin`
- `std_height`
- `std_icu_los_days`
- `std_icu_mortality`
- `std_icu_urine_output_event`
- `std_invasive_mechanical_ventilation_active`
- `std_lactate_bg`
- `std_map`
- `std_non_crrt_rrt_active`
- `std_noninvasive_ventilation_active`
- `std_paco2`
- `std_pao2`
- `std_ph_bg`
- `std_platelet_count`
- `std_potassium`
- `std_respiratory_rate`
- `std_rrt_active`
- `std_rrt_fluid_removal_event`
- `std_rrt_modality_episode`
- `std_sbp`
- `std_sex`
- `std_sodium`
- `std_spo2`
- `std_temp`
- `std_tracheostomy_status_active`
- `std_vasopressor_support_active`
- `std_weight_event`
- `std_weight_icu_baseline_grouped_proxy`
- `std_wbc_count`

## Remaining Execution Queue

### Batch 1: Core Vital And ICU Numeric Spine

These are the highest-yield same-name-ready variables because they are direct event-level Amsterdam numeric candidates and are reused by later severity, ventilation, shock, and kidney workflows.

Status: completed and approved on 2026-05-03.

Formal review:

- `docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH1_FORMAL_APPROVAL_REVIEW.md`

Recommended order:

1. `std_map`
2. `std_sbp`
3. `std_dbp`
4. `std_respiratory_rate`
5. `std_spo2`
6. `std_temp`
7. `std_glucose`
8. `std_sodium`
9. `std_potassium`
10. `std_chloride`
11. `std_creatinine`
12. `std_lactate_bg`
13. `std_paco2`
14. `std_pao2`
15. `std_bicarbonate_bg`
16. `std_bun`
17. `std_hemoglobin`
18. `std_hematocrit`
19. `std_platelet_count`
20. `std_wbc_count`

Execution rule:

- use Amsterdam `numericitems_event` plus dictionary-driven item review
- write governed mapping specs
- run first execution, rerun, reproducibility
- write formal approval review
- update public card and rerun the coverage audit

### Batch 2: Numeric Spine Later

These remain same-name-ready, but should follow Batch 1 because they either depend on stricter item-family review or are lower-priority for the immediate ICU backbone.

Status: candidate artifacts, governed first execution, governed rerun, and reproducibility evidence completed on 2026-05-04; first variable-level formal review completed on 2026-05-04.

Review evidence:

- `docs/standard_system_mvp/VARIABLE_REVIEW_REPORTING_STANDARD.md`
- `docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH2_CANDIDATE_EVIDENCE_REVIEW.md`
- `docs/standard_system_mvp/AMSTERDAM_CLASS1_BATCH2_FORMAL_APPROVAL_REVIEW.md`
- `docs/standard_system_mvp/CLASS1_CURRENT_APPROVAL_CLOSURE.md`

Formal review result:

- approved: `std_oxygen_partial_pressure_bg_allspecimen`, `std_carbon_dioxide_partial_pressure_bg_allspecimen`, `std_oxygen_saturation_bg_allspecimen`, `std_total_bilirubin`, `std_albumin`, `std_inr`, `std_aptt`
- not approved yet: `std_oxygen_saturation_bg_arterial_specimen`, `std_pt`

Recommended order:

1. `std_oxygen_partial_pressure_bg_allspecimen`
2. `std_carbon_dioxide_partial_pressure_bg_allspecimen`
3. `std_oxygen_saturation_bg_allspecimen`
4. `std_oxygen_saturation_bg_arterial_specimen`
5. `std_total_bilirubin`
6. `std_albumin`
7. `std_inr`
8. `std_pt`
9. `std_aptt`

Execution rule:

- treat blood-gas all-specimen and arterial-specimen scope as an explicit mapping boundary
- do not silently merge monitor `SpO2` and blood-gas oxygen saturation
- keep coagulation tests under a narrow lab-event source contract

### Batch 3: Derived Support-State Same-Name Variables

These are ready because their parent support families are already approved or bounded enough for governed derivation.

Recommended order:

1. `std_mechanical_ventilation_imv_niv_active`
2. `std_advanced_respiratory_support_active`

Execution rule:

- derive only from approved or explicitly bounded support-state parents
- preserve parent-source flags
- do not treat these composites as raw device events

### Batch 4: Class 5 Agent Episode

Recommended order:

1. `std_vasopressor_support_agent_episode`

Execution rule:

- use the already approved Amsterdam `std_vasopressor_support_active` parent layer
- preserve agent identity and parent episode linkage
- do not convert this to dose burden or shock phenotype

### Batch 5: ICU Encounter/Admin Same-Name Variables

Recommended order:

1. `std_icu_entry_source`
2. `std_icu_exit_destination`
3. `std_discharge_disposition`

Execution rule:

- use Amsterdam `admissions_core`
- keep ICU/MCU encounter semantics explicit
- do not promote these to hospital-wide encounter semantics

## Explicit Non-Goals

This campaign does not approve:

- `split_identity_needed` variables
- `bounded_candidate_only` variables
- `not_supported_or_blocked` variables
- hospital-level readmission or hospital LOS same-name Amsterdam mappings
- Amsterdam microbiology same-name mappings
- trial-style 28-day outcomes without a follow-up bridge

## Completion Definition

The same-name-ready campaign is complete when all remaining `8` variables have:

- governed variable directory or approved extension of an existing governed class path
- Amsterdam mapping spec
- `execution.py`
- first execution runtime evidence
- rerun reproducibility evidence
- formal approval review
- public card update
- rerun `build_amsterdam_coverage_audit.py`
- `check_public_repository.py` pass

## Immediate Next Step

Resolve the two Batch 2 hold items before treating Batch 2 as closed:

1. `std_oxygen_saturation_bg_arterial_specimen`
2. `std_pt`

The arterial oxygen-saturation candidate needs stronger specimen proof or a narrower Amsterdam-specific claim. The PT candidate needs a source-scale decision because the legacy seconds-labeled Amsterdam source behaves like an INR-like ratio, not PT seconds.
