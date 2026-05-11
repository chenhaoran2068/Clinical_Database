# Build Log: std_nitrite_urinalysis_result

- `process_batch_id`: `20260502T140255Z_MIMIC-IV-3.1_std_nitrite_urinalysis_result`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- raw labevents: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_labevents.parquet`
- d_labitems: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_d_labitems.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/hosp/labevents/index.txt`

## Approved Contract Snapshot

- semantic folder: `laboratory`
- asset shape: `event-level ordinal-result asset`
- retained source scope: `hosp.labevents itemids 51487, 51987`
- standardized value domain: `negative ; positive`
- excluded row classes: `empty/placeholder`, `approved uninterpretable variants`, `approved artifact numeric variants`
- linkage rule: `best-available hadm_id + inferred_unique_stay only when ICU overlap is unique`

## Build Summary

- raw total rows: `845191`
- retained rows: `131979`
- excluded empty/placeholder rows: `713212`
- excluded uninterpretable text rows: `0`
- excluded artifact numeric rows: `0`
- retained result counts: `{'negative': 123979, 'positive': 8000}`
- hadm recovered rows: `5382`
- inferred_unique_stay rows: `7385`
- hospital_only_no_icu_overlap rows: `33105`
- insufficient_linkage_info rows: `91488`
