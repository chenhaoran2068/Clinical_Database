# Build Log: std_microbiology_antibiotic_susceptibility

- `process_batch_id`: `20260502T155650Z_MIMIC-IV-3.1_std_microbiology_antibiotic_susceptibility`
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
- row grain: `1 row per microbiology susceptibility leaf row`
- default anchor: `hospital_admission_if_available_else_subject_only`

## Validation Summary

- total rows: `1314671`
- unique `subject_id`: `52973`
- non-null unique `hadm_id`: `33109`
- null `hadm_id` rows: `838045`
- standardized interpretation counts: `{'susceptible': 1050745, 'resistant': 224987, 'intermediate': 38687, 'susceptible_dose_dependent': 203, 'other_rare_raw_code': 49}`
- direct resistance-analysis eligible rows: `1314412`
- rare raw interpretation counts: `{'D': 203, 'Z': 39, 'N': 6, 'P': 4}`

## Semantic Cautions

- Do not merge these laboratory-result rows with microbiology orders until a validated order-to-result linkage rule exists.
- Keep raw specimen and test labels visible for exact source interpretation.
- Keep raw comments visible for negative-result phrasing and stain-only findings.
