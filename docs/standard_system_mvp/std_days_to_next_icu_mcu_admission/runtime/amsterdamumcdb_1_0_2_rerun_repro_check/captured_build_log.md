# Build Log: std_days_to_next_icu_mcu_admission

- `process_batch_id`: `20260502T052846Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_mcu_admission`
- `database_id`: `AmsterdamUMCdb-1.0.2`
- `source_table`: `admissions_core`
- `source_scope`: `IC, MC, IC&MC, MC&IC`
- `anchor`: `current dischargedat`
- `future_event`: `first later same-patient Amsterdam ICU/MCU local admission with admittedat > current dischargedat`

## Build Summary

- `process_batch_id`: `20260502T052846Z_AmsterdamUMCdb-1.0.2_std_days_to_next_icu_mcu_admission`
- `total_rows`: `23106`
- `unique_subject_id`: `20109`
- `unique_stay_id`: `23106`
- `observed_rows`: `2967`
- `missing_rows`: `20139`
- `no_later_icu_mcu_admission_observed_rows`: `20139`
- `unresolved_missing_dischargedat_rows`: `0`
- `min_days`: `0.001`
- `p50_days`: `12.838`
- `p95_days`: `1592.307`
- `max_days`: `4531.061`
- `negative_or_zero_observed_duration_rows`: `0`
- `death_before_next_icu_mcu_admission_flag_rows`: `31`
- `no_next_death_after_discharge_flag_rows`: `3974`

## Approval Boundary

- This build is Amsterdam-only and uses the split ICU/MCU identity.
- It must not be interpreted as `std_days_to_next_hospital_admission`.
- It must not be collapsed into same-name `std_days_to_next_icu_admission` while MC-only rows remain in scope.
