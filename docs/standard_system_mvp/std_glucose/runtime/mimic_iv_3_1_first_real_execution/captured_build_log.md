# Build Log: std_glucose

- `process_batch_id`: `20260503T093032Z_MIMIC-IV-3.1_std_glucose`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`
- `recorded_at`: `2026-05-03T09:30:32Z`

## Source Inputs

- official chemistry source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/source_supplied_derived/chemistry.parquet`
- raw labevents audit source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_labevents.parquet`
- item dictionary: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_d_labitems.parquet`
- admission map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm/std_id_map_subject_hadm_long.parquet`
- stay map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts_postgres/measurement/chemistry.sql`
- wrapper script: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_glucose/extract_code/Extract_Code_std_glucose.py`
- shared helper: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/shared_extract_code/_chemistry_core_builder.py`

## Source Profiling Snapshot

- raw itemid / label: `50931 / Glucose`
- raw fluid/category: `Blood / Chemistry`
- official non-null rows: `3621278`
- official hadm_id null rows: `1103927`
- raw total rows: `3621769`
- raw non-null numeric rows: `3621282`
- raw positive rows: `3621279`
- raw zero rows: `3`
- raw negative rows: `0`
- raw unit counts (all rows): `{"mg/dL": 3621769}`

## Current Retained Contract Used

- semantic family: `laboratory`
- asset shape: `event-level measurement asset`
- main retained source scope: `source_supplied_derived.chemistry.glucose`
- raw audit source itemid: `50931`
- standard unit: `mg/dL`
- retained precision: `integer`
- rounding rule: `nearest integer, half away from zero`
- current cleaned-value kept range: `[1.0, 2000.0] mg/dL`
- relative-time anchor for uniquely linked rows: `icu_intime_if_uniquely_linked`
- relative-time unit for uniquely linked rows: `minutes`

## Validation Summary

- `ambiguous_multi_stay_rows`: `8`
- `exact_event_key_duplicate_rows`: `436`
- `excluded_outlier_rows`: `223`
- `hadm_recovered_rows`: `22393`
- `hadm_unresolved_rows`: `1081534`
- `hospital_only_no_icu_overlap_rows`: `1976232`
- `inferred_unique_stay_rows`: `563512`
- `insufficient_linkage_info_rows`: `1081526`
- `kept_rows`: `3621055`
- `normalized_max`: `5840.0`
- `normalized_min`: `1.0`
- `p01`: `63.0`
- `p50`: `110.0`
- `p99`: `356.0`
- `p999`: `703.0`
- `raw_eq_0_rows`: `0`
- `raw_gt_cleaned_max_rows`: `223`
- `raw_lt_0_rows`: `0`
- `raw_lt_cleaned_min_rows`: `0`
- `raw_match_duplicate_resolved_rows`: `0`
- `relative_time_max`: `323870`
- `relative_time_min`: `0`
- `source_abnormal_true_outlier_rows`: `223`
- `source_abnormal_true_rows`: `2342937`
- `source_hadm_direct_rows`: `2517351`
- `source_hadm_null_rows`: `1103927`
- `source_unit_counts`: `{'mg/dL': 3621278}`
- `total_rows`: `3621278`
- `unique_hadm_id`: `414600`
- `unique_stay_id`: `90770`
- `unique_subject_id`: `289222`

## Semantic Cautions

- This is an event-level hospital-lab routine-chemistry asset, not a patient- or stay-level baseline summary.
- stay_id is inferred when uniquely linkable; it is not a direct source field in chemistry.parquet.
- Hospital-only rows and insufficient-linkage rows are intentionally retained for audit rather than silently dropped.
- The official chemistry derived source already excludes null raw values upstream and preserves the official chemistry concept grain.
