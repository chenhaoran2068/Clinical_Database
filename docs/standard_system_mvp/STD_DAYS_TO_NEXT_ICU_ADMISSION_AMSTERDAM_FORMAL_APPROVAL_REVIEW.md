# Formal Approval Review: std_days_to_next_icu_admission on AmsterdamUMCdb-1.0.2

Review date: `2026-05-02`

## Approval Decision

Approved.

`std_days_to_next_icu_admission` is approved for `AmsterdamUMCdb-1.0.2` as a governed Class 2 `duration_summary` variable.

This approval is a same-name Amsterdam add-on to the existing MIMIC-approved ICU-only variable.

It is ICU-only in Amsterdam scope.

It does not approve Amsterdam for same-name `std_days_to_next_hospital_admission`.

It does not replace the MC-inclusive split identity `std_days_to_next_icu_mcu_admission`.

## Variable Identity

- variable id: `std_days_to_next_icu_admission`
- standardized English name: `Days to next ICU admission`
- class: `baseline_summary_window_numeric`
- summary subclass: `duration_summary`
- database: `AmsterdamUMCdb-1.0.2`
- target grain: one Amsterdam ICU-semantic local admission
- anchor: current ICU-semantic local admission `dischargedat`
- future event: first later same-patient Amsterdam ICU-semantic local admission with `admittedat > current dischargedat`
- unit: days
- retained primary value field: `std_days_to_next_icu_admission`

## Evidence Package

Public governed artifacts:

- `docs/standard_system_mvp/std_days_to_next_icu_admission/variable_spec.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/mapping_spec_amsterdamumcdb_1_0_2.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/execution.py`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/manifest.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution/validation_report.json`
- `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_rerun_repro_check/reproducibility_report.json`

Local evidence:

- `Methods/Clinical_Database/local_work/Layer 2/AmsterdamUMCdb-1.0.2/reviewed_unsplit/admissions_core.parquet`
- `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/outcomes/std_days_to_next_icu_admission/std_days_to_next_icu_admission_long.parquet`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_days_to_next_icu_admission/asset_manifest.md`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_days_to_next_icu_admission/query_summary`
- `Methods/Clinical_Database/local_work/Layer 5/AmsterdamUMCdb-1.0.2/std_days_to_next_icu_admission/Layer5_PerVariable_KnowledgePackage.xlsx`

Pre-approval boundary review:

- `docs/standard_system_mvp/AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md`

Existing sibling approval:

- `docs/standard_system_mvp/STD_DAYS_TO_NEXT_ICU_MCU_ADMISSION_AMSTERDAM_FORMAL_APPROVAL_REVIEW.md`

## Runtime Evidence

Amsterdam first governed execution:

- runtime directory: `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_first_real_execution`
- process batch id: `20260502T060015Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_admission`
- runtime validation: pass

Amsterdam rerun reproducibility execution:

- runtime directory: `docs/standard_system_mvp/std_days_to_next_icu_admission/runtime/amsterdamumcdb_1_0_2_rerun_repro_check`
- process batch id: `20260502T060021Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_admission`
- runtime validation: pass
- reproducibility report: pass

MIMIC public mapping compatibility:

- `mapping_spec_mimic_iv_3_1.json` passed governed validate-only checks under the same public `execution.py`
- the existing MIMIC local approval remains the prior content basis for `MIMIC-IV-3.1`
- this review adds Amsterdam same-name approval rather than re-opening the MIMIC content decision

## Output Summary

Retained Amsterdam ICU-only output:

- total rows: `18386`
- unique `subject_id`: `16518`
- unique `stay_id`: `18386`
- observed next ICU local admission rows: `1860`
- missing duration rows: `16526`
- no later ICU local admission observed rows: `16526`
- unresolved missing `dischargedat` rows: `0`
- excluded MC-only rows: `4720`

Observed duration distribution:

- minimum days: `0.001`
- median days: `9.289`
- p95 days: `1609.622`
- maximum days: `4187.087`
- negative or zero observed duration rows: `0`

Death-context fields:

- `death_before_next_icu_admission_flag` rows: `22`
- `no_next_death_after_discharge_flag` rows: `3129`

These death fields are approved only as context flags.

They are not the primary ordering rule.

## Source Scope

Approved Amsterdam ICU-semantic scope:

- `IC`
- `IC&MC`
- `MC&IC`

Excluded Amsterdam scope:

- `MC`

This exclusion is the core reason this approval can use the existing same-name `std_days_to_next_icu_admission` identity.

The MC-inclusive Amsterdam local-admission timing output remains under `std_days_to_next_icu_mcu_admission`.

## Boundary Decisions

Hospital-level boundary:

- not approved as `std_days_to_next_hospital_admission`
- Amsterdam still lacks a governed hospital admission/discharge bridge under the current opening layer
- raw `admissionid` remains a local ICU/MCU stay-equivalent key, not a canonical hospital encounter identifier

ICU/MCU split boundary:

- this review approves ICU-only same-name Amsterdam mapping
- MC-only rows must not be retained in this same-name output
- MC-inclusive timing must remain under `std_days_to_next_icu_mcu_admission`

Null semantics:

- null retained value means no later Amsterdam ICU-semantic local admission was observed after current local discharge
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

`std_days_to_next_icu_admission` is approved for `AmsterdamUMCdb-1.0.2`.

The approval is bounded to Amsterdam ICU-semantic local-admission timing, source-observed follow-up, strict post-discharge future admission selection, nullable retained duration, and explicit separation from both hospital-level next-admission timing and MC-inclusive ICU/MCU local-admission timing.
