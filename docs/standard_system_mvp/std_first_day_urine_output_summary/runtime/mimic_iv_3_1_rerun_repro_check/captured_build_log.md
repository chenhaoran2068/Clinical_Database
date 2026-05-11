# Build Log: std_first_day_urine_output_summary

- `process_batch_id`: `20260425T110817Z_MIMIC-IV-3.1_std_first_day_urine_output_summary`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- upstream official-compatible urine child: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/supportive_therapy/std_icu_urine_output_event/std_icu_urine_output_event_long.parquet`
- ICU stay timing source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- official reference SQL: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts_postgres/firstday/first_day_urine_output.sql`
- official reference parquet: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/first_day_urine_output.parquet`

## Approved Retained Contract

- evidence class: `official-compatible first-day ICU urine-output summary`
- derive from the approved `std_icu_urine_output_event` child asset rather than raw outputevents
- use the official first-day window exactly: `charttime >= intime` and `charttime <= intime + 24h`
- preserve official-style nullability: if no first-day urine row exists, keep `first_day_urine_output_ml = NULL`
- retain per-stay timing context fields and explicit observed-window cautions without changing the official aggregation numerator

## Validation Summary

- row_count: `94458`
- stays_with_first_day_urine: `89442`
- stays_without_first_day_urine: `5016`
- total_first_day_urine_output_ml: `152814080.4930113`
- official_compare_exact_match_rows: `94458`
- official_compare_official_only_rows: `0`
- official_compare_local_only_rows: `0`
- official_compare_subject_mismatch_rows: `0`
- official_compare_value_mismatch_rows: `0`

## Semantic Cautions

- This first-day summary keeps official NULL behavior for stays without any qualifying first-day urine row and does not force missing to zero.
- The official first-day window is not clipped by ICU outtime in the aggregation rule; retained partial-window flags are advisory context rather than numerator edits.
- `urine_output_rate` logic remains intentionally deferred because it requires additional weight and time-window handling beyond this opening child line.
