# Build Log: std_id_map_subject_hadm

- `process_batch_id`: `20260502T145018Z_MIMIC-IV-3.1_std_id_map_subject_hadm`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Input

- `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_admissions.parquet`

## Output Paths

- Layer 3 asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm/std_id_map_subject_hadm_long.parquet`
- Layer 5 preview: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_id_map_subject_hadm/preview/std_id_map_subject_hadm_preview.csv`
- Layer 5 asset manifest: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_id_map_subject_hadm/asset_manifest.md`
- Knowledge package: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_id_map_subject_hadm/Layer5_PerVariable_KnowledgePackage.xlsx`

## Validation Summary

- total rows: `546028`
- unique subject_id: `223452`
- unique hadm_id: `546028`
- subjects with multiple admissions: `100163`

## Retention Note

- This is the latest effective build log only.
- Historical build rows are not written into the Layer 3 data table itself.
