# Build Log: std_creatinine

- `process_batch_id`: `20260503T095346Z_MIMIC-IV-3.1_std_creatinine`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`
- `recorded_at`: `2026-05-03T09:53:46Z`

## Source Inputs

- official chemistry source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/chemistry.parquet`
- raw labevents audit source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_labevents.parquet`
- item dictionary: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_d_labitems.parquet`
- admission map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm/std_id_map_subject_hadm_long.parquet`
- stay map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts_postgres/measurement/chemistry.sql`
- wrapper script: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_creatinine/extract_code/Extract_Code_std_creatinine.py`
- shared helper: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/shared_extract_code/_chemistry_core_builder.py`

## Source Profiling Snapshot

- raw itemid / label: `50912 / Creatinine`
- raw fluid/category: `Blood / Chemistry`
- official non-null rows: `4317389`
- official hadm_id null rows: `1731670`
- raw total rows: `4319091`
- raw non-null numeric rows: `4317525`
- raw positive rows: `4317391`
- raw zero rows: `134`
- raw negative rows: `0`
- raw unit counts (all rows): `{"mg/dL": 4319091}`

## Current Retained Contract Used

- semantic family: `laboratory`
- asset shape: `event-level measurement asset`
- main retained source scope: `source_supplied_derived.chemistry.creatinine`
- raw audit source itemid: `50912`
- standard unit: `mg/dL`
- retained precision: `round(2)`
- rounding rule: `round(2) half away from zero`
- current cleaned-value kept range: `[0.1, 20.0] mg/dL`
- relative-time anchor for uniquely linked rows: `icu_intime_if_uniquely_linked`
- relative-time unit for uniquely linked rows: `minutes`

## Validation Summary

- `ambiguous_multi_stay_rows`: `8`
- `exact_event_key_duplicate_rows`: `6043`
- `excluded_outlier_rows`: `551`
- `hadm_recovered_rows`: `23329`
- `hadm_unresolved_rows`: `1708341`
- `hospital_only_no_icu_overlap_rows`: `2034314`
- `inferred_unique_stay_rows`: `574734`
- `insufficient_linkage_info_rows`: `1708333`
- `kept_rows`: `4316838`
- `normalized_max`: `80.0`
- `normalized_min`: `0.07`
- `p01`: `0.4`
- `p50`: `0.9`
- `p99`: `7.7`
- `p999`: `13.9`
- `raw_eq_0_rows`: `0`
- `raw_gt_cleaned_max_rows`: `549`
- `raw_lt_0_rows`: `0`
- `raw_lt_cleaned_min_rows`: `2`
- `raw_match_duplicate_resolved_rows`: `0`
- `relative_time_max`: `323870`
- `relative_time_min`: `0`
- `source_abnormal_true_outlier_rows`: `551`
- `source_abnormal_true_rows`: `1364091`
- `source_hadm_direct_rows`: `2585719`
- `source_hadm_null_rows`: `1731670`
- `source_unit_counts`: `{'mg/dL': 4317389}`
- `total_rows`: `4317389`
- `unique_hadm_id`: `424398`
- `unique_stay_id`: `90888`
- `unique_subject_id`: `295011`

## Semantic Cautions

- This is an event-level hospital-lab routine-chemistry asset, not a patient- or stay-level baseline summary.
- stay_id is inferred when uniquely linkable; it is not a direct source field in chemistry.parquet.
- Hospital-only rows and insufficient-linkage rows are intentionally retained for audit rather than silently dropped.
- The official chemistry derived source already excludes null raw values upstream and preserves the official chemistry concept grain.
