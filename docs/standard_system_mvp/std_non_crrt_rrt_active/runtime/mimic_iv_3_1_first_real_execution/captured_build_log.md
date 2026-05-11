# Build Log: std_non_crrt_rrt_active

- `process_batch_id`: `20260502T113938Z_MIMIC-IV-3.1_std_non_crrt_rrt_active`
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
- support definition class: `opening_non_crrt_rrt_support_state_v1`
- support mode class: `non_crrt_rrt`
- interval merge rule: `union_overlapping_or_contiguous_rrt_interval_components_within_non_crrt_family_asset`
- retain absolute support interval plus ICU-relative start/end times in minutes

## Validation Summary

- output row count: `7816`
- unique stay count: `3790`

## Semantic Cautions

- positive-only non-CRRT RRT episode asset
- opening v1 does not claim complete capture of all hybrid or prolonged-intermittent modalities
- absence of a row does not prove absence of all non-continuous kidney support in every database
