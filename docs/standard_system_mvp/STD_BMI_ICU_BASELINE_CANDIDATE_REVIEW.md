# `std_bmi_icu_baseline` Candidate Review

Review date: `2026-04-28`

Supersession update: this candidate review has now been followed by formal governed approval in `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`.

This note is retained as the candidate-stage audit record. It should no longer be read as the current final status.

## Formal Verdict

Formal decision:

- public-card metadata blocker: fixed
- content-level candidate review: pass
- Class 2 ICU-baseline readiness judgment: eligible for next governed MVP promotion
- governed standard-system approval status at candidate-review time: not yet promoted by this note

This means `std_bmi_icu_baseline` is suitable to enter the next governed Class 2 promotion step, but it should not be described as a closed governed MVP until it has:

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

- `docs/std_variable_cards/std_bmi_icu_baseline.md`

## What Was Reviewed

Reviewed public surface:

- `docs/std_variable_cards/std_bmi_icu_baseline.md`
- `docs/std_variable_cards/std_weight_icu_baseline.md`
- `docs/std_variable_cards/std_height.md`
- `docs/standard_system_mvp/STD_WEIGHT_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`

Reviewed local MIMIC evidence:

- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_icu_baseline/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_icu_baseline/extract_code/Extract_Code_std_bmi_icu_baseline.py`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_icu_baseline/query_summary/std_bmi_icu_baseline_quality_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_icu_baseline/query_summary/std_bmi_icu_baseline_distribution_summary.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_icu_baseline/query_summary/std_bmi_icu_baseline_source_audit_summary.json`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_bmi_icu_baseline/query_summary/std_bmi_icu_baseline_rule_trace.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_weight_icu_baseline/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_height/asset_manifest.md`

## Candidate Meaning

`std_bmi_icu_baseline` means:

- ICU-stay baseline BMI
- target grain: one retained row per `stay_id`
- retained value: `std_bmi_kg_per_m2`
- unit: `kg/m^2`
- precision: `round(2)`
- formula: `weight_kg / (height_m ^ 2)`
- upstream weight source: approved `std_weight_icu_baseline`
- upstream height source: approved `std_height`

It does not mean:

- raw BMI directly copied from a source table
- patient-fixed lifetime BMI
- hospital-admission baseline BMI
- first-day mean BMI
- BMI recomputed from raw height and raw weight outside approved upstream assets

## Local Content Summary

The local asset manifest reports:

- database: `MIMIC-IV-3.1`
- status: `reviewed_approved`
- version: `v1`
- latest review date: `2026-04-01`
- total retained rows: `73,432`
- upstream ICU-baseline weight rows: `88,690`
- missing height rows after join: `15,258`
- outlier-flagged BMI rows: `53`

The retained columns are:

- `subject_id`
- `hadm_id`
- `stay_id`
- `std_bmi_kg_per_m2`
- `is_bmi_outlier_by_contract`
- `weight_source_preferred`
- `height_source_preferred`

The local quality summary reports:

- unique `subject_id`: `50,438`
- unique `hadm_id`: `69,015`
- unique `stay_id`: `73,432`
- duplicate retained `stay_id` risk: not indicated by the current summary because row count equals unique `stay_id`
- BMI outlier flag distribution:
- `False`: `73,379`
- `True`: `53`

Weight source distribution:

- `admission_weight_kg`: `54,273`
- `admission_weight_lbs`: `13,994`
- `daily_weight_kg`: `5,165`

Height source distribution:

- `hosp_omr`: `50,737`
- `icu_chartevents_height_cm`: `22,695`

## Upstream Dependency Review

### Weight

The upstream `std_weight_icu_baseline` asset is already reviewed-approved for `MIMIC-IV-3.1`.

It contributes:

- ICU admission anchor
- `stay_id` target grain
- selected cleaned ICU-baseline weight in `kg`
- explicit ICU-baseline window and clipping rules
- governed Class 2 runtime evidence

Interpretation:

- BMI inherits ICU-baseline anchor semantics from this weight asset.
- BMI should not redefine its own ICU baseline window independently.

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
- one retained numeric row per anchor-qualified ICU stay

Why it fits:

- it is not event-level
- it has a clear anchor inherited from ICU-baseline weight
- it has a clear formula
- it has a stable unit
- it has explicit upstream dependencies

Why it is higher risk than simple weight:

- it is derived from two upstream assets
- it inherits missingness from both height and weight
- it combines patient-level height with ICU-stay-level baseline weight
- extreme values should be flagged, not silently removed

## Approval-Sensitive Points

The following points must be locked before governed MVP approval:

- `std_weight_icu_baseline` must remain the only approved weight input for this variable.
- MIMIC `std_height` must remain the only approved height input for this variable.
- height must be converted from `cm` to `m` before the formula.
- formula must remain `weight_kg / (height_m ^ 2)`.
- output unit must remain `kg/m^2`.
- output precision must remain `round(2)`.
- outlier rows must be retained with `is_bmi_outlier_by_contract`, not silently dropped.
- target key must be `stay_id`, not `hadm_id`.

## Current Blocking Status

No content-level blocking finding remains.

Remaining governed-MVP blocker:

- the public machine-readable standard-system chain has not yet been created for this BMI variable

That is an engineering/governance completion blocker, not a semantic rejection.

## Recommended Next Action

Recommended next action:

- promote `std_bmi_icu_baseline` into the governed Class 2 MVP surface after `std_bmi_admission_baseline`, or promote both as a paired BMI-derived-baseline mini-batch

Required promotion artifacts:

- `docs/standard_system_mvp/std_bmi_icu_baseline/variable_spec.json`
- `docs/standard_system_mvp/std_bmi_icu_baseline/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_bmi_icu_baseline/execution.py`
- execute-mode runtime evidence
- rerun reproducibility evidence
- formal approval review note

Historical gate rule at candidate-review time: do not update Class 2 closure to call this variable governed-approved until those artifacts exist and pass validation.

Current status update: those artifacts now exist and are reviewed in `docs/standard_system_mvp/STD_BMI_ICU_BASELINE_FORMAL_APPROVAL_REVIEW.md`.

## Final Decision

`std_bmi_icu_baseline` passes candidate review for Class 2 promotion.

At candidate-review time, it should have been treated as:

- content-eligible
- MIMIC-only at this stage
- derived ICU-baseline numeric
- pending governed MVP promotion

At candidate-review time, it should not have been treated as:

- fully governed standard-system approved
- cross-database approved
- interchangeable with admission-baseline BMI
- independent of upstream height and weight governance

Current final status is superseded by the formal approval review.

## Source Pointers

Public source references used for BMI interpretation:

- CDC BMI formula and interpretation page: <https://www.cdc.gov/bmi/adult-calculator/bmi-categories.html>
