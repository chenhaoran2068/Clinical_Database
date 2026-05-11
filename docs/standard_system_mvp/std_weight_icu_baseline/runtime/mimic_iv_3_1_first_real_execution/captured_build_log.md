# Build Log: std_weight_icu_baseline

- `process_batch_id`: `20260426T022944Z_MIMIC-IV-3.1_std_weight_icu_baseline`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Upstream Dependency

- source event asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/anthropometrics/std_weight_event/std_weight_event_long.parquet`
- only `cleaning_status = kept` rows are eligible for baseline derivation

## Approved Baseline Contract Used

- anchor = `icu.icustays.intime`
- candidate window = `[max(admittime, icu_intime - 360 minutes), min(icu_outtime, dischtime, icu_intime + 360 minutes)]`
- selection = smallest absolute time distance to anchor
- tie-break 1 = source priority `admission_weight_kg > admission_weight_lbs > daily_weight_kg`
- tie-break 2 = earlier measurement time
- `baseline_offset_minutes` keeps integer minutes; exact `0` stays `0`, other values round away from `0`

## Validation Summary

- total rows: `88690`
- unique stay_id: `88690`
- all stays coverage rows: `88690` of `94458`
- all stays coverage rate: `0.938936`
- selected `admission_weight_kg` rows: `65549`
- selected `admission_weight_lbs` rows: `16448`
- selected `daily_weight_kg` rows: `6693`
