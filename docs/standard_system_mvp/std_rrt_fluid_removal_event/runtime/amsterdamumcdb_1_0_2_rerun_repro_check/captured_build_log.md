# Build Log: std_rrt_fluid_removal_event

- `process_batch_id`: `20260502T131511Z_AmsterdamUMCdb-1.0.2_std_rrt_fluid_removal_event`
- `database_id`: `AmsterdamUMCdb-1.0.2`
- `status`: `reviewed_approved`
- `approved_scope`: `Amsterdam numericitems itemid 8805 and 8806 only`

## Boundary

- This is a formal Amsterdam same-name approved source-event-primary execution.
- Rate settings, cumulative counters, access lines, active flags, modality episodes, urine output, and total output are excluded.
- Parent-link absence is retained as a caution rather than silently filtering rows out.

## Summary

- `row_count`: `98695`
- `unique_subject_id`: `937`
- `unique_stay_id`: `1019`
- `approved_itemid_8805_row_count`: `98383`
- `approved_itemid_8806_row_count`: `312`
- `rows_with_parent_link`: `86376`
- `rows_without_parent_link`: `12319`
- `negative_value_caution_row_count`: `6`
- `extreme_value_caution_row_count`: `6`
- `event_before_admission_anchor_caution_row_count`: `1`
- `event_after_discharge_caution_row_count`: `1`
- `fluid_removed_volume_ml_total`: `15466790.0`
- `counts_by_itemid`: `{'8805': 98383, '8806': 312}`
- `counts_by_event_name`: `{'cvvh_removed_volume': 98383, 'hemodialysis_removed_volume': 312}`
- `parent_link_status_counts`: `{'linked_to_approved_parent_episode': 86376, 'missing_expected_parent_episode_overlap': 12319}`
- `volume_by_event_name`: `{'cvvh_removed_volume': 14994976.0, 'hemodialysis_removed_volume': 471814.0}`
