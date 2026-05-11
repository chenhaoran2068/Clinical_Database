# Build Log: std_heart_rate

- `process_batch_id`: `20260424T103651Z_MIMIC-IV-3.1_std_heart_rate`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- source split asset: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/split_cleaned/icu_chartevents_itemid_tables/chartevents_itemid_220045_heart_rate`
- icustays: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- d_items: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_d_items.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/icu/chartevents/index.txt`

## Source Item Metadata

- itemid: `220045`
- label: `Heart Rate`
- category: `Routine Vital Signs`
- linksto: `chartevents`
- source unit: `bpm`
- param_type: `Numeric`

## Current Retained Contract Used

- asset shape: event-level measurement asset
- standard unit: `bpm`
- retained standardized / cleaned precision: `integer`
- rounding rule: nearest integer, half away from zero
- current cleaned-value kept range: `[0, 250] bpm`
- anchor type: `icu_intime`
- relative time unit: `minutes`
- stay linkage: `direct_stay`

## Validation Summary

- total rows: `8752069`
- unique subject_id: `65365`
- unique hadm_id: `85240`
- unique stay_id: `94437`
- kept rows: `8752005`
- excluded_outlier rows: `64`
- warning=true rows: `37514`
- warning=true and outlier rows: `16`
- non-integer raw rows: `68`
- normalized min: `-241395`
- normalized max: `10000000`
- p1 raw: `50.0`
- p50 raw: `85.0`
- p99 raw: `136.0`
- p99.9 raw: `160.0`
- rows before intime: `30494`
- rows after outtime: `2961`
- relative_time_value min: `-525596` minutes
- relative_time_value max: `531096` minutes

## Semantic Cautions

- This asset is event-level and should not be interpreted as a baseline heart-rate asset.
- Some direct stay-linked heart-rate rows have charttime outside the documented stay window; they are retained and logged rather than silently deleted.
- The cleaned-value threshold was revised to `[0, 250] bpm` after user approval so 0 bpm can be retained for cardiac-arrest or active-resuscitation contexts.
