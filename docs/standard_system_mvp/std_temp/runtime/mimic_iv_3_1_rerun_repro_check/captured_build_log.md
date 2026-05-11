# Build Log: std_temp

- `process_batch_id`: `20260503T102123Z_MIMIC-IV-3.1_std_temp`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- source split asset Fahrenheit: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/split_cleaned/icu_chartevents_itemid_tables/chartevents_itemid_223761_temperature_fahrenheit`
- source split asset Celsius: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/split_cleaned/icu_chartevents_itemid_tables/chartevents_itemid_223762_temperature_celsius`
- source split asset site context: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/split_cleaned/icu_chartevents_itemid_tables/chartevents_itemid_224642_temperature_site`
- icustays: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- d_items: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_d_items.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/icu/chartevents/index.txt`

## Current Retained Contract Used

- asset shape: event-level measurement asset
- retained source scope: ICU chartevents itemids 223761 + 223762 only
- exact-key duplicate rule: prefer source Celsius over converted Fahrenheit
- raw context enrichment: retain exact-key Temperature Site when available
- standard unit: `degrees_celsius`
- retained standardized / cleaned precision: `round(1)`
- rounding rule: half away from zero
- current cleaned-value kept range: `[25.0, 45.0] degrees_celsius`
- anchor type: `icu_intime`
- relative time unit: `minutes`
- stay linkage: `direct_stay`

## Validation Summary

- source rows before exact-key deduplication: `2449883`
- exact-key rows removed during Celsius-priority deduplication: `3416`
- total rows retained after deduplication: `2446467`
- unique subject_id: `65004`
- unique hadm_id: `84768`
- unique stay_id: `93632`
- kept rows: `2444580`
- excluded_outlier rows: `1887`
- warning=true rows: `35643`
- warning=true and outlier rows: `42`
- rows kept from source itemid 223761: `2051624`
- rows kept from source itemid 223762: `394843`
- exact-key site matches: `2332968`
- exact-key site match rate: `0.953607`
- normalized min: `-73.3`
- normalized max: `130050.6`
- kept p1: `35.2`
- kept p50: `36.9`
- kept p99: `39.0`
- kept p99.9: `39.7`
- rows before intime: `13859`
- rows after outtime: `1302`
- relative_time_value min: `-525596` minutes
- relative_time_value max: `531096` minutes
