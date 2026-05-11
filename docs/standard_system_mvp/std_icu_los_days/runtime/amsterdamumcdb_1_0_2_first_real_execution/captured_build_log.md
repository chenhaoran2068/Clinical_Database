# Build Log: std_icu_los_days

- process_batch_id: `20260425T035814Z_AmsterdamUMCdb-1.0.2_std_icu_los_days`
- built_at_utc: `2026-04-25T03:58:14Z`
- database_id: `AmsterdamUMCdb-1.0.2`
- asset_status: `reviewed_approved`
- source_table: `admissions_core`
- source_scope_locations: `IC, IC&MC, MC&IC`
- excluded_locations_for_same_name_contract: `MC`
- output_asset: `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/outcomes/std_icu_los_days/std_icu_los_days_long.parquet`
- total_rows: `18386`
- unique_patients: `16518`
- zero_duration_rows: `3`
- negative_duration_rows: `0`
- p50_days_raw: `1.244097`
- p99_days_raw: `52.705938`
- p50_abs_diff_hours: `0.300000`
- p90_abs_diff_hours: `0.700000`

## Semantic Caution

- This same-name ICU LOS asset excludes Amsterdam `MC`-only admissions by design.
- The retained value uses raw offsets from `admittedat` and `dischargedat`.
- `lengthofstay` is a source-supplied reported summary field and remains audit-only in this asset.
- The official AmsterdamUMCdb paper ICU LOS summary is exactly reproduced by `lengthofstay / 24`, but this retained asset intentionally keeps raw offsets as the primary value.
