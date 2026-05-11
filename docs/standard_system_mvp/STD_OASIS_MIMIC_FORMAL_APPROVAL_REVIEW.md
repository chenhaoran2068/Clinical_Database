# std_oasis MIMIC Formal Approval Review

Review date: 2026-05-02

Status: reviewed_approved_mimic_governed_class8_lateral_expansion

Database: `MIMIC-IV-3.1`

Standard variable: `std_oasis`

Variable class: `score_phenotype_composite_derived`

## Decision

MIMIC-IV-3.1 is approved for governed same-name `std_oasis`.

The approved meaning is a source-supplied ICU first-day OASIS score summary. The retained primary value is `std_oasis_total` in `score_points`, with same-row official hospital mortality probability and OASIS component subscores retained as context.

This approval does not approve SOFA, SAPSII, mortality phenotype truth, raw score-component event streams, sepsis onset, or recalculation from raw events under this same variable identity.

## Governed Artifacts

Public governed files:

- `docs/standard_system_mvp/std_oasis/variable_spec.json`
- `docs/standard_system_mvp/std_oasis/mapping_spec_mimic_iv_3_1.json`
- `docs/standard_system_mvp/std_oasis/execution.py`
- `Framework_Guideline/StandardVariableClass_ScorePhenotypeCompositeDerived_Contract.md`

Runtime evidence:

- first execution: `docs/standard_system_mvp/std_oasis/runtime/mimic_iv_3_1_first_real_execution/`
- rerun: `docs/standard_system_mvp/std_oasis/runtime/mimic_iv_3_1_rerun_repro_check/`
- reproducibility report: `docs/standard_system_mvp/std_oasis/runtime/mimic_iv_3_1_rerun_repro_check/reproducibility_report.json`

Runtime process batches:

- first execution: `20260502T145031Z_MIMIC-IV-3.1_std_oasis`
- rerun: `20260502T145059Z_MIMIC-IV-3.1_std_oasis`

Reproducibility status: `pass`.

## Approved Source Scope

Approved MIMIC source:

- source table: `source_supplied_derived.oasis`
- supporting table: `icu.icustays`
- official SQL reference: `References/MIMIC/2026-03-20_snapshot_v2/raw/mimic_code/mimic-iv/concepts/score/oasis.sql`
- source value field: `oasis`
- target grain: one retained score summary row per `stay_id`

Approved retained context:

- `std_oasis_hospital_mortality_prob`
- age score
- pre-ICU length-of-stay score
- GCS score
- heart-rate score
- mean blood pressure score
- respiratory-rate score
- temperature score
- urine-output score
- mechanical ventilation score
- elective surgery score

## Output Summary

First governed execution output:

- total retained rows: `94,458`
- unique ICU stays: `94,458`
- primary score minimum: `6.0`
- primary score maximum: `72.0`
- approved canonical score range: `0` to `100` score points

Reviewed local quality evidence also shows:

- hospital mortality probability range: `0.004454` to `0.952817`
- primary score null rows: `0`
- mortality probability null rows: `0`
- selected component subscores can be null while the primary score remains present

## Exclusion Boundary

This approval excludes:

- recalculating OASIS from raw events as if it were the same mapping
- replacing OASIS with SOFA or SAPSII
- interpreting the probability column as observed mortality outcome
- treating no retained row as low risk or zero score
- using OASIS as sepsis, AKI, or respiratory failure phenotype truth

## Approval Rationale

The mapping is narrow enough for Class 8 because it locks a source-supplied composite score, ICU-stay summary grain, first-day score window, primary score value, component trace, probability range, and no-row interpretation. It broadens Class 8 beyond SOFA time series into stay-level score summaries.

## Bottom Line

MIMIC-IV-3.1 is approved for `std_oasis` as the Class 8 lateral expansion beyond SOFA. Future Class 8 score mappings should prove source score identity, time window, retained primary value, and component trace before using the same-name pattern.
