# Build Log: std_vasopressor_support_active

- `process_batch_id`: `20260502T090104Z_MIMIC-IV-3.1_std_vasopressor_support_active`
- `database_id`: `MIMIC-IV-3.1`
- `processed_by`: `Codex`

## Source Inputs

- reviewed foundation asset: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/medication/std_icu_vasoactive_medication_infusion_event/std_icu_vasoactive_medication_infusion_event_long.parquet`
- supporting stay anchor map: `Methods/Clinical_Database/local_work/Layer 3/MIMIC-IV-3.1/id_mapping/std_id_map_subject_hadm_stay/std_id_map_subject_hadm_stay_long.parquet`
- opening upstream inclusion: `vasoactive_rate_analysis_eligible = True`
- opening role classes: `vasopressor`, `mixed_pressor_inotrope`
- official interval-style reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/medication/vasoactive_agent.sql`

## Approved Retained Contract

- semantic folder: `treatment_state`
- retain one row per `stay_id + continuous support episode`
- source grain before merge: reviewed parent vasoactive courses
- support definition class: `continuous_support_episode_from_reviewed_course_union_pressor_plus_mixed_pressor`
- source rule summary: `local_reconstruction_from_reviewed_vasoactive_foundation_course_union_include_vasopressor_and_mixed_pressor_inotrope_exact_contiguous_only_v1`
- merge rule: `merge_overlapping_or_exact_contiguous_courses_only`
- agent inclusion rule: `include_vasopressor_and_mixed_pressor_inotrope_only`
- rate eligibility rule: `require_vasoactive_rate_analysis_eligible_true`
- keep support-state semantics separate from equivalent-dose and shock-diagnosis semantics

## Validation Summary

- output row count: `71270`
- output unique stay count: `26886`
- mixed_pressor_inotrope episodes retained: `2717`
- mixed_pressor_only episodes retained: `1461`
- concurrent-agent episodes retained: `11023`
- short episodes `<=15m`: `2920`
- prolonged episodes `>=7d`: `601`
- nonpositive duration rows: `0`

## Semantic Cautions

- positive-only episode asset; absence of row does not prove hemodynamic stability
- opening v1 includes `mixed_pressor_inotrope`; later shock analyses may run stricter sensitivity filters
- `mixed_pressor_only_episode_flag` explicitly marks episodes carried only by mixed pressor/inotrope exposure
- `short_support_episode_caution_flag` and `prolonged_support_episode_caution_flag` highlight duration extremes without changing the truth layer
- this asset is not septic-shock truth and should be combined with sepsis, MAP, lactate, and later fluid-resuscitation logic downstream
- opening v1 does not bridge positive gaps between separated parent courses
