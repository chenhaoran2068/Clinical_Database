# Build Log: std_icu_entry_source

- process_batch_id: `20260504T021920Z_AmsterdamUMCdb-1.0.2_std_icu_entry_source`
- database_id: `AmsterdamUMCdb-1.0.2`
- status: `built_runtime_repro_pass_owner_approval_pending`
- row_count: `9031`
- unique_stay_id: `9031`
- layer3_asset_path: `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/encounter_information/std_icu_entry_source/std_icu_entry_source_long.parquet`

## Boundary

- Rows with null source values are not emitted in this first candidate asset.
- Amsterdam admissionid is normalized to stay_id; hadm_id is not separately available in the current opening mapping.
- This build is not owner-approved; it is candidate runtime evidence for later detailed review.
