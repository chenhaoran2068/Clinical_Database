# Build Log: std_crrt_family_active

- `process_batch_id`: `20260502T113331Z_MIMIC-IV-3.1_std_crrt_family_active`
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
- support definition class: `opening_crrt_family_support_state_v1`
- support mode class: `crrt_family`
- interval merge rule: `union_overlapping_or_contiguous_rrt_interval_components_within_crrt_family_asset`
- retain absolute support interval plus ICU-relative start/end times in minutes

## Validation Summary

- output row count: `6346`
- unique stay count: `2938`

## Semantic Cautions

- positive-only CRRT-family episode asset
- opening v1 excludes SCUF from automatic family-parent inclusion
- do not replace exact modality analysis with this family layer when modality matters
