# std_invasive_mechanical_ventilation_active Formal Approval Review

Last updated: 2026-05-01

## Approval Verdict

Formal decision:

- `std_invasive_mechanical_ventilation_active` is approved as the first governed Class 3 MVP variable.
- The approved class is `binary_state_episode`.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive-only invasive mechanical ventilation active episodes.

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking mapping finding remains
- no blocking runtime-evidence finding remains
- no blocking reproducibility finding remains

User approval record:

- approved by project owner after pre-approval review on 2026-05-01
- approval is bounded to the `MIMIC-IV-3.1` implementation described in this note
- AmsterdamUMCdb same-name feasibility remains separate candidate work and is not approved by this decision

## What This Approves

This review approves:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- first execute-mode runtime evidence
- rerun reproducibility evidence
- the first concrete governed example of the Class 3 `binary_state_episode` class

The approved meaning is:

- one retained row per positive invasive mechanical ventilation state episode
- ICU-stay anchored
- source status exactly `InvasiveVent`
- retained value `std_invasive_mechanical_ventilation_active = true`
- explicit `support_starttime`
- explicit `support_endtime`
- explicit `support_duration_minutes`
- no false rows emitted

Absence of a retained row means:

- no retained positive `InvasiveVent` episode under the approved official source-status rule

Absence of a retained row does not mean:

- universal proof that the patient had no respiratory support
- proof that all possible local raw-source support evidence was absent
- approval of a negative-state grid

## What This Does Not Approve

This review does not approve:

- noninvasive ventilation active
- high-flow nasal cannula active
- supplemental oxygen active
- tracheostomy status active
- any advanced respiratory support active
- vasopressor active
- renal replacement therapy active
- ventilator-free days
- respiratory-support-free days
- Amsterdam implementation

Those require separate variable identities, mapping specs, runtime evidence, and review.

## Current Spec And Mapping Locks

Reviewed public artifacts:

- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/variable_spec.json`
- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/execution.py`
- `Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md`
- `docs/standard_system_mvp/variable_classes/binary_state_episode/README.md`
- `docs/standard_system_mvp/CLASS3_FIRST_MVP_SELECTION.md`

The mapping locks:

- source table: `source_supplied_derived.ventilation`
- source status field: `ventilation_status`
- included source status: `InvasiveVent`
- source start field: `starttime`
- source end field: `endtime`
- target grain: one retained positive invasive mechanical ventilation state episode row
- primary output value field: `std_invasive_mechanical_ventilation_active`

The mapping explicitly keeps `icu.procedureevents` itemid `225792` as audit-only evidence rather than the replacement source.

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `46,004`
- unique `subject_id`: `29,183`
- unique `hadm_id`: `32,584`
- unique `stay_id`: `34,148`
- source status set within retained episodes: `InvasiveVent` only
- episodes per stay p50 / p90 / p99 / max: `1 / 2 / 6 / 56`
- support duration minutes p50 / p90 / p95 / p99 / max: `1,167 / 7,920 / 12,480 / 24,540 / 155,220`
- short episodes `<=60m`: `483`
- prolonged episodes `>=7d`: `3,257`
- support starts before ICU intime: `4,476`
- support ends after ICU outtime: `45`

Interpretation:

- the result is a positive episode table, not a stay-level yes/no summary
- multiple episodes per stay are expected when the official source splits intervals
- short and prolonged episodes are flagged rather than silently deleted
- pre-ICU relative starts are retained because the official episode can overlap the ICU admission anchor

## Source-Audit Summary

Official ventilation-source status counts:

- `HFNC`: `4,744`
- `InvasiveVent`: `46,004`
- `NonInvasiveVent`: `4,833`
- `None`: `197`
- `SupplementalOxygen`: `83,749`
- `Tracheostomy`: `5,285`

Approved retained source status:

- `InvasiveVent` only

Procedureevents comparison:

