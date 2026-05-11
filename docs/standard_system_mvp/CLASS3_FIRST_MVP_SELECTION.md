# Class-3 First MVP Selection And Execution Checklist

Last updated: 2026-05-02

## Purpose

This note selects the first governed Class 3 representative variable and records the detailed execution checklist for closing it.

Class 3 is the first post-Class-2 variable family where the retained value is a time-varying binary support state rather than a numeric measurement or numeric summary.

## Selected Representative

Selected first representative:

- `std_invasive_mechanical_ventilation_active`

Selected database:

- `MIMIC-IV-3.1`

Selected class:

- `binary_state_episode`

Why this variable is selected first:

- it is a clear positive active-state variable
- it has an already reviewed local Layer 5 package
- it is anchored to ICU stay episodes
- it uses the official MIMIC ventilation-state surface
- it has a single narrow included source status: `InvasiveVent`
- it is more stable as a first Class 3 MVP than a medication-support variable that would immediately require multi-drug dose and ingredient governance

## Class-3 Meaning For This First MVP

Class 3 means:

- time-varying binary state or active flag
- retained as positive state rows or positive state episodes
- one row means the state is active during the retained interval
- absence of a row means no retained positive episode under the current source contract
- absence of a row must not be overinterpreted as universal proof that the state was impossible

For the first MVP, the class is intentionally narrowed to:

- positive-only binary state episodes
- ICU-stay anchored
- explicit start and end timestamps
- explicit duration
- explicit source-status inclusion rule

This is narrower than all possible binary variables.

It does not yet cover:

- one-row-per-timepoint binary grids
- negative-state rows
- diagnosis flags
- ordinal/text lab results
- treatment dose events
- multi-agent medication support classes
- derived support-free-day outcomes

## Detailed To-Do List

### 1. Lock The Class Definition

Deliverables:

- add `Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md`
- add `docs/standard_system_mvp/variable_classes/binary_state_episode/README.md`
- add class skeleton templates
- add a class-specific validator wrapper in `scripts/standard_system_mvp_engine.py`

Review standard:

- the class must distinguish binary state episodes from numeric event variables
- the class must distinguish positive-only state rows from proven negative rows
- the class must require start/end interval semantics
- the class must require an explicit source-status inclusion rule

### 2. Lock The Variable Spec

Deliverables:

- add `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/variable_spec.json`

Review standard:

- `variable_id` is stable
- immutable semantic intent is invasive mechanical ventilation active state
- the target grain is one positive support episode per ICU stay
- the allowed retained value is `true`
- the same-name rule forbids widening to NIV, HFNC, supplemental oxygen, or tracheostomy

### 3. Lock The MIMIC Mapping Spec

Deliverables:

- add `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_mimic_iv_3_1.json`

Review standard:

- source table is explicit
- included source status is exactly `InvasiveVent`
- source status field is explicit
- source grain and target grain are explicit
- identifier linkage to `stay_id`, `hadm_id`, and `subject_id` is explicit
- official source semantics remain visible
- procedureevents audit is recorded as a comparison, not as a replacement source

### 4. Add Governed Execution Entrypoint

Deliverables:

- add `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/execution.py`

Review standard:

- formal outputs are produced through the governed entrypoint
- the entrypoint reads `variable_spec.json` and `mapping_spec_mimic_iv_3_1.json`
- ad hoc SQL or side scripts are not the approved public route

### 5. Run First Governed Execution

Deliverables:

- add runtime evidence under `runtime/mimic_iv_3_1_first_real_execution/`
- include `validation_report.json`
- include `manifest.json`
- include captured logs

Review standard:

- runtime validation must pass
- local reference implementation must return success
- output artifact signatures must be recorded
- build summary must include row count, unique stay count, short episode count, and prolonged episode count

### 6. Run Rerun Reproducibility Gate

Deliverables:

- add runtime evidence under `runtime/mimic_iv_3_1_rerun_repro_check/`
- add `reproducibility_report.json`

Review standard:

- rerun validation must pass
- rerun-invariant artifacts must retain identical signatures
- process batch IDs must differ as expected
- stable build-summary fields must match

### 7. Write Formal Approval Review

Deliverables:

- add `STD_INVASIVE_MECHANICAL_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`

Review standard:

- internal counts are reported
- official source alignment is explained
- procedureevents audit is interpreted without replacing the official source
- public plausibility is checked
- boundaries are explicit

### 8. Update Public Governance Surfaces

Deliverables:

- update `README.md`
- update `docs/GETTING_STARTED.md`
- update `docs/standard_system_mvp/README.md`
- update `docs/standard_system_mvp/VARIABLE_CLASS_LANDSCAPE_AND_ROLLOUT.md`
- update `scripts/export_public_metadata.py`
- update `scripts/check_public_repository.py`
- update `docs/RELEASE_CHANGELOG.md`

