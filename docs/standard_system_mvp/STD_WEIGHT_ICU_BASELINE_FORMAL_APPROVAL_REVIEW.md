# `std_weight_icu_baseline` Formal Approval Review

Review date: `2026-04-26`

## Formal Decision

- status: `reviewed_approved`
- approved database: `MIMIC-IV-3.1`
- standard variable: `std_weight_icu_baseline`
- variable class: `baseline_summary_window_numeric`
- summary subclass: `baseline_snapshot`
- governed mapping spec: `docs/standard_system_mvp/std_weight_icu_baseline/mapping_spec_mimic_iv_3_1.json`
- governed execution entrypoint: `docs/standard_system_mvp/std_weight_icu_baseline/execution.py`
- upstream dependency: approved MIMIC `std_weight_event`

## Approved Meaning

`std_weight_icu_baseline` is approved as the MIMIC ICU-stay-level baseline body-weight snapshot.

It means:

- one retained row per ICU stay when a qualifying baseline weight event exists
- canonical unit is `kg`
- source events come from approved cleaned `std_weight_event` rows
- target anchor is `icu.icustays.intime`
- candidate window is `[-360, +360]` minutes around ICU admission
- the candidate window is clipped by hospital admission, ICU outtime, and hospital discharge boundaries
- selection uses closest absolute time distance to ICU admission
- tie-breaks use source priority, then earlier measurement time, then stable source measurement id

It does not mean:

- patient-level stable body weight
- hospital-admission baseline weight
- first-day average weight
- discharge weight
- Amsterdam grouped/proxy weight

## Build Results

The governed execute-mode run produced:

- retained rows: `88690`
- unique `subject_id`: `64471`
- unique `hadm_id`: `83948`
- unique `stay_id`: `88690`
- all ICU stays: `94458`
- ICU-stay coverage: `88690 / 94458 = 0.938936`
- selected `admission_weight_kg` rows: `65549`
- selected `admission_weight_lbs` rows: `16448`
- selected `daily_weight_kg` rows: `6693`

## Governed Runtime Evidence

Public-safe runtime evidence exists for both first real execution and rerun reproducibility:

- `docs/standard_system_mvp/std_weight_icu_baseline/runtime/mimic_iv_3_1_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_weight_icu_baseline/runtime/mimic_iv_3_1_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_weight_icu_baseline/runtime/mimic_iv_3_1_rerun_repro_check/validation_report.json`
- `docs/standard_system_mvp/std_weight_icu_baseline/runtime/mimic_iv_3_1_rerun_repro_check/manifest.json`
- `docs/standard_system_mvp/std_weight_icu_baseline/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime validation status:

- first real execution: `pass`
- rerun execution: `pass`
- reproducibility report: `pass`

## Approval-Sensitive Checks

This approval depends on the following checks:

- target grain is ICU stay, not hospital admission
- retained key is `stay_id`
- no duplicate retained `stay_id` is allowed
- upstream weight rows must already be cleaned and normalized to `kg`
- candidate rows must have direct `stay_id` linkage
- candidate rows must fall inside the approved clipped ICU-baseline window
- target ICU stays without a qualifying event are absent rather than retained as null rows
- Amsterdam grouped/proxy evidence remains under `std_weight_icu_baseline_grouped_proxy`

## Class-2 Interpretation

This variable strengthens Class 2 because it adds a second exact MIMIC baseline-snapshot example after `std_weight_admission_baseline`.

The important distinction is:

- `std_weight_admission_baseline` is hospital-admission anchored
- `std_weight_icu_baseline` is ICU-admission anchored

The two variables are related but not interchangeable.

## Final Judgment

MIMIC-IV-3.1 `std_weight_icu_baseline` is approved as a governed Class 2 `baseline_snapshot` variable.

The approval is bounded to exact cleaned event-derived ICU baseline weight and does not approve grouped/proxy body-size values or subject-level stable weight under this name.
