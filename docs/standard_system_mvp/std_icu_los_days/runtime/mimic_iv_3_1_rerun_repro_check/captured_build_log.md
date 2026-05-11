# Build Log: std_icu_los_days

- `process_batch_id`: `20260425T035753Z_MIMIC-IV-3.1_std_icu_los_days`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`
- `owner`: `ChenHR`
- `contract_approved_by`: `ChenHR`
- `contract_approved_at`: `2026-03-25`

## Build Summary

- `max_days_raw`: `226.4030787037037`
- `min_days_raw`: `0.00125`
- `missing_outtime_rows`: `14`
- `observed_rows`: `94444`
- `total_rows`: `94458`
- `unique_stay_id`: `94458`

## Distribution Snapshot

```json
{
  "icu_los_observation_status_counts": {
    "missing_outtime": 14,
    "observed": 94444
  },
  "std_icu_los_days_summary": {
    "min": 0.001,
    "p01": 0.209,
    "p50": 1.966,
    "p99": 26.43856999999999,
    "max": 226.403
  }
}
```

## Source Audit Snapshot

```json
{
  "main_source": "icu_icustays.los",
  "direct_time_difference_audit_mismatch_rows": 0,
  "icustay_detail_reference_source": "source_supplied_derived.icustay_detail.los_icu",
  "icustay_detail_vs_full_precision_diff_rows": 94341,
  "note": "icustay_detail.los_icu is a rounded reference representation rather than the full-precision primary field."
}
```