Review standard:

- the Class 3 first MVP is discoverable
- generated inventory and release-safe manifest include the new files
- public repository checks pass

## Approval Boundary

This first Class 3 MVP approval will claim only:

- `std_invasive_mechanical_ventilation_active`
- `MIMIC-IV-3.1`
- positive-only invasive mechanical ventilation active episodes
- source status `InvasiveVent`
- ICU-stay anchored interval output

At the moment of first-MVP approval, it did not claim:

- NIV active approval
- HFNC active approval
- supplemental oxygen active approval
- tracheostomy status approval
- vasopressor active approval
- RRT active approval
- ventilator-free-day outcomes
- respiratory-support-free-day outcomes
- Amsterdam implementation

## Expected Next Step After Closure

After this first representative closes, the next Class 3 expansion should stay within the same respiratory-support family before jumping to vasopressors.

Recommended next candidates:

- `std_noninvasive_ventilation_active`
- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- `std_tracheostomy_status_active`

Reason:

- these can reuse the same source table, same class contract, and same official ventilation taxonomy while testing whether the class skeleton generalizes across adjacent binary active-state variables.

## Promotion Outcome

Status as of `2026-05-02`:

- the first Class 3 MVP has been closed through `std_invasive_mechanical_ventilation_active`
- Amsterdam same-name `std_invasive_mechanical_ventilation_active` has also been approved after source-audit review
- the first respiratory-support-family expansion has now been promoted through `std_noninvasive_ventilation_active` on `MIMIC-IV-3.1`
- governed variable directory: `docs/standard_system_mvp/std_noninvasive_ventilation_active/`
- formal approval review: `docs/standard_system_mvp/STD_NONINVASIVE_VENTILATION_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- the remaining direct MIMIC respiratory-support siblings have also been promoted through governed approval:
  - `std_high_flow_nasal_cannula_active`
  - `std_supplemental_oxygen_active`
  - `std_tracheostomy_status_active`
- formal approval reviews:
  - `docs/standard_system_mvp/STD_HIGH_FLOW_NASAL_CANNULA_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
  - `docs/standard_system_mvp/STD_SUPPLEMENTAL_OXYGEN_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
  - `docs/standard_system_mvp/STD_TRACHEOSTOMY_STATUS_ACTIVE_FORMAL_APPROVAL_REVIEW.md`
- the base single-status MIMIC respiratory-support family is now closed for `InvasiveVent`, `NonInvasiveVent`, `HFNC`, `SupplementalOxygen`, and `Tracheostomy`
- Amsterdam respiratory-support sibling audit is now also complete for the current third-layer scope:
  - `std_noninvasive_ventilation_active` is reviewed-approved on `AmsterdamUMCdb-1.0.2` using `processitems` itemids `10740 / Beademen non-invasief` and `9671 / CPAP`
  - `std_tracheostomy_status_active` is reviewed-approved on `AmsterdamUMCdb-1.0.2` using `processitems` itemid `12635 / Tracheostoma`
  - `std_high_flow_nasal_cannula_active` remains blocked on Amsterdam because no narrow HFNC / high-flow nasal cannula / Optiflow source was found
  - `std_supplemental_oxygen_active` remains blocked on Amsterdam as a Class 3 episode because current oxygen evidence is route/device/flow/order evidence without a governed intervalization rule
- the first non-respiratory Class 3 treatment-support state has now been promoted through `std_vasopressor_support_active`
  - `MIMIC-IV-3.1` is reviewed-approved from the local reviewed vasoactive infusion-course foundation, retaining `vasopressor` and `mixed_pressor_inotrope` role classes
  - `AmsterdamUMCdb-1.0.2` is reviewed-approved from continuous syringe-pump `drugitems` rows for approved vasopressor-capable itemids
  - both mappings keep pure inotrope therapy, agent-specific episodes, norepinephrine-equivalent dose, shock phenotype, and vasopressor-free days out of this same-name active-state asset
- the renal-support Class 3 active-state path has now been promoted through `std_rrt_active`
  - `MIMIC-IV-3.1` is reviewed-approved from official RRT/CRRT derived evidence plus dialysis procedure intervals
  - `AmsterdamUMCdb-1.0.2` is reviewed-approved from `processitems` intervals for `12465 / CVVH` and `16363 / Hemodialyse`
  - both mappings keep CRRT-only, non-CRRT-only, exact modality, fluid-removal, access-line, first-day summary, AKI/KDIGO, and renal SOFA semantics out of this same-name active-state asset
- remaining Class 3 expansion work should now move beyond direct respiratory support, vasopressor active closure, and RRT active closure, for example toward broader respiratory composites, future oxygen event-stream-to-episode derivation work, or separate Class 5 agent/modal episode variables
