# Variable Class Landscape And Rollout

This note answers one practical question:

After the first `std_heart_rate` MVP, what classes can we already see, and in what order should we industrialize them?

## Current judgment

Yes, the right execution path is:

1. extract the first reusable class skeleton
2. identify the currently knowable variable classes
3. scale class by class
4. only then industrialize the 400+ `MIMIC-IV-3.1` variables

That is better than pretending one schema already fits everything.

## First reusable class now formalized

Current first class:

- `event_level_numeric_primary_source`

Meaning:

- event-level
- numeric
- clear primary source
- canonical unit/range/cleaning possible

Current public skeleton:

- `docs/standard_system_mvp/variable_classes/event_level_numeric_primary_source/`

Current first concrete governed example:

- `docs/standard_system_mvp/std_heart_rate/`

## Third reusable class now formalized

Current third class:

- `binary_state_episode`

Meaning:

- positive-only binary active-state episode
- explicit start and end time
- explicit duration
- ICU-stay anchored in the first MVP
- absence of a row is not universal proof of a negative state

Current public skeleton:

- `docs/standard_system_mvp/variable_classes/binary_state_episode/`

Current first concrete governed example:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/`

Current first respiratory-support-family expansion:

- `docs/standard_system_mvp/std_noninvasive_ventilation_active/`

Current closed MIMIC respiratory-support-family single-status set:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/`
- `docs/standard_system_mvp/std_high_flow_nasal_cannula_active/`
- `docs/standard_system_mvp/std_supplemental_oxygen_active/`
- `docs/standard_system_mvp/std_tracheostomy_status_active/`

Current Amsterdam respiratory-support-family third-layer status:

- reviewed-approved same-name assets: `std_invasive_mechanical_ventilation_active`, `std_noninvasive_ventilation_active`, and `std_tracheostomy_status_active`
- reviewed-blocked same-name candidates under current evidence: `std_high_flow_nasal_cannula_active` and `std_supplemental_oxygen_active`
- source-audit closure: `docs/standard_system_mvp/AMSTERDAM_RESPIRATORY_SUPPORT_FAMILY_SOURCE_AUDIT_REVIEW.md`

Current first non-respiratory treatment-support active-state expansion:

- `docs/standard_system_mvp/std_vasopressor_support_active/`
- reviewed-approved same-name assets: `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- boundary: any vasopressor-capable support active, not agent-specific episode detail, equivalent dose, shock phenotype, pure inotrope support, or vasopressor-free days

Current renal-support active-state expansion:

- `docs/standard_system_mvp/std_rrt_active/`
- reviewed-approved same-name assets: `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- boundary: any RRT active, not CRRT-only, non-CRRT-only, exact modality episodes, dialysis access-line status, fluid-removal events, first-day summaries, AKI/KDIGO stage, or renal SOFA phenotype

Current RRT child-family expansion:

