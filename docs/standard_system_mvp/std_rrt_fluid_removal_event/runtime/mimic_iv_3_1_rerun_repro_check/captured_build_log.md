# Build Log: std_rrt_fluid_removal_event

- `process_batch_id`: `20260502T131539Z_MIMIC-IV-3.1_std_rrt_fluid_removal_event`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- approved parent RRT umbrella: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/treatment_state/std_rrt_active/std_rrt_active_long.parquet`
- approved CRRT parameter source: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/device_support/std_crrt_device_parameter_event/std_crrt_device_parameter_event_long.parquet`
- approved non-CRRT support-state source: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/treatment_state/std_non_crrt_rrt_active/std_non_crrt_rrt_active_long.parquet`
- official RRT SQL reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts_postgres/treatment/rrt.sql`
- official CRRT SQL reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts_postgres/treatment/crrt.sql`

## Approved Retained Contract

- evidence class: `RRT extracorporeal fluid-removal bridge event`
- this bridge does not rewrite the approved measured-charted ICU balance trio; it provides additive extracorporeal-removal evidence for downstream join or augmentation
- CRRT-side default bridge source is the approved `hourly_patient_fluid_removal_volume` from `std_crrt_device_parameter_event`
- `ultrafiltrate_output_volume` is retained as context-only specialized evidence and does not enter the opening default bridge numerator
- non-CRRT default bridge source is `226499 Hemodialysis Output` overlapping approved `std_non_crrt_rrt_active` episodes
- `225806 Volume In (PD)` and `225807 Volume Out (PD)` are retained as peritoneal-dialysis context-only rows in opening v1 and do not enter the default bridge numerator
- event timestamps remain source-faithful `charttime` records; opening v1 does not back-shift retrospective removal charting to an inferred prior-hour interval
- opening v1 deliberately avoids claiming complete extracorporeal output truth for all non-CRRT modalities; it remains a conservative bridge layer

## Validation Summary

- row_count: `702910`
- unique_stay_id: `4418`
- default_bridge_row_count: `338554`
- context_only_row_count: `364356`
- default_bridge_eligible_volume_ml: `130066286.79`
- fluid_removal_event_name_counts: `{'hemodialysis_output_volume': 3307, 'machine_hourly_patient_removal_volume': 335247, 'peritoneal_dialysis_volume_in_context': 1669, 'peritoneal_dialysis_volume_out_context': 1456, 'ultrafiltrate_output_volume_context': 361231}`
- fluid_removal_event_name_volume_ml: `{'hemodialysis_output_volume': 6350804.09, 'machine_hourly_patient_removal_volume': 123623777.7, 'peritoneal_dialysis_volume_in_context': 3212390.0, 'peritoneal_dialysis_volume_out_context': 3094315.0, 'ultrafiltrate_output_volume_context': 127242738.49999996}`
- source_rrt_family_class_counts: `{'crrt_family': 696478, 'non_crrt_rrt': 6432}`

## Semantic Cautions

- This bridge is an extracorporeal-removal augmentation layer, not a replacement for the approved measured charted ICU balance foundation.
- `machine_hourly_patient_removal_volume` is suitable as an extracorporeal-removal bridge component but still does not, by itself, equal whole-body cumulative fluid balance.
- `hemodialysis_output_volume` is often charted as a single end-of-session removal total for an intermittent dialysis course rather than a physiologically smooth hour-by-hour removal stream.
- Source `charttime` for removal rows may represent retrospective charting of prior removal, so downstream hour-level smoothing or episode-level redistribution remains a separate modeling choice rather than an opening bridge rule.
- `ultrafiltrate_output_volume_context` and the peritoneal-dialysis volume rows are retained as context-only evidence in opening v1 and must not be silently promoted into the default bridge numerator.
- Opening v1 keeps nonnegative numeric eligibility explicit; negative raw source rows remain visible through caution fields rather than silently disappearing.
