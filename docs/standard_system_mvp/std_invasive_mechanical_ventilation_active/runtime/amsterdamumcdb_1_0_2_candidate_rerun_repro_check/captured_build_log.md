# Amsterdam Candidate Build Log

- variable_id: `std_invasive_mechanical_ventilation_active`
- database_id: `AmsterdamUMCdb-1.0.2`
- status: `candidate_only_not_reviewed_approved`
- process_batch_id: `20260501T155259Z_AmsterdamUMCdb-1.0.2_std_invasive_mechanical_ventilation_active`
- generated_at: `2026-05-01T15:52:59Z`

## Candidate Boundary

- retains `retain_candidate` rows
- retains `retain_candidate_with_flag` rows with visible weaning flag
- excludes manual-review rows under the accepted conservative first-pass policy
- withholds possible transition rows from this first-pass candidate
- excludes invalid timing rows

## Build Summary

- duration_minutes_max: `248286`
- duration_minutes_min: `1`
- duration_minutes_p50: `832`
- duration_minutes_p95: `23013.199999999968`
- invalid_timing_excluded: `1`
- manual_policy_excluded: `205`
- manual_policy_withheld_possible_transition: `6`
- manual_review_rows: `211`
- output_rows: `18259`
- process_batch_id: `20260501T155259Z_AmsterdamUMCdb-1.0.2_std_invasive_mechanical_ventilation_active`
- prolonged_episode_ge_7d: `2465`
- retained_clean: `18061`
- retained_with_weaning_flag: `198`
- short_episode_le_60m: `285`
- source_rows: `18471`
- status: `candidate_only_not_reviewed_approved`
- total_not_retained_first_pass: `212`
- unique_stay_id: `15879`
- weaning_flagged_output_rows: `198`
