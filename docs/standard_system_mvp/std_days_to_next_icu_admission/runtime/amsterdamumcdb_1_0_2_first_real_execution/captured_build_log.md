# Build Log: std_days_to_next_icu_admission

- `process_batch_id`: `20260502T060015Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_admission`
- `database_id`: `AmsterdamUMCdb-1.0.2`
- `source_table`: `admissions_core`
- `source_scope`: `IC, IC&MC, MC&IC`
- `excluded_same_name_scope`: `MC`
- `anchor`: `current dischargedat`
- `future_event`: `first later same-patient Amsterdam ICU-semantic local admission with admittedat > current dischargedat`

## Build Summary

- `process_batch_id`: `20260502T060015Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_admission`
- `total_rows`: `18386`
- `unique_subject_id`: `16518`
- `unique_stay_id`: `18386`
- `observed_rows`: `1860`
- `missing_rows`: `16526`
- `no_next_icu_admission_observed_rows`: `16526`
- `unresolved_missing_outtime_rows`: `0`
- `excluded_mc_only_rows`: `4720`
- `min_days`: `0.001`
- `p50_days`: `9.289`
- `p95_days`: `1609.622`
- `max_days`: `4187.087`
- `negative_or_zero_observed_duration_rows`: `0`
- `death_before_next_icu_admission_flag_rows`: `22`
- `no_next_death_after_discharge_flag_rows`: `3129`

## Approval Boundary

- This build is an Amsterdam same-name ICU-only mapping.
- It must not be interpreted as `std_days_to_next_hospital_admission`.
- It must not include MC-only rows; MC-inclusive timing belongs to `std_days_to_next_icu_mcu_admission`.
