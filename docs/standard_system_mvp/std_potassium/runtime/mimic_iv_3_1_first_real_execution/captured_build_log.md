# Build Log: std_potassium

- `process_batch_id`: `20260503T094314Z_MIMIC-IV-3.1_std_potassium`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`
- `recorded_at`: `2026-05-03T09:43:14Z`

## Source Inputs

- official chemistry source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/chemistry.parquet`
- raw labevents audit source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_labevents.parquet`
- item dictionary: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_d_labitems.parquet`
- admission map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm/std_id_map_subject_hadm_long.parquet`
- stay map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts_postgres/measurement/chemistry.sql`
- wrapper script: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_potassium/extract_code/Extract_Code_std_potassium.py`
- shared helper: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/shared_extract_code/_chemistry_core_builder.py`

## Source Profiling Snapshot

- raw itemid / label: `50971 / Potassium`
- raw fluid/category: `Blood / Chemistry`
- official non-null rows: `4147219`
- official hadm_id null rows: `1500475`
- raw total rows: `4149507`
- raw non-null numeric rows: `4147219`
- raw positive rows: `4147219`
- raw zero rows: `0`
- raw negative rows: `0`
- raw unit counts (all rows): `{"mEq/L": 4149507}`

## Current Retained Contract Used

- semantic family: `laboratory`
- asset shape: `event-level measurement asset`
- main retained source scope: `source_supplied_derived.chemistry.potassium`
- raw audit source itemid: `50971`
- standard unit: `mEq/L`
- retained precision: `round(1)`
- rounding rule: `round(1) half away from zero`
- current cleaned-value kept range: `[1.0, 10.0] mEq/L`
- relative-time anchor for uniquely linked rows: `icu_intime_if_uniquely_linked`
- relative-time unit for uniquely linked rows: `minutes`

## Validation Summary

- `ambiguous_multi_stay_rows`: `8`
- `exact_event_key_duplicate_rows`: `1728`
- `excluded_outlier_rows`: `30`
- `hadm_recovered_rows`: `23387`
- `hadm_unresolved_rows`: `1477088`
- `hospital_only_no_icu_overlap_rows`: `2057422`
- `inferred_unique_stay_rows`: `612709`
- `insufficient_linkage_info_rows`: `1477080`
- `kept_rows`: `4147189`
- `normalized_max`: `26.5`
- `normalized_min`: `0.7`
- `p01`: `3.0`
- `p50`: `4.1`
- `p99`: `6.1`
- `p999`: `8.2`
- `raw_eq_0_rows`: `0`
- `raw_gt_cleaned_max_rows`: `27`
- `raw_lt_0_rows`: `0`
- `raw_lt_cleaned_min_rows`: `3`
- `raw_match_duplicate_resolved_rows`: `0`
- `relative_time_max`: `323870`
- `relative_time_min`: `0`
- `source_abnormal_true_outlier_rows`: `30`
- `source_abnormal_true_rows`: `381272`
- `source_hadm_direct_rows`: `2646744`
- `source_hadm_null_rows`: `1500475`
- `source_unit_counts`: `{'mEq/L': 4147219}`
- `total_rows`: `4147219`
- `unique_hadm_id`: `420002`
- `unique_stay_id`: `90931`
- `unique_subject_id`: `288115`

## Semantic Cautions

- This is an event-level hospital-lab routine-chemistry asset, not a patient- or stay-level baseline summary.
- stay_id is inferred when uniquely linkable; it is not a direct source field in chemistry.parquet.
- Hospital-only rows and insufficient-linkage rows are intentionally retained for audit rather than silently dropped.
- The official chemistry derived source already excludes null raw values upstream and preserves the official chemistry concept grain.
