# Build Log: std_oasis

- `process_batch_id`: `20260502T145059Z_MIMIC-IV-3.1_std_oasis`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- source score table: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/oasis.parquet`
- ICU anchor table: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- official score SQL: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/score/oasis.sql`

## Retained Rule Summary

- source rule summary: `official_mimic_oasis_sql_first_day_icu_summary`
- retain one row per `stay_id`
- retained time semantics label: `icu_first_day_window`
- primary standardized score column: `std_oasis_total`
- approved primary score range: `[0, 100]`
- retain official same-row context columns on the same standardized row

## Output Summary

- total rows: `94458`
- unique subject_id: `65366`
- unique hadm_id: `85242`
- unique stay_id: `94458`
- main score min: `6.0`
- main score max: `72.0`
