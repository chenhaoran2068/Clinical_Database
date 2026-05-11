# Build Log: std_first_day_urine_output_summary

- process_batch_id: `20260425T110442Z_AmsterdamUMCdb-1.0.2_std_first_day_urine_output_summary`
- built_at_utc: `2026-04-25T11:04:42Z`
- database_id: `AmsterdamUMCdb-1.0.2`
- asset_status: `reviewed_approved`
- target_scope: `location in (IC, IC&MC, MC&IC)`
- upstream_source: approved Amsterdam `std_icu_urine_output_event`
- row_count: `18386`
- stays_with_first_day_urine: `18115`
- stays_without_first_day_urine: `271`
- total_first_day_urine_output_ml: `33246351.0`
- median_first_day_urine_output_ml: `1670.0`

## Contract Notes

- This summary is derived from the approved event layer, not raw `numericitems`.
- The aggregation window is admission-relative first 24 hours and is not clipped by discharge time.
- MC-only admissions are excluded to preserve the same-name ICU semantic boundary.
- No-source rows are retained with NULL output rather than forced to zero.
