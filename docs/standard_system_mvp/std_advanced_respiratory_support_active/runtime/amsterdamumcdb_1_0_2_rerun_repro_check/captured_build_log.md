# Build Log: std_advanced_respiratory_support_active

- process_batch_id: `20260504T021920Z_AmsterdamUMCdb-1.0.2_std_advanced_respiratory_support_active`
- database_id: `AmsterdamUMCdb-1.0.2`
- status: `built_candidate_hfnc_source_gap_owner_approval_pending`
- row_count: `22630`
- unique_stay_id: `16428`
- layer3_asset_path: `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_advanced_respiratory_support_active/std_advanced_respiratory_support_active_long.parquet`

## Boundary

- Positive-only rows only; no false rows are emitted.
- The Amsterdam output is derived from already governed Amsterdam parent support assets.
- IMV parent scope is std_invasive_mechanical_ventilation_active; NIV parent scope is std_noninvasive_ventilation_active.
- HFNC is part of the public advanced-respiratory-support concept but is not sourced in Amsterdam; owner approval is blocked until this gap is adjudicated.
