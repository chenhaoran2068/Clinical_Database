# Amsterdam Class 1-9 Execution Queue

Last generated: 2026-05-07T22:58:56Z

Status: generated build-first/approval-later queue; owner approval is not implied

## Source

- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_variable_coverage_audit.csv`
- `docs/standard_system_mvp/CLASS1_TO_CLASS9_BUILD_FIRST_APPROVAL_LATER_PLAN.md`

## Interpretation

This table is an execution queue, not an approval table.

A variable can be built, technically reviewed, or already public-covered without being newly approved by the project owner in the current approval wave.

## Generated Files

- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.csv`
- `docs/standard_system_mvp/amsterdam_coverage_audit/amsterdam_class1_to_class9_execution_queue.json`

## Queue Counts

| queue | count | meaning |
| --- | --- | --- |
| Q0_already_public_covered | 51 | Already public-covered; no new build needed in this campaign |
| Q1_technical_review_owner_approval_pending | 7 | Built/reviewed; technical recommendation exists, owner approval deferred |
| Q2_direct_build_queue | 3 | Direct build queue; source identity appears buildable without blocking upstream approval |
| Q3_hold_candidate_problem_found | 5 | Hold; candidate evidence exists but review found a material problem |
| Q4_bounded_candidate_build_or_review | 198 | Bounded candidate; build/review with narrow source-boundary control |
| Q5_deferred_pending_approved_parent | 58 | Deferred; needs approved or explicitly bounded upstream parent/component |
| Q6_split_identity_or_proxy_needed | 15 | Do not force same-name; split identity or local proxy needed |
| Q7_blocked_current_source_surface | 128 | Blocked under current Amsterdam source surface |

## Class Counts

| class_id | count | label |
| --- | --- | --- |
| class1_event_level_numeric | 296 | Class 1: event-level numeric primary-source |
| class2_baseline_summary_window_numeric | 21 | Class 2: baseline/summary/window numeric |
| class3_binary_state_episode | 23 | Class 3: binary state/active flag/episode |
| class4_treatment_device_io_event_stream | 30 | Class 4: treatment/device/input-output event stream |
| class5_episode_interval_bridge | 30 | Class 5: episode/interval/follow-up bridge |
| class6_ordinal_text_semiquantitative_result | 18 | Class 6: ordinal/text/semiquantitative result |
| class7_diagnosis_admin_demographic_id_map | 17 | Class 7: diagnosis/admin/demographic/id-map |
| class8_score_phenotype_composite_derived | 27 | Class 8: score/phenotype/composite derived |
| class9_microbiology_multi_entity_family | 3 | Class 9: microbiology multi-entity family |

## Queue By Class

| class_id | Q0_already_public_covered | Q1_technical_review_owner_approval_pending | Q2_direct_build_queue | Q3_hold_candidate_problem_found | Q4_bounded_candidate_build_or_review | Q5_deferred_pending_approved_parent | Q6_split_identity_or_proxy_needed | Q7_blocked_current_source_surface |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| class1_event_level_numeric | 34 | 7 | 0 | 2 | 143 | 0 | 0 | 110 |
| class2_baseline_summary_window_numeric | 6 | 0 | 0 | 0 | 0 | 7 | 8 | 0 |
| class3_binary_state_episode | 7 | 0 | 1 | 1 | 14 | 0 | 0 | 0 |
| class4_treatment_device_io_event_stream | 2 | 0 | 0 | 0 | 23 | 0 | 0 | 5 |
| class5_episode_interval_bridge | 1 | 0 | 1 | 0 | 0 | 24 | 4 | 0 |
| class6_ordinal_text_semiquantitative_result | 0 | 0 | 0 | 0 | 18 | 0 | 0 | 0 |
| class7_diagnosis_admin_demographic_id_map | 1 | 0 | 1 | 2 | 0 | 0 | 3 | 10 |
| class8_score_phenotype_composite_derived | 0 | 0 | 0 | 0 | 0 | 27 | 0 | 0 |
| class9_microbiology_multi_entity_family | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 |

## Owner-Approval Pending Technical Recommendations

| variable_id | class | review_status | build_status | public_card_status | next_action |
| --- | --- | --- | --- | --- | --- |
| std_albumin | class1_event_level_numeric | technical_review_recommend_approve_with_caveat | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave with the documented distribution caveat |
| std_aptt | class1_event_level_numeric | technical_review_recommend_approve | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave; do not count as owner-approved yet |
| std_carbon_dioxide_partial_pressure_bg_allspecimen | class1_event_level_numeric | technical_review_recommend_approve | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave; do not count as owner-approved yet |
| std_inr | class1_event_level_numeric | technical_review_recommend_approve | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave; do not count as owner-approved yet |
| std_oxygen_partial_pressure_bg_allspecimen | class1_event_level_numeric | technical_review_recommend_approve | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave; do not count as owner-approved yet |
| std_oxygen_saturation_bg_allspecimen | class1_event_level_numeric | technical_review_recommend_approve | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave; do not count as owner-approved yet |
| std_total_bilirubin | class1_event_level_numeric | technical_review_recommend_approve | built_runtime_repro_pass | reviewed_approved | carry to future owner approval wave; do not count as owner-approved yet |