- procedure itemid: `225792`
- procedure label: `Invasive Ventilation`
- procedure row count: `35,479`
- procedure unique `stay_id`: `31,969`
- official ventilation unique `stay_id`: `34,148`
- overlap unique `stay_id`: `28,858`
- official-only unique `stay_id`: `5,290`
- procedure-only unique `stay_id`: `3,111`

Interpretation:

- procedureevents do not perfectly reproduce the official ventilation state table
- the official ventilation state table remains the retained source of truth for this MVP
- procedureevents are useful audit evidence, not a reason to replace the approved source

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260501T012621Z_MIMIC-IV-3.1_std_invasive_mechanical_ventilation_active`
- validation status: `pass`
- subprocess return code: `0`
- primary output signature recorded: yes

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_invasive_mechanical_ventilation_active/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260501T012633Z_MIMIC-IV-3.1_std_invasive_mechanical_ventilation_active`
- reproducibility status: `pass`
- primary output asset is rerun-invariant by signature
- preview CSV is rerun-invariant by signature
- stable build-summary fields match across reruns

Stable build-summary fields:

- row count: `46,004`
- unique `stay_id`: `34,148`
- short episodes `<=60m`: `483`
- prolonged episodes `>=7d`: `3,257`

## Official-Source Alignment

Current official-source alignment judgment: acceptable.

The MIMIC official ventilation concept surface defines a derived ventilation state table with named respiratory-support statuses.

This implementation follows that official source surface by:

- using `source_supplied_derived.ventilation`
- retaining only rows where `ventilation_status = InvasiveVent`
- preserving official interval boundaries
- preserving `InvasiveVent` as the source status set
- keeping procedureevents as audit-only rather than silently changing the source definition

The source alignment is especially important because the same respiratory-support family contains adjacent but different states:

- `NonInvasiveVent`
- `HFNC`
- `SupplementalOxygen`
- `Tracheostomy`

Those are not silently included in this variable.

## Public Plausibility Review

Current plausibility judgment: acceptable.

The result magnitude is plausible for a large ICU database because:

- `34,148` ICU stays have at least one retained invasive ventilation episode
- the median episode duration is about `19.45` hours
- p90 is about `5.5` days
- p99 is about `17.0` days
- very long episodes exist but are flagged as prolonged
- very short episodes exist but are flagged as short

The distribution does not suggest:

- a minutes-versus-hours unit inversion
- accidental inclusion of all oxygen support states
- conversion into a one-row-per-stay binary flag
- accidental deletion of repeated episodes

## Approval Boundary

Approved:

- `std_invasive_mechanical_ventilation_active`
- `MIMIC-IV-3.1`
- Class 3 `binary_state_episode`
- positive-only retained episodes
- official status `InvasiveVent`
- ICU-stay anchored intervals

Not approved:

- false rows
- minute-level state grids
- noninvasive ventilation
- high-flow nasal cannula
- tracheostomy status
- broad advanced respiratory support
- ventilator-free-day outcomes
- Amsterdam mapping

## Final Decision

`std_invasive_mechanical_ventilation_active` is approved as the first governed Class 3 MVP variable.

This approval proves that the public standard-system MVP can now represent:

- event-level numeric variables
- baseline/summary/window numeric variables
- positive-only binary state episode variables

The next recommended Class 3 expansion should remain inside the respiratory-support family before moving to vasopressors or renal replacement therapy.

Recommended next candidates:

- `std_noninvasive_ventilation_active`
- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- `std_tracheostomy_status_active`

## Source Pointers

Public official/source references:

- MIMIC-IV v3.1 official dataset page: <https://physionet.org/content/mimiciv/3.1/>
- MIMIC official ventilation concept SQL: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts/treatment/ventilation.sql>
- MIMIC official SOFA concept SQL: <https://raw.githubusercontent.com/MIT-LCP/mimic-code/main/mimic-iv/concepts/score/sofa.sql>
