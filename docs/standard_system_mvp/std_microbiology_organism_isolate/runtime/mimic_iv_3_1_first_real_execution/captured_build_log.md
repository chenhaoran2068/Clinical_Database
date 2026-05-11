# Build Log: std_microbiology_organism_isolate

- `process_batch_id`: `20260502T155017Z_MIMIC-IV-3.1_std_microbiology_organism_isolate`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- microbiology source: `Methods/Clinical_Database/local_work/Layer 2/MIMIC-IV-3.1/reviewed_unsplit/hosp_microbiologyevents.parquet`
- microbiologyevents documentation: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/hosp/microbiologyevents/index.txt`
- deferred future order-side documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/hosp/poe/index.txt`
- deferred future order-detail documentation reference: `References/MIMIC/2026-03-20_snapshot_v2/text/mimic_docs/modules/hosp/poe_detail/index.txt`

## Approved Retained Contract

- evidence class: `recorded_microbiology_laboratory_result`
- current status: `built_pending_user_review`
- row grain: `1 row per micro_specimen_id + test_seq + organism branch`
- default anchor: `hospital_admission_if_available_else_subject_only`

## Validation Summary

- total rows: `306613`
- unique `subject_id`: `89352`
- non-null unique `hadm_id`: `51516`
- null `hadm_id` rows: `180039`
- isolates with susceptibility child: `139153`
- organism positive analysis counts: `{'count_as_positive_isolate': 262045, 'exclude_cancelled_placeholder': 37140, 'exclude_flora_or_mixed_summary': 7428}`
- rows with quantity text: `27`

## Semantic Cautions

- Do not merge these laboratory-result rows with microbiology orders until a validated order-to-result linkage rule exists.
- Keep raw specimen and test labels visible for exact source interpretation.
- Keep raw comments visible for negative-result phrasing and stain-only findings.
