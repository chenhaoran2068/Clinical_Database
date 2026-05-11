# Build Log: std_respiratory_rate

- `process_batch_id`: `20260503T101314Z_MIMIC-IV-3.1_std_respiratory_rate`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- source split asset: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/split_cleaned/icu_chartevents_itemid_tables/chartevents_itemid_220210_respiratory_rate`
- icustays: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- d_items: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_d_items.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/icu/chartevents/index.txt`

## Current Retained Contract Used

- asset shape: event-level measurement asset
- standard unit: `breaths_per_minute`
- retained standardized / cleaned precision: `integer`
- rounding rule: nearest integer, half away from zero
- current cleaned-value kept range: `[0, 80] breaths_per_minute`
- anchor type: `icu_intime`
- relative time unit: `minutes`
- stay linkage: `direct_stay`

## Validation Summary

- total rows: `8636655`
- unique subject_id: `65302`
- unique hadm_id: `85156`
- unique stay_id: `94334`
- kept rows: `8636179`
- excluded_outlier rows: `476`
- warning=true rows: `20045`
- warning=true and outlier rows: `9`
- non-integer raw rows: `4`
- normalized min: `0`
- normalized max: `7000400`
- p1 raw: `8.0`
- p50 raw: `19.0`
- p99 raw: `37.0`
- p99.9 raw: `48.0`
- rows before intime: `29882`
- rows after outtime: `2889`
- relative_time_value min: `-525596` minutes
- relative_time_value max: `325941` minutes
