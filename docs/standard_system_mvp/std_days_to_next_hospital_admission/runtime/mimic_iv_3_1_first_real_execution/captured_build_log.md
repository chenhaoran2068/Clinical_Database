# Build Log: std_days_to_next_hospital_admission

- `process_batch_id`: `20260501T170538Z_MIMIC-IV-3.1_std_days_to_next_hospital_admission`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`
- `owner`: `ChenHR`
- `contract_approved_by`: `ChenHR`
- `contract_approved_at`: `2026-03-26`

## Build Summary

- `max_days`: `5340.54`
- `min_days`: `0.001`
- `missing_rows`: `224467`
- `observed_rows`: `321561`
- `p50_days`: `85.111`
- `p95_days`: `1774.269`
- `total_rows`: `546028`
- `unique_hadm_id`: `546028`

## Distribution Snapshot

- `observed_gap_days_summary`: `{"observed_rows": 321561, "missing_rows": 224467, "min": 0.001, "p50": 85.111, "p95": 1774.269, "max": 5340.54}`

## Source Audit Snapshot

- `source_tables`: `["hosp_admissions"]`
- `search_rule`: `"first later different hospitalization with admittime > current dischtime"`
- `rows_with_missing_dischtime`: `0`
- `self_match_rows_prevented`: `175`
- `pure_admittime_order_nonpositive_next_total`: `2131`
- `pure_admittime_order_zero_gap_rows`: `2083`
- `pure_admittime_order_negative_gap_rows`: `48`
- `valid_post_discharge_next_recovered_after_nonpositive_rows`: `1116`
- `no_valid_post_discharge_next_after_nonpositive_rows`: `1015`
- `observed_next_hospital_admission_rows`: `321561`
- `no_observed_next_hospital_admission_rows`: `224467`
- `hospital_expire_flag_one_with_observed_30d_readmission_rows`: `2`
- `observed_gap_days_summary_raw`: `{"observed_rows": 321561, "missing_rows": 224467, "min": 0.0006944444444444445, "p50": 85.11111111111111, "p95": 1774.2694444444444, "max": 5340.540277777777}`
- `observed_30d_rate_all_admissions`: `0.19698623513812477`
- `observed_30d_rate_discharge_alive`: `0.20133388990073509`