- `docs/standard_system_mvp/std_crrt_family_active/`
- `docs/standard_system_mvp/std_non_crrt_rrt_active/`
- approved databases: `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- boundary: these are child family active flags under `std_rrt_active`, not umbrella any-RRT truth and not exact modality episodes
- Amsterdam source boundary: `std_crrt_family_active` is CVVH-based; `std_non_crrt_rrt_active` is source-bounded to Hemodialyse active intervals and does not prove peritoneal active intervals in the opening mapping

## Fourth reusable class now formalized

Current fourth class:

- `treatment_device_io_event_stream`

Meaning:

- source-faithful treatment, device, medication, or intake-output event row
- explicit event time
- numeric or amount-like value
- source unit and standard unit when deterministic
- required source-context fields
- optional parent treatment/support episode context
- no smoothing, counter differencing, or summary aggregation unless separately governed

Current public skeleton:

- `docs/standard_system_mvp/variable_classes/treatment_device_io_event_stream/`

Current first concrete governed example:

- `docs/standard_system_mvp/std_rrt_fluid_removal_event/`
- approved database: `MIMIC-IV-3.1`
- Amsterdam status: reproducible bounded candidate only, not approved
- boundary: this is a fluid-removal event stream, not RRT active state, exact modality episode, urine output, total output, hourly balance bridge, rate setting, or cumulative device counter

## Fifth reusable class now formalized

Current fifth class:

- `episode_interval_bridge`

Meaning:

- positive interval episode
- explicit start and end time
- explicit duration
- retained categorical label or modality
- optional parent-link bridge back to broader support episodes

Current public skeleton:

- `docs/standard_system_mvp/variable_classes/episode_interval_bridge/`

Current first concrete governed example:

- `docs/standard_system_mvp/std_rrt_modality_episode/`
- approved databases: `MIMIC-IV-3.1` and `AmsterdamUMCdb-1.0.2`
- Amsterdam opening labels: `CVVH` and `IHD`, with parent links back to any-RRT and family episodes

## Ninth reusable class now formalized

Current ninth class:

- `microbiology_multi_entity_family`

Meaning:

- source-faithful microbiology hierarchy
- parent specimen-test event
- child organism branch/isolate
- leaf antibiotic susceptibility row
- explicit parent-child keys and raw text retention
- no-row interpretation is not negative culture, no organism, no resistance, or no infection

Current public skeleton:

- `docs/standard_system_mvp/variable_classes/microbiology_multi_entity_family/`

Current opening governed family:

- `docs/standard_system_mvp/std_microbiology_test_event/`
- `docs/standard_system_mvp/std_microbiology_organism_isolate/`
- `docs/standard_system_mvp/std_microbiology_antibiotic_susceptibility/`
- approved database: `MIMIC-IV-3.1`
- runtime status: first execution, rerun, and reproducibility pass for all three sibling entities
- rollout closure: `docs/standard_system_mvp/CLASS9_MICROBIOLOGY_MULTI_ENTITY_FAMILY_ROLLOUT.md`

## Currently knowable top-level classes

| Class | What it means | Typical examples | Suggested order |
| --- | --- | --- | --- |
| 1. Event-level numeric, clear primary source | One time-stamped numeric event stream with one clear source family and deterministic cleaning | `std_heart_rate`, `std_respiratory_rate`, `std_temp`, `std_sbp`, `std_dbp`, `std_map`, `std_spo2`, `std_glucose`, `std_sodium`, `std_potassium`, `std_creatinine`, `std_bun` | first |
| 2. Baseline/summary/window numeric | Numeric outputs built from event streams but aggregated to baseline, daily, first-day, or follow-up windows | `std_weight_admission_baseline`, `std_weight_icu_baseline_grouped_proxy`, `std_sofa_first_day`, `std_first_day_urine_output_summary`, `std_icu_los_days`, `trial_style_28d_imv_free_days` | second |
| 3. Event-level binary state/flag | Time-varying yes/no state rather than raw numeric measurement | `std_invasive_mechanical_ventilation_active`, `std_noninvasive_ventilation_active`, `std_high_flow_nasal_cannula_active`, `std_supplemental_oxygen_active`, `std_tracheostomy_status_active`, `std_vasopressor_support_active`, `std_rrt_active`, `std_crrt_family_active`, `std_non_crrt_rrt_active` | third |
| 4. Treatment/device/input-output event stream | Event records for treatment, infusion, ventilator, fluid, or device parameters | `std_rrt_fluid_removal_event`, `std_icu_medication_input_event`, `std_ventilator_parameter_event`, `std_ecmo_device_parameter_event`, `std_icu_output_event` | fourth |
| 5. Episode/interval/bridge | Start-stop intervals, modality episodes, or follow-up bridge tables | `std_rrt_modality_episode`, `std_vasopressor_support_agent_episode`, `std_icu_admission_28d_followup_bridge` | fifth |
| 6. Ordinal/text/semiquantitative result | Result is not primarily numeric continuous measurement | `std_bacteria_urine_sediment_result`, `std_nitrite_urinalysis_result`, `std_protein_urinalysis_result` | sixth |
| 7. Diagnosis/admin/demographic/id-map | Administrative coding, demographic category, or identifier linkage | `std_sex`, `std_race`, `std_hospital_current_diagnosis_icd`, `std_id_map_subject_hadm_stay` | seventh |
| 8. Score/phenotype/composite derived | Multi-rule constructed outputs, helper variables, scores, onset logic, or criteria packages | `std_sofa2`, `std_sapsii`, `std_oasis`, `std_aki_kdigo`, `std_sepsis3_onset_delta_sofa_from_chronic_baseline` | eighth |
| 9. Microbiology multi-entity family | Test event, isolate, organism, susceptibility, and cross-row microbiology logic | `std_microbiology_test_event`, `std_microbiology_organism_isolate`, `std_microbiology_antibiotic_susceptibility` | ninth |

## Cross-cutting axes

Some naming families are important, but they are not top-level build classes by themselves.

Examples:

- specimen/body-fluid variants such as `_ascites`, `_csf`, `_pleural`, `_other_body_fluid`
- blood-gas variants such as `_bg`
- urine or stool specimen suffixes

Those are usually domain modifiers layered on top of one of the top-level classes above.

## Why this order is practical

Why class 1 first:

- simplest governed runtime path
- simplest mapping lock
- simplest validation gate
- large early yield

Why class 2 next:

- it can often reuse class-1 event outputs as upstream evidence
- it introduces aggregation without yet forcing fully different semantics like microbiology or diagnosis coding

Why class 3 and 4 after that:

- they stay close to event streams, but add state logic, support logic, and interval semantics

Why the later classes wait:

- ordinal/text, diagnosis/admin, scores, and microbiology each need a meaningfully different representation and validation model

## Immediate rollout interpretation

The right next industrial batch is not all 463 public cards at once.

The right next industrial batch is:

- finish class 1 skeleton
- use it for the first class-1 candidate wave
- then freeze the class-2 contract
- then continue class by class

## Current first class-1 candidate wave

A practical first wave after `std_heart_rate` is:

- `std_glucose`
- `std_respiratory_rate`
- `std_temp`
- `std_sbp`
- `std_dbp`
- `std_map`
- `std_spo2`
- `std_sodium`
- `std_potassium`
- `std_creatinine`

That wave is large enough to expose real edge cases while still staying inside one class.