## Direct Build Queue

| variable_id | class | phase | dependency_status | next_action |
| --- | --- | --- | --- | --- |
| std_mechanical_ventilation_imv_niv_active | class3_binary_state_episode | derivable_from_approved_support_family | approved_or_bounded_support_parent_available | carry to the next detailed review packet; do not treat as owner-approved yet |
| std_vasopressor_support_agent_episode | class5_episode_interval_bridge | derivable_from_approved_support_family | approved_or_bounded_support_parent_available | carry to the next detailed review packet; do not treat as owner-approved yet |
| std_icu_entry_source | class7_diagnosis_admin_demographic_id_map | admissions_core_admin_field_ready | source_grain_review_required_but_no_upstream_parent | carry to the next detailed review packet; do not treat as owner-approved yet |

## Hold Candidates

| variable_id | class | build_status | reason | next_action |
| --- | --- | --- | --- | --- |
| std_oxygen_saturation_bg_arterial_specimen | class1_event_level_numeric | built_runtime_repro_pass | Amsterdam candidate is almost identical to all-specimen blood-gas oxygen saturation and lacks a universal structured arterial specimen proof. | keep candidate evidence, resolve source-boundary problem, and do not approve in same-name wave |
| std_pt | class1_event_level_numeric | built_runtime_repro_pass | Amsterdam legacy seconds-labeled prothrombin-time source has an INR-like distribution, not a PT-seconds distribution. | keep candidate evidence, resolve source-boundary problem, and do not approve in same-name wave |
| std_advanced_respiratory_support_active | class3_binary_state_episode | built_runtime_repro_pass | Amsterdam governed build now exists from approved IMV and NIV parents, but the public same-name concept includes HFNC and no narrow Amsterdam HFNC source is approved in the current source surface. | keep candidate evidence, resolve source-boundary problem, and do not approve in same-name wave |
| std_discharge_disposition | class7_diagnosis_admin_demographic_id_map | built_runtime_repro_pass | Amsterdam governed build now exists from admissions_core.destination, but most retained destination values are numeric local codes without an approved destination-code dictionary for same-name grouped discharge disposition. | keep candidate evidence, resolve source-boundary problem, and do not approve in same-name wave |
| std_icu_exit_destination | class7_diagnosis_admin_demographic_id_map | built_runtime_repro_pass | Amsterdam governed build now exists from admissions_core.destination, but most retained destination values are numeric local codes without an approved destination-code dictionary for same-name ICU exit destination. | keep candidate evidence, resolve source-boundary problem, and do not approve in same-name wave |

## Split Identity Needed

| variable_id | class | phase | audit_rationale |
| --- | --- | --- | --- |
| std_bmi_admission_baseline | class2_baseline_summary_window_numeric | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_bmi_icu_baseline | class2_baseline_summary_window_numeric | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_days_to_next_hospital_admission | class2_baseline_summary_window_numeric | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_hospital_los_days | class2_baseline_summary_window_numeric | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_hospital_mortality | class2_baseline_summary_window_numeric | hospital_vs_icu_followup_boundary | Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge. |
| std_hospital_readmission_30d | class2_baseline_summary_window_numeric | hospital_vs_icu_followup_boundary | Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge. |
| std_weight_admission_baseline | class2_baseline_summary_window_numeric | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_weight_icu_baseline | class2_baseline_summary_window_numeric | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_hospital_admission_28d_mortality | class5_episode_interval_bridge | hospital_vs_icu_followup_boundary | Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge. |
| std_hospital_admission_30d_mortality | class5_episode_interval_bridge | hospital_vs_icu_followup_boundary | Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge. |
| std_hospital_admission_365d_mortality | class5_episode_interval_bridge | hospital_vs_icu_followup_boundary | Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge. |
| std_hospital_admission_90d_mortality | class5_episode_interval_bridge | hospital_vs_icu_followup_boundary | Amsterdam can support ICU/local-admission outcome variants only after a separate follow-up or mortality bridge. |
| std_age | class7_diagnosis_admin_demographic_id_map | age_group_not_exact_age | Amsterdam exposes agegroup, not exact MIMIC-like age; grouped-age identity is needed for exactness. |
| std_id_map_subject_hadm | class7_diagnosis_admin_demographic_id_map | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |
| std_id_map_subject_hadm_stay | class7_diagnosis_admin_demographic_id_map | known_boundary_from_prior_review | Prior Amsterdam review showed the same-name route would mix hospital-level or exact-measurement semantics; split/proxy identity is needed. |

## Next Work Rule

Start with `Q2_direct_build_queue` unless the project owner explicitly opens an approval wave.

Keep `Q1_technical_review_owner_approval_pending` visible for later approval, but do not spend the next build round trying to approve it.

Use the CSV/JSON files for the full 465-variable queue.
