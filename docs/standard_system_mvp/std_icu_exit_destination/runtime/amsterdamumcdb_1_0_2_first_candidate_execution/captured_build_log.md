# Build Log: std_icu_exit_destination

- process_batch_id: `20260504T021858Z_AmsterdamUMCdb-1.0.2_std_icu_exit_destination`
- database_id: `AmsterdamUMCdb-1.0.2`
- status: `built_candidate_destination_code_dictionary_pending_owner_approval`
- row_count: `22886`
- unique_stay_id: `22886`
- layer3_asset_path: `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/encounter_information/std_icu_exit_destination/std_icu_exit_destination_long.parquet`

## Boundary

- Rows with null source values are not emitted in this first candidate asset.
- Amsterdam admissionid is normalized to stay_id; hadm_id is not separately available in the current opening mapping.
- This build is not owner-approved; it is candidate runtime evidence for later detailed review.
- Numeric Amsterdam destination codes remain local coded values pending official code-dictionary adjudication.
