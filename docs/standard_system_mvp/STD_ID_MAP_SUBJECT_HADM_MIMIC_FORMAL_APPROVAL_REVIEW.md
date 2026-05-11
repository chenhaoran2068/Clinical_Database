# std_id_map_subject_hadm MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class7_lateral_expansion

Database: `MIMIC-IV-3.1`

Standard variable: `std_id_map_subject_hadm`

Variable class: `diagnosis_admin_demographic_id_map`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_id_map_subject_hadm`.

The approved meaning is a hospital-admission-level identifier bridge linking `subject_id` to `hadm_id`, with `admittime` and `dischtime` retained as the source-authoritative hospital encounter window.

This approval does not approve ICU-stay mapping, readmission outcome, diagnosis event, demographic category, or follow-up phenotype under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_id_map_subject_hadm/variable_spec.json`
- `docs/standard_system_mvp/std_id_map_subject_hadm/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_id_map_subject_hadm/execution.py`
- `Framework_Guideline/StandardVariableClass_DiagnosisAdminDemographicIdMap_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_id_map_subject_hadm/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_id_map_subject_hadm/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_id_map_subject_hadm/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T145011Z_MIMIC-IV-3.1_std_id_map_subject_hadm`
- rerun: `20260502T145018Z_MIMIC-IV-3.1_std_id_map_subject_hadm`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.admissions`
- retained fields: `subject_id`, `hadm_id`, `admittime`, `dischtime`
- source grain: one row per `hadm_id`
- target grain: one retained id-map row per `hadm_id`

## Output Summary

First governed execution output:

- total rows: `546,028`
- unique subjects: `223,452`
- unique hospital admissions: `546,028`
- subjects with multiple admissions: `100,163`

Approved key rule:

- `hadm_id` is the unique retained row key
- `subject_id` is expected to repeat across admissions

## Exclusion Boundary

This approval excludes:

- ICU stay mapping
- hospital readmission outcome calculation
- next-admission duration
- diagnosis or procedure code events
- demographic categories
- treating absence from this map as no hospitalization in the source population

## Approval Rationale

The mapping is narrow, source-authoritative, and mechanically verifiable. It establishes the Class 7 governed pattern for ID bridge assets: identifier grain first, source authority locked, duplicate key rule explicit, and no-row interpretation separated from downstream outcomes.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_id_map_subject_hadm` as the Class 7 lateral expansion beyond patient-level sex. Future hospital-level bridge variables should depend on this kind of admission-level map rather than rebuilding the relationship ad hoc.
