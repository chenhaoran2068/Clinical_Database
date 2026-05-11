# Build Log: std_non_crrt_rrt_active

- `process_batch_id`: `20260502T112847Z_AmsterdamUMCdb-1.0.2_std_non_crrt_rrt_active`
- `database_id`: `AmsterdamUMCdb-1.0.2`
- `row_count`: `57`
- `unique_stay_id`: `46`
- `valid_source_row_count`: `58`
- `invalid_timing_source_row_count`: `0`

## Boundary

- Amsterdam opening mapping is hemodialysis-only for non-CRRT active support; peritoneal active intervals are not proven by processitems.
- Peritoneaal catheter is access evidence, not peritoneal dialysis active interval evidence.
- Peritoneaaldialyse numeric volume rows remain fluid/event evidence and are not active-state intervals in this opening mapping.
