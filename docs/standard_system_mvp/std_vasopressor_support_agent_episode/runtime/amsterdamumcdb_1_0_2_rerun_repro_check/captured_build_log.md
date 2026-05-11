# Build Log: std_vasopressor_support_agent_episode

- process_batch_id: `20260504T021920Z_AmsterdamUMCdb-1.0.2_std_vasopressor_support_agent_episode`
- database_id: `AmsterdamUMCdb-1.0.2`
- status: `built_runtime_repro_pass_owner_approval_pending`
- row_count: `26616`
- unique_stay_id: `13487`
- layer3_asset_path: `Methods/Clinical_Database/local_work/Layer 3/AmsterdamUMCdb-1.0.2/treatment_state/std_vasopressor_support_agent_episode/std_vasopressor_support_agent_episode_long.parquet`

## Boundary

- Positive child agent episodes are linked to the parent std_vasopressor_support_active Amsterdam asset.
- Agent labels are retained from approved Amsterdam drugitems itemids; terlipressin is retained as terlipressin, not silently converted to vasopressin.
- Pure inotrope, bolus-only, topical/non-IV, screening, dose-equivalent, and shock-phenotype semantics are excluded.
