# Build Log: std_sofa

- `process_batch_id`: `20260502T140817Z_MIMIC-IV-3.1_std_sofa`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- source score table: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/sofa.parquet`
- ICU anchor table: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- official score SQL: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/score/sofa.sql`

## Retained Rule Summary

- source rule summary: `official_mimic_sofa_sql_hourly_with_24h_rolling_worst_components`
- dependency summary: `icustay_hourly hourly backbone plus bg, ventilation, vitalsign, gcs, enzyme, chemistry, complete_blood_count, urine_output_rate, and vasoactive-agent concepts`
- retain one row per `stay_id + score_hour_index`
- primary standardized score column: `std_sofa_total_24hours`
- rolling-score semantics: the primary score is the official rolling 24-hour SOFA total at each ICU hour
- same-row official context retained: hourly organ component scores plus rolling 24-hour organ component scores
- source hour-grid semantics: `score_hour_index` and hour timestamps come from official icustay_hourly clock-hours, not exact ICU intime/outtime boundaries

## Output Summary

- total rows: `8219121`
- unique subject_id: `65365`
- unique hadm_id: `85240`
- unique stay_id: `94437`
- main score min: `0`
- main score max: `23`
- partial windows <24h: `2031859`
- full windows =24h: `6187262`
