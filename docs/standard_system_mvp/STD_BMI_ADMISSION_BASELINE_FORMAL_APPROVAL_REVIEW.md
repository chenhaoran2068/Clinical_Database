# `std_bmi_admission_baseline` Formal Approval Review

Review date: `2026-04-28`

## Formal Decision

- status: `reviewed_approved`
- approved database: `MIMIC-IV-3.1`
- standard variable: `std_bmi_admission_baseline`
- variable class: `baseline_summary_window_numeric`
- summary subclass: `baseline_snapshot` derived numeric
- governed variable spec: `docs/standard_system_mvp/std_bmi_admission_baseline/variable_spec.json`
- governed mapping spec: `docs/standard_system_mvp/std_bmi_admission_baseline/mapping_spec_mimic_iv_3_1.json`
- governed execution entrypoint: `docs/standard_system_mvp/std_bmi_admission_baseline/execution.py`
- upstream dependencies: approved MIMIC `std_weight_admission_baseline` plus approved MIMIC `std_height`

This note promotes the earlier candidate review into governed MVP approval.

## Approved Meaning

`std_bmi_admission_baseline` is approved as the MIMIC hospital-admission baseline body mass index snapshot.

It means:

- one retained row per hospital admission encounter when both upstream inputs are available
- retained key is `hadm_id`
- canonical unit is `kg/m^2`
- retained value is `std_bmi_kg_per_m2`
- formula is `std_weight_kg_baseline / ((std_height_cm / 100.0) ^ 2)`
- retained precision is `round(2)`
- the baseline anchor, window, and selected weight event are inherited from `std_weight_admission_baseline`
- height comes from the approved subject-level `std_height` asset
- rows outside the BMI review-flag range are retained with `is_bmi_outlier_by_contract`

It does not mean:

- raw BMI copied directly from a source table
- patient-fixed lifetime BMI
- ICU-start BMI
- first-day mean BMI
- BMI recomputed from raw height and raw weight outside approved upstream assets
- an analysis-ready cohort with extreme BMI rows silently removed

## Build Results

The governed execute-mode run produced:

- retained rows: `55501`
- unique `subject_id`: `41655`
- unique `hadm_id`: `55501`
- upstream admission-baseline weight rows: `69312`
- missing height rows after join: `13811`
- height-join coverage rate versus upstream weight rows: `0.800742`
- outlier-flagged BMI rows: `38`
- BMI minimum: `7.54`
- BMI maximum: `170.99`
- selected upstream weight rows from `admission_weight_kg`: `54370`
- selected upstream weight rows from `admission_weight_lbs`: `263`
- selected upstream weight rows from `daily_weight_kg`: `868`
- height rows from `hosp_omr`: `37153`
- height rows from `icu_chartevents_height_cm`: `18348`

The public card is:

- `docs/std_variable_cards/std_bmi_admission_baseline.md`

## Governed Runtime Evidence

Public-safe runtime evidence exists for both first real execution and rerun reproducibility:

- `docs/standard_system_mvp/std_bmi_admission_baseline/runtime/mimic_iv_3_1_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_bmi_admission_baseline/runtime/mimic_iv_3_1_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_bmi_admission_baseline/runtime/mimic_iv_3_1_rerun_repro_check/validation_report.json`
- `docs/standard_system_mvp/std_bmi_admission_baseline/runtime/mimic_iv_3_1_rerun_repro_check/manifest.json`
- `docs/standard_system_mvp/std_bmi_admission_baseline/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime validation status:

- first real execution: `pass`
- rerun execution: `pass`
- reproducibility report: `pass`

Stable rerun summary fields matched:

- `total_rows`
- `unique_subject_id`
- `unique_hadm_id`
- `upstream_weight_rows_total`
- `missing_height_rows`
- `height_join_coverage_rows`
- `height_join_coverage_rate_vs_weight`
- `bmi_outlier_rows`
- `bmi_min`
- `bmi_max`
- weight-source count fields
- height-source count fields

## Approval-Sensitive Checks

This approval depends on the following checks:

- target grain is hospital admission encounter, not ICU stay
- retained key is `hadm_id`
- no duplicate retained `hadm_id` is allowed
- BMI is derived only from approved `std_weight_admission_baseline` and approved `std_height`
- height must be converted from centimeters to meters before applying the formula
- unit is `kg/m^2`
- precision is `round(2)`
- rows without retained height are absent rather than represented as null BMI rows
- outlier-flagged rows are retained and must not be silently dropped by the governed asset
- the hard valid range is wider than the review-flag range because the current approved local asset intentionally retains extreme flagged BMI values

## Class-2 Interpretation

This variable strengthens Class 2 because it proves that derived baseline snapshots can be governed under the same class-2 hard chain when their upstream dependencies are explicit.

The important distinction is:

- `std_weight_admission_baseline` is the selected hospital-admission baseline weight
- `std_bmi_admission_baseline` is derived from that selected weight plus subject-level height
- `std_bmi_admission_baseline` is not interchangeable with `std_bmi_icu_baseline`

## Remaining Boundary

The approval is MIMIC-only at this stage.

AmsterdamUMCdb-1.0.2 is not approved for same-name `std_bmi_admission_baseline` in this review.

Before Amsterdam can share this variable identity, it must have compatible governed upstream evidence for exact admission-baseline weight and subject-level height, and the resulting BMI must pass the same spec, mapping, execution, runtime, rerun, and formal review gate.

## Final Judgment

MIMIC-IV-3.1 `std_bmi_admission_baseline` is approved as a governed Class 2 `baseline_snapshot` derived numeric variable.

The approval is bounded to BMI derived from approved admission-baseline weight and approved subject-level height, with missing-height rows absent and extreme BMI rows retained with explicit outlier flags.

## Source Pointers

Public source references used for BMI interpretation:

- CDC BMI formula and interpretation page: <https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html>
