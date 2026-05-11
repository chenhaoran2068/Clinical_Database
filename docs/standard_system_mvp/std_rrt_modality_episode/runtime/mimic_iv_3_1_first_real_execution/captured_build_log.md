# Build Log: std_rrt_modality_episode

- `process_batch_id`: `20260502T114546Z_MIMIC-IV-3.1_std_rrt_modality_episode`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- task contract: `Task_Tracking/MIMIC-IV-3.1/MIMIC_L3_RRTSupportState_Tasklist.md`
- source audit note: `Methods/Clinical_Database/local_work/Layer 5/MIMIC-IV-3.1/treatment_domain_discovery/rrt_support_state_opening_source_audit_20260409.md`
- official broad RRT SQL: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/treatment/rrt.sql`
- official CRRT SQL: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/treatment/crrt.sql`

## Approved Retained Contract

- semantic folder: `treatment_state`
- retain source-faithful positive-only episode rows rather than a minute grid
- support definition class: `opening_exact_rrt_modality_episode_v1`
- support mode class: `exact_rrt_modality`
- interval merge rule: `union_overlapping_or_contiguous_rrt_interval_components_within_exact_modality`
- retain absolute support interval plus ICU-relative start/end times in minutes

## Validation Summary

- output row count: `56004`
- unique stay count: `5819`

## Semantic Cautions

- exact modality child asset under the RRT parent layers
- unresolved ambiguous evidence is intentionally not forced into this child table
- SCUF remains visible here even when it is not promoted into the opening family parent
