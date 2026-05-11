# Build Log: std_noninvasive_ventilation_active

- `process_batch_id`: `20260502T080340Z_MIMIC-IV-3.1_std_noninvasive_ventilation_active`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- direct source asset: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/ventilation.parquet`
- supporting stay anchor map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`
- official SQL reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/treatment/ventilation.sql`
- included source statuses: `NonInvasiveVent`

## Approved Retained Contract

- semantic folder: `treatment_state`
- retain one row per `stay_id + support episode`
- support mode class: `noninvasive_ventilation`
- support definition class: `official_noninvasive_ventilation_episode`
- source status inclusion rule: `include_noninvasivevent_only`
- source rule summary: `direct_filter_of_official_ventilation_where_status_equals_noninvasivevent_v1`
- source gap rule: `official_14h_gap_or_status_change`

## Validation Summary

- output row count: `4833`
- output unique stay count: `2974`
- short episodes `<=60m`: `33`
- prolonged episodes `>=7d`: `2`
- support starts before ICU intime: `106`

## Semantic Cautions

- positive-only support-state episode asset
- retained status scope is limited to: NonInvasiveVent
- absence of a row does not prove absence of all respiratory support
- duration extremes are preserved and surfaced via caution flags
