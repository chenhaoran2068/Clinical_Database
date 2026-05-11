# std_noninvasive_ventilation_active Formal Approval Review

Last updated: 2026-05-02

## Approval Verdict

Formal decision:

- `std_noninvasive_ventilation_active` is approved as the first Class 3 respiratory-support-family expansion after invasive ventilation.
- The approved class is `binary_state_episode`.
- The approved database is `MIMIC-IV-3.1`.
- The approved interpretation is positive-only noninvasive ventilation active episodes.

Blocking-findings judgment:

- no blocking semantic finding remains
- no blocking mapping finding remains
- no blocking runtime-evidence finding remains
- no blocking reproducibility finding remains

This approval is bounded to the `MIMIC-IV-3.1` implementation described in this note.

AmsterdamUMCdb same-name NIV/CPAP feasibility remains separate candidate work and is not approved by this decision.

## What This Approves

This review approves:

- public `variable_spec.json`
- public `mapping_spec_mimic_iv_3_1.json`
- governed `execution.py`
- first execute-mode runtime evidence
- rerun reproducibility evidence
- the first respiratory-support-family expansion of the Class 3 `binary_state_episode` class

The approved meaning is:

- one retained row per positive noninvasive ventilation state episode
- ICU-stay anchored
- source status exactly `NonInvasiveVent`
- retained value `std_noninvasive_ventilation_active = true`
- explicit `support_starttime`
- explicit `support_endtime`
- explicit `support_duration_minutes`
- no false rows emitted

Absence of a retained row means:

- no retained positive `NonInvasiveVent` episode under the approved official source-status rule

Absence of a retained row does not mean:

- universal proof that the patient had no respiratory support
- proof that all possible local raw-source support evidence was absent
- approval of a negative-state grid

## What This Does Not Approve

This review does not approve:

- invasive mechanical ventilation active
- high-flow nasal cannula active
- supplemental oxygen active
- tracheostomy status active
- any advanced respiratory support active
- ventilator-free days
- respiratory-support-free days
- Amsterdam implementation

Those require separate variable identities, mapping specs, runtime evidence, and review.

## Current Spec And Mapping Locks

Reviewed public artifacts:

- `docs/standard_system_mvp/std_noninvasive_ventilation_active/variable_spec.json`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_noninvasive_ventilation_active/execution.py`
- `Framework_Guideline/StandardVariableClass_BinaryStateEpisode_Contract.md`
- `docs/standard_system_mvp/variable_classes/binary_state_episode/README.md`
- `docs/standard_system_mvp/CLASS3_FIRST_MVP_SELECTION.md`

The mapping locks:

- source table: `source_supplied_derived.ventilation`
- source status field: `ventilation_status`
- included source status: `NonInvasiveVent`
- source start field: `starttime`
- source end field: `endtime`
- target grain: one retained positive noninvasive ventilation state episode row
- primary output value field: `std_noninvasive_ventilation_active`

The mapping explicitly excludes adjacent states:

- `InvasiveVent`
- `HFNC`
- `SupplementalOxygen`
- `Tracheostomy`

## Internal Result Summary

The local reviewed-approved result reports:

- row count: `4,833`
- unique `subject_id`: `2,455`
- unique `hadm_id`: `2,857`
- unique `stay_id`: `2,974`
- source status set within retained episodes: `NonInvasiveVent` only
- episodes per stay p50 / p90 / p99 / max: `1 / 3 / 7 / 19`
- support duration minutes p50 / p90 / p95 / p99 / max: `480 / 1020 / 1289 / 2386 / 14040`
- short episodes `<=60m`: `33`
- prolonged episodes `>=7d`: `2`
- support starts before ICU intime: `106`
- support ends after ICU outtime: `0`

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

- `NonInvasiveVent` only

Interpretation:

- MIMIC exposes NIV as a distinct official ventilation status
- the official ventilation state table remains the retained source of truth for this MVP
- adjacent support states are visible for boundary review but are not retained in this same-name output

## Governed Runtime Evidence

First execute-mode runtime evidence:

- runtime directory: `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/mimic_iv_3_1_first_real_execution/`
- process batch: `20260502T080338Z_MIMIC-IV-3.1_std_noninvasive_ventilation_active`
- validation status: `pass`
- subprocess return code: `0`
- primary output signature recorded: yes

Rerun reproducibility evidence:

- runtime directory: `docs/standard_system_mvp/std_noninvasive_ventilation_active/runtime/mimic_iv_3_1_rerun_repro_check/`
- process batch: `20260502T080340Z_MIMIC-IV-3.1_std_noninvasive_ventilation_active`
- reproducibility status: `pass`
- primary output asset is rerun-invariant by signature
- preview CSV is rerun-invariant by signature
- stable build-summary fields match across reruns

Stable build-summary fields:

- row count: `4,833`
- unique `stay_id`: `2,974`
- short episodes `<=60m`: `33`
- prolonged episodes `>=7d`: `2`

## Official-Source Alignment

Current official-source alignment judgment: acceptable.

The MIMIC official ventilation concept surface defines a derived ventilation state table with named respiratory-support statuses.

This implementation follows that official source surface by:

- using `source_supplied_derived.ventilation`
- retaining only rows where `ventilation_status = NonInvasiveVent`
- preserving official interval boundaries
- preserving `NonInvasiveVent` as the source status set

The source alignment is especially important because the same respiratory-support family contains adjacent but different states:

- `InvasiveVent`
- `HFNC`
- `SupplementalOxygen`
- `Tracheostomy`

Those are not silently included in this variable.

## Public Plausibility Review

Current plausibility judgment: acceptable.

The result magnitude is plausible for a large ICU database because:

- `2,974` ICU stays have at least one retained noninvasive ventilation episode
- the median episode duration is `480` minutes
- p90 is `1020` minutes
- p99 is `2386` minutes
- very long episodes exist but are rare and flagged as prolonged
- very short episodes exist but are flagged as short

The distribution does not suggest:

- a minutes-versus-hours unit inversion
- accidental inclusion of all oxygen support states
- conversion into a one-row-per-stay binary flag
- accidental deletion of repeated episodes

## Approval Boundary

Approved:

- `std_noninvasive_ventilation_active`
- `MIMIC-IV-3.1`
- Class 3 `binary_state_episode`
- positive-only retained episodes
- official status `NonInvasiveVent`
- ICU-stay anchored intervals

Not approved:

- false rows
- minute-level state grids
- invasive mechanical ventilation
- high-flow nasal cannula
- supplemental oxygen
- tracheostomy status
- broad advanced respiratory support
- ventilator-free-day outcomes
- Amsterdam mapping

## Final Decision

`std_noninvasive_ventilation_active` is approved as the first governed Class 3 respiratory-support-family expansion after `std_invasive_mechanical_ventilation_active`.

The next recommended Class 3 expansion can remain inside the same family:

- `std_high_flow_nasal_cannula_active`
- `std_supplemental_oxygen_active`
- `std_tracheostomy_status_active`
