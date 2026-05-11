# Build Log: std_microbiology_test_event

- `process_batch_id`: `20260502T154552Z_MIMIC-IV-3.1_std_microbiology_test_event`
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
- row grain: `1 row per micro_specimen_id + test_seq`
- default anchor: `hospital_admission_if_available_else_subject_only`

## Validation Summary

- total rows: `1562787`
- unique `subject_id`: `198590`
- non-null unique `hadm_id`: `160675`
- null `hadm_id` rows: `765553`
- events with organism child: `253594`
- events with positive isolate child: `213534`
- events with susceptibility child: `117722`
- event positivity analysis counts: `{'negative_denominator': 950279, 'positive_numerator': 185104, 'exclude_mixed_or_contaminated': 179595, 'manual_review_needed': 93539, 'exclude_quantity_text_only': 79647, 'exclude_placeholder_only': 40029, 'exclude_cancelled_or_invalid': 20047, 'exclude_commensal_or_normal_flora': 14547}`

## Semantic Cautions

- Do not merge these laboratory-result rows with microbiology orders until a validated order-to-result linkage rule exists.
- Keep raw specimen and test labels visible for exact source interpretation.
- Keep raw comments visible for negative-result phrasing and stain-only findings.
