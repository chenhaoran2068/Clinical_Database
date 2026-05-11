# Build Log: std_vasopressor_support_agent_episode

- `process_batch_id`: `20260504T022746Z_MIMIC-IV-3.1_std_vasopressor_support_agent_episode`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- reviewed foundation asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/medication/std_icu_vasoactive_medication_infusion_event/std_icu_vasoactive_medication_infusion_event_long.parquet`
- parent support asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/treatment_state/std_vasopressor_support_active/std_vasopressor_support_active_long.parquet`
- supporting stay anchor map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`
- opening upstream inclusion: `vasoactive_rate_analysis_eligible = True`
- opening role classes: `vasopressor`, `mixed_pressor_inotrope`
- official interval-style reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/medication/vasoactive_agent.sql`

## Approved Retained Contract

- semantic folder: `treatment_state`
- retain one row per `stay_id + std_vasoactive_agent + continuous agent support episode`
- source grain before merge: reviewed parent vasoactive courses
- support definition class: `agent_specific_support_episode_from_reviewed_course_union_pressor_plus_mixed_pressor`
- source rule summary: `local_child_reconstruction_from_reviewed_vasoactive_foundation_agent_specific_course_union_include_vasopressor_and_mixed_pressor_inotrope_exact_contiguous_only_v1`
- merge rule: `within the same agent, merge only overlapping or exactly contiguous parent courses`
- parent link rule: `map_agent_episode_to_exactly_one_parent_support_episode_by_interval_containment`
- concurrency rule: `strict_positive_overlap_with_distinct_agent_episode_only`
- keep agent identity and parent support linkage explicit rather than collapsing back into the any-support parent row

## Validation Summary

- output row count: `96606`
- output unique stay count: `26886`
- output unique parent support episode count: `71270`
- strict concurrent-other-agent rows: `35786`
- short agent episodes `<=15m`: `3879`
- prolonged agent episodes `>=7d`: `638`
- null time rows: `0`

## Semantic Cautions

- child companion asset; use the parent any-support table when agent identity is irrelevant
- retained `mixed_pressor_inotrope` agent rows are present by design and should be filtered explicitly for pure-pressor sensitivity analyses
- strict concurrency here means real positive overlap with a distinct agent, not merely belonging to a multi-agent parent episode
- this asset is still a treatment-state detail layer and should not be used as septic-shock truth by itself
