# Build Log: std_spo2

- `process_batch_id`: `20260503T102001Z_MIMIC-IV-3.1_std_spo2`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- source split asset: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/split_cleaned/icu_chartevents_itemid_tables/chartevents_itemid_220277_o2_saturation_pulseoxymetry`
- icustays: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_icustays.parquet`
- d_items: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/icu_d_items.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/icu/chartevents/index.txt`

## Source Item Metadata

- retained itemid: `220277`
- retained label: `O2 saturation pulseoxymetry`
- retained category: `Respiratory`
- retained linksto: `chartevents`
- retained source unit: `%`
- retained param_type: `Numeric`
- explicitly excluded itemid from std_spo2: `220227`

## Current Retained Contract Used

- asset shape: event-level measurement asset
- retained source scope: ICU chartevents itemid `220277` only
- explicitly excluded concept family: itemid `220227` arterial O2 saturation (SaO2)
- ED o2sat fields are intentionally excluded from this first build
- standard unit: `percent`
- retained standardized / cleaned precision: `integer`
- rounding rule: nearest integer, half away from zero
- current cleaned-value kept range: `[1, 100] percent`
- anchor type: `icu_intime`
- relative time unit: `minutes`
- stay linkage: `direct_stay`

## Validation Summary

- total rows: `8567015`
- unique subject_id: `65304`
- unique hadm_id: `85146`
- unique stay_id: `94306`
- kept rows: `8566275`
- excluded_outlier rows: `740`
- warning=true rows: `29117`
- warning=true and outlier rows: `58`
- non-integer raw rows: `18`
- exact event-key duplicate rows: `0`
- normalized min: `-951234`
- normalized max: `9900000`
- raw < 0 rows: `7`
- raw < 1 rows: `578`
- raw = 0 rows: `566`
- raw < 50 rows: `3087`
- raw < 70 rows: `11179`
- raw > 100 rows: `164`
- raw > 105 rows: `163`
- kept < 88 rows: `91260`
- kept < 90 rows: `165649`
- kept = 100 rows: `1826096`
- p1 raw: `87.0`
- p50 raw: `97.0`
- p99 raw: `100.0`
- p99.9 raw: `100.0`
- rows before intime: `28980`
- rows after outtime: `2757`
- relative_time_value min: `-525596` minutes
- relative_time_value max: `531096` minutes

## Semantic Cautions

- This asset is SpO2 only and must not be interpreted as SaO2.
- This asset is event-level and should not be interpreted as a baseline oxygen-saturation asset.
- ED oxygen-saturation fields are intentionally excluded from this first retained build.
- The cleaned-value threshold preserves severe but plausible low saturations while excluding values below 1 percent and above 100 percent.
