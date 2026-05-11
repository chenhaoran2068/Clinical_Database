# `std_hospital_los_days` Formal Approval Review

Review date: `2026-04-28`

## Formal Decision

- status: `reviewed_approved`
- approved database: `MIMIC-IV-3.1`
- standard variable: `std_hospital_los_days`
- variable class: `baseline_summary_window_numeric`
- summary subclass: `duration_summary`
- governed variable spec: `docs/standard_system_mvp/std_hospital_los_days/variable_spec.json`
- governed mapping spec: `docs/standard_system_mvp/std_hospital_los_days/mapping_spec_mimic_iv_3_1.json`
- governed execution entrypoint: `docs/standard_system_mvp/std_hospital_los_days/execution.py`
- current local implementation: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_hospital_los_days/extract_code/Extract_Code_std_hospital_los_days.py`

## Approved Meaning

`std_hospital_los_days` is approved as the MIMIC hospital-admission-level length-of-stay duration summary.

It means:

- one retained row per hospital admission encounter
- retained key is `hadm_id`
- canonical unit is `days`
- source start boundary is `hosp_admissions.admittime`
- source end boundary is `hosp_admissions.dischtime`
- retained value is computed as `(dischtime - admittime) / 86400`
- output precision is `round(3)` using the current approved half-away-from-zero implementation
- rare negative-duration source edge cases are retained and explicitly flagged by `hospital_los_validity_status`

It does not mean:

- ICU length of stay
- ICU/MC stay-equivalent duration
- patient-level total follow-up time
- first-day duration
- an ICU-subset-only `icustay_detail.los_hospital` value
- a nonnegative-only analysis cohort with negative source edge cases silently removed

## Build Results

The governed execute-mode run produced:

- retained rows: `546028`
- unique `hadm_id`: `546028`
- nonnegative duration rows: `545853`
- negative duration rows: `175`
- zero-duration rows: `5`
- raw minimum duration: `-0.9451388888888889` days
- raw maximum duration: `515.5625` days

The public card is:

- `docs/std_variable_cards/std_hospital_los_days.md`

## Governed Runtime Evidence

Public-safe runtime evidence exists for both first real execution and rerun reproducibility:

- `docs/standard_system_mvp/std_hospital_los_days/runtime/mimic_iv_3_1_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_hospital_los_days/runtime/mimic_iv_3_1_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_hospital_los_days/runtime/mimic_iv_3_1_rerun_repro_check/validation_report.json`
- `docs/standard_system_mvp/std_hospital_los_days/runtime/mimic_iv_3_1_rerun_repro_check/manifest.json`
- `docs/standard_system_mvp/std_hospital_los_days/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime validation status:

- first real execution: `pass`
- rerun execution: `pass`
- reproducibility report: `pass`

Stable rerun summary fields matched:

- `total_rows`
- `unique_hadm_id`
- `negative_duration_rows`
- `nonnegative_duration_rows`
- `zero_duration_rows`
- `min_days_raw`
- `max_days_raw`

## Official-Source Alignment

MIMIC-IV v3.1 official scope reports `546,028` hospital admissions.

The governed `std_hospital_los_days` retained output also has:

- retained rows: `546028`
- unique `hadm_id`: `546028`

Interpretation:

- the retained grain aligns with the official hospital-admission count
- this supports the `hadm_id`-level encounter interpretation

The local source audit compares the direct `hosp_admissions.admittime` / `hosp_admissions.dischtime` calculation against the ICU-linked official derived `icustay_detail.los_hospital` audit subset.

Current audit result:

- ICU-linked comparable rows: `94458`
- ICU-linked mismatch rows: `0`

Interpretation:

- the all-admission retained source is the direct hospital admission interval
- the ICU-linked official derived field is consistent as an audit subset
- the audit field does not replace the all-admission primary source

## Approval-Sensitive Checks

This approval depends on the following checks:

- target grain is hospital admission encounter, not ICU stay
- retained key is `hadm_id`
- no duplicate retained `hadm_id` is allowed
- source start and end boundaries are `admittime` and `dischtime`
- unit is days
- precision is `round(3)`
- negative-duration rows are not silently dropped
- downstream nonnegative analyses must use `hospital_los_validity_status`
- `icustay_detail.los_hospital` remains audit-only

## Class-2 Interpretation

This variable strengthens Class 2 because it adds a hospital-admission duration summary after the first ICU-duration proof.

The important distinction is:

- `std_icu_los_days` is ICU-stay or ICU-semantic stay-equivalent duration
- `std_hospital_los_days` is hospital-admission encounter duration

The two variables are related but not interchangeable.

## Remaining Boundary

Amsterdam is not approved for same-name `std_hospital_los_days` in this review.

Before Amsterdam can share this variable identity, it must show true hospital-admission start and discharge semantics.

If Amsterdam only has ICU/MC admission boundaries for the relevant retained source, that evidence should remain under an ICU/stay-duration identity rather than being forced into `std_hospital_los_days`.

A dedicated candidate review now records that boundary in:

- `docs/standard_system_mvp/STD_HOSPITAL_LOS_DAYS_AMSTERDAM_CANDIDATE_REVIEW.md`

## Final Judgment

MIMIC-IV-3.1 `std_hospital_los_days` is approved as a governed Class 2 `duration_summary` variable.

The approval is bounded to hospital-admission encounter duration computed from `hosp_admissions.admittime` and `hosp_admissions.dischtime`, with negative-duration edge cases retained and explicitly flagged rather than silently removed.
