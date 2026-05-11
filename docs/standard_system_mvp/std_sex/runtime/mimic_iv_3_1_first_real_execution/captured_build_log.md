# Build Log: std_sex

- `process_batch_id`: `20260502T140341Z_MIMIC-IV-3.1_std_sex`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Input

- `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_patients.parquet`
- raw source field: `gender`
- raw mapping used in this build: `F -> female`, `M -> male`

## Output Paths

- Layer 3 asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/demographics/std_sex/std_sex_long.parquet`
- Layer 5 preview: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_sex/preview/std_sex_preview.csv`
- Layer 5 asset manifest: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_sex/asset_manifest.md`
- Knowledge package: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/std_sex/Layer5_PerVariable_KnowledgePackage.xlsx`

## Validation Summary

- total rows: `364627`
- unique subject_id: `364627`
- female rows: `191984`
- male rows: `172643`

## Semantic Caution

- The MIMIC raw source field is named `gender`.
- This retained asset is intentionally labeled `sex` because the current MIMIC field behaves as a binary administrative sex-like variable, not a self-identified social-identity variable.
- Do not interpret this retained variable as a self-identified social-identity variable without stronger source-specific justification.
