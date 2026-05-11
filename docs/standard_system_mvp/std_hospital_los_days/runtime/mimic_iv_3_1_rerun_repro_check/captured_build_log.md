# Build Log: std_hospital_los_days

- `process_batch_id`: `20260428T124519Z_MIMIC-IV-3.1_std_hospital_los_days`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`
- `owner`: `ChenHR`
- `contract_approved_by`: `ChenHR`
- `contract_approved_at`: `2026-03-25`

## Build Summary

- `max_days_raw`: `515.5625`
- `min_days_raw`: `-0.9451388888888889`
- `negative_duration_rows`: `175`
- `nonnegative_duration_rows`: `545853`
- `total_rows`: `546028`
- `unique_hadm_id`: `546028`
- `zero_duration_rows`: `5`

## Distribution Snapshot

```json
{
  "hospital_los_validity_status_counts": {
    "negative_duration": 175,
    "nonnegative_duration": 545853
  },
  "std_hospital_los_days_summary": {
    "min": -0.945,
    "p01": 0.11,
    "p50": 2.818,
    "p99": 33.92037999999989,
    "max": 515.563
  }
}
```

## Source Audit Snapshot

```json
{
  "main_source": "computed_from_hosp_admissions_admittime_and_dischtime",
  "official_subset_audit_source": "source_supplied_derived.icustay_detail.los_hospital",
  "icu_linked_comparable_rows": 94458,
  "icu_linked_mismatch_rows": 0,
  "note": "The admissions table has no direct los column; icustay_detail provides an ICU-linked subset audit only."
}
```
