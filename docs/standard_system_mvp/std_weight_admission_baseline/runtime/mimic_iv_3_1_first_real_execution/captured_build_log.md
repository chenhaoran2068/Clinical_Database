# Build Log: std_weight_admission_baseline

- `process_batch_id`: `20260425T045645Z_MIMIC-IV-3.1_std_weight_admission_baseline`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Upstream Dependency

- source event asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/anthropometrics/std_weight_event/std_weight_event_long.parquet`
- only `cleaning_status = kept` rows are eligible for baseline derivation

## Approved Baseline Contract Used

- anchor = `hosp.admissions.admittime`
- candidate window = `[admittime, min(dischtime, admittime + 1440 minutes)]`
- selection = smallest absolute time distance to anchor
- tie-break 1 = source priority `admission_weight_kg > admission_weight_lbs > daily_weight_kg`
- tie-break 2 = earlier measurement time
- `baseline_offset_minutes` keeps integer minutes; exact `0` stays `0`, other values round away from `0`

## Validation Summary

- total rows: `69312`
- unique hadm_id: `69312`
- all admissions coverage rows: `69312` of `546028`
- all admissions coverage rate: `0.126939`
- ICU admissions coverage rows: `69312` of `85242`
- ICU admissions coverage rate: `0.81312`
- selected `admission_weight_kg` rows: `68048`
- selected `admission_weight_lbs` rows: `268`
- selected `daily_weight_kg` rows: `996`
