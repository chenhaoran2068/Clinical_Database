# Public Release Note: public-method-foundation-2026-04-21

- release version: `0.1.0-dev`
- release tag: `public-method-foundation-2026-04-21`
- release label: `public-method-repository-foundation`
- release status: `working_tree_snapshot`
- release date: `2026-04-21`
- changelog heading: `## 0.1.0-dev - 2026-04-21`

## Release summary

- established the public database lineage and version matrix
- established family-level onboarding and governance playbooks
- established public workflow entrypoints and public repository checks
- established public tutorials and std-variable card publication layer
- established `docs/release_safe_manifest.json` and `docs/PUBLIC_INVENTORY.md`
- added formal contracts for family new-version admission and release-safe manifest release governance
- added a formal standard-system maturity roadmap linking current repository strengths to the next executable and validated build layers
- added a formal current-stage completion standard defining why the foundation stage can now be considered closed
- started the first public standard-system MVP draft surface with machine-readable `std_heart_rate` variable and MIMIC mapping specs, a governed execution entrypoint, the first runtime validation/manifest artifacts, and a formal runtime-evidence contract plus post-run validator
- lifted the first `std_heart_rate` execute/rerun pilot into a reusable event-level numeric primary-source skeleton with a shared governed engine, class contract, and explicit class-landscape rollout map
- added `std_glucose` as the second governed event-level numeric MVP instance on `MIMIC-IV-3.1`, including execute-mode runtime evidence, rerun reproducibility evidence, and a runtime-local captured build-log safeguard for mutable local log archives
- added `std_respiratory_rate` as the third governed event-level numeric MVP instance on `MIMIC-IV-3.1`, confirming the same class skeleton also closes on an ICU vital-sign stream beyond heart rate
- completed the first large `MIMIC-IV-3.1` class-1 governed batch for `std_sodium`, `std_potassium`, `std_creatinine`, `std_spo2`, `std_temp`, `std_sbp`, `std_dbp`, and `std_map`, each with machine-readable spec locks, governed execute-mode runtime evidence, rerun reproducibility evidence, and passing public post-run validators
- added a formal `CLASS1_FIRST_BATCH_APPROVAL_SUMMARY.md` note to separate the first reviewed 10-variable `MIMIC-IV-3.1` class-1 content-approval batch from the broader governed MVP prototype surface
- refreshed `std_heart_rate` to the same current approval bar by closing its `MIMIC-IV-3.1` baseline/rerun runtime evidence under the current mapping-spec contract, writing a formal `STD_HEART_RATE_FORMAL_APPROVAL_REVIEW.md`, and lifting the current class-1 public closure into `CLASS1_CURRENT_APPROVAL_CLOSURE.md`
- tightened the current class-1 closure surface by explicitly class-locking `std_heart_rate` under `event_level_numeric_primary_source` and updating `GETTING_STARTED.md` so the newer class-1 approval notes are discoverable from the public onboarding path
- defined the second reusable MVP class `baseline_summary_window_numeric`, added its class contract and public skeleton templates, and recorded `std_icu_los_days` as the first dual-database class-2 MVP candidate with written acceptance criteria
- closed the first class-2 governed MVP on `std_icu_los_days`, including class-2 public spec locks, a class-aware governed execution runner, dual-database execute-mode runtime evidence, dual-database rerun reproducibility evidence, and a formal approval review note
- added `std_weight_admission_baseline` as the first governed MIMIC-only class-2 baseline-snapshot example after `std_icu_los_days`, with a public variable spec, MIMIC mapping spec, governed execution entrypoint, execute/rerun runtime evidence, reproducibility gate, and formal approval review note
- reviewed the Amsterdam `std_weight_admission_baseline` local candidate and formally kept it out of same-name public approval because its current evidence is grouped/proxy ICU-MCU admission weight rather than the current hospital-admission event-baseline contract
- split that Amsterdam grouped/proxy evidence into `std_weight_icu_baseline_grouped_proxy` and approved it as a separate Amsterdam-only class-2 variable with public spec, Amsterdam mapping spec, governed execute/rerun evidence, reproducibility report, public card, and formal approval review note
- added `CLASS2_CURRENT_APPROVAL_CLOSURE.md` to record the bounded current-stage Class 2 approval across `std_icu_los_days`, `std_weight_admission_baseline`, and `std_weight_icu_baseline_grouped_proxy`, while explicitly not claiming full class-2 industrialization
- added `std_first_day_urine_output_summary` as the first governed MIMIC-only class-2 window-summary example, with public spec, MIMIC mapping spec, governed execute/rerun evidence, official first-day urine-output reference matching, public card normalization, formal approval review, and an updated `CLASS2_CURRENT_APPROVAL_CLOSURE.md` covering all three current class-2 subclasses
- reviewed Amsterdam eligibility for same-name `std_first_day_urine_output_summary` as an intermediate candidate step, with Amsterdam `std_icu_urine_output_event` identified as the required upstream event-layer prerequisite before later summary approval
- approved Amsterdam `std_icu_urine_output_event` as the governed upstream urine-output event layer, including public variable/mapping specs, execute/rerun runtime evidence, reproducibility validation, a formal approval review note, and a cross-database public card update
- promoted Amsterdam `std_first_day_urine_output_summary` from candidate to reviewed-approved same-name status by adding an Amsterdam mapping spec, governed execute/rerun runtime evidence, reproducibility validation, a formal Amsterdam approval review note, and a cross-database public card update
- added `CLASS2_TOTAL_CLOSURE_REVIEW_AND_MIMIC_EXPANSION_DECISION.md` to record the current Class 2 total closure review and approve the next controlled `MIMIC-IV-3.1` expansion path, starting with `std_weight_icu_baseline` and `std_hospital_los_days`
- promoted MIMIC-IV-3.1 `std_weight_icu_baseline` into the governed Class 2 MVP surface with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public card refresh, and a formal approval review note
- promoted MIMIC-IV-3.1 `std_hospital_los_days` into the governed Class 2 MVP surface with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public card refresh, and a formal approval review note
- reviewed Amsterdam eligibility for same-name `std_hospital_los_days` and kept it out of same-name approval because the current Amsterdam duration evidence is ICU/MC or ICU-semantic stay duration, not a verified hospital-admission encounter duration
- repaired the public-card `latest_review_date` metadata for `std_bmi_admission_baseline` and `std_bmi_icu_baseline`, added candidate reviews, then promoted both derived BMI baselines into the governed Class 2 MVP surface with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public card refresh, and formal approval review notes
- recorded reviewer approval of the current five-variable Amsterdam governed result distributions in `AMSTERDAM_GOVERNED_RESULTS_DISTRIBUTION_APPROVAL_REVIEW.md`, covering `std_heart_rate`, `std_icu_los_days`, `std_weight_icu_baseline_grouped_proxy`, `std_icu_urine_output_event`, and `std_first_day_urine_output_summary`
- promoted `std_invasive_mechanical_ventilation_active` as the first governed Class 3 `binary_state_episode` MVP on `MIMIC-IV-3.1`, with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, and a formal approval review note
- recorded project-owner approval of the bounded `MIMIC-IV-3.1` `std_invasive_mechanical_ventilation_active` implementation and opened an Amsterdam same-name candidate review that identifies `processitems` itemid `9328` / `Beademen` as the next source-audit target without claiming Amsterdam approval yet
- promoted Amsterdam `std_invasive_mechanical_ventilation_active` from candidate review to reviewed-approved same-name Class 3 status by approving `processitems` itemid `9328` / `Beademen` as the narrow invasive-ventilation-active source, excluding NIV/CPAP process overlaps, retaining adjacent respiratory-support evidence only as flags, adding governed execute/rerun runtime evidence, validating reproducibility, refreshing the cross-database public card, and writing a formal Amsterdam approval review note
- promoted MIMIC-IV-3.1 `std_noninvasive_ventilation_active` into the governed Class 3 respiratory-support-family surface, with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, and a formal approval review note while keeping IMV, HFNC, supplemental oxygen, and tracheostomy as separate states
- promoted MIMIC-IV-3.1 `std_high_flow_nasal_cannula_active`, `std_supplemental_oxygen_active`, and `std_tracheostomy_status_active` into the governed Class 3 respiratory-support-family surface, closing the direct MIMIC single-status respiratory set with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public-card updates, and formal approval review notes
- selected `std_days_to_next_hospital_admission` as the next small `MIMIC-IV-3.1` Class 2 candidate after BMI, documenting it as a post-discharge observed follow-up duration-summary boundary test rather than a governed approval
- promoted MIMIC-IV-3.1 `std_days_to_next_hospital_admission` into the governed Class 2 MVP surface with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public card refresh, and a formal approval review note while explicitly keeping Amsterdam same-name approval blocked pending a hospital-admission encounter bridge
- completed `AMSTERDAM_HOSPITAL_ADMISSION_BRIDGE_FEASIBILITY_REVIEW.md`, confirming that the current Amsterdam opening layer does not prove a hospital-admission/discharge bridge and therefore cannot support Amsterdam same-name approval for `std_hospital_los_days` or `std_days_to_next_hospital_admission`
- added `AMSTERDAM_NEXT_ICU_MCU_ADMISSION_DURATION_CANDIDATE_REVIEW.md` to record the safe Amsterdam post-bridge route: next local ICU/MCU admission duration is feasible, but MC-inclusive timing requires a split identity such as `std_days_to_next_icu_mcu_admission` rather than same-name `std_days_to_next_icu_admission`
- promoted Amsterdam `std_days_to_next_icu_mcu_admission` into the governed Class 2 MVP surface as the approved split ICU/MCU local-admission follow-up duration, with public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, a public card, and a formal Amsterdam approval review note
- promoted Amsterdam same-name `std_days_to_next_icu_admission` into the governed Class 2 MVP surface as the ICU-only local-admission follow-up duration, with MC-only rows excluded, public variable/mapping specs, governed execute/rerun runtime evidence, reproducibility validation, a cross-database public card update, and a formal Amsterdam approval review note
- completed the Amsterdam Class 3 respiratory-support-family third-layer audit by approving same-name `std_noninvasive_ventilation_active` from `10740 / Beademen non-invasief` plus `9671 / CPAP`, approving same-name `std_tracheostomy_status_active` from `12635 / Tracheostoma`, and formally blocking Amsterdam same-name `std_high_flow_nasal_cannula_active` and `std_supplemental_oxygen_active` under current evidence instead of forcing unsupported active-episode mappings
- promoted `std_vasopressor_support_active` as the first non-respiratory Class 3 treatment-support active-state example, with MIMIC and Amsterdam same-name mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public-card refresh, and formal approval reviews while keeping agent-specific episode, dose, shock, pure inotrope, and free-day semantics separate
- promoted `std_rrt_active` as the next Class 3 treatment-support active-state example, with MIMIC and Amsterdam same-name mapping specs, governed execute/rerun runtime evidence, reproducibility validation, public-card refresh, and formal approval reviews while keeping CRRT-only, non-CRRT-only, exact modality, dialysis access-line, fluid-removal, first-day summary, AKI/KDIGO, and renal SOFA semantics separate
- promoted the MIMIC-IV-3.1 and AmsterdamUMCdb-1.0.2 RRT child layers by approving `std_crrt_family_active` and `std_non_crrt_rrt_active` as separate Class 3 family active flags, and `std_rrt_modality_episode` as the first governed Class 5 `episode_interval_bridge` example with exact modality labels and parent links; Amsterdam non-CRRT approval is source-bounded to `Hemodialyse` active intervals

## Snapshot counts

- family count: `6`
- database count: `7`
- public std-variable cards: `465`
- cross-database public cards: `56`
- release-safe file count: `2133`

## Coverage by database

| database_id | role | public card count |
| --- | --- | --- |
| `MIMIC-IV-3.1` | core_database | `463` |
| `MIMIC-IV-ECHO-1.0` | sibling_module | `0` |
| `AmsterdamUMCdb-1.0.2` | core_database | `58` |
| `SICdb-1.0.5` | core_database | `0` |
| `NWICU-0.1.0` | core_database | `0` |
| `eICU-CRD-2.0` | core_database | `0` |
| `Zigong-1.1` | core_database | `0` |

## Generated companion artifacts

- `docs/release_safe_manifest.json`
- `docs/PUBLIC_INVENTORY.md`
- `docs/public_exports/repository_status.json`
- `docs/public_exports/database_variable_coverage.json`
- `docs/public_exports/family_variable_coverage.json`
- `docs/public_exports/variable_coverage_summary.md`

## Release boundary

This release note describes only the GitHub-safe public method repository surface. It does not enumerate restricted raw data, local parquet copies, or patient-level Layer 2-5 outputs.
