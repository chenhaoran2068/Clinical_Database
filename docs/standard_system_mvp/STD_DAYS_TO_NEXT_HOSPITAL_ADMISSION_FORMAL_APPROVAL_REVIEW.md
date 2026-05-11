# `std_days_to_next_hospital_admission` Formal Approval Review

Review date: `2026-05-02`

## Formal Decision

- status: `reviewed_approved`
- approved database: `MIMIC-IV-3.1`
- standard variable: `std_days_to_next_hospital_admission`
- variable class: `baseline_summary_window_numeric`
- summary subclass: `duration_summary`
- governed variable spec: `docs/standard_system_mvp/std_days_to_next_hospital_admission/variable_spec.json`
- governed mapping spec: `docs/standard_system_mvp/std_days_to_next_hospital_admission/mapping_spec_mimic_iv_3_1.json`
- governed execution entrypoint: `docs/standard_system_mvp/std_days_to_next_hospital_admission/execution.py`
- current local implementation: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_days_to_next_hospital_admission/extract_code/Extract_Code_std_days_to_next_hospital_admission.py`

## Approved Meaning

`std_days_to_next_hospital_admission` is approved as the MIMIC hospital-admission-level post-discharge observed time-to-next-hospital-admission duration summary.

It means:

- one retained row per hospital admission encounter
- retained key is `hadm_id`
- canonical unit is `days`
- anchor is current hospital discharge time, `hosp_admissions.dischtime`
- retained value is elapsed days to the first later different hospitalization with `admittime > current dischtime`
- output precision is `round(3)` using the current approved half-away-from-zero implementation
- retained null means no later different hospitalization was observed in the captured MIMIC source snapshot

It does not mean:

- a 30-day readmission binary flag
- ICU readmission timing
- same-hospitalization ICU return timing
- all-system rehospitalization follow-up
- proof that a patient was never rehospitalized
- zero days when no later hospitalization is observed

## Build Results

The governed execute-mode run produced:

- retained rows: `546028`
- unique `hadm_id`: `546028`
- observed next-hospital-admission rows: `321561`
- no later hospitalization observed rows: `224467`
- minimum observed days: `0.001`
- median observed days: `85.111`
- p95 observed days: `1774.269`
- maximum observed days: `5340.54`

The public card is:

- `docs/std_variable_cards/std_days_to_next_hospital_admission.md`

## Governed Runtime Evidence

Public-safe runtime evidence exists for both first real execution and rerun reproducibility:

- `docs/standard_system_mvp/std_days_to_next_hospital_admission/runtime/mimic_iv_3_1_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_days_to_next_hospital_admission/runtime/mimic_iv_3_1_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_days_to_next_hospital_admission/runtime/mimic_iv_3_1_rerun_repro_check/validation_report.json`
- `docs/standard_system_mvp/std_days_to_next_hospital_admission/runtime/mimic_iv_3_1_rerun_repro_check/manifest.json`
- `docs/standard_system_mvp/std_days_to_next_hospital_admission/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime validation status:

- first real execution: `pass`
- rerun execution: `pass`
- reproducibility report: `pass`

Stable rerun summary fields matched:

- `total_rows`
- `unique_hadm_id`
- `observed_rows`
- `missing_rows`
- `min_days`
- `p50_days`
- `p95_days`
- `max_days`

The rerun also preserved the primary output asset and preview signatures under the current runtime-evidence reproducibility policy.

## Source-Audit Checks

The approved MIMIC mapping uses:

- source table: `hosp_admissions`
- search rule: first later different hospitalization with `admittime > current dischtime`
- rows with missing discharge time: `0`
- self-match rows prevented: `175`
- immediate nonpositive next-row artifacts audited: `2131`
- zero-gap immediate next-row artifacts: `2083`
- negative-gap immediate next-row artifacts: `48`
- rows recovered by skipping nonpositive immediate artifacts and finding a later valid admission: `1116`
- rows with no valid later post-discharge admission after nonpositive immediate artifacts: `1015`

Interpretation:

- the retained next-hospitalization search is stricter than simply taking the next admissions row
- same-time, overlapping, self-match, or nonpositive-gap rows do not become retained next admissions
- the output remains a duration summary and does not silently convert nulls to binary negatives or zeros

## Approval-Sensitive Checks

This approval depends on the following checks:

- target grain is hospital admission encounter, not ICU stay
- retained key is `hadm_id`
- no duplicate retained `hadm_id` is allowed
- anchor is `dischtime`
- eligible next admission must be a later different hospitalization
- next `admittime` must be strictly after current `dischtime`
- unit is days
- precision is `round(3)`
- retained null means no later different hospitalization observed in the captured MIMIC source
- null is not zero and is not complete all-system absence of rehospitalization

## Class-2 Interpretation

This variable extends Class 2 without changing the class boundary.

It remains inside `baseline_summary_window_numeric` because the main governance problem is:

- target grain
- anchor rule
- future-event selection rule
- elapsed-duration computation
- null/no-source-row interpretation
- rerun-stable numeric representation

The important distinction is:

- `std_hospital_los_days` measures the duration inside the current hospital admission
- `std_days_to_next_hospital_admission` measures the observed future duration after discharge to the next hospitalization
- `std_hospital_readmission_30d` would be a binary outcome and is not approved here
- `std_days_to_next_icu_admission` remains a separate ICU-stay-level sibling candidate because it has different grain and status-column semantics

## Amsterdam Boundary

Amsterdam is not approved for same-name `std_days_to_next_hospital_admission` in this review.

Reason:

- the current Amsterdam opening surface is ICU/MCU admission oriented
- true hospital-admission encounter start and discharge boundaries have not yet been governed in the public layer
- the same boundary kept Amsterdam out of same-name `std_hospital_los_days`

Amsterdam can be revisited only after a separate hospital-admission encounter bridge proves true hospital admission/discharge semantics.

The current bridge review now records that the Amsterdam opening layer does not prove that bridge:

- `docs/standard_system_mvp/AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md`

The safe Amsterdam follow-up route is documented separately:

- `docs/standard_system_mvp/AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md`
- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

That route is ICU/MCU local-admission timing, not same-name next hospital admission.

## Final Judgment

MIMIC-IV-3.1 `std_days_to_next_hospital_admission` is approved as a governed Class 2 `duration_summary` variable.

The approval is bounded to hospital-admission encounter grain, discharge anchoring, first later different hospitalization selection, source-observed follow-up scope, and nullable retained duration semantics.
