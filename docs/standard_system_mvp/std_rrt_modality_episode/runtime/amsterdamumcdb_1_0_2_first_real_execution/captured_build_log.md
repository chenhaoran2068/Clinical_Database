# Build Log: std_rrt_modality_episode

- `process_batch_id`: `20260502T112847Z_AmsterdamUMCdb-1.0.2_std_rrt_modality_episode`
- `database_id`: `AmsterdamUMCdb-1.0.2`
- `row_count`: `5313`
- `unique_stay_id`: `1098`
- `valid_source_row_count`: `5413`
- `invalid_timing_source_row_count`: `0`

## Boundary

- Amsterdam opening mapping emits exact modality labels CVVH and IHD and links them back to parent any-RRT and family episodes.
- Peritoneaal catheter is access evidence, not peritoneal dialysis active interval evidence.
- Peritoneaaldialyse numeric volume rows remain fluid/event evidence and are not active-state intervals in this opening mapping.
