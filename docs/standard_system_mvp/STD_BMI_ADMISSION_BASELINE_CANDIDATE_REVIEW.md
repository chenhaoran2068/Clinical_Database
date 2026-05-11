# `std_bmi_admission_baseline` Candidate Review

Review date: `2026-04-28`

Supersession update: this candidate review has now been followed by formal governed approval in `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`.

This note is retained as the candidate-stage audit record. It should no longer be read as the current final status.

## Formal Verdict

Formal decision:

- public-card metadata blocker: fixed
- content-level candidate review: pass
- Class 2 admission-readiness judgment: eligible for next governed MVP promotion
- governed standard-system approval status at candidate-review time: not yet promoted by this note

This means `std_bmi_admission_baseline` is suitable to enter the next governed Class 2 promotion step, but it should not be described as a closed governed MVP until it has:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- execute-mode runtime `validation_report.json`
- execute-mode runtime `manifest.json`
- rerun runtime evidence
- reproducibility report

## Metadata Repair Completed

The public variable card previously showed:

- `latest_review_date = ########`

The local asset manifest shows:

- `latest_review_date = 2026-04-01`

The public card has now been regenerated and shows:

- `latest_review_date = 2026-04-01`

The corrected public card is:

- `docs/std_variable_cards/std_bmi_admission_baseline.md`

## What Was Reviewed

Reviewed public surface:

- `docs/std_variable_cards/std_bmi_admission_baseline.md`
- `docs/std_variable_cards/std_weight_admission_baseline.md`
- `docs/std_variable_cards/std_height.md`
- `docs/standard_system_mvp/STD_WEIGHT_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`

Reviewed local MIMIC evidence:

- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_admission_baseline/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_admission_baseline/extract_code/Extract_Code_std_bmi_admission_baseline.py`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_admission_baseline/query_summary/std_bmi_admission_baseline_quality_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_admission_baseline/query_summary/std_bmi_admission_baseline_distribution_summary.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_admission_baseline/query_summary/std_bmi_admission_baseline_source_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_admission_baseline/query_summary/std_bmi_admission_baseline_rule_trace.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_weight_admission_baseline/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_height/asset_manifest.md`

## Candidate Meaning

`std_bmi_admission_baseline` means:

- hospital-admission encounter baseline BMI
- target grain: one retained row per `hadm_id`
- retained value: `std_bmi_kg_per_m2`
- unit: `kg/m^2`
- precision: `round(2)`
- formula: `weight_kg / (height_m ^ 2)`
- upstream weight source: approved `std_weight_admission_baseline`
- upstream height source: approved `std_height`

It does not mean:

- raw BMI directly copied from a source table
- patient-fixed lifetime BMI
- ICU-start BMI
- first-day mean BMI
- BMI recomputed from raw height and raw weight outside approved upstream assets

## Local Content Summary

The local asset manifest reports:

- database: `MIMIC-IV-3.1`
- status: `reviewed_approved`
- version: `v1`
- latest review date: `2026-04-01`
- total retained rows: `55,501`
- upstream admission-baseline weight rows: `69,312`
- missing height rows after join: `13,811`
- outlier-flagged BMI rows: `38`

The retained columns are:

- `subject_id`
- `hadm_id`
- `selected_stay_id`
- `std_bmi_kg_per_m2`
- `is_bmi_outlier_by_contract`
- `weight_source_preferred`
- `height_source_preferred`

The local quality summary reports:

- unique `subject_id`: `41,655`
- unique `hadm_id`: `55,501`
- duplicate retained `hadm_id` risk: not indicated by the current summary because row count equals unique `hadm_id`
- BMI outlier flag distribution:
- `False`: `55,463`
- `True`: `38`

Weight source distribution:

- `admission_weight_kg`: `54,370`
- `daily_weight_kg`: `868`
- `admission_weight_lbs`: `263`

Height source distribution:

- `hosp_omr`: `37,153`
- `icu_chartevents_height_cm`: `18,348`

## Upstream Dependency Review

### Weight

The upstream `std_weight_admission_baseline` asset is already reviewed-approved for `MIMIC-IV-3.1`.

It contributes:

- hospital-admission anchor
- `hadm_id` target grain
- selected cleaned baseline weight in `kg`
- explicit no-source-row behavior
- governed Class 2 runtime evidence

Interpretation:

- BMI inherits hospital-admission anchor semantics from this weight asset.
- BMI should not redefine its own admission baseline window independently.

### Height

The upstream MIMIC `std_height` asset is already reviewed-approved.

It contributes:

- patient-level standardized height in `cm`
- source priority across hospital OMR and ICU chartevents height sources
- approved patient-level retained height asset

Interpretation:

- BMI inherits height availability and height source limitations.
- Missing BMI is partly a missing-height issue, not only a missing-weight issue.

## Class 2 Fit

This candidate fits Class 2 as:

- variable class: `baseline_summary_window_numeric`
- summary subclass: `baseline_snapshot`
- derived numeric baseline snapshot
- one retained numeric row per anchor-qualified hospital admission encounter

Why it fits:

- it is not event-level
- it has a clear anchor inherited from admission-baseline weight
- it has a clear formula
- it has a stable unit
- it has explicit upstream dependencies

Why it is higher risk than simple weight:

- it is derived from two upstream assets
- it inherits missingness from both height and weight
- it depends on exact alignment between patient-level height and admission-level weight
- extreme values should be flagged, not silently removed

## Approval-Sensitive Points

The following points must be locked before governed MVP approval:

- `std_weight_admission_baseline` must remain the only approved weight input for this variable.
- MIMIC `std_height` must remain the only approved height input for this variable.
- height must be converted from `cm` to `m` before the formula.
- formula must remain `weight_kg / (height_m ^ 2)`.
- output unit must remain `kg/m^2`.
- output precision must remain `round(2)`.
- outlier rows must be retained with `is_bmi_outlier_by_contract`, not silently dropped.
- target key must be `hadm_id`, not `stay_id`.

## Current Blocking Status

No content-level blocking finding remains.

Remaining governed-MVP blocker:

- the public machine-readable standard-system chain has not yet been created for this BMI variable

That is an engineering/governance completion blocker, not a semantic rejection.

## Recommended Next Action

Recommended next action:

- promote `std_bmi_admission_baseline` into the governed Class 2 MVP surface after this candidate review

Required promotion artifacts:

- `docs/standard_system_mvp/std_bmi_admission_baseline/variable_spec.json`
- `docs/standard_system_mvp/std_bmi_admission_baseline/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_bmi_admission_baseline/execution.py`
- execute-mode runtime evidence
- rerun reproducibility evidence
- formal approval review note

Historical gate rule at candidate-review time: do not update Class 2 closure to call this variable governed-approved until those artifacts exist and pass validation.

Current status update: those artifacts now exist and are reviewed in `docs/standard_system_mvp/STD_BMI_ADMISSION_BASELINE_FORMAL_APPROVAL_REVIEW.md`.

## Final Decision

`std_bmi_admission_baseline` passes candidate review for Class 2 promotion.

At candidate-review time, it should have been treated as:

- content-eligible
- MIMIC-only at this stage
- derived baseline numeric
- pending governed MVP promotion

At candidate-review time, it should not have been treated as:

- fully governed standard-system approved
- cross-database approved
- independent of upstream height and weight governance

Current final status is superseded by the formal approval review.

## Source Pointers

Public source references used for BMI interpretation:

- CDC BMI formula and interpretation page: <https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html>
