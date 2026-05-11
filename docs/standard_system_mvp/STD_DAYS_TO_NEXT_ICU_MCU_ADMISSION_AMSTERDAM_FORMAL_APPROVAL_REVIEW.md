# Formal Approval Review: std_days_to_next_icu_mcu_admission on AmsterdamUMCdb-1.0.2

Review date: `2026-05-02`

## Approval Decision

Approved.

`std_days_to_next_icu_mcu_admission` is approved for `AmsterdamUMCdb-1.0.2` as a governed Class 2 `duration_summary` variable.

This approval is Amsterdam-only and uses the split ICU/MCU identity.

It does not approve Amsterdam for same-name `std_days_to_next_hospital_admission`.

It does not publish MC-inclusive Amsterdam timing under same-name `std_days_to_next_icu_admission`.

## Variable Identity

- variable id: `std_days_to_next_icu_mcu_admission`
- standardized English name: `Days to next ICU/MCU admission`
- class: `baseline_summary_window_numeric`
- summary subclass: `duration_summary`
- database: `AmsterdamUMCdb-1.0.2`
- target grain: one Amsterdam ICU/MCU local admission
- anchor: current local ICU/MCU `dischargedat`
- future event: first later same-patient Amsterdam ICU/MCU local admission with `admittedat > current dischargedat`
- unit: days
- retained primary value field: `std_days_to_next_icu_mcu_admission`

## Evidence Package

Public governed artifacts:

- `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/variable_spec.json`
- `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/execution.py`
- `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json`

Local evidence:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/admissions_core.parquet`
- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/outcomes/std_days_to_next_icu_mcu_admission/std_days_to_next_icu_mcu_admission_long.parquet`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_days_to_next_icu_mcu_admission/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_days_to_next_icu_mcu_admission/query_summary`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_days_to_next_icu_mcu_admission/Layer5_PerVariable_KnowledgePackage.xlsx`

Pre-approval candidate boundary review:

- `docs/standard_system_mvp/AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md`

## Runtime Evidence

First governed execution:

- runtime directory: `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution`
- process batch id: `20260502T052839Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_mcu_admission`
- runtime validation: pass

Rerun reproducibility execution:

- runtime directory: `docs/standard_system_mvp/std_days_to_next_icu_mcu_admission/runtime/amsterdamumcdb_1_0_2_rerun_repro_check`
- process batch id: `20260502T052846Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_mcu_admission`
- runtime validation: pass
- reproducibility report: pass

## Output Summary

Retained output:

- total rows: `23106`
- unique `subject_id`: `20109`
- unique `stay_id`: `23106`
- observed next ICU/MCU local admission rows: `2967`
- missing duration rows: `20139`
- no later ICU/MCU local admission observed rows: `20139`
- unresolved missing `dischargedat` rows: `0`

Observed duration distribution:

- minimum days: `0.001`
- median days: `12.838`
- p95 days: `1592.307`
- maximum days: `4531.061`
- negative or zero observed duration rows: `0`

Death-context flags:

- `death_before_next_icu_mcu_admission_flag` rows: `31`
- `no_next_death_after_discharge_flag` rows: `3974`

These death fields are approved only as context flags.

They are not the primary ordering rule.

## Source Scope

Approved Amsterdam source scope:

- `IC`
- `MC`
- `IC&MC`
- `MC&IC`

This is why the variable uses the split identity `std_days_to_next_icu_mcu_admission`.

The MC-only rows are intentionally included.

## Boundary Decisions

Hospital-level boundary:

- not approved as `std_days_to_next_hospital_admission`
- Amsterdam still lacks a governed hospital admission/discharge bridge under the current opening layer
- raw `admissionid` remains a local ICU/MCU stay-equivalent key, not a canonical `hadm_id`

ICU-only boundary:

- not approved as Amsterdam same-name `std_days_to_next_icu_admission` in this review
- same-name `std_days_to_next_icu_admission` would require ICU-semantic-only scope: `IC`, `IC&MC`, `MC&IC`
- MC-inclusive output must remain under the split ICU/MCU identity

Null semantics:

- null retained value means no later Amsterdam ICU/MCU local admission was observed after current local discharge
- null does not mean zero days
- null does not prove absence of future critical care outside the captured source
- null does not encode a binary readmission flag

## Class-2 Interpretation

This variable remains inside Class 2 because the main governed burden is:

- anchor definition
- future-event search rule
- duration calculation
- target grain
- null/status semantics

It is not Class 5 episode logic because the retained output is not a start-stop treatment or support episode.

It is not Class 7 administrative identity mapping because no hospital encounter bridge is created.

## Final Judgment

`std_days_to_next_icu_mcu_admission` is approved for `AmsterdamUMCdb-1.0.2`.

The approval is bounded to Amsterdam ICU/MCU local-admission timing, source-observed follow-up, strict post-discharge future admission selection, nullable retained duration, and explicit separation from both hospital-level readmission timing and ICU-only next-admission timing.
