# std_sex MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class7_mvp

Database: `MIMIC-IV-3.1`

Standard variable: `std_sex`

Variable class: `diagnosis_admin_demographic_id_map`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_sex`.

The approved meaning is a source-standardized patient-level sex-like administrative demographic category. The retained grain is one row per `subject_id`.

This approval does not approve encounter-level sex, ICU-stay-level sex, gender identity, race/ethnicity, diagnosis-derived sex inference, or phenotype truth under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_sex/variable_spec.json`
- `docs/standard_system_mvp/std_sex/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_sex/execution.py`
- `Framework_Guideline/StandardVariableClass_DiagnosisAdminDemographicIdMap_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_sex/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_sex/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_sex/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T140341Z_MIMIC-IV-3.1_std_sex`
- rerun: `20260502T140347Z_MIMIC-IV-3.1_std_sex`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `hosp.patients`
- source field: `gender`
- source grain: one patient row per `subject_id`
- target grain: one retained row per `subject_id`

Approved normalization:

| Source value | Retained value |
| --- | --- |
| `F` | `female` |
| `M` | `male` |

Unexpected or unclear source values fail review rather than being force-mapped.

## Output Summary

First governed execution output:

- total retained rows: `364,627`
- unique subjects: `364,627`
- female rows: `191,984`
- male rows: `172,643`

## Exclusion Boundary

This approval excludes:

- interpreting the raw MIMIC field name as a broader gender-identity construct
- expanding the patient-level asset to admission or ICU-stay grain without an explicit join rule
- imputing missing values from names, diagnoses, procedures, notes, or downstream phenotype logic

## Approval Rationale

The mapping is narrow, source-authoritative, and patient-grain stable. It establishes the Class 7 governed pattern for demographic/admin/id-map style variables: explicit identifier scope, explicit source authority, explicit normalization, and explicit no-row/no-imputation rule.

## Bottom Line

MIMIC-IV-3.1 is a governed approved database mapping for Class 7 through `std_sex`. The next Class 7 work should use the same pattern for an id map, race/ethnicity, or diagnosis-code event family without mixing those meanings into this sex variable.
