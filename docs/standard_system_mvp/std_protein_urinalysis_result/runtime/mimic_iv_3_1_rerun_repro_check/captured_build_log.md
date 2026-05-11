# Build Log: std_protein_urinalysis_result

- `process_batch_id`: `20260502T144953Z_MIMIC-IV-3.1_std_protein_urinalysis_result`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- raw labevents: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_labevents.parquet`
- d_labitems: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_d_labitems.parquet`
- source documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/hosp/labevents/index.txt`

## Approved Contract Snapshot

- semantic folder: `laboratory`
- asset shape: `event-level ordinal-result asset`
- retained source scope: `hosp.labevents itemids 51492, 51992`
- standardized value domain: `negative ; trace ; mild_positive ; moderate_positive ; marked_positive ; severe_positive`
- excluded row classes: `empty/placeholder`, `approved uninterpretable variants`, `approved artifact numeric variants`
- linkage rule: `best-available hadm_id + inferred_unique_stay only when ICU overlap is unique`

## Build Summary

- raw total rows: `845193`
- retained rows: `380346`
- excluded empty/placeholder rows: `464846`
- excluded uninterpretable text rows: `0`
- excluded artifact numeric rows: `1`
- retained result counts: `{'mild_positive': 166099, 'negative': 81205, 'moderate_positive': 56884, 'trace': 54296, 'marked_positive': 18421, 'severe_positive': 3441}`
- hadm recovered rows: `13827`
- inferred_unique_stay rows: `32819`
- hospital_only_no_icu_overlap rows: `110616`
- insufficient_linkage_info rows: `236909`
